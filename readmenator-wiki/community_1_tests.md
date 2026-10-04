# tests

*Community 1 | 56 files | cohesion 0.66*

## Definition

This community groups 56 file(s) rooted at `tests` with dominant language py (cohesion 0.66). Central symbols: `AlertDispatcher`, `AuditEvent`, `AuditLog`, `AuthGate`, `BoundedJobRegistry`, `BufferedEventSink`, `CLUSTER_PALETTE`, `CaseStore`. Core file: `static/js/estorides.js` (165 symbols). Documented purpose: estorides CLI.  Usage: estorides "example.com" estorides "8.8.8.8" --include-paid estorides "user@example.com" --only-sources shodan_internetdb,ipapi_free estor.

## Files

### `tests` (23 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_audit_log.py` | py | testing | 5 | yes |
| `tests/test_auth_gate.py` | py | testing | 10 | yes |
| `tests/test_case_crypto.py` | py | testing | 5 | yes |
| `tests/test_cli_watch.py` | py | testing | 16 | yes |
| `tests/test_csp_safe_styles.py` | py | testing | 11 | yes |

### `estorides_core` (21 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/__init__.py` | py | utility | 0 | yes |
| `estorides_core/alerter.py` | py | utility | 15 | yes |
| `estorides_core/audit.py` | py | infrastructure | 11 | yes |
| `estorides_core/case_crypto.py` | py | utility | 4 | yes |
| `estorides_core/cases.py` | py | utility | 21 | yes |

### `estorides_export` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_export/__init__.py` | py | utility | 0 | yes |
| `estorides_export/encryption.py` | py | utility | 4 | yes |
| `estorides_export/misp.py` | py | utility | 3 | yes |
| `estorides_export/recon_report.py` | py | utility | 11 | no |

### `.` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_cli.py` | py | utility | 31 | yes |
| `estorides_web.py` | py | presentation | 94 | yes |
| `estorides_web_tools.py` | py | presentation | 5 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/estorides.js` | js | utility | 165 | yes |

### `tests/properties` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_csp_safe_styles_properties.py` | py | testing | 3 | yes |

### `tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/sync_docs.py` | py | utility | 2 | yes |

*... and 36 more files in this community.*


## Key Symbols

- `_setup_logging` (function, `estorides_cli.py:39`) `def _setup_logging(verbose)`
- `_collect_selectors` (function, `estorides_cli.py:46`) `def _collect_selectors(events, types)` - Group discovered entity values by type for the requested type set.
- `_resolve_proxy` (function, `estorides_cli.py:62`) `def _resolve_proxy(args)` - Resolve the egress proxy from the OPSEC flags.
- `_add_opsec_flags` (function, `estorides_cli.py:75`) `def _add_opsec_flags(parser)` - Attach the shared operator-OPSEC flags to a subcommand parser.
- `cmd_discover` (function, `estorides_cli.py:93`) `def cmd_discover(args)` - v1.2 — fanout the surface from a seed.
- `cmd_run` (function, `estorides_cli.py:205`) `def cmd_run(args)`
- `_on_done` (function, `estorides_cli.py:222`) `def _on_done(source_name, ok, status, elapsed_ms)`
- `cmd_scope` (function, `estorides_cli.py:282`) `def cmd_scope(args)` - Classify discovered assets against a program's scope rules.
- `cmd_graph_export` (function, `estorides_cli.py:328`) `def cmd_graph_export(args)`
- `cmd_export_stix` (function, `estorides_cli.py:351`) `def cmd_export_stix(args)`
- `cmd_export_misp` (function, `estorides_cli.py:361`) `def cmd_export_misp(args)`
- `cmd_report` (function, `estorides_cli.py:371`) `def cmd_report(args)` - Render a Markdown report for a case.
- `cmd_diff` (function, `estorides_cli.py:412`) `def cmd_diff(args)` - Diff two cases. CLI twin of /api/cases/diff.
- `cmd_status` (function, `estorides_cli.py:440`) `def cmd_status(_)`
- `cmd_fusion` (function, `estorides_cli.py:447`) `def cmd_fusion(args)` - Query the cross-run fusion datastore.
- `cmd_watch_add` (function, `estorides_cli.py:490`) `def cmd_watch_add(args)` - Add a new recurring watch target.
- `_watch_runner_factory` (function, `estorides_cli.py:532`) `def _watch_runner_factory(proxy, passive_only)` - Create an async watch runner wired to the Orchestrator.
- `_run` (function, `estorides_cli.py:540`) `def _run(watch)`
- `cmd_watch_list` (function, `estorides_cli.py:554`) `def cmd_watch_list(args)` - List all watch targets.
- `cmd_watch_remove` (function, `estorides_cli.py:574`) `def cmd_watch_remove(args)` - Delete a watch target.
- `cmd_watch_enable` (function, `estorides_cli.py:586`) `def cmd_watch_enable(args)`
- `cmd_watch_disable` (function, `estorides_cli.py:599`) `def cmd_watch_disable(args)`
- `cmd_watch_history` (function, `estorides_cli.py:611`) `def cmd_watch_history(args)`
- `cmd_alerts_test` (function, `estorides_cli.py:632`) `def cmd_alerts_test(args)`
- `cmd_alerts_channels` (function, `estorides_cli.py:644`) `def cmd_alerts_channels(args)`
- `cmd_scheduler_start` (function, `estorides_cli.py:656`) `def cmd_scheduler_start(args)`
- `cmd_scheduler_stop` (function, `estorides_cli.py:666`) `def cmd_scheduler_stop(args)`
- `cmd_scheduler_status` (function, `estorides_cli.py:676`) `def cmd_scheduler_status(args)`
- `cmd_serve` (function, `estorides_cli.py:684`) `def cmd_serve(args)`
- `build_parser` (function, `estorides_cli.py:701`) `def build_parser()`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 128
- Cross-boundary resolved imports (EXTRACTED): 53

## Connections

- [EXTRACTED] depends_on community 1 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/alerter.py imports estorides_core/ssrf_guard.py.
- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/fusion_store.py imports estorides_core/ids.py.
- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_web_tools.py imports estorides_core/tool_install.py.
- [EXTRACTED] depends_on community 0 <-> 1 (strength 0.9): Extracted import edge crosses communities: wsgi.py imports estorides_web.py.
- [INFERRED] shares_context community 1 <-> 2 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 1 (tests) and community 2 (estorides_core).
- [INFERRED] shares_context community 1 <-> 5 (strength 0.5): Inferred shared context (language py) with no import path between community 1 (tests) and community 5 (estorides_core).
- [INFERRED] shares_context community 1 <-> 7 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 1 (tests) and community 7 (tests/properties).
- [INFERRED] shares_context community 1 <-> 9 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 1 (tests) and community 9 (orphans).

## Risks

- [taint medium] `estorides_core/alerter.py` -> `estorides_core/alerter.py` via `urllib.request` (0 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/alerter.py` via `urllib.request` (0 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [cycle] `estorides_web.py` -> `estorides_web_tools.py` -> `estorides_web.py`
- [layer strict] `estorides_web.py` (presentation) -> `estorides_core/fusion_store.py` (data_access)

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `estorides_export/recon_report.py`)? What purpose do they serve?
- Can the cycle `estorides_web.py` -> `estorides_web_tools.py` be broken with an interface?
- Is the dangerous import `urllib.request` in `estorides_core/alerter.py` still required, or can it be isolated?
- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 0.66?

## Sources

- `estorides_cli.py`
- `estorides_core/__init__.py`
- `estorides_core/alerter.py`
- `estorides_core/audit.py`
- `estorides_core/case_crypto.py`
- `estorides_core/cases.py`
- `estorides_core/discoverer.py`
- `estorides_core/entity_extraction.py`
- `estorides_core/feeds.py`
- `estorides_core/fusion_analytics.py`
- `estorides_core/fusion_store.py`
- `estorides_core/graph_kuzu.py`
- `estorides_core/job_registry.py`
- `estorides_core/knowledge_graph.py`
- `estorides_core/monitoring.py`
- `estorides_core/openapi.py`
- `estorides_core/pivot_engine.py`
- `estorides_core/scope.py`
- `estorides_core/socmint.py`
- `estorides_core/sqlite_store.py`
- *... and 36 more*
