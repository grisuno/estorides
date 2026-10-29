"""
estorides_core.airports
=======================
Public-domain airport reference data and a nearest-airport index.

The dataset is OurAirports (public domain, no key): one CSV row per
aerodrome worldwide with an ICAO/IATA/local identifier, coordinates,
country, region and municipality. Estorides uses it for one question —
*given an aircraft position, which aerodrome is it near?* — which is the
difference between "an unknown contact at 3 000 ft" and "an unknown
contact on approach into Ramstein".

Everything here is deterministic and side-effect free: the download and
the on-disk cache live in :mod:`estorides_core.feeds`. The module keeps
only the parse, the index and the distance maths.

Branding: Estorides, developed by Lazy Own Red Team.
"""
from __future__ import annotations

import csv
import io
import math
from collections.abc import Iterable
from typing import Any

from .aviation import haversine_km

# Aerodrome kinds worth indexing. Heliports, seaplane bases, closed
# fields and balloonports are dropped: they add noise without answering
# "what is this aircraft near?".
DEFAULT_AIRPORT_TYPES: tuple[str, ...] = (
    "large_airport",
    "medium_airport",
    "small_airport",
)

# One degree of latitude is ~111.32 km everywhere; used to stop the
# expanding-ring search, never to compute the distance itself.
KM_PER_DEGREE = 111.32


def _text(value: Any, limit: int = 96) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text[:limit] or None


def _coordinate(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def normalise_airport(row: dict[str, Any]) -> dict[str, Any] | None:
    """Normalise one OurAirports CSV row, or ``None`` when unusable."""
    latitude = _coordinate(row.get("latitude_deg"))
    longitude = _coordinate(row.get("longitude_deg"))
    if latitude is None or longitude is None:
        return None
    if abs(latitude) > 90 or abs(longitude) > 180:
        return None
    ident = _text(row.get("ident"), 16)
    if ident is None:
        return None
    icao = _text(row.get("icao_code"), 8) or _text(row.get("gps_code"), 8)
    iata = _text(row.get("iata_code"), 8)
    return {
        "ident": ident.upper(),
        "icao": icao.upper() if icao else None,
        "iata": iata.upper() if iata else None,
        "name": _text(row.get("name")),
        "type": _text(row.get("type"), 24),
        "latitude": latitude,
        "longitude": longitude,
        "elevation_ft": _coordinate(row.get("elevation_ft")),
        "country": _text(row.get("iso_country"), 8),
        "region": _text(row.get("iso_region"), 16),
        "municipality": _text(row.get("municipality")),
        "scheduled_service": (row.get("scheduled_service") or "").strip().lower()
        in {"yes", "true", "1"},
    }


def parse_airports_csv(
    text: Any,
    *,
    types: Iterable[str] = DEFAULT_AIRPORT_TYPES,
    limit: int = 0,
) -> list[dict[str, Any]]:
    """Parse an OurAirports CSV export into normalised airport dicts.

    Rows with bad coordinates, a missing identifier and rows outside
    ``types`` are dropped. Duplicate identifiers keep the first row so a
    re-export cannot double the index.
    """
    if not isinstance(text, str) or not text.strip():
        return []
    wanted = {value for value in types if isinstance(value, str)}
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    try:
        reader = csv.DictReader(io.StringIO(text))
        for row in reader:
            if not isinstance(row, dict):
                continue
            if wanted and (row.get("type") or "").strip() not in wanted:
                continue
            airport = normalise_airport(row)
            if airport is None or airport["ident"] in seen:
                continue
            seen.add(airport["ident"])
            out.append(airport)
            if limit > 0 and len(out) >= limit:
                break
    except (csv.Error, UnicodeDecodeError):
        return out
    return out


class AirportIndex:
    """Spatial index over normalised airports.

    Buckets airports into one-degree cells so a nearest-airport query
    touches a handful of cells instead of the whole catalogue: the map
    layer asks this for every aircraft in a regional snapshot.
    """

    def __init__(self, airports: Iterable[dict[str, Any]]) -> None:
        self.airports: list[dict[str, Any]] = []
        self._grid: dict[tuple[int, int], list[dict[str, Any]]] = {}
        self._by_code: dict[str, dict[str, Any]] = {}
        for airport in airports:
            if not isinstance(airport, dict):
                continue
            latitude = _coordinate(airport.get("latitude"))
            longitude = _coordinate(airport.get("longitude"))
            if latitude is None or longitude is None:
                continue
            self.airports.append(airport)
            self._grid.setdefault(_cell(latitude, longitude), []).append(airport)
            for key in ("ident", "icao", "iata"):
                code = airport.get(key)
                if isinstance(code, str) and code.strip():
                    self._by_code.setdefault(code.strip().upper(), airport)

    def __len__(self) -> int:
        return len(self.airports)

    def by_code(self, code: Any) -> dict[str, Any] | None:
        """Look an aerodrome up by ICAO, IATA, GPS or local identifier."""
        if not isinstance(code, str):
            return None
        return self._by_code.get(code.strip().upper())

    def nearest(
        self, latitude: Any, longitude: Any, max_km: float = 50.0
    ) -> dict[str, Any] | None:
        """Closest airport within ``max_km``, annotated with ``distance_km``."""
        lat = _coordinate(latitude)
        lon = _coordinate(longitude)
        if lat is None or lon is None or abs(lat) > 90 or abs(lon) > 180:
            return None
        if not isinstance(max_km, (int, float)) or isinstance(max_km, bool):
            return None
        radius = float(max_km)
        if not math.isfinite(radius) or radius <= 0:
            return None
        base = _cell(lat, lon)
        ring_limit = math.ceil(radius / KM_PER_DEGREE) + 1
        best: dict[str, Any] | None = None
        best_km = radius
        for ring in range(ring_limit + 1):
            # A cell on this ring is at least (ring - 1) degrees away, so
            # once that floor exceeds the best distance nothing closer
            # can be hiding further out.
            if ring and (ring - 1) * KM_PER_DEGREE > best_km:
                break
            for cell_lat in range(base[0] - ring, base[0] + ring + 1):
                for cell_lon in range(base[1] - ring, base[1] + ring + 1):
                    if max(abs(cell_lat - base[0]), abs(cell_lon - base[1])) != ring:
                        continue
                    for airport in self._grid.get((cell_lat, cell_lon), ()):
                        distance = haversine_km(
                            lat, lon, airport.get("latitude"), airport.get("longitude")
                        )
                        if distance is None or distance > best_km:
                            continue
                        best, best_km = airport, distance
        if best is None:
            return None
        out = dict(best)
        out["distance_km"] = round(best_km, 3)
        return out

    def within_bbox(self, bbox: Any) -> list[dict[str, Any]]:
        """Airports inside ``(min_lon, min_lat, max_lon, max_lat)``."""
        if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
            return []
        try:
            min_lon, min_lat, max_lon, max_lat = (float(v) for v in bbox)
        except (TypeError, ValueError):
            return []
        return [
            airport for airport in self.airports
            if min_lon <= airport["longitude"] <= max_lon
            and min_lat <= airport["latitude"] <= max_lat
        ]


def _cell(latitude: float, longitude: float) -> tuple[int, int]:
    """One-degree grid cell for a coordinate (``lon`` wraps at the pole)."""
    return math.floor(latitude), math.floor(longitude)


def build_index(airports: Iterable[dict[str, Any]]) -> AirportIndex:
    """Convenience constructor: ``build_index(parse_airports_csv(text))``."""
    return AirportIndex(airports)


def airport_brief(airport: dict[str, Any] | None) -> dict[str, Any] | None:
    """Compact airport view for feed payloads (popup-sized, not exhaustive)."""
    if not isinstance(airport, dict):
        return None
    return {
        "ident": airport.get("ident"),
        "icao": airport.get("icao"),
        "iata": airport.get("iata"),
        "name": airport.get("name"),
        "municipality": airport.get("municipality"),
        "country": airport.get("country"),
        "distance_km": airport.get("distance_km"),
    }
