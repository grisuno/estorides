"""
estorides_core.orchestrator
============================
The main entry point. Glues together:
  * source registry  (source_loader)
  * async http       (async_client)
  * parsers          (parsers)
  * entity extract   (entity_extraction)
  * knowledge graph  (knowledge_graph)
  * LLM manager      (llm.manager)
  * dataset export   (exporters)

Public surface:
  orchestrator = Orchestrator()
  await orchestrator.run(query, ...)
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from estorides_llm import LLMManager
from .async_client import AsyncClient
from .config import DATASET_PATH, SOURCES_DIR
from .entity_extraction import (Entity, detect_query_type, extract_from_json,
                                merge)
from .knowledge_graph import KnowledgeGraph
from .parsers import get_parser
from .source_loader import Source, SourceRegistry

log = logging.getLogger("estorides.orchestrator")


def _safe_format(template: Any, **kwargs: Any) -> Any:
    """Format a string template with {key} placeholders.

    Non-string values (int, list, dict) are returned as-is so YAMLs that
    use raw integers or list literals in params/body don't blow up."""
    if not isinstance(template, str):
        return template
    def repl(m: re.Match[str]) -> str:
        return str(kwargs.get(m.group(1), m.group(0)))
    return re.sub(r"\{([^}]+)\}", repl, template)


def _resolve_auth(source: Source) -> Optional[str]:
    """Look up the API key for a source that needs one."""
    if not source.get("requires_key"):
        return None
    env_name = source.get("key_env")
    if not env_name:
        return None
    return __import__("os").environ.get(env_name)


def _domain_from_query(q: str) -> Optional[str]:
    """Heuristic: if the query looks like a domain, return it; if it's an IP, return None."""
    q = q.strip()
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", q):
        return None
    if re.match(r"^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$", q):
        return q.lower()
    return None


class Orchestrator:
    def __init__(self) -> None:
        self.registry = SourceRegistry(SOURCES_DIR)
        self.registry.load()
        self.llm = LLMManager()
        self.kg = KnowledgeGraph()

    # -------------------------------------------------------------- single
    async def run(
        self,
        query: str,
        *,
        source_names: Optional[List[str]] = None,
        include_paid: bool = False,
        parallel: int = 8,
        timeout: float = 12.0,
        deadline: float = 30.0,
        on_source_done: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Run a full intelligence cycle. Returns a structured result.

        `deadline` is a hard wall-clock cap (seconds) for the whole fanout.
        Any source that hasn't responded by then is dropped and reported as
        "deadline_exceeded" so the run can never get stuck."""
        if not query or not query.strip():
            return {"error": "query required", "results": []}
        query = query.strip()

        query_type = detect_query_type(query)
        targets = self._select_sources(source_names, include_paid=include_paid, query_type=query_type)
        if not targets:
            return {"error": f"no sources matched for query_type={query_type}", "results": []}

        log.info("query_type=%s, running %d sources for query=%r (deadline=%.0fs)",
                 query_type, len(targets), query, deadline)

        # ----- fan out, capped by a global deadline -----
        async with AsyncClient(timeout=timeout, max_parallel=parallel) as client:
            tasks: List[asyncio.Task] = [
                asyncio.create_task(self._execute_source(client, s, query, on_source_done))
                for s in targets
            ]
            try:
                raw_results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=deadline,
                )
            except asyncio.TimeoutError:
                log.warning("deadline %.0fs reached, cancelling %d pending sources",
                            deadline, sum(1 for t in tasks if not t.done()))
                for t in tasks:
                    if not t.done():
                        t.cancel()
                # give cancelled tasks a moment to clean up
                await asyncio.gather(*tasks, return_exceptions=True)
                # Use whatever did complete, mark the rest as missed
                raw_results = []
                for t, s in zip(tasks, targets):
                    if t.done() and not t.cancelled() and t.exception() is None:
                        raw_results.append(t.result())
                    else:
                        raw_results.append((s, None, None, {
                            "source": s["name"],
                            "error": "deadline_exceeded",
                            "attempts": 0,
                        }))
                # also fire the on_done callback for missed sources
                if on_source_done is not None:
                    for s, _, _, meta in raw_results:
                        if meta.get("error") == "deadline_exceeded":
                            try:
                                on_source_done(s["name"], False, "deadline", deadline * 1000.0)
                            except Exception:
                                pass

        # ----- post-process -----
        observations: List[Dict[str, Any]] = []
        all_entities: List[Entity] = []
        for source, parsed, raw, meta in raw_results:
            if parsed is None and raw is None:
                continue
            obs = {
                "source": source["name"],
                "category": source["category"],
                "description": source["description"],
                "parser": source["parser"],
                "parsed": parsed,
                "raw": raw,
                "meta": meta,
            }
            observations.append(obs)

            # 1) extract entities once, from the parsed view if we have one
            # (raw is its superset and rescanning it only duplicates work).
            primary = parsed if parsed is not None else raw
            entities = extract_from_json(primary, source["name"])
            all_entities.extend(entities)

            # 2) add to knowledge graph (entity + co-occurrence)
            self.kg.add_observation(source["name"], entities)

        # ----- higher-level relationships -----
        self._infer_relationships(observations, query)

        # ----- entity summary -----
        merged = merge(all_entities)

        # ----- LLM analysis (also bounded — never let a slow LLM block the run) -----
        # The request_timeout is threaded into the underlying HTTP calls so the
        # worker thread actually returns; otherwise wait_for would abandon it and
        # asyncio.run() would still block on the orphan at shutdown.
        llm_budget = min(deadline, 10.0)
        try:
            analysis = await asyncio.wait_for(
                asyncio.to_thread(
                    self.llm.generate,
                    f"Produce an intelligence assessment of the target '{query}'.",
                    context=observations,
                    request_timeout=llm_budget,
                ),
                timeout=llm_budget + 2.0,
            )
        except asyncio.TimeoutError:
            log.warning("LLM analysis exceeded timeout, returning stub")
            analysis = {
                "backend": "stub", "model": "stub",
                "content": "[LLM analysis skipped — exceeded timeout]",
                "error": "llm_timeout",
            }

        # ----- export -----
        self._write_dataset(query, observations, merged, analysis)

        return {
            "query": query,
            "generated_at": time.time(),
            "sources_queried": len(targets),
            "sources_succeeded": len(observations),
            "observations": observations,
            "entities": [e.to_dict() for e in merged],
            "graph": {
                "summary": self.kg.summary(),
                "top_entities": self.kg.top_entities(20),
            },
            "analysis": analysis,
        }

    # ----------------------------------------------------------- internals
    def _select_sources(
        self,
        names: Optional[List[str]],
        *,
        include_paid: bool,
        query_type: Optional[str] = None,
    ) -> List[Source]:
        if names:
            chosen = [self.registry.get(n) for n in names]
            chosen = [s for s in chosen if s is not None]
        else:
            chosen = list(self.registry.all())
        if not include_paid:
            chosen = [s for s in chosen if not s["requires_key"]]
        if query_type:
            # Keep sources whose applies_to contains "any" or the query_type.
            chosen = [s for s in chosen
                      if "any" in s.get("applies_to", ["any"]) or query_type in s.get("applies_to", [])]
        return chosen

    async def _execute_source(
        self,
        client: AsyncClient,
        source: Source,
        query: str,
        on_done: Optional[Any] = None,
    ) -> Tuple[Source, Any, Any, Dict[str, Any]]:
        tool = source["tool"]
        method = (tool.get("method") or "GET").upper()
        api_key = _resolve_auth(source)

        # ----- format url/headers/params/body with query + api_key -----
        fmt = {"query": query, "api_key": api_key or ""}
        url = _safe_format(tool.get("url", ""), **fmt)
        headers = {k: _safe_format(v, **fmt) for k, v in (tool.get("headers") or {}).items()}
        params = {k: _safe_format(v, **fmt) for k, v in (tool.get("params") or {}).items()}
        body = {k: _safe_format(v, **fmt) for k, v in (tool.get("body") or {}).items()} or None

        t0 = time.monotonic()
        data, meta = await client.fetch(method, url, headers=headers, params=params, body=body)
        elapsed_ms = (time.monotonic() - t0) * 1000.0
        meta["source"] = source["name"]

        if on_done is not None:
            try:
                ok = data is not None
                on_done(source["name"], ok, meta.get("status", "—"), elapsed_ms)
            except Exception:  # never let the callback break the run
                pass

        # ----- structured parse if available -----
        parser = get_parser(source["parser"])
        parsed: Any = None
        try:
            if data is not None:
                parsed = parser(data)
        except Exception as e:  # noqa: BLE001
            log.debug("parser %s failed for %s: %s", source["parser"], source["name"], e)

        return source, parsed, data, meta

    def _infer_relationships(self, observations: List[Dict[str, Any]], query: str) -> None:
        """Heuristics: build explicit edges between entities that share a source
        AND have a structural link (e.g. domain→IP from DNS, IP→ASN from RIPE)."""
        for obs in observations:
            parsed = obs.get("parsed")
            if not isinstance(parsed, dict):
                continue
            src = obs["source"]

            # domain -> ip (DNS)
            if src == "dns_google" or src == "dns_cloudflare" or src == "dns_lookup":
                records = parsed.get("records") or {}
                for ip in records.get("1", []):
                    self.kg.add_relationship("domain", query.lower(), "resolves_to",
                                             "ipv4", ip, source=src)

            # crtsh -> subdomains -> linked to query
            if src == "crtsh_certificates":
                for sub in (parsed.get("subdomains") or [])[:30]:
                    self.kg.add_relationship("domain", query.lower(), "has_subdomain",
                                             "domain", sub, source=src)

            # shodan_internetdb -> ip ports/cves
            if src == "shodan_internetdb":
                ip = parsed.get("ip")
                for cve in parsed.get("cves", [])[:30]:
                    self.kg.add_relationship("ipv4", ip, "has_cve",
                                             "cve", cve, source=src)
                for port in parsed.get("ports", []):
                    self.kg.add_relationship("ipv4", ip, "exposes_port",
                                             "port", str(port), source=src)

            # greynoise -> ip classification
            if src == "greynoise_community":
                ip = parsed.get("ip")
                if ip and parsed.get("classification"):
                    self.kg.add_relationship("ipv4", ip, "classified_as",
                                             "classification",
                                             parsed["classification"], source=src)

            # abuseipdb -> ip confidence
            if src == "abuseipdb_check":
                ip = parsed.get("ip")
                if ip and parsed.get("abuseConfidenceScore") is not None:
                    self.kg.add_relationship("ipv4", ip, "abuse_score",
                                             "score", str(parsed["abuseConfidenceScore"]),
                                             source=src)

            # whois -> registrant email
            if src == "hackertarget_whois":
                whois = parsed  # dict from whois_text
                for key, val in (whois.items() if isinstance(whois, dict) else []):
                    if key.lower() in ("registrant email", "admin email", "tech email") and val:
                        self.kg.add_relationship("domain", query.lower(), "registered_with_email",
                                                 "email", val, source=src)

            # urlscan -> technologies
            if src == "urlscan_public":
                for r in (parsed.get("results") or [])[:10]:
                    for tech in (r.get("technologies") or []):
                        if tech:
                            self.kg.add_relationship("domain", r.get("domain") or query.lower(),
                                                     "uses_technology", "technology", tech,
                                                     source=src)

            # phonebook -> email -> person/company
            if src in ("phonebook_email", "phonebook_domain"):
                for r in (parsed.get("results") or [])[:30]:
                    email = r.get("email") or r.get("domain")
                    if r.get("name") and email:
                        self.kg.add_relationship("email" if "@" in str(email) else "domain",
                                                 str(email), "associated_with_person",
                                                 "person", r["name"], source=src)

            # ipapi -> ip -> country
            if src == "ipapi_free":
                ip = parsed.get("ip")
                if ip and parsed.get("country"):
                    self.kg.add_relationship("ipv4", ip, "located_in",
                                             "country", parsed["country"], source=src)

            # otx -> pulses -> adversary
            if src == "alienvault_otx":
                for p in (parsed.get("pulses") or [])[:20]:
                    adv = p.get("adversary")
                    if adv:
                        self.kg.add_relationship("indicator", query, "linked_to_threat_actor",
                                                 "threat_actor", adv, source=src)
                    for attack_id in (p.get("attack_ids") or []):
                        self.kg.add_relationship("indicator", query, "mapped_to_technique",
                                                 "mitre_technique", attack_id, source=src)

            # nvd_cve -> indicator
            if src == "nvd_cve":
                for item in (parsed.get("items") or [])[:20]:
                    cve = item.get("cve")
                    if cve:
                        self.kg.add_relationship("indicator", query, "matches_cve",
                                                 "cve", cve, source=src)

    def _write_dataset(self, query: str, observations, entities, analysis):
        record = {
            "query": query,
            "timestamp": time.time(),
            "observation_count": len(observations),
            "entities": [e.to_dict() for e in entities],
            "analysis": analysis,
            "graph_summary": self.kg.summary(),
        }
        with DATASET_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
