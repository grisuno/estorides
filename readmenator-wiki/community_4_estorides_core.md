# estorides_core

*Community 4 | 11 files | cohesion 0.72*

## Definition

This community groups 11 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.72). Central symbols: `Change`, `ChangeConfig`, `ChangeReport`, `ChangeSummary`, `ConfidenceInput`, `ConfidenceResult`, `Credibility`, `Diff`. Core file: `tests/test_reliability_scoring.py` (70 symbols). Documented purpose: estorides_core.change_detection.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/change_detection.py` | py | utility | 20 | yes |
| `estorides_core/hypothesis_engine.py` | py | utility | 23 | yes |
| `estorides_core/ids.py` | py | utility | 1 | yes |
| `estorides_core/reliability_scoring.py` | py | utility | 16 | yes |
| `tests/properties/test_change_detection_properties.py` | py | testing | 8 | yes |
| `tests/properties/test_hypothesis_engine_properties.py` | py | testing | 9 | yes |
| `tests/properties/test_reliability_scoring_properties.py` | py | testing | 12 | yes |
| `tests/test_change_detection.py` | py | testing | 43 | yes |
| `tests/test_hypothesis_engine.py` | py | testing | 35 | yes |
| `tests/test_ids.py` | py | testing | 7 | yes |
| `tests/test_reliability_scoring.py` | py | testing | 70 | yes |

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
- `EntityRef` (class, `estorides_core/hypothesis_engine.py:57`) `class EntityRef` - A typed reference to an entity involved in a hypothesis.
- `Evidence` (class, `estorides_core/hypothesis_engine.py:65`) `class Evidence` - One piece of supporting or contradicting evidence.
- `Hypothesis` (class, `estorides_core/hypothesis_engine.py:76`) `class Hypothesis` - A typed, scored, auditable intelligence conclusion.
- `_truncate` (method, `estorides_core/hypothesis_engine.py:113`) `def _truncate(value)` - Stringify a value, bounded to ``_VALUE_MAX_CHARS``.
- `_is_mapping` (method, `estorides_core/hypothesis_engine.py:123`) `def _is_mapping(value)`
- `_entity_lookup` (method, `estorides_core/hypothesis_engine.py:127`) `def _entity_lookup(entities)` - Build ``{type: {value, value, ...}}`` from the entity list.
- `_hypothesis_id` (method, `estorides_core/hypothesis_engine.py:148`) `def _hypothesis_id(htype, entity_refs, supporting)` - Deterministic 16-char hex id for a hypothesis.
- `_score` (method, `estorides_core/hypothesis_engine.py:166`) `def _score(supporting, contradicting)` - Net-support score in (0, 1].
- `_confidence` (method, `estorides_core/hypothesis_engine.py:180`) `def _confidence(supporting, contradicting)` - Reliability-weighted confidence via :mod:`reliability_scoring`.
- `_clip_claim` (method, `estorides_core/hypothesis_engine.py:201`) `def _clip_claim(template)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 20
- Cross-boundary resolved imports (EXTRACTED): 5

## Connections

- [EXTRACTED] depends_on community 6 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/entity_resolution.py imports estorides_core/ids.py.
- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/fusion_store.py imports estorides_core/ids.py.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in estorides_core changed?
- Should estorides_core be split, given cohesion 0.72?

## Sources

- `estorides_core/change_detection.py`
- `estorides_core/hypothesis_engine.py`
- `estorides_core/ids.py`
- `estorides_core/reliability_scoring.py`
- `tests/properties/test_change_detection_properties.py`
- `tests/properties/test_hypothesis_engine_properties.py`
- `tests/properties/test_reliability_scoring_properties.py`
- `tests/test_change_detection.py`
- `tests/test_hypothesis_engine.py`
- `tests/test_ids.py`
- `tests/test_reliability_scoring.py`
