# target_scoring — Target Asset Ranking & Attack Surface Scoring

## Purpose
Aggregate all reconnaissance findings across every module and produce a
prioritised, ranked list of targets with actionable attack recommendations.
Answers "what do I attack first?" for the red team operator.

## Inputs
- `tech_fingerprint: Optional[TechFingerprintResult]`
- `vuln_correlation: Optional[VulnCorrelationResult]`
- `cloud_assets: Optional[CloudAssetDiscoveryResult]`
- `people_intel: Optional[PeopleIntelResult]`
- `code_exposure: Optional[CodeExposureResult]`
- `supply_chain: Optional[SupplyChainResult]`
- `pdns: Optional[PDNSResult]`
- `scope_domains: List[str]` — targets in scope

## Outputs
```
TargetScoringResult {
  targets: List[ScoredTarget]
  top_recommendations: List[str]
  summary: ScoringSummary
}

ScoredTarget {
  target: str                        # domain/IP
  attack_surface_score: float        # 0-1 overall exposure
  soft_target_score: float           # 0-1 ease of exploitation
  crown_jewel_score: float           # 0-1 business value
  lateral_potential: float           # 0-1 pivot potential
  composite_score: float             # weighted combination
  tier: str                          # critical | high | medium | low | noise
  key_findings: List[str]
  recommended_actions: List[str]
}

ScoringSummary {
  total_targets: int
  critical_targets: int
  high_targets: int
  medium_targets: int
  low_targets: int
  noise_targets: int
  top_target: Optional[str]
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| No input data | `NO_DATA` | Return empty targets, summary zeroes |
| No targets in scope | `NO_SCOPE` | Score all discovered targets |
| Missing fingerprint data | `PARTIAL_DATA` | Score with available data, mark confidence |
| All scores zero | `NO_FINDINGS` | Return targets with composite=0, tier=noise |

## Security guarantees
- All computation is local (no external calls)
- No scoring data leaves the process
- Scoring weights are configurable via `TargetScoringConfig`
- No correlation between different customer's data (single-session)

## Out of scope
- Automated exploitation recommendations
- Attack execution
- C2 infrastructure planning
- Payload generation

## BDD Scenarios

### S1 [Happy path] Target with open bucket + old nginx ranked critical
Given a target with an open S3 bucket (critical) and nginx 1.18.0 with CVEs (high)
When target_scoring scores it
Then composite_score > 0.7
and tier is "critical"
and recommended_actions includes both findings

### S2 [Happy path] Target with no findings ranked noise
Given a target with no tech fingerprint, no vulns, no cloud assets, no code exposure
When target_scoring scores it
Then composite_score = 0.0
and tier is "noise"

### S3 [Edge] Mixed scoring with multiple targets
Given 5 targets with varying findings (1 critical, 2 high, 1 medium, 1 noise)
When target_scoring ranks them
Then summary.critical_targets = 1
and summary.high_targets = 2
and summary.medium_targets = 1
and summary.noise_targets = 1
and top_target is the critical one

### S4 [Security] Configurable weights
Given a custom TargetScoringConfig with different weight values
When target_scoring computes scores
Then the scoring uses the provided weights
and composite_score changes accordingly

### S5 [Happy path] Crown jewel detection
Given a target with subdomains "jenkins.target.com", "jira.target.com", "vpn.target.com"
When target_scoring evaluates crown_jewel_score
Then these targets receive higher crown_jewel_score than "blog.target.com"
and crown_jewel_score > 0.7 for "jenkins.target.com"

### S6 [Edge] Partial data scenario
Given only tech_fingerprint data available (no code, no cloud, no people)
When target_scoring scores
Then the result marks confidence as "partial"
and scores reflect only available data

### S7 [Happy path] Lateral movement potential
Given employees with breached passwords reused across platforms
When target_scoring evaluates lateral_potential
Then lateral_potential > 0.5
and recommended_actions includes password reuse warning

### S8 [Security] No external data exfiltration
Given a complete TargetScoringResult with all findings
When the result is serialised
Then no credential data appears in the output
and all sensitive fields are abstracted to scores
