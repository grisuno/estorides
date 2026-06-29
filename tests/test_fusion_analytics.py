"""ATDD + BDD tests for estorides_core.fusion_analytics.

Implements the Given-When-Then contracts from spec/fusion_analytics.md
(module 2e). Must FAIL at the red step (implementation doesn't exist yet)
and PASS after the green step.

Run from project root:
    .venv/bin/pytest tests/test_fusion_analytics.py -v
"""
from __future__ import annotations

import time
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

from estorides_core.fusion_analytics import FusionAnalytics
from estorides_core.fusion_store import FusionStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def store_and_analytics(tmp_path: Path) -> Generator:
    fs = FusionStore(tmp_path / "test_fusion.sqlite")
    analytics = FusionAnalytics(fs)
    with fs._lock:
        cur = fs._conn
        cur.execute("DELETE FROM fusion_entities")
        cur.execute("DELETE FROM fusion_sources")
        cur.execute("DELETE FROM fusion_properties")
        cur.execute("DELETE FROM fusion_relationships")
        cur.execute("DELETE FROM fusion_entity_sources")
        cur.execute("DELETE FROM fusion_observations")
    yield fs, analytics
    fs.close()


def _populate_evilcorp(store: FusionStore) -> str:
    etype, value = "domain", "evilcorp.com"
    eid = store.fuse_entity({
        "type": etype, "value": value, "confidence": 0.85,
        "sources": ["crtsh_certificates", "dns_google", "ipapi_free"],
    })
    store.fuse_properties(eid, {"country": "RU", "asn": "AS12345"}, "ipapi_free")
    store.fuse_properties(eid, {"country": "RU", "isp": "Rostelecom"}, "ipwhois")
    store.fuse_properties(eid, {"country": "RU"}, "abuseipdb_check")
    store.fuse_properties(eid, {"org": "Evil Corp"}, "hackertarget_whois")
    store.fuse_relationship("domain", "evilcorp.com", "resolves_to", "ipv4", "192.0.2.1", source="dns_google")
    store.fuse_relationship("domain", "evilcorp.com", "registered_with_email", "email", "admin@evilcorp.com", source="hackertarget_whois")
    return eid


def _register_source(store: FusionStore, name: str, **kw: Any) -> None:
    store.register_sources([{"name": name, "category": kw.get("category", "test"), "parser": "", "contact": "none"}])


# ---------------------------------------------------------------------------
# E1 · Happy path: entity_timeline
# ---------------------------------------------------------------------------
class TestEntityTimeline:
    def test_returns_full_timeline(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        eid = _populate_evilcorp(fs)
        result = analytics.entity_timeline(eid)
        assert result is not None
        assert result["entity_id"] == eid
        assert result["type"] == "domain"
        assert result["value"] == "evilcorp.com"
        assert len(result["observations"]) >= 1
        assert len(result["properties"]) >= 2
        assert len(result["relationships"]) >= 2
        assert len(result["source_timeline"]) >= 3
        assert result["first_seen"] <= result["last_seen"]

    def test_nonexistent_eid_returns_none(self, store_and_analytics: Any) -> None:
        _, analytics = store_and_analytics
        assert analytics.entity_timeline("nonexistent") is None


# ---------------------------------------------------------------------------
# E2 · entity_summary
# ---------------------------------------------------------------------------
class TestEntitySummary:
    def test_returns_summary_stats(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        eid = _populate_evilcorp(fs)
        result = analytics.entity_summary(eid)
        assert result is not None
        assert result["entity_id"] == eid
        assert result["type"] == "domain"
        assert result["value"] == "evilcorp.com"
        assert result["source_count"] >= 3
        assert result["properties_summary"]["total"] >= 4
        assert result["relationships_summary"]["total"] >= 2
        assert "country" in result["properties_summary"]["keys"]

    def test_nonexistent_eid_returns_none(self, store_and_analytics: Any) -> None:
        _, analytics = store_and_analytics
        assert analytics.entity_summary("nonexistent") is None


# ---------------------------------------------------------------------------
# E3 · entity_timeline with nonexistent eid
# ---------------------------------------------------------------------------
class TestEntityTimelineNonexistent:
    def test_returns_none(self, store_and_analytics: Any) -> None:
        _, analytics = store_and_analytics
        assert analytics.entity_timeline("does_not_exist") is None


# ---------------------------------------------------------------------------
# E4 · source_stats
# ---------------------------------------------------------------------------
class TestSourceStats:
    def test_returns_source_metrics(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _register_source(fs, "crtsh_certificates", category="web")
        # Bump fetch counters
        with fs._tx() as c:
            c.execute(
                "UPDATE fusion_sources SET fetch_count=100, ok_count=85, last_seen=? WHERE name=?",
                (time.time(), "crtsh_certificates"),
            )
        result = analytics.source_stats("crtsh_certificates")
        assert result is not None
        assert result["source_name"] == "crtsh_certificates"
        assert result["fetch_count"] >= 0
        assert 0.0 <= result["success_rate"] <= 1.0
        assert result["first_seen"] <= result["last_seen"]

    def test_nonexistent_source_returns_none(self, store_and_analytics: Any) -> None:
        _, analytics = store_and_analytics
        assert analytics.source_stats("no_such_source") is None

    def test_success_rate_correct(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _register_source(fs, "test_source", category="test")
        with fs._tx() as c:
            c.execute(
                "UPDATE fusion_sources SET fetch_count=10, ok_count=7 WHERE name=?",
                ("test_source",),
            )
        result = analytics.source_stats("test_source")
        assert result is not None
        assert result["success_rate"] == 0.7


# ---------------------------------------------------------------------------
# E6 · multi_source_consensus
# ---------------------------------------------------------------------------
class TestMultiSourceConsensus:
    def test_consensus_picks_majority_value(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        eid = _populate_evilcorp(fs)
        result = analytics.multi_source_consensus(eid, "country")
        assert result["consensus_value"] == "RU"
        assert result["consensus_strength"] == 1.0  # all 3 sources say RU
        assert len(result["values"]) >= 1
        assert result["total_sources"] >= 2

    def test_nonexistent_key_returns_empty(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        eid = _populate_evilcorp(fs)
        result = analytics.multi_source_consensus(eid, "nonexistent")
        assert result["values"] == []
        assert result["consensus_value"] == ""


# ---------------------------------------------------------------------------
# E8 · corroborated_properties
# ---------------------------------------------------------------------------
class TestCorroboratedProperties:
    def test_filters_by_min_sources(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        eid = _populate_evilcorp(fs)
        result = analytics.corroborated_properties(eid, min_sources=2)
        keys = {r["key"] for r in result}
        assert "country" in keys
        assert "org" not in keys  # only 1 source

    def test_min_sources_one_returns_all(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        eid = _populate_evilcorp(fs)
        result = analytics.corroborated_properties(eid, min_sources=1)
        assert len(result) >= 4


# ---------------------------------------------------------------------------
# E9 · entity_search
# ---------------------------------------------------------------------------
class TestEntitySearch:
    def test_search_by_term(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _populate_evilcorp(fs)
        results = analytics.entity_search("evilcorp")
        assert len(results) >= 1
        for r in results:
            assert "id" in r
            assert "type" in r
            assert "value" in r
            assert "confidence" in r
            assert "source_count" in r

    def test_search_no_results(self, store_and_analytics: Any) -> None:
        _, analytics = store_and_analytics
        results = analytics.entity_search("zzz_nonexistent_yyy")
        assert results == []

    def test_search_filter_by_type(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _populate_evilcorp(fs)
        results = analytics.entity_search("evilcorp", etype="domain")
        assert all(r["type"] == "domain" for r in results)

    def test_search_with_confidence_and_source_filters(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _populate_evilcorp(fs)
        results = analytics.entity_search("evilcorp", min_confidence=0.5, min_sources=2)
        assert all(r["confidence"] >= 0.5 for r in results)
        assert all(r["source_count"] >= 2 for r in results)


# ---------------------------------------------------------------------------
# E11 · top_changed
# ---------------------------------------------------------------------------
class TestTopChanged:
    def test_returns_recently_active_entities(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _populate_evilcorp(fs)
        results = analytics.top_changed(days=365)
        assert len(results) >= 1
        for r in results:
            assert "entity_id" in r
            assert "type" in r
            assert "value" in r

    def test_empty_window_returns_empty(self, store_and_analytics: Any) -> None:
        _, analytics = store_and_analytics
        results = analytics.top_changed(days=1)
        assert results == []


# ---------------------------------------------------------------------------
# E12 · source_corroboration_matrix
# ---------------------------------------------------------------------------
class TestSourceCorroborationMatrix:
    def test_returns_pairs_with_shared_counts(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _register_source(fs, "crtsh_certificates", category="web")
        _register_source(fs, "dns_google", category="dns")
        _register_source(fs, "ipapi_free", category="geo")
        _populate_evilcorp(fs)
        results = analytics.source_corroboration_matrix()
        assert len(results) >= 1
        for r in results:
            assert "source_a" in r
            assert "source_b" in r
            assert r["shared_entities"] >= 0


# ---------------------------------------------------------------------------
# E13 · FusionAnalytics with store=None
# ---------------------------------------------------------------------------
class TestWithNoneStore:
    def test_all_methods_return_empty(self) -> None:
        analytics = FusionAnalytics(None)
        assert analytics.entity_timeline("x") is None
        assert analytics.entity_summary("x") is None
        assert analytics.source_stats("x") is None
        assert analytics.multi_source_consensus("x", "k") == {"values": [], "consensus_value": "", "total_sources": 0, "entity_id": "x", "property_key": "k", "consensus_strength": 0.0}
        assert analytics.corroborated_properties("x") == []
        assert analytics.entity_search("x") == []
        assert analytics.top_changed() == []
        assert analytics.source_corroboration_matrix() == []


class TestBoundaryConditions:
    def test_min_sources_zero_treated_as_one(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        eid = _populate_evilcorp(fs)
        result = analytics.corroborated_properties(eid, min_sources=0)
        assert len(result) >= 4

    def test_negative_days_treated_as_one(self, store_and_analytics: Any) -> None:
        fs, analytics = store_and_analytics
        _populate_evilcorp(fs)
        results = analytics.top_changed(days=-1)
        assert isinstance(results, list)
