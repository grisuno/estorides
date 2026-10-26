"""
estorides_core.aerospace
========================
Pure normalisers and orbital helpers for the free air-and-space
intelligence layer set.

Everything in this module is deterministic and side-effect free: no
network, no filesystem, no environment. The feeds in
:mod:`estorides_core.feeds` own the transport; this module owns the
math and the mapping from upstream payloads to Estorides records.

Upstreams supported (all keyless):

  * CelesTrak GP (TLE catalog)
  * OpenSky Network state vectors and tracks
  * adsb.lol v2 aircraft snapshots
  * adsbdb aircraft / callsign enrichment
  * Launch Library 2 launches

Branding: Estorides, developed by Lazy Own Red Team.
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from typing import Any

EARTH_RADIUS_KM = 6378.137
EARTH_MU_KM3_S2 = 398600.4418
KNOT_TO_MPS = 0.514444
FOOT_TO_M = 0.3048
FPM_TO_MPS = 0.00508

# CelesTrak groups loaded by default for the map layer. Order matters
# only for documentation; the feed deduplicates by NORAD id.
DEFAULT_SATELLITE_GROUPS: tuple[str, ...] = (
    "stations",
    "visual",
    "gps-ops",
    "glo-ops",
    "galileo",
    "geo",
)

_CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php"


def celestrak_group_url(group: str) -> str:
    """Return the CelesTrak TLE URL for one catalog group."""
    return f"{_CELESTRAK_URL}?GROUP={group}&FORMAT=tle"


# --------------------------------------------------------------- primitives
def _finite(value: Any) -> float | None:
    """Return ``value`` as a finite float, or ``None``.

    Booleans are rejected on purpose: ``True`` is not an altitude.
    """
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _valid_coordinates(latitude: Any, longitude: Any) -> tuple[float, float] | None:
    lat = _finite(latitude)
    lon = _finite(longitude)
    if lat is None or lon is None:
        return None
    if abs(lat) > 90.0 or abs(lon) > 180.0:
        return None
    return lat, lon


def _clean(value: Any, limit: int = 64) -> str | None:
    """Normalise a text field: trimmed, bounded, ``None`` when empty."""
    text = _text(value)
    return text[:limit] or None


def _as_dict(value: Any) -> dict[str, Any]:
    """Return ``value`` when it is a dict, else an empty dict."""
    return value if isinstance(value, dict) else {}


# ------------------------------------------------------------ TLE catalog
_ALPHA5 = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # I and O are not used by Alpha-5


def _digits(value: str) -> bool:
    """True only for ASCII digits (``str.isdigit`` accepts superscripts)."""
    return value.isascii() and value.isdigit()


def decode_catalog_field(field: Any) -> int | None:
    """Decode a TLE catalog field, including the Alpha-5 spelling.

    Plain digits decode directly. Alpha-5 uses one letter for the
    ten-thousands digit (A=10 .. Z=33, skipping I and O) followed by
    exactly four digits, so ``A0000`` is 100000 and ``Z9999`` is
    339999. Anything else is ``None``.
    """
    text = _text(field)
    if not text:
        return None
    if _digits(text):
        return int(text)
    if len(text) != 5:
        return None
    letter = text[0]
    if letter not in _ALPHA5:
        return None
    if not _digits(text[1:]):
        return None
    tens = _ALPHA5.index(letter) + 10
    return tens * 10000 + int(text[1:])


def tle_catalog_number(line: Any) -> int | None:
    """Return the NORAD catalog number from TLE line 1 or line 2."""
    text = _text(line)
    if len(text) < 7:
        return None
    return decode_catalog_field(text[2:7].strip())


def _text_payload(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        return _text(payload.get("raw_text"))
    return ""


def parse_tle_catalog(payload: Any) -> list[dict[str, Any]]:
    """Parse three-line TLE text into ``{name, norad_id, line1, line2}``.

    Malformed sets are skipped without dropping the valid sets that
    follow them. Duplicate NORAD ids keep the first entry so a
    satellite that appears in several CelesTrak groups is propagated
    once.
    """
    text = _text_payload(payload)
    if not text:
        return []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    out: list[dict[str, Any]] = []
    seen: set[int] = set()
    cursor = 0
    # A bounded for-loop (instead of a while) guarantees progress even
    # when a malformed set repeats, so hostile input cannot spin.
    for index in range(0, len(lines) - 2):
        if index < cursor:
            continue
        name, line1, line2 = lines[index], lines[index + 1], lines[index + 2]
        catalog1 = tle_catalog_number(line1)
        catalog2 = tle_catalog_number(line2)
        if (
            line1.startswith("1 ")
            and line2.startswith("2 ")
            and catalog1 is not None
            and catalog1 == catalog2
        ):
            if catalog1 not in seen:
                seen.add(catalog1)
                out.append({
                    "name": name,
                    "norad_id": catalog1,
                    "line1": line1,
                    "line2": line2,
                })
            cursor = index + 3
        else:
            cursor = index + 1
    return out


def tle_epoch_unix(line1: Any) -> float | None:
    """Return the TLE epoch as Unix seconds, or ``None``."""
    text = _text(line1)
    if len(text) < 32 or not text.startswith("1 "):
        return None
    raw_year = text[18:20]
    raw_day = text[20:32].strip()
    if not _digits(raw_year):
        return None
    try:
        day = float(raw_day)
    except ValueError:
        return None
    if not math.isfinite(day) or day < 1.0 or day > 367.0:
        return None
    year = 2000 + int(raw_year) if int(raw_year) < 57 else 1900 + int(raw_year)
    epoch = datetime(year, 1, 1, tzinfo=timezone.utc) + timedelta(days=day - 1.0)
    return epoch.timestamp()


def tle_mean_elements(line1: Any, line2: Any) -> dict[str, float] | None:
    """Extract the mean orbital elements needed for propagation."""
    text1 = _text(line1)
    text2 = _text(line2)
    epoch = tle_epoch_unix(text1)
    if epoch is None or len(text2) < 63 or not text2.startswith("2 "):
        return None
    inclination = _finite(text2[8:16])
    raan = _finite(text2[17:25])
    eccentricity = _finite("0." + text2[26:33].strip())
    arg_perigee = _finite(text2[34:42])
    mean_anomaly = _finite(text2[43:51])
    mean_motion = _finite(text2[52:63])
    values = (inclination, raan, eccentricity, arg_perigee, mean_anomaly, mean_motion)
    if any(value is None for value in values):
        return None
    if inclination is None or raan is None or eccentricity is None:
        return None
    if arg_perigee is None or mean_anomaly is None or mean_motion is None:
        return None
    if mean_motion <= 0 or not 0.0 <= eccentricity < 1.0:
        return None
    return {
        "epoch_unix": epoch,
        "inclination_deg": inclination,
        "raan_deg": raan,
        "eccentricity": eccentricity,
        "arg_perigee_deg": arg_perigee,
        "mean_anomaly_deg": mean_anomaly,
        "mean_motion_rev_day": mean_motion,
    }


def gmst_deg(when_unix: float) -> float:
    """Greenwich mean sidereal time in degrees for a Unix instant."""
    julian_date = when_unix / 86400.0 + 2440587.5
    days = julian_date - 2451545.0
    centuries = days / 36525.0
    angle = (
        280.46061837
        + 360.98564736629 * days
        + 0.000387933 * centuries * centuries
        - (centuries ** 3) / 38710000.0
    )
    return angle % 360.0


def eci_to_geodetic(position_km: Any, when_unix: Any) -> dict[str, float] | None:
    """Convert an ECI/TEME position in km to latitude, longitude, altitude.

    The altitude uses a spherical Earth; it is a map-display value, not
    a geodetic height above the WGS84 ellipsoid.
    """
    when = _finite(when_unix)
    if when is None or not isinstance(position_km, (list, tuple)) or len(position_km) < 3:
        return None
    x = _finite(position_km[0])
    y = _finite(position_km[1])
    z = _finite(position_km[2])
    if x is None or y is None or z is None:
        return None
    radius = math.sqrt(x * x + y * y + z * z)
    if radius <= 0.0:
        return None
    latitude = math.degrees(math.asin(max(-1.0, min(1.0, z / radius))))
    longitude = math.degrees(math.atan2(y, x)) - gmst_deg(when)
    longitude = (longitude + 180.0) % 360.0 - 180.0
    return {
        "latitude": latitude,
        "longitude": longitude,
        "altitude_km": radius - EARTH_RADIUS_KM,
    }

def kepler_subsatellite_point(
    line1: Any, line2: Any, when_unix: Any
) -> dict[str, Any] | None:
    """Two-body sub-satellite point from TLE mean elements.

    This ignores J2 and drag; it exists so the feature works without the
    optional ``sgp4`` package. Near the TLE epoch it is accurate enough
    for a 2D map marker.
    """
    elements = tle_mean_elements(line1, line2)
    when = _finite(when_unix)
    if elements is None or when is None:
        return None
    elapsed = when - elements["epoch_unix"]
    mean_motion = elements["mean_motion_rev_day"] * 2.0 * math.pi / 86400.0
    semi_major = (EARTH_MU_KM3_S2 / (mean_motion * mean_motion)) ** (1.0 / 3.0)
    eccentricity = elements["eccentricity"]
    mean_anomaly = math.radians(elements["mean_anomaly_deg"]) + mean_motion * elapsed
    mean_anomaly %= 2.0 * math.pi
    eccentric_anomaly = mean_anomaly
    for _ in range(12):
        delta = (
            eccentric_anomaly
            - eccentricity * math.sin(eccentric_anomaly)
            - mean_anomaly
        ) / (1.0 - eccentricity * math.cos(eccentric_anomaly))
        eccentric_anomaly -= delta
        if abs(delta) < 1e-10:
            break
    true_anomaly = math.atan2(
        math.sqrt(max(0.0, 1.0 - eccentricity * eccentricity))
        * math.sin(eccentric_anomaly),
        math.cos(eccentric_anomaly) - eccentricity,
    )
    radius = semi_major * (1.0 - eccentricity * math.cos(eccentric_anomaly))
    argument_of_latitude = math.radians(elements["arg_perigee_deg"]) + true_anomaly
    inclination = math.radians(elements["inclination_deg"])
    raan = math.radians(elements["raan_deg"])
    cos_u = math.cos(argument_of_latitude)
    sin_u = math.sin(argument_of_latitude)
    cos_i = math.cos(inclination)
    position = (
        radius * (math.cos(raan) * cos_u - math.sin(raan) * sin_u * cos_i),
        radius * (math.sin(raan) * cos_u + math.cos(raan) * sin_u * cos_i),
        radius * (sin_u * math.sin(inclination)),
    )
    point = eci_to_geodetic(position, when)
    if point is None:
        return None
    result: dict[str, Any] = dict(point)
    result.update({
        "velocity_kms": math.sqrt(EARTH_MU_KM3_S2 * (2.0 / radius - 1.0 / semi_major)),
        "epoch_unix": elements["epoch_unix"],
        "propagator": "kepler",
    })
    return result




def _sgp4_point(line1: str, line2: str, when_unix: float) -> dict[str, Any] | None:
    """SGP4 sub-satellite point when the optional package is present."""
    try:
        from sgp4.api import Satrec, jday  # type: ignore[import-untyped]
    except ImportError:
        return None
    try:
        satellite = Satrec.twoline2rv(line1, line2)
        instant = datetime.fromtimestamp(when_unix, tz=timezone.utc)
        julian_day, fraction = jday(
            instant.year,
            instant.month,
            instant.day,
            instant.hour,
            instant.minute,
            instant.second + instant.microsecond / 1e6,
        )
        error, position, velocity = satellite.sgp4(julian_day, fraction)
        if error != 0:
            return None
        point = eci_to_geodetic((position[0], position[1], position[2]), when_unix)
        if point is None:
            return None
        result: dict[str, Any] = dict(point)
        result["velocity_kms"] = math.sqrt(
            velocity[0] ** 2 + velocity[1] ** 2 + velocity[2] ** 2
        )
        result["epoch_unix"] = tle_epoch_unix(line1)
        result["propagator"] = "sgp4"
        return result
    except (TypeError, ValueError, IndexError, ZeroDivisionError):
        return None


def subsatellite_point(
    line1: Any, line2: Any, when_unix: Any
) -> dict[str, Any] | None:
    """Sub-satellite point using SGP4 when available, Kepler otherwise."""
    text1 = _text(line1)
    text2 = _text(line2)
    when = _finite(when_unix)
    if not text1 or not text2 or when is None:
        return None
    point = _sgp4_point(text1, text2, when)
    if point is not None:
        return point
    return kepler_subsatellite_point(text1, text2, when)



# --------------------------------------------------------------- aircraft
_EMITTER_CATEGORIES = {
    "A1": 2, "A2": 3, "A3": 4, "A4": 5, "A5": 6, "A6": 7, "A7": 8,
    "B1": 9, "B2": 10, "B3": 11, "B4": 12, "B6": 14, "B7": 15,
}


def _emitter_category(value: Any) -> int | None:
    """Map an adsb.lol ``A3``-style category to the OpenSky integer."""
    text = _text(value).upper()
    if not text:
        return None
    if _digits(text):
        number = int(text)
        return number if 0 <= number <= 17 else None
    return _EMITTER_CATEGORIES.get(text)


def _aircraft_record(
    *,
    icao24: Any,
    latitude: Any,
    longitude: Any,
    callsign: Any = None,
    origin_country: Any = None,
    baro_altitude_m: Any = None,
    geo_altitude_m: Any = None,
    on_ground: Any = False,
    velocity_mps: Any = None,
    heading_deg: Any = None,
    vertical_rate_mps: Any = None,
    squawk: Any = None,
    spi: Any = False,
    position_source: Any = None,
    category: Any = None,
    observed_at: Any = None,
    source: str = "opensky",
) -> dict[str, Any] | None:
    """Build one common aircraft record, or ``None`` when unusable."""
    identifier = _clean(icao24, 16)
    coordinates = _valid_coordinates(latitude, longitude)
    if identifier is None or coordinates is None:
        return None
    lat, lon = coordinates
    return {
        "icao24": identifier.lower(),
        "callsign": _clean(callsign, 16),
        "origin_country": _clean(origin_country, 64),
        "latitude": lat,
        "longitude": lon,
        "baro_altitude_m": _finite(baro_altitude_m),
        "geo_altitude_m": _finite(geo_altitude_m),
        "on_ground": bool(on_ground),
        "velocity_mps": _finite(velocity_mps),
        "heading_deg": _finite(heading_deg),
        "vertical_rate_mps": _finite(vertical_rate_mps),
        "squawk": _clean(squawk, 8),
        "spi": bool(spi),
        "position_source": _finite(position_source),
        "category": _finite(category),
        "observed_at": _finite(observed_at),
        "source": source,
    }


def normalize_opensky_states(payload: Any) -> list[dict[str, Any]]:
    """Normalise an OpenSky ``/api/states/all`` response.

    Invalid rows are dropped individually. Duplicate ICAO addresses keep
    the first valid vector. Units stay SI: metres, m/s, degrees.
    """
    if not isinstance(payload, dict):
        return []
    rows = payload.get("states")
    if not isinstance(rows, list):
        return []
    response_time = _finite(payload.get("time"))
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, (list, tuple)) or len(row) < 17:
            continue
        record = _aircraft_record(
            icao24=row[0],
            callsign=row[1],
            origin_country=row[2],
            latitude=row[6],
            longitude=row[5],
            baro_altitude_m=row[7],
            on_ground=row[8] is True,
            velocity_mps=row[9],
            heading_deg=row[10],
            vertical_rate_mps=row[11],
            geo_altitude_m=row[13],
            squawk=row[14],
            spi=row[15] is True,
            position_source=row[16],
            category=row[17] if len(row) > 17 else None,
            observed_at=_finite(row[4]) or response_time,
            source="opensky",
        )
        if record is None or record["icao24"] in seen:
            continue
        seen.add(record["icao24"])
        out.append(record)
    return out


def _adsblol_now(payload: dict[str, Any]) -> float | None:
    now = _finite(payload.get("now"))
    if now is None:
        return None
    if now > 10_000_000_000:
        now /= 1000.0
    return now


def normalize_adsblol_aircraft(payload: Any) -> list[dict[str, Any]]:
    """Normalise an adsb.lol v2 ``/v2/...`` aircraft response.

    adsb.lol reports feet, knots and feet per minute; the common record
    is SI. ``alt_baro: "ground"`` marks the aircraft as on the ground.
    """
    if not isinstance(payload, dict):
        return []
    rows = payload.get("ac")
    if not isinstance(rows, list):
        return []
    now = _adsblol_now(payload)
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        on_ground = row.get("alt_baro") == "ground"
        baro_feet = None if on_ground else _finite(row.get("alt_baro"))
        geo_feet = _finite(row.get("alt_geom"))
        speed_knots = _finite(row.get("gs"))
        vertical_fpm = _finite(row.get("baro_rate"))
        if vertical_fpm is None:
            vertical_fpm = _finite(row.get("geom_rate"))
        seen_position = _finite(row.get("seen_pos"))
        if seen_position is None:
            seen_position = _finite(row.get("seen"))
        observed_at = None if now is None or seen_position is None else now - seen_position
        record = _aircraft_record(
            icao24=row.get("hex"),
            callsign=row.get("flight") or row.get("r"),
            latitude=row.get("lat"),
            longitude=row.get("lon"),
            baro_altitude_m=None if baro_feet is None else baro_feet * FOOT_TO_M,
            geo_altitude_m=None if geo_feet is None else geo_feet * FOOT_TO_M,
            on_ground=on_ground,
            velocity_mps=None if speed_knots is None else speed_knots * KNOT_TO_MPS,
            heading_deg=row.get("track"),
            vertical_rate_mps=(
                None if vertical_fpm is None else vertical_fpm * FPM_TO_MPS
            ),
            squawk=row.get("squawk"),
            spi=row.get("spi") == 1,
            category=_emitter_category(row.get("category")),
            observed_at=observed_at,
            source="adsb.lol",
        )
        if record is None or record["icao24"] in seen:
            continue
        seen.add(record["icao24"])
        out.append(record)
    return out


def normalize_opensky_track(payload: Any) -> dict[str, Any]:
    """Normalise an OpenSky ``/api/tracks/all`` response."""
    if not isinstance(payload, dict):
        return {}
    waypoints: list[dict[str, Any]] = []
    rows = payload.get("path")
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, (list, tuple)) or len(row) < 3:
                continue
            coordinates = _valid_coordinates(row[1], row[2])
            if coordinates is None:
                continue
            lat, lon = coordinates
            waypoints.append({
                "observed_at": _finite(row[0]),
                "latitude": lat,
                "longitude": lon,
                "baro_altitude_m": _finite(row[3]) if len(row) > 3 else None,
                "heading_deg": _finite(row[5]) if len(row) > 5 else None,
                "on_ground": bool(row[6]) if len(row) > 6 else False,
            })
    return {
        "icao24": _clean(payload.get("icao24"), 16),
        "callsign": _clean(payload.get("callsign"), 16),
        "start_time": _finite(payload.get("startTime")),
        "end_time": _finite(payload.get("endTime")),
        "waypoints": waypoints,
    }


def normalize_adsbdb(payload: Any) -> dict[str, Any]:
    """Normalise an adsbdb aircraft or callsign flight-route response."""
    if not isinstance(payload, dict):
        return {}
    response = payload.get("response")
    if not isinstance(response, dict):
        return {}
    aircraft = response.get("aircraft")
    if isinstance(aircraft, dict):
        return {
            "kind": "aircraft",
            "icao24": _clean(aircraft.get("mode_s"), 16),
            "registration": _clean(aircraft.get("registration"), 24),
            "icao_type": _clean(aircraft.get("icao_type"), 16),
            "manufacturer": _clean(aircraft.get("manufacturer"), 64),
            "type": _clean(aircraft.get("type"), 64),
            "owner": _clean(aircraft.get("registered_owner"), 96),
            "owner_country": _clean(
                aircraft.get("registered_owner_country_name"), 64
            ),
            "photo_url": _clean(aircraft.get("url_photo"), 512),
        }
    route = response.get("flightroute")
    if isinstance(route, dict):
        airline = _as_dict(route.get("airline"))
        origin = _as_dict(route.get("origin"))
        destination = _as_dict(route.get("destination"))
        return {
            "kind": "flightroute",
            "callsign": _clean(route.get("callsign"), 16),
            "airline": _clean(airline.get("name"), 96),
            "airline_icao": _clean(airline.get("icao"), 8),
            "origin": _clean(origin.get("iata") or origin.get("icao"), 8),
            "origin_name": _clean(origin.get("name"), 96),
            "destination": _clean(
                destination.get("iata") or destination.get("icao"), 8
            ),
            "destination_name": _clean(destination.get("name"), 96),
        }
    return {}


def normalize_launch_library(payload: Any) -> list[dict[str, Any]]:
    """Normalise a Launch Library 2 ``/launches/`` response.

    Launches without pad coordinates are still returned (the operator
    may want the schedule), but only located launches become map
    points in the feed.
    """
    if not isinstance(payload, dict):
        return []
    results = payload.get("results")
    if not isinstance(results, list):
        return []
    out: list[dict[str, Any]] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        status = _as_dict(item.get("status"))
        provider = _as_dict(item.get("launch_service_provider"))
        rocket = _as_dict(item.get("rocket"))
        configuration = _as_dict(rocket.get("configuration"))
        pad = _as_dict(item.get("pad"))
        location = _as_dict(pad.get("location"))
        mission = _as_dict(item.get("mission"))
        orbit = _as_dict(mission.get("orbit"))
        coordinates = _valid_coordinates(
            pad.get("latitude"), pad.get("longitude")
        )
        out.append({
            "id": _clean(item.get("id"), 64),
            "name": _clean(item.get("name"), 200),
            "net": _clean(item.get("net"), 40),
            "status": _clean(status.get("abbrev") or status.get("name"), 40),
            "provider": _clean(provider.get("name"), 96),
            "rocket": _clean(
                configuration.get("full_name") or configuration.get("name"), 96
            ),
            "pad": _clean(pad.get("name"), 96),
            "location": _clean(location.get("name"), 96),
            "latitude": None if coordinates is None else coordinates[0],
            "longitude": None if coordinates is None else coordinates[1],
            "mission": _clean(mission.get("name"), 120),
            "orbit": _clean(orbit.get("name"), 40),
        })
    return out


def cap_records(records: Any, limit: Any) -> list[dict[str, Any]]:
    """Return at most ``limit`` records. A non-positive limit yields []."""
    if not isinstance(records, list):
        return []
    maximum = _finite(limit)
    if maximum is None:
        return []
    bounded = int(maximum)
    if bounded <= 0:
        return []
    return [record for record in records[:bounded] if isinstance(record, dict)]

