"""
Property-based invariants for estorides_core.aerospace.

Scenario A9 (every normaliser is total) and the coordinate invariants of
A3/A5/A6 are the executable contract. Hypothesis generates hostile JSON,
arbitrary rows and arbitrary TLE text; nothing may raise and every
emitted coordinate must be inside WGS84 bounds.
"""
from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from estorides_core import aerospace

FIELD_TYPES = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(max_size=200),
)

JSON_SAFE = st.recursive(
    FIELD_TYPES,
    lambda children: st.one_of(
        st.lists(children, max_size=8),
        st.dictionaries(st.text(max_size=32), children, max_size=8),
    ),
    max_leaves=32,
)

COORD = st.one_of(
    st.none(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.text(max_size=12),
    st.integers(min_value=-1000, max_value=1000),
)


def _coordinates_are_valid(record: dict) -> bool:
    latitude = record["latitude"]
    longitude = record["longitude"]
    return -90.0 <= latitude <= 90.0 and -180.0 <= longitude <= 180.0


@settings(max_examples=300, deadline=None)
@given(payload=JSON_SAFE)
def test_normalisers_never_raise(payload: object) -> None:
    assert isinstance(aerospace.normalize_opensky_states(payload), list)
    assert isinstance(aerospace.normalize_adsblol_aircraft(payload), list)
    assert isinstance(aerospace.normalize_launch_library(payload), list)
    assert isinstance(aerospace.normalize_adsbdb(payload), dict)
    assert isinstance(aerospace.normalize_opensky_track(payload), dict)
    assert isinstance(aerospace.parse_tle_catalog(payload), list)
    assert isinstance(aerospace.cap_records(payload, 10), list)


@settings(max_examples=300, deadline=None)
@given(lat=COORD, lon=COORD)
def test_opensky_coordinates_stay_in_bounds(lat: object, lon: object) -> None:
    payload = {"states": [["abc123", "X", "Y", 0, 0, lon, lat, None,
                          False, None, None, None, None, None, None,
                          False, 0, 0]]}
    for record in aerospace.normalize_opensky_states(payload):
        assert _coordinates_are_valid(record)


@settings(max_examples=300, deadline=None)
@given(lat=COORD, lon=COORD)
def test_adsblol_coordinates_stay_in_bounds(lat: object, lon: object) -> None:
    payload = {"now": 1700000000, "ac": [{"hex": "abc123", "lat": lat, "lon": lon}]}
    for record in aerospace.normalize_adsblol_aircraft(payload):
        assert _coordinates_are_valid(record)


@settings(max_examples=200, deadline=None)
@given(text=st.text(max_size=400))
def test_tle_parser_only_returns_complete_sets(text: str) -> None:
    for satellite in aerospace.parse_tle_catalog(text):
        assert satellite["line1"].startswith("1 ")
        assert satellite["line2"].startswith("2 ")
        assert aerospace.tle_catalog_number(satellite["line1"]) == satellite["norad_id"]


@settings(max_examples=200, deadline=None)
@given(field=st.text(max_size=8))
def test_catalog_field_never_raises(field: str) -> None:
    value = aerospace.decode_catalog_field(field)
    assert value is None or value >= 0


@settings(max_examples=100, deadline=None)
@given(offset=st.floats(min_value=-86400, max_value=86400, allow_nan=False))
def test_subsatellite_point_stays_physical(offset: float) -> None:
    line1 = "1 25544U 98067A   24001.50000000  .00016717  00000+0  30777-3 0  9994"
    line2 = "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.50000000431234"
    epoch = aerospace.tle_epoch_unix(line1)
    assert epoch is not None
    point = aerospace.kepler_subsatellite_point(line1, line2, epoch + offset)
    assert point is not None
    assert -90.0 <= point["latitude"] <= 90.0
    assert -180.0 <= point["longitude"] <= 180.0
    assert point["altitude_km"] > 100.0
