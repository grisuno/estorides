# tech_fingerprint — Technology Stack Fingerprinting

## Purpose
Identify the full technology stack of a target domain/IP from passive HTTP
response analysis: web server, WAF, CMS, frameworks, JS libraries, analytics,
CDN, SSL/TLS configurations. This is the foundation for vulnerability
correlation and attack surface prioritisation.

## Inputs
- `domain: str` — target domain (e.g. `example.com`)
- `headers: Dict[str, str]` — HTTP response headers
- `html: str` — first ~100KB of HTML body
- `cookies: List[str]` — set-cookie header values
- `status: int` — HTTP status code

## Outputs
```
TechFingerprintResult {
  technologies: List[Tech]       # detected technologies
  confidence: float               # overall fingerprint confidence (0-1)
  source_count: int               # how many signals contributed
}

Tech {
  name: str                       # e.g. "nginx", "Cloudflare", "WordPress"
  category: str                   # server | waf | cms | framework | js_library | analytics | cdn | os | language
  version: Optional[str]          # version string if detected
  confidence: float               # 0-1 per-technology
  cve_candidates: List[str]       # CVE IDs matching this version
  first_seen_in: str              # which source/header/pattern
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| Empty headers + empty html | `NO_INPUT` | Return empty result, confidence=0 |
| Malformed version string | `VERSION_PARSE_ERROR` | Return tech without version, log warning |
| Unknown/ambiguous pattern match | `LOW_CONFIDENCE` | Return tech with confidence <0.5 |
| Rate limit from external API | `RATE_LIMITED` | Return only local fingerprint results |

## Security guarantees
- No code execution from fingerprints (pure pattern matching)
- No regex injection (all patterns are pre-compiled constants)
- No external I/O in the core module (HTTP fetching is done upstream)
- Input size bounded at 100KB for HTML, 10KB for headers

## Out of scope
- Active probing (Wappalyzer browser-based detection)
- JavaScript execution / DOM analysis
- Machine learning classification
- Screenshot analysis

## BDD Scenarios

### S1 [Happy path] Detect Nginx + PHP + jQuery from headers + HTML
Given a domain with HTTP response headers containing "Server: nginx/1.18.0"
and "X-Powered-By: PHP/7.4.33" and HTML containing 'src="jquery-3.6.0.min.js"'
When tech_fingerprint is run
Then it returns technologies containing "nginx" with version "1.18.0"
and "PHP" with version "7.4.33"
and "jQuery" with version "3.6.0"
and confidence > 0.7

### S2 [Edge case] Empty response
Given empty headers and empty HTML
When tech_fingerprint is run
Then it returns an empty technologies list
and confidence = 0.0

### S3 [Error case] Malformed version string
Given a header like "Server: nginx\x00\x00\x00"
When tech_fingerprint is run
Then it returns "nginx" without version
and logs VERSION_PARSE_ERROR at warning level

### S4 [Security] HTML with script injection as version
Given HTML containing '<script>alert("jQuery-1.0.0")</script>'
When tech_fingerprint is run
Then no script content is interpreted as technology version
and the result does not contain technologies from script content

### S5 [Happy path] WAF detection via headers
Given response headers containing "cf-ray" and "cf-cache-status"
When tech_fingerprint is run
Then it returns "Cloudflare" in technologies with category "cdn"
and confidence > 0.8

### S6 [Happy path] CMS detection from HTML meta
Given HTML containing '<meta name="generator" content="WordPress 6.2" />'
When tech_fingerprint is run
Then it returns "WordPress" in technologies with category "cms"
and version "6.2"

### S7 [Edge] Multiple matches, deduplication
Given two different sources indicating "nginx" (header + cookie pattern)
When tech_fingerprint is run
Then "nginx" appears only once in technologies
and its confidence reflects both sources

### S8 [Security] Very long HTML input
Given HTML of 500KB with technology patterns scattered throughout
When tech_fingerprint is run
Then it processes only the first 100KB
and does not exceed 200ms processing time
