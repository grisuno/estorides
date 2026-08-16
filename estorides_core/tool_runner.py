from __future__ import annotations

import hashlib
import logging
import shutil
import subprocess
from dataclasses import asdict, dataclass
from typing import Any

from .config import TOOL_ALLOWLIST, TOOL_MAX_OUTPUT_BYTES, TOOL_TIMEOUT

log = logging.getLogger("estorides.tool_runner")

SHELL_METACHAR_RE = __import__("re").compile(r"[;|`$()\n\r]")


class ToolError(Exception):
    pass


class ToolNotAllowedError(ToolError):
    pass


class ToolInjectionError(ToolError):
    pass


class ToolNotFoundError(ToolError):
    pass


class ToolTimeoutError(ToolError):
    pass


@dataclass(frozen=True)
class ToolResult:
    tool_name: str
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float
    parsed_entities: list[dict[str, Any]]
    confidence: float
    raw_output_sha1: str
    truncated: bool = False
    error_code: str | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["truncated"] = self.truncated
        d["error_code"] = self.error_code
        d["error_message"] = self.error_message
        return d

    @classmethod
    def from_failure(
        cls,
        tool_name: str,
        error_code: str,
        error_message: str,
        duration_s: float,
        exit_code: int | None = None,
        stdout: str = "",
        stderr: str = "",
        parsed_entities: list[dict[str, Any]] | None = None,
    ) -> ToolResult:
        return cls(
            tool_name=tool_name,
            exit_code=exit_code if exit_code is not None else -1,
            stdout=stdout,
            stderr=stderr,
            duration_s=duration_s,
            parsed_entities=parsed_entities or [],
            confidence=0.0,
            raw_output_sha1="",
            truncated=False,
            error_code=error_code,
            error_message=error_message,
        )


@dataclass(frozen=True)
class ToolErrorResult:
    tool_name: str
    error_code: str
    message: str
    exit_code: int | None
    duration_s: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _check_injection(args: list[str]) -> None:
    for arg in args:
        if not isinstance(arg, str):
            raise ToolInjectionError(f"arg is not a string: {arg!r}")
        if SHELL_METACHAR_RE.search(arg):
            raise ToolInjectionError(
                f"shell metacharacter in arg: {arg!r}"
            )


def _resolve_binary(tool_name: str) -> str:
    path = shutil.which(tool_name)
    if path is None:
        raise ToolNotFoundError(f"binary not found: {tool_name}")
    return path


def _check_allowlist(tool_name: str) -> None:
    if tool_name not in TOOL_ALLOWLIST:
        raise ToolNotAllowedError(
            f"tool not in allowlist: {tool_name}"
        )


def _parse_entities_generic(stdout: str, tool_name: str) -> list[dict[str, Any]]:
    from .entity_extraction import detect_query_type
    entities: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for pattern in (
            r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
            r"\b(?:[A-Fa-f0-9]{1,4}:){2,7}[A-Fa-f0-9]{1,4}\b",
            r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[A-Za-z]{2,24}\b",
            r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,24}\b",
            r"\b(?:AKIA|ghp|ghs|gho)_[A-Za-z0-9]{20,}\b",
        ):
            for m in __import__("re", fromlist=["compile"]).finditer(pattern, line):
                val = m.group(0)
                qtype = detect_query_type(val)
                if qtype:
                    entities.append(
                        {
                            "type": qtype,
                            "value": val,
                            "confidence": 0.5,
                            "source": tool_name,
                            "raw": line,
                        }
                    )
    return entities


# Public alias: system_app_sources reuses this scanner as the fallback
# parser for tool output whose declared parser failed or returned nothing.
parse_entities_generic = _parse_entities_generic


def run_tool(
    tool_name: str,
    args: list[str],
    target: str = "",
    timeout: int | None = None,
    max_output_bytes: int = TOOL_MAX_OUTPUT_BYTES,
    cwd: str | None = None,
) -> ToolResult | ToolErrorResult:
    start = __import__("time").monotonic()

    try:
        _check_allowlist(tool_name)
    except ToolNotAllowedError as exc:
        log.warning("tool not allowed: %s", exc)
        return ToolErrorResult(
            tool_name=tool_name,
            error_code="TOOL_NOT_ALLOWED",
            message=str(exc),
            exit_code=None,
            duration_s=__import__("time").monotonic() - start,
        )

    if not args:
        log.warning("tool %s called with empty args", tool_name)
        return ToolErrorResult(
            tool_name=tool_name,
            error_code="NO_ARGS",
            message="no arguments provided for tool",
            exit_code=None,
            duration_s=__import__("time").monotonic() - start,
        )

    try:
        _check_injection(args)
    except ToolInjectionError as exc:
        log.warning("injection detected in args for %s: %s", tool_name, exc)
        return ToolErrorResult(
            tool_name=tool_name,
            error_code="TOOL_INJECTION",
            message=str(exc),
            exit_code=None,
            duration_s=__import__("time").monotonic() - start,
        )

    try:
        binary_path = _resolve_binary(tool_name)
    except ToolNotFoundError as exc:
        log.warning("tool binary not found: %s", exc)
        return ToolErrorResult(
            tool_name=tool_name,
            error_code="TOOL_NOT_FOUND",
            message=str(exc),
            exit_code=None,
            duration_s=__import__("time").monotonic() - start,
        )

    cmd = [binary_path, *list(args)]
    effective_timeout = timeout if timeout is not None else TOOL_TIMEOUT
    effective_timeout = min(effective_timeout, 3600)

    log.info(
        "tool_runner: executing %s (target=%s, timeout=%ds)",
        tool_name,
        target,
        effective_timeout,
    )

    try:
        proc = subprocess.run(  # noqa: S603
            cmd,
            shell=False,
            capture_output=True,
            timeout=effective_timeout,
            text=False,
            cwd=cwd or None,
        )
        duration = __import__("time").monotonic() - start
    except subprocess.TimeoutExpired:
        duration = __import__("time").monotonic() - start
        log.warning(
            "tool_runner: %s timed out after %ds for target=%s",
            tool_name,
            effective_timeout,
            target,
        )
        return ToolErrorResult(
            tool_name=tool_name,
            error_code="TOOL_TIMEOUT",
            message=f"tool exceeded {effective_timeout}s timeout",
            exit_code=None,
            duration_s=duration,
        )
    except OSError as exc:
        duration = __import__("time").monotonic() - start
        log.warning("tool_runner: OSError for %s: %s", tool_name, exc)
        return ToolErrorResult(
            tool_name=tool_name,
            error_code="TOOL_NOT_FOUND",
            message=str(exc),
            exit_code=None,
            duration_s=duration,
        )

    stdout_raw = proc.stdout or b""
    stderr_raw = proc.stderr or b""

    truncated = False
    if len(stdout_raw) > max_output_bytes:
        stdout_raw = stdout_raw[:max_output_bytes]
        truncated = True
        log.warning(
            "tool_runner: %s stdout truncated to %d bytes for target=%s",
            tool_name,
            max_output_bytes,
            target,
        )
    if len(stderr_raw) > max_output_bytes:
        stderr_raw = stderr_raw[:max_output_bytes]
        truncated = True

    try:
        stdout_str = stdout_raw.decode("utf-8", errors="replace")
        stderr_str = stderr_raw.decode("utf-8", errors="replace")
    except Exception:
        stdout_str = ""
        stderr_str = ""

    try:
        sha1 = hashlib.sha1(stdout_raw).hexdigest()  # nosec B324
    except Exception:
        sha1 = ""

    if proc.returncode != 0:
        log.warning(
            "tool_runner: %s exited with code %d for target=%s (duration=%.2fs)",
            tool_name,
            proc.returncode,
            target,
            duration,
        )

    entities = _parse_entities_generic(stdout_str, tool_name)
    confidence = min(1.0, len(entities) * 0.3) if entities else 0.0

    log.info(
        "tool_runner: %s finished for target=%s (exit=%d, entities=%d, sha1=%s)",
        tool_name,
        target,
        proc.returncode,
        len(entities),
        sha1,
    )

    return ToolResult(
        tool_name=tool_name,
        exit_code=proc.returncode,
        stdout=stdout_str,
        stderr=stderr_str,
        duration_s=duration,
        parsed_entities=entities,
        confidence=confidence,
        raw_output_sha1=sha1,
        truncated=truncated,
        error_code=None if proc.returncode == 0 else "TOOL_CRASH",
        error_message=stderr_str.strip() or None if proc.returncode != 0 else None,
    )
