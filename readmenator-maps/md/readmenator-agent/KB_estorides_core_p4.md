# Subsystem: estorides_core (page 4 of 4)
Previous: [KB_estorides_core_p3.md](KB_estorides_core_p3.md)

## estorides_core/sqlite_store.py
- Doc: estorides_core.sqlite_store
- Layer: data_access
- Language: py
- Symbols:
  - `SqliteStore` (class, line 34) `class SqliteStore`
  - `DictMixin` (class, line 109) `class DictMixin`
  - `__init__` (method, line 50) `def __init__(self, path)`
  - `_init_schema` (method, line 66) `def _init_schema(self)`
  - `_tx` (method, line 72) `def _tx(self)`
  - `close` (method, line 82) `def close(self)`
  - `__del__` (method, line 89) `def __del__(self)`
  - `to_dict` (method, line 112) `def to_dict(self)`
- Imported by: `estorides_core/cases.py`, `estorides_core/entity_store.py`, `estorides_core/fusion_store.py`, `estorides_core/monitoring.py`, `tests/test_sqlite_store.py`

## estorides_core/ssrf_guard.py
- Doc: estorides_core.ssrf_guard
- Layer: utility
- Language: py
- Symbols:
  - `GuardResult` (class, line 99) `class GuardResult`
  - `_is_blocked_v4` (function, line 110) `def _is_blocked_v4(ip)`
  - `_is_blocked_v6` (function, line 114) `def _is_blocked_v6(addr)`
  - `_normalise_host` (function, line 126) `def _normalise_host(host)`
  - `_is_host_in_blocked_literal` (function, line 134) `def _is_host_in_blocked_literal(host)`
  - `_resolve` (function, line 155) `def _resolve(host)`
  - `_matches_allowlist` (function, line 172) `def _matches_allowlist(host, allowlist)`
  - `_load_allowlist` (function, line 189) `def _load_allowlist()`
  - `check_url` (function, line 194) `def check_url(url)`
  - `assert_safe` (function, line 262) `def assert_safe(url)`
  - `SSRFError` (class, line 269) `class SSRFError(ValueError)`
  - `__bool__` (method, line 105) `def __bool__(self)`
- Imported by: `estorides_core/alerter.py`, `estorides_core/async_client.py`, `estorides_core/feeds.py`, `estorides_core/intel_resolver.py`, `estorides_core/ontology.py`, `estorides_core/osiris_sources.py`, `tests/test_security_remediation.py`

## estorides_core/supply_chain.py
- Layer: utility
- Language: py
- Symbols:
  - `ThirdParty` (class, line 54) `class ThirdParty`
  - `SharedInfra` (class, line 66) `class SharedInfra`
  - `Relationship` (class, line 78) `class Relationship`
  - `SupplyChainResult` (class, line 89) `class SupplyChainResult`
  - `detect_mx_provider` (function, line 106) `def detect_mx_provider(mx_records)`
  - `detect_ns_provider` (function, line 114) `def detect_ns_provider(ns_records)`
  - `detect_cdn` (function, line 122) `def detect_cdn(cname)`
  - `analyse_third_parties` (function, line 129) `def analyse_third_parties(third_parties, subsidiaries)`
  - `detect_shared_infrastructure` (function, line 140) `def detect_shared_infrastructure(asn)`
  - `to_dict` (method, line 61) `def to_dict(self)`
  - `to_dict` (method, line 73) `def to_dict(self)`
  - `to_dict` (method, line 84) `def to_dict(self)`
  - `to_dict` (method, line 96) `def to_dict(self)`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_supply_chain.py`

## estorides_core/system_app_sources.py
- Doc: estorides_core.system_app_sources
- Layer: utility
- Language: py
- Symbols:
  - `SystemAppResult` (class, line 57) `class SystemAppResult`
  - `is_system_app` (function, line 81) `def is_system_app(source)`
  - `tool_available` (function, line 91) `def tool_available(binary)`
  - `render_args` (function, line 96) `def render_args(args, query, outdir)`
  - `_read_capped` (function, line 121) `def _read_capped(path, cap)`
  - `_loads_lenient` (function, line 131) `def _loads_lenient(text)`
  - `_line_filter_parser` (function, line 150) `def _line_filter_parser()`
  - `parse_amass_json` (function, line 193) `def parse_amass_json(payload)`
  - `parse_maigret_json` (function, line 225) `def parse_maigret_json(payload)`
  - `parse_phoneinfoga_json` (function, line 247) `def parse_phoneinfoga_json(payload)`
  - `parse_sherlock_text` (function, line 260) `def parse_sherlock_text(payload)`
  - `parse_holehe_text` (function, line 265) `def parse_holehe_text(payload)`
  - `parse_wafw00f_text` (function, line 270) `def parse_wafw00f_text(payload)`
  - `parse_sublist3r_lines` (function, line 275) `def parse_sublist3r_lines(payload)`
  - `parse_dnsrecon_text` (function, line 280) `def parse_dnsrecon_text(payload)`
  - `parse_dnsenum_text` (function, line 285) `def parse_dnsenum_text(payload)`
  - `parse_fierce_text` (function, line 292) `def parse_fierce_text(payload)`
  - `parse_dmitry_text` (function, line 297) `def parse_dmitry_text(payload)`
  - `parse_urlcrazy_text` (function, line 302) `def parse_urlcrazy_text(payload)`
  - `parse_metagoofil_text` (function, line 307) `def parse_metagoofil_text(payload)`
  - `parse_whatweb_text` (function, line 312) `def parse_whatweb_text(payload)`
  - `parse_theharvester_text` (function, line 317) `def parse_theharvester_text(payload)`
  - `parse_usufy_text` (function, line 322) `def parse_usufy_text(payload)`
  - `parse_mailfy_text` (function, line 327) `def parse_mailfy_text(payload)`
  - `parse_phonefy_text` (function, line 332) `def parse_phonefy_text(payload)`
  - `parse_searchfy_text` (function, line 337) `def parse_searchfy_text(payload)`
  - `parse_tool_output` (function, line 365) `def parse_tool_output(source_name, parser_name, data)`
  - `execute` (function, line 396) `def execute(source, query)`
  - `to_dict` (method, line 76) `def to_dict(self)`
  - `parser` (function, line 165) `def parser(payload)`
  - `fail` (function, line 418) `def fail(code, message)`
  - `repl` (function, line 109) `def repl(m)`
- Depends on: `estorides_core/config.py`, `estorides_core/parsers.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_core/orchestrator.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/test_system_app_sources.py`

## estorides_core/tech_fingerprint.py
- Layer: utility
- Language: py
- Symbols:
  - `Tech` (class, line 89) `class Tech`
  - `TechFingerprintResult` (class, line 102) `class TechFingerprintResult`
  - `fingerprint` (function, line 115) `def fingerprint(headers, html, cookies, status)`
  - `to_dict` (method, line 97) `def to_dict(self)`
  - `to_dict` (method, line 107) `def to_dict(self)`
  - `_add` (function, line 129) `def _add(name, category, version, source, confidence)`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_tech_fingerprint.py`

## estorides_core/tool_install.py
- Doc: estorides_core.tool_install
- Layer: utility
- Language: py
- Symbols:
  - `InstallRecipe` (class, line 81) `class InstallRecipe`
  - `InstallResult` (class, line 103) `class InstallResult`
  - `_elevate` (function, line 117) `def _elevate(cmd)`
  - `_run` (function, line 132) `def _run(cmd)`
  - `_check_shell_command` (function, line 148) `def _check_shell_command(command)`
  - `_needs_elevation` (function, line 154) `def _needs_elevation(command)`
  - `is_valid_recipe_name` (function, line 169) `def is_valid_recipe_name(name)`
  - `is_valid_binary` (function, line 174) `def is_valid_binary(name)`
  - `_recipe_table` (function, line 179) `def _recipe_table()`
  - `_recipe_path` (function, line 193) `def _recipe_path(name)`
  - `load_recipe` (function, line 210) `def load_recipe(name)`
  - `recipe_available` (function, line 254) `def recipe_available(name)`
  - `tool_available` (function, line 259) `def tool_available(binary)`
  - `list_recipes` (function, line 270) `def list_recipes()`
  - `ToolStatus` (class, line 278) `class ToolStatus`
  - `_system_app_binaries` (function, line 297) `def _system_app_binaries(sources_dir)`
  - `doctor` (function, line 321) `def doctor(sources_dir)`
  - `_install_apt` (function, line 358) `def _install_apt(recipe)`
  - `_tools_root` (function, line 371) `def _tools_root()`
  - `_install_git` (function, line 375) `def _install_git(recipe)`
  - `install_tool` (function, line 414) `def install_tool(tool_name)`
  - `_verify` (function, line 506) `def _verify(binary)`
  - `main` (function, line 516) `def main(argv)`
  - `has_apt` (method, line 95) `def has_apt(self)`
  - `has_git` (method, line 98) `def has_git(self)`
  - `to_dict` (method, line 113) `def to_dict(self)`
  - `to_dict` (method, line 287) `def to_dict(self)`
- Depends on: `estorides_core/config.py`, `estorides_core/tool_runner.py`
- Imported by: `estorides_web_tools.py`, `tests/test_central_config.py`, `tests/test_tool_doctor.py`, `tests/test_tool_install.py`

## estorides_core/tool_runner.py
- Layer: utility
- Language: py
- Symbols:
  - `ToolError` (class, line 17) `class ToolError(Exception)`
  - `ToolNotAllowedError` (class, line 21) `class ToolNotAllowedError(ToolError)`
  - `ToolInjectionError` (class, line 25) `class ToolInjectionError(ToolError)`
  - `ToolNotFoundError` (class, line 29) `class ToolNotFoundError(ToolError)`
  - `ToolTimeoutError` (class, line 33) `class ToolTimeoutError(ToolError)`
  - `ToolResult` (class, line 38) `class ToolResult`
  - `ToolErrorResult` (class, line 86) `class ToolErrorResult`
  - `_check_injection` (function, line 97) `def _check_injection(args)`
  - `_resolve_binary` (function, line 107) `def _resolve_binary(tool_name)`
  - `_check_allowlist` (function, line 114) `def _check_allowlist(tool_name)`
  - `_parse_entities_generic` (function, line 121) `def _parse_entities_generic(stdout, tool_name)`
  - `run_tool` (function, line 156) `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)`
  - `to_dict` (method, line 51) `def to_dict(self)`
  - `from_failure` (method, line 59) `def from_failure(cls, tool_name, error_code, error_message, duration_s, exit_code, stdout, stderr, parsed_entities)`
  - `to_dict` (method, line 93) `def to_dict(self)`
- Depends on: `estorides_core/config.py`, `estorides_core/entity_extraction.py`
- Imported by: `estorides_core/active_recon.py`, `estorides_core/lan_runner.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_install.py`, `tests/properties/test_system_app_sources_properties.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py`, `tests/test_lan_runner.py`, `tests/test_system_app_sources.py`, `tests/test_tool_runner.py`

## estorides_core/transforms.py
- Doc: estorides_core.transforms
- Layer: utility
- Language: py
- Symbols:
  - `Transform` (class, line 73) `class Transform`
  - `_empty` (function, line 98) `def _empty(root_type, value)`
  - `_resolver_filtered` (function, line 102) `def _resolver_filtered(ent_type, value, relations)`
  - `_filter_runner` (function, line 123) `def _filter_runner(relations)`
  - `_norm` (function, line 132) `def _norm(s)`
  - `_osiris` (function, line 137) `def _osiris()`
  - `_run_bgp` (function, line 145) `def _run_bgp(ent_type, value)`
  - `_run_leaks` (function, line 171) `def _run_leaks(ent_type, value)`
  - `_run_github` (function, line 196) `def _run_github(ent_type, value)`
  - `TransformRegistry` (class, line 227) `class TransformRegistry`
  - `_str_list` (function, line 324) `def _str_list(raw)`
  - `_static_runner` (function, line 334) `def _static_runner(nodes_tpl, links_tpl)`
  - `_transform_from_yaml` (function, line 364) `def _transform_from_yaml(raw, origin)`
  - `iter_sse_events` (function, line 408) `def iter_sse_events(transform_id, ent_type, value, runner)`
  - `_T` (function, line 443) `def _T(id, label, tier, applies, runner, description, output_types, cost)`
  - `summary` (method, line 85) `def summary(self)`
  - `run` (function, line 124) `def run(ent_type, value)`
  - `__init__` (method, line 230) `def __init__(self)`
  - `register` (method, line 233) `def register(self, t)`
  - `for_type` (method, line 236) `def for_type(self, ent_type)`
  - `run` (method, line 248) `def run(self, transform_id, ent_type, value)`
  - `load_yaml_dir` (method, line 282) `def load_yaml_dir(self, directory)`
  - `run` (function, line 337) `def run(ent_type, value)`
  - `sub` (function, line 340) `def sub(s, depth)`
- Depends on: `estorides_core/config.py`, `estorides_core/intel_resolver.py`
- Imported by: `estorides_web.py`, `tests/test_transforms.py`

## estorides_core/transliteration.py
- Doc: estorides_core.transliteration
- Layer: utility
- Language: py
- Symbols:
  - `_strip_diacritics` (function, line 76) `def _strip_diacritics(text)`
  - `to_latin` (function, line 87) `def to_latin(text)`
  - `consonant_skeleton` (function, line 112) `def consonant_skeleton(text)`
  - `is_non_latin` (function, line 139) `def is_non_latin(text)`
- Imported by: `estorides_core/entity_resolution.py`, `tests/test_entity_resolution.py`

## estorides_core/validation.py
- Doc: estorides_core.validation
- Layer: utility
- Language: py
- Symbols:
  - `QueryValidationError` (class, line 55) `class QueryValidationError(ValueError)`
  - `Query` (class, line 63) `class Query`
  - `_strip_and_collapse` (function, line 73) `def _strip_and_collapse(text)`
  - `validate_query` (function, line 85) `def validate_query(raw)`
  - `__init__` (method, line 57) `def __init__(self, reason, message)`
  - `__str__` (method, line 69) `def __str__(self)`
- Depends on: `estorides_core/entity_extraction.py`
- Imported by: `estorides_cli.py`, `estorides_web.py`, `tests/test_tool_runner.py`

## estorides_core/vuln_correlation.py
- Layer: utility
- Language: py
- Symbols:
  - `DefaultCred` (class, line 14) `class DefaultCred`
  - `VulnEntry` (class, line 24) `class VulnEntry`
  - `VulnCorrelationResult` (class, line 43) `class VulnCorrelationResult`
  - `_parsed_version` (function, line 141) `def _parsed_version(version)`
  - `_version_in_range` (function, line 153) `def _version_in_range(version, v_start, v_end)`
  - `lookup_cve_for_tech` (function, line 169) `def lookup_cve_for_tech(tech_name, version)`
  - `correlate_technologies` (function, line 202) `def correlate_technologies(technologies)`
  - `compute_attack_readiness` (function, line 228) `def compute_attack_readiness(vulnerabilities)`
  - `to_dict` (method, line 19) `def to_dict(self)`
  - `to_dict` (method, line 38) `def to_dict(self)`
  - `to_dict` (method, line 52) `def to_dict(self)`
- Imported by: `estorides_core/recon_pipeline.py`, `tests/test_vuln_correlation.py`

## estorides_core/web_security.py
- Doc: estorides_core.web_security
- Layer: presentation
- Language: py
- Symbols:
  - `build_https_url` (function, line 58) `def build_https_url(public_host, path, query_string)`
  - `WebSecurityConfig` (class, line 87) `class WebSecurityConfig`
  - `_env_str` (function, line 137) `def _env_str(name, default)`
  - `load_security_config` (function, line 144) `def load_security_config()`
  - `install_security` (function, line 169) `def install_security(app, cfg)`
  - `_extract_bearer_token` (function, line 286) `def _extract_bearer_token()`
  - `make_auth_gate` (function, line 321) `def make_auth_gate()`
  - `AuthGate` (class, line 341) `class AuthGate`
  - `require_auth` (function, line 388) `def require_auth(view)`
  - `install_auth_gate` (function, line 421) `def install_auth_gate(app, gate)`
  - `_current_gate` (function, line 440) `def _current_gate()`
  - `auto_generated_token` (function, line 444) `def auto_generated_token()`
  - `is_cors_enabled` (method, line 128) `def is_cors_enabled(self)`
  - `is_origin_allowed` (method, line 132) `def is_origin_allowed(self)`
  - `_security_headers` (function, line 217) `def _security_headers(resp)`
  - `_cors_preflight` (function, line 250) `def _cors_preflight()`
  - `enabled` (method, line 351) `def enabled(self)`
  - `check` (method, line 354) `def check(self)`
  - `auth_meta_for_index` (method, line 362) `def auth_meta_for_index(self)`
  - `issue_session_cookie_kwargs` (method, line 371) `def issue_session_cookie_kwargs(self)`
  - `wrapper` (function, line 402) `def wrapper()`
  - `_redirect_to_https` (function, line 203) `def _redirect_to_https()`
- Imported by: `estorides_web.py`, `estorides_web_tools.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_hardening.py`, `tests/test_map_basemap.py`, `tests/test_security_remediation.py`, `tests/test_web_helpers.py`

