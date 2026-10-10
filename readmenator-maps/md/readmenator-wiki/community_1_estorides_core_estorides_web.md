# estorides_core: estorides_web

*Community 1 | 24 files | cohesion 0.48*

## Definition

This community groups 24 file(s) rooted at `tests` with dominant language py (cohesion 0.48). Central symbols: `AuditEvent`, `AuditLog`, `AuthGate`, `Bm25Index`, `GraphRagConfig`, `GraphRagIndex`, `GraphRagSearcher`, `InvalidTelemetryConfigError`. Core file: `estorides_web.py` (95 symbols). Documented purpose: Deprecated entry point. Use:  - the `estorides` console script (installed by `pip install -e .`), or - `python3 estorides_cli.py serve` for the dev server, or -.

## Files

### `tests` (10 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_audit_log.py` | py | testing | 5 | yes |
| `tests/test_auth_gate.py` | py | testing | 10 | yes |
| `tests/test_csp_safe_styles.py` | py | testing | 11 | yes |
| `tests/test_graph_rag_search.py` | py | testing | 11 | yes |
| `tests/test_map_basemap.py` | py | testing | 5 | yes |
| `tests/test_openapi.py` | py | testing | 1 | yes |

### `estorides_core` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/audit.py` | py | utility | 11 | yes |
| `estorides_core/graph_rag_search.py` | py | utility | 44 | yes |
| `estorides_core/openapi.py` | py | utility | 1 | yes |
| `estorides_core/ops_observability.py` | py | utility | 10 | yes |
| `estorides_core/search_telemetry.py` | py | utility | 22 | yes |
| `estorides_core/web_security.py` | py | presentation | 22 | yes |

### `.` (5 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `app.py` | py | utility | 0 | yes |
| `estorides_web.py` | py | presentation | 95 | yes |
| `estorides_web_tools.py` | py | presentation | 5 | yes |
| `web.py` | py | utility | 0 | yes |
| `wsgi.py` | py | utility | 0 | yes |

### `tests/properties` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_csp_safe_styles_properties.py` | py | testing | 3 | yes |
| `tests/properties/test_search_telemetry_properties.py` | py | testing | 6 | yes |

### `tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/sync_docs.py` | py | utility | 2 | yes |

*... and 4 more files in this community.*


## Key Symbols

- `AuditEvent` (class, `estorides_core/audit.py:55`) `class AuditEvent`
- `to_jsonl` (method, `estorides_core/audit.py:68`) `def to_jsonl(self)`
- `AuditLog` (class, `estorides_core/audit.py:72`) `class AuditLog` - Append-only JSONL audit log with a size cap.
- `__init__` (method, `estorides_core/audit.py:90`) `def __init__(self, path)`
- `record` (method, `estorides_core/audit.py:104`) `def record(self, event)`
- `_maybe_rotate_locked` (method, `estorides_core/audit.py:115`) `def _maybe_rotate_locked(self)` - If the active file is over the cap, rotate in place.
- `query` (method, `estorides_core/audit.py:150`) `def query(self, event)`
- `RateLimiter` (class, `estorides_core/audit.py:180`) `class RateLimiter` - In-process sliding-window rate limiter.
- `__init__` (method, `estorides_core/audit.py:201`) `def __init__(self)`
- `allow` (method, `estorides_core/audit.py:214`) `def allow(self, key)` - Return (allowed, retry_after_seconds).
- `reset` (method, `estorides_core/audit.py:238`) `def reset(self, key)`
- `GraphRagConfig` (class, `estorides_core/graph_rag_search.py:53`) `class GraphRagConfig` - Presupuestos y pesos de retrieval (env `ESTORIDES_GRAPHRAG_*`).
- `graph_rag_config_from_env` (method, `estorides_core/graph_rag_search.py:75`) `def graph_rag_config_from_env()` - Construye la config desde env; malformada → defaults (nunca raise).
- `tokenize` (method, `estorides_core/graph_rag_search.py:98`) `def tokenize(text, min_len, stopwords)` - Parte en tokens minusculos; camelCase se divide y se conserva entero.
- `Bm25Index` (class, `estorides_core/graph_rag_search.py:112`) `class Bm25Index` - Okapi BM25 sobre un corpus fijo de listas de tokens.
- `__init__` (method, `estorides_core/graph_rag_search.py:115`) `def __init__(self, documents, k1, b)`
- `scores` (method, `estorides_core/graph_rag_search.py:136`) `def scores(self, query)` - Un score BM25 por documento, en orden de corpus.
- `_stochastic` (method, `estorides_core/graph_rag_search.py:153`) `def _stochastic(ids, edges)` - Filas estocasticas (indice, prob) + nodos dangling, orden determinista.
- `pagerank` (method, `estorides_core/graph_rag_search.py:176`) `def pagerank(ids, edges, alpha, max_iter, tolerance)` - PageRank dirigido y pesado; los scores suman 1 (determinista).
- `personalized_pagerank` (method, `estorides_core/graph_rag_search.py:207`) `def personalized_pagerank(ids, edges, seeds, alpha, max_iter, tolerance)` - PPR con teletransporte al seed; seeds ajenos se ignoran.
- `_md_safe` (method, `estorides_core/graph_rag_search.py:250`) `def _md_safe(text, limit)` - Gemelo de graph_force._md_safe: neutraliza markdown hostil.
- `RagEntity` (class, `estorides_core/graph_rag_search.py:260`) `class RagEntity`
- `RagRelation` (class, `estorides_core/graph_rag_search.py:271`) `class RagRelation`
- `RagTextUnit` (class, `estorides_core/graph_rag_search.py:281`) `class RagTextUnit`
- `RagCommunity` (class, `estorides_core/graph_rag_search.py:289`) `class RagCommunity`
- `RagContext` (class, `estorides_core/graph_rag_search.py:305`) `class RagContext`
- `GraphRagIndex` (class, `estorides_core/graph_rag_search.py:317`) `class GraphRagIndex`
- `to_dict` (method, `estorides_core/graph_rag_search.py:324`) `def to_dict(self)`
- `from_dict` (method, `estorides_core/graph_rag_search.py:334`) `def from_dict(cls, data)`
- `rows` (method, `estorides_core/graph_rag_search.py:335`) `def rows(name)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 39
- Cross-boundary resolved imports (EXTRACTED): 40

## Connections

- [EXTRACTED] depends_on community 4 <-> 1 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_web.py.
- [EXTRACTED] depends_on community 1 <-> 2 (strength 0.9): Extracted import edge crosses communities: estorides_core/audit.py imports estorides_core/config.py.

## Risks

- [cycle] `estorides_web.py` -> `estorides_web_tools.py` -> `estorides_web.py`
- [layer strict] `estorides_web.py` (presentation) -> `estorides_core/fusion_store.py` (data_access)
- [layer strict] `tests/properties/test_csp_safe_styles_properties.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_graph_rag_search.py` (testing) -> `estorides_web.py` (presentation)
- [layer strict] `tests/test_hardening.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_map_basemap.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_openapi.py` (testing) -> `estorides_web.py` (presentation)
- [layer strict] `tests/test_security_remediation.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_web_helpers.py` (testing) -> `estorides_core/web_security.py` (presentation)
- [layer strict] `tests/test_web_helpers.py` (testing) -> `estorides_web.py` (presentation)
- [layer strict] `tests/test_web_tools_blueprint.py` (testing) -> `estorides_web.py` (presentation)

## Open Questions

- Can the cycle `estorides_web.py` -> `estorides_web_tools.py` be broken with an interface?
- What would break if the most connected file in estorides_core: estorides_web changed?
- Should estorides_core: estorides_web be split, given cohesion 0.48?

## Sources

- `app.py`
- `estorides_core/audit.py`
- `estorides_core/graph_rag_search.py`
- `estorides_core/openapi.py`
- `estorides_core/ops_observability.py`
- `estorides_core/search_telemetry.py`
- `estorides_core/web_security.py`
- `estorides_web.py`
- `estorides_web_tools.py`
- `tests/properties/test_csp_safe_styles_properties.py`
- `tests/properties/test_search_telemetry_properties.py`
- `tests/test_audit_log.py`
- `tests/test_auth_gate.py`
- `tests/test_csp_safe_styles.py`
- `tests/test_graph_rag_search.py`
- `tests/test_map_basemap.py`
- `tests/test_openapi.py`
- `tests/test_ops_observability.py`
- `tests/test_search_telemetry.py`
- `tests/test_web_helpers.py`
- *... and 4 more*
