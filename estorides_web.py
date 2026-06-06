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
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request, send_from_directory

from estorides_core.config import (DATASET_PATH, FLASK_DEBUG, FLASK_HOST,
                                   FLASK_PORT, GRAPH_PATH, REPORTS_DIR,
                                   STATIC_DIR, TEMPLATES_DIR)
from estorides_core.knowledge_graph import KnowledgeGraph
from estorides_core.orchestrator import Orchestrator
from estorides_export import export_misp, export_stix

log = logging.getLogger("estorides.web")


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
    def api_run() -> Any:
        body = request.get_json(force=True) or {}
        query = (body.get("query") or "").strip()
        if not query:
            return jsonify({"error": "query required"}), 400
        try:
            result = asyncio.run(orch.run(
                query,
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
        return jsonify(_shape_for_ui(result))

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

    @app.route("/api/export/<fmt>")
    def api_export(fmt: str) -> Any:
        import networkx as nx
        if not GRAPH_PATH.exists():
            return jsonify({"error": "no graph — run a query first"}), 400
        kg = KnowledgeGraph()
        kg.graph = nx.read_graphml(GRAPH_PATH)
        if fmt == "stix":
            p = export_stix(kg, path=REPORTS_DIR / f"bundle_{int(time.time())}.json")
        elif fmt == "misp":
            p = export_misp(kg, path=REPORTS_DIR / f"event_{int(time.time())}.json")
        elif fmt == "graphml":
            p = kg.export_graphml(REPORTS_DIR / f"graph_{int(time.time())}.graphml")
        elif fmt == "json":
            p = REPORTS_DIR / f"graph_{int(time.time())}.json"
            p.write_text(json.dumps(kg.export_json(), indent=2, ensure_ascii=False),
                         encoding="utf-8")
        else:
            return jsonify({"error": f"unknown format {fmt}"}), 400
        return send_from_directory(p.parent, p.name, as_attachment=True)

    return app


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
