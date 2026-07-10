"""Property-based invariants for estorides_core.reliability_scoring.

Hypothesis replaces libFuzzer/AFL for Python. These tests run >= 1000
random examples per property and must never crash, raise (except
``InvalidArgument`` from input validation), or violate the invariants.

Run from the project root::

    .venv/bin/pytest tests/properties/test_reliability_scoring_properties.py -v
"""
from __future__ import annotations

from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from estorides_core.reliability_scoring import (
    CREDIBILITY_WEIGHT,
    RELIABILITY_WEIGHT,
    SOURCE_TYPE_WEIGHT,
    Credibility,
    SourceReliability,
    SourceType,
    compute_confidence,
    merge_confidence,
    reliability_from_name,
    source_type_from_name,
)

# Strategies constrained to the spec's valid ranges.
reliability_st = st.sampled_from(list(SourceReliability))
credibility_st = st.sampled_from(list(Credibility))
nonneg_int_st = st.integers(min_value=0, max_value=10_000)
nonneg_float_st = st.floats(min_value=0.0, max_value=1e12, allow_nan=False, allow_infinity=False)
base_confidence_st = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
half_life_st = st.floats(min_value=0.5, max_value=10_000.0, allow_nan=False, allow_infinity=False)
source_name_st = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd", "Pc", "Pd", "Zs", "Po", "Sm"),
        whitelist_characters="\x00\x07\x08\x1b",
    ),
    min_size=0,
    max_size=200,
)


# Invariant 1: the score is always in [0, 1].
@given(
    reliability=reliability_st,
    credibility=credibility_st,
    corroboration=nonneg_int_st,
    age=nonneg_float_st,
    base=base_confidence_st,
    half_life=half_life_st,
)
@settings(max_examples=1000, deadline=None, suppress_health_check=list(HealthCheck))
def test_score_always_bounded(reliability, credibility, corroboration, age, base, half_life) -> None:
    from estorides_core.reliability_scoring import ConfidenceInput  # local import for clean traceback

    inp = ConfidenceInput(
        source_reliability=reliability,
        credibility=credibility,
        corroboration_count=corroboration,
        observation_age_seconds=age,
        base_confidence=base,
    )
    result = compute_confidence(inp, half_life_days=half_life)
    assert 0.0 <= result.score <= 1.0, result


# Invariant 2: corroboration weight is in [0, 1] and is monotone non-decreasing.
@given(n=st.integers(min_value=0, max_value=10_000))
@settings(max_examples=1000, deadline=None)
def test_corroboration_weight_in_unit_interval(n: int) -> None:
    from estorides_core.reliability_scoring import ConfidenceInput

    inp = ConfidenceInput(
        source_reliability=SourceReliability.A,
        corroboration_count=n,
    )
    result = compute_confidence(inp)
    assert 0.0 <= result.corroboration_weight <= 1.0, result


# Invariant 3: freshness weight is in (0, 1] and is monotone non-increasing in age.
@given(age1=nonneg_float_st, age2=nonneg_float_st)
@settings(max_examples=1000, deadline=None)
def test_freshness_monotone_in_age(age1: float, age2: float) -> None:
    from estorides_core.reliability_scoring import ConfidenceInput

    assume(age1 < age2)
    inp_a = ConfidenceInput(
        source_reliability=SourceReliability.A,
        corroboration_count=1,
        observation_age_seconds=age1,
    )
    inp_b = ConfidenceInput(
        source_reliability=SourceReliability.A,
        corroboration_count=1,
        observation_age_seconds=age2,
    )
    r_a = compute_confidence(inp_a, half_life_days=30.0)
    r_b = compute_confidence(inp_b, half_life_days=30.0)
    # age2 > age1 ⇒ freshness en age2 ≤ freshness en age1.
    assert r_b.freshness_weight <= r_a.freshness_weight, (r_a, r_b, age1, age2)


# Invariant 4: reliability_from_name never raises and always returns a valid enum.
@given(name=source_name_st)
@settings(max_examples=2000, deadline=None)
def test_reliability_from_name_never_raises(name: str) -> None:
    result = reliability_from_name(name)
    assert isinstance(result, SourceReliability)
    assert result in SourceReliability


# Invariant 5: merge_confidence returns score in [0, 1] and is monotone in `existing`.
@given(
    existing=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    new_obs=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
    new_rel=reliability_st,
    new_cred=credibility_st,
    cor=st.integers(min_value=1, max_value=1_000),
    age=nonneg_float_st,
)
@settings(max_examples=1000, deadline=None)
def test_merge_confidence_bounded(existing, new_obs, new_rel, new_cred, cor, age) -> None:
    result = merge_confidence(
        existing=existing,
        new_observation=new_obs,
        new_reliability=new_rel,
        new_credibility=new_cred,
        corroboration_count=cor,
        observation_age_seconds=age,
    )
    assert 0.0 <= result.score <= 1.0
    # max(existing, new_score) → siempre >= existing
    assert result.score >= existing - 1e-9


# Invariant 6: enum weights are exactly the curated set (no arbitrary floats).
def test_reliability_weight_set_is_curated() -> None:
    expected = {1.00, 0.85, 0.70, 0.50, 0.30, 0.10}
    assert set(RELIABILITY_WEIGHT.values()) == expected


def test_credibility_weight_set_is_curated() -> None:
    expected = {1.00, 0.85, 0.60, 0.30, 0.10, 0.50}
    assert set(CREDIBILITY_WEIGHT.values()) == expected


# Invariant 7: corroboration is monotonically non-decreasing in count.
# Adding an independent source to the same observation can only raise
# (or leave equal) the corroboration weight.
@given(
    n1=st.integers(min_value=0, max_value=10_000),
    n2=st.integers(min_value=0, max_value=10_000),
)
@settings(max_examples=1000, deadline=None)
def test_corroboration_is_monotone_in_count(n1: int, n2: int) -> None:
    from estorides_core.reliability_scoring import ConfidenceInput

    assume(n1 <= n2)
    inp1 = ConfidenceInput(
        source_reliability=SourceReliability.B,
        corroboration_count=n1,
    )
    inp2 = ConfidenceInput(
        source_reliability=SourceReliability.B,
        corroboration_count=n2,
    )
    r1 = compute_confidence(inp1)
    r2 = compute_confidence(inp2)
    assert r2.corroboration_weight >= r1.corroboration_weight - 1e-12
    assert r2.score >= r1.score - 1e-12


# Invariant 8: higher reliability never produces a lower score on the
# same input (everything else equal).
@given(
    rel1=reliability_st,
    rel2=reliability_st,
)
@settings(max_examples=500, deadline=None)
def test_higher_reliability_dominates(rel1: SourceReliability, rel2: SourceReliability) -> None:
    # Order the two by their weight to make the comparison deterministic.
    from estorides_core.reliability_scoring import RELIABILITY_WEIGHT, ConfidenceInput
    w1, w2 = RELIABILITY_WEIGHT[rel1], RELIABILITY_WEIGHT[rel2]
    if w1 > w2:
        higher, lower = rel1, rel2
    elif w2 > w1:
        higher, lower = rel2, rel1
    else:
        return  # mismo reliability, nada que probar
    inp_h = ConfidenceInput(source_reliability=higher, corroboration_count=3)
    inp_l = ConfidenceInput(source_reliability=lower, corroboration_count=3)
    assert compute_confidence(inp_h).score > compute_confidence(inp_l).score


# Invariant 9: source_type_from_name never raises and always returns a valid enum.
@given(name=source_name_st)
@settings(max_examples=2000, deadline=None)
def test_source_type_from_name_never_raises(name: str) -> None:
    result = source_type_from_name(name)
    assert isinstance(result, SourceType)
    assert result in SourceType


# Invariant 10: source_type_weight is always in {1.00, 0.85, 0.60}.
@given(
    reliability=reliability_st,
    credibility=credibility_st,
    source_type=st.sampled_from(list(SourceType)),
    corroboration=nonneg_int_st,
    age=nonneg_float_st,
    base=base_confidence_st,
    half_life=half_life_st,
)
@settings(max_examples=1000, deadline=None, suppress_health_check=list(HealthCheck))
def test_source_type_weight_always_curated(
    reliability, credibility, source_type, corroboration, age, base, half_life
) -> None:
    from estorides_core.reliability_scoring import ConfidenceInput

    inp = ConfidenceInput(
        source_reliability=reliability,
        credibility=credibility,
        source_type=source_type,
        corroboration_count=corroboration,
        observation_age_seconds=age,
        base_confidence=base,
    )
    result = compute_confidence(inp, half_life_days=half_life)
    assert result.source_type_weight in {1.00, 0.85, 0.60}, result
    if source_type == SourceType.PRIMARY:
        assert result.source_type_weight == 1.00
    elif source_type == SourceType.TERTIARY:
        assert result.source_type_weight == 0.60


# Invariant 11: SOURCE_TYPE_WEIGHT set is exactly the curated values.
def test_source_type_weight_set_is_curated() -> None:
    expected = {1.00, 0.85, 0.60}
    assert set(SOURCE_TYPE_WEIGHT.values()) == expected
