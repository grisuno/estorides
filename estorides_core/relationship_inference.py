"""
estorides_core.relationship_inference
=====================================
Strategy registry for deriving higher-level knowledge-graph edges
from raw observations.

The orchestrator's old `_infer_relationships()` was a chain of
hard-coded `if src == "foo": ...` blocks — every new source that
wanted to contribute edges meant editing the central orchestrator.
This module replaces that with a registry: a `RelationshipInferer`
is a small callable that knows how to translate one observation
into graph edges, and the orchestrator walks the registry.

Add a new inferer by:
  1. Writing a function `def my_inferer(observation, query, kg) -> None`
  2. Decorating it with `@register_inferer("source_name")`

The orchestrator picks the right inferer by the observation's
`source` field, so the source name and inferer name must match.

An inferer is a NO-OP if the observation has nothing useful to
contribute (returns None), or raises a `ValueError` if the
observation is malformed in a way the orchestrator should log
and skip.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Protocol, runtime_checkable

log = logging.getLogger("estorides.inferers")


# ----------------------------------------------------------------- protocol
@runtime_checkable
class RelationshipInferer(Protocol):
    """Translate a single observation into one or more knowledge-graph edges.

    Args:
        observation: the structured observation dict produced by the
            orchestrator. Has keys: source, category, parsed, raw, meta.
        query: the user's original query string. Useful for edges that
            connect a finding back to the pivot (e.g. "domain X
            resolved to IP Y for query X").
        kg: the KnowledgeGraph to mutate. The inferer adds nodes and
            edges via the existing `add_relationship()` API.

    Returns:
        None. Side effects only: writes to the knowledge graph.
    """
    def __call__(
        self,
        observation: Dict[str, Any],
        query: str,
        kg: Any,
    ) -> None: ...


# ----------------------------------------------------------------- registry
INFERERS: Dict[str, RelationshipInferer] = {}


def register_inferer(source_name: str) -> Callable[[RelationshipInferer], RelationshipInferer]:
    """Decorator: register `func` as the inferer for `source_name`.

    Re-registration is a debug log + overwrite; the orchestrator picks
    the LAST registered inferer for a given source name, so a test
    can monkey-patch an inferer without monkey-patching the source.
    """
    def deco(func: RelationshipInferer) -> RelationshipInferer:
        if source_name in INFERERS:
            log.debug("re-registering inferer for source %r", source_name)
        INFERERS[source_name] = func
        return func
    return deco


def infer_relationship(
    observation: Dict[str, Any],
    query: str,
    kg: Any,
) -> bool:
    """Dispatch an observation to its inferer (if any).

    Returns True if an inferer ran, False otherwise. An inferer that
    raises is logged at WARNING and returns False; the orchestrator
    keeps going so one bad source doesn't poison the whole run.
    """
    src = observation.get("source", "")
    fn = INFERERS.get(src)
    if fn is None:
        return False
    try:
        fn(observation, query, kg)
    except Exception as e:  # noqa: BLE001
        log.warning("inferer for source %r failed: %s", src, e)
        return False
    return True


# ----------------------------------------------------------------- builtins
@register_inferer("dns_google")
@register_inferer("dns_cloudflare")
@register_inferer("dns_lookup")
def _infer_dns(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    records = parsed.get("records") or {}
    for ip in records.get("1", []):
        kg.add_relationship("domain", query.lower(), "resolves_to",
                             "ipv4", ip, source=observation["source"])


@register_inferer("crtsh_certificates")
def _infer_crtsh(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    for sub in (parsed.get("subdomains") or [])[:30]:
        kg.add_relationship("domain", query.lower(), "has_subdomain",
                             "domain", sub, source=observation["source"])


@register_inferer("shodan_internetdb")
def _infer_shodan(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    ip = parsed.get("ip")
    if not ip:
        return
    for cve in parsed.get("cves", [])[:30]:
        kg.add_relationship("ipv4", ip, "has_cve", "cve", cve, source=observation["source"])
    for port in parsed.get("ports", []):
        kg.add_relationship("ipv4", ip, "exposes_port", "port", str(port), source=observation["source"])


@register_inferer("greynoise_community")
def _infer_greynoise(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    ip = parsed.get("ip")
    if ip and parsed.get("classification"):
        kg.add_relationship("ipv4", ip, "classified_as", "classification",
                             parsed["classification"], source=observation["source"])


@register_inferer("abuseipdb_check")
def _infer_abuseipdb(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    ip = parsed.get("ip")
    if ip and parsed.get("abuseConfidenceScore") is not None:
        kg.add_relationship("ipv4", ip, "abuse_score", "score",
                             str(parsed["abuseConfidenceScore"]), source=observation["source"])


@register_inferer("hackertarget_whois")
def _infer_whois(observation: Dict[str, Any], query: str, kg: Any) -> None:
    whois = observation.get("parsed") or {}
    if not isinstance(whois, dict):
        return
    for key, val in whois.items():
        if key.lower() in ("registrant email", "admin email", "tech email") and val:
            kg.add_relationship("domain", query.lower(), "registered_with_email",
                                 "email", val, source=observation["source"])


@register_inferer("urlscan_public")
def _infer_urlscan(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    for r in (parsed.get("results") or [])[:10]:
        for tech in (r.get("technologies") or []):
            if tech:
                kg.add_relationship("domain", r.get("domain") or query.lower(),
                                     "uses_technology", "technology", tech,
                                     source=observation["source"])


@register_inferer("phonebook_email")
@register_inferer("phonebook_domain")
def _infer_phonebook(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    for r in (parsed.get("results") or [])[:30]:
        email = r.get("email") or r.get("domain")
        if r.get("name") and email:
            kind = "email" if "@" in str(email) else "domain"
            kg.add_relationship(kind, str(email), "associated_with_person",
                                 "person", r["name"], source=observation["source"])


@register_inferer("ipapi_free")
def _infer_ipapi(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    ip = parsed.get("ip")
    if ip and parsed.get("country"):
        kg.add_relationship("ipv4", ip, "located_in", "country",
                             parsed["country"], source=observation["source"])


@register_inferer("alienvault_otx")
def _infer_otx(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    for p in (parsed.get("pulses") or [])[:20]:
        adv = p.get("adversary")
        if adv:
            kg.add_relationship("indicator", query, "linked_to_threat_actor",
                                 "threat_actor", adv, source=observation["source"])
        for attack_id in (p.get("attack_ids") or []):
            kg.add_relationship("indicator", query, "mapped_to_technique",
                                 "mitre_technique", attack_id, source=observation["source"])


@register_inferer("nvd_cve")
def _infer_nvd(observation: Dict[str, Any], query: str, kg: Any) -> None:
    parsed = observation.get("parsed") or {}
    for item in (parsed.get("items") or [])[:20]:
        cve = item.get("cve")
        if cve:
            kg.add_relationship("indicator", query, "matches_cve",
                                 "cve", cve, source=observation["source"])
