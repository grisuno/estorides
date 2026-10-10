# estorides_core: hypothesis_engine

*Community 3 | 19 files | cohesion 0.66*

## Definition

This community groups 19 file(s) rooted at `tests` with dominant language py (cohesion 0.66). Central symbols: `Change`, `ChangeConfig`, `ChangeReport`, `ChangeSummary`, `ConfidenceInput`, `ConfidenceResult`, `Credibility`, `Diff`. Core file: `tests/test_reliability_scoring.py` (70 symbols). Documented purpose: estorides_core.change_detection.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/change_detection.py` | py | utility | 20 | yes |
| `estorides_core/fusion_analytics.py` | py | utility | 14 | yes |
| `estorides_core/fusion_store.py` | py | data_access | 18 | yes |
| `estorides_core/hypothesis_engine.py` | py | utility | 23 | yes |
| `estorides_core/ids.py` | py | utility | 1 | yes |
| `estorides_core/recon_fusion.py` | py | utility | 19 | yes |
| `estorides_core/reliability_scoring.py` | py | utility | 16 | yes |
| `tests/properties/test_change_detection_properties.py` | py | testing | 8 | yes |
| `tests/properties/test_hypothesis_engine_properties.py` | py | testing | 9 | yes |
| `tests/properties/test_recon_fusion_properties.py` | py | testing | 17 | yes |
| `tests/properties/test_reliability_scoring_properties.py` | py | testing | 12 | yes |
| `tests/test_change_detection.py` | py | testing | 43 | yes |
| `tests/test_fusion_analytics.py` | py | testing | 36 | yes |
| `tests/test_hypothesis_engine.py` | py | testing | 35 | yes |
| `tests/test_ids.py` | py | testing | 7 | yes |
| `tests/test_probabilistic_fusion.py` | py | testing | 27 | yes |
| `tests/test_recon_fusion.py` | py | testing | 33 | yes |
| `tests/test_reliability_scoring.py` | py | testing | 70 | yes |
| `tests/test_ui_professional.py` | py | testing | 39 | yes |

## Key Symbols

- `Edge` (class, `estorides_core/change_detection.py:59`) `class Edge` - Outgoing edge: typed destination + relation name.
- `SnapshotEntity` (class, `estorides_core/change_detection.py:67`) `class SnapshotEntity` - One entity as captured at snapshot time.
- `__post_init__` (method, `estorides_core/change_detection.py:85`) `def __post_init__(self)`
- `Snapshot` (class, `estorides_core/change_detection.py:97`) `class Snapshot` - An immutable view of an investigation at one point in time.
- `ChangeConfig` (class, `estorides_core/change_detection.py:105`) `class ChangeConfig` - Tuning for :func:`detect_changes`.
- `__post_init__` (method, `estorides_core/change_detection.py:116`) `def __post_init__(self)`
- `Diff` (class, `estorides_core/change_detection.py:126`) `class Diff` - Structured description of a single change's delta.
- `Change` (class, `estorides_core/change_detection.py:135`) `class Change` - One detected change.
- `ChangeSummary` (class, `estorides_core/change_detection.py:152`) `class ChangeSummary` - Aggregate stats for a :class:`ChangeReport`.
- `ChangeReport` (class, `estorides_core/change_detection.py:169`) `class ChangeReport` - Top-N changes + summary stats for a single diff operation.
- `_truncate_key` (method, `estorides_core/change_detection.py:177`) `def _truncate_key(key)`
- `_change_id` (method, `estorides_core/change_detection.py:184`) `def _change_id(kind, entity_id, diff_signature)`
- `_reliability_floor` (method, `estorides_core/change_detection.py:188`) `def _reliability_floor(letter)` - A=1, B=2, ..., F=6. For 'min_reliability' comparison.
- `_filter_sources_by_reliability` (method, `estorides_core/change_detection.py:193`) `def _filter_sources_by_reliability(sources, min_reliability)`
- `_property_diff` (method, `estorides_core/change_detection.py:206`) `def _property_diff(before, after)` - Compute the per-key add/change/remove between two property maps.
- `_edge_set` (method, `estorides_core/change_detection.py:225`) `def _edge_set(edges)`
- `_union_sources` (method, `estorides_core/change_detection.py:229`) `def _union_sources(a, b)` - Sorted union of two entities' source lists.
- `_make_change` (method, `estorides_core/change_detection.py:241`) `def _make_change(kind, entity_id, entity_type, entity_value, sig)` - Build a :class:`Change` with the deterministic id derived from
- `_below_min_reliability` (method, `estorides_core/change_detection.py:274`) `def _below_min_reliability(source, min_reliability)` - True if a source's reliability is strictly *worse* than the
- `detect_changes` (method, `estorides_core/change_detection.py:284`) `def detect_changes(snapshot_before, snapshot_after)` - Diff two snapshots. Pure: no I/O, deterministic, bounded.
- `FusionAnalytics` (class, `estorides_core/fusion_analytics.py:31`) `class FusionAnalytics` - Read-only analytics queries over the fusion store.
- `__init__` (method, `estorides_core/fusion_analytics.py:40`) `def __init__(self, store)`
- `entity_timeline` (method, `estorides_core/fusion_analytics.py:46`) `def entity_timeline(self, eid)`
- `entity_summary` (method, `estorides_core/fusion_analytics.py:132`) `def entity_summary(self, eid)`
- `source_stats` (method, `estorides_core/fusion_analytics.py:213`) `def source_stats(self, source_name)`
- `multi_source_consensus` (method, `estorides_core/fusion_analytics.py:290`) `def multi_source_consensus(self, eid, key)`
- `corroborated_properties` (method, `estorides_core/fusion_analytics.py:343`) `def corroborated_properties(self, eid, min_sources)`
- `entity_search` (method, `estorides_core/fusion_analytics.py:374`) `def entity_search(self, term, etype)`
- `top_changed` (method, `estorides_core/fusion_analytics.py:432`) `def top_changed(self, days, limit)`
- `source_corroboration_matrix` (method, `estorides_core/fusion_analytics.py:477`) `def source_corroboration_matrix(self, limit)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 31
- Cross-boundary resolved imports (EXTRACTED): 14

## Connections

- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/fusion_store.py.
- [EXTRACTED] depends_on community 8 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/entity_resolution.py imports estorides_core/ids.py.
- [EXTRACTED] depends_on community 3 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/fusion_store.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 0 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/orchestrator.py imports estorides_core/recon_fusion.py.

## Risks

- [layer strict] `estorides_web.py` (presentation) -> `estorides_core/fusion_store.py` (data_access)

## Open Questions

- What would break if the most connected file in estorides_core: hypothesis_engine changed?
- Should estorides_core: hypothesis_engine be split, given cohesion 0.66?

## Sources

- `estorides_core/change_detection.py`
- `estorides_core/fusion_analytics.py`
- `estorides_core/fusion_store.py`
- `estorides_core/hypothesis_engine.py`
- `estorides_core/ids.py`
- `estorides_core/recon_fusion.py`
- `estorides_core/reliability_scoring.py`
- `tests/properties/test_change_detection_properties.py`
- `tests/properties/test_hypothesis_engine_properties.py`
- `tests/properties/test_recon_fusion_properties.py`
- `tests/properties/test_reliability_scoring_properties.py`
- `tests/test_change_detection.py`
- `tests/test_fusion_analytics.py`
- `tests/test_hypothesis_engine.py`
- `tests/test_ids.py`
- `tests/test_probabilistic_fusion.py`
- `tests/test_recon_fusion.py`
- `tests/test_reliability_scoring.py`
- `tests/test_ui_professional.py`
