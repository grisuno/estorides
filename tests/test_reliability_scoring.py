"""ATDD + BDD tests for estorides_core.reliability_scoring.

These tests implement the Given-When-Then contracts declared in
``spec/reliability_scoring.md`` (module 2a). They MUST fail against the
unwritten implementation (the red step of the cycle), and they MUST pass
after the green step. Property-based invariants live in
``tests/properties/test_reliability_scoring_properties.py``.

Run from the project root::

    .venv/bin/pytest tests/test_reliability_scoring.py -v
"""
from __future__ import annotations

import math
from itertools import pairwise

import pytest

# Importing the module under test — this import is expected to FAIL at
# the red step. The test file itself is the contract; the implementation
# is what makes the tests turn green.
from estorides_core.reliability_scoring import (
    CREDIBILITY_WEIGHT,
    DEFAULT_CREDIBILITY,
    DEFAULT_HALF_LIFE_DAYS,
    DEFAULT_RELIABILITY,
    RELIABILITY_WEIGHT,
    ConfidenceInput,
    Credibility,
    SourceReliability,
    compute_confidence,
    merge_confidence,
    reliability_from_name,
)


# ---------------------------------------------------------------------------
# S1 — Happy path: fuente A, corroborada, fresca
# ---------------------------------------------------------------------------
class TestHappyPathHighReliabilityCorroboratedFresh:
    """S1 del spec."""

    def test_score_in_high_band(self) -> None:
        # Given: A source, probably-true, 5 corroborators, fresh.
        # Formula: 1.0 * 1.0 * 0.85 * log10(6) * 1.0 * 1.0 ≈ 0.66
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            credibility=Credibility.PROBABLY_TRUE,
            corroboration_count=5,
            observation_age_seconds=0.0,
            base_confidence=1.0,
        )
        # When
        result = compute_confidence(inp)
        # Then: high band — well above mid but not necessarily 0.85+ (the
        # model is multiplicative; 0.85 would require cred=1 and cor≈10).
        assert 0.60 <= result.score <= 1.0, (
            f"expected score in [0.60, 1.0], got {result.score}"
        )

    def test_reliability_weight_is_one(self) -> None:
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            corroboration_count=5,
        )
        result = compute_confidence(inp)
        assert result.reliability_weight == 1.00

    def test_freshness_weight_is_one_when_age_zero(self) -> None:
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            corroboration_count=5,
            observation_age_seconds=0.0,
        )
        result = compute_confidence(inp)
        assert result.freshness_weight == 1.0

    def test_corroboration_weight_matches_log10(self) -> None:
        # log10(1 + 5) ≈ 0.778
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            corroboration_count=5,
        )
        result = compute_confidence(inp)
        assert result.corroboration_weight == pytest.approx(math.log10(6), rel=1e-9)

    def test_credibility_weight_for_probably_true(self) -> None:
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            credibility=Credibility.PROBABLY_TRUE,
            corroboration_count=5,
        )
        result = compute_confidence(inp)
        assert result.credibility_weight == 0.85


# ---------------------------------------------------------------------------
# S2 — Edge: fuente desconocida cae al default
# ---------------------------------------------------------------------------
class TestUnknownSourceFallsBackToDefault:
    """S2 del spec."""

    @pytest.mark.parametrize(
        "name",
        [
            "totally_unknown_xyz_123",
            "made_up_source_42",
            "some_random_feed",
        ],
    )
    def test_unknown_source_returns_default(self, name: str) -> None:
        # Given / When
        result = reliability_from_name(name)
        # Then
        assert result == DEFAULT_RELIABILITY == SourceReliability.C

    def test_unknown_source_produces_weak_score_with_one_corroboration(self) -> None:
        # Given: fuente C, 1 corroboración, fresh, credibility 6 (cannot be
        # judged, peso 0.5). Score = 0.7*0.5*log10(2)*1*1 ≈ 0.105.
        # "Moderate" en este modelo es débil porque 1 sola fuente no basta.
        reliability = reliability_from_name("totally_unknown_xyz_123")
        inp = ConfidenceInput(
            source_reliability=reliability,
            credibility=Credibility.CANNOT_BE_JUDGED,
            corroboration_count=1,
            observation_age_seconds=0.0,
            base_confidence=1.0,
        )
        # When
        result = compute_confidence(inp)
        # Then: no es cero (porque tiene 1 corroboración) ni 1.0 (porque
        # es C, no corroborado). Banda débil pero positiva.
        assert 0.05 <= result.score <= 0.20, (
            f"expected weak positive score for C/1/0d, got {result.score}"
        )

    def test_unknown_source_with_many_corroborators_reaches_high_band(self) -> None:
        # 50 fuentes independientes C, fresh, credibility 2 (probably true).
        # cor satura en 1.0 (log10(51) ≈ 1.71, clamp). El techo es reliability
        # * credibility = 0.7 * 0.85 = 0.595. El modelo dice: "muchas fuentes
        # C siguen siendo C, no llegan a 1.0".
        reliability = reliability_from_name("totally_unknown_xyz_123")
        inp = ConfidenceInput(
            source_reliability=reliability,
            credibility=Credibility.PROBABLY_TRUE,
            corroboration_count=50,
            observation_age_seconds=0.0,
            base_confidence=1.0,
        )
        result = compute_confidence(inp)
        assert 0.55 <= result.score <= 0.65, (
            f"50 corroboradores de C saturan en ~0.595, got {result.score}"
        )


# ---------------------------------------------------------------------------
# S3 — Edge: cero corroboración, fuente A, fresh — score queda en cero
# ---------------------------------------------------------------------------
class TestZeroCorroborationYieldsZeroScore:
    """S3 del spec: una sola fuente, no importa lo fiable que sea, score = 0."""

    def test_zero_corroboration_collapses_score(self) -> None:
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            credibility=Credibility.CONFIRMED,
            corroboration_count=0,
            observation_age_seconds=0.0,
            base_confidence=1.0,
        )
        result = compute_confidence(inp)
        assert result.score == 0.0
        assert result.corroboration_weight == 0.0


# ---------------------------------------------------------------------------
# S4 — Edge: observación muy vieja
# ---------------------------------------------------------------------------
class TestVeryOldObservationDecaysToZero:
    """S4 del spec."""

    def test_one_year_old_with_low_corroboration_decays(self) -> None:
        # 365 días, half-life 30 → exp(-ln(2)*12) ≈ 0.00018
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            credibility=Credibility.CONFIRMED,
            corroboration_count=1,
            observation_age_seconds=365 * 24 * 60 * 60,
            base_confidence=1.0,
        )
        result = compute_confidence(inp, half_life_days=30.0)
        assert result.freshness_weight < 0.001
        assert result.score < 0.01

    def test_freshness_is_monotonically_decreasing(self) -> None:
        """Una observación más vieja siempre tiene freshness menor o igual."""
        scores_freshness = []
        for age_days in (0, 1, 7, 30, 90, 365):
            inp = ConfidenceInput(
                source_reliability=SourceReliability.A,
                corroboration_count=2,
                observation_age_seconds=age_days * 86400.0,
            )
            result = compute_confidence(inp, half_life_days=30.0)
            scores_freshness.append(result.freshness_weight)
        # Estrictamente decreciente (no hay empates porque ln(2) > 0).
        for prev, curr in pairwise(scores_freshness):
            assert curr < prev, (
                f"freshness debe decrecer con age: {scores_freshness}"
            )


# ---------------------------------------------------------------------------
# S5 — Error: input inválido del programador
# ---------------------------------------------------------------------------
class TestInvalidInputRaisesValueError:
    """S5 del spec."""

    def test_negative_corroboration_count_raises(self) -> None:
        with pytest.raises(ValueError, match="corroboration_count must be >= 0"):
            ConfidenceInput(
                source_reliability=SourceReliability.A,
                corroboration_count=-1,
            )

    def test_negative_observation_age_raises(self) -> None:
        with pytest.raises(ValueError, match="observation_age_seconds must be >= 0"):
            ConfidenceInput(
                source_reliability=SourceReliability.A,
                observation_age_seconds=-1.0,
            )

    @pytest.mark.parametrize("bad", [-0.1, 1.1, 2.0, -1.0, 1.5])
    def test_base_confidence_out_of_range_raises(self, bad: float) -> None:
        with pytest.raises(ValueError, match="base_confidence must be in"):
            ConfidenceInput(
                source_reliability=SourceReliability.A,
                base_confidence=bad,
            )

    def test_half_life_zero_raises(self) -> None:
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            corroboration_count=2,
        )
        with pytest.raises(ValueError, match="half_life_days must be > 0"):
            compute_confidence(inp, half_life_days=0.0)

    def test_half_life_negative_raises(self) -> None:
        inp = ConfidenceInput(
            source_reliability=SourceReliability.A,
            corroboration_count=2,
        )
        with pytest.raises(ValueError, match="half_life_days must be > 0"):
            compute_confidence(inp, half_life_days=-5.0)


# ---------------------------------------------------------------------------
# S6 — Seguridad: nombre de fuente hostil
# ---------------------------------------------------------------------------
class TestHostileSourceNameIsHandledSafely:
    """S6 del spec: input del operador, posiblemente adversario, no rompe."""

    @pytest.mark.parametrize(
        "hostile",
        [
            "",                       # vacío
            "   ",                    # whitespace
            "\x00evil",               # NUL byte
            "\x07\x08\x1b[31m",       # control + ANSI
            "A" * 10_000,             # 10kB
            "__import__",             # dunder trick
            "' OR 1=1 --",            # SQL-ish
            "<script>alert(1)</script>",  # XSS-ish
            "../../../etc/passwd",    # path traversal
            "🔥💀\u202e",             # emoji + bidi override
        ],
    )
    def test_hostile_name_does_not_raise(self, hostile: str) -> None:
        # Given / When / Then: ninguna llamada lanza.
        result = reliability_from_name(hostile)
        # Y siempre devuelve un SourceReliability válido.
        assert isinstance(result, SourceReliability)
        assert result in SourceReliability


# ---------------------------------------------------------------------------
# S7 — Merge: una fuente A supera a una C
# ---------------------------------------------------------------------------
class TestMergeReliableBeatsLessReliable:
    """S7 del spec."""

    def test_new_a_source_raises_score(self) -> None:
        # existing = 0.18 viene de una fuente C, fresh, una sola
        # corroboración (1*0.7*0.85*log10(2)*1*1 ≈ 0.179).
        # El nuevo evento es A con cor=2 → new_score ≈ 0.41 > 0.18.
        result = merge_confidence(
            existing=0.18,
            new_observation=1.0,
            new_reliability=SourceReliability.A,
            new_credibility=Credibility.PROBABLY_TRUE,
            corroboration_count=2,
            observation_age_seconds=0.0,
        )
        assert result.score > 0.18
        assert result.score <= 1.0
        assert result.source_reliability == SourceReliability.A

    def test_merge_takes_max_of_existing_and_new(self) -> None:
        # El merge es max(existing, new_score), no suma ni promedio.
        # existing=0.7 (entidad ya vista con score 0.7).
        # Nueva observación: A + CONFIRMED + 10 corroboradores + fresh.
        # new_score = 1*1*1*log10(11)*1*1 = 1.04 → clamp a 1.0.
        # result = max(0.7, 1.0) = 1.0.
        result = merge_confidence(
            existing=0.7,
            new_observation=1.0,
            new_reliability=SourceReliability.A,
            new_credibility=Credibility.CONFIRMED,
            corroboration_count=10,
            observation_age_seconds=0.0,
        )
        assert result.score == pytest.approx(1.0, rel=1e-9)

    def test_merge_keeps_existing_when_new_is_weaker(self) -> None:
        # existing=0.7 (entidad fuerte). Nueva observación F → new_score ≈ 0.015
        # → result = max(0.7, 0.015) = 0.7. La débil no sube el score.
        result = merge_confidence(
            existing=0.7,
            new_observation=1.0,
            new_reliability=SourceReliability.F,
            new_credibility=Credibility.CANNOT_BE_JUDGED,
            corroboration_count=1,
            observation_age_seconds=0.0,
        )
        assert result.score == pytest.approx(0.7, rel=1e-9)

    def test_merge_result_is_always_bounded(self) -> None:
        result = merge_confidence(
            existing=0.99,
            new_observation=1.0,
            new_reliability=SourceReliability.A,
            new_credibility=Credibility.CONFIRMED,
            corroboration_count=10,
            observation_age_seconds=0.0,
        )
        assert 0.0 <= result.score <= 1.0


# ---------------------------------------------------------------------------
# S8 — Merge: una fuente F no puede subir el score
# ---------------------------------------------------------------------------
class TestMergeUnreliableCannotRaise:
    """S8 del spec."""

    def test_f_source_against_strong_existing_keeps_existing(self) -> None:
        result = merge_confidence(
            existing=0.9,
            new_observation=1.0,
            new_reliability=SourceReliability.F,
            new_credibility=Credibility.CANNOT_BE_JUDGED,
            corroboration_count=1,
            observation_age_seconds=0.0,
        )
        # La nueva observación, por sí sola, no debe superar el existing.
        # Fórmula con F (0.10) * 6 (0.50) * cor(1)=0.30 * fresh(1) = 0.015.
        # max(0.9, 0.015) = 0.9.
        assert result.score == pytest.approx(0.9, rel=1e-9)

    def test_merge_existing_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError, match="existing"):
            merge_confidence(
                existing=1.5,
                new_observation=1.0,
                new_reliability=SourceReliability.A,
                new_credibility=Credibility.CONFIRMED,
                corroboration_count=1,
                observation_age_seconds=0.0,
            )

    def test_merge_new_observation_out_of_range_raises(self) -> None:
        with pytest.raises(ValueError, match="new_observation"):
            merge_confidence(
                existing=0.18,
                new_observation=-0.1,
                new_reliability=SourceReliability.A,
                new_credibility=Credibility.CONFIRMED,
                corroboration_count=1,
                observation_age_seconds=0.0,
            )


# ---------------------------------------------------------------------------
# S9 — Determinismo
# ---------------------------------------------------------------------------
class TestDeterminism:
    """S9 del spec: misma entrada → misma salida, bit a bit."""

    def test_compute_confidence_is_pure(self) -> None:
        inp = ConfidenceInput(
            source_reliability=SourceReliability.B,
            credibility=Credibility.POSSIBLY_TRUE,
            corroboration_count=3,
            observation_age_seconds=12345.6,
            base_confidence=0.7,
        )
        a = compute_confidence(inp)
        b = compute_confidence(inp)
        assert a == b
        assert repr(a) == repr(b)

    def test_merge_confidence_is_pure(self) -> None:
        a = merge_confidence(
            existing=0.3,
            new_observation=0.8,
            new_reliability=SourceReliability.C,
            new_credibility=Credibility.POSSIBLY_TRUE,
            corroboration_count=2,
            observation_age_seconds=100.0,
        )
        b = merge_confidence(
            existing=0.3,
            new_observation=0.8,
            new_reliability=SourceReliability.C,
            new_credibility=Credibility.POSSIBLY_TRUE,
            corroboration_count=2,
            observation_age_seconds=100.0,
        )
        assert a == b


# ---------------------------------------------------------------------------
# S10 — Bounded (las propiedades se cubren en hypothesis; aquí solo un smoke)
# ---------------------------------------------------------------------------
class TestBoundedSmoke:
    """S10 del spec: smoke test del contrato de cota."""

    def test_reliability_weights_match_nato_admiralty(self) -> None:
        # Los seis valores curados, sin valores arbitrarios.
        assert RELIABILITY_WEIGHT[SourceReliability.A] == 1.00
        assert RELIABILITY_WEIGHT[SourceReliability.B] == 0.85
        assert RELIABILITY_WEIGHT[SourceReliability.C] == 0.70
        assert RELIABILITY_WEIGHT[SourceReliability.D] == 0.50
        assert RELIABILITY_WEIGHT[SourceReliability.E] == 0.30
        assert RELIABILITY_WEIGHT[SourceReliability.F] == 0.10

    def test_credibility_weights_match_nato_admiralty(self) -> None:
        assert CREDIBILITY_WEIGHT[Credibility.CONFIRMED] == 1.00
        assert CREDIBILITY_WEIGHT[Credibility.PROBABLY_TRUE] == 0.85
        assert CREDIBILITY_WEIGHT[Credibility.POSSIBLY_TRUE] == 0.60
        assert CREDIBILITY_WEIGHT[Credibility.DOUBTFUL] == 0.30
        assert CREDIBILITY_WEIGHT[Credibility.IMPROBABLE] == 0.10
        assert CREDIBILITY_WEIGHT[Credibility.CANNOT_BE_JUDGED] == 0.50

    def test_default_half_life_is_thirty_days(self) -> None:
        assert DEFAULT_HALF_LIFE_DAYS == 30.0

    def test_default_credibility_is_cannot_be_judged(self) -> None:
        assert DEFAULT_CREDIBILITY == Credibility.CANNOT_BE_JUDGED
