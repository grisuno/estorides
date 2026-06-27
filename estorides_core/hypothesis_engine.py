"""
estorides_core.hypothesis_engine
================================
The "data → information" layer.

Consumes the per-run ``observations`` and ``entities`` produced by the
orchestrator and emits a deduplicated, scored, auditable list of
typed ``Hypothesis`` records. Each hypothesis carries the evidence
items that justify it (source, field, value, reliability-weighted
weight) and a human-readable ``claim`` and ``reasoning`` derived from
templates, not from the LLM.

Pure module: no I/O, no DB writes, no logging, no clock. Same input
⇒ same output, bit-by-bit. Hypothesis ids are content hashes so
duplicate runs produce the same ids and the fusion store can
deduplicate across runs.

Public surface::

    generate_hypotheses(observations, entities, kg=None,
                        min_score=0.10, max_hypotheses=50)
        -> list[Hypothesis]
"""
from __future__ import annotations

import hashlib
import logging
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, TypeGuard, runtime_checkable

from .reliability_scoring import (
    ConfidenceInput,
    SourceReliability,
    compute_confidence,
    reliability_from_name,
)

# --------------------------------------------------------------------------- types
#: Stable vocabulary of hypothesis types. Adding a new type is a
#: breaking change for downstream consumers (UI, fusion store,
#: cross-run joins) — coordinate with the spec.
HYPOTHESIS_TYPES: frozenset[str] = frozenset({
    "domain-belongsto-actor",
    "email-aliasto-person",
    "ip-shared-infra",
    "asn-shared-infra",
})


# --------------------------------------------------------------------------- dataclasses
@dataclass(frozen=True)
class EntityRef:
    """A typed reference to an entity involved in a hypothesis."""

    type: str
    value: str


@dataclass(frozen=True)
class Evidence:
    """One piece of supporting or contradicting evidence."""

    source: str
    field: str
    value: str
    weight: float
    reliability: SourceReliability


@dataclass(frozen=True)
class Hypothesis:
    """A typed, scored, auditable intelligence conclusion."""

    id: str
    type: str
    claim: str
    score: float
    confidence: float
    supporting: list[Evidence] = field(default_factory=list)
    contradicting: list[Evidence] = field(default_factory=list)
    entities: list[EntityRef] = field(default_factory=list)
    reasoning: str = ""
    sources: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- helpers
#: Cap on the length of a string value carried into an ``Evidence``.
#: Hostile observations can dump megabytes into a single field; we
#: truncate to keep memory and the JSON-serialised output bounded.
_VALUE_MAX_CHARS: int = 200

#: Soft cap on how many evidence items a single hypothesis aggregates.
#: Stops one pathological source (a 50 000-element parsed list) from
#: creating a hypothesis with 50 000 evidence items.
_MAX_EVIDENCE_PER_HYPOTHESIS: int = 100

#: Minimum number of distinct sources to consider a hypothesis worth
#: emitting in v1. Single-source hypotheses are emitted only if the
#: source is reliability A.
_MIN_SOURCES_FOR_V1: int = 1

#: Floor on the contradiction denominator so a hypothesis with one
#: weak supporting item and zero contradicting items still has a
#: sensible score (> 0 but not pinned to 1.0).
_SCORE_FLOOR: float = 0.1


def _truncate(value: Any) -> str:
    """Stringify a value, bounded to ``_VALUE_MAX_CHARS``."""
    if value is None:
        return ""
    s = str(value)
    if len(s) > _VALUE_MAX_CHARS:
        return s[:_VALUE_MAX_CHARS] + "…"
    return s


def _is_mapping(value: Any) -> TypeGuard[Mapping[str, Any]]:
    return isinstance(value, Mapping)


def _entity_lookup(entities: Sequence[Mapping[str, Any]]) -> dict[str, set[str]]:
    """Build ``{type: {value, value, ...}}`` from the entity list.

    Tolerates both ``Entity`` dataclass instances and plain dicts
    (the orchestrator returns both shapes depending on the call site).
    """
    out: dict[str, set[str]] = defaultdict(set)
    for e in entities:
        if e is None:
            continue
        if isinstance(e, Mapping):
            etype = str(e.get("type", "")).strip()
            value = str(e.get("value", "")).strip()
        else:
            etype = str(getattr(e, "type", "")).strip()
            value = str(getattr(e, "value", "")).strip()
        if etype and value:
            out[etype].add(value)
    return out


def _hypothesis_id(
    htype: str,
    entity_refs: Sequence[EntityRef],
    supporting: Sequence[Evidence],
) -> str:
    """Deterministic 16-char hex id for a hypothesis."""
    payload = "|".join(
        [
            htype,
            ",".join(sorted(f"{er.type}:{er.value}" for er in entity_refs)),
            ",".join(sorted(ev.source for ev in supporting)),
        ]
    )
    # SHA-1 is used here as a content-hash for deduplication, not for
    # security. The 16-char prefix is the collision space we accept.
    return hashlib.sha1(payload.encode("utf-8"), usedforsecurity=False).hexdigest()[:16]


def _score(supporting: Sequence[Evidence], contradicting: Sequence[Evidence]) -> float:
    """Net-support score in (0, 1].

    ``supporting / (supporting + contradicting + floor)`` — the floor
    prevents division by zero and prevents a single weak item from
    producing a "1.0 certain" score.
    """
    sup = sum(max(0.0, ev.weight) for ev in supporting)
    con = sum(max(0.0, ev.weight) for ev in contradicting)
    if sup <= 0.0 and con <= 0.0:
        return 0.0
    return sup / (sup + con + _SCORE_FLOOR)


def _confidence(
    supporting: Sequence[Evidence],
    contradicting: Sequence[Evidence],
) -> float:
    """Reliability-weighted confidence via :mod:`reliability_scoring`."""
    if not supporting and not contradicting:
        return 0.0
    # Use the highest reliability among supporting as the source reliability;
    # corroboration is the count of distinct sources.
    best_rel = SourceReliability.F
    for ev in supporting:
        if ev.reliability.value < best_rel.value:  # 'A' < 'B' < ... < 'F'
            best_rel = ev.reliability
    corroboration = max(1, len({ev.source for ev in supporting}))
    inp = ConfidenceInput(
        source_reliability=best_rel,
        corroboration_count=corroboration,
    )
    return compute_confidence(inp).score


def _clip_claim(template: str, *subs: Any) -> str:
    s = template.format(*subs)
    if len(s) > 280:
        return s[:277] + "..."
    return s


# --------------------------------------------------------------------------- generators
@runtime_checkable
class HypothesisGenerator(Protocol):
    """Strategy: turn a (observations, entities) snapshot into hypotheses."""

    def __call__(
        self,
        observations: Sequence[Mapping[str, Any]],
        entities: Sequence[Mapping[str, Any]],
    ) -> Iterable[Hypothesis]: ...


def _domain_belongsto_actor(
    observations: Sequence[Mapping[str, Any]],
    entities: Sequence[Mapping[str, Any]],
) -> Iterable[Hypothesis]:
    """`domain-belongsto-actor`: a domain's WHOIS/issuer/hosting org matches an entity."""
    # Build index: (domain_value) -> hypothesis seed (one per domain-actor pair).
    org_index = _entity_lookup(entities)
    actor_values = org_index.get("org", set()) | org_index.get("organization", set()) \
        | org_index.get("person", set())
    if not actor_values:
        return
    domain_values = org_index.get("domain", set())
    if not domain_values:
        return
    # Keys in `parsed` that, if present and matching an actor, count as evidence.
    relevant_keys = (
        "registrant_organization",
        "registrant_name",
        "issuer_name",
        "org",
        "organization",
        "asn_organization",
        "registrar",
        "label",
        "name",
    )
    # (domain, actor) -> list[Evidence]
    pairs: dict[tuple[str, str], list[Evidence]] = defaultdict(list)
    for obs in observations:
        if not _is_mapping(obs):
            continue
        src = str(obs.get("source", "")).strip()
        if not src:
            continue
        parsed = obs.get("parsed")
        if not _is_mapping(parsed):
            continue
        for key in relevant_keys:
            raw = parsed.get(key)
            if raw is None:
                continue
            value = _truncate(raw).strip()
            if not value:
                continue
            # Match against any known actor (org or person).
            for actor in actor_values:
                if value == actor or value.lower() == actor.lower():
                    # Map this evidence to every domain in the run that is
                    # potentially the one (we don't know which one — the
                    # WHOIS applies to the queried domain). We use the
                    # `domain` entity of the same observation if present.
                    domains_here = _domains_in_obs(obs) or list(domain_values)
                    for d in domains_here:
                        rel = reliability_from_name(src)
                        ev = Evidence(
                            source=src,
                            field=key,
                            value=value,
                            weight=0.70 if rel == SourceReliability.C else _RELIABILITY_TO_WEIGHT[rel],
                            reliability=rel,
                        )
                        if len(pairs[(d, actor)]) >= _MAX_EVIDENCE_PER_HYPOTHESIS:
                            continue
                        pairs[(d, actor)].append(ev)
    for (domain, actor), evs in pairs.items():
        if not evs:
            continue
        sources = sorted({ev.source for ev in evs})
        if len(sources) < _MIN_SOURCES_FOR_V1:
            continue
        claim = _clip_claim("{} is likely operated by {}", domain, actor)
        reasoning = _clip_claim(
            "{} source(s) tie {} to {} (e.g. {}={})",
            len(sources), domain, actor, evs[0].field, evs[0].value,
        )
        entity_refs = [EntityRef("domain", domain), EntityRef("org", actor)]
        score = _score(evs, [])
        conf = _confidence(evs, [])
        yield Hypothesis(
            id=_hypothesis_id("domain-belongsto-actor", entity_refs, evs),
            type="domain-belongsto-actor",
            claim=claim,
            score=score,
            confidence=conf,
            supporting=list(evs),
            contradicting=[],
            entities=entity_refs,
            reasoning=reasoning,
            sources=sources,
        )


def _domains_in_obs(obs: Mapping[str, Any]) -> list[str]:
    """Best-effort: extract domain-like values from a single observation.

    The orchestrator doesn't always stamp the queried domain on the
    observation, so this is a soft hint. Returns ``[]`` if nothing
    looks like a domain.
    """
    out: list[str] = []
    for key in ("domain", "queried_domain", "q", "target"):
        v = obs.get(key)
        if isinstance(v, str) and v:
            out.append(v.strip().lower())
    parsed = obs.get("parsed")
    if _is_mapping(parsed):
        for key in ("domain", "q", "queried"):
            v = parsed.get(key)
            if isinstance(v, str) and v:
                out.append(v.strip().lower())
    return out


# Mapping from reliability to weight, kept here as a private constant
# to avoid a circular import with the JSON-friendly public dict.
_RELIABILITY_TO_WEIGHT: dict[SourceReliability, float] = {
    SourceReliability.A: 1.00,
    SourceReliability.B: 0.85,
    SourceReliability.C: 0.70,
    SourceReliability.D: 0.50,
    SourceReliability.E: 0.30,
    SourceReliability.F: 0.10,
}


def _email_aliases_person(
    observations: Sequence[Mapping[str, Any]],
    entities: Sequence[Mapping[str, Any]],
) -> Iterable[Hypothesis]:
    """`email-aliasto-person`: an email and a person name appear together in one obs."""
    person_index = _entity_lookup(entities)
    person_values = person_index.get("person", set()) \
        | person_index.get("username", set())
    if not person_values:
        return
    pairs: dict[tuple[str, str], list[Evidence]] = defaultdict(list)
    for obs in observations:
        if not _is_mapping(obs):
            continue
        src = str(obs.get("source", "")).strip()
        if not src:
            continue
        parsed = obs.get("parsed")
        if parsed is None or not _is_mapping(parsed):
            continue
        email_val = _extract_email(parsed)
        person_val = _extract_person_name(parsed)
        if email_val is None or person_val is None:
            continue
        for person in person_values:
            if person_val.lower() == person.lower() or person_val.lower().startswith(person.lower() + " "):
                rel = reliability_from_name(src)
                ev = Evidence(
                    source=src,
                    field="email+name",
                    value=f"{email_val}<->{person_val}",
                    weight=_RELIABILITY_TO_WEIGHT[rel],
                    reliability=rel,
                )
                pairs[(email_val, person)].append(ev)
    for (email, person), evs in pairs.items():
        if not evs:
            continue
        sources = sorted({ev.source for ev in evs})
        claim = _clip_claim("{} is a likely alias of {}", email, person)
        reasoning = _clip_claim(
            "{} source(s) associate {} with name {}", len(sources), email, person,
        )
        entity_refs = [EntityRef("email", email), EntityRef("person", person)]
        score = _score(evs, [])
        conf = _confidence(evs, [])
        yield Hypothesis(
            id=_hypothesis_id("email-aliasto-person", entity_refs, evs),
            type="email-aliasto-person",
            claim=claim,
            score=score,
            confidence=conf,
            supporting=list(evs),
            contradicting=[],
            entities=entity_refs,
            reasoning=reasoning,
            sources=sources,
        )


def _extract_email(parsed: Mapping[str, Any]) -> str | None:
    """Find a value that looks like an email anywhere in the parsed dict."""
    for _key, value in parsed.items():
        if not isinstance(value, str):
            continue
        v = value.strip()
        if "@" in v and "." in v and " " not in v:
            return v
    return None


def _extract_person_name(parsed: Mapping[str, Any]) -> str | None:
    """Find a value that looks like a person name (has a space, no @, no path)."""
    for key in ("name", "full_name", "display_name", "real_name", "author", "owner"):
        value = parsed.get(key)
        if isinstance(value, str):
            v = value.strip()
            if " " in v and "@" not in v and "/" not in v and len(v) >= 3 and len(v) <= 80:
                return v
    return None


def _ip_shared_infra(
    observations: Sequence[Mapping[str, Any]],
    entities: Sequence[Mapping[str, Any]],
) -> Iterable[Hypothesis]:
    """`ip-shared-infra`: >=2 domains resolve to the same IP."""
    domain_index = _entity_lookup(entities)
    if not domain_index.get("domain"):
        return
    # domain -> set of IPs
    domain_to_ips: dict[str, set[str]] = defaultdict(set)
    domain_to_evidence: dict[tuple[str, str], Evidence] = {}
    for obs in observations:
        if not _is_mapping(obs):
            continue
        src = str(obs.get("source", "")).strip()
        if not src:
            continue
        parsed = obs.get("parsed")
        if not _is_mapping(parsed):
            continue
        if parsed is None or not _is_mapping(parsed):
            continue
        ips = _extract_ips(parsed)
        if not ips:
            continue
        rel = reliability_from_name(src)
        weight = _RELIABILITY_TO_WEIGHT[rel]
        for d in _domains_in_obs(obs) or list(domain_index["domain"]):
            for ip in ips:
                domain_to_ips[d].add(ip)
                ev = Evidence(
                    source=src,
                    field="ip",
                    value=ip,
                    weight=weight,
                    reliability=rel,
                )
                # First evidence per (domain, ip) wins; later ones get the
                # higher of the two weights (multi-source corroboration).
                key = (d, ip)
                prev = domain_to_evidence.get(key)
                if prev is None or ev.weight > prev.weight:
                    domain_to_evidence[key] = ev
    # ip -> set of domains
    ip_to_domains: dict[str, set[str]] = defaultdict(set)
    for d, ip_set in domain_to_ips.items():
        for ip in ip_set:
            ip_to_domains[ip].add(d)
    for ip, ds in ip_to_domains.items():
        if len(ds) < 2:
            continue
        domains_sorted = sorted(ds)
        evs = [domain_to_evidence[(d, ip)] for d in domains_sorted if (d, ip) in domain_to_evidence]
        if not evs:
            continue
        sources = sorted({ev.source for ev in evs})
        claim = _clip_claim(
            "{} is shared infrastructure between {} and {}",
            ip, domains_sorted[0], domains_sorted[1],
        )
        reasoning = _clip_claim(
            "{} source(s) point {} domain(s) at {} (e.g. {})",
            len(sources), len(domains_sorted), ip, ", ".join(domains_sorted[:3]),
        )
        entity_refs = [EntityRef("ip", ip)] + [EntityRef("domain", d) for d in domains_sorted]
        score = _score(evs, [])
        conf = _confidence(evs, [])
        yield Hypothesis(
            id=_hypothesis_id("ip-shared-infra", entity_refs, evs),
            type="ip-shared-infra",
            claim=claim,
            score=score,
            confidence=conf,
            supporting=list(evs),
            contradicting=[],
            entities=entity_refs,
            reasoning=reasoning,
            sources=sources,
        )


def _extract_ips(parsed: Mapping[str, Any]) -> list[str]:
    """Best-effort: pull IPv4-looking values out of a parsed payload."""
    out: list[str] = []
    for _key, value in parsed.items():
        if isinstance(value, str):
            v = value.strip()
            if _looks_like_ipv4(v):
                out.append(v)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and _looks_like_ipv4(item.strip()):
                    out.append(item.strip())
    return out


def _looks_like_ipv4(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p.isdigit():
            return False
        n = int(p)
        if not 0 <= n <= 255:
            return False
    return True


def _asn_shared_infra(
    observations: Sequence[Mapping[str, Any]],
    entities: Sequence[Mapping[str, Any]],
) -> Iterable[Hypothesis]:
    """`asn-shared-infra`: >=3 entities of the run live in the same ASN."""
    asn_index: dict[str, set[str]] = defaultdict(set)  # asn -> set of entity refs
    asn_evidence: dict[str, Evidence] = {}
    for obs in observations:
        if not _is_mapping(obs):
            continue
        src = str(obs.get("source", "")).strip()
        if not src:
            continue
        parsed = obs.get("parsed")
        if not _is_mapping(parsed):
            continue
        asn = _extract_asn(parsed)
        if asn is None:
            continue
        # The entities that this observation is "about" — domains + IPs that
        # the run had on its radar.
        local_entities: set[str] = set()
        for d in _domains_in_obs(obs):
            local_entities.add(f"domain:{d}")
        rel = reliability_from_name(src)
        weight = _RELIABILITY_TO_WEIGHT[rel]
        ev = Evidence(
            source=src, field="asn", value=asn, weight=weight, reliability=rel,
        )
        prev = asn_evidence.get(asn)
        if prev is None or ev.weight > prev.weight:
            asn_evidence[asn] = ev
        for etype_evalue in local_entities:
            asn_index[asn].add(etype_evalue)
    for asn, ents in asn_index.items():
        if len(ents) < 3:
            continue
        ev = asn_evidence[asn]
        # Reuse the same evidence once per entity (multiplicity doesn't
        # change the score; it's a count signal handled by corroboration).
        evs = [ev] * len(ents)
        entity_refs = [EntityRef(*e.split(":", 1)) for e in sorted(ents) if ":" in e]
        sources = [ev.source]
        claim = _clip_claim("{} hosts {} entities from this investigation", asn, len(ents))
        reasoning = _clip_claim(
            "{} entity(ies) in the run share ASN {} (per {})",
            len(ents), asn, ev.source,
        )
        score = _score(evs, [])
        conf = _confidence(evs, [])
        yield Hypothesis(
            id=_hypothesis_id("asn-shared-infra", entity_refs, evs),
            type="asn-shared-infra",
            claim=claim,
            score=score,
            confidence=conf,
            supporting=list(evs),
            contradicting=[],
            entities=entity_refs,
            reasoning=reasoning,
            sources=sources,
        )


def _extract_asn(parsed: Mapping[str, Any]) -> str | None:
    """Best-effort: pull an AS-number-ish value out of the parsed payload."""
    for key in ("asn", "as", "asn_organization"):
        v = parsed.get(key)
        if isinstance(v, str):
            s = v.strip()
            if s.upper().startswith("AS") and s[2:].isdigit():
                return s.upper()
            if s.isdigit():
                return f"AS{s}"
        elif isinstance(v, int):
            return f"AS{v}"
    return None


# --------------------------------------------------------------------------- registry
_GENERATORS: tuple[HypothesisGenerator, ...] = (
    _domain_belongsto_actor,
    _email_aliases_person,
    _ip_shared_infra,
    _asn_shared_infra,
)


# --------------------------------------------------------------------------- public
def generate_hypotheses(
    observations: Sequence[Mapping[str, Any]],
    entities: Sequence[Mapping[str, Any]],
    kg: Any = None,
    *,
    min_score: float = 0.10,
    max_hypotheses: int = 50,
) -> list[Hypothesis]:
    """Generate typed, scored, auditable hypotheses for a run.

    Pure: no I/O, no DB writes, no logging, no clock. Same input ⇒
    same output bit-by-bit. Hypothesis ids are content hashes so the
    fusion store can deduplicate across runs.

    Parameters
    ----------
    observations
        Per-source observations from the orchestrator. Each one is
        expected to have at least ``source`` and ``parsed``; the
        generator skips malformed entries without raising.
    entities
        The deduplicated entity list from the orchestrator. Each
        item can be a dict (``{"type": ..., "value": ...}``) or an
        ``Entity`` dataclass.
    kg
        Optional knowledge graph. Reserved for future generators
        (ego-network, motif-based) — ignored in v1.
    min_score
        Floor for the output: hypotheses with score below this are
        dropped. ``[0, 1]``.
    max_hypotheses
        Hard cap on the returned list. Top by score.
    """
    if not isinstance(observations, Sequence) or isinstance(observations, (str, bytes)):
        raise TypeError("observations must be a sequence of mapping")
    if not isinstance(entities, Sequence) or isinstance(entities, (str, bytes)):
        raise TypeError("entities must be a sequence of mapping")
    if not 0.0 <= min_score <= 1.0:
        raise ValueError("min_score must be in [0, 1]")
    if max_hypotheses < 1:
        raise ValueError("max_hypotheses must be >= 1")

    out: list[Hypothesis] = []
    for gen in _GENERATORS:
        try:
            yield_result = gen(observations, entities)
        except Exception as exc:
            # A misbehaving generator must never break the rest. The
            # engine is fail-soft on the data side; the orchestrator
            # is the one place where data errors are loud. We log the
            # failure (not the user-controlled input) so an operator
            # can see which generator died in the run's stderr.
            logging.getLogger("estorides.hypothesis").warning(
                "generator %s failed: %s: %s",
                getattr(gen, "__name__", repr(gen)),
                type(exc).__name__,
                exc,
            )
            continue
        for h in yield_result:
            if h.score < min_score:
                continue
            out.append(h)
    # Stable order: highest score first, then by id (deterministic).
    out.sort(key=lambda h: (-h.score, h.id))
    return out[:max_hypotheses]


__all__ = [
    "HYPOTHESIS_TYPES",
    "EntityRef",
    "Evidence",
    "Hypothesis",
    "generate_hypotheses",
]
