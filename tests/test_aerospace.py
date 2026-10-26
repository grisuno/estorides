"""
BDD tests for spec/aerospace.md.

Covers the pure TLE/orbit helpers, the aircraft and launch normalisers,
the four map feeds, the seven query sources and the /api/feeds
whitelist. Each scenario id (A1..A14) matches the spec.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from estorides_core import aerospace
from estorides_core import feeds as feed_module

ROOT = Path(__file__).resolve().parent.parent

ISS_LINE1 = "1 25544U 98067A   24001.50000000  .00016717  00000+0  30777-3 0  9994"
ISS_LINE2 = "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.50000000431234"

# A second satellite (GEO) used for dedupe and multi-set parsing.
GEO_LINE1 = "1 28884U 05041A   24001.50000000  .00000000  00000+0  00000+0 0  9990"
GEO_LINE2 = "2 28884   0.0180  94.3177 0001856 282.2612  77.7428  1.00271798 67623"


def _iss_epoch() -> float:
    epoch = aerospace.tle_epoch_unix(ISS_LINE1)
    assert epoch is not None
    return epoch


class TestA1TleParsing:
    def test_malformed_set_is_skipped(self) -> None:
        text = "\n".join([
            "ISS (ZARYA)", ISS_LINE1, ISS_LINE2,
            "BROKEN SET", "1 99999U 24001A", "not a tle line",
            "GEO SAT", GEO_LINE1, GEO_LINE2,
        ])
        parsed = aerospace.parse_tle_catalog(text)
        assert [item["norad_id"] for item in parsed] == [25544, 28884]

    def test_raw_text_envelope_and_duplicates(self) -> None:
        text = "\n".join([ISS_LINE1, ISS_LINE2, "ISS AGAIN", ISS_LINE1, ISS_LINE2])
        text = "ISS (ZARYA)\n" + text
        parsed = aerospace.parse_tle_catalog({"raw_text": text})
        assert len(parsed) == 1
        assert parsed[0]["name"] == "ISS (ZARYA)"
        assert parsed[0]["line1"] == ISS_LINE1

    def test_missing_trailing_set_returns_empty(self) -> None:
        assert aerospace.parse_tle_catalog("ONLY\n1 25544U 98067A") == []


class TestA2AlphaFive:
    def test_alpha5_decoding(self) -> None:
        assert aerospace.decode_catalog_field("A0000") == 100000
        assert aerospace.decode_catalog_field("Z9999") == 339999
        assert aerospace.decode_catalog_field("25544") == 25544

    def test_alpha5_rejects_i_o_and_bad_shapes(self) -> None:
        for bad in ("I0000", "O0000", "a0000", "A00", "A00000", "1.234", " 25544a"):
            assert aerospace.decode_catalog_field(bad) is None

    def test_catalog_number_reads_columns_three_to_seven(self) -> None:
        assert aerospace.tle_catalog_number(ISS_LINE1) == 25544
        assert aerospace.tle_catalog_number(ISS_LINE2) == 25544
        assert aerospace.tle_catalog_number("short") is None


class TestA3SubsatellitePoint:
    def test_iss_point_is_physical(self) -> None:
        point = aerospace.subsatellite_point(
            ISS_LINE1, ISS_LINE2, _iss_epoch() + 60
        )
        assert point is not None
        assert -90.0 <= point["latitude"] <= 90.0
        assert -180.0 <= point["longitude"] <= 180.0
        assert 300.0 <= point["altitude_km"] <= 500.0
        assert point["velocity_kms"] > 7.0

    def test_kepler_fallback_returns_a_point(self) -> None:
        point = aerospace.kepler_subsatellite_point(
            ISS_LINE1, ISS_LINE2, _iss_epoch() + 60
        )
        assert point is not None
        assert point["propagator"] == "kepler"

    def test_invalid_inputs_return_none(self) -> None:
        assert aerospace.subsatellite_point("", "", 0) is None
        assert aerospace.subsatellite_point(ISS_LINE1, ISS_LINE2, "soon") is None
        assert aerospace.eci_to_geodetic([1, 2], 0) is None
        assert aerospace.eci_to_geodetic([0, 0, 0], 0) is None


class TestA4Sgp4Agreement:
    def test_sgp4_and_kepler_agree_near_epoch(self) -> None:
        pytest.importorskip("sgp4")
        moment = _iss_epoch() + 60
        sgp4_point = aerospace._sgp4_point(ISS_LINE1, ISS_LINE2, moment)
        kepler_point = aerospace.kepler_subsatellite_point(
            ISS_LINE1, ISS_LINE2, moment
        )
        assert sgp4_point is not None and kepler_point is not None
        delta_lat = abs(sgp4_point["latitude"] - kepler_point["latitude"])
        delta_lon = abs(sgp4_point["longitude"] - kepler_point["longitude"])
        assert delta_lat < 1.0
        assert delta_lon < 1.0


class TestTleElements:
    def test_mean_elements(self) -> None:
        elements = aerospace.tle_mean_elements(ISS_LINE1, ISS_LINE2)
        assert elements is not None
        assert elements["inclination_deg"] == pytest.approx(51.6416)
        assert elements["eccentricity"] == pytest.approx(0.0006703)
        assert elements["mean_motion_rev_day"] == pytest.approx(15.5)

    def test_epoch_decodes_two_digit_year(self) -> None:
        epoch = aerospace.tle_epoch_unix(ISS_LINE1)
        assert epoch is not None
        assert 1704067200.0 <= epoch <= 1704153600.0

    def test_bad_elements_return_none(self) -> None:
        assert aerospace.tle_mean_elements("bad", "bad") is None
        assert aerospace.tle_mean_elements(ISS_LINE1, ISS_LINE2[:40]) is None

def _opensky_payload() -> dict[str, Any]:
    return {
        "time": 1700000000,
        "states": [
            ["abc123", "UAL123  ", "United States", 1699999990, 1699999995,
             -73.78, 40.64, 10000.0, False, 250.0, 90.0, 1.5, None,
             10100.0, "1200", False, 0, 3],
            ["def456", "BAW1    ", "United Kingdom", 1699999990, 1699999995,
             "not-a-number", 51.5, 9000.0, False, 200.0, 180.0, 0.0,
             None, 9000.0, "7000", False, 0, 4],
            ["abc123", "DUP     ", "United States", 1699999990, 1699999995,
             -73.0, 40.0, 10000.0, False, 250.0, 90.0, 1.5, None,
             10100.0, "1200", False, 0, 3],
            ["badrow"],
        ],
    }


class TestA5OpenSky:
    def test_only_valid_and_unique_vectors_survive(self) -> None:
        records = aerospace.normalize_opensky_states(_opensky_payload())
        assert len(records) == 1
        record = records[0]
        assert record["icao24"] == "abc123"
        assert record["callsign"] == "UAL123"
        assert record["latitude"] == pytest.approx(40.64)
        assert record["longitude"] == pytest.approx(-73.78)
        assert record["baro_altitude_m"] == pytest.approx(10000.0)
        assert record["velocity_mps"] == pytest.approx(250.0)
        assert record["observed_at"] == pytest.approx(1699999995)
        assert record["source"] == "opensky"

    def test_out_of_range_coordinates_are_dropped(self) -> None:
        payload = {"states": [
            ["aaa111", "X", "Y", 0, 0, 181.0, 0.0, None, False, None, None,
             None, None, None, None, False, 0, 0],
            ["bbb222", "X", "Y", 0, 0, 0.0, 91.0, None, False, None, None,
             None, None, None, None, False, 0, 0],
        ]}
        assert aerospace.normalize_opensky_states(payload) == []


class TestA6AdsbLol:
    def test_units_are_converted(self) -> None:
        payload = {"now": 1700000000, "ac": [{
            "hex": "ABC123", "flight": "UAL123 ", "lat": 40.0, "lon": -73.0,
            "alt_baro": 30000, "alt_geom": 31000, "gs": 400.0, "track": 90.0,
            "baro_rate": 1000.0, "seen_pos": 2.0, "squawk": "1200",
            "category": "A3",
        }]}
        record = aerospace.normalize_adsblol_aircraft(payload)[0]
        assert record["icao24"] == "abc123"
        assert record["baro_altitude_m"] == pytest.approx(30000 * 0.3048)
        assert record["geo_altitude_m"] == pytest.approx(31000 * 0.3048)
        assert record["velocity_mps"] == pytest.approx(400.0 * 0.514444)
        assert record["vertical_rate_mps"] == pytest.approx(1000.0 * 0.00508)
        assert record["observed_at"] == pytest.approx(1699999998)
        assert record["category"] == 4
        assert record["source"] == "adsb.lol"

    def test_ground_state_has_no_barometric_altitude(self) -> None:
        payload = {"now": 1700000000000, "ac": [{
            "hex": "abc123", "lat": 40.0, "lon": -73.0, "alt_baro": "ground",
        }]}
        record = aerospace.normalize_adsblol_aircraft(payload)[0]
        assert record["on_ground"] is True
        assert record["baro_altitude_m"] is None


class TestA7Adsbdb:
    def test_aircraft_shape(self) -> None:
        payload = {"response": {"aircraft": {
            "mode_s": "400A1B", "registration": "G-ABCD", "icao_type": "B738",
            "manufacturer": "Boeing", "type": "737-8K5",
            "registered_owner": "Test Air", "registered_owner_country_name": "UK",
        }}}
        out = aerospace.normalize_adsbdb(payload)
        assert out["kind"] == "aircraft"
        assert out["registration"] == "G-ABCD"
        assert out["owner"] == "Test Air"

    def test_flightroute_shape(self) -> None:
        payload = {"response": {"flightroute": {
            "callsign": "BAW123",
            "airline": {"name": "British Airways", "icao": "BAW"},
            "origin": {"iata": "LHR", "name": "London Heathrow"},
            "destination": {"iata": "JFK", "name": "New York JFK"},
        }}}
        out = aerospace.normalize_adsbdb(payload)
        assert out["kind"] == "flightroute"
        assert out["origin"] == "LHR"
        assert out["destination"] == "JFK"
        assert out["airline"] == "British Airways"


class TestA8LaunchLibrary:
    def test_pad_coordinates_and_context(self) -> None:
        payload = {"results": [{
            "id": "abc-1", "name": "Falcon 9 | Starlink",
            "net": "2026-01-01T00:00:00Z",
            "status": {"abbrev": "Go"},
            "launch_service_provider": {"name": "SpaceX"},
            "rocket": {"configuration": {"full_name": "Falcon 9 Block 5"}},
            "pad": {"name": "SLC-40", "latitude": "28.5619", "longitude": "-80.5772",
                    "location": {"name": "Cape Canaveral"}},
            "mission": {"name": "Starlink Group", "orbit": {"name": "LEO"}},
        }]}
        launch = aerospace.normalize_launch_library(payload)[0]
        assert launch["latitude"] == pytest.approx(28.5619)
        assert launch["longitude"] == pytest.approx(-80.5772)
        assert launch["status"] == "Go"
        assert launch["provider"] == "SpaceX"
        assert launch["rocket"] == "Falcon 9 Block 5"
        assert launch["orbit"] == "LEO"

    def test_missing_pad_keeps_schedule_entry(self) -> None:
        payload = {"results": [{"id": "x", "name": "No pad"}]}
        launch = aerospace.normalize_launch_library(payload)[0]
        assert launch["latitude"] is None
        assert launch["longitude"] is None


class TestA9TotalContract:
    HOSTILE = [None, "x", 42, [], {}, ["row"], {"states": "nope"}, {"ac": [1]},
               {"response": None}, {"results": "nope"}]

    @pytest.mark.parametrize("payload", HOSTILE)
    def test_normalisers_are_total(self, payload: Any) -> None:
        assert aerospace.normalize_opensky_states(payload) == []
        assert aerospace.normalize_adsblol_aircraft(payload) == []
        assert aerospace.normalize_launch_library(payload) == []
        assert isinstance(aerospace.normalize_adsbdb(payload), dict)
        assert isinstance(aerospace.normalize_opensky_track(payload), dict)
        assert isinstance(aerospace.parse_tle_catalog(payload), list)

    def test_cap_records(self) -> None:
        records = [{"n": 1}, {"n": 2}, {"n": 3}, "not-a-dict"]
        assert aerospace.cap_records(records, 2) == [{"n": 1}, {"n": 2}]
        assert aerospace.cap_records(records, 0) == []
        assert aerospace.cap_records(records, -5) == []
        assert aerospace.cap_records(records, 100) == [{"n": 1}, {"n": 2}, {"n": 3}]
        assert aerospace.cap_records(None, 5) == []


class _FakeResponse:
    def __init__(self, payload: Any = None, text: str = "", status: int = 200) -> None:
        self._payload = payload
        self.text = text
        self.status_code = status

    def json(self) -> Any:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def _patch_requests(monkeypatch: pytest.MonkeyPatch, by_url: dict[str, _FakeResponse]) -> list[str]:
    calls: list[str] = []

    def fake_get(url: str, **kwargs: Any) -> _FakeResponse:
        calls.append(url)
        for prefix, response in by_url.items():
            if url.startswith(prefix):
                return response
        return _FakeResponse(status=404)

    monkeypatch.setattr("requests.get", fake_get)
    return calls


class TestA10AircraftFeed:
    def test_two_points(self, monkeypatch: pytest.MonkeyPatch) -> None:
        _patch_requests(monkeypatch, {
            "https://opensky-network.org": _FakeResponse(payload={
                "time": 1700000000,
                "states": [
                    ["abc123", "UAL123", "US", 1699999990, 1699999995,
                     -73.0, 40.0, 9000.0, False, 240.0, 90.0, 0.0, None,
                     9000.0, "1200", False, 0, 3],
                    ["def456", "BAW1", "UK", 1699999990, 1699999995,
                     -0.1, 51.5, 8000.0, False, 230.0, 270.0, 0.0, None,
                     8000.0, "7000", False, 0, 3],
                ],
            }),
        })
        points = feed_module.AircraftFeed()._fetch()
        assert len(points) == 2
        assert {point.kind for point in points} == {"aircraft"}
        assert {point.label for point in points} == {"UAL123", "BAW1"}
        assert all(-180 <= point.lon <= 180 for point in points)

    def test_cap_is_honoured(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("ESTORIDES_AIRCRAFT_MAX", "1")
        _patch_requests(monkeypatch, {
            "https://opensky-network.org": _FakeResponse(payload=_opensky_payload()),
        })
        assert len(feed_module.AircraftFeed()._fetch()) == 1


class TestA11SatellitesFeed:
    def test_deduplicates_and_survives_bad_tle(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("ESTORIDES_SATELLITES_GROUPS", "stations,visual")
        catalog = "\n".join([
            "ISS (ZARYA)", ISS_LINE1, ISS_LINE2,
            "BROKEN", "1 00000U", "2 11111U",
        ])
        _patch_requests(monkeypatch, {
            "https://celestrak.org": _FakeResponse(text=catalog),
        })
        points = feed_module.SatellitesFeed()._fetch()
        assert len(points) == 1
        assert points[0].kind == "satellite"
        assert points[0].extra["norad_id"] == 25544
        assert points[0].extra["propagator"] in {"sgp4", "kepler"}

    def test_one_failing_group_does_not_kill_the_layer(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("ESTORIDES_SATELLITES_GROUPS", "stations")

        def fake_get(url: str, **kwargs: Any) -> _FakeResponse:
            return _FakeResponse(status=503)

        monkeypatch.setattr("requests.get", fake_get)
        assert feed_module.SatellitesFeed()._fetch() == []


class TestA12LaunchesFeed:
    def test_only_located_launches_become_points(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        payload = {"results": [
            {"id": "a", "name": "No pad", "pad": {}},
            {"id": "b", "name": "Cape launch", "pad": {
                "name": "SLC-40", "latitude": "28.5", "longitude": "-80.5",
            }},
        ]}
        _patch_requests(monkeypatch, {
            "https://ll.thespacedevs.com": _FakeResponse(payload=payload),
        })
        points = feed_module.RocketLaunchesFeed()._fetch()
        assert len(points) == 1
        assert points[0].label == "Cape launch"
        assert points[0].kind == "launch"


class TestFeedRegistry:
    def test_all_aerospace_feeds_registered(self) -> None:
        assert {"aircraft", "military_aircraft", "satellites",
                "rocket_launches"}.issubset(feed_module.FEEDS)

    def test_attribution_is_exposed(self) -> None:
        listed = {feed["name"]: feed for feed in feed_module.list_feeds()}
        assert "OpenSky" in listed["aircraft"]["attribution"]
        assert "adsb.lol" in listed["military_aircraft"]["attribution"]
        assert "CelesTrak" in listed["satellites"]["attribution"]
        assert "Launch Library" in listed["rocket_launches"]["attribution"]

    def test_fetch_all_names_filter(self, monkeypatch: pytest.MonkeyPatch) -> None:
        requested: list[str] = []

        class _Stub:
            def __init__(self, name: str) -> None:
                self.name = name
                self.attribution = ""
                self.description = ""

            def fetch(self, *, use_cache: bool = True) -> list[Any]:
                requested.append(self.name)
                return []

        monkeypatch.setattr(feed_module, "FEEDS", {
            "aircraft": _Stub("aircraft"),
            "satellites": _Stub("satellites"),
        })
        out = feed_module.fetch_all(names=["satellites"])
        assert list(out) == ["satellites"]
        assert requested == ["satellites"]


AEROSPACE_SOURCES = {
    "celestrak_satellite_by_catalog": "celestrak_tle",
    "celestrak_satellite_by_name": "celestrak_tle",
    "celestrak_group_catalog": "celestrak_tle",
    "adsbdb_aircraft_lookup": "adsbdb",
    "adsbdb_callsign_lookup": "adsbdb",
    "opensky_aircraft_track": "opensky_track",
    "launch_library_search": "launch_library",
}


class TestAerospaceSources:
    def _registry(self) -> dict[str, Any]:
        from estorides_core.source_loader import SourceRegistry

        registry = SourceRegistry(ROOT / "sources")
        registry.load()
        return {source["name"]: source for source in registry.all()}

    def test_every_source_loads_with_expected_contract(self) -> None:
        registry = self._registry()
        for name, parser in AEROSPACE_SOURCES.items():
            source = registry[name]
            assert source["category"] == "21. Aerospace"
            assert source["contact"] == "none"
            assert source["requires_key"] is False
            assert source["parser"] == parser
            assert source["tool"]["url"].startswith("https://")

    def test_category_directory_matches_label(self) -> None:
        directory = ROOT / "sources" / "21_aerospace"
        assert directory.is_dir()
        names = {path.stem for path in directory.glob("*.yaml")}
        assert names == set(AEROSPACE_SOURCES)

    def test_every_parser_is_registered(self) -> None:
        from estorides_core.parsers import PARSERS, get_parser

        for parser in set(AEROSPACE_SOURCES.values()):
            assert parser in PARSERS
            assert callable(get_parser(parser))


class TestAerospaceParsers:
    def test_celestrak_parser(self) -> None:
        from estorides_core.parsers import get_parser

        out = get_parser("celestrak_tle")({
            "raw_text": f"ISS (ZARYA)\n{ISS_LINE1}\n{ISS_LINE2}\n",
        })
        assert out["count"] == 1
        assert out["satellites"][0]["norad_id"] == 25544

    def test_opensky_and_adsblol_parsers(self) -> None:
        from estorides_core.parsers import get_parser

        opensky = get_parser("opensky_states")(_opensky_payload())
        assert opensky["count"] == 1
        adsblol = get_parser("adsblol_aircraft")({"ac": [{
            "hex": "abc123", "lat": 1.0, "lon": 2.0,
        }]})
        assert adsblol["count"] == 1

    def test_adsbdb_and_launch_parsers(self) -> None:
        from estorides_core.parsers import get_parser

        aircraft = get_parser("adsbdb")({"response": {"aircraft": {
            "mode_s": "400A1B", "registration": "G-ABCD",
        }}})
        assert aircraft["registration"] == "G-ABCD"
        launches = get_parser("launch_library")({"results": [{
            "id": "x", "pad": {"latitude": "1.0", "longitude": "2.0"},
        }]})
        assert launches["count"] == 1

    @pytest.mark.parametrize("payload", TestA9TotalContract.HOSTILE)
    def test_new_parsers_are_total(self, payload: Any) -> None:
        from estorides_core.parsers import get_parser

        for name in AEROSPACE_SOURCES.values():
            assert get_parser(name)(payload) is not None


class TestA13FeedSelection:
    def _client(self) -> Any:
        from estorides_web import create_app

        app = create_app()
        app.config["TESTING"] = True
        return app.test_client()

    def test_unknown_feed_is_rejected(self) -> None:
        response = self._client().get("/api/feeds?feeds=aircraft,nope")
        assert response.status_code == 400
        body = response.get_json()
        assert body["error"] == "unknown feed"
        assert body["unknown"] == ["nope"]
        assert "aircraft" in body["valid"]


class TestA14Branding:
    def test_no_upstream_project_branding(self) -> None:
        haystack = "\n".join([
            (ROOT / "templates" / "index.html").read_text(encoding="utf-8"),
            (ROOT / "static" / "js" / "estorides.js").read_text(encoding="utf-8"),
        ]).lower()
        for banned in ("gods-eye-view", "god's eye view", "godseye", "gods eye"):
            assert banned not in haystack

    def test_panel_is_branded_estorides(self) -> None:
        html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
        assert 'id="estorides-aero-panel"' in html
        assert "Estorides Aerospace" in html

