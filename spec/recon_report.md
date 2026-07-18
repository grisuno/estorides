# recon_report — Reconnaissance Report Generator

## Purpose
Generate an executive-level markdown report aggregating all passive
reconnaissance findings into a structured, readable document suitable for
client delivery, team briefings, and engagement documentation.

## Inputs
- `target_scoring: TargetScoringResult` — scored targets with findings
- `tech_fingerprint: Optional[TechFingerprintResult]`
- `cloud_assets: Optional[CloudAssetDiscoveryResult]`
- `people_intel: Optional[PeopleIntelResult]`
- `code_exposure: Optional[CodeExposureResult]`
- `supply_chain: Optional[SupplyChainResult]`
- `pdns: Optional[PDNSResult]`
- `query: str` — original search query
- `metadata: ReportMetadata` — operator info, engagement details

## Outputs
```
ReportResult {
  markdown: str                       # full report text
  sections: List[ReportSection]
  word_count: int
  generated_at: str
}

ReportSection {
  title: str
  level: int                          # heading level (1, 2, 3)
  content: str
  severity: Optional[str]             # section-level severity flag
}

ReportMetadata {
  operator: str
  engagement: str
  date: str
  classification: str                 # TLP level: WHITE | GREEN | AMBER | RED
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| No scoring data | `NO_DATA` | Generate minimal report with query only |
| Missing optional modules | `PARTIAL_DATA` | Skip missing sections, note "no data" |
| Report generation failure | `GENERATION_ERR` | Return partial report with error section |
| TLP level invalid | `INVALID_TLP` | Default to TLP:AMBER |

## Security guarantees
- Report classification controlled by TLP input
- No raw credentials in report output (abstracted to "credentials found")
- No internal paths or internal hostnames in client reports
- Report can be encrypted with `age` via the existing encryption module

## Out of scope
- PDF generation (handled by visual review toolchain)
- HTML dashboard (handled by web UI)
- Automated report delivery
- Translation to other languages

## BDD Scenarios

### S1 [Happy path] Full report with all data
Given a complete set of recon results across all modules
When recon_report generates the report
Then markdown contains sections for: Executive Summary, Attack Surface,
Technology Stack, Cloud Assets, People Intelligence, Code Exposure,
Supply Chain, Critical Findings, Recommendations
and word_count > 500

### S2 [Happy path] Executive summary content
Given critical findings including an open S3 bucket and hardcoded AWS keys
When recon_report generates the executive summary
Then the summary mentions both critical findings
and includes a risk rating

### S3 [Edge] Minimal data
Given only a target query with no findings
When recon_report generates the report
Then it produces a minimal report with query info
and notes "No significant findings discovered"
and word_count >= 50

### S4 [Security] TLP classification header
Given a report with classification "TLP:AMBER"
When recon_report formats the report
Then the first line contains "TLP:AMBER"
and the classification is prominently displayed

### S5 [Happy path] Recommendations prioritised
Given 10 findings across all modules
When recon_report writes the recommendations section
Then recommendations are ordered by impact (critical first)
and each recommendation has a clear action statement

### S6 [Security] No credentials in report body
Given code_exposure findings containing raw AWS keys
When recon_report generates the report
Then the report body does not contain the actual key values
and instead says "[REDACTED] - AWS Access Key" or similar

### S7 [Happy path] Subdomain tree visualization
Given pdns results with 20 subdomains in a hierarchy
When recon_report renders the subdomain section
Then it produces an ASCII tree of subdomain relationships
and marks which are active vs historical

### S8 [Edge] Single critical finding report
Given only one critical finding (open S3 bucket with files)
When recon_report generates the report
Then the report is concise but complete
and the bucket finding is prominently featured in executive summary
