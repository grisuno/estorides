"""
BDD / regression tests for the remote-JSON parser layer.

Doctrine (`parsers.py` header): every parser MUST be total — any
unrecognised input returns an empty container, never raises. The
orchestrator trusts that contract, so a remote source returning
`null` where an object is expected must not abort a run.

  - P1: known malformed payloads return empty containers, no raise
  - P2: valid payloads still parse (no over-eager guard regression)
"""
from __future__ import annotations

import pytest

from estorides_core import parsers


class TestP1Totality:
    """Given a remote payload with nulls/strings where objects belong."""

    @pytest.mark.parametrize("parser_name,payload", [
        ("parse_otx", {"results": [None, {"id": 1, "indicators": None}, "x"]}),
        ("parse_otx", {"results": None}),
        ("parse_keybase", {"them": [{
            "basics": None, "profile": None,
            "proofs_summary": {"twitter": [None]},
            "public_keys": None, "devices": [{"device": None}, None],
        }]}),
        ("parse_keybase", None),
        ("parse_ethplorer", {"tokens": [None, {"tokenInfo": None, "balance": 1}, "z"]}),
        ("parse_github_advisories", [{"vulnerabilities": [None, {"package": None}]}]),
        ("parse_wayback_cdx", ["not-a-header", ["a", "b"]]),
    ])
    def test_parser_is_total(self, parser_name: str, payload: object) -> None:
        fn = getattr(parsers, parser_name)
        fn(payload)  # must not raise

    def test_otx_null_entry_skipped(self) -> None:
        out = parsers.parse_otx({"results": [None, {"id": "p1"}]})
        assert [p["id"] for p in out["pulses"]] == ["p1"]

    def test_keybase_missing_them(self) -> None:
        assert parsers.parse_keybase({"them": []}) == {"error": "no result"}

    def test_wayback_non_list_header(self) -> None:
        assert parsers.parse_wayback_cdx(["nope", ["a"]]) == []


class TestP2NoRegression:
    def test_otx_valid(self) -> None:
        out = parsers.parse_otx({"count": 1, "results": [{
            "id": "p1", "name": "Pulse", "indicators": [1, 2],
        }]})
        assert out["count"] == 1
        assert out["pulses"][0]["indicators_count"] == 2

    def test_keybase_valid(self) -> None:
        out = parsers.parse_keybase({"them": [{
            "basics": {"username": "alice"},
            "profile": {"full_name": "Alice"},
            "proofs_summary": {"github": [{"service_url": "https://github.com/alice"}]},
            "public_keys": {"primary": [{"key_fingerprint": "FP"}]},
            "devices": [{"device": {"name": "phone"}}],
        }]})
        assert out["username"] == "alice"
        assert out["full_name"] == "Alice"
        assert out["github"] == "https://github.com/alice"
        assert out["public_keys"] == [{"bundle": None, "key_fingerprint": "FP"}]
        assert out["devices"] == [{"name": "phone", "type": None}]

    def test_ethplorer_valid(self) -> None:
        out = parsers.parse_ethplorer({
            "address": "0x1", "countTxs": 5,
            "tokens": [{"tokenInfo": {"symbol": "ETH", "name": "Ether"}, "balance": "10"}],
        })
        assert out["tokens"] == [{"symbol": "ETH", "name": "Ether", "balance": "10"}]
