# estorides_core: source_health_monitoring

*Community 9 | 3 files | cohesion 1.00*

## Definition

This community groups 3 file(s) rooted at `tests/properties` with dominant language py (cohesion 1.00). Central symbols: `DashboardSummary`, `HealthDashboard`, `SourceHealthConfig`, `SourceHealthInput`, `SourceHealthResult`, `SourceHealthStatus`, `TestDashboard`, `TestDataclassContract`. Core file: `tests/test_source_health_monitoring.py` (52 symbols). Documented purpose: estorides_core.source_health_monitoring.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/source_health_monitoring.py` | py | utility | 14 | yes |
| `tests/properties/test_source_health_monitoring_properties.py` | py | testing | 7 | yes |
| `tests/test_source_health_monitoring.py` | py | testing | 52 | yes |

## Key Symbols

- `SourceHealthStatus` (class, `estorides_core/source_health_monitoring.py:31`) `class SourceHealthStatus(str, Enum)` - Operational health classification for an OSINT source.
- `SourceHealthConfig` (class, `estorides_core/source_health_monitoring.py:42`) `class SourceHealthConfig` - Thresholds for source health classification.
- `__post_init__` (method, `estorides_core/source_health_monitoring.py:58`) `def __post_init__(self)`
- `SourceHealthInput` (class, `estorides_core/source_health_monitoring.py:98`) `class SourceHealthInput` - Raw per-source data for health computation.
- `__post_init__` (method, `estorides_core/source_health_monitoring.py:112`) `def __post_init__(self)`
- `SourceHealthResult` (class, `estorides_core/source_health_monitoring.py:134`) `class SourceHealthResult` - Health assessment for a single source.
- `to_dict` (method, `estorides_core/source_health_monitoring.py:146`) `def to_dict(self)`
- `DashboardSummary` (class, `estorides_core/source_health_monitoring.py:160`) `class DashboardSummary` - Aggregate dashboard statistics.
- `HealthDashboard` (class, `estorides_core/source_health_monitoring.py:173`) `class HealthDashboard` - Grouped health view: hot sources, degrading sources, aggregate stats.
- `to_dict` (method, `estorides_core/source_health_monitoring.py:184`) `def to_dict(self)`
- `_clamp01` (method, `estorides_core/source_health_monitoring.py:202`) `def _clamp01(value)`
- `_classify` (method, `estorides_core/source_health_monitoring.py:210`) `def _classify(success_rate, avg_latency_ms, freshness_hours, fetch_count, config` - Classify a source's health status based on thresholds.
- `compute_health` (method, `estorides_core/source_health_monitoring.py:235`) `def compute_health(inp, config)` - Compute the health assessment for a single source.
- `build_dashboard` (method, `estorides_core/source_health_monitoring.py:295`) `def build_dashboard(records, config)` - Build a health dashboard from per-source health inputs.
- `_valid_input` (function, `tests/properties/test_source_health_monitoring_properties.py:21`) `def _valid_input(fetch, ok, latency, last_seen, now)` - Build a valid SourceHealthInput, clamping ok <= fetch.
- `test_health_score_always_bounded` (function, `tests/properties/test_source_health_monitoring_properties.py:49`) `def test_health_score_always_bounded(fetch, ok, latency, last_seen, now)`
- `test_status_always_valid_enum` (function, `tests/properties/test_source_health_monitoring_properties.py:63`) `def test_status_always_valid_enum(fetch, ok, latency, last_seen, now)`
- `test_success_rate_bounds` (function, `tests/properties/test_source_health_monitoring_properties.py:78`) `def test_success_rate_bounds(fetch, ok, latency, last_seen, now)`
- `test_unknown_when_below_min_fetches` (function, `tests/properties/test_source_health_monitoring_properties.py:89`) `def test_unknown_when_below_min_fetches(fetch, config_min)`
- `valid_health_inputs` (function, `tests/properties/test_source_health_monitoring_properties.py:97`) `def valid_health_inputs(draw)`
- `test_dashboard_summary_counts_match` (function, `tests/properties/test_source_health_monitoring_properties.py:112`) `def test_dashboard_summary_counts_match(records)` - Dashboard summary counts must sum to total.
- `TestHealthySource` (class, `tests/test_source_health_monitoring.py:29`) `class TestHealthySource` - H1: high success rate, low latency -> HEALTHY.
- `test_healthy_status` (method, `tests/test_source_health_monitoring.py:32`) `def test_healthy_status(self)`
- `test_success_rate_computed` (method, `tests/test_source_health_monitoring.py:44`) `def test_success_rate_computed(self)`
- `test_avg_latency_computed` (method, `tests/test_source_health_monitoring.py:56`) `def test_avg_latency_computed(self)`
- `test_freshness_hours_computed` (method, `tests/test_source_health_monitoring.py:68`) `def test_freshness_hours_computed(self)`
- `test_health_score_high_band` (method, `tests/test_source_health_monitoring.py:80`) `def test_health_score_high_band(self)`
- `TestDegradingLowSuccess` (class, `tests/test_source_health_monitoring.py:97`) `class TestDegradingLowSuccess` - H2: low success rate -> DEGRADING.
- `test_degrading_status` (method, `tests/test_source_health_monitoring.py:100`) `def test_degrading_status(self)`
- `test_success_rate_reflects_failures` (method, `tests/test_source_health_monitoring.py:112`) `def test_success_rate_reflects_failures(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 2
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in estorides_core: source_health_monitoring changed?
- Should estorides_core: source_health_monitoring be split, given cohesion 1.00?

## Sources

- `estorides_core/source_health_monitoring.py`
- `tests/properties/test_source_health_monitoring_properties.py`
- `tests/test_source_health_monitoring.py`
