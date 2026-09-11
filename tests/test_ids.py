"""
BDD tests for the shared deterministic id helper (spec/ids.md).

  - ID1: deterministic and content-addressed
  - ID2: length is honoured
  - ID3: different payloads do not collide in the 16-char space (smoke)
"""
from __future__ import annotations

import hashlib

from estorides_core.ids import stable_id


class TestID1Determinism:
    def test_same_payload_same_id(self) -> None:
        assert stable_id("domain:example.com") == stable_id("domain:example.com")

    def test_matches_legacy_formula(self) -> None:
        payload = "domain:example.com"
        legacy = hashlib.sha1(
            payload.encode("utf-8"), usedforsecurity=False
        ).hexdigest()[:16]
        assert stable_id(payload) == legacy


class TestID2Length:
    def test_length_honoured(self) -> None:
        assert len(stable_id("x", length=8)) == 8
        assert len(stable_id("x")) == 16


class TestID3Distinct:
    def test_distinct_payloads(self) -> None:
        assert stable_id("domain:a.com") != stable_id("domain:b.com")
