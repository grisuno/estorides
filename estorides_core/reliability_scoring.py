"""
estorides_core.reliability_scoring
==================================
Single source of truth for the ``confidence`` of an observation.

Replaces the two incompatible heuristics that used to live in
:mod:`estorides_core.entity_extraction` (``min(1.0, c + 0.1)``) and
:mod:`estorides_core.fusion_store` (``MAX(existing, incoming)``). The
model is NATO Admiralty System (source reliability A-F x information
credibility 1-6) extended with two operational factors: corroboration
(``min(1, log10(1 + n))`` over independent sources) and freshness
(exp half-life). Pure functions, no I/O, no logging, fail-loud on
programmer input, fail-soft on operator input.

The public surface:

    SourceReliability     enum str  {A, B, C, D, E, F}
    Credibility           enum int  {1..6}
    ConfidenceInput       dataclass, validated
    ConfidenceResult      dataclass frozen, JSON-serialisable
    compute_confidence    pure, O(1), no I/O
    merge_confidence      pure, O(1), no I/O
    reliability_from_name pure, never raises, never logs input
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum


# --------------------------------------------------------------------------- enums
class SourceReliability(str, Enum):
    """NATO Admiralty source-reliability rating (A-F)."""

    A = "A"  # Completely reliable
    B = "B"  # Usually reliable
    C = "C"  # Fairly reliable
    D = "D"  # Not usually reliable
    E = "E"  # Unreliable
    F = "F"  # Cannot be judged


class Credibility(int, Enum):
    """NATO Admiralty information-credibility rating (1-6)."""

    CONFIRMED = 1
    PROBABLY_TRUE = 2
    POSSIBLY_TRUE = 3
    DOUBTFUL = 4
    IMPROBABLE = 5
    CANNOT_BE_JUDGED = 6


# --------------------------------------------------------------------------- weights
RELIABILITY_WEIGHT: dict[SourceReliability, float] = {
    SourceReliability.A: 1.00,
    SourceReliability.B: 0.85,
    SourceReliability.C: 0.70,
    SourceReliability.D: 0.50,
    SourceReliability.E: 0.30,
    SourceReliability.F: 0.10,
}

CREDIBILITY_WEIGHT: dict[Credibility, float] = {
    Credibility.CONFIRMED: 1.00,
    Credibility.PROBABLY_TRUE: 0.85,
    Credibility.POSSIBLY_TRUE: 0.60,
    Credibility.DOUBTFUL: 0.30,
    Credibility.IMPROBABLE: 0.10,
    Credibility.CANNOT_BE_JUDGED: 0.50,
}

DEFAULT_RELIABILITY: SourceReliability = SourceReliability.C
DEFAULT_CREDIBILITY: Credibility = Credibility.CANNOT_BE_JUDGED
DEFAULT_HALF_LIFE_DAYS: float = 30.0


# --------------------------------------------------------------------------- curated map
SOURCE_RELIABILITY_MAP: dict[str, SourceReliability] = {
    "crt_sh_certificates": SourceReliability.A,
    "rdap_domain": SourceReliability.A,
    "rdap_ip": SourceReliability.A,
    "ripe_stat": SourceReliability.A,
    "nvd_cve": SourceReliability.A,
    "cve_search_circl": SourceReliability.A,
    "haveibeenpwned_breach": SourceReliability.A,
    "macvendors_lookup": SourceReliability.A,
    "wikidata_search": SourceReliability.B,
    "wikipedia_search": SourceReliability.B,
    "wikipedia_summary": SourceReliability.B,
    "shodan_internetdb": SourceReliability.B,
    "alienvault_otx": SourceReliability.B,
    "otx_domain_passive": SourceReliability.B,
    "otx_ip_passive": SourceReliability.B,
    "abuseipdb_check": SourceReliability.B,
    "greynoise_community": SourceReliability.B,
    "phishtank_lookup": SourceReliability.B,
    "urlhaus_recent": SourceReliability.B,
    "urlhaus_payloads": SourceReliability.B,
    "github_advisories": SourceReliability.B,
    "github_repos": SourceReliability.B,
    "ipapi_co_full": SourceReliability.B,
    "wayback_machine_cdx": SourceReliability.B,
    "wayback_machine_snapshot": SourceReliability.B,
    "urlscan_public": SourceReliability.B,
    "ipapi_free": SourceReliability.C,
    "ipinfo_free": SourceReliability.C,
    "ipwhois_free": SourceReliability.C,
    "ipwho_is": SourceReliability.C,
    "hackertarget_whois": SourceReliability.C,
    "hackertarget_dns": SourceReliability.C,
    "hackertarget_hostsearch": SourceReliability.C,
    "dns_google": SourceReliability.B,
    "dns_cloudflare": SourceReliability.B,
    "dehashed_email": SourceReliability.C,
    "intelx_email": SourceReliability.C,
    "leakcheck_public": SourceReliability.D,
    "telegram_search_ligated": SourceReliability.D,
    "psbdmp_ws": SourceReliability.D,
    "gists_github_search": SourceReliability.C,
    "duckduckgo_instant": SourceReliability.D,
    "untrusted_webscraper": SourceReliability.F,
}


# --------------------------------------------------------------------------- dataclasses
@dataclass(frozen=True)
class ConfidenceInput:
    """Validated input to :func:`compute_confidence`."""

    source_reliability: SourceReliability = DEFAULT_RELIABILITY
    credibility: Credibility = DEFAULT_CREDIBILITY
    corroboration_count: int = 0
    observation_age_seconds: float = 0.0
    base_confidence: float = 1.0

    def __post_init__(self) -> None:
        if self.corroboration_count < 0:
            raise ValueError("corroboration_count must be >= 0")
        if self.observation_age_seconds < 0.0:
            raise ValueError("observation_age_seconds must be >= 0")
        if not 0.0 <= self.base_confidence <= 1.0:
            raise ValueError("base_confidence must be in [0, 1]")


@dataclass(frozen=True)
class ConfidenceResult:
    """Auditable output of :func:`compute_confidence` / :func:`merge_confidence`."""

    score: float
    reliability_weight: float
    credibility_weight: float
    corroboration_weight: float
    freshness_weight: float
    source_reliability: SourceReliability
    credibility: Credibility
    observation_age_seconds: float
    corroboration_count: int


# --------------------------------------------------------------------------- formulas
def _corroboration_weight(n: int) -> float:
    """``min(1, log10(1 + n))``.  0 sources → 0; 1 → 0.30; 9 → 1.0."""
    if n <= 0:
        return 0.0
    return min(1.0, math.log10(1.0 + n))


def _freshness_weight(age_seconds: float, half_life_days: float) -> float:
    """Exponential decay.  age=0 → 1.0; one half-life → 0.5."""
    if half_life_days <= 0.0:
        raise ValueError("half_life_days must be > 0")
    if age_seconds <= 0.0:
        return 1.0
    age_days = age_seconds / 86400.0
    return math.exp(-math.log(2) * age_days / half_life_days)


def _validate_score(value: float, field_name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{field_name} must be in [0, 1], got {value!r}")


def _clamp01(value: float) -> float:
    """Clamp to the closed unit interval."""
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return value


# --------------------------------------------------------------------------- public
def compute_confidence(
    inp: ConfidenceInput,
    *,
    half_life_days: float = DEFAULT_HALF_LIFE_DAYS,
) -> ConfidenceResult:
    """Compute the audit-trailed confidence score for one observation.

    Pure: no I/O, no logging, no clock. Identical input → identical output
    bit-by-bit. Bounded to ``[0, 1]``.
    """
    if half_life_days <= 0.0:
        raise ValueError("half_life_days must be > 0")

    r = RELIABILITY_WEIGHT[inp.source_reliability]
    c = CREDIBILITY_WEIGHT[inp.credibility]
    cor = _corroboration_weight(inp.corroboration_count)
    fresh = _freshness_weight(inp.observation_age_seconds, half_life_days)
    score = _clamp01(inp.base_confidence * r * c * cor * fresh)

    return ConfidenceResult(
        score=score,
        reliability_weight=r,
        credibility_weight=c,
        corroboration_weight=cor,
        freshness_weight=fresh,
        source_reliability=inp.source_reliability,
        credibility=inp.credibility,
        observation_age_seconds=inp.observation_age_seconds,
        corroboration_count=inp.corroboration_count,
    )


def merge_confidence(
    existing: float,
    new_observation: float,
    *,
    new_reliability: SourceReliability,
    new_credibility: Credibility,
    corroboration_count: int,
    observation_age_seconds: float,
    half_life_days: float = DEFAULT_HALF_LIFE_DAYS,
) -> ConfidenceResult:
    """Merge a new observation's confidence into an existing entity score.

    The result is ``max(existing, new_score)`` clamped to ``[0, 1]``. An
    unreliable new observation cannot raise a strongly-corroborated
    existing one; a reliable new observation can lift a weakly-attested
    one. The :class:`ConfidenceResult` exposes the weights of the *new*
    observation so the audit trail is intact.
    """
    _validate_score(existing, "existing")
    _validate_score(new_observation, "new_observation")
    if corroboration_count < 1:
        raise ValueError("corroboration_count must be >= 1 for a merge")
    if observation_age_seconds < 0.0:
        raise ValueError("observation_age_seconds must be >= 0")

    new_inp = ConfidenceInput(
        source_reliability=new_reliability,
        credibility=new_credibility,
        corroboration_count=corroboration_count,
        observation_age_seconds=observation_age_seconds,
        base_confidence=new_observation,
    )
    new_result = compute_confidence(new_inp, half_life_days=half_life_days)
    return ConfidenceResult(
        score=_clamp01(max(existing, new_result.score)),
        reliability_weight=new_result.reliability_weight,
        credibility_weight=new_result.credibility_weight,
        corroboration_weight=new_result.corroboration_weight,
        freshness_weight=new_result.freshness_weight,
        source_reliability=new_result.source_reliability,
        credibility=new_result.credibility,
        observation_age_seconds=new_result.observation_age_seconds,
        corroboration_count=new_result.corroboration_count,
    )


def reliability_from_name(source_name: str | None) -> SourceReliability:
    """Look up the reliability for a source by name; never raises.

    Operator input is potentially adversarial. We do not log, do not
    validate beyond ``lower().strip()``, and never raise. Unknown names
    fall back to :data:`DEFAULT_RELIABILITY`.
    """
    if not source_name:
        return DEFAULT_RELIABILITY
    key = source_name.strip().lower()
    if not key:
        return DEFAULT_RELIABILITY
    return SOURCE_RELIABILITY_MAP.get(key, DEFAULT_RELIABILITY)


__all__ = [
    "CREDIBILITY_WEIGHT",
    "DEFAULT_CREDIBILITY",
    "DEFAULT_HALF_LIFE_DAYS",
    "DEFAULT_RELIABILITY",
    "RELIABILITY_WEIGHT",
    "SOURCE_RELIABILITY_MAP",
    "ConfidenceInput",
    "ConfidenceResult",
    "Credibility",
    "SourceReliability",
    "compute_confidence",
    "merge_confidence",
    "reliability_from_name",
]
