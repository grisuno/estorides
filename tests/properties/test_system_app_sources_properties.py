"""Property-based invariants for estorides_core.system_app_sources.

Hypothesis replaces libFuzzer/AFL. >= 1000 random examples per property.
Run from the project root::

    .venv/bin/pytest tests/properties/test_system_app_sources_properties.py -v
"""
from __future__ import annotations

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from estorides_core.system_app_sources import (
    TOOL_PARSER_NAMES,
    _read_capped,
    parse_tool_output,
    render_args,
)

safe_alpha_st = st.characters(
    whitelist_categories=("Lu", "Ll", "Nd"),
    whitelist_characters="-._/@+",
)

inject_char_st = st.sampled_from([";", "|", "`", "$", "(", ")", "\n", "\r"])


# P1 · registered tool parsers never raise on arbitrary text; output is a list.
@given(
    parser_name=st.sampled_from(TOOL_PARSER_NAMES),
    blob=st.one_of(
        st.text(max_size=2000),
        st.binary(max_size=2000).map(lambda b: b.decode("utf-8", errors="replace")),
    ),
)
@settings(max_examples=1000, deadline=None, suppress_health_check=(HealthCheck.too_slow,))
def test_tool_parsers_never_raise(parser_name: str, blob: str) -> None:
    from estorides_core.parsers import get_parser

    parser = get_parser(parser_name)
    out = parser(blob)
    assert isinstance(out, list), f"{parser_name} returned {type(out)}"


# P2 · render_args never crashes and never emits metachars for safe inputs;
#      placeholders are substituted verbatim.
@given(
    args=st.lists(
        st.text(alphabet=safe_alpha_st, min_size=1, max_size=24), min_size=0, max_size=8
    ),
    query=st.text(alphabet=safe_alpha_st, min_size=1, max_size=64),
    outdir=st.text(alphabet=safe_alpha_st, min_size=1, max_size=64),
)
@settings(max_examples=1000, deadline=None)
def test_render_args_safe_inputs_no_metachars(
    args: list[str], query: str, outdir: str
) -> None:
    rendered = render_args(args, query, outdir)
    assert all(isinstance(a, str) for a in rendered)
    for a in rendered:
        for bad in (";", "|", "`", "$", "(", ")", "\n", "\r"):
            assert bad not in a, f"metachar {bad!r} in {a!r}"


@given(
    query=st.text(max_size=64),
    outdir=st.text(max_size=64),
)
@settings(max_examples=1000, deadline=None)
def test_render_args_substitution_is_verbatim(query: str, outdir: str) -> None:
    rendered = render_args(["{query}", "q={query}", "{outdir}/f"], query, outdir)
    assert rendered[0] == query
    assert rendered[1] == f"q={query}"
    assert rendered[2] == f"{outdir}/f"


# P3 · capped file reads never exceed the cap (plus decode slack).
@given(
    blob=st.binary(min_size=0, max_size=64 * 1024),
    cap=st.integers(min_value=1, max_value=4096),
)
@settings(max_examples=1000, deadline=None, suppress_health_check=(HealthCheck.too_slow,))
def test_read_capped_respects_limit(blob: bytes, cap: int) -> None:
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False, prefix="estorides_prop_") as fh:
        fh.write(blob)
        path = fh.name
    try:
        text = _read_capped(path, cap)
        assert len(text) <= cap + 4, f"{len(text)} > {cap + 4}"
    finally:
        import os

        os.unlink(path)


# P4 · parse_tool_output never raises, always returns a list, even with
#      unknown parser names and hostile payloads.
@given(
    parser_name=st.one_of(
        st.sampled_from(TOOL_PARSER_NAMES), st.text(min_size=1, max_size=32)
    ),
    data=st.one_of(
        st.text(max_size=2000),
        st.binary(max_size=2000).map(lambda b: b.decode("utf-8", errors="replace")),
    ),
)
@settings(max_examples=1000, deadline=None, suppress_health_check=(HealthCheck.too_slow,))
def test_parse_tool_output_never_raises(parser_name: str, data: str) -> None:
    out = parse_tool_output("prop_source", parser_name, data, fallback_text=data)
    assert isinstance(out, list)


# P5 · adversarial queries are always caught at the runner boundary:
#      render_args is verbatim (P2), so a metachar-bearing query must
#      produce an arg that _check_injection rejects.
@given(
    prefix=st.text(alphabet=safe_alpha_st, min_size=0, max_size=8),
    bad=inject_char_st,
    suffix=st.text(alphabet=safe_alpha_st, min_size=0, max_size=8),
)
@settings(max_examples=1000, deadline=None)
def test_adversarial_query_rejected_at_runner_boundary(
    prefix: str, bad: str, suffix: str
) -> None:
    import pytest

    from estorides_core.tool_runner import ToolInjectionError, _check_injection

    query = f"{prefix}{bad}{suffix}"
    rendered = render_args(["{query}", "--x"], query, "/out")
    with pytest.raises(ToolInjectionError):
        _check_injection(rendered)
