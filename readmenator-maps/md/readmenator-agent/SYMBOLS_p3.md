# Symbols (page 3 of 6)
Previous: [SYMBOLS_p2.md](SYMBOLS_p2.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `_transform_from_yaml` | method | `estorides_core/transforms.py:362` | `def _transform_from_yaml(raw, origin)` |
| `for_type` | method | `estorides_core/transforms.py:234` | `def for_type(self, ent_type)` |
| `iter_sse_events` | method | `estorides_core/transforms.py:406` | `def iter_sse_events(transform_id, ent_type, value, runner)` |
| `load_yaml_dir` | method | `estorides_core/transforms.py:280` | `def load_yaml_dir(self, directory)` |
| `register` | method | `estorides_core/transforms.py:231` | `def register(self, t)` |
| `run` | method | `estorides_core/transforms.py:122` | `def run(ent_type, value)` |
| `run` | method | `estorides_core/transforms.py:246` | `def run(self, transform_id, ent_type, value)` |
| `run` | method | `estorides_core/transforms.py:335` | `def run(ent_type, value)` |
| `sub` | method | `estorides_core/transforms.py:338` | `def sub(s, depth)` |
| `summary` | method | `estorides_core/transforms.py:83` | `def summary(self)` |
| `_strip_diacritics` | function | `estorides_core/transliteration.py:76` | `def _strip_diacritics(text)` |
| `consonant_skeleton` | function | `estorides_core/transliteration.py:112` | `def consonant_skeleton(text)` |
| `is_non_latin` | function | `estorides_core/transliteration.py:139` | `def is_non_latin(text)` |
| `to_latin` | function | `estorides_core/transliteration.py:87` | `def to_latin(text)` |
| `Query` | class | `estorides_core/validation.py:63` | `class Query` |
| `QueryValidationError` | class | `estorides_core/validation.py:55` | `class QueryValidationError(ValueError)` |
| `__init__` | method | `estorides_core/validation.py:57` | `def __init__(self, reason, message)` |
| `__str__` | method | `estorides_core/validation.py:69` | `def __str__(self)` |
| `_strip_and_collapse` | method | `estorides_core/validation.py:73` | `def _strip_and_collapse(text)` |
| `validate_query` | method | `estorides_core/validation.py:85` | `def validate_query(raw)` |
| `DefaultCred` | class | `estorides_core/vuln_correlation.py:14` | `class DefaultCred` |
| `VulnCorrelationResult` | class | `estorides_core/vuln_correlation.py:43` | `class VulnCorrelationResult` |
| `VulnEntry` | class | `estorides_core/vuln_correlation.py:24` | `class VulnEntry` |
| `_parsed_version` | method | `estorides_core/vuln_correlation.py:141` | `def _parsed_version(version)` |
| `_version_in_range` | method | `estorides_core/vuln_correlation.py:153` | `def _version_in_range(version, v_start, v_end)` |
| `compute_attack_readiness` | method | `estorides_core/vuln_correlation.py:228` | `def compute_attack_readiness(vulnerabilities)` |
| `correlate_technologies` | method | `estorides_core/vuln_correlation.py:202` | `def correlate_technologies(technologies)` |
| `lookup_cve_for_tech` | method | `estorides_core/vuln_correlation.py:169` | `def lookup_cve_for_tech(tech_name, version)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:19` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:38` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:52` | `def to_dict(self)` |
| `AuthGate` | class | `estorides_core/web_security.py:341` | `class AuthGate` |
| `WebSecurityConfig` | class | `estorides_core/web_security.py:87` | `class WebSecurityConfig` |
| `_cors_preflight` | method | `estorides_core/web_security.py:250` | `def _cors_preflight()` |
| `_current_gate` | method | `estorides_core/web_security.py:440` | `def _current_gate()` |
| `_env_str` | method | `estorides_core/web_security.py:137` | `def _env_str(name, default)` |
| `_extract_bearer_token` | method | `estorides_core/web_security.py:286` | `def _extract_bearer_token()` |
| `_redirect_to_https` | method | `estorides_core/web_security.py:203` | `def _redirect_to_https()` |
| `_security_headers` | method | `estorides_core/web_security.py:217` | `def _security_headers(resp)` |
| `auth_meta_for_index` | method | `estorides_core/web_security.py:362` | `def auth_meta_for_index(self)` |
| `auto_generated_token` | method | `estorides_core/web_security.py:444` | `def auto_generated_token()` |
| `build_https_url` | function | `estorides_core/web_security.py:58` | `def build_https_url(public_host, path, query_string)` |
| `check` | method | `estorides_core/web_security.py:354` | `def check(self)` |
| `enabled` | method | `estorides_core/web_security.py:351` | `def enabled(self)` |
| `install_auth_gate` | method | `estorides_core/web_security.py:421` | `def install_auth_gate(app, gate)` |
| `install_security` | method | `estorides_core/web_security.py:169` | `def install_security(app, cfg)` |
| `is_cors_enabled` | method | `estorides_core/web_security.py:128` | `def is_cors_enabled(self)` |
| `is_origin_allowed` | method | `estorides_core/web_security.py:132` | `def is_origin_allowed(self)` |
| `issue_session_cookie_kwargs` | method | `estorides_core/web_security.py:371` | `def issue_session_cookie_kwargs(self)` |
| `load_security_config` | method | `estorides_core/web_security.py:144` | `def load_security_config()` |
| `make_auth_gate` | method | `estorides_core/web_security.py:321` | `def make_auth_gate()` |
| `require_auth` | method | `estorides_core/web_security.py:388` | `def require_auth(view)` |
| `wrapper` | method | `estorides_core/web_security.py:402` | `def wrapper()` |
| `_have_age` | function | `estorides_export/encryption.py:47` | `def _have_age()` |
| `encrypt_file` | function | `estorides_export/encryption.py:51` | `def encrypt_file(plaintext_path, recipient_pubkey)` |
| `export_misp_encrypted` | function | `estorides_export/encryption.py:128` | `def export_misp_encrypted(kg, recipient_pubkey, path)` |
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
| `_drive` | method | `estorides_web.py:1550` | `def _drive()` |
| `_err` | method | `estorides_web.py:1281` | `def _err()` |
| `_gen` | method | `estorides_web.py:1286` | `def _gen()` |
| `_graph_rag_block` | method | `estorides_web.py:234` | `def _graph_rag_block(query, budget_tokens)` |
| `_new_stream_job_id` | method | `estorides_web.py:185` | `def _new_stream_job_id()` |
| `_provides` | function | `estorides_web.py:81` | `def _provides(service, message)` |
| `_rate_limit_decorator` | method | `estorides_web.py:190` | `def _rate_limit_decorator()` |
| `_run` | method | `estorides_web.py:1659` | `def _run()` |
| `_send_and_cleanup` | function | `estorides_web.py:133` | `def _send_and_cleanup(p, tmpdir)` |
| `_serve_loop` | method | `estorides_web.py:1710` | `def _serve_loop()` |
| `_shape_for_ui` | method | `estorides_web.py:1723` | `def _shape_for_ui(result)` |
| `_sse_response` | function | `estorides_web.py:76` | `def _sse_response(gen)` |
| `_watch_runner` | method | `estorides_web.py:1067` | `def _watch_runner(swatch)` |
| `admin_sources` | method | `estorides_web.py:904` | `def admin_sources()` |
| `api_alerts_channels` | method | `estorides_web.py:1192` | `def api_alerts_channels()` |
| `api_alerts_test` | method | `estorides_web.py:1200` | `def api_alerts_test()` |
| `api_analyze_stream` | method | `estorides_web.py:1646` | `def api_analyze_stream()` |
| `api_cases_delete` | method | `estorides_web.py:643` | `def api_cases_delete(case_id)` |
| `api_cases_diff` | method | `estorides_web.py:674` | `def api_cases_diff()` |
| `api_cases_get` | method | `estorides_web.py:629` | `def api_cases_get(case_id)` |
| `api_cases_list` | method | `estorides_web.py:616` | `def api_cases_list()` |
| `api_cases_save` | method | `estorides_web.py:651` | `def api_cases_save(case_id)` |
| `api_discover_jobs` | method | `estorides_web.py:1452` | `def api_discover_jobs()` |
| `api_discover_start` | method | `estorides_web.py:1406` | `def api_discover_start()` |
| `api_discover_stop` | method | `estorides_web.py:1458` | `def api_discover_stop()` |
| `api_discover_stream` | method | `estorides_web.py:1470` | `def api_discover_stream()` |
| `api_export` | method | `estorides_web.py:538` | `def api_export(fmt)` |
| `api_feeds` | method | `estorides_web.py:507` | `def api_feeds()` |
| `api_fusion_analytics_consensus` | method | `estorides_web.py:884` | `def api_fusion_analytics_consensus(eid)` |
| `api_fusion_analytics_corroboration_matrix` | method | `estorides_web.py:1004` | `def api_fusion_analytics_corroboration_matrix()` |
| `api_fusion_analytics_entity_summary` | method | `estorides_web.py:864` | `def api_fusion_analytics_entity_summary(eid)` |
| `api_fusion_analytics_entity_timeline` | method | `estorides_web.py:854` | `def api_fusion_analytics_entity_timeline(eid)` |
| `api_fusion_analytics_source_stats` | method | `estorides_web.py:874` | `def api_fusion_analytics_source_stats(source_name)` |
| `api_fusion_analytics_top_changed` | method | `estorides_web.py:894` | `def api_fusion_analytics_top_changed()` |
| `api_fusion_entities` | method | `estorides_web.py:815` | `def api_fusion_entities()` |
| `api_fusion_entity` | method | `estorides_web.py:836` | `def api_fusion_entity(eid)` |
| `api_fusion_sources` | method | `estorides_web.py:806` | `def api_fusion_sources()` |
| `api_fusion_stats` | method | `estorides_web.py:798` | `def api_fusion_stats()` |
| `api_graph` | method | `estorides_web.py:418` | `def api_graph()` |
| `api_intel_graph` | method | `estorides_web.py:738` | `def api_intel_graph()` |
| `api_intel_resolve` | method | `estorides_web.py:699` | `def api_intel_resolve()` |
| `api_intel_stats` | method | `estorides_web.py:777` | `def api_intel_stats()` |
| `api_ollama_status` | method | `estorides_web.py:356` | `def api_ollama_status()` |
| `api_osiris_bgp` | method | `estorides_web.py:1309` | `def api_osiris_bgp()` |
| `api_osiris_github` | method | `estorides_web.py:1351` | `def api_osiris_github()` |
| `api_osiris_kev` | method | `estorides_web.py:1379` | `def api_osiris_kev()` |
| `api_osiris_leaks` | method | `estorides_web.py:1365` | `def api_osiris_leaks()` |
| `api_osiris_mac` | method | `estorides_web.py:1323` | `def api_osiris_mac()` |
| `api_osiris_malware` | method | `estorides_web.py:1388` | `def api_osiris_malware()` |
| `api_osiris_phone` | method | `estorides_web.py:1337` | `def api_osiris_phone()` |
| `api_osiris_threats` | method | `estorides_web.py:1393` | `def api_osiris_threats()` |
| `api_run` | method | `estorides_web.py:362` | `def api_run()` |
| `api_run_stream` | method | `estorides_web.py:1599` | `def api_run_stream()` |
| `api_run_stream_start` | method | `estorides_web.py:1520` | `def api_run_stream_start()` |
| `api_run_stream_stop` | method | `estorides_web.py:1587` | `def api_run_stream_stop()` |
| `api_scheduler_status` | method | `estorides_web.py:1216` | `def api_scheduler_status()` |
| `api_socmint_discover` | method | `estorides_web.py:1048` | `def api_socmint_discover()` |
| `api_socmint_platforms` | method | `estorides_web.py:1040` | `def api_socmint_platforms()` |
| `api_socmint_resolve` | method | `estorides_web.py:1018` | `def api_socmint_resolve()` |
| `api_sources_yaml_create` | method | `estorides_web.py:947` | `def api_sources_yaml_create()` |
| `api_sources_yaml_delete` | method | `estorides_web.py:987` | `def api_sources_yaml_delete(name)` |
| `api_sources_yaml_list` | method | `estorides_web.py:921` | `def api_sources_yaml_list()` |
| `api_sources_yaml_update` | method | `estorides_web.py:968` | `def api_sources_yaml_update(name)` |
| `api_status` | method | `estorides_web.py:350` | `def api_status()` |
| `api_transform_run` | method | `estorides_web.py:1248` | `def api_transform_run()` |
| `api_transform_stream` | method | `estorides_web.py:1270` | `def api_transform_stream()` |
| `api_transforms` | method | `estorides_web.py:1234` | `def api_transforms()` |
| `api_watch_create` | method | `estorides_web.py:1100` | `def api_watch_create()` |
| `api_watch_delete` | method | `estorides_web.py:1146` | `def api_watch_delete(watch_id)` |
| `api_watch_disable` | method | `estorides_web.py:1170` | `def api_watch_disable(watch_id)` |
| `api_watch_enable` | method | `estorides_web.py:1157` | `def api_watch_enable(watch_id)` |
| `api_watch_get` | method | `estorides_web.py:1134` | `def api_watch_get(watch_id)` |
| `api_watch_history` | method | `estorides_web.py:1182` | `def api_watch_history(watch_id)` |
| `api_watch_list` | method | `estorides_web.py:1091` | `def api_watch_list()` |
| `create_app` | method | `estorides_web.py:256` | `def create_app()` |
| `deco` | method | `estorides_web.py:88` | `def deco(view)` |
| `deco` | method | `estorides_web.py:197` | `def deco(view)` |
| `done` | method | `estorides_web.py:175` | `def done(self)` |
| `gen` | method | `estorides_web.py:1483` | `def gen()` |
| `gen` | method | `estorides_web.py:1605` | `def gen()` |
| `gen` | method | `estorides_web.py:1681` | `def gen()` |
| `healthz` | method | `estorides_web.py:292` | `def healthz()` |
| `index` | method | `estorides_web.py:329` | `def index()` |
| `metrics` | method | `estorides_web.py:317` | `def metrics()` |
| `openapi_doc` | method | `estorides_web.py:324` | `def openapi_doc()` |
| `readyz` | method | `estorides_web.py:303` | `def readyz()` |
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
| `CLUSTER_PALETTE` | function | `static/js/estorides.js:1135` | `` |
| `TELEMETRY` | function | `static/js/estorides.js:41` | `` |
| `_installErrMsg` | function | `static/js/estorides.js:243` | `` |
| `_redrawGraph` | function | `static/js/estorides.js:1720` | `` |
| `_sanitizeInput` | function | `static/js/estorides.js:2567` | `` |
| `_sseAuthToken` | function | `static/js/estorides.js:2981` | `` |
| `_sseUrl` | function | `static/js/estorides.js:2985` | `` |
| `actions` | function | `static/js/estorides.js:2576` | `` |
| `add` | function | `static/js/estorides.js:1526` | `` |
| `addDiscoverEntityToTab` | function | `static/js/estorides.js:3163` | `` |
| `addText` | function | `static/js/estorides.js:1532` | `` |
| `analyseEntity` | function | `static/js/estorides.js:951` | `` |
| `appendStreamEntity` | function | `static/js/estorides.js:676` | `` |
| `appendStreamObservation` | function | `static/js/estorides.js:654` | `` |
| `applyLevelStyles` | function | `static/js/estorides.js:1379` | `` |
| `applyResultFilters` | function | `static/js/estorides.js:259` | `` |
| `attribute` | class | `static/js/estorides.js:2921` | `` |
| `bindResultFilters` | function | `static/js/estorides.js:280` | `` |
| `boxQ` | function | `static/js/estorides.js:880` | `` |
| `buildCaseMapCoords` | function | `static/js/estorides.js:2302` | `` |
| `buildMapCoords` | function | `static/js/estorides.js:1852` | `` |
| `buildResultCard` | function | `static/js/estorides.js:138` | `` |
| `c` | function | `static/js/estorides.js:1168` | `` |
| `c` | function | `static/js/estorides.js:1251` | `` |
| `caseActionDiff` | function | `static/js/estorides.js:2445` | `` |
| `caseActionReport` | function | `static/js/estorides.js:2506` | `` |
| `caseActionSave` | function | `static/js/estorides.js:2424` | `` |
| `cat` | function | `static/js/estorides.js:261` | `` |
| `check` | function | `static/js/estorides.js:3222` | `` |
| `cid` | function | `static/js/estorides.js:1188` | `` |
| `clearAll` | function | `static/js/estorides.js:705` | `` |
| `clearMap` | function | `static/js/estorides.js:336` | `` |
| `close` | function | `static/js/estorides.js:2590` | `` |
| `clusterColor` | function | `static/js/estorides.js:1166` | `` |
| `colorFor` | function | `static/js/estorides.js:1952` | `` |
| `colorForKind` | function | `static/js/estorides.js:2052` | `` |
| `confirmModal` | function | `static/js/estorides.js:2629` | `` |
| `debounce` | function | `static/js/estorides.js:2346` | `` |
| `deriveClusters` | function | `static/js/estorides.js:1185` | `` |
| `detectQueryTypeLocal` | function | `static/js/estorides.js:55` | `` |
| `doSearch` | function | `static/js/estorides.js:2875` | `` |
| `drawGraph` | function | `static/js/estorides.js:2170` | `` |
| `drawGraphWithExtras` | function | `static/js/estorides.js:1078` | `` |
| `drawHulls` | function | `static/js/estorides.js:1689` | `` |
| `entities` | function | `static/js/estorides.js:2227` | `` |
| `escapeAttr` | function | `static/js/estorides.js:1816` | `` |
| `escapeHTML` | function | `static/js/estorides.js:2396` | `` |
| `escapeHtml` | function | `static/js/estorides.js:3191` | `` |
| `expandNode` | function | `static/js/estorides.js:984` | `` |
| `filterTimeline` | function | `static/js/estorides.js:2121` | `` |
| `flush` | function | `static/js/estorides.js:909` | `` |
| `flush` | function | `static/js/estorides.js:1426` | `` |
| `flushDiscoverEntities` | function | `static/js/estorides.js:3203` | `` |
| `fmtTime` | function | `static/js/estorides.js:2110` | `` |
| `focusGraphNodeByValue` | function | `static/js/estorides.js:301` | `` |
| `focusNode` | function | `static/js/estorides.js:1387` | `` |
| `frac` | function | `static/js/estorides.js:2097` | `` |
| `handleDiscoverEvent` | function | `static/js/estorides.js:3124` | `` |
| `handleRunStreamEvent` | function | `static/js/estorides.js:616` | `` |
| `hideContextMenu` | function | `static/js/estorides.js:1242` | `` |
| `hideDiscoverProgress` | function | `static/js/estorides.js:3028` | `` |
| `hideTooltip` | function | `static/js/estorides.js:1198` | `` |
| `hideWorkingIndicator` | function | `static/js/estorides.js:1737` | `` |
| `k` | function | `static/js/estorides.js:1028` | `` |
| `k` | function | `static/js/estorides.js:1493` | `` |
| `labelFor` | function | `static/js/estorides.js:1250` | `` |
| `levelOf` | function | `static/js/estorides.js:1162` | `` |
| `loadAnalysisModels` | function | `static/js/estorides.js:787` | `` |
| `loadCases` | function | `static/js/estorides.js:2200` | `` |
| `loadFusionEntityDetail` | function | `static/js/estorides.js:2913` | `` |
| `loadFusionSearch` | function | `static/js/estorides.js:2868` | `` |
| `loadFusionStats` | function | `static/js/estorides.js:2820` | `` |
| `loadFusionTab` | function | `static/js/estorides.js:2814` | `` |
| `loadFusionTopChanged` | function | `static/js/estorides.js:2839` | `` |
| `loadSidebarCollapsed` | function | `static/js/estorides.js:2735` | `` |
| `loadSidebarWidth` | function | `static/js/estorides.js:2721` | `` |
| `makeModelPill` | function | `static/js/estorides.js:806` | `` |
| `maybePlotDiscoverEntity` | function | `static/js/estorides.js:3196` | `` |
| `mergeExpansionIntoGraph` | function | `static/js/estorides.js:1014` | `` |
| `obs` | function | `static/js/estorides.js:2064` | `` |
| `obs` | function | `static/js/estorides.js:2228` | `` |
| `on` | class | `static/js/estorides.js:1905` | `` |
| `openCaseDetail` | function | `static/js/estorides.js:2226` | `` |
| `openModal` | function | `static/js/estorides.js:2570` | `` |
| `out` | function | `static/js/estorides.js:246` | `` |
| `plotPoints` | function | `static/js/estorides.js:341` | `` |
| `pollToolInstall` | function | `static/js/estorides.js:220` | `` |
| `populateCategoryFilter` | function | `static/js/estorides.js:253` | `` |
| `promptModal` | function | `static/js/estorides.js:2605` | `` |
| `pump` | function | `static/js/estorides.js:930` | `` |
| `purifyHTML` | function | `static/js/estorides.js:1212` | `` |
| `pushLink` | function | `static/js/estorides.js:1102` | `` |
| `q` | function | `static/js/estorides.js:2201` | `` |
| `reanalyze` | function | `static/js/estorides.js:861` | `` |
| `removed` | function | `static/js/estorides.js:2476` | `` |
| `renderAnalysis` | function | `static/js/estorides.js:819` | `` |
| `renderAnalysisModels` | function | `static/js/estorides.js:794` | `` |
| `renderCaseDiffPanel` | function | `static/js/estorides.js:2465` | `` |
| `renderCaseItem` | function | `static/js/estorides.js:2320` | `` |
| `renderEntities` | function | `static/js/estorides.js:1971` | `` |
| `renderGraphCore` | function | `static/js/estorides.js:1619` | `` |
| `renderGraphSummary` | function | `static/js/estorides.js:2023` | `` |
| `renderMarkdownInto` | function | `static/js/estorides.js:834` | `` |
| `renderResult` | function | `static/js/estorides.js:739` | `` |
| `renderTieredResults` | function | `static/js/estorides.js:1750` | `` |
| `renderTimeline` | function | `static/js/estorides.js:2060` | `` |
| `replotStreamData` | function | `static/js/estorides.js:443` | `` |
| `requestToolInstall` | function | `static/js/estorides.js:197` | `` |
| `resolverTypeFor` | function | `static/js/estorides.js:1142` | `` |
| `restoreCaseToWorkspace` | function | `static/js/estorides.js:2281` | `` |
| `rows` | function | `static/js/estorides.js:2473` | `` |
| `runQuery` | function | `static/js/estorides.js:470` | `` |
| `runQueryBlocking` | function | `static/js/estorides.js:540` | `` |
| `runTransform` | function | `static/js/estorides.js:1399` | `` |
| `runTransformStream` | function | `static/js/estorides.js:1420` | `` |
| `safeColor` | function | `static/js/estorides.js:1176` | `` |
| `saveLevelOverrides` | function | `static/js/estorides.js:1158` | `` |
| `saveSidebarCollapsed` | function | `static/js/estorides.js:2743` | `` |
| `saveSidebarWidth` | function | `static/js/estorides.js:2732` | `` |
| `saved` | function | `static/js/estorides.js:2324` | `` |
| `scheduleRender` | function | `static/js/estorides.js:904` | `` |
| `searchEntity` | function | `static/js/estorides.js:573` | `` |
| `selectNode` | function | `static/js/estorides.js:1515` | `` |
| `set` | function | `static/js/estorides.js:32` | `` |
| `setDiscoverProgress` | function | `static/js/estorides.js:3016` | `` |
| `setNodeLevel` | function | `static/js/estorides.js:1370` | `` |
| `setRunProgress` | function | `static/js/estorides.js:86` | `` |
| `setSanitizedHTML` | function | `static/js/estorides.js:1223` | `` |
| `setStatus` | function | `static/js/estorides.js:733` | `` |
| `setStatus` | function | `static/js/estorides.js:3009` | `` |
| `setStatusDot` | function | `static/js/estorides.js:1726` | `` |
| `setThinkingVisible` | function | `static/js/estorides.js:849` | `` |
| `setVisible` | function | `static/js/estorides.js:12` | `` |
| `showBridgeTooltip` | function | `static/js/estorides.js:1247` | `` |
| `showContextMenu` | function | `static/js/estorides.js:1295` | `` |
| `showEmptyState` | function | `static/js/estorides.js:107` | `` |
| `showFriendlyError` | function | `static/js/estorides.js:288` | `` |
| `showNodeTooltip` | function | `static/js/estorides.js:1276` | `` |
| `showReportModal` | function | `static/js/estorides.js:2542` | `` |
| `showToast` | function | `static/js/estorides.js:66` | `` |
| `showTooltipAt` | function | `static/js/estorides.js:1232` | `` |
| `showWorkingIndicator` | function | `static/js/estorides.js:1732` | `` |
| `sig` | function | `static/js/estorides.js:678` | `` |
| `sig` | function | `static/js/estorides.js:3168` | `` |
| `startDiscover` | function | `static/js/estorides.js:3033` | `` |
| `status` | function | `static/js/estorides.js:148` | `` |
| `status` | function | `static/js/estorides.js:262` | `` |
| `stopDiscover` | function | `static/js/estorides.js:3107` | `` |
| `stopRunStream` | function | `static/js/estorides.js:455` | `` |
| `summariseObservation` | function | `static/js/estorides.js:113` | `` |
| `switchCanvasTab` | function | `static/js/estorides.js:314` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:310` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:2801` | `` |
| `tag` | function | `static/js/estorides.js:2691` | `` |
| `text` | function | `static/js/estorides.js:260` | `` |
| `to` | class | `static/js/estorides.js:401` | `` |
| `toggleThinking` | function | `static/js/estorides.js:856` | `` |
| `toggleTierSection` | function | `static/js/estorides.js:1742` | `` |
| `toolBinary` | function | `static/js/estorides.js:142` | `` |
| `tr` | function | `static/js/estorides.js:1345` | `` |
| `tr` | function | `static/js/estorides.js:1583` | `` |
| `truncate` | function | `static/js/estorides.js:2401` | `` |
| `undoGraph` | function | `static/js/estorides.js:1480` | `` |
| `updateQueryChip` | function | `static/js/estorides.js:76` | `` |
| `validCoord` | function | `static/js/estorides.js:1948` | `` |
| `a` | function | `static/js/graph_force.js:270` | `` |
| `adaptLocal` | function | `static/js/graph_force.js:66` | `` |
| `applyFilters` | function | `static/js/graph_force.js:644` | `` |
| `applyLayout3D` | function | `static/js/graph_force.js:475` | `` |
| `cid` | function | `static/js/graph_force.js:88` | `` |
| `clearSelection` | function | `static/js/graph_force.js:516` | `` |
| `clusterForce` | function | `static/js/graph_force.js:278` | `` |
| `collideForce` | function | `static/js/graph_force.js:320` | `` |
| `colorOf` | function | `static/js/graph_force.js:194` | `` |
| `computeHighlight` | function | `static/js/graph_force.js:218` | `` |
| `currentRaw` | function | `static/js/graph_force.js:121` | `` |
| `dimmed` | function | `static/js/graph_force.js:195` | `` |
| `edges` | function | `static/js/graph_force.js:659` | `` |
| `entities` | function | `static/js/graph_force.js:179` | `` |
| `esc` | function | `static/js/graph_force.js:25` | `` |
| `fail` | function | `static/js/graph_force.js:52` | `` |
| `fam` | function | `static/js/graph_force.js:89` | `` |
| `famAnchor` | function | `static/js/graph_force.js:263` | `` |
| `famOf` | function | `static/js/graph_force.js:273` | `` |
| `fn` | function | `static/js/graph_force.js:661` | `` |
| `focusFamily` | function | `static/js/graph_force.js:529` | `` |
| `force` | function | `static/js/graph_force.js:280` | `` |
| `force` | function | `static/js/graph_force.js:305` | `` |
| `force` | function | `static/js/graph_force.js:322` | `` |
| `hiddenKind` | function | `static/js/graph_force.js:196` | `` |
| `hud` | function | `static/js/graph_force.js:560` | `` |
| `indexRaw` | function | `static/js/graph_force.js:163` | `` |
| `linkStrengthFn` | function | `static/js/graph_force.js:349` | `` |
| `lkey` | function | `static/js/graph_force.js:193` | `` |
| `m` | function | `static/js/graph_force.js:335` | `` |
| `markFamilies` | function | `static/js/graph_force.js:554` | `` |
| `mount3D` | function | `static/js/graph_force.js:386` | `` |
| `nodes` | function | `static/js/graph_force.js:652` | `` |
| `onSelect3D` | function | `static/js/graph_force.js:492` | `` |
| `ordered` | function | `static/js/graph_force.js:80` | `` |
| `pickHit` | function | `static/js/graph_force.js:736` | `` |
| `radialForce` | function | `static/js/graph_force.js:303` | `` |
| `radius` | function | `static/js/graph_force.js:345` | `` |
| `readHash` | function | `static/js/graph_force.js:765` | `` |
| `rebuildRaw` | function | `static/js/graph_force.js:137` | `` |
| `refresh3D` | function | `static/js/graph_force.js:459` | `` |
| `refreshFamList` | function | `static/js/graph_force.js:258` | `` |
| `reload3D` | function | `static/js/graph_force.js:465` | `` |
| `renderLegend` | function | `static/js/graph_force.js:590` | `` |
| `resize3D` | function | `static/js/graph_force.js:470` | `` |
| `ringOf` | function | `static/js/graph_force.js:295` | `` |
| `runSearch` | function | `static/js/graph_force.js:670` | `` |
| `s` | function | `static/js/graph_force.js:173` | `` |
| `s` | function | `static/js/graph_force.js:211` | `` |
| `s` | function | `static/js/graph_force.js:542` | `` |
| `setEngineButtons` | function | `static/js/graph_force.js:365` | `` |
| `settings` | function | `static/js/graph_force.js:59` | `` |
| `short` | function | `static/js/graph_force.js:21` | `` |
| `show3DChrome` | function | `static/js/graph_force.js:374` | `` |
| `src` | function | `static/js/graph_force.js:146` | `` |
| `stat` | function | `static/js/graph_force.js:564` | `` |
| `syncIsolateBtn` | function | `static/js/graph_force.js:787` | `` |
| `t` | function | `static/js/graph_force.js:174` | `` |
| `t` | function | `static/js/graph_force.js:212` | `` |
| `t` | function | `static/js/graph_force.js:543` | `` |
| `tag` | function | `static/js/graph_force.js:892` | `` |
| `tip` | function | `static/js/graph_force.js:241` | `` |
| `to2D` | function | `static/js/graph_force.js:756` | `` |
| `to3D` | function | `static/js/graph_force.js:747` | `` |
| `toast` | function | `static/js/graph_force.js:44` | `` |
| `toggle` | function | `static/js/graph_force.js:817` | `` |
| `visiblePayload` | function | `static/js/graph_force.js:201` | `` |
| `wireToolbar` | function | `static/js/graph_force.js:792` | `` |
| `writeHash` | function | `static/js/graph_force.js:780` | `` |
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

Next: [SYMBOLS_p4.md](SYMBOLS_p4.md)
