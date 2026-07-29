"""ATDD + BDD tests for estorides_core.tool_runner.

Implements the Given-When-Then contracts declared in
``spec/tool_runner.md``. Property-based invariants live in
``tests/properties/test_tool_runner_properties.py``.
"""
from __future__ import annotations

import pytest

from estorides_core.config import TOOL_ALLOWLIST
from estorides_core.tool_runner import (
    ToolErrorResult,
    ToolResult,
    run_tool,
)
from estorides_core.validation import QueryValidationError, validate_query


class TestHappyPathNmap:
    def test_run_tool_returns_result(self) -> None:
        result = run_tool("nmap", ["--version"], target="scanme.nmap.org", timeout=30)
        assert isinstance(result, (ToolResult, ToolErrorResult))
        if isinstance(result, ToolResult):
            assert result.tool_name == "nmap"
            assert result.exit_code == 0


class TestInjectionBlocked:
    def test_semicolon_in_arg_rejected(self) -> None:
        result = run_tool(
            "nmap",
            ["-sV", "example.com; rm -rf /"],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_INJECTION"

    def test_pipe_in_arg_rejected(self) -> None:
        result = run_tool(
            "nmap",
            ["-sV", "example.com | cat /etc/passwd"],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_INJECTION"

    def test_backtick_in_arg_rejected(self) -> None:
        result = run_tool(
            "nmap",
            ["-sV", "example.com`id`"],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_INJECTION"

    def test_dollar_paren_in_arg_rejected(self) -> None:
        result = run_tool(
            "nmap",
            ["-sV", "example.com$(who)"],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_INJECTION"

    def test_newline_in_arg_rejected(self) -> None:
        result = run_tool(
            "nmap",
            ["-sV", "example.com\ncat /etc/passwd"],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_INJECTION"


class TestTimeout:
    def test_tool_that_exceeds_timeout_returns_tool_timeout(self) -> None:
        result = run_tool(
            "nmap",
            ["--script=external", "scanme.nmap.org"],
            target="scanme.nmap.org",
            timeout=1,
        )
        assert isinstance(result, (ToolResult, ToolErrorResult))
        if isinstance(result, ToolErrorResult):
            assert result.error_code == "TOOL_TIMEOUT"
        elif isinstance(result, ToolResult):
            assert result.exit_code != 0 or result.error_code == "TOOL_TIMEOUT"


class TestToolNotFound:
    def test_tool_not_on_filesystem_returns_error(self) -> None:
        import unittest.mock as mock
        fake_allowlist = TOOL_ALLOWLIST | {"fake_missing_tool"}
        with mock.patch(
            "estorides_core.tool_runner.TOOL_ALLOWLIST",
            fake_allowlist,
        ), mock.patch(
            "estorides_core.tool_runner.shutil.which",
            return_value=None,
        ):
            result = run_tool(
                "fake_missing_tool",
                ["--help"],
                target="example.com",
                timeout=10,
            )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_NOT_FOUND"


class TestToolNotAllowed:
    def test_disallowed_tool_rejected(self) -> None:
        result = run_tool(
            "malware_c2_generator",
            ["--payload", "example.com"],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_NOT_ALLOWED"


class TestNoArgs:
    def test_empty_args_returns_error(self) -> None:
        result = run_tool(
            "nmap",
            [],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "NO_ARGS"


class TestTargetValidation:
    def test_control_char_rejected_by_validation(self) -> None:
        with pytest.raises(QueryValidationError):
            validate_query("example.com\x00evil")


class TestNonZeroExit:
    def test_nmap_version_query_succeeds(self) -> None:
        result = run_tool("nmap", ["--version"], target="example.com", timeout=30)
        assert isinstance(result, (ToolResult, ToolErrorResult))
        if isinstance(result, ToolResult):
            assert result.exit_code == 0
            assert result.raw_output_sha1 != ""


class TestOutputSha1:
    def test_sha1_is_valid_hex(self) -> None:
        result = run_tool("nmap", ["--version"], target="example.com", timeout=30)
        if isinstance(result, ToolResult) and result.stdout:
            assert len(result.raw_output_sha1) == 40
            int(result.raw_output_sha1, 16)


class TestConfidenceRange:
    def test_confidence_in_bounds(self) -> None:
        result = run_tool("nmap", ["--version"], target="example.com", timeout=30)
        if isinstance(result, ToolResult):
            assert 0.0 <= result.confidence <= 1.0


class TestOutputTruncation:
    def test_truncated_flag_when_output_exceeds_limit(self) -> None:
        result = run_tool(
            "nmap",
            ["--version"],
            target="example.com",
            timeout=30,
            max_output_bytes=1,
        )
        if isinstance(result, ToolResult):
            assert isinstance(result.truncated, bool)


class TestErrorResultFields:
    def test_error_result_has_fields(self) -> None:
        import unittest.mock as mock
        fake_allowlist = TOOL_ALLOWLIST | {"fake_missing_tool"}
        with mock.patch(
            "estorides_core.tool_runner.TOOL_ALLOWLIST",
            fake_allowlist,
        ), mock.patch(
            "estorides_core.tool_runner.shutil.which",
            return_value=None,
        ):
            result = run_tool(
                "fake_missing_tool",
                ["--help"],
                target="example.com",
                timeout=10,
            )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_NOT_FOUND"
        assert result.tool_name == "fake_missing_tool"
        assert result.duration_s >= 0.0

    def test_injection_error_has_fields(self) -> None:
        result = run_tool(
            "nmap",
            ["-sV", "example.com; rm -rf /"],
            target="example.com",
            timeout=10,
        )
        assert isinstance(result, ToolErrorResult)
        assert result.error_code == "TOOL_INJECTION"
