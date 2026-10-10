# graph_force3d — vista de grafo 2D/3D estilo ReadMenator + contexto IA

> Cerrado 2026-10-09. Cambios de cierre: puentes inter-cluster pineados
> antes del corte por `max_nodes` (S3 lo exige); `showNavInfo(false)` en
> 3D (el hint de three.js tapaba el HUD); `#gf-stage top:64px` +
> HUD/toast a 74px + leyenda D3 a 74px con toolbar visible (clase
> `gf-bar`); `drawGraphWithExtras` publica el merged en
> `window._graphData` para que el 3D vea expansiones del resolver.
> Boy-scout: `{{ s.keys }}` → `{{ s['keys'] }}` en `index.html`
> (imprimía el método `dict.keys`). Visual review headless con selenium:
> `.scratchpad/gf_2d.png`, `gf_3d.png`, `gf_3d_click.png` (HUD 16 nodes,
> highlight + inspector + transforms OK). Suite: 954 verdes + 2 fallos
> pre-existentes orden-dependientes (`test_central_config`,
> `test_openapi`, idénticos con stash).

## Purpose

La vista de grafo de Estorides (D3/SVG en `#graph-canvas`) se queda corta
frente al explorador `graph-force.html` de ReadMenator: sin modo 3D, sin
buscador de nodos, sin filtros por tipo, sin leyenda de comunidades
clicable, sin layouts (force/clusters/layers/tree), sin inspector
(passport del nodo), sin export PNG/JSON, sin HUD ni deep-links. Este
módulo porta el sistema de grafos de ReadMenator (`readmenator/
_forcegraph.py` + `graph-force.html`: 668 líneas, motor vasturiano
`force-graph` 2D vendored + `3d-force-graph` por CDN bajo demanda) a la
vista de grafo de Estorides, manteniendo la vista 2D existente como
fallback y añadiendo el botón **3D** igual que en ReadMenator. Además
expone la misma información del grafo como **contexto markdown con
presupuesto de tokens** para la capa de IA local (GraphRAG extractivo,
sin llamadas a LLM: entidades, relaciones, comunidades y fuentes).

Decisión de diseño: el motor `force-graph` (2D vendored offline + 3D CDN
on-demand) pasa a ser el renderer principal en ambos modos; el renderer
D3 (`renderGraphCore`) queda intacto como fallback legacy si el vendor
falta y no hay red (`engine-error`, mismo `fail()` de ReadMenator). Las
interacciones propias de Estorides (expand-on-click vía resolver,
context-menu de transforms, bridge tooltips, anillos de intel-tier) se
re-enganchan sobre el nuevo motor, no se pierden.

## Inputs

- `nodes`: lista de dicts con la forma que emite `/api/graph`
  (`id, label, type, kind, color, cluster, cluster_color, level, size`).
  Tipos OSINT abiertos (`domain, ipv4, email, person, company, cve,
  btc_address, ...`); `cluster` int (`-1` = sin comunidad); `level`
  (`data, information, intelligence, counter_intelligence`).
- `edges`: lista de dicts (`source, target, relation, inter_cluster?,
  clusters?`).
- `clusters`: lista de dicts (`id, size, color, label`).
- `max_nodes` (default 300), `max_edges` (default 1000): topes de
  render; la truncación es determinista (grado desc, puentes
  inter-cluster primero, desempate por `id`).
- `budget_chars` (default 12000): presupuesto del contexto IA.

Casos vacíos: `nodes=[]` → payload `{nodes:[], edges:[]}` + contexto con
mensaje "empty graph"; `edges` huérfanos (extremo ausente) se descartan;
campos ausentes usan defaults (`label=id, type="unknown", cluster=-1`).

## Outputs

`estorides_core/graph_force.py` (puro, sin I/O):

- `family_color_from_name(name, ...) -> str`: color HSL estable (djb2,
  mismos defaults que ReadMenator: sat 55+12, light 58+10).
- `node_value(symbols, degree, findings=0) -> float`: `max(1,
  log2(symbols+degree+findings+1))`.
- `build_force_payload(nodes, edges, clusters, max_nodes=300,
  max_edges=1000) -> dict`: `{nodes:[...], edges:[...]}` con forma RAW
  ReadMenator adaptada a OSINT:
  - entidad → `{id, label, type:"entity", kind, degree, findings:0,
    community, community_label, family, layer, color, rank, rank_pos,
    doc:""}` donde `family` = label del cluster o `kind`,
    `layer` = intel `level`, `color` = `cluster_color` o color de familia
    estable, `rank` = PageRank-por-grado normalizado (ver notas),
    `rank_pos` = posición 1-based por grado desc.
  - comunidad → `{id:"community:<n>", label, type:"community",
    community_id, size, color}` + edge `member_of`.
  - tier → `{id:"tier:<level>", label, type:"tier", color}` + edge
    `layered_as`.
  - edge OSINT → `{source, target, type:relation, weight:1, color}` con
    paleta `EDGE_COLORS` (mismos valores que ReadMenator renombrados a
    relaciones OSINT: `related-to, resolves-to, same-as, contains,
    member_of, layered_as`).
- `force_settings() -> dict`: mismos valores que `SETTINGS` de
  ReadMenator (`charge:-300, linkDistance:120, linkStrength:0.3,
  nodeRelSize:4, hulls:True, hullFill:0.07, hullStroke:0.5, hullPad:18,
  particles:4, dimNode, dimLink, labelTopN:30, labelZoom:1.6,
  labelMax:28, clusterStrength:0.6, collidePad:4, dagLevel:60, flyMs:700,
  flyZoom:3.0, searchResults:8`); fuente única para el JS (inyectado vía
  `/api/graph` como `settings`).
- `build_ai_context(nodes, edges, clusters, budget_chars=12000) -> dict`:
  `{markdown, approx_tokens, entities, relations, reports}`. Markdown
  extractivo con secciones `Entities` (top por grado, con kind/cluster/
  score), `Relationships` (puentes inter-cluster primero), `Communities`
  (una línea por cluster: tamaño, miembros top, densidad) y `Sources`
  (nota de procedencia: fusion_store). Truncado duro a `budget_chars`
  (corte por línea completa + marcador `…truncated`). Sin llamadas LLM,
  determinista.

Frontend (wire-up, verificado por tests CSP + `node --check` + visual
review, no por pytest):

- `static/js/vendor/force-graph.min.js`: copia byte-idéntica del vendor
  de ReadMenator (v1.52.0, MIT vasturiano, se conserva el header de
  licencia). `3d-force-graph` solo por CDN bajo demanda (igual que
  ReadMenator `CDN_3D`), fail-soft con toast sin red.
- Toolbar en `#graph-canvas` clonando `graph-force.html`: searchbox +
  resultados, seg `[2D|3D]`, seg layouts
  (Force/Clusters/Layers→Tiers/Tree), botones Names/Hulls/Flow/Freeze/
  Fit/3D/PNG/JSON/Theme→(sigue el tema Estorides, sin botón propio).
  El botón **3D** se comporta igual que en ReadMenator: si el motor 3D
  no está cargado lo carga del CDN y monta; si no hay red, toast y se
  queda en 2D.
- HUD (nodes/edges/highlighted/focus), leyenda (pills por tipo para
  mostrar/ocultar + comunidades clicables para enfocar), inspector
  (passport: métricas, reach 1-3 hops, isolate, vecinos agrupados por
  relación, deep-link `#node=<id>&layout=`), tooltip, PNG/JSON export,
  shortcuts (`/ Esc Backspace 1-4 L H I F Space`), `hidden` en
  overlays nuevos.
- CSS: valores idénticos a `graph-force.html`, con nombres re-escopados
  bajo `#graph-canvas.gf` (`--canvas`→`--gf-canvas`, `.topbar`→
  `.gf-toolbar`, etc.; tabla de mapeo en el código). Sin `style="…"`.
- Interacciones Estorides preservadas: click → `selectNode` + expand vía
  resolver; right-click → context-menu de transforms; doble-click →
  focus; links inter-cluster → bridge tooltip.

## Tabla de errores

| Condición | Código / comportamiento |
| --- | --- |
| `nodes` vacío | payload vacío + `summary {node_count:0,...}`; el frontend muestra "no graph yet", sin excepción |
| edge con extremo ausente del payload | se descarta en silencio (conteo en `meta.dropped_edges`) |
| truncación por `max_nodes/max_edges` | determinista: grado desc, puentes primero, desempate `id`; `meta.truncated=True` |
| vendor 2D ausente + CDN inalcanzable | `fail()` muestra `#engine-error`; fallback al renderer D3 legacy |
| CDN 3D inalcanzable (click 3D sin red) | toast "3D engine needs network access", se queda en 2D |
| input no JSON-safe (`set/bytes/objeto`) | `TypeError` con mensaje (fail-closed, nunca se serializa parcial) |
| strings hostiles gigantes (>10k chars) | truncados a límites (`labelMax 28` display, `LABEL_MAX_CHARS`, contexto a `budget_chars`) |
| `budget_chars <= 0` | `ValueError` |

## Garantías de seguridad

- **Todo input es hostil** (doctrina): labels/values remotos nunca tocan
  `innerHTML` sin escapar; el backend no genera HTML (solo JSON); el
  frontend construye DOM con `textContent`/`mkEl` y sanitiza tooltips con
  el DOMPurify vendored (`purifyHTML`); los labels dibujados en canvas
  no interpretan HTML.
- **CSP intacta**: cero `style="…"` en markup nuevo y en template
  literals JS (colores dinámicos por CSSOM `el.style.*`, como exige
  `spec/csp_safe_styles.md`); el `tip()` de ReadMenator con
  `<span style="color:…">` se porta como clase `.gf-warn`, no se copia
  el inline style. CSP `script-src` ya permite `cdn.jsdelivr.net` (3D)
  y `'self'` (vendor 2D).
- **Sin `eval`/Function**: el vendor es código estático auditado
  (misma copia que ReadMenator); la carga CDN 3D usa `<script src>`
  con URL constante (no construida con input).
- **Límites**: `MAX_LABEL 512`, `MAX_NODES 2000`, `MAX_BUDGET 200000`
  chars; `budget_chars` acota el contexto IA (sin blowup de prompt
  para el LLM local).
- `bandit` 0 High/Medium, `mypy --strict` limpio, `ruff` limpio.

## Out of scope

- Búsqueda BM25 + Personalized PageRank + map-reduce global (el
  `GraphRagSearcher` completo de ReadMenator): módulo de seguimiento
  `graph_rag_search`; aquí solo el contexto extractivo con presupuesto.
- Reemplazar el mapa Leaflet o el timeline.
- Motores alternativos (vis-network, sigma, Cytoscape).
- Vendorizar `3d-force-graph` (pesa ~MBs con three.js; CDN bajo demanda
  como en ReadMenator).
- re-scoring de `reliability_scoring` / fusión (solo lectura del grafo).
- Nuevos endpoints REST (el payload viaja dentro de `/api/graph` como
  campos `force` + `settings`; sin rutas nuevas).

## Escenarios BDD Given-When-Then

### S1 — happy path: payload OSINT con forma RAW
Given: 3 nodos (`a:domain` cluster 0, `b:ipv4` cluster 0, `c:email`
  cluster 1) y 2 edges (`a→b resolves-to`, `b→c related-to`
  inter-cluster)
When: `build_force_payload(nodes, edges, clusters)`
Then: devuelve 3 entidades + 2 nodos comunidad + 2 nodos tier; los edges
  incluyen los 2 OSINT + `member_of`/`layered_as`; `a` y `b` comparten
  `family`; grados `a=1 b=2 c=1`; `rank_pos` de `b` es 1.

### S2 — edge: grafo vacío
Given: `nodes=[]`, `edges=[]`, `clusters=[]`
When: `build_force_payload` + `build_ai_context`
Then: payload `{nodes:[], edges:[], meta:{node_count:0,…}}` sin raise;
  el contexto markdown contiene "empty graph" y `entities==[]`.

### S3 — error: truncación determinista con puentes primero
Given: 10 nodos en línea + 1 puente inter-cluster al final, con
  `max_nodes=5, max_edges=4`
When: `build_force_payload` dos veces
Then: ambas salidas son byte-idénticas; `meta.truncated` es True; el
  puente sobrevive al corte aunque sus extremos tengan grado bajo.

### S4 — seguridad: input no JSON-safe falla cerrado
Given: un nodo cuyo `label` es un `set` y otro con `bytes`
When: `build_force_payload`
Then: raise `TypeError` (nunca devuelve payload parcial serializable a
  medias); `json.dumps` del resultado de un payload válido funciona.

### S5 — seguridad: contexto IA acotado y sin inyección de markdown
Given: labels con ` ``` `, `[link](javascript:…)`, `# header` y 50KB de
  texto, `budget_chars=500`
When: `build_ai_context`
Then: `len(markdown) <= 500`; no hay fences sin cerrar (conteo de
  ` ``` ` par); el marcador `…truncated` aparece; `approx_tokens > 0`.

### S6 — determinismo de colores y settings
Given: el mismo `family` dos veces + `force_settings()`
When: se colorea y se leen settings
Then: mismo HSL las dos veces, formato `hsl(<0-360>, <55-67>%,
  <58-68>%)`; settings contiene las 19 claves con los valores
  ReadMenator (`charge==-300`, `linkDistance==120`, `particles==4`…).

## Amendment 2026-10-10 — exclusive render, pointer alignment, matte 3D, exploration actions

Inspired by the CAIRN Explorer (`Cisco-Talos/Cognitive-Artifact-Intelligence-Research-Network`,
`cairn/explorer_ui.py`): separate 2D/3D ownership of one canvas, type-colour
palette on a dark radial field, family pills, detail panel on click,
bridge-edge inspection, physics reheat.

### S7 — exclusive render (no 2D/3D overlap)
Given: the 3D engine owns `#graph-canvas` (`GF.state.engine === '3d'`)
When: a resolver expansion or transform merges new nodes
  (`drawGraphWithExtras` in `estorides.js`)
Then: only `window._graphData` is updated; `renderGraphCore` is NOT called
  (the `graph_force.js` sync loop reloads the 3D scene). Any D3 SVG
  repainted while 3D is active carries the `gf-hide` class. Leaving 3D
  (`to2D`) hides `#gf-stage` and pauses the WebGL loop
  (`pauseAnimation`); entering 3D hides every direct-child D3 `svg` and
  resumes the loop. Exactly one engine paints at any time.

### S8 — pointer alignment in 2D and 3D
Given: the GF toolbar occupies the top of `#graph-canvas`
When: either engine sizes its viewport
Then: the 2D SVG is sized to `container - toolbarHeight` and flows below
  the toolbar (no overflow offset); the 3D renderer is sized from the
  `#gf-stage` box, never from the full canvas. `#graph-canvas.gf-bar`
  is a flex column (`toolbar / stage-or-svg`), so no magic `top: 64px`
  offset exists. Node picking matches the marker under the cursor.

### S9 — matte data-point styling (not atoms, not planets)
Given: the 3D scene renders entities, communities and tiers
When: the operator looks at the 3D view
Then: nodes are small faceted matte markers (`nodeRelSize 3`,
  `nodeResolution 10`, `nodeOpacity 0.95`) on a dark radial field
  (`ellipse at 60% 40%, #111420 to #030a1c`, same as CAIRN `#graph-wrap`);
  links are thin (`0.5`, opacity `0.5`); flow particles appear only on
  highlighted edges. No glow sprites, no large translucent orbs.

### S10 — node actions (select-only click)
Given: a node is visible in 3D
When: single click / double click / Alt+click / right-click / Enter / F / C
Then: single click selects + inspects only (never mutates the graph);
  double click (second click < 350 ms), Enter key, or the Expand button
  pivots through the resolver; Alt+click or right-click opens the
  transforms context menu; F centers and zooms on the selection; C copies
  a deep link (`#node=<id>&layout=`); hover highlights the 1-hop
  neighbourhood only when nothing is selected. Tooltip reads
  "click to inspect, double-click to expand".

### S11 — edge actions + exploration toolbar
Given: edges are visible in 3D
When: the operator clicks an edge or uses the toolbar
Then: clicking a bridge edge opens the cross-reference tooltip;
  clicking a plain edge reports `source --relation--> target`; hovering an
  edge shows a pointer cursor. Toolbar (all English, no emojis): Reheat
  (restart physics, key R), Bridges (bridge-edges-only filter, key B,
  works in 2D and 3D, shown in the HUD), Expand (Enter), Focus (F),
  Link (copy deep link, key C). Existing controls keep working
  (search, layouts, Names, Hulls, Flow, Freeze, Fit, PNG, JSON, reach
  1-3, Isolate with key I).
