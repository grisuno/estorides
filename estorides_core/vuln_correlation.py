from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.vuln_correlation")

VERSION_RE = re.compile(r"(\d+(?:\.\d+)*)")


@dataclass
class DefaultCred:
    username: str
    password: str
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VulnEntry:
    cve_id: str
    cvss_score: float
    severity: str
    affected_tech: str
    affected_version: str
    exploit_available: bool
    exploit_type: str
    exploit_db_id: int | None
    metasploit_module: str | None
    default_credentials: DefaultCred | None
    description: str
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VulnCorrelationResult:
    vulnerabilities: list[VulnEntry] = field(default_factory=list)
    total_vulnerabilities: int = 0
    critical_count: int = 0
    high_count: int = 0
    exploit_available_count: int = 0
    attack_readiness_score: float = 0.0
    most_critical: VulnEntry | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "vulnerabilities": [v.to_dict() for v in self.vulnerabilities],
            "total_vulnerabilities": self.total_vulnerabilities,
            "critical_count": self.critical_count,
            "high_count": self.high_count,
            "exploit_available_count": self.exploit_available_count,
            "attack_readiness_score": self.attack_readiness_score,
            "most_critical": self.most_critical.to_dict() if self.most_critical else None,
        }


VULN_DB: dict[str, list[dict[str, Any]]] = {
    "nginx": [
        {"cve": "CVE-2021-23017", "cvss": 7.5, "severity": "high", "version_start": "0", "version_end": "1.21.0", "exploit": "edb", "edb_id": 50065, "msf": None, "desc": "DNS resolver uAF in nginx"},
        {"cve": "CVE-2021-3618", "cvss": 5.3, "severity": "medium", "version_start": "0", "version_end": "1.21.1", "exploit": "none", "edb_id": None, "msf": None, "desc": "ALPACA — TLS protocol confusion"},
        {"cve": "CVE-2024-24989", "cvss": 6.5, "severity": "medium", "version_start": "0", "version_end": "1.24.0", "exploit": "none", "edb_id": None, "msf": None, "desc": "HTTP/2 memory leak"},
    ],
    "Apache HTTPD": [
        {"cve": "CVE-2021-41773", "cvss": 7.5, "severity": "high", "version_start": "2.4.49", "version_end": "2.4.50", "exploit": "edb", "edb_id": 50383, "msf": "exploit/multi/http/apache_normalize_path_rce", "desc": "Path traversal + RCE in Apache 2.4.49"},
        {"cve": "CVE-2021-42013", "cvss": 9.8, "severity": "critical", "version_start": "2.4.49", "version_end": "2.4.51", "exploit": "edb", "edb_id": 50406, "msf": "exploit/multi/http/apache_normalize_path_rce", "desc": "RCE via path traversal in Apache 2.4.50"},
        {"cve": "CVE-2023-25690", "cvss": 9.8, "severity": "critical", "version_start": "2.4.0", "version_end": "2.4.56", "exploit": "none", "edb_id": None, "msf": None, "desc": "HTTP request splitting"},
    ],
    "PHP": [
        {"cve": "CVE-2024-4577", "cvss": 9.8, "severity": "critical", "version_start": "5.0.0", "version_end": "8.1.29", "exploit": "edb", "edb_id": 52038, "msf": None, "desc": "Windows CGI RCE"},
        {"cve": "CVE-2022-31626", "cvss": 7.5, "severity": "high", "version_start": "7.0.0", "version_end": "8.1.12", "exploit": "none", "edb_id": None, "msf": None, "desc": "PHAR deserialization"},
    ],
    "WordPress": [
        {"cve": "CVE-2024-4430", "cvss": 8.8, "severity": "high", "version_start": "0", "version_end": "6.5.5", "exploit": "none", "edb_id": None, "msf": None, "desc": "XSS in WP core"},
        {"cve": "CVE-2024-4400", "cvss": 6.4, "severity": "medium", "version_start": "0", "version_end": "6.6.2", "exploit": "none", "edb_id": None, "msf": None, "desc": "Stored XSS in HTML API"},
    ],
    "Jenkins": [
        {"cve": "CVE-2024-23897", "cvss": 9.8, "severity": "critical", "version_start": "0", "version_end": "2.442", "exploit": "edb", "edb_id": 51997, "msf": "exploit/multi/http/jenkins_cli_arbitrary_read", "desc": "Arbitrary file read via CLI"},
        {"cve": "CVE-2024-43044", "cvss": 9.8, "severity": "critical", "version_start": "0", "version_end": "2.476", "exploit": "none", "edb_id": None, "msf": None, "desc": "Remoting RCE"},
    ],
    "Apache Struts": [
        {"cve": "CVE-2017-5638", "cvss": 10.0, "severity": "critical", "version_start": "2.3.5", "version_end": "2.3.31", "exploit": "edb", "edb_id": 41570, "msf": "exploit/multi/http/struts2_content_type_ognl", "desc": "OGNL RCE via Content-Type"},
        {"cve": "CVE-2017-9805", "cvss": 9.8, "severity": "critical", "version_start": "2.0.0", "version_end": "2.5.99", "exploit": "edb", "edb_id": 42673, "msf": "exploit/multi/http/struts2_rest_xstream", "desc": "REST plugin RCE via XStream"},
        {"cve": "CVE-2018-11776", "cvss": 9.8, "severity": "critical", "version_start": "2.3.0", "version_end": "2.3.35", "exploit": "edb", "edb_id": 45262, "msf": "exploit/multi/http/struts2_namespace_ognl", "desc": "OGNL RCE via namespace"},
        {"cve": "CVE-2023-50164", "cvss": 9.8, "severity": "critical", "version_start": "2.0.0", "version_end": "2.5.33", "exploit": "edb", "edb_id": 52023, "msf": None, "desc": "File upload RCE via multipart"},
        {"cve": "CVE-2024-53677", "cvss": 9.8, "severity": "critical", "version_start": "2.0.0", "version_end": "2.6.0", "exploit": "none", "edb_id": None, "msf": None, "desc": "File upload logic flaw RCE"},
    ],
    "Drupal": [
        {"cve": "CVE-2019-6340", "cvss": 8.1, "severity": "high", "version_start": "8.0.0", "version_end": "8.6.9", "exploit": "edb", "edb_id": 46459, "msf": None, "desc": "RESTful RCE"},
        {"cve": "CVE-2018-7600", "cvss": 9.8, "severity": "critical", "version_start": "7.0.0", "version_end": "7.58", "exploit": "edb", "edb_id": 44449, "msf": "exploit/multi/http/drupal_drupageddon", "desc": "Drupalgeddon2 RCE"},
    ],
    "IIS": [
        {"cve": "CVE-2021-31166", "cvss": 9.8, "severity": "critical", "version_start": "10.0", "version_end": "10.0.20348", "exploit": "none", "edb_id": None, "msf": None, "desc": "HTTP.sys RCE"},
    ],
}

DEFAULT_CREDS: dict[str, list[DefaultCred]] = {
    "Jenkins": [
        DefaultCred("admin", "admin", "Jenkins default"),
    ],
    "Tomcat": [
        DefaultCred("admin", "admin", "Tomcat default"),
        DefaultCred("tomcat", "tomcat", "Tomcat default"),
    ],
    "MySQL": [
        DefaultCred("root", "", "MySQL default (no password)"),
    ],
    "PostgreSQL": [
        DefaultCred("postgres", "postgres", "PostgreSQL default"),
    ],
    "MongoDB": [
        DefaultCred("admin", "admin", "MongoDB default"),
    ],
    "Redis": [
        DefaultCred("default", "", "Redis default (no password)"),
    ],
    "Elasticsearch": [
        DefaultCred("elastic", "changeme", "Elasticsearch default"),
    ],
    "Kibana": [
        DefaultCred("kibana", "kibana", "Kibana default"),
    ],
    "Grafana": [
        DefaultCred("admin", "admin", "Grafana default"),
    ],
    "RabbitMQ": [
        DefaultCred("guest", "guest", "RabbitMQ default"),
    ],
    "Jupyter": [
        DefaultCred("jupyter", "jupyter", "Jupyter default"),
    ],
}


def _parsed_version(version: str | None) -> tuple[int, ...] | None:
    if not version:
        return None
    m = VERSION_RE.match(version)
    if not m:
        return None
    try:
        return tuple(int(x) for x in m.group(1).split("."))
    except ValueError:
        return None


def _version_in_range(version: tuple[int, ...], v_start: str, v_end: str) -> bool:
    try:
        start_parts = tuple(int(x) for x in v_start.split("."))
    except ValueError:
        start_parts = (0,)
    try:
        end_parts = tuple(int(x) for x in v_end.split("."))
    except ValueError:
        end_parts = (999,)

    start_parts = start_parts + (0,) * (len(version) - len(start_parts))
    end_parts = end_parts + (99,) * (len(version) - len(end_parts))

    return start_parts <= version <= end_parts


def lookup_cve_for_tech(tech_name: str, version: str | None) -> list[VulnEntry]:
    results: list[VulnEntry] = []
    vulns = VULN_DB.get(tech_name, [])
    parsed = _parsed_version(version)

    for v in vulns:
        if parsed and _version_in_range(parsed, v["version_start"], v["version_end"]):
            confidence = 0.9
        elif parsed:
            continue
        else:
            confidence = 0.3

        default_creds = DEFAULT_CREDS.get(tech_name)

        results.append(VulnEntry(
            cve_id=v["cve"],
            cvss_score=v["cvss"],
            severity=v["severity"],
            affected_tech=tech_name,
            affected_version=version or "unknown",
            exploit_available=v["exploit"] != "none",
            exploit_type=v["exploit"],
            exploit_db_id=v["edb_id"],
            metasploit_module=v["msf"],
            default_credentials=default_creds[0] if default_creds and v["cvss"] >= 9.0 else None,
            description=v["desc"],
            confidence=confidence,
        ))

    return results


def correlate_technologies(technologies: list[dict[str, Any]]) -> VulnCorrelationResult:
    all_vulns: list[VulnEntry] = []

    for tech in technologies:
        name = tech.get("name", "")
        version = tech.get("version")
        cves = lookup_cve_for_tech(name, version)
        all_vulns.extend(cves)

    critical = sum(1 for v in all_vulns if v.severity == "critical")
    high = sum(1 for v in all_vulns if v.severity == "high")
    exploit_available = sum(1 for v in all_vulns if v.exploit_available)
    most_critical = max(all_vulns, key=lambda v: v.cvss_score) if all_vulns else None
    readiness = compute_attack_readiness(all_vulns)

    return VulnCorrelationResult(
        vulnerabilities=all_vulns,
        total_vulnerabilities=len(all_vulns),
        critical_count=critical,
        high_count=high,
        exploit_available_count=exploit_available,
        attack_readiness_score=readiness,
        most_critical=most_critical,
    )


def compute_attack_readiness(vulnerabilities: list[VulnEntry]) -> float:
    if not vulnerabilities:
        return 0.0

    exploit_factor = sum(1 for v in vulnerabilities if v.exploit_available) / len(vulnerabilities)
    cvss_factor = sum(v.cvss_score for v in vulnerabilities) / (len(vulnerabilities) * 10.0)
    critical_factor = sum(1 for v in vulnerabilities if v.severity == "critical") / len(vulnerabilities)

    score = exploit_factor * 0.5 + cvss_factor * 0.3 + critical_factor * 0.2
    return round(min(1.0, max(0.0, score)), 4)
