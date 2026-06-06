"""
estorides_export.stix
=====================
STIX 2.1 bundle export. Each unique entity becomes a STIX object
(identity, ipv4-addr, domain-name, email-addr, software, vulnerability,
url). Co-occurrences become sighting relationships. Sourced by the
identity "Estorides".

Spec: https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html
"""
from __future__ import annotations

import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List

from estorides_core.config import STIX_BUNDLE_PATH
from estorides_core.knowledge_graph import KnowledgeGraph

log = logging.getLogger("estorides.stix")

IDENTITY_REF = "identity--estorides-1"


def _id(stix_type: str) -> str:
    return f"{stix_type}--{uuid.uuid4()}"


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())


# entity-type -> STIX 2.1 object type
ENTITY_TO_STIX = {
    "ipv4": "ipv4-addr",
    "ipv6": "ipv6-addr",
    "domain": "domain-name",
    "url": "url",
    "email": "email-addr",
    "btc_address": "crypto-wallet",
    "eth_address": "crypto-wallet",
    "cve": "vulnerability",
    "ghsa": "vulnerability",
    "md5": "file",
    "sha1": "file",
    "sha256": "file",
    "asn": "autonomous-system",
    "mac": "mac-addr",
}


def bundle_from_graph(kg: KnowledgeGraph, *, name: str = "Estorides Run") -> Dict[str, Any]:
    objects: List[Dict[str, Any]] = []

    # ---- identity ----
    objects.append({
        "type": "identity",
        "spec_version": "2.1",
        "id": IDENTITY_REF,
        "created": _now(),
        "modified": _now(),
        "name": name,
        "identity_class": "system",
        "description": "Estorides OSINT platform",
        "sectors": ["technology"],
        "contact_information": "estorides@local",
    })

    # ---- per-node STIX objects ----
    node_id_to_stix: Dict[str, str] = {}
    for nid, data in kg.graph.nodes(data=True):
        ent_type = data.get("type")
        stix_type = ENTITY_TO_STIX.get(ent_type or "")
        if not stix_type:
            continue
        value = data.get("value")
        stix_id = _id(stix_type)
        node_id_to_stix[nid] = stix_id
        obj: Dict[str, Any] = {
            "type": stix_type,
            "spec_version": "2.1",
            "id": stix_id,
            "created": _now(),
            "modified": _now(),
        }
        if stix_type == "ipv4-addr":
            obj["value"] = value
        elif stix_type == "ipv6-addr":
            obj["value"] = value
        elif stix_type == "domain-name":
            obj["value"] = value
        elif stix_type == "url":
            obj["value"] = value
        elif stix_type == "email-addr":
            obj["value"] = value
        elif stix_type == "crypto-wallet":
            obj["value"] = value
            obj["cryptocurrency_type"] = "bitcoin" if ent_type == "btc_address" else "ethereum"
        elif stix_type == "vulnerability":
            obj["name"] = value
        elif stix_type == "file":
            obj["hashes"] = {ent_type: value}
        elif stix_type == "autonomous-system":
            obj["number"] = int(str(value).lstrip("AS") or 0) or None
        elif stix_type == "mac-addr":
            obj["value"] = value

        # add labels + custom property for provenance
        if data.get("contexts"):
            obj["x_estorides_contexts"] = data["contexts"][:3]
        if data.get("sources"):
            obj["x_estorides_sources"] = sorted(data["sources"])

        objects.append(obj)

    # ---- relationships ----
    for u, v, attrs in kg.graph.edges(data=True):
        rel = attrs.get("relation", "related-to")
        su, sv = node_id_to_stix.get(u), node_id_to_stix.get(v)
        if not su or not sv:
            continue
        rel_id = _id("relationship")
        rel_obj = {
            "type": "relationship",
            "spec_version": "2.1",
            "id": rel_id,
            "created": _now(),
            "modified": _now(),
            "relationship_type": rel.replace("-", "_"),
            "source_ref": su,
            "target_ref": sv,
        }
        objects.append(rel_obj)

    return {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid4()}",
        "objects": objects,
    }


def export(kg: KnowledgeGraph, path: Path = STIX_BUNDLE_PATH) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    bundle = bundle_from_graph(kg)
    path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("STIX 2.1 bundle written to %s (%d objects)", path, len(bundle["objects"]))
    return path
