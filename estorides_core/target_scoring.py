from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.target_scoring")

CROWN_JEWEL_KEYWORDS = {
    "jenkins", "jira", "vpn", "confluence", "gitlab", "grafana",
    "kibana", "prometheus", "admin", "dashboard", "console",
    "manager", "monitor", "sso", "auth", "login", "owa",
    "webmail", "exchange", "splunk", "nexus", "artifactory",
    "sonarqube", "harbor", "registry", "pipeline", "runner",
    "ci", "cd", "deploy", "release", "build", "test",
    "api", "graphql", "swagger", "docs", "wiki",
}


@dataclass
class TargetScoringConfig:
    surface_weight: float = 0.35
    soft_weight: float = 0.30
    jewel_weight: float = 0.20
    lateral_weight: float = 0.15

    def __post_init__(self) -> None:
        total = self.surface_weight + self.soft_weight + self.jewel_weight + self.lateral_weight
        if abs(total - 1.0) > 0.01:
            log.warning("TargetScoringConfig weights sum to %.2f, normalising", total)


@dataclass
class ScoredTarget:
    target: str
    attack_surface_score: float
    soft_target_score: float
    crown_jewel_score: float
    lateral_potential: float
    composite_score: float
    tier: str
    key_findings: list[str]
    recommended_actions: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ScoringSummary:
    total_targets: int = 0
    critical_targets: int = 0
    high_targets: int = 0
    medium_targets: int = 0
    low_targets: int = 0
    noise_targets: int = 0
    top_target: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TargetScoringResult:
    targets: list[ScoredTarget] = field(default_factory=list)
    top_recommendations: list[str] = field(default_factory=list)
    summary: ScoringSummary = field(default_factory=ScoringSummary)

    def to_dict(self) -> dict[str, Any]:
        return {
            "targets": [t.to_dict() for t in self.targets],
            "top_recommendations": self.top_recommendations,
            "summary": self.summary.to_dict(),
        }


def compute_composite(
    surface: float, soft: float, jewel: float, lateral: float,
    config: TargetScoringConfig | None = None,
) -> float:
    cfg = config or TargetScoringConfig()
    return round(
        surface * cfg.surface_weight
        + soft * cfg.soft_weight
        + jewel * cfg.jewel_weight
        + lateral * cfg.lateral_weight,
        4,
    )


def _determine_tier(composite: float) -> str:
    if composite > 0.7:
        return "critical"
    elif composite > 0.5:
        return "high"
    elif composite > 0.3:
        return "medium"
    elif composite > 0.1:
        return "low"
    return "noise"


def _compute_crown_jewel(target: str) -> float:
    hostname = target.split("://", 1)[-1].split("/")[0]
    parts = hostname.lower().split(".")
    for part in parts:
        if part in CROWN_JEWEL_KEYWORDS:
            return 0.9
    for kw in CROWN_JEWEL_KEYWORDS:
        if kw in hostname.lower():
            return 0.7
    return 0.2


def score_target(
    target: str,
    tech_data: dict[str, Any],
    vuln_data: dict[str, Any],
    cloud_data: dict[str, Any] | None = None,
    people_data: dict[str, Any] | None = None,
    code_data: dict[str, Any] | None = None,
    supply_data: dict[str, Any] | None = None,
    pdns_data: dict[str, Any] | None = None,
    config: TargetScoringConfig | None = None,
) -> ScoredTarget:
    surface = 0.0
    soft = 0.0
    lateral = 0.0
    findings: list[str] = []

    if cloud_data:
        assets = cloud_data.get("assets", []) if isinstance(cloud_data, dict) else getattr(cloud_data, "assets", [])
        accessible = sum(1 for a in assets if (isinstance(a, dict) and a.get("accessible")) or getattr(a, "accessible", False))
        if accessible > 0:
            surface += 0.3
            findings.append(f"{accessible} accessible cloud asset(s)")

    if vuln_data:
        if isinstance(vuln_data, dict):
            total_vulns = vuln_data.get("total_vulnerabilities", 0)
            critical = vuln_data.get("critical_count", 0)
        else:
            total_vulns = getattr(vuln_data, "total_vulnerabilities", 0)
            critical = getattr(vuln_data, "critical_count", 0)

        if critical > 0:
            soft += 0.4
            findings.append(f"{critical} critical vulnerability(ies)")
        if total_vulns > 0:
            soft += min(0.3, total_vulns * 0.05)

    if code_data:
        if isinstance(code_data, dict):
            code_critical = (code_data.get("severity_summary") or {}).get("critical", 0)
        else:
            code_critical = getattr(getattr(code_data, "severity_summary", None), "critical", 0)

        if code_critical > 0:
            lateral += 0.2
            surface += 0.2
            findings.append(f"{code_critical} critical code exposure(s)")

    if people_data:
        if isinstance(people_data, dict):
            risk = people_data.get("risk_score", 0)
        else:
            risk = getattr(people_data, "risk_score", 0)
        if risk > 0.5:
            lateral += 0.2
            findings.append("High-risk employee breach exposure")

    if pdns_data:
        if isinstance(pdns_data, dict):
            total_subs = pdns_data.get("total_subdomains", 0)
        else:
            total_subs = getattr(pdns_data, "total_subdomains", 0)
        if total_subs > 10:
            surface += 0.1
        elif total_subs > 50:
            surface += 0.2

    if tech_data:
        if isinstance(tech_data, dict):
            tech_count = len(tech_data.get("technologies", []))
        else:
            tech_count = len(getattr(tech_data, "technologies", []))
        if tech_count > 5:
            surface += 0.1

    crown_jewel = _compute_crown_jewel(target)
    surface = min(1.0, surface)
    soft = min(1.0, soft)
    lateral = min(1.0, lateral)
    composite = compute_composite(surface, soft, crown_jewel, lateral, config)
    tier = _determine_tier(composite)

    recs = []
    if findings:
        recs.append(f"Prioritise {target} — {len(findings)} finding(s): {'; '.join(findings)}")
    if tier == "critical":
        recs.append(f"Immediate attention required for {target}")
    if crown_jewel > 0.5:
        recs.append(f"{target} appears to be a crown jewel asset")

    return ScoredTarget(
        target=target,
        attack_surface_score=surface,
        soft_target_score=soft,
        crown_jewel_score=crown_jewel,
        lateral_potential=lateral,
        composite_score=composite,
        tier=tier,
        key_findings=findings,
        recommended_actions=recs,
    )


def score_all_targets(
    targets: list[ScoredTarget],
) -> TargetScoringResult:
    summary = ScoringSummary(total_targets=len(targets))
    for t in targets:
        if t.tier == "critical":
            summary.critical_targets += 1
        elif t.tier == "high":
            summary.high_targets += 1
        elif t.tier == "medium":
            summary.medium_targets += 1
        elif t.tier == "low":
            summary.low_targets += 1
        else:
            summary.noise_targets += 1

    sorted_targets = sorted(targets, key=lambda t: t.composite_score, reverse=True)
    if sorted_targets:
        summary.top_target = sorted_targets[0].target

    all_recs: list[str] = []
    for t in sorted_targets:
        all_recs.extend(t.recommended_actions)

    return TargetScoringResult(
        targets=sorted_targets,
        top_recommendations=all_recs[:10],
        summary=summary,
    )
