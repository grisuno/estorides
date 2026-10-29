# estorides_core: config

*Community 4 | 16 files | cohesion 0.35*

## Definition

This community groups 16 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.35). Central symbols: `AsyncClient`, `BufferedEventSink`, `CacheConfig`, `CircuitBreaker`, `EntityResolver`, `EntityRunner`, `EventSink`, `Fake`. Core file: `estorides_core/config.py` (29 symbols). Documented purpose: estorides_core.async_client.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/async_client.py` | py | infrastructure | 21 | yes |
| `estorides_core/config.py` | py | infrastructure | 29 | yes |
| `estorides_core/intel_resolver.py` | py | utility | 26 | yes |
| `estorides_core/lan_bundle.py` | py | utility | 8 | yes |
| `estorides_core/observation_models.py` | py | business_logic | 14 | yes |
| `estorides_core/ontology.py` | py | utility | 25 | yes |
| `estorides_core/osiris_sources.py` | py | utility | 8 | yes |
| `estorides_core/pivot_engine.py` | py | utility | 25 | yes |
| `estorides_core/ssrf_guard.py` | py | utility | 12 | yes |
| `estorides_core/transforms.py` | py | utility | 24 | yes |
| `tests/properties/test_observation_models_properties.py` | py | testing | 7 | yes |
| `tests/test_async_client.py` | py | testing | 15 | yes |
| `tests/test_config_env.py` | py | testing | 13 | yes |
| `tests/test_observation_models.py` | py | testing | 28 | yes |
| `tests/test_structured_extraction.py` | py | testing | 8 | yes |
| `tests/test_transforms.py` | py | testing | 12 | yes |

## Key Symbols

- `_is_socks` (function, `estorides_core/async_client.py:49`) `def _is_socks(proxy)` - True when the proxy URL is a SOCKS proxy (e.g. Tor).
- `_redact_proxy` (function, `estorides_core/async_client.py:54`) `def _redact_proxy(proxy)` - Strip any `user:pass@` credentials from a proxy URL before logging.
- `CircuitBreaker` (class, `estorides_core/async_client.py:64`) `class CircuitBreaker` - Per-host circuit breaker.
- `allow` (method, `estorides_core/async_client.py:69`) `def allow(self, host)`
- `record_success` (method, `estorides_core/async_client.py:75`) `def record_success(self, host)`
- `record_failure` (method, `estorides_core/async_client.py:79`) `def record_failure(self, host)`
- `ResponseCache` (class, `estorides_core/async_client.py:86`) `class ResponseCache` - SQLite-backed response cache. Key = (url + method + body hash).
- `__init__` (method, `estorides_core/async_client.py:95`) `def __init__(self, path)`
- `_conn` (method, `estorides_core/async_client.py:109`) `def _conn(self)` - Short-lived connection that is always closed.
- `_init_db` (method, `estorides_core/async_client.py:123`) `def _init_db(self)`
- `_key` (method, `estorides_core/async_client.py:136`) `def _key(method, url, body)`
- `get` (method, `estorides_core/async_client.py:145`) `def get(self, method, url, body)`
- `set` (method, `estorides_core/async_client.py:161`) `def set(self, method, url, body, value)`
- `AsyncClient` (class, `estorides_core/async_client.py:172`) `class AsyncClient` - Async HTTP client with retries, backoff, circuit breaker, cache.
- `__init__` (method, `estorides_core/async_client.py:175`) `def __init__(self)`
- `__aenter__` (method, `estorides_core/async_client.py:206`) `def __aenter__(self)`
- `_next_http_proxy` (method, `estorides_core/async_client.py:250`) `def _next_http_proxy(self)` - Round-robin the next HTTP proxy, or None (SOCKS/connector or direct).
- `__aexit__` (method, `estorides_core/async_client.py:258`) `def __aexit__(self)`
- `session` (method, `estorides_core/async_client.py:264`) `def session(self)`
- `fetch` (method, `estorides_core/async_client.py:270`) `def fetch(self, method, url)` - Fetch a URL. Returns (parsed_data, meta).
- `sync_fetch` (function, `estorides_core/async_client.py:400`) `def sync_fetch(method, url)`
- `_installed_share` (function, `estorides_core/config.py:42`) `def _installed_share()` - `<prefix>/share/estorides` — the data-files target of a pip install.
- `_resolve_dir` (function, `estorides_core/config.py:47`) `def _resolve_dir(env_key, dirname)` - Resolve a read-only runtime data dir.
- `_resolve_writable_dir` (function, `estorides_core/config.py:63`) `def _resolve_writable_dir(env_key, dirname)` - Resolve a writable runtime dir (no import-time mkdir, issue #49).
- `ensure_data_dirs` (function, `estorides_core/config.py:101`) `def ensure_data_dirs()` - Idempotently create DATA_DIR.
- `ensure_reports_dir` (function, `estorides_core/config.py:112`) `def ensure_reports_dir()` - Idempotently create REPORTS_DIR.
- `_env_tool_allowlist` (function, `estorides_core/config.py:169`) `def _env_tool_allowlist()`
- `contact_level` (function, `estorides_core/config.py:247`) `def contact_level(contact)` - Map a contact class to its numeric severity, unknown values to active.
- `effective_proxies` (function, `estorides_core/config.py:273`) `def effective_proxies(explicit)` - Resolve the proxy rotation pool from an explicit value or the env.
- `CacheConfig` (class, `estorides_core/config.py:407`) `class CacheConfig` - Disk response-cache behaviour.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 34
- Cross-boundary resolved imports (EXTRACTED): 48

## Connections

- [EXTRACTED] depends_on community 3 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 1 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/__init__.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 0 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/audit.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 6 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/discoverer.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 9 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/entity_extraction.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 8 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/feeds.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 2 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/fusion_store.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 10 <-> 4 (strength 0.9): Extracted import edge crosses communities: estorides_core/knowledge_graph.py imports estorides_core/config.py.

## Risks

- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/async_client.py` via `requests` (0 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)

## Open Questions

- Is the dangerous import `requests` in `estorides_core/async_client.py` still required, or can it be isolated?
- What would break if the most connected file in estorides_core: config changed?
- Should estorides_core: config be split, given cohesion 0.35?

## Sources

- `estorides_core/async_client.py`
- `estorides_core/config.py`
- `estorides_core/intel_resolver.py`
- `estorides_core/lan_bundle.py`
- `estorides_core/observation_models.py`
- `estorides_core/ontology.py`
- `estorides_core/osiris_sources.py`
- `estorides_core/pivot_engine.py`
- `estorides_core/ssrf_guard.py`
- `estorides_core/transforms.py`
- `tests/properties/test_observation_models_properties.py`
- `tests/test_async_client.py`
- `tests/test_config_env.py`
- `tests/test_observation_models.py`
- `tests/test_structured_extraction.py`
- `tests/test_transforms.py`
