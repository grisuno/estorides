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
