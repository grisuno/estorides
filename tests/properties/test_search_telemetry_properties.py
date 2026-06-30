"""Property-based fuzzing for `search_telemetry` (spec S12 + predicate laws).

Each property runs >= 1000 random examples (doctrine section 6). The progress
computation must be total over the integers (never raise on numeric input) and
keep its bounds invariant; the brand/emoji predicates must be total over
arbitrary text and never raise.
"""
from __future__ import annotations

from hypothesis import given, settings
from hypothesis import strategies as st

from estorides_core.search_telemetry import (
    SearchTelemetry,
    UnknownPhaseError,
    disallowed_brands_in,
    emoji_in,
    percent_encoded_emoji_in,
)

_TEL = SearchTelemetry()
_PHASE_KEYS = tuple(phase.key for phase in _TEL.phases())
_RUNS = settings(max_examples=1000)


@_RUNS
@given(
    completed=st.integers(min_value=-10_000, max_value=10_000),
    total=st.integers(min_value=-10_000, max_value=10_000),
    phase_key=st.sampled_from(_PHASE_KEYS),
)
def test_progress_invariants_hold(completed: int, total: int, phase_key: str) -> None:
    view = _TEL.progress(completed=completed, total=total, phase_key=phase_key)
    assert 0 <= view.percent <= 100
    assert view.total == max(total, 0)
    assert 0 <= view.completed <= max(total, 0)
    assert view.aria_valuemax == 100
    if view.indeterminate:
        assert view.aria_valuenow is None
    else:
        assert view.aria_valuenow == view.percent


@_RUNS
@given(phase_key=st.text(min_size=1).filter(lambda k: k not in _PHASE_KEYS))
def test_progress_rejects_unknown_phase(phase_key: str) -> None:
    try:
        _TEL.progress(0, 10, phase_key=phase_key)
    except UnknownPhaseError:
        return
    raise AssertionError("unknown phase key must raise UnknownPhaseError")


@_RUNS
@given(text=st.text())
def test_brand_predicate_is_total(text: str) -> None:
    result = disallowed_brands_in(text)
    assert isinstance(result, tuple)
    for brand in result:
        assert brand in text.lower()


@_RUNS
@given(text=st.text())
def test_emoji_predicate_is_total(text: str) -> None:
    result = emoji_in(text)
    assert isinstance(result, tuple)
    for glyph in result:
        assert glyph in text


@_RUNS
@given(text=st.text())
def test_percent_encoded_emoji_predicate_is_total(text: str) -> None:
    result = percent_encoded_emoji_in(text)
    assert isinstance(result, tuple)


@_RUNS
@given(
    prefix=st.text(alphabet="abcdefghijklmnopqrstuvwxyz ", max_size=20),
    suffix=st.text(alphabet="abcdefghijklmnopqrstuvwxyz ", max_size=20),
)
def test_brand_predicate_flags_embedded_brand(prefix: str, suffix: str) -> None:
    text = f"{prefix} palantir {suffix}"
    assert "palantir" in disallowed_brands_in(text)
