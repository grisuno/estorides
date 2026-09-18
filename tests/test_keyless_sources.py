"""M3 RED tests: keyless BGPView + CISA KEV sources and total parsers."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _registry() -> dict:
    import estorides_core.orchestrator as oc

    reg = oc.SourceRegistry(ROOT / "sources")
    reg.load()
    return {s["name"]: s for s in reg.all()}


def test_bgpview_ip_source() -> None:
    reg = _registry()
    src = reg["bgpview_ip"]
    assert src["requires_key"] is False
    assert "ipv4" in src["applies_to"]
    assert "bgpview.io/ip" in src["tool"]["url"]


def test_bgpview_asn_source() -> None:
    reg = _registry()
    src = reg["bgpview_asn"]
    assert src["requires_key"] is False
    assert "asn" in src["applies_to"]


def test_cisa_kev_source() -> None:
    reg = _registry()
    src = reg["cisa_kev_recent"]
    assert src["requires_key"] is False
    assert "cve" in src["applies_to"]


def test_parse_bgpview_extracts() -> None:
    from estorides_core.parsers import get_parser

    p = get_parser("bgpview")
    out = p({
        "status": "ok",
        "data": {
            "prefixes": [{"prefix": "1.2.3.0/24", "asn": {"asn": 13335}}],
            "rir_allocation": {"rir_name": "RIPE", "prefix": "1.2.0.0/16"},
        },
    })
    assert out["prefixes"] and out["asns"] == [13335]


def test_parsers_total_on_hostile_input() -> None:
    from estorides_core.parsers import get_parser

    for name in ("bgpview", "cisa_kev"):
        p = get_parser(name)
        for bad in (None, "x", 42, [], {"status": "error"}, {"data": None}):
            assert p(bad) is not None


def test_parse_cisa_kev_extracts() -> None:
    from estorides_core.parsers import get_parser

    p = get_parser("cisa_kev")
    out = p({
        "vulnerabilities": [{
            "cveID": "CVE-2021-44228", "vendorProject": "Apache",
            "product": "Log4j2", "vulnerabilityName": "Log4Shell",
            "dateAdded": "2021-12-10", "dueDate": "2021-12-24",
        }],
    })
    assert out["total"] == 1
    assert out["vulnerabilities"][0]["cveID"] == "CVE-2021-44228"
