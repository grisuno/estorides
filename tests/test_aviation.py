"""
BDD tests for :mod:`estorides_core.aviation`.

Covers aircraft classification, emergency status, community flags, the
geometry helpers the regional feed relies on, and the hexdb.io
normalisers. Every assertion pins one observable behaviour so a mutant
that flips it cannot survive.
"""
from __future__ import annotations

from typing import Any

import pytest

from estorides_core import aviation


class TestClassification:
    @pytest.mark.parametrize("type_code,expected", [
        ("A320", aviation.CLASS_AIRLINER),
        ("B738", aviation.CLASS_AIRLINER),
        ("b738", aviation.CLASS_AIRLINER),
        ("B77W", aviation.CLASS_WIDEBODY),
        ("A359", aviation.CLASS_WIDEBODY),
        ("A388", aviation.CLASS_QUADJET),
        ("B744", aviation.CLASS_QUADJET),
        ("C17", aviation.CLASS_QUADJET),
        ("AT72", aviation.CLASS_TURBOPROP),
        ("DH8D", aviation.CLASS_TURBOPROP),
        ("C130", aviation.CLASS_TURBOPROP),
        ("C208", aviation.CLASS_TURBOPROP),
        ("C172", aviation.CLASS_LIGHT),
        ("SR22", aviation.CLASS_LIGHT),
        ("PA28", aviation.CLASS_LIGHT),
        ("EC135", aviation.CLASS_HELICOPTER),
        ("AS332", aviation.CLASS_HELICOPTER),
        ("R44", aviation.CLASS_HELICOPTER),
        ("AS33", aviation.CLASS_GLIDER),
        ("LS8", aviation.CLASS_GLIDER),
        ("MQ9", aviation.CLASS_UAV),
        ("RQ4", aviation.CLASS_UAV),
        ("F16C", aviation.CLASS_FASTJET),
        ("SU30", aviation.CLASS_FASTJET),
        ("B2", aviation.CLASS_FASTJET),
        ("GLF6", aviation.CLASS_BIZJET),
        ("C25A", aviation.CLASS_BIZJET),
        ("LJ45", aviation.CLASS_BIZJET),
    ])
    def test_type_designator_wins(self, type_code: str, expected: str) -> None:
        assert aviation.classify_aircraft(type_code) == expected

    def test_unknown_designator_falls_back_to_category(self) -> None:
        assert aviation.classify_aircraft("ZZZZ", "A7") == aviation.CLASS_HELICOPTER
        assert aviation.classify_aircraft("ZZZZ", None) == aviation.CLASS_UNKNOWN

    @pytest.mark.parametrize("category,expected", [
        (2, aviation.CLASS_LIGHT),
        (4, aviation.CLASS_AIRLINER),
        (6, aviation.CLASS_WIDEBODY),
        (7, aviation.CLASS_FASTJET),
        (8, aviation.CLASS_HELICOPTER),
        (9, aviation.CLASS_GLIDER),
        (10, aviation.CLASS_BALLOON),
        (14, aviation.CLASS_UAV),
        (15, aviation.CLASS_SPACE),
        (16, aviation.CLASS_GROUND),
        ("12", aviation.CLASS_LIGHT),
        ("B2", aviation.CLASS_BALLOON),
        ("C2", aviation.CLASS_GROUND),
    ])
    def test_category_fallback(self, category: Any, expected: str) -> None:
        assert aviation.classify_aircraft(None, category) == expected

    @pytest.mark.parametrize("category", [None, 0, 1, 11, 13, 99, "", "Z9", True])
    def test_unmapped_categories_are_unknown(self, category: Any) -> None:
        assert aviation.classify_aircraft(None, category) == aviation.CLASS_UNKNOWN

    def test_type_code_is_normalised(self) -> None:
        assert aviation.normalize_type_code(" b73 8 ") == "B738"
        assert aviation.normalize_type_code(None) == ""
        assert aviation.normalize_type_code(42) == ""

    def test_labels(self) -> None:
        assert aviation.aircraft_class_label("widebody") == "Widebody"
        assert aviation.aircraft_class_label("nope") == "Unknown"
        assert aviation.aircraft_class_label(None) == "Unknown"


class TestEmergency:
    @pytest.mark.parametrize("value,expected", [
        ("7700", "7700"),
        (7700, "7700"),
        (" 7500 ", "7500"),
        ("770", None),
        ("07700", None),
        ("7708", None),          # 8 is not a transponder digit
        ("abcd", None),
        (None, None),
        (True, None),
        (77.0, None),
    ])
    def test_squawk_normalisation(self, value: Any, expected: str | None) -> None:
        assert aviation.normalize_squawk(value) == expected

    def test_squawk_names_the_status(self) -> None:
        status = aviation.emergency_status("7700")
        assert status == {
            "kind": "general",
            "label": "General emergency",
            "severity": "emergency",
            "squawk": "7700",
            "source": "squawk",
        }

    def test_every_icao_code(self) -> None:
        assert aviation.emergency_status("7500")["kind"] == "unlawful"
        assert aviation.emergency_status("7600")["kind"] == "nordo"
        assert aviation.emergency_status("7700")["kind"] == "general"

    def test_adsb_field_alone(self) -> None:
        status = aviation.emergency_status(None, "minfuel")
        assert status is not None
        assert status["severity"] == "priority"
        assert status["source"] == "ads-b"
        assert status["squawk"] is None

    def test_more_severe_signal_wins(self) -> None:
        # A 7700 squawk beats an ADS-B "minimum fuel" priority.
        status = aviation.emergency_status("7700", "minfuel")
        assert status is not None
        assert status["kind"] == "general"
        assert status["source"] == "squawk"

    def test_adsb_priority_is_kept_when_no_squawk_kind(self) -> None:
        status = aviation.emergency_status("1200", "lifeguard")
        assert status is not None
        assert status["kind"] == "lifeguard"
        assert status["source"] == "ads-b"

    def test_adsb_wins_a_tie(self) -> None:
        status = aviation.emergency_status("7700", "downed")
        assert status is not None
        assert status["kind"] == "downed"
        assert status["source"] == "ads-b"

    @pytest.mark.parametrize("squawk,emergency", [
        (None, None),
        ("1200", None),
        ("1200", "none"),
        ("1200", "reserved"),
        ("1200", "nonsense"),
        ("", ""),
    ])
    def test_no_status(self, squawk: Any, emergency: Any) -> None:
        assert aviation.emergency_status(squawk, emergency) is None

    def test_is_emergency(self) -> None:
        assert aviation.is_emergency(aviation.emergency_status("7700")) is True
        assert aviation.is_emergency(aviation.emergency_status(None, "minfuel")) is False
        assert aviation.is_emergency(None) is False
        assert aviation.is_emergency({"severity": "priority"}) is False

    def test_phrase_quotes_only_the_squawk_source(self) -> None:
        assert (aviation.emergency_phrase(aviation.emergency_status("7700"))
                == "broadcasting squawk 7700 (general emergency)")
        assert (aviation.emergency_phrase(aviation.emergency_status(None, "general"))
                == "ADS-B reports general emergency")
        assert aviation.emergency_phrase(None) is None
        assert aviation.emergency_phrase({"kind": "nope"}) is None


class TestDbFlags:
    @pytest.mark.parametrize("value,expected", [
        (0, {"military": False, "interesting": False, "pia": False, "ladd": False}),
        (1, {"military": True, "interesting": False, "pia": False, "ladd": False}),
        (2, {"military": False, "interesting": True, "pia": False, "ladd": False}),
        (4, {"military": False, "interesting": False, "pia": True, "ladd": False}),
        (8, {"military": False, "interesting": False, "pia": False, "ladd": True}),
        (15, {"military": True, "interesting": True, "pia": True, "ladd": True}),
        ("3", {"military": True, "interesting": True, "pia": False, "ladd": False}),
    ])
    def test_bits(self, value: Any, expected: dict[str, bool]) -> None:
        flags = aviation.decode_db_flags(value)
        assert flags is not None
        assert {key: flags[key] for key in expected} == expected
        assert flags["raw"] == int(float(value))

    @pytest.mark.parametrize("value", [None, -1, "abc", True, float("nan")])
    def test_invalid(self, value: Any) -> None:
        assert aviation.decode_db_flags(value) is None


class TestGeometry:
    def test_london_new_york(self) -> None:
        distance = aviation.haversine_km(51.47, -0.4543, 40.6413, -73.7781)
        assert distance == pytest.approx(5555, abs=25)

    def test_same_point_is_zero(self) -> None:
        assert aviation.haversine_km(40.0, -3.0, 40.0, -3.0) == pytest.approx(0.0)

    @pytest.mark.parametrize("args", [
        (None, 0, 0, 0), (91, 0, 0, 0), (0, 181, 0, 0), (0, 0, "x", 0),
    ])
    def test_invalid(self, args: tuple[Any, Any, Any, Any]) -> None:
        assert aviation.haversine_km(*args) is None

    def test_bbox_centre_and_radius(self) -> None:
        geometry = aviation.bbox_center_radius((-3.8, 40.3, -3.5, 40.6))
        assert geometry is not None
        centre_lat, centre_lon, radius_nm = geometry
        assert centre_lat == pytest.approx(40.45)
        assert centre_lon == pytest.approx(-3.65)
        # ~0.3 degrees of latitude/diagonal is roughly 12-17 nm of half-diagonal.
        assert 5 < radius_nm < 30

    @pytest.mark.parametrize("bbox", [
        None, (), (0, 0, 0, 0), (1, 1, 0, 0), (-181, 0, 1, 1), (0, -91, 1, 1),
        ("a", 0, 1, 1),
    ])
    def test_bad_bbox(self, bbox: Any) -> None:
        assert aviation.bbox_center_radius(bbox) is None

    def test_point_in_bbox(self) -> None:
        assert aviation.point_in_bbox(40.0, -3.0, (-4, 39, -2, 41)) is True
        assert aviation.point_in_bbox(38.0, -3.0, (-4, 39, -2, 41)) is False
        assert aviation.point_in_bbox(None, -3.0, (-4, 39, -2, 41)) is False
        assert aviation.point_in_bbox(40.0, -3.0, None) is False


class TestHexdb:
    def test_aircraft_record(self) -> None:
        record = aviation.normalize_hexdb_aircraft({
            "ModeS": "3C6444",
            "Registration": "D-AIBD",
            "Manufacturer": "Airbus",
            "ICAOTypeCode": "A319",
            "Type": "A319 112",
            "RegisteredOwners": "Lufthansa",
            "OperatorFlagCode": "DLH",
        })
        assert record["kind"] == "aircraft"
        assert record["icao24"] == "3c6444"
        assert record["registration"] == "D-AIBD"
        assert record["type_code"] == "A319"
        assert record["owner"] == "Lufthansa"
        assert record["aircraft_class"] == aviation.CLASS_AIRLINER

    def test_missing_aircraft_is_empty(self) -> None:
        assert aviation.normalize_hexdb_aircraft(
            {"status": "404", "error": "Aircraft not found."}
        ) == {}
        assert aviation.normalize_hexdb_aircraft({}) == {}
        assert aviation.normalize_hexdb_aircraft(None) == {}

    def test_route_record(self) -> None:
        record = aviation.normalize_hexdb_route({
            "flight": "IBE31", "route": "EGLL-LEMD", "updatetime": 1680676201,
        })
        assert record["kind"] == "flightroute"
        assert record["callsign"] == "IBE31"
        assert record["origin"] == "EGLL"
        assert record["destination"] == "LEMD"
        assert record["updated_at"] == pytest.approx(1680676201.0)

    def test_route_without_airports(self) -> None:
        record = aviation.normalize_hexdb_route({"flight": "IBE31", "route": "-"})
        assert record["callsign"] == "IBE31"
        assert record["origin"] is None
        assert record["destination"] is None

    @pytest.mark.parametrize("payload", [None, "x", 42, [], {}, {"status": "500"}])
    def test_total_contract(self, payload: Any) -> None:
        assert isinstance(aviation.normalize_hexdb_aircraft(payload), dict)
        assert isinstance(aviation.normalize_hexdb_route(payload), dict)
