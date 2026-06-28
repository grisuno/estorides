"""
estorides_core.change_detection
===============================
The temporal layer: "what changed in this investigation since the last
run?". Takes two immutable :class:`Snapshot` objects and emits a
:class:`ChangeReport` listing every new entity, every disappeared one,
every property change, every new source corroboration, and every
edge added/removed. Each :class:`Change` carries an auditable
``score`` reliability-weighted via :mod:`reliability_scoring`.

Pure module: no I/O, no DB writes, no logging of payload, no clock.
Same input ⇒ same output bit-by-bit. Change ids are content hashes
so the case store can deduplicate events across runs.

Public surface::

    detect_changes(snapshot_before, snapshot_after, *, config=ChangeConfig())
        -> ChangeReport
"""
from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from .reliability_scoring import (
    SourceReliability,
    reliability_from_name,
)

# --------------------------------------------------------------------------- constants
#: Stable vocabulary of change kinds. Adding a new kind is a breaking
#: change for downstream consumers (UI, audit log, alert rules).
CHANGE_KINDS: frozenset[str] = frozenset({
    "new",
    "disappeared",
    "property_changed",
    "source_added",
    "source_removed",
    "edge_added",
    "edge_removed",
    "confidence_shifted",
})

#: Cap on a single property-key length carried into a ``Diff``. Hostile
#: data can dump megabytes into a single key; we truncate to keep
#: memory and the JSON output bounded.
_KEY_MAX_CHARS: int = 200

#: Threshold above which a ``|confidence_after - confidence_before|``
#: emits a ``confidence_shifted`` change.
_CONFIDENCE_SHIFT_THRESHOLD: float = 0.20


# --------------------------------------------------------------------------- dataclasses
@dataclass(frozen=True)
class Edge:
    """Outgoing edge: typed destination + relation name."""

    dst: str
    rel: str


@dataclass(frozen=True)
class SnapshotEntity:
    """One entity as captured at snapshot time.

    Mirrors the fields the fusion store already persists
    (``first_seen``/``last_seen``/``confidence``/``sources``), so a
    Snapshot can be built directly from a fused row.
    """

    id: str
    type: str
    value: str
    sources: list[str] = field(default_factory=list)
    properties: dict[str, str] = field(default_factory=dict)
    edges: list[Edge] = field(default_factory=list)
    first_seen: float = 0.0
    last_seen: float = 0.0
    confidence: float = 0.5

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("SnapshotEntity.id must be a non-empty string")
        if not self.type:
            raise ValueError("SnapshotEntity.type must be a non-empty string")
        if not self.value:
            raise ValueError("SnapshotEntity.value must be a non-empty string")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("SnapshotEntity.confidence must be in [0, 1]")


@dataclass(frozen=True)
class Snapshot:
    """An immutable view of an investigation at one point in time."""

    entities: list[SnapshotEntity] = field(default_factory=list)
    snapshot_at: float = 0.0


@dataclass(frozen=True)
class ChangeConfig:
    """Tuning for :func:`detect_changes`."""

    min_reliability: SourceReliability = SourceReliability.C
    min_change_score: float = 0.10
    disappear_grace_days: float = 7.0
    include_disappeared: bool = True
    include_property_changes: bool = True
    include_source_added: bool = True
    max_changes: int = 500

    def __post_init__(self) -> None:
        if not 0.0 <= self.min_change_score <= 1.0:
            raise ValueError("min_change_score must be in [0, 1]")
        if self.max_changes < 1:
            raise ValueError("max_changes must be >= 1")
        if self.disappear_grace_days < 0.0:
            raise ValueError("disappear_grace_days must be >= 0")


@dataclass(frozen=True)
class Diff:
    """Structured description of a single change's delta."""

    added: list[str] = field(default_factory=list)
    changed: dict[str, list[str]] = field(default_factory=dict)
    removed: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Change:
    """One detected change."""

    id: str
    kind: str
    entity_id: str
    entity_type: str
    entity_value: str
    before: dict[str, Any] | None
    after: dict[str, Any] | None
    diff: Diff
    score: float
    sources: list[str]
    detected_at: float


@dataclass(frozen=True)
class ChangeSummary:
    """Aggregate stats for a :class:`ChangeReport`."""

    total: int
    by_kind: dict[str, int]
    entities_compared: int
    entities_added: int
    entities_removed: int
    properties_changed: int
    score_max: float
    score_mean: float
    computed_at: float
    snapshot_before_at: float
    snapshot_after_at: float


@dataclass(frozen=True)
class ChangeReport:
    """Top-N changes + summary stats for a single diff operation."""

    changes: list[Change]
    summary: ChangeSummary


# --------------------------------------------------------------------------- helpers
def _truncate_key(key: Any) -> str:
    s = str(key)
    if len(s) > _KEY_MAX_CHARS:
        return s[: _KEY_MAX_CHARS - 1] + "…"
    return s


def _change_id(kind: str, entity_id: str, diff_signature: str) -> str:
    payload = "|".join([kind, entity_id, diff_signature])
    return hashlib.sha1(payload.encode("utf-8"), usedforsecurity=False).hexdigest()[:16]


def _reliability_weight(name: str) -> float:
    """Reliability weight via 2a, with 0 fallback for the impossible
    case where the enum value is not a letter A-F."""
    rel = reliability_from_name(name)
    if rel == SourceReliability.A:
        return 1.00
    if rel == SourceReliability.B:
        return 0.85
    if rel == SourceReliability.C:
        return 0.70
    if rel == SourceReliability.D:
        return 0.50
    if rel == SourceReliability.E:
        return 0.30
    return 0.10  # F or fallback


def _reliability_floor(letter: SourceReliability) -> int:
    """A=1, B=2, ..., F=6. For 'min_reliability' comparison."""
    return ord(letter.value) - ord("A") + 1


def _filter_sources_by_reliability(
    sources: Iterable[str],
    min_reliability: SourceReliability,
) -> list[str]:
    floor = _reliability_floor(min_reliability)
    out: list[str] = []
    for s in sources:
        rel = reliability_from_name(s)
        if _reliability_floor(rel) <= floor:
            out.append(s)
    return out


def _property_diff(
    before: Mapping[str, str],
    after: Mapping[str, str],
) -> Diff:
    """Compute the per-key add/change/remove between two property maps."""
    before_keys = set(before.keys())
    after_keys = set(after.keys())
    added = [_truncate_key(k) for k in sorted(after_keys - before_keys)]
    removed = [_truncate_key(k) for k in sorted(before_keys - after_keys)]
    changed: dict[str, list[str]] = {}
    for k in sorted(before_keys & after_keys):
        if before[k] != after[k]:
            changed[_truncate_key(k)] = [
                str(before[k])[:_KEY_MAX_CHARS],
                str(after[k])[:_KEY_MAX_CHARS],
            ]
    return Diff(added=added, changed=changed, removed=removed)


def _edge_set(edges: Sequence[Edge]) -> set[tuple[str, str]]:
    return {(e.dst, e.rel) for e in edges}


def _union_sources(a: SnapshotEntity, b: SnapshotEntity) -> list[str]:
    """Sorted union of two entities' source lists.

    Used in every per-entity Change (property_changed, source_added,
    source_removed, edge_added, edge_removed, confidence_shifted) as
    the ``sources`` field of the audit trail — the analyst should be
    able to see every source that touched the entity, not just the
    trigger of the change.
    """
    return sorted(set(a.sources) | set(b.sources))


def _make_change(
    kind: str,
    entity_id: str,
    entity_type: str,
    entity_value: str,
    sig: str,
    *,
    before: dict[str, Any] | None,
    after: dict[str, Any] | None,
    diff: Diff,
    score: float,
    sources: list[str],
    detected_at: float,
) -> Change:
    """Build a :class:`Change` with the deterministic id derived from
    ``kind + entity_id + sig``. Centralised so the eight change kinds
    can never disagree on the field set or the id format.
    """
    return Change(
        id=_change_id(kind, entity_id, sig),
        kind=kind,
        entity_id=entity_id,
        entity_type=entity_type,
        entity_value=entity_value,
        before=before,
        after=after,
        diff=diff,
        score=score,
        sources=sources,
        detected_at=detected_at,
    )


def _below_min_reliability(
    source: str,
    min_reliability: SourceReliability,
) -> bool:
    """True if a source's reliability is strictly *worse* than the
    configured minimum (i.e. it should be filtered out)."""
    return _reliability_floor(reliability_from_name(source)) > _reliability_floor(min_reliability)


# --------------------------------------------------------------------------- public
def detect_changes(
    snapshot_before: Snapshot | None,
    snapshot_after: Snapshot | None,
    *,
    config: ChangeConfig | None = None,
) -> ChangeReport:
    """Diff two snapshots. Pure: no I/O, deterministic, bounded.

    Parameters
    ----------
    snapshot_before, snapshot_after
        The two snapshots to diff. Either may be ``None``:
        ``before=None`` ⇒ first run, every entity is ``new``;
        ``after=None`` ⇒ no future data, empty report.
    config
        Optional tuning. See :class:`ChangeConfig`.
    """
    if config is None:
        config = ChangeConfig()
    if snapshot_after is None:
        empty = ChangeSummary(
            total=0, by_kind={}, entities_compared=0,
            entities_added=0, entities_removed=0, properties_changed=0,
            score_max=0.0, score_mean=0.0,
            computed_at=0.0,
            snapshot_before_at=snapshot_before.snapshot_at if snapshot_before else 0.0,
            snapshot_after_at=0.0,
        )
        return ChangeReport(changes=[], summary=empty)

    before_at = snapshot_before.snapshot_at if snapshot_before else 0.0
    after_at = snapshot_after.snapshot_at

    before_index: dict[str, SnapshotEntity] = {}
    if snapshot_before is not None:
        for e in snapshot_before.entities:
            before_index[e.id] = e

    after_index: dict[str, SnapshotEntity] = {}
    for e in snapshot_after.entities:
        after_index[e.id] = e

    changes: list[Change] = []

    # 1) New entities + property_changed + source_added + source_removed
    #    + edge_added + edge_removed + confidence_shifted
    for eid, ent_after in after_index.items():
        if eid not in before_index:
            # new entity
            filtered = _filter_sources_by_reliability(ent_after.sources, config.min_reliability)
            score = max((_reliability_weight(s) for s in filtered), default=0.0)
            if score < config.min_change_score:
                continue
            changes.append(_make_change(
                "new", eid, ent_after.type, ent_after.value,
                f"sources={','.join(sorted(filtered))}",
                before=None,
                after={"sources": list(ent_after.sources),
                       "properties": dict(ent_after.properties),
                       "confidence": ent_after.confidence},
                diff=Diff(added=sorted(ent_after.properties.keys())),
                score=score,
                sources=sorted(filtered),
                detected_at=after_at,
            ))
            continue
        ent_before = before_index[eid]
        # property_changed
        if config.include_property_changes:
            d = _property_diff(ent_before.properties, ent_after.properties)
            if d.added or d.changed or d.removed:
                # Score: 0.5 + 0.5 * corroboration (capped at 1.0)
                all_sources = _union_sources(ent_before, ent_after)
                cor = min(1.0, len(_filter_sources_by_reliability(all_sources, config.min_reliability)) / 5.0)
                score = min(1.0, 0.5 + 0.5 * cor)
                if score >= config.min_change_score:
                    sig_parts = [
                        f"+{','.join(d.added)}",
                        f"~{','.join(d.changed.keys())}",
                        f"-{','.join(d.removed)}",
                    ]
                    changes.append(_make_change(
                        "property_changed", eid, ent_after.type, ent_after.value,
                        "|".join(sig_parts),
                        before={"properties": dict(ent_before.properties)},
                        after={"properties": dict(ent_after.properties)},
                        diff=d,
                        score=score,
                        sources=all_sources,
                        detected_at=after_at,
                    ))
        # source_added
        if config.include_source_added:
            before_set = set(ent_before.sources)
            after_set = set(ent_after.sources)
            new_sources = sorted(after_set - before_set)
            for src in new_sources:
                if _below_min_reliability(src, config.min_reliability):
                    continue
                score = _reliability_weight(src)
                if score < config.min_change_score:
                    continue
                changes.append(_make_change(
                    "source_added", eid, ent_after.type, ent_after.value,
                    src,
                    before={"sources": sorted(before_set)},
                    after={"sources": [src]},
                    diff=Diff(added=[src]),
                    score=score,
                    sources=[src],
                    detected_at=after_at,
                ))
        # source_removed (rare signal)
        removed_sources = sorted(set(ent_before.sources) - set(ent_after.sources))
        for src in removed_sources:
            score = 0.3
            if score < config.min_change_score:
                continue
            changes.append(_make_change(
                "source_removed", eid, ent_after.type, ent_after.value,
                src,
                before={"sources": [src]},
                after={"sources": sorted(set(ent_after.sources))},
                diff=Diff(removed=[src]),
                score=score,
                sources=[src],
                detected_at=after_at,
            ))
        # edge_added / edge_removed
        edges_before = _edge_set(ent_before.edges)
        edges_after = _edge_set(ent_after.edges)
        added_edges = edges_after - edges_before
        removed_edges = edges_before - edges_after
        if added_edges:
            changes.append(_make_change(
                "edge_added", eid, ent_after.type, ent_after.value,
                ",".join(sorted(f"{d}/{r}" for d, r in added_edges)),
                before={"edges": sorted(f"{d}/{r}" for d, r in edges_before)},
                after={"edges": sorted(f"{d}/{r}" for d, r in added_edges)},
                diff=Diff(added=sorted(f"{d}/{r}" for d, r in added_edges)),
                score=0.5,
                sources=_union_sources(ent_before, ent_after),
                detected_at=after_at,
            ))
        if removed_edges:
            changes.append(_make_change(
                "edge_removed", eid, ent_after.type, ent_after.value,
                ",".join(sorted(f"{d}/{r}" for d, r in removed_edges)),
                before={"edges": sorted(f"{d}/{r}" for d, r in removed_edges)},
                after={"edges": sorted(f"{d}/{r}" for d, r in edges_after)},
                diff=Diff(removed=sorted(f"{d}/{r}" for d, r in removed_edges)),
                score=0.5,
                sources=_union_sources(ent_before, ent_after),
                detected_at=after_at,
            ))
        # confidence_shifted
        delta = abs(ent_after.confidence - ent_before.confidence)
        if delta > _CONFIDENCE_SHIFT_THRESHOLD:
            changes.append(_make_change(
                "confidence_shifted", eid, ent_after.type, ent_after.value,
                f"{ent_before.confidence:.4f}->{ent_after.confidence:.4f}",
                before={"confidence": ent_before.confidence},
                after={"confidence": ent_after.confidence},
                diff=Diff(changed={"confidence": [
                    f"{ent_before.confidence:.4f}",
                    f"{ent_after.confidence:.4f}",
                ]}),
                score=delta,
                sources=_union_sources(ent_before, ent_after),
                detected_at=after_at,
            ))

    # 2) Disappeared entities (with grace)
    if config.include_disappeared and snapshot_before is not None:
        grace_seconds = config.disappear_grace_days * 86400.0
        for eid, ent_before in before_index.items():
            if eid in after_index:
                continue
            # Was the entity recent? If yes, treat as transient miss.
            if after_at - ent_before.last_seen < grace_seconds:
                continue
            # Score: 1 - confidence_before (rarer si era fiable)
            score = 1.0 - ent_before.confidence
            if score < config.min_change_score:
                continue
            changes.append(_make_change(
                "disappeared", eid, ent_before.type, ent_before.value,
                f"last_seen={ent_before.last_seen}",
                before={"sources": list(ent_before.sources), "last_seen": ent_before.last_seen},
                after=None,
                diff=Diff(removed=sorted(ent_before.properties.keys())),
                score=score,
                sources=sorted(ent_before.sources),
                detected_at=after_at,
            ))

    # 3) Sort and cap
    changes.sort(key=lambda c: (-c.score, c.id))
    if len(changes) > config.max_changes:
        changes = changes[: config.max_changes]

    # 4) Summary
    by_kind: dict[str, int] = {}
    for c in changes:
        by_kind[c.kind] = by_kind.get(c.kind, 0) + 1
    if changes:
        score_max = max(c.score for c in changes)
        score_mean = sum(c.score for c in changes) / len(changes)
    else:
        score_max = 0.0
        score_mean = 0.0
    summary = ChangeSummary(
        total=len(changes),
        by_kind=by_kind,
        entities_compared=len(before_index),
        entities_added=by_kind.get("new", 0),
        entities_removed=by_kind.get("disappeared", 0),
        properties_changed=by_kind.get("property_changed", 0),
        score_max=score_max,
        score_mean=score_mean,
        computed_at=after_at,
        snapshot_before_at=before_at,
        snapshot_after_at=after_at,
    )
    return ChangeReport(changes=changes, summary=summary)


__all__ = [
    "CHANGE_KINDS",
    "Change",
    "ChangeConfig",
    "ChangeReport",
    "ChangeSummary",
    "Diff",
    "Edge",
    "Snapshot",
    "SnapshotEntity",
    "detect_changes",
]
