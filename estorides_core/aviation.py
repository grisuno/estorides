"""
estorides_core.aviation
=======================
Pure aircraft-intelligence helpers shared by the aerospace sources and
the real-time map feeds.

Everything here is deterministic and side-effect free: no network, no
filesystem, no environment. Transport lives in
:mod:`estorides_core.feeds`; the orbital math lives in
:mod:`estorides_core.aerospace`; the airport dataset lives in
:mod:`estorides_core.airports`.

What this module answers for one airframe:

  * **Which class of aircraft is it?** — ICAO type designators and
    ADS-B emitter categories collapse into a small display vocabulary
    (light, turboprop, airliner, widebody, quadjet, helicopter, fastjet,
    bizjet, glider, balloon, uav, ground, space).
  * **Is it broadcasting an emergency?** — Mode A squawks 7500/7600/7700
    plus the ADS-B emergency/priority field, with severity and the exact
    wording an analyst may safely quote.
  * **What do the community database flags say?** — military, interesting,
    PIA and LADD bits from the readsb ``dbFlags`` bitfield.
  * **How far apart are two points?** — haversine distance and
    bounding-box helpers used by the regional aircraft feed.

Design note: nothing here decides that an incident happened. A squawk is
what a transponder broadcast in one poll; crews pass through 7x00 codes
while dialling, and a code does not confirm or resolve an emergency.

Branding: Estorides, developed by Lazy Own Red Team.
"""
from __future__ import annotations

import math
from typing import Any

# Display vocabulary. Labels are English data strings (the interface
# translates them client-side like every other record field).
CLASS_LIGHT = "light"
CLASS_GLIDER = "glider"
CLASS_BALLOON = "balloon"
CLASS_TURBOPROP = "turboprop"
CLASS_AIRLINER = "airliner"
CLASS_WIDEBODY = "widebody"
CLASS_QUADJET = "quadjet"
CLASS_HELICOPTER = "helicopter"
CLASS_FASTJET = "fastjet"
CLASS_BIZJET = "bizjet"
CLASS_UAV = "uav"
CLASS_GROUND = "ground"
CLASS_SPACE = "space"
CLASS_UNKNOWN = "unknown"

CLASS_LABELS: dict[str, str] = {
    CLASS_LIGHT: "Light aircraft",
    CLASS_GLIDER: "Glider",
    CLASS_BALLOON: "Balloon / airship",
    CLASS_TURBOPROP: "Turboprop",
    CLASS_AIRLINER: "Airliner",
    CLASS_WIDEBODY: "Widebody",
    CLASS_QUADJET: "Four-engine jet",
    CLASS_HELICOPTER: "Helicopter",
    CLASS_FASTJET: "Fast jet",
    CLASS_BIZJET: "Business jet",
    CLASS_UAV: "Uncrewed aircraft",
    CLASS_GROUND: "Surface vehicle",
    CLASS_SPACE: "Space / trans-atmospheric",
    CLASS_UNKNOWN: "Unknown",
}

EARTH_RADIUS_KM = 6371.0088
KM_PER_NM = 1.852
# adsb.lol (readsb) refuses a radius above 250 nautical miles.
MAX_REGIONAL_RADIUS_NM = 250.0


# --------------------------------------------------------------- primitives
def _finite(value: Any) -> float | None:
    """Return ``value`` as a finite float, or ``None`` (bools rejected)."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def _clean(value: Any, limit: int = 64) -> str | None:
    """Trim, bound and empty-collapse a text field."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text[:limit] or None


def _codes(blob: str) -> frozenset[str]:
    """Build a type-designator set from a whitespace-separated blob."""
    return frozenset(part for part in blob.split() if part)


# ------------------------------------------------------- type classification
# ICAO Doc 8643 type designators grouped by the class an operator cares
# about on a map. The sets are curated, not exhaustive: an unknown
# four-letter designator falls back to the emitter category and then to
# "unknown" — guessing "airliner" for a microlight would be worse than
# admitting the gap.
_HELICOPTER = _codes("""
    A109 A119 A139 A169 A189 AS32 AS50 AS55 AS65 AW09 AW119 AW139 AW169 AW189
    B06 B06T B105 B204 B205 B206 B212 B214 B222 B407 B412 B427 B429 B430 B47G
    B505 CH47 CH53 EC20 EC25 EC30 EC35 EC45 EC55 EC66 EC75 EXEC EXPL GAZL H47
    H60 H64 H500 LYNX MD52 MD60 NH90 PUMA S61 S64 S70 S76 S92 S97 UH1 UH60
""")
_HELICOPTER_PREFIXES = (
    "EC1", "EC2", "EC3", "EC4", "EC5", "EC6",
    "AS32", "AS332", "AS35", "AS36", "AS5", "AS6", "AW1", "A109", "A119", "A139",
    "A169", "A189",
    "H60", "H64", "UH", "AH6", "CH4", "MD5", "NH90",
    "R22", "R44", "R66", "S61", "S64", "S70", "S76", "S92", "S97",
    "LYNX", "PUMA", "GAZL", "EXEC", "EXPL", "SCAV",
)

_QUADJET = _codes("""
    A124 A140 A225 A342 A343 A345 A346 A388 B52 B741 B742 B743 B744 B748 B74D
    B74R B74S C17 C5M IL96 K35R
""")

_WIDEBODY = _codes("""
    A30B A306 A310 A332 A333 A337 A338 A339 A359 A35K B762 B763 B764 B767 B772
    B773 B777 B778 B779 B77L B77W B788 B789 B78X DC10 IL86 L101 MD11
""")

_TURBOPROP = _codes("""
    A400 AN12 AN24 AN26 AN30 AN32 AT43 AT44 AT45 AT46 AT72 AT73 AT75 AT76 ATP
    B190 B300 B350 BE20 C130 C208 C212 C408 CN35 CVLT D228 D328 DH8A DH8B DH8C
    DH8D DHC6 DHC7 E110 E120 F27 F50 JS31 JS32 JS41 MU2 PC12 PC6 SAAB SB20
    SF34 SH36 SW3 SW4 TBM0 TBM7 TBM8 TBM9
""")
_TURBOPROP_PREFIXES = ("TBM",)

_GLIDER = _codes("""
    ARCE AS33 ASG ASK ASW DG1T DG30 DG40 DG50 DG80 DISC DIMO DUOD G102 G103 G104
    GLID H201 JANS KEST L13 L23 L33 LS3 LS4 LS6 LS7 LS8 MOSQ NIM3 NIM4 NIMB
    PEGA PIK PW5 PW6 STD3 TWIN VENS VENT
""")
_GLIDER_PREFIXES = ("DG", "LS", "ASW", "ASG")

_BIZJET = _codes("""
    BE40 C25A C25B C25C C25M C500 C501 C510 C525 C550 C551 C560 C56X C650 C680
    C68A C700 C750 CL30 CL35 CL60 E50P E545 E55P F2TH F900 FA10 FA20 FA50 FA7X
    FA8X G150 G280 GA5C GA6C GL5T GL7T GLEX GLF2 GLF3 GLF4 GLF5 GLF6 H25A H25B
    HDJT LJ23 LJ24 LJ25 LJ31 LJ35 LJ40 LJ45 LJ55 LJ60 LJ70 LJ75 PRM1 PC24
""")
_BIZJET_PREFIXES = ("GLF", "LJ", "C25", "CL3", "CL6", "FA")

_LIGHT = _codes("""
    AA1 AA5 BE19 BE23 BE24 BE33 BE35 BE36 BE58 BE76 BL8 C140 C150 C152 C162
    C170 C172 C175 C177 C180 C182 C185 C188 C206 C207 C210 C310 C337 CH7 COL4
    DA20 DA40 DA42 DA62 DR20 DR40 G115 GA8 GLAS M20P M20T P28A P28B P28R PA18
    PA24 PA28 PA32 PA34 PA38 PA44 PA46 RV10 RV14 RV4 RV6 RV7 RV8 RV9 S22T
    SR20 SR22 TB20 TB21
""")

_FASTJET = _codes("""
    A10 AV8 AV8B B1 B2 B52 EF2K EUFI F117 F14 F15 F16 F18 F22 F35 F4 F5 GRIP
    HAWK J10 J11 J20 J7 J8 JH7 JAS39 M2K MIG21 MIG23 MIG25 MIG29 MIG31 MIR RFAL
    SU27 SU30 SU34 SU35 SU57 TOR TYPH
""")
_FASTJET_PREFIXES = ("F15", "F16", "F18", "F35", "EF2", "MIR", "MIG", "SU2",
                     "SU3", "SU5", "JAS", "GRIP", "TYPH", "EUFI")

_UAV = _codes("""
    ANKA BAY HERO MQ1 MQ4 MQ8 MQ9 PHAN RQ4 RQ7 RQ9 TB2 ZEPH
""")
_UAV_PREFIXES = ("MQ", "RQ", "TB2", "BAY", "HERO", "ANKA", "ZEPH", "PHAN",
                 "GHAM")

# Narrowbody airliners: the families whose variants all read the same on a
# map. Widest and four-engine families are matched earlier, so a prefix
# here only catches the short/medium-haul hulls.
_AIRLINER_PREFIXES = (
    "A19", "A20", "A21", "A22", "A31", "A32", "A148",
    "B37", "B38", "B39", "B73", "B71", "B75",
    "MD8", "MD9", "E17", "E19", "E29", "CRJ", "RJ8", "RJ9",
    "T204", "T214",
)

# Ordered widest-match-first: each entry is (class, exact set, prefixes).
_TYPE_TABLES: tuple[tuple[str, frozenset[str], tuple[str, ...]], ...] = (
    (CLASS_HELICOPTER, _HELICOPTER, _HELICOPTER_PREFIXES),
    (CLASS_UAV, _UAV, _UAV_PREFIXES),
    (CLASS_FASTJET, _FASTJET, _FASTJET_PREFIXES),
    (CLASS_QUADJET, _QUADJET, ()),
    (CLASS_WIDEBODY, _WIDEBODY, ()),
    (CLASS_TURBOPROP, _TURBOPROP, _TURBOPROP_PREFIXES),
    (CLASS_GLIDER, _GLIDER, _GLIDER_PREFIXES),
    (CLASS_BIZJET, _BIZJET, _BIZJET_PREFIXES),
    (CLASS_LIGHT, _LIGHT, ()),
    (CLASS_AIRLINER, frozenset(), _AIRLINER_PREFIXES),
)

# OpenSky state-vector category integers (extended=1, index 17).
_OPENSKY_CATEGORY: dict[int, str] = {
    2: CLASS_LIGHT, 3: CLASS_AIRLINER, 4: CLASS_AIRLINER, 5: CLASS_AIRLINER,
    6: CLASS_WIDEBODY, 7: CLASS_FASTJET, 8: CLASS_HELICOPTER, 9: CLASS_GLIDER,
    10: CLASS_BALLOON, 12: CLASS_LIGHT, 14: CLASS_UAV, 15: CLASS_SPACE,
    16: CLASS_GROUND, 17: CLASS_GROUND, 18: CLASS_GROUND, 19: CLASS_GROUND,
    20: CLASS_GROUND,
}

# ADS-B emitter category strings (DO-260B): A1..A7, B1..B7, C1..C5.
_EMITTER_CATEGORY: dict[str, str] = {
    "A1": CLASS_LIGHT, "A2": CLASS_LIGHT, "A3": CLASS_AIRLINER,
    "A4": CLASS_AIRLINER, "A5": CLASS_WIDEBODY, "A6": CLASS_FASTJET,
    "A7": CLASS_HELICOPTER,
    "B1": CLASS_GLIDER, "B2": CLASS_BALLOON, "B4": CLASS_LIGHT,
    "B6": CLASS_UAV, "B7": CLASS_SPACE,
    "C1": CLASS_GROUND, "C2": CLASS_GROUND, "C3": CLASS_GROUND,
    "C4": CLASS_GROUND, "C5": CLASS_GROUND,
}


def normalize_type_code(value: Any) -> str:
    """Return an upper-case ICAO type designator, or ``""``."""
    text = _clean(value, 12)
    return text.upper().replace(" ", "") if text else ""


def classify_aircraft(type_code: Any = None, category: Any = None) -> str:
    """Return the display class for one airframe.

    The type designator wins over the emitter category because it is
    specific. A designator nobody curated falls through to the category;
    with neither signal the answer is :data:`CLASS_UNKNOWN`.
    """
    code = normalize_type_code(type_code)
    if code:
        for cls, exact, prefixes in _TYPE_TABLES:
            if code in exact or (prefixes and code.startswith(prefixes)):
                return cls
    return _category_class(category)


def _category_class(category: Any) -> str:
    """Map an emitter category (int, numeric string or ``A3``) to a class."""
    if category is None or isinstance(category, bool):
        return CLASS_UNKNOWN
    number = _finite(category)
    if number is not None:
        return _OPENSKY_CATEGORY.get(int(number), CLASS_UNKNOWN)
    if isinstance(category, str):
        return _EMITTER_CATEGORY.get(category.strip().upper(), CLASS_UNKNOWN)
    return CLASS_UNKNOWN


def aircraft_class_label(value: Any) -> str:
    """Human-readable label for a class slug (``unknown`` when absent)."""
    slug = _clean(value, 24)
    return CLASS_LABELS.get(slug or "", CLASS_LABELS[CLASS_UNKNOWN])


# ----------------------------------------------------------- emergencies
# ICAO-standard Mode A codes: they mean the same thing worldwide.
_SQUAWK_KINDS: dict[str, str] = {
    "7500": "unlawful",
    "7600": "nordo",
    "7700": "general",
}

# Transponder states an ADS-B receiver may report (a superset of 7x00).
EMERGENCY_KINDS: dict[str, dict[str, str]] = {
    "general": {"label": "General emergency", "severity": "emergency"},
    "unlawful": {"label": "Unlawful interference", "severity": "emergency"},
    "nordo": {"label": "Radio failure", "severity": "emergency"},
    "downed": {"label": "Downed aircraft", "severity": "emergency"},
    "minfuel": {"label": "Minimum fuel", "severity": "priority"},
    "lifeguard": {"label": "Lifeguard (medical priority)", "severity": "priority"},
}

_SEVERITY_RANK: dict[str, int] = {"priority": 1, "emergency": 2}


def normalize_squawk(value: Any) -> str | None:
    """Return a Mode A code as four octal digits, or ``None``.

    ``"7700"`` and ``7700`` are both accepted; anything that is not four
    digits in 0-7 (the transponder alphabet) is rejected rather than
    silently truncated.
    """
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        text = f"{value:04d}"
    elif isinstance(value, str):
        text = value.strip()
    else:
        return None
    if len(text) != 4 or not text.isdigit():
        return None
    if any(char not in "01234567" for char in text):
        return None
    return text


def emergency_status(squawk: Any = None, emergency: Any = None) -> dict[str, Any] | None:
    """Derive the emergency state from one observation.

    Both inputs are what the transponder broadcast in this poll: the Mode
    A squawk and the ADS-B emergency/priority field. The most severe
    signal wins; on a tie the ADS-B field wins because it is more
    specific. ``source`` says which one named the status, so a report can
    quote the squawk only when the squawk is the evidence.
    """
    code = normalize_squawk(squawk)
    reported = _clean(emergency, 24)
    reported_key = reported.lower() if reported else ""
    squawk_kind = _SQUAWK_KINDS.get(code or "")
    adsb_kind = reported_key if reported_key in EMERGENCY_KINDS else None
    chosen: str | None
    if squawk_kind and adsb_kind:
        squawk_rank = _SEVERITY_RANK[EMERGENCY_KINDS[squawk_kind]["severity"]]
        adsb_rank = _SEVERITY_RANK[EMERGENCY_KINDS[adsb_kind]["severity"]]
        chosen = adsb_kind if adsb_rank >= squawk_rank else squawk_kind
    else:
        chosen = adsb_kind or squawk_kind
    if chosen is None:
        return None
    return {
        "kind": chosen,
        **EMERGENCY_KINDS[chosen],
        "squawk": code,
        "source": "squawk" if squawk_kind == chosen else "ads-b",
    }


def is_emergency(status: Any) -> bool:
    """True when a status dict describes an emergency (not a priority)."""
    return isinstance(status, dict) and status.get("severity") == "emergency"


def emergency_phrase(status: Any) -> str | None:
    """Wording an analyst may quote, without flattening the signal into a fact.

    ``broadcasting squawk 7700 (general emergency)`` when the Mode A code
    is the evidence, ``ADS-B reports general emergency`` otherwise.
    """
    if not isinstance(status, dict):
        return None
    kind = status.get("kind")
    if kind not in EMERGENCY_KINDS:
        return None
    label = EMERGENCY_KINDS[str(kind)]["label"].lower()
    if status.get("source") == "squawk" and normalize_squawk(status.get("squawk")):
        return f"broadcasting squawk {status['squawk']} ({label})"
    return f"ADS-B reports {label}"


# ------------------------------------------------------- community flags
_DB_FLAG_BITS: tuple[tuple[str, int], ...] = (
    ("military", 1),
    ("interesting", 2),
    ("pia", 4),
    ("ladd", 8),
)


def decode_db_flags(value: Any) -> dict[str, Any] | None:
    """Decode the readsb ``dbFlags`` bitfield into named booleans.

    Bit 0 military, bit 1 interesting (PIA/type mismatch), bit 2 PIA
    (privacy ICAO address), bit 3 LADD (limited address display). The raw
    integer is preserved so a future bit is not silently lost.
    """
    number = _finite(value)
    if number is None or number < 0:
        return None
    flags: dict[str, Any] = {name: bool(int(number) & bit)
                             for name, bit in _DB_FLAG_BITS}
    flags["raw"] = int(number)
    return flags


# ---------------------------------------------------- navigation integrity
# ADS-B quality fields. NACp (navigation accuracy category for position)
# and NIC (navigation integrity category) fall when a receiver loses GPS
# quality — which is what jamming and spoofing look like from the ground.
# They are reported facts, not a verdict: a low value can also mean an old
# transponder that never had them.
NAV_LEVELS: tuple[str, ...] = ("nominal", "degraded", "poor", "no-integrity",
                               "unknown")


def navigation_integrity(
    *,
    nac_p: Any = None,
    nic: Any = None,
    sil: Any = None,
    on_ground: bool = False,
) -> dict[str, Any]:
    """Classify the navigation integrity an airframe is reporting.

    ``nominal`` at NACp/NIC >= 8, ``degraded`` at 6-7, ``poor`` at 1-5 and
    ``no-integrity`` at 0. With neither field present the level is
    ``unknown`` — absence of evidence, not evidence of jamming.
    ``suspected_jamming`` is only set for an airborne aircraft in the
    ``poor`` or ``no-integrity`` band.
    """
    accuracy = _finite(nac_p)
    integrity = _finite(nic)
    signal = _finite(sil)
    metric = accuracy if accuracy is not None else integrity
    if metric is None:
        level = "unknown"
    elif metric >= 8:
        level = "nominal"
    elif metric >= 6:
        level = "degraded"
    elif metric >= 1:
        level = "poor"
    else:
        level = "no-integrity"
    return {
        "level": level,
        "nac_p": accuracy,
        "nic": integrity,
        "sil": signal,
        "suspected_jamming": bool(
            level in {"poor", "no-integrity"} and not on_ground
        ),
    }


# --------------------------------------------------------------- geometry
def haversine_km(lat1: Any, lon1: Any, lat2: Any, lon2: Any) -> float | None:
    """Great-circle distance in kilometres, or ``None`` for bad input."""
    a_lat, a_lon, b_lat, b_lon = (_finite(lat1), _finite(lon1),
                                  _finite(lat2), _finite(lon2))
    if None in (a_lat, a_lon, b_lat, b_lon):
        return None
    if abs(a_lat) > 90 or abs(b_lat) > 90 or abs(a_lon) > 180 or abs(b_lon) > 180:
        return None
    phi1, phi2 = math.radians(a_lat), math.radians(b_lat)
    d_phi = phi2 - phi1
    d_lambda = math.radians(b_lon - a_lon)
    h = (math.sin(d_phi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(h)))


def bbox_center_radius(bbox: Any) -> tuple[float, float, float] | None:
    """Centre and half-diagonal radius (nautical miles) of a bbox.

    ``bbox`` is ``(min_lon, min_lat, max_lon, max_lat)`` — the same order
    :func:`estorides_core.feeds.fetch_all` uses. ``None`` for a malformed
    or degenerate box, and for boxes wider than the regional query limit
    (callers then fall back to the worldwide snapshot).
    """
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        return None
    values = [_finite(item) for item in bbox]
    if any(value is None for value in values):
        return None
    min_lon, min_lat, max_lon, max_lat = (float(value) for value in values)  # type: ignore[arg-type]
    if min_lon >= max_lon or min_lat >= max_lat:
        return None
    if abs(min_lat) > 90 or abs(max_lat) > 90:
        return None
    if abs(min_lon) > 180 or abs(max_lon) > 180:
        return None
    centre_lat = (min_lat + max_lat) / 2.0
    centre_lon = (min_lon + max_lon) / 2.0
    diagonal_km = haversine_km(min_lat, min_lon, max_lat, max_lon)
    if diagonal_km is None:
        return None
    radius_nm = max(diagonal_km / 2.0 / KM_PER_NM, 1.0)
    return centre_lat, centre_lon, radius_nm


def point_in_bbox(lat: Any, lon: Any, bbox: Any) -> bool:
    """True when ``(lat, lon)`` falls inside an inclusive bbox."""
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        return False
    latitude, longitude = _finite(lat), _finite(lon)
    if latitude is None or longitude is None:
        return False
    min_lon, min_lat, max_lon, max_lat = bbox
    try:
        return (float(min_lon) <= longitude <= float(max_lon)
                and float(min_lat) <= latitude <= float(max_lat))
    except (TypeError, ValueError):
        return False


# ------------------------------------------------------------- hexdb.io
def normalize_hexdb_aircraft(payload: Any) -> dict[str, Any]:
    """Normalise a hexdb.io ``/api/v1/aircraft/{hex}`` response.

    hexdb answers ``{"status": "404", ...}`` for an unknown airframe; that
    becomes an empty dict so the caller can tell "no record" from "bad
    payload". Registration, type and owner are the fields that turn a bare
    ICAO address into an identifiable airframe.
    """
    if not isinstance(payload, dict):
        return {}
    status = _clean(payload.get("status"), 8)
    if status and status.isdigit() and status != "200":
        return {}
    mode_s = _clean(payload.get("ModeS"), 16)
    registration = _clean(payload.get("Registration"), 16)
    type_code = _clean(payload.get("ICAOTypeCode"), 12)
    if mode_s is None and registration is None and type_code is None:
        return {}
    return {
        "kind": "aircraft",
        "icao24": mode_s.lower() if mode_s else None,
        "registration": registration,
        "type_code": type_code,
        "manufacturer": _clean(payload.get("Manufacturer"), 64),
        "type": _clean(payload.get("Type"), 96),
        "owner": _clean(payload.get("RegisteredOwners"), 96),
        "operator_flag": _clean(payload.get("OperatorFlagCode"), 8),
        "aircraft_class": classify_aircraft(type_code),
    }


def normalize_hexdb_route(payload: Any) -> dict[str, Any]:
    """Normalise a hexdb.io ``/api/v1/route/icao/{callsign}`` response.

    The route arrives as ``"EGLL-LEMD"``; a missing or dashed route keeps
    the callsign but leaves the airports ``None`` rather than inventing
    them.
    """
    if not isinstance(payload, dict):
        return {}
    callsign = _clean(payload.get("flight"), 16)
    route = _clean(payload.get("route"), 32)
    if callsign is None and route is None:
        return {}
    origin: str | None = None
    destination: str | None = None
    if route:
        parts = [part.strip().upper() for part in route.split("-")]
        if len(parts) == 2 and all(part.isalnum() and 3 <= len(part) <= 4
                                   for part in parts):
            origin, destination = parts
    return {
        "kind": "flightroute",
        "callsign": callsign.upper() if callsign else None,
        "route": route,
        "origin": origin,
        "destination": destination,
        "updated_at": _finite(payload.get("updatetime")),
    }
