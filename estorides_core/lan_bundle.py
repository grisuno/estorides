"""
estorides_core.lan_bundle
=========================
LAN output deliverables for automation.

Builds inventory, graph, LazyOwn, and STIX payloads from LanDevice
lists and writes them atomically to an output directory.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .config import DATA_DIR

log = logging.getLogger("estorides.lan_bundle")

SCHEMA_VERSION = 1
_STEM_RE = re.compile(r"[^A-Za-z0-9_-]+")


def sanitize_stem(stem: Any) -> str:
    """Sanitize a file stem. Bad input falls back to lan."""
    if not isinstance(stem, str) or not stem.strip():
        return "lan"
    raw = stem.strip()
    if ".." in raw or "/" in raw or "\\" in raw:
        return "lan"
    clean = _STEM_RE.sub("", raw)
    return clean or "lan"


def default_output_dir() -> Path:
    """Resolve the LAN output directory from env or data default."""
    raw = os.environ.get("ESTORIDES_LAN_OUTPUT_DIR", "")
    if raw.strip():
        return Path(raw.strip())
    return DATA_DIR / "lan_output"


def build_bundle(
    devices: list[Any],
    *,
    scope_cidr: str | None = None,
    generated_at: float | None = None,
) -> dict[str, Any]:
    """Build all four payloads. Never raises on bad items."""
    devs = [d for d in devices if hasattr(d, "device_id")] if isinstance(
        devices, list
    ) else []
    ts = generated_at if generated_at is not None else time.time()
    scope = scope_cidr.strip() if isinstance(scope_cidr, str) and scope_cidr.strip() else None

    inventory_devices = []
    for dev in devs:
        try:
            inventory_devices.append(
                {
                    "device_id": str(dev.device_id),
                    "ips": sorted(dev.ips) if dev.ips else [],
                    "mac": dev.mac,
                    "hostnames": sorted(dev.hostnames) if dev.hostnames else [],
                    "sources": sorted(dev.sources) if dev.sources else [],
                }
            )
        except Exception as exc:
            log.debug("lan_bundle: dropping bad device: %s", exc)
    inventory_devices.sort(key=lambda d: d["device_id"])
    inventory = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": ts,
        "scope_cidr": scope,
        "device_count": len(inventory_devices),
        "devices": inventory_devices,
    }

    graph_nodes: list[dict[str, Any]] = []
    graph_edges: list[dict[str, Any]] = []
    net_id = f"network:{scope}" if scope else "network:lan"
    if devs:
        graph_nodes.append(
            {
                "id": net_id,
                "kind": "network",
                "label": scope or "lan",
                "type": "network",
                "sources": ["lan"],
            }
        )
    for item in inventory_devices:
        did = item["device_id"]
        sources = item["sources"] or ["lan"]
        graph_nodes.append(
            {
                "id": f"device:{did}",
                "kind": "device",
                "label": item["mac"] or (item["ips"][0] if item["ips"] else did),
                "type": "device",
                "sources": sources,
            }
        )
        graph_edges.append(
            {
                "source": f"device:{did}",
                "target": net_id,
                "type": "member_of",
                "evidence": "estorides:lan",
            }
        )
        if item["mac"]:
            graph_nodes.append(
                {
                    "id": f"mac:{item['mac']}",
                    "kind": "device",
                    "label": item["mac"],
                    "type": "mac",
                    "sources": sources,
                }
            )
            graph_edges.append(
                {
                    "source": f"device:{did}",
                    "target": f"mac:{item['mac']}",
                    "type": "has_mac",
                    "evidence": "estorides:lan",
                }
            )
        for ip in item["ips"]:
            etype = "ipv6" if ":" in ip else "ipv4"
            graph_nodes.append(
                {
                    "id": f"{etype}:{ip}",
                    "kind": "device",
                    "label": ip,
                    "type": etype,
                    "sources": sources,
                }
            )
            graph_edges.append(
                {
                    "source": f"device:{did}",
                    "target": f"{etype}:{ip}",
                    "type": "has_ip",
                    "evidence": "estorides:lan",
                }
            )
        for host in item["hostnames"]:
            graph_nodes.append(
                {
                    "id": f"domain:{host.lower()}",
                    "kind": "device",
                    "label": host,
                    "type": "domain",
                    "sources": sources,
                }
            )
            graph_edges.append(
                {
                    "source": f"device:{did}",
                    "target": f"domain:{host.lower()}",
                    "type": "has_hostname",
                    "evidence": "estorides:lan",
                }
            )
    graph_nodes.sort(key=lambda n: n["id"])
    graph_edges.sort(key=lambda e: (e["source"], e["target"], e["type"]))
    graph = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": ts,
        "scope_cidr": scope,
        "nodes": graph_nodes,
        "edges": graph_edges,
    }

    lz_nodes: list[dict[str, Any]] = []
    lz_edges: list[dict[str, Any]] = []
    for item in inventory_devices:
        did = item["device_id"]
        sources = item["sources"] or ["lan"]
        for ip in item["ips"]:
            lz_nodes.append(
                {
                    "kind": "host",
                    "etype": "ipv6" if ":" in ip else "ipv4",
                    "value": ip,
                    "label": ip,
                    "sources": sources,
                    "attrs": {"device_id": did},
                }
            )
        if item["mac"]:
            lz_nodes.append(
                {
                    "kind": "mac",
                    "etype": "mac",
                    "value": item["mac"],
                    "label": item["mac"],
                    "sources": sources,
                    "attrs": {"device_id": did},
                }
            )
        for host in item["hostnames"]:
            lz_nodes.append(
                {
                    "kind": "domain",
                    "etype": "domain",
                    "value": host,
                    "label": host,
                    "sources": sources,
                    "attrs": {"device_id": did},
                }
            )
    lz_nodes.sort(key=lambda n: (n["kind"], n["value"]))
    for item in inventory_devices:
        for ip in item["ips"]:
            if item["mac"]:
                lz_edges.append(
                    {
                        "source_kind": "host",
                        "source_value": ip,
                        "target_kind": "mac",
                        "target_value": item["mac"],
                        "type": "observed_in",
                        "evidence": "estorides:lan",
                    }
                )
    lz_edges.sort(
        key=lambda e: (
            e["source_kind"], e["source_value"],
            e["target_kind"], e["target_value"],
        )
    )
    lazyown = {
        "source": "estorides-lan",
        "schema_version": SCHEMA_VERSION,
        "generated_at": ts,
        "scope_cidr": scope,
        "nodes": lz_nodes,
        "edges": lz_edges,
    }

    stix_objects: list[dict[str, Any]] = [
        {
            "type": "identity",
            "spec_version": "2.1",
            "id": "identity--estorides-1",
            "created": _fmt_ts(ts),
            "modified": _fmt_ts(ts),
            "name": "Estorides LAN",
            "identity_class": "system",
        }
    ]
    id_map: dict[str, str] = {}
    for item in inventory_devices:
        for ip in item["ips"]:
            sid = f"ipv4-addr--{uuid.uuid5(uuid.NAMESPACE_URL, 'lan:' + ip)}"
            id_map[f"ip:{ip}"] = sid
            stix_objects.append(
                {
                    "type": "ipv4-addr" if ":" not in ip else "ipv6-addr",
                    "spec_version": "2.1",
                    "id": sid,
                    "created": _fmt_ts(ts),
                    "modified": _fmt_ts(ts),
                    "value": ip,
                }
            )
        if item["mac"]:
            sid = f"mac-addr--{uuid.uuid5(uuid.NAMESPACE_URL, 'lan:' + item['mac'])}"
            id_map[f"mac:{item['mac']}"] = sid
            stix_objects.append(
                {
                    "type": "mac-addr",
                    "spec_version": "2.1",
                    "id": sid,
                    "created": _fmt_ts(ts),
                    "modified": _fmt_ts(ts),
                    "value": item["mac"],
                }
            )
        for host in item["hostnames"]:
            sid = f"domain-name--{uuid.uuid5(uuid.NAMESPACE_URL, 'lan:' + host.lower())}"
            id_map[f"domain:{host.lower()}"] = sid
            stix_objects.append(
                {
                    "type": "domain-name",
                    "spec_version": "2.1",
                    "id": sid,
                    "created": _fmt_ts(ts),
                    "modified": _fmt_ts(ts),
                    "value": host,
                }
            )
    for edge in graph_edges:
        src = _stix_ref(edge["source"], id_map)
        dst = _stix_ref(edge["target"], id_map)
        if not src or not dst:
            continue
        stix_objects.append(
            {
                "type": "relationship",
                "spec_version": "2.1",
                "id": f"relationship--{uuid.uuid4()}",
                "created": _fmt_ts(ts),
                "modified": _fmt_ts(ts),
                "relationship_type": edge["type"],
                "source_ref": src,
                "target_ref": dst,
            }
        )
    stix = {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid5(uuid.NAMESPACE_URL, 'lan:' + str(ts))}",
        "objects": stix_objects,
    }
    return {
        "inventory": inventory,
        "graph": graph,
        "lazyown": lazyown,
        "stix": stix,
    }


def _fmt_ts(ts: float) -> str:
    import datetime as _dt

    return (
        _dt.datetime.fromtimestamp(ts, tz=_dt.timezone.utc)
        .isoformat()
        .replace("+00:00", ".000Z")
    )


def _stix_ref(node_id: str, id_map: dict[str, str]) -> str | None:
    if node_id in id_map:
        return id_map[node_id]
    if node_id.startswith(("mac:", "ipv4:", "ipv6:", "domain:")):
        kind, _, val = node_id.partition(":")
        return id_map.get(f"{'ip' if kind in ('ipv4', 'ipv6') else kind}:{val}")
    return None


@dataclass
class LanBundleResult:
    """Outcome of write_bundle. Failures are values, never raises."""

    paths: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    device_count: int = 0
    node_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def write_bundle(
    devices: list[Any],
    *,
    output_dir: str | Path | None = None,
    stem: str = "lan",
    scope_cidr: str | None = None,
) -> LanBundleResult:
    """Write all four deliverables atomically. Never raises."""
    clean_stem = sanitize_stem(stem)
    target = Path(output_dir) if output_dir else default_output_dir()
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return LanBundleResult(
            paths={}, errors=[f"output dir not creatable: {exc}"]
        )
    if target.is_file():
        return LanBundleResult(paths={}, errors=["output dir is a file"])
    try:
        bundle = build_bundle(devices, scope_cidr=scope_cidr)
    except Exception as exc:
        return LanBundleResult(paths={}, errors=[f"build failed: {exc}"])
    payloads = {
        "inventory": bundle["inventory"],
        "graph": bundle["graph"],
        "lazyown": bundle["lazyown"],
        "stix": bundle["stix"],
    }
    paths: dict[str, str] = {}
    errors: list[str] = []
    for fmt_name, payload in payloads.items():
        dest = target / f"{clean_stem}_{fmt_name}.json"
        try:
            text = json.dumps(payload, indent=2, ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            errors.append(f"{fmt_name} not serializable: {exc}")
            continue
        tmp = dest.with_suffix(".tmp")
        try:
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(dest)
            paths[fmt_name] = str(dest)
        except OSError as exc:
            errors.append(f"{fmt_name} write failed: {exc}")
            try:
                tmp.unlink(missing_ok=True)
            except OSError:
                pass
    return LanBundleResult(
        paths=paths,
        errors=errors,
        device_count=bundle["inventory"].get("device_count", 0),
        node_count=len(bundle["graph"].get("nodes", [])),
    )
