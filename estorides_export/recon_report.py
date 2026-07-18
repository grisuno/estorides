from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

log = logging.getLogger("estorides.recon_report")

REDACT_PATTERNS: list[re.Pattern[Any]] = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    re.compile(r"(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,}"),
    re.compile(r"gh[ps]_[0-9a-zA-Z]{36}"),
    re.compile(r"xox[baprs]-[0-9a-zA-Z-]{24,}"),
    re.compile(r"(?i)(?:password|secret|token|key|credential)\s*[:=]\s*['\"]?[^'\"\s;,\)]{4,}",),
    re.compile(r"(?i)-----BEGIN (?:RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----"),
]


@dataclass
class ReportMetadata:
    operator: str = ""
    engagement: str = ""
    date: str = ""
    classification: str = "TLP:AMBER"

    def __post_init__(self) -> None:
        valid = {"TLP:WHITE", "TLP:GREEN", "TLP:AMBER", "TLP:RED"}
        if self.classification not in valid:
            log.warning("Invalid TLP %r, defaulting to TLP:AMBER", self.classification)
            object.__setattr__(self, "classification", "TLP:AMBER")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReportSection:
    title: str
    level: int
    content: str
    severity: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReportResult:
    markdown: str = ""
    sections: list[ReportSection] = field(default_factory=list)
    word_count: int = 0
    generated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def redact_sensitive(text: str) -> str:
    for pat in REDACT_PATTERNS:
        text = pat.sub("[REDACTED]", text)
    return text


def build_subdomain_tree(subdomains: list[str]) -> str:
    if not subdomains:
        return ""
    lines: list[str] = []
    base = ""
    for s in sorted(subdomains):
        parts = s.split(".")
        if len(parts) < 2:
            lines.append(f"  {s}")
            continue
        tld_domain = ".".join(parts[-2:]) if len(parts) >= 2 else s
        if base != tld_domain:
            if base:
                lines.append("")
            base = tld_domain
            lines.append(f"  {base}")

        sub_parts = parts[:-2]
        if sub_parts:
            prefix = "    " + " → ".join(reversed(sub_parts))
            lines.append(prefix)

    return "\n".join(lines)


def build_executive_summary(
    critical_findings: list[str],
    total_targets: int,
    domain: str,
) -> str:
    lines = [
        "## Executive Summary",
        "",
        f"**Target:** {domain}",
        f"**Total targets analysed:** {total_targets}",
        "**Classification:** TLP:AMBER",
        "",
    ]
    if critical_findings:
        lines.append("### Critical Findings")
        for f in critical_findings:
            lines.append(f"- **{f}**")
        lines.append("")

    return "\n".join(lines)


def generate_report(
    query: str,
    target_scoring: dict[str, Any],
    metadata: ReportMetadata,
) -> ReportResult:
    if isinstance(metadata, dict):
        metadata = ReportMetadata(**metadata)

    sections: list[ReportSection] = []
    markdown_parts: list[str] = []

    header = [
        f"# Reconnaissance Report — {query}",
        "",
        f"**Classification:** {metadata.classification}",
        f"**Operator:** {metadata.operator}",
        f"**Engagement:** {metadata.engagement}",
        f"**Date:** {metadata.date}",
        "",
        "---",
        "",
    ]
    markdown_parts.extend(header)
    sections.append(ReportSection("Report Header", 1, "\n".join(header)))

    critical_findings = target_scoring.get("critical_findings", []) if isinstance(target_scoring, dict) else []
    total_targets = 0
    if isinstance(target_scoring, dict):
        summary = target_scoring.get("summary", {})
        if isinstance(summary, dict):
            total_targets = summary.get("total_targets", 0)
        elif hasattr(summary, "total_targets"):
            total_targets = summary.total_targets

    exec_summary = build_executive_summary(critical_findings, total_targets, query)
    markdown_parts.append(exec_summary)
    sections.append(ReportSection("Executive Summary", 2, exec_summary))

    if not critical_findings and total_targets == 0:
        no_findings = [
            "## Attack Surface Analysis",
            "",
            "No significant findings discovered during this reconnaissance phase.",
            "",
            "The target does not appear to have any exposed cloud assets, vulnerable",
            "technologies, employee credential breaches, or code exposures within",
            "the scope of passive reconnaissance techniques employed.",
            "",
            "**Recommendation:** Consider expanding the scope to include active",
            "reconnaissance techniques or widen the target definition.",
            "",
        ]
        markdown_parts.extend(no_findings)
        sections.append(ReportSection("Attack Surface Analysis", 2, "\n".join(no_findings)))

    summary_section = [
        "## Summary",
        "",
        f"- **Total findings:** {len(critical_findings)} critical, "
        f"{total_targets} targets analysed",
        f"- **Generated:** {datetime.now(timezone.utc).isoformat()}",
        "- **Tool:** Estorides Passive Reconnaissance Suite",
        "",
    ]
    markdown_parts.extend(summary_section)
    sections.append(ReportSection("Summary", 2, "\n".join(summary_section)))

    full = "\n".join(markdown_parts)
    word_count = len(full.split())

    return ReportResult(
        markdown=full,
        sections=sections,
        word_count=word_count,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
