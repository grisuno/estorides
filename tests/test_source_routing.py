"""M2 RED tests: alias routing + phone/mac YAML backfill."""
from __future__ import annotations

from pathlib import Path

import yaml

from estorides_core.orchestrator import Orchestrator

ROOT = Path(__file__).resolve().parent.parent


def _names(types: str) -> set[str]:
    orch = Orchestrator.__new__(Orchestrator)
    import estorides_core.orchestrator as oc

    reg = oc.SourceRegistry(ROOT / "sources")
    reg.load()
    orch.registry = reg
    out = orch._select_sources(
        None, include_paid=True, query_type=types, max_contact=None
    )
    return {s["name"] for s in out}


def test_phone_routes_to_phone_tools() -> None:
    names = _names("phone")
    assert "kali_phoneinfoga" in names
    assert "kali_phonefy" in names


def test_mac_routes_to_macvendors() -> None:
    assert "macvendors_lookup" in _names("mac")


def test_hash_alias_matches_concrete() -> None:
    names = _names("hash")
    assert names & {"malwarebazaar_hash", "threatfox_iocs"} or any(
        "hash" in n or "malware" in n or "threatfox" in n for n in names
    )


def test_url_also_matches_domain_sources() -> None:
    assert "crt_sh_certificates" in _names("url")


def test_phone_yaml_tags() -> None:
    for tool in ("kali_phoneinfoga", "kali_phonefy"):
        d = yaml.safe_load(
            (ROOT / "sources" / "20_system_tools" / f"{tool}.yaml").read_text()
        )
        assert "phone" in (d.get("applies_to") or [])


def test_bare_hex_routes_to_aircraft_lookups() -> None:
    """`estorides run 400a1b` detects `username`, so aircraft sources
    must opt into that tag or a hex query only reaches social profiles."""
    from estorides_core.entity_extraction import detect_query_type

    names = _names(detect_query_type("400a1b"))
    assert "adsblol_aircraft_by_hex" in names
    assert "hexdb_aircraft_lookup" in names
    assert "adsbdb_aircraft_lookup" in names


def test_callsign_and_type_route_to_adsblol() -> None:
    from estorides_core.entity_extraction import detect_query_type

    names = _names(detect_query_type("BAW123"))
    assert "adsblol_aircraft_by_callsign" in names
    assert "hexdb_route_lookup" in names
    names = _names(detect_query_type("A400"))
    assert "adsblol_aircraft_by_type" in names
    names = _names(detect_query_type("7700"))
    assert "adsblol_emergency_squawk" in names
