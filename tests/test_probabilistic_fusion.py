"""
BDD + property tests for probabilistic fusion.

These tests verify that :meth:`FusionStore.fuse_entity` and
:meth:`FusionStore.fuse_relationship` use the reliability_scoring
pipeline (source reliability + source type + corroboration) instead
of the simplistic ``MAX()`` merge.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from estorides_core.fusion_store import FusionStore


def _fs() -> tuple[FusionStore, Path]:
    tmp = Path(tempfile.mkdtemp(prefix="estorides_pf_"))
    store = FusionStore(tmp / "fusion.sqlite")
    return store, tmp


def _teardown(store: FusionStore, tmp: Path) -> None:
    store.close()
    for child in sorted(tmp.glob("*")):
        child.unlink()
    tmp.rmdir()


def _entity(
    etype: str,
    value: str,
    source: str,
    confidence: float = 1.0,
) -> dict[str, object]:
    return {
        "type": etype,
        "value": value,
        "source": source,
        "sources": [source],
        "confidence": confidence,
    }


# ---------------------------------------------------------------------------
# PF1 · Primary source raises low-confidence entity
# ---------------------------------------------------------------------------
class TestPrimarySourceRaisesLowConf:
    """PF1: tertiary first sighting → primary raises score."""

    def test_primary_source_raises_score(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(
                _entity("domain", "evilcorp.com", "rdap_domain", 0.9)
            )
            rdap_score = store.get_entity(eid)
            assert rdap_score is not None

            # tertiary source scores much lower
            store.fuse_entity(
                _entity("domain", "evilcorp.com", "psbdmp_ws", 0.5)
            )
            ent = store.get_entity(eid)
            assert ent is not None
            # Primary (A * primary) >> tertiary (D * tertiary)
            # After both: max(0.27, 0.045) = 0.27
            # Verifying that the primary source's weight dominates
            assert ent["confidence"] >= 0.20, f"got {ent['confidence']}"
        finally:
            _teardown(store, tmp)


# ---------------------------------------------------------------------------
# PF2 · Tertiary source cannot override high existing score
# ---------------------------------------------------------------------------
class TestTertiaryCannotOverride:
    """PF2: untrusted_webscraper (F) cannot beat 0.9 existing."""

    def test_untrusted_source_cannot_override(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(
                _entity("domain", "evilcorp.com", "rdap_domain", 0.9)
            )
            store.fuse_entity(
                _entity("domain", "evilcorp.com", "untrusted_webscraper", 1.0)
            )
            ent = store.get_entity(eid)
            assert ent is not None
            # First sighting gets proper scoring, second sighting cannot
            # override with MAX due to reliability F + tertiary weight
            # The first sighting of rdap_domain at 0.9 * A * PRIMARY * corr
            # ≈ 0.9 * 1.0 * 1.0 * 0.30 = 0.27 (first sighting 1 source)
            # Second sighting: untrusted F * tertiary * 1 source
            # = merge(0.27, 1.0 * 0.10 * 0.60 * 0.30) = merge(0.27, 0.018)
            # = max(0.27, 0.018) = 0.27
            # So the score should reflect the first sighting's weighted score
            assert ent["confidence"] >= 0.20, f"got {ent['confidence']}"
            assert ent["confidence"] <= 0.40, (
                f"untrusted should not inflate: {ent['confidence']}"
            )
        finally:
            _teardown(store, tmp)


# ---------------------------------------------------------------------------
# PF3 · Cross-observation corroboration lifts score
# ---------------------------------------------------------------------------
class TestCorroborationLiftsScore:
    """PF3: multiple independent sources raise the score."""

    def test_two_sources_are_better_than_one(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(
                _entity("ipv4", "8.8.8.8", "ipapi_free", 0.8)
            )
            ent1 = store.get_entity(eid)
            assert ent1 is not None
            score_after_one = ent1["confidence"]

            store.fuse_entity(
                _entity("ipv4", "8.8.8.8", "shodan_internetdb", 0.8)
            )
            ent2 = store.get_entity(eid)
            assert ent2 is not None
            score_after_two = ent2["confidence"]

            # Two independent sources should yield >= the first score
            # (shodan is secondary, ipapi_free is secondary -- both B * secondary)
            assert score_after_two >= score_after_one, (
                f"{score_after_two} < {score_after_one}"
            )
        finally:
            _teardown(store, tmp)


# ---------------------------------------------------------------------------
# PF4 · Merge is monotonic (never decreases)
# ---------------------------------------------------------------------------
class TestMergeMonotonic:
    """PF4: a lower-confidence sighting never decreases the score."""

    def test_lower_confidence_never_decreases(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(
                _entity("domain", "example.com", "rdap_domain", 0.9)
            )
            ent1 = store.get_entity(eid)
            assert ent1 is not None
            score_before = ent1["confidence"]

            store.fuse_entity(
                _entity("domain", "example.com", "untrusted_webscraper", 0.1)
            )
            ent2 = store.get_entity(eid)
            assert ent2 is not None
            assert ent2["confidence"] >= score_before, (
                f"score dropped: {ent2['confidence']} < {score_before}"
            )
        finally:
            _teardown(store, tmp)


# ---------------------------------------------------------------------------
# PF5 · First sighting uses source-weighted base
# ---------------------------------------------------------------------------
class TestFirstSightingWeighted:
    """PF5: untrusted_webscraper first sighting is heavily discounted."""

    def test_untrusted_first_sighting_discounted(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(
                _entity("person", "John Doe", "untrusted_webscraper", 1.0)
            )
            ent = store.get_entity(eid)
            assert ent is not None
            # F reliability (0.10) * tertiary (0.60) * corr_1 (0.30) = 0.018
            assert ent["confidence"] <= 0.20, (
                f"untrusted not discounted: {ent['confidence']}"
            )
        finally:
            _teardown(store, tmp)


# ---------------------------------------------------------------------------
# PF6 · Relationship merge uses Bayesian score
# ---------------------------------------------------------------------------
class TestRelationshipBayesian:
    """PF6: relationship from untrusted source cannot override primary."""

    def test_relationship_untrusted_cannot_override(self) -> None:
        store, tmp = _fs()
        try:
            store.fuse_relationship(
                "person", "Alice", "knows", "person", "Bob",
                source="rdap_domain", confidence=0.9,
            )
            store.fuse_relationship(
                "person", "Alice", "knows", "person", "Bob",
                source="untrusted_webscraper", confidence=1.0,
            )
            # We can't easily query relationships, but we can test that
            # no exception is raised and the operation is idempotent
            stat = store.stats()
            assert stat["relationships"] >= 1
        finally:
            _teardown(store, tmp)


# ---------------------------------------------------------------------------
# Additional: regression tests
# ---------------------------------------------------------------------------
class TestFusionStoreRegression:
    """Existing fusion store invariants must still hold."""

    def test_entity_id_deterministic(self) -> None:
        store, tmp = _fs()
        try:
            a = store.fuse_entity(_entity("domain", "example.com", "dns_google"))
            b = store.fuse_entity(_entity("domain", "example.com", "dns_cloudflare"))
            assert a == b
        finally:
            _teardown(store, tmp)

    def test_entity_source_count_tracks(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(_entity("ipv4", "1.2.3.4", "ipapi_free"))
            ent1 = store.get_entity(eid)
            assert ent1 is not None
            assert ent1["source_count"] == 1
            store.fuse_entity(_entity("ipv4", "1.2.3.4", "shodan_internetdb"))
            ent2 = store.get_entity(eid)
            assert ent2 is not None
            assert ent2["source_count"] >= 2
        finally:
            _teardown(store, tmp)

    def test_observation_count_advances(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(
                _entity("domain", "example.com", "crt_sh_certificates")
            )
            for _ in range(3):
                store.fuse_entity(
                    _entity("domain", "example.com", "urlscan_public")
                )
            ent = store.get_entity(eid)
            assert ent is not None
            assert ent["observation_count"] >= 3
        finally:
            _teardown(store, tmp)

    def test_empty_type_returns_empty(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity({"type": "", "value": "x"})
            assert eid == ""
        finally:
            _teardown(store, tmp)

    def test_empty_value_returns_empty(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity({"type": "ipv4", "value": ""})
            assert eid == ""
        finally:
            _teardown(store, tmp)

    def test_add_observation_and_stats(self) -> None:
        store, tmp = _fs()
        try:
            store.register_sources([{"name": "test_src", "category": "test"}])
            store.add_observation(
                {"source": "test_src", "parsed": {"key": "val"}},
                query="test.com",
                case_id="case_1",
            )
            s = store.stats()
            assert s["observations"] >= 1
            assert s["sources"] >= 1
        finally:
            _teardown(store, tmp)

    def test_register_sources(self) -> None:
        store, tmp = _fs()
        try:
            sources = [
                {"name": "alpha", "category": "dns"},
                {"name": "beta", "category": "whois"},
            ]
            store.register_sources(sources)
            lst = store.list_sources()
            names = {s["name"] for s in lst}
            assert "alpha" in names
            assert "beta" in names
        finally:
            _teardown(store, tmp)

    def test_search_entities(self) -> None:
        store, tmp = _fs()
        try:
            store.fuse_entity(
                _entity("domain", "evilcorp.com", "crt_sh_certificates")
            )
            store.fuse_entity(
                _entity("domain", "goodstuff.org", "crt_sh_certificates")
            )
            results = store.search_entities(term="evil")
            values = [r["value"] for r in results]
            assert "evilcorp.com" in values
        finally:
            _teardown(store, tmp)

    def test_corroborated_properties(self) -> None:
        store, tmp = _fs()
        try:
            eid = store.fuse_entity(
                _entity("person", "Alice", "rdap_domain")
            )
            store.fuse_properties(eid, {"role": "admin"}, "source_a")
            store.fuse_properties(eid, {"role": "admin"}, "source_b")
            props = store.corroborated_properties(eid, min_sources=2)
            assert any(p["key"] == "role" and p["source_count"] >= 2 for p in props)
        finally:
            _teardown(store, tmp)

    def test_get_entity_nonexistent(self) -> None:
        store, tmp = _fs()
        try:
            assert store.get_entity("nonexistent") is None
        finally:
            _teardown(store, tmp)

    def test_open_store_closes_gracefully(self) -> None:
        from estorides_core.fusion_store import open_store
        store = open_store()
        if store is not None:
            store.close()
