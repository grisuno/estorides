"""
estorides_core.intel_resolver
=============================
Cross-feed entity resolver. Inspired by Osiris' `intel/server.js`
(simplifaisoul/osiris), the resolver is the single entry point that
takes a `(type, id)` pair and returns nodes + edges connecting it
across every feed we have a primitive for:

  type=ip         -> ASN, ISP, organisation, country (Wikidata + IP-API)
  type=domain     -> registrant org, ASN, country, sanctions cross-check
  type=company    -> parent org, country, sanctions (Wikidata + OFAC SDN)
  type=person     -> employer, nationality, sanctions (Wikidata + OFAC SDN)
  type=country    -> region, neighbours, risk score
  type=cve        -> affected vendors, exploits (NVD/EPSS cross-check)

The resolver never *fetches* the source. It composes the local cache
(`SanctionsIndex`, `WikidataCache`) with on-demand SPARQL queries
when a node is missing. The orchestrator's post-process stage can
call this once per significant entity and wire the result into the
knowledge graph + Kuzu backend.

Public surface:

    resolver = EntityResolver()
    out = resolver.resolve("ip", "1.2.3.4")
    out = resolver.resolve("company", "Acme Corp")
    out = resolver.resolve("person", "Vladimir Putin")

Return shape (matches Osiris' `nodes`/`links` for drop-in reuse):

    {
      "type": "ip", "id": "1.2.3.4",
      "root_id": "ip:1.2.3.4",
      "nodes": [
        {"id": "ip:1.2.3.4", "label": "1.2.3.4", "type": "ip", "kind": "ip", "properties": {...}},
        {"id": "company:Cloudflare", "label": "Cloudflare", "type": "company", ...},
        ...
      ],
      "links": [
        {"source": "ip:1.2.3.4", "target": "company:Cloudflare", "relation": "hosted_by"},
        ...
      ],
      "sources": ["ip-api.com", "wikidata", "ofac_sdn"],
      "fetched_at": 1700000000.0,
    }

Adding a new resolver is one method + a decorator. No central
registry to edit; the `resolve()` dispatcher uses a small typed
table.
"""
from __future__ import annotations

import ipaddress
import json
import logging
import os
import re
import threading
import time
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple

import requests

from .config import DATA_DIR
from .ssrf_guard import assert_safe

log = logging.getLogger("estorides.resolver")

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
WIKIDATA_UA = "Estorides/1.0 (+open-source OSINT platform; cross-feed resolver)"
IP_API_URL = "https://ip-api.com/json/{ip}"  # free, no key
RIPE_STAT_URL = "https://stat.ripe.net/data/whois/data.json?resource={ip}"
VT_API_BASE = "https://www.virustotal.com/api/v3"
VT_KEY_ENV = "VT_API_KEY"

CACHE_TTL = 24 * 60 * 60
CACHE_MAX = 5_000


# ---------------------------------------------------------------------------
# SPARQL helpers
# ---------------------------------------------------------------------------
_SPARQL_HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": WIKIDATA_UA,
}


def _run_sparql(query: str) -> List[Dict[str, Any]]:
    """Execute a SPARQL SELECT against the Wikidata endpoint.

    Returns the list of result rows. SSRF-guarded via the URL."""
    assert_safe(WIKIDATA_ENDPOINT)
    try:
        r = requests.get(
            WIKIDATA_ENDPOINT,
            params={"query": query, "format": "json"},
            headers=_SPARQL_HEADERS,
            timeout=10,
        )
        if r.status_code != 200:
            log.debug("wikidata %s: %s", r.status_code, r.text[:120])
            return []
        return r.json().get("results", {}).get("bindings", [])
    except Exception as e:  # noqa: BLE001
        log.debug("wikidata error: %s", e)
        return []


def _val(row: Dict[str, Any], key: str) -> str:
    """Pull a string value out of a SPARQL JSON row."""
    cell = row.get(key) or {}
    return str(cell.get("value") or "").strip()


# ---------------------------------------------------------------------------
# Bounded TTL cache (mirrors WikidataCache but for resolver responses)
# ---------------------------------------------------------------------------
class _TTLCache:
    def __init__(self, *, max_items: int = CACHE_MAX, ttl: int = CACHE_TTL) -> None:
        self.max_items = max_items
        self.ttl = ttl
        self._lock = threading.Lock()
        self._store: "OrderedDict[Tuple[str, str], Tuple[float, Any]]" = OrderedDict()

    def get(self, kind: str, key: str) -> Optional[Any]:
        k = (kind, key.lower())
        with self._lock:
            entry = self._store.get(k)
            if entry is None:
                return None
            ts, val = entry
            if (time.time() - ts) > self.ttl:
                self._store.pop(k, None)
                return None
            self._store.move_to_end(k)
            return val

    def put(self, kind: str, key: str, value: Any) -> None:
        k = (kind, key.lower())
        with self._lock:
            self._store[k] = (time.time(), value)
            self._store.move_to_end(k)
            while len(self._store) > self.max_items:
                self._store.popitem(last=False)

    def stats(self) -> Dict[str, int]:
        with self._lock:
            return {"size": len(self._store), "max": self.max_items}


# ---------------------------------------------------------------------------
# Resolver
# ---------------------------------------------------------------------------
class EntityResolver:
    """Cross-feed entity resolution.

    Composes Wikidata SPARQL, the OFAC SDN index (via the existing
    `OntologyEngine.sanctions`), and a couple of free IP-intel
    services into a single response shape suitable for both the UI
    (entity graph panel) and the orchestrator (knowledge graph
    enrichment)."""

    def __init__(self) -> None:
        self.cache = _TTLCache()
        # Late import: the ontology module owns the OFAC index and
        # importing it here would create a circular dep at module
        # load if the orchestrator also imported the resolver.
        from .ontology import ontology
        self._ontology = ontology

    # ------------------------------------------------------ public API
    def resolve(self, ent_type: str, ent_id: str) -> Dict[str, Any]:
        ent_type = (ent_type or "").lower().strip()
        ent_id = (ent_id or "").strip()
        if not ent_type or not ent_id:
            return {"error": "type and id required", "nodes": [], "links": []}

        cached = self.cache.get(ent_type, ent_id)
        if cached is not None:
            return cached

        dispatch: Dict[str, Callable[[str], Dict[str, Any]]] = {
            "ip": self._resolve_ip,
            "domain": self._resolve_domain,
            "company": self._resolve_company,
            "person": self._resolve_person,
            "country": self._resolve_country,
            "cve": self._resolve_cve,
            "btc_address": self._resolve_btc,
            "eth_address": self._resolve_eth,
            "file": self._resolve_file,
            "hash": self._resolve_file,
            "md5": self._resolve_file,
            "sha1": self._resolve_file,
            "sha256": self._resolve_file,
        }
        handler = dispatch.get(ent_type)
        if handler is None:
            return {
                "error": f"unsupported type {ent_type!r}",
                "supported": list(dispatch.keys()),
                "nodes": [], "links": [],
            }
        out = handler(ent_id)
        out.setdefault("type", ent_type)
        out.setdefault("id", ent_id)
        out.setdefault("fetched_at", time.time())
        self.cache.put(ent_type, ent_id, out)
        return out

    # ------------------------------------------------------ VirusTotal
    def _vt_get(self, path: str, limit: Optional[int] = 10) -> Optional[Dict[str, Any]]:
        """GET a VirusTotal v3 path, returning parsed JSON or None.

        Reads the API key from `VT_API_KEY`; if it is absent the call
        is a silent no-op so the resolver degrades cleanly without a
        key. SSRF-guarded via the constructed URL."""
        key = os.environ.get(VT_KEY_ENV, "").strip()
        if not key:
            return None
        url = f"{VT_API_BASE}/{path.lstrip('/')}"
        params = {"limit": limit} if limit is not None else {}
        try:
            assert_safe(url)
            r = requests.get(
                url,
                headers={
                    "x-apikey": key,
                    "Accept": "application/json",
                    "User-Agent": WIKIDATA_UA,
                },
                params=params,
                timeout=10,
            )
            if r.status_code != 200:
                log.debug("virustotal %s %s: %s", r.status_code, path, r.text[:120])
                return None
            return r.json()
        except Exception as e:  # noqa: BLE001
            log.debug("virustotal error %s: %s", path, e)
            return None

    def _vt_add_relationship(
        self,
        path: str,
        *,
        root_id: str,
        relation: str,
        node_type: str,
        node_kind: str,
        id_prefix: str,
        nodes: List[Dict[str, Any]],
        links: List[Dict[str, Any]],
        sources: List[str],
        attr_field: Optional[str] = None,
        limit: int = 10,
    ) -> None:
        """Expand one VirusTotal relationship endpoint into nodes/links.

        `attr_field` pulls the related value from `attributes` (e.g.
        `host_name` for IP resolutions) instead of the raw object id."""
        data = self._vt_get(path, limit=limit)
        if not data:
            return
        items = data.get("data") or []
        if not isinstance(items, list):
            return
        added = False
        for it in items[:limit]:
            if not isinstance(it, dict):
                continue
            if attr_field:
                val = (it.get("attributes") or {}).get(attr_field)
            else:
                val = it.get("id")
            if not val:
                continue
            nid = f"{id_prefix}:{str(val).lower()}"
            nodes.append({
                "id": nid, "label": str(val), "type": node_type,
                "kind": node_kind, "properties": {"source": "virustotal"},
            })
            links.append({"source": root_id, "target": nid, "relation": relation})
            added = True
        if added and "virustotal" not in sources:
            sources.append("virustotal")

    def _vt_flag_malicious(self, path: str, node: Dict[str, Any], sources: List[str]) -> None:
        """Stamp a node with VirusTotal detection stats (counter-intel signal)."""
        data = self._vt_get(path, limit=None)
        if not data:
            return
        data_obj = data.get("data")
        attrs = data_obj.get("attributes", {}) if isinstance(data_obj, dict) else {}
        stats = attrs.get("last_analysis_stats") or {}
        node["properties"]["vt_malicious"] = int(stats.get("malicious", 0) or 0)
        node["properties"]["vt_suspicious"] = int(stats.get("suspicious", 0) or 0)
        if attrs.get("reputation") is not None:
            node["properties"]["vt_reputation"] = attrs.get("reputation")
        if "virustotal" not in sources:
            sources.append("virustotal")

    # ------------------------------------------------------ IP
    def _resolve_ip(self, ip: str) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"ip:{ip}"
        nodes.append({
            "id": root_id, "label": ip, "type": "ip", "kind": "ip",
            "properties": {"source": "query"},
        })
        if not _is_valid_ipv4(ip):
            return {
                "root_id": root_id, "nodes": nodes, "links": links,
                "sources": sources, "error": "not a valid IPv4",
            }

        # ---- IP-API (geolocation, org, ASN) ----
        try:
            assert_safe(IP_API_URL.format(ip=ip))
            r = requests.get(
                IP_API_URL.format(ip=ip),
                headers={"User-Agent": WIKIDATA_UA},
                timeout=8,
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("status") == "success":
                    sources.append("ip-api.com")
                    org = data.get("org") or data.get("isp") or ""
                    asn = data.get("as", "")
                    country = data.get("country", "")
                    cc = data.get("countryCode", "")
                    if org:
                        org_id = f"company:{_norm(org)}"
                        nodes.append({
                            "id": org_id, "label": org, "type": "company",
                            "kind": "org", "properties": {"source": "ip-api.com"},
                        })
                        links.append({
                            "source": root_id, "target": org_id,
                            "relation": "hosted_by",
                        })
                    if asn:
                        asn_id = f"asn:{asn.split()[0] if asn else 'unknown'}"
                        nodes.append({
                            "id": asn_id, "label": asn, "type": "asn",
                            "kind": "infrastructure", "properties": {"source": "ip-api.com"},
                        })
                        links.append({
                            "source": root_id, "target": asn_id,
                            "relation": "announced_by",
                        })
                    if cc:
                        place_id = f"country:{cc}"
                        nodes.append({
                            "id": place_id, "label": country or cc,
                            "type": "country", "kind": "place",
                            "properties": {"code": cc, "source": "ip-api.com"},
                        })
                        links.append({
                            "source": root_id, "target": place_id,
                            "relation": "located_in",
                        })
        except Exception as e:  # noqa: BLE001
            log.debug("ip-api lookup failed: %s", e)

        # ---- VirusTotal related elements (no-op without VT_API_KEY) ----
        self._vt_flag_malicious(f"ip_addresses/{ip}", nodes[0], sources)
        self._vt_add_relationship(
            f"ip_addresses/{ip}/resolutions", root_id=root_id,
            relation="resolves_to", node_type="domain", node_kind="domain",
            id_prefix="domain", attr_field="host_name",
            nodes=nodes, links=links, sources=sources,
        )
        self._vt_add_relationship(
            f"ip_addresses/{ip}/communicating_files", root_id=root_id,
            relation="communicates_with", node_type="file", node_kind="file",
            id_prefix="file", nodes=nodes, links=links, sources=sources,
        )

        # ---- OFAC sanctions cross-check on the org/ASN owner ----
        for n in list(nodes):
            if n["type"] == "company":
                hits = self._ontology.sanctions.lookup(n["label"])
                for h in hits[:3]:
                    sid = f"sanction:{h.id or _norm(h.name)}"
                    nodes.append({
                        "id": sid, "label": h.name, "type": "sanction",
                        "kind": "sanction",
                        "properties": {
                            "schema": h.schema, "programs": h.programs,
                            "source": "ofac_sdn",
                        },
                    })
                    links.append({
                        "source": n["id"], "target": sid,
                        "relation": "sanctioned",
                    })
                if hits:
                    sources.append("ofac_sdn")

        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }

    # ------------------------------------------------------ Domain
    def _resolve_domain(self, domain: str) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"domain:{domain.lower()}"
        nodes.append({
            "id": root_id, "label": domain, "type": "domain",
            "kind": "domain", "properties": {"source": "query"},
        })
        d = domain.lower().strip()
        # ---- Wikidata search for the org that owns this domain ----
        try:
            q = (
                'SELECT ?org ?orgLabel WHERE { '
                '  ?org wdt:P856 "' + _escape_sparql(d) + '". '
                '  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } '
                '} LIMIT 5'
            )
            for row in _run_sparql(q):
                label = _val(row, "orgLabel")
                qid = _val(row, "org")
                if not label:
                    continue
                sources.append("wikidata")
                org_id = f"company:{_norm(label)}"
                nodes.append({
                    "id": org_id, "label": label, "type": "company",
                    "kind": "org",
                    "properties": {"wikidata_id": qid, "source": "wikidata"},
                })
                links.append({
                    "source": root_id, "target": org_id,
                    "relation": "registered_by",
                })
        except Exception as e:  # noqa: BLE001
            log.debug("wikidata domain lookup failed: %s", e)

        # ---- VirusTotal related elements (no-op without VT_API_KEY) ----
        self._vt_flag_malicious(f"domains/{d}", nodes[0], sources)
        self._vt_add_relationship(
            f"domains/{d}/resolutions", root_id=root_id,
            relation="resolves_to", node_type="ip", node_kind="ip",
            id_prefix="ip", attr_field="ip_address",
            nodes=nodes, links=links, sources=sources,
        )
        self._vt_add_relationship(
            f"domains/{d}/subdomains", root_id=root_id,
            relation="has_subdomain", node_type="domain", node_kind="domain",
            id_prefix="domain", nodes=nodes, links=links, sources=sources,
        )
        self._vt_add_relationship(
            f"domains/{d}/communicating_files", root_id=root_id,
            relation="communicates_with", node_type="file", node_kind="file",
            id_prefix="file", nodes=nodes, links=links, sources=sources,
        )
        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }

    # ------------------------------------------------------ File
    def _resolve_file(self, file_hash: str) -> Dict[str, Any]:
        """Resolve a file hash via VirusTotal relationships.

        Surfaces the network footprint of a sample (contacted IPs and
        domains, dropped/bundled files) and stamps the detection count
        so a malicious sample lights up the counter-intelligence tier."""
        h = file_hash.lower().strip()
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"file:{h}"
        nodes.append({
            "id": root_id, "label": file_hash, "type": "file",
            "kind": "file", "properties": {"source": "query"},
        })
        self._vt_flag_malicious(f"files/{h}", nodes[0], sources)
        self._vt_add_relationship(
            f"files/{h}/contacted_ips", root_id=root_id,
            relation="contacts", node_type="ip", node_kind="ip",
            id_prefix="ip", nodes=nodes, links=links, sources=sources,
        )
        self._vt_add_relationship(
            f"files/{h}/contacted_domains", root_id=root_id,
            relation="contacts", node_type="domain", node_kind="domain",
            id_prefix="domain", nodes=nodes, links=links, sources=sources,
        )
        self._vt_add_relationship(
            f"files/{h}/dropped_files", root_id=root_id,
            relation="drops", node_type="file", node_kind="file",
            id_prefix="file", nodes=nodes, links=links, sources=sources,
        )
        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }

    # ------------------------------------------------------ Company
    def _resolve_company(self, name: str) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"company:{_norm(name)}"
        nodes.append({
            "id": root_id, "label": name, "type": "company",
            "kind": "org", "properties": {"source": "query"},
        })
        # OFAC sanctions
        for h in self._ontology.sanctions.lookup(name)[:5]:
            sources.append("ofac_sdn")
            sid = f"sanction:{h.id or _norm(h.name)}"
            nodes.append({
                "id": sid, "label": h.name, "type": "sanction",
                "kind": "sanction",
                "properties": {
                    "schema": h.schema, "programs": h.programs,
                    "source": "ofac_sdn",
                },
            })
            links.append({
                "source": root_id, "target": sid,
                "relation": "sanctioned",
            })
        # Wikidata parent org
        try:
            q = (
                'SELECT ?parent ?parentLabel WHERE { '
                '  ?org rdfs:label "' + _escape_sparql(name) + '"@en. '
                '  ?org wdt:P31/wdt:P279* wd:Q4830453. '  # instance of business
                '  OPTIONAL { ?org wdt:P749 ?parent. } '
                '  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } '
                '} LIMIT 5'
            )
            for row in _run_sparql(q):
                plabel = _val(row, "parentLabel")
                pqid = _val(row, "parent")
                if not plabel:
                    continue
                sources.append("wikidata")
                pid = f"company:{_norm(plabel)}"
                nodes.append({
                    "id": pid, "label": plabel, "type": "company",
                    "kind": "org",
                    "properties": {"wikidata_id": pqid, "source": "wikidata"},
                })
                links.append({
                    "source": root_id, "target": pid,
                    "relation": "subsidiary_of",
                })
        except Exception as e:  # noqa: BLE001
            log.debug("wikidata company lookup failed: %s", e)
        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }

    # ------------------------------------------------------ Person
    def _resolve_person(self, name: str) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"person:{_norm(name)}"
        nodes.append({
            "id": root_id, "label": name, "type": "person",
            "kind": "person", "properties": {"source": "query"},
        })
        # OFAC sanctions
        for h in self._ontology.sanctions.lookup(name)[:5]:
            sources.append("ofac_sdn")
            sid = f"sanction:{h.id or _norm(h.name)}"
            nodes.append({
                "id": sid, "label": h.name, "type": "sanction",
                "kind": "sanction",
                "properties": {
                    "schema": h.schema, "programs": h.programs,
                    "source": "ofac_sdn",
                },
            })
            links.append({
                "source": root_id, "target": sid,
                "relation": "sanctioned",
            })
        # Wikidata employer + nationality
        try:
            q = (
                'SELECT ?employerLabel ?countryLabel WHERE { '
                '  ?p rdfs:label "' + _escape_sparql(name) + '"@en. '
                '  ?p wdt:P31 wd:Q5. '  # instance of human
                '  OPTIONAL { ?p wdt:P108 ?employer. } '
                '  OPTIONAL { ?p wdt:P27 ?country. } '
                '  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } '
                '} LIMIT 5'
            )
            for row in _run_sparql(q):
                emp = _val(row, "employerLabel")
                cty = _val(row, "countryLabel")
                if emp:
                    sources.append("wikidata")
                    eid = f"company:{_norm(emp)}"
                    nodes.append({
                        "id": eid, "label": emp, "type": "company",
                        "kind": "org", "properties": {"source": "wikidata"},
                    })
                    links.append({
                        "source": root_id, "target": eid,
                        "relation": "employed_by",
                    })
                if cty:
                    sources.append("wikidata")
                    cid = f"country:{_norm(cty)}"
                    nodes.append({
                        "id": cid, "label": cty, "type": "country",
                        "kind": "place", "properties": {"source": "wikidata"},
                    })
                    links.append({
                        "source": root_id, "target": cid,
                        "relation": "nationality",
                    })
        except Exception as e:  # noqa: BLE001
            log.debug("wikidata person lookup failed: %s", e)
        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }

    # ------------------------------------------------------ Country
    def _resolve_country(self, name: str) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"country:{_norm(name)}"
        nodes.append({
            "id": root_id, "label": name, "type": "country",
            "kind": "place", "properties": {"source": "query"},
        })
        try:
            q = (
                'SELECT ?neighbourLabel WHERE { '
                '  ?c rdfs:label "' + _escape_sparql(name) + '"@en. '
                '  ?c wdt:P31 wd:Q6256. '
                '  ?c wdt:P47 ?neighbour. '
                '  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } '
                '} LIMIT 10'
            )
            for row in _run_sparql(q):
                nb = _val(row, "neighbourLabel")
                if not nb:
                    continue
                sources.append("wikidata")
                nid = f"country:{_norm(nb)}"
                nodes.append({
                    "id": nid, "label": nb, "type": "country",
                    "kind": "place", "properties": {"source": "wikidata"},
                })
                links.append({
                    "source": root_id, "target": nid,
                    "relation": "borders",
                })
        except Exception as e:  # noqa: BLE001
            log.debug("wikidata country lookup failed: %s", e)
        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }

    # ------------------------------------------------------ CVE
    def _resolve_cve(self, cve_id: str) -> Dict[str, Any]:
        cve_id = cve_id.upper().strip()
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"cve:{cve_id.lower()}"
        nodes.append({
            "id": root_id, "label": cve_id, "type": "cve",
            "kind": "vulnerability", "properties": {"source": "query"},
        })
        # Free NVD lookup (no key, rate-limited)
        try:
            nvd_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
            assert_safe(nvd_url)
            r = requests.get(
                nvd_url,
                headers={"User-Agent": WIKIDATA_UA},
                timeout=10,
            )
            if r.status_code == 200:
                data = r.json()
                for v in data.get("vulnerabilities", [])[:1]:
                    c = v.get("cve", {})
                    descs = c.get("descriptions", [])
                    en = next((d["value"] for d in descs if d.get("lang") == "en"), "")
                    metrics = c.get("metrics", {}).get("cvssMetricV31", [])
                    score = ""
                    if metrics:
                        score = str(metrics[0].get("cvssData", {}).get("baseScore", ""))
                    sources.append("nvd")
                    nodes[0]["properties"].update({
                        "description": en[:400],
                        "cvss": score,
                        "source": "nvd",
                    })
                    for cfg in c.get("configurations", [])[:5]:
                        for n in cfg.get("nodes", []):
                            for cpe in n.get("cpeMatch", []):
                                criteria = cpe.get("criteria", "")
                                if not criteria:
                                    continue
                                vendor = criteria.split(":", 3)[3] if criteria.count(":") >= 3 else ""
                                prod = criteria.split(":", 4)[4] if criteria.count(":") >= 4 else ""
                                if not (vendor and prod):
                                    continue
                                vid = f"org:{_norm(vendor)}"
                                nodes.append({
                                    "id": vid, "label": vendor, "type": "company",
                                    "kind": "vendor", "properties": {"source": "nvd"},
                                })
                                links.append({
                                    "source": root_id, "target": vid,
                                    "relation": "affects_vendor",
                                })
                                # Also a product
                                pid = f"product:{_norm(vendor)}:{_norm(prod)}"
                                nodes.append({
                                    "id": pid, "label": f"{vendor} {prod}", "type": "product",
                                    "kind": "product", "properties": {"source": "nvd"},
                                })
                                links.append({
                                    "source": vid, "target": pid,
                                    "relation": "produces",
                                })
        except Exception as e:  # noqa: BLE001
            log.debug("nvd lookup failed: %s", e)
        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }

    # ------------------------------------------------------ Crypto (sanctions only)
    def _resolve_btc(self, addr: str) -> Dict[str, Any]:
        return self._resolve_crypto(addr, "btc")

    def _resolve_eth(self, addr: str) -> Dict[str, Any]:
        return self._resolve_crypto(addr, "eth")

    def _resolve_crypto(self, addr: str, kind: str) -> Dict[str, Any]:
        nodes: List[Dict[str, Any]] = []
        links: List[Dict[str, Any]] = []
        sources: List[str] = []
        root_id = f"{kind}_address:{addr.lower()}"
        nodes.append({
            "id": root_id, "label": addr, "type": f"{kind}_address",
            "kind": "crypto", "properties": {"source": "query"},
        })
        for h in self._ontology.sanctions.lookup_crypto(addr)[:5]:
            sources.append("ofac_sdn")
            sid = f"sanction:{h.id or _norm(h.name)}"
            nodes.append({
                "id": sid, "label": h.name, "type": "sanction",
                "kind": "sanction",
                "properties": {
                    "schema": h.schema, "programs": h.programs,
                    "source": "ofac_sdn",
                },
            })
            links.append({
                "source": root_id, "target": sid,
                "relation": "sanctioned",
            })
        return {
            "root_id": root_id, "nodes": nodes, "links": links,
            "sources": sorted(set(sources)),
        }


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------
def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _is_valid_ipv4(s: str) -> bool:
    try:
        ipaddress.IPv4Address(s)
        return True
    except (ValueError, TypeError):
        return False


def _escape_sparql(s: str) -> str:
    # Minimal: only allow through characters that survive literal
    # embedding into a double-quoted SPARQL string. Anything more
    # elaborate should use the caller's own quoting.
    return s.replace("\\", "\\\\").replace('"', '\\"')


# Module-level singleton
resolver = EntityResolver()
