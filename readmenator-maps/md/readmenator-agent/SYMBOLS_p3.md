# Symbols (page 3 of 7)
Previous: [SYMBOLS_p2.md](SYMBOLS_p2.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `parse_whatweb_text` | function | `estorides_core/system_app_sources.py:312` | `def parse_whatweb_text(payload)` |
| `parser` | function | `estorides_core/system_app_sources.py:165` | `def parser(payload)` |
| `render_args` | function | `estorides_core/system_app_sources.py:96` | `def render_args(args, query, outdir)` |
| `repl` | function | `estorides_core/system_app_sources.py:109` | `def repl(m)` |
| `to_dict` | method | `estorides_core/system_app_sources.py:76` | `def to_dict(self)` |
| `tool_available` | function | `estorides_core/system_app_sources.py:91` | `def tool_available(binary)` |
| `Tech` | class | `estorides_core/tech_fingerprint.py:89` | `class Tech` |
| `TechFingerprintResult` | class | `estorides_core/tech_fingerprint.py:102` | `class TechFingerprintResult` |
| `_add` | function | `estorides_core/tech_fingerprint.py:129` | `def _add(name, category, version, source, confidence)` |
| `fingerprint` | function | `estorides_core/tech_fingerprint.py:115` | `def fingerprint(headers, html, cookies, status)` |
| `to_dict` | method | `estorides_core/tech_fingerprint.py:97` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/tech_fingerprint.py:107` | `def to_dict(self)` |
| `InstallRecipe` | class | `estorides_core/tool_install.py:81` | `class InstallRecipe` |
| `InstallResult` | class | `estorides_core/tool_install.py:103` | `class InstallResult` |
| `ToolStatus` | class | `estorides_core/tool_install.py:278` | `class ToolStatus` |
| `_check_shell_command` | function | `estorides_core/tool_install.py:148` | `def _check_shell_command(command)` |
| `_elevate` | function | `estorides_core/tool_install.py:117` | `def _elevate(cmd)` |
| `_install_apt` | function | `estorides_core/tool_install.py:358` | `def _install_apt(recipe)` |
| `_install_git` | function | `estorides_core/tool_install.py:375` | `def _install_git(recipe)` |
| `_needs_elevation` | function | `estorides_core/tool_install.py:154` | `def _needs_elevation(command)` |
| `_recipe_path` | function | `estorides_core/tool_install.py:193` | `def _recipe_path(name)` |
| `_recipe_table` | function | `estorides_core/tool_install.py:179` | `def _recipe_table()` |
| `_run` | function | `estorides_core/tool_install.py:132` | `def _run(cmd)` |
| `_system_app_binaries` | function | `estorides_core/tool_install.py:297` | `def _system_app_binaries(sources_dir)` |
| `_tools_root` | function | `estorides_core/tool_install.py:371` | `def _tools_root()` |
| `_verify` | function | `estorides_core/tool_install.py:506` | `def _verify(binary)` |
| `doctor` | function | `estorides_core/tool_install.py:321` | `def doctor(sources_dir)` |
| `has_apt` | method | `estorides_core/tool_install.py:95` | `def has_apt(self)` |
| `has_git` | method | `estorides_core/tool_install.py:98` | `def has_git(self)` |
| `install_tool` | function | `estorides_core/tool_install.py:414` | `def install_tool(tool_name)` |
| `is_valid_binary` | function | `estorides_core/tool_install.py:174` | `def is_valid_binary(name)` |
| `is_valid_recipe_name` | function | `estorides_core/tool_install.py:169` | `def is_valid_recipe_name(name)` |
| `list_recipes` | function | `estorides_core/tool_install.py:270` | `def list_recipes()` |
| `load_recipe` | function | `estorides_core/tool_install.py:210` | `def load_recipe(name)` |
| `main` | function | `estorides_core/tool_install.py:516` | `def main(argv)` |
| `recipe_available` | function | `estorides_core/tool_install.py:254` | `def recipe_available(name)` |
| `to_dict` | method | `estorides_core/tool_install.py:113` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/tool_install.py:287` | `def to_dict(self)` |
| `tool_available` | function | `estorides_core/tool_install.py:259` | `def tool_available(binary)` |
| `ToolError` | class | `estorides_core/tool_runner.py:17` | `class ToolError(Exception)` |
| `ToolErrorResult` | class | `estorides_core/tool_runner.py:86` | `class ToolErrorResult` |
| `ToolInjectionError` | class | `estorides_core/tool_runner.py:25` | `class ToolInjectionError(ToolError)` |
| `ToolNotAllowedError` | class | `estorides_core/tool_runner.py:21` | `class ToolNotAllowedError(ToolError)` |
| `ToolNotFoundError` | class | `estorides_core/tool_runner.py:29` | `class ToolNotFoundError(ToolError)` |
| `ToolResult` | class | `estorides_core/tool_runner.py:38` | `class ToolResult` |
| `ToolTimeoutError` | class | `estorides_core/tool_runner.py:33` | `class ToolTimeoutError(ToolError)` |
| `_check_allowlist` | function | `estorides_core/tool_runner.py:114` | `def _check_allowlist(tool_name)` |
| `_check_injection` | function | `estorides_core/tool_runner.py:97` | `def _check_injection(args)` |
| `_parse_entities_generic` | function | `estorides_core/tool_runner.py:121` | `def _parse_entities_generic(stdout, tool_name)` |
| `_resolve_binary` | function | `estorides_core/tool_runner.py:107` | `def _resolve_binary(tool_name)` |
| `from_failure` | method | `estorides_core/tool_runner.py:59` | `def from_failure(cls, tool_name, error_code, error_message, duration_s, exit_code, stdout, stderr, parsed_entities)` |
| `run_tool` | function | `estorides_core/tool_runner.py:156` | `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)` |
| `to_dict` | method | `estorides_core/tool_runner.py:51` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/tool_runner.py:93` | `def to_dict(self)` |
| `Transform` | class | `estorides_core/transforms.py:71` | `class Transform` |
| `TransformRegistry` | class | `estorides_core/transforms.py:225` | `class TransformRegistry` |
| `_T` | function | `estorides_core/transforms.py:441` | `def _T(id, label, tier, applies, runner, description, output_types, cost)` |
| `__init__` | method | `estorides_core/transforms.py:228` | `def __init__(self)` |
| `_empty` | function | `estorides_core/transforms.py:96` | `def _empty(root_type, value)` |
| `_filter_runner` | function | `estorides_core/transforms.py:121` | `def _filter_runner(relations)` |
| `_norm` | function | `estorides_core/transforms.py:130` | `def _norm(s)` |
| `_osiris` | function | `estorides_core/transforms.py:135` | `def _osiris()` |
| `_resolver_filtered` | function | `estorides_core/transforms.py:100` | `def _resolver_filtered(ent_type, value, relations)` |
| `_run_bgp` | function | `estorides_core/transforms.py:143` | `def _run_bgp(ent_type, value)` |
| `_run_github` | function | `estorides_core/transforms.py:194` | `def _run_github(ent_type, value)` |
| `_run_leaks` | function | `estorides_core/transforms.py:169` | `def _run_leaks(ent_type, value)` |
| `_static_runner` | function | `estorides_core/transforms.py:332` | `def _static_runner(nodes_tpl, links_tpl)` |
| `_str_list` | function | `estorides_core/transforms.py:322` | `def _str_list(raw)` |
| `_transform_from_yaml` | function | `estorides_core/transforms.py:362` | `def _transform_from_yaml(raw, origin)` |
| `for_type` | method | `estorides_core/transforms.py:234` | `def for_type(self, ent_type)` |
| `iter_sse_events` | function | `estorides_core/transforms.py:406` | `def iter_sse_events(transform_id, ent_type, value, runner)` |
| `load_yaml_dir` | method | `estorides_core/transforms.py:280` | `def load_yaml_dir(self, directory)` |
| `register` | method | `estorides_core/transforms.py:231` | `def register(self, t)` |
| `run` | function | `estorides_core/transforms.py:122` | `def run(ent_type, value)` |
| `run` | method | `estorides_core/transforms.py:246` | `def run(self, transform_id, ent_type, value)` |
| `run` | function | `estorides_core/transforms.py:335` | `def run(ent_type, value)` |
| `sub` | function | `estorides_core/transforms.py:338` | `def sub(s, depth)` |
| `summary` | method | `estorides_core/transforms.py:83` | `def summary(self)` |
| `_strip_diacritics` | function | `estorides_core/transliteration.py:76` | `def _strip_diacritics(text)` |
| `consonant_skeleton` | function | `estorides_core/transliteration.py:112` | `def consonant_skeleton(text)` |
| `is_non_latin` | function | `estorides_core/transliteration.py:139` | `def is_non_latin(text)` |
| `to_latin` | function | `estorides_core/transliteration.py:87` | `def to_latin(text)` |
| `Query` | class | `estorides_core/validation.py:63` | `class Query` |
| `QueryValidationError` | class | `estorides_core/validation.py:55` | `class QueryValidationError(ValueError)` |
| `__init__` | method | `estorides_core/validation.py:57` | `def __init__(self, reason, message)` |
| `__str__` | method | `estorides_core/validation.py:69` | `def __str__(self)` |
| `_strip_and_collapse` | function | `estorides_core/validation.py:73` | `def _strip_and_collapse(text)` |
| `validate_query` | function | `estorides_core/validation.py:85` | `def validate_query(raw)` |
| `DefaultCred` | class | `estorides_core/vuln_correlation.py:14` | `class DefaultCred` |
| `VulnCorrelationResult` | class | `estorides_core/vuln_correlation.py:43` | `class VulnCorrelationResult` |
| `VulnEntry` | class | `estorides_core/vuln_correlation.py:24` | `class VulnEntry` |
| `_parsed_version` | function | `estorides_core/vuln_correlation.py:141` | `def _parsed_version(version)` |
| `_version_in_range` | function | `estorides_core/vuln_correlation.py:153` | `def _version_in_range(version, v_start, v_end)` |
| `compute_attack_readiness` | function | `estorides_core/vuln_correlation.py:228` | `def compute_attack_readiness(vulnerabilities)` |
| `correlate_technologies` | function | `estorides_core/vuln_correlation.py:202` | `def correlate_technologies(technologies)` |
| `lookup_cve_for_tech` | function | `estorides_core/vuln_correlation.py:169` | `def lookup_cve_for_tech(tech_name, version)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:19` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:38` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/vuln_correlation.py:52` | `def to_dict(self)` |
| `AuthGate` | class | `estorides_core/web_security.py:341` | `class AuthGate` |
| `WebSecurityConfig` | class | `estorides_core/web_security.py:87` | `class WebSecurityConfig` |
| `_cors_preflight` | function | `estorides_core/web_security.py:250` | `def _cors_preflight()` |
| `_current_gate` | function | `estorides_core/web_security.py:440` | `def _current_gate()` |
| `_env_str` | function | `estorides_core/web_security.py:137` | `def _env_str(name, default)` |
| `_extract_bearer_token` | function | `estorides_core/web_security.py:286` | `def _extract_bearer_token()` |
| `_redirect_to_https` | function | `estorides_core/web_security.py:203` | `def _redirect_to_https()` |
| `_security_headers` | function | `estorides_core/web_security.py:217` | `def _security_headers(resp)` |
| `auth_meta_for_index` | method | `estorides_core/web_security.py:362` | `def auth_meta_for_index(self)` |
| `auto_generated_token` | function | `estorides_core/web_security.py:444` | `def auto_generated_token()` |
| `build_https_url` | function | `estorides_core/web_security.py:58` | `def build_https_url(public_host, path, query_string)` |
| `check` | method | `estorides_core/web_security.py:354` | `def check(self)` |
| `enabled` | method | `estorides_core/web_security.py:351` | `def enabled(self)` |
| `install_auth_gate` | function | `estorides_core/web_security.py:421` | `def install_auth_gate(app, gate)` |
| `install_security` | function | `estorides_core/web_security.py:169` | `def install_security(app, cfg)` |
| `is_cors_enabled` | method | `estorides_core/web_security.py:128` | `def is_cors_enabled(self)` |
| `is_origin_allowed` | method | `estorides_core/web_security.py:132` | `def is_origin_allowed(self)` |
| `issue_session_cookie_kwargs` | method | `estorides_core/web_security.py:371` | `def issue_session_cookie_kwargs(self)` |
| `load_security_config` | function | `estorides_core/web_security.py:144` | `def load_security_config()` |
| `make_auth_gate` | function | `estorides_core/web_security.py:321` | `def make_auth_gate()` |
| `require_auth` | function | `estorides_core/web_security.py:388` | `def require_auth(view)` |
| `wrapper` | function | `estorides_core/web_security.py:402` | `def wrapper()` |
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
| `build_executive_summary` | function | `estorides_export/recon_report.py:92` | `def build_executive_summary(critical_findings, total_targets, domain, classification)` |
| `build_subdomain_tree` | function | `estorides_export/recon_report.py:67` | `def build_subdomain_tree(subdomains)` |
| `generate_report` | function | `estorides_export/recon_report.py:115` | `def generate_report(query, target_scoring, metadata)` |
| `redact_sensitive` | function | `estorides_export/recon_report.py:61` | `def redact_sensitive(text)` |
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
| `deco` | function | `estorides_llm/manager.py:105` | `def deco(backend_or_cls)` |
| `generate` | method | `estorides_llm/manager.py:373` | `def generate(self, prompt)` |
| `get_ollama_status` | method | `estorides_llm/manager.py:414` | `def get_ollama_status(self)` |
| `get_status` | method | `estorides_llm/manager.py:124` | `def get_status()` |
| `register` | function | `estorides_llm/manager.py:97` | `def register(name)` |
| `stream` | method | `estorides_llm/manager.py:422` | `def stream(self, prompt)` |
| `stream_generate` | method | `estorides_llm/manager.py:80` | `def stream_generate(self, prompt, context, model, temperature, request_timeout)` |
| `stream_generate` | method | `estorides_llm/manager.py:188` | `def stream_generate(self, prompt, context, model, temperature, request_timeout)` |
| `_RunStreamJob` | class | `estorides_web.py:149` | `class _RunStreamJob` |
| `__init__` | method | `estorides_web.py:157` | `def __init__(self, job_id, query, query_type, case_id)` |
| `_arg_int` | function | `estorides_web.py:119` | `def _arg_int(name, default)` |
| `_client_ip` | function | `estorides_web.py:102` | `def _client_ip()` |
| `_drive` | function | `estorides_web.py:1632` | `def _drive()` |
| `_err` | function | `estorides_web.py:1351` | `def _err()` |
| `_gen` | function | `estorides_web.py:1356` | `def _gen()` |
| `_graph_rag_block` | function | `estorides_web.py:236` | `def _graph_rag_block(query, budget_tokens)` |
| `_new_stream_job_id` | function | `estorides_web.py:187` | `def _new_stream_job_id()` |
| `_provides` | function | `estorides_web.py:83` | `def _provides(service, message)` |
| `_rate_limit_decorator` | function | `estorides_web.py:192` | `def _rate_limit_decorator()` |
| `_run` | function | `estorides_web.py:1741` | `def _run()` |
| `_send_and_cleanup` | function | `estorides_web.py:135` | `def _send_and_cleanup(p, tmpdir)` |
| `_serve_loop` | function | `estorides_web.py:1792` | `def _serve_loop()` |
| `_shape_for_ui` | function | `estorides_web.py:1805` | `def _shape_for_ui(result)` |
| `_sse_response` | function | `estorides_web.py:78` | `def _sse_response(gen)` |
| `_watch_runner` | function | `estorides_web.py:1137` | `def _watch_runner(swatch)` |
| `admin_sources` | function | `estorides_web.py:974` | `def admin_sources()` |
| `api_alerts_channels` | function | `estorides_web.py:1262` | `def api_alerts_channels()` |
| `api_alerts_test` | function | `estorides_web.py:1270` | `def api_alerts_test()` |
| `api_analyze_stream` | function | `estorides_web.py:1728` | `def api_analyze_stream()` |
| `api_cases_delete` | function | `estorides_web.py:713` | `def api_cases_delete(case_id)` |
| `api_cases_diff` | function | `estorides_web.py:744` | `def api_cases_diff()` |
| `api_cases_get` | function | `estorides_web.py:699` | `def api_cases_get(case_id)` |
| `api_cases_list` | function | `estorides_web.py:686` | `def api_cases_list()` |
| `api_cases_save` | function | `estorides_web.py:721` | `def api_cases_save(case_id)` |
| `api_discover_jobs` | function | `estorides_web.py:1529` | `def api_discover_jobs()` |
| `api_discover_start` | function | `estorides_web.py:1476` | `def api_discover_start()` |
| `api_discover_stop` | function | `estorides_web.py:1535` | `def api_discover_stop()` |
| `api_discover_stream` | function | `estorides_web.py:1547` | `def api_discover_stream()` |
| `api_export` | function | `estorides_web.py:608` | `def api_export(fmt)` |
| `api_feeds` | function | `estorides_web.py:577` | `def api_feeds()` |
| `api_fusion_analytics_consensus` | function | `estorides_web.py:954` | `def api_fusion_analytics_consensus(eid)` |
| `api_fusion_analytics_corroboration_matrix` | function | `estorides_web.py:1074` | `def api_fusion_analytics_corroboration_matrix()` |
| `api_fusion_analytics_entity_summary` | function | `estorides_web.py:934` | `def api_fusion_analytics_entity_summary(eid)` |
| `api_fusion_analytics_entity_timeline` | function | `estorides_web.py:924` | `def api_fusion_analytics_entity_timeline(eid)` |
| `api_fusion_analytics_source_stats` | function | `estorides_web.py:944` | `def api_fusion_analytics_source_stats(source_name)` |
| `api_fusion_analytics_top_changed` | function | `estorides_web.py:964` | `def api_fusion_analytics_top_changed()` |
| `api_fusion_entities` | function | `estorides_web.py:885` | `def api_fusion_entities()` |
| `api_fusion_entity` | function | `estorides_web.py:906` | `def api_fusion_entity(eid)` |
| `api_fusion_sources` | function | `estorides_web.py:876` | `def api_fusion_sources()` |
| `api_fusion_stats` | function | `estorides_web.py:868` | `def api_fusion_stats()` |
| `api_graph` | function | `estorides_web.py:474` | `def api_graph()` |
| `api_intel_graph` | function | `estorides_web.py:808` | `def api_intel_graph()` |
| `api_intel_resolve` | function | `estorides_web.py:769` | `def api_intel_resolve()` |
| `api_intel_stats` | function | `estorides_web.py:847` | `def api_intel_stats()` |
| `api_lan_scan` | function | `estorides_web.py:436` | `def api_lan_scan()` |
| `api_lan_scope` | function | `estorides_web.py:428` | `def api_lan_scope()` |
| `api_ollama_status` | function | `estorides_web.py:358` | `def api_ollama_status()` |
| `api_osiris_bgp` | function | `estorides_web.py:1379` | `def api_osiris_bgp()` |
| `api_osiris_github` | function | `estorides_web.py:1421` | `def api_osiris_github()` |
| `api_osiris_kev` | function | `estorides_web.py:1449` | `def api_osiris_kev()` |
| `api_osiris_leaks` | function | `estorides_web.py:1435` | `def api_osiris_leaks()` |
| `api_osiris_mac` | function | `estorides_web.py:1393` | `def api_osiris_mac()` |
| `api_osiris_malware` | function | `estorides_web.py:1458` | `def api_osiris_malware()` |
| `api_osiris_phone` | function | `estorides_web.py:1407` | `def api_osiris_phone()` |
| `api_osiris_threats` | function | `estorides_web.py:1463` | `def api_osiris_threats()` |
| `api_run` | function | `estorides_web.py:364` | `def api_run()` |
| `api_run_stream` | function | `estorides_web.py:1681` | `def api_run_stream()` |
| `api_run_stream_start` | function | `estorides_web.py:1597` | `def api_run_stream_start()` |
| `api_run_stream_stop` | function | `estorides_web.py:1669` | `def api_run_stream_stop()` |
| `api_scheduler_status` | function | `estorides_web.py:1286` | `def api_scheduler_status()` |
| `api_socmint_discover` | function | `estorides_web.py:1118` | `def api_socmint_discover()` |
| `api_socmint_platforms` | function | `estorides_web.py:1110` | `def api_socmint_platforms()` |
| `api_socmint_resolve` | function | `estorides_web.py:1088` | `def api_socmint_resolve()` |
| `api_sources_yaml_create` | function | `estorides_web.py:1017` | `def api_sources_yaml_create()` |
| `api_sources_yaml_delete` | function | `estorides_web.py:1057` | `def api_sources_yaml_delete(name)` |
| `api_sources_yaml_list` | function | `estorides_web.py:991` | `def api_sources_yaml_list()` |
| `api_sources_yaml_update` | function | `estorides_web.py:1038` | `def api_sources_yaml_update(name)` |
| `api_status` | function | `estorides_web.py:352` | `def api_status()` |
| `api_transform_run` | function | `estorides_web.py:1318` | `def api_transform_run()` |
| `api_transform_stream` | function | `estorides_web.py:1340` | `def api_transform_stream()` |
| `api_transforms` | function | `estorides_web.py:1304` | `def api_transforms()` |
| `api_watch_create` | function | `estorides_web.py:1170` | `def api_watch_create()` |
| `api_watch_delete` | function | `estorides_web.py:1216` | `def api_watch_delete(watch_id)` |
| `api_watch_disable` | function | `estorides_web.py:1240` | `def api_watch_disable(watch_id)` |
| `api_watch_enable` | function | `estorides_web.py:1227` | `def api_watch_enable(watch_id)` |
| `api_watch_get` | function | `estorides_web.py:1204` | `def api_watch_get(watch_id)` |
| `api_watch_history` | function | `estorides_web.py:1252` | `def api_watch_history(watch_id)` |
| `api_watch_list` | function | `estorides_web.py:1161` | `def api_watch_list()` |
| `create_app` | function | `estorides_web.py:258` | `def create_app()` |
| `deco` | function | `estorides_web.py:90` | `def deco(view)` |
| `deco` | function | `estorides_web.py:199` | `def deco(view)` |
| `done` | method | `estorides_web.py:177` | `def done(self)` |
| `gen` | function | `estorides_web.py:1560` | `def gen()` |
| `gen` | function | `estorides_web.py:1687` | `def gen()` |
| `gen` | function | `estorides_web.py:1763` | `def gen()` |
| `healthz` | function | `estorides_web.py:294` | `def healthz()` |
| `index` | function | `estorides_web.py:331` | `def index()` |
| `metrics` | function | `estorides_web.py:319` | `def metrics()` |
| `openapi_doc` | function | `estorides_web.py:326` | `def openapi_doc()` |
| `readyz` | function | `estorides_web.py:305` | `def readyz()` |
| `should_stop` | method | `estorides_web.py:169` | `def should_stop(self)` |
| `status` | method | `estorides_web.py:173` | `def status(self)` |
| `stop` | method | `estorides_web.py:166` | `def stop(self)` |
| `wrapper` | function | `estorides_web.py:92` | `def wrapper()` |
| `wrapper` | function | `estorides_web.py:201` | `def wrapper()` |
| `_worker` | function | `estorides_web_tools.py:91` | `def _worker()` |
| `api_tool_install` | function | `estorides_web_tools.py:75` | `def api_tool_install(name)` |
| `api_tool_install_status` | function | `estorides_web_tools.py:120` | `def api_tool_install_status(name)` |
| `api_tools_doctor` | function | `estorides_web_tools.py:68` | `def api_tools_doctor()` |
| `api_tools_list` | function | `estorides_web_tools.py:49` | `def api_tools_list()` |
| `install_full` | function | `install.sh:51` | `` |
| `install_minimal` | function | `install.sh:55` | `` |
| `CLUSTER_PALETTE` | function | `static/js/estorides.js:1388` | `` |
| `TELEMETRY` | function | `static/js/estorides.js:114` | `` |
| `_installErrMsg` | function | `static/js/estorides.js:316` | `` |
| `_redrawGraph` | function | `static/js/estorides.js:1993` | `` |
| `_sanitizeInput` | function | `static/js/estorides.js:2840` | `` |
| `_sseAuthToken` | function | `static/js/estorides.js:3254` | `` |
| `_sseUrl` | function | `static/js/estorides.js:3259` | `` |
| `actions` | function | `static/js/estorides.js:2849` | `` |
| `add` | function | `static/js/estorides.js:1781` | `` |
| `addDiscoverEntityToTab` | function | `static/js/estorides.js:3447` | `` |
| `addText` | function | `static/js/estorides.js:1787` | `` |
| `analyseEntity` | function | `static/js/estorides.js:1193` | `` |
| `appendStreamEntity` | function | `static/js/estorides.js:918` | `` |
| `appendStreamObservation` | function | `static/js/estorides.js:896` | `` |
| `applyLevelStyles` | function | `static/js/estorides.js:1632` | `` |
| `applyResultFilters` | function | `static/js/estorides.js:332` | `` |
| `attribute` | class | `static/js/estorides.js:3194` | `` |
| `barH` | function | `static/js/estorides.js:1644` | `` |
| `barH` | function | `static/js/estorides.js:1893` | `` |
| `bindResultFilters` | function | `static/js/estorides.js:353` | `` |
| `boxQ` | function | `static/js/estorides.js:1122` | `` |
| `buildCaseMapCoords` | function | `static/js/estorides.js:2575` | `` |
| `buildMapCoords` | function | `static/js/estorides.js:2125` | `` |
| `buildResultCard` | function | `static/js/estorides.js:211` | `` |
| `c` | function | `static/js/estorides.js:1421` | `` |
| `c` | function | `static/js/estorides.js:1504` | `` |
| `caseActionDiff` | function | `static/js/estorides.js:2718` | `` |
| `caseActionReport` | function | `static/js/estorides.js:2779` | `` |
| `caseActionSave` | function | `static/js/estorides.js:2697` | `` |
| `cat` | function | `static/js/estorides.js:334` | `` |
| `check` | function | `static/js/estorides.js:3505` | `` |
| `cid` | function | `static/js/estorides.js:1441` | `` |
| `clearAll` | function | `static/js/estorides.js:947` | `` |
| `clearMap` | function | `static/js/estorides.js:409` | `` |
| `close` | function | `static/js/estorides.js:2863` | `` |
| `clusterColor` | function | `static/js/estorides.js:1419` | `` |
| `colorFor` | function | `static/js/estorides.js:2225` | `` |
| `colorForKind` | function | `static/js/estorides.js:2325` | `` |
| `confirmModal` | function | `static/js/estorides.js:2902` | `` |
| `debounce` | function | `static/js/estorides.js:2619` | `` |
| `deriveClusters` | function | `static/js/estorides.js:1438` | `` |
| `detectQueryTypeLocal` | function | `static/js/estorides.js:128` | `` |
| `doSearch` | function | `static/js/estorides.js:3148` | `` |
| `done` | function | `static/js/estorides.js:70` | `` |
| `drawGraph` | function | `static/js/estorides.js:2443` | `` |
| `drawGraphWithExtras` | function | `static/js/estorides.js:1320` | `` |
| `drawHulls` | function | `static/js/estorides.js:1962` | `` |
| `ensureLanConsent` | function | `static/js/estorides.js:46` | `` |
| `entities` | function | `static/js/estorides.js:2500` | `` |
| `escapeAttr` | function | `static/js/estorides.js:2089` | `` |
| `escapeHTML` | function | `static/js/estorides.js:2669` | `` |
| `escapeHtml` | function | `static/js/estorides.js:3475` | `` |
| `expandNode` | function | `static/js/estorides.js:1226` | `` |
| `fetch` | method | `static/js/estorides.js:3326` | `` |
| `filterTimeline` | function | `static/js/estorides.js:2394` | `` |
| `flush` | function | `static/js/estorides.js:1151` | `` |
| `flush` | function | `static/js/estorides.js:1681` | `` |
| `flushDiscoverEntities` | function | `static/js/estorides.js:3487` | `` |
| `fmtTime` | function | `static/js/estorides.js:2383` | `` |
| `focusGraphNodeByValue` | function | `static/js/estorides.js:374` | `` |
| `focusNode` | function | `static/js/estorides.js:1640` | `` |
| `frac` | function | `static/js/estorides.js:2370` | `` |
| `handleDiscoverEvent` | function | `static/js/estorides.js:3408` | `` |
| `handleRunStreamEvent` | function | `static/js/estorides.js:858` | `` |
| `hideContextMenu` | function | `static/js/estorides.js:1495` | `` |
| `hideDiscoverProgress` | function | `static/js/estorides.js:3302` | `` |
| `hideTooltip` | function | `static/js/estorides.js:1451` | `` |
| `hideWorkingIndicator` | function | `static/js/estorides.js:2010` | `` |
| `is3DActive` | function | `static/js/estorides.js:1367` | `` |
| `isLanQueryLocal` | function | `static/js/estorides.js:24` | `` |
| `k` | function | `static/js/estorides.js:1270` | `` |
| `k` | function | `static/js/estorides.js:1748` | `` |
| `labelFor` | function | `static/js/estorides.js:1503` | `` |
| `lanRunFields` | function | `static/js/estorides.js:33` | `` |
| `levelOf` | function | `static/js/estorides.js:1415` | `` |
| `loadAnalysisModels` | function | `static/js/estorides.js:1029` | `` |
| `loadCases` | function | `static/js/estorides.js:2473` | `` |
| `loadFusionEntityDetail` | function | `static/js/estorides.js:3186` | `` |
| `loadFusionSearch` | function | `static/js/estorides.js:3141` | `` |
| `loadFusionStats` | function | `static/js/estorides.js:3093` | `` |
| `loadFusionTab` | function | `static/js/estorides.js:3087` | `` |
| `loadFusionTopChanged` | function | `static/js/estorides.js:3112` | `` |
| `loadSidebarCollapsed` | function | `static/js/estorides.js:3008` | `` |
| `loadSidebarWidth` | function | `static/js/estorides.js:2994` | `` |
| `makeModelPill` | function | `static/js/estorides.js:1048` | `` |
| `maybePlotDiscoverEntity` | function | `static/js/estorides.js:3480` | `` |
| `mergeExpansionIntoGraph` | function | `static/js/estorides.js:1256` | `` |
| `msg` | function | `static/js/estorides.js:662` | `` |
| `obs` | function | `static/js/estorides.js:2337` | `` |
| `obs` | function | `static/js/estorides.js:2501` | `` |
| `on` | class | `static/js/estorides.js:2178` | `` |
| `onNo` | function | `static/js/estorides.js:78` | `` |
| `onYes` | function | `static/js/estorides.js:77` | `` |
| `openCaseDetail` | function | `static/js/estorides.js:2499` | `` |
| `openModal` | function | `static/js/estorides.js:2843` | `` |
| `out` | function | `static/js/estorides.js:319` | `` |
| `plotPoints` | function | `static/js/estorides.js:414` | `` |
| `pollToolInstall` | function | `static/js/estorides.js:293` | `` |
| `populateCategoryFilter` | function | `static/js/estorides.js:326` | `` |
| `promptModal` | function | `static/js/estorides.js:2878` | `` |
| `pump` | function | `static/js/estorides.js:1172` | `` |
| `purifyHTML` | function | `static/js/estorides.js:1465` | `` |
| `pushLink` | function | `static/js/estorides.js:1344` | `` |
| `q` | function | `static/js/estorides.js:2474` | `` |
| `reanalyze` | function | `static/js/estorides.js:1103` | `` |
| `removed` | function | `static/js/estorides.js:2749` | `` |
| `renderAnalysis` | function | `static/js/estorides.js:1061` | `` |
| `renderAnalysisModels` | function | `static/js/estorides.js:1036` | `` |
| `renderCaseDiffPanel` | function | `static/js/estorides.js:2738` | `` |
| `renderCaseItem` | function | `static/js/estorides.js:2593` | `` |
| `renderEntities` | function | `static/js/estorides.js:2244` | `` |
| `renderGraphCore` | function | `static/js/estorides.js:1874` | `` |
| `renderGraphSummary` | function | `static/js/estorides.js:2296` | `` |
| `renderLanResults` | function | `static/js/estorides.js:551` | `` |
| `renderMarkdownInto` | function | `static/js/estorides.js:1076` | `` |
| `renderResult` | function | `static/js/estorides.js:981` | `` |
| `renderTieredResults` | function | `static/js/estorides.js:2023` | `` |
| `renderTimeline` | function | `static/js/estorides.js:2333` | `` |
| `replotStreamData` | function | `static/js/estorides.js:518` | `` |
| `requestToolInstall` | function | `static/js/estorides.js:270` | `` |
| `resolverTypeFor` | function | `static/js/estorides.js:1395` | `` |
| `restoreCaseToWorkspace` | function | `static/js/estorides.js:2554` | `` |
| `rows` | function | `static/js/estorides.js:2746` | `` |
| `runQuery` | function | `static/js/estorides.js:685` | `` |
| `runQueryBlocking` | function | `static/js/estorides.js:773` | `` |
| `runTransform` | function | `static/js/estorides.js:1654` | `` |
| `runTransformStream` | function | `static/js/estorides.js:1675` | `` |
| `safe` | function | `static/js/estorides.js:60` | `` |
| `safeColor` | function | `static/js/estorides.js:1429` | `` |
| `saveLevelOverrides` | function | `static/js/estorides.js:1411` | `` |
| `saveSidebarCollapsed` | function | `static/js/estorides.js:3016` | `` |
| `saveSidebarWidth` | function | `static/js/estorides.js:3005` | `` |
| `saved` | function | `static/js/estorides.js:2597` | `` |
| `scheduleRender` | function | `static/js/estorides.js:1146` | `` |
| `scope` | function | `static/js/estorides.js:621` | `` |
| `searchEntity` | function | `static/js/estorides.js:807` | `` |
| `selectNode` | function | `static/js/estorides.js:1770` | `` |
| `set` | function | `static/js/estorides.js:105` | `` |
| `setDiscoverProgress` | function | `static/js/estorides.js:3290` | `` |
| `setNodeLevel` | function | `static/js/estorides.js:1623` | `` |
| `setRunProgress` | function | `static/js/estorides.js:159` | `` |
| `setSanitizedHTML` | function | `static/js/estorides.js:1476` | `` |
| `setStatus` | function | `static/js/estorides.js:975` | `` |
| `setStatus` | function | `static/js/estorides.js:3283` | `` |
| `setStatusDot` | function | `static/js/estorides.js:1999` | `` |
| `setThinkingVisible` | function | `static/js/estorides.js:1091` | `` |
| `setTimeout` | method | `static/js/estorides.js:2942` | `` |
| `setVisible` | function | `static/js/estorides.js:12` | `` |
| `showBridgeTooltip` | function | `static/js/estorides.js:1500` | `` |
| `showContextMenu` | function | `static/js/estorides.js:1548` | `` |
| `showEmptyState` | function | `static/js/estorides.js:180` | `` |
| `showFriendlyError` | function | `static/js/estorides.js:361` | `` |
| `showNodeTooltip` | function | `static/js/estorides.js:1529` | `` |
| `showReportModal` | function | `static/js/estorides.js:2815` | `` |
| `showToast` | function | `static/js/estorides.js:139` | `` |
| `showTooltipAt` | function | `static/js/estorides.js:1485` | `` |
| `showWorkingIndicator` | function | `static/js/estorides.js:2005` | `` |
| `sig` | function | `static/js/estorides.js:920` | `` |
| `sig` | function | `static/js/estorides.js:3451` | `` |
| `startDiscover` | function | `static/js/estorides.js:3307` | `` |
| `startLanScan` | function | `static/js/estorides.js:620` | `` |
| `status` | function | `static/js/estorides.js:221` | `` |
| `status` | function | `static/js/estorides.js:335` | `` |
| `stopDiscover` | function | `static/js/estorides.js:3391` | `` |
| `stopRunStream` | function | `static/js/estorides.js:530` | `` |
| `summariseObservation` | function | `static/js/estorides.js:186` | `` |
| `switchCanvasTab` | function | `static/js/estorides.js:387` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:383` | `` |
| `switchSidebarTab` | function | `static/js/estorides.js:3074` | `` |
| `t` | function | `static/js/estorides.js:25` | `` |
| `tag` | function | `static/js/estorides.js:2964` | `` |
| `text` | function | `static/js/estorides.js:333` | `` |
| `to` | class | `static/js/estorides.js:474` | `` |
| `toggleThinking` | function | `static/js/estorides.js:1098` | `` |
| `toggleTierSection` | function | `static/js/estorides.js:2015` | `` |
| `toolBinary` | function | `static/js/estorides.js:215` | `` |
| `tr` | function | `static/js/estorides.js:1598` | `` |
| `tr` | function | `static/js/estorides.js:1838` | `` |
| `truncate` | function | `static/js/estorides.js:2674` | `` |
| `undoGraph` | function | `static/js/estorides.js:1735` | `` |
| `updateQueryChip` | function | `static/js/estorides.js:149` | `` |
| `validCoord` | function | `static/js/estorides.js:2221` | `` |
| `add` | function | `static/js/graph_bundle.js:411` | `` |
| `add` | method | `static/js/graph_bundle.js:415` | `` |
| `aimAt` | function | `static/js/graph_bundle.js:662` | `` |
| `bspline` | function | `static/js/graph_bundle.js:100` | `` |
| `buildCurves` | function | `static/js/graph_bundle.js:138` | `` |
| `center` | function | `static/js/graph_bundle.js:165` | `` |
| `clip` | function | `static/js/graph_bundle.js:67` | `` |
| `colorOf` | function | `static/js/graph_bundle.js:89` | `` |
| `curve` | function | `static/js/graph_bundle.js:121` | `` |
| `depthAlpha` | function | `static/js/graph_bundle.js:176` | `` |
| `djb2KindColor` | function | `static/js/graph_bundle.js:33` | `` |
| `draw` | function | `static/js/graph_bundle.js:232` | `` |
| `drawGroups` | function | `static/js/graph_bundle.js:292` | `` |
| `drawHud` | function | `static/js/graph_bundle.js:406` | `` |
| `drawLabels` | function | `static/js/graph_bundle.js:368` | `` |
| `drawNodes` | function | `static/js/graph_bundle.js:344` | `` |
| `edgeState` | function | `static/js/graph_bundle.js:186` | `` |
| `facing` | function | `static/js/graph_bundle.js:656` | `` |
| `flowsOf` | function | `static/js/graph_bundle.js:484` | `` |
| `focusGroup` | function | `static/js/graph_bundle.js:651` | `` |
| `focusNode` | function | `static/js/graph_bundle.js:646` | `` |
| `focusState` | function | `static/js/graph_bundle.js:178` | `` |
| `frame` | function | `static/js/graph_bundle.js:787` | `` |
| `g` | function | `static/js/graph_bundle.js:229` | `` |
| `groupButton` | function | `static/js/graph_bundle.js:513` | `` |
| `hitGroup` | function | `static/js/graph_bundle.js:444` | `` |
| `hitNode` | function | `static/js/graph_bundle.js:421` | `` |
| `ingest` | function | `static/js/graph_bundle.js:727` | `` |
| `init` | function | `static/js/graph_bundle.js:813` | `` |
| `ink` | function | `static/js/graph_bundle.js:75` | `` |
| `inspectInGraph` | function | `static/js/graph_bundle.js:498` | `` |
| `keyOf` | function | `static/js/graph_bundle.js:95` | `` |
| `labelSet` | function | `static/js/graph_bundle.js:356` | `` |
| `listInto` | function | `static/js/graph_bundle.js:520` | `` |
| `listInto` | method | `static/js/graph_bundle.js:559` | `` |

Next: [SYMBOLS_p4.md](SYMBOLS_p4.md)
