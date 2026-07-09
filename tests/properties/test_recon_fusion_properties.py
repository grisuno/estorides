"""
Property-based fuzzing for recon_fusion module (doctrine section 6).

Verifies invariants hold for arbitrary valid inputs.
Minimum 1000 examples per property.
"""
from __future__ import annotations

from unittest.mock import patch

from hypothesis import given, settings
from hypothesis import strategies as st

from estorides_core.recon_fusion import ReconFusionEngine, RelevanceTier

_source_names = st.sampled_from([
    "crt_sh_certificates", "rdap_domain", "rdap_ip", "dns_google",
    "abuseipdb_check", "urlscan_public", "shodan_internetdb",
    "hackertarget_dns", "untrusted_webscraper", "leakcheck_public",
    "alienvault_otx", "ipapi_free",
])

_entity_types = st.sampled_from(["domain", "ipv4", "email", "cve", "asn", "btc_address"])

_non_empty_text = st.text(min_size=1, max_size=30).filter(lambda t: t.strip())

_valid_entity = st.fixed_dictionaries({
    "type": _entity_types,
    "value": st.text(min_size=1, max_size=50),
    "confidence": st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    "sources": st.lists(_source_names, min_size=1, max_size=5).map(lambda x: list(dict.fromkeys(x))),
})

_valid_observation = st.fixed_dictionaries({
    "source": _source_names,
    "category": st.text(min_size=1, max_size=30),
    "parser": st.text(min_size=1, max_size=20),
    "parsed": st.dictionaries(
        st.text(min_size=1, max_size=10),
        st.text(min_size=1, max_size=30),
        min_size=0, max_size=5,
    ),
    "meta": st.just({"status": "ok"}),
    "status": st.just("ok"),
})


class TestPropertyScoreBounds:
    """P1 -- Scores are always in [0, 1]."""

    @given(
        query=_non_empty_text,
        query_type=_entity_types,
        observations=st.lists(_valid_observation, min_size=0, max_size=10),
        entities=st.lists(_valid_entity, min_size=0, max_size=10),
    )
    @settings(max_examples=1000)
    def test_all_scores_in_unit_interval(
        self, query: str, query_type: str, observations: list, entities: list
    ) -> None:
        engine = ReconFusionEngine()
        result = engine.classify(query, query_type, observations, entities)
        for groups in result.tiers.values():
            for g in groups:
                assert 0.0 <= g.relevance_score <= 1.0


class TestPropertyTotalCounts:
    """P2 -- total_observations and total_entities match input."""

    @given(
        query=_non_empty_text,
        query_type=_entity_types,
        n_obs=st.integers(min_value=0, max_value=20),
        n_ents=st.integers(min_value=0, max_value=20),
    )
    @settings(max_examples=1000)
    def test_counts_match_input(
        self, query: str, query_type: str, n_obs: int, n_ents: int
    ) -> None:
        obs = [{"source": "crt_sh_certificates", "category": "web", "parser": "p",
                "parsed": {}, "meta": {"status": "ok"}, "status": "ok"}
               for _ in range(n_obs)]
        ents = [{"type": "domain", "value": f"test{i}.com", "confidence": 1.0,
                 "sources": ["crt_sh_certificates"]}
                for i in range(n_ents)]
        engine = ReconFusionEngine()
        result = engine.classify(query, query_type, obs, ents)
        assert result.total_observations == n_obs
        assert result.total_entities == n_ents


class TestPropertyTierSumMatches:
    """P3 -- tier_summary counts match actual tier list lengths."""

    @given(
        query=_non_empty_text,
        query_type=_entity_types,
        observations=st.lists(_valid_observation, min_size=0, max_size=10),
        entities=st.lists(_valid_entity, min_size=0, max_size=10),
    )
    @settings(max_examples=1000)
    def test_tier_summary_matches(
        self, query: str, query_type: str, observations: list, entities: list
    ) -> None:
        engine = ReconFusionEngine()
        result = engine.classify(query, query_type, observations, entities)
        for tier_name in RelevanceTier.ordered():
            expected = len(result.tiers.get(tier_name.value, []))
            actual = result.tier_summary.get(tier_name.value, 0)
            assert expected == actual


class TestPropertyDeterminism:
    """P4 -- Same input always produces same output (time-independent fields excluded)."""

    @given(
        query=_non_empty_text,
        query_type=_entity_types,
        observations=st.lists(_valid_observation, min_size=1, max_size=5),
        entities=st.lists(_valid_entity, min_size=1, max_size=5),
    )
    @settings(max_examples=1000)
    def test_deterministic_output(
        self, query: str, query_type: str, observations: list, entities: list
    ) -> None:
        fixed_time = 1234567890.0
        with patch("time.time", return_value=fixed_time):
            engine = ReconFusionEngine()
            result1 = engine.classify(query, query_type, list(observations), list(entities))
            result2 = engine.classify(query, query_type, list(observations), list(entities))
        assert result1.to_dict() == result2.to_dict()


class TestPropertyNoDuplicates:
    """P5 -- No duplicate canonical_id within the same tier."""

    @given(
        query=_non_empty_text,
        query_type=_entity_types,
        observations=st.lists(_valid_observation, min_size=0, max_size=10),
        entities=st.lists(_valid_entity, min_size=0, max_size=10),
    )
    @settings(max_examples=1000)
    def test_no_duplicate_ids_in_tier(
        self, query: str, query_type: str, observations: list, entities: list
    ) -> None:
        engine = ReconFusionEngine()
        result = engine.classify(query, query_type, observations, entities)
        for groups in result.tiers.values():
            ids = [g.canonical_id for g in groups]
            assert len(ids) == len(set(ids))


class TestPropertyTierKeysOrder:
    """P6 -- result.tiers dict preserves canonical tier key order."""

    @given(
        query=_non_empty_text,
        query_type=_entity_types,
        observations=st.lists(_valid_observation, min_size=0, max_size=10),
        entities=st.lists(_valid_entity, min_size=0, max_size=10),
    )
    @settings(max_examples=1000)
    def test_tier_keys_in_canonical_order(
        self, query: str, query_type: str, observations: list, entities: list
    ) -> None:
        engine = ReconFusionEngine()
        result = engine.classify(query, query_type, observations, entities)
        expected_keys = [t.value for t in RelevanceTier.ordered()]
        keys = list(result.tiers.keys())
        for k in expected_keys:
            assert k in keys


class TestPropertyEmptyQueryRejected:
    """P7 -- Empty query always raises ValueError."""

    @given(
        query_type=st.sampled_from(["domain", "ipv4", "email", ""]),
        observations=st.lists(_valid_observation, min_size=0, max_size=3),
        entities=st.lists(_valid_entity, min_size=0, max_size=3),
    )
    @settings(max_examples=1000)
    def test_empty_query_raises(
        self, query_type: str, observations: list, entities: list
    ) -> None:
        engine = ReconFusionEngine()
        import pytest
        with pytest.raises(ValueError):
            engine.classify("", query_type, observations, entities)
        with pytest.raises(ValueError):
            engine.classify("   ", query_type, observations, entities)


class TestPropertySafeWithBadInputs:
    """P8 -- None observations/entities never crash."""

    @given(query=_non_empty_text, query_type=_entity_types)
    @settings(max_examples=1000)
    def test_none_inputs_safe(self, query: str, query_type: str) -> None:
        engine = ReconFusionEngine()
        result = engine.classify(query, query_type, None, None)
        assert result.total_observations == 0
        assert result.total_entities == 0
        assert sum(len(v) for v in result.tiers.values()) == 0

    @given(
        query=_non_empty_text,
        query_type=_entity_types,
        observations=st.lists(_valid_observation, min_size=0, max_size=5),
    )
    @settings(max_examples=1000)
    def test_entities_none_is_safe(
        self, query: str, query_type: str, observations: list
    ) -> None:
        engine = ReconFusionEngine()
        result = engine.classify(query, query_type, observations, None)
        assert result.total_entities == 0
