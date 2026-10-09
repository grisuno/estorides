# estorides_core: people_intel

*Community 5 | 15 files | cohesion 1.00*

## Definition

This community groups 15 file(s) rooted at `estorides_core` with dominant language py (cohesion 1.00). Central symbols: `BreachContext`, `BreachRecord`, `CertRecord`, `CloudAsset`, `CloudAssetDiscoveryError`, `CloudAssetDiscoveryResult`, `CodeExposureResult`, `CodeFinding`. Core file: `tests/test_code_exposure.py` (21 symbols). Documented purpose: ATDD + BDD tests for estorides_core.cloud_asset_discovery.  Implements the Given-When-Then contracts declared in ``spec/cloud_asset_discovery.md``..

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/cloud_asset_discovery.py` | py | utility | 7 | no |
| `estorides_core/code_exposure.py` | py | utility | 10 | no |
| `estorides_core/pdns_monitor.py` | py | utility | 11 | no |
| `estorides_core/people_intel.py` | py | utility | 13 | no |
| `estorides_core/recon_pipeline.py` | py | utility | 1 | no |
| `estorides_core/supply_chain.py` | py | utility | 13 | no |
| `estorides_core/tech_fingerprint.py` | py | utility | 6 | no |
| `estorides_core/vuln_correlation.py` | py | utility | 11 | no |
| `tests/test_cloud_asset_discovery.py` | py | testing | 18 | yes |
| `tests/test_code_exposure.py` | py | testing | 21 | yes |
| `tests/test_pdns_monitor.py` | py | testing | 17 | yes |
| `tests/test_people_intel.py` | py | testing | 18 | yes |
| `tests/test_supply_chain.py` | py | testing | 17 | yes |
| `tests/test_tech_fingerprint.py` | py | testing | 16 | yes |
| `tests/test_vuln_correlation.py` | py | testing | 17 | yes |

## Key Symbols

- `CloudAsset` (class, `estorides_core/cloud_asset_discovery.py:34`) `class CloudAsset`
- `to_dict` (method, `estorides_core/cloud_asset_discovery.py:45`) `def to_dict(self)`
- `CloudAssetDiscoveryResult` (class, `estorides_core/cloud_asset_discovery.py:50`) `class CloudAssetDiscoveryResult`
- `to_dict` (method, `estorides_core/cloud_asset_discovery.py:56`) `def to_dict(self)`
- `generate_bucket_names` (method, `estorides_core/cloud_asset_discovery.py:65`) `def generate_bucket_names(domain)`
- `assess_bucket` (method, `estorides_core/cloud_asset_discovery.py:84`) `def assess_bucket(url, method)`
- `CloudAssetDiscoveryError` (class, `estorides_core/cloud_asset_discovery.py:93`) `class CloudAssetDiscoveryError(Exception)`
- `CodeFinding` (class, `estorides_core/code_exposure.py:47`) `class CodeFinding`
- `to_dict` (method, `estorides_core/code_exposure.py:57`) `def to_dict(self)`
- `SeveritySummary` (class, `estorides_core/code_exposure.py:62`) `class SeveritySummary`
- `to_dict` (method, `estorides_core/code_exposure.py:69`) `def to_dict(self)`
- `CodeExposureResult` (class, `estorides_core/code_exposure.py:74`) `class CodeExposureResult`
- `to_dict` (method, `estorides_core/code_exposure.py:81`) `def to_dict(self)`
- `validate_aws_key` (method, `estorides_core/code_exposure.py:91`) `def validate_aws_key(key)`
- `_is_placeholder` (method, `estorides_core/code_exposure.py:95`) `def _is_placeholder(text)`
- `classify_finding` (method, `estorides_core/code_exposure.py:99`) `def classify_finding(content, source, file_path)`
- `analyse_findings` (method, `estorides_core/code_exposure.py:189`) `def analyse_findings(findings, rate_limited)`
- `HistoricalSubdomain` (class, `estorides_core/pdns_monitor.py:13`) `class HistoricalSubdomain`
- `to_dict` (method, `estorides_core/pdns_monitor.py:22`) `def to_dict(self)`
- `IPRecord` (class, `estorides_core/pdns_monitor.py:27`) `class IPRecord`
- `to_dict` (method, `estorides_core/pdns_monitor.py:35`) `def to_dict(self)`
- `CertRecord` (class, `estorides_core/pdns_monitor.py:40`) `class CertRecord`
- `to_dict` (method, `estorides_core/pdns_monitor.py:50`) `def to_dict(self)`
- `PDNSResult` (class, `estorides_core/pdns_monitor.py:55`) `class PDNSResult`
- `to_dict` (method, `estorides_core/pdns_monitor.py:62`) `def to_dict(self)`
- `classify_subdomain_status` (method, `estorides_core/pdns_monitor.py:72`) `def classify_subdomain_status(fqdn, resolved_ips)`
- `extract_sans_from_cert` (method, `estorides_core/pdns_monitor.py:76`) `def extract_sans_from_cert(cert)`
- `analyse_pdns_data` (method, `estorides_core/pdns_monitor.py:80`) `def analyse_pdns_data(subdomains, ip_history, new_certs)`
- `BreachRecord` (class, `estorides_core/people_intel.py:15`) `class BreachRecord`
- `to_dict` (method, `estorides_core/people_intel.py:22`) `def to_dict(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 16
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 8 file(s) lack file-level docs (e.g. `estorides_core/cloud_asset_discovery.py`)? What purpose do they serve?
- What would break if the most connected file in estorides_core: people_intel changed?
- Should estorides_core: people_intel be split, given cohesion 1.00?

## Sources

- `estorides_core/cloud_asset_discovery.py`
- `estorides_core/code_exposure.py`
- `estorides_core/pdns_monitor.py`
- `estorides_core/people_intel.py`
- `estorides_core/recon_pipeline.py`
- `estorides_core/supply_chain.py`
- `estorides_core/tech_fingerprint.py`
- `estorides_core/vuln_correlation.py`
- `tests/test_cloud_asset_discovery.py`
- `tests/test_code_exposure.py`
- `tests/test_pdns_monitor.py`
- `tests/test_people_intel.py`
- `tests/test_supply_chain.py`
- `tests/test_tech_fingerprint.py`
- `tests/test_vuln_correlation.py`
