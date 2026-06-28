"""Property-based invariants for estorides_core.change_detection.

Hypothesis fuzzing: random snapshots, must always satisfy the
boundedness invariants declared in spec S12.

Run from the project root::

    .venv/bin/pytest tests/properties/test_change_detection_properties.py -v
"""
from __future__ import annotations

import re

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from estorides_core.change_detection import (
    ChangeConfig,
    Snapshot,
    SnapshotEntity,
    detect_changes,
)

# Strategies
short_str = st.text(
    alphabet=st.characters(
        whitelist_categories=("Lu", "Ll", "Nd"),
        max_codepoint=0x7E,
    ),
    min_size=1, max_size=40,
)
source_st = st.sampled_from(
    ["crt_sh_certificates", "rdap_domain", "ipapi_free", "abuseipdb_check",
     "dns_google", "github_user", "psbdmp_ws", "wikidata_search"]
)
type_st = st.sampled_from(["domain", "ipv4", "org", "email", "person"])
entity_st = st.builds(
    SnapshotEntity,
    id=st.uuids().map(str),
    type=type_st,
    value=short_str,
    sources=st.lists(source_st, min_size=0, max_size=5),
    properties=st.dictionaries(
        keys=st.sampled_from(["asn", "country", "org", "registrant_organization"]),
        values=short_str,
        min_size=0, max_size=4,
    ),
    edges=st.lists(
        st.tuples(
            st.sampled_from(["ipv4", "domain", "asn"]),
            short_str,
        ).map(lambda t: (f"{t[0]}:{t[1]}", "related_to")),
        min_size=0, max_size=2,
    ).map(lambda items: [(d, r) for d, r in items]),
    first_seen=st.floats(min_value=0, max_value=1e10, allow_nan=False, allow_infinity=False),
    last_seen=st.floats(min_value=0, max_value=1e10, allow_nan=False, allow_infinity=False),
    confidence=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
)
snapshot_st = st.builds(
    Snapshot,
    entities=st.lists(entity_st, min_size=0, max_size=8),
    snapshot_at=st.floats(min_value=0, max_value=1e10, allow_nan=False, allow_infinity=False),
)


@settings(max_examples=1000, deadline=None, suppress_health_check=list(HealthCheck))
@given(before=snapshot_st, after=snapshot_st)
def test_scores_always_bounded(before: Snapshot, after: Snapshot) -> None:
    report = detect_changes(before, after)
    for c in report.changes:
        assert 0.0 <= c.score <= 1.0, c


@settings(max_examples=1000, deadline=None)
@given(before=snapshot_st, after=snapshot_st)
def test_max_changes_respected(before: Snapshot, after: Snapshot) -> None:
    for cap in (1, 5, 50):
        cfg = ChangeConfig(max_changes=cap)
        report = detect_changes(before, after, config=cfg)
        assert len(report.changes) <= cap, report


@settings(max_examples=1000, deadline=None)
@given(before=snapshot_st, after=snapshot_st)
def test_id_is_16_char_hex(before: Snapshot, after: Snapshot) -> None:
    hex16 = re.compile(r"^[0-9a-f]{16}$")
    report = detect_changes(before, after)
    for c in report.changes:
        assert hex16.match(c.id), f"id {c.id!r} is not 16-char hex"


@settings(max_examples=1000, deadline=None)
@given(before=snapshot_st, after=snapshot_st)
def test_idempotent(before: Snapshot, after: Snapshot) -> None:
    a = detect_changes(before, after)
    b = detect_changes(before, after)
    assert [c.id for c in a.changes] == [c.id for c in b.changes]
    for ca, cb in zip(a.changes, b.changes, strict=False):
        assert ca.score == pytest.approx(cb.score, rel=1e-12)


@settings(max_examples=1000, deadline=None)
@given(after=snapshot_st)
def test_first_run_reports_all_as_new(after: Snapshot) -> None:
    report = detect_changes(None, after)
    for c in report.changes:
        assert c.kind == "new"


@settings(max_examples=1000, deadline=None)
@given(before=snapshot_st)
def test_after_none_returns_empty(before: Snapshot) -> None:
    report = detect_changes(before, None)
    assert report.changes == []
    assert report.summary.total == 0


@settings(max_examples=1000, deadline=None)
@given(entities=st.lists(entity_st, min_size=1, max_size=20))
def test_before_vs_no_after_empty(entities: list[SnapshotEntity]) -> None:
    before = Snapshot(entities=entities, snapshot_at=0.0)
    report = detect_changes(before, None)
    assert report.changes == []


@settings(max_examples=1000, deadline=None)
@given(
    before=st.lists(entity_st, min_size=0, max_size=10),
    after=st.lists(entity_st, min_size=0, max_size=10),
)
def test_summary_consistency(
    before: list[SnapshotEntity], after: list[SnapshotEntity]
) -> None:
    """Whatever the input, the summary fields must agree with the
    ``changes`` list: ``total == len(changes)``, ``by_kind`` counts
    each kind exactly, ``score_max/mean`` are derived from the actual
    changes, and ``entities_compared == len(before.entities)`` (or 0 if
    ``before`` is None)."""
    before_snap = Snapshot(entities=before, snapshot_at=1000.0)
    after_snap = Snapshot(entities=after, snapshot_at=2000.0)
    report = detect_changes(before_snap, after_snap)

    assert report.summary.total == len(report.changes)
    counted: dict[str, int] = {}
    for c in report.changes:
        counted[c.kind] = counted.get(c.kind, 0) + 1
    assert report.summary.by_kind == counted
    assert report.summary.entities_added == counted.get("new", 0)
    assert report.summary.entities_removed == counted.get("disappeared", 0)
    assert report.summary.properties_changed == counted.get("property_changed", 0)
    assert report.summary.entities_compared == len(before)
    if report.changes:
        assert report.summary.score_max == max(c.score for c in report.changes)
        assert report.summary.score_mean == pytest.approx(
            sum(c.score for c in report.changes) / len(report.changes)
        )
    else:
        assert report.summary.score_max == 0.0
        assert report.summary.score_mean == 0.0
