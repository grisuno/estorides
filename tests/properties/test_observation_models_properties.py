"""
Property-based invariants for estorides_core.observation_models.

Each ``@given`` run exercises at least 1000 random examples by default
(hypothesis derives the count from the example budget). The invariants are
the executable translation of BDD scenario O9 in spec/observation_models.md.
"""
from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from estorides_core.observation_models import (
    MAX_STR_LEN,
    MAX_URL_LEN,
    MAX_VALUE_LEN,
    Observation,
    ObservationMeta,
    ObservedEntity,
)

FIELD_TYPES = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(),
)

JSON_SAFE = st.recursive(
    FIELD_TYPES,
    lambda children: st.one_of(
        st.lists(children),
        st.dictionaries(st.text(), children),
    ),
)

# Shallow JSON dicts for fields typed ``dict[str, Any]``. Kept flat (no
# recursion) so input generation stays fast enough for hypothesis' health
# check on the 1000-example budget.
JSON_DICT = st.dictionaries(st.text(max_size=64), FIELD_TYPES)


@st.composite
def meta_strategy(draw: st.DrawFn) -> dict:
    return {
        "url": draw(st.text(max_size=MAX_URL_LEN * 3)),
        "method": draw(st.text(max_size=32)),
        "host": draw(st.text(max_size=128)),
        "attempts": draw(st.integers(min_value=0, max_value=100)),
        "cached": draw(st.booleans()),
        "proxied": draw(st.booleans()),
        "status": draw(st.integers(min_value=0, max_value=599)),
        "content_type": draw(st.text(max_size=128)),
        "error": draw(st.text(max_size=256)),
    }


@st.composite
def obs_strategy(draw: st.DrawFn) -> dict:
    return {
        "source": draw(st.text(min_size=1, max_size=MAX_STR_LEN)),
        "category": draw(st.text(max_size=MAX_STR_LEN)),
        "description": draw(st.text(max_size=MAX_STR_LEN)),
        "parser": draw(st.text(max_size=MAX_STR_LEN)),
        "parsed": draw(JSON_SAFE),
        "raw": draw(JSON_SAFE),
        "meta": draw(meta_strategy()),
        "observed_at": draw(st.floats(min_value=0.0, max_value=1e12, allow_nan=False, allow_infinity=False)),
        "ontology": draw(JSON_DICT),
        "mitre": draw(JSON_DICT),
    }


@st.composite
def entity_strategy(draw: st.DrawFn) -> dict:
    return {
        "type": draw(st.text(min_size=1, max_size=MAX_STR_LEN)),
        "value": draw(st.text(min_size=1, max_size=MAX_VALUE_LEN)),
        "source": draw(st.text(max_size=MAX_STR_LEN)),
        "context": draw(st.text(max_size=MAX_STR_LEN)),
        "confidence": draw(st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)),
        "attributes": draw(JSON_DICT),
        "sources": draw(st.lists(st.text(max_size=MAX_STR_LEN))),
    }


@settings(max_examples=1000)
@given(obs_strategy())
def test_observation_round_trip_stability(payload: dict) -> None:
    obs = Observation.model_validate(payload)
    legacy = obs.to_legacy_dict()
    reloaded = Observation.model_validate(legacy)
    assert reloaded.source == obs.source
    assert reloaded.parser == obs.parser
    assert reloaded.meta.status == obs.meta.status
    # meta.method is always uppercased on validation, so it round-trips.
    assert reloaded.meta.method == reloaded.meta.method.upper()


@settings(max_examples=1000)
@given(obs_strategy())
def test_observation_bounded_fields(payload: dict) -> None:
    obs = Observation.model_validate(payload)
    assert len(obs.meta.url) <= MAX_URL_LEN
    assert len(obs.source) <= MAX_STR_LEN
    assert len(obs.category) <= MAX_STR_LEN
    assert obs.observed_at >= 0.0
    assert obs.meta.attempts >= 0
    assert obs.meta.status >= 0


@settings(max_examples=1000)
@given(entity_strategy())
def test_entity_round_trip_and_bounds(payload: dict) -> None:
    ent = ObservedEntity.model_validate(payload)
    assert 0.0 <= ent.confidence <= 1.0
    assert len(ent.value) <= MAX_VALUE_LEN
    assert len(ent.type) <= MAX_STR_LEN
    legacy = ent.to_legacy_dict()
    reloaded = ObservedEntity.model_validate(legacy)
    assert reloaded.value == ent.value
    assert reloaded.confidence == ent.confidence


@settings(max_examples=1000)
@given(st.lists(meta_strategy()))
def test_meta_never_echoes_unbounded_url(metas: list[dict]) -> None:
    for raw in metas:
        m = ObservationMeta.model_validate(raw)
        assert len(m.url) <= MAX_URL_LEN
