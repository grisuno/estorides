# Subsystem: estorides_core (page 4 of 4)
Previous: [KB_estorides_core_p3.md](KB_estorides_core_p3.md)

## estorides_core/tool_install.py
- Doc: estorides_core.tool_install
- Layer: utility
- Language: py
- Symbols:
  - `InstallRecipe` (class, line 81) `class InstallRecipe`
  - `InstallResult` (class, line 103) `class InstallResult`
  - `_elevate` (method, line 117) `def _elevate(cmd)`
  - `_run` (method, line 132) `def _run(cmd)`
  - `_check_shell_command` (method, line 148) `def _check_shell_command(command)`
  - `_needs_elevation` (method, line 154) `def _needs_elevation(command)`
  - `is_valid_recipe_name` (method, line 169) `def is_valid_recipe_name(name)`
  - `is_valid_binary` (method, line 174) `def is_valid_binary(name)`
  - `_recipe_table` (method, line 179) `def _recipe_table()`
  - `_recipe_path` (method, line 193) `def _recipe_path(name)`
  - `load_recipe` (method, line 210) `def load_recipe(name)`
  - `recipe_available` (method, line 254) `def recipe_available(name)`
  - `tool_available` (method, line 259) `def tool_available(binary)`
  - `list_recipes` (method, line 270) `def list_recipes()`
  - `ToolStatus` (class, line 278) `class ToolStatus`
  - `_system_app_binaries` (method, line 297) `def _system_app_binaries(sources_dir)`
  - `doctor` (method, line 321) `def doctor(sources_dir)`
  - `_install_apt` (method, line 358) `def _install_apt(recipe)`
  - `_tools_root` (method, line 371) `def _tools_root()`
  - `_install_git` (method, line 375) `def _install_git(recipe)`
  - `install_tool` (method, line 414) `def install_tool(tool_name)`
  - `_verify` (method, line 506) `def _verify(binary)`
  - `main` (method, line 516) `def main(argv)`
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
  - `_check_injection` (method, line 97) `def _check_injection(args)`
  - `_resolve_binary` (method, line 107) `def _resolve_binary(tool_name)`
  - `_check_allowlist` (method, line 114) `def _check_allowlist(tool_name)`
  - `_parse_entities_generic` (method, line 121) `def _parse_entities_generic(stdout, tool_name)`
  - `run_tool` (method, line 156) `def run_tool(tool_name, args, target, timeout, max_output_bytes, cwd)`
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
  - `_empty` (method, line 98) `def _empty(root_type, value)`
  - `_resolver_filtered` (method, line 102) `def _resolver_filtered(ent_type, value, relations)`
  - `_filter_runner` (method, line 123) `def _filter_runner(relations)`
  - `_norm` (method, line 132) `def _norm(s)`
  - `_osiris` (method, line 137) `def _osiris()`
  - `_run_bgp` (method, line 145) `def _run_bgp(ent_type, value)`
  - `_run_leaks` (method, line 171) `def _run_leaks(ent_type, value)`
  - `_run_github` (method, line 196) `def _run_github(ent_type, value)`
  - `TransformRegistry` (class, line 227) `class TransformRegistry`
  - `_str_list` (method, line 324) `def _str_list(raw)`
  - `_static_runner` (method, line 334) `def _static_runner(nodes_tpl, links_tpl)`
  - `_transform_from_yaml` (method, line 364) `def _transform_from_yaml(raw, origin)`
  - `iter_sse_events` (method, line 408) `def iter_sse_events(transform_id, ent_type, value, runner)`
  - `_T` (method, line 443) `def _T(id, label, tier, applies, runner, description, output_types, cost)`
  - `summary` (method, line 85) `def summary(self)`
  - `run` (method, line 124) `def run(ent_type, value)`
  - `__init__` (method, line 230) `def __init__(self)`
  - `register` (method, line 233) `def register(self, t)`
  - `for_type` (method, line 236) `def for_type(self, ent_type)`
  - `run` (method, line 248) `def run(self, transform_id, ent_type, value)`
  - `load_yaml_dir` (method, line 282) `def load_yaml_dir(self, directory)`
  - `run` (method, line 337) `def run(ent_type, value)`
  - `sub` (method, line 340) `def sub(s, depth)`
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
  - `_strip_and_collapse` (method, line 73) `def _strip_and_collapse(text)`
  - `validate_query` (method, line 85) `def validate_query(raw)`
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
  - `_parsed_version` (method, line 141) `def _parsed_version(version)`
  - `_version_in_range` (method, line 153) `def _version_in_range(version, v_start, v_end)`
  - `lookup_cve_for_tech` (method, line 169) `def lookup_cve_for_tech(tech_name, version)`
  - `correlate_technologies` (method, line 202) `def correlate_technologies(technologies)`
  - `compute_attack_readiness` (method, line 228) `def compute_attack_readiness(vulnerabilities)`
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
  - `_env_str` (method, line 137) `def _env_str(name, default)`
  - `load_security_config` (method, line 144) `def load_security_config()`
  - `install_security` (method, line 169) `def install_security(app, cfg)`
  - `_extract_bearer_token` (method, line 286) `def _extract_bearer_token()`
  - `make_auth_gate` (method, line 321) `def make_auth_gate()`
  - `AuthGate` (class, line 341) `class AuthGate`
  - `require_auth` (method, line 388) `def require_auth(view)`
  - `install_auth_gate` (method, line 421) `def install_auth_gate(app, gate)`
  - `_current_gate` (method, line 440) `def _current_gate()`
  - `auto_generated_token` (method, line 444) `def auto_generated_token()`
  - `is_cors_enabled` (method, line 128) `def is_cors_enabled(self)`
  - `is_origin_allowed` (method, line 132) `def is_origin_allowed(self)`
  - `_security_headers` (method, line 217) `def _security_headers(resp)`
  - `_cors_preflight` (method, line 250) `def _cors_preflight()`
  - `enabled` (method, line 351) `def enabled(self)`
  - `check` (method, line 354) `def check(self)`
  - `auth_meta_for_index` (method, line 362) `def auth_meta_for_index(self)`
  - `issue_session_cookie_kwargs` (method, line 371) `def issue_session_cookie_kwargs(self)`
  - `wrapper` (method, line 402) `def wrapper()`
  - `_redirect_to_https` (method, line 203) `def _redirect_to_https()`
- Imported by: `estorides_web.py`, `estorides_web_tools.py`, `tests/properties/test_csp_safe_styles_properties.py`, `tests/test_auth_gate.py`, `tests/test_csp_safe_styles.py`, `tests/test_hardening.py`, `tests/test_map_basemap.py`, `tests/test_security_remediation.py`, `tests/test_web_helpers.py`

