"""
estorides.web
=============
Flask app providing:
  * 2D map     (Leaflet)
  * knowledge graph (D3.js force-directed)
  * timeline
  * source results panel
  * multi-LLM analysis
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

from flask import Flask, Response, jsonify, render_template, request, send_from_directory

from estorides_core.audit import audit_log, rate_limiter
from estorides_core.config import (DATASET_PATH, FLASK_DEBUG, FLASK_HOST,
    FLASK_PORT, GRAPH_PATH, REPORTS_DIR, STATIC_DIR, TEMPLATES_DIR)
from estorides_core.discoverer import DISCOVER_JOBS, start_discover, list_jobs as list_discover_jobs
from estorides_core.entity_extraction import detect_query_type
from estorides_core.feeds import fetch_all, list_feeds
from estorides_core.knowledge_graph import KnowledgeGraph
from estorides_core.orchestrator import Orchestrator
from estorides_core.validation import QueryValidationError, validate_query
from estorides_export import export_misp, export_stix
from estorides_export.encryption import export_misp_encrypted, export_stix_encrypted

log = logging.getLogger("estorides.web")

# We bind helpers at module level so they can be re-used in tests
# without going through the Flask app factory.

def _client_ip() -> str:
    """Best-effort client IP extraction.

    Trusts X-Forwarded-For only when behind a known proxy
    (ESTORIDES_TRUST_PROXY=1). Without that, falls back to
    `request.remote_addr`. This avoids the classic
    "set X-Forwarded-For to bypass rate limits" mistake on a
    directly-exposed deployment.
    """
    if os.environ.get("ESTORIDES_TRUST_PROXY") == "1":
        fwd = request.headers.get("X-Forwarded-For")
        if fwd:
            # First entry is the original client; the rest are proxies.
            return fwd.split(",")[0].strip()
    return request.remote_addr or "unknown"


def _rate_limit_decorator(*, event: str) -> Callable:
    """Decorator: enforce per-IP rate limit, write an audit row either way.

    Catches the rate-limit denial BEFORE doing real work, so a flood
    can't tie up the orchestrator. Audit row written for both allow
    and deny so the trail is complete.
    """
    def deco(view: Callable) -> Callable:
        @wraps(view)
        def wrapper(*args: Any, **kwargs: Any) -> Response:
            ip = _client_ip()
            allowed, retry = rate_limiter.allow(ip)
            if not allowed:
                audit_log.query(
                    "rate_limited", remote_ip=ip, method=request.method,
                    path=request.path, status="denied", runtime_ms=0.0,
                    retry_after=retry,
                )
                resp = jsonify({"error": "rate-limited", "retry_after": retry})
                resp.status_code = 429
                resp.headers["Retry-After"] = str(retry)
                return resp
            t0 = time.monotonic()
            status = "ok"
            try:
                return view(*args, **kwargs)
            except QueryValidationError as e:
                status = "rejected"
                resp = jsonify({"error": "invalid-query", "reason": e.reason})
                resp.status_code = 400
                return resp
            except Exception:  # noqa: BLE001
                status = "error"
                raise
            finally:
                audit_log.query(
                    event, remote_ip=ip, method=request.method,
                    path=request.path, status=status,
                    runtime_ms=(time.monotonic() - t0) * 1000.0,
                )
        return wrapper
    return deco


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )
    orch = Orchestrator()

    @app.route("/")
    def index() -> Any:
        return render_template("index.html")

    @app.route("/api/status")
    def api_status() -> Any:
        return jsonify(orch.registry.summary())

    @app.route("/api/run", methods=["POST"])
    @_rate_limit_decorator(event="api_run")
    def api_run() -> Any:
        body = request.get_json(silent=True) or {}
        # Validate query through the central guard. A failure here
        # surfaces a 400 with the rejection reason — no orchestrator work.
        q = validate_query(str(body.get("query") or ""))
        t0 = time.monotonic()
        try:
            result = asyncio.run(orch.run(
                q.normalised,
                source_names=body.get("sources") or None,
                include_paid=bool(body.get("include_paid", False)),
                parallel=int(body.get("parallel", 8)),
                timeout=float(body.get("timeout", 8.0)),
                deadline=float(body.get("deadline", 30.0)),
            ))
        except Exception as e:  # noqa: BLE001
            log.exception("run failed")
            return jsonify({"error": str(e)}), 500

        # save graph to disk for later export
        orch.kg.export_graphml(GRAPH_PATH)
        shaped = _shape_for_ui(result)
        # Attach query type so the UI can show "type: domain" without
        # re-detecting on the client.
        shaped["query_type"] = q.type
        shaped["query_normalised"] = q.normalised
        # Audit row for successful runs — observation count and source
        # count go in `extra` so the trail captures run size.
        audit_log.query(
            "api_run", remote_ip=_client_ip(), method=request.method,
            path=request.path, query=q.normalised,
            sources=result.get("sources_queried", 0),
            observations=result.get("sources_succeeded", 0),
            status="ok", runtime_ms=(time.monotonic() - t0) * 1000.0,
            query_type=q.type,
        )
        return jsonify(shaped)

    @app.route("/api/graph")
    def api_graph() -> Any:
        if not GRAPH_PATH.exists():
            return jsonify({"nodes": [], "edges": []})
        import networkx as nx
        kg = KnowledgeGraph()
        kg.graph = nx.read_graphml(GRAPH_PATH)
        # Limit to N nodes for rendering.
        n = int(request.args.get("limit", 200))
        g = kg.graph
        deg = dict(g.degree())
        top = sorted(deg.items(), key=lambda kv: kv[1], reverse=True)[:n]
        keep = {k for k, _ in top}
        sub = g.subgraph(keep).copy()
        nodes = [
            {
                "id": d.get("id"),
                "label": d.get("value", ""),
                "type": d.get("type"),
                "kind": d.get("kind"),
                "color": d.get("color", "#888"),
                "size": 4 + min(20, deg.get(d.get("id"), 0)),
            }
            for _, d in sub.nodes(data=True)
        ]
        edges = [
            {"source": u, "target": v,
             "relation": attrs.get("relation", "related-to")}
            for u, v, attrs in sub.edges(data=True)
            if u in keep and v in keep
        ][:1000]
        return jsonify({"nodes": nodes, "edges": edges,
                        "summary": kg.summary(),
                        "top_entities": kg.top_entities(50)})

    @app.route("/api/feeds")
    @_rate_limit_decorator(event="api_feeds")
    def api_feeds() -> Any:
        """Return real-time feed points (quakes, fires, news) for the map.

        Optional query string:
          bbox=min_lon,min_lat,max_lon,max_lat — drop points outside.
          no_cache=1 — bypass the on-disk cache.
        """
        bbox: Any = None
        bbox_str = request.args.get("bbox")
        if bbox_str:
            try:
                parts = [float(x) for x in bbox_str.split(",")]
                if len(parts) == 4:
                    bbox = tuple(parts)  # type: ignore[assignment]
            except ValueError:
                return jsonify({"error": "invalid bbox"}), 400
        use_cache = request.args.get("no_cache", "0") != "1"
        all_points = fetch_all(bbox=bbox, use_cache=use_cache)
        out: Dict[str, List[Dict[str, Any]]] = {}
        for name, points in all_points.items():
            out[name] = [p.to_dict() for p in points]
        return jsonify({
            "feeds": list_feeds(),
            "points": out,
            "bbox": bbox,
            "fetched_at": time.time(),
        })

    @app.route("/api/export/<fmt>")
    @_rate_limit_decorator(event="api_export")
    def api_export(fmt: str) -> Any:
        import networkx as nx
        if not GRAPH_PATH.exists():
            return jsonify({"error": "no graph — run a query first"}), 400
        kg = KnowledgeGraph()
        kg.graph = nx.read_graphml(GRAPH_PATH)
        # Optional encrypted export: client passes `?key=age1xxx`.
        # When the key is present and the format supports it we
        # produce an .age file; otherwise we fall back to plaintext
        # and let the client encrypt out-of-band.
        age_key = request.args.get("key", "").strip()
        try:
            if fmt == "stix":
                p = REPORTS_DIR / f"bundle_{int(time.time())}.json"
                p = export_stix_encrypted(kg, age_key, p) if age_key else export_stix(kg, path=p)
            elif fmt == "misp":
                p = REPORTS_DIR / f"event_{int(time.time())}.json"
                p = export_misp_encrypted(kg, age_key, p) if age_key else export_misp(kg, path=p)
            elif fmt == "graphml":
                p = kg.export_graphml(REPORTS_DIR / f"graph_{int(time.time())}.graphml")
            elif fmt == "json":
                p = REPORTS_DIR / f"graph_{int(time.time())}.json"
                p.write_text(json.dumps(kg.export_json(), indent=2, ensure_ascii=False),
                             encoding="utf-8")
            else:
                return jsonify({"error": f"unknown format {fmt}"}), 400
        except ValueError as e:
            return jsonify({"error": "invalid-encryption-key", "detail": str(e)}), 400
        except RuntimeError as e:
            return jsonify({"error": "encryption-failed", "detail": str(e)}), 500
        return send_from_directory(p.parent, p.name, as_attachment=True)

    # =======================================================================
    # v1.1 — Case store, Kùzu graph, intel resolver, extra OSINT sources
    # =======================================================================
    try:
        from estorides_core.cases import store as case_store
    except Exception:  # noqa: BLE001
        case_store = None  # type: ignore[assignment]
    try:
        from estorides_core.graph_kuzu import backend as kuzu_backend
    except Exception:  # noqa: BLE001
        kuzu_backend = None  # type: ignore[assignment]
    try:
        from estorides_core.intel_resolver import resolver as intel_resolver
    except Exception:  # noqa: BLE001
        intel_resolver = None  # type: ignore[assignment]

    @app.route("/api/cases", methods=["GET"])
    @_rate_limit_decorator(event="api_cases")
    def api_cases_list() -> Any:
        if case_store is None:
            return jsonify({"error": "case store unavailable"}), 503
        q = request.args.get("q", "").strip()
        qt = request.args.get("type", "").strip()
        limit = int(request.args.get("limit", 20))
        return jsonify({
            "cases": case_store.search_cases(q, limit=limit, query_type=qt),
            "stats": case_store.stats(),
        })

    @app.route("/api/cases/<case_id>", methods=["GET"])
    @_rate_limit_decorator(event="api_cases_get")
    def api_cases_get(case_id: str) -> Any:
        if case_store is None:
            return jsonify({"error": "case store unavailable"}), 503
        case = case_store.get_case(case_id)
        if not case:
            return jsonify({"error": "not-found"}), 404
        full = request.args.get("full", "0") == "1"
        if full:
            case["observations"] = case_store.list_observations(case_id)
            case["entities"] = case_store.list_entities(case_id)
        return jsonify(case)

    @app.route("/api/cases/<case_id>", methods=["DELETE"])
    @_rate_limit_decorator(event="api_cases_delete")
    def api_cases_delete(case_id: str) -> Any:
        if case_store is None:
            return jsonify({"error": "case store unavailable"}), 503
        case_store.delete_case(case_id)
        return jsonify({"deleted": case_id})

    @app.route("/api/intel/resolve", methods=["GET"])
    @_rate_limit_decorator(event="api_intel_resolve")
    def api_intel_resolve() -> Any:
        """Cross-feed entity resolution (Osiris-style /resolve).

        Examples:
          GET /api/intel/resolve?type=ip&id=1.1.1.1
          GET /api/intel/resolve?type=person&id=Tim%20Cook
          GET /api/intel/resolve?type=cve&id=CVE-2024-3094
        """
        if intel_resolver is None:
            return jsonify({"error": "intel resolver unavailable"}), 503
        ent_type = request.args.get("type", "").strip().lower()
        ent_id = request.args.get("id", "").strip()
        if not ent_type or not ent_id:
            return jsonify({
                "error": "missing parameter",
                "usage": "/api/intel/resolve?type=<ip|domain|company|person|country|cve|btc_address|eth_address>&id=<value>"
            }), 400
        out = intel_resolver.resolve(ent_type, ent_id)
        # If Kùzu is up, also dump what we have on this entity in the
        # persistent graph (cross-run memory). The combination of
        # "fresh intel" + "historical observations" is the Palantir
        # payoff: a single endpoint that says "everything we know."
        if kuzu_backend is not None:
            try:
                # Find the canonical id in our schema.
                from estorides_core.graph_kuzu import _node_id, _label_for
                nid = _node_id(ent_type, ent_id)
                neighbors = kuzu_backend.neighbors(nid, hops=2)
                out["persistent_neighbors"] = neighbors
            except Exception as e:  # noqa: BLE001
                out["persistent_neighbors_error"] = str(e)
        return jsonify(out)

    @app.route("/api/intel/graph", methods=["GET"])
    @_rate_limit_decorator(event="api_intel_graph")
    def api_intel_graph() -> Any:
        """Cypher query against the Kùzu persistent graph.

        Examples:
          GET /api/intel/graph?q=MATCH%20(n%3AEnt)%20RETURN%20n.id%20LIMIT%2010
        """
        if kuzu_backend is None:
            return jsonify({"error": "kuzu backend unavailable"}), 503
        q = request.args.get("q", "").strip()
        if not q:
            return jsonify({
                "error": "missing query parameter",
                "usage": "/api/intel/graph?q=<cypher>&limit=N",
                "stats": kuzu_backend.stats(),
            }), 400
        # Defence: only allow MATCH / RETURN-style read queries.
        # We don't want the public endpoint to run arbitrary writes
        # (CREATE / MERGE / DELETE / SET) without auth.
        upper = q.upper().lstrip()
        if not (upper.startswith("MATCH") or upper.startswith("RETURN") or upper.startswith("WITH")):
            return jsonify({
                "error": "read-only endpoint — queries must start with MATCH/RETURN/WITH",
            }), 400
        for forbidden in ("CREATE", "MERGE", "DELETE", "SET ", "DETACH", "DROP", "ALTER"):
            if forbidden in upper:
                return jsonify({
                    "error": f"forbidden keyword {forbidden!r} — read-only endpoint",
                }), 400
        try:
            rows = kuzu_backend.cypher(q)
        except Exception as e:  # noqa: BLE001
            return jsonify({"error": "cypher-failed", "detail": str(e)}), 400
        return jsonify({"rows": rows, "count": len(rows)})

    @app.route("/api/intel/stats", methods=["GET"])
    @_rate_limit_decorator(event="api_intel_stats")
    def api_intel_stats() -> Any:
        """Stats for both the case store and the Kùzu graph."""
        out: Dict[str, Any] = {}
        if case_store is not None:
            out["cases"] = case_store.stats()
        if kuzu_backend is not None:
            out["kuzu"] = kuzu_backend.stats()
        if intel_resolver is not None:
            out["resolver_cache"] = intel_resolver.cache.stats()
        return jsonify(out)

    # ----- Osiris-style extra OSINT endpoints (keyless) -----
    try:
        from estorides_core import osiris_sources
    except Exception:  # noqa: BLE001
        osiris_sources = None  # type: ignore[assignment]

    @app.route("/api/osiris/bgp", methods=["GET"])
    @_rate_limit_decorator(event="api_osiris_bgp")
    def api_osiris_bgp() -> Any:
        if osiris_sources is None:
            return jsonify({"error": "osiris sources unavailable"}), 503
        q = request.args.get("query", "").strip()
        if not q:
            return jsonify({"error": "missing query (IP or ASxxxxx)"}), 400
        return jsonify(osiris_sources.fetch_bgp(q))

    @app.route("/api/osiris/mac", methods=["GET"])
    @_rate_limit_decorator(event="api_osiris_mac")
    def api_osiris_mac() -> Any:
        if osiris_sources is None:
            return jsonify({"error": "osiris sources unavailable"}), 503
        mac = request.args.get("mac", "").strip()
        if not mac:
            return jsonify({"error": "missing mac"}), 400
        return jsonify(osiris_sources.fetch_mac(mac))

    @app.route("/api/osiris/phone", methods=["GET"])
    @_rate_limit_decorator(event="api_osiris_phone")
    def api_osiris_phone() -> Any:
        if osiris_sources is None:
            return jsonify({"error": "osiris sources unavailable"}), 503
        n = request.args.get("number", "").strip()
        if not n:
            return jsonify({"error": "missing number"}), 400
        return jsonify(osiris_sources.fetch_phone(n))

    @app.route("/api/osiris/github", methods=["GET"])
    @_rate_limit_decorator(event="api_osiris_github")
    def api_osiris_github() -> Any:
        if osiris_sources is None:
            return jsonify({"error": "osiris sources unavailable"}), 503
        u = request.args.get("user", "").strip()
        if not u:
            return jsonify({"error": "missing user"}), 400
        return jsonify(osiris_sources.fetch_github_user(u))

    @app.route("/api/osiris/leaks", methods=["GET"])
    @_rate_limit_decorator(event="api_osiris_leaks")
    def api_osiris_leaks() -> Any:
        if osiris_sources is None:
            return jsonify({"error": "osiris sources unavailable"}), 503
        e = request.args.get("email", "").strip()
        if not e:
            return jsonify({"error": "missing email"}), 400
        return jsonify(osiris_sources.fetch_leaks(e))

    @app.route("/api/osiris/cisa-kev", methods=["GET"])
    @_rate_limit_decorator(event="api_osiris_kev")
    def api_osiris_kev() -> Any:
        if osiris_sources is None:
            return jsonify({"error": "osiris sources unavailable"}), 503
        limit = int(request.args.get("limit", 10))
        days = int(request.args.get("days", 30))
        return jsonify(osiris_sources.fetch_cisa_kev(limit=limit, days=days))

    @app.route("/api/osiris/malware", methods=["GET"])
    @_rate_limit_decorator(event="api_osiris_malware")
    def api_osiris_malware() -> Any:
        if osiris_sources is None:
            return jsonify({"error": "osiris sources unavailable"}), 503
        limit = int(request.args.get("limit", 200))
        return jsonify(osiris_sources.fetch_malware_c2(limit=limit))

    @app.route("/api/osiris_threats")
    def api_osiris_threats() -> Any:
        return jsonify({"error": "moved to /api/osiris/*"}), 404

    # --------------------------------------------------------- v1.2 discoverer
    # Background fanout: drop a seed (domain or IP), the worker
    # resolves it, pulls subdomains / siblings out of every
    # source's result, enqueues them, and pushes nodes to the
    # SSE stream in real time. The UI just calls start + subscribes
    # to the stream — no polling, no manual orchestration.

    @app.route("/api/discover/start", methods=["POST"])
    def api_discover_start() -> Any:
        body = request.get_json(silent=True) or {}
        seed_value = (body.get("value") or request.args.get("value") or "").strip()
        seed_type = (body.get("type") or request.args.get("type") or "domain").strip()
        if not seed_value:
            return jsonify({"error": "value is required"}), 400
        # The detect_query_type helper knows the regex; reusing it
        # here means the UI can pass a free-form value and the
        # server figures out if it's an IP, domain, or email.
        if seed_type == "auto":
            seed_type = detect_query_type(seed_value) or "domain"
        # Bounds from the request, capped so a buggy client can't
        # ask for a 10,000-step job.
        try:
            max_depth = min(int(body.get("max_depth", 2)), 3)
            max_steps = min(int(body.get("max_steps", 50)), 200)
            max_entities = min(int(body.get("max_entities", 5000)), 20000)
        except (TypeError, ValueError):
            return jsonify({"error": "max_depth/max_steps/max_entities must be ints"}), 400
        deadline_s = float(body.get("deadline_s", 30.0))
        parallel = min(int(body.get("parallel", 4)), 10)
        # Run the start in a worker thread because it has to
        # await the asyncio task that schedules the background
        # discoverer. The handler itself stays synchronous.
        job = asyncio.run_coroutine_threadsafe(
            start_discover(
                seed_type=seed_type,
                seed_value=seed_value,
                max_depth=max_depth,
                max_steps=max_steps,
                max_entities=max_entities,
                deadline_s=deadline_s,
                parallel=parallel,
            ),
            _background_loop,
        ).result(timeout=15)
        return jsonify({
            "job_id": job.job_id,
            "case_id": job.case_id,
            "status": job.status,
            "stream_url": f"/api/discover/stream?job_id={job.job_id}",
            "max_depth": max_depth,
            "max_steps": max_steps,
        })

    @app.route("/api/discover/jobs", methods=["GET"])
    def api_discover_jobs() -> Any:
        return jsonify({"jobs": list_discover_jobs(limit=int(request.args.get("limit", 20)))})

    @app.route("/api/discover/stop", methods=["POST"])
    def api_discover_stop() -> Any:
        body = request.get_json(silent=True) or {}
        job_id = (body.get("job_id") or request.args.get("job_id") or "").strip()
        job = DISCOVER_JOBS.get(job_id)
        if not job:
            return jsonify({"error": "unknown job_id"}), 404
        job.stop()
        return jsonify({"job_id": job_id, "status": "stopping"})

    @app.route("/api/discover/stream", methods=["GET"])
    def api_discover_stream() -> Any:
        """Server-Sent Events for a discoverer job.

        The browser opens `EventSource('/api/discover/stream?job_id=...')`
        and we keep the connection open, pushing one event per
        JSON line as the background worker discovers things. The
        stream closes when the job finishes (status=done|error|stopped).
        """
        job_id = (request.args.get("job_id") or "").strip()
        job = DISCOVER_JOBS.get(job_id)
        if not job:
            return jsonify({"error": "unknown job_id"}), 404

        def gen():
            # Initial event: tell the client the cursor so reconnects
            # can resume from the right offset.
            cursor = 0
            yield f"event: hello\ndata: {json.dumps({'job_id': job.job_id, 'status': job.status, 'cursor': cursor, 'case_id': job.case_id, 'seed': {'type': job.seed_type, 'value': job.seed_value}})}\n\n"
            last_status = job.status
            idle_ticks = 0
            while True:
                # Drain new events since cursor.
                while cursor < len(job.events):
                    ev = job.events[cursor]
                    cursor += 1
                    yield f"data: {json.dumps(ev)}\n\n"
                # Heartbeats every 5s so the proxy doesn't drop us.
                idle_ticks += 1
                if idle_ticks >= 5:
                    yield f": keepalive {int(time.time())}\n\n"
                    idle_ticks = 0
                # Job ended → send a final 'closed' event and stop.
                if job.status in ("done", "error", "stopped") and cursor >= len(job.events):
                    yield f"event: closed\ndata: {json.dumps({'status': job.status, 'steps_done': job.steps_done, 'entities_seen': job.entities_seen, 'error': job.error})}\n\n"
                    return
                if job.status != last_status:
                    last_status = job.status
                time.sleep(1.0)

        # The right content type for SSE + disable buffering so
        # Flask doesn't accumulate events into a single response.
        return Response(gen(), mimetype="text/event-stream", headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        })

    return app


# The web server is sync (Flask). The discoverer needs an asyncio
# loop. We start a long-lived daemon thread that owns a loop and
# use `asyncio.run_coroutine_threadsafe` from the request handlers
# above to dispatch `start_discover` into it. This avoids spinning
# up a new loop per request and keeps the SSE writer in the same
# loop that the discoverer task runs in.
import threading
def _serve_loop() -> None:
    global _background_loop
    _background_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(_background_loop)
    try:
        _background_loop.run_forever()
    finally:
        _background_loop.close()

_background_loop: asyncio.AbstractEventLoop = None  # type: ignore[assignment]
threading.Thread(target=_serve_loop, daemon=True, name="estorides-discoverer").start()


def _shape_for_ui(result: Dict[str, Any]) -> Dict[str, Any]:
    """Trim raw responses for the UI and reformat observations."""
    obs = []
    for o in result.get("observations", []):
        obs.append({
            "source": o["source"],
            "category": o["category"],
            "description": o["description"],
            "parser": o["parser"],
            "parsed": o.get("parsed"),
            "meta": o.get("meta"),
        })
    return {
        "query": result.get("query"),
        "generated_at": result.get("generated_at"),
        "sources_queried": result.get("sources_queried"),
        "sources_succeeded": result.get("sources_succeeded"),
        "observations": obs,
        "entities": result.get("entities", []),
        "graph": result.get("graph", {}),
        "analysis": result.get("analysis", {}),
    }


if __name__ == "__main__":
    app = create_app()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
