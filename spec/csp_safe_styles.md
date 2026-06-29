# `csp_safe_styles` — Spec (Módulo 2d)

> Cierra el regression introducido por el commit `45c3af5` ("use unsafe-hashes
> for style-src"): la nueva CSP bloquea los inline styles que el frontend
> aún emite. El fix correcto NO es agregar hashes ni volver a
> `'unsafe-inline'`: es **eliminar todo `style="..."`** del template y del
> JS, moviendo los estilos a CSS classes o a asignación de propiedades
> CSSOM (que CSP no restringe).

---

## Purpose

El commit `45c3af5` cambió `style-src` de `'self' 'unsafe-inline' 'unsafe-hashes'`
a `'self' 'unsafe-hashes' https://unpkg.com`. La intención era cerrar el
vector CSS-injection (bloquear `<style>...</style>` arbitrario). Pero el
frontend — tanto el template Jinja como el JS — sigue emitiendo
`style="..."` (en atributos HTML de `<div>`/`<span>`/`<button>`/`<h4>` y en
template literals de JS). El browser ahora bloquea esos estilos con:

```
Applying inline style violates the following Content Security Policy
directive 'style-src 'self' 'unsafe-hashes' https://unpkg.com'. Either the
'unsafe-inline' keyword, a hash ('sha256-...'), or a nonce ('nonce-...')
is required to enable inline execution. The action has been blocked.
```

Los cuatro hashes únicos que el browser reporta (uno por valor de estilo
distinto) son los de estos strings exactos en `templates/index.html`:

| hash (sha256-…) | valor del style |
| --- | --- |
| `aqNNdDLnnrDOnTNdkJpYlAxKVJtLt9CtFLklmInuUAE=` | `display:none` |
| `ln6mO1ws+orx5dTCWpC63YQAsILO1+L5xOD6D8xqaLA=` | `padding:0 6px;font-size:10px` |
| `/ycNsz0hurrQPddmeQbeE9CNJOUYr1fe8mzaLjW9fSc=` | `margin-top: 14px;` |
| `Duf2atnAuKYQJLP8weHjB4u7h1/rXqGctpxZ7QK2sds=` | `margin-top:12px` |

**No alcanza con agregar hashes al CSP**: el JS también usa
`style="background:${cs}"` con valores dinámicos (uno por cluster). Esos
nunca van a tener un hash estable, y aunque lo tuvieran, mantener un
allowlist de hashes para colores generados en runtime es absurdo. La
solución correcta es estructural: **el frontend deja de emitir inline
styles**, y los colores dinámicos se aplican vía `el.style.background = cs`
(propiedad CSSOM, fuera del scope de `style-src`).

Este módulo hace tres cosas:
1. **Template** (`templates/index.html`): mueve los 11 inline styles
   estáticos a clases CSS (`hidden` para `display:none`; clases nuevas
   para el resto).
2. **CSS** (`static/css/estorides_ui.css`): recibe las clases nuevas.
3. **JS** (`static/js/estorides.js`): reescribe los template literals que
   interpolan `${cs}` / `${ct}` / `${colorForKind(...)}` para asignar la
   propiedad CSSOM sobre un `createElement` previo, en vez de inyectar
   `style="..."` en `innerHTML`.

---

## Inputs

| Origen | Línea(s) actuales | style actual | Acción |
| --- | --- | --- | --- |
| `templates/index.html:33` | `<div id="run-progress" ... style="display:none">` | `display:none` | agregar atributo HTML5 `hidden` (equivale visualmente) |
| `templates/index.html:39` | `<span id="discover-progress" ... style="display:none">` | `display:none` | atributo `hidden` |
| `templates/index.html:42` | `<button id="discover-stop" class="ghost" style="padding:0 6px;font-size:10px">` | `padding:0 6px;font-size:10px` | nueva clase `.stop-btn-sm` |
| `templates/index.html:61` | `<div id="result-filters" ... style="display:none">` | `display:none` | atributo `hidden` |
| `templates/index.html:135` | `<div class="meta-row" style="margin-top: 14px;">` | `margin-top: 14px;` | nueva clase `.meta-row-spaced` |
| `templates/index.html:169-171` | 3 × `<div ... style="display:none">` | `display:none` | atributo `hidden` |
| `templates/index.html:192` | `<div id="onboarding" ... style="display:none">` | `display:none` | atributo `hidden` |
| `templates/index.html:208` | `<div id="kbd-help" ... style="display:none">` | `display:none` | atributo `hidden` |
| `templates/index.html:221` | `<div class="onboarding-actions" style="margin-top:12px">` | `margin-top:12px` | nueva clase `.kbd-actions` (extiende `.onboarding-actions`) |
| `static/js/estorides.js:810,812` | `<span class="tt-chip" style="background:${cs}">` | dinámico (color cluster) | refactor: `createElement('span')`, asignar `chip.style.background = cs`, luego `innerHTML = label` |
| `static/js/estorides.js:1301` | `<div style="color:var(--text-2);padding:12px;text-align:center">no entities</div>` | estático | nueva clase `.empty-entities` |
| `static/js/estorides.js:1313` | `<h4 style="font-size:11px;...">Top entities (degree)</h4>` | estático | nueva clase `.graph-top-title` |
| `static/js/estorides.js:1317` | `<span style="color:${colorForKind(e.kind)}">` | dinámico (color kind) | refactor: `createElement('span')`, `kindEl.style.color = colorForKind(e.kind)`, `innerHTML = type` |
| `static/js/estorides.js:1332` | `<h3 style="color:var(--accent-2);margin-bottom:8px">Acquisition Timeline</h3>` | estático | nueva clase `.timeline-title` |
| `static/js/estorides.js:1342-1343` | `<span style="color:var(--text-2)">` ×2 | estático | nueva clase `.timeline-meta` |

Total: **11 inline styles estáticos** en template + **4 inline styles en JS**
(2 estáticos, 2 con `${}`). Resultado: **cero `style="..."` en todo el repo
después del refactor**, sin tocar la CSP para nada.

---

## Outputs

### Forma final de los archivos

`templates/index.html`: cero atributos `style=`, presencia de atributo
HTML5 `hidden` en los 8 elementos que necesitan empezar ocultos.

`static/css/estorides_ui.css`: tres reglas nuevas
(`.stop-btn-sm`, `.meta-row-spaced`, `.empty-entities`,
`.graph-top-title`, `.timeline-title`, `.timeline-meta`, `.kbd-actions`)
ubicadas en el bloque del componente correspondiente.

`static/js/estorides.js`: las dos funciones con template literals
`showBridgeTooltip` y `renderGraphSummary` se reescriben para usar
`document.createElement` + `el.style.X = …` para los valores dinámicos.
Los strings de reemplazo puro (que eran estáticos) se reemplazan por
clases.

### CSP

`estorides_core/web_security.py:csp_policy` queda **idéntica** — la CSP
ya era correcta, el bug estaba en el frontend. Se elimina el comentario
"Issue #41: tighten style-src against CSS injection" (ya no aplica) y se
actualiza el comentario inline para reflejar que **la defensa en
profundidad** es: (a) CSP bloquea inline styles, (b) el frontend los
emite vía CSSOM, (c) no hay forma de inyectar `<style>` por markup.

### Tests

`tests/test_csp_safe_styles.py`:
- `test_index_html_has_no_style_attribute`: parsea el template, asserta
  cero matches de `style="..."`.
- `test_estorides_js_has_no_style_attribute_in_string_literals`: parsea
  el JS, busca `style="` o `style:\s*"` en template literals y
  strings; asserta cero matches.
- `test_css_has_required_classes`: verifica que las clases nuevas
  existen en `estorides_ui.css`.
- `test_csp_policy_does_not_relax_for_unsafe_inline`: parsea
  `WebSecurityConfig.csp_policy` y asserta que ni `style-src` ni
  `default-src` contienen `'unsafe-inline'`.
- `test_hidden_attribute_is_set_on_offscreen_elements`: confirma que
  los 8 IDs/elementos offscreen usan `hidden` (no `display:none`).
- `test_dynamic_chip_color_uses_cssom_assignment`: parsea el JS, busca
  `chip.style.background = ` (o equivalente) y confirma que el color
  dinámico se asigna por CSSOM, no por `style="..."`.
- `test_dynamic_kind_color_uses_cssom_assignment`: idem para
  `colorForKind(e.kind)`.
- `test_template_renders_with_default_state`: renderiza
  `index.html` con un Flask test client; verifica que la CSP está, que
  el HTML no contiene `style="`, y que el atributo `hidden` aparece
  donde corresponde.

Adicional: `tests/properties/test_csp_safe_styles_properties.py` con
property-based (hypothesis) que genera templates con placeholders
arbitrarios y confirma que **ninguna sustitución de Jinja introduce
`style="`** (defensa contra inyecciones futuras).

---

## Tabla de errores

| Modo de fallo | Código | Mensaje | Comportamiento |
| --- | --- | --- | --- |
| CSS class añadida en JS pero no en CSS | `ImportError` al cargar el stylesheet | (browser) "Unknown property name" | El test `test_css_has_required_classes` lo detecta antes. |
| Inline style dinámico con hash explícito en CSP | `CSPViolation` (browser console) | "Applying inline style violates…" | **Prohibido**: el módulo no usa `'unsafe-inline'`, no usa hashes, no usa nonces. |
| Operador pone `ESTORIDES_CSP` con `'unsafe-inline'` en env | CSP permite inline; UI "funciona" sin refactor | (silencioso) | Aceptable como override del operador, pero los tests no lo cubren: la política por defecto sigue siendo tight. |
| `hidden` attribute interactúa mal con CSS `[hidden] { display: none }` | Elemento se ve cuando debería estar oculto | (visual) | El browser default stylesheet ya incluye `[hidden] { display: none }`; el test `test_hidden_attribute_is_set_on_offscreen_elements` lo confirma. |

---

## Garantías de seguridad

1. **Cero inline styles emitidos por el frontend.** Verificado por
   `test_index_html_has_no_style_attribute` y
   `test_estorides_js_has_no_style_attribute_in_string_literals`.
2. **CSP `style-src` se mantiene sin `'unsafe-inline'`.** Verificado por
   `test_csp_policy_does_not_relax_for_unsafe_inline`.
3. **Asignación de color dinámico por CSSOM**, fuera del scope de CSP.
   `el.style.background = cs` no genera una entrada en la
   directive-applied list de `style-src`; es un setter de la CSSOM.
4. **Defensa contra inyecciones futuras**: el property-based test
   genera templates con strings arbitrarios interpuestos en posiciones
   donde podrían colarse atributos `style=`; confirma que la
   sustitución de Jinja nunca produce un `style="` malicioso.
5. **`hidden` attribute es HTML estándar**, presente en todos los
   browsers soportados (IE11+, todo lo moderno). No introduce
   dependencias ni polyfills.

---

## Out of scope

- No se cambia `script-src` (sigue siendo `'self' https://unpkg.com
  https://cdn.jsdelivr.net`).
- No se cambian los headers que ya estaban bien
  (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`,
  `Permissions-Policy`).
- No se introduce `nonce-…` ni un sistema de nonces: la solución
  correcta no los necesita.
- No se refactoriza el CSS de la app (sólo se **agregan** reglas
  nuevas en `estorides_ui.css`; las existentes no se tocan salvo en el
  caso de `.onboarding-actions`, al que se le añade un selector
  adicional para `.kbd-actions` que hereda estilos).
- No se cambia `estorides.css` (paleta, layout principal, sidebar
  layout). Las clases nuevas viven todas en `estorides_ui.css` que es
  donde está el resto del CSS aditivo.

---

## Escenarios BDD (Given-When-Then)

> Los tests los traducen a ejecutables en `tests/test_csp_safe_styles.py`.

**S1 — Happy path: template sin inline styles.**
Given el template `templates/index.html` recién cargado,
When el test cuenta atributos `style="..."`,
Then encuentra **cero** ocurrencias.

**S2 — Happy path: JS sin inline styles en template literals.**
Given el módulo `static/js/estorides.js`,
When el test busca `style="` o `style:\s*'` en cualquier string literal
o template literal,
Then encuentra **cero** ocurrencias.

**S3 — Edge: atributo HTML5 `hidden` reemplaza `display:none`.**
Given el template renderizado por Flask,
When el test inspecciona los 8 elementos que arrancan ocultos
(`#run-progress`, `#discover-progress`, `#result-filters`,
`#graph-tooltip`, `#graph-context-menu`, `#graph-inspector`,
`#onboarding`, `#kbd-help`),
Then todos tienen el atributo `hidden` y ninguno tiene `style=`.

**S4 — Edge: color dinámico de cluster por CSSOM.**
Given un grafo con dos clusters, uno de color `#ff0000` y otro `#00ff00`,
When `showBridgeTooltip` se llama,
Then el primer `<span class="tt-chip">` tiene
`element.style.backgroundColor === 'rgb(255, 0, 0)'`
y el segundo `'rgb(0, 255, 0)'`, **y el HTML generado no contiene
`style="background:`**.

**S5 — Error: CSP no permite `'unsafe-inline'`.**
Given `WebSecurityConfig().csp_policy`,
When el test parsea las directivas y busca `'unsafe-inline'`,
Then no aparece ni en `style-src` ni en `default-src`.

**S6 — Seguridad: el refactor no relaja la CSP.**
Given el módulo `estorides_core/web_security.py` después del refactor,
When se importa `WebSecurityConfig`,
Then `csp_policy` es **exactamente** el mismo string que antes
(caracter por caracter, fuera del comentario explicativo).

**S7 — Seguridad: Jinja no permite colar `style="` por
interpolación de query/case/notas/etc.**
Given un template donde la query del usuario es `evil" style="background:red`,
When Flask renderiza `index.html` (la query no se renderiza dentro del
template, pero el test simula inyección en cada slot de Jinja),
Then el output **nunca** contiene `style="` válido y la sustitución
escapa correctamente con la regla `|e` (o no se renderiza en absoluto).

**S8 — Visual: la UI no se ve rota tras el refactor.**
Given el screenshot de referencia del run anterior,
When el agente exporta la página actual a PDF y la rasteriza
(véase `spec/visual_review.md`),
Then no hay solapamientos, no hay colores faltantes, y los chips de
cluster se ven coloreados con el color del cluster (no en gris).

---

## Cambios al cerrar el módulo

- `templates/index.html` — 11 atributos `style=` eliminados.
- `static/css/estorides_ui.css` — 6 clases nuevas
  (`.stop-btn-sm`, `.meta-row-spaced`, `.empty-entities`,
  `.graph-top-title`, `.timeline-title`, `.timeline-meta`,
  `.kbd-actions`).
- `static/js/estorides.js` — 2 funciones refactorizadas
  (`showBridgeTooltip`, `renderGraphSummary`) + 1 simplificada
  (`renderTimeline`, ya no usa `style="color:var(--text-2)"` dos veces).
- `estorides_core/web_security.py` — comentario inline actualizado
  (sin cambio de comportamiento, sin cambio de `csp_policy`).
- `tests/test_csp_safe_styles.py` — 8 tests BDD.
- `tests/properties/test_csp_safe_styles_properties.py` — 1 property
  con 1000+ ejemplos.
- `spec/csp_safe_styles.md` — este archivo, fechado al cierre.
- `CLAUDE.md` — fila nueva en la tabla de hitos cerrados.
- `docs/index.html` — card nueva del módulo 2d.
- `README.md` — sin cambios (la UI visible no cambia, sólo el código
  que la genera).
