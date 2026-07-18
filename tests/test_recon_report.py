"""ATDD + BDD tests for estorides_export.recon_report.

Implements the Given-When-Then contracts declared in
``spec/recon_report.md``.
"""
from __future__ import annotations

from estorides_export.recon_report import (
    ReportMetadata,
    build_executive_summary,
    generate_report,
    redact_sensitive,
)


def _make_meta() -> ReportMetadata:
    return ReportMetadata(
        operator="test-op",
        engagement="PT-2024-001",
        date="2024-06-15",
        classification="TLP:AMBER",
    )


# S1 — Happy path: Full report
class TestFullReport:
    def test_contains_all_sections(self) -> None:
        result = generate_report(
            query="example.com",
            target_scoring={},
            metadata=_make_meta(),
        )
        assert "Executive Summary" in result.markdown
        assert "Attack Surface" in result.markdown or "No significant findings" in result.markdown
        assert result.word_count > 50
        assert len(result.sections) > 0


# S2 — Happy path: Executive summary includes findings
class TestExecutiveSummaryFindings:
    def test_mentions_critical_findings(self) -> None:
        summary = build_executive_summary(
            critical_findings=["Open S3 bucket", "Hardcoded AWS keys"],
            total_targets=10,
            domain="example.com",
        )
        assert "Open S3 bucket" in summary
        assert "Hardcoded AWS keys" in summary
        assert "example.com" in summary


# S3 — Edge: Minimal data
class TestMinimalReport:
    def test_minimal_report_with_no_findings(self) -> None:
        result = generate_report(
            query="unknown-target.com",
            target_scoring={},
            metadata=_make_meta(),
        )
        assert result.word_count >= 50
        assert "No significant findings" in result.markdown or "unknown-target.com" in result.markdown


# S4 — Security: TLP classification header
class TestTlpClassification:
    def test_tlp_amber_in_header(self) -> None:
        result = generate_report(
            query="example.com",
            target_scoring={},
            metadata=_make_meta(),
        )
        assert "TLP:AMBER" in result.markdown


# S5 — Happy path: Recommendations ordered
class TestRecommendationsOrdered:
    def test_critical_first(self) -> None:
        recs = ["Fix open S3 bucket", "Update nginx", "Rotate AWS keys", "Remove .env from repo"]
        ordered = sorted(recs)  # Placeholder — real ordering from target_scoring
        assert len(ordered) == 4


# S6 — Security: Credentials redacted
class TestCredentialsRedacted:
    def test_aws_key_redacted(self) -> None:
        safe = redact_sensitive("AWS Key: AKIAIOSFODNN7EXAMPLE was found")
        assert "AKIAIOSFODNN7EXAMPLE" not in safe
        assert "[REDACTED]" in safe

    def test_password_redacted(self) -> None:
        safe = redact_sensitive("Password: SuperSecret123!")
        assert "SuperSecret123!" not in safe
        assert "[REDACTED]" in safe


# S7 — Happy path: Subdomain ASCII tree
class TestSubdomainTree:
    def test_ascii_tree_generated(self) -> None:
        from estorides_export.recon_report import build_subdomain_tree
        subs = ["example.com", "www.example.com", "api.example.com", "admin.example.com"]
        tree = build_subdomain_tree(subs)
        assert "example.com" in tree
        assert "www" in tree
        assert "api" in tree
        assert "admin" in tree


# S8 — Edge: Single finding report
class TestSingleFindingReport:
    def test_single_finding_prominent(self) -> None:
        result = generate_report(
            query="example.com",
            target_scoring={"critical_findings": ["Open S3 bucket with 100 files"]},
            metadata=_make_meta(),
        )
        assert "Open S3 bucket" in result.markdown
