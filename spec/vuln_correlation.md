# vuln_correlation — Vulnerability Correlation

## Purpose
Correlate detected technology stacks with known vulnerabilities, exploits,
and default credentials. Given a list of technologies with versions, return
relevant CVEs, Exploit-DB entries, Metasploit modules, and default credentials
to prioritise attack vectors.

## Inputs
- `technologies: List[Tech]` — from tech_fingerprint
- `enrich_from_nvd: bool` — whether to query NVD API (default True)

## Outputs
```
VulnCorrelationResult {
  vulnerabilities: List[VulnEntry]
  total_vulnerabilities: int
  critical_count: int
  high_count: int
  exploit_available_count: int
  attack_readiness_score: float       # 0-1, higher = easier to exploit
  most_critical: Optional[VulnEntry]
}

VulnEntry {
  cve_id: str
  cvss_score: float
  severity: str                       # critical | high | medium | low | none
  affected_tech: str
  affected_version: str
  exploit_available: bool
  exploit_type: str                   # metasploit | edb | public_poC | none
  exploit_db_id: Optional[int]
  metasploit_module: Optional[str]
  default_credentials: Optional[DefaultCred]
  description: str
  confidence: float
}

DefaultCred {
  username: str
  password: str
  source: str                         # where the default cred was documented
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| No technologies provided | `NO_INPUT` | Empty results |
| NVD API unavailable | `NVD_UNAVAILABLE` | Use embedded local lookup table only |
| Version string unparseable | `VERSION_PARSE_ERR` | Match without version, lower confidence |
| Unknown technology | `UNKNOWN_TECH` | Skip silently |

## Security guarantees
- No active exploitation of discovered vulnerabilities
- All NVD queries are read-only API calls
- Default credentials list is read-only, never modified
- CVE data is cached locally for 24h

## Out of scope
- Active vulnerability scanning
- Metasploit integration (module listing only)
- Exploit execution
- Custom exploit development

## BDD Scenarios

### S1 [Happy path] CVE match for known version
Given a technology "nginx" with version "1.18.0"
When vuln_correlation is run
Then it returns CVE entries (e.g. CVE-2021-23017, CVE-2021-3618)
and cvss_score > 0 for matched entries

### S2 [Happy path] Metasploit module available
Given a technology "Apache Struts" with version "2.5.12"
When vuln_correlation is run
Then at least one vulnerability has exploit_type "metasploit"
and metasploit_module is not None

### S3 [Edge] Unknown technology
Given a technology "SuperRareFramework" with version "1.0" (not in any database)
When vuln_correlation is run
Then it returns zero vulnerabilities
and attack_readiness_score = 0.0

### S4 [Security] Default credentials returned
Given a technology "Jenkins" with version "2.0" (default creds known)
When vuln_correlation is run
Then it returns default_credentials with username "admin"
and confidence for the credential entry is recorded

### S5 [Happy path] Critical CVE prioritised
Given multiple technologies with varying CVSS scores
When vuln_correlation ranks them
Then most_critical is the entry with the highest CVSS score
and attack_readiness_score reflects exploit availability

### S6 [Edge] Version too generic (no specific version)
Given a technology "nginx" without version number
When vuln_correlation is run
Then it matches CVEs against the latest known stable version
and confidence is reduced (< 0.5)
