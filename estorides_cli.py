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
from estorides_core.validation import QueryValidationError, validate_query
from estorides_export import export_misp, export_stix


TOR_DEFAULT_PROXY = "socks5://127.0.0.1:9050"


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level,
                        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
                        datefmt="%H:%M:%S")


def _collect_selectors(events: List[dict], types: tuple) -> dict:
    """Group discovered entity values by type for the requested type set.

    Used to surface the human selectors (emails, usernames, persons, orgs,
    phones) a discover run found, separately from the infrastructure list."""
    buckets: dict = {t: set() for t in types}
    for ev in events:
        if ev.get("type") != "node_found":
            continue
        ent = ev.get("entity") or {}
        et = ent.get("type")
        if et in buckets and ent.get("value"):
            buckets[et].add(ent["value"])
    return {t: sorted(v) for t, v in buckets.items() if v}


def _resolve_proxy(args: argparse.Namespace) -> str | None:
    """Resolve the egress proxy from the OPSEC flags.

    `--tor` is a convenience alias for the default local Tor SOCKS port;
    an explicit `--proxy` wins over it. Returns None when neither is set,
    in which case the engine still honours the env-configured proxy pool."""
    if getattr(args, "proxy", None):
        return args.proxy
    if getattr(args, "tor", False):
        return TOR_DEFAULT_PROXY
    return None


def _add_opsec_flags(parser: argparse.ArgumentParser) -> None:
    """Attach the shared operator-OPSEC flags to a subcommand parser."""
    parser.add_argument(
        "--passive-only", action="store_true",
        help="only query sources that never touch the target (contact=none); "
             "excludes third-party broker probes such as traceroute/ping/header fetch",
    )
    parser.add_argument(
        "--proxy", default=None,
        help="route all egress through this proxy, e.g. socks5://127.0.0.1:9050 "
             "or http://127.0.0.1:8080 (SOCKS needs the aiohttp_socks package)",
    )
    parser.add_argument(
        "--tor", action="store_true",
        help=f"shorthand for --proxy {TOR_DEFAULT_PROXY}",
    )


async def cmd_discover(args: argparse.Namespace) -> int:
    """v1.2 — fanout the surface from a seed.

    Mirrors the /api/discover/start endpoint but as a CLI subcommand
    so an operator can drop a seed in a terminal and walk away.
    Streams progress to stdout. The final case is dumped to
    --out-json if provided.
    """
    from estorides_core.discoverer import start_discover
    from estorides_core.cases import store as case_store
    seed_type = args.type
    if seed_type == "auto":
        from estorides_core.entity_extraction import detect_query_type
        seed_type = detect_query_type(args.query) or "domain"
    log = logging.getLogger("estorides.cli.discover")
    log.info(
        "starting background discover seed=%s:%s max_depth=%d max_steps=%d",
        seed_type, args.query, args.max_depth, args.max_steps,
    )
    proxy = _resolve_proxy(args)
    if args.passive_only:
        log.info("opsec: passive-only — target-touching sources excluded")
    if proxy:
        log.info("opsec: egress via proxy %s", proxy)
    job = await start_discover(
        seed_type=seed_type,
        seed_value=args.query,
        max_depth=args.max_depth,
        max_steps=args.max_steps,
        max_entities=args.max_entities,
        deadline_s=args.deadline,
        parallel=args.parallel,
        passive_only=args.passive_only,
        proxy=proxy,
    )
    # Poll the job's event buffer until the worker ends, printing
    # a one-line summary per event so the operator sees the surface
    # grow in real time.
    last_emit = 0
    while True:
        s = job.status
        if s in ("done", "error", "stopped"):
            break
        if time.time() - last_emit > 1.0 and job.events:
            # Show only the most recent N events since the last print
            # to keep the terminal readable.
            for ev in job.events[-8:]:
                t = ev.get("type")
                if t == "node_found":
                    e = ev.get("entity") or {}
                    src = (ev.get("from") or {}).get("value", "")
                    log.info("  + %s = %s  (from %s, depth %d)",
                             e.get("type"), e.get("value"), src, ev.get("depth"))
                elif t == "step_done":
                    log.info("  step %d done · +%d new in queue · %d remaining",
                             ev.get("step"), ev.get("new_to_queue", 0), ev.get("queue_remaining", 0))
            last_emit = time.time()
        await asyncio.sleep(0.5)
    # Final summary + dump.
    log.info("done · %d steps · %d entities seen · %d events",
             job.steps_done, job.entities_seen, len(job.events))
    # Pull the final case so the operator gets a stable artifact.
    case = case_store.get_case(job.case_id) or {}
    # Build a minimal surface JSON: seed + every domain/ip entity
    # the discoverer recorded.
    surface = {
        "seed": {"type": job.seed_type, "value": job.seed_value},
        "case_id": job.case_id,
        "steps_done": job.steps_done,
        "entities_seen": job.entities_seen,
        "domains": sorted({
            e.get("value", "")
            for ev in job.events
            if ev.get("type") == "node_found"
            for e in [ev.get("entity") or {}]
            if e.get("type") in ("domain", "ipv4", "ipv6")
        }),
        "people": _collect_selectors(job.events, ("email", "username", "person", "org", "phone_e164")),
        "case_summary": case,
    }
    if args.out_json:
        with open(args.out_json, "w") as f:
            json.dump(surface, f, ensure_ascii=False, indent=2, default=str)
        log.info("wrote surface to %s", args.out_json)
    # Friendly stdout summary so the operator can eyeball the
    # size of the discovered surface.
    print(
        f"\n=== Discover summary ===\n"
        f"  seed        : {job.seed_type}:{job.seed_value}\n"
        f"  case_id     : {job.case_id}\n"
        f"  status      : {job.status}\n"
        f"  steps       : {job.steps_done}\n"
        f"  entities    : {job.entities_seen}\n"
        f"  domains     : {len(surface['domains'])}\n"
    )
    if surface['domains']:
        sample = surface['domains'][:15]
        for d in sample:
            print(f"    - {d}")
        if len(surface['domains']) > 15:
            print(f"    … and {len(surface['domains']) - 15} more")
    people = surface.get("people") or {}
    if people:
        total = sum(len(v) for v in people.values())
        print(f"\n  people/selectors ({total}):")
        for sel_type, values in people.items():
            shown = ", ".join(values[:8])
            more = f" … +{len(values) - 8}" if len(values) > 8 else ""
            print(f"    {sel_type:<11}: {shown}{more}")
    return 0 if job.status == "done" else 1


async def cmd_run(args: argparse.Namespace) -> int:
    # Validate the query the same way the web layer does. A failure here
    # surfaces a clean error to the operator instead of a half-built run.
    try:
        q = validate_query(args.query)
    except QueryValidationError as e:
        print(f"error: invalid query ({e.reason}): {e}", file=sys.stderr)
        return 2
    args.query = q.normalised

    orch = Orchestrator()
    sources = None
    if args.only_sources:
        sources = [s.strip() for s in args.only_sources.split(",") if s.strip()]

    # Per-source progress on stderr so the user can see what's happening.
    import sys as _sys
    def _on_done(source_name: str, ok: bool, status: Any, elapsed_ms: float) -> None:
        mark = "OK" if ok else "--"
        print(f"  [{mark}] {source_name:<28} status={status}  ({elapsed_ms:.0f}ms)", file=_sys.stderr, flush=True)

    proxy = _resolve_proxy(args)
    if args.passive_only:
        print("  [opsec] passive-only: target-touching sources excluded", file=_sys.stderr)
    if proxy:
        print(f"  [opsec] egress via proxy: {proxy}", file=_sys.stderr)
    result = await orch.run(
        args.query,
        source_names=sources,
        include_paid=args.include_paid,
        parallel=args.parallel,
        timeout=args.timeout,
        deadline=args.deadline,
        on_source_done=_on_done,
        passive_only=args.passive_only,
        proxy=proxy,
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


def cmd_scope(args: argparse.Namespace) -> int:
    """Classify discovered assets against a program's scope rules.

    Reads assets (a `discover --out-json` surface or a flat host list),
    applies the in/out-of-scope rules, and emits the in-scope host/IP
    lists an operator pipes into the active phase. Out-of-scope assets are
    surfaced explicitly so they are never targeted by accident."""
    from estorides_core.scope import (build_report, load_assets,
                                       load_rules_file, write_flat_lists)

    assets_path = Path(args.assets)
    scope_path = Path(args.scope)
    if not assets_path.exists():
        print(f"error: assets file not found: {assets_path}", file=sys.stderr)
        return 2
    if not scope_path.exists():
        print(f"error: scope rules file not found: {scope_path}", file=sys.stderr)
        return 2

    matcher = load_rules_file(scope_path)
    assets = load_assets(assets_path)
    report = build_report(matcher, assets)

    print("\n=== Scope classification ===")
    print(f"  assets read   : {len(assets)}")
    print(f"  in-scope      : {len(report.in_scope)}  ({len(report.hosts)} hosts / {len(report.ips)} IPs)")
    print(f"  out-of-scope  : {len(report.out_of_scope)}")
    print(f"  unknown       : {len(report.unknown)}")
    if report.out_of_scope:
        print("\n  Out-of-scope (do NOT target):")
        for a in report.out_of_scope[:15]:
            print(f"    ! {a}")
        if len(report.out_of_scope) > 15:
            print(f"    … and {len(report.out_of_scope) - 15} more")

    if args.out:
        Path(args.out).write_text(
            json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\n  report JSON   : {args.out}")
    if args.flat_dir:
        written = write_flat_lists(report, Path(args.flat_dir))
        for label, path in written.items():
            print(f"  {label:<14}: {path}")
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
    _add_opsec_flags(run)
    run.set_defaults(func=lambda a: asyncio.run(cmd_run(a)))

    # v1.2 — background discoverer. Walks the surface from a
    # seed: resolves it, picks out newly-discovered subdomains /
    # sibling domains, enqueues them, and repeats up to a depth
    # cap. Streams progress to stdout so an operator can watch
    # the surface grow.
    disc = sub.add_parser(
        "discover",
        help="background subdomain/domain fanout from a seed (domain or IP)",
    )
    disc.add_argument("query", help="seed value: domain, IP, or email")
    disc.add_argument("--type", default="auto",
                      choices=["auto", "domain", "ipv4", "ipv6", "email"],
                      help="seed type (default: auto-detect)")
    disc.add_argument("--max-depth", type=int, default=2, help="recursion depth (default 2)")
    disc.add_argument("--max-steps", type=int, default=30, help="max orchestrator runs (default 30)")
    disc.add_argument("--max-entities", type=int, default=1000, help="stop after N entities")
    disc.add_argument("--deadline", type=float, default=20.0, help="per-step deadline seconds")
    disc.add_argument("--parallel", type=int, default=4, help="max concurrent sources per step")
    disc.add_argument("--out-json", help="path to write the final surface JSON")
    _add_opsec_flags(disc)
    disc.set_defaults(func=lambda a: asyncio.run(cmd_discover(a)))

    sc = sub.add_parser(
        "scope",
        help="classify discovered assets against bug-bounty scope rules",
    )
    sc.add_argument("--assets", required=True,
                    help="discover --out-json surface, or a flat host/IP list")
    sc.add_argument("--scope", required=True,
                    help="rules file (wildcards/CIDR/regex; '## out-of-scope' divider supported)")
    sc.add_argument("--out", help="path to write the classification JSON")
    sc.add_argument("--flat-dir",
                    help="directory to write in_scope_hosts.txt / in_scope_ips.txt / unknown.txt")
    sc.set_defaults(func=cmd_scope)

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
