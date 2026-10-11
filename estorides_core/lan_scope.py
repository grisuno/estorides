"""
estorides_core.lan_scope
========================
Private local scope auto-detection.

Pure parsing plus one thin OS reader. The reader inspects local
interface configuration only; it sends no probes.
"""
from __future__ import annotations

import ipaddress
import logging
import re
import shutil
import subprocess
from typing import Any

log = logging.getLogger("estorides.lan_scope")

_IP_LINE_RE = re.compile(r"\binet6?\s+([0-9A-Fa-f.:]+/\d{1,3})\b")


def parse_interface_addr(raw: dict[str, Any] | Any) -> str | None:
    """Normalize one interface address to CIDR, or None when unsafe."""
    if not isinstance(raw, dict):
        return None
    addr = raw.get("address")
    if not isinstance(addr, str) or not addr.strip():
        prefix_raw = raw.get("prefix")
        if prefix_raw is None:
            return None
        return None
    text = addr.strip()
    if "/" not in text:
        prefix = raw.get("prefix")
        try:
            prefix_int = int(prefix)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return None
        text = f"{text}/{prefix_int}"
    try:
        iface = ipaddress.ip_interface(text)
    except ValueError:
        return None
    net = iface.network
    if net.is_loopback or net.is_multicast or net.is_reserved:
        return None
    if isinstance(net, ipaddress.IPv4Network):
        if not net.is_private:
            return None
        if net.prefixlen < 8:
            return None
    else:
        is_ula = str(net.network_address).lower().startswith(("fd", "fc"))
        if not (net.is_private or net.is_link_local or is_ula):
            if not net.is_private:
                return None
        if net.prefixlen < 32:
            return None
    return str(net)


def select_private_cidrs(interfaces: list[Any]) -> list[str]:
    """Keep private CIDRs only, sorted and deduped. Never raises."""
    out: set[str] = set()
    if not isinstance(interfaces, list):
        return []
    for item in interfaces:
        try:
            cidr = parse_interface_addr(item)
        except Exception as exc:
            log.debug("lan_scope: skipping unparsable item: %s", exc)
            continue
        if cidr:
            out.add(cidr)
    return sorted(out)


def default_scope(interfaces: list[Any]) -> str | None:
    """First private CIDR, or None when no private network exists."""
    cidrs = select_private_cidrs(interfaces)
    return cidrs[0] if cidrs else None


def parse_ip_addr_output(text: str) -> list[dict[str, str]]:
    """Parse `ip addr` output into address dicts. Pure, never raises."""
    if not isinstance(text, str) or not text:
        return []
    return [{"address": m.group(1)} for m in _IP_LINE_RE.finditer(text)]


def read_local_interfaces() -> list[dict[str, str]]:
    """Read local interface addresses. Fail-soft, no probes sent."""
    ip_bin = shutil.which("ip")
    if ip_bin is None:
        return []
    found: list[dict[str, str]] = []
    for family in ("inet", "inet6"):
        try:
            proc = subprocess.run(  # noqa: S603
                [ip_bin, "-o", "-f", family, "addr", "show"],
                shell=False,
                capture_output=True,
                timeout=10,
                text=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            log.debug("lan_scope reader failed for %s: %s", family, exc)
            continue
        if proc.returncode != 0:
            continue
        found.extend(parse_ip_addr_output(proc.stdout or ""))
    return found
