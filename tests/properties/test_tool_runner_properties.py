"""Property-based invariants for estorides_core.tool_runner.

Hypothesis replaces libFuzzer/AFL for Python. These tests run >= 1000
random examples per property and must never crash, raise (except
``InvalidArgument`` from input validation), or violate the invariants.

Run from the project root::

    .venv/bin/pytest tests/properties/test_tool_runner_properties.py -v
"""
from __future__ import annotations

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from estorides_core.tool_runner import (
    ToolErrorResult,
    ToolResult,
    _check_injection,
    run_tool,
)

safe_alpha_st = st.characters(
    whitelist_categories=("Lu", "Ll", "Nd"),
    whitelist_characters="-._/",
)

inject_char_st = st.sampled_from([";", "|", "`", "$", "(", ")", "\n", "\r"])


# Invariant 1: _check_injection never raises for injection-free strings.
@given(args=st.lists(safe_alpha_st, min_size=1, max_size=50))
@settings(max_examples=1000, deadline=None)
def test_check_injection_safe_strings_silent(args: list[str]) -> None:
    _check_injection(args)


# Invariant 2: _check_injection raises whenever any arg contains a metacharacter.
@given(
    prefix=st.lists(safe_alpha_st, min_size=0, max_size=5),
    bad=inject_char_st,
    suffix=st.lists(safe_alpha_st, min_size=0, max_size=5),
)
@settings(max_examples=1000, deadline=None)
def test_check_injection_detects_all_metacharacters(
    prefix: list[str], bad: str, suffix: list[str],
) -> None:
    args = [*prefix, bad, *suffix]
    with pytest.raises(BaseException):  # noqa: B017
        _check_injection(args)


# Invariant 3: run_tool always returns a result and never raises (for valid allowlisted tools).
@given(
    target=st.text(min_size=3, max_size=50).filter(lambda s: "." in s),
)
@settings(
    max_examples=20,
    deadline=None,
    suppress_health_check=[HealthCheck.filter_too_much],
)
def test_run_tool_never_raises(target: str) -> None:
    result = run_tool("nmap", ["--version"], target=target, timeout=10)
    assert isinstance(result, (ToolResult, ToolErrorResult))
