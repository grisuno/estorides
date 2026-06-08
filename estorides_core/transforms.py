"""
estorides_core.transforms
=========================
Maltego-style transform registry. A *transform* takes one entity
`(type, value)` and returns related `nodes`/`links` in the same shape
as :mod:`estorides_core.intel_resolver`, so the web layer and the D3
graph can merge the result with the existing expansion pipeline.

Transforms are grouped into the four-stage intelligence pipeline the
operator walks a selector through:

    data -> information -> intelligence -> counter_intelligence

Most transforms are thin filters over a single cross-feed resolution
(`resolver.resolve`), which already fans a selector out across Wikidata,
IP-API, OFAC and VirusTotal relationships. A few wrap the keyless Osiris
probes (BGP, breach leaks, GitHub) and adapt their raw payloads into the
node/link shape.

Public surface::

    from estorides_core.transforms import registry
    registry.for_type("ip")                 # -> [{"id","label","tier"}, ...]
    registry.run("ip_to_sanctions", "ip", "1.2.3.4")
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set

log = logging.getLogger("estorides.transforms")

# The ordered pipeline tiers; mirrors knowledge_graph.INTEL_LEVELS.
TIERS = ("data", "information", "intelligence", "counter_intelligence")

Result = Dict[str, Any]


@dataclass
class Transform:
    """One named transform applicable to a set of entity types."""

    id: str
    label: str
    tier: str
    applies: Set[str]
    runner: Callable[[str, str], Result]
    description: str = ""

    def summary(self) -> Dict[str, str]:
        return {
            "id": self.id, "label": self.label, "tier": self.tier,
            "description": self.description,
        }


# ---------------------------------------------------------------------------
# Resolver-backed runners
# ---------------------------------------------------------------------------
def _empty(root_type: str, value: str) -> Result:
    return {"nodes": [], "links": [], "sources": []}


def _resolver_filtered(ent_type: str, value: str, relations: Optional[Set[str]]) -> Result:
    """Resolve `(ent_type, value)` and keep only links whose relation is
    in `relations` (or every link when `relations` is None). The root
    node plus any node touched by a kept link is returned."""
    from .intel_resolver import resolver
    out = resolver.resolve(ent_type, value)
    all_nodes = out.get("nodes", []) or []
    all_links = out.get("links", []) or []
    root_id = out.get("root_id")
    if relations is None:
        links = list(all_links)
    else:
        links = [l for l in all_links if l.get("relation") in relations]
    keep: Set[str] = {root_id} if root_id else set()
    for l in links:
        keep.add(l.get("source"))
        keep.add(l.get("target"))
    nodes = [n for n in all_nodes if n.get("id") in keep]
    return {"nodes": nodes, "links": links, "sources": out.get("sources", [])}


def _filter_runner(relations: Optional[Set[str]]) -> Callable[[str, str], Result]:
    def run(ent_type: str, value: str) -> Result:
        return _resolver_filtered(ent_type, value, relations)
    return run


# ---------------------------------------------------------------------------
# Osiris-backed runners (keyless probes adapted to node/link shape)
# ---------------------------------------------------------------------------
def _norm(s: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def _osiris():
    try:
        from . import osiris_sources
        return osiris_sources
    except Exception:  # noqa: BLE001
        return None


def _run_bgp(ent_type: str, value: str) -> Result:
    osiris = _osiris()
    if osiris is None:
        return _empty(ent_type, value)
    data = osiris.fetch_bgp(value) or {}
    root_id = f"ip:{value.lower()}"
    nodes: List[Dict[str, Any]] = [{
        "id": root_id, "label": value, "type": "ip", "kind": "ip",
        "properties": {"source": "query"},
    }]
    links: List[Dict[str, Any]] = []
    asn = data.get("asn") or data.get("as") or data.get("ASN")
    if asn:
        aid = f"asn:{_norm(str(asn))}"
        nodes.append({"id": aid, "label": f"AS{asn}", "type": "asn",
                      "kind": "infrastructure", "properties": {"source": "bgp"}})
        links.append({"source": root_id, "target": aid, "relation": "announced_by"})
    holder = data.get("holder") or data.get("name") or data.get("descr")
    if holder:
        hid = f"company:{_norm(str(holder))}"
        nodes.append({"id": hid, "label": str(holder), "type": "company",
                      "kind": "org", "properties": {"source": "bgp"}})
        links.append({"source": root_id, "target": hid, "relation": "hosted_by"})
    return {"nodes": nodes, "links": links, "sources": ["bgp"] if links else []}


def _run_leaks(ent_type: str, value: str) -> Result:
    osiris = _osiris()
    if osiris is None:
        return _empty(ent_type, value)
    data = osiris.fetch_leaks(value) or {}
    root_id = f"email:{value.lower()}"
    nodes: List[Dict[str, Any]] = [{
        "id": root_id, "label": value, "type": "email", "kind": "person",
        "properties": {"source": "query"},
    }]
    links: List[Dict[str, Any]] = []
    breaches = data.get("breaches") or data.get("results") or data.get("sources") or []
    if isinstance(breaches, dict):
        breaches = list(breaches.keys())
    for b in breaches[:25]:
        name = b.get("name") if isinstance(b, dict) else str(b)
        if not name:
            continue
        bid = f"breach:{_norm(name)}"
        nodes.append({"id": bid, "label": name, "type": "breach",
                      "kind": "breach", "properties": {"source": "leaks"}})
        links.append({"source": root_id, "target": bid, "relation": "exposed_in"})
    return {"nodes": nodes, "links": links, "sources": ["leaks"] if links else []}


def _run_github(ent_type: str, value: str) -> Result:
    osiris = _osiris()
    if osiris is None:
        return _empty(ent_type, value)
    data = osiris.fetch_github_user(value) or {}
    if not isinstance(data, dict) or data.get("error"):
        return _empty(ent_type, value)
    root_id = f"username:{value.lower()}"
    nodes: List[Dict[str, Any]] = [{
        "id": root_id, "label": value, "type": "username", "kind": "person",
        "properties": {"source": "query"},
    }]
    links: List[Dict[str, Any]] = []
    company = data.get("company")
    if company:
        cid = f"company:{_norm(str(company))}"
        nodes.append({"id": cid, "label": str(company), "type": "company",
                      "kind": "org", "properties": {"source": "github"}})
        links.append({"source": root_id, "target": cid, "relation": "employed_by"})
    blog = data.get("blog")
    if blog:
        did = f"url:{str(blog).lower()}"
        nodes.append({"id": did, "label": str(blog), "type": "url",
                      "kind": "url", "properties": {"source": "github"}})
        links.append({"source": root_id, "target": did, "relation": "owns"})
    return {"nodes": nodes, "links": links, "sources": ["github"]}


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
class TransformRegistry:
    """Holds every transform and dispatches by id."""

    def __init__(self) -> None:
        self._by_id: Dict[str, Transform] = {}

    def register(self, t: Transform) -> None:
        self._by_id[t.id] = t

    def for_type(self, ent_type: str) -> List[Dict[str, str]]:
        ent_type = (ent_type or "").lower().strip()
        out = [
            t.summary() for t in self._by_id.values()
            if ent_type in t.applies or "any" in t.applies
        ]
        out.sort(key=lambda s: (TIERS.index(s["tier"]) if s["tier"] in TIERS else 9,
                                s["label"]))
        return out

    def run(self, transform_id: str, ent_type: str, value: str) -> Result:
        t = self._by_id.get(transform_id)
        if t is None:
            return {"error": f"unknown transform {transform_id!r}",
                    "nodes": [], "links": [], "sources": []}
        try:
            res = t.runner(ent_type, value)
        except Exception as e:  # noqa: BLE001
            log.debug("transform %s failed: %s", transform_id, e)
            return {"error": str(e), "nodes": [], "links": [], "sources": []}
        res.setdefault("nodes", [])
        res.setdefault("links", [])
        res.setdefault("sources", [])
        res["transform"] = transform_id
        res["tier"] = t.tier
        return res


registry = TransformRegistry()


def _T(id: str, label: str, tier: str, applies: Set[str],
       runner: Callable[[str, str], Result], description: str = "") -> None:
    registry.register(Transform(id, label, tier, applies, runner, description))


# IP ----------------------------------------------------------------------
_T("ip_to_infra", "IP → Hosting / ASN", "information", {"ip", "ipv4", "ipv6"},
   _filter_runner({"hosted_by", "announced_by", "located_in"}),
   "Hosting organisation, announcing ASN and country.")
_T("ip_to_bgp", "IP → BGP / ASN (Osiris)", "information", {"ip", "ipv4", "ipv6"},
   _run_bgp, "BGP route holder and ASN via RIPEstat.")
_T("ip_to_domains", "IP → Related domains (VT)", "intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner({"resolves_to"}), "Domains that resolved to this IP (VirusTotal).")
_T("ip_to_files", "IP → Communicating files (VT)", "intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner({"communicates_with"}), "Samples seen communicating with this IP.")
_T("ip_to_sanctions", "IP → Sanctions (OFAC)", "counter_intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits on the hosting owner.")
_T("ip_full", "IP → Full cross-resolve", "intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner(None), "Everything the resolver knows about this IP.")

# Domain ------------------------------------------------------------------
_T("domain_to_org", "Domain → Registrant org", "information", {"domain"},
   _filter_runner({"registered_by"}), "Owning organisation (Wikidata).")
_T("domain_to_ips", "Domain → Resolved IPs (VT)", "intelligence", {"domain"},
   _filter_runner({"resolves_to"}), "IPs this domain resolved to (VirusTotal).")
_T("domain_to_subs", "Domain → Subdomains (VT)", "intelligence", {"domain"},
   _filter_runner({"has_subdomain"}), "Known subdomains (VirusTotal).")
_T("domain_to_files", "Domain → Communicating files (VT)", "intelligence", {"domain"},
   _filter_runner({"communicates_with"}), "Samples communicating with this domain.")
_T("domain_full", "Domain → Full cross-resolve", "intelligence", {"domain"},
   _filter_runner(None), "Everything the resolver knows about this domain.")

# File / hash -------------------------------------------------------------
_T("file_to_infra", "File → Contacted infra (VT)", "intelligence",
   {"file", "hash", "md5", "sha1", "sha256"},
   _filter_runner({"contacts"}), "IPs and domains the sample contacted.")
_T("file_to_drops", "File → Dropped files (VT)", "intelligence",
   {"file", "hash", "md5", "sha1", "sha256"},
   _filter_runner({"drops"}), "Files dropped by this sample.")
_T("file_full", "File → Full cross-resolve", "counter_intelligence",
   {"file", "hash", "md5", "sha1", "sha256"},
   _filter_runner(None), "Network footprint and detection of the sample.")

# Company -----------------------------------------------------------------
_T("company_to_parent", "Company → Parent / subsidiary", "information", {"company"},
   _filter_runner({"subsidiary_of"}), "Corporate parent (Wikidata).")
_T("company_to_sanctions", "Company → Sanctions (OFAC)", "counter_intelligence", {"company"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits.")
_T("company_full", "Company → Full cross-resolve", "intelligence", {"company"},
   _filter_runner(None), "Everything the resolver knows about this company.")

# Person ------------------------------------------------------------------
_T("person_to_employer", "Person → Employer", "information", {"person"},
   _filter_runner({"employed_by"}), "Employer (Wikidata).")
_T("person_to_nationality", "Person → Nationality", "information", {"person"},
   _filter_runner({"nationality"}), "Nationality (Wikidata).")
_T("person_to_sanctions", "Person → Sanctions (OFAC)", "counter_intelligence", {"person"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits.")

# Email / username --------------------------------------------------------
_T("email_to_leaks", "Email → Breach leaks (Osiris)", "counter_intelligence", {"email"},
   _run_leaks, "Breaches exposing this address.")
_T("username_to_github", "Username → GitHub profile (Osiris)", "data", {"username"},
   _run_github, "Public GitHub profile, employer and site.")

# CVE ---------------------------------------------------------------------
_T("cve_to_vendors", "CVE → Affected vendors", "intelligence", {"cve"},
   _filter_runner({"affects_vendor"}), "Vendors and products affected (NVD).")
_T("cve_full", "CVE → Full cross-resolve", "intelligence", {"cve"},
   _filter_runner(None), "Everything the resolver knows about this CVE.")

# Country -----------------------------------------------------------------
_T("country_to_borders", "Country → Bordering countries", "information", {"country"},
   _filter_runner({"borders"}), "Neighbouring countries (Wikidata).")

# Crypto ------------------------------------------------------------------
_T("crypto_to_sanctions", "Address → Sanctions (OFAC)", "counter_intelligence",
   {"btc_address", "eth_address"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits on the wallet.")
