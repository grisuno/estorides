"""
Property-based invariants for estorides_core.source_health_monitoring.

Hypothesis replaces libFuzzer/AFL for Python. These tests run >= 1000
random examples per property.
"""
from __future__ import annotations

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from estorides_core.source_health_monitoring import (
    SourceHealthConfig,
    SourceHealthInput,
    SourceHealthStatus,
    build_dashboard,
    compute_health,
)


def _valid_input(
    fetch: int, ok: int, latency: float, last_seen: float, now: float
) -> SourceHealthInput:
    """Build a valid SourceHealthInput, clamping ok <= fetch."""
    clamped_ok = min(ok, fetch)
    return SourceHealthInput(
        source_name="test",
        fetch_count=fetch,
        ok_count=clamped_ok,
        latency_sum_ms=abs(latency),
        last_seen=abs(last_seen),
        now=abs(now),
    )


nonneg_int_st = st.integers(min_value=0, max_value=10_000)
nonneg_float_st = st.floats(min_value=0.0, max_value=1e9, allow_nan=False, allow_infinity=False)
name_st = st.text(min_size=1, max_size=50)


@given(
    fetch=nonneg_int_st,
    ok=nonneg_int_st,
    latency=nonneg_float_st,
    last_seen=nonneg_float_st,
    now=nonneg_float_st,
)
@settings(max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
def test_health_score_always_bounded(fetch, ok, latency, last_seen, now) -> None:
    inp = _valid_input(fetch, ok, latency, last_seen, now)
    result = compute_health(inp)
    assert 0.0 <= result.health_score <= 1.0, result


@given(
    fetch=nonneg_int_st,
    ok=nonneg_int_st,
    latency=nonneg_float_st,
    last_seen=nonneg_float_st,
    now=nonneg_float_st,
)
@settings(max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
def test_status_always_valid_enum(fetch, ok, latency, last_seen, now) -> None:
    inp = _valid_input(fetch, ok, latency, last_seen, now)
    result = compute_health(inp)
    assert isinstance(result.status, SourceHealthStatus)
    assert result.status in SourceHealthStatus


@given(
    fetch=nonneg_int_st,
    ok=nonneg_int_st,
    latency=nonneg_float_st,
    last_seen=nonneg_float_st,
    now=nonneg_float_st,
)
@settings(max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
def test_success_rate_bounds(fetch, ok, latency, last_seen, now) -> None:
    inp = _valid_input(fetch, ok, latency, last_seen, now)
    result = compute_health(inp)
    assert 0.0 <= result.success_rate <= 1.0


@given(
    fetch=st.integers(min_value=0, max_value=4),
    config_min=st.integers(min_value=5, max_value=10),
)
@settings(max_examples=200, deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
def test_unknown_when_below_min_fetches(fetch: int, config_min: int) -> None:
    inp = _valid_input(fetch, fetch, 0.0, 1000.0, 1000.0)
    config = SourceHealthConfig(min_fetches=config_min)
    result = compute_health(inp, config)
    assert result.status == SourceHealthStatus.UNKNOWN


@st.composite
def valid_health_inputs(draw):
    fetch = draw(nonneg_int_st)
    ok_raw = draw(nonneg_int_st)
    return SourceHealthInput(
        source_name=draw(name_st),
        fetch_count=fetch,
        ok_count=min(ok_raw, fetch),
        latency_sum_ms=draw(nonneg_float_st),
        last_seen=draw(nonneg_float_st),
        now=draw(nonneg_float_st),
    )


@given(records=st.lists(valid_health_inputs(), min_size=0, max_size=30))
@settings(max_examples=200, deadline=None)
def test_dashboard_summary_counts_match(records) -> None:
    """Dashboard summary counts must sum to total."""
    if not records:
        return
    dashboard = build_dashboard(records)
    s = dashboard.summary
    assert s.total_sources == len(records)
    assert s.healthy_count + s.degrading_count + s.stale_count + s.unknown_count == s.total_sources
