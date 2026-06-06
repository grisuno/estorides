#!/usr/bin/env python3
"""
estorides CLI.

Usage:
  estorides "example.com"
  estorides "8.8.8.8" --include-paid
  estorides "user@example.com" --only-sources shodan_internetdb,ipapi_free
  estorides graph --export graphml
  estorides report --query "example.com" --out report.md
  estorides stix --out bundle.json
  estorides serve --port 5050
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any, List

from estorides_core.config import (DATASET_PATH, FLASK_HOST, FLASK_PORT,
                                   GRAPH_PATH, REPORTS_DIR, REPORTS_DIR as RD)
from estorides_core.knowledge_graph import KnowledgeGraph
from estorides_core.orchestrator import Orchestrator
from estorides_export import export_misp, export_stix


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level,
                        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
                        datefmt="%H:%M:%S")


async def cmd_run(args: argparse.Namespace) -> int:
    orch = Orchestrator()
    sources = None
    if args.only_sources:
        sources = [s.strip() for s in args.only_sources.split(",") if s.strip()]

    # Per-source progress on stderr so the user can see what's happening.
    import sys as _sys
    def _on_done(source_name: str, ok: bool, status: Any, elapsed_ms: float) -> None:
        mark = "OK" if ok else "--"
        print(f"  [{mark}] {source_name:<28} status={status}  ({elapsed_ms:.0f}ms)", file=_sys.stderr, flush=True)

    result = await orch.run(
        args.query,
        source_names=sources,
        include_paid=args.include_paid,
        parallel=args.parallel,
        timeout=args.timeout,
        deadline=args.deadline,
        on_source_done=_on_done,
    )
    if "error" in result and not result.get("observations"):
        print(json.dumps(result, indent=2))
        return 2

    # print summary
    s = result.get("graph", {}).get("summary", {})
    print(f"\n=== Estorides Report ===")
    print(f"Query: {result['query']}")
    print(f"Sources queried: {result['sources_queried']} | succeeded: {result['sources_succeeded']}")
    print(f"Entities: {len(result['entities'])} | Graph: {s.get('node_count',0)} nodes / {s.get('edge_count',0)} edges")

    # top entities
    if result.get("graph", {}).get("top_entities"):
        print("\nTop entities (by degree):")
        for e in result["graph"]["top_entities"][:15]:
            etype = e.get("type") or "?"
            value = str(e.get("value") or "")
            score = e.get("score") or 0
            print(f"  {etype:<14} {value:<50} score={score:.1f}")

    if result.get("analysis"):
        print("\n=== LLM Analysis ===")
        a = result["analysis"]
        print(f"(backend={a.get('backend')}, model={a.get('model')})")
        print(a.get("content", ""))

    # write json
    if args.out_json:
        out_json = args.out_json
    else:
        ts = result.get("generated_at") or time.time()
        out_json = f"estorides_result_{int(ts)}.json"
    Path(out_json).write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str),
                              encoding="utf-8")
    print(f"\nFull JSON: {out_json}")
    print(f"Dataset:   {DATASET_PATH}")
    print(f"Graph:     {GRAPH_PATH}")
    return 0


def cmd_graph_export(args: argparse.Namespace) -> int:
    kg = KnowledgeGraph()
    # The orchestrator only persists via the dataset, not the graph.
    # For now, we re-load the latest graphml if it exists; otherwise return empty.
    if GRAPH_PATH.exists():
        import networkx as nx
        kg.graph = nx.read_graphml(GRAPH_PATH)
        print(f"Loaded {kg.graph.number_of_nodes()} nodes / {kg.graph.number_of_edges()} edges")
    else:
        print("No graph found — run a query first.")
        return 1
    if args.format == "graphml":
        p = kg.export_graphml(GRAPH_PATH)
    elif args.format == "json":
        p = Path("estorides_graph.json")
        p.write_text(json.dumps(kg.export_json(), indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        print(f"Unknown format {args.format}")
        return 2
    print(f"Exported: {p}")
    return 0


def cmd_export_stix(args: argparse.Namespace) -> int:
    import networkx as nx
    kg = KnowledgeGraph()
    if GRAPH_PATH.exists():
        kg.graph = nx.read_graphml(GRAPH_PATH)
    p = export_stix(kg, path=Path(args.out))
    print(f"STIX bundle: {p}")
    return 0


def cmd_export_misp(args: argparse.Namespace) -> int:
    import networkx as nx
    kg = KnowledgeGraph()
    if GRAPH_PATH.exists():
        kg.graph = nx.read_graphml(GRAPH_PATH)
    p = export_misp(kg, path=Path(args.out))
    print(f"MISP event: {p}")
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    orch = Orchestrator()
    summary = orch.registry.summary()
    print(json.dumps(summary, indent=2))
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    # Bootstrap sys.path so `python3 estorides_cli.py serve` works without
    # requiring the user to set PYTHONPATH.
    cli_dir = Path(__file__).resolve().parent
    if str(cli_dir) not in sys.path:
        sys.path.insert(0, str(cli_dir))
    from estorides_web import create_app
    app = create_app()
    app.run(host=args.host, port=args.port, debug=args.debug, threaded=True)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="estorides", description="State-level OSINT orchestrator")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="run a query")
    run.add_argument("query")
    run.add_argument("--include-paid", action="store_true", help="enable sources that need an API key")
    run.add_argument("--only-sources", help="comma-separated list of source names")
    run.add_argument("--parallel", type=int, default=8, help="max concurrent sources (default 8)")
    run.add_argument("--timeout", type=float, default=8.0, help="per-source HTTP timeout in seconds (default 8)")
    run.add_argument("--deadline", type=float, default=30.0,
                     help="hard wall-clock cap for the whole run in seconds (default 30). "
                          "Sources still running at this point are dropped.")
    run.add_argument("--out-json", help="path to write full result JSON")
    run.set_defaults(func=lambda a: asyncio.run(cmd_run(a)))

    g = sub.add_parser("graph", help="export knowledge graph")
    g.add_argument("--export", dest="format", choices=["graphml", "json"], default="graphml")
    g.set_defaults(func=cmd_graph_export)

    s = sub.add_parser("stix", help="export STIX 2.1 bundle")
    s.add_argument("--out", default="estorides_bundle.json")
    s.set_defaults(func=cmd_export_stix)

    m = sub.add_parser("misp", help="export MISP event JSON")
    m.add_argument("--out", default="estorides_misp.json")
    m.set_defaults(func=cmd_export_misp)

    sub.add_parser("status", help="list sources and categories").set_defaults(func=cmd_status)

    sv = sub.add_parser("serve", help="run the web UI")
    sv.add_argument("--host", default=FLASK_HOST)
    sv.add_argument("--port", type=int, default=FLASK_PORT)
    sv.add_argument("--debug", action="store_true")
    sv.set_defaults(func=cmd_serve)

    return p


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    _setup_logging(args.verbose)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
