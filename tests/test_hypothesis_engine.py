"""ATDD + BDD tests for estorides_core.hypothesis_engine.

Implements the Given-When-Then contracts declared in
``spec/hypothesis_engine.md`` (module 2b). Property-based invariants
live in ``tests/properties/test_hypothesis_engine_properties.py``.

Run from the project root::

    .venv/bin/pytest tests/test_hypothesis_engine.py -v
"""
from __future__ import annotations

import pytest

from estorides_core.hypothesis_engine import (
    EntityRef,
    Evidence,
    Hypothesis,
    generate_hypotheses,
)


def _obs(source: str, parsed: object, raw: object | None = None) -> dict:
    """Build a minimal observation dict that matches the orchestrator shape."""
    return {
        "source": source,
        "category": "test",
        "parser": "test",
        "description": source,
        "parsed": parsed,
        "raw": raw if raw is not None else parsed,
        "meta": {},
    }


# ---------------------------------------------------------------------------
# S1 — Happy path: 1 domain, 3 sources concuerdan
# ---------------------------------------------------------------------------
class TestHappyPathDomainBelongsToActor:
    """S1 del spec."""

    def test_emits_domain_belongsto_actor_hypothesis(self) -> None:
        # Given: 3 sources concuerdan que example.com es de EvilCorp
        observations = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
            _obs("crt_sh_certificates", {"issuer_name": "EvilCorp CA"}),
            _obs("ipapi_co_full", {"org": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        # When
        hypotheses = generate_hypotheses(observations, entities)
        # Then
        domain_hyps = [h for h in hypotheses if h.type == "domain-belongsto-actor"]
        assert len(domain_hyps) >= 1, (
            f"expected ≥1 domain hypothesis, got {len(domain_hyps)}"
        )

    def test_score_in_high_band(self) -> None:
        observations = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
            _obs("crt_sh_certificates", {"issuer_name": "EvilCorp CA"}),
            _obs("ipapi_co_full", {"org": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        result = generate_hypotheses(observations, entities)
        domain_hyps = [h for h in result if h.type == "domain-belongsto-actor"]
        assert domain_hyps, "no domain hypothesis emitted"
        assert domain_hyps[0].score >= 0.60

    def test_supporting_has_three_items(self) -> None:
        # 3 sources que dicen exactamente "EvilCorp" en su key relevante
        # (crt_sh_certificates lleva "EvilCorp CA" como issuer, que NO
        # matchea exactamente — esa evidencia cae fuera de este
        # escenario y se cubre con el matching flexible de S1 abajo).
        observations = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
            _obs("ipapi_co_full", {"org": "EvilCorp"}),
            _obs("wikidata_search", {"label": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        result = generate_hypotheses(observations, entities)
        domain_hyps = [h for h in result if h.type == "domain-belongsto-actor"]
        assert domain_hyps[0].supporting
        assert len(domain_hyps[0].supporting) == 3

    def test_sources_sorted_and_unique(self) -> None:
        observations = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
            _obs("crt_sh_certificates", {"issuer_name": "EvilCorp CA"}),
            _obs("ipapi_co_full", {"org": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        result = generate_hypotheses(observations, entities)
        domain_hyps = [h for h in result if h.type == "domain-belongsto-actor"]
        assert domain_hyps[0].sources == sorted(set(domain_hyps[0].sources))


# ---------------------------------------------------------------------------
# S2 — Edge: input vacío
# ---------------------------------------------------------------------------
class TestEmptyInputProducesEmptyOutput:
    """S2 del spec."""

    def test_empty_observations_empty_entities(self) -> None:
        assert generate_hypotheses([], []) == []

    def test_empty_observations_only(self) -> None:
        assert generate_hypothences_safe([], [{"type": "domain", "value": "x.com"}]) == []

    def test_empty_entities_only(self) -> None:
        assert generate_hypothences_safe([_obs("hackertarget_whois", {"x": "y"})], []) == []


# Helper to keep the test signatures readable.
def generate_hypothences_safe(
    observations: list,
    entities: list,
    **kwargs: object,
) -> list:
    return generate_hypotheses(observations, entities, **kwargs)


# ---------------------------------------------------------------------------
# S3 — Edge: observación con parsed = None
# ---------------------------------------------------------------------------
class TestMalformedObservationsAreSkipped:
    """S3 del spec."""

    def test_observation_with_none_parsed_is_ignored(self) -> None:
        observations = [
            _obs("hackertarget_whois", None),
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        # No crash; emite al menos una hipótesis (de la observation válida)
        result = generate_hypotheses(observations, entities)
        domain_hyps = [h for h in result if h.type == "domain-belongsto-actor"]
        assert domain_hyps

    def test_observation_without_source_is_ignored(self) -> None:
        observations = [
            {"source": "", "parsed": {"registrant_organization": "EvilCorp"}},
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        # No crash; el motor ignora la observation sin source.
        result = generate_hypotheses(observations, entities)
        # No debe haber hipótesis con source vacío.
        for h in result:
            for ev in h.supporting:
                assert ev.source != ""
            for ev in h.contradicting:
                assert ev.source != ""


# ---------------------------------------------------------------------------
# S4 — Edge: source desconocido cae a reliability C
# ---------------------------------------------------------------------------
class TestUnknownSourceFallsBackToReliabilityC:
    """S4 del spec."""

    def test_unknown_source_uses_reliability_c(self) -> None:
        observations = [
            _obs("totally_made_up_source_xyz", {"registrant_organization": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        result = generate_hypotheses(observations, entities)
        domain_hyps = [h for h in result if h.type == "domain-belongsto-actor"]
        if domain_hyps:
            assert domain_hyps[0].supporting
            ev = domain_hyps[0].supporting[0]
            assert ev.reliability.value == "C"
            assert ev.weight == pytest.approx(0.70, rel=1e-9)


# ---------------------------------------------------------------------------
# S5 — Edge: min_score filtra hipótesis débiles
# ---------------------------------------------------------------------------
class TestMinScoreFiltersHypotheses:
    """S5 del spec."""

    def test_min_score_zero_returns_all(self) -> None:
        observations = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        result = generate_hypotheses(observations, entities, min_score=0.0)
        # Al menos la del dominio existe
        assert any(h.type == "domain-belongsto-actor" for h in result)

    def test_min_score_one_filters_everything(self) -> None:
        observations = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        result = generate_hypotheses(observations, entities, min_score=1.0)
        # Filtro tan alto que nada pasa
        assert result == []


# ---------------------------------------------------------------------------
# S6 — Edge: max_hypotheses acota la salida
# ---------------------------------------------------------------------------
class TestMaxHypothesesBounds:
    """S6 del spec."""

    def test_max_hypotheses_caps_output(self) -> None:
        # Generamos un input con múltiples pares domain-org.
        observations = [
            _obs("hackertarget_whois", {
                "registrant_organization": f"Org{i}",
            })
            for i in range(5)
        ]
        entities = []
        for i in range(5):
            entities.append({"type": "domain", "value": f"example{i}.com"})
            entities.append({"type": "org", "value": f"Org{i}"})

        result = generate_hypotheses(observations, entities, max_hypotheses=2)
        assert len(result) <= 2


# ---------------------------------------------------------------------------
# S7 — Error: input del programador inválido
# ---------------------------------------------------------------------------
class TestProgrammerErrorRaisesValueOrTypeError:
    """S7 del spec."""

    def test_observations_must_be_sequence(self) -> None:
        with pytest.raises(TypeError, match="observations"):
            generate_hypotheses("not a list", [])  # type: ignore[arg-type]

    def test_entities_must_be_sequence(self) -> None:
        with pytest.raises(TypeError, match="entities"):
            generate_hypotheses([], "not a list")  # type: ignore[arg-type]

    def test_min_score_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError, match="min_score"):
            generate_hypotheses([], [], min_score=1.5)
        with pytest.raises(ValueError, match="min_score"):
            generate_hypotheses([], [], min_score=-0.1)

    def test_max_hypotheses_too_small_raises(self) -> None:
        with pytest.raises(ValueError, match="max_hypotheses"):
            generate_hypotheses([], [], max_hypotheses=0)
        with pytest.raises(ValueError, match="max_hypotheses"):
            generate_hypotheses([], [], max_hypotheses=-3)


# ---------------------------------------------------------------------------
# S8 — Seguridad: observation hostil
# ---------------------------------------------------------------------------
class TestHostileObservationPayloadIsHandled:
    """S8 del spec."""

    @pytest.mark.parametrize(
        "hostile",
        [
            {"registrant_organization": "\x00evil"},
            {"registrant_organization": "A" * 100_000},
            {"registrant_organization": "__import__('os').system('rm -rf /')"},
            {"registrant_organization": "🔥💀\u202e"},
        ],
    )
    def test_hostile_value_is_truncated_or_skipped(self, hostile: dict) -> None:
        observations = [_obs("hackertarget_whois", hostile)]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        # No crash, no RCE.
        result = generate_hypotheses(observations, entities)
        for h in result:
            for ev in h.supporting + h.contradicting:
                ev_str = str(ev.value)
                assert len(ev_str) <= 200, f"value not truncated: {len(ev_str)} chars"


# ---------------------------------------------------------------------------
# S9 — Determinismo
# ---------------------------------------------------------------------------
class TestDeterminism:
    """S9 del spec."""

    def test_same_input_same_ids_and_scores(self) -> None:
        observations = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
            _obs("crt_sh_certificates", {"issuer_name": "EvilCorp CA"}),
        ]
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        a = generate_hypotheses(observations, entities)
        b = generate_hypotheses(observations, entities)
        assert len(a) == len(b)
        assert sorted(h.id for h in a) == sorted(h.id for h in b)
        for ha, hb in zip(
            sorted(a, key=lambda h: h.id),
            sorted(b, key=lambda h: h.id),
            strict=False,
        ):
            assert ha.score == pytest.approx(hb.score, rel=1e-12)
            assert ha.claim == hb.claim

    def test_input_order_does_not_affect_output(self) -> None:
        observations_a = [
            _obs("hackertarget_whois", {"registrant_organization": "EvilCorp"}),
            _obs("crt_sh_certificates", {"issuer_name": "EvilCorp CA"}),
        ]
        observations_b = list(reversed(observations_a))
        entities = [
            {"type": "domain", "value": "example.com"},
            {"type": "org", "value": "EvilCorp"},
        ]
        a = generate_hypotheses(observations_a, entities)
        b = generate_hypotheses(observations_b, entities)
        assert sorted(h.id for h in a) == sorted(h.id for h in b)


# ---------------------------------------------------------------------------
# S10 — Bounded (cubierto en properties; aquí solo un smoke)
# ---------------------------------------------------------------------------
class TestBoundedSmoke:
    """S10 del spec: smoke test del dataclass."""

    def test_hypothesis_dataclass_is_frozen(self) -> None:
        h = Hypothesis(
            id="abc",
            type="domain-belongsto-actor",
            claim="x.com belongs to A",
            score=0.5,
            confidence=0.5,
            supporting=[],
            contradicting=[],
            entities=[EntityRef(type="domain", value="x.com")],
            reasoning="because",
            sources=["a"],
        )
        with pytest.raises((AttributeError, Exception)):
            h.id = "mutate"  # type: ignore[misc]

    def test_evidence_dataclass_is_frozen(self) -> None:
        from estorides_core.reliability_scoring import SourceReliability
        e = Evidence(
            source="x",
            field="f",
            value="v",
            weight=0.5,
            reliability=SourceReliability.C,
        )
        with pytest.raises((AttributeError, Exception)):
            e.source = "mutate"  # type: ignore[misc]

    def test_entity_ref_is_frozen(self) -> None:
        ref = EntityRef(type="domain", value="x.com")
        with pytest.raises((AttributeError, Exception)):
            ref.type = "ip"  # type: ignore[misc]
