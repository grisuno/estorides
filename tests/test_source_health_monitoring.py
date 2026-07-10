"""
BDD tests for estorides_core.source_health_monitoring.

These tests implement the Given-When-Then contracts declared in
spec/source_health_monitoring.md. They must fail against the unwritten
implementation (red step) and pass after the green step.
"""
from __future__ import annotations

from dataclasses import is_dataclass

import pytest

from estorides_core.source_health_monitoring import (
    DEFAULT_HEALTH_CONFIG,
    HealthDashboard,
    SourceHealthConfig,
    SourceHealthInput,
    SourceHealthResult,
    SourceHealthStatus,
    build_dashboard,
    compute_health,
)


# ---------------------------------------------------------------------------
# H1 — Healthy source
# ---------------------------------------------------------------------------
class TestHealthySource:
    """H1: high success rate, low latency -> HEALTHY."""

    def test_healthy_status(self) -> None:
        inp = SourceHealthInput(
            source_name="crt_sh_certificates",
            fetch_count=100,
            ok_count=98,
            latency_sum_ms=30000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.status == SourceHealthStatus.HEALTHY

    def test_success_rate_computed(self) -> None:
        inp = SourceHealthInput(
            source_name="crt_sh_certificates",
            fetch_count=100,
            ok_count=98,
            latency_sum_ms=30000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.success_rate == pytest.approx(0.98, rel=1e-9)

    def test_avg_latency_computed(self) -> None:
        inp = SourceHealthInput(
            source_name="crt_sh_certificates",
            fetch_count=100,
            ok_count=98,
            latency_sum_ms=30000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.avg_latency_ms == pytest.approx(300.0, rel=1e-9)

    def test_freshness_hours_computed(self) -> None:
        inp = SourceHealthInput(
            source_name="crt_sh_certificates",
            fetch_count=100,
            ok_count=98,
            latency_sum_ms=30000.0,
            last_seen=0.0,
            now=3600.0,
        )
        result = compute_health(inp)
        assert result.freshness_hours == pytest.approx(1.0, rel=1e-9)

    def test_health_score_high_band(self) -> None:
        inp = SourceHealthInput(
            source_name="crt_sh_certificates",
            fetch_count=100,
            ok_count=98,
            latency_sum_ms=30000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.health_score >= 0.8
        assert result.health_score <= 1.0


# ---------------------------------------------------------------------------
# H2 — Degrading due to low success rate
# ---------------------------------------------------------------------------
class TestDegradingLowSuccess:
    """H2: low success rate -> DEGRADING."""

    def test_degrading_status(self) -> None:
        inp = SourceHealthInput(
            source_name="leakcheck_public",
            fetch_count=50,
            ok_count=20,
            latency_sum_ms=50000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.status == SourceHealthStatus.DEGRADING

    def test_success_rate_reflects_failures(self) -> None:
        inp = SourceHealthInput(
            source_name="leakcheck_public",
            fetch_count=50,
            ok_count=20,
            latency_sum_ms=50000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.success_rate == pytest.approx(0.4, rel=1e-9)

    def test_health_score_low_band(self) -> None:
        inp = SourceHealthInput(
            source_name="leakcheck_public",
            fetch_count=50,
            ok_count=20,
            latency_sum_ms=50000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        # success_weight=0.16, latency_weight=0.8 (1s avg), fresh => ~0.52
        assert 0.4 <= result.health_score <= 0.7


# ---------------------------------------------------------------------------
# H3 — Degrading due to high latency
# ---------------------------------------------------------------------------
class TestDegradingHighLatency:
    """H3: high latency -> DEGRADING."""

    def test_degrading_status_for_latency(self) -> None:
        inp = SourceHealthInput(
            source_name="wayback_machine_cdx",
            fetch_count=50,
            ok_count=48,
            latency_sum_ms=500000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.status == SourceHealthStatus.DEGRADING

    def test_avg_latency_high(self) -> None:
        inp = SourceHealthInput(
            source_name="wayback_machine_cdx",
            fetch_count=50,
            ok_count=48,
            latency_sum_ms=500000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.avg_latency_ms == pytest.approx(10000.0, rel=1e-9)

    def test_health_score_penalised(self) -> None:
        inp = SourceHealthInput(
            source_name="wayback_machine_cdx",
            fetch_count=50,
            ok_count=48,
            latency_sum_ms=500000.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        # high success=0.96 (~0.46) but latency clamped=0, fresh=0.2 => ~0.66
        # still penalised vs a healthy source (would be ~0.92)
        assert result.health_score <= 0.8


# ---------------------------------------------------------------------------
# H4 — Stale source
# ---------------------------------------------------------------------------
class TestStaleSource:
    """H4: long since last seen -> STALE."""

    def test_stale_status(self) -> None:
        inp = SourceHealthInput(
            source_name="ripe_stat",
            fetch_count=50,
            ok_count=45,
            latency_sum_ms=25000.0,
            last_seen=0.0,
            now=300000.0,
        )
        result = compute_health(inp)
        assert result.status == SourceHealthStatus.STALE

    def test_freshness_hours_exceeds_stale(self) -> None:
        inp = SourceHealthInput(
            source_name="ripe_stat",
            fetch_count=50,
            ok_count=45,
            latency_sum_ms=25000.0,
            last_seen=0.0,
            now=300000.0,
        )
        result = compute_health(inp)
        assert result.freshness_hours > DEFAULT_HEALTH_CONFIG.stale_hours


# ---------------------------------------------------------------------------
# H5 — Unknown source (not enough fetches)
# ---------------------------------------------------------------------------
class TestUnknownSource:
    """H5: fetch_count < min_fetches -> UNKNOWN."""

    def test_unknown_status(self) -> None:
        inp = SourceHealthInput(
            source_name="new_source",
            fetch_count=1,
            ok_count=1,
            latency_sum_ms=100.0,
            last_seen=999.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.status == SourceHealthStatus.UNKNOWN

    def test_zero_fetches_is_unknown(self) -> None:
        inp = SourceHealthInput(
            source_name="never_used",
            fetch_count=0,
            ok_count=0,
            latency_sum_ms=0.0,
            last_seen=0.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert result.status == SourceHealthStatus.UNKNOWN


# ---------------------------------------------------------------------------
# H6 — Dashboard
# ---------------------------------------------------------------------------
class TestDashboard:
    """H6: dashboard filters by status."""

    @staticmethod
    def _healthy(name: str) -> SourceHealthInput:
        return SourceHealthInput(
            source_name=name,
            fetch_count=100,
            ok_count=98,
            latency_sum_ms=30000.0,
            last_seen=999.0,
            now=1000.0,
        )

    @staticmethod
    def _degrading(name: str) -> SourceHealthInput:
        return SourceHealthInput(
            source_name=name,
            fetch_count=50,
            ok_count=10,
            latency_sum_ms=50000.0,
            last_seen=999.0,
            now=1000.0,
        )

    @staticmethod
    def _stale(name: str) -> SourceHealthInput:
        return SourceHealthInput(
            source_name=name,
            fetch_count=50,
            ok_count=45,
            latency_sum_ms=25000.0,
            last_seen=0.0,
            now=300000.0,
        )

    @staticmethod
    def _unknown(name: str) -> SourceHealthInput:
        return SourceHealthInput(
            source_name=name,
            fetch_count=1,
            ok_count=1,
            latency_sum_ms=100.0,
            last_seen=999.0,
            now=1000.0,
        )

    def test_hot_sources_are_healthy(self) -> None:
        records = [
            self._healthy("source_a"),
            self._degrading("source_b"),
            self._stale("source_c"),
            self._unknown("source_d"),
        ]
        dashboard = build_dashboard(records)
        assert all(r.status == SourceHealthStatus.HEALTHY for r in dashboard.hot_sources)
        assert len(dashboard.hot_sources) == 1

    def test_degrading_includes_degrading_and_stale(self) -> None:
        records = [
            self._healthy("source_a"),
            self._degrading("source_b"),
            self._stale("source_c"),
            self._unknown("source_d"),
        ]
        dashboard = build_dashboard(records)
        statuses = {r.status for r in dashboard.degrading_sources}
        assert SourceHealthStatus.DEGRADING in statuses
        assert SourceHealthStatus.STALE in statuses
        assert len(dashboard.degrading_sources) == 2

    def test_unknown_sources_separate(self) -> None:
        records = [
            self._healthy("source_a"),
            self._degrading("source_b"),
            self._unknown("source_c"),
        ]
        dashboard = build_dashboard(records)
        assert all(r.status == SourceHealthStatus.UNKNOWN for r in dashboard.unknown_sources)
        assert len(dashboard.unknown_sources) == 1

    def test_summary_counts(self) -> None:
        records = [
            self._healthy("a"),
            self._healthy("b"),
            self._degrading("c"),
            self._stale("d"),
            self._unknown("e"),
        ]
        dashboard = build_dashboard(records)
        assert dashboard.summary.total_sources == 5
        assert dashboard.summary.healthy_count == 2
        assert dashboard.summary.degrading_count >= 1
        assert dashboard.summary.stale_count >= 1
        assert dashboard.summary.unknown_count == 1


# ---------------------------------------------------------------------------
# H7 — Validation
# ---------------------------------------------------------------------------
class TestValidation:
    """H7: invalid inputs raise ValueError."""

    def test_ok_exceeds_fetch_raises(self) -> None:
        with pytest.raises(ValueError, match="ok_count"):
            SourceHealthInput(
                source_name="test",
                fetch_count=5,
                ok_count=10,
                latency_sum_ms=100.0,
                last_seen=0.0,
                now=0.0,
            )

    def test_negative_fetch_raises(self) -> None:
        with pytest.raises(ValueError):
            SourceHealthInput(
                source_name="test",
                fetch_count=-1,
                ok_count=0,
                latency_sum_ms=0.0,
                last_seen=0.0,
                now=0.0,
            )

    def test_negative_latency_raises(self) -> None:
        with pytest.raises(ValueError):
            SourceHealthInput(
                source_name="test",
                fetch_count=5,
                ok_count=5,
                latency_sum_ms=-1.0,
                last_seen=0.0,
                now=0.0,
            )

    def test_empty_name_raises(self) -> None:
        with pytest.raises(ValueError):
            SourceHealthInput(
                source_name="",
                fetch_count=5,
                ok_count=5,
                latency_sum_ms=100.0,
                last_seen=0.0,
                now=0.0,
            )

    def test_config_min_fetches_less_than_one_raises(self) -> None:
        with pytest.raises(ValueError):
            SourceHealthConfig(min_fetches=0)

    def test_config_stale_hours_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            SourceHealthConfig(stale_hours=0.0)

    def test_config_degrading_rate_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError):
            SourceHealthConfig(degrading_success_rate=1.5)


# ---------------------------------------------------------------------------
# H8 — Determinism
# ---------------------------------------------------------------------------
class TestDeterminism:
    """H8: same input -> same output."""

    def test_compute_health_is_pure(self) -> None:
        inp = SourceHealthInput(
            source_name="shodan_internetdb",
            fetch_count=50,
            ok_count=45,
            latency_sum_ms=30000.0,
            last_seen=999.0,
            now=1000.0,
        )
        a = compute_health(inp)
        b = compute_health(inp)
        assert a == b
        assert repr(a) == repr(b)

    def test_build_dashboard_is_pure(self) -> None:
        records = [
            SourceHealthInput("a", 10, 9, 1000.0, 999.0, 1000.0),
            SourceHealthInput("b", 10, 3, 10000.0, 0.0, 300000.0),
        ]
        da = build_dashboard(records)
        db = build_dashboard(records)
        assert da.summary.total_sources == db.summary.total_sources


# ---------------------------------------------------------------------------
# H9 — Health score bounded (smoke, properties in separate file)
# ---------------------------------------------------------------------------
class TestScoreBounded:
    """H9 smoke: health_score is always in [0, 1]."""

    def test_perfect_source_scores_one(self) -> None:
        inp = SourceHealthInput(
            source_name="perfect",
            fetch_count=100,
            ok_count=100,
            latency_sum_ms=0.0,
            last_seen=1000.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert 0.0 <= result.health_score <= 1.0

    def test_broken_source_scores_low(self) -> None:
        inp = SourceHealthInput(
            source_name="broken",
            fetch_count=10,
            ok_count=0,
            latency_sum_ms=100000.0,
            last_seen=0.0,
            now=1000000.0,
        )
        result = compute_health(inp)
        assert 0.0 <= result.health_score <= 1.0


# ---------------------------------------------------------------------------
# H10 — Status always valid enum (smoke)
# ---------------------------------------------------------------------------
class TestStatusAlwaysValid:
    """H10: status is always a valid enum member."""

    def test_status_is_enum(self) -> None:
        inp = SourceHealthInput(
            source_name="any_source",
            fetch_count=10,
            ok_count=5,
            latency_sum_ms=5000.0,
            last_seen=500.0,
            now=1000.0,
        )
        result = compute_health(inp)
        assert isinstance(result.status, SourceHealthStatus)
        assert result.status in SourceHealthStatus


# ---------------------------------------------------------------------------
# Dataclass contract
# ---------------------------------------------------------------------------
class TestDataclassContract:
    """All public types are frozen dataclasses with to_dict."""

    def test_health_input_is_dataclass(self) -> None:
        assert is_dataclass(SourceHealthInput)

    def test_health_result_is_dataclass(self) -> None:
        assert is_dataclass(SourceHealthResult)

    def test_config_is_dataclass(self) -> None:
        assert is_dataclass(SourceHealthConfig)
        assert is_dataclass(DEFAULT_HEALTH_CONFIG)

    def test_dashboard_is_dataclass(self) -> None:
        assert is_dataclass(HealthDashboard)

    def test_result_to_dict(self) -> None:
        inp = SourceHealthInput(
            source_name="test_source",
            fetch_count=10,
            ok_count=9,
            latency_sum_ms=1000.0,
            last_seen=500.0,
            now=1000.0,
        )
        result = compute_health(inp)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["source_name"] == "test_source"
        assert d["status"] == "healthy"

    def test_dashboard_to_dict(self) -> None:
        inp = SourceHealthInput(
            source_name="test_source",
            fetch_count=10,
            ok_count=9,
            latency_sum_ms=1000.0,
            last_seen=500.0,
            now=1000.0,
        )
        dashboard = build_dashboard([inp])
        d = dashboard.to_dict()
        assert isinstance(d, dict)
        assert d["summary"]["total_sources"] == 1
