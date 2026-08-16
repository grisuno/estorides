"""
estorides_core.system_app_sources
=================================
Kali OSINT CLI tools as first-class sources (`kind: system_app`).

A system_app source is a YAML-declared local binary executed through the
existing :mod:`estorides_core.tool_runner` sandbox (allowlist, no shell,
injection blocking, timeouts, output caps) whose output is parsed and fed
into the **same** aggregation pipeline as HTTP sources: observations →
entity extraction → fusion → reliability scoring → recon tiers.

The YAML schema differs from HTTP sources (`tool.binary` + `tool.args`
instead of `tool.url` + `tool.params`) — one registry, two origin kinds,
zero special-casing downstream.

Public surface:

    KIND_SYSTEM_APP        "system_app" origin kind constant
    SystemAppResult        frozen dataclass, JSON-serialisable
    is_system_app          kind/binary predicate
    tool_available         shutil.which wrapper (monkeypatchable)
    render_args            {query}/{outdir} template substitution, pure
    parse_tool_output      parser dispatch with never-raise contract
    execute                full run: sandbox + parse + audit metadata
    TOOL_PARSER_NAMES      registered tool-output parsers (for fuzzing)
"""
from __future__ import annotations

import json
import logging
import platform
import re
import shutil
import tempfile
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .config import TOOL_ALLOWLIST, TOOL_MAX_OUTPUT_BYTES
from .parsers import get_parser, register_parser
from .tool_runner import ToolErrorResult, run_tool

log = logging.getLogger("estorides.system_app_sources")

KIND_SYSTEM_APP: str = "system_app"
KIND_HTTP_API: str = "http_api"
VALID_KINDS: frozenset[str] = frozenset({KIND_SYSTEM_APP, KIND_HTTP_API})
VALID_OUTPUT_FORMATS: frozenset[str] = frozenset({"json", "text", "lines"})

_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")


# ------------------------------------------------------------------ result ----
@dataclass(frozen=True)
class SystemAppResult:
    """Normalised outcome of one system_app tool invocation.

    Mirrors the contract in ``spec/system_app_sources.md``: failures are
    values, never exceptions."""

    source_name: str
    tool_name: str
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float
    parsed: Any = None
    raw_output_sha1: str = ""
    truncated: bool = False
    error_code: str | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------- helpers ----
def is_system_app(source: Any) -> bool:
    """True when a source dict is a system_app (or has a binary tool)."""
    if not isinstance(source, dict):
        return False
    if source.get("kind") == KIND_SYSTEM_APP:
        return True
    tool = source.get("tool")
    return isinstance(tool, dict) and bool(tool.get("binary"))


def tool_available(binary: str) -> bool:
    """Resolve a binary on the filesystem (shutil.which)."""
    return shutil.which(binary) is not None


def render_args(args: list[Any], query: str, outdir: str) -> list[str]:
    """Substitute ``{query}``/``{outdir}`` placeholders in an args template.

    Unknown placeholders are left verbatim (same contract as the HTTP
    ``_safe_format``). Non-string template elements are programmer error
    and raise ``ValueError`` — a silently stringified int is a typo that
    must be caught at source-authoring time, not at exec time.
    """
    rendered: list[str] = []
    for arg in args:
        if not isinstance(arg, str):
            raise ValueError(f"tool.args element is not a string: {arg!r}")

        def repl(m: re.Match[str]) -> str:
            placeholder = m.group(1)
            if placeholder == "query":
                return query
            if placeholder == "outdir":
                return outdir
            return m.group(0)

        rendered.append(_PLACEHOLDER_RE.sub(repl, arg))
    return rendered


def _read_capped(path: str, cap: int) -> str:
    """Read a file, capped at ``cap`` bytes, UTF-8 with replacement."""
    try:
        with open(path, "rb") as fh:
            data = fh.read(cap)
    except OSError:
        return ""
    return data.decode("utf-8", errors="replace")


def _loads_lenient(text: str) -> Any:
    """Best-effort JSON parse of tool output (tolerates log-prefix noise)."""
    try:
        return json.loads(text)
    except ValueError:
        pass
    idx = text.find("{")
    if idx == -1:
        idx = text.find("[")
    if idx == -1:
        return None
    try:
        obj, _end = json.JSONDecoder().raw_decode(text[idx:])
        return obj
    except ValueError:
        return None


# ------------------------------------------------------------------ parsers ----
def _line_filter_parser(
    *,
    startswith: tuple[str, ...] = (),
    contains: tuple[str, ...] = (),
    regex: str | None = None,
    strip_prefixes: tuple[str, ...] = (),
) -> Callable[[Any], list[str]]:
    """Factory for noise-reducing line parsers (one definition, N tools).

    Keep-lines must match *every* supplied condition; ``strip_prefixes``
    are removed from surviving lines so the operator sees data, not noise.
    """

    rx = re.compile(regex) if regex else None

    def parser(payload: Any) -> list[str]:
        if payload is None:
            return []
        text = payload if isinstance(payload, str) else str(payload)
        out: list[str] = []
        for line in text.splitlines():
            s = line.strip()
            if not s:
                continue
            if startswith and not s.startswith(startswith):
                continue
            if contains and not any(c in s for c in contains):
                continue
            if rx is not None and not rx.search(s):
                continue
            for prefix in strip_prefixes:
                if s.startswith(prefix):
                    s = s[len(prefix):].strip()
            out.append(s)
        return out

    return parser


_HOSTNAME_RE = r"^[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[a-z]{2,}$"


@register_parser("amass_json")
def parse_amass_json(payload: Any) -> list[dict[str, Any]]:
    """amass ``-json`` output: one JSON object per line (DNS + infra)."""
    if not isinstance(payload, str):
        return []
    out: list[dict[str, Any]] = []
    for line in payload.splitlines():
        line = line.strip()
        if not line:
            continue
        obj = _loads_lenient(line)
        if not isinstance(obj, dict):
            continue
        if "ip" in obj and "name" not in obj:
            out.append({"ip": obj["ip"], "asn": obj.get("asn"), "cidr": obj.get("cidr")})
            continue
        addresses = [
            a.get("ip")
            for a in obj.get("addresses", [])
            if isinstance(a, dict) and a.get("ip")
        ]
        out.append(
            {
                "domain": obj.get("name") or obj.get("domain") or "",
                "asn": obj.get("asn"),
                "addresses": addresses,
                "tags": obj.get("tag") or obj.get("tags"),
            }
        )
    return out


@register_parser("maigret_json")
def parse_maigret_json(payload: Any) -> list[dict[str, Any]]:
    """maigret ``--json simple``: one object keyed by site name."""
    if not isinstance(payload, str):
        return []
    obj = _loads_lenient(payload)
    if not isinstance(obj, dict):
        return []
    out: list[dict[str, Any]] = []
    for site, info in obj.items():
        if not isinstance(info, dict) or not info.get("exists"):
            continue
        out.append(
            {
                "site": site,
                "exists": True,
                "url": info.get("url_user") or info.get("url") or "",
            }
        )
    return out


@register_parser("phoneinfoga_json")
def parse_phoneinfoga_json(payload: Any) -> list[Any]:
    """phoneinfoga v2 ``scan``: a single JSON object (possibly after logs)."""
    if not isinstance(payload, str):
        return []
    obj = _loads_lenient(payload)
    if isinstance(obj, dict):
        return [obj]
    if isinstance(obj, list):
        return obj
    return []


@register_parser("sherlock_text")
def parse_sherlock_text(payload: Any) -> list[str]:
    return _line_filter_parser(startswith=("[+]",), strip_prefixes=("[+]",))(payload)


@register_parser("holehe_text")
def parse_holehe_text(payload: Any) -> list[str]:
    return _line_filter_parser(startswith=("[+]",), strip_prefixes=("[+]",))(payload)


@register_parser("wafw00f_text")
def parse_wafw00f_text(payload: Any) -> list[str]:
    return _line_filter_parser(startswith=("[+]",), strip_prefixes=("[+]",))(payload)


@register_parser("sublist3r_lines")
def parse_sublist3r_lines(payload: Any) -> list[str]:
    return _line_filter_parser(regex=_HOSTNAME_RE)(payload)


@register_parser("dnsrecon_text")
def parse_dnsrecon_text(payload: Any) -> list[str]:
    return _line_filter_parser(regex=r"^\s*(?:A|AAAA|CNAME|NS|MX|TXT|PTR|SOA|SRV)\s+\S")(payload)


@register_parser("dnsenum_text")
def parse_dnsenum_text(payload: Any) -> list[str]:
    return _line_filter_parser(
        regex=r"^\S+\s+\d{1,3}(?:\.\d{1,3}){3}\s*$|\s(?:NS|MX|TXT|CNAME)\s+"
    )(payload)


@register_parser("fierce_text")
def parse_fierce_text(payload: Any) -> list[str]:
    return _line_filter_parser(contains=("Found",))(payload)


@register_parser("dmitry_text")
def parse_dmitry_text(payload: Any) -> list[str]:
    return _line_filter_parser(regex=r"Found|@")(payload)


@register_parser("urlcrazy_text")
def parse_urlcrazy_text(payload: Any) -> list[str]:
    return _line_filter_parser(regex=_HOSTNAME_RE)(payload)


@register_parser("metagoofil_text")
def parse_metagoofil_text(payload: Any) -> list[str]:
    return _line_filter_parser(contains=("http", "@"))(payload)


@register_parser("whatweb_text")
def parse_whatweb_text(payload: Any) -> list[str]:
    return _line_filter_parser(startswith=("http",))(payload)


@register_parser("theharvester_text")
def parse_theharvester_text(payload: Any) -> list[str]:
    return _line_filter_parser(regex=r"@|http|^[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")(payload)


@register_parser("usufy_text")
def parse_usufy_text(payload: Any) -> list[str]:
    return _line_filter_parser(contains=("@", "http", "found", "Found"))(payload)


@register_parser("mailfy_text")
def parse_mailfy_text(payload: Any) -> list[str]:
    return _line_filter_parser(contains=("@", "http", "found", "Found"))(payload)


@register_parser("phonefy_text")
def parse_phonefy_text(payload: Any) -> list[str]:
    return _line_filter_parser(contains=("@", "http", "found", "Found"))(payload)


@register_parser("searchfy_text")
def parse_searchfy_text(payload: Any) -> list[str]:
    return _line_filter_parser(contains=("@", "http", "found", "Found"))(payload)


TOOL_PARSER_NAMES: tuple[str, ...] = (
    "amass_json",
    "maigret_json",
    "phoneinfoga_json",
    "sherlock_text",
    "holehe_text",
    "wafw00f_text",
    "sublist3r_lines",
    "dnsrecon_text",
    "dnsenum_text",
    "fierce_text",
    "dmitry_text",
    "urlcrazy_text",
    "metagoofil_text",
    "whatweb_text",
    "theharvester_text",
    "usufy_text",
    "mailfy_text",
    "phonefy_text",
    "searchfy_text",
)


# -------------------------------------------------------------- dispatch ----
def parse_tool_output(
    source_name: str,
    parser_name: str | None,
    data: Any,
    *,
    fallback_text: str = "",
) -> list[Any]:
    """Parse tool output with the declared parser; never raises.

    A parser that returns a non-list is wrapped; an empty/None parse falls
    back to the generic entity scanner over the raw text so a tool with a
    broken/unknown parser still yields entities.
    """
    from .tool_runner import parse_entities_generic

    parser = get_parser(parser_name or "raw_text")
    try:
        parsed = parser(data)
    except Exception as exc:
        log.debug("tool parser %r failed for %s: %s", parser_name, source_name, exc)
        parsed = None
    if parsed is None:
        parsed = []
    elif not isinstance(parsed, list):
        parsed = [parsed]
    if not parsed and fallback_text:
        return parse_entities_generic(fallback_text, source_name)
    return parsed


# --------------------------------------------------------------- execute ----
def execute(
    source: dict[str, Any],
    query: str,
    *,
    timeout: int | None = None,
    max_output_bytes: int = TOOL_MAX_OUTPUT_BYTES,
    _runner: Callable[..., Any] = run_tool,
) -> SystemAppResult:
    """Execute one system_app source through the tool_runner sandbox.

    Failures (missing binary, not allowlisted, wrong platform, injection,
    timeout, crash) are ``SystemAppResult`` values — never exceptions.
    ``{outdir}`` renders into a fresh private TemporaryDirectory that is
    removed after parsing.
    """
    name = str(source.get("name") or "unnamed_source")
    tool = source.get("tool")
    if not isinstance(tool, dict):
        tool = {}
    binary = str(tool.get("binary") or "")
    t0 = time.monotonic()

    def fail(code: str, message: str) -> SystemAppResult:
        return SystemAppResult(
            source_name=name,
            tool_name=binary,
            success=False,
            exit_code=-1,
            stdout="",
            stderr="",
            duration_s=time.monotonic() - t0,
            parsed=None,
            raw_output_sha1="",
            truncated=False,
            error_code=code,
            error_message=message,
        )

    if not binary:
        log.warning("system_app source %s declares no tool.binary", name)
        return fail("NO_BINARY", "source declares no tool.binary")
    if binary not in TOOL_ALLOWLIST:
        log.warning("system_app source %s: tool not allowlisted: %s", name, binary)
        return fail("TOOL_NOT_ALLOWED", f"tool not in allowlist: {binary}")
    if not tool_available(binary):
        log.warning("system_app source %s: binary not found: %s", name, binary)
        return fail("TOOL_NOT_FOUND", f"binary not found on system: {binary}")
    declared_os = str(source.get("os") or "any").strip().lower()
    host_os = platform.system().lower()
    if declared_os != "any" and declared_os != host_os:
        log.warning(
            "system_app source %s declares os=%r but host is %r",
            name, declared_os, host_os,
        )
        return fail(
            "UNSUPPORTED_PLATFORM",
            f"source requires os={declared_os}, host is {host_os}",
        )

    outfile_template = tool.get("output_file")
    with tempfile.TemporaryDirectory(prefix="estorides_tool_") as outdir:
        args = render_args(list(tool.get("args") or []), query, outdir)
        result = _runner(
            binary, args, target=query, timeout=timeout,
            max_output_bytes=max_output_bytes, cwd=outdir,
        )
        if isinstance(result, ToolErrorResult):
            return SystemAppResult(
                source_name=name,
                tool_name=binary,
                success=False,
                exit_code=result.exit_code if result.exit_code is not None else -1,
                stdout="",
                stderr="",
                duration_s=result.duration_s,
                parsed=None,
                raw_output_sha1="",
                truncated=False,
                error_code=result.error_code,
                error_message=result.message,
            )
        stdout = result.stdout
        data: Any = stdout
        if outfile_template:
            rendered_out = render_args([str(outfile_template)], query, outdir)[0]
            if Path(rendered_out).is_file():
                data = _read_capped(rendered_out, max_output_bytes)
        parsed = parse_tool_output(
            name, str(source.get("parser") or ""), data, fallback_text=stdout,
        )
        return SystemAppResult(
            source_name=name,
            tool_name=binary,
            success=result.exit_code == 0,
            exit_code=result.exit_code,
            stdout=stdout,
            stderr=result.stderr,
            duration_s=result.duration_s,
            parsed=parsed,
            raw_output_sha1=result.raw_output_sha1,
            truncated=result.truncated,
            error_code=result.error_code,
            error_message=result.error_message,
        )
