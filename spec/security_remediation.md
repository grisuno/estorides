# Security Remediation — cross-cutting vulnerabilities

## Purpose

Close 6 high/medium CodeQL findings across the Estorides codebase that expose
sensitive information, allow DOM-based XSS, redirect via unvalidated user
input, and lack CI workflow permission boundaries. Each finding is a single
root cause in its owning module and is fixed without breaking existing behavior.

## Vulnerabilities

| # | Severity | Module | Line | CWE | Root cause |
|---|----------|--------|------|-----|------------|
| 10 | High | ssrf_guard.py | 169 | CWE-532 | DNS resolution exceptions logged with sensitive hostname |
| 20 | High | estorides.js | 893 | CWE-79 | `innerHTML = html` without sanitisation of template content |
| 16 | High | estorides.js | 1068 | CWE-79 | `innerHTML = ...` with unescaped user data in class/value attrs |
| 26 | Medium | estorides_web.py | 881 | CWE-209 | `str(e)` from KeyError returned to client |
| 25 | Medium | estorides_web.py | 865 | CWE-209 | `str(e)` from ValueError returned to client |
| 24 | Medium | estorides_web.py | 846 | CWE-209 | `str(e)` from ValueError returned to client |
| 22 | Medium | estorides_web.py | 675 | CWE-209 | Stats endpoint leaks internal state shape |
| 21 | Medium | estorides_web.py | 632 | CWE-209 | Error response includes usage hints with table/column names |
| 19 | Medium | estorides_web.py | 451 | CWE-209 | `str(e)` from RuntimeError returned to client |
| 18 | Medium | estorides_web.py | 448 | CWE-209 | `str(e)` from ValueError returned to client |
| 11 | Medium | web_security.py | 196 | CWE-601 | `redirect(request.url.replace(...))` — open redirect via Host header |
| 9 | Medium | estorides_web.py | 991 | CWE-209 | Unvalidated osiris endpoint returns raw error |
| 8 | Medium | estorides_web.py | 980 | CWE-209 | Unvalidated osiris endpoint returns raw error |
| 7 | Medium | estorides_web.py | 958 | CWE-209 | Unvalidated osiris endpoint returns raw error |
| 6 | Medium | estorides_web.py | 947 | CWE-209 | Unvalidated osiris endpoint returns raw error |
| 5 | Medium | estorides_web.py | 930 | CWE-209 | Unvalidated osiris endpoint returns raw error |
| 17 | Medium | ci.yml | 11 | CWE-266 | No `permissions:` block — default is write-all |

## Inputs

- **ssrf_guard.py**: `host` (str) from DNS resolution — may contain internal
  hostnames. `e` (socket.gaierror) — may contain DNS server details.
- **estorides.js**: `html` (string) parameter to `showTooltipAt` — template
  literal with escaped user data but raw `innerHTML` assignment. `d` (object)
  in `selectNode` — properties may contain unsanitized strings.
- **estorides_web.py**: Exception objects (`ValueError`, `RuntimeError`,
  `KeyError`) from encryption, source file operations, and osiris fetches.
- **web_security.py**: `request.url` (str) — the `Host` header is attacker-
  controlled.
- **ci.yml**: No input; missing YAML key.

## Outputs

- **ssrf_guard.py**: Log line without hostname or exception detail. Example:
  `log.debug("DNS resolution failed (len=%d)", len(host))` — host length
  only, zero exception detail.
- **estorides.js**: Safe DOM construction using `createElement` + `textContent`
  for user-controlled values. No `innerHTML` assignment with dynamic content.
- **estorides_web.py**: JSON response `{"error": "<safe-error-code>"}` with
  no `detail` or `str(e)` fields. Exception logged server-side only.
- **web_security.py**: HTTPS redirect constructed from `request.host` (validated
  by Flask's host matching) + `request.path`, not from `request.url`.
- **ci.yml**: `permissions: read-all` at top level, `contents: read` per job.

## Error table

| Module | Error condition | HTTP / behaviour | Log level |
|--------|----------------|------------------|-----------|
| ssrf_guard.py | DNS resolution failure | N/A (no HTTP) | DEBUG with sanitised message |
| estorides.js | N/A | N/A — DOM construction is safe by design | N/A |
| estorides_web.py | ValueError in encryption key | 400 `{"error": "invalid-encryption-key"}` | WARNING (no detail) |
| estorides_web.py | RuntimeError in encryption | 500 `{"error": "encryption-failed"}` | ERROR (no detail) |
| estorides_web.py | KeyError in source delete | 404 `{"error": "source-not-found"}` | WARNING |
| estorides_web.py | ValueError in source write | 400 `{"error": "invalid-source-config"}` | WARNING |
| estorides_web.py | Osiris endpoint error | 500 `{"error": "osiris-failed"}` | ERROR |
| web_security.py | HTTPS redirect | 308 redirect to `https://host/path` | DEBUG |
| ci.yml | N/A | N/A — CI fails gracefully | N/A |

## Security guarantees

- No exception detail, internal path, table name, or column name reaches the
  HTTP response body.
- No internal hostname or IP is logged in DNS resolution failure messages.
- No `innerHTML` assignment uses unescaped user data — all DOM construction
  goes through `textContent` or `escapeHTML()`.
- HTTPS redirect cannot be hijacked via the `Host` header — only
  `request.host` (Flask-validated) is used.
- CI workflow has minimum necessary `read-all` permissions — no write access
  to any scope.

## Out of scope

- CSP violations (covered by `csp_safe_styles` module).
- SQL injection in Kuzu queries (handled by read-only gate in
  `api_intel_graph`).
- Rate-limiting / DoS (handled by `_rate_limit_decorator`).
- Auth bypass (handled by `require_auth` / `AuthGate`).

## BDD Scenarios

### S1 — DNS failure log does not leak hostname
Given: `ssrf_guard._resolve("internal-build-server.corp.example")`  
When: DNS resolution fails with `socket.gaierror`  
Then: the log message contains only the hostname length, not the hostname itself, and no exception detail.

### S2 — DNS failure log does not leak exception detail
Given: a `socket.gaierror` with message `"Temporary failure in name resolution"`  
When: caught in `_resolve`  
Then: the log message omits the exception `str()`.

### S3 — Encryption ValueError does not leak detail
Given: a POST to `/api/export/stix?key=invalid`  
When: the encryption layer raises `ValueError("bad bech32: invalid separator position")`  
Then: the response body is `{"error": "invalid-encryption-key"}` (no detail field).

### S4 — Encryption RuntimeError does not leak detail
Given: a POST to `/api/export/misp?key=age1...`  
When: the encryption layer raises `RuntimeError("gnupg internal path /etc/gpg/...")`  
Then: the response body is `{"error": "encryption-failed"}` (no detail field).

### S5 — Source delete KeyError does not leak detail
Given: a DELETE to `/api/sources/yaml/nonexistent`  
When: `registry.delete_source_file` raises `KeyError("'nonexistent'")`  
Then: the response is `{"error": "source-not-found"}` with status 404.

### S6 — Source write ValueError does not leak detail
Given: a POST to `/api/sources/yaml` with invalid body  
When: `registry.write_source_file` raises `ValueError("missing required field: url")`  
Then: the response is `{"error": "invalid-source-config"}` with status 400.

### S7 — HTTPS redirect is safe from Host header injection
Given: a request to `http://evil.com:8080/path` with `Host: attacker.com`  
When: `_redirect_to_https` runs  
Then: the redirect URL uses `request.host` not `request.url`, preventing open redirect.

### S8 — DOM tooltip does not use innerHTML with unsanitised data
Given: a graph node with label `<script>alert(1)</script>`  
When: `showTooltipAt` is called  
Then: the content is inserted via `textContent` or escaped; no script execution.

### S9 — DOM inspector does not use innerHTML with unsanitised data
Given: a graph node with property `{"xss": "<img onerror=alert(1) src=x>"}`  
When: `selectNode` renders the inspector panel  
Then: properties are inserted via `textContent` or escaped; no script execution.

### S10 — CI workflow has explicit read permissions
Given: `.github/workflows/ci.yml`  
When: inspected  
Then: `permissions: read-all` is present at the top level.

### S11 — Osiris endpoint failure does not leak detail
Given: `osiris_sources.fetch_mac("00:11:22:33:44:55")` raises `Exception`  
When: the exception handler runs  
Then: the response is `{"error": "osiris-failed"}` with status 500.

### S12 — Graph endpoint failure returns generic error
Given: a GET to `/api/intel/graph?q=MATCH...` with a query that fails  
When: the cypher execution raises an exception  
Then: the response is `{"error": "cypher-failed"}` (the existing behaviour is already correct — verified no regression).
