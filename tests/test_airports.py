"""
BDD tests for :mod:`estorides_core.airports`.

The catalogue is a plain CSV, so the tests are the parser and the index:
what gets dropped, which identifier answers, and how close "near" is.
"""
from __future__ import annotations

from typing import Any

import pytest

from estorides_core import airports

HEADER = (
    "id,ident,type,name,latitude_deg,longitude_deg,elevation_ft,continent,"
    "iso_country,iso_region,municipality,scheduled_service,gps_code,iata_code,"
    "local_code,home_link,wikipedia_link,keywords\n"
)

CSV_TEXT = HEADER + (
    '1,LEMD,large_airport,Adolfo Suarez Madrid-Barajas,40.4719,-3.5626,1998,'
    'EU,ES,ES-MD,Madrid,yes,LEMD,MAD,MAD,,,madrid barajas\n'
    '2,LEBL,large_airport,Barcelona El Prat,41.2971,2.0785,12,EU,ES,ES-CT,'
    'Barcelona,yes,LEBL,BCN,BCN,,,barcelona\n'
    '3,LECU,medium_airport,Cuatro Vientos,40.3707,-3.7852,2269,EU,ES,ES-MD,'
    'Madrid,no,LECU,,\n'
    '4,HELI,heliport,Private Helipad,40.45,-3.60,2000,EU,ES,ES-MD,Madrid,no,,,\n'
    '5,BAD,small_airport,Broken coordinates,not-a-number,-3.6,0,EU,ES,ES-MD,'
    'Nowhere,no,,,\n'
    '6,LEMD,large_airport,Duplicate Ident,40.0,-3.0,0,EU,ES,ES-MD,Madrid,no,,,\n'
)


class TestParse:
    def test_filters_and_dedupes(self) -> None:
        parsed = airports.parse_airports_csv(CSV_TEXT)
        idents = [airport["ident"] for airport in parsed]
        assert idents == ["LEMD", "LEBL", "LECU"]

    def test_normalisation(self) -> None:
        madrid = airports.parse_airports_csv(CSV_TEXT)[0]
        assert madrid["icao"] == "LEMD"
        assert madrid["iata"] == "MAD"
        assert madrid["name"] == "Adolfo Suarez Madrid-Barajas"
        assert madrid["latitude"] == pytest.approx(40.4719)
        assert madrid["longitude"] == pytest.approx(-3.5626)
        assert madrid["elevation_ft"] == pytest.approx(1998.0)
        assert madrid["country"] == "ES"
        assert madrid["region"] == "ES-MD"
        assert madrid["municipality"] == "Madrid"
        assert madrid["scheduled_service"] is True

    def test_type_filter(self) -> None:
        parsed = airports.parse_airports_csv(CSV_TEXT, types=("large_airport",))
        assert [airport["ident"] for airport in parsed] == ["LEMD", "LEBL"]

    def test_limit(self) -> None:
        assert len(airports.parse_airports_csv(CSV_TEXT, limit=1)) == 1
        assert airports.parse_airports_csv(CSV_TEXT, limit=0) != []

    @pytest.mark.parametrize("text", [None, "", 42, "not,csv\n"])
    def test_hostile_input(self, text: Any) -> None:
        assert isinstance(airports.parse_airports_csv(text), list)


class TestIndex:
    @pytest.fixture()
    def index(self) -> airports.AirportIndex:
        return airports.build_index(airports.parse_airports_csv(CSV_TEXT))

    def test_nearest_within_radius(self, index: airports.AirportIndex) -> None:
        near = index.nearest(40.45, -3.60, max_km=25)
        assert near is not None
        assert near["ident"] == "LEMD"
        assert near["distance_km"] < 10

    def test_nearest_none_when_far(self, index: airports.AirportIndex) -> None:
        assert index.nearest(10.0, 10.0, max_km=25) is None

    def test_nearest_respects_radius(self, index: airports.AirportIndex) -> None:
        # Madrid-Barajas is ~4 km from this point; a 2 km cap excludes it.
        assert index.nearest(40.45, -3.60, max_km=2) is None

    @pytest.mark.parametrize("args", [
        (None, 0), (95, 0), (0, 200), (0, 0, None), (0, 0, 0), (0, 0, -1),
    ])
    def test_nearest_hostile(self, index: airports.AirportIndex,
                             args: tuple[Any, ...]) -> None:
        assert index.nearest(*args) is None

    def test_by_code(self, index: airports.AirportIndex) -> None:
        assert index.by_code("LEMD")["iata"] == "MAD"
        assert index.by_code("mad")["ident"] == "LEMD"
        assert index.by_code("lecu")["municipality"] == "Madrid"
        assert index.by_code("ZZZZ") is None
        assert index.by_code(None) is None

    def test_within_bbox(self, index: airports.AirportIndex) -> None:
        inside = index.within_bbox((-4.0, 40.0, -3.0, 41.0))
        assert {airport["ident"] for airport in inside} == {"LEMD", "LECU"}
        assert index.within_bbox(None) == []
        assert index.within_bbox((0, 0)) == []

    def test_len_and_empties(self) -> None:
        assert len(airports.build_index([])) == 0
        assert len(airports.build_index([{"latitude": 1.0}])) == 0

    def test_brief(self) -> None:
        near = airports.build_index(airports.parse_airports_csv(CSV_TEXT)).nearest(
            40.45, -3.60, max_km=25
        )
        brief = airports.airport_brief(near)
        assert brief is not None
        assert brief["ident"] == "LEMD"
        assert brief["icao"] == "LEMD"
        assert brief["iata"] == "MAD"
        assert "distance_km" in brief
        assert airports.airport_brief(None) is None
