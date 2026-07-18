from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.people_intel")

DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
EMAIL_RE = re.compile(r"^[^@\s]+@([^@\s]+\.[^@\s]+)$")


@dataclass
class BreachRecord:
    breach_name: str
    email: str
    password: str | None
    data_classes: list[str]
    severity: str

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("password", None)
        return d


@dataclass
class Employee:
    name: str | None
    role: str | None
    emails: list[str]
    phone: str | None
    linkedin: str | None
    twitter: str | None
    github: str | None
    sources: list[str]
    breaches: list[BreachRecord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "emails": self.emails,
            "phone": self.phone,
            "linkedin": self.linkedin,
            "twitter": self.twitter,
            "github": self.github,
            "sources": self.sources,
            "breach_count": len(self.breaches),
            "breaches": [b.to_dict() for b in self.breaches],
        }


@dataclass
class BreachContext:
    email: str
    total_breaches: int
    passwords_exposed: bool
    severity: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PeopleIntelResult:
    employees: list[Employee] = field(default_factory=list)
    email_pattern: str | None = None
    email_pattern_confidence: float = 0.0
    total_employees_found: int = 0
    breaches: list[BreachContext] = field(default_factory=list)
    risk_score: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "employees": [e.to_dict() for e in self.employees],
            "email_pattern": self.email_pattern,
            "email_pattern_confidence": self.email_pattern_confidence,
            "total_employees_found": self.total_employees_found,
            "breaches": [b.to_dict() for b in self.breaches],
            "risk_score": self.risk_score,
        }


_COMMON_PATTERNS: list[tuple[re.Pattern[Any], str]] = [
    (re.compile(r"^([a-z]+)\.([a-z]+)@"), "{first}.{last}@{domain}"),
    (re.compile(r"^([a-z])\.([a-z]+)@"), "{first_initial}.{last}@{domain}"),
    (re.compile(r"^([a-z]+)\.([a-z])@"), "{first}.{last_initial}@{domain}"),
    (re.compile(r"^([a-z]+)@"), "{first}@{domain}"),
    (re.compile(r"^([a-z]+)([a-z]+)@"), "{first_initial}{last}@{domain}"),
    (re.compile(r"^([a-z]{2})([a-z]+)@"), "{first_2}{last}@{domain}"),
    (re.compile(r"^([a-z]+)-([a-z]+)@"), "{first}-{last}@{domain}"),
    (re.compile(r"^([a-z]+)_([a-z]+)@"), "{first}_{last}@{domain}"),
]


def infer_email_pattern(emails: list[str]) -> tuple[str | None, float]:
    if not emails:
        return None, 0.0

    local_parts = []
    domain = None
    for e in emails:
        m = EMAIL_RE.match(e)
        if m:
            local_parts.append(e.split("@")[0])
            if domain is None:
                domain = m.group(1)

    if not local_parts:
        return None, 0.0

    if len(local_parts) < 2:
        matched, best_pattern = _match_pattern(local_parts[0])
        if not matched:
            return None, 0.0
        return best_pattern, 0.3

    pattern_votes: dict[str, int] = {}
    for part in local_parts:
        matched, pat = _match_pattern(part)
        if matched:
            pattern_votes[pat] = pattern_votes.get(pat, 0) + 1

    if not pattern_votes:
        return None, 0.0

    best = max(pattern_votes, key=lambda k: pattern_votes[k])
    ratio = pattern_votes[best] / len(local_parts)
    confidence = min(0.95, ratio * (1 - 1 / len(local_parts)))

    return best, confidence


def _match_pattern(local: str) -> tuple[bool, str]:
    for pat, desc in _COMMON_PATTERNS:
        if pat.match(local + "@domain.com"):
            return True, desc
    return False, "unknown"


def _severity_from_breaches(breaches: list[BreachRecord]) -> str:
    if any(b.severity == "critical" for b in breaches):
        return "critical"
    if any(b.severity == "high" for b in breaches):
        return "high"
    if any(b.severity == "medium" for b in breaches):
        return "medium"
    return "low"


def correlate_breaches(employees: list[Employee]) -> list[BreachContext]:
    email_map: dict[str, list[BreachRecord]] = {}
    for emp in employees:
        for email in emp.emails:
            if email not in email_map:
                email_map[email] = []
            email_map[email].extend(emp.breaches)

    contexts = []
    for email, breaches in email_map.items():
        if not breaches:
            continue
        passwords_exposed = any(b.password is not None for b in breaches)
        severity = _severity_from_breaches(breaches)
        contexts.append(BreachContext(
            email=email,
            total_breaches=len(breaches),
            passwords_exposed=passwords_exposed,
            severity=severity,
        ))
    return contexts


def analyse_employees(
    employees: list[Employee],
    domain: str,
) -> PeopleIntelResult:
    if not DOMAIN_RE.match(domain):
        raise ValueError("INVALID_DOMAIN")

    emails = []
    for emp in employees:
        for e in emp.emails:
            if e.endswith(f"@{domain}"):
                emails.append(e)

    pattern, conf = infer_email_pattern(emails)
    if pattern and domain:
        pattern = pattern.replace("{domain}", domain)
    breaches = correlate_breaches(employees)

    risk_score = 0.0
    if breaches:
        severity_weights = {"critical": 1.0, "high": 0.7, "medium": 0.4, "low": 0.2}
        severity_scores = [severity_weights.get(b.severity, 0) for b in breaches]
        breach_factor = min(1.0, sum(severity_scores) / max(1, len(breaches)))
        password_factor = 0.3 if any(b.passwords_exposed for b in breaches) else 0.0
        risk_score = min(1.0, breach_factor * 0.7 + password_factor * 0.3)

    return PeopleIntelResult(
        employees=employees,
        email_pattern=pattern,
        email_pattern_confidence=conf,
        total_employees_found=len(employees),
        breaches=breaches,
        risk_score=risk_score,
    )
