"""
estorides_core.source_health_monitoring
=======================================
Per-source operational health tracking.

Computes health status (healthy/degrading/stale/unknown), composite health
score, and a dashboard of hot vs degrading sources from raw fetch counters.
Pure functions: no I/O, no logging, deterministic.

Public surface::

    SourceHealthStatus  enum  {healthy, degrading, stale, unknown}
    SourceHealthInput   dataclass, validated
    SourceHealthResult  dataclass frozen, JSON-serialisable
    SourceHealthConfig  dataclass, validated
    HealthDashboard     dataclass frozen, JSON-serialisable
    compute_health      pure, O(1)
    build_dashboard     pure, O(n)
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum


# --------------------------------------------------------------------------- helpers (module-level, no _env_* to keep pure)
def _env_float(name: str, default: float) -> float:
    """Read a float env var, falling back to default on absence/error."""
    import os
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    """Read an int env var, falling back to default on absence/error."""
    import os
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


# --------------------------------------------------------------------------- enums
class SourceHealthStatus(str, Enum):
    """Operational health classification for an OSINT source."""

    HEALTHY = "healthy"
    DEGRADING = "degrading"
    STALE = "stale"
    UNKNOWN = "unknown"


# --------------------------------------------------------------------------- config
@dataclass(frozen=True)
class SourceHealthConfig:
    """Thresholds for source health classification.

    Every field has a corresponding ``ESTORIDES_HEALTH_*`` environment
    variable override at import time. The defaults are conservative:
    three failures in ten = degrading; a week offline = stale.
    """

    min_fetches: int = 3
    degrading_success_rate: float = 0.6
    degrading_latency_ms: float = 5000.0
    stale_hours: float = 72.0
    healthy_success_rate: float = 0.9
    healthy_latency_ms: float = 2000.0
    hot_min_entities: int = 10

    def __post_init__(self) -> None:
        if self.min_fetches < 1:
            raise ValueError(f"min_fetches must be >= 1, got {self.min_fetches}")
        if self.stale_hours <= 0.0:
            raise ValueError(f"stale_hours must be > 0, got {self.stale_hours}")
        if not 0.0 <= self.degrading_success_rate <= 1.0:
            raise ValueError(
                f"degrading_success_rate must be in [0, 1], got {self.degrading_success_rate}"
            )
        if not 0.0 <= self.healthy_success_rate <= 1.0:
            raise ValueError(
                f"healthy_success_rate must be in [0, 1], got {self.healthy_success_rate}"
            )
        if self.degrading_latency_ms < 0.0:
            raise ValueError(
                f"degrading_latency_ms must be >= 0, got {self.degrading_latency_ms}"
            )
        if self.healthy_latency_ms < 0.0:
            raise ValueError(
                f"healthy_latency_ms must be >= 0, got {self.healthy_latency_ms}"
            )
        if self.hot_min_entities < 0:
            raise ValueError(
                f"hot_min_entities must be >= 0, got {self.hot_min_entities}"
            )


DEFAULT_HEALTH_CONFIG: SourceHealthConfig = SourceHealthConfig(
    min_fetches=_env_int("ESTORIDES_HEALTH_MIN_FETCHES", 3),
    degrading_success_rate=_env_float("ESTORIDES_HEALTH_DEGRADING_SR", 0.6),
    degrading_latency_ms=_env_float("ESTORIDES_HEALTH_DEGRADING_LATENCY", 5000.0),
    stale_hours=_env_float("ESTORIDES_HEALTH_STALE_HOURS", 72.0),
    healthy_success_rate=_env_float("ESTORIDES_HEALTH_HEALTHY_SR", 0.9),
    healthy_latency_ms=_env_float("ESTORIDES_HEALTH_HEALTHY_LATENCY", 2000.0),
    hot_min_entities=_env_int("ESTORIDES_HEALTH_HOT_MIN_ENTITIES", 10),
)


# --------------------------------------------------------------------------- dataclasses
@dataclass(frozen=True)
class SourceHealthInput:
    """Raw per-source data for health computation.

    All fields are required; the caller (orchestrator, fusion analytics)
    extracts these from the fusion store or its own tracking.
    """

    source_name: str
    fetch_count: int
    ok_count: int
    latency_sum_ms: float
    last_seen: float
    now: float

    def __post_init__(self) -> None:
        if not self.source_name:
            raise ValueError("source_name must be non-empty")
        if self.fetch_count < 0:
            raise ValueError(f"fetch_count must be >= 0, got {self.fetch_count}")
        if self.ok_count < 0:
            raise ValueError(f"ok_count must be >= 0, got {self.ok_count}")
        if self.ok_count > self.fetch_count:
            raise ValueError(
                f"ok_count ({self.ok_count}) must not exceed fetch_count ({self.fetch_count})"
            )
        if self.latency_sum_ms < 0.0:
            raise ValueError(
                f"latency_sum_ms must be >= 0, got {self.latency_sum_ms}"
            )
        if self.last_seen < 0.0:
            raise ValueError(f"last_seen must be >= 0, got {self.last_seen}")
        if self.now < 0.0:
            raise ValueError(f"now must be >= 0, got {self.now}")


@dataclass(frozen=True)
class SourceHealthResult:
    """Health assessment for a single source."""

    source_name: str
    status: SourceHealthStatus
    success_rate: float
    avg_latency_ms: float
    freshness_hours: float
    health_score: float
    fetch_count: int
    unique_entity_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "source_name": self.source_name,
            "status": self.status.value,
            "success_rate": round(self.success_rate, 4),
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "freshness_hours": round(self.freshness_hours, 4),
            "health_score": round(self.health_score, 4),
            "fetch_count": self.fetch_count,
            "unique_entity_count": self.unique_entity_count,
        }


@dataclass(frozen=True)
class DashboardSummary:
    """Aggregate dashboard statistics."""

    total_sources: int
    healthy_count: int
    degrading_count: int
    stale_count: int
    unknown_count: int
    avg_health_score: float
    computed_at: float = 0.0


@dataclass(frozen=True)
class HealthDashboard:
    """Grouped health view: hot sources, degrading sources, aggregate stats."""

    hot_sources: list[SourceHealthResult] = field(default_factory=list)
    degrading_sources: list[SourceHealthResult] = field(default_factory=list)
    unknown_sources: list[SourceHealthResult] = field(default_factory=list)
    summary: DashboardSummary = field(default_factory=lambda: DashboardSummary(
        total_sources=0, healthy_count=0, degrading_count=0,
        stale_count=0, unknown_count=0, avg_health_score=0.0,
    ))

    def to_dict(self) -> dict[str, object]:
        return {
            "hot_sources": [r.to_dict() for r in self.hot_sources],
            "degrading_sources": [r.to_dict() for r in self.degrading_sources],
            "unknown_sources": [r.to_dict() for r in self.unknown_sources],
            "summary": {
                "total_sources": self.summary.total_sources,
                "healthy_count": self.summary.healthy_count,
                "degrading_count": self.summary.degrading_count,
                "stale_count": self.summary.stale_count,
                "unknown_count": self.summary.unknown_count,
                "avg_health_score": round(self.summary.avg_health_score, 4),
                "computed_at": self.summary.computed_at,
            },
        }


# --------------------------------------------------------------------------- core logic
def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


def _classify(
    success_rate: float,
    avg_latency_ms: float,
    freshness_hours: float,
    fetch_count: int,
    config: SourceHealthConfig,
) -> SourceHealthStatus:
    """Classify a source's health status based on thresholds."""
    if fetch_count < config.min_fetches:
        return SourceHealthStatus.UNKNOWN
    if freshness_hours > config.stale_hours:
        return SourceHealthStatus.STALE
    if (
        success_rate < config.degrading_success_rate
        or avg_latency_ms > config.degrading_latency_ms
    ):
        return SourceHealthStatus.DEGRADING
    if (
        success_rate >= config.healthy_success_rate
        and avg_latency_ms <= config.healthy_latency_ms
    ):
        return SourceHealthStatus.HEALTHY
    return SourceHealthStatus.DEGRADING


def compute_health(
    inp: SourceHealthInput,
    config: SourceHealthConfig = DEFAULT_HEALTH_CONFIG,
) -> SourceHealthResult:
    """Compute the health assessment for a single source.

    Pure: no I/O, no logging, deterministic. The formula is::

        success_weight = success_rate ^ 2
        latency_weight = clamp(1 - avg_latency_s / degrading_latency_s, 0, 1)
        freshness_weight = clamp(1 - freshness_hours / stale_hours, 0, 1)
        health_score = 0.5 * success_weight + 0.3 * latency_weight + 0.2 * freshness_weight
    """
    fetch_count = inp.fetch_count
    ok_count = inp.ok_count

    success_rate = ok_count / fetch_count if fetch_count > 0 else 0.0
    avg_latency_ms = inp.latency_sum_ms / fetch_count if fetch_count > 0 else 0.0
    age_seconds = max(0.0, inp.now - inp.last_seen)
    freshness_hours = age_seconds / 3600.0

    status = _classify(
        success_rate=success_rate,
        avg_latency_ms=avg_latency_ms,
        freshness_hours=freshness_hours,
        fetch_count=fetch_count,
        config=config,
    )

    success_weight = success_rate * success_rate
    degrading_latency_s = config.degrading_latency_ms / 1000.0
    avg_latency_s = avg_latency_ms / 1000.0
    if degrading_latency_s > 0.0:
        latency_weight = _clamp01(
            1.0 - (avg_latency_s / degrading_latency_s)
        )
    else:
        latency_weight = 0.0
    if config.stale_hours > 0.0:
        freshness_weight = _clamp01(
            1.0 - (freshness_hours / config.stale_hours)
        )
    else:
        freshness_weight = 0.0

    health_score = _clamp01(
        0.5 * success_weight + 0.3 * latency_weight + 0.2 * freshness_weight
    )

    return SourceHealthResult(
        source_name=inp.source_name,
        status=status,
        success_rate=success_rate,
        avg_latency_ms=avg_latency_ms,
        freshness_hours=freshness_hours,
        health_score=health_score,
        fetch_count=fetch_count,
    )


def build_dashboard(
    records: Iterable[SourceHealthInput],
    config: SourceHealthConfig = DEFAULT_HEALTH_CONFIG,
) -> HealthDashboard:
    """Build a health dashboard from per-source health inputs.

    Groups sources into hot (healthy), degrading (degrading + stale), and
    unknown lists. Computes aggregate summary statistics.
    """
    results = [compute_health(r, config) for r in records]

    hot: list[SourceHealthResult] = []
    degrading: list[SourceHealthResult] = []
    unknown: list[SourceHealthResult] = []

    for r in results:
        if r.status == SourceHealthStatus.UNKNOWN:
            unknown.append(r)
        elif r.status == SourceHealthStatus.HEALTHY:
            hot.append(r)
        else:
            degrading.append(r)

    hot.sort(key=lambda r: (-r.health_score, r.source_name))
    degrading.sort(key=lambda r: (r.health_score, r.source_name))
    unknown.sort(key=lambda r: r.source_name)

    total = len(results)
    healthy_count = len(hot)
    degrading_count = sum(1 for r in results if r.status == SourceHealthStatus.DEGRADING)
    stale_count = sum(1 for r in results if r.status == SourceHealthStatus.STALE)
    unknown_count = len(unknown)
    avg_score = (
        sum(r.health_score for r in results) / total
        if total > 0 else 0.0
    )

    summary = DashboardSummary(
        total_sources=total,
        healthy_count=healthy_count,
        degrading_count=degrading_count,
        stale_count=stale_count,
        unknown_count=unknown_count,
        avg_health_score=avg_score,
    )

    return HealthDashboard(
        hot_sources=hot,
        degrading_sources=degrading,
        unknown_sources=unknown,
        summary=summary,
    )


__all__ = [
    "DEFAULT_HEALTH_CONFIG",
    "DashboardSummary",
    "HealthDashboard",
    "SourceHealthConfig",
    "SourceHealthInput",
    "SourceHealthResult",
    "SourceHealthStatus",
    "build_dashboard",
    "compute_health",
]
