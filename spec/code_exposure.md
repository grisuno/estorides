# code_exposure — GitHub Dorking & Code Exposure

## Purpose
Search public code repositories for credentials, configuration files, internal
URLs, API keys, and sensitive data exposed by the target organisation. Uses
automated dork queries across GitHub, GitLab, and other public code hosts.

## Inputs
- `org_name: str` — GitHub/GitLab organisation name
- `domain: str` — target domain (for domain-specific code search)
- `keywords: List[str]` — optional, additional search terms

## Outputs
```
CodeExposureResult {
  findings: List[CodeFinding]
  total_findings: int
  severity_summary: SeveritySummary
  scan_timestamp: str
}

CodeFinding {
  source: str              # github | gitlab | shodan | npm | pypi | dockerhub
  type: str                # credential | api_key | config | internal_url | secret | token | other
  file_path: str
  repository: str
  snippet: str             # surrounding context (~200 chars)
  matched_pattern: str
  severity: str            # critical | high | medium | low | info
  verified: bool           # whether the secret format validates (e.g. AWS key format)
}

SeveritySummary {
  critical: int
  high: int
  medium: int
  low: int
  info: int
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| API rate limited | `RATE_LIMITED` | Return partial results + rate_limit_remaining: 0 |
| No organisation found | `ORG_NOT_FOUND` | Return empty findings, total=0 |
| Invalid org name | `INVALID_ORG` | Return error |
| Search token expired | `AUTH_EXPIRED` | Return error with guidance to refresh GITHUB_TOKEN |

## Security guarantees
- No credentials found are stored in the fusion store (memory-only)
- No automated exploit of discovered secrets
- All searches use public API endpoints (no scraping)
- Findings are ephemeral and not persisted across runs unless explicitly saved
- Snippet length is capped at 200 characters

## Out of scope
- Private repository scanning
- Binary analysis
- Commit history mining (only current HEAD)
- Active exploitation of discovered credentials

## BDD Scenarios

### S1 [Happy path] AWS key found in public repo
Given an org "target-org" with a public repo containing "AKIAIOSFODNN7EXAMPLE"
When code_exposure is run
Then it returns a finding with type "credential"
and severity "critical"
and verified is True (AWS key format validates)

### S2 [Edge] No public repositories found
Given an org "target-org" with no public repos
When code_exposure is run
Then total_findings = 0
and severity_summary shows all zeros

### S3 [Error] API rate limited
Given the GitHub API returns 403 with rate limit info
When code_exposure is run
Then it returns partial results with rate_limit_remaining: 0
and an appropriate error entry

### S4 [Security] Internal URL exposed in code
Given a file containing "https://internal-jenkins.target-org.com/"
When code_exposure is run
Then the finding type is "internal_url"
and severity is "high"

### S5 [Happy path] .env file exposed
Given a public repo containing a .env file with DB_PASSWORD
When code_exposure is run
Then it returns findings with type "config"
and severity "critical"

### S6 [Edge] False positive — example credentials
Given code containing "password = 'your-password-here'" or "api_key = 'YOUR_API_KEY'"
When code_exposure is run
Then the finding is marked as severity "info" (pattern-matched but likely placeholder)

### S7 [Happy path] Multi-platform search
Given an org "target-org" with both GitHub and GitLab repos
When code_exposure is run
Then findings include both "github" and "gitlab" source entries

### S8 [Security] Snippet length bounded
Given a file with a 10000-character line containing a secret
When code_exposure captures the snippet
Then snippet length <= 200 characters
