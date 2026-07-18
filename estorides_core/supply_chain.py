from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.supply_chain")

MX_PROVIDER_MAP: dict[re.Pattern[Any], str] = {
    re.compile(r"aspmx\.l\.google\.com", re.I): "Google Workspace",
    re.compile(r"googlemail\.com", re.I): "Google Workspace",
    re.compile(r"mail\.protection\.outlook\.com", re.I): "Microsoft 365",
    re.compile(r"mail\.messaging\.microsoft\.com", re.I): "Microsoft 365",
    re.compile(r"mx\.(?:1|2)\.icloud\.com", re.I): "iCloud Mail",
    re.compile(r"mx\.zoho\.com", re.I): "Zoho Mail",
    re.compile(r"mx\.sendgrid\.net", re.I): "SendGrid",
    re.compile(r"spf\.mx\.cloudflare\.net", re.I): "Cloudflare Email",
    re.compile(r"mailgun\.org", re.I): "Mailgun",
    re.compile(r"mx\.(?:1|2)\.(?:hosted|server)\.(?:spamfiltering|mxes)\.com", re.I): "Mimecast",
    re.compile(r"eu\.(?:protect|mail)\.proofpoint\.com", re.I): "Proofpoint",
}

NS_PROVIDER_MAP: dict[re.Pattern[Any], str] = {
    re.compile(r"ns\d+\.cloudflare\.com", re.I): "Cloudflare DNS",
    re.compile(r"ns\d+\.awsdns", re.I): "AWS Route53",
    re.compile(r"dns\.google\.com", re.I): "Google Cloud DNS",
    re.compile(r"ns\d+\.azure-dns", re.I): "Azure DNS",
    re.compile(r"ns\d+\.namecheap\.com", re.I): "Namecheap",
    re.compile(r"dns\d+\.registrar-servers\.com", re.I): "Namecheap",
    re.compile(r"ns\d+\.godaddy\.com", re.I): "GoDaddy",
    re.compile(r"pdns\d+\.ultradns", re.I): "UltraDNS",
    re.compile(r"ns\d+\.he\.net", re.I): "Hurricane Electric",
    re.compile(r"dns\d+\.digitalocean\.com", re.I): "DigitalOcean",
    re.compile(r"ns\d+\.linode\.com", re.I): "Linode",
    re.compile(r"ns\d+\.ovh\.net", re.I): "OVH",
}

CDN_PATTERNS: list[tuple[re.Pattern[Any], str]] = [
    (re.compile(r"\.cloudflare\.net$", re.I), "Cloudflare"),
    (re.compile(r"\.cloudfront\.net$", re.I), "Amazon CloudFront"),
    (re.compile(r"\.akamai(?:d|edge)?\.net$", re.I), "Akamai"),
    (re.compile(r"\.fastly\.net$", re.I), "Fastly"),
    (re.compile(r"\.stackpathcdn\.com$", re.I), "StackPath"),
    (re.compile(r"\.cdn\.azure\.(?:us|cn|de)?$", re.I), "Azure CDN"),
    (re.compile(r"\.cdn\.edgecdn\.net$", re.I), "EdgeCDN"),
    (re.compile(r"\.kinstacdn\.com$", re.I), "Kinsta"),
    (re.compile(r"\.sucuri\.net$", re.I), "Sucuri"),
    (re.compile(r"\.incapsula\.com$", re.I), "Incapsula"),
]


@dataclass
class ThirdParty:
    name: str
    relationship_type: str
    domain: str | None
    evidence: list[str]
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SharedInfra:
    asn: int
    description: str
    other_domains: list[str]
    total_domains_on_infra: int
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Relationship:
    source: str
    target: str
    type: str
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SupplyChainResult:
    third_parties: list[ThirdParty] = field(default_factory=list)
    subsidiaries: list[str] = field(default_factory=list)
    shared_infrastructure: list[SharedInfra] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    total_third_parties: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "third_parties": [tp.to_dict() for tp in self.third_parties],
            "subsidiaries": self.subsidiaries,
            "shared_infrastructure": [s.to_dict() for s in self.shared_infrastructure],
            "relationships": [r.to_dict() for r in self.relationships],
            "total_third_parties": self.total_third_parties,
        }


def detect_mx_provider(mx_records: list[str]) -> str | None:
    for mx in mx_records:
        for pat, provider in MX_PROVIDER_MAP.items():
            if pat.search(mx):
                return provider
    return None


def detect_ns_provider(ns_records: list[str]) -> str | None:
    for ns in ns_records:
        for pat, provider in NS_PROVIDER_MAP.items():
            if pat.search(ns):
                return provider
    return None


def detect_cdn(cname: str) -> str | None:
    for pat, provider in CDN_PATTERNS:
        if pat.search(cname):
            return provider
    return None


def analyse_third_parties(
    third_parties: list[ThirdParty],
    subsidiaries: list[str] | None = None,
) -> SupplyChainResult:
    return SupplyChainResult(
        third_parties=third_parties,
        subsidiaries=subsidiaries or [],
        total_third_parties=len(third_parties),
    )


def detect_shared_infrastructure(asn: int) -> SharedInfra | None:
    return None
