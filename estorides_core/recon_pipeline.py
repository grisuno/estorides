from __future__ import annotations

import logging

from .tech_fingerprint import TechFingerprintResult, fingerprint
from .vuln_correlation import VulnCorrelationResult, correlate_technologies
from .cloud_asset_discovery import CloudAssetDiscoveryResult
from .people_intel import Employee, PeopleIntelResult, analyse_employees
from .code_exposure import CodeExposureResult, analyse_findings
from .supply_chain import ThirdParty, SupplyChainResult, analyse_third_parties
from .pdns_monitor import PDNSResult, analyse_pdns_data
from .target_scoring import (
    TargetScoringConfig,
    TargetScoringResult,
    score_all_targets,
    score_target,
)

log = logging.getLogger("estorides.recon_pipeline")


def run_passive_recon(
    query: str,
    headers: dict | None = None,
    html: str | None = None,
    cookies: list[str] | None = None,
    employees: list[Employee] | None = None,
    code_findings: list | None = None,
    third_parties: list[ThirdParty] | None = None,
    pdns_subdomains: list | None = None,
    cloud_assets: list | None = None,
) -> dict:
    headers = headers or {}
    html = html or ""
    employees = employees or []
    code_findings = code_findings or []
    third_parties = third_parties or []
    pdns_subdomains = pdns_subdomains or []
    cloud_assets = cloud_assets or []

    result: dict = {}

    tech_result = fingerprint(headers, html, cookies)
    result["tech_fingerprint"] = tech_result.to_dict() if hasattr(tech_result, "to_dict") else {}

    vuln_result = correlate_technologies(
        tech_result.technologies if hasattr(tech_result, "technologies") else []
    )
    result["vuln_correlation"] = vuln_result.to_dict() if hasattr(vuln_result, "to_dict") else {}

    if employees:
        intel_result = analyse_employees(employees, query)
        result["people_intel"] = intel_result.to_dict() if hasattr(intel_result, "to_dict") else {}

    cloud_data = CloudAssetDiscoveryResult(
        assets=cloud_assets,
        total_assets=len(cloud_assets),
        accessible_count=sum(1 for a in cloud_assets if getattr(a, "accessible", False)),
        listing_count=sum(1 for a in cloud_assets if getattr(a, "listing_enabled", False)),
    )
    result["cloud_assets"] = cloud_data.to_dict() if hasattr(cloud_data, "to_dict") else {}

    code_data = analyse_findings(code_findings)
    result["code_exposure"] = code_data.to_dict()

    supply_data = analyse_third_parties(third_parties)
    result["supply_chain"] = supply_data.to_dict()

    pdns_data = analyse_pdns_data(pdns_subdomains, {}, [])
    result["pdns_monitor"] = pdns_data.to_dict()

    target = score_target(
        query,
        result.get("tech_fingerprint", {}),
        result.get("vuln_correlation", {}),
        cloud_data=result.get("cloud_assets", {}),
        people_data=result.get("people_intel", {}),
        code_data=result.get("code_exposure", {}),
        supply_data=result.get("supply_chain", {}),
        pdns_data=result.get("pdns_monitor", {}),
    )
    scoring_result = score_all_targets([target])
    result["target_scoring"] = scoring_result.to_dict()

    result["query"] = query
    return result
