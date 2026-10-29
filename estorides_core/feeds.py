"""
estorides_core.feeds
====================
Real-time intelligence feeds, polled and cached locally.

This is the "osiris map layers" feature, brought to the Python side:
each feed is a small object that knows how to fetch, parse, and
normalise one external signal (flights, earthquakes, fires, news,
sanctions) into a common GeoPoint shape ready for the map.

Why a separate module instead of just YAML sources?
  * The feeds are polled, not queried. They don't take a user query;
    they take a bounding box or a time window.
  * They produce spatiotemporal data (lat, lon, timestamp) which
    doesn't fit the source-parser model.
  * They have a much higher refresh rate (15-60 min) so we cache
    aggressively to disk and short-circuit on the same minute.

Each feed exposes a uniform API:
  * `name`  — slug used by the API
  * `description` — human-readable one-liner
  * `fetch(bbox=None)` — list[dict] of normalised records
  * `point(record)` — (lat, lon) tuple, or None

Records are plain dicts with at least: {lat, lon, timestamp, label, source}.
"""
from __future__ import annotations

import json
import logging
import math
import os
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .aerospace import (
    DEFAULT_SATELLITE_GROUPS,
    cap_records,
    celestrak_group_url,
    normalize_adsblol_aircraft,
    normalize_launch_library,
    normalize_opensky_states,
    parse_tle_catalog,
    subsatellite_point,
)
from .airports import AirportIndex, airport_brief, build_index, parse_airports_csv
from .aviation import (
    MAX_REGIONAL_RADIUS_NM,
    bbox_center_radius,
    emergency_phrase,
)
from .config import DATA_DIR
from .ssrf_guard import assert_safe

log = logging.getLogger("estorides.feeds")

FEED_CACHE_DIR: Path = DATA_DIR / "feeds"
# Issue #49: directory is created lazily via ensure_feed_cache_dir().
# No side effect at import time.

# Default cache TTL: 15 minutes. Stable data (news, conflict zones) can
# be cached longer; spiky data (flights) shorter. Each feed overrides.
DEFAULT_TTL_S: int = 15 * 60

# A moving map produces one regional cache file per quantised bbox. Keep
# the newest few so a long session cannot fill the disk with them.
BBOX_CACHE_MAX_FILES: int = 50


def _env_int(name: str, default: int) -> int:
    """Read a positive integer from the environment, clamped to >= 0."""
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(0, value)


def _env_float(name: str, default: float) -> float:
    """Read a positive float from the environment, falling back on garbage."""
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if math.isfinite(value) and value > 0 else default


def _env_flag(name: str, default: bool = False) -> bool:
    """Read a boolean flag (``1/true/yes/on``) from the environment."""
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on"}


def _bbox_cache_key(bbox: Any) -> str:
    """Filename-safe cache key for a bbox, quantised to 0.01 degrees.

    Two requests a few hundred metres apart land on the same regional
    cache entry, which is exactly the tolerance a 15 s refresh needs.
    """
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        return ""
    parts: list[str] = []
    for value in bbox:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return ""
        if not math.isfinite(number):
            return ""
        parts.append(f"{number:.2f}".replace("-", "m").replace(".", "_"))
    return "-".join(parts)


# ------------------------------------------------------- airport reference
AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"
AIRPORTS_CACHE_FILE: Path = DATA_DIR / "airports.json"
AIRPORTS_TTL_S: int = 30 * 24 * 60 * 60   # OurAirports changes weekly, not hourly
AIRPORTS_MAX_BYTES: int = 64 * 1024 * 1024

_airport_index: AirportIndex | None = None
_airport_index_lock = threading.Lock()


def airports_enabled() -> bool:
    """True when aircraft records should be annotated with a nearby airport.

    Off by default: enabling it downloads the public-domain OurAirports
    catalogue (~13 MB) once and refreshes it monthly. Set
    ``ESTORIDES_AIRPORTS_ENRICH=1`` to opt in.
    """
    return _env_flag("ESTORIDES_AIRPORTS_ENRICH", False)


def _airport_index_from_disk() -> tuple[AirportIndex | None, float]:
    """Return the cached index and its epoch, or ``(None, 0)``."""
    try:
        blob = json.loads(AIRPORTS_CACHE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, 0.0
    airports = blob.get("airports")
    if not isinstance(airports, list) or not airports:
        return None, 0.0
    fetched_at = blob.get("fetched_at")
    stamp = float(fetched_at) if isinstance(fetched_at, (int, float)) else 0.0
    return build_index(airports), stamp


def _download_airport_catalogue() -> list[dict[str, Any]]:
    """Fetch and parse the OurAirports CSV. Raises on failure."""
    import requests

    url = os.environ.get("ESTORIDES_AIRPORTS_URL", "").strip() or AIRPORTS_URL
    assert_safe(url)
    response = requests.get(
        url,
        timeout=60,
        headers={"User-Agent": "Estorides/1.0 (+osint platform)"},
        stream=True,
    )
    response.raise_for_status()
    chunks: list[bytes] = []
    total = 0
    for chunk in response.iter_content(chunk_size=1 << 20):
        if not chunk:
            continue
        total += len(chunk)
        if total > AIRPORTS_MAX_BYTES:
            raise ValueError("airport catalogue exceeds the configured size cap")
        chunks.append(chunk)
    return parse_airports_csv(b"".join(chunks).decode("utf-8", errors="replace"))


def _load_airport_index() -> AirportIndex | None:
    """Load (and refresh) the airport index. Never raises; ``None`` on failure."""
    global _airport_index
    with _airport_index_lock:
        cached, fetched_at = _airport_index_from_disk()
        fresh = cached is not None and (time.time() - fetched_at) < AIRPORTS_TTL_S
        if fresh:
            _airport_index = cached
            return _airport_index
        if _airport_index is not None and cached is None:
            return _airport_index
        try:
            airports = _download_airport_catalogue()
        except Exception as e:  # the layer must survive a bad download
            log.warning("airport catalogue unavailable: %s", e)
            _airport_index = cached or _airport_index
            return _airport_index
        if not airports:
            _airport_index = cached or _airport_index
            return _airport_index
        try:
            AIRPORTS_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            AIRPORTS_CACHE_FILE.write_text(
                json.dumps({"fetched_at": time.time(), "airports": airports},
                           ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as e:
            log.debug("airport cache write failed (non-fatal): %s", e)
        _airport_index = build_index(airports)
        return _airport_index


def _annotate_airports(points: list[FeedPoint]) -> list[FeedPoint]:
    """Attach the nearest aerodrome to each point, when the feature is on."""
    if not points or not airports_enabled():
        return points
    index = _load_airport_index()
    if index is None or not len(index):
        return points
    radius_km = _env_float("ESTORIDES_AIRPORTS_RADIUS_KM", 25.0)
    for point in points:
        nearest = index.nearest(point.lat, point.lon, max_km=radius_km)
        brief = airport_brief(nearest)
        if brief is not None:
            point.extra["nearest_airport"] = brief
    return points


# ---------------------------------------------------------------- shape
@dataclass
class FeedPoint:
    """Normalised point for the map layer.

    `kind` discriminates the marker on the map (flight / quake / fire /
    news / vessel). `extra` is an open dict for source-specific fields
    the frontend may want to render in the popup.
    """
    lat: float
    lon: float
    timestamp: float
    label: str
    source: str
    kind: str
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ----------------------------------------------------------------- base
class Feed(ABC):
    """Base class for a real-time feed."""

    name: str = ""
    description: str = ""
    # Required upstream credit. Rendered by the map layer panel and
    # returned by GET /api/feeds. Empty means "no attribution required".
    attribution: str = ""
    default_ttl_s: int = DEFAULT_TTL_S
    # Some feeds are cheap in a region and expensive worldwide; they
    # override this to refresh a bbox answer faster than the global one.
    bbox_ttl_s: int = 0
    cache_filename: str = ""  # set by subclass in __init__

    def __init__(self) -> None:
        if not self.cache_filename:
            self.cache_filename = f"{self.name}.json"

    @abstractmethod
    def _fetch(self) -> list[FeedPoint]:
        """Subclass implementation: hit the upstream and return points."""

    def _fetch_bbox(
        self, bbox: tuple[float, float, float, float]
    ) -> list[FeedPoint] | None:
        """Regional override for a bounding box.

        Returning ``None`` means "this feed has no regional form"; the
        caller then runs the worldwide :meth:`_fetch` and clips the
        result. A feed that can answer a box directly (denser, cheaper and
        inside the upstream's own limits) overrides this.
        """
        return None

    def _answers_regionally(self) -> bool:
        """True when this feed overrides :meth:`_fetch_bbox`."""
        return type(self)._fetch_bbox is not Feed._fetch_bbox

    def cache_path(
        self, bbox: tuple[float, float, float, float] | None = None
    ) -> Path:
        """On-disk cache path, namespaced by bbox when one is supplied.

        A feed that cannot answer a box regionally keeps one global cache
        file even when the caller passes a bbox: its answer is the world,
        clipped afterwards, so keying it by box would refetch the same
        world once per viewport.
        """
        key = _bbox_cache_key(bbox) if self._answers_regionally() else ""
        stem = f"{self.name}-{key}" if key else self.name
        return FEED_CACHE_DIR / f"{stem}.json"

    def _prune_bbox_cache(self, keep: Path) -> None:
        """Keep the newest ``BBOX_CACHE_MAX_FILES`` regional cache files."""
        try:
            siblings = sorted(
                (path for path in FEED_CACHE_DIR.glob(f"{self.name}-*.json")
                 if path != keep),
                key=lambda path: path.stat().st_mtime,
            )
        except OSError:
            return
        excess = len(siblings) - max(0, BBOX_CACHE_MAX_FILES - 1)
        for path in siblings[:max(0, excess)]:
            try:
                path.unlink()
            except OSError:
                continue

    def fetch(
        self,
        *,
        use_cache: bool = True,
        bbox: tuple[float, float, float, float] | None = None,
    ) -> list[FeedPoint]:
        """Public entrypoint. Reads/writes the on-disk cache.

        The cache is a simple `{fetched_at, points}` JSON blob — good
        enough for a self-hosted deployment. A real production system
        would want a TTL'd Redis layer, but that pulls in a network
        dependency.

        A ``bbox`` asks for a regional answer: the feed may serve it from
        its upstream's own regional endpoint and caches it under a
        bbox-specific key, so a wide and a narrow request never poison
        each other.
        """
        cache_path = self.cache_path(bbox)
        regional = bbox is not None and self._answers_regionally()
        ttl = self.bbox_ttl_s if regional and self.bbox_ttl_s else self.default_ttl_s
        if use_cache and cache_path.exists():
            try:
                blob = json.loads(cache_path.read_text(encoding="utf-8"))
                if (time.time() - blob.get("fetched_at", 0)) < ttl:
                    return [FeedPoint(**p) for p in blob.get("points", [])]
            except (json.JSONDecodeError, TypeError):
                pass  # corrupt cache, fall through to refetch

        try:
            points = self._fetch_bbox(bbox) if regional else None
            if points is None:
                points = self._fetch()
        except Exception as e:
            log.warning("feed %s fetch failed: %s", self.name, e)
            # Serve stale cache rather than nothing, but only if it
            # exists and is less than 6 hours old.
            if cache_path.exists():
                try:
                    blob = json.loads(cache_path.read_text(encoding="utf-8"))
                    if (time.time() - blob.get("fetched_at", 0)) < 6 * 3600:
                        log.info("serving stale cache for feed %s", self.name)
                        return [FeedPoint(**p) for p in blob.get("points", [])]
                except (json.JSONDecodeError, TypeError):
                    pass
            return []
        try:
            # Lazy directory creation (issue #49): mkdir only when
            # we're actually about to write the cache, not at import.
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(
                json.dumps({"fetched_at": time.time(),
                            "points": [p.to_dict() for p in points]},
                           ensure_ascii=False),
                encoding="utf-8",
            )
            if bbox is not None:
                self._prune_bbox_cache(cache_path)
        except OSError as e:
            log.debug("feed cache write failed (non-fatal): %s", e)
        return points

    def point(self, record: dict[str, Any]) -> tuple[float, float] | None:
        """Default: return (lat, lon) if both present."""
        lat = record.get("lat")
        lon = record.get("lon")
        if lat is None or lon is None:
            return None
        try:
            return float(lat), float(lon)
        except (TypeError, ValueError):
            return None


# ---------------------------------------------------------------- USGS earthquakes
class EarthquakesFeed(Feed):
    """USGS M2.5+ earthquakes, last 24h, worldwide."""
    name = "earthquakes"
    description = "USGS M2.5+ earthquakes (last 24h)"
    attribution = "USGS earthquake hazards program (public domain)"
    default_ttl_s = 10 * 60  # 10 min — seismic events are time-sensitive

    USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

    def _fetch(self) -> list[FeedPoint]:
        assert_safe(self.USGS_URL)
        import requests
        r = requests.get(self.USGS_URL, timeout=15,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        data = r.json()
        out: list[FeedPoint] = []
        for feat in data.get("features", []):
            geom = feat.get("geometry") or {}
            coords = geom.get("coordinates") or [None, None, None]
            props = feat.get("properties") or {}
            lon, lat, depth = (coords + [None, None, None])[:3]
            if lat is None or lon is None:
                continue
            out.append(FeedPoint(
                lat=float(lat),
                lon=float(lon),
                timestamp=float(geom.get("time", 0)) / 1000.0,
                label=f"M{props.get('mag'):.1f} — {props.get('place', '?')}" if props.get("mag") is not None else props.get("place", "?"),
                source="usgs",
                kind="quake",
                extra={
                    "magnitude": props.get("mag"),
                    "depth_km": depth,
                    "url": props.get("url"),
                    "tsunami": bool(props.get("tsunami", 0)),
                    "felt": props.get("felt"),
                },
            ))
        return out


# ---------------------------------------------------------------- NASA FIRMS fires
class FiresFeed(Feed):
    """NASA FIRMS active fire hotspots (VIIRS_NOAA20_NRT, last 24h).

    FIRMS retired its keyless CSV download in 2024. The new endpoint
    at `api/data/active_fire/csv/...` requires a MAP_KEY (free with
    NASA Earthdata registration) which is read from the
    `ESTORIDES_FIRMS_KEY` env var. If the key is missing the feed
    silently returns zero points and logs a warning — it never
    breaks the rest of the platform.
    """
    name = "fires"
    description = "NASA FIRMS active fire hotspots (VIIRS_NOAA20_NRT, last 24h)"
    default_ttl_s = 30 * 60  # 30 min — thermal anomalies don't move fast

    FIRMS_URL = (
        "https://firms.modaps.eosdis.nasa.gov/api/data/active_fire/csv/"
        "VIIRS_NOAA20_NRT/world/24h.csv"
    )

    def _fetch(self) -> list[FeedPoint]:
        api_key = os.environ.get("ESTORIDES_FIRMS_KEY", "").strip()
        if not api_key:
            log.info("FIRMS key not set (ESTORIDES_FIRMS_KEY), skipping fire feed")
            return []
        url = f"{self.FIRMS_URL}?MAP_KEY={api_key}"
        assert_safe(url)
        import csv
        import io

        import requests
        r = requests.get(url, timeout=30,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        reader = csv.DictReader(io.StringIO(r.text))
        out: list[FeedPoint] = []
        for row in reader:
            lat_raw = row.get("latitude")
            lon_raw = row.get("longitude")
            if lat_raw is None or lon_raw is None:
                continue
            try:
                lat = float(lat_raw)
                lon = float(lon_raw)
            except (TypeError, ValueError):
                continue
            out.append(FeedPoint(
                lat=lat,
                lon=lon,
                timestamp=time.time(),  # FIRMS doesn't give per-row ts in CSV
                label=f"Fire — {row.get('confidence', '?')}% confidence",
                source="nasa_firms",
                kind="fire",
                extra={
                    "confidence": row.get("confidence"),
                    "brightness": row.get("bright_ti4"),
                    "satellite": row.get("satellite"),
                },
            ))
        return out


# ---------------------------------------------------------------- GDELT news geolocated
class NewsFeed(Feed):
    """GDELT 2.0 — global news articles (article-list API).

    The GeoJSON endpoint we used in the previous version was retired.
    The current keyless endpoint is the article-list API at
    `/api/v2/doc/doc` which returns a JSON `articles` array. We
    attempt to geocode the article URL via the embedded
    `socialimage` or `domain` field when coordinates aren't in the
    payload — falling back to the article's source domain
    coordinates is intentionally out of scope for this version, so
    a record without explicit coordinates is dropped."""
    name = "news"
    description = "GDELT 2.0 global news articles (last 15 min)"
    default_ttl_s = 15 * 60

    GDELT_URL = (
        "https://api.gdeltproject.org/api/v2/doc/doc?query=*"
        "&mode=artlist&maxrecords=250&format=json"
    )

    def _fetch(self) -> list[FeedPoint]:
        assert_safe(self.GDELT_URL)
        import requests
        r = requests.get(self.GDELT_URL, timeout=20,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        try:
            data = r.json()
        except json.JSONDecodeError:
            return []
        out: list[FeedPoint] = []
        for art in data.get("articles", []) or []:
            # GDELT article-list doesn't carry coordinates. We still
            # surface the article as a feed point at (0, 0) so the
            # map can show the "global news activity" layer; the
            # frontend treats 0,0 specially. A future version will
            # geocode the article URL against a domain→country
            # table to give each news dot a real position.
            title = art.get("title", "?")[:200]
            out.append(FeedPoint(
                lat=0.0,
                lon=0.0,
                timestamp=time.time(),
                label=title,
                source="gdelt",
                kind="news",
                extra={
                    "url": art.get("url"),
                    "domain": art.get("domain"),
                    "language": art.get("language"),
                },
            ))
        return out


# ---------------------------------------------------------------- OpenSky aircraft
def _aircraft_feed_point(
    record: dict[str, Any], *, kind: str, source: str
) -> FeedPoint:
    """One map point from a common aircraft record.

    The extra dict is what the popup renders, so it carries identity
    (type, registration, owner), kinematics, the transponder state and the
    community flags. Empty values are dropped to keep /api/feeds small;
    ``False`` survives because "not on the ground" is information.
    """
    extra: dict[str, Any] = {
        "icao24": record.get("icao24"),
        "callsign": record.get("callsign"),
        "country": record.get("origin_country"),
        "altitude_m": record.get("baro_altitude_m"),
        "geo_altitude_m": record.get("geo_altitude_m"),
        "speed_mps": record.get("velocity_mps"),
        "heading_deg": record.get("heading_deg"),
        "vertical_rate_mps": record.get("vertical_rate_mps"),
        "on_ground": bool(record.get("on_ground")),
        "category": record.get("category"),
        "aircraft_class": record.get("aircraft_class"),
        "type_code": record.get("type_code"),
        "registration": record.get("registration"),
        "owner": record.get("owner"),
        "description": record.get("description"),
        "squawk": record.get("squawk"),
    }
    emergency = record.get("emergency")
    if isinstance(emergency, dict):
        extra["emergency"] = emergency
        phrase = emergency_phrase(emergency)
        if phrase:
            extra["emergency_phrase"] = phrase
    flags = record.get("db_flags")
    if isinstance(flags, dict):
        extra["flags"] = flags
    integrity = record.get("navigation_integrity")
    if isinstance(integrity, dict) and integrity.get("level") not in (None, "unknown"):
        extra["navigation_integrity"] = integrity
    extra = {key: value for key, value in extra.items() if value is not None}
    return FeedPoint(
        lat=record["latitude"],
        lon=record["longitude"],
        timestamp=record["observed_at"] or time.time(),
        label=record["callsign"] or record["icao24"],
        source=source,
        kind=kind,
        extra=extra,
    )


class AircraftFeed(Feed):
    """Aircraft in the air, from the cheapest keyless source for the ask.

    Without a bbox the feed takes the OpenSky worldwide snapshot (the
    anonymous tier is rate-limited; the 5-minute cache keeps the platform
    inside the published research/education budget). With a bbox it asks
    adsb.lol for that exact region: community receivers are denser than
    OpenSky locally, the regional query costs no credits, and 250 nm is
    the upstream's own radius limit — beyond it the worldwide snapshot is
    the better answer.
    """
    name = "aircraft"
    description = "Live aircraft (OpenSky worldwide, adsb.lol for a region)"
    attribution = (
        "OpenSky Network (research/education terms); "
        "adsb.lol contributors (ODbL 1.0)"
    )
    default_ttl_s = 5 * 60
    bbox_ttl_s = 60          # a regional snapshot refreshes every minute

    STATES_URL = "https://opensky-network.org/api/states/all?extended=1"
    POINT_URL = "https://api.adsb.lol/v2/point/{lat:.4f}/{lon:.4f}/{radius}"

    def _limit(self) -> int:
        return _env_int("ESTORIDES_AIRCRAFT_MAX", 3000)

    def _fetch(self) -> list[FeedPoint]:
        assert_safe(self.STATES_URL)
        import requests
        r = requests.get(self.STATES_URL, timeout=20,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        records = cap_records(normalize_opensky_states(r.json()), self._limit())
        points = [
            _aircraft_feed_point(record, kind="aircraft", source="opensky")
            for record in records
        ]
        return _annotate_airports(points)

    def _fetch_bbox(
        self, bbox: tuple[float, float, float, float]
    ) -> list[FeedPoint] | None:
        if not _env_flag("ESTORIDES_AIRCRAFT_REGIONAL", True):
            return None
        geometry = bbox_center_radius(bbox)
        if geometry is None:
            return None
        latitude, longitude, radius_nm = geometry
        if radius_nm > MAX_REGIONAL_RADIUS_NM:
            return None
        radius = math.ceil(radius_nm)
        radius = max(1, min(radius, int(MAX_REGIONAL_RADIUS_NM)))
        url = self.POINT_URL.format(lat=latitude, lon=longitude, radius=radius)
        assert_safe(url)
        import requests
        r = requests.get(url, timeout=20,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        records = cap_records(normalize_adsblol_aircraft(r.json()), self._limit())
        points = [
            _aircraft_feed_point(record, kind="aircraft", source="adsb.lol")
            for record in records
        ]
        return _annotate_airports(points)


# ---------------------------------------------------------------- adsb.lol military
class MilitaryAircraftFeed(Feed):
    """Military aircraft currently broadcasting ADS-B (adsb.lol, ODbL).

    adsb.lol is a community network; the military feed is a small,
    keyless subset that is useful for pattern-of-life work. The
    attribution is required by ODbL.
    """
    name = "military_aircraft"
    description = "adsb.lol military aircraft snapshot (ODbL)"
    attribution = "adsb.lol contributors (ODbL 1.0)"
    default_ttl_s = 2 * 60

    MIL_URL = "https://api.adsb.lol/v2/mil"

    def _fetch(self) -> list[FeedPoint]:
        assert_safe(self.MIL_URL)
        import requests
        r = requests.get(self.MIL_URL, timeout=20,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        limit = _env_int("ESTORIDES_AIRCRAFT_MAX", 3000)
        records = cap_records(normalize_adsblol_aircraft(r.json()), limit)
        points = [
            _aircraft_feed_point(record, kind="military_aircraft", source="adsb.lol")
            for record in records
        ]
        return _annotate_airports(points)


# ------------------------------------------------------- adsb.lol emergencies
class AircraftEmergencyFeed(Feed):
    """Aircraft currently broadcasting an emergency squawk (adsb.lol, ODbL).

    Three ICAO Mode A codes are polled — 7500 unlawful interference,
    7600 radio failure, 7700 general emergency — plus the ADS-B
    emergency/priority field, which is a superset. A code is what the
    transponder broadcast in this poll, never a finding: crews pass
    through 7x00 codes while dialling. One-minute cache, because this is
    the most time-sensitive layer in the set.
    """
    name = "aircraft_emergency"
    description = "Aircraft broadcasting an emergency squawk (adsb.lol, ODbL)"
    attribution = "adsb.lol contributors (ODbL 1.0)"
    default_ttl_s = 60

    SQUAWKS: tuple[str, ...] = ("7500", "7600", "7700")
    SQUAWK_URL = "https://api.adsb.lol/v2/squawk/{squawk}"

    def _fetch(self) -> list[FeedPoint]:
        import requests
        limit = _env_int("ESTORIDES_EMERGENCY_MAX", 200)
        out: list[FeedPoint] = []
        seen: set[str] = set()
        for squawk in self.SQUAWKS:
            if len(out) >= limit:
                break
            url = self.SQUAWK_URL.format(squawk=squawk)
            assert_safe(url)
            try:
                r = requests.get(
                    url, timeout=15,
                    headers={"User-Agent": "Estorides/1.0 (+osint platform)"},
                )
                r.raise_for_status()
            except Exception as e:  # one code down must not kill the layer
                log.warning("adsb.lol squawk %s failed: %s", squawk, e)
                continue
            for record in cap_records(normalize_adsblol_aircraft(r.json()), limit):
                if record["icao24"] in seen:
                    continue
                seen.add(record["icao24"])
                out.append(
                    _aircraft_feed_point(
                        record, kind="aircraft_emergency", source="adsb.lol"
                    )
                )
        return out


# ---------------------------------------------------------------- CelesTrak satellites
class SatellitesFeed(Feed):
    """Satellites in orbit, propagated from CelesTrak TLEs to now.

    Six keyless CelesTrak groups are fetched (stations, visual, GPS,
    GLONASS, Galileo, GEO) and each TLE is propagated to the current
    instant. SGP4 is used when the optional ``sgp4`` package is
    installed; a two-body fallback keeps the layer working otherwise.
    """
    name = "satellites"
    description = "CelesTrak satellites (stations, navigation, GEO)"
    attribution = "CelesTrak GP data (citation requested)"
    default_ttl_s = 10 * 60

    def _groups(self) -> list[str]:
        raw = os.environ.get("ESTORIDES_SATELLITES_GROUPS", "").strip()
        if not raw:
            return list(DEFAULT_SATELLITE_GROUPS)
        groups = [item.strip() for item in raw.split(",") if item.strip()]
        return groups or list(DEFAULT_SATELLITE_GROUPS)

    def _fetch(self) -> list[FeedPoint]:
        import requests
        limit = _env_int("ESTORIDES_SATELLITES_MAX", 1200)
        now = time.time()
        seen: set[int] = set()
        out: list[FeedPoint] = []
        for group in self._groups():
            if len(out) >= limit:
                break
            url = celestrak_group_url(group)
            assert_safe(url)
            try:
                r = requests.get(
                    url,
                    timeout=15,
                    headers={"User-Agent": "Estorides/1.0 (+osint platform)"},
                )
                r.raise_for_status()
            except Exception as e:
                log.warning("celestrak group %s failed: %s", group, e)
                continue
            for satellite in parse_tle_catalog({"raw_text": r.text}):
                norad_id = satellite["norad_id"]
                if norad_id in seen:
                    continue
                point = subsatellite_point(
                    satellite["line1"], satellite["line2"], now
                )
                if point is None:
                    continue
                seen.add(norad_id)
                out.append(FeedPoint(
                    lat=point["latitude"],
                    lon=point["longitude"],
                    timestamp=now,
                    label=satellite["name"],
                    source="celestrak",
                    kind="satellite",
                    extra={
                        "norad_id": norad_id,
                        "group": group,
                        "altitude_km": point["altitude_km"],
                        "velocity_kms": point["velocity_kms"],
                        "propagator": point["propagator"],
                    },
                ))
                if len(out) >= limit:
                    break
        return out


# ------------------------------------------------------------- Launch Library 2
class RocketLaunchesFeed(Feed):
    """Recent and upcoming orbital launches with pad coordinates.

    Launch Library 2 is keyless on the free tier. Only launches with
    pad coordinates become map points; the rest stay visible in the
    source result for schedule work.
    """
    name = "rocket_launches"
    description = "Launch Library 2 recent and upcoming launches"
    attribution = "Launch Library 2 (thespacedevs.com)"
    default_ttl_s = 60 * 60

    LAUNCHES_URL = "https://ll.thespacedevs.com/2.3.0/launches/"

    def _fetch(self) -> list[FeedPoint]:
        from datetime import datetime, timedelta, timezone
        assert_safe(self.LAUNCHES_URL)
        now = datetime.now(timezone.utc)
        params = {
            "net__gte": (now - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "net__lte": (now + timedelta(days=45)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "limit": str(min(_env_int("ESTORIDES_LAUNCHES_MAX", 100), 100)),
            "mode": "detailed",
        }
        import requests
        r = requests.get(
            self.LAUNCHES_URL,
            params=params,
            timeout=20,
            headers={"User-Agent": "Estorides/1.0 (+osint platform)"},
        )
        r.raise_for_status()
        out: list[FeedPoint] = []
        for launch in normalize_launch_library(r.json()):
            if launch["latitude"] is None or launch["longitude"] is None:
                continue
            label = launch["name"] or launch["id"] or "launch"
            out.append(FeedPoint(
                lat=launch["latitude"],
                lon=launch["longitude"],
                timestamp=time.time(),
                label=label,
                source="launch_library_2",
                kind="launch",
                extra={
                    "id": launch["id"],
                    "net": launch["net"],
                    "status": launch["status"],
                    "provider": launch["provider"],
                    "rocket": launch["rocket"],
                    "pad": launch["pad"],
                    "location": launch["location"],
                    "mission": launch["mission"],
                    "orbit": launch["orbit"],
                },
            ))
        return out


# ----------------------------------------------------------------- registry
FEEDS: dict[str, Feed] = {
    cls().name: cls()
    for cls in (
        EarthquakesFeed,
        FiresFeed,
        NewsFeed,
        AircraftFeed,
        MilitaryAircraftFeed,
        AircraftEmergencyFeed,
        SatellitesFeed,
        RocketLaunchesFeed,
    )
}


def list_feeds() -> list[dict[str, str]]:
    """Return public feed descriptions for the /api/feeds endpoint."""
    return [
        {
            "name": f.name,
            "description": f.description,
            "attribution": f.attribution,
        }
        for f in FEEDS.values()
    ]


def get_feed(name: str) -> Feed | None:
    return FEEDS.get(name)


def fetch_all(bbox: tuple[float, float, float, float] | None = None,
              use_cache: bool = True,
              names: list[str] | None = None) -> dict[str, list[FeedPoint]]:
    """Fetch every registered feed (optionally clipped to a bbox).

    Used by /api/feeds to populate the map in one round-trip.

    bbox = (min_lon, min_lat, max_lon, max_lat). Points outside the
    bbox are dropped before the response is returned.

    `names` narrows the fan-out to the listed feed slugs. Unknown names
    are ignored here; the HTTP layer validates them so a caller gets a
    clear 400 instead of a silently empty layer.
    """
    out: dict[str, list[FeedPoint]] = {}
    wanted = set(names) if names else None
    for feed in FEEDS.values():
        if wanted is not None and feed.name not in wanted:
            continue
        try:
            points = feed.fetch(use_cache=use_cache, bbox=bbox)
        except Exception as e:
            log.warning("feed %s raised: %s", feed.name, e)
            out[feed.name] = []
            continue
        if bbox is not None:
            min_lon, min_lat, max_lon, max_lat = bbox
            points = [p for p in points
                      if min_lon <= p.lon <= max_lon and min_lat <= p.lat <= max_lat]
        out[feed.name] = points
    return out
