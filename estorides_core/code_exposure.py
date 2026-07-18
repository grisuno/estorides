from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.code_exposure")

MAX_SNIPPET_CHARS = 200

AWS_KEY_RE = re.compile(r"AKIA[0-9A-Z]{16}")
GCP_KEY_RE = re.compile(r"AIza[0-9A-Za-z_-]{35}")
STRIPE_KEY_RE = re.compile(r"(?:sk|pk)_(?:live|test)_[0-9a-zA-Z]{24,}")
GITHUB_TOKEN_RE = re.compile(r"gh[ps]_[0-9a-zA-Z]{36}")
SLACK_TOKEN_RE = re.compile(r"xox[baprs]-[0-9a-zA-Z-]{24,}")
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)PRIVATE KEY-----", re.MULTILINE)
JWT_RE = re.compile(r"eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+")

INTERNAL_URL_RE = re.compile(r"https?://(?:internal|intranet|private|dev|staging|jenkins|jira|confluence|gitlab|grafana|kibana|prometheus|admin|dashboard)[.\-][a-z0-9.-]+", re.I)

CRED_PATTERNS: list[tuple[re.Pattern[Any], str, str]] = [
    (re.compile(r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"](?!your-password|placeholder|example)[^'\"]{4,}['\"]"), "credential", "critical"),
    (re.compile(r"(?i)(?:secret|api[_-]?key|apikey)\s*[:=]\s*['\"](?!YOUR_API_KEY|your-api-key|placeholder)[^'\"]{8,}['\"]"), "api_key", "critical"),
    (re.compile(r"(?i)aws[_-]?(?:access[_-]?key|secret[_-]?access[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]"), "credential", "critical"),
    (re.compile(r"(?i)db[_-]?(?:url|connection|database)[_:=\s][^\"'\s]+"), "config", "high"),
    (re.compile(r"(?i)connection[_:=\s][\"']?[a-z]+://[^\"'\s]+[\"']?"), "config", "high"),
    (re.compile(r"(?i)(?:internal|private)\s*[:=]\s*['\"]?(?:true|yes)['\"]?"), "config", "medium"),
]

CONFIG_FILE_PATTERNS: list[tuple[re.Pattern[Any], str, str]] = [
    (re.compile(r"(?i)\.env"), "config", "critical"),
    (re.compile(r"(?i)credentials\.(?:json|ini|cfg)"), "credential", "critical"),
    (re.compile(r"(?i)config\.(?:json|yaml|yml|xml|ini|cfg|php|py|rb|js|ts)"), "config", "medium"),
    (re.compile(r"(?i)\.aws/config"), "config", "critical"),
    (re.compile(r"(?i)\.(?:git-credentials|netrc|ssh/.*)"), "credential", "critical"),
    (re.compile(r"(?i)docker-compose\.yml"), "config", "low"),
    (re.compile(r"(?i)terraform\.(?:tf|tfvars)"), "config", "high"),
    (re.compile(r"(?i)kubernetes.*\.(?:yaml|yml)"), "config", "high"),
    (re.compile(r"(?i)helmfile\.yaml"), "config", "high"),
]

PLACEHOLDER_RE = re.compile(r"(?i)(?:your-|example|placeholder|test_|YOUR_)")


@dataclass
class CodeFinding:
    source: str
    type: str
    file_path: str
    repository: str
    snippet: str
    matched_pattern: str
    severity: str
    verified: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SeveritySummary:
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    info: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CodeExposureResult:
    findings: list[CodeFinding] = field(default_factory=list)
    total_findings: int = 0
    severity_summary: SeveritySummary = field(default_factory=SeveritySummary)
    scan_timestamp: str = ""
    rate_limited: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "findings": [f.to_dict() for f in self.findings],
            "total_findings": self.total_findings,
            "severity_summary": self.severity_summary.to_dict(),
            "scan_timestamp": self.scan_timestamp,
            "rate_limited": self.rate_limited,
        }


def validate_aws_key(key: str) -> bool:
    return bool(AWS_KEY_RE.fullmatch(key.strip()))


def _is_placeholder(text: str) -> bool:
    return bool(PLACEHOLDER_RE.search(text))


def classify_finding(content: str, source: str, file_path: str) -> CodeFinding:
    internal_url_match = INTERNAL_URL_RE.search(content)
    if internal_url_match:
        return CodeFinding(
            source=source, type="internal_url",
            file_path=file_path, repository="",
            snippet=content[:MAX_SNIPPET_CHARS],
            matched_pattern="INTERNAL_URL",
            severity="high", verified=False,
        )

    if PRIVATE_KEY_RE.search(content):
        return CodeFinding(
            source=source, type="credential",
            file_path=file_path, repository="",
            snippet=content[:MAX_SNIPPET_CHARS],
            matched_pattern="PRIVATE_KEY",
            severity="critical", verified=True,
        )

    if AWS_KEY_RE.search(content):
        return CodeFinding(
            source=source, type="credential",
            file_path=file_path, repository="",
            snippet=content[:MAX_SNIPPET_CHARS],
            matched_pattern="AWS_ACCESS_KEY",
            severity="critical", verified=True,
        )

    if GCP_KEY_RE.search(content):
        return CodeFinding(
            source=source, type="api_key",
            file_path=file_path, repository="",
            snippet=content[:MAX_SNIPPET_CHARS],
            matched_pattern="GCP_API_KEY",
            severity="critical", verified=True,
        )

    if STRIPE_KEY_RE.search(content) or SLACK_TOKEN_RE.search(content) or GITHUB_TOKEN_RE.search(content):
        return CodeFinding(
            source=source, type="credential",
            file_path=file_path, repository="",
            snippet=content[:MAX_SNIPPET_CHARS],
            matched_pattern="API_TOKEN",
            severity="critical", verified=True,
        )

    simple_pass = re.search(r"(?i)(?:password|passwd|pwd|secret|api[_-]?key|token)\s*[:=]\s*['\"][^'\"]{2,}['\"]", content)
    if simple_pass and _is_placeholder(content):
        return CodeFinding(
            source=source, type="credential",
            file_path=file_path, repository="",
            snippet=content[:MAX_SNIPPET_CHARS],
            matched_pattern="CREDENTIAL_PLACEHOLDER",
            severity="info", verified=False,
        )

    for pat, ftype, sev in CRED_PATTERNS:
        m = pat.search(content)
        if m:
            matched_text = m.group(0)
            if _is_placeholder(matched_text):
                sev = "info"
            return CodeFinding(
                source=source, type=ftype,
                file_path=file_path, repository="",
                snippet=content[:MAX_SNIPPET_CHARS],
                matched_pattern=ftype.upper(),
                severity=sev, verified=sev == "critical",
            )

    for pat, ftype, sev in CONFIG_FILE_PATTERNS:
        if pat.search(file_path):
            return CodeFinding(
                source=source, type=ftype,
                file_path=file_path, repository="",
                snippet=content[:MAX_SNIPPET_CHARS],
                matched_pattern=f"FILE:{file_path}",
                severity=sev, verified=False,
            )

    return CodeFinding(
        source=source, type="other",
        file_path=file_path, repository="",
        snippet=content[:MAX_SNIPPET_CHARS],
        matched_pattern="UNKNOWN",
        severity="info", verified=False,
    )


def analyse_findings(
    findings: list[CodeFinding],
    rate_limited: bool = False,
) -> CodeExposureResult:
    summary = SeveritySummary()
    for f in findings:
        sev = f.severity.lower()
        if sev == "critical":
            summary.critical += 1
        elif sev == "high":
            summary.high += 1
        elif sev == "medium":
            summary.medium += 1
        elif sev == "low":
            summary.low += 1
        else:
            summary.info += 1

    return CodeExposureResult(
        findings=findings,
        total_findings=len(findings),
        severity_summary=summary,
        rate_limited=rate_limited,
    )
