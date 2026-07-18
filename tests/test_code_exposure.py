"""ATDD + BDD tests for estorides_core.code_exposure.

Implements the Given-When-Then contracts declared in
``spec/code_exposure.md``.
"""
from __future__ import annotations

from estorides_core.code_exposure import (
    CodeFinding,
    analyse_findings,
    classify_finding,
    validate_aws_key,
)


# S1 — Happy path: AWS key found
class TestAwsKeyDetection:
    def test_detects_aws_key_as_critical(self) -> None:
        findings = [
            CodeFinding(
                source="github", type="credential",
                file_path="config.py", repository="target-org/app",
                snippet='AWS_KEY="AKIAIOSFODNN7EXAMPLE"',
                matched_pattern="AWS_ACCESS_KEY",
                severity="critical", verified=True,
            )
        ]
        result = analyse_findings(findings)
        assert result.total_findings == 1
        assert result.severity_summary.critical == 1

    def test_validates_aws_key_format(self) -> None:
        assert validate_aws_key("AKIAIOSFODNN7EXAMPLE") is True
        assert validate_aws_key("NOT_A_KEY") is False


# S2 — Edge: No findings
class TestNoFindings:
    def test_empty_when_no_repos(self) -> None:
        result = analyse_findings([])
        assert result.total_findings == 0
        assert result.severity_summary.critical == 0
        assert result.severity_summary.high == 0


# S3 — Error: Rate limited
class TestRateLimited:
    def test_returns_partial_on_rate_limit(self) -> None:
        partial = analyse_findings([], rate_limited=True)
        assert partial.total_findings == 0


# S4 — Security: Internal URL detection
class TestInternalUrlDetection:
    def test_internal_url_is_high_severity(self) -> None:
        finding = classify_finding("https://internal-jenkins.target-org.com/", "github", "config.yaml")
        assert finding.type == "internal_url"
        assert finding.severity == "high"


# S5 — Happy path: .env file detection
class TestEnvFileDetection:
    def test_env_file_is_critical_config(self) -> None:
        finding = classify_finding("DB_PASSWORD=super_secret", "github", ".env")
        assert finding.type == "config"
        assert finding.severity == "critical"


# S6 — Edge: Placeholder credentials
class TestPlaceholderCredentials:
    def test_placeholder_marked_info(self) -> None:
        finding = classify_finding('password = "your-password-here"', "github", "config.py")
        assert finding.severity == "info"

    def test_example_key_marked_info(self) -> None:
        finding = classify_finding("api_key = 'YOUR_API_KEY'", "github", "settings.py")
        assert finding.severity == "info"


# S7 — Happy path: Multi-platform
class TestMultiPlatform:
    def test_aggregates_multi_source(self) -> None:
        findings = [
            CodeFinding("github", "credential", "a", "repo1", "key=abc", "AWS_KEY", "critical", True),
            CodeFinding("gitlab", "credential", "b", "repo2", "key=def", "AWS_KEY", "critical", True),
        ]
        result = analyse_findings(findings)
        assert result.total_findings == 2
        sources = {f.source for f in result.findings}
        assert "github" in sources
        assert "gitlab" in sources


# S8 — Security: Snippet bounded
class TestSnippetBounded:
    def test_snippet_under_200_chars(self) -> None:
        long_line = "SECRET=" + "x" * 10000
        finding = classify_finding(long_line, "github", "config.py")
        assert len(finding.snippet) <= 200


# S9 — Happy path: classify_finding types
class TestClassifyFindingTypes:
    def test_ssh_key_detection(self) -> None:
        finding = classify_finding("-----BEGIN OPENSSH PRIVATE KEY-----", "github", "id_rsa")
        assert finding.type == "credential"
        assert finding.severity == "critical"

    def test_api_key_detection(self) -> None:
        finding = classify_finding("sk_live_abcd1234efgh5678ijkl9012mnop", "github", "config.py")
        assert finding.type == "credential"
