from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.pdns_monitor")

MONITOR_POLL_INTERVAL_S = 3600


@dataclass
class HistoricalSubdomain:
    fqdn: str
    first_seen: str
    last_seen: str
    resolution_count: int
    resolved_ips: list[str]
    sources: list[str]
    is_active: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class IPRecord:
    ip: str
    first_seen: str
    last_seen: str
    asn: int | None
    asn_description: str | None
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CertRecord:
    serial: str
    subject: str
    issuer: str
    not_before: str
    not_after: str
    dns_names: list[str]
    is_wildcard: bool
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PDNSResult:
    subdomains: list[HistoricalSubdomain] = field(default_factory=list)
    ip_history: dict[str, list[IPRecord]] = field(default_factory=dict)
    new_certs: list[CertRecord] = field(default_factory=list)
    total_subdomains: int = 0
    total_new_certs: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "subdomains": [s.to_dict() for s in self.subdomains],
            "ip_history": {k: [r.to_dict() for r in v] for k, v in self.ip_history.items()},
            "new_certs": [c.to_dict() for c in self.new_certs],
            "total_subdomains": self.total_subdomains,
            "total_new_certs": self.total_new_certs,
        }


def classify_subdomain_status(fqdn: str, resolved_ips: list[str]) -> bool:
    return len(resolved_ips) > 0


def extract_sans_from_cert(cert: CertRecord) -> list[str]:
    return cert.dns_names


def analyse_pdns_data(
    subdomains: list[HistoricalSubdomain],
    ip_history: dict[str, list[IPRecord]],
    new_certs: list[CertRecord],
) -> PDNSResult:
    return PDNSResult(
        subdomains=subdomains,
        ip_history=ip_history,
        new_certs=new_certs,
        total_subdomains=len(subdomains),
        total_new_certs=len(new_certs),
    )
