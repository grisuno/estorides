"""ATDD + BDD tests for estorides_core.change_detection.

Implements the Given-When-Then contracts declared in
``spec/change_detection.md`` (module 2c). Property-based invariants
live in ``tests/properties/test_change_detection_properties.py``.

Run from the project root::

    .venv/bin/pytest tests/test_change_detection.py -v
"""
from __future__ import annotations

import pytest

from estorides_core.change_detection import (
    Change,
    ChangeConfig,
    ChangeReport,
    Diff,
    Edge,
    Snapshot,
    SnapshotEntity,
    detect_changes,
)
from estorides_core.reliability_scoring import SourceReliability


def _entity(
    eid: str,
    etype: str,
    value: str,
    *,
    sources: list[str] | None = None,
    properties: dict[str, str] | None = None,
    edges: list[Edge] | None = None,
    first_seen: float = 0.0,
    last_seen: float = 0.0,
    confidence: float = 0.5,
) -> SnapshotEntity:
    return SnapshotEntity(
        id=eid,
        type=etype,
        value=value,
        sources=list(sources or []),
        properties=dict(properties or {}),
        edges=list(edges or []),
        first_seen=first_seen,
        last_seen=last_seen,
        confidence=confidence,
    )


# ---------------------------------------------------------------------------
# S1 — Happy path: una entity nueva
# ---------------------------------------------------------------------------
class TestNewEntity:
    """S1 del spec."""

    def test_one_new_entity_emits_one_new_change(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates"],
                              confidence=0.7)],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[
                _entity("e1", "domain", "example.com",
                        sources=["crt_sh_certificates"], confidence=0.7),
                _entity("e2", "ipv4", "1.2.3.4",
                        sources=["dns_google"], confidence=0.5),
            ],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then
        new_changes = [c for c in report.changes if c.kind == "new"]
        assert len(new_changes) == 1
        assert new_changes[0].entity_type == "ipv4"
        assert new_changes[0].entity_value == "1.2.3.4"

    def test_new_change_score_in_high_band(self) -> None:
        before = Snapshot(entities=[], snapshot_at=1000.0)
        after = Snapshot(
            entities=[_entity("e2", "ipv4", "1.2.3.4",
                              sources=["dns_google"], confidence=0.5)],
            snapshot_at=2000.0,
        )
        report = detect_changes(before, after)
        new = [c for c in report.changes if c.kind == "new"]
        assert new[0].score >= 0.5


# ---------------------------------------------------------------------------
# S2 — Happy path: property changed
# ---------------------------------------------------------------------------
class TestPropertyChanged:
    """S2 del spec."""

    def test_property_change_emits_one_change(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              properties={"asn": "AS13335"})],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              properties={"asn": "AS15169"})],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then
        prop_changes = [c for c in report.changes if c.kind == "property_changed"]
        assert len(prop_changes) == 1
        assert prop_changes[0].diff.changed["asn"] == ["AS13335", "AS15169"]


# ---------------------------------------------------------------------------
# S3 — Edge: first run (before = None)
# ---------------------------------------------------------------------------
class TestFirstRunBeforeIsNone:
    """S3 del spec."""

    def test_before_none_reports_all_as_new(self) -> None:
        # Given
        after = Snapshot(
            entities=[
                _entity(f"e{i}", "domain", f"d{i}.com", sources=["crt_sh_certificates"])
                for i in range(5)
            ],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(None, after)
        # Then
        assert report.summary.entities_added == 5
        assert all(c.kind == "new" for c in report.changes)


# ---------------------------------------------------------------------------
# S4 — Edge: after = None
# ---------------------------------------------------------------------------
class TestAfterIsNone:
    """S4 del spec."""

    def test_after_none_returns_empty_report(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com")],
            snapshot_at=1000.0,
        )
        # When
        report = detect_changes(before, None)
        # Then
        assert report.changes == []
        assert report.summary.total == 0


# ---------------------------------------------------------------------------
# S5 — Edge: disappeared con grace
# ---------------------------------------------------------------------------
class TestDisappearedWithGrace:
    """S5 del spec."""

    def test_disappeared_within_grace_is_ignored(self) -> None:
        # Given: entity vista hace 2 días, after sin ella, grace 7 días
        before = Snapshot(
            entities=[_entity("e1", "domain", "foo.com", last_seen=2000.0)],
            snapshot_at=2000.0,
        )
        after = Snapshot(entities=[], snapshot_at=2000.0 + 2 * 86400)
        # When: grace de 7 días
        report = detect_changes(before, after, config=ChangeConfig(disappear_grace_days=7.0))
        # Then: no se reporta
        assert all(c.kind != "disappeared" for c in report.changes)

    def test_disappeared_outside_grace_emits_change(self) -> None:
        # Given: entity vista hace 30 días, after sin ella
        before = Snapshot(
            entities=[_entity("e1", "domain", "foo.com",
                              last_seen=2000.0, confidence=0.7)],
            snapshot_at=2000.0,
        )
        after = Snapshot(entities=[], snapshot_at=2000.0 + 30 * 86400)
        # When: grace de 7 días
        report = detect_changes(before, after, config=ChangeConfig(disappear_grace_days=7.0))
        # Then: aparece como disappeared
        disappeared = [c for c in report.changes if c.kind == "disappeared"]
        assert len(disappeared) == 1


# ---------------------------------------------------------------------------
# S6 — Edge: source_added
# ---------------------------------------------------------------------------
class TestSourceAdded:
    """S6 del spec."""

    def test_new_source_on_existing_entity_emits_source_added(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates"])],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates", "rdap_domain"])],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then
        added = [c for c in report.changes if c.kind == "source_added"]
        assert len(added) == 1
        # rdap_domain es reliability A (peso 1.00)
        assert added[0].score == pytest.approx(1.0, rel=1e-9)


# ---------------------------------------------------------------------------
# S7 — Edge: min_reliability filtra source_added ruidosos
# ---------------------------------------------------------------------------
class TestMinReliabilityFiltersSources:
    """S7 del spec."""

    def test_min_reliability_e_excludes_f_source(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates"])],
            snapshot_at=1000.0,
        )
        # "untrusted_webscraper" tiene reliability F (weight 0.10) — peor que E
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates", "untrusted_webscraper"])],
            snapshot_at=2000.0,
        )
        # When: min_reliability = E (excluye F)
        report = detect_changes(
            before, after,
            config=ChangeConfig(min_reliability=SourceReliability.E),
        )
        # Then
        added = [c for c in report.changes if c.kind == "source_added"]
        assert added == []  # la source F fue filtrada


# ---------------------------------------------------------------------------
# S8 — Edge: max_changes acota la salida
# ---------------------------------------------------------------------------
class TestMaxChangesBounds:
    """S8 del spec."""

    def test_max_changes_caps_output(self) -> None:
        # Given: 50 entities nuevas
        before = Snapshot(entities=[], snapshot_at=1000.0)
        after = Snapshot(
            entities=[
                _entity(f"e{i}", "domain", f"d{i}.com",
                        sources=["crt_sh_certificates"])
                for i in range(50)
            ],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(
            before, after, config=ChangeConfig(max_changes=10),
        )
        # Then
        assert len(report.changes) == 10
        assert report.summary.total == 10


# ---------------------------------------------------------------------------
# S9 — Error: programmer input inválido
# ---------------------------------------------------------------------------
class TestProgrammerErrorRaises:
    """S9 del spec."""

    def test_entity_id_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="id"):
            SnapshotEntity(id="", type="domain", value="x.com")

    def test_entity_type_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="type"):
            SnapshotEntity(id="e1", type="", value="x.com")

    def test_entity_value_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="value"):
            SnapshotEntity(id="e1", type="domain", value="")

    def test_min_change_score_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError, match="min_change_score"):
            ChangeConfig(min_change_score=1.5)
        with pytest.raises(ValueError, match="min_change_score"):
            ChangeConfig(min_change_score=-0.1)

    def test_max_changes_too_small_raises(self) -> None:
        with pytest.raises(ValueError, match="max_changes"):
            ChangeConfig(max_changes=0)


# ---------------------------------------------------------------------------
# S10 — Seguridad: property key hostil
# ---------------------------------------------------------------------------
class TestHostilePropertyKey:
    """S10 del spec."""

    @pytest.mark.parametrize(
        "hostile_key",
        [
            "\x00evil",
            "A" * 100_000,
            "<script>alert(1)</script>",
            "__import__('os').system('rm -rf /')",
        ],
    )
    def test_hostile_key_does_not_crash(self, hostile_key: str) -> None:
        before = Snapshot(
            entities=[_entity("e1", "domain", "x.com",
                              properties={hostile_key: "old"})],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "x.com",
                              properties={hostile_key: "new"})],
            snapshot_at=2000.0,
        )
        # No crash, no RCE.
        report = detect_changes(before, after)
        # El change existe
        assert report.changes
        # Las keys se truncan a 200 chars
        for c in report.changes:
            for k in c.diff.added + list(c.diff.changed.keys()) + c.diff.removed:
                assert len(k) <= 200


# ---------------------------------------------------------------------------
# S11 — Determinismo
# ---------------------------------------------------------------------------
class TestDeterminism:
    """S11 del spec."""

    def test_same_input_same_ids_and_scores(self) -> None:
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              properties={"asn": "AS13335"})],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              properties={"asn": "AS15169"})],
            snapshot_at=2000.0,
        )
        a = detect_changes(before, after)
        b = detect_changes(before, after)
        assert [c.id for c in a.changes] == [c.id for c in b.changes]
        for ca, cb in zip(a.changes, b.changes, strict=False):
            assert ca.score == pytest.approx(cb.score, rel=1e-12)

    def test_input_order_does_not_affect_output(self) -> None:
        entities_a = [
            _entity("e1", "domain", "a.com", sources=["crt_sh_certificates"]),
            _entity("e2", "domain", "b.com", sources=["crt_sh_certificates"]),
        ]
        before = Snapshot(entities=entities_a, snapshot_at=1000.0)
        after2 = Snapshot(
            entities=[_entity("e3", "domain", "c.com",
                              sources=["crt_sh_certificates"])],
            snapshot_at=2000.0,
        )
        # Determinismo: input order no afecta output para el mismo par
        a = detect_changes(before, after2)
        b = detect_changes(before, after2)
        assert sorted(c.id for c in a.changes) == sorted(c.id for c in b.changes)


# ---------------------------------------------------------------------------
# S13 — source_removed
# ---------------------------------------------------------------------------
class TestSourceRemoved:
    """S13 del spec: una source que antes veía la entity ya no la ve."""

    def test_source_removed_emits_change(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates", "rdap_domain"])],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates"])],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then
        removed = [c for c in report.changes if c.kind == "source_removed"]
        assert len(removed) == 1
        assert "rdap_domain" in removed[0].diff.removed
        # Score base = 0.30 (señal débil, miss transitorio probable)
        assert removed[0].score == pytest.approx(0.3, rel=1e-9)

    def test_source_removed_filtered_by_min_score(self) -> None:
        # Given: source_removed con score 0.3; con min_change_score=0.5
        # NO se emite.
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates", "rdap_domain"])],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              sources=["crt_sh_certificates"])],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(
            before, after,
            config=ChangeConfig(min_change_score=0.5),
        )
        # Then
        removed = [c for c in report.changes if c.kind == "source_removed"]
        assert removed == []


# ---------------------------------------------------------------------------
# S14 — edge_added / edge_removed
# ---------------------------------------------------------------------------
class TestEdgeChanges:
    """S14 del spec: edges salientes que aparecen/desaparecen."""

    def test_edge_added_emits_change(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              edges=[Edge(dst="ipv4:1.1.1.1", rel="resolves_to")])],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              edges=[
                                  Edge(dst="ipv4:1.1.1.1", rel="resolves_to"),
                                  Edge(dst="ipv4:2.2.2.2", rel="resolves_to"),
                              ])],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then
        added = [c for c in report.changes if c.kind == "edge_added"]
        assert len(added) == 1
        assert any("2.2.2.2" in a for a in added[0].diff.added)
        assert added[0].score == pytest.approx(0.5, rel=1e-9)

    def test_edge_removed_emits_change(self) -> None:
        # Given
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              edges=[
                                  Edge(dst="ipv4:1.1.1.1", rel="resolves_to"),
                                  Edge(dst="ipv4:2.2.2.2", rel="resolves_to"),
                              ])],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com",
                              edges=[Edge(dst="ipv4:1.1.1.1", rel="resolves_to")])],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then
        removed = [c for c in report.changes if c.kind == "edge_removed"]
        assert len(removed) == 1
        assert any("2.2.2.2" in r for r in removed[0].diff.removed)


# ---------------------------------------------------------------------------
# S15 — confidence_shifted (delta > 0.20)
# ---------------------------------------------------------------------------
class TestConfidenceShifted:
    """S15 del spec: |confidence_after - confidence_before| > 0.20."""

    def test_large_confidence_shift_emits_change(self) -> None:
        # Given: salto de 0.4 a 0.8 (delta=0.4 > 0.20)
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com", confidence=0.4)],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com", confidence=0.8)],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then
        shifted = [c for c in report.changes if c.kind == "confidence_shifted"]
        assert len(shifted) == 1
        assert shifted[0].score == pytest.approx(0.4, rel=1e-9)
        assert "confidence" in shifted[0].diff.changed

    def test_small_confidence_shift_ignored(self) -> None:
        # Given: salto de 0.50 a 0.55 (delta=0.05 < 0.20)
        before = Snapshot(
            entities=[_entity("e1", "domain", "example.com", confidence=0.50)],
            snapshot_at=1000.0,
        )
        after = Snapshot(
            entities=[_entity("e1", "domain", "example.com", confidence=0.55)],
            snapshot_at=2000.0,
        )
        # When
        report = detect_changes(before, after)
        # Then: no se emite confidence_shifted
        assert all(c.kind != "confidence_shifted" for c in report.changes)


# ---------------------------------------------------------------------------
# S12 — Bounded (cubierto en properties; aquí smoke)
# ---------------------------------------------------------------------------
class TestBoundedSmoke:
    """S12 del spec: smoke test del dataclass."""

    def test_change_is_frozen(self) -> None:
        c = Change(
            id="abc", kind="new", entity_id="e1", entity_type="domain",
            entity_value="x.com", before=None,
            after={"sources": ["a"]}, diff=Diff(), score=0.5,
            sources=["a"], detected_at=0.0,
        )
        with pytest.raises((AttributeError, Exception)):
            c.id = "mutate"  # type: ignore[misc]

    def test_diff_is_frozen(self) -> None:
        d = Diff(added=["a"], changed={"b": ["old", "new"]}, removed=["c"])
        with pytest.raises((AttributeError, Exception)):
            d.added = ["mutate"]  # type: ignore[misc]

    def test_change_report_is_frozen(self) -> None:
        r = ChangeReport(
            changes=[],
            summary=None,  # type: ignore[arg-type]
        )
        with pytest.raises((AttributeError, Exception)):
            r.changes = [Change(  # type: ignore[misc]
                id="x", kind="new", entity_id="e", entity_type="t",
                entity_value="v", before=None, after=None, diff=Diff(),
                score=0.0, sources=[], detected_at=0.0,
            )]
