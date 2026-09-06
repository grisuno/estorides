# API

## _test_entity_resolution.py

### check `def check(name, cond, detail)`
- Defined: `_test_entity_resolution.py:27`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### _ent `def _ent(etype, value, source)`
- Defined: `_test_entity_resolution.py:36`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### _by_value `def _by_value(result, value)`
- Defined: `_test_entity_resolution.py:40`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_transliteration `def test_transliteration()`
- Defined: `_test_entity_resolution.py:47`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_jaro_winkler `def test_jaro_winkler()`
- Defined: `_test_entity_resolution.py:63`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_normalization `def test_normalization()`
- Defined: `_test_entity_resolution.py:74`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_score_pair_policy `def test_score_pair_policy()`
- Defined: `_test_entity_resolution.py:98`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_resolution_merge `def test_resolution_merge()`
- Defined: `_test_entity_resolution.py:111`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_to_entity_roundtrip `def test_to_entity_roundtrip()`
- Defined: `_test_entity_resolution.py:167`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_cross_run_stability `def test_cross_run_stability()`
- Defined: `_test_entity_resolution.py:182`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_empty_and_edge_inputs `def test_empty_and_edge_inputs()`
- Defined: `_test_entity_resolution.py:211`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### main `def main()`
- Defined: `_test_entity_resolution.py:219`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

## _test_fusion.py

### check `def check(label, cond)`
- Defined: `_test_fusion.py:24`
- Depends on: `estorides_core/fusion_store.py`

### _fresh_store `def _fresh_store()`
- Defined: `_test_fusion.py:32`
- Depends on: `estorides_core/fusion_store.py`

### test_deterministic_identity `def test_deterministic_identity()`
- Defined: `_test_fusion.py:37`
- Depends on: `estorides_core/fusion_store.py`

### test_cross_run_dedup_and_provenance `def test_cross_run_dedup_and_provenance()`
- Defined: `_test_fusion.py:45`
- Depends on: `estorides_core/fusion_store.py`

### test_property_corroboration_and_conflict `def test_property_corroboration_and_conflict()`
- Defined: `_test_fusion.py:59`
- Depends on: `estorides_core/fusion_store.py`

### test_min_sources_filter `def test_min_sources_filter()`
- Defined: `_test_fusion.py:76`
- Depends on: `estorides_core/fusion_store.py`

### test_relationship_fusion `def test_relationship_fusion()`
- Defined: `_test_fusion.py:87`
- Depends on: `estorides_core/fusion_store.py`

### test_observation_and_source_counters `def test_observation_and_source_counters()`
- Defined: `_test_fusion.py:97`
- Depends on: `estorides_core/fusion_store.py`

### test_fail_soft_open `def test_fail_soft_open()`
- Defined: `_test_fusion.py:116`
- Depends on: `estorides_core/fusion_store.py`

### main `def main()`
- Defined: `_test_fusion.py:124`
- Depends on: `estorides_core/fusion_store.py`

## _test_hardening.py

### _ok `def _ok(name, ok, detail)`
- Defined: `_test_hardening.py:25`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_security_headers `def test_security_headers()`
- Defined: `_test_hardening.py:36`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_cors_default_off `def test_cors_default_off()`
- Defined: `_test_hardening.py:53`
- Doc: Without ESTORIDES_CORS_ORIGINS, CORS headers must not be emitted.
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_cors_allowlist `def test_cors_allowlist()`
- Defined: `_test_hardening.py:62`
- Doc: With an allowlist, only matching origins get a CORS header.
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_debug_killswitch `def test_debug_killswitch()`
- Defined: `_test_hardening.py:87`
- Doc: When DEBUG is on, install_security must refuse to run.
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_max_body_rejection `def test_max_body_rejection()`
- Defined: `_test_hardening.py:101`
- Doc: A request body larger than MAX_CONTENT_LENGTH must be rejected.
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_case_diff `def test_case_diff()`
- Defined: `_test_hardening.py:113`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_case_diff_endpoints `def test_case_diff_endpoints()`
- Defined: `_test_hardening.py:137`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_case_save_endpoint `def test_case_save_endpoint()`
- Defined: `_test_hardening.py:148`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_report_renders `def test_report_renders()`
- Defined: `_test_hardening.py:165`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_report_with_diff `def test_report_with_diff()`
- Defined: `_test_hardening.py:181`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### test_console_script_help `def test_console_script_help()`
- Defined: `_test_hardening.py:196`
- Doc: `./estorides` must run even without `pip install -e .`.
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

### main `def main()`
- Defined: `_test_hardening.py:210`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

## _test_passive.py

### check `def check(name, cond, detail)`
- Defined: `_test_passive.py:20`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`

### main `def main()`
- Defined: `_test_passive.py:29`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`

## _test_people.py

### check `def check(name, cond, detail)`
- Defined: `_test_people.py:21`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/pivot_engine.py`

### _types `def _types(payload)`
- Defined: `_test_people.py:30`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/pivot_engine.py`

### main `def main()`
- Defined: `_test_people.py:37`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/pivot_engine.py`

### run `def run(self, query)`
- Defined: `_test_people.py:67`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/pivot_engine.py`

## _test_proxy.py

### check `def check(name, cond, detail)`
- Defined: `_test_proxy.py:21`
- Depends on: `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/config.py`

### main `def main()`
- Defined: `_test_proxy.py:30`
- Depends on: `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/config.py`

### _enter_and_rotate `def _enter_and_rotate()`
- Defined: `_test_proxy.py:52`
- Depends on: `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/config.py`

### _enter_socks `def _enter_socks()`
- Defined: `_test_proxy.py:72`
- Depends on: `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/config.py`

## _test_scope.py

### check `def check(name, cond, detail)`
- Defined: `_test_scope.py:18`
- Depends on: `estorides_core/scope.py`

### main `def main()`
- Defined: `_test_scope.py:27`
- Depends on: `estorides_core/scope.py`

## _validate.py

### main `def main()`
- Defined: `_validate.py:17`

## estorides_cli.py

### _setup_logging `def _setup_logging(verbose)`
- Defined: `estorides_cli.py:36`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### _collect_selectors `def _collect_selectors(events, types)`
- Defined: `estorides_cli.py:43`
- Doc: Group discovered entity values by type for the requested type set.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### _resolve_proxy `def _resolve_proxy(args)`
- Defined: `estorides_cli.py:59`
- Doc: Resolve the egress proxy from the OPSEC flags.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### _add_opsec_flags `def _add_opsec_flags(parser)`
- Defined: `estorides_cli.py:72`
- Doc: Attach the shared operator-OPSEC flags to a subcommand parser.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_discover `def cmd_discover(args)`
- Defined: `estorides_cli.py:90`
- Doc: v1.2 — fanout the surface from a seed.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_run `def cmd_run(args)`
- Defined: `estorides_cli.py:202`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_scope `def cmd_scope(args)`
- Defined: `estorides_cli.py:279`
- Doc: Classify discovered assets against a program's scope rules.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_graph_export `def cmd_graph_export(args)`
- Defined: `estorides_cli.py:326`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_export_stix `def cmd_export_stix(args)`
- Defined: `estorides_cli.py:349`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_export_misp `def cmd_export_misp(args)`
- Defined: `estorides_cli.py:359`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_report `def cmd_report(args)`
- Defined: `estorides_cli.py:369`
- Doc: Render a Markdown report for a case.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_diff `def cmd_diff(args)`
- Defined: `estorides_cli.py:410`
- Doc: Diff two cases. CLI twin of /api/cases/diff.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_status `def cmd_status(_)`
- Defined: `estorides_cli.py:438`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_fusion `def cmd_fusion(args)`
- Defined: `estorides_cli.py:445`
- Doc: Query the cross-run fusion datastore.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_watch_add `def cmd_watch_add(args)`
- Defined: `estorides_cli.py:488`
- Doc: Add a new recurring watch target.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### _watch_runner_factory `def _watch_runner_factory(proxy, passive_only)`
- Defined: `estorides_cli.py:523`
- Doc: Create an async watch runner wired to the Orchestrator.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_watch_list `def cmd_watch_list(args)`
- Defined: `estorides_cli.py:545`
- Doc: List all watch targets.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_watch_remove `def cmd_watch_remove(args)`
- Defined: `estorides_cli.py:565`
- Doc: Delete a watch target.
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_watch_enable `def cmd_watch_enable(args)`
- Defined: `estorides_cli.py:577`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_watch_disable `def cmd_watch_disable(args)`
- Defined: `estorides_cli.py:590`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_watch_history `def cmd_watch_history(args)`
- Defined: `estorides_cli.py:602`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_alerts_test `def cmd_alerts_test(args)`
- Defined: `estorides_cli.py:623`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_alerts_channels `def cmd_alerts_channels(args)`
- Defined: `estorides_cli.py:635`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_scheduler_start `def cmd_scheduler_start(args)`
- Defined: `estorides_cli.py:647`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_scheduler_stop `def cmd_scheduler_stop(args)`
- Defined: `estorides_cli.py:657`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_scheduler_status `def cmd_scheduler_status(args)`
- Defined: `estorides_cli.py:667`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### cmd_serve `def cmd_serve(args)`
- Defined: `estorides_cli.py:675`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### build_parser `def build_parser()`
- Defined: `estorides_cli.py:692`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### main `def main(argv)`
- Defined: `estorides_cli.py:847`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### _on_done `def _on_done(source_name, ok, status, elapsed_ms)`
- Defined: `estorides_cli.py:219`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

### _run `def _run(watch)`
- Defined: `estorides_cli.py:531`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

## estorides_core/active_recon.py

### _parse_nmap_stdout `def _parse_nmap_stdout(stdout, tool_name)`
- Defined: `estorides_core/active_recon.py:102`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### _parse_nikto_stdout `def _parse_nikto_stdout(stdout, tool_name)`
- Defined: `estorides_core/active_recon.py:125`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### _parse_sqlmap_stdout `def _parse_sqlmap_stdout(stdout, tool_name)`
- Defined: `estorides_core/active_recon.py:144`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### _parse_dnsrecon_stdout `def _parse_dnsrecon_stdout(stdout, tool_name)`
- Defined: `estorides_core/active_recon.py:171`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### _parse_harvester_stdout `def _parse_harvester_stdout(stdout, tool_name)`
- Defined: `estorides_core/active_recon.py:188`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### run_nmap `def run_nmap(target, args)`
- Defined: `estorides_core/active_recon.py:213`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### run_nikto `def run_nikto(target, args)`
- Defined: `estorides_core/active_recon.py:243`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### run_sqlmap `def run_sqlmap(target, args)`
- Defined: `estorides_core/active_recon.py:269`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### run_dnsrecon `def run_dnsrecon(target, args)`
- Defined: `estorides_core/active_recon.py:295`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### run_theHarvester `def run_theHarvester(target, args)`
- Defined: `estorides_core/active_recon.py:325`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/active_recon.py:24`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_entities `def to_entities(self)`
- Defined: `estorides_core/active_recon.py:27`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/active_recon.py:41`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_entities `def to_entities(self)`
- Defined: `estorides_core/active_recon.py:44`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/active_recon.py:58`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_entities `def to_entities(self)`
- Defined: `estorides_core/active_recon.py:61`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/active_recon.py:77`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_entities `def to_entities(self)`
- Defined: `estorides_core/active_recon.py:80`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/active_recon.py:95`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

### to_entities `def to_entities(self)`
- Defined: `estorides_core/active_recon.py:98`
- Depends on: `estorides_core/tool_runner.py`
- Imported by: `tests/test_active_recon.py`

## estorides_core/alerter.py

### _check_cooldown `def _check_cooldown(channel)`
- Defined: `estorides_core/alerter.py:42`
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### _http_post `def _http_post(url, payload)`
- Defined: `estorides_core/alerter.py:53`
- Doc: POST JSON payload to URL, return True on success.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### _send_slack `def _send_slack(webhook_url, title, body, severity)`
- Defined: `estorides_core/alerter.py:84`
- Doc: Send a Slack message via Incoming Webhook.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### _send_discord `def _send_discord(webhook_url, title, body, severity)`
- Defined: `estorides_core/alerter.py:99`
- Doc: Send a Discord embed via Webhook.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### _send_telegram `def _send_telegram(bot_token, chat_id, title, body, severity)`
- Defined: `estorides_core/alerter.py:114`
- Doc: Send a Telegram message via Bot API.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### _send_email `def _send_email(smtp_host, smtp_port, smtp_user, smtp_pass, from_addr, to_addr, title, body, severity)`
- Defined: `estorides_core/alerter.py:129`
- Doc: Send an email alert via SMTP.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### _send_webhook `def _send_webhook(webhook_url, title, body, severity)`
- Defined: `estorides_core/alerter.py:150`
- Doc: Send a generic webhook POST.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### _fmt_time `def _fmt_time(ts)`
- Defined: `estorides_core/alerter.py:284`
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### send `def send(self, channel, title, body, severity)`
- Defined: `estorides_core/alerter.py:174`
- Doc: Send an alert to a single channel. Returns True on success.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### send_watch_alert `def send_watch_alert(self, watch, entity_count, obs_count, new_entities)`
- Defined: `estorides_core/alerter.py:230`
- Doc: Send alerts for a completed watch run to all configured channels.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### test `def test(self, channel)`
- Defined: `estorides_core/alerter.py:250`
- Doc: Send a test alert to verify channel configuration.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

### available_channels `def available_channels(self)`
- Defined: `estorides_core/alerter.py:260`
- Doc: Return list of configured channels with their status.
- Depends on: `estorides_core/ssrf_guard.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`, `tests/test_security_remediation.py`

## estorides_core/async_client.py

### _is_socks `def _is_socks(proxy)`
- Defined: `estorides_core/async_client.py:41`
- Doc: True when the proxy URL is a SOCKS proxy (e.g. Tor).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### _redact_proxy `def _redact_proxy(proxy)`
- Defined: `estorides_core/async_client.py:46`
- Doc: Strip any `user:pass@` credentials from a proxy URL before logging.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### sync_fetch `def sync_fetch(method, url)`
- Defined: `estorides_core/async_client.py:375`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### allow `def allow(self, host)`
- Defined: `estorides_core/async_client.py:61`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### record_success `def record_success(self, host)`
- Defined: `estorides_core/async_client.py:67`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### record_failure `def record_failure(self, host)`
- Defined: `estorides_core/async_client.py:71`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### __init__ `def __init__(self, path)`
- Defined: `estorides_core/async_client.py:87`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### _init_db `def _init_db(self)`
- Defined: `estorides_core/async_client.py:100`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### _key `def _key(method, url, body)`
- Defined: `estorides_core/async_client.py:113`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### get `def get(self, method, url, body)`
- Defined: `estorides_core/async_client.py:122`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### set `def set(self, method, url, body, value)`
- Defined: `estorides_core/async_client.py:138`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/async_client.py:152`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### __aenter__ `def __aenter__(self)`
- Defined: `estorides_core/async_client.py:181`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### _next_http_proxy `def _next_http_proxy(self)`
- Defined: `estorides_core/async_client.py:225`
- Doc: Round-robin the next HTTP proxy, or None (SOCKS/connector or direct).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### __aexit__ `def __aexit__(self)`
- Defined: `estorides_core/async_client.py:233`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### session `def session(self)`
- Defined: `estorides_core/async_client.py:239`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

### fetch `def fetch(self, method, url)`
- Defined: `estorides_core/async_client.py:245`
- Doc: Fetch a URL. Returns (parsed_data, meta).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `_test_proxy.py`, `estorides_core/orchestrator.py`

## estorides_core/audit.py

### to_jsonl `def to_jsonl(self)`
- Defined: `estorides_core/audit.py:68`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

### __init__ `def __init__(self, path)`
- Defined: `estorides_core/audit.py:90`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

### record `def record(self, event)`
- Defined: `estorides_core/audit.py:104`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

### _maybe_rotate_locked `def _maybe_rotate_locked(self)`
- Defined: `estorides_core/audit.py:115`
- Doc: If the active file is over the cap, rotate in place.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

### query `def query(self, event)`
- Defined: `estorides_core/audit.py:150`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/audit.py:201`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

### allow `def allow(self, key)`
- Defined: `estorides_core/audit.py:214`
- Doc: Return (allowed, retry_after_seconds).
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

### reset `def reset(self, key)`
- Defined: `estorides_core/audit.py:238`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/test_audit_log.py`

## estorides_core/cases.py

### __init__ `def __init__(self, path)`
- Defined: `estorides_core/cases.py:121`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### _init_schema `def _init_schema(self)`
- Defined: `estorides_core/cases.py:135`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### _tx `def _tx(self)`
- Defined: `estorides_core/cases.py:141`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### create_case `def create_case(self, query, query_type, notes)`
- Defined: `estorides_core/cases.py:152`
- Doc: Open a new case and return its id (8-char slug).
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### add_observation `def add_observation(self, case_id, observation)`
- Defined: `estorides_core/cases.py:168`
- Doc: Persist a single observation row.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### add_entities `def add_entities(self, case_id, entities)`
- Defined: `estorides_core/cases.py:202`
- Doc: Persist the merged entity list. Duplicate (type, value) rows
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### finalise `def finalise(self, case_id, analysis, kg_path, mitre, source_count, obs_count, entity_count, status)`
- Defined: `estorides_core/cases.py:225`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### delete_case `def delete_case(self, case_id)`
- Defined: `estorides_core/cases.py:255`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### get_case `def get_case(self, case_id)`
- Defined: `estorides_core/cases.py:260`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### list_observations `def list_observations(self, case_id)`
- Defined: `estorides_core/cases.py:273`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### list_entities `def list_entities(self, case_id)`
- Defined: `estorides_core/cases.py:296`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### diff_entities `def diff_entities(self, case_a, case_b)`
- Defined: `estorides_core/cases.py:311`
- Doc: Compare two cases by entity (type, value) keys.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### search_cases `def search_cases(self, query_substring, limit, query_type)`
- Defined: `estorides_core/cases.py:358`
- Doc: Lightweight case search. LIKE on `query` (not indexed, but
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### search_by_entity `def search_by_entity(self, ent_type, value, limit)`
- Defined: `estorides_core/cases.py:388`
- Doc: Find every case that observed a given entity.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### stats `def stats(self)`
- Defined: `estorides_core/cases.py:416`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### _row_to_case `def _row_to_case(self, row)`
- Defined: `estorides_core/cases.py:424`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### _safe_json `def _safe_json(text)`
- Defined: `estorides_core/cases.py:442`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### close `def close(self)`
- Defined: `estorides_core/cases.py:450`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### _per_type `def _per_type(pairs)`
- Defined: `estorides_core/cases.py:332`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

### _serialise `def _serialise(pairs)`
- Defined: `estorides_core/cases.py:338`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`

## estorides_core/change_detection.py

### _truncate_key `def _truncate_key(key)`
- Defined: `estorides_core/change_detection.py:176`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _change_id `def _change_id(kind, entity_id, diff_signature)`
- Defined: `estorides_core/change_detection.py:183`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _reliability_weight `def _reliability_weight(name)`
- Defined: `estorides_core/change_detection.py:188`
- Doc: Reliability weight via 2a, with 0 fallback for the impossible
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _reliability_floor `def _reliability_floor(letter)`
- Defined: `estorides_core/change_detection.py:205`
- Doc: A=1, B=2, ..., F=6. For 'min_reliability' comparison.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _filter_sources_by_reliability `def _filter_sources_by_reliability(sources, min_reliability)`
- Defined: `estorides_core/change_detection.py:210`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _property_diff `def _property_diff(before, after)`
- Defined: `estorides_core/change_detection.py:223`
- Doc: Compute the per-key add/change/remove between two property maps.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _edge_set `def _edge_set(edges)`
- Defined: `estorides_core/change_detection.py:242`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _union_sources `def _union_sources(a, b)`
- Defined: `estorides_core/change_detection.py:246`
- Doc: Sorted union of two entities' source lists.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _make_change `def _make_change(kind, entity_id, entity_type, entity_value, sig)`
- Defined: `estorides_core/change_detection.py:258`
- Doc: Build a :class:`Change` with the deterministic id derived from
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### _below_min_reliability `def _below_min_reliability(source, min_reliability)`
- Defined: `estorides_core/change_detection.py:291`
- Doc: True if a source's reliability is strictly *worse* than the
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### detect_changes `def detect_changes(snapshot_before, snapshot_after)`
- Defined: `estorides_core/change_detection.py:301`
- Doc: Diff two snapshots. Pure: no I/O, deterministic, bounded.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/change_detection.py:84`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/change_detection.py:115`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_change_detection_properties.py`, `tests/test_change_detection.py`

## estorides_core/cloud_asset_discovery.py

### generate_bucket_names `def generate_bucket_names(domain)`
- Defined: `estorides_core/cloud_asset_discovery.py:65`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_cloud_asset_discovery.py`, `tests/test_cloud_asset_discovery.py`

### assess_bucket `def assess_bucket(url, method)`
- Defined: `estorides_core/cloud_asset_discovery.py:84`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_cloud_asset_discovery.py`, `tests/test_cloud_asset_discovery.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/cloud_asset_discovery.py:45`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_cloud_asset_discovery.py`, `tests/test_cloud_asset_discovery.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/cloud_asset_discovery.py:56`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_cloud_asset_discovery.py`, `tests/test_cloud_asset_discovery.py`

## estorides_core/code_exposure.py

### validate_aws_key `def validate_aws_key(key)`
- Defined: `estorides_core/code_exposure.py:91`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`

### _is_placeholder `def _is_placeholder(text)`
- Defined: `estorides_core/code_exposure.py:95`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`

### classify_finding `def classify_finding(content, source, file_path)`
- Defined: `estorides_core/code_exposure.py:99`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`

### analyse_findings `def analyse_findings(findings, rate_limited)`
- Defined: `estorides_core/code_exposure.py:189`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/code_exposure.py:57`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/code_exposure.py:69`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/code_exposure.py:81`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_code_exposure.py`

## estorides_core/config.py

### _env_int `def _env_int(name, default)`
- Defined: `estorides_core/config.py:32`
- Doc: Read an int env var, falling back to `default` on absence/parse error.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _env_float `def _env_float(name, default)`
- Defined: `estorides_core/config.py:44`
- Doc: Read a float env var, falling back to `default` on absence/parse error.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _env_bool `def _env_bool(name, default)`
- Defined: `estorides_core/config.py:56`
- Doc: Read a boolean env var. Truthy tokens: 1/true/yes/on (case-insensitive).
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### ensure_data_dirs `def ensure_data_dirs()`
- Defined: `estorides_core/config.py:86`
- Doc: Idempotently create DATA_DIR.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### ensure_reports_dir `def ensure_reports_dir()`
- Defined: `estorides_core/config.py:97`
- Doc: Idempotently create REPORTS_DIR.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _env_tool_allowlist `def _env_tool_allowlist()`
- Defined: `estorides_core/config.py:151`
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### contact_level `def contact_level(contact)`
- Defined: `estorides_core/config.py:224`
- Doc: Map a contact class to its numeric severity, unknown values to active.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### effective_proxies `def effective_proxies(explicit)`
- Defined: `estorides_core/config.py:250`
- Doc: Resolve the proxy rotation pool from an explicit value or the env.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _pivot_weight_map `def _pivot_weight_map()`
- Defined: `estorides_core/config.py:543`
- Doc: Default per-type lead weights for the pivot scorer.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _csv_frozenset `def _csv_frozenset(name, default)`
- Defined: `estorides_core/config.py:560`
- Doc: Read a comma-separated env var into a frozenset, else the default.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### is_active `def is_active(self)`
- Defined: `estorides_core/config.py:382`
- Doc: Cache is only consulted when enabled and the TTL is positive.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### is_pivotable `def is_pivotable(self, entity_type)`
- Defined: `estorides_core/config.py:402`
- Doc: True when an entity of `entity_type` should be re-queried.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### lead_score `def lead_score(self, entity_type, depth, parent_score)`
- Defined: `estorides_core/config.py:406`
- Doc: Priority of expanding this lead. Higher expands sooner.
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### clamp_depth `def clamp_depth(self, value)`
- Defined: `estorides_core/config.py:436`
- Doc: Clamp a requested depth into [1, max_depth_cap].
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### clamp_steps `def clamp_steps(self, value)`
- Defined: `estorides_core/config.py:440`
- Doc: Clamp a requested step budget into [1, max_steps_cap].
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### clamp_entities `def clamp_entities(self, value)`
- Defined: `estorides_core/config.py:444`
- Doc: Clamp a requested entity budget into [1, max_entities_cap].
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### clamp_parallel `def clamp_parallel(self, value)`
- Defined: `estorides_core/config.py:448`
- Doc: Clamp a requested fan-out width into [1, parallel_cap].
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### clamp_deadline `def clamp_deadline(self, value)`
- Defined: `estorides_core/config.py:452`
- Doc: Clamp a requested per-target deadline into (0, deadline_cap_seconds].
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/config.py:491`
- Imported by: `_test_passive.py`, `_test_people.py`, `_test_proxy.py`, `estorides_cli.py`, `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/feeds.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/observation_models.py`, `estorides_core/ontology.py`, `estorides_core/orchestrator.py`, `estorides_core/osiris_sources.py`, `estorides_core/pivot_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `estorides_core/tool_runner.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_llm/manager.py`, `estorides_web.py`, `tests/test_monitoring.py`, `tests/test_recon_fusion.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

## estorides_core/discoverer.py

### _new_job_id `def _new_job_id()`
- Defined: `estorides_core/discoverer.py:189`
- Doc: Monotonic-ish id with a timestamp prefix for natural sort.
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### create_discover_job `def create_discover_job(seed_type, seed_value)`
- Defined: `estorides_core/discoverer.py:194`
- Doc: Create and register a discovery job synchronously.
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### start_discover `def start_discover(seed_type, seed_value)`
- Defined: `estorides_core/discoverer.py:252`
- Doc: Create a discovery job and schedule its worker on the current loop.
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### start_discover_threadsafe `def start_discover_threadsafe(loop, seed_type, seed_value)`
- Defined: `estorides_core/discoverer.py:285`
- Doc: Create the job in the calling thread, fire its worker on `loop`.
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _run_discoverer `def _run_discoverer(job)`
- Defined: `estorides_core/discoverer.py:319`
- Doc: The background loop. One asyncio task per job, driving the engine.
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### list_jobs `def list_jobs(limit)`
- Defined: `estorides_core/discoverer.py:349`
- Doc: Snapshot of the recent jobs for the /api/discover/jobs endpoint.
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### stop `def stop(self)`
- Defined: `estorides_core/discoverer.py:78`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### should_stop `def should_stop(self)`
- Defined: `estorides_core/discoverer.py:81`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### push_event `def push_event(self, ev)`
- Defined: `estorides_core/discoverer.py:84`
- Doc: Append an event and keep the buffer bounded.
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### __init__ `def __init__(self, job)`
- Defined: `estorides_core/discoverer.py:103`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### emit `def emit(self, event)`
- Defined: `estorides_core/discoverer.py:106`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_started `def _on_started(self, data)`
- Defined: `estorides_core/discoverer.py:113`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_target_start `def _on_target_start(self, data)`
- Defined: `estorides_core/discoverer.py:116`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_entity `def _on_entity(self, data)`
- Defined: `estorides_core/discoverer.py:126`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_target_done `def _on_target_done(self, data)`
- Defined: `estorides_core/discoverer.py:141`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_target_error `def _on_target_error(self, data)`
- Defined: `estorides_core/discoverer.py:153`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_stopping `def _on_stopping(self, data)`
- Defined: `estorides_core/discoverer.py:160`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_finished `def _on_finished(self, data)`
- Defined: `estorides_core/discoverer.py:163`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

### _on_fatal `def _on_fatal(self, data)`
- Defined: `estorides_core/discoverer.py:174`
- Depends on: `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/graph_kuzu.py`, `estorides_core/job_registry.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `static/js/estorides.js`

## estorides_core/entity_extraction.py

### detect_query_type `def detect_query_type(query)`
- Defined: `estorides_core/entity_extraction.py:63`
- Doc: Return the detected type of a free-form query.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _is_valid_domain `def _is_valid_domain(candidate)`
- Defined: `estorides_core/entity_extraction.py:84`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _context `def _context(text, start, end, window)`
- Defined: `estorides_core/entity_extraction.py:97`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### extract_from_text `def extract_from_text(text, source)`
- Defined: `estorides_core/entity_extraction.py:103`
- Doc: Find every recognised entity in a raw text blob.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _ip_in_textual_context `def _ip_in_textual_context(text, idx)`
- Defined: `estorides_core/entity_extraction.py:155`
- Doc: Heuristic: only count a numeric match as an IP if it isn't part of a
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### extract_from_json `def extract_from_json(payload, source)`
- Defined: `estorides_core/entity_extraction.py:165`
- Doc: Pull entities out of a JSON-like structure.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _clean_scalar `def _clean_scalar(value)`
- Defined: `estorides_core/entity_extraction.py:233`
- Doc: Return a stripped string for a scalar leaf, or None for non-scalars.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _looks_like_person `def _looks_like_person(value)`
- Defined: `estorides_core/entity_extraction.py:243`
- Doc: True when a value reads like a human name (has a space, mostly letters).
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _looks_like_username `def _looks_like_username(value)`
- Defined: `estorides_core/entity_extraction.py:254`
- Doc: True when a value reads like a handle (no spaces, handle charset).
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _classify_keyed_value `def _classify_keyed_value(key, value)`
- Defined: `estorides_core/entity_extraction.py:261`
- Doc: Map a (key, scalar value) pair to a human-selector entity type, or None.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### extract_structured `def extract_structured(payload, source)`
- Defined: `estorides_core/entity_extraction.py:285`
- Doc: Extract human selectors (email, username, person, org, phone) by key.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### merge `def merge()`
- Defined: `estorides_core/entity_extraction.py:337`
- Doc: Deduplicate by (type, value) and merge sources / contexts.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### _fuzzy_cluster `def _fuzzy_cluster(entities)`
- Defined: `estorides_core/entity_extraction.py:431`
- Doc: Group entities of the same type by string similarity and merge.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/entity_extraction.py:34`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### visit `def visit(node, key)`
- Defined: `estorides_core/entity_extraction.py:299`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### find `def find(x)`
- Defined: `estorides_core/entity_extraction.py:452`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### union `def union(a, b)`
- Defined: `estorides_core/entity_extraction.py:458`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

### norm `def norm(v)`
- Defined: `estorides_core/entity_extraction.py:463`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_entity_resolution.py`, `_test_people.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/entity_resolution.py`, `estorides_core/knowledge_graph.py`, `estorides_core/orchestrator.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_entity_resolution.py`, `tests/test_socmint.py`

## estorides_core/entity_resolution.py

### jaro `def jaro(s1, s2)`
- Defined: `estorides_core/entity_resolution.py:83`
- Doc: Return the Jaro similarity of two strings in ``[0, 1]``.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### jaro_winkler `def jaro_winkler(s1, s2, prefix_weight)`
- Defined: `estorides_core/entity_resolution.py:126`
- Doc: Jaro-Winkler similarity: Jaro with a shared-prefix bonus.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _soundex `def _soundex(token)`
- Defined: `estorides_core/entity_resolution.py:146`
- Doc: Return a 4-character Soundex code for a Latin token.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _normalize_domain `def _normalize_domain(value)`
- Defined: `estorides_core/entity_resolution.py:178`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _normalize_name `def _normalize_name(value)`
- Defined: `estorides_core/entity_resolution.py:187`
- Doc: Order-independent transliterated key for persons and orgs.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### normalize_value `def normalize_value(etype, value)`
- Defined: `estorides_core/entity_resolution.py:206`
- Doc: Return the canonical normalised form of an entity value.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### canonical_id `def canonical_id(etype, normalized)`
- Defined: `estorides_core/entity_resolution.py:246`
- Doc: Stable, content-addressed id for a normalised entity.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### blocking_keys `def blocking_keys(etype, normalized, value)`
- Defined: `estorides_core/entity_resolution.py:258`
- Doc: Return the blocking keys that bucket an entity for comparison.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### score_pair `def score_pair(etype, a_value, b_value, a_norm, b_norm)`
- Defined: `estorides_core/entity_resolution.py:303`
- Doc: Score how likely two same-type entities denote the same object.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _script_of `def _script_of(value)`
- Defined: `estorides_core/entity_resolution.py:451`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### resolve_entities `def resolve_entities(entities)`
- Defined: `estorides_core/entity_resolution.py:728`
- Doc: Module-level convenience wrapper around :class:`EntityResolver`.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/entity_resolution.py:358`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### to_entity `def to_entity(self)`
- Defined: `estorides_core/entity_resolution.py:374`
- Doc: Project back onto the legacy :class:`Entity` shape.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/entity_resolution.py:410`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/entity_resolution.py:426`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### __init__ `def __init__(self, n)`
- Defined: `estorides_core/entity_resolution.py:436`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### find `def find(self, x)`
- Defined: `estorides_core/entity_resolution.py:439`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### union `def union(self, a, b)`
- Defined: `estorides_core/entity_resolution.py:445`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/entity_resolution.py:470`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### resolve `def resolve(self, entities)`
- Defined: `estorides_core/entity_resolution.py:483`
- Doc: Resolve ``entities`` into canonical identities and links.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _build_records `def _build_records(self, entities)`
- Defined: `estorides_core/entity_resolution.py:499`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _exact_merge `def _exact_merge(records, uf)`
- Defined: `estorides_core/entity_resolution.py:514`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _fuzzy_merge `def _fuzzy_merge(self, records, uf)`
- Defined: `estorides_core/entity_resolution.py:526`
- Doc: Block, score, merge at threshold, and collect link candidates.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _build_links `def _build_links(candidates, uf, root_to_cid)`
- Defined: `estorides_core/entity_resolution.py:567`
- Doc: Translate index-pair link candidates into canonical-id links.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _materialise `def _materialise(self, records, uf)`
- Defined: `estorides_core/entity_resolution.py:595`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _representative `def _representative(members)`
- Defined: `estorides_core/entity_resolution.py:662`
- Doc: Pick a stable representative for a cluster.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _best_internal_match `def _best_internal_match(members)`
- Defined: `estorides_core/entity_resolution.py:680`
- Doc: Return the (method, score) of the strongest non-exact pair.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _reconcile_with_store `def _reconcile_with_store(self, canonicals)`
- Defined: `estorides_core/entity_resolution.py:706`
- Doc: Map canonicals onto persisted ids and record their aliases.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### rank `def rank(rec)`
- Defined: `estorides_core/entity_resolution.py:671`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/transliteration.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

## estorides_core/entity_store.py

### open_store `def open_store(path)`
- Defined: `estorides_core/entity_store.py:184`
- Doc: Open the store, returning None instead of raising on failure.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### __init__ `def __init__(self, path)`
- Defined: `estorides_core/entity_store.py:65`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _init_schema `def _init_schema(self)`
- Defined: `estorides_core/entity_store.py:75`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### _tx `def _tx(self)`
- Defined: `estorides_core/entity_store.py:81`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### lookup `def lookup(self, etype, normalized, aliases)`
- Defined: `estorides_core/entity_store.py:91`
- Doc: Return an existing canonical id for any known form, or None.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### upsert `def upsert(self, entity)`
- Defined: `estorides_core/entity_store.py:129`
- Doc: Persist (insert or update) a canonical entity and its aliases.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### stats `def stats(self)`
- Defined: `estorides_core/entity_store.py:168`
- Doc: Return a one-glance summary of store size.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

### close `def close(self)`
- Defined: `estorides_core/entity_store.py:179`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`
- Imported by: `_test_entity_resolution.py`, `estorides_core/orchestrator.py`, `tests/test_entity_resolution.py`

## estorides_core/feeds.py

### list_feeds `def list_feeds()`
- Defined: `estorides_core/feeds.py:313`
- Doc: Return public feed descriptions for the /api/feeds endpoint.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### get_feed `def get_feed(name)`
- Defined: `estorides_core/feeds.py:321`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### fetch_all `def fetch_all(bbox, use_cache)`
- Defined: `estorides_core/feeds.py:325`
- Doc: Fetch every registered feed (optionally clipped to a bbox).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/feeds.py:69`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/feeds.py:82`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### _fetch `def _fetch(self)`
- Defined: `estorides_core/feeds.py:87`
- Doc: Subclass implementation: hit the upstream and return points.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### fetch `def fetch(self)`
- Defined: `estorides_core/feeds.py:90`
- Doc: Public entrypoint. Reads/writes the on-disk cache.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### point `def point(self, record)`
- Defined: `estorides_core/feeds.py:135`
- Doc: Default: return (lat, lon) if both present.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### _fetch `def _fetch(self)`
- Defined: `estorides_core/feeds.py:156`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### _fetch `def _fetch(self)`
- Defined: `estorides_core/feeds.py:209`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

### _fetch `def _fetch(self)`
- Defined: `estorides_core/feeds.py:271`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_web.py`

## estorides_core/fusion_analytics.py

### __init__ `def __init__(self, store)`
- Defined: `estorides_core/fusion_analytics.py:40`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### entity_timeline `def entity_timeline(self, eid)`
- Defined: `estorides_core/fusion_analytics.py:46`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### entity_summary `def entity_summary(self, eid)`
- Defined: `estorides_core/fusion_analytics.py:132`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### source_stats `def source_stats(self, source_name)`
- Defined: `estorides_core/fusion_analytics.py:213`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### multi_source_consensus `def multi_source_consensus(self, eid, key)`
- Defined: `estorides_core/fusion_analytics.py:290`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### corroborated_properties `def corroborated_properties(self, eid, min_sources)`
- Defined: `estorides_core/fusion_analytics.py:343`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### entity_search `def entity_search(self, term, etype)`
- Defined: `estorides_core/fusion_analytics.py:374`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### top_changed `def top_changed(self, days, limit)`
- Defined: `estorides_core/fusion_analytics.py:432`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### source_corroboration_matrix `def source_corroboration_matrix(self, limit)`
- Defined: `estorides_core/fusion_analytics.py:477`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### _resolve_entity_value `def _resolve_entity_value(self, eid)`
- Defined: `estorides_core/fusion_analytics.py:509`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### _resolve_entity_type `def _resolve_entity_type(self, eid)`
- Defined: `estorides_core/fusion_analytics.py:520`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### _intel_level `def _intel_level(source_count, sources)`
- Defined: `estorides_core/fusion_analytics.py:532`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

### _deduplicate_relationships `def _deduplicate_relationships(rels)`
- Defined: `estorides_core/fusion_analytics.py:540`
- Imported by: `estorides_web.py`, `tests/test_fusion_analytics.py`

## estorides_core/fusion_store.py

### entity_id `def entity_id(etype, value, normalized)`
- Defined: `estorides_core/fusion_store.py:178`
- Doc: Deterministic, run-independent id for an entity.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### open_store `def open_store(path)`
- Defined: `estorides_core/fusion_store.py:753`
- Doc: Open the fusion store, returning None instead of raising on failure.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### __init__ `def __init__(self, path)`
- Defined: `estorides_core/fusion_store.py:199`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### _init_schema `def _init_schema(self)`
- Defined: `estorides_core/fusion_store.py:210`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### _tx `def _tx(self)`
- Defined: `estorides_core/fusion_store.py:216`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### _ensure_entity_stub `def _ensure_entity_stub(conn, etype, value)`
- Defined: `estorides_core/fusion_store.py:227`
- Doc: Insert a minimal entity row if absent and return its id.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### register_sources `def register_sources(self, sources)`
- Defined: `estorides_core/fusion_store.py:247`
- Doc: Mirror the YAML source catalogue into the store.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### add_observation `def add_observation(self, observation)`
- Defined: `estorides_core/fusion_store.py:284`
- Doc: Fuse a single source response into the cross-run observation log
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### fuse_entity `def fuse_entity(self, entity)`
- Defined: `estorides_core/fusion_store.py:325`
- Doc: Fuse one entity into the canonical store and return its id.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### fuse_entities `def fuse_entities(self, entities)`
- Defined: `estorides_core/fusion_store.py:428`
- Doc: Fuse a batch of entities, returning the list of fused ids.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### fuse_properties `def fuse_properties(self, eid, parsed, source)`
- Defined: `estorides_core/fusion_store.py:441`
- Doc: Fuse the flat scalar attributes of a parsed observation onto an
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### fuse_relationship `def fuse_relationship(self, src_type, src_value, relation, dst_type, dst_value)`
- Defined: `estorides_core/fusion_store.py:487`
- Doc: Fuse one directed edge between two entities, attributed to source.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### fuse_graph `def fuse_graph(self, kg)`
- Defined: `estorides_core/fusion_store.py:557`
- Doc: Mirror the analytic edges of a knowledge graph into the store.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### get_entity `def get_entity(self, eid)`
- Defined: `estorides_core/fusion_store.py:593`
- Doc: Return one fused entity with its provenance, properties and edges.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### search_entities `def search_entities(self, term, etype)`
- Defined: `estorides_core/fusion_store.py:639`
- Doc: Search fused entities by value substring and/or type.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### corroborated_properties `def corroborated_properties(self, eid, min_sources)`
- Defined: `estorides_core/fusion_store.py:682`
- Doc: Return an entity's properties that at least ``min_sources`` distinct
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### list_sources `def list_sources(self, limit)`
- Defined: `estorides_core/fusion_store.py:699`
- Doc: Return the source catalogue with accumulated fetch/ok counters.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### stats `def stats(self)`
- Defined: `estorides_core/fusion_store.py:717`
- Doc: One-glance dashboard of the fused store's size.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### close `def close(self)`
- Defined: `estorides_core/fusion_store.py:745`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### normalize_value `def normalize_value(etype, value)`
- Defined: `estorides_core/fusion_store.py:74`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

### _count `def _count(table)`
- Defined: `estorides_core/fusion_store.py:720`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_resolution.py`, `estorides_core/reliability_scoring.py`
- Imported by: `_test_fusion.py`, `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `tests/test_fusion_analytics.py`, `tests/test_probabilistic_fusion.py`, `tests/test_probabilistic_fusion.py`

## estorides_core/graph_kuzu.py

### _label_for `def _label_for(ent_type)`
- Defined: `estorides_core/graph_kuzu.py:124`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### _node_id `def _node_id(type_, value)`
- Defined: `estorides_core/graph_kuzu.py:133`
- Doc: Canonical id used as PRIMARY KEY in Kuzu.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### __init__ `def __init__(self, path)`
- Defined: `estorides_core/graph_kuzu.py:205`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### _init_schema `def _init_schema(self)`
- Defined: `estorides_core/graph_kuzu.py:233`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### upsert_entity `def upsert_entity(self, ent_type, value, source)`
- Defined: `estorides_core/graph_kuzu.py:245`
- Doc: Insert (or merge) an entity. Returns its canonical node id.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### upsert_relationship `def upsert_relationship(self, src_type, src_value, rel, dst_type, dst_value)`
- Defined: `estorides_core/graph_kuzu.py:295`
- Doc: Insert an edge between two entities.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### neighbors `def neighbors(self, node_id, hops, relation, limit)`
- Defined: `estorides_core/graph_kuzu.py:346`
- Doc: Return nodes reachable from `node_id` within `hops` edges.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### cypher `def cypher(self, query, params)`
- Defined: `estorides_core/graph_kuzu.py:379`
- Doc: Run a Cypher query and return rows as a list of dicts.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### stats `def stats(self)`
- Defined: `estorides_core/graph_kuzu.py:406`
- Doc: Return counts of every node label and edge rel type.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

### close `def close(self)`
- Defined: `estorides_core/graph_kuzu.py:436`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_core/discoverer.py`, `estorides_core/orchestrator.py`, `estorides_web.py`, `estorides_web.py`

## estorides_core/hypothesis_engine.py

### _truncate `def _truncate(value)`
- Defined: `estorides_core/hypothesis_engine.py:110`
- Doc: Stringify a value, bounded to ``_VALUE_MAX_CHARS``.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _is_mapping `def _is_mapping(value)`
- Defined: `estorides_core/hypothesis_engine.py:120`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _entity_lookup `def _entity_lookup(entities)`
- Defined: `estorides_core/hypothesis_engine.py:124`
- Doc: Build ``{type: {value, value, ...}}`` from the entity list.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _hypothesis_id `def _hypothesis_id(htype, entity_refs, supporting)`
- Defined: `estorides_core/hypothesis_engine.py:145`
- Doc: Deterministic 16-char hex id for a hypothesis.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _score `def _score(supporting, contradicting)`
- Defined: `estorides_core/hypothesis_engine.py:163`
- Doc: Net-support score in (0, 1].
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _confidence `def _confidence(supporting, contradicting)`
- Defined: `estorides_core/hypothesis_engine.py:177`
- Doc: Reliability-weighted confidence via :mod:`reliability_scoring`.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _clip_claim `def _clip_claim(template)`
- Defined: `estorides_core/hypothesis_engine.py:198`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _domain_belongsto_actor `def _domain_belongsto_actor(observations, entities)`
- Defined: `estorides_core/hypothesis_engine.py:217`
- Doc: `domain-belongsto-actor`: a domain's WHOIS/issuer/hosting org matches an entity.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _domains_in_obs `def _domains_in_obs(obs)`
- Defined: `estorides_core/hypothesis_engine.py:309`
- Doc: Best-effort: extract domain-like values from a single observation.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _email_aliases_person `def _email_aliases_person(observations, entities)`
- Defined: `estorides_core/hypothesis_engine.py:342`
- Doc: `email-aliasto-person`: an email and a person name appear together in one obs.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _extract_email `def _extract_email(parsed)`
- Defined: `estorides_core/hypothesis_engine.py:402`
- Doc: Find a value that looks like an email anywhere in the parsed dict.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _extract_person_name `def _extract_person_name(parsed)`
- Defined: `estorides_core/hypothesis_engine.py:413`
- Doc: Find a value that looks like a person name (has a space, no @, no path).
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _ip_shared_infra `def _ip_shared_infra(observations, entities)`
- Defined: `estorides_core/hypothesis_engine.py:424`
- Doc: `ip-shared-infra`: >=2 domains resolve to the same IP.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _extract_ips `def _extract_ips(parsed)`
- Defined: `estorides_core/hypothesis_engine.py:505`
- Doc: Best-effort: pull IPv4-looking values out of a parsed payload.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _looks_like_ipv4 `def _looks_like_ipv4(s)`
- Defined: `estorides_core/hypothesis_engine.py:520`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _asn_shared_infra `def _asn_shared_infra(observations, entities)`
- Defined: `estorides_core/hypothesis_engine.py:533`
- Doc: `asn-shared-infra`: >=3 entities of the run live in the same ASN.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### _extract_asn `def _extract_asn(parsed)`
- Defined: `estorides_core/hypothesis_engine.py:597`
- Doc: Best-effort: pull an AS-number-ish value out of the parsed payload.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### generate_hypotheses `def generate_hypotheses(observations, entities, kg)`
- Defined: `estorides_core/hypothesis_engine.py:622`
- Doc: Generate typed, scored, auditable hypotheses for a run.
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

### __call__ `def __call__(self, observations, entities)`
- Defined: `estorides_core/hypothesis_engine.py:210`
- Depends on: `estorides_core/reliability_scoring.py`
- Imported by: `tests/properties/test_hypothesis_engine_properties.py`, `tests/test_hypothesis_engine.py`

## estorides_core/intel_resolver.py

### _run_sparql `def _run_sparql(query)`
- Defined: `estorides_core/intel_resolver.py:90`
- Doc: Execute a SPARQL SELECT against the Wikidata endpoint.
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _val `def _val(row, key)`
- Defined: `estorides_core/intel_resolver.py:111`
- Doc: Pull a string value out of a SPARQL JSON row.
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _norm `def _norm(s)`
- Defined: `estorides_core/intel_resolver.py:789`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _is_valid_ipv4 `def _is_valid_ipv4(s)`
- Defined: `estorides_core/intel_resolver.py:793`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _escape_sparql `def _escape_sparql(s)`
- Defined: `estorides_core/intel_resolver.py:801`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/intel_resolver.py:121`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### get `def get(self, kind, key)`
- Defined: `estorides_core/intel_resolver.py:127`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### put `def put(self, kind, key, value)`
- Defined: `estorides_core/intel_resolver.py:140`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### stats `def stats(self)`
- Defined: `estorides_core/intel_resolver.py:148`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/intel_resolver.py:165`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### resolve `def resolve(self, ent_type, ent_id)`
- Defined: `estorides_core/intel_resolver.py:174`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _vt_get `def _vt_get(self, path, limit)`
- Defined: `estorides_core/intel_resolver.py:214`
- Doc: GET a VirusTotal v3 path, returning parsed JSON or None.
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _vt_add_relationship `def _vt_add_relationship(self, path)`
- Defined: `estorides_core/intel_resolver.py:245`
- Doc: Expand one VirusTotal relationship endpoint into nodes/links.
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _vt_flag_malicious `def _vt_flag_malicious(self, path, node, sources)`
- Defined: `estorides_core/intel_resolver.py:290`
- Doc: Stamp a node with VirusTotal detection stats (counter-intel signal).
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_ip `def _resolve_ip(self, ip)`
- Defined: `estorides_core/intel_resolver.py:306`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_domain `def _resolve_domain(self, domain)`
- Defined: `estorides_core/intel_resolver.py:412`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_file `def _resolve_file(self, file_hash)`
- Defined: `estorides_core/intel_resolver.py:473`
- Doc: Resolve a file hash via VirusTotal relationships.
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_company `def _resolve_company(self, name)`
- Defined: `estorides_core/intel_resolver.py:510`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_person `def _resolve_person(self, name)`
- Defined: `estorides_core/intel_resolver.py:569`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_country `def _resolve_country(self, name)`
- Defined: `estorides_core/intel_resolver.py:638`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_cve `def _resolve_cve(self, cve_id)`
- Defined: `estorides_core/intel_resolver.py:678`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_btc `def _resolve_btc(self, addr)`
- Defined: `estorides_core/intel_resolver.py:750`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_eth `def _resolve_eth(self, addr)`
- Defined: `estorides_core/intel_resolver.py:753`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

### _resolve_crypto `def _resolve_crypto(self, addr, kind)`
- Defined: `estorides_core/intel_resolver.py:756`
- Depends on: `estorides_core/config.py`, `estorides_core/ontology.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/transforms.py`, `estorides_web.py`

## estorides_core/job_registry.py

### __init__ `def __init__(self)`
- Defined: `estorides_core/job_registry.py:49`
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### register `def register(self, key, value)`
- Defined: `estorides_core/job_registry.py:60`
- Doc: Insert (or replace) a job, evicting expired and overflow entries.
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### get `def get(self, key)`
- Defined: `estorides_core/job_registry.py:80`
- Doc: Return the value for `key` or None. Refreshes the LRU order.
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### pop `def pop(self, key)`
- Defined: `estorides_core/job_registry.py:95`
- Doc: Remove and return the value for `key`, or None.
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### keys `def keys(self)`
- Defined: `estorides_core/job_registry.py:101`
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### values `def values(self)`
- Defined: `estorides_core/job_registry.py:105`
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### __len__ `def __len__(self)`
- Defined: `estorides_core/job_registry.py:109`
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### evict_expired `def evict_expired(self)`
- Defined: `estorides_core/job_registry.py:113`
- Doc: Sweep and drop TTL-expired entries. Returns the number dropped.
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

### _evict_expired_locked `def _evict_expired_locked(self, now)`
- Defined: `estorides_core/job_registry.py:119`
- Imported by: `estorides_core/discoverer.py`, `estorides_web.py`, `tests/test_job_registry.py`

## estorides_core/knowledge_graph.py

### _node_sources `def _node_sources(node)`
- Defined: `estorides_core/knowledge_graph.py:73`
- Doc: Read the distinct source set off a node, tolerating GraphML's
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### __init__ `def __init__(self, name)`
- Defined: `estorides_core/knowledge_graph.py:91`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### add_entity `def add_entity(self, entity)`
- Defined: `estorides_core/knowledge_graph.py:97`
- Doc: Insert an entity. Returns the node id used.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### add_observation `def add_observation(self, source, entities)`
- Defined: `estorides_core/knowledge_graph.py:127`
- Doc: Add every entity + every co-occurrence edge within the same response.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### add_relationship `def add_relationship(self, src_type, src_value, rel, dst_type, dst_value)`
- Defined: `estorides_core/knowledge_graph.py:142`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### export_graphml `def export_graphml(self, path)`
- Defined: `estorides_core/knowledge_graph.py:164`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### export_json `def export_json(self)`
- Defined: `estorides_core/knowledge_graph.py:183`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### summary `def summary(self)`
- Defined: `estorides_core/knowledge_graph.py:197`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### top_entities `def top_entities(self, n, by)`
- Defined: `estorides_core/knowledge_graph.py:215`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### communities `def communities(self, nodes)`
- Defined: `estorides_core/knowledge_graph.py:235`
- Doc: Partition entity nodes into communities (clusters).
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### intel_level `def intel_level(self, node_id, bridge_nodes)`
- Defined: `estorides_core/knowledge_graph.py:266`
- Doc: Classify a node into the intelligence pipeline tier.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### ego_subgraph `def ego_subgraph(self, node_id, radius)`
- Defined: `estorides_core/knowledge_graph.py:311`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### neighbours `def neighbours(self, node_id, relation)`
- Defined: `estorides_core/knowledge_graph.py:322`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### _node_id `def _node_id(self, kind, value)`
- Defined: `estorides_core/knowledge_graph.py:338`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### _source_node `def _source_node(self, source)`
- Defined: `estorides_core/knowledge_graph.py:341`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

### _node_color `def _node_color(self, ent_type)`
- Defined: `estorides_core/knowledge_graph.py:351`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_core/orchestrator.py`, `estorides_export/encryption.py`, `estorides_export/misp.py`, `estorides_export/stix.py`, `estorides_web.py`, `tests/test_encrypted_export.py`

## estorides_core/mitre_attack.py

### _scan_keywords `def _scan_keywords(text)`
- Defined: `estorides_core/mitre_attack.py:156`
- Doc: Scan a text blob for ATT&CK-relevant keywords.
- Imported by: `estorides_core/orchestrator.py`

### map_observation `def map_observation(observation)`
- Defined: `estorides_core/mitre_attack.py:170`
- Doc: Return ATT&CK techniques associated with an observation.
- Imported by: `estorides_core/orchestrator.py`

### map_observations `def map_observations(observations)`
- Defined: `estorides_core/mitre_attack.py:213`
- Doc: Bulk mapper. Stamps each observation in place with `_mitre` key.
- Imported by: `estorides_core/orchestrator.py`

### all_techniques_for `def all_techniques_for(observations)`
- Defined: `estorides_core/mitre_attack.py:229`
- Doc: Aggregate: unique techniques across all observations, sorted by id.
- Imported by: `estorides_core/orchestrator.py`

## estorides_core/monitoring.py

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/monitoring.py:106`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/monitoring.py:110`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### from_dict `def from_dict(cls, d)`
- Defined: `estorides_core/monitoring.py:126`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### from_row `def from_row(cls, row)`
- Defined: `estorides_core/monitoring.py:142`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### __init__ `def __init__(self, path)`
- Defined: `estorides_core/monitoring.py:158`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### _init_schema `def _init_schema(self)`
- Defined: `estorides_core/monitoring.py:169`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### _tx `def _tx(self)`
- Defined: `estorides_core/monitoring.py:175`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### create_watch `def create_watch(self, watch)`
- Defined: `estorides_core/monitoring.py:185`
- Doc: Persist a new watch target.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### get_watch `def get_watch(self, watch_id)`
- Defined: `estorides_core/monitoring.py:200`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### update_watch `def update_watch(self, watch)`
- Defined: `estorides_core/monitoring.py:209`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### delete_watch `def delete_watch(self, watch_id)`
- Defined: `estorides_core/monitoring.py:222`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### list_watches `def list_watches(self, enabled_only)`
- Defined: `estorides_core/monitoring.py:226`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### due_watches `def due_watches(self, now)`
- Defined: `estorides_core/monitoring.py:236`
- Doc: Return enabled watches whose next_run_at <= now.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### record_run_start `def record_run_start(self, watch_id)`
- Defined: `estorides_core/monitoring.py:249`
- Doc: Record a watch run start, return history entry id.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### record_run_complete `def record_run_complete(self, history_id, status, entity_count, obs_count, error, alert_sent)`
- Defined: `estorides_core/monitoring.py:259`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### history `def history(self, watch_id, limit)`
- Defined: `estorides_core/monitoring.py:272`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### stats `def stats(self)`
- Defined: `estorides_core/monitoring.py:289`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### close `def close(self)`
- Defined: `estorides_core/monitoring.py:299`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### __init__ `def __init__(self, store, runner, alerter)`
- Defined: `estorides_core/monitoring.py:316`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### running `def running(self)`
- Defined: `estorides_core/monitoring.py:329`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### start `def start(self)`
- Defined: `estorides_core/monitoring.py:332`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### stop `def stop(self)`
- Defined: `estorides_core/monitoring.py:343`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### set_runner `def set_runner(self, runner)`
- Defined: `estorides_core/monitoring.py:349`
- Doc: Set the orchestrator runner function (sync or async).
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### set_alerter `def set_alerter(self, alerter)`
- Defined: `estorides_core/monitoring.py:353`
- Doc: Set the alert dispatcher.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### _loop `def _loop(self)`
- Defined: `estorides_core/monitoring.py:357`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

### _execute_watch `def _execute_watch(self, watch)`
- Defined: `estorides_core/monitoring.py:368`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_monitoring.py`

## estorides_core/observation_models.py

### _check_json_safe `def _check_json_safe(value)`
- Defined: `estorides_core/observation_models.py:44`
- Doc: Return ``value`` if it is JSON-safe (None/bool/int/float/str/list/dict).
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### _bound_url `def _bound_url(cls, value)`
- Defined: `estorides_core/observation_models.py:87`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### _upper_method `def _upper_method(cls, value)`
- Defined: `estorides_core/observation_models.py:92`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### to_legacy_dict `def to_legacy_dict(self)`
- Defined: `estorides_core/observation_models.py:95`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### _json_safe `def _json_safe(cls, value)`
- Defined: `estorides_core/observation_models.py:125`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### to_legacy_dict `def to_legacy_dict(self)`
- Defined: `estorides_core/observation_models.py:128`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### _json_safe `def _json_safe(cls, value)`
- Defined: `estorides_core/observation_models.py:160`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### to_legacy_dict `def to_legacy_dict(self)`
- Defined: `estorides_core/observation_models.py:163`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

### to_legacy_dict `def to_legacy_dict(self)`
- Defined: `estorides_core/observation_models.py:183`
- Depends on: `estorides_core/config.py`
- Imported by: `tests/properties/test_observation_models_properties.py`, `tests/test_observation_models.py`

## estorides_core/ontology.py

### _normalise_name `def _normalise_name(s)`
- Defined: `estorides_core/ontology.py:84`
- Doc: Lower-case, strip punctuation/diacritics, collapse whitespace.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/ontology.py:79`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/ontology.py:115`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### is_ready `def is_ready(self)`
- Defined: `estorides_core/ontology.py:131`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### entries `def entries(self)`
- Defined: `estorides_core/ontology.py:134`
- Doc: Return the current snapshot, loading if necessary.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### lookup `def lookup(self, name)`
- Defined: `estorides_core/ontology.py:141`
- Doc: Find sanction entries whose name or alias matches `name`.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### lookup_crypto `def lookup_crypto(self, address)`
- Defined: `estorides_core/ontology.py:151`
- Doc: Cross-check a BTC/ETH address against the SDN list.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### size `def size(self)`
- Defined: `estorides_core/ontology.py:168`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### _refresh `def _refresh(self)`
- Defined: `estorides_core/ontology.py:172`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### _download `def _download(self)`
- Defined: `estorides_core/ontology.py:201`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### _persist `def _persist(self, text)`
- Defined: `estorides_core/ontology.py:213`
- Doc: Best-effort write of the raw CSV for offline re-use.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### _parse `def _parse(self, text)`
- Defined: `estorides_core/ontology.py:226`
- Doc: Parse the OpenSanctions simple CSV into SanctionEntry records.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### _index `def _index(self, entries)`
- Defined: `estorides_core/ontology.py:255`
- Doc: Build a normalised-name → entries lookup.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/ontology.py:276`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### get `def get(self, kind, value)`
- Defined: `estorides_core/ontology.py:282`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### put `def put(self, kind, value, payload)`
- Defined: `estorides_core/ontology.py:296`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### stats `def stats(self)`
- Defined: `estorides_core/ontology.py:304`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### clear `def clear(self)`
- Defined: `estorides_core/ontology.py:308`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/ontology.py:317`
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### check_observation `def check_observation(self, observation)`
- Defined: `estorides_core/ontology.py:321`
- Doc: Run a single observation through the ontology.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

### _candidate_fields `def _candidate_fields(source, parsed)`
- Defined: `estorides_core/ontology.py:359`
- Doc: Return (field_name, value) pairs to check against sanctions.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`
- Imported by: `estorides_core/intel_resolver.py`, `estorides_core/orchestrator.py`

## estorides_core/orchestrator.py

### pending_system_app_tasks `def pending_system_app_tasks()`
- Defined: `estorides_core/orchestrator.py:52`
- Doc: Number of slow CLI-tool runs still in flight (for the stream gate).
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _safe_format `def _safe_format(template)`
- Defined: `estorides_core/orchestrator.py:111`
- Doc: Format a string template with {key} placeholders.
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _resolve_auth `def _resolve_auth(source)`
- Defined: `estorides_core/orchestrator.py:123`
- Doc: Look up the API key for a source that needs one.
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _domain_from_query `def _domain_from_query(q)`
- Defined: `estorides_core/orchestrator.py:133`
- Doc: Heuristic: if the query looks like a domain, return it; if it's an IP, return None.
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### repl `def repl(m)`
- Defined: `estorides_core/orchestrator.py:118`
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/orchestrator.py:144`
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### run `def run(self, query)`
- Defined: `estorides_core/orchestrator.py:159`
- Doc: Run a full intelligence cycle. Returns a structured result.
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _select_sources `def _select_sources(self, names)`
- Defined: `estorides_core/orchestrator.py:649`
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _execute_source `def _execute_source(self, client, source, query, on_done, on_result)`
- Defined: `estorides_core/orchestrator.py:682`
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _extract_cursor `def _extract_cursor(data, cfg)`
- Defined: `estorides_core/orchestrator.py:843`
- Doc: Extract the next-page cursor from a parsed response body.
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _infer_relationships `def _infer_relationships(self, observations, query)`
- Defined: `estorides_core/orchestrator.py:848`
- Doc: Delegate each observation to its registered inferer.
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _write_dataset `def _write_dataset(self, query, observations, entities, analysis)`
- Defined: `estorides_core/orchestrator.py:861`
- Depends on: `estorides_core/async_client.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/knowledge_graph.py`, `estorides_core/mitre_attack.py`, `estorides_core/ontology.py`, `estorides_core/pagination.py`, `estorides_core/parsers.py`, `estorides_core/recon_fusion.py`, `estorides_core/relationship_inference.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`
- Imported by: `_test_passive.py`, `estorides_cli.py`, `estorides_cli.py`, `estorides_core/discoverer.py`, `estorides_core/discoverer.py`, `estorides_web.py`, `estorides_web.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

## estorides_core/osiris_sources.py

### _cached_get `def _cached_get(url)`
- Defined: `estorides_core/osiris_sources.py:81`
- Doc: GET with a small on-disk JSON cache. Returns parsed JSON or None.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

### fetch_bgp `def fetch_bgp(query)`
- Defined: `estorides_core/osiris_sources.py:119`
- Doc: Look up an IP or AS number against bgpview.io (free, no key).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

### fetch_mac `def fetch_mac(mac)`
- Defined: `estorides_core/osiris_sources.py:185`
- Doc: Look up a MAC address against macvendors.co (free, no key).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

### fetch_phone `def fetch_phone(number)`
- Defined: `estorides_core/osiris_sources.py:233`
- Doc: Best-effort phone geolocation.
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

### fetch_github_user `def fetch_github_user(username)`
- Defined: `estorides_core/osiris_sources.py:302`
- Doc: Look up a GitHub user (keyless, rate-limited).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

### fetch_leaks `def fetch_leaks(email)`
- Defined: `estorides_core/osiris_sources.py:356`
- Doc: Breach analytics for `email` via xposedornot (free, no key).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

### fetch_cisa_kev `def fetch_cisa_kev(limit, days)`
- Defined: `estorides_core/osiris_sources.py:400`
- Doc: Recently-added CVEs from the CISA KEV feed (authoritative).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

### fetch_malware_c2 `def fetch_malware_c2(limit)`
- Defined: `estorides_core/osiris_sources.py:452`
- Doc: Active botnet C2 (Feodo) + recent malware URLs (URLhaus).
- Depends on: `estorides_core/config.py`, `estorides_core/ssrf_guard.py`

## estorides_core/pagination.py

### build_page_params `def build_page_params(cfg, page_num)`
- Defined: `estorides_core/pagination.py:62`
- Doc: Build URL params dict for a given page number.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/test_pagination.py`

### extract_cursor `def extract_cursor(data, cfg)`
- Defined: `estorides_core/pagination.py:78`
- Doc: Extract the next-page cursor from a parsed response body.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/test_pagination.py`

### count_results `def count_results(data, cfg)`
- Defined: `estorides_core/pagination.py:99`
- Doc: Count results in a parsed response page.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/test_pagination.py`

### from_dict `def from_dict(raw)`
- Defined: `estorides_core/pagination.py:38`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/test_pagination.py`

### enabled `def enabled(self)`
- Defined: `estorides_core/pagination.py:54`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/test_pagination.py`

### needs_page_size `def needs_page_size(self)`
- Defined: `estorides_core/pagination.py:58`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/test_pagination.py`

## estorides_core/parsers.py

### _flat `def _flat(obj)`
- Defined: `estorides_core/parsers.py:31`
- Doc: Recursively flatten a dict/list into a list of leaf values.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### _first `def _first(obj)`
- Defined: `estorides_core/parsers.py:45`
- Doc: Recursively dig into a JSON-ish structure to find the first matching key.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_dns_json `def parse_dns_json(payload)`
- Defined: `estorides_core/parsers.py:63`
- Doc: Google/Cloudflare DNS-over-HTTPS response.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_crtsh_json `def parse_crtsh_json(payload)`
- Defined: `estorides_core/parsers.py:78`
- Doc: crt.sh CT log response.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_rdap `def parse_rdap(payload)`
- Defined: `estorides_core/parsers.py:96`
- Doc: RDAP (RFC 7483) domain object.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_ipapi `def parse_ipapi(payload)`
- Defined: `estorides_core/parsers.py:171`
- Doc: ip-api.com response.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_ipinfo `def parse_ipinfo(payload)`
- Defined: `estorides_core/parsers.py:197`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_ipapi_co `def parse_ipapi_co(payload)`
- Defined: `estorides_core/parsers.py:212`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_shodan_internetdb `def parse_shodan_internetdb(payload)`
- Defined: `estorides_core/parsers.py:221`
- Doc: internetdb.shodan.io — IP service summary.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_greynoise `def parse_greynoise(payload)`
- Defined: `estorides_core/parsers.py:235`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_ipwhois `def parse_ipwhois(payload)`
- Defined: `estorides_core/parsers.py:250`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_abuseipdb `def parse_abuseipdb(payload)`
- Defined: `estorides_core/parsers.py:268`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### _vt_stats `def _vt_stats(attrs)`
- Defined: `estorides_core/parsers.py:284`
- Doc: Flatten VirusTotal v3 last_analysis_stats into a compact dict.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_vt_ip `def parse_vt_ip(payload)`
- Defined: `estorides_core/parsers.py:298`
- Doc: VirusTotal v3 — IP address object.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_vt_domain `def parse_vt_domain(payload)`
- Defined: `estorides_core/parsers.py:319`
- Doc: VirusTotal v3 — domain object.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_vt_file `def parse_vt_file(payload)`
- Defined: `estorides_core/parsers.py:346`
- Doc: VirusTotal v3 — file object.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_ripe_stat `def parse_ripe_stat(payload)`
- Defined: `estorides_core/parsers.py:370`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_nominatim `def parse_nominatim(payload)`
- Defined: `estorides_core/parsers.py:381`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_urlscan `def parse_urlscan(payload)`
- Defined: `estorides_core/parsers.py:399`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_wayback_cdx `def parse_wayback_cdx(payload)`
- Defined: `estorides_core/parsers.py:421`
- Doc: CDX returns a list where the first row is the header.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_wayback_avail `def parse_wayback_avail(payload)`
- Defined: `estorides_core/parsers.py:434`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_threatfox `def parse_threatfox(payload)`
- Defined: `estorides_core/parsers.py:443`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_urlhaus `def parse_urlhaus(payload)`
- Defined: `estorides_core/parsers.py:452`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_urlhaus_payloads `def parse_urlhaus_payloads(payload)`
- Defined: `estorides_core/parsers.py:461`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_malwarebazaar `def parse_malwarebazaar(payload)`
- Defined: `estorides_core/parsers.py:470`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_otx `def parse_otx(payload)`
- Defined: `estorides_core/parsers.py:479`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_hibp_breach `def parse_hibp_breach(payload)`
- Defined: `estorides_core/parsers.py:503`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_hibp_paste `def parse_hibp_paste(payload)`
- Defined: `estorides_core/parsers.py:521`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_phonebook `def parse_phonebook(payload)`
- Defined: `estorides_core/parsers.py:537`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_wikipedia `def parse_wikipedia(payload)`
- Defined: `estorides_core/parsers.py:558`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_wikidata `def parse_wikidata(payload)`
- Defined: `estorides_core/parsers.py:567`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_openalex `def parse_openalex(payload)`
- Defined: `estorides_core/parsers.py:579`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_crossref `def parse_crossref(payload)`
- Defined: `estorides_core/parsers.py:599`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_arxiv `def parse_arxiv(payload)`
- Defined: `estorides_core/parsers.py:619`
- Doc: arXiv returns Atom XML; we expect callers to have converted to a dict.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_nvd_cve `def parse_nvd_cve(payload)`
- Defined: `estorides_core/parsers.py:640`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_github_advisories `def parse_github_advisories(payload)`
- Defined: `estorides_core/parsers.py:662`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_blockchain_btc `def parse_blockchain_btc(payload)`
- Defined: `estorides_core/parsers.py:686`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_blockstream `def parse_blockstream(payload)`
- Defined: `estorides_core/parsers.py:702`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_ethplorer `def parse_ethplorer(payload)`
- Defined: `estorides_core/parsers.py:718`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_microlink `def parse_microlink(payload)`
- Defined: `estorides_core/parsers.py:734`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_github_user `def parse_github_user(payload)`
- Defined: `estorides_core/parsers.py:754`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_github_search `def parse_github_search(payload)`
- Defined: `estorides_core/parsers.py:774`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_reddit `def parse_reddit(payload)`
- Defined: `estorides_core/parsers.py:789`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_mastodon `def parse_mastodon(payload)`
- Defined: `estorides_core/parsers.py:819`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_keybase `def parse_keybase(payload)`
- Defined: `estorides_core/parsers.py:835`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_hackernews `def parse_hackernews(payload)`
- Defined: `estorides_core/parsers.py:859`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_reddit_search `def parse_reddit_search(payload)`
- Defined: `estorides_core/parsers.py:871`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_dev_to `def parse_dev_to(payload)`
- Defined: `estorides_core/parsers.py:885`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_text_lines `def parse_text_lines(payload)`
- Defined: `estorides_core/parsers.py:900`
- Doc: Generic: split raw_text by newlines, drop empties.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_raw_text `def parse_raw_text(payload)`
- Defined: `estorides_core/parsers.py:911`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_http_headers `def parse_http_headers(payload)`
- Defined: `estorides_core/parsers.py:919`
- Doc: hackertarget returns text; expect a one-line-per-header response.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_whois_text `def parse_whois_text(payload)`
- Defined: `estorides_core/parsers.py:935`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_twitter_user `def parse_twitter_user(payload)`
- Defined: `estorides_core/parsers.py:953`
- Doc: Twitter/X API v2 user by username.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_youtube_user `def parse_youtube_user(payload)`
- Defined: `estorides_core/parsers.py:988`
- Doc: YouTube Data API v3 channel by handle.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_twitch_user `def parse_twitch_user(payload)`
- Defined: `estorides_core/parsers.py:1025`
- Doc: Twitch Helix API user by login.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### parse_discord_discovery `def parse_discord_discovery(payload)`
- Defined: `estorides_core/parsers.py:1058`
- Doc: Discord server discovery via discords.com API.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### _normalise_discord_server `def _normalise_discord_server(raw)`
- Defined: `estorides_core/parsers.py:1078`
- Doc: Normalise a single raw Discord server dict into a standard shape.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### get_parser `def get_parser(name)`
- Defined: `estorides_core/parsers.py:1175`
- Doc: Return the parser function for `name`, or a passthrough lambda.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### register_parser `def register_parser(name, description)`
- Defined: `estorides_core/parsers.py:1188`
- Doc: Decorator: register `func` as a parser under `name`.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### list_parsers `def list_parsers()`
- Defined: `estorides_core/parsers.py:1204`
- Doc: Return (name, description) tuples for every registered parser.
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

### deco `def deco(func)`
- Defined: `estorides_core/parsers.py:1196`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/system_app_sources.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_socmint.py`

## estorides_core/pdns_monitor.py

### classify_subdomain_status `def classify_subdomain_status(fqdn, resolved_ips)`
- Defined: `estorides_core/pdns_monitor.py:72`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`, `tests/test_pdns_monitor.py`

### extract_sans_from_cert `def extract_sans_from_cert(cert)`
- Defined: `estorides_core/pdns_monitor.py:76`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`, `tests/test_pdns_monitor.py`

### analyse_pdns_data `def analyse_pdns_data(subdomains, ip_history, new_certs)`
- Defined: `estorides_core/pdns_monitor.py:80`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`, `tests/test_pdns_monitor.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/pdns_monitor.py:22`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`, `tests/test_pdns_monitor.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/pdns_monitor.py:35`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`, `tests/test_pdns_monitor.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/pdns_monitor.py:50`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`, `tests/test_pdns_monitor.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/pdns_monitor.py:62`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_pdns_monitor.py`, `tests/test_pdns_monitor.py`

## estorides_core/people_intel.py

### infer_email_pattern `def infer_email_pattern(emails)`
- Defined: `estorides_core/people_intel.py:98`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### _match_pattern `def _match_pattern(local)`
- Defined: `estorides_core/people_intel.py:136`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### _severity_from_breaches `def _severity_from_breaches(breaches)`
- Defined: `estorides_core/people_intel.py:143`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### correlate_breaches `def correlate_breaches(employees)`
- Defined: `estorides_core/people_intel.py:153`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### analyse_employees `def analyse_employees(employees, domain)`
- Defined: `estorides_core/people_intel.py:176`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/people_intel.py:22`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/people_intel.py:40`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/people_intel.py:62`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/people_intel.py:75`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_people_intel.py`

## estorides_core/pivot_engine.py

### emit `def emit(self, event)`
- Defined: `estorides_core/pivot_engine.py:62`
- Doc: Publish one event. A slow or failing sink must never break a run.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/pivot_engine.py:70`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### emit `def emit(self, event)`
- Defined: `estorides_core/pivot_engine.py:73`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### __init__ `def __init__(self, capacity)`
- Defined: `estorides_core/pivot_engine.py:87`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### emit `def emit(self, event)`
- Defined: `estorides_core/pivot_engine.py:94`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### run `def run(self, query)`
- Defined: `estorides_core/pivot_engine.py:120`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### time_left `def time_left(self)`
- Defined: `estorides_core/pivot_engine.py:155`
- Doc: Seconds remaining before the global wall-clock deadline.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### exhausted `def exhausted(self)`
- Defined: `estorides_core/pivot_engine.py:159`
- Doc: Reason the run must stop, or None while budget remains.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### __init__ `def __init__(self, runner, sink)`
- Defined: `estorides_core/pivot_engine.py:198`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### _emit `def _emit(self, event_type)`
- Defined: `estorides_core/pivot_engine.py:246`
- Doc: Build and publish an event, swallowing any sink failure.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### _heap_push `def _heap_push(heap, counter, lead)`
- Defined: `estorides_core/pivot_engine.py:255`
- Doc: Push a lead as a max-heap by score (negated for heapq).
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### run `def run(self, seed_type, seed_value)`
- Defined: `estorides_core/pivot_engine.py:264`
- Doc: Execute the cross-search from `(seed_type, seed_value)`.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### _expand_lead `def _expand_lead(self, lead, frontier, budget)`
- Defined: `estorides_core/pivot_engine.py:341`
- Doc: Run the fan-out for one lead and enqueue its scored children.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### _ingest_children `def _ingest_children(self, parent, result, frontier, budget)`
- Defined: `estorides_core/pivot_engine.py:411`
- Doc: Score the entities a target produced and enqueue the best ones.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### _on_source_done `def _on_source_done(name, ok, status, elapsed_ms)`
- Defined: `estorides_core/pivot_engine.py:356`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

### _on_source_result `def _on_source_result(observation)`
- Defined: `estorides_core/pivot_engine.py:366`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_people.py`, `estorides_core/discoverer.py`, `estorides_web.py`

## estorides_core/recon_fusion.py

### _normalize_value `def _normalize_value(etype, value)`
- Defined: `estorides_core/recon_fusion.py:104`
- Doc: Deterministic normalisation matching fusion_store.entity_id.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _canonical_id `def _canonical_id(etype, value)`
- Defined: `estorides_core/recon_fusion.py:109`
- Doc: Deterministic sha1-based entity id matching fusion_store convention.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _reliability_weight `def _reliability_weight(source_name, overrides)`
- Defined: `estorides_core/recon_fusion.py:115`
- Doc: Map a source name to its numeric reliability weight.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _corroboration_factor `def _corroboration_factor(source_count)`
- Defined: `estorides_core/recon_fusion.py:134`
- Doc: Logarithmic corroboration weight: min(1, log10(1 + n)).
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _freshness_factor `def _freshness_factor(age_hours, max_hours)`
- Defined: `estorides_core/recon_fusion.py:141`
- Doc: Linear freshness decay from 1.0 (fresh) to 0.1 (stale).
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _direct_match_query `def _direct_match_query(value, query)`
- Defined: `estorides_core/recon_fusion.py:149`
- Doc: True if the entity value matches the original query.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _extract_key_findings `def _extract_key_findings(observations)`
- Defined: `estorides_core/recon_fusion.py:154`
- Doc: Extract textual key findings from a list of observations.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _reliability_weight_for_letter `def _reliability_weight_for_letter(letter)`
- Defined: `estorides_core/recon_fusion.py:443`
- Doc: Convert a reliability letter (A-F) to its numeric weight.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### ordered `def ordered(cls)`
- Defined: `estorides_core/recon_fusion.py:37`
- Doc: Return tiers in canonical display order.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/recon_fusion.py:61`
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/recon_fusion.py:92`
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### __init__ `def __init__(self, config)`
- Defined: `estorides_core/recon_fusion.py:183`
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### classify `def classify(self, query, query_type, observations, entities)`
- Defined: `estorides_core/recon_fusion.py:186`
- Doc: Classify raw observations and entities into relevance-tiered groups.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _deduplicate `def _deduplicate(self, observations)`
- Defined: `estorides_core/recon_fusion.py:236`
- Doc: Remove exact duplicates based on config dedup keys.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _group_by_entity `def _group_by_entity(self, observations, entities)`
- Defined: `estorides_core/recon_fusion.py:254`
- Doc: Group observations and entities by canonical entity id.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _classify_groups `def _classify_groups(self, groups, query)`
- Defined: `estorides_core/recon_fusion.py:338`
- Doc: Assign each group a relevance tier and score.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

### _assign_tier `def _assign_tier(self, source_count, avg_reliability, direct_match)`
- Defined: `estorides_core/recon_fusion.py:403`
- Doc: Determine the relevance tier based on source count and reliability.
- Depends on: `estorides_core/config.py`, `estorides_core/reliability_scoring.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_recon_fusion_properties.py`, `tests/test_recon_fusion.py`, `tests/test_ui_professional.py`

## estorides_core/recon_pipeline.py

### run_passive_recon `def run_passive_recon(query, headers, html, cookies, employees, code_findings, third_parties, pdns_subdomains, cloud_assets)`
- Defined: `estorides_core/recon_pipeline.py:22`
- Depends on: `estorides_core/cloud_asset_discovery.py`, `estorides_core/code_exposure.py`, `estorides_core/pdns_monitor.py`, `estorides_core/people_intel.py`, `estorides_core/supply_chain.py`, `estorides_core/tech_fingerprint.py`, `estorides_core/vuln_correlation.py`

## estorides_core/relationship_inference.py

### register_inferer `def register_inferer(source_name)`
- Defined: `estorides_core/relationship_inference.py:63`
- Doc: Decorator: register `func` as the inferer for `source_name`.
- Imported by: `estorides_core/orchestrator.py`

### infer_relationship `def infer_relationship(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:78`
- Doc: Dispatch an observation to its inferer (if any).
- Imported by: `estorides_core/orchestrator.py`

### _infer_dns `def _infer_dns(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:105`
- Imported by: `estorides_core/orchestrator.py`

### _infer_crtsh `def _infer_crtsh(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:114`
- Imported by: `estorides_core/orchestrator.py`

### _infer_shodan `def _infer_shodan(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:122`
- Imported by: `estorides_core/orchestrator.py`

### _infer_greynoise `def _infer_greynoise(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:134`
- Imported by: `estorides_core/orchestrator.py`

### _infer_abuseipdb `def _infer_abuseipdb(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:143`
- Imported by: `estorides_core/orchestrator.py`

### _infer_whois `def _infer_whois(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:152`
- Imported by: `estorides_core/orchestrator.py`

### _infer_urlscan `def _infer_urlscan(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:163`
- Imported by: `estorides_core/orchestrator.py`

### _infer_phonebook `def _infer_phonebook(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:175`
- Imported by: `estorides_core/orchestrator.py`

### _infer_ipapi `def _infer_ipapi(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:186`
- Imported by: `estorides_core/orchestrator.py`

### _infer_otx `def _infer_otx(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:195`
- Imported by: `estorides_core/orchestrator.py`

### _infer_nvd `def _infer_nvd(observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:208`
- Imported by: `estorides_core/orchestrator.py`

### __call__ `def __call__(self, observation, query, kg)`
- Defined: `estorides_core/relationship_inference.py:51`
- Imported by: `estorides_core/orchestrator.py`

### deco `def deco(func)`
- Defined: `estorides_core/relationship_inference.py:70`
- Imported by: `estorides_core/orchestrator.py`

## estorides_core/reliability_scoring.py

### _corroboration_weight `def _corroboration_weight(n)`
- Defined: `estorides_core/reliability_scoring.py:279`
- Doc: ``min(1, log10(1 + n))``.  0 sources → 0; 1 → 0.30; 9 → 1.0.
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### _freshness_weight `def _freshness_weight(age_seconds, half_life_days)`
- Defined: `estorides_core/reliability_scoring.py:286`
- Doc: Exponential decay.  age=0 → 1.0; one half-life → 0.5.
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### _validate_score `def _validate_score(value, field_name)`
- Defined: `estorides_core/reliability_scoring.py:296`
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### _clamp01 `def _clamp01(value)`
- Defined: `estorides_core/reliability_scoring.py:301`
- Doc: Clamp to the closed unit interval.
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### compute_confidence `def compute_confidence(inp)`
- Defined: `estorides_core/reliability_scoring.py:311`
- Doc: Compute the audit-trailed confidence score for one observation.
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### merge_confidence `def merge_confidence(existing, new_observation)`
- Defined: `estorides_core/reliability_scoring.py:349`
- Doc: Merge a new observation's confidence into an existing entity score.
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### reliability_from_name `def reliability_from_name(source_name)`
- Defined: `estorides_core/reliability_scoring.py:399`
- Doc: Look up the reliability for a source by name; never raises.
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### source_type_from_name `def source_type_from_name(source_name)`
- Defined: `estorides_core/reliability_scoring.py:414`
- Doc: Look up the source type hierarchy for a source by name; never raises.
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/reliability_scoring.py:252`
- Imported by: `estorides_core/change_detection.py`, `estorides_core/fusion_store.py`, `estorides_core/hypothesis_engine.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `estorides_core/recon_fusion.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/properties/test_reliability_scoring_properties.py`, `tests/test_change_detection.py`, `tests/test_hypothesis_engine.py`, `tests/test_reliability_scoring.py`

## estorides_core/scope.py

### normalise_asset `def normalise_asset(raw)`
- Defined: `estorides_core/scope.py:52`
- Doc: Reduce a raw asset string to a comparable host or IP literal.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### is_ip `def is_ip(asset)`
- Defined: `estorides_core/scope.py:79`
- Doc: True when `asset` parses as a bare IPv4 or IPv6 address.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### _wildcard_factory `def _wildcard_factory(text)`
- Defined: `estorides_core/scope.py:161`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### _regex_factory `def _regex_factory(text)`
- Defined: `estorides_core/scope.py:168`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### _cidr_factory `def _cidr_factory(text)`
- Defined: `estorides_core/scope.py:179`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### _ip_factory `def _ip_factory(text)`
- Defined: `estorides_core/scope.py:188`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### _exact_host_factory `def _exact_host_factory(text)`
- Defined: `estorides_core/scope.py:195`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### parse_rule `def parse_rule(line)`
- Defined: `estorides_core/scope.py:211`
- Doc: Parse one rule line into a ScopeRule, or None for blank/comment/invalid.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### parse_rules `def parse_rules(lines)`
- Defined: `estorides_core/scope.py:223`
- Doc: Parse many rule lines, skipping blanks, comments and invalid entries.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### load_rules_file `def load_rules_file(path)`
- Defined: `estorides_core/scope.py:285`
- Doc: Build a matcher from a rules file, honouring the out-of-scope divider.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### load_assets `def load_assets(path)`
- Defined: `estorides_core/scope.py:303`
- Doc: Read assets from a file: a discover surface JSON or a flat host list.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### _assets_from_json `def _assets_from_json(doc)`
- Defined: `estorides_core/scope.py:322`
- Doc: Extract candidate assets from a parsed discover/result JSON document.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### build_report `def build_report(matcher, assets)`
- Defined: `estorides_core/scope.py:371`
- Doc: Classify `assets` with `matcher` and return a :class:`ScopeReport`.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### write_flat_lists `def write_flat_lists(report, out_dir)`
- Defined: `estorides_core/scope.py:381`
- Doc: Write newline-delimited flat lists for piping into active tooling.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### matches `def matches(self, asset)`
- Defined: `estorides_core/scope.py:93`
- Doc: True when `asset` (already normalised) is covered by this rule.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### describe `def describe(self)`
- Defined: `estorides_core/scope.py:97`
- Doc: Human-readable form of the rule, for reports and audit.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### matches `def matches(self, asset)`
- Defined: `estorides_core/scope.py:107`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### describe `def describe(self)`
- Defined: `estorides_core/scope.py:112`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### matches `def matches(self, asset)`
- Defined: `estorides_core/scope.py:122`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### describe `def describe(self)`
- Defined: `estorides_core/scope.py:125`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### matches `def matches(self, asset)`
- Defined: `estorides_core/scope.py:135`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### describe `def describe(self)`
- Defined: `estorides_core/scope.py:143`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### matches `def matches(self, asset)`
- Defined: `estorides_core/scope.py:153`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### describe `def describe(self)`
- Defined: `estorides_core/scope.py:156`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### __init__ `def __init__(self, in_scope, out_of_scope)`
- Defined: `estorides_core/scope.py:242`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### in_rules `def in_rules(self)`
- Defined: `estorides_core/scope.py:251`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### out_rules `def out_rules(self)`
- Defined: `estorides_core/scope.py:255`
- Imported by: `_test_scope.py`, `estorides_cli.py`

### classify `def classify(self, raw_asset)`
- Defined: `estorides_core/scope.py:258`
- Doc: Return IN_SCOPE, OUT_OF_SCOPE or UNKNOWN for a single asset.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### partition `def partition(self, assets)`
- Defined: `estorides_core/scope.py:269`
- Doc: Bucket many assets, returning sorted, de-duplicated lists.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### hosts `def hosts(self)`
- Defined: `estorides_core/scope.py:352`
- Doc: In-scope hostnames (everything in-scope that is not an IP).
- Imported by: `_test_scope.py`, `estorides_cli.py`

### ips `def ips(self)`
- Defined: `estorides_core/scope.py:357`
- Doc: In-scope bare IP addresses.
- Imported by: `_test_scope.py`, `estorides_cli.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/scope.py:361`
- Imported by: `_test_scope.py`, `estorides_cli.py`

## estorides_core/search_telemetry.py

### disallowed_brands_in `def disallowed_brands_in(text)`
- Defined: `estorides_core/search_telemetry.py:75`
- Doc: Return the third-party brand tokens found in ``text``.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### emoji_in `def emoji_in(text)`
- Defined: `estorides_core/search_telemetry.py:89`
- Doc: Return the emoji glyphs found in ``text``, de-duplicated in order.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### percent_encoded_emoji_in `def percent_encoded_emoji_in(text)`
- Defined: `estorides_core/search_telemetry.py:103`
- Doc: Return percent-encoded supplementary-plane emoji sequences in ``text``.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### _assert_clean `def _assert_clean(label)`
- Defined: `estorides_core/search_telemetry.py:167`
- Doc: Raise :class:`InvalidTelemetryConfigError` if any text leaks brand/emoji.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### _default_config `def _default_config()`
- Defined: `estorides_core/search_telemetry.py:309`
- Doc: Build the canonical Estorides telemetry catalog.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/search_telemetry.py:191`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### __init__ `def __init__(self, config)`
- Defined: `estorides_core/search_telemetry.py:223`
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### shortcuts `def shortcuts(self)`
- Defined: `estorides_core/search_telemetry.py:229`
- Doc: Return the keyboard-shortcut catalog.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### tips `def tips(self)`
- Defined: `estorides_core/search_telemetry.py:233`
- Doc: Return the onboarding tips catalog.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### phases `def phases(self)`
- Defined: `estorides_core/search_telemetry.py:237`
- Doc: Return the search-phase vocabulary.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### phase `def phase(self, key)`
- Defined: `estorides_core/search_telemetry.py:241`
- Doc: Return the phase for ``key`` or raise :class:`UnknownPhaseError`.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### progress `def progress(self, completed, total, phase_key)`
- Defined: `estorides_core/search_telemetry.py:249`
- Doc: Compute a clamped, render-ready :class:`ProgressView`.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

### context `def context(self)`
- Defined: `estorides_core/search_telemetry.py:288`
- Doc: Return the JSON-serialisable catalog for template/JS injection.
- Depends on: `estorides_core/config.py`
- Imported by: `estorides_web.py`, `tests/properties/test_search_telemetry_properties.py`, `tests/test_csp_safe_styles.py`, `tests/test_search_telemetry.py`, `tests/test_ui_professional.py`

## estorides_core/socmint.py

### _extract_profile_urls `def _extract_profile_urls(text)`
- Defined: `estorides_core/socmint.py:164`
- Doc: Extract social media profile URLs from a text blob.
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

### _confidence_for_platform_matches `def _confidence_for_platform_matches(platform_count, has_verified, has_keybase)`
- Defined: `estorides_core/socmint.py:185`
- Doc: Compute cross-platform confidence based on evidence strength.
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/socmint.py:92`
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/socmint.py:119`
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/socmint.py:214`
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

### resolve `def resolve(self, username, platforms)`
- Defined: `estorides_core/socmint.py:218`
- Doc: Build a SocialMediaProfile for a username across all platforms.
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

### discover_from_text `def discover_from_text(self, text)`
- Defined: `estorides_core/socmint.py:311`
- Doc: Extract social media profiles from a text blob.
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

### platform_list `def platform_list(self)`
- Defined: `estorides_core/socmint.py:344`
- Doc: Return the full platform registry as a serialisable list.
- Imported by: `estorides_web.py`, `tests/test_socmint.py`, `tests/test_socmint.py`, `tests/test_socmint.py`

## estorides_core/source_health_monitoring.py

### _env_float `def _env_float(name, default)`
- Defined: `estorides_core/source_health_monitoring.py:28`
- Doc: Read a float env var, falling back to default on absence/error.
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### _env_int `def _env_int(name, default)`
- Defined: `estorides_core/source_health_monitoring.py:40`
- Doc: Read an int env var, falling back to default on absence/error.
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### _clamp01 `def _clamp01(value)`
- Defined: `estorides_core/source_health_monitoring.py:224`
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### _classify `def _classify(success_rate, avg_latency_ms, freshness_hours, fetch_count, config)`
- Defined: `estorides_core/source_health_monitoring.py:232`
- Doc: Classify a source's health status based on thresholds.
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### compute_health `def compute_health(inp, config)`
- Defined: `estorides_core/source_health_monitoring.py:257`
- Doc: Compute the health assessment for a single source.
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### build_dashboard `def build_dashboard(records, config)`
- Defined: `estorides_core/source_health_monitoring.py:317`
- Doc: Build a health dashboard from per-source health inputs.
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/source_health_monitoring.py:80`
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_core/source_health_monitoring.py:134`
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/source_health_monitoring.py:168`
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/source_health_monitoring.py:206`
- Imported by: `tests/properties/test_source_health_monitoring_properties.py`, `tests/test_source_health_monitoring.py`

## estorides_core/source_loader.py

### __init__ `def __init__(self, data)`
- Defined: `estorides_core/source_loader.py:28`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### __getattr__ `def __getattr__(self, key)`
- Defined: `estorides_core/source_loader.py:31`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### __init__ `def __init__(self, sources_dir)`
- Defined: `estorides_core/source_loader.py:41`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### load `def load(self)`
- Defined: `estorides_core/source_loader.py:47`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _load_file `def _load_file(self, path)`
- Defined: `estorides_core/source_loader.py:71`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _normalise `def _normalise(self, raw)`
- Defined: `estorides_core/source_loader.py:100`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### get `def get(self, name)`
- Defined: `estorides_core/source_loader.py:188`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### all `def all(self)`
- Defined: `estorides_core/source_loader.py:191`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### by_category `def by_category(self, category)`
- Defined: `estorides_core/source_loader.py:194`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### categories `def categories(self)`
- Defined: `estorides_core/source_loader.py:197`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### names `def names(self)`
- Defined: `estorides_core/source_loader.py:200`
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### filter `def filter(self)`
- Defined: `estorides_core/source_loader.py:203`
- Doc: Return sources matching the given predicates.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _category_dir_name `def _category_dir_name(self, category)`
- Defined: `estorides_core/source_loader.py:225`
- Doc: Derive a filesystem-safe directory name from a category label.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _source_path `def _source_path(self, name, category)`
- Defined: `estorides_core/source_loader.py:241`
- Doc: Derive the filesystem path for a source based on its name and category.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _find_source_file `def _find_source_file(self, name)`
- Defined: `estorides_core/source_loader.py:247`
- Doc: Locate a source file on disk by name, scanning all category dirs.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### write_source_file `def write_source_file(self, data)`
- Defined: `estorides_core/source_loader.py:259`
- Doc: Write a source dict to the correct YAML file, overwriting if exists.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### delete_source_file `def delete_source_file(self, name)`
- Defined: `estorides_core/source_loader.py:329`
- Doc: Delete a source file by name. Raises KeyError if not found on disk.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### summary `def summary(self)`
- Defined: `estorides_core/source_loader.py:338`
- Doc: Compact summary used by /api/status.
- Depends on: `estorides_core/config.py`
- Imported by: `_test_passive.py`, `estorides_core/orchestrator.py`, `tests/test_monitoring.py`, `tests/test_socmint.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

## estorides_core/ssrf_guard.py

### _is_blocked_v4 `def _is_blocked_v4(ip)`
- Defined: `estorides_core/ssrf_guard.py:110`
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### _is_blocked_v6 `def _is_blocked_v6(addr)`
- Defined: `estorides_core/ssrf_guard.py:114`
- Doc: Match an IPv6 textual address against the prefix table.
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### _normalise_host `def _normalise_host(host)`
- Defined: `estorides_core/ssrf_guard.py:134`
- Doc: Lowercase, strip brackets from IPv6 literals, return None if empty.
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### _is_host_in_blocked_literal `def _is_host_in_blocked_literal(host)`
- Defined: `estorides_core/ssrf_guard.py:142`
- Doc: If `host` is a literal IP in a blocked range, return a reason string.
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### _resolve `def _resolve(host)`
- Defined: `estorides_core/ssrf_guard.py:163`
- Doc: Resolve `host` to its A + AAAA records. Empty on failure.
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### _matches_allowlist `def _matches_allowlist(host, allowlist)`
- Defined: `estorides_core/ssrf_guard.py:180`
- Doc: Return True if `host` matches any entry in the allowlist.
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### _load_allowlist `def _load_allowlist()`
- Defined: `estorides_core/ssrf_guard.py:197`
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### check_url `def check_url(url)`
- Defined: `estorides_core/ssrf_guard.py:202`
- Doc: Validate a URL for outbound fetch.
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### assert_safe `def assert_safe(url)`
- Defined: `estorides_core/ssrf_guard.py:270`
- Doc: Raise SSRFError if `url` is not safe to fetch.
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

### __bool__ `def __bool__(self)`
- Defined: `estorides_core/ssrf_guard.py:105`
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

## estorides_core/supply_chain.py

### detect_mx_provider `def detect_mx_provider(mx_records)`
- Defined: `estorides_core/supply_chain.py:106`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### detect_ns_provider `def detect_ns_provider(ns_records)`
- Defined: `estorides_core/supply_chain.py:114`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### detect_cdn `def detect_cdn(cname)`
- Defined: `estorides_core/supply_chain.py:122`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### analyse_third_parties `def analyse_third_parties(third_parties, subsidiaries)`
- Defined: `estorides_core/supply_chain.py:129`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### detect_shared_infrastructure `def detect_shared_infrastructure(asn)`
- Defined: `estorides_core/supply_chain.py:140`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/supply_chain.py:61`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/supply_chain.py:73`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/supply_chain.py:84`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/supply_chain.py:96`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

## estorides_core/system_app_sources.py

### is_system_app `def is_system_app(source)`
- Defined: `estorides_core/system_app_sources.py:81`
- Doc: True when a source dict is a system_app (or has a binary tool).
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### tool_available `def tool_available(binary)`
- Defined: `estorides_core/system_app_sources.py:91`
- Doc: Resolve a binary on the filesystem (shutil.which).
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### render_args `def render_args(args, query, outdir)`
- Defined: `estorides_core/system_app_sources.py:96`
- Doc: Substitute ``{query}``/``{outdir}`` placeholders in an args template.
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _read_capped `def _read_capped(path, cap)`
- Defined: `estorides_core/system_app_sources.py:121`
- Doc: Read a file, capped at ``cap`` bytes, UTF-8 with replacement.
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _loads_lenient `def _loads_lenient(text)`
- Defined: `estorides_core/system_app_sources.py:131`
- Doc: Best-effort JSON parse of tool output (tolerates log-prefix noise).
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### _line_filter_parser `def _line_filter_parser()`
- Defined: `estorides_core/system_app_sources.py:150`
- Doc: Factory for noise-reducing line parsers (one definition, N tools).
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_amass_json `def parse_amass_json(payload)`
- Defined: `estorides_core/system_app_sources.py:193`
- Doc: amass ``-json`` output: one JSON object per line (DNS + infra).
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_maigret_json `def parse_maigret_json(payload)`
- Defined: `estorides_core/system_app_sources.py:225`
- Doc: maigret ``--json simple``: one object keyed by site name.
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_phoneinfoga_json `def parse_phoneinfoga_json(payload)`
- Defined: `estorides_core/system_app_sources.py:247`
- Doc: phoneinfoga v2 ``scan``: a single JSON object (possibly after logs).
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_sherlock_text `def parse_sherlock_text(payload)`
- Defined: `estorides_core/system_app_sources.py:260`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_holehe_text `def parse_holehe_text(payload)`
- Defined: `estorides_core/system_app_sources.py:265`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_wafw00f_text `def parse_wafw00f_text(payload)`
- Defined: `estorides_core/system_app_sources.py:270`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_sublist3r_lines `def parse_sublist3r_lines(payload)`
- Defined: `estorides_core/system_app_sources.py:275`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_dnsrecon_text `def parse_dnsrecon_text(payload)`
- Defined: `estorides_core/system_app_sources.py:280`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_dnsenum_text `def parse_dnsenum_text(payload)`
- Defined: `estorides_core/system_app_sources.py:285`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_fierce_text `def parse_fierce_text(payload)`
- Defined: `estorides_core/system_app_sources.py:292`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_dmitry_text `def parse_dmitry_text(payload)`
- Defined: `estorides_core/system_app_sources.py:297`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_urlcrazy_text `def parse_urlcrazy_text(payload)`
- Defined: `estorides_core/system_app_sources.py:302`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_metagoofil_text `def parse_metagoofil_text(payload)`
- Defined: `estorides_core/system_app_sources.py:307`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_whatweb_text `def parse_whatweb_text(payload)`
- Defined: `estorides_core/system_app_sources.py:312`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_theharvester_text `def parse_theharvester_text(payload)`
- Defined: `estorides_core/system_app_sources.py:317`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_usufy_text `def parse_usufy_text(payload)`
- Defined: `estorides_core/system_app_sources.py:322`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_mailfy_text `def parse_mailfy_text(payload)`
- Defined: `estorides_core/system_app_sources.py:327`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_phonefy_text `def parse_phonefy_text(payload)`
- Defined: `estorides_core/system_app_sources.py:332`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_searchfy_text `def parse_searchfy_text(payload)`
- Defined: `estorides_core/system_app_sources.py:337`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parse_tool_output `def parse_tool_output(source_name, parser_name, data)`
- Defined: `estorides_core/system_app_sources.py:365`
- Doc: Parse tool output with the declared parser; never raises.
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### execute `def execute(source, query)`
- Defined: `estorides_core/system_app_sources.py:396`
- Doc: Execute one system_app source through the tool_runner sandbox.
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/system_app_sources.py:76`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### parser `def parser(payload)`
- Defined: `estorides_core/system_app_sources.py:165`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### fail `def fail(code, message)`
- Defined: `estorides_core/system_app_sources.py:418`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

### repl `def repl(m)`
- Defined: `estorides_core/system_app_sources.py:109`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`, `tests/test_system_app_sources.py`

## estorides_core/tech_fingerprint.py

### fingerprint `def fingerprint(headers, html, cookies, status)`
- Defined: `estorides_core/tech_fingerprint.py:115`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_tech_fingerprint.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/tech_fingerprint.py:97`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_tech_fingerprint.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/tech_fingerprint.py:107`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_tech_fingerprint.py`

### _add `def _add(name, category, version, source, confidence)`
- Defined: `estorides_core/tech_fingerprint.py:129`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_tech_fingerprint.py`

## estorides_core/tool_install.py

### _elevate `def _elevate(cmd)`
- Defined: `estorides_core/tool_install.py:111`
- Doc: Prepend an elevation wrapper when required.
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### _run `def _run(cmd)`
- Defined: `estorides_core/tool_install.py:126`
- Doc: Run a subprocess as an argument list, capping output.
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### _check_shell_command `def _check_shell_command(command)`
- Defined: `estorides_core/tool_install.py:142`
- Doc: Reject hostile tokens in a trusted recipe's install_command.
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### _needs_elevation `def _needs_elevation(command)`
- Defined: `estorides_core/tool_install.py:148`
- Doc: True when an install_command writes system-wide and needs root.
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### _recipe_path `def _recipe_path(name)`
- Defined: `estorides_core/tool_install.py:154`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### load_recipe `def load_recipe(name)`
- Defined: `estorides_core/tool_install.py:158`
- Doc: Load a tool recipe from ``tool_recipes/<name>.yaml`` (or ``None``).
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### recipe_available `def recipe_available(name)`
- Defined: `estorides_core/tool_install.py:191`
- Doc: True when a recipe exists for ``name`` (the UI gates the button on this).
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### tool_available `def tool_available(binary)`
- Defined: `estorides_core/tool_install.py:196`
- Doc: True when the binary resolves on PATH (mirrors system_app_sources).
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### list_recipes `def list_recipes()`
- Defined: `estorides_core/tool_install.py:205`
- Doc: Names of all tool recipe files in ``tool_recipes/`` (sorted).
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### _install_apt `def _install_apt(recipe)`
- Defined: `estorides_core/tool_install.py:213`
- Doc: Install an apt package via the elevation wrapper (run0/sudo).
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### _install_git `def _install_git(recipe)`
- Defined: `estorides_core/tool_install.py:226`
- Doc: Clone the repo (as operator) and run install_command (elevated if system-wide).
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### install_tool `def install_tool(tool_name)`
- Defined: `estorides_core/tool_install.py:257`
- Doc: Install a missing tool from its recipe (if any).
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### _verify `def _verify(binary)`
- Defined: `estorides_core/tool_install.py:334`
- Doc: Post-install check: can the binary now be resolved?
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### main `def main(argv)`
- Defined: `estorides_core/tool_install.py:344`
- Doc: Minimal CLI: ``python -m estorides_core.tool_install <tool> [--force]``.
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### has_apt `def has_apt(self)`
- Defined: `estorides_core/tool_install.py:89`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### has_git `def has_git(self)`
- Defined: `estorides_core/tool_install.py:92`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/tool_install.py:107`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web.py`, `estorides_web.py`, `tests/test_tool_install.py`

## estorides_core/tool_runner.py

### _check_injection `def _check_injection(args)`
- Defined: `estorides_core/tool_runner.py:97`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _resolve_binary `def _resolve_binary(tool_name)`
- Defined: `estorides_core/tool_runner.py:107`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _check_allowlist `def _check_allowlist(tool_name)`
- Defined: `estorides_core/tool_runner.py:114`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### _parse_entities_generic `def _parse_entities_generic(stdout, tool_name)`
- Defined: `estorides_core/tool_runner.py:121`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### run_tool `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)`
- Defined: `estorides_core/tool_runner.py:156`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/tool_runner.py:51`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### from_failure `def from_failure(cls, tool_name, error_code, error_message, duration_s, exit_code, stdout, stderr, parsed_entities)`
- Defined: `estorides_core/tool_runner.py:59`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/tool_runner.py:93`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/system_app_sources.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

## estorides_core/transforms.py

### _empty `def _empty(root_type, value)`
- Defined: `estorides_core/transforms.py:61`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _resolver_filtered `def _resolver_filtered(ent_type, value, relations)`
- Defined: `estorides_core/transforms.py:65`
- Doc: Resolve `(ent_type, value)` and keep only links whose relation is
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _filter_runner `def _filter_runner(relations)`
- Defined: `estorides_core/transforms.py:86`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _norm `def _norm(s)`
- Defined: `estorides_core/transforms.py:95`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _osiris `def _osiris()`
- Defined: `estorides_core/transforms.py:100`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _run_bgp `def _run_bgp(ent_type, value)`
- Defined: `estorides_core/transforms.py:108`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _run_leaks `def _run_leaks(ent_type, value)`
- Defined: `estorides_core/transforms.py:134`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _run_github `def _run_github(ent_type, value)`
- Defined: `estorides_core/transforms.py:159`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### _T `def _T(id, label, tier, applies, runner, description)`
- Defined: `estorides_core/transforms.py:230`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### summary `def summary(self)`
- Defined: `estorides_core/transforms.py:51`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### run `def run(ent_type, value)`
- Defined: `estorides_core/transforms.py:87`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### __init__ `def __init__(self)`
- Defined: `estorides_core/transforms.py:193`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### register `def register(self, t)`
- Defined: `estorides_core/transforms.py:196`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### for_type `def for_type(self, ent_type)`
- Defined: `estorides_core/transforms.py:199`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

### run `def run(self, transform_id, ent_type, value)`
- Defined: `estorides_core/transforms.py:209`
- Depends on: `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`

## estorides_core/transliteration.py

### _strip_diacritics `def _strip_diacritics(text)`
- Defined: `estorides_core/transliteration.py:76`
- Doc: Drop combining marks via NFKD decomposition.
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_resolution.py`, `tests/test_entity_resolution.py`

### to_latin `def to_latin(text)`
- Defined: `estorides_core/transliteration.py:87`
- Doc: Return a lowercased, diacritic-free Latin transliteration.
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_resolution.py`, `tests/test_entity_resolution.py`

### consonant_skeleton `def consonant_skeleton(text)`
- Defined: `estorides_core/transliteration.py:112`
- Doc: Return the Latin transliteration with vowels and spaces removed.
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_resolution.py`, `tests/test_entity_resolution.py`

### is_non_latin `def is_non_latin(text)`
- Defined: `estorides_core/transliteration.py:139`
- Doc: True if any character is outside the Basic Latin / Latin-1 range.
- Imported by: `_test_entity_resolution.py`, `estorides_core/entity_resolution.py`, `tests/test_entity_resolution.py`

## estorides_core/validation.py

### _strip_and_collapse `def _strip_and_collapse(text)`
- Defined: `estorides_core/validation.py:73`
- Depends on: `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_tool_runner.py`

### validate_query `def validate_query(raw)`
- Defined: `estorides_core/validation.py:85`
- Doc: Validate and normalise a user query string.
- Depends on: `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_tool_runner.py`

### __init__ `def __init__(self, reason, message)`
- Defined: `estorides_core/validation.py:57`
- Depends on: `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_tool_runner.py`

### __str__ `def __str__(self)`
- Defined: `estorides_core/validation.py:69`
- Depends on: `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_tool_runner.py`

## estorides_core/vuln_correlation.py

### _parsed_version `def _parsed_version(version)`
- Defined: `estorides_core/vuln_correlation.py:141`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

### _version_in_range `def _version_in_range(version, v_start, v_end)`
- Defined: `estorides_core/vuln_correlation.py:153`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

### lookup_cve_for_tech `def lookup_cve_for_tech(tech_name, version)`
- Defined: `estorides_core/vuln_correlation.py:169`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

### correlate_technologies `def correlate_technologies(technologies)`
- Defined: `estorides_core/vuln_correlation.py:202`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

### compute_attack_readiness `def compute_attack_readiness(vulnerabilities)`
- Defined: `estorides_core/vuln_correlation.py:228`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/vuln_correlation.py:19`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/vuln_correlation.py:38`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_core/vuln_correlation.py:52`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

## estorides_core/web_security.py

### build_https_url `def build_https_url(public_host, path, query_string)`
- Defined: `estorides_core/web_security.py:55`
- Doc: Build a safe HTTPS redirect target from a trusted host and client path.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _env_str `def _env_str(name, default)`
- Defined: `estorides_core/web_security.py:134`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _env_int `def _env_int(name, default)`
- Defined: `estorides_core/web_security.py:141`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _env_bool `def _env_bool(name, default)`
- Defined: `estorides_core/web_security.py:152`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### load_security_config `def load_security_config()`
- Defined: `estorides_core/web_security.py:159`
- Doc: Resolve the security policy from env vars.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### install_security `def install_security(app, cfg)`
- Defined: `estorides_core/web_security.py:184`
- Doc: Wire security middleware into a Flask app.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _extract_bearer_token `def _extract_bearer_token()`
- Defined: `estorides_core/web_security.py:301`
- Doc: Pull the bearer token from header, alt-header, cookie, or query param.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### make_auth_gate `def make_auth_gate()`
- Defined: `estorides_core/web_security.py:336`
- Doc: Build the auth gate from the current environment.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### require_auth `def require_auth(view)`
- Defined: `estorides_core/web_security.py:403`
- Doc: Decorator: enforce the bearer-token gate on a view.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### install_auth_gate `def install_auth_gate(app, gate)`
- Defined: `estorides_core/web_security.py:436`
- Doc: Attach the gate to a Flask app and a module-level slot.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _current_gate `def _current_gate()`
- Defined: `estorides_core/web_security.py:455`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### auto_generated_token `def auto_generated_token()`
- Defined: `estorides_core/web_security.py:459`
- Doc: Return the auto-generated token (None if user set ESTORIDES_AUTH_TOKEN manually).
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### is_cors_enabled `def is_cors_enabled(self)`
- Defined: `estorides_core/web_security.py:125`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### is_origin_allowed `def is_origin_allowed(self)`
- Defined: `estorides_core/web_security.py:129`
- Doc: CORS is opt-in; this is the runtime check used by the after_request hook.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _security_headers `def _security_headers(resp)`
- Defined: `estorides_core/web_security.py:232`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _cors_preflight `def _cors_preflight()`
- Defined: `estorides_core/web_security.py:265`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### enabled `def enabled(self)`
- Defined: `estorides_core/web_security.py:366`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### check `def check(self)`
- Defined: `estorides_core/web_security.py:369`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### auth_meta_for_index `def auth_meta_for_index(self)`
- Defined: `estorides_core/web_security.py:377`
- Doc: Token to embed in `index.html` so the UI can auto-authenticate.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### issue_session_cookie_kwargs `def issue_session_cookie_kwargs(self)`
- Defined: `estorides_core/web_security.py:386`
- Doc: Arguments for `set_cookie` to install the session cookie.
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### wrapper `def wrapper()`
- Defined: `estorides_core/web_security.py:417`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

### _redirect_to_https `def _redirect_to_https()`
- Defined: `estorides_core/web_security.py:218`
- Imported by: `estorides_web.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_csp_safe_styles.py`, `tests/test_security_remediation.py`

## estorides_export/encryption.py

### _have_age `def _have_age()`
- Defined: `estorides_export/encryption.py:47`
- Depends on: `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`

### encrypt_file `def encrypt_file(plaintext_path, recipient_pubkey)`
- Defined: `estorides_export/encryption.py:51`
- Doc: Encrypt `plaintext_path` to `<plaintext_path>.age` for the recipient.
- Depends on: `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`

### export_stix_encrypted `def export_stix_encrypted(kg, recipient_pubkey, path)`
- Defined: `estorides_export/encryption.py:100`
- Doc: Build the STIX bundle, write to disk, encrypt to <path>.age.
- Depends on: `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`

### export_misp_encrypted `def export_misp_encrypted(kg, recipient_pubkey, path)`
- Defined: `estorides_export/encryption.py:128`
- Depends on: `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`, `estorides_web.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`, `tests/test_encrypted_export.py`

## estorides_export/misp.py

### event_from_graph `def event_from_graph(kg)`
- Defined: `estorides_export/misp.py:36`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

### _category `def _category(ent_type)`
- Defined: `estorides_export/misp.py:65`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

### export `def export(kg, path)`
- Defined: `estorides_export/misp.py:79`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

## estorides_export/recon_report.py

### redact_sensitive `def redact_sensitive(text)`
- Defined: `estorides_export/recon_report.py:61`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

### build_subdomain_tree `def build_subdomain_tree(subdomains)`
- Defined: `estorides_export/recon_report.py:67`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

### build_executive_summary `def build_executive_summary(critical_findings, total_targets, domain)`
- Defined: `estorides_export/recon_report.py:92`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

### generate_report `def generate_report(query, target_scoring, metadata)`
- Defined: `estorides_export/recon_report.py:114`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

### __post_init__ `def __post_init__(self)`
- Defined: `estorides_export/recon_report.py:29`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_export/recon_report.py:35`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_export/recon_report.py:46`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

### to_dict `def to_dict(self)`
- Defined: `estorides_export/recon_report.py:57`
- Imported by: `estorides_export/__init__.py`, `tests/test_recon_report.py`, `tests/test_recon_report.py`

## estorides_export/report.py

### _tldr `def _tldr(case, entities, sources_queried, sources_succeeded, diff)`
- Defined: `estorides_export/report.py:37`
- Doc: Top-of-page executive summary. 6-10 lines max.
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`

### _iocs `def _iocs(entities)`
- Defined: `estorides_export/report.py:77`
- Doc: The sections the next responder (CTI team, SOC) actually pastes
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`

### _diff_section `def _diff_section(diff)`
- Defined: `estorides_export/report.py:121`
- Doc: The "what's new since last run" block. Empty when no baseline.
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`

### _analysis `def _analysis(case)`
- Defined: `estorides_export/report.py:156`
- Doc: The LLM analysis (or stub) embedded verbatim in a code block.
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`

### _meta_footer `def _meta_footer(case, sources_queried, sources_succeeded)`
- Defined: `estorides_export/report.py:177`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`

### render_markdown_report `def render_markdown_report(case, entities, sources_queried, sources_succeeded, diff)`
- Defined: `estorides_export/report.py:194`
- Doc: Build a Markdown report for `case`.
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `estorides_cli.py`, `estorides_export/__init__.py`, `static/js/estorides.js`

## estorides_export/stix.py

### _id `def _id(stix_type)`
- Defined: `estorides_export/stix.py:28`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

### _now `def _now()`
- Defined: `estorides_export/stix.py:32`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

### bundle_from_graph `def bundle_from_graph(kg)`
- Defined: `estorides_export/stix.py:55`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

### export `def export(kg, path)`
- Defined: `estorides_export/stix.py:145`
- Depends on: `estorides_core/config.py`, `estorides_core/knowledge_graph.py`
- Imported by: `estorides_export/__init__.py`

## estorides_llm/intelligence_prompts.py

### format_context `def format_context(sources)`
- Defined: `estorides_llm/intelligence_prompts.py:98`
- Doc: Render a list of observation dicts into a context block for the LLM.
- Imported by: `estorides_llm/manager.py`

## estorides_llm/manager.py

### register `def register(name)`
- Defined: `estorides_llm/manager.py:90`
- Doc: Decorator: register a backend under `name`.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### __call__ `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- Defined: `estorides_llm/manager.py:62`
- Doc: Return (content, model_id). Empty content means "skip me".
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### stream_generate `def stream_generate(self, prompt, context, model, temperature, request_timeout)`
- Defined: `estorides_llm/manager.py:73`
- Doc: Optional: stream (kind, text) chunks. Base backends may skip.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### deco `def deco(backend_or_cls)`
- Defined: `estorides_llm/manager.py:98`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### get_status `def get_status()`
- Defined: `estorides_llm/manager.py:117`
- Doc: Return available ollama models and reachability status.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### _resolve_model `def _resolve_model(self, request_timeout)`
- Defined: `estorides_llm/manager.py:127`
- Doc: Pick a model ollama actually has pulled.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### stream_generate `def stream_generate(self, prompt, context, model, temperature, request_timeout)`
- Defined: `estorides_llm/manager.py:181`
- Doc: Stream an ollama response as (kind, text) chunks.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### __call__ `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- Defined: `estorides_llm/manager.py:220`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### __call__ `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- Defined: `estorides_llm/manager.py:267`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### __call__ `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- Defined: `estorides_llm/manager.py:312`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### __init__ `def __init__(self)`
- Defined: `estorides_llm/manager.py:350`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### generate `def generate(self, prompt)`
- Defined: `estorides_llm/manager.py:366`
- Doc: Try each backend in priority order; return the first that succeeds.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### get_ollama_status `def get_ollama_status(self)`
- Defined: `estorides_llm/manager.py:407`
- Doc: Return ollama reachability and available models.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### stream `def stream(self, prompt)`
- Defined: `estorides_llm/manager.py:415`
- Doc: Stream an analysis from a specific ollama model.
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

### _stub_response `def _stub_response(self, prompt, context)`
- Defined: `estorides_llm/manager.py:451`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`

## estorides_web.py

### _client_ip `def _client_ip()`
- Defined: `estorides_web.py:75`
- Doc: Best-effort client IP extraction.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _arg_int `def _arg_int(name, default)`
- Defined: `estorides_web.py:92`
- Doc: Read an int query-string arg, falling back to `default` on parse error.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _send_and_cleanup `def _send_and_cleanup(p, tmpdir)`
- Defined: `estorides_web.py:108`
- Doc: Send `p` as an attachment, then nuke `tmpdir` regardless of outcome.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _new_stream_job_id `def _new_stream_job_id()`
- Defined: `estorides_web.py:160`
- Doc: Timestamp-prefixed id so jobs sort chronologically.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _rate_limit_decorator `def _rate_limit_decorator()`
- Defined: `estorides_web.py:165`
- Doc: Decorator: enforce per-IP rate limit, write an audit row either way.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### create_app `def create_app()`
- Defined: `estorides_web.py:209`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _serve_loop `def _serve_loop()`
- Defined: `estorides_web.py:1700`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _shape_for_ui `def _shape_for_ui(result)`
- Defined: `estorides_web.py:1713`
- Doc: Trim raw responses for the UI and reformat observations.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### __init__ `def __init__(self, job_id, query, query_type, case_id)`
- Defined: `estorides_web.py:130`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### stop `def stop(self)`
- Defined: `estorides_web.py:139`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### should_stop `def should_stop(self)`
- Defined: `estorides_web.py:142`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### status `def status(self)`
- Defined: `estorides_web.py:146`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### done `def done(self)`
- Defined: `estorides_web.py:150`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### deco `def deco(view)`
- Defined: `estorides_web.py:172`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### index `def index()`
- Defined: `estorides_web.py:240`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_status `def api_status()`
- Defined: `estorides_web.py:261`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_ollama_status `def api_ollama_status()`
- Defined: `estorides_web.py:267`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_tools_list `def api_tools_list()`
- Defined: `estorides_web.py:277`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_tool_install `def api_tool_install(name)`
- Defined: `estorides_web.py:297`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_tool_install_status `def api_tool_install_status(name)`
- Defined: `estorides_web.py:338`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_run `def api_run()`
- Defined: `estorides_web.py:348`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_graph `def api_graph()`
- Defined: `estorides_web.py:404`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_feeds `def api_feeds()`
- Defined: `estorides_web.py:480`
- Doc: Return real-time feed points (quakes, fires, news) for the map.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_export `def api_export(fmt)`
- Defined: `estorides_web.py:511`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_cases_list `def api_cases_list()`
- Defined: `estorides_web.py:588`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_cases_get `def api_cases_get(case_id)`
- Defined: `estorides_web.py:602`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_cases_delete `def api_cases_delete(case_id)`
- Defined: `estorides_web.py:617`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_cases_save `def api_cases_save(case_id)`
- Defined: `estorides_web.py:626`
- Doc: Bookmark a case from the UI.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_cases_diff `def api_cases_diff()`
- Defined: `estorides_web.py:655`
- Doc: Symmetric diff between two cases by entity (type, value).
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_intel_resolve `def api_intel_resolve()`
- Defined: `estorides_web.py:681`
- Doc: Cross-feed entity resolution (Osiris-style /resolve).
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_intel_graph `def api_intel_graph()`
- Defined: `estorides_web.py:721`
- Doc: Cypher query against the Kùzu persistent graph.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_intel_stats `def api_intel_stats()`
- Defined: `estorides_web.py:762`
- Doc: Stats for both the case store and the Kùzu graph.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_stats `def api_fusion_stats()`
- Defined: `estorides_web.py:782`
- Doc: One-glance dashboard of the fused, cross-run fact base.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_sources `def api_fusion_sources()`
- Defined: `estorides_web.py:791`
- Doc: The YAML source catalogue with accumulated fetch/ok counters.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_entities `def api_fusion_entities()`
- Defined: `estorides_web.py:801`
- Doc: Search fused entities.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_entity `def api_fusion_entity(eid)`
- Defined: `estorides_web.py:823`
- Doc: Full fused view of one entity: provenance, properties, edges.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_analytics_entity_timeline `def api_fusion_analytics_entity_timeline(eid)`
- Defined: `estorides_web.py:842`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_analytics_entity_summary `def api_fusion_analytics_entity_summary(eid)`
- Defined: `estorides_web.py:853`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_analytics_source_stats `def api_fusion_analytics_source_stats(source_name)`
- Defined: `estorides_web.py:864`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_analytics_consensus `def api_fusion_analytics_consensus(eid)`
- Defined: `estorides_web.py:875`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_analytics_top_changed `def api_fusion_analytics_top_changed()`
- Defined: `estorides_web.py:886`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### admin_sources `def admin_sources()`
- Defined: `estorides_web.py:898`
- Doc: Render the YAML source manager page.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_sources_yaml_list `def api_sources_yaml_list()`
- Defined: `estorides_web.py:915`
- Doc: Return every YAML source with full configuration.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_sources_yaml_create `def api_sources_yaml_create()`
- Defined: `estorides_web.py:941`
- Doc: Create a new YAML source.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_sources_yaml_update `def api_sources_yaml_update(name)`
- Defined: `estorides_web.py:962`
- Doc: Update/replace a YAML source.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_sources_yaml_delete `def api_sources_yaml_delete(name)`
- Defined: `estorides_web.py:981`
- Doc: Delete a YAML source.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_fusion_analytics_corroboration_matrix `def api_fusion_analytics_corroboration_matrix()`
- Defined: `estorides_web.py:997`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_socmint_resolve `def api_socmint_resolve()`
- Defined: `estorides_web.py:1012`
- Doc: Resolve a username across known social media platforms.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_socmint_platforms `def api_socmint_platforms()`
- Defined: `estorides_web.py:1035`
- Doc: Return the list of all known social media platforms.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_socmint_discover `def api_socmint_discover()`
- Defined: `estorides_web.py:1044`
- Doc: Extract social media profile URLs from a text blob.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_watch_list `def api_watch_list()`
- Defined: `estorides_web.py:1088`
- Doc: List all watch targets.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_watch_create `def api_watch_create()`
- Defined: `estorides_web.py:1098`
- Doc: Create a new watch target.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_watch_get `def api_watch_get(watch_id)`
- Defined: `estorides_web.py:1133`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_watch_delete `def api_watch_delete(watch_id)`
- Defined: `estorides_web.py:1146`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_watch_enable `def api_watch_enable(watch_id)`
- Defined: `estorides_web.py:1158`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_watch_disable `def api_watch_disable(watch_id)`
- Defined: `estorides_web.py:1172`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_watch_history `def api_watch_history(watch_id)`
- Defined: `estorides_web.py:1185`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_alerts_channels `def api_alerts_channels()`
- Defined: `estorides_web.py:1196`
- Doc: List configured alert channels and their status.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_alerts_test `def api_alerts_test()`
- Defined: `estorides_web.py:1205`
- Doc: Send a test alert to a channel.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_scheduler_status `def api_scheduler_status()`
- Defined: `estorides_web.py:1222`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_transforms `def api_transforms()`
- Defined: `estorides_web.py:1241`
- Doc: List the transforms applicable to an entity type.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_transform_run `def api_transform_run()`
- Defined: `estorides_web.py:1256`
- Doc: Run one transform and return nodes/links for graph merge.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_bgp `def api_osiris_bgp()`
- Defined: `estorides_web.py:1285`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_mac `def api_osiris_mac()`
- Defined: `estorides_web.py:1300`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_phone `def api_osiris_phone()`
- Defined: `estorides_web.py:1315`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_github `def api_osiris_github()`
- Defined: `estorides_web.py:1330`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_leaks `def api_osiris_leaks()`
- Defined: `estorides_web.py:1345`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_kev `def api_osiris_kev()`
- Defined: `estorides_web.py:1360`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_malware `def api_osiris_malware()`
- Defined: `estorides_web.py:1370`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_osiris_threats `def api_osiris_threats()`
- Defined: `estorides_web.py:1377`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_discover_start `def api_discover_start()`
- Defined: `estorides_web.py:1390`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_discover_jobs `def api_discover_jobs()`
- Defined: `estorides_web.py:1436`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_discover_stop `def api_discover_stop()`
- Defined: `estorides_web.py:1442`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_discover_stream `def api_discover_stream()`
- Defined: `estorides_web.py:1454`
- Doc: Server-Sent Events for a discoverer job.
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_run_stream_start `def api_run_stream_start()`
- Defined: `estorides_web.py:1509`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_run_stream_stop `def api_run_stream_stop()`
- Defined: `estorides_web.py:1576`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_run_stream `def api_run_stream()`
- Defined: `estorides_web.py:1588`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### api_analyze_stream `def api_analyze_stream()`
- Defined: `estorides_web.py:1639`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### wrapper `def wrapper()`
- Defined: `estorides_web.py:174`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _worker `def _worker()`
- Defined: `estorides_web.py:309`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### gen `def gen()`
- Defined: `estorides_web.py:1467`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _drive `def _drive()`
- Defined: `estorides_web.py:1539`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### gen `def gen()`
- Defined: `estorides_web.py:1594`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _run `def _run()`
- Defined: `estorides_web.py:1652`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### gen `def gen()`
- Defined: `estorides_web.py:1667`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

### _watch_runner `def _watch_runner(swatch)`
- Defined: `estorides_web.py:1065`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

## install.sh

### install_full
- Defined: `install.sh:51`
- Doc: 3) Two install passes: full first, minimal fallback. We don't want a single Cython build error to leave the user with a 

### install_minimal
- Defined: `install.sh:55`

## static/js/estorides.js

### detectQueryTypeLocal
- Defined: `static/js/estorides.js:44`
- Doc: --- UX helpers (v1.4) ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showToast
- Defined: `static/js/estorides.js:55`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### updateQueryChip
- Defined: `static/js/estorides.js:65`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### setRunProgress
- Defined: `static/js/estorides.js:75`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showEmptyState
- Defined: `static/js/estorides.js:96`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### summariseObservation
- Defined: `static/js/estorides.js:102`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### buildResultCard
- Defined: `static/js/estorides.js:127`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### requestToolInstall
- Defined: `static/js/estorides.js:186`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### pollToolInstall
- Defined: `static/js/estorides.js:209`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### _installErrMsg
- Defined: `static/js/estorides.js:232`
- Doc: Turn a failed install result into a meaningful, non-"unknown" message.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### populateCategoryFilter
- Defined: `static/js/estorides.js:242`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### applyResultFilters
- Defined: `static/js/estorides.js:248`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### bindResultFilters
- Defined: `static/js/estorides.js:269`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showFriendlyError
- Defined: `static/js/estorides.js:277`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### focusGraphNodeByValue
- Defined: `static/js/estorides.js:290`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### switchSidebarTab
- Defined: `static/js/estorides.js:299`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### switchCanvasTab
- Defined: `static/js/estorides.js:303`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### clearMap
- Defined: `static/js/estorides.js:317`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### plotPoints
- Defined: `static/js/estorides.js:322`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### replotStreamData
- Defined: `static/js/estorides.js:424`
- Doc: Rebuild the geospatial + temporal views from everything seen so far. plotPoints clears and redraws from the full coord s
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### stopRunStream
- Defined: `static/js/estorides.js:436`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### runQuery
- Defined: `static/js/estorides.js:451`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### runQueryBlocking
- Defined: `static/js/estorides.js:521`
- Doc: Blocking fallback: the original one-shot render path.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### searchEntity
- Defined: `static/js/estorides.js:554`
- Doc: Deep-search an entity through the full OSINT pipeline without clearing existing data — appends and merges into current s
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### handleRunStreamEvent
- Defined: `static/js/estorides.js:597`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### appendStreamObservation
- Defined: `static/js/estorides.js:635`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### appendStreamEntity
- Defined: `static/js/estorides.js:657`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### clearAll
- Defined: `static/js/estorides.js:686`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### setStatus
- Defined: `static/js/estorides.js:714`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderResult
- Defined: `static/js/estorides.js:720`
- Doc: --- result rendering ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadAnalysisModels
- Defined: `static/js/estorides.js:768`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderAnalysisModels
- Defined: `static/js/estorides.js:775`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### makeModelPill
- Defined: `static/js/estorides.js:787`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderAnalysis
- Defined: `static/js/estorides.js:800`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderMarkdown
- Defined: `static/js/estorides.js:816`
- Doc: Render Markdown to sanitised HTML (CSP-safe). The LLM output is treated as hostile: marked() is a text→HTML parser with 
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### setThinkingVisible
- Defined: `static/js/estorides.js:826`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### toggleThinking
- Defined: `static/js/estorides.js:833`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### reanalyze
- Defined: `static/js/estorides.js:838`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### analyseEntity
- Defined: `static/js/estorides.js:928`
- Doc: Analyse a single graph/fusion entity: seed the analysis context with the entity's own data (kept in the Results context 
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### expandNode
- Defined: `static/js/estorides.js:961`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### mergeExpansionIntoGraph
- Defined: `static/js/estorides.js:989`
- Doc: Merge a /api/intel/resolve response into the current D3 graph and Leaflet map. Idempotent: re-clicking the same node won
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### drawGraphWithExtras
- Defined: `static/js/estorides.js:1049`
- Doc: Re-draws the D3 graph with the original nodes/edges PLUS any extras passed in (from a /api/intel/resolve call). The extr
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### pushLink
- Defined: `static/js/estorides.js:1073`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### resolverTypeFor
- Defined: `static/js/estorides.js:1107`
- Doc: Map a graph node's type/kind onto a resolver/transform entity type.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### saveLevelOverrides
- Defined: `static/js/estorides.js:1123`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### levelOf
- Defined: `static/js/estorides.js:1127`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### clusterColor
- Defined: `static/js/estorides.js:1131`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### safeColor
- Defined: `static/js/estorides.js:1141`
- Doc: Cluster colors come from remote data (TELEMETRY.cluster_palette and per-cluster `color`). Treat them as hostile: only ac
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### deriveClusters
- Defined: `static/js/estorides.js:1150`
- Doc: Build a clusters[] summary from a flat node list (used after a merge when the server-side clusters array isn't carried a
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### hideTooltip
- Defined: `static/js/estorides.js:1163`
- Doc: --- floating overlays (tooltip + context menu) ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### sanitizeHTML
- Defined: `static/js/estorides.js:1167`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showTooltipAt
- Defined: `static/js/estorides.js:1182`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### hideContextMenu
- Defined: `static/js/estorides.js:1193`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showBridgeTooltip
- Defined: `static/js/estorides.js:1199`
- Doc: Cross-referenced tooltip for an inter-cluster (bridge) link.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showNodeTooltip
- Defined: `static/js/estorides.js:1228`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showContextMenu
- Defined: `static/js/estorides.js:1247`
- Doc: --- context menu: transforms grouped by intel tier ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### setNodeLevel
- Defined: `static/js/estorides.js:1317`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### applyLevelStyles
- Defined: `static/js/estorides.js:1326`
- Doc: Re-apply level rings to every rendered node circle.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### focusNode
- Defined: `static/js/estorides.js:1334`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### runTransform
- Defined: `static/js/estorides.js:1346`
- Doc: Run a graph pivot transform and merge the result into the graph+map.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### selectNode
- Defined: `static/js/estorides.js:1364`
- Doc: --- side inspector panel ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### add
- Defined: `static/js/estorides.js:1375`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### addText
- Defined: `static/js/estorides.js:1381`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderGraphCore
- Defined: `static/js/estorides.js:1455`
- Doc: --- unified force-graph renderer (clusters + rings + interactions) ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### drawHulls
- Defined: `static/js/estorides.js:1525`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### _redrawGraph
- Defined: `static/js/estorides.js:1556`
- Doc: Low-level D3 redraw given a flat nodes/links list (back-compat shim).
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### setStatusDot
- Defined: `static/js/estorides.js:1562`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showWorkingIndicator
- Defined: `static/js/estorides.js:1568`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### hideWorkingIndicator
- Defined: `static/js/estorides.js:1573`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### toggleTierSection
- Defined: `static/js/estorides.js:1578`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderTieredResults
- Defined: `static/js/estorides.js:1586`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### escapeAttr
- Defined: `static/js/estorides.js:1652`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### buildMapCoords
- Defined: `static/js/estorides.js:1688`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### validCoord
- Defined: `static/js/estorides.js:1784`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### colorFor
- Defined: `static/js/estorides.js:1788`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderEntities
- Defined: `static/js/estorides.js:1807`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderGraphSummary
- Defined: `static/js/estorides.js:1857`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### colorForKind
- Defined: `static/js/estorides.js:1886`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderTimeline
- Defined: `static/js/estorides.js:1894`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### fmtTime
- Defined: `static/js/estorides.js:1944`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### filterTimeline
- Defined: `static/js/estorides.js:1955`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### drawGraph
- Defined: `static/js/estorides.js:2004`
- Doc: --- D3 graph view ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadCases
- Defined: `static/js/estorides.js:2035`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### openCaseDetail
- Defined: `static/js/estorides.js:2061`
- Doc: Rich case modal: loads the saved DB record (query, entities, observations) and offers Analyse (re-run on the case data) 
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### restoreCaseToWorkspace
- Defined: `static/js/estorides.js:2116`
- Doc: Restore a case's saved entities into the workspace tabs (entities list, graph summary, map, timeline) without re-running
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### buildCaseMapCoords
- Defined: `static/js/estorides.js:2137`
- Doc: Build map coords from a case's saved entities, reusing the same latitude/longitude resolution and country-centroid fallb
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderCaseItem
- Defined: `static/js/estorides.js:2155`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### debounce
- Defined: `static/js/estorides.js:2181`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### escapeHTML
- Defined: `static/js/estorides.js:2231`
- Doc: --- utils ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### truncate
- Defined: `static/js/estorides.js:2236`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### caseActionSave
- Defined: `static/js/estorides.js:2259`
- Doc: Bookmark a case. The endpoint prefixes the notes column with "[saved]" so the bookmarked case surfaces in the list at a 
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### caseActionDiff
- Defined: `static/js/estorides.js:2280`
- Doc: Compare this case to another. The user picks the baseline; the response is rendered inline in a diff panel under the cas
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### renderCaseDiffPanel
- Defined: `static/js/estorides.js:2300`
- Doc: Render the diff result below the case. The panel survives until the user reloads the cases list (or opens another diff).
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### caseActionReport
- Defined: `static/js/estorides.js:2341`
- Doc: Render the Markdown report. We just dump the text into a modal overlay — keeping it in-browser is enough; the CLI comman
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### showReportModal
- Defined: `static/js/estorides.js:2377`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### _sanitizeInput
- Defined: `static/js/estorides.js:2402`
- Doc: --- generic modal helpers (replace alert/prompt/confirm) ---- User input collected here is treated as hostile: coerced t
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### openModal
- Defined: `static/js/estorides.js:2405`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### promptModal
- Defined: `static/js/estorides.js:2440`
- Doc: Promise-style text prompt. Resolves with a sanitized string or null.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### confirmModal
- Defined: `static/js/estorides.js:2464`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadSidebarWidth
- Defined: `static/js/estorides.js:2556`
- Doc: Responsive sidebar toggle + resizable divider.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### saveSidebarWidth
- Defined: `static/js/estorides.js:2567`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadSidebarCollapsed
- Defined: `static/js/estorides.js:2570`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### saveSidebarCollapsed
- Defined: `static/js/estorides.js:2578`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### switchSidebarTab
- Defined: `static/js/estorides.js:2636`
- Doc: --- Fusion tab ----
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadFusionTab
- Defined: `static/js/estorides.js:2649`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadFusionStats
- Defined: `static/js/estorides.js:2655`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadFusionTopChanged
- Defined: `static/js/estorides.js:2674`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadFusionSearch
- Defined: `static/js/estorides.js:2703`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### doSearch
- Defined: `static/js/estorides.js:2710`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### loadFusionEntityDetail
- Defined: `static/js/estorides.js:2748`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### _sseUrl
- Defined: `static/js/estorides.js:2811`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### setStatus
- Defined: `static/js/estorides.js:2835`
- Doc: The discoverer code lives outside the IIFE, so the module-private setStatus is not in scope here. Provide a global one t
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### setDiscoverProgress
- Defined: `static/js/estorides.js:2842`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### hideDiscoverProgress
- Defined: `static/js/estorides.js:2854`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### startDiscover
- Defined: `static/js/estorides.js:2859`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### stopDiscover
- Defined: `static/js/estorides.js:2933`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### handleDiscoverEvent
- Defined: `static/js/estorides.js:2950`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### addDiscoverEntityToTab
- Defined: `static/js/estorides.js:2989`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### escapeHtml
- Defined: `static/js/estorides.js:3017`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### maybePlotDiscoverEntity
- Defined: `static/js/estorides.js:3022`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### flushDiscoverEntities
- Defined: `static/js/estorides.js:3029`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### check
- Defined: `static/js/estorides.js:3048`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### set
- Defined: `static/js/estorides.js:21`
- Doc: Headers may be a Headers instance, an object, or absent.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### TELEMETRY
- Defined: `static/js/estorides.js:30`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### toolBinary
- Defined: `static/js/estorides.js:131`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### status
- Defined: `static/js/estorides.js:137`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### out
- Defined: `static/js/estorides.js:235`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### text
- Defined: `static/js/estorides.js:249`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### cat
- Defined: `static/js/estorides.js:250`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### status
- Defined: `static/js/estorides.js:251`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### sig
- Defined: `static/js/estorides.js:659`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### boxQ
- Defined: `static/js/estorides.js:857`
- Doc: The target being assessed = the current query box (if the user typed something) else the last completed run.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### scheduleRender
- Defined: `static/js/estorides.js:881`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### flush
- Defined: `static/js/estorides.js:886`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### pump
- Defined: `static/js/estorides.js:907`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### k
- Defined: `static/js/estorides.js:1002`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### CLUSTER_PALETTE
- Defined: `static/js/estorides.js:1100`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### c
- Defined: `static/js/estorides.js:1133`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### cid
- Defined: `static/js/estorides.js:1153`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### labelFor
- Defined: `static/js/estorides.js:1202`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### c
- Defined: `static/js/estorides.js:1203`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### tr
- Defined: `static/js/estorides.js:1297`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### tr
- Defined: `static/js/estorides.js:1432`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### obs
- Defined: `static/js/estorides.js:1898`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### frac
- Defined: `static/js/estorides.js:1931`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### q
- Defined: `static/js/estorides.js:2036`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### entities
- Defined: `static/js/estorides.js:2062`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### obs
- Defined: `static/js/estorides.js:2063`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### saved
- Defined: `static/js/estorides.js:2159`
- Doc: Saved cases get a visible bookmark pill so the operator can scan the list for "things I came back to" at a glance.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### rows
- Defined: `static/js/estorides.js:2308`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### removed
- Defined: `static/js/estorides.js:2311`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### actions
- Defined: `static/js/estorides.js:2411`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### close
- Defined: `static/js/estorides.js:2425`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### tag
- Defined: `static/js/estorides.js:2526`
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### _sseAuthToken
- Defined: `static/js/estorides.js:2807`
- Doc: Auth token for SSE (EventSource can't set custom headers).
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

### sig
- Defined: `static/js/estorides.js:2994`
- Doc: Avoid duplicates with the simple in-memory check.
- Depends on: `estorides_core/discoverer.py`, `estorides_export/report.py`

## static/js/source_manager.js

### authHeaders
- Defined: `static/js/source_manager.js:7`
- Doc: /* Estorides Source Manager — form-based YAML editor (function () { 'use strict'; /* ─── auth ───

### apiFetch
- Defined: `static/js/source_manager.js:15`

### getCheckedTags
- Defined: `static/js/source_manager.js:67`
- Doc: contact: $('field-contact'), logsQueries: $('field-logs-queries'), toolUrl: $('field-tool-url'), toolMethod: $('field-to

### setCheckedTags
- Defined: `static/js/source_manager.js:74`

### readForm
- Defined: `static/js/source_manager.js:84`
- Doc: var checks = container.querySelectorAll('input[type="checkbox"]:checked'); return Array.from(checks).map(function (c) { 

### writeForm
- Defined: `static/js/source_manager.js:120`
- Doc: try { var b = JSON.parse(fields.toolBody.value.trim() || '{}'); if (Object.keys(b).length) s.tool.body = b; } catch (e) 

### updateYamlPreview
- Defined: `static/js/source_manager.js:183`
- Doc: fields.pagCursorPath.value = pag.cursor_path || ''; setCheckedTags('field-applies-to', s.applies_to); setCheckedTags('fi

### renderList
- Defined: `static/js/source_manager.js:193`
- Doc: updateYamlPreview(); } /* ─── update YAML preview ─── function updateYamlPreview() { try { var s = readForm(); yamlPrevi

### escHtml
- Defined: `static/js/source_manager.js:223`
- Doc: var keyBadge = s.requires_key ? '<span class="src-item-key-badge">key</span>' : ''; var sysBadge = s.kind === 'system_ap

### escAttr
- Defined: `static/js/source_manager.js:224`

### toast
- Defined: `static/js/source_manager.js:227`
- Doc: '<div class="src-item-info">' + '<div class="src-item-name">' + escHtml(s.name) + sysBadge + keyBadge + '</div>' + '<div

### loadSources
- Defined: `static/js/source_manager.js:236`
- Doc: /* ─── helpers ─── function escHtml(s) { return String(s).replace(/[&<>"]/g, function (m) { return ({ '&': '&amp;', '<':

### clearEditor
- Defined: `static/js/source_manager.js:251`
- Doc: apiFetch('/api/sources/yaml').then(function (data) { sources = data.sources || []; srcCount.textContent = data.total + '

### selectSource
- Defined: `static/js/source_manager.js:261`
- Doc: }); } /* ─── clear editor ─── function clearEditor() { form.hidden = true; editorEmpty.hidden = false; writeForm(null); 

### saveSource
- Defined: `static/js/source_manager.js:273`
- Doc: /* ─── select source ─── function selectSource(name) { var s = sources.filter(function (s) { return s.name === name; })[

### deleteSource
- Defined: `static/js/source_manager.js:304`
- Doc: toast('Source "' + data.name + '" saved', 'ok'); formStatus.textContent = 'Saved'; formStatus.className = 'form-status o

### newSource
- Defined: `static/js/source_manager.js:334`
- Doc: overlay.remove(); apiFetch('/api/sources/yaml/' + encodeURIComponent(currentName), { method: 'DELETE' }).then(function (

## tests/properties/test_change_detection_properties.py

### test_scores_always_bounded `def test_scores_always_bounded(before, after)`
- Defined: `tests/properties/test_change_detection_properties.py:69`
- Depends on: `estorides_core/change_detection.py`

### test_max_changes_respected `def test_max_changes_respected(before, after)`
- Defined: `tests/properties/test_change_detection_properties.py:77`
- Depends on: `estorides_core/change_detection.py`

### test_id_is_16_char_hex `def test_id_is_16_char_hex(before, after)`
- Defined: `tests/properties/test_change_detection_properties.py:86`
- Depends on: `estorides_core/change_detection.py`

### test_idempotent `def test_idempotent(before, after)`
- Defined: `tests/properties/test_change_detection_properties.py:95`
- Depends on: `estorides_core/change_detection.py`

### test_first_run_reports_all_as_new `def test_first_run_reports_all_as_new(after)`
- Defined: `tests/properties/test_change_detection_properties.py:105`
- Depends on: `estorides_core/change_detection.py`

### test_after_none_returns_empty `def test_after_none_returns_empty(before)`
- Defined: `tests/properties/test_change_detection_properties.py:113`
- Depends on: `estorides_core/change_detection.py`

### test_before_vs_no_after_empty `def test_before_vs_no_after_empty(entities)`
- Defined: `tests/properties/test_change_detection_properties.py:121`
- Depends on: `estorides_core/change_detection.py`

### test_summary_consistency `def test_summary_consistency(before, after)`
- Defined: `tests/properties/test_change_detection_properties.py:132`
- Doc: Whatever the input, the summary fields must agree with the
- Depends on: `estorides_core/change_detection.py`

## tests/properties/test_csp_safe_styles_properties.py

### test_js_never_gains_a_style_attribute_in_template_literal `def test_js_never_gains_a_style_attribute_in_template_literal(insertion)`
- Defined: `tests/properties/test_csp_safe_styles_properties.py:58`
- Doc: Hypothetical: a future patch appends the given string somewhere
- Depends on: `estorides_core/web_security.py`

### test_template_never_gains_a_style_attribute `def test_template_never_gains_a_style_attribute(insertion)`
- Defined: `tests/properties/test_csp_safe_styles_properties.py:105`
- Doc: Hypothetical: a future patch adds the given string somewhere in
- Depends on: `estorides_core/web_security.py`

### test_csp_style_src_never_gains_unsafe_inline `def test_csp_style_src_never_gains_unsafe_inline(bad)`
- Defined: `tests/properties/test_csp_safe_styles_properties.py:137`
- Doc: Hypothetical: a future patch sets `style-src` to
- Depends on: `estorides_core/web_security.py`

## tests/properties/test_hypothesis_engine_properties.py

### test_scores_always_bounded `def test_scores_always_bounded(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:54`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_claim_length_under_cap `def test_claim_length_under_cap(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:66`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_reasoning_length_under_cap `def test_reasoning_length_under_cap(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:77`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_sources_sorted_unique `def test_sources_sorted_unique(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:88`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_id_is_deterministic_hex `def test_id_is_deterministic_hex(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:99`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_idempotent `def test_idempotent(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:112`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_max_hypotheses_caps_output `def test_max_hypotheses_caps_output(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:123`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_min_score_filters `def test_min_score_filters(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:134`
- Depends on: `estorides_core/hypothesis_engine.py`

### test_hostile_observation_does_not_crash `def test_hostile_observation_does_not_crash(observations, entities)`
- Defined: `tests/properties/test_hypothesis_engine_properties.py:147`
- Depends on: `estorides_core/hypothesis_engine.py`

## tests/properties/test_observation_models_properties.py

### meta_strategy `def meta_strategy(draw)`
- Defined: `tests/properties/test_observation_models_properties.py:45`
- Depends on: `estorides_core/observation_models.py`

### obs_strategy `def obs_strategy(draw)`
- Defined: `tests/properties/test_observation_models_properties.py:60`
- Depends on: `estorides_core/observation_models.py`

### entity_strategy `def entity_strategy(draw)`
- Defined: `tests/properties/test_observation_models_properties.py:76`
- Depends on: `estorides_core/observation_models.py`

### test_observation_round_trip_stability `def test_observation_round_trip_stability(payload)`
- Defined: `tests/properties/test_observation_models_properties.py:90`
- Depends on: `estorides_core/observation_models.py`

### test_observation_bounded_fields `def test_observation_bounded_fields(payload)`
- Defined: `tests/properties/test_observation_models_properties.py:103`
- Depends on: `estorides_core/observation_models.py`

### test_entity_round_trip_and_bounds `def test_entity_round_trip_and_bounds(payload)`
- Defined: `tests/properties/test_observation_models_properties.py:115`
- Depends on: `estorides_core/observation_models.py`

### test_meta_never_echoes_unbounded_url `def test_meta_never_echoes_unbounded_url(metas)`
- Defined: `tests/properties/test_observation_models_properties.py:128`
- Depends on: `estorides_core/observation_models.py`

## tests/properties/test_recon_fusion_properties.py

### test_all_scores_in_unit_interval `def test_all_scores_in_unit_interval(self, query, query_type, observations, entities)`
- Defined: `tests/properties/test_recon_fusion_properties.py:58`
- Depends on: `estorides_core/recon_fusion.py`

### test_counts_match_input `def test_counts_match_input(self, query, query_type, n_obs, n_ents)`
- Defined: `tests/properties/test_recon_fusion_properties.py:78`
- Depends on: `estorides_core/recon_fusion.py`

### test_tier_summary_matches `def test_tier_summary_matches(self, query, query_type, observations, entities)`
- Defined: `tests/properties/test_recon_fusion_properties.py:103`
- Depends on: `estorides_core/recon_fusion.py`

### test_deterministic_output `def test_deterministic_output(self, query, query_type, observations, entities)`
- Defined: `tests/properties/test_recon_fusion_properties.py:124`
- Depends on: `estorides_core/recon_fusion.py`

### test_no_duplicate_ids_in_tier `def test_no_duplicate_ids_in_tier(self, query, query_type, observations, entities)`
- Defined: `tests/properties/test_recon_fusion_properties.py:145`
- Depends on: `estorides_core/recon_fusion.py`

### test_tier_keys_in_canonical_order `def test_tier_keys_in_canonical_order(self, query, query_type, observations, entities)`
- Defined: `tests/properties/test_recon_fusion_properties.py:165`
- Depends on: `estorides_core/recon_fusion.py`

### test_empty_query_raises `def test_empty_query_raises(self, query_type, observations, entities)`
- Defined: `tests/properties/test_recon_fusion_properties.py:185`
- Depends on: `estorides_core/recon_fusion.py`

### test_none_inputs_safe `def test_none_inputs_safe(self, query, query_type)`
- Defined: `tests/properties/test_recon_fusion_properties.py:201`
- Depends on: `estorides_core/recon_fusion.py`

### test_entities_none_is_safe `def test_entities_none_is_safe(self, query, query_type, observations)`
- Defined: `tests/properties/test_recon_fusion_properties.py:214`
- Depends on: `estorides_core/recon_fusion.py`

## tests/properties/test_reliability_scoring_properties.py

### test_score_always_bounded `def test_score_always_bounded(reliability, credibility, corroboration, age, base, half_life)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:56`
- Depends on: `estorides_core/reliability_scoring.py`

### test_corroboration_weight_in_unit_interval `def test_corroboration_weight_in_unit_interval(n)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:73`
- Depends on: `estorides_core/reliability_scoring.py`

### test_freshness_monotone_in_age `def test_freshness_monotone_in_age(age1, age2)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:87`
- Depends on: `estorides_core/reliability_scoring.py`

### test_reliability_from_name_never_raises `def test_reliability_from_name_never_raises(name)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:110`
- Depends on: `estorides_core/reliability_scoring.py`

### test_merge_confidence_bounded `def test_merge_confidence_bounded(existing, new_obs, new_rel, new_cred, cor, age)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:126`
- Depends on: `estorides_core/reliability_scoring.py`

### test_reliability_weight_set_is_curated `def test_reliability_weight_set_is_curated()`
- Defined: `tests/properties/test_reliability_scoring_properties.py:141`
- Depends on: `estorides_core/reliability_scoring.py`

### test_credibility_weight_set_is_curated `def test_credibility_weight_set_is_curated()`
- Defined: `tests/properties/test_reliability_scoring_properties.py:146`
- Depends on: `estorides_core/reliability_scoring.py`

### test_corroboration_is_monotone_in_count `def test_corroboration_is_monotone_in_count(n1, n2)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:159`
- Depends on: `estorides_core/reliability_scoring.py`

### test_higher_reliability_dominates `def test_higher_reliability_dominates(rel1, rel2)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:184`
- Depends on: `estorides_core/reliability_scoring.py`

### test_source_type_from_name_never_raises `def test_source_type_from_name_never_raises(name)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:202`
- Depends on: `estorides_core/reliability_scoring.py`

### test_source_type_weight_always_curated `def test_source_type_weight_always_curated(reliability, credibility, source_type, corroboration, age, base, half_life)`
- Defined: `tests/properties/test_reliability_scoring_properties.py:219`
- Depends on: `estorides_core/reliability_scoring.py`

### test_source_type_weight_set_is_curated `def test_source_type_weight_set_is_curated()`
- Defined: `tests/properties/test_reliability_scoring_properties.py:241`
- Depends on: `estorides_core/reliability_scoring.py`

## tests/properties/test_search_telemetry_properties.py

### test_progress_invariants_hold `def test_progress_invariants_hold(completed, total, phase_key)`
- Defined: `tests/properties/test_search_telemetry_properties.py:32`
- Depends on: `estorides_core/search_telemetry.py`

### test_progress_rejects_unknown_phase `def test_progress_rejects_unknown_phase(phase_key)`
- Defined: `tests/properties/test_search_telemetry_properties.py:46`
- Depends on: `estorides_core/search_telemetry.py`

### test_brand_predicate_is_total `def test_brand_predicate_is_total(text)`
- Defined: `tests/properties/test_search_telemetry_properties.py:56`
- Depends on: `estorides_core/search_telemetry.py`

### test_emoji_predicate_is_total `def test_emoji_predicate_is_total(text)`
- Defined: `tests/properties/test_search_telemetry_properties.py:65`
- Depends on: `estorides_core/search_telemetry.py`

### test_percent_encoded_emoji_predicate_is_total `def test_percent_encoded_emoji_predicate_is_total(text)`
- Defined: `tests/properties/test_search_telemetry_properties.py:74`
- Depends on: `estorides_core/search_telemetry.py`

### test_brand_predicate_flags_embedded_brand `def test_brand_predicate_flags_embedded_brand(prefix, suffix)`
- Defined: `tests/properties/test_search_telemetry_properties.py:84`
- Depends on: `estorides_core/search_telemetry.py`

## tests/properties/test_source_health_monitoring_properties.py

### _valid_input `def _valid_input(fetch, ok, latency, last_seen, now)`
- Defined: `tests/properties/test_source_health_monitoring_properties.py:21`
- Doc: Build a valid SourceHealthInput, clamping ok <= fetch.
- Depends on: `estorides_core/source_health_monitoring.py`

### test_health_score_always_bounded `def test_health_score_always_bounded(fetch, ok, latency, last_seen, now)`
- Defined: `tests/properties/test_source_health_monitoring_properties.py:49`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_status_always_valid_enum `def test_status_always_valid_enum(fetch, ok, latency, last_seen, now)`
- Defined: `tests/properties/test_source_health_monitoring_properties.py:63`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_success_rate_bounds `def test_success_rate_bounds(fetch, ok, latency, last_seen, now)`
- Defined: `tests/properties/test_source_health_monitoring_properties.py:78`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_unknown_when_below_min_fetches `def test_unknown_when_below_min_fetches(fetch, config_min)`
- Defined: `tests/properties/test_source_health_monitoring_properties.py:89`
- Depends on: `estorides_core/source_health_monitoring.py`

### valid_health_inputs `def valid_health_inputs(draw)`
- Defined: `tests/properties/test_source_health_monitoring_properties.py:97`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_dashboard_summary_counts_match `def test_dashboard_summary_counts_match(records)`
- Defined: `tests/properties/test_source_health_monitoring_properties.py:112`
- Doc: Dashboard summary counts must sum to total.
- Depends on: `estorides_core/source_health_monitoring.py`

## tests/properties/test_system_app_sources_properties.py

### test_tool_parsers_never_raise `def test_tool_parsers_never_raise(parser_name, blob)`
- Defined: `tests/properties/test_system_app_sources_properties.py:37`
- Depends on: `estorides_core/parsers.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_render_args_safe_inputs_no_metachars `def test_render_args_safe_inputs_no_metachars(args, query, outdir)`
- Defined: `tests/properties/test_system_app_sources_properties.py:55`
- Depends on: `estorides_core/parsers.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_render_args_substitution_is_verbatim `def test_render_args_substitution_is_verbatim(query, outdir)`
- Defined: `tests/properties/test_system_app_sources_properties.py:70`
- Depends on: `estorides_core/parsers.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_read_capped_respects_limit `def test_read_capped_respects_limit(blob, cap)`
- Defined: `tests/properties/test_system_app_sources_properties.py:83`
- Depends on: `estorides_core/parsers.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_parse_tool_output_never_raises `def test_parse_tool_output_never_raises(parser_name, data)`
- Defined: `tests/properties/test_system_app_sources_properties.py:110`
- Depends on: `estorides_core/parsers.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_adversarial_query_rejected_at_runner_boundary `def test_adversarial_query_rejected_at_runner_boundary(prefix, bad, suffix)`
- Defined: `tests/properties/test_system_app_sources_properties.py:124`
- Depends on: `estorides_core/parsers.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

## tests/properties/test_target_management_properties.py

### test_p1_add_target_never_raises `def test_p1_add_target_never_raises(etype, value)`
- Defined: `tests/properties/test_target_management_properties.py:21`

### test_p2_validated_id_is_deterministic `def test_p2_validated_id_is_deterministic(etype, value)`
- Defined: `tests/properties/test_target_management_properties.py:31`

### test_p3_make_target_id_stable_under_case `def test_p3_make_target_id_stable_under_case(etype, value)`
- Defined: `tests/properties/test_target_management_properties.py:40`

### test_p4_valid_domains_validate `def test_p4_valid_domains_validate(d)`
- Defined: `tests/properties/test_target_management_properties.py:56`

### test_p5_valid_ipv4_validate `def test_p5_valid_ipv4_validate(ip)`
- Defined: `tests/properties/test_target_management_properties.py:68`

### test_p6_valid_emails_validate `def test_p6_valid_emails_validate(email)`
- Defined: `tests/properties/test_target_management_properties.py:77`

### test_p7_auto_detect_never_fails `def test_p7_auto_detect_never_fails(value)`
- Defined: `tests/properties/test_target_management_properties.py:83`

### test_p8_validate_target_never_raises `def test_p8_validate_target_never_raises(value)`
- Defined: `tests/properties/test_target_management_properties.py:89`

### test_p9_batch_import_idempotent `def test_p9_batch_import_idempotent(targets)`
- Defined: `tests/properties/test_target_management_properties.py:105`

### test_p10_batch_import_never_raises `def test_p10_batch_import_never_raises(text)`
- Defined: `tests/properties/test_target_management_properties.py:116`

## tests/properties/test_tool_runner_properties.py

### test_check_injection_safe_strings_silent `def test_check_injection_safe_strings_silent(args)`
- Defined: `tests/properties/test_tool_runner_properties.py:35`
- Depends on: `estorides_core/tool_runner.py`

### test_check_injection_detects_all_metacharacters `def test_check_injection_detects_all_metacharacters(prefix, bad, suffix)`
- Defined: `tests/properties/test_tool_runner_properties.py:46`
- Depends on: `estorides_core/tool_runner.py`

### test_run_tool_never_raises `def test_run_tool_never_raises(target)`
- Defined: `tests/properties/test_tool_runner_properties.py:63`
- Depends on: `estorides_core/tool_runner.py`

## tests/test_active_recon.py

### test_run_nmap_returns_result `def test_run_nmap_returns_result(self)`
- Defined: `tests/test_active_recon.py:25`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_nmap_result_has_to_dict `def test_nmap_result_has_to_dict(self)`
- Defined: `tests/test_active_recon.py:29`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_nmap_result_to_entities_is_list `def test_nmap_result_to_entities_is_list(self)`
- Defined: `tests/test_active_recon.py:38`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_run_nikto_returns_result `def test_run_nikto_returns_result(self)`
- Defined: `tests/test_active_recon.py:46`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_nikto_result_has_to_dict `def test_nikto_result_has_to_dict(self)`
- Defined: `tests/test_active_recon.py:50`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_run_sqlmap_returns_result `def test_run_sqlmap_returns_result(self)`
- Defined: `tests/test_active_recon.py:59`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_sqlmap_result_has_to_dict `def test_sqlmap_result_has_to_dict(self)`
- Defined: `tests/test_active_recon.py:63`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_run_dnsrecon_returns_result `def test_run_dnsrecon_returns_result(self)`
- Defined: `tests/test_active_recon.py:72`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_dnsrecon_result_has_to_dict `def test_dnsrecon_result_has_to_dict(self)`
- Defined: `tests/test_active_recon.py:76`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_run_theHarvester_returns_result `def test_run_theHarvester_returns_result(self)`
- Defined: `tests/test_active_recon.py:85`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_harvester_result_has_to_dict `def test_harvester_result_has_to_dict(self)`
- Defined: `tests/test_active_recon.py:89`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_nmap_result_is_dataclass `def test_nmap_result_is_dataclass(self)`
- Defined: `tests/test_active_recon.py:98`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_nikto_result_is_dataclass `def test_nikto_result_is_dataclass(self)`
- Defined: `tests/test_active_recon.py:106`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_sqlmap_result_is_dataclass `def test_sqlmap_result_is_dataclass(self)`
- Defined: `tests/test_active_recon.py:113`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_dnsrecon_result_is_dataclass `def test_dnsrecon_result_is_dataclass(self)`
- Defined: `tests/test_active_recon.py:120`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_harvester_result_is_dataclass `def test_harvester_result_is_dataclass(self)`
- Defined: `tests/test_active_recon.py:127`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

### test_nmap_error_result_has_empty_entities `def test_nmap_error_result_has_empty_entities(self)`
- Defined: `tests/test_active_recon.py:136`
- Depends on: `estorides_core/active_recon.py`, `estorides_core/tool_runner.py`

## tests/test_audit_log.py

### _ev `def _ev(ts)`
- Defined: `tests/test_audit_log.py:12`
- Depends on: `estorides_core/audit.py`

### test_audit_log_appends `def test_audit_log_appends(tmp_path)`
- Defined: `tests/test_audit_log.py:22`
- Depends on: `estorides_core/audit.py`

### test_audit_log_rotates_when_cap_exceeded `def test_audit_log_rotates_when_cap_exceeded(tmp_path)`
- Defined: `tests/test_audit_log.py:31`
- Depends on: `estorides_core/audit.py`

### test_audit_log_rotation_respects_keep_count `def test_audit_log_rotation_respects_keep_count(tmp_path)`
- Defined: `tests/test_audit_log.py:48`
- Depends on: `estorides_core/audit.py`

### test_audit_log_no_rotation_when_disabled `def test_audit_log_no_rotation_when_disabled(tmp_path)`
- Defined: `tests/test_audit_log.py:61`
- Depends on: `estorides_core/audit.py`

## tests/test_auth_gate.py

### app_with_gate `def app_with_gate(monkeypatch)`
- Defined: `tests/test_auth_gate.py:22`
- Doc: A Flask app with the auth gate enabled, token 'sek'.
- Depends on: `estorides_core/web_security.py`

### test_gate_auto_generates_token_when_unset `def test_gate_auto_generates_token_when_unset(monkeypatch)`
- Defined: `tests/test_auth_gate.py:41`
- Depends on: `estorides_core/web_security.py`

### test_gate_on_rejects_anonymous `def test_gate_on_rejects_anonymous(app_with_gate)`
- Defined: `tests/test_auth_gate.py:53`
- Depends on: `estorides_core/web_security.py`

### test_gate_on_accepts_bearer_header `def test_gate_on_accepts_bearer_header(app_with_gate)`
- Defined: `tests/test_auth_gate.py:61`
- Depends on: `estorides_core/web_security.py`

### test_gate_on_accepts_alt_header `def test_gate_on_accepts_alt_header(app_with_gate)`
- Defined: `tests/test_auth_gate.py:68`
- Depends on: `estorides_core/web_security.py`

### test_gate_on_accepts_cookie `def test_gate_on_accepts_cookie(app_with_gate)`
- Defined: `tests/test_auth_gate.py:74`
- Depends on: `estorides_core/web_security.py`

### test_gate_on_rejects_wrong_token `def test_gate_on_rejects_wrong_token(app_with_gate)`
- Defined: `tests/test_auth_gate.py:81`
- Depends on: `estorides_core/web_security.py`

### test_gate_on_auto_generated_token_in_meta `def test_gate_on_auto_generated_token_in_meta(monkeypatch)`
- Defined: `tests/test_auth_gate.py:87`
- Depends on: `estorides_core/web_security.py`

### test_gate_on_exposes_token_for_index_meta `def test_gate_on_exposes_token_for_index_meta()`
- Defined: `tests/test_auth_gate.py:95`
- Depends on: `estorides_core/web_security.py`

### private `def private()`
- Defined: `tests/test_auth_gate.py:34`
- Depends on: `estorides_core/web_security.py`

## tests/test_change_detection.py

### _entity `def _entity(eid, etype, value)`
- Defined: `tests/test_change_detection.py:28`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_one_new_entity_emits_one_new_change `def test_one_new_entity_emits_one_new_change(self)`
- Defined: `tests/test_change_detection.py:59`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_new_change_score_in_high_band `def test_new_change_score_in_high_band(self)`
- Defined: `tests/test_change_detection.py:84`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_property_change_emits_one_change `def test_property_change_emits_one_change(self)`
- Defined: `tests/test_change_detection.py:102`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_before_none_reports_all_as_new `def test_before_none_reports_all_as_new(self)`
- Defined: `tests/test_change_detection.py:128`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_after_none_returns_empty_report `def test_after_none_returns_empty_report(self)`
- Defined: `tests/test_change_detection.py:150`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_disappeared_within_grace_is_ignored `def test_disappeared_within_grace_is_ignored(self)`
- Defined: `tests/test_change_detection.py:169`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_disappeared_outside_grace_emits_change `def test_disappeared_outside_grace_emits_change(self)`
- Defined: `tests/test_change_detection.py:181`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_new_source_on_existing_entity_emits_source_added `def test_new_source_on_existing_entity_emits_source_added(self)`
- Defined: `tests/test_change_detection.py:202`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_min_reliability_e_excludes_f_source `def test_min_reliability_e_excludes_f_source(self)`
- Defined: `tests/test_change_detection.py:229`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_max_changes_caps_output `def test_max_changes_caps_output(self)`
- Defined: `tests/test_change_detection.py:258`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_entity_id_empty_raises `def test_entity_id_empty_raises(self)`
- Defined: `tests/test_change_detection.py:284`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_entity_type_empty_raises `def test_entity_type_empty_raises(self)`
- Defined: `tests/test_change_detection.py:288`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_entity_value_empty_raises `def test_entity_value_empty_raises(self)`
- Defined: `tests/test_change_detection.py:292`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_min_change_score_out_of_range_raises `def test_min_change_score_out_of_range_raises(self)`
- Defined: `tests/test_change_detection.py:296`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_max_changes_too_small_raises `def test_max_changes_too_small_raises(self)`
- Defined: `tests/test_change_detection.py:302`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_hostile_key_does_not_crash `def test_hostile_key_does_not_crash(self, hostile_key)`
- Defined: `tests/test_change_detection.py:322`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_same_input_same_ids_and_scores `def test_same_input_same_ids_and_scores(self)`
- Defined: `tests/test_change_detection.py:349`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_input_order_does_not_affect_output `def test_input_order_does_not_affect_output(self)`
- Defined: `tests/test_change_detection.py:366`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_source_removed_emits_change `def test_source_removed_emits_change(self)`
- Defined: `tests/test_change_detection.py:389`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_source_removed_filtered_by_min_score `def test_source_removed_filtered_by_min_score(self)`
- Defined: `tests/test_change_detection.py:410`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_edge_added_emits_change `def test_edge_added_emits_change(self)`
- Defined: `tests/test_change_detection.py:439`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_edge_removed_emits_change `def test_edge_removed_emits_change(self)`
- Defined: `tests/test_change_detection.py:462`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_large_confidence_shift_emits_change `def test_large_confidence_shift_emits_change(self)`
- Defined: `tests/test_change_detection.py:491`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_small_confidence_shift_ignored `def test_small_confidence_shift_ignored(self)`
- Defined: `tests/test_change_detection.py:509`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_change_is_frozen `def test_change_is_frozen(self)`
- Defined: `tests/test_change_detection.py:531`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_diff_is_frozen `def test_diff_is_frozen(self)`
- Defined: `tests/test_change_detection.py:541`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

### test_change_report_is_frozen `def test_change_report_is_frozen(self)`
- Defined: `tests/test_change_detection.py:546`
- Depends on: `estorides_core/change_detection.py`, `estorides_core/reliability_scoring.py`

## tests/test_cloud_asset_discovery.py

### _make_asset `def _make_asset(provider, url, accessible, listing)`
- Defined: `tests/test_cloud_asset_discovery.py:16`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_accessible_bucket_returned `def test_accessible_bucket_returned(self)`
- Defined: `tests/test_cloud_asset_discovery.py:28`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_listing_bucket_has_files `def test_listing_bucket_has_files(self)`
- Defined: `tests/test_cloud_asset_discovery.py:41`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_empty_when_no_cloud_assets `def test_empty_when_no_cloud_assets(self)`
- Defined: `tests/test_cloud_asset_discovery.py:59`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_assess_bucket_uses_get_only `def test_assess_bucket_uses_get_only(self)`
- Defined: `tests/test_cloud_asset_discovery.py:69`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_cloudfront_cname_detected `def test_cloudfront_cname_detected(self)`
- Defined: `tests/test_cloud_asset_discovery.py:78`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_firebase_accessible `def test_firebase_accessible(self)`
- Defined: `tests/test_cloud_asset_discovery.py:91`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_generates_common_permutations `def test_generates_common_permutations(self)`
- Defined: `tests/test_cloud_asset_discovery.py:104`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_strips_tld_for_permutations `def test_strips_tld_for_permutations(self)`
- Defined: `tests/test_cloud_asset_discovery.py:114`
- Depends on: `estorides_core/cloud_asset_discovery.py`

### test_rate_limit_constant_defined `def test_rate_limit_constant_defined(self)`
- Defined: `tests/test_cloud_asset_discovery.py:128`
- Depends on: `estorides_core/cloud_asset_discovery.py`

## tests/test_code_exposure.py

### test_detects_aws_key_as_critical `def test_detects_aws_key_as_critical(self)`
- Defined: `tests/test_code_exposure.py:18`
- Depends on: `estorides_core/code_exposure.py`

### test_validates_aws_key_format `def test_validates_aws_key_format(self)`
- Defined: `tests/test_code_exposure.py:32`
- Depends on: `estorides_core/code_exposure.py`

### test_empty_when_no_repos `def test_empty_when_no_repos(self)`
- Defined: `tests/test_code_exposure.py:39`
- Depends on: `estorides_core/code_exposure.py`

### test_returns_partial_on_rate_limit `def test_returns_partial_on_rate_limit(self)`
- Defined: `tests/test_code_exposure.py:48`
- Depends on: `estorides_core/code_exposure.py`

### test_internal_url_is_high_severity `def test_internal_url_is_high_severity(self)`
- Defined: `tests/test_code_exposure.py:55`
- Depends on: `estorides_core/code_exposure.py`

### test_env_file_is_critical_config `def test_env_file_is_critical_config(self)`
- Defined: `tests/test_code_exposure.py:63`
- Depends on: `estorides_core/code_exposure.py`

### test_placeholder_marked_info `def test_placeholder_marked_info(self)`
- Defined: `tests/test_code_exposure.py:71`
- Depends on: `estorides_core/code_exposure.py`

### test_example_key_marked_info `def test_example_key_marked_info(self)`
- Defined: `tests/test_code_exposure.py:75`
- Depends on: `estorides_core/code_exposure.py`

### test_aggregates_multi_source `def test_aggregates_multi_source(self)`
- Defined: `tests/test_code_exposure.py:82`
- Depends on: `estorides_core/code_exposure.py`

### test_snippet_under_200_chars `def test_snippet_under_200_chars(self)`
- Defined: `tests/test_code_exposure.py:96`
- Depends on: `estorides_core/code_exposure.py`

### test_ssh_key_detection `def test_ssh_key_detection(self)`
- Defined: `tests/test_code_exposure.py:104`
- Depends on: `estorides_core/code_exposure.py`

### test_api_key_detection `def test_api_key_detection(self)`
- Defined: `tests/test_code_exposure.py:109`
- Depends on: `estorides_core/code_exposure.py`

## tests/test_csp_safe_styles.py

### _strip_template_jinja `def _strip_template_jinja(template_text)`
- Defined: `tests/test_csp_safe_styles.py:41`
- Doc: Replace `{{ ... }}` and `{% ... %}` with empty so the file is grep-able.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### _strip_js_comments_and_strings_outside_templates `def _strip_js_comments_and_strings_outside_templates(js_text)`
- Defined: `tests/test_csp_safe_styles.py:55`
- Doc: Return the *template-literal contents* of the JS file as a single string.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_index_html_has_no_style_attribute `def test_index_html_has_no_style_attribute()`
- Defined: `tests/test_csp_safe_styles.py:90`
- Doc: S1 — `style="..."` must not appear anywhere in the rendered template.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_estorides_js_has_no_style_in_template_literals `def test_estorides_js_has_no_style_in_template_literals()`
- Defined: `tests/test_csp_safe_styles.py:111`
- Doc: S2 — `style="..."` must not appear in any template literal in the JS.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_offscreen_element_uses_hidden_attribute `def test_offscreen_element_uses_hidden_attribute(element_id)`
- Defined: `tests/test_csp_safe_styles.py:145`
- Doc: S3 — Each offscreen element must have the HTML5 `hidden` attribute.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_css_has_required_class `def test_css_has_required_class(selector)`
- Defined: `tests/test_csp_safe_styles.py:189`
- Doc: The CSS file must define the new classes the refactor relies on.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_csp_policy_does_not_relax_for_unsafe_inline `def test_csp_policy_does_not_relax_for_unsafe_inline()`
- Defined: `tests/test_csp_safe_styles.py:201`
- Doc: S5 — The locked-down CSP must stay locked down.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_csp_policy_is_unchanged_after_refactor `def test_csp_policy_is_unchanged_after_refactor()`
- Defined: `tests/test_csp_safe_styles.py:225`
- Doc: S6 — The default CSP string is byte-identical to the pre-refactor value.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_dynamic_cluster_color_uses_cssom_assignment `def test_dynamic_cluster_color_uses_cssom_assignment()`
- Defined: `tests/test_csp_safe_styles.py:252`
- Doc: S4 — The bridge-tooltip chip must set background via CSSOM.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_dynamic_kind_color_uses_cssom_assignment `def test_dynamic_kind_color_uses_cssom_assignment()`
- Defined: `tests/test_csp_safe_styles.py:272`
- Doc: S4 (kind) — `colorForKind(e.kind)` must reach CSSOM, not innerHTML.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

### test_rendered_template_has_no_style_attribute_and_uses_hidden `def test_rendered_template_has_no_style_attribute_and_uses_hidden()`
- Defined: `tests/test_csp_safe_styles.py:289`
- Doc: End-to-end: render `index.html` and assert no inline styles leak.
- Depends on: `estorides_core/search_telemetry.py`, `estorides_core/web_security.py`

## tests/test_encrypted_export.py

### _kg_with_one_node `def _kg_with_one_node()`
- Defined: `tests/test_encrypted_export.py:27`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

### _patch_age_ok `def _patch_age_ok()`
- Defined: `tests/test_encrypted_export.py:33`
- Doc: Pretend `age` is on PATH and that `age -e -r ...` produced ciphertext.
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

### test_stix_encrypted_removes_plaintext `def test_stix_encrypted_removes_plaintext(tmp_path)`
- Defined: `tests/test_encrypted_export.py:43`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

### test_misp_encrypted_removes_plaintext `def test_misp_encrypted_removes_plaintext(tmp_path)`
- Defined: `tests/test_encrypted_export.py:52`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

### test_stix_encrypted_removes_plaintext_on_failure `def test_stix_encrypted_removes_plaintext_on_failure(tmp_path)`
- Defined: `tests/test_encrypted_export.py:61`
- Doc: Even when age fails, the plaintext must be removed.
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

### __init__ `def __init__(self, rc, stderr)`
- Defined: `tests/test_encrypted_export.py:22`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

### _run `def _run(cmd, stdin, stdout, stderr, check)`
- Defined: `tests/test_encrypted_export.py:35`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

### _run_fail `def _run_fail(cmd, stdin, stdout, stderr, check)`
- Defined: `tests/test_encrypted_export.py:66`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/knowledge_graph.py`, `estorides_export/encryption.py`

## tests/test_entity_resolution.py

### _ent `def _ent(etype, value, source, confidence)`
- Defined: `tests/test_entity_resolution.py:28`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### _by_value `def _by_value(result, value)`
- Defined: `tests/test_entity_resolution.py:32`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_cyrillic_to_latin `def test_cyrillic_to_latin(self)`
- Defined: `tests/test_entity_resolution.py:45`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_greek_accented_to_latin `def test_greek_accented_to_latin(self)`
- Defined: `tests/test_entity_resolution.py:48`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_diacritic_fold `def test_diacritic_fold(self)`
- Defined: `tests/test_entity_resolution.py:51`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_consonant_skeleton_arabic_matches_latin `def test_consonant_skeleton_arabic_matches_latin(self)`
- Defined: `tests/test_entity_resolution.py:54`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_consonant_skeleton_gemination `def test_consonant_skeleton_gemination(self)`
- Defined: `tests/test_entity_resolution.py:57`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_distinct_names_have_distinct_skeletons `def test_distinct_names_have_distinct_skeletons(self)`
- Defined: `tests/test_entity_resolution.py:60`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_non_latin_detector `def test_non_latin_detector(self)`
- Defined: `tests/test_entity_resolution.py:63`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_identical_strings_score_one `def test_identical_strings_score_one(self)`
- Defined: `tests/test_entity_resolution.py:71`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_empty_pair_scores_zero `def test_empty_pair_scores_zero(self)`
- Defined: `tests/test_entity_resolution.py:74`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_classic_jaro_winkler_bound `def test_classic_jaro_winkler_bound(self)`
- Defined: `tests/test_entity_resolution.py:77`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_dissimilar_strings_score_low `def test_dissimilar_strings_score_low(self)`
- Defined: `tests/test_entity_resolution.py:81`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_scores_stay_in_unit_interval `def test_scores_stay_in_unit_interval(self)`
- Defined: `tests/test_entity_resolution.py:84`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_ipv4_normalised `def test_ipv4_normalised(self)`
- Defined: `tests/test_entity_resolution.py:92`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_ipv6_compressed `def test_ipv6_compressed(self)`
- Defined: `tests/test_entity_resolution.py:95`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_hash_lowered `def test_hash_lowered(self)`
- Defined: `tests/test_entity_resolution.py:101`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_cve_uppered `def test_cve_uppered(self)`
- Defined: `tests/test_entity_resolution.py:107`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_domain_strips_scheme_www_path `def test_domain_strips_scheme_www_path(self)`
- Defined: `tests/test_entity_resolution.py:110`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_person_order_independent `def test_person_order_independent(self)`
- Defined: `tests/test_entity_resolution.py:116`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_org_suffix_stripped `def test_org_suffix_stripped(self)`
- Defined: `tests/test_entity_resolution.py:121`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_asn_normalised `def test_asn_normalised(self)`
- Defined: `tests/test_entity_resolution.py:126`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_email_lowered `def test_email_lowered(self)`
- Defined: `tests/test_entity_resolution.py:129`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_deterministic `def test_deterministic(self)`
- Defined: `tests/test_entity_resolution.py:136`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_different_values_different_ids `def test_different_values_different_ids(self)`
- Defined: `tests/test_entity_resolution.py:141`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_id_format `def test_id_format(self)`
- Defined: `tests/test_entity_resolution.py:146`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_three_spellings_fuse `def test_three_spellings_fuse(self)`
- Defined: `tests/test_entity_resolution.py:158`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_fused_identity_carries_all_sources `def test_fused_identity_carries_all_sources(self)`
- Defined: `tests/test_entity_resolution.py:169`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_cross_script_flagged_in_attributes `def test_cross_script_flagged_in_attributes(self)`
- Defined: `tests/test_entity_resolution.py:180`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_domain_case_variants_merge `def test_domain_case_variants_merge(self)`
- Defined: `tests/test_entity_resolution.py:197`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_domain_merge_is_exact `def test_domain_merge_is_exact(self)`
- Defined: `tests/test_entity_resolution.py:207`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_look_alike_domains_stay_separate `def test_look_alike_domains_stay_separate(self)`
- Defined: `tests/test_entity_resolution.py:224`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_look_alike_domains_produce_same_as_link `def test_look_alike_domains_produce_same_as_link(self)`
- Defined: `tests/test_entity_resolution.py:233`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_deterministic_near_miss_never_matches `def test_deterministic_near_miss_never_matches(self)`
- Defined: `tests/test_entity_resolution.py:249`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_score_pair_deterministic_mismatch `def test_score_pair_deterministic_mismatch(self)`
- Defined: `tests/test_entity_resolution.py:259`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_identical_ips_merge `def test_identical_ips_merge(self)`
- Defined: `tests/test_entity_resolution.py:275`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_near_ips_stay_separate `def test_near_ips_stay_separate(self)`
- Defined: `tests/test_entity_resolution.py:292`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_org_suffix_variants_merge `def test_org_suffix_variants_merge(self)`
- Defined: `tests/test_entity_resolution.py:312`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_distinct_persons_not_absorbed `def test_distinct_persons_not_absorbed(self)`
- Defined: `tests/test_entity_resolution.py:329`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_to_dict_serialises `def test_to_dict_serialises(self)`
- Defined: `tests/test_entity_resolution.py:350`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_to_entity_projects_legacy `def test_to_entity_projects_legacy(self)`
- Defined: `tests/test_entity_resolution.py:361`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_resolution_result_has_one_entity `def test_resolution_result_has_one_entity(self)`
- Defined: `tests/test_entity_resolution.py:373`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_empty_input_returns_empty `def test_empty_input_returns_empty(self)`
- Defined: `tests/test_entity_resolution.py:385`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_same_normalised_same_id `def test_same_normalised_same_id(self)`
- Defined: `tests/test_entity_resolution.py:397`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_different_normalised_different_id `def test_different_normalised_different_id(self)`
- Defined: `tests/test_entity_resolution.py:409`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_blank_value_does_not_crash `def test_blank_value_does_not_crash(self)`
- Defined: `tests/test_entity_resolution.py:421`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_whitespace_only_handled `def test_whitespace_only_handled(self)`
- Defined: `tests/test_entity_resolution.py:425`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_single_entity_produces_one_canonical `def test_single_entity_produces_one_canonical(self)`
- Defined: `tests/test_entity_resolution.py:429`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_confidence_boosted_by_multiple_sources `def test_confidence_boosted_by_multiple_sources(self)`
- Defined: `tests/test_entity_resolution.py:434`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

### test_cross_run_id_stability `def test_cross_run_id_stability(self)`
- Defined: `tests/test_entity_resolution.py:451`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

## tests/test_fusion_analytics.py

### store_and_analytics `def store_and_analytics(tmp_path)`
- Defined: `tests/test_fusion_analytics.py:27`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### _populate_evilcorp `def _populate_evilcorp(store)`
- Defined: `tests/test_fusion_analytics.py:42`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### _register_source `def _register_source(store, name)`
- Defined: `tests/test_fusion_analytics.py:57`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_returns_full_timeline `def test_returns_full_timeline(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:65`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_nonexistent_eid_returns_none `def test_nonexistent_eid_returns_none(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:79`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_returns_summary_stats `def test_returns_summary_stats(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:88`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_nonexistent_eid_returns_none `def test_nonexistent_eid_returns_none(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:101`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_returns_none `def test_returns_none(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:110`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_returns_source_metrics `def test_returns_source_metrics(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:119`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_nonexistent_source_returns_none `def test_nonexistent_source_returns_none(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:135`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_success_rate_correct `def test_success_rate_correct(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:139`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_consensus_picks_majority_value `def test_consensus_picks_majority_value(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:156`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_nonexistent_key_returns_empty `def test_nonexistent_key_returns_empty(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:165`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_filters_by_min_sources `def test_filters_by_min_sources(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:177`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_min_sources_one_returns_all `def test_min_sources_one_returns_all(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:185`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_search_by_term `def test_search_by_term(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:196`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_search_no_results `def test_search_no_results(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:208`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_search_filter_by_type `def test_search_filter_by_type(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:213`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_search_with_confidence_and_source_filters `def test_search_with_confidence_and_source_filters(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:219`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_returns_recently_active_entities `def test_returns_recently_active_entities(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:231`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_empty_window_returns_empty `def test_empty_window_returns_empty(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:241`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_returns_pairs_with_shared_counts `def test_returns_pairs_with_shared_counts(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:251`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_all_methods_return_empty `def test_all_methods_return_empty(self)`
- Defined: `tests/test_fusion_analytics.py:269`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_min_sources_zero_treated_as_one `def test_min_sources_zero_treated_as_one(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:282`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

### test_negative_days_treated_as_one `def test_negative_days_treated_as_one(self, store_and_analytics)`
- Defined: `tests/test_fusion_analytics.py:288`
- Depends on: `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`

## tests/test_hypothesis_engine.py

### _obs `def _obs(source, parsed, raw)`
- Defined: `tests/test_hypothesis_engine.py:23`
- Doc: Build a minimal observation dict that matches the orchestrator shape.
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### generate_hypothences_safe `def generate_hypothences_safe(observations, entities)`
- Defined: `tests/test_hypothesis_engine.py:127`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_emits_domain_belongsto_actor_hypothesis `def test_emits_domain_belongsto_actor_hypothesis(self)`
- Defined: `tests/test_hypothesis_engine.py:42`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_score_in_high_band `def test_score_in_high_band(self)`
- Defined: `tests/test_hypothesis_engine.py:61`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_supporting_has_three_items `def test_supporting_has_three_items(self)`
- Defined: `tests/test_hypothesis_engine.py:76`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_sources_sorted_and_unique `def test_sources_sorted_and_unique(self)`
- Defined: `tests/test_hypothesis_engine.py:95`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_empty_observations_empty_entities `def test_empty_observations_empty_entities(self)`
- Defined: `tests/test_hypothesis_engine.py:116`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_empty_observations_only `def test_empty_observations_only(self)`
- Defined: `tests/test_hypothesis_engine.py:119`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_empty_entities_only `def test_empty_entities_only(self)`
- Defined: `tests/test_hypothesis_engine.py:122`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_observation_with_none_parsed_is_ignored `def test_observation_with_none_parsed_is_ignored(self)`
- Defined: `tests/test_hypothesis_engine.py:141`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_observation_without_source_is_ignored `def test_observation_without_source_is_ignored(self)`
- Defined: `tests/test_hypothesis_engine.py:155`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_unknown_source_uses_reliability_c `def test_unknown_source_uses_reliability_c(self)`
- Defined: `tests/test_hypothesis_engine.py:179`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_min_score_zero_returns_all `def test_min_score_zero_returns_all(self)`
- Defined: `tests/test_hypothesis_engine.py:202`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_min_score_one_filters_everything `def test_min_score_one_filters_everything(self)`
- Defined: `tests/test_hypothesis_engine.py:214`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_max_hypotheses_caps_output `def test_max_hypotheses_caps_output(self)`
- Defined: `tests/test_hypothesis_engine.py:233`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_observations_must_be_sequence `def test_observations_must_be_sequence(self)`
- Defined: `tests/test_hypothesis_engine.py:256`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_entities_must_be_sequence `def test_entities_must_be_sequence(self)`
- Defined: `tests/test_hypothesis_engine.py:260`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_min_score_out_of_range_raises `def test_min_score_out_of_range_raises(self)`
- Defined: `tests/test_hypothesis_engine.py:264`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_max_hypotheses_too_small_raises `def test_max_hypotheses_too_small_raises(self)`
- Defined: `tests/test_hypothesis_engine.py:270`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_hostile_value_is_truncated_or_skipped `def test_hostile_value_is_truncated_or_skipped(self, hostile)`
- Defined: `tests/test_hypothesis_engine.py:292`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_same_input_same_ids_and_scores `def test_same_input_same_ids_and_scores(self)`
- Defined: `tests/test_hypothesis_engine.py:312`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_input_order_does_not_affect_output `def test_input_order_does_not_affect_output(self)`
- Defined: `tests/test_hypothesis_engine.py:333`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_hypothesis_dataclass_is_frozen `def test_hypothesis_dataclass_is_frozen(self)`
- Defined: `tests/test_hypothesis_engine.py:354`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_evidence_dataclass_is_frozen `def test_evidence_dataclass_is_frozen(self)`
- Defined: `tests/test_hypothesis_engine.py:370`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

### test_entity_ref_is_frozen `def test_entity_ref_is_frozen(self)`
- Defined: `tests/test_hypothesis_engine.py:382`
- Depends on: `estorides_core/hypothesis_engine.py`, `estorides_core/reliability_scoring.py`

## tests/test_job_registry.py

### test_register_returns_value `def test_register_returns_value()`
- Defined: `tests/test_job_registry.py:11`
- Depends on: `estorides_core/job_registry.py`

### test_size_cap_evicts_oldest `def test_size_cap_evicts_oldest()`
- Defined: `tests/test_job_registry.py:17`
- Depends on: `estorides_core/job_registry.py`

### test_get_refreshes_lru_order `def test_get_refreshes_lru_order()`
- Defined: `tests/test_job_registry.py:28`
- Depends on: `estorides_core/job_registry.py`

### test_ttl_eviction `def test_ttl_eviction()`
- Defined: `tests/test_job_registry.py:39`
- Depends on: `estorides_core/job_registry.py`

### test_pop_removes_entry `def test_pop_removes_entry()`
- Defined: `tests/test_job_registry.py:53`
- Depends on: `estorides_core/job_registry.py`

### test_keys_values_consistent `def test_keys_values_consistent()`
- Defined: `tests/test_job_registry.py:61`
- Depends on: `estorides_core/job_registry.py`

### test_invalid_construction `def test_invalid_construction()`
- Defined: `tests/test_job_registry.py:69`
- Depends on: `estorides_core/job_registry.py`

### test_replacement_does_not_evict `def test_replacement_does_not_evict()`
- Defined: `tests/test_job_registry.py:76`
- Doc: Re-registering the same key keeps the size stable and LRU order intact.
- Depends on: `estorides_core/job_registry.py`

## tests/test_monitoring.py

### tmp_store `def tmp_store()`
- Defined: `tests/test_monitoring.py:32`
- Doc: Create a temporary WatchStore for testing, auto-closes on teardown.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### sample_watch `def sample_watch()`
- Defined: `tests/test_monitoring.py:42`
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_create_watch `def test_create_watch(self, tmp_store)`
- Defined: `tests/test_monitoring.py:61`
- Doc: Given a valid query, a watch is created with status pending.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_watch_next_run_in_future `def test_watch_next_run_in_future(self, sample_watch)`
- Defined: `tests/test_monitoring.py:69`
- Doc: Given a watch, next_run_at is in the future.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_watch_appears_in_list `def test_watch_appears_in_list(self, tmp_store, sample_watch)`
- Defined: `tests/test_monitoring.py:73`
- Doc: Given a persisted watch, it appears in the watch list.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_due_watches_returns_enabled `def test_due_watches_returns_enabled(self, tmp_store)`
- Defined: `tests/test_monitoring.py:89`
- Doc: Given enabled watches past due, only those are returned.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_interval_honored `def test_interval_honored(self, tmp_store)`
- Defined: `tests/test_monitoring.py:101`
- Doc: Given a watch with interval 15, due returns it at the right time.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_disable_does_not_delete `def test_disable_does_not_delete(self, tmp_store, sample_watch)`
- Defined: `tests/test_monitoring.py:118`
- Doc: Given a disabled watch, it still exists in the store.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_disabled_not_due `def test_disabled_not_due(self, tmp_store)`
- Defined: `tests/test_monitoring.py:127`
- Doc: Given a disabled watch past due, it is not returned as due.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_delete_removes_watch `def test_delete_removes_watch(self, tmp_store, sample_watch)`
- Defined: `tests/test_monitoring.py:145`
- Doc: Given a deleted watch, it no longer appears.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_delete_removes_from_list `def test_delete_removes_from_list(self, tmp_store, sample_watch)`
- Defined: `tests/test_monitoring.py:151`
- Doc: Given a deleted watch, the list no longer contains it.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_record_run_start `def test_record_run_start(self, tmp_store, sample_watch)`
- Defined: `tests/test_monitoring.py:167`
- Doc: Given a watch, recording a run returns a history id.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_history_appears `def test_history_appears(self, tmp_store, sample_watch)`
- Defined: `tests/test_monitoring.py:173`
- Doc: Given a completed run, history shows it.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_history_empty_for_new_watch `def test_history_empty_for_new_watch(self, tmp_store, sample_watch)`
- Defined: `tests/test_monitoring.py:183`
- Doc: Given a watch with no runs, history is empty.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_webhook_builds_correct_payload `def test_webhook_builds_correct_payload(self)`
- Defined: `tests/test_monitoring.py:197`
- Doc: Given a webhook alert, the payload has the right structure.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_source_yaml_loads `def test_source_yaml_loads(self, source_name)`
- Defined: `tests/test_monitoring.py:220`
- Doc: Given a source YAML file, it loads without errors.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_source_requires_key `def test_source_requires_key(self, source_name, key_env)`
- Defined: `tests/test_monitoring.py:235`
- Doc: Given a source YAML, it declares the correct key_env.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_all_new_sources_passive `def test_all_new_sources_passive(self)`
- Defined: `tests/test_monitoring.py:244`
- Doc: Given the new sources, all are contact: none (passive).
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_available_channels_returns_all `def test_available_channels_returns_all(self)`
- Defined: `tests/test_monitoring.py:263`
- Doc: Given the dispatcher, available_channels returns all channel types.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_channel_env_vars_listed `def test_channel_env_vars_listed(self)`
- Defined: `tests/test_monitoring.py:274`
- Doc: Given available channels, each has its env_var listed.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_unknown_channel_returns_false `def test_unknown_channel_returns_false(self)`
- Defined: `tests/test_monitoring.py:281`
- Doc: Given an unknown channel name, send returns False.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_to_dict_roundtrip `def test_to_dict_roundtrip(self)`
- Defined: `tests/test_monitoring.py:295`
- Doc: Given a WatchTarget, to_dict and from_dict roundtrip.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_default_next_run_set `def test_default_next_run_set(self)`
- Defined: `tests/test_monitoring.py:308`
- Doc: Given a WatchTarget with no next_run_at, it defaults to future.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_default_channels_empty `def test_default_channels_empty(self)`
- Defined: `tests/test_monitoring.py:313`
- Doc: Given a WatchTarget with no channels, channels is empty.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

### test_new_sources_loaded `def test_new_sources_loaded(self)`
- Defined: `tests/test_monitoring.py:327`
- Doc: Given the source directory, the new sources are loaded and counted.
- Depends on: `estorides_core/alerter.py`, `estorides_core/config.py`, `estorides_core/monitoring.py`, `estorides_core/source_loader.py`

## tests/test_observation_models.py

### _full_meta `def _full_meta()`
- Defined: `tests/test_observation_models.py:25`
- Depends on: `estorides_core/observation_models.py`

### _full_obs `def _full_obs()`
- Defined: `tests/test_observation_models.py:39`
- Depends on: `estorides_core/observation_models.py`

### test_o1_full_observation_validates `def test_o1_full_observation_validates()`
- Defined: `tests/test_observation_models.py:57`
- Depends on: `estorides_core/observation_models.py`

### test_o2_error_observation_validates `def test_o2_error_observation_validates()`
- Defined: `tests/test_observation_models.py:72`
- Depends on: `estorides_core/observation_models.py`

### test_o3_missing_required_field_fails `def test_o3_missing_required_field_fails()`
- Defined: `tests/test_observation_models.py:85`
- Depends on: `estorides_core/observation_models.py`

### test_o4_unknown_meta_key_forbidden `def test_o4_unknown_meta_key_forbidden()`
- Defined: `tests/test_observation_models.py:96`
- Depends on: `estorides_core/observation_models.py`

### test_o5_wrong_typed_field_fails `def test_o5_wrong_typed_field_fails()`
- Defined: `tests/test_observation_models.py:106`
- Depends on: `estorides_core/observation_models.py`

### test_o6_oversized_url_truncated_not_failed `def test_o6_oversized_url_truncated_not_failed()`
- Defined: `tests/test_observation_models.py:116`
- Depends on: `estorides_core/observation_models.py`

### test_o6_oversized_value_rejected `def test_o6_oversized_value_rejected()`
- Defined: `tests/test_observation_models.py:124`
- Depends on: `estorides_core/observation_models.py`

### test_o6_error_message_does_not_embed_hostile_value `def test_o6_error_message_does_not_embed_hostile_value()`
- Defined: `tests/test_observation_models.py:134`
- Depends on: `estorides_core/observation_models.py`

### test_o7_confidence_out_of_range_rejected `def test_o7_confidence_out_of_range_rejected(confidence)`
- Defined: `tests/test_observation_models.py:146`
- Depends on: `estorides_core/observation_models.py`

### test_o7_confidence_at_bounds_accepted `def test_o7_confidence_at_bounds_accepted()`
- Defined: `tests/test_observation_models.py:152`
- Depends on: `estorides_core/observation_models.py`

### test_o8_run_result_aggregates `def test_o8_run_result_aggregates()`
- Defined: `tests/test_observation_models.py:163`
- Depends on: `estorides_core/observation_models.py`

### test_o8_run_result_with_error_surfaces_error `def test_o8_run_result_with_error_surfaces_error()`
- Defined: `tests/test_observation_models.py:182`
- Depends on: `estorides_core/observation_models.py`

### test_security_non_json_safe_value_rejected `def test_security_non_json_safe_value_rejected(field)`
- Defined: `tests/test_observation_models.py:198`
- Depends on: `estorides_core/observation_models.py`

### test_security_non_json_safe_attributes_rejected `def test_security_non_json_safe_attributes_rejected()`
- Defined: `tests/test_observation_models.py:205`
- Depends on: `estorides_core/observation_models.py`

### test_security_bytes_top_level_parsed_rejected `def test_security_bytes_top_level_parsed_rejected()`
- Defined: `tests/test_observation_models.py:212`
- Depends on: `estorides_core/observation_models.py`

### test_security_non_string_dict_key_rejected `def test_security_non_string_dict_key_rejected()`
- Defined: `tests/test_observation_models.py:219`
- Depends on: `estorides_core/observation_models.py`

### test_security_arbitrary_object_rejected `def test_security_arbitrary_object_rejected()`
- Defined: `tests/test_observation_models.py:226`
- Depends on: `estorides_core/observation_models.py`

### test_security_nested_object_inside_list_rejected `def test_security_nested_object_inside_list_rejected()`
- Defined: `tests/test_observation_models.py:236`
- Doc: A hostile object nested inside a list must also be rejected (recursion).
- Depends on: `estorides_core/observation_models.py`

### test_security_arbitrary_object_message_names_the_type `def test_security_arbitrary_object_message_names_the_type()`
- Defined: `tests/test_observation_models.py:247`
- Doc: The rejection message must name the offending type, not the input content.
- Depends on: `estorides_core/observation_models.py`

### test_security_non_string_key_message_names_the_problem `def test_security_non_string_key_message_names_the_problem()`
- Defined: `tests/test_observation_models.py:260`
- Depends on: `estorides_core/observation_models.py`

### test_security_arbitrary_object_message_exact `def test_security_arbitrary_object_message_exact()`
- Defined: `tests/test_observation_models.py:270`
- Doc: The rejection message for an arbitrary object is the exact contract text.
- Depends on: `estorides_core/observation_models.py`

### test_length_caps_are_positive `def test_length_caps_are_positive()`
- Defined: `tests/test_observation_models.py:287`
- Depends on: `estorides_core/observation_models.py`

## tests/test_pagination.py

### test_first_page_is_one `def test_first_page_is_one(self)`
- Defined: `tests/test_pagination.py:24`
- Depends on: `estorides_core/pagination.py`

### test_second_page_increments `def test_second_page_increments(self)`
- Defined: `tests/test_pagination.py:29`
- Depends on: `estorides_core/pagination.py`

### test_default_param_name `def test_default_param_name(self)`
- Defined: `tests/test_pagination.py:34`
- Depends on: `estorides_core/pagination.py`

### test_no_pagination_returns_empty `def test_no_pagination_returns_empty(self)`
- Defined: `tests/test_pagination.py:39`
- Depends on: `estorides_core/pagination.py`

### test_first_page_offset_zero `def test_first_page_offset_zero(self)`
- Defined: `tests/test_pagination.py:51`
- Depends on: `estorides_core/pagination.py`

### test_second_page_offset_25 `def test_second_page_offset_25(self)`
- Defined: `tests/test_pagination.py:56`
- Depends on: `estorides_core/pagination.py`

### test_third_page_offset_50 `def test_third_page_offset_50(self)`
- Defined: `tests/test_pagination.py:61`
- Depends on: `estorides_core/pagination.py`

### test_custom_param_names `def test_custom_param_names(self)`
- Defined: `tests/test_pagination.py:66`
- Depends on: `estorides_core/pagination.py`

### test_extracts_cursor_from_simple_path `def test_extracts_cursor_from_simple_path(self)`
- Defined: `tests/test_pagination.py:81`
- Depends on: `estorides_core/pagination.py`

### test_extracts_cursor_from_nested_path `def test_extracts_cursor_from_nested_path(self)`
- Defined: `tests/test_pagination.py:86`
- Depends on: `estorides_core/pagination.py`

### test_missing_path_returns_none `def test_missing_path_returns_none(self)`
- Defined: `tests/test_pagination.py:91`
- Depends on: `estorides_core/pagination.py`

### test_empty_cursor_returns_none `def test_empty_cursor_returns_none(self)`
- Defined: `tests/test_pagination.py:95`
- Depends on: `estorides_core/pagination.py`

### test_null_cursor_returns_none `def test_null_cursor_returns_none(self)`
- Defined: `tests/test_pagination.py:99`
- Depends on: `estorides_core/pagination.py`

### test_non_dict_response_returns_none `def test_non_dict_response_returns_none(self)`
- Defined: `tests/test_pagination.py:103`
- Depends on: `estorides_core/pagination.py`

### test_disabled_strategy_returns_none `def test_disabled_strategy_returns_none(self)`
- Defined: `tests/test_pagination.py:107`
- Depends on: `estorides_core/pagination.py`

### test_build_params_empty_for_cursor `def test_build_params_empty_for_cursor(self)`
- Defined: `tests/test_pagination.py:111`
- Depends on: `estorides_core/pagination.py`

### test_cursor_custom_param `def test_cursor_custom_param(self)`
- Defined: `tests/test_pagination.py:116`
- Depends on: `estorides_core/pagination.py`

### test_default_config_disabled `def test_default_config_disabled(self)`
- Defined: `tests/test_pagination.py:131`
- Depends on: `estorides_core/pagination.py`

### test_empty_dict_disabled `def test_empty_dict_disabled(self)`
- Defined: `tests/test_pagination.py:135`
- Depends on: `estorides_core/pagination.py`

### test_none_disabled `def test_none_disabled(self)`
- Defined: `tests/test_pagination.py:139`
- Depends on: `estorides_core/pagination.py`

### test_enabled_when_strategy_set `def test_enabled_when_strategy_set(self)`
- Defined: `tests/test_pagination.py:143`
- Depends on: `estorides_core/pagination.py`

### test_partial_page_detected `def test_partial_page_detected(self)`
- Defined: `tests/test_pagination.py:154`
- Depends on: `estorides_core/pagination.py`

### test_full_page_not_detected_as_partial `def test_full_page_not_detected_as_partial(self)`
- Defined: `tests/test_pagination.py:159`
- Depends on: `estorides_core/pagination.py`

### test_list_response_counted_directly `def test_list_response_counted_directly(self)`
- Defined: `tests/test_pagination.py:164`
- Depends on: `estorides_core/pagination.py`

### test_using_custom_response_list_path `def test_using_custom_response_list_path(self)`
- Defined: `tests/test_pagination.py:168`
- Depends on: `estorides_core/pagination.py`

### test_default_max_pages `def test_default_max_pages(self)`
- Defined: `tests/test_pagination.py:183`
- Depends on: `estorides_core/pagination.py`

### test_custom_max_pages `def test_custom_max_pages(self)`
- Defined: `tests/test_pagination.py:187`
- Depends on: `estorides_core/pagination.py`

### test_zero_page_size_means_no_check `def test_zero_page_size_means_no_check(self)`
- Defined: `tests/test_pagination.py:193`
- Depends on: `estorides_core/pagination.py`

### test_all_fields_mapped `def test_all_fields_mapped(self)`
- Defined: `tests/test_pagination.py:208`
- Depends on: `estorides_core/pagination.py`

### test_partial_dict_uses_defaults `def test_partial_dict_uses_defaults(self)`
- Defined: `tests/test_pagination.py:230`
- Depends on: `estorides_core/pagination.py`

### test_empty_string_strategy_disabled `def test_empty_string_strategy_disabled(self)`
- Defined: `tests/test_pagination.py:236`
- Depends on: `estorides_core/pagination.py`

## tests/test_pdns_monitor.py

### test_returns_subdomains_from_ct `def test_returns_subdomains_from_ct(self)`
- Defined: `tests/test_pdns_monitor.py:19`
- Depends on: `estorides_core/pdns_monitor.py`

### test_tracks_ip_changes `def test_tracks_ip_changes(self)`
- Defined: `tests/test_pdns_monitor.py:33`
- Depends on: `estorides_core/pdns_monitor.py`

### test_empty_when_no_history `def test_empty_when_no_history(self)`
- Defined: `tests/test_pdns_monitor.py:48`
- Depends on: `estorides_core/pdns_monitor.py`

### test_new_cert_with_san `def test_new_cert_with_san(self)`
- Defined: `tests/test_pdns_monitor.py:56`
- Depends on: `estorides_core/pdns_monitor.py`

### test_no_zone_transfer_attempted `def test_no_zone_transfer_attempted(self)`
- Defined: `tests/test_pdns_monitor.py:77`
- Depends on: `estorides_core/pdns_monitor.py`

### test_wildcard_cert_detected `def test_wildcard_cert_detected(self)`
- Defined: `tests/test_pdns_monitor.py:86`
- Depends on: `estorides_core/pdns_monitor.py`

### test_active_status_when_resolves `def test_active_status_when_resolves(self)`
- Defined: `tests/test_pdns_monitor.py:103`
- Depends on: `estorides_core/pdns_monitor.py`

### test_inactive_when_no_resolution `def test_inactive_when_no_resolution(self)`
- Defined: `tests/test_pdns_monitor.py:106`
- Depends on: `estorides_core/pdns_monitor.py`

### test_minimum_poll_interval `def test_minimum_poll_interval(self)`
- Defined: `tests/test_pdns_monitor.py:112`
- Depends on: `estorides_core/pdns_monitor.py`

## tests/test_people_intel.py

### _make_emp `def _make_emp(name, role, email)`
- Defined: `tests/test_people_intel.py:18`
- Depends on: `estorides_core/people_intel.py`

### test_returns_employees_from_domain `def test_returns_employees_from_domain(self)`
- Defined: `tests/test_people_intel.py:29`
- Depends on: `estorides_core/people_intel.py`

### test_empty_when_no_employees `def test_empty_when_no_employees(self)`
- Defined: `tests/test_people_intel.py:43`
- Depends on: `estorides_core/people_intel.py`

### test_rejects_invalid_domain `def test_rejects_invalid_domain(self)`
- Defined: `tests/test_people_intel.py:51`
- Depends on: `estorides_core/people_intel.py`

### test_breach_with_password_is_critical `def test_breach_with_password_is_critical(self)`
- Defined: `tests/test_people_intel.py:58`
- Depends on: `estorides_core/people_intel.py`

### test_infers_first_dot_last_pattern `def test_infers_first_dot_last_pattern(self)`
- Defined: `tests/test_people_intel.py:82`
- Depends on: `estorides_core/people_intel.py`

### test_infers_firstinitial_last_pattern `def test_infers_firstinitial_last_pattern(self)`
- Defined: `tests/test_people_intel.py:91`
- Depends on: `estorides_core/people_intel.py`

### test_single_email_low_confidence `def test_single_email_low_confidence(self)`
- Defined: `tests/test_people_intel.py:102`
- Depends on: `estorides_core/people_intel.py`

### test_multiple_breaches_increase_risk `def test_multiple_breaches_increase_risk(self)`
- Defined: `tests/test_people_intel.py:109`
- Depends on: `estorides_core/people_intel.py`

### test_passwords_not_in_serialised_output `def test_passwords_not_in_serialised_output(self)`
- Defined: `tests/test_people_intel.py:129`
- Depends on: `estorides_core/people_intel.py`

## tests/test_probabilistic_fusion.py

### _fs `def _fs()`
- Defined: `tests/test_probabilistic_fusion.py:17`
- Depends on: `estorides_core/fusion_store.py`

### _teardown `def _teardown(store, tmp)`
- Defined: `tests/test_probabilistic_fusion.py:23`
- Depends on: `estorides_core/fusion_store.py`

### _entity `def _entity(etype, value, source, confidence)`
- Defined: `tests/test_probabilistic_fusion.py:30`
- Depends on: `estorides_core/fusion_store.py`

### test_primary_source_raises_score `def test_primary_source_raises_score(self)`
- Defined: `tests/test_probabilistic_fusion.py:51`
- Depends on: `estorides_core/fusion_store.py`

### test_untrusted_source_cannot_override `def test_untrusted_source_cannot_override(self)`
- Defined: `tests/test_probabilistic_fusion.py:80`
- Depends on: `estorides_core/fusion_store.py`

### test_two_sources_are_better_than_one `def test_two_sources_are_better_than_one(self)`
- Defined: `tests/test_probabilistic_fusion.py:113`
- Depends on: `estorides_core/fusion_store.py`

### test_lower_confidence_never_decreases `def test_lower_confidence_never_decreases(self)`
- Defined: `tests/test_probabilistic_fusion.py:145`
- Depends on: `estorides_core/fusion_store.py`

### test_untrusted_first_sighting_discounted `def test_untrusted_first_sighting_discounted(self)`
- Defined: `tests/test_probabilistic_fusion.py:173`
- Depends on: `estorides_core/fusion_store.py`

### test_relationship_untrusted_cannot_override `def test_relationship_untrusted_cannot_override(self)`
- Defined: `tests/test_probabilistic_fusion.py:195`
- Depends on: `estorides_core/fusion_store.py`

### test_entity_id_deterministic `def test_entity_id_deterministic(self)`
- Defined: `tests/test_probabilistic_fusion.py:220`
- Depends on: `estorides_core/fusion_store.py`

### test_entity_source_count_tracks `def test_entity_source_count_tracks(self)`
- Defined: `tests/test_probabilistic_fusion.py:229`
- Depends on: `estorides_core/fusion_store.py`

### test_observation_count_advances `def test_observation_count_advances(self)`
- Defined: `tests/test_probabilistic_fusion.py:243`
- Depends on: `estorides_core/fusion_store.py`

### test_empty_type_returns_empty `def test_empty_type_returns_empty(self)`
- Defined: `tests/test_probabilistic_fusion.py:259`
- Depends on: `estorides_core/fusion_store.py`

### test_empty_value_returns_empty `def test_empty_value_returns_empty(self)`
- Defined: `tests/test_probabilistic_fusion.py:267`
- Depends on: `estorides_core/fusion_store.py`

### test_add_observation_and_stats `def test_add_observation_and_stats(self)`
- Defined: `tests/test_probabilistic_fusion.py:275`
- Depends on: `estorides_core/fusion_store.py`

### test_register_sources `def test_register_sources(self)`
- Defined: `tests/test_probabilistic_fusion.py:290`
- Depends on: `estorides_core/fusion_store.py`

### test_search_entities `def test_search_entities(self)`
- Defined: `tests/test_probabilistic_fusion.py:305`
- Depends on: `estorides_core/fusion_store.py`

### test_corroborated_properties `def test_corroborated_properties(self)`
- Defined: `tests/test_probabilistic_fusion.py:320`
- Depends on: `estorides_core/fusion_store.py`

### test_get_entity_nonexistent `def test_get_entity_nonexistent(self)`
- Defined: `tests/test_probabilistic_fusion.py:333`
- Depends on: `estorides_core/fusion_store.py`

### test_open_store_closes_gracefully `def test_open_store_closes_gracefully(self)`
- Defined: `tests/test_probabilistic_fusion.py:340`
- Depends on: `estorides_core/fusion_store.py`

## tests/test_recon_fusion.py

### _observation `def _observation(source, category, parser, status, parsed)`
- Defined: `tests/test_recon_fusion.py:14`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### _entity `def _entity(etype, value, confidence, sources)`
- Defined: `tests/test_recon_fusion.py:31`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_critical_with_5_sources `def test_critical_with_5_sources(self)`
- Defined: `tests/test_recon_fusion.py:49`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_two_reliable_sources_critical `def test_two_reliable_sources_critical(self)`
- Defined: `tests/test_recon_fusion.py:68`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_single_a_source_is_medium `def test_single_a_source_is_medium(self)`
- Defined: `tests/test_recon_fusion.py:85`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_single_f_source_is_noise `def test_single_f_source_is_noise(self)`
- Defined: `tests/test_recon_fusion.py:105`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_empty_observations_and_entities `def test_empty_observations_and_entities(self)`
- Defined: `tests/test_recon_fusion.py:120`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_direct_match_boosts_score `def test_direct_match_boosts_score(self)`
- Defined: `tests/test_recon_fusion.py:133`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_empty_query_raises `def test_empty_query_raises(self)`
- Defined: `tests/test_recon_fusion.py:150`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_bad_thresholds_raise `def test_bad_thresholds_raise(self)`
- Defined: `tests/test_recon_fusion.py:160`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_none_observations_safe `def test_none_observations_safe(self)`
- Defined: `tests/test_recon_fusion.py:176`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_entity_without_type_ignored `def test_entity_without_type_ignored(self)`
- Defined: `tests/test_recon_fusion.py:186`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_identical_observations_deduped `def test_identical_observations_deduped(self)`
- Defined: `tests/test_recon_fusion.py:198`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_tier_ordered_by_score `def test_tier_ordered_by_score(self)`
- Defined: `tests/test_recon_fusion.py:215`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_mixed_entities_across_tiers `def test_mixed_entities_across_tiers(self)`
- Defined: `tests/test_recon_fusion.py:230`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_fusion_result_serialisable `def test_fusion_result_serialisable(self)`
- Defined: `tests/test_recon_fusion.py:255`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_enum_members `def test_enum_members(self)`
- Defined: `tests/test_recon_fusion.py:270`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

### test_enum_order_list `def test_enum_order_list(self)`
- Defined: `tests/test_recon_fusion.py:277`
- Depends on: `estorides_core/config.py`, `estorides_core/recon_fusion.py`

## tests/test_recon_report.py

### _make_meta `def _make_meta()`
- Defined: `tests/test_recon_report.py:18`
- Depends on: `estorides_export/recon_report.py`

### test_contains_all_sections `def test_contains_all_sections(self)`
- Defined: `tests/test_recon_report.py:29`
- Depends on: `estorides_export/recon_report.py`

### test_mentions_critical_findings `def test_mentions_critical_findings(self)`
- Defined: `tests/test_recon_report.py:43`
- Depends on: `estorides_export/recon_report.py`

### test_minimal_report_with_no_findings `def test_minimal_report_with_no_findings(self)`
- Defined: `tests/test_recon_report.py:58`
- Depends on: `estorides_export/recon_report.py`

### test_tlp_amber_in_header `def test_tlp_amber_in_header(self)`
- Defined: `tests/test_recon_report.py:73`
- Depends on: `estorides_export/recon_report.py`

### test_critical_first `def test_critical_first(self)`
- Defined: `tests/test_recon_report.py:84`
- Depends on: `estorides_export/recon_report.py`

### test_aws_key_redacted `def test_aws_key_redacted(self)`
- Defined: `tests/test_recon_report.py:92`
- Depends on: `estorides_export/recon_report.py`

### test_password_redacted `def test_password_redacted(self)`
- Defined: `tests/test_recon_report.py:97`
- Depends on: `estorides_export/recon_report.py`

### test_ascii_tree_generated `def test_ascii_tree_generated(self)`
- Defined: `tests/test_recon_report.py:105`
- Depends on: `estorides_export/recon_report.py`

### test_single_finding_prominent `def test_single_finding_prominent(self)`
- Defined: `tests/test_recon_report.py:119`
- Depends on: `estorides_export/recon_report.py`

## tests/test_reliability_scoring.py

### test_score_in_high_band `def test_score_in_high_band(self)`
- Defined: `tests/test_reliability_scoring.py:48`
- Depends on: `estorides_core/reliability_scoring.py`

### test_reliability_weight_is_one `def test_reliability_weight_is_one(self)`
- Defined: `tests/test_reliability_scoring.py:67`
- Depends on: `estorides_core/reliability_scoring.py`

### test_freshness_weight_is_one_when_age_zero `def test_freshness_weight_is_one_when_age_zero(self)`
- Defined: `tests/test_reliability_scoring.py:76`
- Depends on: `estorides_core/reliability_scoring.py`

### test_corroboration_weight_matches_log10 `def test_corroboration_weight_matches_log10(self)`
- Defined: `tests/test_reliability_scoring.py:86`
- Depends on: `estorides_core/reliability_scoring.py`

### test_credibility_weight_for_probably_true `def test_credibility_weight_for_probably_true(self)`
- Defined: `tests/test_reliability_scoring.py:95`
- Depends on: `estorides_core/reliability_scoring.py`

### test_unknown_source_returns_default `def test_unknown_source_returns_default(self, name)`
- Defined: `tests/test_reliability_scoring.py:120`
- Depends on: `estorides_core/reliability_scoring.py`

### test_unknown_source_produces_weak_score_with_one_corroboration `def test_unknown_source_produces_weak_score_with_one_corroboration(self)`
- Defined: `tests/test_reliability_scoring.py:126`
- Depends on: `estorides_core/reliability_scoring.py`

### test_unknown_source_with_many_corroborators_reaches_high_band `def test_unknown_source_with_many_corroborators_reaches_high_band(self)`
- Defined: `tests/test_reliability_scoring.py:146`
- Depends on: `estorides_core/reliability_scoring.py`

### test_zero_corroboration_collapses_score `def test_zero_corroboration_collapses_score(self)`
- Defined: `tests/test_reliability_scoring.py:172`
- Depends on: `estorides_core/reliability_scoring.py`

### test_one_year_old_with_low_corroboration_decays `def test_one_year_old_with_low_corroboration_decays(self)`
- Defined: `tests/test_reliability_scoring.py:191`
- Depends on: `estorides_core/reliability_scoring.py`

### test_freshness_is_monotonically_decreasing `def test_freshness_is_monotonically_decreasing(self)`
- Defined: `tests/test_reliability_scoring.py:204`
- Doc: Una observación más vieja siempre tiene freshness menor o igual.
- Depends on: `estorides_core/reliability_scoring.py`

### test_negative_corroboration_count_raises `def test_negative_corroboration_count_raises(self)`
- Defined: `tests/test_reliability_scoring.py:228`
- Depends on: `estorides_core/reliability_scoring.py`

### test_negative_observation_age_raises `def test_negative_observation_age_raises(self)`
- Defined: `tests/test_reliability_scoring.py:235`
- Depends on: `estorides_core/reliability_scoring.py`

### test_base_confidence_out_of_range_raises `def test_base_confidence_out_of_range_raises(self, bad)`
- Defined: `tests/test_reliability_scoring.py:243`
- Depends on: `estorides_core/reliability_scoring.py`

### test_half_life_zero_raises `def test_half_life_zero_raises(self)`
- Defined: `tests/test_reliability_scoring.py:250`
- Depends on: `estorides_core/reliability_scoring.py`

### test_half_life_negative_raises `def test_half_life_negative_raises(self)`
- Defined: `tests/test_reliability_scoring.py:258`
- Depends on: `estorides_core/reliability_scoring.py`

### test_hostile_name_does_not_raise `def test_hostile_name_does_not_raise(self, hostile)`
- Defined: `tests/test_reliability_scoring.py:288`
- Depends on: `estorides_core/reliability_scoring.py`

### test_new_a_source_raises_score `def test_new_a_source_raises_score(self)`
- Defined: `tests/test_reliability_scoring.py:302`
- Depends on: `estorides_core/reliability_scoring.py`

### test_merge_takes_max_of_existing_and_new `def test_merge_takes_max_of_existing_and_new(self)`
- Defined: `tests/test_reliability_scoring.py:319`
- Depends on: `estorides_core/reliability_scoring.py`

### test_merge_keeps_existing_when_new_is_weaker `def test_merge_keeps_existing_when_new_is_weaker(self)`
- Defined: `tests/test_reliability_scoring.py:335`
- Depends on: `estorides_core/reliability_scoring.py`

### test_merge_result_is_always_bounded `def test_merge_result_is_always_bounded(self)`
- Defined: `tests/test_reliability_scoring.py:350`
- Depends on: `estorides_core/reliability_scoring.py`

### test_f_source_against_strong_existing_keeps_existing `def test_f_source_against_strong_existing_keeps_existing(self)`
- Defined: `tests/test_reliability_scoring.py:369`
- Depends on: `estorides_core/reliability_scoring.py`

### test_merge_existing_out_of_range_raises `def test_merge_existing_out_of_range_raises(self)`
- Defined: `tests/test_reliability_scoring.py:384`
- Depends on: `estorides_core/reliability_scoring.py`

### test_merge_new_observation_out_of_range_raises `def test_merge_new_observation_out_of_range_raises(self)`
- Defined: `tests/test_reliability_scoring.py:396`
- Depends on: `estorides_core/reliability_scoring.py`

### test_compute_confidence_is_pure `def test_compute_confidence_is_pure(self)`
- Defined: `tests/test_reliability_scoring.py:415`
- Depends on: `estorides_core/reliability_scoring.py`

### test_merge_confidence_is_pure `def test_merge_confidence_is_pure(self)`
- Defined: `tests/test_reliability_scoring.py:428`
- Depends on: `estorides_core/reliability_scoring.py`

### test_reliability_weights_match_nato_admiralty `def test_reliability_weights_match_nato_admiralty(self)`
- Defined: `tests/test_reliability_scoring.py:456`
- Depends on: `estorides_core/reliability_scoring.py`

### test_credibility_weights_match_nato_admiralty `def test_credibility_weights_match_nato_admiralty(self)`
- Defined: `tests/test_reliability_scoring.py:465`
- Depends on: `estorides_core/reliability_scoring.py`

### test_default_half_life_is_thirty_days `def test_default_half_life_is_thirty_days(self)`
- Defined: `tests/test_reliability_scoring.py:473`
- Depends on: `estorides_core/reliability_scoring.py`

### test_default_credibility_is_cannot_be_judged `def test_default_credibility_is_cannot_be_judged(self)`
- Defined: `tests/test_reliability_scoring.py:476`
- Depends on: `estorides_core/reliability_scoring.py`

### test_primary_tertiary_score_order `def test_primary_tertiary_score_order(self)`
- Defined: `tests/test_reliability_scoring.py:486`
- Depends on: `estorides_core/reliability_scoring.py`

### test_primary_weight_is_one `def test_primary_weight_is_one(self)`
- Defined: `tests/test_reliability_scoring.py:519`
- Depends on: `estorides_core/reliability_scoring.py`

### test_secondary_weight_is_085 `def test_secondary_weight_is_085(self)`
- Defined: `tests/test_reliability_scoring.py:528`
- Depends on: `estorides_core/reliability_scoring.py`

### test_tertiary_weight_is_060 `def test_tertiary_weight_is_060(self)`
- Defined: `tests/test_reliability_scoring.py:537`
- Depends on: `estorides_core/reliability_scoring.py`

### test_primary_c_beats_tertiary_a `def test_primary_c_beats_tertiary_a(self)`
- Defined: `tests/test_reliability_scoring.py:553`
- Depends on: `estorides_core/reliability_scoring.py`

### test_primary_c_weight `def test_primary_c_weight(self)`
- Defined: `tests/test_reliability_scoring.py:580`
- Depends on: `estorides_core/reliability_scoring.py`

### test_rdap_is_primary `def test_rdap_is_primary(self)`
- Defined: `tests/test_reliability_scoring.py:597`
- Depends on: `estorides_core/reliability_scoring.py`

### test_leakcheck_is_tertiary `def test_leakcheck_is_tertiary(self)`
- Defined: `tests/test_reliability_scoring.py:600`
- Depends on: `estorides_core/reliability_scoring.py`

### test_wikidata_is_secondary `def test_wikidata_is_secondary(self)`
- Defined: `tests/test_reliability_scoring.py:603`
- Depends on: `estorides_core/reliability_scoring.py`

### test_shodan_is_secondary `def test_shodan_is_secondary(self)`
- Defined: `tests/test_reliability_scoring.py:606`
- Depends on: `estorides_core/reliability_scoring.py`

### test_unknown_falls_back_to_default `def test_unknown_falls_back_to_default(self)`
- Defined: `tests/test_reliability_scoring.py:609`
- Depends on: `estorides_core/reliability_scoring.py`

### test_none_falls_back `def test_none_falls_back(self)`
- Defined: `tests/test_reliability_scoring.py:612`
- Depends on: `estorides_core/reliability_scoring.py`

### test_empty_falls_back `def test_empty_falls_back(self)`
- Defined: `tests/test_reliability_scoring.py:615`
- Depends on: `estorides_core/reliability_scoring.py`

### test_hostile_input_does_not_raise `def test_hostile_input_does_not_raise(self)`
- Defined: `tests/test_reliability_scoring.py:618`
- Depends on: `estorides_core/reliability_scoring.py`

### test_new_primary_raises_score `def test_new_primary_raises_score(self)`
- Defined: `tests/test_reliability_scoring.py:631`
- Depends on: `estorides_core/reliability_scoring.py`

### test_new_tertiary_does_not_raise_weak_existing `def test_new_tertiary_does_not_raise_weak_existing(self)`
- Defined: `tests/test_reliability_scoring.py:644`
- Depends on: `estorides_core/reliability_scoring.py`

### test_source_type_weights_are_exact `def test_source_type_weights_are_exact(self)`
- Defined: `tests/test_reliability_scoring.py:665`
- Depends on: `estorides_core/reliability_scoring.py`

### test_primary_always_gives_one `def test_primary_always_gives_one(self)`
- Defined: `tests/test_reliability_scoring.py:670`
- Depends on: `estorides_core/reliability_scoring.py`

### test_tertiary_always_gives_060 `def test_tertiary_always_gives_060(self)`
- Defined: `tests/test_reliability_scoring.py:679`
- Depends on: `estorides_core/reliability_scoring.py`

## tests/test_search_telemetry.py

### _render_index `def _render_index()`
- Defined: `tests/test_search_telemetry.py:36`
- Doc: Render `index.html` exactly as the web layer does, telemetry included.
- Depends on: `estorides_core/search_telemetry.py`

### test_s1_determinate_progress_midsearch `def test_s1_determinate_progress_midsearch()`
- Defined: `tests/test_search_telemetry.py:52`
- Depends on: `estorides_core/search_telemetry.py`

### test_s2_indeterminate_progress `def test_s2_indeterminate_progress()`
- Defined: `tests/test_search_telemetry.py:67`
- Depends on: `estorides_core/search_telemetry.py`

### test_s3_completion_stops_spinner `def test_s3_completion_stops_spinner()`
- Defined: `tests/test_search_telemetry.py:79`
- Depends on: `estorides_core/search_telemetry.py`

### test_s4_out_of_range_is_clamped `def test_s4_out_of_range_is_clamped()`
- Defined: `tests/test_search_telemetry.py:90`
- Depends on: `estorides_core/search_telemetry.py`

### test_s5_unknown_phase_rejected `def test_s5_unknown_phase_rejected()`
- Defined: `tests/test_search_telemetry.py:103`
- Depends on: `estorides_core/search_telemetry.py`

### test_s6_catalog_is_brand_and_emoji_clean `def test_s6_catalog_is_brand_and_emoji_clean()`
- Defined: `tests/test_search_telemetry.py:114`
- Depends on: `estorides_core/search_telemetry.py`

### test_s7_rendered_template_has_no_third_party_brand `def test_s7_rendered_template_has_no_third_party_brand()`
- Defined: `tests/test_search_telemetry.py:132`
- Depends on: `estorides_core/search_telemetry.py`

### test_s8_rendered_chrome_has_no_emoji `def test_s8_rendered_chrome_has_no_emoji()`
- Defined: `tests/test_search_telemetry.py:141`
- Depends on: `estorides_core/search_telemetry.py`

### test_s9_brand_predicate_boundaries `def test_s9_brand_predicate_boundaries()`
- Defined: `tests/test_search_telemetry.py:153`
- Depends on: `estorides_core/search_telemetry.py`

### _valid_kwargs `def _valid_kwargs()`
- Defined: `tests/test_search_telemetry.py:163`
- Depends on: `estorides_core/search_telemetry.py`

### test_s10_empty_brand_rejected `def test_s10_empty_brand_rejected()`
- Defined: `tests/test_search_telemetry.py:178`
- Depends on: `estorides_core/search_telemetry.py`

### test_s10_no_tips_rejected `def test_s10_no_tips_rejected()`
- Defined: `tests/test_search_telemetry.py:185`
- Depends on: `estorides_core/search_telemetry.py`

### test_s10_duplicate_phase_rejected `def test_s10_duplicate_phase_rejected()`
- Defined: `tests/test_search_telemetry.py:192`
- Depends on: `estorides_core/search_telemetry.py`

### test_s10_emoji_in_catalog_rejected `def test_s10_emoji_in_catalog_rejected()`
- Defined: `tests/test_search_telemetry.py:205`
- Depends on: `estorides_core/search_telemetry.py`

### test_s10_brand_collision_rejected `def test_s10_brand_collision_rejected()`
- Defined: `tests/test_search_telemetry.py:212`
- Depends on: `estorides_core/search_telemetry.py`

### test_s10_missing_sentinel_phase_rejected `def test_s10_missing_sentinel_phase_rejected()`
- Defined: `tests/test_search_telemetry.py:219`
- Depends on: `estorides_core/search_telemetry.py`

### test_s11_template_renders_from_catalog `def test_s11_template_renders_from_catalog()`
- Defined: `tests/test_search_telemetry.py:233`
- Depends on: `estorides_core/search_telemetry.py`

### test_default_telemetry_is_a_shared_instance `def test_default_telemetry_is_a_shared_instance()`
- Defined: `tests/test_search_telemetry.py:247`
- Depends on: `estorides_core/search_telemetry.py`

## tests/test_security_remediation.py

### test_dns_failure_log_omits_hostname `def test_dns_failure_log_omits_hostname(self, caplog)`
- Defined: `tests/test_security_remediation.py:29`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_dns_failure_log_omits_ip_in_hostname `def test_dns_failure_log_omits_ip_in_hostname(self, caplog)`
- Defined: `tests/test_security_remediation.py:43`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_dns_failure_log_contains_host_length_not_host `def test_dns_failure_log_contains_host_length_not_host(self, caplog)`
- Defined: `tests/test_security_remediation.py:55`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### app `def app(self)`
- Defined: `tests/test_security_remediation.py:79`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### _make_export_route `def _make_export_route(self, app, raise_val, error_msg, status)`
- Defined: `tests/test_security_remediation.py:86`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### _make_export_route_fixed `def _make_export_route_fixed(self, app, raise_val, error_msg, status)`
- Defined: `tests/test_security_remediation.py:118`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_encryption_valueerror_leaks_detail `def test_encryption_valueerror_leaks_detail(self, app)`
- Defined: `tests/test_security_remediation.py:151`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_encryption_valueerror_fixed_no_detail `def test_encryption_valueerror_fixed_no_detail(self, app)`
- Defined: `tests/test_security_remediation.py:159`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_encryption_runtimeerror_fixed_no_detail `def test_encryption_runtimeerror_fixed_no_detail(self, app)`
- Defined: `tests/test_security_remediation.py:167`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### app `def app(self)`
- Defined: `tests/test_security_remediation.py:180`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_source_delete_keyerror_fixed `def test_source_delete_keyerror_fixed(self, app)`
- Defined: `tests/test_security_remediation.py:187`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_source_create_valueerror_fixed `def test_source_create_valueerror_fixed(self, app)`
- Defined: `tests/test_security_remediation.py:208`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_source_update_valueerror_fixed `def test_source_update_valueerror_fixed(self, app)`
- Defined: `tests/test_security_remediation.py:232`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### app `def app(self)`
- Defined: `tests/test_security_remediation.py:264`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_redirect_uses_public_host_not_request_host `def test_redirect_uses_public_host_not_request_host(self, app)`
- Defined: `tests/test_security_remediation.py:271`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_redirect_scheme_is_https `def test_redirect_scheme_is_https(self, app)`
- Defined: `tests/test_security_remediation.py:285`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_ci_yml_has_permissions `def test_ci_yml_has_permissions(self)`
- Defined: `tests/test_security_remediation.py:309`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_ci_yml_permissions_is_read_all `def test_ci_yml_permissions_is_read_all(self)`
- Defined: `tests/test_security_remediation.py:325`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### app `def app(self)`
- Defined: `tests/test_security_remediation.py:340`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### _make_osiris_route_fixed `def _make_osiris_route_fixed(self, app, route_path)`
- Defined: `tests/test_security_remediation.py:347`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_osiris_exception_returns_generic `def test_osiris_exception_returns_generic(self, app)`
- Defined: `tests/test_security_remediation.py:386`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_redirect_implementation_uses_public_host `def test_redirect_implementation_uses_public_host(self)`
- Defined: `tests/test_security_remediation.py:402`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_source_has_no_url_replace `def test_source_has_no_url_replace(self)`
- Defined: `tests/test_security_remediation.py:418`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_js_file_exists `def test_js_file_exists(self)`
- Defined: `tests/test_security_remediation.py:436`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_innerhtml_not_used_with_template_literals `def test_innerhtml_not_used_with_template_literals(self)`
- Defined: `tests/test_security_remediation.py:439`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_showtooltipat_safe `def test_showtooltipat_safe(self)`
- Defined: `tests/test_security_remediation.py:459`
- Doc: showTooltipAt must sanitize html before innerHTML assignment.
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_selectnode_inspector_safe `def test_selectnode_inspector_safe(self)`
- Defined: `tests/test_security_remediation.py:473`
- Doc: selectNode must build DOM safely for the inspector panel.
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_refuses_link_local_metadata `def test_refuses_link_local_metadata(self)`
- Defined: `tests/test_security_remediation.py:502`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_refuses_loopback `def test_refuses_loopback(self)`
- Defined: `tests/test_security_remediation.py:507`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_refuses_disallowed_scheme `def test_refuses_disallowed_scheme(self)`
- Defined: `tests/test_security_remediation.py:511`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### test_user_channel_url_cannot_reach_internal_host `def test_user_channel_url_cannot_reach_internal_host(self)`
- Defined: `tests/test_security_remediation.py:515`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### api_export_test `def api_export_test()`
- Defined: `tests/test_security_remediation.py:97`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### api_export_fixed `def api_export_fixed()`
- Defined: `tests/test_security_remediation.py:130`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### api_delete `def api_delete(name)`
- Defined: `tests/test_security_remediation.py:191`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### api_create `def api_create()`
- Defined: `tests/test_security_remediation.py:212`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### api_update `def api_update(name)`
- Defined: `tests/test_security_remediation.py:236`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### fetch_bgp `def fetch_bgp(q)`
- Defined: `tests/test_security_remediation.py:354`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### fetch_mac `def fetch_mac(mac)`
- Defined: `tests/test_security_remediation.py:357`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### fetch_phone `def fetch_phone(n)`
- Defined: `tests/test_security_remediation.py:360`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### fetch_github_user `def fetch_github_user(u)`
- Defined: `tests/test_security_remediation.py:363`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### fetch_leaks `def fetch_leaks(e)`
- Defined: `tests/test_security_remediation.py:366`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

### osiris_endpoint `def osiris_endpoint()`
- Defined: `tests/test_security_remediation.py:376`
- Depends on: `estorides_core/alerter.py`, `estorides_core/ssrf_guard.py`, `estorides_core/web_security.py`

## tests/test_socmint.py

### youtube_response `def youtube_response()`
- Defined: `tests/test_socmint.py:40`
- Doc: Simulated YouTube Data API v3 response for @mkbhd.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### twitch_response `def twitch_response()`
- Defined: `tests/test_socmint.py:73`
- Doc: Simulated Twitch Helix API response for shroud.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### twitter_response `def twitter_response()`
- Defined: `tests/test_socmint.py:92`
- Doc: Simulated Twitter/X API v2 response for elonmusk.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### discord_response `def discord_response()`
- Defined: `tests/test_socmint.py:117`
- Doc: Simulated discords.com API search response.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_channel_id `def test_parser_returns_channel_id(self, youtube_response)`
- Defined: `tests/test_socmint.py:147`
- Doc: Given a valid YouTube channel response, the parser returns the channel_id.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_subscriber_count `def test_parser_returns_subscriber_count(self, youtube_response)`
- Defined: `tests/test_socmint.py:153`
- Doc: Given a valid YouTube channel response, the parser returns subscriber_count.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_metadata `def test_parser_returns_metadata(self, youtube_response)`
- Defined: `tests/test_socmint.py:160`
- Doc: Given a valid YouTube channel response, the parser returns title and description.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_empty_items_returns_not_found `def test_empty_items_returns_not_found(self)`
- Defined: `tests/test_socmint.py:177`
- Doc: Given an empty items list, the parser returns not_found.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_missing_items_returns_not_found `def test_missing_items_returns_not_found(self)`
- Defined: `tests/test_socmint.py:182`
- Doc: Given a response with no items key, the parser returns not_found.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_yaml_source_has_requires_key `def test_yaml_source_has_requires_key(self)`
- Defined: `tests/test_socmint.py:196`
- Doc: Given the youtube_user YAML source, requires_key is True.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_registered `def test_parser_registered(self)`
- Defined: `tests/test_socmint.py:209`
- Doc: Given the youtube_user source, its parser is registered.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_user_id `def test_parser_returns_user_id(self, twitch_response)`
- Defined: `tests/test_socmint.py:225`
- Doc: Given a valid Twitch response, the parser returns the user id.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_display_name `def test_parser_returns_display_name(self, twitch_response)`
- Defined: `tests/test_socmint.py:231`
- Doc: Given a valid Twitch response, the parser returns display_name.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_metadata `def test_parser_returns_metadata(self, twitch_response)`
- Defined: `tests/test_socmint.py:237`
- Doc: Given a valid Twitch response, the parser returns type and view_count.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_empty_data_returns_not_found `def test_empty_data_returns_not_found(self)`
- Defined: `tests/test_socmint.py:253`
- Doc: Given an empty data list, the parser returns not_found.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_error_response_returns_api_error `def test_error_response_returns_api_error(self)`
- Defined: `tests/test_socmint.py:258`
- Doc: Given an error response, the parser returns api_error with the detail message.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_missing_data_returns_not_found `def test_missing_data_returns_not_found(self)`
- Defined: `tests/test_socmint.py:268`
- Doc: Given a response with no data key, the parser returns not_found.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_username `def test_parser_returns_username(self, twitter_response)`
- Defined: `tests/test_socmint.py:282`
- Doc: Given a valid Twitter response, the parser returns username.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_followers_count `def test_parser_returns_followers_count(self, twitter_response)`
- Defined: `tests/test_socmint.py:288`
- Doc: Given a valid Twitter response, the parser returns followers_count.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_verified_flag `def test_parser_returns_verified_flag(self, twitter_response)`
- Defined: `tests/test_socmint.py:294`
- Doc: Given a valid Twitter response, the parser returns the verified flag.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_metadata `def test_parser_returns_metadata(self, twitter_response)`
- Defined: `tests/test_socmint.py:299`
- Doc: Given a valid Twitter response, the parser returns location and description.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_not_found_with_errors `def test_not_found_with_errors(self)`
- Defined: `tests/test_socmint.py:306`
- Doc: Given an error response with errors list, returns not_found.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_server_list `def test_parser_returns_server_list(self, discord_response)`
- Defined: `tests/test_socmint.py:322`
- Doc: Given a Discord server search response, the parser returns server list.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_server_names `def test_parser_returns_server_names(self, discord_response)`
- Defined: `tests/test_socmint.py:328`
- Doc: Given a Discord server search response, server names are correct.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_returns_member_counts `def test_parser_returns_member_counts(self, discord_response)`
- Defined: `tests/test_socmint.py:334`
- Doc: Given a Discord server search response, member counts are integers.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_empty_response `def test_empty_response(self)`
- Defined: `tests/test_socmint.py:341`
- Doc: Given an empty response, the parser returns empty results.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_none_response `def test_none_response(self)`
- Defined: `tests/test_socmint.py:347`
- Doc: Given a None response, the parser returns empty results.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_torvalds `def test_resolve_torvalds(self)`
- Defined: `tests/test_socmint.py:361`
- Doc: Given username 'torvalds', the inferer returns profiles across platforms.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_includes_keybase `def test_resolve_includes_keybase(self)`
- Defined: `tests/test_socmint.py:367`
- Doc: Given a username, Keybase appears in platform profiles.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_includes_github `def test_resolve_includes_github(self)`
- Defined: `tests/test_socmint.py:373`
- Doc: Given a username, GitHub appears in platform profiles.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_has_high_confidence_for_populated_username `def test_resolve_has_high_confidence_for_populated_username(self)`
- Defined: `tests/test_socmint.py:379`
- Doc: Given a common username, cross-platform confidence is above 0.5.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_linked_platforms_contains_keybase_note `def test_resolve_linked_platforms_contains_keybase_note(self)`
- Defined: `tests/test_socmint.py:386`
- Doc: Given a username, linked_platforms shows the Keybase proof chain.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_has_profile_urls `def test_resolve_has_profile_urls(self)`
- Defined: `tests/test_socmint.py:393`
- Doc: Given a username, each platform profile has a profile_url.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_empty_username `def test_empty_username(self)`
- Defined: `tests/test_socmint.py:409`
- Doc: Given an empty username, returns no_matches.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_none_username `def test_none_username(self)`
- Defined: `tests/test_socmint.py:414`
- Doc: Given None as username, returns no_matches.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_always_has_profile_count `def test_always_has_profile_count(self)`
- Defined: `tests/test_socmint.py:419`
- Doc: Given any username, total_platforms is the count of known platforms.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_platform_urls_are_valid `def test_platform_urls_are_valid(self)`
- Defined: `tests/test_socmint.py:427`
- Doc: Given any username, all profile URLs are valid templates.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_none_input `def test_none_input(self)`
- Defined: `tests/test_socmint.py:445`
- Doc: Given None input, returns error.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_list_input `def test_list_input(self)`
- Defined: `tests/test_socmint.py:450`
- Doc: Given a list instead of dict, returns error.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_string_input `def test_string_input(self)`
- Defined: `tests/test_socmint.py:455`
- Doc: Given a string instead of dict, returns error.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_missing_statistics `def test_missing_statistics(self)`
- Defined: `tests/test_socmint.py:460`
- Doc: Given a response without statistics, parser returns defaults gracefully.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_401_error `def test_401_error(self)`
- Defined: `tests/test_socmint.py:482`
- Doc: Given a 401 error response, returns api_error.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_none_input `def test_none_input(self)`
- Defined: `tests/test_socmint.py:491`
- Doc: Given None input, returns error.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_list_input `def test_list_input(self)`
- Defined: `tests/test_socmint.py:496`
- Doc: Given a list instead of dict, returns error.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_youtube_profile_extracts_person `def test_youtube_profile_extracts_person(self)`
- Defined: `tests/test_socmint.py:510`
- Doc: Given a YouTube channel with display_name, extract_structured yields a person.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_twitter_profile_extracts_person_and_username `def test_twitter_profile_extracts_person_and_username(self)`
- Defined: `tests/test_socmint.py:528`
- Doc: Given a Twitter parser output, extract_structured yields person/username entities.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_social_media_urls_in_text `def test_social_media_urls_in_text(self)`
- Defined: `tests/test_socmint.py:548`
- Doc: Given text containing social URLs, the inferer discovers cross-platform links.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_discover_empty_text `def test_discover_empty_text(self)`
- Defined: `tests/test_socmint.py:558`
- Doc: Given empty text, discover_from_text returns empty.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_discover_no_urls `def test_discover_no_urls(self)`
- Defined: `tests/test_socmint.py:563`
- Doc: Given text without URLs, discover_from_text returns empty.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_platform_list_returns_all `def test_platform_list_returns_all(self)`
- Defined: `tests/test_socmint.py:577`
- Doc: Given the inferer, platform_list returns all known platforms.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_platform_list_has_required_fields `def test_platform_list_has_required_fields(self)`
- Defined: `tests/test_socmint.py:583`
- Doc: Given the platform list, every entry has the core fields.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_single_platform `def test_resolve_single_platform(self)`
- Defined: `tests/test_socmint.py:596`
- Doc: Given a specific platform filter, only that platform appears.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_multiple_platforms `def test_resolve_multiple_platforms(self)`
- Defined: `tests/test_socmint.py:602`
- Doc: Given a list of platforms, only those platforms appear.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_resolve_validates_twitter_requires_key `def test_resolve_validates_twitter_requires_key(self)`
- Defined: `tests/test_socmint.py:609`
- Doc: Given the inferer resolve, Twitter profiles are marked as requiring key.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_handles_none `def test_parser_handles_none(self, parser_fn)`
- Defined: `tests/test_socmint.py:631`
- Doc: Given None input, the parser does not raise.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_handles_int `def test_parser_handles_int(self, parser_fn)`
- Defined: `tests/test_socmint.py:645`
- Doc: Given int input, the parser does not raise.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

### test_parser_handles_string `def test_parser_handles_string(self, parser_fn)`
- Defined: `tests/test_socmint.py:659`
- Doc: Given string input, the parser does not raise.
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/parsers.py`, `estorides_core/socmint.py`, `estorides_core/source_loader.py`

## tests/test_source_health_monitoring.py

### test_healthy_status `def test_healthy_status(self)`
- Defined: `tests/test_source_health_monitoring.py:32`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_success_rate_computed `def test_success_rate_computed(self)`
- Defined: `tests/test_source_health_monitoring.py:44`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_avg_latency_computed `def test_avg_latency_computed(self)`
- Defined: `tests/test_source_health_monitoring.py:56`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_freshness_hours_computed `def test_freshness_hours_computed(self)`
- Defined: `tests/test_source_health_monitoring.py:68`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_health_score_high_band `def test_health_score_high_band(self)`
- Defined: `tests/test_source_health_monitoring.py:80`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_degrading_status `def test_degrading_status(self)`
- Defined: `tests/test_source_health_monitoring.py:100`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_success_rate_reflects_failures `def test_success_rate_reflects_failures(self)`
- Defined: `tests/test_source_health_monitoring.py:112`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_health_score_low_band `def test_health_score_low_band(self)`
- Defined: `tests/test_source_health_monitoring.py:124`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_degrading_status_for_latency `def test_degrading_status_for_latency(self)`
- Defined: `tests/test_source_health_monitoring.py:144`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_avg_latency_high `def test_avg_latency_high(self)`
- Defined: `tests/test_source_health_monitoring.py:156`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_health_score_penalised `def test_health_score_penalised(self)`
- Defined: `tests/test_source_health_monitoring.py:168`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_stale_status `def test_stale_status(self)`
- Defined: `tests/test_source_health_monitoring.py:189`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_freshness_hours_exceeds_stale `def test_freshness_hours_exceeds_stale(self)`
- Defined: `tests/test_source_health_monitoring.py:201`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_unknown_status `def test_unknown_status(self)`
- Defined: `tests/test_source_health_monitoring.py:220`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_zero_fetches_is_unknown `def test_zero_fetches_is_unknown(self)`
- Defined: `tests/test_source_health_monitoring.py:232`
- Depends on: `estorides_core/source_health_monitoring.py`

### _healthy `def _healthy(name)`
- Defined: `tests/test_source_health_monitoring.py:252`
- Depends on: `estorides_core/source_health_monitoring.py`

### _degrading `def _degrading(name)`
- Defined: `tests/test_source_health_monitoring.py:263`
- Depends on: `estorides_core/source_health_monitoring.py`

### _stale `def _stale(name)`
- Defined: `tests/test_source_health_monitoring.py:274`
- Depends on: `estorides_core/source_health_monitoring.py`

### _unknown `def _unknown(name)`
- Defined: `tests/test_source_health_monitoring.py:285`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_hot_sources_are_healthy `def test_hot_sources_are_healthy(self)`
- Defined: `tests/test_source_health_monitoring.py:295`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_degrading_includes_degrading_and_stale `def test_degrading_includes_degrading_and_stale(self)`
- Defined: `tests/test_source_health_monitoring.py:306`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_unknown_sources_separate `def test_unknown_sources_separate(self)`
- Defined: `tests/test_source_health_monitoring.py:319`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_summary_counts `def test_summary_counts(self)`
- Defined: `tests/test_source_health_monitoring.py:329`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_ok_exceeds_fetch_raises `def test_ok_exceeds_fetch_raises(self)`
- Defined: `tests/test_source_health_monitoring.py:351`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_negative_fetch_raises `def test_negative_fetch_raises(self)`
- Defined: `tests/test_source_health_monitoring.py:362`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_negative_latency_raises `def test_negative_latency_raises(self)`
- Defined: `tests/test_source_health_monitoring.py:373`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_empty_name_raises `def test_empty_name_raises(self)`
- Defined: `tests/test_source_health_monitoring.py:384`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_config_min_fetches_less_than_one_raises `def test_config_min_fetches_less_than_one_raises(self)`
- Defined: `tests/test_source_health_monitoring.py:395`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_config_stale_hours_zero_raises `def test_config_stale_hours_zero_raises(self)`
- Defined: `tests/test_source_health_monitoring.py:399`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_config_degrading_rate_out_of_range_raises `def test_config_degrading_rate_out_of_range_raises(self)`
- Defined: `tests/test_source_health_monitoring.py:403`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_compute_health_is_pure `def test_compute_health_is_pure(self)`
- Defined: `tests/test_source_health_monitoring.py:414`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_build_dashboard_is_pure `def test_build_dashboard_is_pure(self)`
- Defined: `tests/test_source_health_monitoring.py:428`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_perfect_source_scores_one `def test_perfect_source_scores_one(self)`
- Defined: `tests/test_source_health_monitoring.py:444`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_broken_source_scores_low `def test_broken_source_scores_low(self)`
- Defined: `tests/test_source_health_monitoring.py:456`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_status_is_enum `def test_status_is_enum(self)`
- Defined: `tests/test_source_health_monitoring.py:475`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_health_input_is_dataclass `def test_health_input_is_dataclass(self)`
- Defined: `tests/test_source_health_monitoring.py:495`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_health_result_is_dataclass `def test_health_result_is_dataclass(self)`
- Defined: `tests/test_source_health_monitoring.py:498`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_config_is_dataclass `def test_config_is_dataclass(self)`
- Defined: `tests/test_source_health_monitoring.py:501`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_dashboard_is_dataclass `def test_dashboard_is_dataclass(self)`
- Defined: `tests/test_source_health_monitoring.py:505`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_result_to_dict `def test_result_to_dict(self)`
- Defined: `tests/test_source_health_monitoring.py:508`
- Depends on: `estorides_core/source_health_monitoring.py`

### test_dashboard_to_dict `def test_dashboard_to_dict(self)`
- Defined: `tests/test_source_health_monitoring.py:523`
- Depends on: `estorides_core/source_health_monitoring.py`

## tests/test_supply_chain.py

### test_cloudflare_cdn_detected `def test_cloudflare_cdn_detected(self)`
- Defined: `tests/test_supply_chain.py:19`
- Depends on: `estorides_core/supply_chain.py`

### test_google_workspace_mx_detected `def test_google_workspace_mx_detected(self)`
- Defined: `tests/test_supply_chain.py:37`
- Depends on: `estorides_core/supply_chain.py`

### test_microsoft_365_mx_detected `def test_microsoft_365_mx_detected(self)`
- Defined: `tests/test_supply_chain.py:51`
- Depends on: `estorides_core/supply_chain.py`

### test_empty_when_self_hosted `def test_empty_when_self_hosted(self)`
- Defined: `tests/test_supply_chain.py:67`
- Depends on: `estorides_core/supply_chain.py`

### test_asn_sharing_detected `def test_asn_sharing_detected(self)`
- Defined: `tests/test_supply_chain.py:75`
- Depends on: `estorides_core/supply_chain.py`

### test_no_http_to_third_parties `def test_no_http_to_third_parties(self)`
- Defined: `tests/test_supply_chain.py:96`
- Depends on: `estorides_core/supply_chain.py`

### test_subsidiary_relationship `def test_subsidiary_relationship(self)`
- Defined: `tests/test_supply_chain.py:114`
- Depends on: `estorides_core/supply_chain.py`

### test_lets_encrypt_not_flagged `def test_lets_encrypt_not_flagged(self)`
- Defined: `tests/test_supply_chain.py:134`
- Depends on: `estorides_core/supply_chain.py`

### test_godaddy_registrar `def test_godaddy_registrar(self)`
- Defined: `tests/test_supply_chain.py:149`
- Depends on: `estorides_core/supply_chain.py`

## tests/test_system_app_sources.py

### _stub_runner `def _stub_runner(exit_code, stdout, stderr, error_code, error_message, on_run)`
- Defined: `tests/test_system_app_sources.py:48`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### stub `def stub(binary, args)`
- Defined: `tests/test_system_app_sources.py:52`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_execute_renders_query_and_parses_found_lines `def test_execute_renders_query_and_parses_found_lines(self)`
- Defined: `tests/test_system_app_sources.py:80`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_execute_returns_source_and_tool_metadata `def test_execute_returns_source_and_tool_metadata(self)`
- Defined: `tests/test_system_app_sources.py:105`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_execute_reports_tool_not_found `def test_execute_reports_tool_not_found(self, monkeypatch)`
- Defined: `tests/test_system_app_sources.py:120`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_execute_reports_missing_binary_declaration `def test_execute_reports_missing_binary_declaration(self)`
- Defined: `tests/test_system_app_sources.py:130`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_execute_rejects_non_allowlisted_binary `def test_execute_rejects_non_allowlisted_binary(self, monkeypatch)`
- Defined: `tests/test_system_app_sources.py:136`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_nonzero_exit_keeps_parsed_output `def test_nonzero_exit_keeps_parsed_output(self)`
- Defined: `tests/test_system_app_sources.py:152`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_metachar_arg_is_rejected_by_tool_runner `def test_metachar_arg_is_rejected_by_tool_runner(self, monkeypatch)`
- Defined: `tests/test_system_app_sources.py:172`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_file_output_is_parsed_and_outdir_cleaned `def test_file_output_is_parsed_and_outdir_cleaned(self, monkeypatch)`
- Defined: `tests/test_system_app_sources.py:208`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_stdout_json_is_parsed_when_no_file `def test_stdout_json_is_parsed_when_no_file(self, monkeypatch)`
- Defined: `tests/test_system_app_sources.py:235`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_query_and_outdir_substituted `def test_query_and_outdir_substituted(self)`
- Defined: `tests/test_system_app_sources.py:255`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_unknown_tokens_survive `def test_unknown_tokens_survive(self)`
- Defined: `tests/test_system_app_sources.py:259`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_non_string_arg_raises `def test_non_string_arg_raises(self)`
- Defined: `tests/test_system_app_sources.py:263`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_passive_only_drops_touching_tools_even_by_name `def test_passive_only_drops_touching_tools_even_by_name(self)`
- Defined: `tests/test_system_app_sources.py:273`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### _load `def _load(self, tmp_path, yaml_text)`
- Defined: `tests/test_system_app_sources.py:307`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_kind_and_output_format_normalise `def test_kind_and_output_format_normalise(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:329`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_kind_derived_from_binary_when_omitted `def test_kind_derived_from_binary_when_omitted(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:336`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_http_source_gets_http_kind_by_default `def test_http_source_gets_http_kind_by_default(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:341`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_bad_output_format_falls_back_to_text `def test_bad_output_format_falls_back_to_text(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:352`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_non_string_args_reset `def test_non_string_args_reset(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:359`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_unknown_kind_derives_from_block `def test_unknown_kind_derives_from_block(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:366`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_summary_exposes_kind `def test_summary_exposes_kind(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:371`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_real_kali_yamls_load_as_system_app `def test_real_kali_yamls_load_as_system_app(self)`
- Defined: `tests/test_system_app_sources.py:376`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_write_source_file_roundtrip_keeps_system_app_block `def test_write_source_file_roundtrip_keeps_system_app_block(self, tmp_path)`
- Defined: `tests/test_system_app_sources.py:395`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_timeout_error_is_propagated `def test_timeout_error_is_propagated(self, monkeypatch)`
- Defined: `tests/test_system_app_sources.py:409`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### test_binary_branch_runs_in_worker_thread `def test_binary_branch_runs_in_worker_thread(self, monkeypatch)`
- Defined: `tests/test_system_app_sources.py:434`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### on_run `def on_run(binary, args)`
- Defined: `tests/test_system_app_sources.py:83`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### on_run `def on_run(binary, args)`
- Defined: `tests/test_system_app_sources.py:214`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### timeout_runner `def timeout_runner(binary, args)`
- Defined: `tests/test_system_app_sources.py:414`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### slow_execute `def slow_execute(source, query)`
- Defined: `tests/test_system_app_sources.py:444`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

### scenario `def scenario()`
- Defined: `tests/test_system_app_sources.py:463`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

## tests/test_target_management.py

### test_valid_target_returns_result `def test_valid_target_returns_result(self)`
- Defined: `tests/test_target_management.py:22`

### test_has_case_id `def test_has_case_id(self)`
- Defined: `tests/test_target_management.py:30`

### test_id_deterministic `def test_id_deterministic(self)`
- Defined: `tests/test_target_management.py:35`

### test_ipv4_auto `def test_ipv4_auto(self)`
- Defined: `tests/test_target_management.py:47`

### test_ipv6_auto `def test_ipv6_auto(self)`
- Defined: `tests/test_target_management.py:52`

### test_email_auto `def test_email_auto(self)`
- Defined: `tests/test_target_management.py:57`

### test_cve_auto `def test_cve_auto(self)`
- Defined: `tests/test_target_management.py:62`

### test_btc_auto `def test_btc_auto(self)`
- Defined: `tests/test_target_management.py:67`

### test_eth_auto `def test_eth_auto(self)`
- Defined: `tests/test_target_management.py:72`

### test_domain_auto `def test_domain_auto(self)`
- Defined: `tests/test_target_management.py:77`

### test_username_fallback `def test_username_fallback(self)`
- Defined: `tests/test_target_management.py:82`

### test_phone_auto `def test_phone_auto(self)`
- Defined: `tests/test_target_management.py:87`

### test_asn_auto `def test_asn_auto(self)`
- Defined: `tests/test_target_management.py:92`

### test_md5_auto `def test_md5_auto(self)`
- Defined: `tests/test_target_management.py:97`

### test_sha256_auto `def test_sha256_auto(self)`
- Defined: `tests/test_target_management.py:102`

### test_invalid_email `def test_invalid_email(self)`
- Defined: `tests/test_target_management.py:114`

### test_invalid_ipv4 `def test_invalid_ipv4(self)`
- Defined: `tests/test_target_management.py:119`

### test_invalid_domain_script `def test_invalid_domain_script(self)`
- Defined: `tests/test_target_management.py:123`

### test_invalid_url `def test_invalid_url(self)`
- Defined: `tests/test_target_management.py:127`

### test_invalid_phone `def test_invalid_phone(self)`
- Defined: `tests/test_target_management.py:131`

### test_unknown_type `def test_unknown_type(self)`
- Defined: `tests/test_target_management.py:141`

### test_unknown_type_via_manager `def test_unknown_type_via_manager(self)`
- Defined: `tests/test_target_management.py:146`

### test_empty_raises `def test_empty_raises(self)`
- Defined: `tests/test_target_management.py:157`

### test_whitespace_raises `def test_whitespace_raises(self)`
- Defined: `tests/test_target_management.py:161`

### test_validate_value_empty `def test_validate_value_empty(self)`
- Defined: `tests/test_target_management.py:165`

### test_ephemeral_no_case_store `def test_ephemeral_no_case_store(self)`
- Defined: `tests/test_target_management.py:175`

### test_mixed_batch `def test_mixed_batch(self)`
- Defined: `tests/test_target_management.py:187`

### test_simple_lines_no_type `def test_simple_lines_no_type(self)`
- Defined: `tests/test_target_management.py:201`

### test_exceeds_max `def test_exceeds_max(self)`
- Defined: `tests/test_target_management.py:212`

### test_at_max `def test_at_max(self)`
- Defined: `tests/test_target_management.py:217`

### test_script_in_domain_rejected `def test_script_in_domain_rejected(self)`
- Defined: `tests/test_target_management.py:229`

### test_onclick_in_domain_rejected `def test_onclick_in_domain_rejected(self)`
- Defined: `tests/test_target_management.py:233`

### test_sql_injection_in_email_rejected `def test_sql_injection_in_email_rejected(self)`
- Defined: `tests/test_target_management.py:237`

### test_same_id `def test_same_id(self)`
- Defined: `tests/test_target_management.py:247`

### test_same_id_normalised `def test_same_id_normalised(self)`
- Defined: `tests/test_target_management.py:255`

### test_valid_types_pass `def test_valid_types_pass(self)`
- Defined: `tests/test_target_management.py:267`

### test_auto_passes `def test_auto_passes(self)`
- Defined: `tests/test_target_management.py:272`

### test_invalid_fails `def test_invalid_fails(self)`
- Defined: `tests/test_target_management.py:275`

### test_domain_valid `def test_domain_valid(self)`
- Defined: `tests/test_target_management.py:281`

### test_domain_invalid `def test_domain_invalid(self)`
- Defined: `tests/test_target_management.py:285`

### test_ipv4_valid `def test_ipv4_valid(self)`
- Defined: `tests/test_target_management.py:289`

### test_ipv4_invalid_octet `def test_ipv4_invalid_octet(self)`
- Defined: `tests/test_target_management.py:293`

### test_email_valid `def test_email_valid(self)`
- Defined: `tests/test_target_management.py:297`

### test_url_only_http_https `def test_url_only_http_https(self)`
- Defined: `tests/test_target_management.py:301`

### test_username_no_regex `def test_username_no_regex(self)`
- Defined: `tests/test_target_management.py:306`

### test_cve_valid `def test_cve_valid(self)`
- Defined: `tests/test_target_management.py:310`

### test_btc_valid `def test_btc_valid(self)`
- Defined: `tests/test_target_management.py:313`

### test_eth_valid `def test_eth_valid(self)`
- Defined: `tests/test_target_management.py:316`

### test_phone_valid `def test_phone_valid(self)`
- Defined: `tests/test_target_management.py:319`

### test_asn_valid `def test_asn_valid(self)`
- Defined: `tests/test_target_management.py:322`

### test_md5_valid `def test_md5_valid(self)`
- Defined: `tests/test_target_management.py:325`

### test_sha256_valid `def test_sha256_valid(self)`
- Defined: `tests/test_target_management.py:328`

### test_length `def test_length(self)`
- Defined: `tests/test_target_management.py:334`

### test_deterministic `def test_deterministic(self)`
- Defined: `tests/test_target_management.py:337`

### test_case_sensitive_normalised `def test_case_sensitive_normalised(self)`
- Defined: `tests/test_target_management.py:340`

### test_ipv4 `def test_ipv4(self)`
- Defined: `tests/test_target_management.py:345`

### test_ipv6 `def test_ipv6(self)`
- Defined: `tests/test_target_management.py:348`

### test_email `def test_email(self)`
- Defined: `tests/test_target_management.py:351`

### test_domain `def test_domain(self)`
- Defined: `tests/test_target_management.py:354`

### test_url `def test_url(self)`
- Defined: `tests/test_target_management.py:357`

### test_cve `def test_cve(self)`
- Defined: `tests/test_target_management.py:360`

### test_username_fallback `def test_username_fallback(self)`
- Defined: `tests/test_target_management.py:363`

### test_to_dict `def test_to_dict(self)`
- Defined: `tests/test_target_management.py:368`

### test_to_dict `def test_to_dict(self)`
- Defined: `tests/test_target_management.py:380`

### test_to_dict_invalid `def test_to_dict_invalid(self)`
- Defined: `tests/test_target_management.py:397`

### test_basic_csv `def test_basic_csv(self)`
- Defined: `tests/test_target_management.py:411`

### test_csv_invalid `def test_csv_invalid(self)`
- Defined: `tests/test_target_management.py:418`

### test_csv_max_batch `def test_csv_max_batch(self)`
- Defined: `tests/test_target_management.py:425`

### test_csv_exceeds_max `def test_csv_exceeds_max(self)`
- Defined: `tests/test_target_management.py:431`

## tests/test_target_scoring.py

### _make_target `def _make_target(domain, surface, soft, jewel, lateral)`
- Defined: `tests/test_target_scoring.py:17`

### test_open_bucket_and_old_nginx_ranked_critical `def test_open_bucket_and_old_nginx_ranked_critical(self)`
- Defined: `tests/test_target_scoring.py:37`

### test_no_findings_is_noise `def test_no_findings_is_noise(self)`
- Defined: `tests/test_target_scoring.py:45`

### test_5_targets_various_tiers `def test_5_targets_various_tiers(self)`
- Defined: `tests/test_target_scoring.py:53`

### test_custom_weights_change_score `def test_custom_weights_change_score(self)`
- Defined: `tests/test_target_scoring.py:71`

### test_jenkins_jira_vpn_get_high_jewel_score `def test_jenkins_jira_vpn_get_high_jewel_score(self)`
- Defined: `tests/test_target_scoring.py:83`

### test_blog_low_jewel_score `def test_blog_low_jewel_score(self)`
- Defined: `tests/test_target_scoring.py:88`

### test_partial_data_lower_confidence `def test_partial_data_lower_confidence(self)`
- Defined: `tests/test_target_scoring.py:95`

### test_password_reuse_increases_lateral `def test_password_reuse_increases_lateral(self)`
- Defined: `tests/test_target_scoring.py:102`

### test_serialised_output_no_credentials `def test_serialised_output_no_credentials(self)`
- Defined: `tests/test_target_scoring.py:109`

## tests/test_tech_fingerprint.py

### test_detects_nginx_php_jquery `def test_detects_nginx_php_jquery(self)`
- Defined: `tests/test_tech_fingerprint.py:16`
- Depends on: `estorides_core/tech_fingerprint.py`

### test_returns_empty_on_no_input `def test_returns_empty_on_no_input(self)`
- Defined: `tests/test_tech_fingerprint.py:32`
- Depends on: `estorides_core/tech_fingerprint.py`

### test_handles_binary_garbage_in_version `def test_handles_binary_garbage_in_version(self)`
- Defined: `tests/test_tech_fingerprint.py:40`
- Depends on: `estorides_core/tech_fingerprint.py`

### test_does_not_parse_script_as_tech `def test_does_not_parse_script_as_tech(self)`
- Defined: `tests/test_tech_fingerprint.py:50`
- Depends on: `estorides_core/tech_fingerprint.py`

### test_detects_cloudflare_from_headers `def test_detects_cloudflare_from_headers(self)`
- Defined: `tests/test_tech_fingerprint.py:59`
- Depends on: `estorides_core/tech_fingerprint.py`

### test_detects_wordpress_from_meta `def test_detects_wordpress_from_meta(self)`
- Defined: `tests/test_tech_fingerprint.py:70`
- Depends on: `estorides_core/tech_fingerprint.py`

### test_same_tech_from_multiple_signals_appears_once `def test_same_tech_from_multiple_signals_appears_once(self)`
- Defined: `tests/test_tech_fingerprint.py:81`
- Depends on: `estorides_core/tech_fingerprint.py`

### test_only_processes_first_100kb `def test_only_processes_first_100kb(self)`
- Defined: `tests/test_tech_fingerprint.py:91`
- Depends on: `estorides_core/tech_fingerprint.py`

## tests/test_tool_install.py

### no_network `def no_network()`
- Defined: `tests/test_tool_install.py:17`
- Doc: Make every _run call a no-op success so tests never touch the network.
- Depends on: `estorides_core/tool_install.py`

### test_recipe_available_for_known_tool `def test_recipe_available_for_known_tool(self)`
- Defined: `tests/test_tool_install.py:25`
- Depends on: `estorides_core/tool_install.py`

### test_recipe_unavailable_for_unknown_tool `def test_recipe_unavailable_for_unknown_tool(self)`
- Defined: `tests/test_tool_install.py:28`
- Depends on: `estorides_core/tool_install.py`

### test_load_apt_recipe `def test_load_apt_recipe(self)`
- Defined: `tests/test_tool_install.py:31`
- Depends on: `estorides_core/tool_install.py`

### test_load_git_recipe `def test_load_git_recipe(self)`
- Defined: `tests/test_tool_install.py:35`
- Depends on: `estorides_core/tool_install.py`

### test_list_recipes_is_nonempty `def test_list_recipes_is_nonempty(self)`
- Defined: `tests/test_tool_install.py:39`
- Depends on: `estorides_core/tool_install.py`

### test_run0_preferred_over_sudo `def test_run0_preferred_over_sudo(self)`
- Defined: `tests/test_tool_install.py:45`
- Depends on: `estorides_core/tool_install.py`

### test_sudo_fallback_when_no_run0 `def test_sudo_fallback_when_no_run0(self)`
- Defined: `tests/test_tool_install.py:50`
- Depends on: `estorides_core/tool_install.py`

### test_no_elevation_when_root `def test_no_elevation_when_root(self)`
- Defined: `tests/test_tool_install.py:55`
- Depends on: `estorides_core/tool_install.py`

### test_already_installed_noop `def test_already_installed_noop(self, no_network)`
- Defined: `tests/test_tool_install.py:62`
- Depends on: `estorides_core/tool_install.py`

### test_not_in_allowlist_rejected `def test_not_in_allowlist_rejected(self)`
- Defined: `tests/test_tool_install.py:67`
- Depends on: `estorides_core/tool_install.py`

### test_no_recipe_rejected `def test_no_recipe_rejected(self)`
- Defined: `tests/test_tool_install.py:72`
- Depends on: `estorides_core/tool_install.py`

### test_apt_install_success `def test_apt_install_success(self)`
- Defined: `tests/test_tool_install.py:78`
- Depends on: `estorides_core/tool_install.py`

### test_verify_fails_after_install `def test_verify_fails_after_install(self, no_network)`
- Defined: `tests/test_tool_install.py:89`
- Depends on: `estorides_core/tool_install.py`

### test_git_install_runs_clone `def test_git_install_runs_clone(self)`
- Defined: `tests/test_tool_install.py:95`
- Depends on: `estorides_core/tool_install.py`

## tests/test_tool_runner.py

### test_run_tool_returns_result `def test_run_tool_returns_result(self)`
- Defined: `tests/test_tool_runner.py:21`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_semicolon_in_arg_rejected `def test_semicolon_in_arg_rejected(self)`
- Defined: `tests/test_tool_runner.py:30`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_pipe_in_arg_rejected `def test_pipe_in_arg_rejected(self)`
- Defined: `tests/test_tool_runner.py:40`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_backtick_in_arg_rejected `def test_backtick_in_arg_rejected(self)`
- Defined: `tests/test_tool_runner.py:50`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_dollar_paren_in_arg_rejected `def test_dollar_paren_in_arg_rejected(self)`
- Defined: `tests/test_tool_runner.py:60`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_newline_in_arg_rejected `def test_newline_in_arg_rejected(self)`
- Defined: `tests/test_tool_runner.py:70`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_tool_that_exceeds_timeout_returns_tool_timeout `def test_tool_that_exceeds_timeout_returns_tool_timeout(self)`
- Defined: `tests/test_tool_runner.py:82`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_tool_not_on_filesystem_returns_error `def test_tool_not_on_filesystem_returns_error(self)`
- Defined: `tests/test_tool_runner.py:97`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_disallowed_tool_rejected `def test_disallowed_tool_rejected(self)`
- Defined: `tests/test_tool_runner.py:118`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_empty_args_returns_error `def test_empty_args_returns_error(self)`
- Defined: `tests/test_tool_runner.py:130`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_control_char_rejected_by_validation `def test_control_char_rejected_by_validation(self)`
- Defined: `tests/test_tool_runner.py:142`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_nmap_version_query_succeeds `def test_nmap_version_query_succeeds(self)`
- Defined: `tests/test_tool_runner.py:148`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_sha1_is_valid_hex `def test_sha1_is_valid_hex(self)`
- Defined: `tests/test_tool_runner.py:157`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_confidence_in_bounds `def test_confidence_in_bounds(self)`
- Defined: `tests/test_tool_runner.py:165`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_truncated_flag_when_output_exceeds_limit `def test_truncated_flag_when_output_exceeds_limit(self)`
- Defined: `tests/test_tool_runner.py:172`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_error_result_has_fields `def test_error_result_has_fields(self)`
- Defined: `tests/test_tool_runner.py:185`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

### test_injection_error_has_fields `def test_injection_error_has_fields(self)`
- Defined: `tests/test_tool_runner.py:206`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`, `estorides_core/validation.py`

## tests/test_ui_professional.py

### _render_index `def _render_index()`
- Defined: `tests/test_ui_professional.py:27`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### _simulate_tiered_data `def _simulate_tiered_data()`
- Defined: `tests/test_ui_professional.py:39`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_loading_elements_exist `def test_loading_elements_exist(self)`
- Defined: `tests/test_ui_professional.py:67`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_loading_css_defined `def test_loading_css_defined(self)`
- Defined: `tests/test_ui_professional.py:74`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_js_show_working_indicator_exists `def test_js_show_working_indicator_exists(self)`
- Defined: `tests/test_ui_professional.py:83`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_critical_tier_data `def test_critical_tier_data(self)`
- Defined: `tests/test_ui_professional.py:96`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_critical_css_classes_exist `def test_critical_css_classes_exist(self)`
- Defined: `tests/test_ui_professional.py:105`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_noise_tier_data `def test_noise_tier_data(self)`
- Defined: `tests/test_ui_professional.py:120`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_noise_css_classes_exist `def test_noise_css_classes_exist(self)`
- Defined: `tests/test_ui_professional.py:127`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_js_toggle_function_exists `def test_js_toggle_function_exists(self)`
- Defined: `tests/test_ui_professional.py:134`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_aria_attributes_in_js `def test_aria_attributes_in_js(self)`
- Defined: `tests/test_ui_professional.py:144`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_toggle_uses_role_button `def test_toggle_uses_role_button(self)`
- Defined: `tests/test_ui_professional.py:149`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_js_fallback_logic `def test_js_fallback_logic(self)`
- Defined: `tests/test_ui_professional.py:158`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_tiers_missing_returns_empty `def test_tiers_missing_returns_empty(self)`
- Defined: `tests/test_ui_professional.py:163`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_show_toast_exists `def test_show_toast_exists(self)`
- Defined: `tests/test_ui_professional.py:176`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_tier_group_hover_css `def test_tier_group_hover_css(self)`
- Defined: `tests/test_ui_professional.py:185`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_transition_on_tier_group `def test_transition_on_tier_group(self)`
- Defined: `tests/test_ui_professional.py:189`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_fade_in_css_exists `def test_fade_in_css_exists(self)`
- Defined: `tests/test_ui_professional.py:198`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_results_use_fade_in `def test_results_use_fade_in(self)`
- Defined: `tests/test_ui_professional.py:203`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_no_inline_style_in_tier_badge `def test_no_inline_style_in_tier_badge(self)`
- Defined: `tests/test_ui_professional.py:212`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_no_inline_style_in_template `def test_no_inline_style_in_template(self)`
- Defined: `tests/test_ui_professional.py:222`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_no_onclick_attributes `def test_no_onclick_attributes(self)`
- Defined: `tests/test_ui_professional.py:233`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_escape_html_function_exists `def test_escape_html_function_exists(self)`
- Defined: `tests/test_ui_professional.py:245`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_escape_html_properly_defined `def test_escape_html_properly_defined(self)`
- Defined: `tests/test_ui_professional.py:249`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_tier_label_uses_text_content `def test_tier_label_uses_text_content(self)`
- Defined: `tests/test_ui_professional.py:254`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_tier_summary_accuracy `def test_tier_summary_accuracy(self)`
- Defined: `tests/test_ui_professional.py:263`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_every_group_has_required_fields `def test_every_group_has_required_fields(self)`
- Defined: `tests/test_ui_professional.py:268`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

### test_scores_are_normalised `def test_scores_are_normalised(self)`
- Defined: `tests/test_ui_professional.py:280`
- Depends on: `estorides_core/recon_fusion.py`, `estorides_core/search_telemetry.py`

## tests/test_vuln_correlation.py

### _make_tech `def _make_tech(name, version)`
- Defined: `tests/test_vuln_correlation.py:16`
- Depends on: `estorides_core/vuln_correlation.py`

### test_returns_cves_for_nginx `def test_returns_cves_for_nginx(self)`
- Defined: `tests/test_vuln_correlation.py:22`
- Depends on: `estorides_core/vuln_correlation.py`

### test_apache_struts_has_metasploit `def test_apache_struts_has_metasploit(self)`
- Defined: `tests/test_vuln_correlation.py:32`
- Depends on: `estorides_core/vuln_correlation.py`

### test_unknown_tech_returns_empty `def test_unknown_tech_returns_empty(self)`
- Defined: `tests/test_vuln_correlation.py:42`
- Depends on: `estorides_core/vuln_correlation.py`

### test_jenkins_has_default_admin `def test_jenkins_has_default_admin(self)`
- Defined: `tests/test_vuln_correlation.py:51`
- Depends on: `estorides_core/vuln_correlation.py`

### test_most_critical_is_highest_cvss `def test_most_critical_is_highest_cvss(self)`
- Defined: `tests/test_vuln_correlation.py:63`
- Depends on: `estorides_core/vuln_correlation.py`

### test_no_version_reduces_confidence `def test_no_version_reduces_confidence(self)`
- Defined: `tests/test_vuln_correlation.py:72`
- Depends on: `estorides_core/vuln_correlation.py`

### test_exploit_available_increases_score `def test_exploit_available_increases_score(self)`
- Defined: `tests/test_vuln_correlation.py:82`
- Depends on: `estorides_core/vuln_correlation.py`

### test_known_tech_in_local_table `def test_known_tech_in_local_table(self)`
- Defined: `tests/test_vuln_correlation.py:95`
- Depends on: `estorides_core/vuln_correlation.py`

## tools/split_sources.py

### main `def main()`
- Defined: `tools/split_sources.py:19`
