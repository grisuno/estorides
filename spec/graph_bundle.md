# graph_bundle — pestaña Bundles: vista circular 2D + vista esférica 3D estilo ReadMenator

> **Cerrado 2026-10-10.** Cambios de cierre: `groupGap`/`innerRatio`
> camelCase (consistencia con el resto de settings); keydown a eval-time
> (el listener de Bundles se registra antes que el de Graph y frena
> 2/3/c/x/r/[/]/ con `stopImmediatePropagation` solo con el tab activo,
> Escape propaga); layout vertical stage-arriba/panel-abajo (el sidebar es
> demasiado estrecho para side-by-side — hallazgo del visual review);
> `test_s6` a archivo propio (el sandbox `mutants/` no copia
> templates/static). Cierre: 29 tests BDD (S1-S10) + 1 assets + 4
> properties (4000 ex. fuzzing) verdes; ruff/mypy-strict/bandit limpios;
> **mutmut 1190/1229 muertos, 39 equivalentes justificados abajo**;
> visual review selenium (`.scratchpad/gb_circle.png`, `gb_sphere.png`:
> 300 nodos, 10 grupos, HUD/leyenda/panel OK); suite 990 verdes + 3
> fallos pre-existentes rotativos (idéntico set con stash).
>
> ## Amendment 2026-10-10 (round 2) — la vista vive en el canvas derecho
>
> El operador la quiere en el lado derecho (canvas principal), no en el
> sidebar: el bloque `#tab-bundles` se mueve a `#bundles-canvas`
> (`.canvas-tab[data-canvas="bundles"]` tras Graph, panel en
> `.canvas-body`). El JS escucha clicks de ese canvas-tab y activa con
> `#bundles-canvas.active` (teclas igual de acotadas). Backend y algoritmos
> intactos; solo cambia el contenedor. Hallazgo de la suite: el leak
> sqlite pre-existente (`filterwarnings=error`) convirtio a
> `test_s7_sphere_caps_hubs_and_fibonacci` en victima del GC — blindaje
> `ignore::ResourceWarning` a nivel modulo en los 3 archivos de tests
> (precedente: `graph_rag_search` S7; estos tests no abren DBs).
> Origen: `ReadMenator/readmenator/_bundlegraph.py` (301 líneas) +
> `readmenator/_graphlayout.py` (hierarchical/spherical edge bundling, Holten 2006) +
> `readmenator/_bundlegraph_page.py` (template 632 líneas, canvas self-contained sin CDN) +
> `readmenator-maps/graph-bundle.html` (617 líneas generadas).
> En Estorides vive al lado de `spec/graph_force3d.md`: reutiliza su payload RAW,
> no lo duplica. Frontend offline (canvas 2D puro con proyección perspectiva
> propia para la esfera): cero CDN, cero three.js en esta pestaña.

## Purpose

La vista Graph actual (force 2D + 3D con three.js por CDN) no muestra las
costuras entre comunidades: cientos de aristas rectas se tapan entre sí.
El explorador `graph-bundle.html` de ReadMenator resuelve eso con
*hierarchical edge bundling*: cada entidad vive en el borde (arco circular
2D / casquete esférico 3D) agrupada por comunidad, y cada arista se rutea
por la jerarquía (hoja → hub de comunidad → raíz → hub destino → hoja)
como B-spline cuyo `beta` se ajusta en vivo. Los haces gruesos son las
costuras reales entre subsistemas (en Estorides: entre clusters de intel).
Este módulo porta ese explorador a una **vista Bundles en el canvas
principal (derecha), pestaña canvas junto a Map/Graph/Timeline**, con los
mismos estilos oscuros (tokens, topbar, HUD,
leyenda, panel inspector, intro) re-escopados bajo `#bundles-canvas`, y el
mismo comportamiento (buscar, colorear por comunidad/layer/kind, dirección
in/out/both, crossing-only, rotate, reset, PNG, theme, teclas `2/3/C/X/R`).

## Inputs

- `force_payload`: dict con la forma que emite
  `estorides_core/graph_force.build_force_payload` (`{nodes:[...],
  edges:[...], meta:{...}}`), que a su vez viaja dentro de `/api/graph`
  como campo `force`. Nodos esperados:
  - entidad: `{id, label, type:"entity", kind, degree, findings, community,
    community_label, family, layer, color, rank, rank_pos, val, doc}`.
  - comunidad: `{id:"community:<n>", label, type:"community", ...}`.
  - tier: `{id:"tier:<level>", ...}` (se ignora en el bundle).
- `settings` opcionales vía `bundle_settings()` (centralizados en
  `estorides_core/config.py` con `envutil`, mismos defaults que
  `readmenator/_config.py`): `mode, beta=0.85, samples=20, innerRatio=0.55,
  groupGap=0.04, edgeAlpha=0.30, dimAlpha=0.035, labelAllMax=140,
  labelTopN=24, labelMax=26, nodeMin=2.0, nodeMax=7.0,
  hitPx=9.0, rotateSpeed=0.12, perspective=3.0, depthFade=0.7,
  particles=3, revealMs=1400, flowTopN=8, listMax=40`.

Casos vacíos: `nodes=[]` → payload `{nodes:[], groups:[], edges:[]}`;
entidades sin comunidad forman grupo trailing `unassigned`; aristas con
extremo ausente, self-loops y aristas de scaffolding (`member_of`,
`layered_as`) se descartan en silencio.

## Outputs

`estorides_core/graph_bundle.py` (puro, sin I/O, sin numpy):

- `build_bundle_payload(force_payload) -> dict` con **la misma forma** que
  `BundleGraphRenderer.build_payload` para que el JS porteado sea casi
  verbatim:
  - `nodes`: `[{id, f (file/label corto), l (label), g (índice de grupo),
    c (color), ly (layer/nivel intel), lg (kind como "lenguaje"),
    r (rank), rp (rank_pos), fd (findings), d (doc),
    a (ángulo en el círculo, rad), p ([x,y,z] en la esfera radio 1)}]`.
  - `groups`: `[{k (key `community:<n>`), l (nombre), c (color), n (count),
    a0, a1 (arco), h2 ([x,y] hub círculo), h3 ([x,y,z] hub esfera),
    u ([x,y,z] centro del cap)}]`. Orden: comunidades por id asc,
    `unassigned` al final; dentro del grupo por `rank` desc (hubs al
    centro del arco/cap).
  - `edges`: `[[i,j]]` índices a `nodes`; solo aristas entidad→entidad con
    `type` fuera de `{"member_of","layered_as"}`, pares dirigidos
    distintos, ordenados.
- `bundle_settings() -> dict`: mismos 22 campos ReadMenator (ver Inputs),
  más `groupColors` derivado del force payload (por layer/kind) y
  `unassignedKey="unassigned"`. Fuente única para el JS (inyectado vía
  `/api/graph` como `bundle_settings`).
- Layout math porteado de `_graphlayout.py` (determinista, sin aleatorio):
  `hierarchical_edge_bundling`, `spherical_edge_bundling`,
  `fibonacci_sphere`, `_bspline`, `_bundle_curves`, `_split_caps`
  (visibles para tests; el bytecode del algoritmo no cambia, solo los
  nombres de tipos: files→entities, language→kind).

Frontend (wire-up, verificado por CSP + `node --check` + visual review
headless, no por pytest):

- `templates/index.html`: nuevo `<button class="canvas-tab"
  data-canvas="bundles">Bundles</button>` tras Graph + `<div
  id="bundles-canvas" class="bundles-canvas">` en `.canvas-body` con toolbar
  (searchbox, seg `[Circle 2D|Sphere 3D]`, seg color
  `[Community|Layer|Kind]`, seg dir `[Both|Imports|Imported by]`, slider
  beta, botones Crossing/Rotate/Reset/PNG), `<canvas id="gb-c">`, HUD,
  leyenda, panel inspector. Sin `style="…"`, sin `onclick`.
- `static/js/graph_bundle.js`: port de `graph-bundle.html` (misma
  arquitectura: un canvas, cámara perspectiva para la esfera, beta
  recomputado en vivo, search, HUD, leyenda clicable, panel con vecinos
  in/out, PNG, theme que sigue al de Estorides, teclas `2/3/C/X/R`,
  deep-link `#bundle=<id>&view=`). Textos en inglés como el original.
  Nodos/entidades OSINT: `f` = label corto, tooltip `label · kind ·
  cluster · degree`, panel con métricas (degree, rank, findings=0,
  cluster, level) y vecinos agrupados por relación.
- CSS: tokens y reglas idénticas a `BUNDLEGRAPH_PAGE_TEMPLATE`
  (`--canvas, --stage, --mask, --ink, --accent, --glow, --sphere`,
  `.topbar→.gb-toolbar`, `#stage→#gb-stage`, `#hud→#gb-hud`,
  `#legend→#gb-legend`, `#panel→#gb-panel`, `#tip→#gb-tip`), re-escopados
  bajo `#bundles-canvas`. Sin inline styles dinámicos (colores por CSSOM
  `el.style.*` como exige `spec/csp_safe_styles.md`).
- `/api/graph` añade `bundle` + `bundle_settings` fail-soft (try/except →
  `None,None`; el formato legacy nunca se rompe). **Sin rutas nuevas.**

## Tabla de errores

| Condición | Código / comportamiento |
| --- | --- |
| `force_payload` vacío / sin entidades | `{nodes:[],groups:[],edges:[]}` sin raise; la pestaña muestra intro + "no bundles yet" |
| arista con extremo ausente / self-loop / tipo scaffolding | se descarta en silencio |
| nodo no-dict / `id` no-string | `TypeError` fail-closed (nunca payload parcial) |
| campo `label/color/kind/layer` no-string | default (`label=id`, color fallback familia, `unknown`/`data`), no mata el grafo |
| `rank`/`rank_pos` basura | `0.0` / `0` |
| strings gigantes (>512 chars) | truncados a `MAX_LABEL_CHARS=512` (display a `label_max_chars=26`) |
| vendor/JS ausente | la pestaña muestra fallback con enlace a Graph; `/api/graph` legacy intacto |
| `/api/graph` sin `force` (fallo upstream) | `bundle=None`; el frontend reusa `nodes/edges/clusters` legacy si puede, si no muestra vacío |

## Garantías de seguridad

- **Todo input es hostil** (doctrina): labels remotos nunca tocan
  `innerHTML`; backend solo emite JSON (`_json-safe` validado como en
  `graph_force`: `TypeError` ante `set/bytes/objeto`); frontend construye
  DOM con `textContent`/`mkEl` y tooltip/panel pasan por DOMPurify
  vendored; en canvas solo `fillText` (no interpreta HTML).
- **CSP intacta**: cero `style="…"` en markup y en template literals JS;
  colores dinámicos por CSSOM; sin `eval/Function`; sin CDN (bundle 100%
  offline, a diferencia del 3D de Graph).
- **Límites**: `MAX_LABEL_CHARS=512`, `MAX_NODES=2000` (heredado del force
  payload), `COORD_DIGITS=5`; el `beta` del slider se clamp a `[0,1]`.
- `bandit` 0 High/Medium, `mypy --strict` limpio, `ruff` limpio.

## Out of scope

- Layouts force/cluster/radial/dag/árbol en la vista Graph existente
  (módulo de seguimiento `graph_layouts`; aquí solo el bundle).
- ForceAtlas2 animado / video cinemático (`_graphlayout.forceatlas2_frames`,
  `fit_frames`): no se porta.
- `thumbnail_svg` (preview para galería de mapas): no hay galería en
  Estorides; fuera.
- Vendorizar three.js o cambiar el 3D actual: la esfera del bundle es
  proyección propia en canvas 2D, no WebGL.
- Nuevos endpoints REST (el bundle viaja dentro de `/api/graph`).
- Re-scoring de `reliability_scoring` / fusión (solo lectura).

## Escenarios BDD Given-When-Then

### S1 — happy path: payload OSINT con dos comunidades
Given: force payload con 3 entidades (`a` cluster 0, `b` cluster 0,
  `c` cluster 1) y aristas `a→b resolves-to`, `b→c related-to`
When: `build_bundle_payload(force)`
Then: `groups` tiene 2 entradas (`community:0` con `n=2` antes que
  `community:1` con `n=1`); `nodes` tiene 3 con `g` apuntando a su grupo,
  `a` ángulo válido y `p` vector unitario; `edges` tiene 2 pares `[[0,1],
  [1,2]]` (índices por `id` ordenado); el `rank` alto queda primero de su
  grupo.

### S2 — edge: grafo vacío y nodos sin comunidad
Given: `{"nodes":[],"edges":[]}` y otro payload con 2 entidades sin
  `community`
When: `build_bundle_payload` en ambos
Then: el primero devuelve `{nodes:[],groups:[],edges:[]}` sin raise; el
  segundo devuelve 1 grupo `unassigned` con `n=2` al final.

### S3 — error: scaffolding y aristas rotas se descartan, input roto falla cerrado
Given: force payload con aristas `member_of`, `layered_as`, una huérfana,
  un self-loop y un nodo con `label`=`set`
When: `build_bundle_payload`
Then: `edges` solo contiene la arista de relación válida; con el nodo
  roto raise `TypeError` (nunca devuelve payload parcial).

### S4 — seguridad: labels hostiles truncados y JSON-safe
Given: entidad con label de 5KB con `` ``` ``, `[x](javascript:…)`,
  `# header` y un nodo con `bytes`
When: `build_bundle_payload` + `json.dumps` del resultado válido
Then: el label sale truncado a `<=512` chars sin fences ejecutables en el
  payload; el nodo con `bytes` hace raise `TypeError`; `json.dumps` del
  payload válido funciona.

### S5 — determinismo círculo+esfera
Given: el mismo force payload dos veces
When: `build_bundle_payload` dos veces
Then: salidas byte-idénticas (mismos `a`, `p`, `a0/a1`, `h2/h3/u`
  redondeados a 5 decimales); `p` y `u` son unitarios (norma ≈1);
  `bundle_settings()` trae `beta==0.85`, `samples==20`,
  `innerRatio==0.55`, `mode=="2d"`.

### S6 — frontend: vista Bundles en el canvas derecho, offline, sin CSP violations
Given: la app servida con el spec implementado
When: se abre la pestaña canvas `Bundles`, se pulsa `Circle 2D` y `Sphere 3D`, se mueve
  beta, se busca un nodo
Then: el canvas-tab existe tras Graph en el canvas principal (derecha); ambas vistas pintan en el
  mismo canvas sin recargar ni pedir red (sin `<script src>` nuevo, sin
  fetch extra fuera de `/api/graph`); `grep style="…" templates/index.html`
  y `static/js/graph_bundle.js` vacío; tooltip/panel usan DOMPurify;
  `node --check` OK; visual review headless (PDF→PNG) legible.

## Mutantes equivalentes (cierre mutmut 1190/1229)

`mutmut run` sobre `estorides_core/graph_bundle.py` con
`tests/test_graph_bundle.py`: **1190 muertos, 0 timeouts, 39
supervivientes justificados** (verificados a mano: cada mutante aplicado
al arbol deja la suite en verde porque no cambia ningun observable).
Ninguno se deja por vagancia: todos caen en una de estas clases, y cada
uno se cita por id:

- **Default de `.get()` muerto por su propio guard** (8): el `None`-check
  posterior hace irrelevante el default del `.get`. `x__req_str__mutmut_3/5`,
  `x__opt_str__mutmut_3/5`, `x__opt_int__mutmut_3/5`,
  `x__opt_float__mutmut_3/5` (verificado a mano el patron en `_req_str`).
- **Default `None` tragado por `or`/`if not` falsy** (6): el valor solo
  alimenta un `X or fallback` / `if not X`, donde `None` y `""` colapsan
  al mismo fallback. `x_build_bundle_payload__mutmut_109/126/137/234`
  (color/kind/layer/community_label/family de entidad), `__326/__328`
  (default del `comm_color.get`).
- **Init reescrito antes de leerse** (4): `x_build_bundle_payload__mutmut_319/320`
  (`color = ""` del loop de grupos, siempre reescrito por el `.get` o por
  la rama unassigned), `__339/__340` (rama `except ValueError` muerta:
  `label` se construye como `f"community:{cid}"` con `cid` int, `int()` no
  puede fallar).
- **Guard unreachable o tragado** (4): `__196` (`and` en el filtro del loop
  de comunidades: el loop de entidades hace `raise` antes con no-dict, y
  con dicts el fall-through llega al mismo `continue` del guard de `id`);
  `__207/__209/__212` (defaults del `raw.get("id")`: presente → igual,
  ausente → el mismo `continue`).
- **Layout con output independiente** (5): `__294` (`inner_ratio` del
  circulo: `circle.hubs` no se emite, el `h2` del payload se recomputa del
  local), `__295/__296/__297` (centro/radio del circulo: el payload solo
  emite angulos/arcos), `__305` (radio omitido = default 1.0 = valor
  hardcodeado), `x_hierarchical_edge_bundling__mutmut_2` /
  `x_spherical_edge_bundling__mutmut_3` (`samples` 24→25: `per =
  max(2, samples//segments)` da identico para los unicos conteos de
  segmentos alcanzables — 2, 4 y 6 — via `_bundle_curves`; el poligono de
  4 puntos que los distinguiría no se construye nunca).
- **Rama defensiva muerta** (3): `x__bspline__mutmut_7` (`control[+1]` en la
  rama <3 puntos: solo se alcanza con exactamente 2 puntos, donde
  `[1] == [-1]`), `x__bspline__mutmut_39` (`max(2,·)`: la rama principal
  siempre tiene ≥2 segmentos), `x_fibonacci_sphere__mutmut_1` (`<0`:
  `count == 0` devuelve `[]` por ambas vias).
- **Claves construidas, split unico** (3): `__333/__334/__336` (`label` es
  `f"community:{cid}"` con un solo `":"`; variantes de split/rsplit
  devuelven lo mismo).
- **strict= con longitudes siempre iguales** (3):
  `x_spherical_edge_bundling__mutmut_58/61/62` (`_split_caps` reparte
  exactamente `len(groups[label])` puntos por grupo; el `strict=True` es
  documentacion ejecutable, exigido por ruff B905).
- **Init de corte siempre reescrito** (1): `x__split_caps__mutmut_8`
  (`cut = 1` inicial: la primera iteracion `i=1` cumple `gap < total`
  siempre — `0 < sizes < total` — y lo reescribe).
