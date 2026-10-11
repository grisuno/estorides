"""
estorides_core.lan_runner
=========================
Real LAN scan execution: passive readers plus one gated active tool.

Readers are injectable so tests never touch the system. The active
path runs only on the lan_policy triple gate through the tool_runner
sandbox with a bounded timeout.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from typing import Any

from . import lan_bundle as _bundle
from . import lan_inventory as _inventory
from . import lan_policy as _policy
from . import lan_scope as _scope

log = logging.getLogger("estorides.lan_runner")

NMAP_TOOL = "nmap"
ARPSCAN_TOOL = "arp-scan"
NMAP_TIMEOUT_S = 120
ARPSCAN_TIMEOUT_S = 60
ARP_READER_TIMEOUT_S = 10
LEASE_READ_CAP_BYTES = 1_048_576

DHCP_LEASE_PATHS = (
    "/var/lib/dhcp/dnsmasq.leases",
    "/var/lib/misc/dnsmasq.leases",
    "/var/lib/dnsmasq/dnsmasq.leases",
)


@dataclass(frozen=True)
class LanScanResult:
    """Outcome of a LAN scan. Refusals and errors are values."""

    refused: bool
    block_reason: str | None
    message: str
    scope_cidr: str | None = None
    devices: list[dict[str, Any]] = field(default_factory=list)
    device_count: int = 0
    entities: list[dict[str, Any]] = field(default_factory=list)
    bundle: dict[str, str] = field(default_factory=dict)
    bundle_errors: list[str] = field(default_factory=list)
    active_used: bool = False
    notice: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def read_arp_table() -> str:
    """Read the local neighbor table. Fail-soft, no probes sent."""
    ip_bin = shutil.which("ip")
    if ip_bin is None:
        return ""
    try:
        proc = subprocess.run(  # noqa: S603
            [ip_bin, "neigh", "show"],
            shell=False,
            capture_output=True,
            timeout=ARP_READER_TIMEOUT_S,
            text=True,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        log.debug("lan_runner: arp reader failed: %s", exc)
        return ""
    if proc.returncode != 0:
        return ""
    return proc.stdout or ""


def read_dhcp_leases() -> str:
    """Read the first readable dnsmasq lease file. Fail-soft."""
    for path in DHCP_LEASE_PATHS:
        try:
            with open(path, "rb") as fh:
                data = fh.read(LEASE_READ_CAP_BYTES)
            return data.decode("utf-8", errors="replace")
        except OSError:
            continue
    return ""


def _default_runner() -> Callable[..., Any]:
    from . import tool_runner as _tr

    return _tr.run_tool


def _attempt(
    runner: Callable[..., Any],
    tool: str,
    args: list[str],
    scope_cidr: str,
    timeout: int,
) -> str | None:
    """One sandboxed tool attempt. Stdout on success, None otherwise."""
    from .tool_runner import ToolErrorResult

    try:
        result = runner(tool, args, target=scope_cidr, timeout=timeout)
    except Exception as exc:
        log.debug("lan_runner: %s raised: %s", tool, exc)
        return None
    if isinstance(result, ToolErrorResult):
        log.debug("lan_runner: %s failed: %s", tool, result.error_code)
        return None
    if getattr(result, "exit_code", -1) != 0:
        return None
    return getattr(result, "stdout", "") or ""


def run_active_scan(
    scope_cidr: str,
    *,
    runner: Callable[..., Any] | None = None,
) -> tuple[str, str]:
    """Run gated active discovery. Returns (tool, stdout).

    nmap host discovery first (greppable stdout), arp-scan fallback.
    `("", "")` when both fail. Never raises.
    """
    _runner = runner or _default_runner()
    out = _attempt(
        _runner, NMAP_TOOL, ["-sn", "-oG", "-", scope_cidr],
        scope_cidr, NMAP_TIMEOUT_S,
    )
    if out is not None:
        return (NMAP_TOOL, out)
    out = _attempt(
        _runner, ARPSCAN_TOOL, [scope_cidr], scope_cidr, ARPSCAN_TIMEOUT_S,
    )
    if out is not None:
        return (ARPSCAN_TOOL, out)
    return ("", "")


def scan(
    scope_cidr: str | None = None,
    *,
    interfaces: list[Any] | None = None,
    consent: Any = False,
    allow_active: Any = False,
    arp_text: str | None = None,
    dhcp_text: str | None = None,
    active_text: str | None = None,
    output_dir: Any = None,
) -> LanScanResult:
    """Execute a LAN scan. Never raises; refusals are values."""
    checkbox = consent is True and allow_active is True
    decision = _policy.evaluate(
        _policy.LanPolicyRequest(
            consent=consent,
            allow_active=allow_active,
            scope_cidr=scope_cidr,
            requested_contact="none",
        )
    )
    if not decision.allowed:
        return LanScanResult(
            refused=True,
            block_reason=decision.block_reason,
            message=decision.message,
        )
    scope = decision.scope_cidr
    if scope is None:
        scope = _scope.default_scope(interfaces or [])
    if scope is None:
        return LanScanResult(
            refused=True,
            block_reason="scope_invalid",
            message="LAN scan blocked: no private local network found. "
            "Type a scope such as 192.168.1.0/24.",
        )
    notice: str | None = None
    active_used = False
    active_sightings: list[dict[str, Any]] = []
    if checkbox:
        if _policy.max_contact_for(True, True) == "active":
            if active_text is not None:
                tool_name, text = ("nmap", active_text)
            else:
                tool_name, text = run_active_scan(scope)
            if tool_name:
                active_sightings = _inventory.parse_active_output(text, tool_name)
            active_used = bool(active_sightings)
            if not active_sightings:
                notice = "Active tool returned no new hosts; passive results shown."
        else:
            notice = (
                "Active scanning unavailable (server policy); running "
                "passive-only. Set ESTORIDES_LAN_ALLOW_ACTIVE=1 to enable "
                "active tools."
            )
    arp = arp_text if arp_text is not None else read_arp_table()
    dhcp = dhcp_text if dhcp_text is not None else read_dhcp_leases()
    sightings = _inventory.parse_arp_table(arp) + _inventory.parse_dhcp_leases(dhcp)
    sightings += active_sightings
    try:
        devices = _inventory.merge_devices(sightings)
    except Exception as exc:
        log.debug("lan_runner: merge failed: %s", exc)
        devices = []
    entities: list[dict[str, Any]] = []
    for dev in devices:
        try:
            entities.extend(_inventory.device_to_entities(dev))
        except Exception as exc:
            log.debug("lan_runner: entity build failed: %s", exc)
    bundle_paths: dict[str, str] = {}
    bundle_errors: list[str] = []
    try:
        written = _bundle.write_bundle(
            devices, output_dir=output_dir, stem="lan", scope_cidr=scope,
        )
        bundle_paths = dict(written.paths)
        bundle_errors = list(written.errors)
    except Exception as exc:
        bundle_errors = [f"bundle failed: {exc}"]
    device_dicts = [d.to_dict() for d in devices]
    count = len(device_dicts)
    if count == 0:
        message = "LAN scan complete: no devices found in scope."
    elif active_used:
        message = f"LAN scan complete: {count} device(s) (passive plus active)."
    else:
        message = f"LAN scan complete: {count} device(s) (passive)."
    return LanScanResult(
        refused=False,
        block_reason=None,
        message=message,
        scope_cidr=scope,
        devices=device_dicts,
        device_count=count,
        entities=entities,
        bundle=bundle_paths,
        bundle_errors=bundle_errors,
        active_used=active_used,
        notice=notice,
    )
