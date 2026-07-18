# supply_chain — Supply Chain & Third-Party Discovery

## Purpose
Identify third-party vendors, SaaS providers, hosting partners, and
organisational relationships (subsidiaries, acquisitions, shared hosting)
that extend the attack surface beyond the target's own infrastructure.
Maps relationships through DNS, ASN, SSL certificates, and corporate data.

## Inputs
- `domain: str` — target domain
- `org_name: Optional[str]` — organisation name
- `depth: int` — relationship depth (1-3, default 1)

## Outputs
```
SupplyChainResult {
  third_parties: List[ThirdParty]
  subsidiaries: List[str]
  shared_infrastructure: List[SharedInfra]
  relationships: List[Relationship]
  total_third_parties: int
}

ThirdParty {
  name: str
  relationship_type: str      # hosting | saas | analytics | cdn | email_provider | ssl_issuer | dns_provider | registrar
  domain: Optional[str]
  evidence: List[str]         # e.g. "MX points to google.com", "nameserver: ns1.cloudflare.com"
  confidence: float
}

SharedInfra {
  asn: int
  description: str
  other_domains: List[str]    # sample of other domains on same ASN/IP
  total_domains_on_infra: int  # approximate count
  confidence: float
}

Relationship {
  source: str
  target: str
  type: str                   # subsidiary | acquired_by | parent | shared_hosting | shared_cert
  confidence: float
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| No third parties found | `NO_THIRD_PARTIES` | Empty lists |
| Deep search (depth > 3) | `DEPTH_EXCEEDED` | Clamp to 3, proceed |
| Corporate data unavailable | `NO_CORPORATE_DATA` | Subsidiaries empty, other relationships still computed |
| ASN data unavailable | `NO_ASN_DATA` | SharedInfra empty |

## Security guarantees
- All data from public sources (DNS, WHOIS, CT logs, ASN registries)
- No crawling of third-party sites
- No vendor breach scanning
- Rate limits respected per data source

## Out of scope
- Software bill of materials (SBOM) analysis
- Vendor security rating scoring
- Active scanning of third-party infrastructure
- Dark web vendor intelligence

## BDD Scenarios

### S1 [Happy path] CDN provider detected from DNS
Given a domain with CNAME to "example.com.cdn.cloudflare.net"
When supply_chain is run
Then it returns a CDN third-party "Cloudflare"
with confidence >= 0.9
and evidence contains the CNAME record

### S2 [Happy path] Email provider from MX records
Given a domain with MX records pointing to "aspmx.l.google.com"
When supply_chain analyses MX records
Then it returns "Google Workspace" as email_provider
with confidence >= 0.9

### S3 [Edge] No third-party services detected
Given a domain with self-hosted everything (no external MX, NS, analytics)
When supply_chain is run
Then third_parties list is empty
and total_third_parties = 0

### S4 [Happy path] Shared ASN discovery
Given a target domain resolving to 1.2.3.4 in ASN 12345 which hosts 500 other domains
When supply_chain analyses shared infrastructure
Then it finds other_domains on the same ASN
and confidence reflects the ASN relationship

### S5 [Security] No outbound scanning of third parties
Given a discovered third-party domain
When supply_chain processes it
Then it does not make any HTTP requests to that domain
(only uses pre-existing DNS/WHOIS/ASN data)

### S6 [Happy path] Subsidiary from corporate data
Given an org "Acme Corp" with a subsidiary "Acme Labs"
When supply_chain looks up corporate relationships
Then relationship[s] contains an entry from "Acme Corp" to "Acme Labs"
with type "subsidiary"

### S7 [Edge] SSL certificate shared issuer
Given a target and another domain both using "Let's Encrypt" issuer
When supply_chain checks SSL relationships
Then it does NOT flag Let's Encrypt as a shared trust relationship (too common)
and confidence for shared_cert is only raised for niche issuers

### S8 [Happy path] Registrar detected from RDAP
Given a domain registered through "GoDaddy"
When supply_chain analyses RDAP data
Then it returns "GoDaddy" as registrar
with relationship_type "registrar"
