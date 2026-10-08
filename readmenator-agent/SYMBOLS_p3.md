# Symbols (page 3 of 6)
Previous: [SYMBOLS_p2.md](SYMBOLS_p2.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `export_stix_encrypted` | function | `estorides_export/encryption.py:100` | `def export_stix_encrypted(kg, recipient_pubkey, path)` |
| `_category` | function | `estorides_export/misp.py:65` | `def _category(ent_type)` |
| `event_from_graph` | function | `estorides_export/misp.py:36` | `def event_from_graph(kg)` |
| `export` | function | `estorides_export/misp.py:79` | `def export(kg, path)` |
| `ReportMetadata` | class | `estorides_export/recon_report.py:23` | `class ReportMetadata` |
| `ReportResult` | class | `estorides_export/recon_report.py:51` | `class ReportResult` |
| `ReportSection` | class | `estorides_export/recon_report.py:40` | `class ReportSection` |
| `__post_init__` | method | `estorides_export/recon_report.py:29` | `def __post_init__(self)` |
| `build_executive_summary` | method | `estorides_export/recon_report.py:92` | `def build_executive_summary(critical_findings, total_targets, domain, classification)` |
| `build_subdomain_tree` | method | `estorides_export/recon_report.py:67` | `def build_subdomain_tree(subdomains)` |
| `generate_report` | method | `estorides_export/recon_report.py:115` | `def generate_report(query, target_scoring, metadata)` |
| `redact_sensitive` | method | `estorides_export/recon_report.py:61` | `def redact_sensitive(text)` |
| `to_dict` | method | `estorides_export/recon_report.py:35` | `def to_dict(self)` |
| `to_dict` | method | `estorides_export/recon_report.py:46` | `def to_dict(self)` |
| `to_dict` | method | `estorides_export/recon_report.py:57` | `def to_dict(self)` |
| `_analysis` | function | `estorides_export/report.py:158` | `def _analysis(case)` |
| `_diff_section` | function | `estorides_export/report.py:121` | `def _diff_section(diff)` |
| `_iocs` | function | `estorides_export/report.py:77` | `def _iocs(entities)` |
| `_meta_footer` | function | `estorides_export/report.py:179` | `def _meta_footer(case, sources_queried, sources_succeeded)` |
| `_tldr` | function | `estorides_export/report.py:37` | `def _tldr(case, entities, sources_queried, sources_succeeded, diff)` |
| `render_markdown_report` | function | `estorides_export/report.py:196` | `def render_markdown_report(case, entities, sources_queried, sources_succeeded, diff)` |
| `_id` | function | `estorides_export/stix.py:28` | `def _id(stix_type)` |
| `_now` | function | `estorides_export/stix.py:32` | `def _now()` |
| `bundle_from_graph` | function | `estorides_export/stix.py:55` | `def bundle_from_graph(kg)` |
| `export` | function | `estorides_export/stix.py:145` | `def export(kg, path)` |
| `format_context` | function | `estorides_llm/intelligence_prompts.py:97` | `def format_context(sources)` |
| `AnthropicBackend` | class | `estorides_llm/manager.py:316` | `class AnthropicBackend` |
| `LLMBackend` | class | `estorides_llm/manager.py:60` | `class LLMBackend(Protocol)` |
| `LLMManager` | class | `estorides_llm/manager.py:356` | `class LLMManager` |
| `OllamaBackend` | class | `estorides_llm/manager.py:120` | `class OllamaBackend` |
| `OpenAIBackend` | class | `estorides_llm/manager.py:302` | `class OpenAIBackend(_OpenAICompatibleBackend)` |
| `OpenRouterBackend` | class | `estorides_llm/manager.py:309` | `class OpenRouterBackend(_OpenAICompatibleBackend)` |
| `_OpenAICompatibleBackend` | class | `estorides_llm/manager.py:266` | `class _OpenAICompatibleBackend` |
| `__call__` | method | `estorides_llm/manager.py:69` | `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)` |
| `__call__` | method | `estorides_llm/manager.py:227` | `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)` |
| `__call__` | method | `estorides_llm/manager.py:274` | `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)` |
| `__call__` | method | `estorides_llm/manager.py:319` | `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)` |
| `__init__` | method | `estorides_llm/manager.py:357` | `def __init__(self)` |
| `_resolve_model` | method | `estorides_llm/manager.py:134` | `def _resolve_model(self, request_timeout)` |
| `_stub_response` | method | `estorides_llm/manager.py:459` | `def _stub_response(self, prompt, context)` |
| `deco` | method | `estorides_llm/manager.py:105` | `def deco(backend_or_cls)` |
| `generate` | method | `estorides_llm/manager.py:373` | `def generate(self, prompt)` |
| `get_ollama_status` | method | `estorides_llm/manager.py:414` | `def get_ollama_status(self)` |
| `get_status` | method | `estorides_llm/manager.py:124` | `def get_status()` |
| `register` | method | `estorides_llm/manager.py:97` | `def register(name)` |
| `stream` | method | `estorides_llm/manager.py:422` | `def stream(self, prompt)` |
| `stream_generate` | method | `estorides_llm/manager.py:80` | `def stream_generate(self, prompt, context, model, temperature, request_timeout)` |
| `stream_generate` | method | `estorides_llm/manager.py:188` | `def stream_generate(self, prompt, context, model, temperature, request_timeout)` |
| `_RunStreamJob` | class | `estorides_web.py:147` | `class _RunStreamJob` |
| `__init__` | method | `estorides_web.py:155` | `def __init__(self, job_id, query, query_type, case_id)` |
| `_arg_int` | function | `estorides_web.py:117` | `def _arg_int(name, default)` |
| `_client_ip` | function | `estorides_web.py:100` | `def _client_ip()` |
| `_drive` | method | `estorides_web.py:1515` | `def _drive()` |
| `_err` | method | `estorides_web.py:1246` | `def _err()` |
| `_gen` | method | `estorides_web.py:1251` | `def _gen()` |
| `_new_stream_job_id` | method | `estorides_web.py:185` | `def _new_stream_job_id()` |
| `_provides` | function | `estorides_web.py:81` | `def _provides(service, message)` |
| `_rate_limit_decorator` | method | `estorides_web.py:190` | `def _rate_limit_decorator()` |
| `_run` | method | `estorides_web.py:1624` | `def _run()` |
| `_send_and_cleanup` | function | `estorides_web.py:133` | `def _send_and_cleanup(p, tmpdir)` |
| `_serve_loop` | method | `estorides_web.py:1669` | `def _serve_loop()` |
| `_shape_for_ui` | method | `estorides_web.py:1682` | `def _shape_for_ui(result)` |
| `_sse_response` | function | `estorides_web.py:76` | `def _sse_response(gen)` |
| `_watch_runner` | method | `estorides_web.py:1032` | `def _watch_runner(swatch)` |
| `admin_sources` | method | `estorides_web.py:869` | `def admin_sources()` |
| `api_alerts_channels` | method | `estorides_web.py:1157` | `def api_alerts_channels()` |
| `api_alerts_test` | method | `estorides_web.py:1165` | `def api_alerts_test()` |
| `api_analyze_stream` | method | `estorides_web.py:1611` | `def api_analyze_stream()` |
| `api_cases_delete` | method | `estorides_web.py:608` | `def api_cases_delete(case_id)` |
| `api_cases_diff` | method | `estorides_web.py:639` | `def api_cases_diff()` |
| `api_cases_get` | method | `estorides_web.py:594` | `def api_cases_get(case_id)` |
| `api_cases_list` | method | `estorides_web.py:581` | `def api_cases_list()` |
| `api_cases_save` | method | `estorides_web.py:616` | `def api_cases_save(case_id)` |
| `api_discover_jobs` | method | `estorides_web.py:1417` | `def api_discover_jobs()` |
| `api_discover_start` | method | `estorides_web.py:1371` | `def api_discover_start()` |
| `api_discover_stop` | method | `estorides_web.py:1423` | `def api_discover_stop()` |
| `api_discover_stream` | method | `estorides_web.py:1435` | `def api_discover_stream()` |
| `api_export` | method | `estorides_web.py:503` | `def api_export(fmt)` |
| `api_feeds` | method | `estorides_web.py:472` | `def api_feeds()` |
| `api_fusion_analytics_consensus` | method | `estorides_web.py:849` | `def api_fusion_analytics_consensus(eid)` |
| `api_fusion_analytics_corroboration_matrix` | method | `estorides_web.py:969` | `def api_fusion_analytics_corroboration_matrix()` |
| `api_fusion_analytics_entity_summary` | method | `estorides_web.py:829` | `def api_fusion_analytics_entity_summary(eid)` |
| `api_fusion_analytics_entity_timeline` | method | `estorides_web.py:819` | `def api_fusion_analytics_entity_timeline(eid)` |
| `api_fusion_analytics_source_stats` | method | `estorides_web.py:839` | `def api_fusion_analytics_source_stats(source_name)` |
| `api_fusion_analytics_top_changed` | method | `estorides_web.py:859` | `def api_fusion_analytics_top_changed()` |
| `api_fusion_entities` | method | `estorides_web.py:780` | `def api_fusion_entities()` |
| `api_fusion_entity` | method | `estorides_web.py:801` | `def api_fusion_entity(eid)` |
| `api_fusion_sources` | method | `estorides_web.py:771` | `def api_fusion_sources()` |
| `api_fusion_stats` | method | `estorides_web.py:763` | `def api_fusion_stats()` |
| `api_graph` | method | `estorides_web.py:396` | `def api_graph()` |
| `api_intel_graph` | method | `estorides_web.py:703` | `def api_intel_graph()` |
| `api_intel_resolve` | method | `estorides_web.py:664` | `def api_intel_resolve()` |
| `api_intel_stats` | method | `estorides_web.py:742` | `def api_intel_stats()` |
| `api_ollama_status` | method | `estorides_web.py:334` | `def api_ollama_status()` |
| `api_osiris_bgp` | method | `estorides_web.py:1274` | `def api_osiris_bgp()` |
| `api_osiris_github` | method | `estorides_web.py:1316` | `def api_osiris_github()` |
| `api_osiris_kev` | method | `estorides_web.py:1344` | `def api_osiris_kev()` |
| `api_osiris_leaks` | method | `estorides_web.py:1330` | `def api_osiris_leaks()` |
| `api_osiris_mac` | method | `estorides_web.py:1288` | `def api_osiris_mac()` |
| `api_osiris_malware` | method | `estorides_web.py:1353` | `def api_osiris_malware()` |
| `api_osiris_phone` | method | `estorides_web.py:1302` | `def api_osiris_phone()` |
| `api_osiris_threats` | method | `estorides_web.py:1358` | `def api_osiris_threats()` |
| `api_run` | method | `estorides_web.py:340` | `def api_run()` |
| `api_run_stream` | method | `estorides_web.py:1564` | `def api_run_stream()` |
| `api_run_stream_start` | method | `estorides_web.py:1485` | `def api_run_stream_start()` |
| `api_run_stream_stop` | method | `estorides_web.py:1552` | `def api_run_stream_stop()` |
| `api_scheduler_status` | method | `estorides_web.py:1181` | `def api_scheduler_status()` |
| `api_socmint_discover` | method | `estorides_web.py:1013` | `def api_socmint_discover()` |
| `api_socmint_platforms` | method | `estorides_web.py:1005` | `def api_socmint_platforms()` |
| `api_socmint_resolve` | method | `estorides_web.py:983` | `def api_socmint_resolve()` |
| `api_sources_yaml_create` | method | `estorides_web.py:912` | `def api_sources_yaml_create()` |
| `api_sources_yaml_delete` | method | `estorides_web.py:952` | `def api_sources_yaml_delete(name)` |
| `api_sources_yaml_list` | method | `estorides_web.py:886` | `def api_sources_yaml_list()` |
| `api_sources_yaml_update` | method | `estorides_web.py:933` | `def api_sources_yaml_update(name)` |
| `api_status` | method | `estorides_web.py:328` | `def api_status()` |
| `api_transform_run` | method | `estorides_web.py:1213` | `def api_transform_run()` |
| `api_transform_stream` | method | `estorides_web.py:1235` | `def api_transform_stream()` |
| `api_transforms` | method | `estorides_web.py:1199` | `def api_transforms()` |
| `api_watch_create` | method | `estorides_web.py:1065` | `def api_watch_create()` |
| `api_watch_delete` | method | `estorides_web.py:1111` | `def api_watch_delete(watch_id)` |
| `api_watch_disable` | method | `estorides_web.py:1135` | `def api_watch_disable(watch_id)` |
| `api_watch_enable` | method | `estorides_web.py:1122` | `def api_watch_enable(watch_id)` |
| `api_watch_get` | method | `estorides_web.py:1099` | `def api_watch_get(watch_id)` |
| `api_watch_history` | method | `estorides_web.py:1147` | `def api_watch_history(watch_id)` |
| `api_watch_list` | method | `estorides_web.py:1056` | `def api_watch_list()` |
| `create_app` | method | `estorides_web.py:234` | `def create_app()` |
| `deco` | method | `estorides_web.py:88` | `def deco(view)` |
| `deco` | method | `estorides_web.py:197` | `def deco(view)` |
| `done` | method | `estorides_web.py:175` | `def done(self)` |
| `gen` | method | `estorides_web.py:1448` | `def gen()` |
| `gen` | method | `estorides_web.py:1570` | `def gen()` |
| `gen` | method | `estorides_web.py:1640` | `def gen()` |
| `healthz` | method | `estorides_web.py:270` | `def healthz()` |
| `index` | method | `estorides_web.py:307` | `def index()` |
| `metrics` | method | `estorides_web.py:295` | `def metrics()` |
| `openapi_doc` | method | `estorides_web.py:302` | `def openapi_doc()` |
| `readyz` | method | `estorides_web.py:281` | `def readyz()` |
| `should_stop` | method | `estorides_web.py:167` | `def should_stop(self)` |
| `status` | method | `estorides_web.py:171` | `def status(self)` |
| `stop` | method | `estorides_web.py:164` | `def stop(self)` |
| `wrapper` | method | `estorides_web.py:90` | `def wrapper()` |
| `wrapper` | method | `estorides_web.py:199` | `def wrapper()` |
| `_worker` | function | `estorides_web_tools.py:91` | `def _worker()` |
| `api_tool_install` | function | `estorides_web_tools.py:75` | `def api_tool_install(name)` |
| `api_tool_install_status` | function | `estorides_web_tools.py:120` | `def api_tool_install_status(name)` |
| `api_tools_doctor` | function | `estorides_web_tools.py:68` | `def api_tools_doctor()` |
| `api_tools_list` | function | `estorides_web_tools.py:49` | `def api_tools_list()` |
| `install_full` | function | `install.sh:51` | `` |
| `install_minimal` | function | `install.sh:55` | `` |
| `CLUSTER_PALETTE` | function | `static/js/estorides.js:1129` | `` |
| `TELEMETRY` | function | `static/js/estorides.js:41` | `` |
| `_installErrMsg` | function | `static/js/estorides.js:243` | `` |
| `_redrawGraph` | function | `static/js/estorides.js:1704` | `` |
| `_sanitizeInput` | function | `static/js/estorides.js:2551` | `` |
| `_sseAuthToken` | function | `static/js/estorides.js:2965` | `` |
| `_sseUrl` | function | `static/js/estorides.js:2969` | `` |
| `actions` | function | `static/js/estorides.js:2560` | `` |
| `add` | function | `static/js/estorides.js:1520` | `` |
| `addDiscoverEntityToTab` | function | `static/js/estorides.js:3147` | `` |
| `addText` | function | `static/js/estorides.js:1526` | `` |
| `analyseEntity` | function | `static/js/estorides.js:951` | `` |
| `appendStreamEntity` | function | `static/js/estorides.js:676` | `` |
| `appendStreamObservation` | function | `static/js/estorides.js:654` | `` |
| `applyLevelStyles` | function | `static/js/estorides.js:1373` | `` |
| `applyResultFilters` | function | `static/js/estorides.js:259` | `` |
| `attribute` | class | `static/js/estorides.js:2905` | `` |
| `bindResultFilters` | function | `static/js/estorides.js:280` | `` |
| `boxQ` | function | `static/js/estorides.js:880` | `` |
| `buildCaseMapCoords` | function | `static/js/estorides.js:2286` | `` |
| `buildMapCoords` | function | `static/js/estorides.js:1836` | `` |
| `buildResultCard` | function | `static/js/estorides.js:138` | `` |
| `c` | function | `static/js/estorides.js:1162` | `` |
| `c` | function | `static/js/estorides.js:1245` | `` |
| `caseActionDiff` | function | `static/js/estorides.js:2429` | `` |
| `caseActionReport` | function | `static/js/estorides.js:2490` | `` |
| `caseActionSave` | function | `static/js/estorides.js:2408` | `` |
| `cat` | function | `static/js/estorides.js:261` | `` |
| `check` | function | `static/js/estorides.js:3206` | `` |
| `cid` | function | `static/js/estorides.js:1182` | `` |
| `clearAll` | function | `static/js/estorides.js:705` | `` |
| `clearMap` | function | `static/js/estorides.js:336` | `` |
| `close` | function | `static/js/estorides.js:2574` | `` |
| `clusterColor` | function | `static/js/estorides.js:1160` | `` |
| `colorFor` | function | `static/js/estorides.js:1936` | `` |
| `colorForKind` | function | `static/js/estorides.js:2036` | `` |
| `confirmModal` | function | `static/js/estorides.js:2613` | `` |
| `debounce` | function | `static/js/estorides.js:2330` | `` |
| `deriveClusters` | function | `static/js/estorides.js:1179` | `` |
| `detectQueryTypeLocal` | function | `static/js/estorides.js:55` | `` |
| `doSearch` | function | `static/js/estorides.js:2859` | `` |
| `drawGraph` | function | `static/js/estorides.js:2154` | `` |
| `drawGraphWithExtras` | function | `static/js/estorides.js:1078` | `` |
| `drawHulls` | function | `static/js/estorides.js:1673` | `` |
| `entities` | function | `static/js/estorides.js:2211` | `` |
| `escapeAttr` | function | `static/js/estorides.js:1800` | `` |
| `escapeHTML` | function | `static/js/estorides.js:2380` | `` |
| `escapeHtml` | function | `static/js/estorides.js:3175` | `` |
| `expandNode` | function | `static/js/estorides.js:984` | `` |
| `filterTimeline` | function | `static/js/estorides.js:2105` | `` |
| `flush` | function | `static/js/estorides.js:909` | `` |
| `flush` | function | `static/js/estorides.js:1420` | `` |
| `flushDiscoverEntities` | function | `static/js/estorides.js:3187` | `` |
| `fmtTime` | function | `static/js/estorides.js:2094` | `` |
| `focusGraphNodeByValue` | function | `static/js/estorides.js:301` | `` |
| `focusNode` | function | `static/js/estorides.js:1381` | `` |
| `frac` | function | `static/js/estorides.js:2081` | `` |
| `handleDiscoverEvent` | function | `static/js/estorides.js:3108` | `` |
| `handleRunStreamEvent` | function | `static/js/estorides.js:616` | `` |
| `hideContextMenu` | function | `static/js/estorides.js:1236` | `` |
| `hideDiscoverProgress` | function | `static/js/estorides.js:3012` | `` |
| `hideTooltip` | function | `static/js/estorides.js:1192` | `` |
| `hideWorkingIndicator` | function | `static/js/estorides.js:1721` | `` |
| `k` | function | `static/js/estorides.js:1028` | `` |
| `k` | function | `static/js/estorides.js:1487` | `` |
| `labelFor` | function | `static/js/estorides.js:1244` | `` |
| `levelOf` | function | `static/js/estorides.js:1156` | `` |
| `loadAnalysisModels` | function | `static/js/estorides.js:787` | `` |
| `loadCases` | function | `static/js/estorides.js:2184` | `` |
| `loadFusionEntityDetail` | function | `static/js/estorides.js:2897` | `` |
| `loadFusionSearch` | function | `static/js/estorides.js:2852` | `` |
| `loadFusionStats` | function | `static/js/estorides.js:2804` | `` |
| `loadFusionTab` | function | `static/js/estorides.js:2798` | `` |
| `loadFusionTopChanged` | function | `static/js/estorides.js:2823` | `` |
| `loadSidebarCollapsed` | function | `static/js/estorides.js:2719` | `` |
| `loadSidebarWidth` | function | `static/js/estorides.js:2705` | `` |
| `makeModelPill` | function | `static/js/estorides.js:806` | `` |
| `maybePlotDiscoverEntity` | function | `static/js/estorides.js:3180` | `` |
| `mergeExpansionIntoGraph` | function | `static/js/estorides.js:1014` | `` |
| `obs` | function | `static/js/estorides.js:2048` | `` |
| `obs` | function | `static/js/estorides.js:2212` | `` |
| `on` | class | `static/js/estorides.js:1889` | `` |
| `openCaseDetail` | function | `static/js/estorides.js:2210` | `` |
| `openModal` | function | `static/js/estorides.js:2554` | `` |
| `out` | function | `static/js/estorides.js:246` | `` |
| `plotPoints` | function | `static/js/estorides.js:341` | `` |
| `pollToolInstall` | function | `static/js/estorides.js:220` | `` |
| `populateCategoryFilter` | function | `static/js/estorides.js:253` | `` |
| `promptModal` | function | `static/js/estorides.js:2589` | `` |
| `pump` | function | `static/js/estorides.js:930` | `` |
| `purifyHTML` | function | `static/js/estorides.js:1206` | `` |
| `pushLink` | function | `static/js/estorides.js:1102` | `` |
| `q` | function | `static/js/estorides.js:2185` | `` |
| `reanalyze` | function | `static/js/estorides.js:861` | `` |
| `removed` | function | `static/js/estorides.js:2460` | `` |
| `renderAnalysis` | function | `static/js/estorides.js:819` | `` |
| `renderAnalysisModels` | function | `static/js/estorides.js:794` | `` |
| `renderCaseDiffPanel` | function | `static/js/estorides.js:2449` | `` |
| `renderCaseItem` | function | `static/js/estorides.js:2304` | `` |
| `renderEntities` | function | `static/js/estorides.js:1955` | `` |
| `renderGraphCore` | function | `static/js/estorides.js:1603` | `` |
| `renderGraphSummary` | function | `static/js/estorides.js:2007` | `` |
| `renderMarkdownInto` | function | `static/js/estorides.js:834` | `` |
| `renderResult` | function | `static/js/estorides.js:739` | `` |
| `renderTieredResults` | function | `static/js/estorides.js:1734` | `` |
| `renderTimeline` | function | `static/js/estorides.js:2044` | `` |
| `replotStreamData` | function | `static/js/estorides.js:443` | `` |
| `requestToolInstall` | function | `static/js/estorides.js:197` | `` |
| `resolverTypeFor` | function | `static/js/estorides.js:1136` | `` |
| `restoreCaseToWorkspace` | function | `static/js/estorides.js:2265` | `` |
| `rows` | function | `static/js/estorides.js:2457` | `` |
| `runQuery` | function | `static/js/estorides.js:470` | `` |
| `runQueryBlocking` | function | `static/js/estorides.js:540` | `` |
| `runTransform` | function | `static/js/estorides.js:1393` | `` |
| `runTransformStream` | function | `static/js/estorides.js:1414` | `` |
| `safeColor` | function | `static/js/estorides.js:1170` | `` |
| `saveLevelOverrides` | function | `static/js/estorides.js:1152` | `` |
| `saveSidebarCollapsed` | function | `static/js/estorides.js:2727` | `` |
| `saveSidebarWidth` | function | `static/js/estorides.js:2716` | `` |
| `saved` | function | `static/js/estorides.js:2308` | `` |
| `scheduleRender` | function | `static/js/estorides.js:904` | `` |
| `searchEntity` | function | `static/js/estorides.js:573` | `` |
| `selectNode` | function | `static/js/estorides.js:1509` | `` |
| `set` | function | `static/js/estorides.js:32` | `` |
| `setDiscoverProgress` | function | `static/js/estorides.js:3000` | `` |
| `setNodeLevel` | function | `static/js/estorides.js:1364` | `` |
| `setRunProgress` | function | `static/js/estorides.js:86` | `` |
| `setSanitizedHTML` | function | `static/js/estorides.js:1217` | `` |
| `setStatus` | function | `static/js/estorides.js:733` | `` |
| `setStatus` | function | `static/js/estorides.js:2993` | `` |
| `setStatusDot` | function | `static/js/estorides.js:1710` | `` |
| `setThinkingVisible` | function | `static/js/estorides.js:849` | `` |
| `setVisible` | function | `static/js/estorides.js:12` | `` |
| `showBridgeTooltip` | function | `static/js/estorides.js:1241` | `` |
| `showContextMenu` | function | `static/js/estorides.js:1289` | `` |
| `showEmptyState` | function | `static/js/estorides.js:107` | `` |
| `showFriendlyError` | function | `static/js/estorides.js:288` | `` |
| `showNodeTooltip` | function | `static/js/estorides.js:1270` | `` |
| `showReportModal` | function | `static/js/estorides.js:2526` | `` |
| `showToast` | function | `static/js/estorides.js:66` | `` |
| `showTooltipAt` | function | `static/js/estorides.js:1226` | `` |
| `showWorkingIndicator` | function | `static/js/estorides.js:1716` | `` |
| `sig` | function | `static/js/estorides.js:678` | `` |
| `sig` | function | `static/js/estorides.js:3152` | `` |
| `startDiscover` | function | `static/js/estorides.js:3017` | `` |
| `status` | function | `static/js/estorides.js:148` | `` |
| `status` | function | `static/js/estorides.js:262` | `` |
| `stopDiscover` | function | `static/js/estorides.js:3091` | `` |
| `stopRunStream` | function | `static/js/estorides.js:455` | `` |
| `summariseObservation` | function | `static/js/estorides.js:113` | `` |
| `switchCanvasTab` | function | `static/js/estorides.js:314` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:310` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:2785` | `` |
| `tag` | function | `static/js/estorides.js:2675` | `` |
| `text` | function | `static/js/estorides.js:260` | `` |
| `to` | class | `static/js/estorides.js:401` | `` |
| `toggleThinking` | function | `static/js/estorides.js:856` | `` |
| `toggleTierSection` | function | `static/js/estorides.js:1726` | `` |
| `toolBinary` | function | `static/js/estorides.js:142` | `` |
| `tr` | function | `static/js/estorides.js:1339` | `` |
| `tr` | function | `static/js/estorides.js:1577` | `` |
| `truncate` | function | `static/js/estorides.js:2385` | `` |
| `undoGraph` | function | `static/js/estorides.js:1474` | `` |
| `updateQueryChip` | function | `static/js/estorides.js:76` | `` |
| `validCoord` | function | `static/js/estorides.js:1932` | `` |
| `apiFetch` | function | `static/js/source_manager.js:15` | `` |
| `authHeaders` | function | `static/js/source_manager.js:7` | `` |
| `clearEditor` | function | `static/js/source_manager.js:251` | `` |
| `deleteSource` | function | `static/js/source_manager.js:304` | `` |
| `escAttr` | function | `static/js/source_manager.js:224` | `` |
| `escHtml` | function | `static/js/source_manager.js:223` | `` |
| `from` | class | `static/js/source_manager.js:255` | `` |
| `getCheckedTags` | function | `static/js/source_manager.js:67` | `` |
| `loadSources` | function | `static/js/source_manager.js:236` | `` |
| `newSource` | function | `static/js/source_manager.js:334` | `` |
| `readForm` | function | `static/js/source_manager.js:84` | `` |
| `renderList` | function | `static/js/source_manager.js:193` | `` |
| `saveSource` | function | `static/js/source_manager.js:273` | `` |
| `selectSource` | function | `static/js/source_manager.js:261` | `` |
| `setCheckedTags` | function | `static/js/source_manager.js:74` | `` |
| `toast` | function | `static/js/source_manager.js:227` | `` |
| `updateYamlPreview` | function | `static/js/source_manager.js:183` | `` |
| `writeForm` | function | `static/js/source_manager.js:120` | `` |
| `test_after_none_returns_empty` | function | `tests/properties/test_change_detection_properties.py:113` | `def test_after_none_returns_empty(before)` |
| `test_before_vs_no_after_empty` | function | `tests/properties/test_change_detection_properties.py:121` | `def test_before_vs_no_after_empty(entities)` |
| `test_first_run_reports_all_as_new` | function | `tests/properties/test_change_detection_properties.py:105` | `def test_first_run_reports_all_as_new(after)` |
| `test_id_is_16_char_hex` | function | `tests/properties/test_change_detection_properties.py:86` | `def test_id_is_16_char_hex(before, after)` |
| `test_idempotent` | function | `tests/properties/test_change_detection_properties.py:95` | `def test_idempotent(before, after)` |
| `test_max_changes_respected` | function | `tests/properties/test_change_detection_properties.py:77` | `def test_max_changes_respected(before, after)` |
| `test_scores_always_bounded` | function | `tests/properties/test_change_detection_properties.py:69` | `def test_scores_always_bounded(before, after)` |
| `test_summary_consistency` | function | `tests/properties/test_change_detection_properties.py:132` | `def test_summary_consistency(before, after)` |
| `test_csp_style_src_never_gains_unsafe_inline` | function | `tests/properties/test_csp_safe_styles_properties.py:137` | `def test_csp_style_src_never_gains_unsafe_inline(bad)` |
| `test_js_never_gains_a_style_attribute_in_template_literal` | function | `tests/properties/test_csp_safe_styles_properties.py:58` | `def test_js_never_gains_a_style_attribute_in_template_literal(insertion)` |
| `test_template_never_gains_a_style_attribute` | function | `tests/properties/test_csp_safe_styles_properties.py:105` | `def test_template_never_gains_a_style_attribute(insertion)` |
| `test_claim_length_under_cap` | function | `tests/properties/test_hypothesis_engine_properties.py:66` | `def test_claim_length_under_cap(observations, entities)` |
| `test_hostile_observation_does_not_crash` | function | `tests/properties/test_hypothesis_engine_properties.py:147` | `def test_hostile_observation_does_not_crash(observations, entities)` |
| `test_id_is_deterministic_hex` | function | `tests/properties/test_hypothesis_engine_properties.py:99` | `def test_id_is_deterministic_hex(observations, entities)` |
| `test_idempotent` | function | `tests/properties/test_hypothesis_engine_properties.py:112` | `def test_idempotent(observations, entities)` |
| `test_max_hypotheses_caps_output` | function | `tests/properties/test_hypothesis_engine_properties.py:123` | `def test_max_hypotheses_caps_output(observations, entities)` |
| `test_min_score_filters` | function | `tests/properties/test_hypothesis_engine_properties.py:134` | `def test_min_score_filters(observations, entities)` |
| `test_reasoning_length_under_cap` | function | `tests/properties/test_hypothesis_engine_properties.py:77` | `def test_reasoning_length_under_cap(observations, entities)` |
| `test_scores_always_bounded` | function | `tests/properties/test_hypothesis_engine_properties.py:54` | `def test_scores_always_bounded(observations, entities)` |
| `test_sources_sorted_unique` | function | `tests/properties/test_hypothesis_engine_properties.py:88` | `def test_sources_sorted_unique(observations, entities)` |
| `entity_strategy` | function | `tests/properties/test_observation_models_properties.py:76` | `def entity_strategy(draw)` |
| `meta_strategy` | function | `tests/properties/test_observation_models_properties.py:45` | `def meta_strategy(draw)` |
| `obs_strategy` | function | `tests/properties/test_observation_models_properties.py:60` | `def obs_strategy(draw)` |
| `test_entity_round_trip_and_bounds` | function | `tests/properties/test_observation_models_properties.py:115` | `def test_entity_round_trip_and_bounds(payload)` |
| `test_meta_never_echoes_unbounded_url` | function | `tests/properties/test_observation_models_properties.py:128` | `def test_meta_never_echoes_unbounded_url(metas)` |
| `test_observation_bounded_fields` | function | `tests/properties/test_observation_models_properties.py:103` | `def test_observation_bounded_fields(payload)` |
| `test_observation_round_trip_stability` | function | `tests/properties/test_observation_models_properties.py:90` | `def test_observation_round_trip_stability(payload)` |
| `test_all_parsers_are_total` | function | `tests/properties/test_parsers_properties.py:35` | `def test_all_parsers_are_total(payload)` |
| `TestPropertyDeterminism` | class | `tests/properties/test_recon_fusion_properties.py:114` | `class TestPropertyDeterminism` |
| `TestPropertyEmptyQueryRejected` | class | `tests/properties/test_recon_fusion_properties.py:176` | `class TestPropertyEmptyQueryRejected` |
| `TestPropertyNoDuplicates` | class | `tests/properties/test_recon_fusion_properties.py:135` | `class TestPropertyNoDuplicates` |
| `TestPropertySafeWithBadInputs` | class | `tests/properties/test_recon_fusion_properties.py:196` | `class TestPropertySafeWithBadInputs` |
| `TestPropertyScoreBounds` | class | `tests/properties/test_recon_fusion_properties.py:48` | `class TestPropertyScoreBounds` |
| `TestPropertyTierKeysOrder` | class | `tests/properties/test_recon_fusion_properties.py:155` | `class TestPropertyTierKeysOrder` |
| `TestPropertyTierSumMatches` | class | `tests/properties/test_recon_fusion_properties.py:93` | `class TestPropertyTierSumMatches` |
| `TestPropertyTotalCounts` | class | `tests/properties/test_recon_fusion_properties.py:68` | `class TestPropertyTotalCounts` |
| `test_all_scores_in_unit_interval` | method | `tests/properties/test_recon_fusion_properties.py:58` | `def test_all_scores_in_unit_interval(self, query, query_type, observations, entities)` |
| `test_counts_match_input` | method | `tests/properties/test_recon_fusion_properties.py:78` | `def test_counts_match_input(self, query, query_type, n_obs, n_ents)` |
| `test_deterministic_output` | method | `tests/properties/test_recon_fusion_properties.py:124` | `def test_deterministic_output(self, query, query_type, observations, entities)` |
| `test_empty_query_raises` | method | `tests/properties/test_recon_fusion_properties.py:185` | `def test_empty_query_raises(self, query_type, observations, entities)` |
| `test_entities_none_is_safe` | method | `tests/properties/test_recon_fusion_properties.py:214` | `def test_entities_none_is_safe(self, query, query_type, observations)` |
| `test_no_duplicate_ids_in_tier` | method | `tests/properties/test_recon_fusion_properties.py:145` | `def test_no_duplicate_ids_in_tier(self, query, query_type, observations, entities)` |
| `test_none_inputs_safe` | method | `tests/properties/test_recon_fusion_properties.py:201` | `def test_none_inputs_safe(self, query, query_type)` |
| `test_tier_keys_in_canonical_order` | method | `tests/properties/test_recon_fusion_properties.py:165` | `def test_tier_keys_in_canonical_order(self, query, query_type, observations, entities)` |
| `test_tier_summary_matches` | method | `tests/properties/test_recon_fusion_properties.py:103` | `def test_tier_summary_matches(self, query, query_type, observations, entities)` |
| `test_corroboration_is_monotone_in_count` | function | `tests/properties/test_reliability_scoring_properties.py:159` | `def test_corroboration_is_monotone_in_count(n1, n2)` |
| `test_corroboration_weight_in_unit_interval` | function | `tests/properties/test_reliability_scoring_properties.py:73` | `def test_corroboration_weight_in_unit_interval(n)` |
| `test_credibility_weight_set_is_curated` | function | `tests/properties/test_reliability_scoring_properties.py:146` | `def test_credibility_weight_set_is_curated()` |
| `test_freshness_monotone_in_age` | function | `tests/properties/test_reliability_scoring_properties.py:87` | `def test_freshness_monotone_in_age(age1, age2)` |
| `test_higher_reliability_dominates` | function | `tests/properties/test_reliability_scoring_properties.py:184` | `def test_higher_reliability_dominates(rel1, rel2)` |
| `test_merge_confidence_bounded` | function | `tests/properties/test_reliability_scoring_properties.py:126` | `def test_merge_confidence_bounded(existing, new_obs, new_rel, new_cred, cor, age)` |
| `test_reliability_from_name_never_raises` | function | `tests/properties/test_reliability_scoring_properties.py:110` | `def test_reliability_from_name_never_raises(name)` |
| `test_reliability_weight_set_is_curated` | function | `tests/properties/test_reliability_scoring_properties.py:141` | `def test_reliability_weight_set_is_curated()` |
| `test_score_always_bounded` | function | `tests/properties/test_reliability_scoring_properties.py:56` | `def test_score_always_bounded(reliability, credibility, corroboration, age, base, half_life)` |
| `test_source_type_from_name_never_raises` | function | `tests/properties/test_reliability_scoring_properties.py:202` | `def test_source_type_from_name_never_raises(name)` |
| `test_source_type_weight_always_curated` | function | `tests/properties/test_reliability_scoring_properties.py:219` | `def test_source_type_weight_always_curated(reliability, credibility, source_type, corroboration, age, base, half_life)` |
| `test_source_type_weight_set_is_curated` | function | `tests/properties/test_reliability_scoring_properties.py:241` | `def test_source_type_weight_set_is_curated()` |
| `test_brand_predicate_flags_embedded_brand` | function | `tests/properties/test_search_telemetry_properties.py:84` | `def test_brand_predicate_flags_embedded_brand(prefix, suffix)` |
| `test_brand_predicate_is_total` | function | `tests/properties/test_search_telemetry_properties.py:56` | `def test_brand_predicate_is_total(text)` |
| `test_emoji_predicate_is_total` | function | `tests/properties/test_search_telemetry_properties.py:65` | `def test_emoji_predicate_is_total(text)` |
| `test_percent_encoded_emoji_predicate_is_total` | function | `tests/properties/test_search_telemetry_properties.py:74` | `def test_percent_encoded_emoji_predicate_is_total(text)` |
| `test_progress_invariants_hold` | function | `tests/properties/test_search_telemetry_properties.py:32` | `def test_progress_invariants_hold(completed, total, phase_key)` |
| `test_progress_rejects_unknown_phase` | function | `tests/properties/test_search_telemetry_properties.py:46` | `def test_progress_rejects_unknown_phase(phase_key)` |
| `_valid_input` | function | `tests/properties/test_source_health_monitoring_properties.py:21` | `def _valid_input(fetch, ok, latency, last_seen, now)` |
| `test_dashboard_summary_counts_match` | function | `tests/properties/test_source_health_monitoring_properties.py:112` | `def test_dashboard_summary_counts_match(records)` |
| `test_health_score_always_bounded` | function | `tests/properties/test_source_health_monitoring_properties.py:49` | `def test_health_score_always_bounded(fetch, ok, latency, last_seen, now)` |
| `test_status_always_valid_enum` | function | `tests/properties/test_source_health_monitoring_properties.py:63` | `def test_status_always_valid_enum(fetch, ok, latency, last_seen, now)` |
| `test_success_rate_bounds` | function | `tests/properties/test_source_health_monitoring_properties.py:78` | `def test_success_rate_bounds(fetch, ok, latency, last_seen, now)` |
| `test_unknown_when_below_min_fetches` | function | `tests/properties/test_source_health_monitoring_properties.py:89` | `def test_unknown_when_below_min_fetches(fetch, config_min)` |
| `valid_health_inputs` | function | `tests/properties/test_source_health_monitoring_properties.py:97` | `def valid_health_inputs(draw)` |
| `test_adversarial_query_rejected_at_runner_boundary` | function | `tests/properties/test_system_app_sources_properties.py:124` | `def test_adversarial_query_rejected_at_runner_boundary(prefix, bad, suffix)` |
| `test_parse_tool_output_never_raises` | function | `tests/properties/test_system_app_sources_properties.py:110` | `def test_parse_tool_output_never_raises(parser_name, data)` |
| `test_read_capped_respects_limit` | function | `tests/properties/test_system_app_sources_properties.py:83` | `def test_read_capped_respects_limit(blob, cap)` |
| `test_render_args_safe_inputs_no_metachars` | function | `tests/properties/test_system_app_sources_properties.py:55` | `def test_render_args_safe_inputs_no_metachars(args, query, outdir)` |
| `test_render_args_substitution_is_verbatim` | function | `tests/properties/test_system_app_sources_properties.py:70` | `def test_render_args_substitution_is_verbatim(query, outdir)` |
| `test_tool_parsers_never_raise` | function | `tests/properties/test_system_app_sources_properties.py:37` | `def test_tool_parsers_never_raise(parser_name, blob)` |
| `test_p10_batch_import_never_raises` | function | `tests/properties/test_target_management_properties.py:116` | `def test_p10_batch_import_never_raises(text)` |
| `test_p1_add_target_never_raises` | function | `tests/properties/test_target_management_properties.py:21` | `def test_p1_add_target_never_raises(etype, value)` |
| `test_p2_validated_id_is_deterministic` | function | `tests/properties/test_target_management_properties.py:31` | `def test_p2_validated_id_is_deterministic(etype, value)` |
| `test_p3_make_target_id_stable_under_case` | function | `tests/properties/test_target_management_properties.py:40` | `def test_p3_make_target_id_stable_under_case(etype, value)` |
| `test_p4_valid_domains_validate` | function | `tests/properties/test_target_management_properties.py:56` | `def test_p4_valid_domains_validate(d)` |
| `test_p5_valid_ipv4_validate` | function | `tests/properties/test_target_management_properties.py:68` | `def test_p5_valid_ipv4_validate(ip)` |
| `test_p6_valid_emails_validate` | function | `tests/properties/test_target_management_properties.py:77` | `def test_p6_valid_emails_validate(email)` |
| `test_p7_auto_detect_never_fails` | function | `tests/properties/test_target_management_properties.py:83` | `def test_p7_auto_detect_never_fails(value)` |
| `test_p8_validate_target_never_raises` | function | `tests/properties/test_target_management_properties.py:89` | `def test_p8_validate_target_never_raises(value)` |
| `test_p9_batch_import_idempotent` | function | `tests/properties/test_target_management_properties.py:105` | `def test_p9_batch_import_idempotent(targets)` |
| `test_check_injection_detects_all_metacharacters` | function | `tests/properties/test_tool_runner_properties.py:46` | `def test_check_injection_detects_all_metacharacters(prefix, bad, suffix)` |
| `test_check_injection_safe_strings_silent` | function | `tests/properties/test_tool_runner_properties.py:35` | `def test_check_injection_safe_strings_silent(args)` |
| `test_run_tool_never_raises` | function | `tests/properties/test_tool_runner_properties.py:63` | `def test_run_tool_never_raises(target)` |
| `TestDnsreconResult` | class | `tests/test_active_recon.py:71` | `class TestDnsreconResult` |
| `TestErrorResultsFlowThrough` | class | `tests/test_active_recon.py:135` | `class TestErrorResultsFlowThrough` |
| `TestNiktoResult` | class | `tests/test_active_recon.py:45` | `class TestNiktoResult` |
| `TestNmapResult` | class | `tests/test_active_recon.py:24` | `class TestNmapResult` |
| `TestResultTypes` | class | `tests/test_active_recon.py:97` | `class TestResultTypes` |
| `TestSqlmapResult` | class | `tests/test_active_recon.py:58` | `class TestSqlmapResult` |
| `TestTheHarvesterResult` | class | `tests/test_active_recon.py:84` | `class TestTheHarvesterResult` |
| `test_dnsrecon_result_has_to_dict` | method | `tests/test_active_recon.py:76` | `def test_dnsrecon_result_has_to_dict(self)` |
| `test_dnsrecon_result_is_dataclass` | method | `tests/test_active_recon.py:120` | `def test_dnsrecon_result_is_dataclass(self)` |
| `test_harvester_result_has_to_dict` | method | `tests/test_active_recon.py:89` | `def test_harvester_result_has_to_dict(self)` |
| `test_harvester_result_is_dataclass` | method | `tests/test_active_recon.py:127` | `def test_harvester_result_is_dataclass(self)` |
| `test_nikto_result_has_to_dict` | method | `tests/test_active_recon.py:50` | `def test_nikto_result_has_to_dict(self)` |
| `test_nikto_result_is_dataclass` | method | `tests/test_active_recon.py:106` | `def test_nikto_result_is_dataclass(self)` |
| `test_nmap_error_result_has_empty_entities` | method | `tests/test_active_recon.py:136` | `def test_nmap_error_result_has_empty_entities(self)` |
| `test_nmap_result_has_to_dict` | method | `tests/test_active_recon.py:29` | `def test_nmap_result_has_to_dict(self)` |
| `test_nmap_result_is_dataclass` | method | `tests/test_active_recon.py:98` | `def test_nmap_result_is_dataclass(self)` |
| `test_nmap_result_to_entities_is_list` | method | `tests/test_active_recon.py:38` | `def test_nmap_result_to_entities_is_list(self)` |
| `test_run_dnsrecon_returns_result` | method | `tests/test_active_recon.py:72` | `def test_run_dnsrecon_returns_result(self)` |
| `test_run_nikto_returns_result` | method | `tests/test_active_recon.py:46` | `def test_run_nikto_returns_result(self)` |
| `test_run_nmap_returns_result` | method | `tests/test_active_recon.py:25` | `def test_run_nmap_returns_result(self)` |
| `test_run_sqlmap_returns_result` | method | `tests/test_active_recon.py:59` | `def test_run_sqlmap_returns_result(self)` |
| `test_run_theHarvester_returns_result` | method | `tests/test_active_recon.py:85` | `def test_run_theHarvester_returns_result(self)` |
| `test_sqlmap_result_has_to_dict` | method | `tests/test_active_recon.py:63` | `def test_sqlmap_result_has_to_dict(self)` |
| `test_sqlmap_result_is_dataclass` | method | `tests/test_active_recon.py:113` | `def test_sqlmap_result_is_dataclass(self)` |
| `TestEffectiveProxies` | class | `tests/test_async_client.py:33` | `class TestEffectiveProxies` |
| `TestFailClosed` | class | `tests/test_async_client.py:63` | `class TestFailClosed` |
| `TestRedaction` | class | `tests/test_async_client.py:23` | `class TestRedaction` |
| `TestRotation` | class | `tests/test_async_client.py:45` | `class TestRotation` |
| `TestSocksDetection` | class | `tests/test_async_client.py:16` | `class TestSocksDetection` |
| `_enter_and_rotate` | method | `tests/test_async_client.py:49` | `def _enter_and_rotate()` |
| `_enter_socks` | method | `tests/test_async_client.py:68` | `def _enter_socks()` |
| `test_direct_has_no_proxy` | method | `tests/test_async_client.py:57` | `def test_direct_has_no_proxy(self)` |
| `test_explicit_wins` | method | `tests/test_async_client.py:34` | `def test_explicit_wins(self, monkeypatch)` |
| `test_hides_credentials_keeps_host` | method | `tests/test_async_client.py:24` | `def test_hides_credentials_keeps_host(self)` |
| `test_none_by_default` | method | `tests/test_async_client.py:39` | `def test_none_by_default(self, monkeypatch)` |
| `test_passthrough_without_credentials` | method | `tests/test_async_client.py:29` | `def test_passthrough_without_credentials(self)` |
| `test_round_robin` | method | `tests/test_async_client.py:46` | `def test_round_robin(self)` |
| `test_schemes` | method | `tests/test_async_client.py:17` | `def test_schemes(self)` |
| `test_socks_without_backend_raises` | method | `tests/test_async_client.py:64` | `def test_socks_without_backend_raises(self, monkeypatch)` |
| `_ev` | function | `tests/test_audit_log.py:12` | `def _ev(ts)` |
| `test_audit_log_appends` | function | `tests/test_audit_log.py:22` | `def test_audit_log_appends(tmp_path)` |
| `test_audit_log_no_rotation_when_disabled` | function | `tests/test_audit_log.py:61` | `def test_audit_log_no_rotation_when_disabled(tmp_path)` |
| `test_audit_log_rotates_when_cap_exceeded` | function | `tests/test_audit_log.py:31` | `def test_audit_log_rotates_when_cap_exceeded(tmp_path)` |
| `test_audit_log_rotation_respects_keep_count` | function | `tests/test_audit_log.py:48` | `def test_audit_log_rotation_respects_keep_count(tmp_path)` |
| `app_with_gate` | function | `tests/test_auth_gate.py:22` | `def app_with_gate(monkeypatch)` |
| `private` | function | `tests/test_auth_gate.py:34` | `def private()` |
| `test_gate_auto_generates_token_when_unset` | function | `tests/test_auth_gate.py:41` | `def test_gate_auto_generates_token_when_unset(monkeypatch)` |
| `test_gate_on_accepts_alt_header` | function | `tests/test_auth_gate.py:68` | `def test_gate_on_accepts_alt_header(app_with_gate)` |
| `test_gate_on_accepts_bearer_header` | function | `tests/test_auth_gate.py:61` | `def test_gate_on_accepts_bearer_header(app_with_gate)` |
| `test_gate_on_accepts_cookie` | function | `tests/test_auth_gate.py:74` | `def test_gate_on_accepts_cookie(app_with_gate)` |
| `test_gate_on_auto_generated_token_in_meta` | function | `tests/test_auth_gate.py:87` | `def test_gate_on_auto_generated_token_in_meta(monkeypatch)` |
| `test_gate_on_exposes_token_for_index_meta` | function | `tests/test_auth_gate.py:95` | `def test_gate_on_exposes_token_for_index_meta()` |
| `test_gate_on_rejects_anonymous` | function | `tests/test_auth_gate.py:53` | `def test_gate_on_rejects_anonymous(app_with_gate)` |
| `test_gate_on_rejects_wrong_token` | function | `tests/test_auth_gate.py:81` | `def test_gate_on_rejects_wrong_token(app_with_gate)` |
| `_fresh_store` | function | `tests/test_case_crypto.py:5` | `def _fresh_store(tmp_path, monkeypatch, key)` |
| `test_bad_key_falls_back` | function | `tests/test_case_crypto.py:58` | `def test_bad_key_falls_back(tmp_path, monkeypatch)` |
| `test_disabled_stores_plaintext` | function | `tests/test_case_crypto.py:22` | `def test_disabled_stores_plaintext(tmp_path, monkeypatch)` |
| `test_enabled_roundtrip` | function | `tests/test_case_crypto.py:33` | `def test_enabled_roundtrip(tmp_path, monkeypatch)` |
| `test_mixed_rows_and_tamper` | function | `tests/test_case_crypto.py:69` | `def test_mixed_rows_and_tamper(tmp_path, monkeypatch)` |
| `test_config_defaults` | function | `tests/test_central_config.py:7` | `def test_config_defaults()` |
| `test_run_defaults_track_config` | function | `tests/test_central_config.py:20` | `def test_run_defaults_track_config()` |
| `test_tool_install_survives_malformed_env` | function | `tests/test_central_config.py:29` | `def test_tool_install_survives_malformed_env(monkeypatch)` |
| `TestAfterIsNone` | class | `tests/test_change_detection.py:147` | `class TestAfterIsNone` |
| `TestBoundedSmoke` | class | `tests/test_change_detection.py:528` | `class TestBoundedSmoke` |
| `TestConfidenceShifted` | class | `tests/test_change_detection.py:488` | `class TestConfidenceShifted` |
| `TestDeterminism` | class | `tests/test_change_detection.py:346` | `class TestDeterminism` |
| `TestDisappearedWithGrace` | class | `tests/test_change_detection.py:166` | `class TestDisappearedWithGrace` |
| `TestEdgeChanges` | class | `tests/test_change_detection.py:436` | `class TestEdgeChanges` |
| `TestFirstRunBeforeIsNone` | class | `tests/test_change_detection.py:125` | `class TestFirstRunBeforeIsNone` |
| `TestHostilePropertyKey` | class | `tests/test_change_detection.py:310` | `class TestHostilePropertyKey` |
| `TestMaxChangesBounds` | class | `tests/test_change_detection.py:255` | `class TestMaxChangesBounds` |
| `TestMinReliabilityFiltersSources` | class | `tests/test_change_detection.py:226` | `class TestMinReliabilityFiltersSources` |

Next: [SYMBOLS_p4.md](SYMBOLS_p4.md)
