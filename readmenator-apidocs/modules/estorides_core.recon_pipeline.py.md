# `estorides_core.recon_pipeline`

> Source: [estorides_core/recon_pipeline.py:1](../../estorides_core/recon_pipeline.py#L1) | language `py` | coverage 0.0% | [API index](../index.md)

## Contents

- **Functions:** [`run_passive_recon`](#run_passive_recon)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_estorides_core_recon_pipeline_py__run_passive_recon(["run_passive_recon"])
    n_estorides_core_cloud_asset_discovery_py__CloudAssetDiscoveryResult["cloud_asset_discovery.CloudAssetDiscoveryResult"]
    n_estorides_core_cloud_asset_discovery_py__CloudAssetDiscoveryResult_to_dict["cloud_asset_discovery.CloudAssetDiscoveryResult.to_dict"]
    n_estorides_core_code_exposure_py__analyse_findings["code_exposure.analyse_findings"]
    n_estorides_core_pdns_monitor_py__analyse_pdns_data["pdns_monitor.analyse_pdns_data"]
    n_estorides_core_people_intel_py__analyse_employees["people_intel.analyse_employees"]
    n_estorides_core_supply_chain_py__analyse_third_parties["supply_chain.analyse_third_parties"]
    n_estorides_core_tech_fingerprint_py__fingerprint["tech_fingerprint.fingerprint"]
    n_estorides_core_vuln_correlation_py__correlate_technologies["vuln_correlation.correlate_technologies"]
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_cloud_asset_discovery_py__CloudAssetDiscoveryResult
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_cloud_asset_discovery_py__CloudAssetDiscoveryResult_to_dict
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_code_exposure_py__analyse_findings
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_pdns_monitor_py__analyse_pdns_data
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_people_intel_py__analyse_employees
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_supply_chain_py__analyse_third_parties
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_tech_fingerprint_py__fingerprint
    n_estorides_core_recon_pipeline_py__run_passive_recon -.-> n_estorides_core_vuln_correlation_py__correlate_technologies
```

## Functions

<a id="run_passive_recon"></a>

### `run_passive_recon`

`function` | [estorides_core/recon_pipeline.py:22](../../estorides_core/recon_pipeline.py#L22)

```python
def run_passive_recon(query: str, headers: dict | None = None, html: str | None = None, cookies: list[str] | None = None, employees: list[Employee] | None = None, code_findings: list | None = None, third_parties: list[ThirdParty] | None = None, pdns_subdomains: list | None = None, cloud_assets: list | None = None) -> dict
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  |  |
| `headers` | `dict \| None` | `None` |  |
| `html` | `str \| None` | `None` |  |
| `cookies` | `list[str] \| None` | `None` |  |
| `employees` | `list[Employee] \| None` | `None` |  |
| `code_findings` | `list \| None` | `None` |  |
| `third_parties` | `list[ThirdParty] \| None` | `None` |  |
| `pdns_subdomains` | `list \| None` | `None` |  |
| `cloud_assets` | `list \| None` | `None` |  |

**Returns:** `dict`

*Calls:* [`CloudAssetDiscoveryResult`](estorides_core.cloud_asset_discovery.py.md#cloudassetdiscoveryresult), [`CloudAssetDiscoveryResult.to_dict`](estorides_core.cloud_asset_discovery.py.md#cloudassetdiscoveryresult-to_dict), [`analyse_findings`](estorides_core.code_exposure.py.md#analyse_findings), [`analyse_pdns_data`](estorides_core.pdns_monitor.py.md#analyse_pdns_data), [`analyse_employees`](estorides_core.people_intel.py.md#analyse_employees), [`analyse_third_parties`](estorides_core.supply_chain.py.md#analyse_third_parties), [`fingerprint`](estorides_core.tech_fingerprint.py.md#fingerprint), [`correlate_technologies`](estorides_core.vuln_correlation.py.md#correlate_technologies)

---
