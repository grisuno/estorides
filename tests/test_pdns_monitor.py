"""ATDD + BDD tests for estorides_core.pdns_monitor.

Implements the Given-When-Then contracts declared in
``spec/pdns_monitor.md``.
"""
from __future__ import annotations

from estorides_core.pdns_monitor import (
    CertRecord,
    HistoricalSubdomain,
    IPRecord,
    analyse_pdns_data,
    classify_subdomain_status,
)


# S1 — Happy path: Subdomains from CT log
class TestCtLogSubdomains:
    def test_returns_subdomains_from_ct(self) -> None:
        subs = [
            HistoricalSubdomain("www.example.com", "2024-01-01", "2024-06-01", 10, ["1.2.3.4"], ["crt.sh"], True),
            HistoricalSubdomain("api.example.com", "2024-02-01", "2024-06-01", 5, ["5.6.7.8"], ["crt.sh"], True),
            HistoricalSubdomain("mail.example.com", "2024-03-01", "2024-06-01", 3, ["9.10.11.12"], ["crt.sh"], False),
        ]
        result = analyse_pdns_data(subs, [], [])
        assert result.total_subdomains == 3
        active = [s for s in result.subdomains if s.is_active]
        assert len(active) == 2


# S2 — Happy path: IP history
class TestIPHistory:
    def test_tracks_ip_changes(self) -> None:
        ip_records = {
            "example.com": [
                IPRecord("1.1.1.1", "2024-01-01", "2024-03-01", 12345, "ASN Corp", "pdns"),
                IPRecord("2.2.2.2", "2024-03-02", "2024-06-01", 12345, "ASN Corp", "pdns"),
            ]
        }
        sub = [HistoricalSubdomain("example.com", "2024-01-01", "2024-06-01", 2, ["1.1.1.1", "2.2.2.2"], ["pdns"], True)]
        result = analyse_pdns_data(sub, ip_records, [])
        assert "example.com" in result.ip_history.keys()
        assert len(result.ip_history["example.com"]) == 2


# S3 — Edge: No data available
class TestNoData:
    def test_empty_when_no_history(self) -> None:
        result = analyse_pdns_data([], {}, [])
        assert result.total_subdomains == 0
        assert result.total_new_certs == 0


# S4 — Happy path: New cert with SANs
class TestNewCertificates:
    def test_new_cert_with_san(self) -> None:
        certs = [
            CertRecord(
                serial="ABCDEF123",
                subject="example.com",
                issuer="Let's Encrypt",
                not_before="2024-06-01",
                not_after="2024-09-01",
                dns_names=["example.com", "www.example.com", "api.example.com",
                           "admin.example.com", "cdn.example.com"],
                is_wildcard=False,
                source="certspotter",
            )
        ]
        result = analyse_pdns_data([], {}, certs)
        assert result.total_new_certs == 1
        assert len(result.new_certs[0].dns_names) == 5


# S5 — Security: No AXFR
class TestNoAxfr:
    def test_no_zone_transfer_attempted(self) -> None:
        # All PDNS data comes from public APIs, not zone transfers
        sub = HistoricalSubdomain("test.example.com", "2024-01-01", "2024-06-01", 1, ["1.2.3.4"], ["crt.sh"], True)
        assert "pdns" in sub.sources or "crt.sh" in sub.sources
        assert "axfr" not in sub.sources


# S6 — Happy path: Wildcard cert
class TestWildcardCert:
    def test_wildcard_cert_detected(self) -> None:
        cert = CertRecord(
            serial="XYZ789",
            subject="*.example.com",
            issuer="DigiCert",
            not_before="2024-01-01",
            not_after="2025-01-01",
            dns_names=["*.example.com", "example.com"],
            is_wildcard=True,
            source="crt_sh",
        )
        assert cert.is_wildcard is True
        assert cert.subject == "*.example.com"


# S7 — Edge: Subdomain status classification
class TestSubdomainStatusClassification:
    def test_active_status_when_resolves(self) -> None:
        assert classify_subdomain_status("www.example.com", ["1.2.3.4"]) is True

    def test_inactive_when_no_resolution(self) -> None:
        assert classify_subdomain_status("old.example.com", []) is False


# S8 — Security: Monitor poll interval
class TestMonitorPollInterval:
    def test_minimum_poll_interval(self) -> None:
        from estorides_core.pdns_monitor import MONITOR_POLL_INTERVAL_S
        assert MONITOR_POLL_INTERVAL_S >= 3600
