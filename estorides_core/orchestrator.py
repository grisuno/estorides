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
from .config import DATASET_PATH, GRAPH_PATH, SOURCES_DIR
from .entity_extraction import (Entity, detect_query_type, extract_from_json,
                                merge)
from .knowledge_graph import KnowledgeGraph
from .mitre_attack import all_techniques_for, map_observations
from .ontology import ontology
from .parsers import get_parser
from .relationship_inference import infer_relationship
from .source_loader import Source, SourceRegistry

log = logging.getLogger("estorides.orchestrator")

# New modules (v1.0 → v1.1 wiring). Each is wrapped in a try/except
# so a missing optional dep (kuzu, etc.) can never break a run that
# doesn't actually need it.
try:
    from .graph_kuzu import backend as kuzu_backend
except Exception as _e:  # noqa: BLE001
    log.warning("kuzu backend unavailable, running without persistent graph: %s", _e)
    kuzu_backend = None  # type: ignore[assignment]

try:
    from .cases import store as case_store
except Exception as _e:  # noqa: BLE001
    log.warning("case store unavailable, runs will be ephemeral: %s", _e)
    case_store = None  # type: ignore[assignment]

try:
    from .intel_resolver import resolver as intel_resolver
except Exception as _e:  # noqa: BLE001
    log.warning("intel resolver unavailable: %s", _e)
    intel_resolver = None  # type: ignore[assignment]


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
        on_source_result: Optional[Any] = None,
        persist: bool = True,
        case_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Run a full intelligence cycle. Returns a structured result.

        `deadline` is a hard wall-clock cap (seconds) for the whole fanout.
        Any source that hasn't responded by then is dropped and reported as
        "deadline_exceeded" so the run can never get stuck.

        `persist` (default True) writes the run to the persistent case
        store and mirrors every entity/edge to the Kùzu graph. Set
        False for one-off ad-hoc queries (e.g. tests) where you don't
        want the run to bloat the long-term memory.

        `case_id`, when supplied, makes this run append to an existing
        case instead of opening a new one. The recursive pivot engine
        uses this so every hop of a cross-search lands in a single case.

        `on_source_result`, when supplied, is invoked with the shaped
        observation dict the moment each source resolves, before the
        fan-out as a whole completes. This is what lets the UI populate
        progressively instead of blocking on the slowest source."""
        if not query or not query.strip():
            return {"error": "query required", "results": []}
        query = query.strip()

        query_type = detect_query_type(query)
        targets = self._select_sources(source_names, include_paid=include_paid, query_type=query_type)
        if not targets:
            return {"error": f"no sources matched for query_type={query_type}", "results": []}

        # ----- open a case (if persistence is enabled) -----
        # A caller-supplied case_id means "append to this case" (the pivot
        # engine sharing one case across hops); only mint a fresh case when
        # none was provided.
        if case_id is None and persist and case_store is not None:
            try:
                case_id = case_store.create_case(query, query_type)
            except Exception as e:  # noqa: BLE001
                log.warning("case create failed, running ephemeral: %s", e)

        log.info("query_type=%s, running %d sources for query=%r (deadline=%.0fs)",
                 query_type, len(targets), query, deadline)

        # ----- fan out, capped by a global deadline -----
        async with AsyncClient(timeout=timeout, max_parallel=parallel) as client:
            tasks: List[asyncio.Task] = [
                asyncio.create_task(
                    self._execute_source(client, s, query, on_source_done, on_source_result)
                )
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
                # Use whatever did complete, mark the rest as missed.
                # IMPORTANT: a cancelled task's .result() raises
                # CancelledError; only call it for tasks that we know
                # completed without exception. Anything else becomes
                # a synthetic 4-tuple so the downstream unpacking can
                # never trip on a BaseException instance.
                raw_results = []
                for t, s in zip(tasks, targets):
                    if (
                        t.done()
                        and not t.cancelled()
                        and t.exception() is None
                    ):
                        try:
                            raw_results.append(t.result())
                        except Exception as e:  # noqa: BLE001
                            # Defensive: t.exception() said None but
                            # t.result() still raised. Treat as a
                            # failed source rather than crashing.
                            log.warning("source %s result() raised: %s",
                                        s["name"], e)
                            raw_results.append((s, None, None, {
                                "source": s["name"],
                                "error": f"exception:{type(e).__name__}",
                                "error_detail": str(e),
                                "attempts": 0,
                            }))
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
        # `asyncio.gather(..., return_exceptions=True)` puts the actual
        # `Exception` instance (e.g. NameError, KeyError) into the
        # results list when a task raised. Some tasks can also return
        # a value that is not a 4-tuple (e.g. a coroutine that was
        # awaited to completion but whose body had a bug). We sweep
        # the whole list into a normalised form here so the rest of
        # the post-process pipeline can iterate uniformly without
        # ever tripping on a non-iterable element.
        observations: List[Dict[str, Any]] = []
        all_entities: List[Entity] = []
        normalised: List[Tuple[Source, Any, Any, Dict[str, Any]]] = []
        for item, source in zip(raw_results, targets):
            if isinstance(item, BaseException):
                # Surface as an error observation, but keep going so one
                # bad source can't poison the whole run.
                log.warning("source %s raised: %s", source["name"], item)
                normalised.append((source, None, None, {
                    "source": source["name"],
                    "error": f"exception:{item.__class__.__name__}",
                    "error_detail": str(item),
                    "attempts": 0,
                }))
                continue
            # Defensive: a successful task could still return
            # something that is not a 4-tuple if the underlying
            # function is buggy. Wrap any deviation into a synthetic
            # 4-tuple so the downstream `for source, parsed, raw,
            # meta in normalised` cannot trip with
            # "cannot unpack non-iterable X".
            if not isinstance(item, tuple) or len(item) != 4:
                log.warning("source %s returned %r (expected 4-tuple)",
                            source["name"], type(item).__name__)
                normalised.append((source, None, None, {
                    "source": source["name"],
                    "error": f"bad-result-shape:{type(item).__name__}",
                    "attempts": 0,
                }))
                continue
            normalised.append(item)

        for source, parsed, raw, meta in normalised:
            if parsed is None and raw is None:
                # An error observation — still record it so the UI can
                # show which sources failed and why, but don't try to
                # parse entities out of an empty/error response.
                if meta.get("error"):
                    obs = {
                        "source": source["name"],
                        "category": source["category"],
                        "description": source["description"],
                        "parser": source["parser"],
                        "parsed": None,
                        "raw": None,
                        "meta": meta,
                    }
                    try:
                        obs["ontology"] = ontology.check_observation(obs)
                    except Exception as e:  # noqa: BLE001
                        log.debug("ontology check failed for %s: %s", source["name"], e)
                        obs["ontology"] = {"sanctioned": False, "hits": [], "fields": [], "error": str(e)}
                    try:
                        obs["mitre"] = {"techniques": []}
                    except Exception:  # noqa: BLE001
                        pass
                    observations.append(obs)
                    # Persist the error observation too — failure trails
                    # are exactly the kind of thing you want when you
                    # reopen a case six months later.
                    if case_id is not None and case_store is not None:
                        try:
                            case_store.add_observation(case_id, obs)
                        except Exception as e:  # noqa: BLE001
                            log.debug("case observation write failed: %s", e)
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
            # Ontology cross-check: stamp every observation with a
            # sanctions verdict so the LLM analyst stage can mention
            # "SANCTIONED — OFAC SDN match" instead of having to
            # re-derive it. The check is local and CPU-only; for a
            # first-run with an empty cache it returns "unknown"
            # quickly and the result is preserved for the analyst.
            try:
                obs["ontology"] = ontology.check_observation(obs)
            except Exception as e:  # noqa: BLE001
                log.debug("ontology check failed for %s: %s", source["name"], e)
                obs["ontology"] = {"sanctioned": False, "hits": [], "fields": [], "error": str(e)}
            observations.append(obs)

            # Persist the observation to the case store (cheap, in-process).
            if case_id is not None and case_store is not None:
                try:
                    case_store.add_observation(case_id, obs)
                except Exception as e:  # noqa: BLE001
                    log.debug("case observation write failed: %s", e)

            # 1) extract entities once, from the parsed view if we have one
            # (raw is its superset and rescanning it only duplicates work).
            primary = parsed if parsed is not None else raw
            entities = extract_from_json(primary, source["name"])
            all_entities.extend(entities)

            # 2) add to knowledge graph (entity + co-occurrence)
            self.kg.add_observation(source["name"], entities)

            # 2b) mirror the entities to Kùzu (best-effort, non-blocking)
            if kuzu_backend is not None:
                for ent in entities:
                    try:
                        kuzu_backend.upsert_entity(
                            ent.type, ent.value, source=source["name"]
                        )
                    except Exception as e:  # noqa: BLE001
                        log.debug("kuzu mirror entity failed: %s", e)
                        break  # one bad entity should not poison the rest

        # ----- higher-level relationships -----
        self._infer_relationships(observations, query)

        # ----- MITRE ATT&CK mapping -----
        # Stamp every observation with the techniques it suggests, then
        # compute the aggregate technique set so the LLM analyst can
        # mention the relevant tactics without re-deriving them.
        try:
            map_observations(observations)
        except Exception as e:  # noqa: BLE001
            log.debug("mitre mapping failed: %s", e)
        mitre_techniques = all_techniques_for(observations)

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

        # ----- persist entities + finalise the case -----
        if case_id is not None and case_store is not None:
            try:
                case_store.add_entities(
                    case_id, [e.to_dict() for e in merged]
                )
            except Exception as e:  # noqa: BLE001
                log.debug("case entity write failed: %s", e)
            try:
                kg_path_str: Optional[str] = None
                try:
                    kg_path_str = str(self.kg.export_graphml(GRAPH_PATH))
                except Exception as e:  # noqa: BLE001
                    log.debug("kg export for case failed: %s", e)
                case_store.finalise(
                    case_id,
                    analysis=analysis,
                    kg_path=kg_path_str,
                    mitre={"techniques": mitre_techniques},
                    source_count=len(targets),
                    obs_count=len(observations),
                    entity_count=len(merged),
                    status="ok",
                )
            except Exception as e:  # noqa: BLE001
                log.debug("case finalise failed: %s", e)

        # ----- cross-feed enrichment (best-effort, post-LLM) -----
        # Resolve the top entities through the intel resolver to wire
        # them to OFAC + Wikidata + IP-API. The resolver does its own
        # caching, so a case reopened later won't re-fetch the world.
        enrichment: Dict[str, Any] = {}
        if intel_resolver is not None and case_id is not None:
            try:
                # Pick the top 5 entities by seen_count to enrich.
                top = sorted(
                    merged, key=lambda e: e.confidence, reverse=True
                )[:5]
                for ent in top:
                    res = intel_resolver.resolve(ent.type, ent.value)
                    enrichment[f"{ent.type}:{ent.value}"] = res
                    # Also mirror the resolver's nodes/edges into Kùzu.
                    if kuzu_backend is not None:
                        for n in res.get("nodes", []):
                            nprops = n.get("properties", {})
                            kuzu_backend.upsert_entity(
                                n.get("type", "entity"),
                                n.get("label", n.get("id", "")),
                                kind=n.get("kind"),
                            )
                        for link in res.get("links", []):
                            src = link.get("source", "")
                            dst = link.get("target", "")
                            rel = link.get("relation", "")
                            # Parse the type: id form back into
                            # (type, value) so Kùzu can normalise.
                            if ":" in src and ":" in dst and rel:
                                s_t, s_v = src.split(":", 1)
                                d_t, d_v = dst.split(":", 1)
                                try:
                                    kuzu_backend.upsert_relationship(
                                        s_t, s_v, rel, d_t, d_v
                                    )
                                except Exception:
                                    pass
            except Exception as e:  # noqa: BLE001
                log.debug("intel enrichment failed: %s", e)

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
            "mitre": {"techniques": mitre_techniques},
            "analysis": analysis,
            "case_id": case_id,
            "enrichment": enrichment,
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
        on_result: Optional[Any] = None,
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

        # Stream the per-source observation the instant it resolves so a
        # subscriber (the SSE layer) can render it without waiting for the
        # whole fan-out. The downstream batch still produces the canonical,
        # ontology/MITRE-stamped observation; this is the live preview.
        if on_result is not None:
            try:
                on_result({
                    "source": source["name"],
                    "category": source["category"],
                    "description": source["description"],
                    "parser": source["parser"],
                    "parsed": parsed,
                    "meta": meta,
                })
            except Exception:  # never let a subscriber break the run
                pass

        return source, parsed, data, meta

    def _infer_relationships(self, observations: List[Dict[str, Any]], query: str) -> None:
        """Delegate each observation to its registered inferer.

        The previous version of this method was a 90-line `if/elif`
        chain hard-coded to specific source names. The new version
        walks the inferer registry; sources with no inferer are
        silently skipped. Adding a new inferer is now: write a
        function and `@register_inferer("source_name")` it. No edits
        to this method.
        """
        for obs in observations:
            infer_relationship(obs, query, self.kg)

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
