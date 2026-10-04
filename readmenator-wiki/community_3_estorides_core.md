# estorides_core

*Community 3 | 8 files | cohesion 0.41*

## Definition

This community groups 8 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.41). Central symbols: `AsyncClient`, `CircuitBreaker`, `EntityResolver`, `Fake`, `GuardResult`, `OntologyEngine`, `ResponseCache`, `SSRFError`. Core file: `estorides_core/intel_resolver.py` (26 symbols). Documented purpose: estorides_core.async_client.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/async_client.py` | py | infrastructure | 21 | yes |
| `estorides_core/intel_resolver.py` | py | utility | 26 | yes |
| `estorides_core/ontology.py` | py | utility | 25 | yes |
| `estorides_core/osiris_sources.py` | py | utility | 8 | yes |
| `estorides_core/ssrf_guard.py` | py | utility | 12 | yes |
| `estorides_core/transforms.py` | py | data_access | 24 | yes |
| `tests/test_async_client.py` | py | testing | 15 | yes |
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
- `sync_fetch` (method, `estorides_core/async_client.py:400`) `def sync_fetch(method, url)`
- `_run_sparql` (function, `estorides_core/intel_resolver.py:90`) `def _run_sparql(query)` - Execute a SPARQL SELECT against the Wikidata endpoint.
- `_val` (function, `estorides_core/intel_resolver.py:111`) `def _val(row, key)` - Pull a string value out of a SPARQL JSON row.
- `_TTLCache` (class, `estorides_core/intel_resolver.py:120`) `class _TTLCache`
- `__init__` (method, `estorides_core/intel_resolver.py:121`) `def __init__(self)`
- `get` (method, `estorides_core/intel_resolver.py:127`) `def get(self, kind, key)`
- `put` (method, `estorides_core/intel_resolver.py:140`) `def put(self, kind, key, value)`
- `stats` (method, `estorides_core/intel_resolver.py:148`) `def stats(self)`
- `EntityResolver` (class, `estorides_core/intel_resolver.py:156`) `class EntityResolver` - Cross-feed entity resolution.
- `__init__` (method, `estorides_core/intel_resolver.py:165`) `def __init__(self)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 14
- Cross-boundary resolved imports (EXTRACTED): 16

## Connections

- [EXTRACTED] depends_on community 1 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/alerter.py imports estorides_core/ssrf_guard.py.
- [EXTRACTED] depends_on community 3 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/async_client.py imports estorides_core/config.py.
- [INFERRED] shares_context community 0 <-> 3 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 0 (root) and community 3 (estorides_core).

## Risks

- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/alerter.py` -> `estorides_core/ssrf_guard.py` via `urllib.request` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/async_client.py` via `requests` (0 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/async_client.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/feeds.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/intel_resolver.py` via `requests` (0 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/ssrf_guard.py` via `requests` (1 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/ontology.py` via `requests` (1 hops)
- [taint medium] `estorides_core/intel_resolver.py` -> `estorides_core/config.py` via `requests` (1 hops)
- [layer strict] `estorides_web.py` (presentation) -> `estorides_core/transforms.py` (data_access)
- [layer strict] `estorides_web.py` (presentation) -> `estorides_core/transforms.py` (data_access)

## Open Questions

- Is the dangerous import `requests` in `estorides_core/async_client.py` still required, or can it be isolated?
- What would break if the most connected file in estorides_core changed?
- Should estorides_core be split, given cohesion 0.41?

## Sources

- `estorides_core/async_client.py`
- `estorides_core/intel_resolver.py`
- `estorides_core/ontology.py`
- `estorides_core/osiris_sources.py`
- `estorides_core/ssrf_guard.py`
- `estorides_core/transforms.py`
- `tests/test_async_client.py`
- `tests/test_transforms.py`
