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
| 37 | High | estorides.js | 890 | CWE-79 | Regex-based sanitizeHTML can be bypassed (bad HTML filtering regexp) |
| 36 | High | estorides.js | 890 | CWE-79 | Regex-based sanitizeHTML incomplete multi-character sanitisation |
| 35 | High | estorides.js | 890 | CWE-79 | Regex-based sanitizeHTML incomplete multi-character sanitisation |
| 26 | Medium | estorides_web.py | 881 | CWE-209 | `str(e)` from KeyError returned to client |
| 25 | Medium | estorides_web.py | 865 | CWE-209 | `str(e)` from ValueError returned to client |
| 24 | Medium | estorides_web.py | 846 | CWE-209 | `str(e)` from ValueError returned to client |
| 22 | Medium | graph_kuzu.py | 433 | CWE-209 | `stats()` returns `str(e)` in error dict, jsonified by estorides_web.py |
| 21 | Medium | estorides_web.py | 632 | CWE-209 | Error response includes usage hints with table/column names |
| 19 | Medium | estorides_web.py | 451 | CWE-209 | `str(e)` from RuntimeError returned to client |
| 18 | Medium | estorides_web.py | 448 | CWE-209 | `str(e)` from ValueError returned to client |
| 11 | Medium | web_security.py | 197 | CWE-601 | `redirect(request.host)` — Host header is attacker-controlled |
| 32 | Medium | osiris_sources.py | 392 | CWE-209 | `fetch_leaks` returns `str(e)` in error dict, jsonified by estorides_web.py |
| 31 | Medium | osiris_sources.py | 350 | CWE-209 | `fetch_github_user` returns `str(e)` in error dict, jsonified by estorides_web.py |
| 30 | Medium | osiris_sources.py | 210 | CWE-209 | `fetch_mac` returns `str(e)` in error dict, jsonified by estorides_web.py |
| 29 | Medium | osiris_sources.py | 178 | CWE-209 | `fetch_bgp` returns `str(e)` in error dict, jsonified by estorides_web.py |
| 28 | Medium | transforms.py | 218 | CWE-209 | `transform_registry.run()` returns `str(e)`, jsonified by estorides_web.py |
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
- **web_security.py**: HTTPS redirect constructed from `cfg.public_host`
  (configured via `ESTORIDES_PUBLIC_HOST` env var, default `localhost:5050`),
  not from `request.host` or `request.url`.
- **transforms.py / osiris_sources.py / graph_kuzu.py**: Exception error dicts
  use generic strings (e.g. `"bgp-lookup-failed"`), not `str(e)`.
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
  `cfg.public_host` is used.
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
Given: a request to `http://example.com/path` with `Host: attacker.com`  
When: `_redirect_to_https` runs  
Then: the redirect URL uses `cfg.public_host` (e.g. `localhost:5050`), NOT `request.host`, preventing Host header injection open redirect.

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

### S13 — sanitizeHTML uses DOMParser not regex
Given: a string containing `\x3Cscript\x3Ealert(1)\x3C/script\x3E`  
When: `sanitizeHTML` is called  
Then: the DOMParser parses it safely and strips the script element.

### S14 — sanitizeHTML removes event handlers
Given: a string containing `<img onerror=alert(1) src=x>`  
When: `sanitizeHTML` is called  
Then: the `onerror` attribute is removed.

### S15 — sanitizeHTML removes javascript: URIs
Given: a string containing `<a href="javascript:alert(1)">click</a>`  
When: `sanitizeHTML` is called  
Then: the `href` attribute with `javascript:` is removed.

### S16 — Osiris fetch_bgp does not leak exception detail
Given: `fetch_bgp` catches an exception with message `"connection refused"`  
When: the exception handler runs  
Then: the error dict contains `"bgp-lookup-failed"`, not the exception message.

### S17 — TransformRegistry.run does not leak exception detail
Given: `TransformRegistry.run` catches an exception with message `"cache full"`  
When: the exception handler runs  
Then: the error dict contains `"transform-run-failed"`, not the exception message.

### S18 — graph_kuzu stats does not leak exception detail
Given: `KuzuBackend.stats` catches a Cypher exception with message `"Binder exception"`
When: the exception handler runs
Then: the error dict contains `"stats-query-failed"`, not the exception message.

### S19 — alerter never follows HTTP redirects (CodeQL #47)
Given: `_http_post` to an allowlisted public URL whose server answers `302`
  with `Location: http://169.254.169.254/latest/meta-data`
When: the POST runs
Then: no second request is issued (the redirect is refused and the call
  returns `False`), so a malicious webhook cannot pivot to cloud metadata
  after passing the initial SSRF guard.

### S20 — recipe name cannot escape the recipes dir (CodeQL #48/#49)
Given: `load_recipe("../../etc/cron")`, `load_recipe("x/y")`,
  `load_recipe("")` or any name outside `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$`
When: the recipe is loaded
Then: it returns `None` (logged as a warning); no path outside
  `TOOL_RECIPES_DIR` is ever opened. `_recipe_path` additionally asserts
  containment via `resolve()` + `relative_to`.

### S21 — git clone target cannot escape TOOLS_DIR (CodeQL #48/#49 depth)
Given: a recipe whose `install_path` is `"../../evil"`
When: `_install_git` runs
Then: it refuses (`ok=False`, error mentions escaping the tools dir) and
  never invokes `git clone` outside `TOOLS_DIR`.

### S22 — install_tool validates binary before the allowlist (CodeQL #48/#49 depth)
Given: `install_tool("nmap", binary="/bin/sh")`,
  `install_tool("nmap", binary="../../bin/x")`, or a binary not in
  `TOOL_ALLOWLIST`
When: the install runs
Then: it returns `success=False` with an error (`invalid binary` / `not in
  allowlist`) WITHOUT probing PATH — the already-installed shortcut may
  never bypass the allowlist.

### S23 — tool install API rejects hostile names (CodeQL #48/#49 depth)
Given: `POST /api/tools/../../etc/install` or body `{"binary": "/bin/sh"}`
When: the route runs
Then: it returns `404` (unknown recipe) / `400` (invalid binary) without
  touching the filesystem or spawning a worker thread.

### S24 — tooltip sink parses sanitised HTML exactly once (CodeQL #38)
Given: a graph node label `<img src=x onerror=alert(1)>` or
  `<a href="JaVaScRiPt:alert(1)">x</a>` or `<div style="x:url(javascript:y)">`
When: `showTooltipAt` / `renderMarkdown` renders it
Then: the payload reaches the DOM only as nodes parsed from the hardened
  `sanitizeHTML` output (no `insertAdjacentHTML` serialize→reparse
  round-trip); event-handler attributes, dangerous-scheme URLs
  (`javascript:`/`data:`/`vbscript:`/`file:`/`blob:` on
  href/src/action/formaction/xlink:href/srcdoc/cite/background), `style`
  attributes, and `script/iframe/object/embed/style/link/meta/base/form/
  frame/frameset/applet/marquee` elements are all removed.

### S25 — raw webhook URLs refused, recipe allowlist gate (CodeQL #47/#48/#49/#52 closer round 5)
Given: `send("https://hooks.example.com/hook")` or `send("http://127.0.0.1/x")`
When: the dispatcher runs
Then: it returns `False` without opening any socket (`_http_post` never
  called); only named channels (`slack/discord/telegram/email/webhook`)
  backed by operator env vars ever become request destinations, so no
  caller string flows to `Request()` (the #47 sink).
Given: `load_recipe("no-such-recipe-xyz")` or `install_tool` with an
  unknown recipe name
When: called
Then: it returns `None` / "no install recipe" before any path is built
  (`_recipe_path` never called); only directory-listed recipe stems reach
  `TOOL_RECIPES_DIR / f"{name}.yaml"` (the #48/#49/#52 sinks), plus the
  existing regex, separator (`/`, `\\`, NUL, `..`) and `resolve()`/
  `parent` containment checks stay as depth.

### S26 — Markdown render has no HTML-string sink (CodeQL #38 closer round 5)
Given: streamed LLM text `acc` or case analysis `a.content`
When: rendered
Then: it goes through `renderMarkdownInto(el, text)` (parse → sanitize →
  node append) and never through `el.innerHTML = renderMarkdown(...)`;
  no `innerHTML = renderMarkdown` string sink remains in the bundle.
