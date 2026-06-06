"""
estorides_export.misp
=====================
Minimal MISP event JSON. Mirrors STIX in spirit but matches the
MISP galaxy/cluster schema used by the MISP project.

This is *not* a complete MISP integration — it's enough to import
into MISP as an event.
"""
from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict

from estorides_core.config import MISP_EVENT_PATH
from estorides_core.knowledge_graph import KnowledgeGraph

log = logging.getLogger("estorides.misp")

# MISP attribute type mapping.
TYPE_MAP = {
    "ipv4": "ip-dst", "ipv6": "ip-dst",
    "domain": "domain", "url": "url",
    "email": "email", "btc_address": "btc",
    "eth_address": "eth",
    "cve": "vulnerability", "ghsa": "vulnerability",
    "md5": "md5", "sha1": "sha1", "sha256": "sha256",
    "asn": "AS",
}


def event_from_graph(kg: KnowledgeGraph, *, name: str = "Estorides Run") -> Dict[str, Any]:
    attributes = []
    for _, data in kg.graph.nodes(data=True):
        ent_type = data.get("type")
        misp_type = TYPE_MAP.get(ent_type or "")
        if not misp_type:
            continue
        attributes.append({
            "uuid": str(uuid.uuid4()),
            "type": misp_type,
            "category": _category(ent_type),
            "value": str(data.get("value")),
            "to_ids": False,
            "comment": " | ".join(sorted(data.get("sources", [])))[:200],
            "tag": [],
        })
    return {
        "Event": {
            "uuid": str(uuid.uuid4()),
            "info": name,
            "date": time.strftime("%Y-%m-%d", time.gmtime()),
            "threat_level_id": "2",
            "analysis": "2",
            "distribution": "1",
            "Attribute": attributes,
        }
    }


def _category(ent_type: str) -> str:
    if ent_type in ("ipv4", "ipv6", "domain", "url", "asn"):
        return "Network activity"
    if ent_type in ("md5", "sha1", "sha256"):
        return "Payload delivery"
    if ent_type in ("cve", "ghsa"):
        return "External analysis"
    if ent_type in ("email",):
        return "Targeting data"
    if ent_type in ("btc_address", "eth_address"):
        return "Financial fraud"
    return "Other"


def export(kg: KnowledgeGraph, path: Path = MISP_EVENT_PATH) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = event_from_graph(kg)
    path.write_text(json.dumps(event, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("MISP event written to %s (%d attributes)", path, len(event["Event"]["Attribute"]))
    return path
