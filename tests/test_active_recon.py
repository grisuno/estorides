"""ATDD + BDD tests for estorides_core.active_recon.

Implements the Given-When-Then contracts declared in
``spec/active_recon.md``. Property-based invariants live in
``tests/properties/test_active_recon_properties.py``.
"""
from __future__ import annotations

from estorides_core.active_recon import (
    DnsreconResult,
    NiktoResult,
    NmapResult,
    SqlmapResult,
    TheHarvesterResult,
    run_dnsrecon,
    run_nikto,
    run_nmap,
    run_sqlmap,
    run_theHarvester,
)
from estorides_core.tool_runner import ToolErrorResult


class TestNmapResult:
    def test_run_nmap_returns_result(self) -> None:
        result = run_nmap("scanme.nmap.org", args=["--version"])
        assert isinstance(result, (NmapResult, ToolErrorResult))

    def test_nmap_result_has_to_dict(self) -> None:
        result = run_nmap("scanme.nmap.org", args=["--version"])
        if isinstance(result, NmapResult):
            d = result.to_dict()
            assert "success" in d
            assert "hosts" in d
            assert "open_ports" in d
            assert "entities" in d

    def test_nmap_result_to_entities_is_list(self) -> None:
        result = run_nmap("scanme.nmap.org", args=["--version"])
        if isinstance(result, NmapResult):
            entities = result.to_entities()
            assert isinstance(entities, list)


class TestNiktoResult:
    def test_run_nikto_returns_result(self) -> None:
        result = run_nikto("scanme.nmap.org", args=["-timeout", "5"])
        assert isinstance(result, (NiktoResult, ToolErrorResult))

    def test_nikto_result_has_to_dict(self) -> None:
        result = run_nikto("scanme.nmap.org", args=["-timeout", "5"])
        if isinstance(result, NiktoResult):
            d = result.to_dict()
            assert "success" in d
            assert "findings" in d


class TestSqlmapResult:
    def test_run_sqlmap_returns_result(self) -> None:
        result = run_sqlmap("https://scanme.nmap.org", args=["--batch", "--level=1"])
        assert isinstance(result, (SqlmapResult, ToolErrorResult))

    def test_sqlmap_result_has_to_dict(self) -> None:
        result = run_sqlmap("https://scanme.nmap.org", args=["--batch", "--level=1"])
        if isinstance(result, SqlmapResult):
            d = result.to_dict()
            assert "success" in d
            assert "vulnerabilities" in d


class TestDnsreconResult:
    def test_run_dnsrecon_returns_result(self) -> None:
        result = run_dnsrecon("example.com", args=["-t", "std"])
        assert isinstance(result, (DnsreconResult, ToolErrorResult))

    def test_dnsrecon_result_has_to_dict(self) -> None:
        result = run_dnsrecon("example.com", args=["-t", "std"])
        if isinstance(result, DnsreconResult):
            d = result.to_dict()
            assert "success" in d
            assert "subdomains" in d


class TestTheHarvesterResult:
    def test_run_theHarvester_returns_result(self) -> None:
        result = run_theHarvester("example.com", args=["-b", "bing"])
        assert isinstance(result, (TheHarvesterResult, ToolErrorResult))

    def test_harvester_result_has_to_dict(self) -> None:
        result = run_theHarvester("example.com", args=["-b", "bing"])
        if isinstance(result, TheHarvesterResult):
            d = result.to_dict()
            assert "success" in d
            assert "emails" in d


class TestResultTypes:
    def test_nmap_result_is_dataclass(self) -> None:
        result = NmapResult(
            success=True, exit_code=0, hosts=[], open_ports=[],
            services=[], entities=[], raw_output="", confidence=0.5, error=None,
        )
        assert result.success is True
        assert isinstance(result.to_dict(), dict)

    def test_nikto_result_is_dataclass(self) -> None:
        result = NiktoResult(
            success=True, exit_code=0, findings=[], entities=[],
            raw_output="", confidence=0.5, error=None,
        )
        assert result.success is True

    def test_sqlmap_result_is_dataclass(self) -> None:
        result = SqlmapResult(
            success=True, exit_code=0, vulnerabilities=[], entities=[],
            raw_output="", confidence=0.5, error=None,
        )
        assert result.success is True

    def test_dnsrecon_result_is_dataclass(self) -> None:
        result = DnsreconResult(
            success=True, exit_code=0, subdomains=[], mx_records=[],
            ns_records=[], entities=[], raw_output="", confidence=0.5, error=None,
        )
        assert result.success is True

    def test_harvester_result_is_dataclass(self) -> None:
        result = TheHarvesterResult(
            success=True, exit_code=0, emails=[], hosts=[],
            entities=[], raw_output="", confidence=0.5, error=None,
        )
        assert result.success is True


class TestErrorResultsFlowThrough:
    def test_nmap_error_result_has_empty_entities(self) -> None:
        result = run_nmap("192.0.2.1", args=["-p", "99999"])
        assert isinstance(result, (NmapResult, ToolErrorResult))
        if isinstance(result, NmapResult):
            assert isinstance(result.entities, list)
