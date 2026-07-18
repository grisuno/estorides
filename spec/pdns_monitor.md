# pdns_monitor — Passive DNS History & Certificate Monitoring

## Purpose
Provide historical DNS resolution data and ongoing certificate transparency
monitoring for subdomain enumeration. Tracks IP changes over time, discovers
subdomains not currently in DNS, and monitors for new certificate issuance
that may reveal new infrastructure.

## Inputs
- `domain: str` — target domain
- `hours_back: int` — how far back to check (default 168 = 7 days)
- `monitor: bool` — whether to start continuous monitoring (default False)

## Outputs
```
PDNSResult {
  subdomains: List[HistoricalSubdomain]
  ip_history: Dict[str, List[IPRecord]]    # domain → list of historical IPs
  new_certs: List[CertRecord]              # recently issued certificates
  total_subdomains: int
  total_new_certs: int
}

HistoricalSubdomain {
  fqdn: str
  first_seen: str                          # ISO timestamp
  last_seen: str
  resolution_count: int
  resolved_ips: List[str]
  sources: List[str]
  is_active: bool                          # currently resolves
}

IPRecord {
  ip: str
  first_seen: str
  last_seen: str
  asn: Optional[int]
  asn_description: Optional[str]
  source: str
}

CertRecord {
  serial: str
  subject: str
  issuer: str
  not_before: str
  not_after: str
  dns_names: List[str]
  is_wildcard: bool
  source: str                              # ct_log | certspotter | crt_sh
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| No PDNS data available | `NO_PDNS_DATA` | Empty history, subdomains from CT only |
| CertSpotter rate limit | `RATE_LIMITED` | Fall back to crt.sh |
| Invalid domain | `INVALID_DOMAIN` | Return error |
| CT log unavailable | `CT_UNAVAILABLE` | Return DNS-only results |

## Security guarantees
- All queries are read-only, public API calls
- No DNS zone transfers (AXFR)
- Rate limits respected per log/API
- Monitor mode uses polling, not webhooks (no callback URL exposed)

## Out of scope
- Active DNS brute-force
- DNS zone transfer testing
- DNSSEC validation
- Reverse DNS scan of IP ranges

## BDD Scenarios

### S1 [Happy path] Historical subdomain from CT log
Given a domain "example.com" with crt.sh returning 3 subdomains (www, api, mail)
When pdns_monitor queries CT logs
Then it returns 3 HistoricalSubdomain entries
and is_active is True for currently-resolving subdomains
and is_active is False for non-resolving

### S2 [Happy path] IP history from passive DNS
Given a domain that changed IP from 1.1.1.1 to 2.2.2.2 over 30 days
When pdns_monitor retrieves passive DNS history
Then ip_history contains both IPs
and first_seen/last_seen timestamps for each

### S3 [Edge] No historical data available
Given a fresh domain with no CT logs or PDNS history
When pdns_monitor runs
Then total_subdomains = 0
and total_new_certs = 0

### S4 [Happy path] New certificate detected
Given a domain with a recently issued cert (24h) containing 5 SANs
When pdns_monitor checks for new certs
Then new_certs contains the cert
and dns_names includes the 5 SAN entries

### S5 [Security] No AXFR attempted
Given any domain
When pdns_monitor gathers DNS data
Then it never sends an AXFR query
and uses only passive DNS sources (CT logs, PDNS APIs, DNS resolution)

### S6 [Happy path] Wildcard cert detection
Given a certificate with CN "*.example.com"
When pdns_monitor processes the certificate
Then is_wildcard is True
and subject is "*.example.com"

### S7 [Edge] CT log fallback on rate limit
Given CertSpotter returns 429 (rate limit exceeded)
When pdns_monitor queries CT logs
Then it falls back to crt.sh
and subdomains still contain results

### S8 [Security] Monitor mode polling interval
Given pdns_monitor in monitor mode
When the monitoring loop runs
Then it polls at intervals no shorter than 3600 seconds (1 hour)
to avoid aggressive querying of CT logs
