"""
estorides_core.lan_inventory
============================
Passive-first LAN device inventory.

Pure parsers for ARP/neighbor tables and DHCP leases plus MAC-keyed
device merging. No sockets, no subprocess, no file reads.
"""
from __future__ import annotations

import ipaddress
import logging
import re
from dataclasses import asdict, dataclass
from typing import Any

log = logging.getLogger("estorides.lan_inventory")

try:
    from defusedxml.ElementTree import fromstring as _xml_fromstring
except ImportError:  # pragma: no cover - declared dependency
    _xml_fromstring = None  # type: ignore[assignment]

_MAC_COLON_RE = re.compile(r"^([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}$")
_MAC_NODOT_RE = re.compile(r"^[0-9a-fA-F]{12}$")
_MAC_DOT_RE = re.compile(r"^([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}$")
_IP_RE = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
_IP6_RE = re.compile(r"\b(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}\b")

PASSIVE_TOOLS = frozenset({"ip-neigh", "dhcp-leases", "mdns-listen", "ssdp-listen"})

ACTIVE_TOOLS = frozenset(
    {
        "nmap",
        "arp-scan",
        "nbtscan",
        "netdiscover",
        "snmpwalk",
        "enum4linux",
        "smbclient",
        "ncat",
        "socat",
        "nikto",
        "sslscan",
        "sslyze",
    }
)


@dataclass(frozen=True)
class LanDevice:
    """One physical host, merged from one or more sightings."""

    device_id: str
    ips: tuple[str, ...] = ()
    mac: str | None = None
    hostnames: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_mac(raw: Any) -> str | None:
    """Normalize MAC to lowercase colon form, or None when invalid."""
    if not isinstance(raw, str):
        return None
    text = raw.strip().lower()
    if _MAC_COLON_RE.match(text):
        return text.replace("-", ":")
    nosep = re.sub(r"[^0-9a-f]", "", text)
    if len(nosep) == 12 and all(c in "0123456789abcdef" for c in nosep):
        return ":".join(nosep[i : i + 2] for i in range(0, 12, 2))
    return None


def _valid_lan_ip(raw: Any) -> str | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        addr = ipaddress.ip_address(raw.strip())
    except ValueError:
        return None
    if addr.is_loopback or addr.is_multicast or addr.is_reserved:
        return None
    if isinstance(addr, ipaddress.IPv4Address) and not addr.is_private:
        return None
    return str(addr)


def parse_arp_table(text: str) -> list[dict[str, Any]]:
    """Parse `ip neigh` or /proc/net/arp text into sightings."""
    if not isinstance(text, str) or not text:
        return []
    out: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        ip_m = _IP_RE.search(line)
        ip6_m = None if ip_m else _IP6_RE.search(line)
        ip_raw = ip_m.group(0) if ip_m else (ip6_m.group(0) if ip6_m else None)
        ip = _valid_lan_ip(ip_raw) if ip_raw else None
        if ip is None:
            continue
        mac: str | None = None
        for token in re.split(r"\s+", line):
            cand = normalize_mac(token)
            if cand:
                mac = cand
                break
        lowered = line.lower()
        if "incomplete" in lowered or " failed" in lowered or lowered.endswith("failed"):
            continue
        out.append({"ip": ip, "mac": mac, "hostname": None, "source": "ip-neigh"})
    return out


def parse_dhcp_leases(text: str) -> list[dict[str, Any]]:
    """Parse dnsmasq lease lines into sightings."""
    if not isinstance(text, str) or not text:
        return []
    out: list[dict[str, Any]] = []
    for line in text.splitlines():
        parts = line.strip().split()
        if len(parts) < 3:
            continue
        mac = normalize_mac(parts[1])
        ip = _valid_lan_ip(parts[2])
        if ip is None:
            continue
        hostname = parts[3].strip() if len(parts) > 3 else ""
        if hostname in ("", "*"):
            hostname = None  # type: ignore[assignment]
        out.append(
            {"ip": ip, "mac": mac, "hostname": hostname, "source": "dhcp-leases"}
        )
    return out


NMAP_XML_MAX_BYTES = 2_097_152

_GREP_HOST_RE = re.compile(
    r"^Host:\s+(\S+)\s+\(([^)]*)\)\s+Status:\s+(\w+)", re.IGNORECASE
)
_GREP_MAC_RE = re.compile(
    r"^Host:\s+(\S+)\s+\([^)]*\)\s+MAC Address:\s+(\S+)(?:\s+\(([^)]*)\))?",
    re.IGNORECASE,
)


def parse_nmap_xml(text: str) -> list[dict[str, Any]]:
    """Parse nmap -oX output into sightings. Fail-soft, size-capped."""
    if not isinstance(text, str) or not text:
        return []
    if len(text.encode("utf-8", errors="ignore")) > NMAP_XML_MAX_BYTES:
        return []
    # Two layers against entity-expansion attacks: documents carrying
    # a DOCTYPE or ENTITY declaration are rejected outright (nmap -oX
    # never emits one), and parsing goes through defusedxml, which caps
    # entity expansion and blocks external entities.
    upper = text.upper()
    if "<!DOCTYPE" in upper or "<!ENTITY" in upper:
        return []
    if _xml_fromstring is None:
        return []
    try:
        root = _xml_fromstring(text)
    except Exception as exc:
        log.debug("lan_inventory: nmap xml parse failed: %s", exc)
        return []
    out: list[dict[str, Any]] = []
    try:
        hosts = root.findall("host")
    except Exception:
        return []
    for host in hosts:
        status = host.find("status")
        if status is None or status.get("state") != "up":
            continue
        ip: str | None = None
        mac: str | None = None
        vendor: str | None = None
        for addr in host.findall("address"):
            addrtype = (addr.get("addrtype") or "").lower()
            if addrtype in ("ipv4", "ipv6") and ip is None:
                ip = _valid_lan_ip(addr.get("addr") or "")
            elif addrtype == "mac" and mac is None:
                mac = normalize_mac(addr.get("addr") or "")
                raw_vendor = (addr.get("vendor") or "").strip()
                if raw_vendor and raw_vendor.lower() != "unknown":
                    vendor = raw_vendor[:64]
        if ip is None:
            continue
        hostname: str | None = None
        hostnames = host.find("hostnames")
        if hostnames is not None:
            for hn in hostnames.findall("hostname"):
                name = (hn.get("name") or "").strip()
                if name and name.lower() not in ("none", "unknown"):
                    hostname = name[:64]
                    break
        out.append(
            {
                "ip": ip,
                "mac": mac,
                "hostname": hostname or vendor,
                "source": "nmap",
            }
        )
    return out


def parse_nmap_grepable(text: str) -> list[dict[str, Any]]:
    """Parse nmap -oG output into sightings. Fail-soft."""
    if not isinstance(text, str) or not text:
        return []
    by_ip: dict[str, dict[str, Any]] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("Host:"):
            continue
        mac_match = _GREP_MAC_RE.match(line)
        if mac_match:
            ip = _valid_lan_ip(mac_match.group(1))
            if ip is None:
                continue
            entry = by_ip.setdefault(
                ip, {"ip": ip, "mac": None, "hostname": None, "source": "nmap"}
            )
            entry["mac"] = normalize_mac(mac_match.group(2)) or entry["mac"]
            vendor = (mac_match.group(3) or "").strip()
            if vendor and vendor.lower() != "unknown" and not entry["hostname"]:
                entry["hostname"] = vendor[:64]
            continue
        host_match = _GREP_HOST_RE.match(line)
        if host_match:
            if host_match.group(3).lower() != "up":
                continue
            ip = _valid_lan_ip(host_match.group(1))
            if ip is None:
                continue
            entry = by_ip.setdefault(
                ip, {"ip": ip, "mac": None, "hostname": None, "source": "nmap"}
            )
            name = host_match.group(2).strip()
            if name and name.lower() not in ("", "none", "unknown"):
                entry["hostname"] = name[:64]
    return list(by_ip.values())


def parse_active_output(text: str, source: str) -> list[dict[str, Any]]:
    """Dispatch active-tool output by format, tagged with source."""
    tag = source.strip() if isinstance(source, str) and source.strip() else "active"
    if not isinstance(text, str) or not text.strip():
        return []
    stripped = text.lstrip()
    if stripped.startswith("<"):
        parsed = parse_nmap_xml(text)
    elif "Host:" in text:
        parsed = parse_nmap_grepable(text)
    else:
        parsed = parse_arp_table(text)
    for sight in parsed:
        sight["source"] = tag[:64]
    return parsed


def merge_devices(sightings: list[dict[str, Any]]) -> list[LanDevice]:
    """Merge sightings by MAC, falling back to IP. Never raises."""
    groups: dict[str, dict[str, Any]] = {}
    if not isinstance(sightings, list):
        return []
    for sight in sightings:
        if not isinstance(sight, dict):
            continue
        mac = normalize_mac(sight.get("mac"))
        ip = _valid_lan_ip(sight.get("ip"))
        if mac is None and ip is None:
            continue
        key = f"mac:{mac}" if mac else f"ip:{ip}"
        group = groups.setdefault(
            key, {"mac": mac, "ips": set(), "hostnames": set(), "sources": set()}
        )
        if ip:
            group["ips"].add(ip)
        host = sight.get("hostname")
        if isinstance(host, str) and host.strip() and host.strip() != "*":
            group["hostnames"].add(host.strip()[:64])
        src = sight.get("source")
        if isinstance(src, str) and src.strip():
            group["sources"].add(src.strip()[:64])
    # Cross-source fold: an ip:-keyed group whose IP also appears in
    # a mac:-keyed group belongs to the same physical host (nmap sees
    # the IP, passive ARP sees the MAC). Fold it in.
    ip_to_mac_key: dict[str, str] = {}
    for key, group in groups.items():
        if key.startswith("mac:"):
            for ip in group["ips"]:
                ip_to_mac_key.setdefault(ip, key)
    for key in list(groups):
        if key.startswith("mac:"):
            continue
        group = groups[key]
        target = next(
            (ip_to_mac_key[ip] for ip in group["ips"] if ip in ip_to_mac_key),
            None,
        )
        if target is None or target not in groups:
            continue
        dest = groups[target]
        dest["ips"] |= group["ips"]
        dest["hostnames"] |= group["hostnames"]
        dest["sources"] |= group["sources"]
        del groups[key]
    devices: list[LanDevice] = []
    for key in sorted(groups):
        group = groups[key]
        devices.append(
            LanDevice(
                device_id=key,
                ips=tuple(sorted(group["ips"])),
                mac=group["mac"],
                hostnames=tuple(sorted(group["hostnames"])),
                sources=tuple(sorted(group["sources"])),
            )
        )
    return devices


def device_to_entities(device: LanDevice) -> list[dict[str, Any]]:
    """Convert a device into graph-ready entity dicts."""
    entities: list[dict[str, Any]] = []
    for src in device.sources or ("lan",):
        if device.mac:
            entities.append(
                {"type": "mac", "value": device.mac,
                 "source": src, "kind": "device"}
            )
        for ip in device.ips:
            etype = "ipv6" if ":" in ip else "ipv4"
            entities.append(
                {"type": etype, "value": ip, "source": src, "kind": "device"}
            )
        for host in device.hostnames:
            entities.append(
                {"type": "domain", "value": host, "source": src, "kind": "device"}
            )
    return entities


def contact_for_tool(tool: str) -> str:
    """Map a tool name to its contact class. Unknown means active."""
    name = tool.strip().lower() if isinstance(tool, str) else ""
    if name in PASSIVE_TOOLS:
        return "none"
    return "active"
