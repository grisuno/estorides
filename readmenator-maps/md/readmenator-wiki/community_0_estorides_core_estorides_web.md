# estorides_core: estorides_web

*Community 0 | 26 files | cohesion 0.51*

## Definition

This community groups 26 file(s) rooted at `tests` with dominant language py (cohesion 0.51). Central symbols: `AuditEvent`, `AuditLog`, `AuthGate`, `Bm25Index`, `GraphRagConfig`, `GraphRagIndex`, `GraphRagSearcher`, `InvalidTelemetryConfigError`. Core file: `estorides_web.py` (95 symbols). Documented purpose: Deprecated entry point. Use:  - the `estorides` console script (installed by `pip install -e .`), or - `python3 estorides_cli.py serve` for the dev server, or -.

## Files

### `tests` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/test_audit_log.py` | py | testing | 5 | yes |
| `tests/test_auth_gate.py` | py | testing | 10 | yes |
| `tests/test_csp_safe_styles.py` | py | testing | 11 | yes |
| `tests/test_graph_force3d.py` | py | testing | 9 | yes |
| `tests/test_graph_rag_search.py` | py | testing | 11 | yes |
| `tests/test_map_basemap.py` | py | testing | 5 | yes |

### `estorides_core` (7 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/audit.py` | py | utility | 11 | yes |
| `estorides_core/graph_force.py` | py | utility | 12 | yes |
| `estorides_core/graph_rag_search.py` | py | utility | 44 | yes |
| `estorides_core/openapi.py` | py | utility | 1 | yes |
| `estorides_core/ops_observability.py` | py | utility | 10 | yes |
| `estorides_core/search_telemetry.py` | py | utility | 22 | yes |

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

*... and 6 more files in this community.*


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
- `family_color_from_name` (function, `estorides_core/graph_force.py:48`) `def family_color_from_name(name, sat_base, sat_span, light_base, light_span)` - Deriva un color HSL estable desde un label (djb2, como ReadMenator).
- `node_value` (function, `estorides_core/graph_force.py:65`) `def node_value(symbols, degree, findings)` - Escala log2 del tamano de nodo (minimo 1).
- `force_settings` (function, `estorides_core/graph_force.py:70`) `def force_settings()` - Valores SETTINGS de ReadMenator graph-force.html (fuente unica).
- `_req_str` (function, `estorides_core/graph_force.py:97`) `def _req_str(item, key, default, what)` - Lee un campo string obligatorio; fail-closed ante no-str.
- `_opt_str` (function, `estorides_core/graph_force.py:107`) `def _opt_str(item, key, default)` - Lee un campo de estilo; ante no-str usa el default (no mata el grafo).
- `_opt_int` (function, `estorides_core/graph_force.py:113`) `def _opt_int(item, key, default)` - Lee un campo entero; ante basura usa el default.
- `_degrees` (function, `estorides_core/graph_force.py:124`) `def _degrees(node_ids, edges)` - Grado por nodo + edges validos (ambos extremos conocidos).
- `_is_bridge` (function, `estorides_core/graph_force.py:150`) `def _is_bridge(edge)` - Un edge es puente si lo declara o si une clusters distintos.
- `build_force_payload` (function, `estorides_core/graph_force.py:161`) `def build_force_payload(nodes, edges, clusters, max_nodes, max_edges)` - Convierte nodos/edges OSINT (`/api/graph`) al formato RAW force-graph.
- `_md_safe` (function, `estorides_core/graph_force.py:332`) `def _md_safe(text, limit)` - Neutraliza un string remoto para embeberlo en markdown extractivo.
- `_truncate_lines` (function, `estorides_core/graph_force.py:341`) `def _truncate_lines(markdown, budget)` - Corte duro por linea completa + marcador (fences nunca se emiten).
- `build_ai_context` (function, `estorides_core/graph_force.py:353`) `def build_ai_context(nodes, edges, clusters, budget_chars)` - Contexto markdown extractivo con presupuesto para la IA local.
- `GraphRagConfig` (class, `estorides_core/graph_rag_search.py:53`) `class GraphRagConfig` - Presupuestos y pesos de retrieval (env `ESTORIDES_GRAPHRAG_*`).
- `graph_rag_config_from_env` (method, `estorides_core/graph_rag_search.py:75`) `def graph_rag_config_from_env()` - Construye la config desde env; malformada → defaults (nunca raise).
- `tokenize` (method, `estorides_core/graph_rag_search.py:98`) `def tokenize(text, min_len, stopwords)` - Parte en tokens minusculos; camelCase se divide y se conserva entero.
- `Bm25Index` (class, `estorides_core/graph_rag_search.py:112`) `class Bm25Index` - Okapi BM25 sobre un corpus fijo de listas de tokens.
- `__init__` (method, `estorides_core/graph_rag_search.py:115`) `def __init__(self, documents, k1, b)`
- `scores` (method, `estorides_core/graph_rag_search.py:136`) `def scores(self, query)` - Un score BM25 por documento, en orden de corpus.
- `_stochastic` (method, `estorides_core/graph_rag_search.py:153`) `def _stochastic(ids, edges)` - Filas estocasticas (indice, prob) + nodos dangling, orden determinista.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 41
- Cross-boundary resolved imports (EXTRACTED): 38

## Connections

- [EXTRACTED] depends_on community 2 <-> 0 (strength 0.9): Extracted import edge crosses communities: estorides_cli.py imports estorides_web.py.
- [EXTRACTED] depends_on community 0 <-> 3 (strength 0.9): Extracted import edge crosses communities: estorides_core/audit.py imports estorides_core/config.py.

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
- Should estorides_core: estorides_web be split, given cohesion 0.51?

## Sources

- `app.py`
- `estorides_core/audit.py`
- `estorides_core/graph_force.py`
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
- `tests/test_graph_force3d.py`
- `tests/test_graph_rag_search.py`
- `tests/test_map_basemap.py`
- `tests/test_openapi.py`
- `tests/test_ops_observability.py`
- *... and 6 more*
