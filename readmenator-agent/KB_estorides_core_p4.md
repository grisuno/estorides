# Subsystem: estorides_core (page 4 of 4)
Previous: [KB_estorides_core_p3.md](KB_estorides_core_p3.md)

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

