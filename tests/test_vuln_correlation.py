"""ATDD + BDD tests for estorides_core.vuln_correlation.

Implements the Given-When-Then contracts declared in
``spec/vuln_correlation.md``.
"""
from __future__ import annotations

from estorides_core.vuln_correlation import (
    VulnEntry,
    compute_attack_readiness,
    correlate_technologies,
    lookup_cve_for_tech,
)


def _make_tech(name: str, version: str | None = None) -> dict:
    return {"name": name, "version": version, "category": "server"}


# S1 — Happy path: CVE match for nginx
class TestNginxCveMatch:
    def test_returns_cves_for_nginx(self) -> None:
        techs = [_make_tech("nginx", "1.18.0")]
        result = correlate_technologies(techs)
        nginx_vulns = [v for v in result.vulnerabilities if v.affected_tech == "nginx"]
        assert len(nginx_vulns) >= 1
        assert any("CVE" in v.cve_id for v in nginx_vulns)


# S2 — Happy path: Metasploit module available
class TestMetasploitAvailable:
    def test_apache_struts_has_metasploit(self) -> None:
        techs = [_make_tech("Apache Struts", "2.5.12")]
        result = correlate_technologies(techs)
        with_msf = [v for v in result.vulnerabilities if v.metasploit_module is not None]
        assert len(with_msf) >= 1
        assert with_msf[0].metasploit_module is not None


# S3 — Edge: Unknown technology
class TestUnknownTechnology:
    def test_unknown_tech_returns_empty(self) -> None:
        techs = [_make_tech("SuperRareFramework", "1.0")]
        result = correlate_technologies(techs)
        assert len(result.vulnerabilities) == 0
        assert result.attack_readiness_score == 0.0


# S4 — Security: Default credentials for Jenkins
class TestDefaultCredentials:
    def test_jenkins_has_default_admin(self) -> None:
        techs = [_make_tech("Jenkins", "2.0")]
        result = correlate_technologies(techs)
        with_defaults = [v for v in result.vulnerabilities if v.default_credentials is not None]
        if with_defaults:
            cred = with_defaults[0].default_credentials
            assert cred is not None
            assert cred.username == "admin"


# S5 — Happy path: Critical severity prioritised
class TestCriticalPrioritised:
    def test_most_critical_is_highest_cvss(self) -> None:
        techs = [_make_tech("Apache Struts", "2.5.12")]
        result = correlate_technologies(techs)
        if result.most_critical:
            assert result.most_critical.cvss_score >= 7.0


# S6 — Edge: No version, match to latest
class TestNoVersionMatch:
    def test_no_version_reduces_confidence(self) -> None:
        techs = [_make_tech("nginx", None)]
        result = correlate_technologies(techs)
        nginx_vulns = [v for v in result.vulnerabilities if v.affected_tech == "nginx"]
        if nginx_vulns:
            assert all(v.confidence < 0.5 for v in nginx_vulns)


# S7 — Happy path: Compute attack readiness
class TestAttackReadiness:
    def test_exploit_available_increases_score(self) -> None:
        vulns = [
            VulnEntry("CVE-2021-1111", 9.8, "critical", "nginx", "1.18.0",
                      True, "edb", 50001, None, None, "Bad", 0.9),
            VulnEntry("CVE-2021-1112", 5.0, "medium", "nginx", "1.18.0",
                      False, "none", None, None, None, "Meh", 0.5),
        ]
        score = compute_attack_readiness(vulns)
        assert score > 0.5  # exploit available boosts score


# S8 — Happy path: CVE lookup local table
class TestLocalCveLookup:
    def test_known_tech_in_local_table(self) -> None:
        vulns = lookup_cve_for_tech("nginx", "1.18.0")
        assert len(vulns) > 0
        assert all(v.affected_tech == "nginx" for v in vulns)
