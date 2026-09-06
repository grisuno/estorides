# Subsystem: root

## _multi_test.sh
- Layer: testing
- Language: sh

## _test_entity_resolution.py
- Layer: testing
- Language: py
- Symbols:
  - `check` (function, line 27) `def check(name, cond, detail)`
  - `_ent` (function, line 36) `def _ent(etype, value, source)`
  - `_by_value` (function, line 40) `def _by_value(result, value)`
  - `test_transliteration` (function, line 47) `def test_transliteration()`
  - `test_jaro_winkler` (function, line 63) `def test_jaro_winkler()`
  - `test_normalization` (function, line 74) `def test_normalization()`
  - `test_score_pair_policy` (function, line 98) `def test_score_pair_policy()`
  - `test_resolution_merge` (function, line 111) `def test_resolution_merge()`
  - `test_to_entity_roundtrip` (function, line 167) `def test_to_entity_roundtrip()`
  - `test_cross_run_stability` (function, line 182) `def test_cross_run_stability()`
  - `test_empty_and_edge_inputs` (function, line 211) `def test_empty_and_edge_inputs()`
  - `main` (function, line 219) `def main()`
- Depends on: `estorides_core/entity_extraction.py`, `estorides_core/entity_resolution.py`, `estorides_core/entity_store.py`, `estorides_core/transliteration.py`

## _test_fusion.py
- Layer: testing
- Language: py
- Symbols:
  - `check` (function, line 24) `def check(label, cond)`
  - `_fresh_store` (function, line 32) `def _fresh_store()`
  - `test_deterministic_identity` (function, line 37) `def test_deterministic_identity()`
  - `test_cross_run_dedup_and_provenance` (function, line 45) `def test_cross_run_dedup_and_provenance()`
  - `test_property_corroboration_and_conflict` (function, line 59) `def test_property_corroboration_and_conflict()`
  - `test_min_sources_filter` (function, line 76) `def test_min_sources_filter()`
  - `test_relationship_fusion` (function, line 87) `def test_relationship_fusion()`
  - `test_observation_and_source_counters` (function, line 97) `def test_observation_and_source_counters()`
  - `test_fail_soft_open` (function, line 116) `def test_fail_soft_open()`
  - `main` (function, line 124) `def main()`
- Depends on: `estorides_core/fusion_store.py`

## _test_hardening.py
- Layer: testing
- Language: py
- Symbols:
  - `_ok` (function, line 25) `def _ok(name, ok, detail)`
  - `test_security_headers` (function, line 36) `def test_security_headers()`
  - `test_cors_default_off` (function, line 53) `def test_cors_default_off()`
  - `test_cors_allowlist` (function, line 62) `def test_cors_allowlist()`
  - `test_debug_killswitch` (function, line 87) `def test_debug_killswitch()`
  - `test_max_body_rejection` (function, line 101) `def test_max_body_rejection()`
  - `test_case_diff` (function, line 113) `def test_case_diff()`
  - `test_case_diff_endpoints` (function, line 137) `def test_case_diff_endpoints()`
  - `test_case_save_endpoint` (function, line 148) `def test_case_save_endpoint()`
  - `test_report_renders` (function, line 165) `def test_report_renders()`
  - `test_report_with_diff` (function, line 181) `def test_report_with_diff()`
  - `test_console_script_help` (function, line 196) `def test_console_script_help()`
  - `main` (function, line 210) `def main()`
- Depends on: `estorides_core/__init__.py`, `estorides_core/cases.py`, `estorides_export/report.py`, `wsgi.py`

## _test_passive.py
- Layer: testing
- Language: py
- Symbols:
  - `check` (function, line 20) `def check(name, cond, detail)`
  - `main` (function, line 29) `def main()`
- Depends on: `estorides_core/config.py`, `estorides_core/orchestrator.py`, `estorides_core/source_loader.py`

## _test_people.py
- Layer: testing
- Language: py
- Symbols:
  - `check` (function, line 21) `def check(name, cond, detail)`
  - `_types` (function, line 30) `def _types(payload)`
  - `main` (function, line 37) `def main()`
  - `_StubRunner` (class, line 66) `class _StubRunner`
  - `run` (method, line 67) `def run(self, query)`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`, `estorides_core/pivot_engine.py`

## _test_proxy.py
- Layer: testing
- Language: py
- Symbols:
  - `check` (function, line 21) `def check(name, cond, detail)`
  - `main` (function, line 30) `def main()`
  - `_enter_and_rotate` (function, line 52) `def _enter_and_rotate()`
  - `_enter_socks` (function, line 72) `def _enter_socks()`
- Depends on: `estorides_core/__init__.py`, `estorides_core/async_client.py`, `estorides_core/config.py`

## _test_scope.py
- Layer: testing
- Language: py
- Symbols:
  - `check` (function, line 18) `def check(name, cond, detail)`
  - `main` (function, line 27) `def main()`
- Depends on: `estorides_core/scope.py`

## _validate.py
- Layer: utility
- Language: py
- Symbols:
  - `main` (function, line 17) `def main()`

## app.py
- Layer: utility
- Language: py
- Depends on: `wsgi.py`

## estorides_cli.py
- Layer: utility
- Language: py
- Symbols:
  - `_setup_logging` (function, line 36) `def _setup_logging(verbose)`
  - `_collect_selectors` (function, line 43) `def _collect_selectors(events, types)`
  - `_resolve_proxy` (function, line 59) `def _resolve_proxy(args)`
  - `_add_opsec_flags` (function, line 72) `def _add_opsec_flags(parser)`
  - `cmd_discover` (function, line 90) `def cmd_discover(args)`
  - `cmd_run` (function, line 202) `def cmd_run(args)`
  - `cmd_scope` (function, line 279) `def cmd_scope(args)`
  - `cmd_graph_export` (function, line 326) `def cmd_graph_export(args)`
  - `cmd_export_stix` (function, line 349) `def cmd_export_stix(args)`
  - `cmd_export_misp` (function, line 359) `def cmd_export_misp(args)`
  - `cmd_report` (function, line 369) `def cmd_report(args)`
  - `cmd_diff` (function, line 410) `def cmd_diff(args)`
  - `cmd_status` (function, line 438) `def cmd_status(_)`
  - `cmd_fusion` (function, line 445) `def cmd_fusion(args)`
  - `cmd_watch_add` (function, line 488) `def cmd_watch_add(args)`
  - `_watch_runner_factory` (function, line 523) `def _watch_runner_factory(proxy, passive_only)`
  - `cmd_watch_list` (function, line 545) `def cmd_watch_list(args)`
  - `cmd_watch_remove` (function, line 565) `def cmd_watch_remove(args)`
  - `cmd_watch_enable` (function, line 577) `def cmd_watch_enable(args)`
  - `cmd_watch_disable` (function, line 590) `def cmd_watch_disable(args)`
  - `cmd_watch_history` (function, line 602) `def cmd_watch_history(args)`
  - `cmd_alerts_test` (function, line 623) `def cmd_alerts_test(args)`
  - `cmd_alerts_channels` (function, line 635) `def cmd_alerts_channels(args)`
  - `cmd_scheduler_start` (function, line 647) `def cmd_scheduler_start(args)`
  - `cmd_scheduler_stop` (function, line 657) `def cmd_scheduler_stop(args)`
  - `cmd_scheduler_status` (function, line 667) `def cmd_scheduler_status(args)`
  - `cmd_serve` (function, line 675) `def cmd_serve(args)`
  - `build_parser` (function, line 692) `def build_parser()`
  - `main` (function, line 847) `def main(argv)`
  - `_on_done` (function, line 219) `def _on_done(source_name, ok, status, elapsed_ms)`
  - `_run` (function, line 531) `def _run(watch)`
- Depends on: `estorides_core/alerter.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/fusion_store.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/scope.py`, `estorides_core/validation.py`, `estorides_export/__init__.py`, `estorides_export/report.py`, `estorides_web.py`

## estorides_web.py
- Layer: presentation
- Language: py
- Symbols:
  - `_client_ip` (function, line 75) `def _client_ip()`
  - `_arg_int` (function, line 92) `def _arg_int(name, default)`
  - `_send_and_cleanup` (function, line 108) `def _send_and_cleanup(p, tmpdir)`
  - `_RunStreamJob` (class, line 122) `class _RunStreamJob`
  - `_new_stream_job_id` (method, line 160) `def _new_stream_job_id()`
  - `_rate_limit_decorator` (method, line 165) `def _rate_limit_decorator()`
  - `create_app` (method, line 209) `def create_app()`
  - `_serve_loop` (method, line 1700) `def _serve_loop()`
  - `_shape_for_ui` (method, line 1713) `def _shape_for_ui(result)`
  - `__init__` (method, line 130) `def __init__(self, job_id, query, query_type, case_id)`
  - `stop` (method, line 139) `def stop(self)`
  - `should_stop` (method, line 142) `def should_stop(self)`
  - `status` (method, line 146) `def status(self)`
  - `done` (method, line 150) `def done(self)`
  - `deco` (method, line 172) `def deco(view)`
  - `index` (method, line 240) `def index()`
  - `api_status` (method, line 261) `def api_status()`
  - `api_ollama_status` (method, line 267) `def api_ollama_status()`
  - `api_tools_list` (method, line 277) `def api_tools_list()`
  - `api_tool_install` (method, line 297) `def api_tool_install(name)`
  - `api_tool_install_status` (method, line 338) `def api_tool_install_status(name)`
  - `api_run` (method, line 348) `def api_run()`
  - `api_graph` (method, line 404) `def api_graph()`
  - `api_feeds` (method, line 480) `def api_feeds()`
  - `api_export` (method, line 511) `def api_export(fmt)`
  - `api_cases_list` (method, line 588) `def api_cases_list()`
  - `api_cases_get` (method, line 602) `def api_cases_get(case_id)`
  - `api_cases_delete` (method, line 617) `def api_cases_delete(case_id)`
  - `api_cases_save` (method, line 626) `def api_cases_save(case_id)`
  - `api_cases_diff` (method, line 655) `def api_cases_diff()`
  - `api_intel_resolve` (method, line 681) `def api_intel_resolve()`
  - `api_intel_graph` (method, line 721) `def api_intel_graph()`
  - `api_intel_stats` (method, line 762) `def api_intel_stats()`
  - `api_fusion_stats` (method, line 782) `def api_fusion_stats()`
  - `api_fusion_sources` (method, line 791) `def api_fusion_sources()`
  - `api_fusion_entities` (method, line 801) `def api_fusion_entities()`
  - `api_fusion_entity` (method, line 823) `def api_fusion_entity(eid)`
  - `api_fusion_analytics_entity_timeline` (method, line 842) `def api_fusion_analytics_entity_timeline(eid)`
  - `api_fusion_analytics_entity_summary` (method, line 853) `def api_fusion_analytics_entity_summary(eid)`
  - `api_fusion_analytics_source_stats` (method, line 864) `def api_fusion_analytics_source_stats(source_name)`
  - `api_fusion_analytics_consensus` (method, line 875) `def api_fusion_analytics_consensus(eid)`
  - `api_fusion_analytics_top_changed` (method, line 886) `def api_fusion_analytics_top_changed()`
  - `admin_sources` (method, line 898) `def admin_sources()`
  - `api_sources_yaml_list` (method, line 915) `def api_sources_yaml_list()`
  - `api_sources_yaml_create` (method, line 941) `def api_sources_yaml_create()`
  - `api_sources_yaml_update` (method, line 962) `def api_sources_yaml_update(name)`
  - `api_sources_yaml_delete` (method, line 981) `def api_sources_yaml_delete(name)`
  - `api_fusion_analytics_corroboration_matrix` (method, line 997) `def api_fusion_analytics_corroboration_matrix()`
  - `api_socmint_resolve` (method, line 1012) `def api_socmint_resolve()`
  - `api_socmint_platforms` (method, line 1035) `def api_socmint_platforms()`
  - `api_socmint_discover` (method, line 1044) `def api_socmint_discover()`
  - `api_watch_list` (method, line 1088) `def api_watch_list()`
  - `api_watch_create` (method, line 1098) `def api_watch_create()`
  - `api_watch_get` (method, line 1133) `def api_watch_get(watch_id)`
  - `api_watch_delete` (method, line 1146) `def api_watch_delete(watch_id)`
  - `api_watch_enable` (method, line 1158) `def api_watch_enable(watch_id)`
  - `api_watch_disable` (method, line 1172) `def api_watch_disable(watch_id)`
  - `api_watch_history` (method, line 1185) `def api_watch_history(watch_id)`
  - `api_alerts_channels` (method, line 1196) `def api_alerts_channels()`
  - `api_alerts_test` (method, line 1205) `def api_alerts_test()`
  - `api_scheduler_status` (method, line 1222) `def api_scheduler_status()`
  - `api_transforms` (method, line 1241) `def api_transforms()`
  - `api_transform_run` (method, line 1256) `def api_transform_run()`
  - `api_osiris_bgp` (method, line 1285) `def api_osiris_bgp()`
  - `api_osiris_mac` (method, line 1300) `def api_osiris_mac()`
  - `api_osiris_phone` (method, line 1315) `def api_osiris_phone()`
  - `api_osiris_github` (method, line 1330) `def api_osiris_github()`
  - `api_osiris_leaks` (method, line 1345) `def api_osiris_leaks()`
  - `api_osiris_kev` (method, line 1360) `def api_osiris_kev()`
  - `api_osiris_malware` (method, line 1370) `def api_osiris_malware()`
  - `api_osiris_threats` (method, line 1377) `def api_osiris_threats()`
  - `api_discover_start` (method, line 1390) `def api_discover_start()`
  - `api_discover_jobs` (method, line 1436) `def api_discover_jobs()`
  - `api_discover_stop` (method, line 1442) `def api_discover_stop()`
  - `api_discover_stream` (method, line 1454) `def api_discover_stream()`
  - `api_run_stream_start` (method, line 1509) `def api_run_stream_start()`
  - `api_run_stream_stop` (method, line 1576) `def api_run_stream_stop()`
  - `api_run_stream` (method, line 1588) `def api_run_stream()`
  - `api_analyze_stream` (method, line 1639) `def api_analyze_stream()`
  - `wrapper` (method, line 174) `def wrapper()`
  - `_worker` (method, line 309) `def _worker()`
  - `gen` (method, line 1467) `def gen()`
  - `_drive` (method, line 1539) `def _drive()`
  - `gen` (method, line 1594) `def gen()`
  - `_run` (method, line 1652) `def _run()`
  - `gen` (method, line 1667) `def gen()`
  - `_watch_runner` (method, line 1065) `def _watch_runner(swatch)`
- Depends on: `estorides_core/__init__.py`, `estorides_core/alerter.py`, `estorides_core/audit.py`, `estorides_core/cases.py`, `estorides_core/config.py`, `estorides_core/discoverer.py`, `estorides_core/entity_extraction.py`, `estorides_core/feeds.py`, `estorides_core/fusion_analytics.py`, `estorides_core/fusion_store.py`, `estorides_core/graph_kuzu.py`, `estorides_core/intel_resolver.py`, `estorides_core/job_registry.py`, `estorides_core/knowledge_graph.py`, `estorides_core/monitoring.py`, `estorides_core/orchestrator.py`, `estorides_core/pivot_engine.py`, `estorides_core/search_telemetry.py`, `estorides_core/socmint.py`, `estorides_core/tool_install.py`, `estorides_core/transforms.py`, `estorides_core/validation.py`, `estorides_core/web_security.py`, `estorides_export/__init__.py`, `estorides_export/encryption.py`
- Imported by: `estorides_cli.py`, `wsgi.py`

## install.sh
- Layer: utility
- Doc: Bootstrap a venv and install the runtime + optional test dependencies.  Idempotent: re-running on an existing venv is a 
- Language: sh
- Symbols:
  - `install_full` (function, line 51)
  - `install_minimal` (function, line 55)

## web.py
- Layer: utility
- Language: py
- Depends on: `wsgi.py`

## wsgi.py
- Layer: utility
- Language: py
- Depends on: `estorides_web.py`
- Imported by: `_test_hardening.py`, `_test_hardening.py`, `_test_hardening.py`, `_test_hardening.py`, `_test_hardening.py`, `_test_hardening.py`, `app.py`, `web.py`
