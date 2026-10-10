# Symbols (page 3 of 7)
Previous: [SYMBOLS_p2.md](SYMBOLS_p2.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `from_failure` | method | `estorides_core/tool_runner.py:59` | `def from_failure(cls, tool_name, error_code, error_message, duration_s, exit_code, stdout, stderr, parsed_entities)` |
| `run_tool` | method | `estorides_core/tool_runner.py:156` | `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)` |
| `to_dict` | method | `estorides_core/tool_runner.py:51` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/tool_runner.py:93` | `def to_dict(self)` |
| `Transform` | class | `estorides_core/transforms.py:71` | `class Transform` |
| `TransformRegistry` | class | `estorides_core/transforms.py:225` | `class TransformRegistry` |
| `_T` | method | `estorides_core/transforms.py:441` | `def _T(id, label, tier, applies, runner, description, output_types, cost)` |
| `__init__` | method | `estorides_core/transforms.py:228` | `def __init__(self)` |
| `_empty` | method | `estorides_core/transforms.py:96` | `def _empty(root_type, value)` |
| `_filter_runner` | method | `estorides_core/transforms.py:121` | `def _filter_runner(relations)` |
| `_norm` | method | `estorides_core/transforms.py:130` | `def _norm(s)` |
| `_osiris` | method | `estorides_core/transforms.py:135` | `def _osiris()` |
| `_resolver_filtered` | method | `estorides_core/transforms.py:100` | `def _resolver_filtered(ent_type, value, relations)` |
| `_run_bgp` | method | `estorides_core/transforms.py:143` | `def _run_bgp(ent_type, value)` |
| `_run_github` | method | `estorides_core/transforms.py:194` | `def _run_github(ent_type, value)` |
| `_run_leaks` | method | `estorides_core/transforms.py:169` | `def _run_leaks(ent_type, value)` |
| `_static_runner` | method | `estorides_core/transforms.py:332` | `def _static_runner(nodes_tpl, links_tpl)` |
| `_str_list` | method | `estorides_core/transforms.py:322` | `def _str_list(raw)` |
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
| `_drive` | method | `estorides_web.py:1564` | `def _drive()` |
| `_err` | method | `estorides_web.py:1295` | `def _err()` |
| `_gen` | method | `estorides_web.py:1300` | `def _gen()` |
| `_graph_rag_block` | method | `estorides_web.py:234` | `def _graph_rag_block(query, budget_tokens)` |
| `_new_stream_job_id` | method | `estorides_web.py:185` | `def _new_stream_job_id()` |
| `_provides` | function | `estorides_web.py:81` | `def _provides(service, message)` |
| `_rate_limit_decorator` | method | `estorides_web.py:190` | `def _rate_limit_decorator()` |
| `_run` | method | `estorides_web.py:1673` | `def _run()` |
| `_send_and_cleanup` | function | `estorides_web.py:133` | `def _send_and_cleanup(p, tmpdir)` |
| `_serve_loop` | method | `estorides_web.py:1724` | `def _serve_loop()` |
| `_shape_for_ui` | method | `estorides_web.py:1737` | `def _shape_for_ui(result)` |
| `_sse_response` | function | `estorides_web.py:76` | `def _sse_response(gen)` |
| `_watch_runner` | method | `estorides_web.py:1081` | `def _watch_runner(swatch)` |
| `admin_sources` | method | `estorides_web.py:918` | `def admin_sources()` |
| `api_alerts_channels` | method | `estorides_web.py:1206` | `def api_alerts_channels()` |
| `api_alerts_test` | method | `estorides_web.py:1214` | `def api_alerts_test()` |
| `api_analyze_stream` | method | `estorides_web.py:1660` | `def api_analyze_stream()` |
| `api_cases_delete` | method | `estorides_web.py:657` | `def api_cases_delete(case_id)` |
| `api_cases_diff` | method | `estorides_web.py:688` | `def api_cases_diff()` |
| `api_cases_get` | method | `estorides_web.py:643` | `def api_cases_get(case_id)` |
| `api_cases_list` | method | `estorides_web.py:630` | `def api_cases_list()` |
| `api_cases_save` | method | `estorides_web.py:665` | `def api_cases_save(case_id)` |
| `api_discover_jobs` | method | `estorides_web.py:1466` | `def api_discover_jobs()` |
| `api_discover_start` | method | `estorides_web.py:1420` | `def api_discover_start()` |
| `api_discover_stop` | method | `estorides_web.py:1472` | `def api_discover_stop()` |
| `api_discover_stream` | method | `estorides_web.py:1484` | `def api_discover_stream()` |
| `api_export` | method | `estorides_web.py:552` | `def api_export(fmt)` |
| `api_feeds` | method | `estorides_web.py:521` | `def api_feeds()` |
| `api_fusion_analytics_consensus` | method | `estorides_web.py:898` | `def api_fusion_analytics_consensus(eid)` |
| `api_fusion_analytics_corroboration_matrix` | method | `estorides_web.py:1018` | `def api_fusion_analytics_corroboration_matrix()` |
| `api_fusion_analytics_entity_summary` | method | `estorides_web.py:878` | `def api_fusion_analytics_entity_summary(eid)` |
| `api_fusion_analytics_entity_timeline` | method | `estorides_web.py:868` | `def api_fusion_analytics_entity_timeline(eid)` |
| `api_fusion_analytics_source_stats` | method | `estorides_web.py:888` | `def api_fusion_analytics_source_stats(source_name)` |
| `api_fusion_analytics_top_changed` | method | `estorides_web.py:908` | `def api_fusion_analytics_top_changed()` |
| `api_fusion_entities` | method | `estorides_web.py:829` | `def api_fusion_entities()` |
| `api_fusion_entity` | method | `estorides_web.py:850` | `def api_fusion_entity(eid)` |
| `api_fusion_sources` | method | `estorides_web.py:820` | `def api_fusion_sources()` |
| `api_fusion_stats` | method | `estorides_web.py:812` | `def api_fusion_stats()` |
| `api_graph` | method | `estorides_web.py:418` | `def api_graph()` |
| `api_intel_graph` | method | `estorides_web.py:752` | `def api_intel_graph()` |
| `api_intel_resolve` | method | `estorides_web.py:713` | `def api_intel_resolve()` |
| `api_intel_stats` | method | `estorides_web.py:791` | `def api_intel_stats()` |
| `api_ollama_status` | method | `estorides_web.py:356` | `def api_ollama_status()` |
| `api_osiris_bgp` | method | `estorides_web.py:1323` | `def api_osiris_bgp()` |
| `api_osiris_github` | method | `estorides_web.py:1365` | `def api_osiris_github()` |
| `api_osiris_kev` | method | `estorides_web.py:1393` | `def api_osiris_kev()` |
| `api_osiris_leaks` | method | `estorides_web.py:1379` | `def api_osiris_leaks()` |
| `api_osiris_mac` | method | `estorides_web.py:1337` | `def api_osiris_mac()` |
| `api_osiris_malware` | method | `estorides_web.py:1402` | `def api_osiris_malware()` |
| `api_osiris_phone` | method | `estorides_web.py:1351` | `def api_osiris_phone()` |
| `api_osiris_threats` | method | `estorides_web.py:1407` | `def api_osiris_threats()` |
| `api_run` | method | `estorides_web.py:362` | `def api_run()` |
| `api_run_stream` | method | `estorides_web.py:1613` | `def api_run_stream()` |
| `api_run_stream_start` | method | `estorides_web.py:1534` | `def api_run_stream_start()` |
| `api_run_stream_stop` | method | `estorides_web.py:1601` | `def api_run_stream_stop()` |
| `api_scheduler_status` | method | `estorides_web.py:1230` | `def api_scheduler_status()` |
| `api_socmint_discover` | method | `estorides_web.py:1062` | `def api_socmint_discover()` |
| `api_socmint_platforms` | method | `estorides_web.py:1054` | `def api_socmint_platforms()` |
| `api_socmint_resolve` | method | `estorides_web.py:1032` | `def api_socmint_resolve()` |
| `api_sources_yaml_create` | method | `estorides_web.py:961` | `def api_sources_yaml_create()` |
| `api_sources_yaml_delete` | method | `estorides_web.py:1001` | `def api_sources_yaml_delete(name)` |
| `api_sources_yaml_list` | method | `estorides_web.py:935` | `def api_sources_yaml_list()` |
| `api_sources_yaml_update` | method | `estorides_web.py:982` | `def api_sources_yaml_update(name)` |
| `api_status` | method | `estorides_web.py:350` | `def api_status()` |
| `api_transform_run` | method | `estorides_web.py:1262` | `def api_transform_run()` |
| `api_transform_stream` | method | `estorides_web.py:1284` | `def api_transform_stream()` |
| `api_transforms` | method | `estorides_web.py:1248` | `def api_transforms()` |
| `api_watch_create` | method | `estorides_web.py:1114` | `def api_watch_create()` |
| `api_watch_delete` | method | `estorides_web.py:1160` | `def api_watch_delete(watch_id)` |
| `api_watch_disable` | method | `estorides_web.py:1184` | `def api_watch_disable(watch_id)` |
| `api_watch_enable` | method | `estorides_web.py:1171` | `def api_watch_enable(watch_id)` |
| `api_watch_get` | method | `estorides_web.py:1148` | `def api_watch_get(watch_id)` |
| `api_watch_history` | method | `estorides_web.py:1196` | `def api_watch_history(watch_id)` |
| `api_watch_list` | method | `estorides_web.py:1105` | `def api_watch_list()` |
| `create_app` | method | `estorides_web.py:256` | `def create_app()` |
| `deco` | method | `estorides_web.py:88` | `def deco(view)` |
| `deco` | method | `estorides_web.py:197` | `def deco(view)` |
| `done` | method | `estorides_web.py:175` | `def done(self)` |
| `gen` | method | `estorides_web.py:1497` | `def gen()` |
| `gen` | method | `estorides_web.py:1619` | `def gen()` |
| `gen` | method | `estorides_web.py:1695` | `def gen()` |
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
| `CLUSTER_PALETTE` | function | `static/js/estorides.js:1146` | `` |
| `TELEMETRY` | function | `static/js/estorides.js:41` | `` |
| `_installErrMsg` | function | `static/js/estorides.js:243` | `` |
| `_redrawGraph` | function | `static/js/estorides.js:1751` | `` |
| `_sanitizeInput` | function | `static/js/estorides.js:2598` | `` |
| `_sseAuthToken` | function | `static/js/estorides.js:3012` | `` |
| `_sseUrl` | function | `static/js/estorides.js:3016` | `` |
| `actions` | function | `static/js/estorides.js:2607` | `` |
| `add` | function | `static/js/estorides.js:1539` | `` |
| `addDiscoverEntityToTab` | function | `static/js/estorides.js:3194` | `` |
| `addText` | function | `static/js/estorides.js:1545` | `` |
| `analyseEntity` | function | `static/js/estorides.js:951` | `` |
| `appendStreamEntity` | function | `static/js/estorides.js:676` | `` |
| `appendStreamObservation` | function | `static/js/estorides.js:654` | `` |
| `applyLevelStyles` | function | `static/js/estorides.js:1390` | `` |
| `applyResultFilters` | function | `static/js/estorides.js:259` | `` |
| `attribute` | class | `static/js/estorides.js:2952` | `` |
| `barH` | function | `static/js/estorides.js:1402` | `` |
| `barH` | function | `static/js/estorides.js:1651` | `` |
| `bindResultFilters` | function | `static/js/estorides.js:280` | `` |
| `boxQ` | function | `static/js/estorides.js:880` | `` |
| `buildCaseMapCoords` | function | `static/js/estorides.js:2333` | `` |
| `buildMapCoords` | function | `static/js/estorides.js:1883` | `` |
| `buildResultCard` | function | `static/js/estorides.js:138` | `` |
| `c` | function | `static/js/estorides.js:1179` | `` |
| `c` | function | `static/js/estorides.js:1262` | `` |
| `caseActionDiff` | function | `static/js/estorides.js:2476` | `` |
| `caseActionReport` | function | `static/js/estorides.js:2537` | `` |
| `caseActionSave` | function | `static/js/estorides.js:2455` | `` |
| `cat` | function | `static/js/estorides.js:261` | `` |
| `check` | function | `static/js/estorides.js:3253` | `` |
| `cid` | function | `static/js/estorides.js:1199` | `` |
| `clearAll` | function | `static/js/estorides.js:705` | `` |
| `clearMap` | function | `static/js/estorides.js:336` | `` |
| `close` | function | `static/js/estorides.js:2621` | `` |
| `clusterColor` | function | `static/js/estorides.js:1177` | `` |
| `colorFor` | function | `static/js/estorides.js:1983` | `` |
| `colorForKind` | function | `static/js/estorides.js:2083` | `` |
| `confirmModal` | function | `static/js/estorides.js:2660` | `` |
| `debounce` | function | `static/js/estorides.js:2377` | `` |
| `deriveClusters` | function | `static/js/estorides.js:1196` | `` |
| `detectQueryTypeLocal` | function | `static/js/estorides.js:55` | `` |
| `doSearch` | function | `static/js/estorides.js:2906` | `` |
| `drawGraph` | function | `static/js/estorides.js:2201` | `` |
| `drawGraphWithExtras` | function | `static/js/estorides.js:1078` | `` |
| `drawHulls` | function | `static/js/estorides.js:1720` | `` |
| `entities` | function | `static/js/estorides.js:2258` | `` |
| `escapeAttr` | function | `static/js/estorides.js:1847` | `` |
| `escapeHTML` | function | `static/js/estorides.js:2427` | `` |
| `escapeHtml` | function | `static/js/estorides.js:3222` | `` |
| `expandNode` | function | `static/js/estorides.js:984` | `` |
| `filterTimeline` | function | `static/js/estorides.js:2152` | `` |
| `flush` | function | `static/js/estorides.js:909` | `` |
| `flush` | function | `static/js/estorides.js:1439` | `` |
| `flushDiscoverEntities` | function | `static/js/estorides.js:3234` | `` |
| `fmtTime` | function | `static/js/estorides.js:2141` | `` |
| `focusGraphNodeByValue` | function | `static/js/estorides.js:301` | `` |
| `focusNode` | function | `static/js/estorides.js:1398` | `` |
| `frac` | function | `static/js/estorides.js:2128` | `` |
| `handleDiscoverEvent` | function | `static/js/estorides.js:3155` | `` |
| `handleRunStreamEvent` | function | `static/js/estorides.js:616` | `` |
| `hideContextMenu` | function | `static/js/estorides.js:1253` | `` |
| `hideDiscoverProgress` | function | `static/js/estorides.js:3059` | `` |
| `hideTooltip` | function | `static/js/estorides.js:1209` | `` |
| `hideWorkingIndicator` | function | `static/js/estorides.js:1768` | `` |
| `is3DActive` | function | `static/js/estorides.js:1125` | `` |
| `k` | function | `static/js/estorides.js:1028` | `` |
| `k` | function | `static/js/estorides.js:1506` | `` |
| `labelFor` | function | `static/js/estorides.js:1261` | `` |
| `levelOf` | function | `static/js/estorides.js:1173` | `` |
| `loadAnalysisModels` | function | `static/js/estorides.js:787` | `` |
| `loadCases` | function | `static/js/estorides.js:2231` | `` |
| `loadFusionEntityDetail` | function | `static/js/estorides.js:2944` | `` |
| `loadFusionSearch` | function | `static/js/estorides.js:2899` | `` |
| `loadFusionStats` | function | `static/js/estorides.js:2851` | `` |
| `loadFusionTab` | function | `static/js/estorides.js:2845` | `` |
| `loadFusionTopChanged` | function | `static/js/estorides.js:2870` | `` |
| `loadSidebarCollapsed` | function | `static/js/estorides.js:2766` | `` |
| `loadSidebarWidth` | function | `static/js/estorides.js:2752` | `` |
| `makeModelPill` | function | `static/js/estorides.js:806` | `` |
| `maybePlotDiscoverEntity` | function | `static/js/estorides.js:3227` | `` |
| `mergeExpansionIntoGraph` | function | `static/js/estorides.js:1014` | `` |
| `obs` | function | `static/js/estorides.js:2095` | `` |
| `obs` | function | `static/js/estorides.js:2259` | `` |
| `on` | class | `static/js/estorides.js:1936` | `` |
| `openCaseDetail` | function | `static/js/estorides.js:2257` | `` |
| `openModal` | function | `static/js/estorides.js:2601` | `` |
| `out` | function | `static/js/estorides.js:246` | `` |
| `plotPoints` | function | `static/js/estorides.js:341` | `` |
| `pollToolInstall` | function | `static/js/estorides.js:220` | `` |
| `populateCategoryFilter` | function | `static/js/estorides.js:253` | `` |
| `promptModal` | function | `static/js/estorides.js:2636` | `` |
| `pump` | function | `static/js/estorides.js:930` | `` |
| `purifyHTML` | function | `static/js/estorides.js:1223` | `` |
| `pushLink` | function | `static/js/estorides.js:1102` | `` |
| `q` | function | `static/js/estorides.js:2232` | `` |
| `reanalyze` | function | `static/js/estorides.js:861` | `` |
| `removed` | function | `static/js/estorides.js:2507` | `` |
| `renderAnalysis` | function | `static/js/estorides.js:819` | `` |
| `renderAnalysisModels` | function | `static/js/estorides.js:794` | `` |
| `renderCaseDiffPanel` | function | `static/js/estorides.js:2496` | `` |
| `renderCaseItem` | function | `static/js/estorides.js:2351` | `` |
| `renderEntities` | function | `static/js/estorides.js:2002` | `` |
| `renderGraphCore` | function | `static/js/estorides.js:1632` | `` |
| `renderGraphSummary` | function | `static/js/estorides.js:2054` | `` |
| `renderMarkdownInto` | function | `static/js/estorides.js:834` | `` |
| `renderResult` | function | `static/js/estorides.js:739` | `` |
| `renderTieredResults` | function | `static/js/estorides.js:1781` | `` |
| `renderTimeline` | function | `static/js/estorides.js:2091` | `` |
| `replotStreamData` | function | `static/js/estorides.js:443` | `` |
| `requestToolInstall` | function | `static/js/estorides.js:197` | `` |
| `resolverTypeFor` | function | `static/js/estorides.js:1153` | `` |
| `restoreCaseToWorkspace` | function | `static/js/estorides.js:2312` | `` |
| `rows` | function | `static/js/estorides.js:2504` | `` |
| `runQuery` | function | `static/js/estorides.js:470` | `` |
| `runQueryBlocking` | function | `static/js/estorides.js:540` | `` |
| `runTransform` | function | `static/js/estorides.js:1412` | `` |
| `runTransformStream` | function | `static/js/estorides.js:1433` | `` |
| `safeColor` | function | `static/js/estorides.js:1187` | `` |
| `saveLevelOverrides` | function | `static/js/estorides.js:1169` | `` |
| `saveSidebarCollapsed` | function | `static/js/estorides.js:2774` | `` |
| `saveSidebarWidth` | function | `static/js/estorides.js:2763` | `` |
| `saved` | function | `static/js/estorides.js:2355` | `` |
| `scheduleRender` | function | `static/js/estorides.js:904` | `` |
| `searchEntity` | function | `static/js/estorides.js:573` | `` |
| `selectNode` | function | `static/js/estorides.js:1528` | `` |
| `set` | function | `static/js/estorides.js:32` | `` |
| `setDiscoverProgress` | function | `static/js/estorides.js:3047` | `` |
| `setNodeLevel` | function | `static/js/estorides.js:1381` | `` |
| `setRunProgress` | function | `static/js/estorides.js:86` | `` |
| `setSanitizedHTML` | function | `static/js/estorides.js:1234` | `` |
| `setStatus` | function | `static/js/estorides.js:733` | `` |
| `setStatus` | function | `static/js/estorides.js:3040` | `` |
| `setStatusDot` | function | `static/js/estorides.js:1757` | `` |
| `setThinkingVisible` | function | `static/js/estorides.js:849` | `` |
| `setVisible` | function | `static/js/estorides.js:12` | `` |
| `showBridgeTooltip` | function | `static/js/estorides.js:1258` | `` |
| `showContextMenu` | function | `static/js/estorides.js:1306` | `` |
| `showEmptyState` | function | `static/js/estorides.js:107` | `` |
| `showFriendlyError` | function | `static/js/estorides.js:288` | `` |
| `showNodeTooltip` | function | `static/js/estorides.js:1287` | `` |
| `showReportModal` | function | `static/js/estorides.js:2573` | `` |
| `showToast` | function | `static/js/estorides.js:66` | `` |
| `showTooltipAt` | function | `static/js/estorides.js:1243` | `` |
| `showWorkingIndicator` | function | `static/js/estorides.js:1763` | `` |
| `sig` | function | `static/js/estorides.js:678` | `` |
| `sig` | function | `static/js/estorides.js:3199` | `` |
| `startDiscover` | function | `static/js/estorides.js:3064` | `` |
| `status` | function | `static/js/estorides.js:148` | `` |
| `status` | function | `static/js/estorides.js:262` | `` |
| `stopDiscover` | function | `static/js/estorides.js:3138` | `` |
| `stopRunStream` | function | `static/js/estorides.js:455` | `` |
| `summariseObservation` | function | `static/js/estorides.js:113` | `` |
| `switchCanvasTab` | function | `static/js/estorides.js:314` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:310` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:2832` | `` |
| `tag` | function | `static/js/estorides.js:2722` | `` |
| `text` | function | `static/js/estorides.js:260` | `` |
| `to` | class | `static/js/estorides.js:401` | `` |
| `toggleThinking` | function | `static/js/estorides.js:856` | `` |
| `toggleTierSection` | function | `static/js/estorides.js:1773` | `` |
| `toolBinary` | function | `static/js/estorides.js:142` | `` |
| `tr` | function | `static/js/estorides.js:1356` | `` |
| `tr` | function | `static/js/estorides.js:1596` | `` |
| `truncate` | function | `static/js/estorides.js:2432` | `` |
| `undoGraph` | function | `static/js/estorides.js:1493` | `` |
| `updateQueryChip` | function | `static/js/estorides.js:76` | `` |
| `validCoord` | function | `static/js/estorides.js:1979` | `` |
| `add` | function | `static/js/graph_bundle.js:411` | `` |
| `aimAt` | function | `static/js/graph_bundle.js:661` | `` |
| `bspline` | function | `static/js/graph_bundle.js:99` | `` |
| `buildCurves` | function | `static/js/graph_bundle.js:137` | `` |
| `center` | function | `static/js/graph_bundle.js:164` | `` |
| `clip` | function | `static/js/graph_bundle.js:66` | `` |
| `colorOf` | function | `static/js/graph_bundle.js:88` | `` |
| `curve` | function | `static/js/graph_bundle.js:120` | `` |
| `depthAlpha` | function | `static/js/graph_bundle.js:175` | `` |
| `djb2KindColor` | function | `static/js/graph_bundle.js:32` | `` |
| `draw` | function | `static/js/graph_bundle.js:231` | `` |
| `drawGroups` | function | `static/js/graph_bundle.js:291` | `` |
| `drawHud` | function | `static/js/graph_bundle.js:405` | `` |
| `drawLabels` | function | `static/js/graph_bundle.js:367` | `` |
| `drawNodes` | function | `static/js/graph_bundle.js:343` | `` |
| `edgeState` | function | `static/js/graph_bundle.js:185` | `` |
| `facing` | function | `static/js/graph_bundle.js:655` | `` |
| `flowsOf` | function | `static/js/graph_bundle.js:483` | `` |
| `focusGroup` | function | `static/js/graph_bundle.js:650` | `` |
| `focusNode` | function | `static/js/graph_bundle.js:645` | `` |
| `focusState` | function | `static/js/graph_bundle.js:177` | `` |
| `frame` | function | `static/js/graph_bundle.js:786` | `` |
| `g` | function | `static/js/graph_bundle.js:229` | `` |
| `groupButton` | function | `static/js/graph_bundle.js:512` | `` |
| `hitGroup` | function | `static/js/graph_bundle.js:443` | `` |
| `hitNode` | function | `static/js/graph_bundle.js:420` | `` |
| `ingest` | function | `static/js/graph_bundle.js:726` | `` |
| `init` | function | `static/js/graph_bundle.js:812` | `` |
| `ink` | function | `static/js/graph_bundle.js:74` | `` |
| `inspectInGraph` | function | `static/js/graph_bundle.js:497` | `` |
| `keyOf` | function | `static/js/graph_bundle.js:94` | `` |
| `labelSet` | function | `static/js/graph_bundle.js:355` | `` |
| `listInto` | function | `static/js/graph_bundle.js:519` | `` |
| `makeProjector` | function | `static/js/graph_bundle.js:165` | `` |
| `mid` | function | `static/js/graph_bundle.js:306` | `` |
| `mk` | function | `static/js/graph_bundle.js:60` | `` |
| `nodeButton` | function | `static/js/graph_bundle.js:504` | `` |
| `nodeLit` | function | `static/js/graph_bundle.js:205` | `` |
| `nodeRadius` | function | `static/js/graph_bundle.js:333` | `` |
| `pointOn` | function | `static/js/graph_bundle.js:226` | `` |
| `radius` | function | `static/js/graph_bundle.js:160` | `` |
| `rank` | function | `static/js/graph_bundle.js:492` | `` |
| `readHash` | function | `static/js/graph_bundle.js:709` | `` |
| `refresh` | function | `static/js/graph_bundle.js:762` | `` |
| `renderLegend` | function | `static/js/graph_bundle.js:613` | `` |
| `renderPanel` | function | `static/js/graph_bundle.js:529` | `` |
| `resize` | function | `static/js/graph_bundle.js:148` | `` |
| `screenNodes` | function | `static/js/graph_bundle.js:337` | `` |
| `search` | function | `static/js/graph_bundle.js:913` | `` |
| `setBeta` | function | `static/js/graph_bundle.js:679` | `` |
| `setColor` | function | `static/js/graph_bundle.js:671` | `` |
| `setDir` | function | `static/js/graph_bundle.js:675` | `` |
| `setView` | function | `static/js/graph_bundle.js:667` | `` |
| `strokeCurve` | function | `static/js/graph_bundle.js:216` | `` |
| `sync` | function | `static/js/graph_bundle.js:687` | `` |
| `t0` | function | `static/js/graph_bundle.js:275` | `` |
| `tabActive` | function | `static/js/graph_bundle.js:70` | `` |
| `tag` | function | `static/js/graph_bundle.js:958` | `` |
| `tipFor` | function | `static/js/graph_bundle.js:461` | `` |
| `tt` | function | `static/js/graph_bundle.js:279` | `` |
| `v` | function | `static/js/graph_bundle.js:78` | `` |
| `writeHash` | function | `static/js/graph_bundle.js:697` | `` |
| `a` | function | `static/js/graph_force.js:327` | `` |
| `adaptLocal` | function | `static/js/graph_force.js:79` | `` |
| `applyFilters` | function | `static/js/graph_force.js:1241` | `` |
| `applyLayout3D` | function | `static/js/graph_force.js:961` | `` |
| `bindStagePointer` | function | `static/js/graph_force.js:887` | `` |
| `cid` | function | `static/js/graph_force.js:104` | `` |
| `clearSelection` | function | `static/js/graph_force.js:1112` | `` |
| `clusterForce` | function | `static/js/graph_force.js:335` | `` |
| `col` | function | `static/js/graph_force.js:788` | `` |
| `collideForce` | function | `static/js/graph_force.js:377` | `` |
| `colorOf` | function | `static/js/graph_force.js:219` | `` |
| `computeHighlight` | function | `static/js/graph_force.js:275` | `` |
| `convexHullPts` | function | `static/js/graph_force.js:561` | `` |
| `copyDeepLink` | function | `static/js/graph_force.js:1020` | `` |
| `cross` | function | `static/js/graph_force.js:564` | `` |
| `currentRaw` | function | `static/js/graph_force.js:137` | `` |
| `dimmed` | function | `static/js/graph_force.js:220` | `` |
| `done` | function | `static/js/graph_force.js:1022` | `` |
| `drawGlyph3D` | function | `static/js/graph_force.js:651` | `` |
| `drawLabel3D` | function | `static/js/graph_force.js:703` | `` |
| `edges` | function | `static/js/graph_force.js:1256` | `` |
| `entities` | function | `static/js/graph_force.js:205` | `` |
| `esc` | function | `static/js/graph_force.js:25` | `` |
| `expandSelected` | function | `static/js/graph_force.js:999` | `` |
| `fail` | function | `static/js/graph_force.js:65` | `` |
| `fam` | function | `static/js/graph_force.js:105` | `` |
| `famAnchor` | function | `static/js/graph_force.js:320` | `` |
| `famOf` | function | `static/js/graph_force.js:330` | `` |
| `fn` | function | `static/js/graph_force.js:1267` | `` |
| `focusFamily` | function | `static/js/graph_force.js:1125` | `` |
| `focusSelected` | function | `static/js/graph_force.js:1009` | `` |
| `force` | function | `static/js/graph_force.js:337` | `` |
| `force` | function | `static/js/graph_force.js:362` | `` |
| `force` | function | `static/js/graph_force.js:379` | `` |
| `glyphPath` | function | `static/js/graph_force.js:619` | `` |
| `hiddenKind` | function | `static/js/graph_force.js:221` | `` |
| `hitEdge3D` | function | `static/js/graph_force.js:861` | `` |
| `hitNode3D` | function | `static/js/graph_force.js:845` | `` |
| `hoverAt3D` | function | `static/js/graph_force.js:876` | `` |

Next: [SYMBOLS_p4.md](SYMBOLS_p4.md)
