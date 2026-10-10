# estorides_core: estorides

*Community 4 | 18 files | cohesion 0.46*

## Definition

This community groups 18 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.46). Central symbols: `BoundedJobRegistry`, `CLUSTER_PALETTE`, `CaseStore`, `CidrRule`, `DictMixin`, `DiscoverJob`, `ExactHostRule`, `KuzuGraphBackend`. Core file: `static/js/estorides.js` (168 symbols). Documented purpose: estorides CLI.  Usage: estorides "example.com" estorides "8.8.8.8" --include-paid estorides "user@example.com" --only-sources shodan_internetdb,ipapi_free estor.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_cli.py` | py | utility | 31 | yes |
| `estorides_core/case_crypto.py` | py | utility | 4 | yes |
| `estorides_core/cases.py` | py | utility | 21 | yes |
| `estorides_core/discoverer.py` | py | utility | 21 | yes |
| `estorides_core/graph_kuzu.py` | py | utility | 11 | yes |
| `estorides_core/job_registry.py` | py | utility | 10 | yes |
| `estorides_core/monitoring.py` | py | utility | 26 | yes |
| `estorides_core/scope.py` | py | utility | 39 | yes |
| `estorides_core/sqlite_store.py` | py | data_access | 7 | yes |
| `estorides_export/report.py` | py | utility | 6 | yes |
| `static/js/estorides.js` | js | utility | 168 | yes |
| `tests/test_case_crypto.py` | py | testing | 5 | yes |
| `tests/test_cli_watch.py` | py | testing | 16 | yes |
| `tests/test_hardening.py` | py | testing | 17 | yes |
| `tests/test_job_registry.py` | py | testing | 8 | yes |
| `tests/test_obs_fts.py` | py | testing | 3 | yes |
| `tests/test_scope.py` | py | testing | 15 | yes |
| `tests/test_sqlite_store.py` | py | testing | 14 | yes |

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

- Internal resolved imports (EXTRACTED): 37
- Cross-boundary resolved imports (EXTRACTED): 35

## Connections

- [EXTRACTED] depends_on community 4 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 4 <-> 7 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/knowledge_graph.py.
- [EXTRACTED] depends_on community 4 <-> 0 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/orchestrator.py.
- [EXTRACTED] depends_on community 4 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/validation.py.
- [EXTRACTED] depends_on community 4 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/fusion_store.py.
- [EXTRACTED] depends_on community 4 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/entity_extraction.py.
- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_web.py.

## Risks

- [layer strict] `tests/test_hardening.py` (testing) -> `estorides_core/web_security.py` (presentation)

## Open Questions

- What would break if the most connected file in estorides_core: estorides changed?
- Should estorides_core: estorides be split, given cohesion 0.46?

## Sources

- `estorides_cli.py`
- `estorides_core/case_crypto.py`
- `estorides_core/cases.py`
- `estorides_core/discoverer.py`
- `estorides_core/graph_kuzu.py`
- `estorides_core/job_registry.py`
- `estorides_core/monitoring.py`
- `estorides_core/scope.py`
- `estorides_core/sqlite_store.py`
- `estorides_export/report.py`
- `static/js/estorides.js`
- `tests/test_case_crypto.py`
- `tests/test_cli_watch.py`
- `tests/test_hardening.py`
- `tests/test_job_registry.py`
- `tests/test_obs_fts.py`
- `tests/test_scope.py`
- `tests/test_sqlite_store.py`
