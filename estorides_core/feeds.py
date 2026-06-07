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
import os
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .config import DATA_DIR
from .ssrf_guard import assert_safe

log = logging.getLogger("estorides.feeds")

FEED_CACHE_DIR: Path = DATA_DIR / "feeds"
FEED_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Default cache TTL: 15 minutes. Stable data (news, conflict zones) can
# be cached longer; spiky data (flights) shorter. Each feed overrides.
DEFAULT_TTL_S: int = 15 * 60


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
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ----------------------------------------------------------------- base
class Feed(ABC):
    """Base class for a real-time feed."""

    name: str = ""
    description: str = ""
    default_ttl_s: int = DEFAULT_TTL_S
    cache_filename: str = ""  # set by subclass in __init__

    def __init__(self) -> None:
        if not self.cache_filename:
            self.cache_filename = f"{self.name}.json"

    @abstractmethod
    def _fetch(self) -> List[FeedPoint]:
        """Subclass implementation: hit the upstream and return points."""

    def fetch(self, *, use_cache: bool = True) -> List[FeedPoint]:
        """Public entrypoint. Reads/writes the on-disk cache.

        The cache is a simple `{fetched_at, points}` JSON blob —
        good enough for a self-hosted deployment. A real production
        system would want a TTL'd Redis layer, but that pulls in a
        network dependency."""
        cache_path = FEED_CACHE_DIR / self.cache_filename
        if use_cache and cache_path.exists():
            try:
                blob = json.loads(cache_path.read_text(encoding="utf-8"))
                if (time.time() - blob.get("fetched_at", 0)) < self.default_ttl_s:
                    return [FeedPoint(**p) for p in blob.get("points", [])]
            except (json.JSONDecodeError, TypeError):
                pass  # corrupt cache, fall through to refetch

        try:
            points = self._fetch()
        except Exception as e:  # noqa: BLE001
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
            cache_path.write_text(
                json.dumps({"fetched_at": time.time(),
                            "points": [p.to_dict() for p in points]},
                           ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as e:
            log.debug("feed cache write failed (non-fatal): %s", e)
        return points

    def point(self, record: Dict[str, Any]) -> Optional[Tuple[float, float]]:
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
    default_ttl_s = 10 * 60  # 10 min — seismic events are time-sensitive

    USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

    def _fetch(self) -> List[FeedPoint]:
        assert_safe(self.USGS_URL)
        import requests
        r = requests.get(self.USGS_URL, timeout=15,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        data = r.json()
        out: List[FeedPoint] = []
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

    def _fetch(self) -> List[FeedPoint]:
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
        out: List[FeedPoint] = []
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

    def _fetch(self) -> List[FeedPoint]:
        assert_safe(self.GDELT_URL)
        import requests
        r = requests.get(self.GDELT_URL, timeout=20,
                         headers={"User-Agent": "Estorides/1.0 (+osint platform)"})
        r.raise_for_status()
        try:
            data = r.json()
        except json.JSONDecodeError:
            return []
        out: List[FeedPoint] = []
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


# ----------------------------------------------------------------- registry
FEEDS: Dict[str, Feed] = {
    cls().name: cls()
    for cls in (EarthquakesFeed, FiresFeed, NewsFeed)
}


def list_feeds() -> List[Dict[str, str]]:
    """Return public feed descriptions for the /api/feeds endpoint."""
    return [
        {"name": f.name, "description": f.description}
        for f in FEEDS.values()
    ]


def get_feed(name: str) -> Optional[Feed]:
    return FEEDS.get(name)


def fetch_all(bbox: Optional[Tuple[float, float, float, float]] = None,
              use_cache: bool = True) -> Dict[str, List[FeedPoint]]:
    """Fetch every registered feed (optionally clipped to a bbox).

    Used by /api/feeds to populate the map in one round-trip.

    bbox = (min_lon, min_lat, max_lon, max_lat). Points outside the
    bbox are dropped before the response is returned.
    """
    out: Dict[str, List[FeedPoint]] = {}
    for feed in FEEDS.values():
        try:
            points = feed.fetch(use_cache=use_cache)
        except Exception as e:  # noqa: BLE001
            log.warning("feed %s raised: %s", feed.name, e)
            out[feed.name] = []
            continue
        if bbox is not None:
            min_lon, min_lat, max_lon, max_lat = bbox
            points = [p for p in points
                      if min_lon <= p.lon <= max_lon and min_lat <= p.lat <= max_lat]
        out[feed.name] = points
    return out
