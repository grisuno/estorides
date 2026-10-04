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
    registry.for_type("ip")                 # -> [{"id","label","tier",...}, ...]
    registry.run("ip_to_sanctions", "ip", "1.2.3.4")

Transforms can also be added without code: drop a ``*.yaml`` file in
``transforms/`` (same ease as ``sources/``)::

    id: my_pivot
    label: My pivot
    tier: intelligence
    input_types: [domain]
    output_types: [ip]
    cost: free
    engine: resolver
    relations: [resolves_to]

Engines: ``resolver`` (filter over ``intel_resolver``), ``osiris_bgp`` /
``osiris_leaks`` / ``osiris_github``, ``static`` (fixed nodes/links with
``{query}`` substitution). Loaded via :meth:`TransformRegistry.load_yaml_dir`
(YAML multi-doc / lists, like ``source_loader``); broken files are skipped
fail-soft so built-ins always survive.
"""
from __future__ import annotations

import logging
import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("estorides.transforms")

# The ordered pipeline tiers; mirrors knowledge_graph.INTEL_LEVELS.
TIERS = ("data", "information", "intelligence", "counter_intelligence")

# Validation caps (see spec/transforms.md). Values are data only, never
# executed — caps keep a hostile label from becoming a memory hog.
MAX_ID_LEN = 64
MAX_TYPE_LEN = 64
MAX_VALUE_LEN = 512
_ID_RE = re.compile(r"^[a-z0-9_]{1,64}$")
MAX_STATIC_NODES = 50
MAX_STATIC_LINKS = 100

Result = dict[str, Any]


@dataclass
class Transform:
    """One named transform applicable to a set of entity types."""

    id: str
    label: str
    tier: str
    applies: set[str]
    runner: Callable[[str, str], Result]
    description: str = ""
    output_types: list[str] = field(default_factory=list)
    cost: str = "free"

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id, "label": self.label, "tier": self.tier,
            "description": self.description,
            "input_types": sorted(self.applies),
            "output_types": list(self.output_types),
            "cost": self.cost,
        }


# ---------------------------------------------------------------------------
# Resolver-backed runners
# ---------------------------------------------------------------------------
def _empty(root_type: str, value: str) -> Result:
    return {"nodes": [], "links": [], "sources": []}


def _resolver_filtered(ent_type: str, value: str, relations: set[str] | None) -> Result:
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
        links = [lk for lk in all_links if lk.get("relation") in relations]
    keep: set[str] = {root_id} if root_id else set()
    for lk in links:
        keep.add(lk.get("source"))
        keep.add(lk.get("target"))
    nodes = [n for n in all_nodes if n.get("id") in keep]
    return {"nodes": nodes, "links": links, "sources": out.get("sources", [])}


def _filter_runner(relations: set[str] | None) -> Callable[[str, str], Result]:
    def run(ent_type: str, value: str) -> Result:
        return _resolver_filtered(ent_type, value, relations)
    return run


# ---------------------------------------------------------------------------
# Osiris-backed runners (keyless probes adapted to node/link shape)
# ---------------------------------------------------------------------------
def _norm(s: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def _osiris() -> Any:
    try:
        from . import osiris_sources
        return osiris_sources
    except Exception:
        return None


def _run_bgp(ent_type: str, value: str) -> Result:
    osiris = _osiris()
    if osiris is None:
        return _empty(ent_type, value)
    data = osiris.fetch_bgp(value) or {}
    root_id = f"ip:{value.lower()}"
    nodes: list[dict[str, Any]] = [{
        "id": root_id, "label": value, "type": "ip", "kind": "ip",
        "properties": {"source": "query"},
    }]
    links: list[dict[str, Any]] = []
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
    nodes: list[dict[str, Any]] = [{
        "id": root_id, "label": value, "type": "email", "kind": "person",
        "properties": {"source": "query"},
    }]
    links: list[dict[str, Any]] = []
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
    nodes: list[dict[str, Any]] = [{
        "id": root_id, "label": value, "type": "username", "kind": "person",
        "properties": {"source": "query"},
    }]
    links: list[dict[str, Any]] = []
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
        self._by_id: dict[str, Transform] = {}

    def register(self, t: Transform) -> None:
        self._by_id[t.id] = t

    def for_type(self, ent_type: str) -> list[dict[str, Any]]:
        ent_type = (ent_type or "").lower().strip()
        if not ent_type:
            return []
        out = [
            t.summary() for t in self._by_id.values()
            if ent_type in t.applies or "any" in t.applies
        ]
        out.sort(key=lambda s: (TIERS.index(s["tier"]) if s["tier"] in TIERS else 9,
                                s["label"]))
        return out

    def run(self, transform_id: str, ent_type: str, value: str) -> Result:
        tid = (transform_id or "").strip()
        if not _ID_RE.match(tid):
            return {"error": f"invalid transform_id {transform_id!r}",
                    "nodes": [], "links": [], "sources": []}
        t = self._by_id.get(tid)
        if t is None:
            return {"error": f"unknown transform {tid!r}",
                    "nodes": [], "links": [], "sources": []}
        et = (ent_type or "").strip().lower()
        v = (value or "").strip()
        if not et or len(et) > MAX_TYPE_LEN:
            return {"error": "invalid type", "nodes": [], "links": [],
                    "sources": [], "transform": tid, "tier": t.tier}
        if not v or len(v) > MAX_VALUE_LEN:
            return {"error": "invalid value", "nodes": [], "links": [],
                    "sources": [], "transform": tid, "tier": t.tier}
        try:
            res = t.runner(et, v)
        except Exception:
            log.exception("transform %s failed", tid)
            return {"error": "transform-run-failed", "nodes": [], "links": [],
                    "sources": [], "transform": tid, "tier": t.tier}
        if not isinstance(res, dict):
            return {"error": "transform-run-failed", "nodes": [], "links": [],
                    "sources": [], "transform": tid, "tier": t.tier}
        res.setdefault("nodes", [])
        res.setdefault("links", [])
        res.setdefault("sources", [])
        res["transform"] = tid
        res["tier"] = t.tier
        return res

    # ------------------------------------------------------- yaml loading --
    def load_yaml_dir(self, directory: str | Path) -> int:
        """Register every transform declared in ``*.yaml`` under `directory`.

        Same ease as ``sources/``: one file per pivot, multi-doc / list
        docs supported. Broken files are skipped fail-soft; duplicates
        overwrite with a warning. Returns the number of transforms loaded.
        """
        try:
            import yaml
        except Exception:
            log.error("pyyaml unavailable — yaml transforms skipped")
            return 0
        base = Path(directory)
        if not base.exists():
            return 0
        paths = sorted(p for ext in ("*.yaml", "*.yml") for p in base.rglob(ext))
        loaded = 0
        for path in paths:
            try:
                with path.open("r", encoding="utf-8") as fh:
                    docs = list(yaml.safe_load_all(fh))
            except Exception as e:
                log.error("YAML transform parse error in %s: %s", path.name, e)
                continue
            entries: list[dict[str, Any]] = []
            for doc in docs:
                if isinstance(doc, dict):
                    entries.append(doc)
                elif isinstance(doc, list):
                    entries.extend(d for d in doc if isinstance(d, dict))
            for raw in entries:
                tr = _transform_from_yaml(raw, path.name)
                if tr is None:
                    continue
                if tr.id in self._by_id:
                    log.warning("duplicate transform id %s in %s — overwriting",
                                tr.id, path.name)
                self.register(tr)
                loaded += 1
        return loaded


def _str_list(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [s.strip().lower() for s in raw.split(",") if s.strip()]
    if isinstance(raw, (list, tuple)):
        return [str(s).strip().lower() for s in raw if str(s).strip()]
    return []


def _static_runner(nodes_tpl: list[dict[str, Any]],
                   links_tpl: list[dict[str, Any]]) -> Callable[[str, str], Result]:
    """Fixed nodes/links with ``{query}`` substitution (zero I/O)."""
    def run(ent_type: str, value: str) -> Result:
        q = (value or "").strip()[:MAX_VALUE_LEN]

        def sub(s: Any, depth: int = 0) -> Any:
            if isinstance(s, str):
                return s.replace("{query}", q)[:MAX_VALUE_LEN]
            if isinstance(s, dict) and depth < 3:
                return {str(k)[:64]: sub(v, depth + 1)
                        for k, v in list(s.items())[:12]}
            if isinstance(s, list) and depth < 3:
                return [sub(v, depth + 1) for v in s[:12]]
            return s

        nodes: list[dict[str, Any]] = []
        for n in nodes_tpl[:MAX_STATIC_NODES]:
            if not isinstance(n, dict):
                continue
            nodes.append({str(k)[:64]: sub(v) for k, v in list(n.items())[:12]})
        links: list[dict[str, Any]] = []
        for link in links_tpl[:MAX_STATIC_LINKS]:
            if not isinstance(link, dict):
                continue
            links.append({str(k)[:64]: sub(v) for k, v in list(link.items())[:8]})
        return {"nodes": nodes, "links": links, "sources": ["static"]}
    return run


def _transform_from_yaml(raw: dict[str, Any], origin: str) -> Transform | None:
    """Validate one YAML mapping into a Transform (None = skip)."""
    tid = str(raw.get("id") or "").strip()
    if not _ID_RE.match(tid):
        log.warning("yaml transform with bad id skipped in %s: %r", origin, tid)
        return None
    label = str(raw.get("label") or tid).strip()[:128]
    tier = str(raw.get("tier") or "information").strip().lower()
    if tier not in TIERS:
        log.warning("transform %s: unknown tier %r — treating as 'information'", tid, tier)
        tier = "information"
    applies_raw = raw.get("input_types", raw.get("applies", raw.get("applies_to", [])))
    applies = set(_str_list(applies_raw)) or {"any"}
    output_types = _str_list(raw.get("output_types", []))
    cost = str(raw.get("cost") or "free").strip().lower()[:32]
    description = str(raw.get("description") or "").strip()[:512]
    engine = str(raw.get("engine") or "resolver").strip().lower()
    runner: Callable[[str, str], Result] | None = None
    if engine == "resolver":
        rels = raw.get("relations")
        relations: set[str] | None = None if rels is None else set(_str_list(rels))
        runner = _filter_runner(relations)
    elif engine == "osiris_bgp":
        runner = _run_bgp
    elif engine == "osiris_leaks":
        runner = _run_leaks
    elif engine == "osiris_github":
        runner = _run_github
    elif engine == "static":
        nodes_tpl = raw.get("nodes") or []
        links_tpl = raw.get("links") or []
        if not isinstance(nodes_tpl, list):
            nodes_tpl = []
        if not isinstance(links_tpl, list):
            links_tpl = []
        runner = _static_runner(nodes_tpl, links_tpl)
    else:
        log.warning("transform %s: unknown engine %r — skipped", tid, engine)
        return None
    return Transform(id=tid, label=label, tier=tier, applies=applies,
                     runner=runner, description=description,
                     output_types=output_types, cost=cost)


def iter_sse_events(transform_id: str, ent_type: str, value: str,
                    runner: Callable[[str, str], Result] | None = None,
                    ) -> Iterator[tuple[str, dict[str, Any]]]:
    """Yield ``(kind, payload)`` tuples for the SSE stream endpoint.

    Kinds: ``node`` / ``link`` per item, then ``done`` with counts, or
    ``error`` when the run fails. `runner` override exists for tests.
    """
    if runner is not None:
        try:
            res = runner(ent_type, value)
        except Exception:
            log.exception("transform %s failed", transform_id)
            yield "error", {"error": "transform-run-failed"}
            return
        if not isinstance(res, dict):
            yield "error", {"error": "transform-run-failed"}
            return
    else:
        res = registry.run(transform_id, ent_type, value)
        if res.get("error"):
            yield "error", {"error": res["error"]}
            return
    for n in res.get("nodes", []) or []:
        yield "node", n if isinstance(n, dict) else {"id": str(n)}
    for link in res.get("links", []) or []:
        yield "link", link if isinstance(link, dict) else {"target": str(link)}
    yield "done", {"nodes": len(res.get("nodes", []) or []),
                   "links": len(res.get("links", []) or []),
                   "transform": res.get("transform", transform_id)}


registry = TransformRegistry()


def _T(id: str, label: str, tier: str, applies: set[str],
       runner: Callable[[str, str], Result], description: str = "",
       output_types: list[str] | None = None, cost: str = "free") -> None:
    registry.register(Transform(id, label, tier, applies, runner, description,
                                output_types=list(output_types or []), cost=cost))


# IP ----------------------------------------------------------------------
_T("ip_to_infra", "IP → Hosting / ASN", "information", {"ip", "ipv4", "ipv6"},
   _filter_runner({"hosted_by", "announced_by", "located_in"}),
   "Hosting organisation, announcing ASN and country.",
   ["company", "asn", "country"])
_T("ip_to_bgp", "IP → BGP / ASN (Osiris)", "information", {"ip", "ipv4", "ipv6"},
   _run_bgp, "BGP route holder and ASN via RIPEstat.", ["asn", "company"])
_T("ip_to_domains", "IP → Related domains (VT)", "intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner({"resolves_to"}), "Domains that resolved to this IP (VirusTotal).",
   ["domain"])
_T("ip_to_files", "IP → Communicating files (VT)", "intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner({"communicates_with"}), "Samples seen communicating with this IP.",
   ["file"])
_T("ip_to_sanctions", "IP → Sanctions (OFAC)", "counter_intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits on the hosting owner.",
   ["sanction"])
_T("ip_full", "IP → Full cross-resolve", "intelligence", {"ip", "ipv4", "ipv6"},
   _filter_runner(None), "Everything the resolver knows about this IP.",
   ["domain", "file", "company", "country", "sanction"])

# Domain ------------------------------------------------------------------
_T("domain_to_org", "Domain → Registrant org", "information", {"domain"},
   _filter_runner({"registered_by"}), "Owning organisation (Wikidata).", ["company"])
_T("domain_to_ips", "Domain → Resolved IPs (VT)", "intelligence", {"domain"},
   _filter_runner({"resolves_to"}), "IPs this domain resolved to (VirusTotal).", ["ip"])
_T("domain_to_subs", "Domain → Subdomains (VT)", "intelligence", {"domain"},
   _filter_runner({"has_subdomain"}), "Known subdomains (VirusTotal).", ["domain"])
_T("domain_to_files", "Domain → Communicating files (VT)", "intelligence", {"domain"},
   _filter_runner({"communicates_with"}), "Samples communicating with this domain.",
   ["file"])
_T("domain_full", "Domain → Full cross-resolve", "intelligence", {"domain"},
   _filter_runner(None), "Everything the resolver knows about this domain.",
   ["ip", "domain", "file", "company"])

# File / hash -------------------------------------------------------------
_T("file_to_infra", "File → Contacted infra (VT)", "intelligence",
   {"file", "hash", "md5", "sha1", "sha256"},
   _filter_runner({"contacts"}), "IPs and domains the sample contacted.", ["ip", "domain"])
_T("file_to_drops", "File → Dropped files (VT)", "intelligence",
   {"file", "hash", "md5", "sha1", "sha256"},
   _filter_runner({"drops"}), "Files dropped by this sample.", ["file"])
_T("file_full", "File → Full cross-resolve", "counter_intelligence",
   {"file", "hash", "md5", "sha1", "sha256"},
   _filter_runner(None), "Network footprint and detection of the sample.",
   ["ip", "domain", "file"])

# Company -----------------------------------------------------------------
_T("company_to_parent", "Company → Parent / subsidiary", "information", {"company"},
   _filter_runner({"subsidiary_of"}), "Corporate parent (Wikidata).", ["company"])
_T("company_to_sanctions", "Company → Sanctions (OFAC)", "counter_intelligence", {"company"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits.", ["sanction"])
_T("company_full", "Company → Full cross-resolve", "intelligence", {"company"},
   _filter_runner(None), "Everything the resolver knows about this company.",
   ["company", "person", "country", "sanction"])

# Person ------------------------------------------------------------------
_T("person_to_employer", "Person → Employer", "information", {"person"},
   _filter_runner({"employed_by"}), "Employer (Wikidata).", ["company"])
_T("person_to_nationality", "Person → Nationality", "information", {"person"},
   _filter_runner({"nationality"}), "Nationality (Wikidata).", ["country"])
_T("person_to_sanctions", "Person → Sanctions (OFAC)", "counter_intelligence", {"person"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits.", ["sanction"])

# Email / username --------------------------------------------------------
_T("email_to_leaks", "Email → Breach leaks (Osiris)", "counter_intelligence", {"email"},
   _run_leaks, "Breaches exposing this address.", ["breach"])
_T("username_to_github", "Username → GitHub profile (Osiris)", "data", {"username"},
   _run_github, "Public GitHub profile, employer and site.", ["company", "url"])

# CVE ---------------------------------------------------------------------
_T("cve_to_vendors", "CVE → Affected vendors", "intelligence", {"cve"},
   _filter_runner({"affects_vendor"}), "Vendors and products affected (NVD).",
   ["company", "product"])
_T("cve_full", "CVE → Full cross-resolve", "intelligence", {"cve"},
   _filter_runner(None), "Everything the resolver knows about this CVE.",
   ["company", "product"])

# Country -----------------------------------------------------------------
_T("country_to_borders", "Country → Bordering countries", "information", {"country"},
   _filter_runner({"borders"}), "Neighbouring countries (Wikidata).", ["country"])

# Crypto ------------------------------------------------------------------
_T("crypto_to_sanctions", "Address → Sanctions (OFAC)", "counter_intelligence",
   {"btc_address", "eth_address"},
   _filter_runner({"sanctioned"}), "OFAC sanction hits on the wallet.", ["sanction"])


# YAML-defined transforms (same ease as sources/): one file per pivot.
# Fail-soft — a missing dir or broken YAML never touches the built-ins above.
try:
    _yaml_dir = Path(__file__).resolve().parent.parent / "transforms"
    registry.load_yaml_dir(_yaml_dir)
except Exception:
    log.exception("yaml transform autoload failed")
