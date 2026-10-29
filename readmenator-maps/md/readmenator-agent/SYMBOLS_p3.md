# Symbols (page 3 of 8)
Previous: [SYMBOLS_p2.md](SYMBOLS_p2.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `to_dict` | method | `estorides_core/socmint.py:92` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/socmint.py:119` | `def to_dict(self)` |
| `DashboardSummary` | class | `estorides_core/source_health_monitoring.py:160` | `class DashboardSummary` |
| `HealthDashboard` | class | `estorides_core/source_health_monitoring.py:173` | `class HealthDashboard` |
| `SourceHealthConfig` | class | `estorides_core/source_health_monitoring.py:42` | `class SourceHealthConfig` |
| `SourceHealthInput` | class | `estorides_core/source_health_monitoring.py:98` | `class SourceHealthInput` |
| `SourceHealthResult` | class | `estorides_core/source_health_monitoring.py:134` | `class SourceHealthResult` |
| `SourceHealthStatus` | class | `estorides_core/source_health_monitoring.py:31` | `class SourceHealthStatus(str, Enum)` |
| `__post_init__` | method | `estorides_core/source_health_monitoring.py:58` | `def __post_init__(self)` |
| `__post_init__` | method | `estorides_core/source_health_monitoring.py:112` | `def __post_init__(self)` |
| `_clamp01` | function | `estorides_core/source_health_monitoring.py:202` | `def _clamp01(value)` |
| `_classify` | function | `estorides_core/source_health_monitoring.py:210` | `def _classify(success_rate, avg_latency_ms, freshness_hours, fetch_count, config)` |
| `build_dashboard` | function | `estorides_core/source_health_monitoring.py:295` | `def build_dashboard(records, config)` |
| `compute_health` | function | `estorides_core/source_health_monitoring.py:235` | `def compute_health(inp, config)` |
| `to_dict` | method | `estorides_core/source_health_monitoring.py:146` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/source_health_monitoring.py:184` | `def to_dict(self)` |
| `Source` | class | `estorides_core/source_loader.py:22` | `class Source(dict)` |
| `SourceRegistry` | class | `estorides_core/source_loader.py:38` | `class SourceRegistry` |
| `__getattr__` | method | `estorides_core/source_loader.py:31` | `def __getattr__(self, key)` |
| `__init__` | method | `estorides_core/source_loader.py:28` | `def __init__(self, data)` |
| `__init__` | method | `estorides_core/source_loader.py:41` | `def __init__(self, sources_dir)` |
| `_category_dir_name` | method | `estorides_core/source_loader.py:237` | `def _category_dir_name(self, category)` |
| `_find_source_file` | method | `estorides_core/source_loader.py:259` | `def _find_source_file(self, name)` |
| `_load_file` | method | `estorides_core/source_loader.py:71` | `def _load_file(self, path)` |
| `_normalise` | method | `estorides_core/source_loader.py:111` | `def _normalise(self, raw)` |
| `_source_path` | method | `estorides_core/source_loader.py:253` | `def _source_path(self, name, category)` |
| `all` | method | `estorides_core/source_loader.py:203` | `def all(self)` |
| `by_category` | method | `estorides_core/source_loader.py:206` | `def by_category(self, category)` |
| `categories` | method | `estorides_core/source_loader.py:209` | `def categories(self)` |
| `delete_source_file` | method | `estorides_core/source_loader.py:342` | `def delete_source_file(self, name)` |
| `filter` | method | `estorides_core/source_loader.py:215` | `def filter(self)` |
| `get` | method | `estorides_core/source_loader.py:200` | `def get(self, name)` |
| `load` | method | `estorides_core/source_loader.py:47` | `def load(self)` |
| `names` | method | `estorides_core/source_loader.py:212` | `def names(self)` |
| `summary` | method | `estorides_core/source_loader.py:351` | `def summary(self)` |
| `write_source_file` | method | `estorides_core/source_loader.py:272` | `def write_source_file(self, data)` |
| `DictMixin` | class | `estorides_core/sqlite_store.py:109` | `class DictMixin` |
| `SqliteStore` | class | `estorides_core/sqlite_store.py:34` | `class SqliteStore` |
| `__del__` | method | `estorides_core/sqlite_store.py:89` | `def __del__(self)` |
| `__init__` | method | `estorides_core/sqlite_store.py:50` | `def __init__(self, path)` |
| `_init_schema` | method | `estorides_core/sqlite_store.py:66` | `def _init_schema(self)` |
| `_tx` | method | `estorides_core/sqlite_store.py:72` | `def _tx(self)` |
| `close` | method | `estorides_core/sqlite_store.py:82` | `def close(self)` |
| `to_dict` | method | `estorides_core/sqlite_store.py:112` | `def to_dict(self)` |
| `GuardResult` | class | `estorides_core/ssrf_guard.py:99` | `class GuardResult` |
| `SSRFError` | class | `estorides_core/ssrf_guard.py:269` | `class SSRFError(ValueError)` |
| `__bool__` | method | `estorides_core/ssrf_guard.py:105` | `def __bool__(self)` |
| `_is_blocked_v4` | function | `estorides_core/ssrf_guard.py:110` | `def _is_blocked_v4(ip)` |
| `_is_blocked_v6` | function | `estorides_core/ssrf_guard.py:114` | `def _is_blocked_v6(addr)` |
| `_is_host_in_blocked_literal` | function | `estorides_core/ssrf_guard.py:134` | `def _is_host_in_blocked_literal(host)` |
| `_load_allowlist` | function | `estorides_core/ssrf_guard.py:189` | `def _load_allowlist()` |
| `_matches_allowlist` | function | `estorides_core/ssrf_guard.py:172` | `def _matches_allowlist(host, allowlist)` |
| `_normalise_host` | function | `estorides_core/ssrf_guard.py:126` | `def _normalise_host(host)` |
| `_resolve` | function | `estorides_core/ssrf_guard.py:155` | `def _resolve(host)` |
| `assert_safe` | function | `estorides_core/ssrf_guard.py:262` | `def assert_safe(url)` |
| `check_url` | function | `estorides_core/ssrf_guard.py:194` | `def check_url(url)` |
| `Relationship` | class | `estorides_core/supply_chain.py:78` | `class Relationship` |
| `SharedInfra` | class | `estorides_core/supply_chain.py:66` | `class SharedInfra` |
| `SupplyChainResult` | class | `estorides_core/supply_chain.py:89` | `class SupplyChainResult` |
| `ThirdParty` | class | `estorides_core/supply_chain.py:54` | `class ThirdParty` |
| `analyse_third_parties` | function | `estorides_core/supply_chain.py:129` | `def analyse_third_parties(third_parties, subsidiaries)` |
| `detect_cdn` | function | `estorides_core/supply_chain.py:122` | `def detect_cdn(cname)` |
| `detect_mx_provider` | function | `estorides_core/supply_chain.py:106` | `def detect_mx_provider(mx_records)` |
| `detect_ns_provider` | function | `estorides_core/supply_chain.py:114` | `def detect_ns_provider(ns_records)` |
| `detect_shared_infrastructure` | function | `estorides_core/supply_chain.py:140` | `def detect_shared_infrastructure(asn)` |
| `to_dict` | method | `estorides_core/supply_chain.py:61` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/supply_chain.py:73` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/supply_chain.py:84` | `def to_dict(self)` |
| `to_dict` | method | `estorides_core/supply_chain.py:96` | `def to_dict(self)` |
| `SystemAppResult` | class | `estorides_core/system_app_sources.py:57` | `class SystemAppResult` |
| `_line_filter_parser` | function | `estorides_core/system_app_sources.py:150` | `def _line_filter_parser()` |
| `_loads_lenient` | function | `estorides_core/system_app_sources.py:131` | `def _loads_lenient(text)` |
| `_read_capped` | function | `estorides_core/system_app_sources.py:121` | `def _read_capped(path, cap)` |
| `execute` | function | `estorides_core/system_app_sources.py:396` | `def execute(source, query)` |
| `fail` | function | `estorides_core/system_app_sources.py:418` | `def fail(code, message)` |
| `is_system_app` | function | `estorides_core/system_app_sources.py:81` | `def is_system_app(source)` |
| `parse_amass_json` | function | `estorides_core/system_app_sources.py:193` | `def parse_amass_json(payload)` |
| `parse_dmitry_text` | function | `estorides_core/system_app_sources.py:297` | `def parse_dmitry_text(payload)` |
| `parse_dnsenum_text` | function | `estorides_core/system_app_sources.py:285` | `def parse_dnsenum_text(payload)` |
| `parse_dnsrecon_text` | function | `estorides_core/system_app_sources.py:280` | `def parse_dnsrecon_text(payload)` |
| `parse_fierce_text` | function | `estorides_core/system_app_sources.py:292` | `def parse_fierce_text(payload)` |
| `parse_holehe_text` | function | `estorides_core/system_app_sources.py:265` | `def parse_holehe_text(payload)` |
| `parse_maigret_json` | function | `estorides_core/system_app_sources.py:225` | `def parse_maigret_json(payload)` |
| `parse_mailfy_text` | function | `estorides_core/system_app_sources.py:327` | `def parse_mailfy_text(payload)` |
| `parse_metagoofil_text` | function | `estorides_core/system_app_sources.py:307` | `def parse_metagoofil_text(payload)` |
| `parse_phonefy_text` | function | `estorides_core/system_app_sources.py:332` | `def parse_phonefy_text(payload)` |
| `parse_phoneinfoga_json` | function | `estorides_core/system_app_sources.py:247` | `def parse_phoneinfoga_json(payload)` |
| `parse_searchfy_text` | function | `estorides_core/system_app_sources.py:337` | `def parse_searchfy_text(payload)` |
| `parse_sherlock_text` | function | `estorides_core/system_app_sources.py:260` | `def parse_sherlock_text(payload)` |
| `parse_sublist3r_lines` | function | `estorides_core/system_app_sources.py:275` | `def parse_sublist3r_lines(payload)` |
| `parse_theharvester_text` | function | `estorides_core/system_app_sources.py:317` | `def parse_theharvester_text(payload)` |
| `parse_tool_output` | function | `estorides_core/system_app_sources.py:365` | `def parse_tool_output(source_name, parser_name, data)` |
| `parse_urlcrazy_text` | function | `estorides_core/system_app_sources.py:302` | `def parse_urlcrazy_text(payload)` |
| `parse_usufy_text` | function | `estorides_core/system_app_sources.py:322` | `def parse_usufy_text(payload)` |
| `parse_wafw00f_text` | function | `estorides_core/system_app_sources.py:270` | `def parse_wafw00f_text(payload)` |
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
| `Transform` | class | `estorides_core/transforms.py:73` | `class Transform` |
| `TransformRegistry` | class | `estorides_core/transforms.py:227` | `class TransformRegistry` |
| `_T` | function | `estorides_core/transforms.py:443` | `def _T(id, label, tier, applies, runner, description, output_types, cost)` |
| `__init__` | method | `estorides_core/transforms.py:230` | `def __init__(self)` |
| `_empty` | function | `estorides_core/transforms.py:98` | `def _empty(root_type, value)` |
| `_filter_runner` | function | `estorides_core/transforms.py:123` | `def _filter_runner(relations)` |
| `_norm` | function | `estorides_core/transforms.py:132` | `def _norm(s)` |
| `_osiris` | function | `estorides_core/transforms.py:137` | `def _osiris()` |
| `_resolver_filtered` | function | `estorides_core/transforms.py:102` | `def _resolver_filtered(ent_type, value, relations)` |
| `_run_bgp` | function | `estorides_core/transforms.py:145` | `def _run_bgp(ent_type, value)` |
| `_run_github` | function | `estorides_core/transforms.py:196` | `def _run_github(ent_type, value)` |
| `_run_leaks` | function | `estorides_core/transforms.py:171` | `def _run_leaks(ent_type, value)` |
| `_static_runner` | function | `estorides_core/transforms.py:334` | `def _static_runner(nodes_tpl, links_tpl)` |
| `_str_list` | function | `estorides_core/transforms.py:324` | `def _str_list(raw)` |
| `_transform_from_yaml` | function | `estorides_core/transforms.py:364` | `def _transform_from_yaml(raw, origin)` |
| `for_type` | method | `estorides_core/transforms.py:236` | `def for_type(self, ent_type)` |
| `iter_sse_events` | function | `estorides_core/transforms.py:408` | `def iter_sse_events(transform_id, ent_type, value, runner)` |
| `load_yaml_dir` | method | `estorides_core/transforms.py:282` | `def load_yaml_dir(self, directory)` |
| `register` | method | `estorides_core/transforms.py:233` | `def register(self, t)` |
| `run` | function | `estorides_core/transforms.py:124` | `def run(ent_type, value)` |
| `run` | method | `estorides_core/transforms.py:248` | `def run(self, transform_id, ent_type, value)` |
| `run` | function | `estorides_core/transforms.py:337` | `def run(ent_type, value)` |
| `sub` | function | `estorides_core/transforms.py:340` | `def sub(s, depth)` |
| `summary` | method | `estorides_core/transforms.py:85` | `def summary(self)` |
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
| `_drive` | function | `estorides_web.py:1645` | `def _drive()` |
| `_err` | function | `estorides_web.py:1364` | `def _err()` |
| `_gen` | function | `estorides_web.py:1369` | `def _gen()` |
| `_graph_rag_block` | function | `estorides_web.py:236` | `def _graph_rag_block(query, budget_tokens)` |
| `_new_stream_job_id` | function | `estorides_web.py:187` | `def _new_stream_job_id()` |
| `_provides` | function | `estorides_web.py:83` | `def _provides(service, message)` |
| `_rate_limit_decorator` | function | `estorides_web.py:192` | `def _rate_limit_decorator()` |
| `_run` | function | `estorides_web.py:1754` | `def _run()` |
| `_send_and_cleanup` | function | `estorides_web.py:135` | `def _send_and_cleanup(p, tmpdir)` |
| `_serve_loop` | function | `estorides_web.py:1805` | `def _serve_loop()` |
| `_shape_for_ui` | function | `estorides_web.py:1818` | `def _shape_for_ui(result)` |
| `_sse_response` | function | `estorides_web.py:78` | `def _sse_response(gen)` |
| `_watch_runner` | function | `estorides_web.py:1150` | `def _watch_runner(swatch)` |
| `admin_sources` | function | `estorides_web.py:987` | `def admin_sources()` |
| `api_alerts_channels` | function | `estorides_web.py:1275` | `def api_alerts_channels()` |
| `api_alerts_test` | function | `estorides_web.py:1283` | `def api_alerts_test()` |
| `api_analyze_stream` | function | `estorides_web.py:1741` | `def api_analyze_stream()` |
| `api_cases_delete` | function | `estorides_web.py:726` | `def api_cases_delete(case_id)` |
| `api_cases_diff` | function | `estorides_web.py:757` | `def api_cases_diff()` |
| `api_cases_get` | function | `estorides_web.py:712` | `def api_cases_get(case_id)` |
| `api_cases_list` | function | `estorides_web.py:699` | `def api_cases_list()` |
| `api_cases_save` | function | `estorides_web.py:734` | `def api_cases_save(case_id)` |
| `api_discover_jobs` | function | `estorides_web.py:1542` | `def api_discover_jobs()` |
| `api_discover_start` | function | `estorides_web.py:1489` | `def api_discover_start()` |
| `api_discover_stop` | function | `estorides_web.py:1548` | `def api_discover_stop()` |
| `api_discover_stream` | function | `estorides_web.py:1560` | `def api_discover_stream()` |
| `api_export` | function | `estorides_web.py:621` | `def api_export(fmt)` |
| `api_feeds` | function | `estorides_web.py:577` | `def api_feeds()` |
| `api_fusion_analytics_consensus` | function | `estorides_web.py:967` | `def api_fusion_analytics_consensus(eid)` |
| `api_fusion_analytics_corroboration_matrix` | function | `estorides_web.py:1087` | `def api_fusion_analytics_corroboration_matrix()` |
| `api_fusion_analytics_entity_summary` | function | `estorides_web.py:947` | `def api_fusion_analytics_entity_summary(eid)` |
| `api_fusion_analytics_entity_timeline` | function | `estorides_web.py:937` | `def api_fusion_analytics_entity_timeline(eid)` |
| `api_fusion_analytics_source_stats` | function | `estorides_web.py:957` | `def api_fusion_analytics_source_stats(source_name)` |
| `api_fusion_analytics_top_changed` | function | `estorides_web.py:977` | `def api_fusion_analytics_top_changed()` |
| `api_fusion_entities` | function | `estorides_web.py:898` | `def api_fusion_entities()` |
| `api_fusion_entity` | function | `estorides_web.py:919` | `def api_fusion_entity(eid)` |
| `api_fusion_sources` | function | `estorides_web.py:889` | `def api_fusion_sources()` |
| `api_fusion_stats` | function | `estorides_web.py:881` | `def api_fusion_stats()` |
| `api_graph` | function | `estorides_web.py:474` | `def api_graph()` |
| `api_intel_graph` | function | `estorides_web.py:821` | `def api_intel_graph()` |
| `api_intel_resolve` | function | `estorides_web.py:782` | `def api_intel_resolve()` |
| `api_intel_stats` | function | `estorides_web.py:860` | `def api_intel_stats()` |
| `api_lan_scan` | function | `estorides_web.py:436` | `def api_lan_scan()` |
| `api_lan_scope` | function | `estorides_web.py:428` | `def api_lan_scope()` |
| `api_ollama_status` | function | `estorides_web.py:358` | `def api_ollama_status()` |
| `api_osiris_bgp` | function | `estorides_web.py:1392` | `def api_osiris_bgp()` |
| `api_osiris_github` | function | `estorides_web.py:1434` | `def api_osiris_github()` |
| `api_osiris_kev` | function | `estorides_web.py:1462` | `def api_osiris_kev()` |
| `api_osiris_leaks` | function | `estorides_web.py:1448` | `def api_osiris_leaks()` |
| `api_osiris_mac` | function | `estorides_web.py:1406` | `def api_osiris_mac()` |
| `api_osiris_malware` | function | `estorides_web.py:1471` | `def api_osiris_malware()` |
| `api_osiris_phone` | function | `estorides_web.py:1420` | `def api_osiris_phone()` |
| `api_osiris_threats` | function | `estorides_web.py:1476` | `def api_osiris_threats()` |
| `api_run` | function | `estorides_web.py:364` | `def api_run()` |
| `api_run_stream` | function | `estorides_web.py:1694` | `def api_run_stream()` |
| `api_run_stream_start` | function | `estorides_web.py:1610` | `def api_run_stream_start()` |
| `api_run_stream_stop` | function | `estorides_web.py:1682` | `def api_run_stream_stop()` |
| `api_scheduler_status` | function | `estorides_web.py:1299` | `def api_scheduler_status()` |
| `api_socmint_discover` | function | `estorides_web.py:1131` | `def api_socmint_discover()` |
| `api_socmint_platforms` | function | `estorides_web.py:1123` | `def api_socmint_platforms()` |
| `api_socmint_resolve` | function | `estorides_web.py:1101` | `def api_socmint_resolve()` |
| `api_sources_yaml_create` | function | `estorides_web.py:1030` | `def api_sources_yaml_create()` |
| `api_sources_yaml_delete` | function | `estorides_web.py:1070` | `def api_sources_yaml_delete(name)` |
| `api_sources_yaml_list` | function | `estorides_web.py:1004` | `def api_sources_yaml_list()` |
| `api_sources_yaml_update` | function | `estorides_web.py:1051` | `def api_sources_yaml_update(name)` |
| `api_status` | function | `estorides_web.py:352` | `def api_status()` |
| `api_transform_run` | function | `estorides_web.py:1331` | `def api_transform_run()` |
| `api_transform_stream` | function | `estorides_web.py:1353` | `def api_transform_stream()` |
| `api_transforms` | function | `estorides_web.py:1317` | `def api_transforms()` |
| `api_watch_create` | function | `estorides_web.py:1183` | `def api_watch_create()` |
| `api_watch_delete` | function | `estorides_web.py:1229` | `def api_watch_delete(watch_id)` |
| `api_watch_disable` | function | `estorides_web.py:1253` | `def api_watch_disable(watch_id)` |
| `api_watch_enable` | function | `estorides_web.py:1240` | `def api_watch_enable(watch_id)` |
| `api_watch_get` | function | `estorides_web.py:1217` | `def api_watch_get(watch_id)` |
| `api_watch_history` | function | `estorides_web.py:1265` | `def api_watch_history(watch_id)` |
| `api_watch_list` | function | `estorides_web.py:1174` | `def api_watch_list()` |
| `create_app` | function | `estorides_web.py:258` | `def create_app()` |
| `deco` | function | `estorides_web.py:90` | `def deco(view)` |
| `deco` | function | `estorides_web.py:199` | `def deco(view)` |
| `done` | method | `estorides_web.py:177` | `def done(self)` |
| `gen` | function | `estorides_web.py:1573` | `def gen()` |
| `gen` | function | `estorides_web.py:1700` | `def gen()` |
| `gen` | function | `estorides_web.py:1776` | `def gen()` |
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
| `CLUSTER_PALETTE` | function | `static/js/estorides.js:1604` | `` |
| `TELEMETRY` | function | `static/js/estorides.js:114` | `` |
| `_installErrMsg` | function | `static/js/estorides.js:316` | `` |
| `_redrawGraph` | function | `static/js/estorides.js:2209` | `` |
| `_sanitizeInput` | function | `static/js/estorides.js:3056` | `` |
| `_sseAuthToken` | function | `static/js/estorides.js:3470` | `` |
| `_sseUrl` | function | `static/js/estorides.js:3475` | `` |
| `actions` | function | `static/js/estorides.js:3065` | `` |
| `add` | function | `static/js/estorides.js:1997` | `` |
| `addDiscoverEntityToTab` | function | `static/js/estorides.js:3663` | `` |
| `addText` | function | `static/js/estorides.js:2003` | `` |
| `aeroBboxParam` | function | `static/js/estorides.js:508` | `` |
| `aeroEnabledSet` | function | `static/js/estorides.js:476` | `` |
| `aeroPersist` | function | `static/js/estorides.js:488` | `` |
| `aeroPopup` | function | `static/js/estorides.js:525` | `` |
| `aeroRenderLayer` | function | `static/js/estorides.js:579` | `` |
| `aeroStatus` | function | `static/js/estorides.js:496` | `` |
| `analyseEntity` | function | `static/js/estorides.js:1409` | `` |
| `appendStreamEntity` | function | `static/js/estorides.js:1134` | `` |
| `appendStreamObservation` | function | `static/js/estorides.js:1112` | `` |
| `applyLevelStyles` | function | `static/js/estorides.js:1848` | `` |
| `applyResultFilters` | function | `static/js/estorides.js:332` | `` |
| `attribute` | class | `static/js/estorides.js:3410` | `` |
| `barH` | function | `static/js/estorides.js:1860` | `` |
| `barH` | function | `static/js/estorides.js:2109` | `` |
| `bindResultFilters` | function | `static/js/estorides.js:353` | `` |
| `boxQ` | function | `static/js/estorides.js:1338` | `` |
| `buildCaseMapCoords` | function | `static/js/estorides.js:2791` | `` |
| `buildMapCoords` | function | `static/js/estorides.js:2341` | `` |
| `buildResultCard` | function | `static/js/estorides.js:211` | `` |
| `c` | function | `static/js/estorides.js:1637` | `` |
| `c` | function | `static/js/estorides.js:1720` | `` |
| `caseActionDiff` | function | `static/js/estorides.js:2934` | `` |
| `caseActionReport` | function | `static/js/estorides.js:2995` | `` |
| `caseActionSave` | function | `static/js/estorides.js:2913` | `` |
| `cat` | function | `static/js/estorides.js:334` | `` |
| `check` | function | `static/js/estorides.js:3721` | `` |
| `cid` | function | `static/js/estorides.js:1657` | `` |
| `clearAll` | function | `static/js/estorides.js:1163` | `` |
| `clearMap` | function | `static/js/estorides.js:409` | `` |
| `close` | function | `static/js/estorides.js:3079` | `` |
| `clusterColor` | function | `static/js/estorides.js:1635` | `` |
| `colorFor` | function | `static/js/estorides.js:2441` | `` |
| `colorForKind` | function | `static/js/estorides.js:2541` | `` |
| `confirmModal` | function | `static/js/estorides.js:3118` | `` |
| `debounce` | function | `static/js/estorides.js:2835` | `` |
| `deriveClusters` | function | `static/js/estorides.js:1654` | `` |
| `detectQueryTypeLocal` | function | `static/js/estorides.js:128` | `` |
| `doSearch` | function | `static/js/estorides.js:3364` | `` |
| `done` | function | `static/js/estorides.js:70` | `` |
| `drawGraph` | function | `static/js/estorides.js:2659` | `` |
| `drawGraphWithExtras` | function | `static/js/estorides.js:1536` | `` |
| `drawHulls` | function | `static/js/estorides.js:2178` | `` |
| `ensureLanConsent` | function | `static/js/estorides.js:46` | `` |
| `entities` | function | `static/js/estorides.js:2716` | `` |
| `escapeAttr` | function | `static/js/estorides.js:2305` | `` |
| `escapeHTML` | function | `static/js/estorides.js:2885` | `` |
| `escapeHtml` | function | `static/js/estorides.js:3691` | `` |
| `expandNode` | function | `static/js/estorides.js:1442` | `` |
| `fetch` | method | `static/js/estorides.js:3542` | `` |
| `filterTimeline` | function | `static/js/estorides.js:2610` | `` |
| `flush` | function | `static/js/estorides.js:1367` | `` |
| `flush` | function | `static/js/estorides.js:1897` | `` |
| `flushDiscoverEntities` | function | `static/js/estorides.js:3703` | `` |
| `fmtTime` | function | `static/js/estorides.js:2599` | `` |
| `focusGraphNodeByValue` | function | `static/js/estorides.js:374` | `` |
| `focusNode` | function | `static/js/estorides.js:1856` | `` |
| `frac` | function | `static/js/estorides.js:2586` | `` |
| `handleDiscoverEvent` | function | `static/js/estorides.js:3624` | `` |
| `handleRunStreamEvent` | function | `static/js/estorides.js:1074` | `` |
| `hideContextMenu` | function | `static/js/estorides.js:1711` | `` |
| `hideDiscoverProgress` | function | `static/js/estorides.js:3518` | `` |
| `hideTooltip` | function | `static/js/estorides.js:1667` | `` |
| `hideWorkingIndicator` | function | `static/js/estorides.js:2226` | `` |
| `initAerospaceLayers` | function | `static/js/estorides.js:635` | `` |
| `is3DActive` | function | `static/js/estorides.js:1583` | `` |
| `isLanQueryLocal` | function | `static/js/estorides.js:24` | `` |
| `k` | function | `static/js/estorides.js:1486` | `` |
| `k` | function | `static/js/estorides.js:1964` | `` |
| `labelFor` | function | `static/js/estorides.js:1719` | `` |
| `lanRunFields` | function | `static/js/estorides.js:33` | `` |
| `levelOf` | function | `static/js/estorides.js:1631` | `` |
| `loadAeroFeeds` | function | `static/js/estorides.js:603` | `` |
| `loadAnalysisModels` | function | `static/js/estorides.js:1245` | `` |
| `loadCases` | function | `static/js/estorides.js:2689` | `` |
| `loadFusionEntityDetail` | function | `static/js/estorides.js:3402` | `` |
| `loadFusionSearch` | function | `static/js/estorides.js:3357` | `` |
| `loadFusionStats` | function | `static/js/estorides.js:3309` | `` |
| `loadFusionTab` | function | `static/js/estorides.js:3303` | `` |
| `loadFusionTopChanged` | function | `static/js/estorides.js:3328` | `` |
| `loadSidebarCollapsed` | function | `static/js/estorides.js:3224` | `` |
| `loadSidebarWidth` | function | `static/js/estorides.js:3210` | `` |
| `makeModelPill` | function | `static/js/estorides.js:1264` | `` |
| `maybePlotDiscoverEntity` | function | `static/js/estorides.js:3696` | `` |
| `mergeExpansionIntoGraph` | function | `static/js/estorides.js:1472` | `` |
| `msg` | function | `static/js/estorides.js:878` | `` |
| `names` | class | `static/js/estorides.js:460` | `` |
| `obs` | function | `static/js/estorides.js:2553` | `` |
| `obs` | function | `static/js/estorides.js:2717` | `` |
| `on` | class | `static/js/estorides.js:2394` | `` |
| `onNo` | function | `static/js/estorides.js:78` | `` |
| `onYes` | function | `static/js/estorides.js:77` | `` |
| `openCaseDetail` | function | `static/js/estorides.js:2715` | `` |
| `openModal` | function | `static/js/estorides.js:3059` | `` |
| `out` | function | `static/js/estorides.js:319` | `` |
| `plotPoints` | function | `static/js/estorides.js:414` | `` |
| `points` | function | `static/js/estorides.js:624` | `` |
| `pollToolInstall` | function | `static/js/estorides.js:293` | `` |
| `populateCategoryFilter` | function | `static/js/estorides.js:326` | `` |
| `promptModal` | function | `static/js/estorides.js:3094` | `` |
| `pump` | function | `static/js/estorides.js:1388` | `` |
| `purifyHTML` | function | `static/js/estorides.js:1681` | `` |
| `pushLink` | function | `static/js/estorides.js:1560` | `` |
| `q` | function | `static/js/estorides.js:2690` | `` |
| `reanalyze` | function | `static/js/estorides.js:1319` | `` |
| `removed` | function | `static/js/estorides.js:2965` | `` |
| `renderAnalysis` | function | `static/js/estorides.js:1277` | `` |
| `renderAnalysisModels` | function | `static/js/estorides.js:1252` | `` |
| `renderCaseDiffPanel` | function | `static/js/estorides.js:2954` | `` |
| `renderCaseItem` | function | `static/js/estorides.js:2809` | `` |
| `renderEntities` | function | `static/js/estorides.js:2460` | `` |
| `renderGraphCore` | function | `static/js/estorides.js:2090` | `` |

Next: [SYMBOLS_p4.md](SYMBOLS_p4.md)
