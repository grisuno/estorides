from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any

from .tool_runner import ToolErrorResult, run_tool

log = logging.getLogger("estorides.active_recon")


@dataclass
class NmapResult:
    success: bool
    exit_code: int
    hosts: list[dict[str, Any]]
    open_ports: list[dict[str, Any]]
    services: list[dict[str, Any]]
    entities: list[dict[str, Any]]
    raw_output: str
    confidence: float
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_entities(self) -> list[dict[str, Any]]:
        return self.entities


@dataclass
class NiktoResult:
    success: bool
    exit_code: int
    findings: list[dict[str, Any]]
    entities: list[dict[str, Any]]
    raw_output: str
    confidence: float
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_entities(self) -> list[dict[str, Any]]:
        return self.entities


@dataclass
class SqlmapResult:
    success: bool
    exit_code: int
    vulnerabilities: list[dict[str, Any]]
    entities: list[dict[str, Any]]
    raw_output: str
    confidence: float
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_entities(self) -> list[dict[str, Any]]:
        return self.entities


@dataclass
class DnsreconResult:
    success: bool
    exit_code: int
    subdomains: list[dict[str, Any]]
    mx_records: list[dict[str, Any]]
    ns_records: list[dict[str, Any]]
    entities: list[dict[str, Any]]
    raw_output: str
    confidence: float
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_entities(self) -> list[dict[str, Any]]:
        return self.entities


@dataclass
class TheHarvesterResult:
    success: bool
    exit_code: int
    emails: list[dict[str, Any]]
    hosts: list[dict[str, Any]]
    entities: list[dict[str, Any]]
    raw_output: str
    confidence: float
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_entities(self) -> list[dict[str, Any]]:
        return self.entities


def _parse_nmap_stdout(stdout: str, tool_name: str) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    current_host: dict[str, Any] | None = None
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Nmap scan report for"):
            host_val = stripped.replace("Nmap scan report for ", "").strip()
            current_host = {"host": host_val, "type": "domain", "source": tool_name}
            entities.append(current_host)
        elif stripped.startswith("Host is up"):
            if current_host is not None:
                current_host["status"] = "up"
        elif "open" in stripped and "/" in stripped:
            port_info = {
                "port_line": stripped,
                "source": tool_name,
            }
            entities.append(port_info)
    return entities


def _parse_nikto_stdout(stdout: str, tool_name: str) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("+") or stripped.startswith("-"):
            continue
        if "+" in stripped:
            parts = stripped.split("+")
            if len(parts) >= 2:
                entities.append(
                    {
                        "finding": parts[1].strip(),
                        "type": "web_finding",
                        "source": tool_name,
                    }
                )
    return entities


def _parse_sqlmap_stdout(stdout: str, tool_name: str) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if "parameter" in stripped.lower() and "injectable" in stripped.lower():
            entities.append(
                {
                    "finding": stripped,
                    "type": "sqli_finding",
                    "source": tool_name,
                }
            )
        elif "sqlmap" in stripped.lower() and any(
            kw in stripped.lower() for kw in ["GET", "POST", "Cookie", "Referer"]
        ):
            entities.append(
                {
                    "finding": stripped,
                    "type": "sqli_parameter",
                    "source": tool_name,
                }
            )
    return entities


def _parse_dnsrecon_stdout(stdout: str, tool_name: str) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if "[" in stripped and "]" in stripped:
            entities.append(
                {
                    "record": stripped,
                    "type": "dns_record",
                    "source": tool_name,
                }
            )
    return entities


def _parse_harvester_stdout(stdout: str, tool_name: str) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if "@" in stripped and "." in stripped.split("@")[-1]:
            entities.append(
                {
                    "email": stripped,
                    "type": "email",
                    "source": tool_name,
                }
            )
        elif stripped.startswith("http") or stripped.startswith("www"):
            entities.append(
                {
                    "url": stripped,
                    "type": "url",
                    "source": tool_name,
                }
            )
    return entities


def run_nmap(target: str, args: list[str] | None = None) -> NmapResult | ToolErrorResult:
    default_args = ["-sV", "-T4", "-p", "22,80,443", target]
    cmd_args = args if args is not None else default_args
    result = run_tool("nmap", cmd_args, target=target, timeout=300)
    if isinstance(result, ToolErrorResult):
        return NmapResult(
                success=False,
                exit_code=result.exit_code or -1,
                hosts=[],
                open_ports=[],
                services=[],
                entities=[],
                raw_output=result.message,
                confidence=0.0,
                error=result.message,
            )
    entities = _parse_nmap_stdout(result.stdout, "nmap") or result.parsed_entities
    return NmapResult(
        success=result.exit_code == 0,
        exit_code=result.exit_code,
        hosts=[e for e in entities if e.get("type") == "domain" or e.get("type") == "ipv4"],
        open_ports=[e for e in entities if "port_line" in e],
        services=[e for e in entities if "service" in e.get("type", "")],
        entities=entities,
        raw_output=result.stdout,
        confidence=result.confidence,
        error=result.error_message,
    )


def run_nikto(target: str, args: list[str] | None = None) -> NiktoResult | ToolErrorResult:
    default_args = ["-h", target]
    cmd_args = args if args is not None else default_args
    result = run_tool("nikto", cmd_args, target=target, timeout=300)
    if isinstance(result, ToolErrorResult):
        return NiktoResult(
                success=False,
                exit_code=result.exit_code or -1,
                findings=[],
                entities=[],
                raw_output=result.message,
                confidence=0.0,
                error=result.message,
            )
    entities = _parse_nikto_stdout(result.stdout, "nikto") or result.parsed_entities
    return NiktoResult(
        success=result.exit_code == 0,
        exit_code=result.exit_code,
        findings=entities,
        entities=entities,
        raw_output=result.stdout,
        confidence=result.confidence,
        error=result.error_message,
    )


def run_sqlmap(target: str, args: list[str] | None = None) -> SqlmapResult | ToolErrorResult:
    default_args = ["-u", target, "--batch", "--level=3", "--risk=2"]
    cmd_args = args if args is not None else default_args
    result = run_tool("sqlmap", cmd_args, target=target, timeout=300)
    if isinstance(result, ToolErrorResult):
        return SqlmapResult(
                success=False,
                exit_code=result.exit_code or -1,
                vulnerabilities=[],
                entities=[],
                raw_output=result.message,
                confidence=0.0,
                error=result.message,
            )
    entities = _parse_sqlmap_stdout(result.stdout, "sqlmap") or result.parsed_entities
    return SqlmapResult(
        success=result.exit_code == 0,
        exit_code=result.exit_code,
        vulnerabilities=entities,
        entities=entities,
        raw_output=result.stdout,
        confidence=result.confidence,
        error=result.error_message,
    )


def run_dnsrecon(target: str, args: list[str] | None = None) -> DnsreconResult | ToolErrorResult:
    default_args = ["-d", target, "-t", "std"]
    cmd_args = args if args is not None else default_args
    result = run_tool("dnsrecon", cmd_args, target=target, timeout=300)
    if isinstance(result, ToolErrorResult):
        return DnsreconResult(
                success=False,
                exit_code=result.exit_code or -1,
                subdomains=[],
                mx_records=[],
                ns_records=[],
                entities=[],
                raw_output=result.message,
                confidence=0.0,
                error=result.message,
            )
    entities = _parse_dnsrecon_stdout(result.stdout, "dnsrecon") or result.parsed_entities
    return DnsreconResult(
        success=result.exit_code == 0,
        exit_code=result.exit_code,
        subdomains=[],
        mx_records=[],
        ns_records=[],
        entities=entities,
        raw_output=result.stdout,
        confidence=result.confidence,
        error=result.error_message,
    )


def run_theHarvester(target: str, args: list[str] | None = None) -> TheHarvesterResult | ToolErrorResult:
    default_args = ["-d", target, "-b", "all"]
    cmd_args = args if args is not None else default_args
    result = run_tool("theHarvester", cmd_args, target=target, timeout=300)
    if isinstance(result, ToolErrorResult):
        return TheHarvesterResult(
                success=False,
                exit_code=result.exit_code or -1,
                emails=[],
                hosts=[],
                entities=[],
                raw_output=result.message,
                confidence=0.0,
                error=result.message,
            )
    entities = _parse_harvester_stdout(result.stdout, "theHarvester") or result.parsed_entities
    return TheHarvesterResult(
        success=result.exit_code == 0,
        exit_code=result.exit_code,
        emails=[e for e in entities if e.get("type") == "email"],
        hosts=[e for e in entities if e.get("type") == "url"],
        entities=entities,
        raw_output=result.stdout,
        confidence=result.confidence,
        error=result.error_message,
    )


TOOL_MAP: dict[str, Any] = {
    "nmap": run_nmap,
    "nikto": run_nikto,
    "sqlmap": run_sqlmap,
    "dnsrecon": run_dnsrecon,
    "theHarvester": run_theHarvester,
}
