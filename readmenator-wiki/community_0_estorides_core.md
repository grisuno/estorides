# estorides_core

*Community 0 | 123 files | cohesion 1.00*

## Definition

This community groups 123 file(s) rooted at `estorides_core` with dominant language py (cohesion 1.00). Central symbols: `AlertDispatcher`, `AsyncClient`, `AuditEvent`, `AuditLog`, `AuthGate`, `BoundedJobRegistry`, `BufferedEventSink`, `CLUSTER_PALETTE`. Core file: `static/js/estorides.js` (161 symbols). Documented purpose: Deprecated entry point. Use:  - the `estorides` console script (installed by `pip install -e .`), or - `python3 estorides_cli.py serve` for the dev server, or -.

## Files

### `estorides_core` (50 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/__init__.py` | py | utility | 0 | yes |
| `estorides_core/active_recon.py` | py | utility | 25 | no |
| `estorides_core/alerter.py` | py | utility | 15 | yes |
| `estorides_core/async_client.py` | py | infrastructure | 21 | yes |

### `tests` (49 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_active_recon.py` | py | testing | 24 | yes |
| `tests/test_async_client.py` | py | testing | 15 | yes |
| `tests/test_audit_log.py` | py | testing | 5 | yes |
| `tests/test_auth_gate.py` | py | testing | 10 | yes |

### `tests/properties` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_change_detection_properties.py` | py | testing | 8 | yes |
| `tests/properties/test_csp_safe_styles_properties.py` | py | testing | 3 | yes |
| `tests/properties/test_hypothesis_engine_properties.py` | py | testing | 9 | yes |
| `tests/properties/test_observation_models_properties.py` | py | testing | 7 | yes |

### `.` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `app.py` | py | utility | 0 | yes |
| `estorides_cli.py` | py | utility | 31 | yes |
| `estorides_web.py` | py | presentation | 91 | yes |

### `estorides_export` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_export/__init__.py` | py | utility | 0 | yes |
| `estorides_export/encryption.py` | py | utility | 4 | yes |
| `estorides_export/misp.py` | py | utility | 3 | yes |

### `static/js` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/estorides.js` | js | utility | 161 | yes |

### `tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/sync_docs.py` | py | utility | 2 | yes |

*... and 103 more files in this community.*


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

- Internal resolved imports (EXTRACTED): 329
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: estorides_llm/manager.py imports estorides_core/config.py.
- [INFERRED] shares_context community 0 <-> 1 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (estorides_core) and community 1 (estorides_core).
- [INFERRED] shares_context community 0 <-> 2 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 0 (estorides_core) and community 2 (tests/properties).
- [INFERRED] shares_context community 0 <-> 4 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 0 (estorides_core) and community 4 (orphans).
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/__init__.py reaches tests/properties/test_change_detection_properties.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/__init__.py reaches tests/properties/test_hypothesis_engine_properties.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/__init__.py reaches tests/test_recon_report.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/intelligence_prompts.py reaches tests/properties/test_change_detection_properties.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/intelligence_prompts.py reaches tests/properties/test_hypothesis_engine_properties.py in 6 hops.

## Risks

- [taint medium] `estorides_core/alerter.py` -> `estorides_core/alerter.py` via `urllib.request` (0 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/alerter.py` via `urllib.request` (0 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/async_client.py` via `requests` (0 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/feeds.py` via `requests` (0 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)

## Open Questions

- Why do 4 file(s) lack file-level docs (e.g. `estorides_core/active_recon.py`)? What purpose do they serve?
- Can the cycle `estorides_web.py` -> `estorides_web_tools.py` be broken with an interface?
- Is the dangerous import `urllib.request` in `estorides_core/alerter.py` still required, or can it be isolated?
- What would break if the most connected file in estorides_core changed?
- Should estorides_core be split, given cohesion 1.00?

## Sources

- `app.py`
- `estorides_cli.py`
- `estorides_core/__init__.py`
- `estorides_core/active_recon.py`
- `estorides_core/alerter.py`
- `estorides_core/async_client.py`
- `estorides_core/audit.py`
- `estorides_core/case_crypto.py`
- `estorides_core/cases.py`
- `estorides_core/change_detection.py`
- `estorides_core/config.py`
- `estorides_core/discoverer.py`
- `estorides_core/entity_extraction.py`
- `estorides_core/entity_resolution.py`
- `estorides_core/entity_store.py`
- `estorides_core/event_bus.py`
- `estorides_core/feeds.py`
- `estorides_core/fusion_analytics.py`
- `estorides_core/fusion_store.py`
- `estorides_core/graph_kuzu.py`
- *... and 103 more*
