# people_intel — People & Identity Intelligence

## Purpose
Discover employees, infer email patterns, correlate identities across breach
databases and professional networks. Turns a domain into a people graph
suitable for social engineering and spear-phishing campaigns.

## Inputs
- `domain: str` — target organisation domain
- `known_emails: List[str]` — optional, seed emails already known
- `company_name: Optional[str]` — optional, company name for enrichment

## Outputs
```
PeopleIntelResult {
  employees: List[Employee]
  email_pattern: Optional[str]      # inferred pattern like "{first}.{last}@domain"
  email_pattern_confidence: float    # 0-1
  total_employees_found: int
  breaches: List[BreachContext]
  risk_score: float                   # 0-1 (based on breach exposure)
}

Employee {
  name: Optional[str]
  role: Optional[str]
  emails: List[str]
  phone: Optional[str]
  linkedin: Optional[str]
  twitter: Optional[str]
  github: Optional[str]
  sources: List[str]
  breaches: List[BreachRecord]
}

BreachRecord {
  breach_name: str
  email: str
  password: Optional[str]          # hash or plaintext if available
  data_classes: List[str]          # Email, Password, Name, Phone, etc.
  severity: str                    # critical | high | medium | low
}

BreachContext {
  email: str
  total_breaches: int
  passwords_exposed: bool
  severity: str
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| No employees found | `NO_RESULTS` | Empty employees, pattern=null, risk=0 |
| Invalid domain | `INVALID_DOMAIN` | Return error, no processing |
| No breach data available | `NO_BREACH_DATA` | Breaches list empty, risk based on employees only |
| Email pattern ambiguous | `PATTERN_AMBIGUOUS` | Return best guess with confidence <0.5 |

## Security guarantees
- No passwords are stored in plaintext outside the session
- No automated login to any platform
- No scraping of non-public profiles
- All sources are public/open APIs
- Rate limit respect: max 1 req/s per external source

## Out of scope
- Dark web monitoring
- Social media message content scraping
- Phone number validation (carrier check)
- Physical address discovery

## BDD Scenarios

### S1 [Happy path] Employee discovery from domain
Given a domain "example.com" with Hunter returning 3 employees
When people_intel is run
Then it returns 3 employees
and email_pattern is "{first}.{last}@example.com"
and email_pattern_confidence >= 0.8

### S2 [Edge] No employees found for unknown domain
Given a domain "nonexistent-org-123.com" with zero API results
When people_intel is run
Then it returns an empty employees list
and risk_score = 0.0

### S3 [Error] Invalid domain format
Given a domain "not-a-domain!"
When people_intel is run
Then it returns an error with code INVALID_DOMAIN

### S4 [Security] Breach password exposure context
Given an employee "john@example.com" found in "LinkedIn 2021" breach with password hash
When people_intel processes the breach
Then the breach record contains data_classes including "Email" and "Password"
and severity is "critical"

### S5 [Happy path] Email pattern inference from 3+ samples
Given known_emails ["alice@example.com", "bob@example.com", "charlie@example.com"]
When people_intel infers pattern
Then email_pattern is "{first}@{domain}"
and email_pattern_confidence >= 0.9

### S6 [Edge] Single email — pattern ambiguous
Given known_emails ["jsmith@example.com"]
When people_intel infers pattern
Then email_pattern_confidence < 0.5
and email_pattern is "{first_initial}{last}@domain" (best guess)

### S7 [Happy path] Cross-breach correlation
Given an employee appearing in 3 different breaches
When people_intel builds the breach context
Then total_breaches = 3
and passwords_exposed = True (if any breach had password data)
and risk_score > 0.5

### S8 [Security] No external credentials stored
Given a complete people_intel run
When the result is serialised
Then no employee record contains raw passwords
