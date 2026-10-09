# graph_rag_search — GraphRAG local/global para la IA local

> Cerrado 2026-10-09. Cambios de cierre: pin top-1 al nombre exacto por
> construcción (el PPR puro premiaba al hub intermedio, S1 lo exige);
> `_pack` en dos pasadas con marcador `…truncated` + guarda de fence;
> S7 blindado con `filterwarnings(ignore::ResourceWarning)` (víctima del
> GC ajeno, ver abajo). Hallazgo de suite: `filterwarnings=error` +
> sqlite sin cerrar en tests viejos → `ResourceWarning` que el GC
> atribuye al test en curso; las víctimas rotan entre corridas
> (`central_config`, `openapi`, `web_tools_blueprint`, S7 antes del
> blindaje). No es regresión: con stash también hay 2 fallos. Suite
> final: 961 verdes + 2 pre-existentes. Env-pending: properties
> hypothesis + mutmut (venv sin ellos).

## Purpose

`graph_force.build_ai_context()` vuelca siempre el mismo contexto
estático (top por grado). La IA local (Ollama vía
`estorides_llm/manager.py`) merece contexto **rankeado por su pregunta**:
este módulo porta el `GraphRagSearcher` de ReadMenator
(`readmenator/_graphrag.py` + `_rank.py`: índice tipado, BM25, PageRank
global, Personalized PageRank, map-reduce global) al grafo OSINT de
Estorides (entidades, relaciones, comunidades por cluster, unidades de
texto). Sin llamadas a LLM: todo es extractivo y determinista. El
`api_analyze_stream` antepone el bloque al prompt, fail-soft.

## Inputs

- `nodes`: dicts con la forma de `/api/graph`
  (`id, label, type/kind, cluster, level`; opcional `detail: str` con
  texto extractivo extra por entidad, p. ej. fuentes).
- `edges`: dicts (`source, target, relation, inter_cluster?`).
- `clusters`: dicts (`id, label, color?, size?`); ausente → todo a
  comunidad `unassigned`.
- `query: str` (pregunta en lenguaje natural, hostil por defecto).
- `mode`: `auto` (elige), `local` o `global`.
- `budget_tokens` (default 1500): tope del contexto.
- `GraphRagConfig`: creada con `graph_rag_config_from_env()` (vars
  `ESTORIDES_GRAPHRAG_*` vía `envutil`; malformada → defaults, nunca
  crash). Nada hardcodeado fuera de los defaults documentados.

Casos vacíos: grafo vacío → índice vacío + búsqueda que responde
"no matches" sin raise; query vacía → modo global; edges huérfanos se
descartan (conteo en `meta`).

## Outputs

`estorides_core/graph_rag_search.py` (puro, sin I/O, sin networkx):

- `tokenize(text, min_len, stopwords) -> list[str]`: minúsculas,
  camelCase partido, el identificador completo se conserva.
- `Bm25Index(documents, k1, b)` + `scores(query) -> list[float]`
  (Okapi BM25, idéntica fórmula que ReadMenator).
- `pagerank(ids, edges, alpha, max_iter, tolerance) -> dict`: power
  iteration dirigido y pesado sobre `ids` ordenados (determinista);
  scores suman 1. `personalized_pagerank(ids, edges, seeds, ...)`
  con teletransporte al vector seed (seeds fuera del grafo se ignoran;
  suma 0 → uniforme).
- Pesos de relación: `resolves-to 1.0, same-as 1.0, contains 0.9,
  related-to 0.8, member_of 0.5, layered_as 0.4`; `EXTRACTED ×1.0`.
  El walk PPR usa expansión simétrica (cada edge aporta su reverso).
- `RagEntity/RagRelation/RagTextUnit/RagCommunity/RagContext/
  GraphRagIndex`: dataclasses con `to_dict/from_dict` (+
  `schema_version == 1` en `meta`).
- `build_index(nodes, edges, clusters=None, config=None)`:
  entidades (descripción extractiva kind/label/cluster/level/degree),
  relaciones (una por edge válido), text units (una por entidad con
  `detail` o línea extractiva), reportes `c<n>` por cluster +
  `root`. Rating 0-10 = `8 × PageRank-share + 2 × bridge-share`
  (fórmula en `rating_explanation`).
- `GraphRagSearcher(config, index)`: `choose_mode(query)`,
  `search(query, mode="auto", budget_tokens=0)`,
  `local_search` (BM25 seeds entidad+texto → PPR → top entidades,
  relaciones entre ellas, reportes por masa, text units) y
  `global_search` (BM25 sobre reportes → map de findings que casan
  con la query → reduce a overview + comunidades relevantes).
  Empaquetado por secciones con shares (como ReadMenator `_pack`).
  Dos garantías propias: el **nombre exacto** abre la lista top-1 por
  construcción (el PPR puro premiaría al hub intermedio); si el
  presupuesto recorta items, el markdown lo declara con
  `…truncated` (segunda pasada con guarda para el marcador + cierre
  de fence).
- `graph_context_block(query, nx_graph, cluster_of, budget_tokens,
  mode="auto")`: adapta un grafo networkx (duck-typing, sin importar
  nx) + mapa de comunidades al índice y devuelve el markdown listo
  para el prompt. Es el seam testeable del wire-up.
- `ask_context(query, nodes, edges, clusters, budget_tokens, mode)`:
  one-shot build + search.

Wire-up (`estorides_web.api_analyze_stream`, ~10 líneas, fail-soft):
lee `GRAPH_PATH` + `KnowledgeGraph.communities()`, antepone el bloque
al prompt. Sin grafo → prompt intacto. Sin rutas nuevas.

## Tabla de errores

| Condición | Comportamiento |
| --- | --- |
| grafo vacío | índice vacío; `search` local responde "No entity matches…", global responde overview vacío; sin raise |
| query vacía / sin tokens | `choose_mode` → `global` |
| query sin matches léxicos | `choose_mode` → `global` (igual que ReadMenator) |
| edge huérfano / nodo no-dict | descarte + `meta.dropped_edges`; nodo no-dict → `TypeError` |
| campo no JSON-safe (`set/bytes`) | `TypeError` fail-closed (igual que `graph_force`) |
| `budget_tokens <= 0` | `ValueError` |
| labels hostiles gigantes | truncados (`CONTEXT_LABEL_CHARS`, budget por líneas + `…truncated`) |
| `GRAPH_PATH` ausente en analyze | prompt sin bloque (fail-soft, log server-side) |

## Garantías de seguridad

- **Todo input es hostil**: query y labels pasan por `_md_safe`
  (fences/backticks neutralizados, `\r` fuera, colapso de espacios);
  el módulo no genera HTML; `json`-safe garantizado (`to_dict`
  serializa).
- Sin `eval`/Function/imports dinámicos; sin red; sin I/O (ni siquiera
  lee `GRAPH_PATH`: lo recibe ya cargado).
- Presupuesto duro: `len(markdown) <= budget_chars` siempre; tope
  global `MAX_BUDGET_CHARS`.
- `bandit` 0 High/Medium, `mypy --strict` limpio, `ruff` limpio.
- El wire-up nunca filtra excepciones al cliente (CWE-209: genérico
  al stream, detalle al log).

## Out of scope

- Reportes de nivel tema (Louvain sobre el grafo cociente de
  ReadMenator): aquí `root` + `c<n>`; los temas vuelven si algún
  análisis los pide.
- HITS/composite ranker (cobertura test/doc/freshness son señales de
  código, sin sentido OSINT).
- Persistencia del índice en disco (`GraphRagStore`): el grafo cabe
  en memoria (tope `limit` de `/api/graph`); se reconstruye por
  análisis.
- Cambiar `format_context`/`SYSTEM_PROMPT` o el manager LLM.
- Nuevas rutas REST; properties con hypothesis y mutmut (venv sin
  ellos: env-pending, igual que módulos anteriores).

## Escenarios BDD Given-When-Then

### S1 — happy path local: la entidad que casa lidera
Given: `a:label example.com (domain)`, `b:1.2.3.4 (ipv4)`,
  `c:admin@example.com (email)`, edges `a→b resolves-to`, `b→c`
  `related-to`
When: `search("example.com")` (modo auto)
Then: `mode=="local"`, top-1 es `a`, `relations` no vacío, el
  markdown trae `## Entities`, `## Relationships`,
  `## Community reports`, `## Sources`.

### S2 — happy path global: hints eligen map-reduce
Given: el mismo índice
When: `search("overview of everything")`
Then: `mode=="global"`, `reports` no vacío, el markdown trae
  `## Overview` y `## Relevant communities (map-reduce)`.

### S3 — edge: vacío no rompe
Given: `build_index([], [], [])`
When: `search("anything")` y `search("")`
Then: sin raise; local contiene "No entity matches"; `entities==[]`;
  `choose_mode("")=="global"`.

### S4 — seguridad: hostil falla cerrado y acotado
Given: nodo con `label=set`, otro con `bytes`; 10 nodos con labels
  de 5KB con ` ``` ` y `[x](javascript:…)`, budget 500 chars
When: `build_index` con los primeros; `search` con los segundos
Then: `TypeError` en el build; `len(markdown)<=500`, fences pares,
  aparece `…truncated`.

### S5 — matemáticas sanas y deterministas
Given: el grafo S1
When: `pagerank` + dos `search("example.com")` seguidos +
  `build_index` dos veces
Then: scores suman 1 (±1e-6); markdown byte-idéntico;
  `to_dict` byte-idéntico; PPR con seed `{a}` pone a `a` top-1.

### S6 — wire-up: bloque para el prompt desde un DiGraph
Given: un `nx.DiGraph` de 4 nodos con attrs `value/type` + mapa
  `cluster_of`
When: `graph_context_block("assess example.com", graph, cluster_of,
  budget_tokens=400)`
Then: devuelve str con `# GraphRAG` y `example.com`;
  `len<=1600`; con grafo vacío devuelve `""`.
