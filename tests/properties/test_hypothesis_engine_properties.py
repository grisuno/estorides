"""Property-based invariants for estorides_core.hypothesis_engine.

Hypothesis fuzzing: random observations + entities, must always satisfy
the boundedness invariants declared in spec S10.

Run from the project root::

    .venv/bin/pytest tests/properties/test_hypothesis_engine_properties.py -v
"""
from __future__ import annotations

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from estorides_core.hypothesis_engine import generate_hypotheses

# Strategies: small observation lists, small entity lists, bounded strings.
short_str = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        max_codepoint=0x7E,
    ),
    min_size=0,
    max_size=80,
)
hostile_str = st.text(max_size=200)
small_parsed = st.fixed_dictionaries(
    mapping={"registrant_organization": short_str},
    optional={"issuer_name": short_str, "org": short_str, "label": short_str},
)
small_entity = st.fixed_dictionaries(
    mapping={
        "type": st.sampled_from(["domain", "org", "person", "email"]),
        "value": short_str,
    },
)
observation_st = st.fixed_dictionaries(
    mapping={
        "source": st.sampled_from(
            ["hackertarget_whois", "crt_sh_certificates", "ipapi_co_full",
             "rdap_domain", "wikidata_search", "github_user",
             "abuseipdb_check", "totally_made_up_source_xyz", "x"]
        ),
    },
    optional={"parsed": st.one_of(st.none(), small_parsed)},
)


@settings(max_examples=200, deadline=None, suppress_health_check=list(HealthCheck))
@given(
    observations=st.lists(observation_st, min_size=0, max_size=10),
    entities=st.lists(small_entity, min_size=0, max_size=10),
)
def test_scores_always_bounded(observations, entities) -> None:
    result = generate_hypotheses(observations, entities)
    for h in result:
        assert 0.0 <= h.score <= 1.0
        assert 0.0 <= h.confidence <= 1.0


@settings(max_examples=200, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=5),
    entities=st.lists(small_entity, min_size=0, max_size=5),
)
def test_claim_length_under_cap(observations, entities) -> None:
    result = generate_hypotheses(observations, entities)
    for h in result:
        assert len(h.claim) <= 280, f"claim too long: {h.claim!r}"


@settings(max_examples=200, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=5),
    entities=st.lists(small_entity, min_size=0, max_size=5),
)
def test_reasoning_length_under_cap(observations, entities) -> None:
    result = generate_hypotheses(observations, entities)
    for h in result:
        assert len(h.reasoning) <= 500, "reasoning too long"


@settings(max_examples=200, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=5),
    entities=st.lists(small_entity, min_size=0, max_size=5),
)
def test_sources_sorted_unique(observations, entities) -> None:
    result = generate_hypotheses(observations, entities)
    for h in result:
        assert h.sources == sorted(set(h.sources)), h.sources


@settings(max_examples=200, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=5),
    entities=st.lists(small_entity, min_size=0, max_size=5),
)
def test_id_is_deterministic_hex(observations, entities) -> None:
    import re
    result = generate_hypotheses(observations, entities)
    hex16 = re.compile(r"^[0-9a-f]{16}$")
    for h in result:
        assert hex16.match(h.id), f"id {h.id!r} is not a 16-char hex"


@settings(max_examples=100, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=8),
    entities=st.lists(small_entity, min_size=0, max_size=8),
)
def test_idempotent(observations, entities) -> None:
    a = generate_hypotheses(observations, entities)
    b = generate_hypotheses(observations, entities)
    assert sorted(h.id for h in a) == sorted(h.id for h in b)


@settings(max_examples=100, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=5),
    entities=st.lists(small_entity, min_size=0, max_size=5),
)
def test_max_hypotheses_caps_output(observations, entities) -> None:
    for cap in (1, 2, 5):
        result = generate_hypotheses(observations, entities, max_hypotheses=cap)
        assert len(result) <= cap


@settings(max_examples=100, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=5),
    entities=st.lists(small_entity, min_size=0, max_size=5),
)
def test_min_score_filters(observations, entities) -> None:
    high = generate_hypotheses(observations, entities, min_score=0.0)
    low = generate_hypotheses(observations, entities, min_score=0.99)
    assert len(low) <= len(high)
    for h in low:
        assert h.score >= 0.99


@settings(max_examples=200, deadline=None)
@given(
    observations=st.lists(observation_st, min_size=0, max_size=5),
    entities=st.lists(small_entity, min_size=0, max_size=5),
)
def test_hostile_observation_does_not_crash(observations, entities) -> None:
    # Mutate one observation to have a giant string in parsed.
    if observations:
        observations[0]["parsed"] = {"registrant_organization": "A" * 100_000}
    # No assertion: just verify no crash.
    generate_hypotheses(observations, entities)
