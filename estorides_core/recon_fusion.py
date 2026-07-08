"""
estorides_core.recon_fusion
===========================
Passive reconnaissance fusion engine: groups, deduplicates and classifies
OSINT results by relevance tier so the operator sees the most useful
information first.

Pure transformation: List[Observation] + List[Entity] + Query -> FusionResult.
"""
from __future__ import annotations

import hashlib
import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .reliability_scoring import reliability_from_name


class RelevanceTier(str, Enum):
    """Relevance classification for grouped reconnaissance results.

    Ordered from most to least relevant for UI rendering.
    """

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NOISE = "noise"

    @classmethod
    def ordered(cls) -> list[RelevanceTier]:
        """Return tiers in canonical display order."""
        return [cls.CRITICAL, cls.HIGH, cls.MEDIUM, cls.LOW, cls.NOISE]


@dataclass(frozen=True)
class ReconFusionConfig:
    """Centralised tunables for the recon fusion engine.

    Every threshold has an env var equivalent so the operator can adjust
    classification without touching code.
    """

    critical_min_sources: int = 3
    high_min_sources: int = 2
    high_min_reliability: str = "B"
    medium_min_reliability: str = "D"
    noise_max_reliability: str = "F"
    freshness_max_hours: float = 72.0
    direct_match_boost: float = 0.15
    exact_dedup_keys: tuple[str, ...] = ("source", "parser", "status")
    source_reliability_overrides: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.critical_min_sources <= self.high_min_sources:
            raise ValueError(
                f"critical_min_sources ({self.critical_min_sources}) must be "
                f"> high_min_sources ({self.high_min_sources})"
            )
        if self.freshness_max_hours <= 0.0:
            object.__setattr__(self, "freshness_max_hours", 1.0)


@dataclass(frozen=True)
class GroupedEntity:
    """One canonical entity grouped across all sources that observed it."""

    canonical_id: str
    type: str
    value: str
    normalized: str
    relevance_score: float
    tier: str
    source_count: int
    sources: tuple[str, ...]
    max_confidence: float
    direct_match: bool
    first_seen: float
    last_seen: float
    top_observations: tuple[dict[str, Any], ...]
    key_findings: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "type": self.type,
            "value": self.value,
            "normalized": self.normalized,
            "relevance_score": self.relevance_score,
            "tier": self.tier,
            "source_count": self.source_count,
            "sources": list(self.sources),
            "max_confidence": self.max_confidence,
            "direct_match": self.direct_match,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "top_observations": list(self.top_observations),
            "key_findings": list(self.key_findings),
        }


@dataclass(frozen=True)
class FusionResult:
    """Complete output of the recon fusion engine."""

    query: str
    query_type: str
    total_observations: int
    total_entities: int
    tiers: dict[str, list[GroupedEntity]]
    tier_summary: dict[str, int]
    generated_at: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "query_type": self.query_type,
            "total_observations": self.total_observations,
            "total_entities": self.total_entities,
            "tiers": {k: [g.to_dict() for g in v] for k, v in self.tiers.items()},
            "tier_summary": dict(self.tier_summary),
            "generated_at": self.generated_at,
        }


def _normalize_value(etype: str, value: str) -> str:
    """Deterministic normalisation matching fusion_store.entity_id."""
    return f"{etype}:{(value or '').strip().lower()}"


def _canonical_id(etype: str, value: str) -> str:
    """Deterministic sha1-based entity id matching fusion_store convention."""
    norm = _normalize_value(etype, value)
    return hashlib.sha1(norm.encode("utf-8"), usedforsecurity=False).hexdigest()[:16]


def _reliability_weight(source_name: str, overrides: dict[str, str]) -> float:
    """Map a source name to its numeric reliability weight.

    Uses overrides first, then the curated reliability_scoring map.
    Returns 0.7 (C, fairly reliable) as default for unknown sources.
    """
    from .reliability_scoring import RELIABILITY_WEIGHT, SourceReliability

    lookup = overrides.get(source_name)
    if lookup is None:
        rel = reliability_from_name(source_name)
    else:
        try:
            rel = SourceReliability(lookup)
        except ValueError:
            rel = SourceReliability.C
    return RELIABILITY_WEIGHT.get(rel, 0.7)


def _corroboration_factor(source_count: int) -> float:
    """Logarithmic corroboration weight: min(1, log10(1 + n))."""
    if source_count <= 0:
        return 0.0
    return min(1.0, math.log10(1.0 + source_count))


def _freshness_factor(age_hours: float, max_hours: float) -> float:
    """Linear freshness decay from 1.0 (fresh) to 0.1 (stale)."""
    if age_hours <= 0.0:
        return 1.0
    ratio = age_hours / max_hours
    return max(0.1, 1.0 - ratio)


def _direct_match_query(value: str, query: str) -> bool:
    """True if the entity value matches the original query."""
    return value.strip().lower() == query.strip().lower()


def _extract_key_findings(observations: list[dict[str, Any]]) -> list[str]:
    """Extract textual key findings from a list of observations."""
    findings: list[str] = []
    for obs in observations:
        parsed = obs.get("parsed")
        if not isinstance(parsed, dict):
            continue
        for key, val in parsed.items():
            if isinstance(val, str) and len(val) > 2 and len(val) < 100:
                finding = f"{key}: {val}"
                if finding not in findings:
                    findings.append(finding)
            elif isinstance(val, list) and len(val) > 0:
                for item in val[:3]:
                    if isinstance(item, str) and len(item) > 2 and len(item) < 100:
                        finding = f"{key}: {item}"
                        if finding not in findings:
                            findings.append(finding)
        if len(findings) >= 5:
            break
    return findings[:5]


class ReconFusionEngine:
    """Stateless engine that classifies raw OSINT results into relevance tiers.

    Thread-safe (no mutable state). Reusable across requests.
    """

    def __init__(self, config: ReconFusionConfig | None = None) -> None:
        self._cfg = config or ReconFusionConfig()

    def classify(
        self,
        query: str,
        query_type: str,
        observations: list[dict[str, Any]] | None,
        entities: list[dict[str, Any]] | None,
    ) -> FusionResult:
        """Classify raw observations and entities into relevance-tiered groups.

        Args:
            query: The original operator query (non-empty).
            query_type: Detected type of the query.
            observations: Raw observation dicts from the orchestrator.
            entities: Raw entity dicts from entity extraction.

        Returns:
            FusionResult with tiered, grouped, deduplicated results.

        Raises:
            ValueError: If query is empty.
        """
        if not query or not query.strip():
            raise ValueError("query must be non-empty")
        query = query.strip()
        obs_list = list(observations or [])
        ent_list = list(entities or [])

        deduped_obs = self._deduplicate(obs_list)
        grouped = self._group_by_entity(deduped_obs, ent_list)
        classified = self._classify_groups(grouped, query)

        tiers: dict[str, list[GroupedEntity]] = {
            t.value: [] for t in RelevanceTier.ordered()
        }
        for group in classified:
            tiers[group.tier].append(group)
        for key in tiers:
            tiers[key].sort(key=lambda g: g.relevance_score, reverse=True)
        tier_summary = {k: len(v) for k, v in tiers.items()}

        return FusionResult(
            query=query,
            query_type=query_type,
            total_observations=len(obs_list),
            total_entities=len(ent_list),
            tiers=tiers,
            tier_summary=tier_summary,
            generated_at=time.time(),
        )

    def _deduplicate(
        self, observations: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Remove exact duplicates based on config dedup keys.

        Two observations are identical if they share the same values for all
        exact_dedup_keys. The first occurrence is kept.
        """
        seen: set[tuple[Any, ...]] = set()
        result: list[dict[str, Any]] = []
        keys = self._cfg.exact_dedup_keys
        for obs in observations:
            signature = tuple(obs.get(k) for k in keys)
            if signature not in seen:
                seen.add(signature)
                result.append(obs)
        return result

    def _group_by_entity(
        self,
        observations: list[dict[str, Any]],
        entities: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        """Group observations and entities by canonical entity id.

        Primary grouping key is the explicit entity list. Observations are
        attached to groups when the entity value appears in the observation's
        parsed data or the observation source matches the entity's sources.
        """
        groups: dict[str, dict[str, Any]] = {}

        for ent in entities:
            etype = ent.get("type")
            value = ent.get("value")
            if not etype or not value:
                continue
            cid = _canonical_id(etype, str(value))
            norm_str = _normalize_value(etype, str(value))
            if cid not in groups:
                groups[cid] = {
                    "cid": cid,
                    "type": etype,
                    "value": str(value),
                    "normalized": norm_str,
                    "observations": [],
                    "entity_sources": set(),
                    "max_confidence": 0.0,
                    "first_seen": float("inf"),
                    "last_seen": 0.0,
                }
            g = groups[cid]
            g["entity_sources"].update(
                str(s) for s in (ent.get("sources") or []) if s
            )
            conf = float(ent.get("confidence", 1.0) or 1.0)
            if conf > g["max_confidence"]:
                g["max_confidence"] = conf

        parsed_value_index: dict[str, list[str]] = {}
        for cid, g in groups.items():
            val_lower = g["value"].strip().lower()
            parsed_value_index.setdefault(val_lower, []).append(cid)

        for obs in observations:
            obs_source = obs.get("source")
            if not obs_source:
                continue
            parsed = obs.get("parsed")
            if not isinstance(parsed, dict):
                continue

            matched_cids: set[str] = set()
            for _key, val in parsed.items():
                if isinstance(val, str) and len(val) > 0:
                    val_lower = val.strip().lower()
                    if val_lower in parsed_value_index:
                        matched_cids.update(parsed_value_index[val_lower])

            if not matched_cids and isinstance(parsed, dict):
                for cid, g in groups.items():
                    if obs_source in g["entity_sources"]:
                        matched_cids.add(cid)
                        break

            for cid in matched_cids:
                g = groups[cid]
                g["observations"].append(obs)
                g["entity_sources"].add(str(obs_source))
                meta = obs.get("meta") or {}
                if isinstance(meta, dict):
                    now = time.time()
                    g["first_seen"] = min(g["first_seen"], float(meta.get("started_at", now)))
                    g["last_seen"] = max(g["last_seen"], float(meta.get("completed_at", now)))

        for g in groups.values():
            if g["first_seen"] == float("inf"):
                g["first_seen"] = time.time()
            if g["last_seen"] == 0.0:
                g["last_seen"] = time.time()

        return groups

    def _classify_groups(
        self,
        groups: dict[str, dict[str, Any]],
        query: str,
    ) -> list[GroupedEntity]:
        """Assign each group a relevance tier and score."""
        result: list[GroupedEntity] = []
        overrides = self._cfg.source_reliability_overrides

        for cid, g in groups.items():
            gtype: str = g["type"]
            gvalue: str = g["value"]
            norm: str = g["normalized"]
            sources: set[str] = g["entity_sources"]
            obs_list: list[dict[str, Any]] = g["observations"]
            max_conf: float = g["max_confidence"]
            first_seen: float = g["first_seen"]
            last_seen: float = g["last_seen"]

            source_count = len(sources)
            direct = _direct_match_query(gvalue, query)

            avg_reliability = (
                sum(_reliability_weight(s, overrides) for s in sources)
                / max(source_count, 1)
            )
            corroboration = _corroboration_factor(source_count)
            age_hours = (time.time() - last_seen) / 3600.0
            freshness = _freshness_factor(max(age_hours, 0.0), self._cfg.freshness_max_hours)

            base_score = avg_reliability * corroboration * freshness
            if direct:
                base_score *= 1.0 + self._cfg.direct_match_boost
            relevance_score = min(1.0, base_score)

            tier = self._assign_tier(
                source_count=source_count,
                avg_reliability=avg_reliability,
                direct_match=direct,
            )

            top_obs = tuple(obs_list[:3])
            findings = tuple(_extract_key_findings(obs_list))

            grouped_entity = GroupedEntity(
                canonical_id=cid,
                type=gtype,
                value=gvalue,
                normalized=norm,
                relevance_score=round(relevance_score, 4),
                tier=tier.value,
                source_count=source_count,
                sources=tuple(sorted(sources)),
                max_confidence=max_conf,
                direct_match=direct,
                first_seen=first_seen,
                last_seen=last_seen,
                top_observations=top_obs,
                key_findings=findings,
            )
            result.append(grouped_entity)

        result.sort(key=lambda g: g.relevance_score, reverse=True)
        return result

    def _assign_tier(
        self,
        source_count: int,
        avg_reliability: float,
        direct_match: bool,
    ) -> RelevanceTier:
        """Determine the relevance tier based on source count and reliability.

        Thresholds:
            CRITICAL: source_count >= critical_min_sources (3) OR
                      (source_count >= 2 AND avg_reliability >= B weight)
            HIGH:     source_count >= high_min_sources (2) OR
                      (source_count >= 1 AND avg_reliability >= high_min_reliability AND direct_match)
            MEDIUM:   source_count >= 1 AND avg_reliability > noise threshold
            LOW:      source_count >= 1 AND avg_reliability <= noise threshold
            NOISE:    source_count >= 1 AND avg_reliability <= F weight
                      OR no corroboration from untrusted source
        """
        cfg = self._cfg

        high_min_w = _reliability_weight_for_letter(cfg.high_min_reliability)
        medium_min_w = _reliability_weight_for_letter(cfg.medium_min_reliability)
        noise_max_w = _reliability_weight_for_letter(cfg.noise_max_reliability)

        if source_count >= cfg.critical_min_sources:
            return RelevanceTier.CRITICAL
        if source_count >= 2 and avg_reliability >= high_min_w:
            return RelevanceTier.CRITICAL
        if source_count >= cfg.high_min_sources:
            return RelevanceTier.HIGH
        if source_count >= 1 and avg_reliability >= high_min_w and direct_match:
            return RelevanceTier.HIGH
        if source_count >= 1 and avg_reliability > medium_min_w:
            return RelevanceTier.MEDIUM
        if source_count >= 1 and avg_reliability > noise_max_w:
            return RelevanceTier.LOW

        return RelevanceTier.NOISE


def _reliability_weight_for_letter(letter: str) -> float:
    """Convert a reliability letter (A-F) to its numeric weight."""
    from .reliability_scoring import RELIABILITY_WEIGHT, SourceReliability

    try:
        rel = SourceReliability(letter.upper())
    except ValueError:
        return 0.7
    return RELIABILITY_WEIGHT.get(rel, 0.7)


__all__ = [
    "FusionResult",
    "GroupedEntity",
    "ReconFusionConfig",
    "ReconFusionEngine",
    "RelevanceTier",
]
