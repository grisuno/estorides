# `source_health_monitoring` — Spec

> Per-source health tracking and dashboard. Computes success rate, average
> latency, freshness, and a composite health score for every OSINT source,
> then classifies each source as healthy, degrading, stale, or unknown and
> surfaces the "hot" (high-value, reliable) and "degrading" (failing, stale)
> sources for operator awareness.

---

## Purpose

The fusion store's `fusion_sources` table already tracks `fetch_count` and
`ok_count` per source, but these numbers are raw counters — they do not
answer the operational question "which sources should I trust right now?"
A source that worked well yesterday might be failing today; a source that
has never been queried is an unknown.

This module provides a set of pure functions that take per-source health
data (fetches, successes, latency, last-seen timestamp) and produce:

1. **Health status** — `healthy`, `degrading`, `stale`, or `unknown`.
2. **Health score** — `[0.0, 1.0]` composite based on success rate,
   latency, and freshness.
3. **Dashboard** — sorted lists of hot sources (healthy + high output)
   and degrading sources (failing or stale), plus aggregate statistics.

The module does no I/O. It expects the caller (orchestrator, fusion
analytics, API) to pass in source records from the fusion store or any
other data source.

---

## Inputs

### `SourceHealthInput`

| Field | Type | Range | Default | Notes |
|-------|------|-------|---------|-------|
| `source_name` | `str` | non-empty | required | Source name matching `fusion_sources.name` |
| `fetch_count` | `int` | `>= 0` | `0` | Total fetch attempts |
| `ok_count` | `int` | `>= 0` | `0` | Successful fetches (must be <= fetch_count) |
| `latency_sum_ms` | `float` | `>= 0.0` | `0.0` | Cumulative latency of all fetches |
| `last_seen` | `float` | `>= 0.0` | `0.0` | Unix timestamp of last fetch |
| `now` | `float` | `>= 0.0` | `0.0` | Current time (passed in for determinism) |

Validation: `ValueError` if `ok_count > fetch_count`, any negative value,
or empty `source_name`.

### `HealthDashboardInput`

| Field | Type | Range | Notes |
|-------|------|-------|-------|
| `source_health` | `Iterable[SourceHealthInput]` | — | One per tracked source |
| `config` | `SourceHealthConfig` | — | Thresholds (see below) |

### `SourceHealthConfig`

| Field | Type | Range | Default | Env override |
|-------|------|-------|---------|-------------|
| `min_fetches` | `int` | `>= 1` | `3` | `ESTORIDES_HEALTH_MIN_FETCHES` |
| `degrading_success_rate` | `float` | `[0.0, 1.0]` | `0.6` | `ESTORIDES_HEALTH_DEGRADING_SR` |
| `degrading_latency_ms` | `float` | `>= 0` | `5000.0` (5s) | `ESTORIDES_HEALTH_DEGRADING_LATENCY` |
| `stale_hours` | `float` | `> 0` | `72.0` (3 days) | `ESTORIDES_HEALTH_STALE_HOURS` |
| `healthy_success_rate` | `float` | `[0.0, 1.0]` | `0.9` | `ESTORIDES_HEALTH_HEALTHY_SR` |
| `healthy_latency_ms` | `float` | `>= 0` | `2000.0` (2s) | `ESTORIDES_HEALTH_HEALTHY_LATENCY` |
| `hot_min_entities` | `int` | `>= 0` | `10` | `ESTORIDES_HEALTH_HOT_MIN_ENTITIES` |

All thresholds validated in `__post_init__`.

---

## Outputs

### `SourceHealthResult` (dataclass frozen, JSON-serialisable)

```json
{
  "source_name": "crt_sh_certificates",
  "status": "healthy",
  "success_rate": 0.98,
  "avg_latency_ms": 345.2,
  "freshness_hours": 1.5,
  "health_score": 0.92,
  "fetch_count": 150,
  "unique_entity_count": 0
}
```

| Field | Type | Range | Meaning |
|-------|------|-------|---------|
| `source_name` | `str` | — | Source identifier |
| `status` | `SourceHealthStatus` | enum | Classification |
| `success_rate` | `float` | `[0.0, 1.0]` | `ok_count / fetch_count` |
| `avg_latency_ms` | `float` | `>= 0.0` | `latency_sum_ms / fetch_count` |
| `freshness_hours` | `float` | `>= 0.0` | `(now - last_seen) / 3600` |
| `health_score` | `float` | `[0.0, 1.0]` | Composite (see formula) |
| `fetch_count` | `int` | `>= 0` | Raw fetch count from input |
| `unique_entity_count` | `int` | `>= 0` | Entity count (optional, 0 if not provided) |

### `HealthDashboard`

```json
{
  "hot_sources": [ ... ],
  "degrading_sources": [ ... ],
  "unknown_sources": [ ... ],
  "summary": {
    "total_sources": 99,
    "healthy_count": 65,
    "degrading_count": 12,
    "stale_count": 18,
    "unknown_count": 4,
    "avg_health_score": 0.78,
    "computed_at": 1700000000.0
  }
}
```

---

## Health formula

The composite `health_score` is computed as:

```
success_weight = success_rate ^ 2            # quadratic penalty for failures
latency_weight = clamp(1.0 - avg_latency_s / degrading_latency_s, 0.0, 1.0)
freshness_weight = clamp(1.0 - freshness_hours / stale_hours, 0.0, 1.0)

health_score = 0.5 * success_weight + 0.3 * latency_weight + 0.2 * freshness_weight
```

This weights success rate highest (50 %), latency next (30 %), and
freshness last (20 %) — a source that always returns good data quickly
is more operationally valuable than one that last ran a week ago.

## Status classification

1. If `fetch_count < min_fetches` → `UNKNOWN` (not enough data).
2. If `freshness_hours > stale_hours` → `STALE`.
3. If `success_rate < degrading_success_rate` or
   `avg_latency_ms > degrading_latency_ms` → `DEGRADING`.
4. If `success_rate >= healthy_success_rate` and
   `avg_latency_ms <= healthy_latency_ms` → `HEALTHY`.
5. Otherwise → `DEGRADING` (between healthy and degrading thresholds).

## Error table

| Failure mode | Behaviour |
|---|---|
| `SourceHealthInput` with `ok_count > fetch_count` | `ValueError` |
| `SourceHealthInput` with negative `fetch_count` | `ValueError` |
| `SourceHealthInput` with empty `source_name` | `ValueError` |
| `SourceHealthConfig` with `min_fetches < 1` | `ValueError` |
| `SourceHealthConfig` with `stale_hours <= 0` | `ValueError` |
| Config thresholds outside `[0, 1]` for rates | `ValueError` |

## Security guarantees

1. **Pure functions.** No I/O, no logging, no clock. Time is passed in.
2. **Bounded.** O(n) in source count, no recursion, no unbounded loops.
3. **Fail-loud on input.** Programmer errors raise `ValueError`.
4. **Fail-soft on operator input.** `source_name` is never logged.
5. **Determinism.** Same input → same output bit-by-bit.

## Out of scope

- **Persisting health data to DB.** The caller owns persistence. This
  module reads and classifies.
- **Wiring to fusion_store.** The orchestrator or API layer merges the
  fusion store's counters with this module's classifiers.
- **Alerting / webhook dispatch.** Downstream consumers.
- **Historical trend analysis.** Single-window health, not time series.

---

## BDD scenarios

### H1 · Healthy source with high success rate and low latency

**Given** a `SourceHealthInput` with `fetch_count=100`, `ok_count=98`,
`latency_sum_ms=30000.0`, `last_seen=999.0`, `now=1000.0`  
**When** I compute `compute_health(inp, config)`  
**Then** `status == SourceHealthStatus.HEALTHY`  
**And** `success_rate == 0.98`  
**And** `avg_latency_ms == 300.0`  
**And** `freshness_hours == 1.0 / 3600.0`  
**And** `health_score >= 0.8`.

### H2 · Degrading source due to low success rate

**Given** a `SourceHealthInput` with `fetch_count=50`, `ok_count=20`,
`latency_sum_ms=50000.0`, `last_seen=999.0`, `now=1000.0`  
**When** I compute `compute_health(inp, config)`  
**Then** `status == SourceHealthStatus.DEGRADING`  
**And** `success_rate == 0.4`  
**And** `health_score < 0.5`.

### H3 · Degrading source due to high latency

**Given** a `SourceHealthInput` with `fetch_count=50`, `ok_count=48`,
`latency_sum_ms=500000.0` (10s avg), `last_seen=999.0`, `now=1000.0`  
**When** I compute `compute_health(inp, config)`  
**Then** `status == SourceHealthStatus.DEGRADING`  
**And** `avg_latency_ms == 10000.0`  
**And** `health_score < 0.6`.

### H4 · Stale source

**Given** a `SourceHealthInput` with `fetch_count=50`, `ok_count=45`,
`latency_sum_ms=25000.0`, `last_seen=0.0`, `now=300000.0` (> stale_hours)  
**When** I compute `compute_health(inp, config)`  
**Then** `status == SourceHealthStatus.STALE`.

### H5 · Unknown source (not enough fetches)

**Given** a `SourceHealthInput` with `fetch_count=1`, `ok_count=1`,
`latency_sum_ms=100.0`, `last_seen=999.0`, `now=1000.0`,
`config.min_fetches=3`  
**When** I compute `compute_health(inp, config)`  
**Then** `status == SourceHealthStatus.UNKNOWN`.

### H6 · Dashboard filters hot and degrading sources

**Given** ten `SourceHealthInput` records spanning all four statuses  
**When** I compute `build_dashboard(records, config)`  
**Then** `dashboard.hot_sources` contains only `HEALTHY` sources  
**And** `dashboard.degrading_sources` contains `DEGRADING` and `STALE` sources  
**And** `dashboard.unknown_sources` contains `UNKNOWN` sources  
**And** `dashboard.summary.total_sources == 10`.

### H7 · Validation: ok_count > fetch_count raises

**Given** a `SourceHealthInput` with `fetch_count=5`, `ok_count=10`  
**When** I construct it  
**Then** `ValueError` is raised.

### H8 · Determinism

**Given** the same `SourceHealthInput` and `SourceHealthConfig`  
**When** I call `compute_health` twice  
**Then** both results are bitwise identical.

### H9 · Property: health_score is always bounded

**Given** any valid `SourceHealthInput` and any valid `SourceHealthConfig`  
**When** I compute `compute_health`  
**Then** `0.0 <= health_score <= 1.0`.

### H10 · Property: status is always a valid enum member

**Given** any valid `SourceHealthInput` and any valid `SourceHealthConfig`  
**When** I compute `compute_health`  
**Then** `status in {HEALTHY, DEGRADING, STALE, UNKNOWN}`.
