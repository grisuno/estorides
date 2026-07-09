"""
BDD tests for the recon_fusion module (Modulo 2g).

Each scenario maps to a Given-When-Then from spec/recon_fusion.md.
"""
from __future__ import annotations

import pytest

from estorides_core.config import ReconFusionConfig
from estorides_core.recon_fusion import ReconFusionEngine, RelevanceTier


def _observation(
    source: str = "crt_sh_certificates",
    category: str = "03. Web Intelligence",
    parser: str = "certificate_parser",
    status: str = "ok",
    parsed: dict | None = None,
) -> dict:
    return {
        "source": source,
        "category": category,
        "parser": parser,
        "parsed": parsed or {"domain": "evilcorp.com", "issuer": "CA"},
        "meta": {"status": status},
        "status": status,
    }


def _entity(
    etype: str = "domain",
    value: str = "evilcorp.com",
    confidence: float = 1.0,
    sources: list[str] | None = None,
) -> dict:
    return {
        "type": etype,
        "value": value,
        "confidence": confidence,
        "sources": sources or ["crt_sh_certificates"],
    }


# --------------------------------------------------------------------------- S1
class TestS1CriticalCorroborated:
    """S1 -- Happy path: corroborated by 5 sources -> CRITICAL."""

    def test_critical_with_5_sources(self) -> None:
        engine = ReconFusionEngine()
        sources = ("crt_sh_certificates", "rdap_domain", "urlscan_public", "dns_google", "otx_domain_passive")
        obs = [_observation(s, parser="cert") for s in sources]
        ents = [_entity(sources=list(sources))]
        result = engine.classify("evilcorp.com", "domain", obs, ents)
        critical = result.tiers.get("critical", [])
        assert len(critical) >= 1
        group = critical[0]
        assert group.direct_match is True
        assert group.source_count >= 3
        assert group.tier == "critical"
        assert group.value == "evilcorp.com"


# --------------------------------------------------------------------------- S2
class TestS2TwoReliableSources:
    """S2 -- 2 sources with A/B reliability -> CRITICAL (via 2+ src + high rel)."""

    def test_two_reliable_sources_critical(self) -> None:
        engine = ReconFusionEngine()
        sources = ("rdap_ip", "abuseipdb_check")
        obs = [_observation(s, parser="rdap", parsed={"ipv4": "8.8.8.8"}) for s in sources]
        ents = [_entity("ipv4", "8.8.8.8", sources=list(sources))]
        result = engine.classify("8.8.8.8", "ipv4", obs, ents)
        critical = result.tiers.get("critical", [])
        assert len(critical) >= 1
        group = critical[0]
        assert group.source_count >= 2
        assert group.tier == "critical"


# --------------------------------------------------------------------------- S3
class TestS3SingleHighReliability:
    """S3 -- Single high-reliability source -> MEDIUM."""

    def test_single_a_source_is_medium(self) -> None:
        engine = ReconFusionEngine()
        obs = [_observation("crt_sh_certificates", parsed={"domain": "example.com"})]
        ents = [_entity("domain", "example.com")]
        result = engine.classify("test-query.org", "domain", obs, ents)
        medium = result.tiers.get("medium", [])
        # With 1 source (crt_sh = A), no direct match (query differs)
        # Tier = MEDIUM (source_count=1, avg_reliability=1.0 > D_weight=0.5)
        found = [g for g in medium if g.value == "example.com"]
        assert len(found) == 1
        assert found[0].source_count == 1
        assert found[0].max_confidence > 0.5
        assert found[0].direct_match is False
        assert found[0].tier == "medium"


# --------------------------------------------------------------------------- S4
class TestS4SingleLowReliability:
    """S4 -- Single F-reliability source -> NOISE."""

    def test_single_f_source_is_noise(self) -> None:
        engine = ReconFusionEngine()
        obs = [_observation("untrusted_webscraper", parsed={"domain": "sketchy.com"})]
        ents = [_entity("domain", "sketchy.com", sources=["untrusted_webscraper"])]
        result = engine.classify("test-query.org", "domain", obs, ents)
        noise = result.tiers.get("noise", [])
        found = [g for g in noise if g.value == "sketchy.com"]
        assert len(found) == 1
        assert found[0].source_count == 1


# --------------------------------------------------------------------------- S5
class TestS5EmptyInput:
    """S5 -- No observations or entities -> empty result."""

    def test_empty_observations_and_entities(self) -> None:
        engine = ReconFusionEngine()
        result = engine.classify("test.com", "domain", [], [])
        assert result.total_observations == 0
        assert result.total_entities == 0
        for tier_list in result.tiers.values():
            assert len(tier_list) == 0


# --------------------------------------------------------------------------- S6
class TestS6DirectMatchBoost:
    """S6 -- Direct match entity has boosted score."""

    def test_direct_match_boosts_score(self) -> None:
        engine = ReconFusionEngine()
        query = "phishing.com"
        obs = [_observation("crt_sh_certificates", parsed={"domain": "phishing.com"})]
        ents = [_entity("domain", "phishing.com")]
        result = engine.classify(query, "domain", obs, ents)
        high = result.tiers.get("high", [])
        found = [g for g in high if g.value == "phishing.com"]
        assert len(found) == 1
        assert found[0].direct_match is True
        assert found[0].relevance_score > 0.0


# --------------------------------------------------------------------------- S7
class TestS7EmptyQuery:
    """S7 -- Empty query raises ValueError."""

    def test_empty_query_raises(self) -> None:
        engine = ReconFusionEngine()
        with pytest.raises(ValueError, match="query must be non-empty"):
            engine.classify("", "domain", [], [])


# --------------------------------------------------------------------------- S8
class TestS8BadConfig:
    """S8 -- Inconsistent thresholds raise ValueError."""

    def test_bad_thresholds_raise(self) -> None:
        with pytest.raises(ValueError):
            ReconFusionConfig(
                critical_min_sources=2, high_min_sources=3,
                high_min_reliability="B", medium_min_reliability="D",
                noise_max_reliability="F", freshness_max_hours=72.0,
                direct_match_boost=0.15,
                exact_dedup_keys=("source", "parser", "status"),
                source_reliability_overrides={},
            )


# --------------------------------------------------------------------------- S9
class TestS9NoneObservations:
    """S9 -- None observations handled safely."""

    def test_none_observations_safe(self) -> None:
        engine = ReconFusionEngine()
        result = engine.classify("test.com", "domain", None, [])
        assert result.total_observations == 0


# --------------------------------------------------------------------------- S10
class TestS10EntityWithoutType:
    """S10 -- Entity without type is ignored."""

    def test_entity_without_type_ignored(self) -> None:
        engine = ReconFusionEngine()
        bad_entities = [{"value": "test"}]
        result = engine.classify("test.com", "domain", [], bad_entities)
        total = sum(len(v) for v in result.tiers.values())
        assert total == 0


# --------------------------------------------------------------------------- S11
class TestS11Dedup:
    """S11 -- Identical observations deduped to one."""

    def test_identical_observations_deduped(self) -> None:
        engine = ReconFusionEngine()
        obs = [_observation("crt_sh_certificates") for _ in range(3)]
        ents = [_entity("domain", "evilcorp.com")]
        result = engine.classify("evilcorp.com", "domain", obs, ents)
        # 3 identical dedup to 1 obs, source_count=1, direct_match=True
        # With crt_sh (A), source_count=1, direct_match: tier = HIGH
        high = result.tiers.get("high", [])
        found = [g for g in high if g.value == "evilcorp.com"]
        assert len(found) == 1
        assert found[0].source_count >= 1


# --------------------------------------------------------------------------- S12
class TestS12Ordering:
    """S12 -- Tiers ordered by relevance_score descending."""

    def test_tier_ordered_by_score(self) -> None:
        engine = ReconFusionEngine()
        result = engine.classify("test.com", "domain", [], [])
        for tier_name, groups in result.tiers.items():
            scores = [g.relevance_score for g in groups]
            assert all(0.0 <= s <= 1.0 for s in scores)
            assert scores == sorted(scores, reverse=True), f"{tier_name} not sorted"


# ---------------------------------------------------------------------------
# Additional integration tests
# ---------------------------------------------------------------------------
class TestIntegrationMultiEntity:
    """Integration: multiple entities classified across tiers."""

    def test_mixed_entities_across_tiers(self) -> None:
        engine = ReconFusionEngine()
        obs = [
            _observation("crt_sh_certificates", parsed={"domain": "evilcorp.com"}),
            _observation("rdap_domain", parsed={"domain": "evilcorp.com"}),
            _observation("dns_google", parsed={"domain": "evilcorp.com"}),
            _observation("crt_sh_certificates", parsed={"domain": "shadow.evilcorp.com"}),
            _observation("untrusted_webscraper", parsed={"domain": "sketchy-site.com"}),
        ]
        ents = [
            _entity("domain", "evilcorp.com", sources=["crt_sh_certificates", "rdap_domain", "dns_google"]),
            _entity("domain", "shadow.evilcorp.com", sources=["crt_sh_certificates"]),
            _entity("domain", "sketchy-site.com", sources=["untrusted_webscraper"]),
        ]
        result = engine.classify("evilcorp.com", "domain", obs, ents)
        assert len(result.tiers["critical"]) >= 1
        assert len(result.tiers["medium"]) >= 1
        assert len(result.tiers["noise"]) >= 1
        assert result.tier_summary["critical"] >= 1
        assert result.tier_summary["noise"] >= 1


class TestFusionResultDataclass:
    """FusionResult dataclass structural tests."""

    def test_fusion_result_serialisable(self) -> None:
        engine = ReconFusionEngine()
        result = engine.classify("test.com", "domain", [], [])
        data = result.to_dict()
        assert isinstance(data, dict)
        assert "tiers" in data
        assert "tier_summary" in data
        assert "generated_at" in data
        assert data["total_observations"] == 0
        assert data["total_entities"] == 0


class TestRelevanceTierEnum:
    """RelevanceTier enum members and ordering."""

    def test_enum_members(self) -> None:
        assert RelevanceTier.CRITICAL.value == "critical"
        assert RelevanceTier.HIGH.value == "high"
        assert RelevanceTier.MEDIUM.value == "medium"
        assert RelevanceTier.LOW.value == "low"
        assert RelevanceTier.NOISE.value == "noise"

    def test_enum_order_list(self) -> None:
        ordered = RelevanceTier.ordered()
        names = [t.value for t in ordered]
        assert names == ["critical", "high", "medium", "low", "noise"]
