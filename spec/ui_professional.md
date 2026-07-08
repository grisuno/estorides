# `ui_professional` -- Spec (Modulo 2h)

> Interfaz de usuario profesional: animacion de carga, visualizacion por
> tiers de relevancia, refinamientos visuales modernos. Sin emojis, sin
> dependencias nuevas, sin romper CSP.

---

## Purpose

La interfaz web de Estorides es funcional pero carece de refinamientos
profesionales que indiquen al operador que el sistema esta trabajando
activamente. Con 100+ fuentes OSINT lanzadas en paralelo, el operador
necesita:

1. **Una senal visual clara** de que el motor esta trabajando (no
   confundir "cargando" con "congelado").
2. **Resultados organizados por relevancia** -- los datos mas utiles
   primero, el ruido al final, cada seccion colapsable para no saturar.
3. **Una estetica moderna y profesional** -- transiciones suaves,
   glass-morphism sutil, tipografia refinada, sombras elegantes.

Este modulo cubre exclusivamente la capa de presentacion: template HTML,
hojas CSS y codigo JavaScript. No toca logica del backend mas alla de
consumir el campo `tiers` que `recon_fusion` produce.

## Inputs

### Template context

El template `index.html` recibe el contexto existente de `SearchTelemetry`
mas los datos de fusion de `recon_fusion`:

| Variable | Fuente | Formato |
|----------|--------|---------|
| `telemetry` | `SearchTelemetry.context()` | `dict` |
| `tiers` | `FusionResult.tiers` | `dict[str, list[GroupedEntity]]` |
| `tier_summary` | `FusionResult.tier_summary` | `dict[str, int]` |

### API response (from `/api/run`)

El endpoint `/api/run` ahora incluye:

```json
{
  "query_type": "domain",
  "tiers": { "critical": [...], "high": [...], ... },
  "tier_summary": { "critical": 2, "high": 5, ... },
  "observations": [...],
  "entities": [...],
  ...
}
```

## Outputs

### Marcadores visibles

1. **Loading animation** -- Un indicador animado en la barra de estado
   que muestra "Working" con un spinner CSS (circulo giratorio) mientras
   el motor esta corriendo. Al finalizar, el indicador desaparece y el
   estado cambia a "Ready".

2. **Progress animation** -- La barra de progreso existente se mejora con
   una animacion de "respiracion" (pulse) cuando el progreso esta
   indeterminado (aun no se sabe el total de fuentes). Cuando el total
   se conoce, la barra hace transicion suave.

3. **Tiered result display** -- Los resultados se agrupan en 5 secciones
   colapsables:
   - Critical (rojo/accent, expandido por defecto)
   - High (naranja, expandido por defecto)
   - Medium (amarillo, colapsado por defecto)
   - Low (gris, colapsado por defecto)
   - Noise (gris oscuro, colapsado por defecto, con opcion "show noise")
   
   Cada seccion muestra un contador de items, el score de relevancia
   maximo y un boton para expandir/colapsar.

4. **Fade transitions** -- Los resultados aparecen con fade-in suave
   (no pop abrupto). Las tarjetas individuales tienen hover sutil.

5. **Sticky tier header** -- El encabezado de cada seccion de tier se
   mantiene visible al hacer scroll dentro del panel de resultados.

### Estilos CSS

| Selector / Clase | Propiedades |
|-----------------|-------------|
| `.loading-spinner` | `@keyframes spin` rotacion 0.8s linear infinite, color `var(--accent)`, 20px x 20px, borde 2px dashed. |
| `.working-indicator` | `display: flex`, gap, alineacion centro, opacidad 0->1 transicion. |
| `.tier-section` | Margen inferior 12px, borde izquierdo 3px solid color del tier. |
| `.tier-header` | Sticky `top: 0`, `background: var(--bg-1)`, padding 8px 10px, cursor pointer, hover effect. |
| `.tier-body` | `max-height` animado con transicion (0 -> N px). |
| `.tier-badge` | Circulo con contador, color del tier, font-size 10px. |
| `.tier-critical` | Borde izquierdo `#f43f5e`. |
| `.tier-high` | Borde izquierdo `#f59e0b`. |
| `.tier-medium` | Borde izquierdo `#eab308`. |
| `.tier-low` | Borde izquierdo `#6b7280`. |
| `.tier-noise` | Borde izquierdo `#374151`, opacidad 0.6. |
| `.fade-in` | `@keyframes fadeIn` 0.3s ease, opacity 0->1. |
| `.pulse-bar` | `@keyframes pulse` 2s ease-in-out infinite, opacidad 0.6->1. |
| `.status-working` | Color `var(--accent-2)`, animation pulse. |
| `.entity-score` | Barra de score horizontal 80px, color segun valor (>0.7 verde, >0.4 amarillo, <=0.4 rojo). |

### Comportamiento JavaScript

| Funcion | Disparador | Efecto |
|---------|-----------|--------|
| `showWorkingIndicator()` | `runQuery()` or `startDiscover()` | Muestra spinner + "Working" en footer status. |
| `hideWorkingIndicator()` | Run completo o error | Oculta spinner, muestra "Ready" + timestamp. |
| `renderTieredResults(data)` | Recepcion de resultados | Construye las 5 secciones de tiers. |
| `toggleTierSection(key)` | Click en tier-header | Expande/colapsa el tier-body con transicion. |
| `renderTierGroup(group)` | `renderTieredResults` | Construye una tarjeta de entidad agrupada. |
| `updateTierCounts(data)` | Recepcion de resultados | Actualiza los badges de cada tier. |
| `fadeInElement(el)` | Insercion de nuevo DOM | Aplica clase fade-in. |

## Error table

| Modo de fallo | Comportamiento |
|---------------|----------------|
| `tiers` no presente en respuesta API | Fallback a lista plana de observaciones (comportamiento anterior). |
| `tier_summary` no presente | No se muestran contadores. |
| Panel de resultados vacio | Se muestra empty state existente. |
| Loading animation se queda pegada | Timeout de 60 segundos: se oculta y muestra toast "still working...". |
| Tier section sin entidades | No se renderiza (oculta completamente). |

## Security guarantees

1. **CSP intacta.** No se introducen `style` ni `script` inline. Todas
   las animaciones son CSS puro. Todos los manejadores JS se asignan via
   `addEventListener`, no `onclick` attributes.
2. **Sin emojis.** El indicador de carga es CSS puro (circulo giratorio),
   no un caracter emoji.
3. **Sin nuevas dependencias.** No se importan librerias JS/CSS nuevas.
   Las animaciones son CSS nativo (keyframes).
4. **ARIA attributes.** El spinner tiene `role="status"` y
   `aria-label="Loading"`. Las secciones colapsables tienen
   `aria-expanded` y `aria-controls`.
5. **XSS safe.** Todas las inserciones de texto usan `textContent` (no
   `innerHTML`) o `escapeHTML` comprobado.

## Out of scope

- **Tema claro.** Solo modo oscuro existente.
- **Internacionalizacion.** Solo ingles.
- **Sonido.** Sin efectos sonoros.
- **Notificaciones desktop.** Sin Service Workers ni Notification API.
- **Reordenamiento drag-and-drop.** Los tiers tienen orden fijo.

---

## Escenarios BDD (Given-When-Then)

### S1 -- Loading animation aparece al iniciar run

**Given** el operador hace click en "Run"  
**When** `runQuery()` se ejecuta  
**Then** `#footer-status` contiene el spinner CSS  
**And** `showWorkingIndicator()` se llama  
**And** la barra de progreso tiene clase `pulse-bar`.

### S2 -- Tier critical se renderiza expandido

**Given** una respuesta API con `tiers.critical` de 3 entidades  
**When** `renderTieredResults(data)` procesa la respuesta  
**Then** el DOM contiene un `section.tier-section.tier-critical`  
**And** `.tier-body` es visible (no hidden)  
**And** el contador `.tier-badge` muestra "3".

### S3 -- Tier noise se renderiza colapsado

**Given** una respuesta API con `tiers.noise` de 5 entidades  
**When** `renderTieredResults(data)` procesa la respuesta  
**Then** el DOM contiene `section.tier-section.tier-noise`  
**And** `.tier-body` no es visible inicialmente  
**And** el header tiene `aria-expanded="false"`.

### S4 -- Click en tier-header expande/colapsa

**Given** un tier-section renderizado y colapsado  
**When** el operador hace click en `.tier-header`  
**Then** `aria-expanded` cambia a `"true"`  
**And** `.tier-body` se vuelve visible  
**And** una segunda vez lo colapsa.

### S5 -- Sin datos de tiers, fallback a vista plana

**Given** una respuesta API sin campo `tiers`  
**When** `renderTieredResults(data)` se ejecuta  
**Then** se usa `buildResultCard(obs)` para cada observacion  
**And** no se muestran tier-sections  
**And** se muestra toast informativo.

### S6 -- Loading animation timeout

**Given** el motor tarda > 60 segundos  
**When** el timeout de loading expira  
**Then** el spinner se oculta  
**And** aparece toast con "still working...".

### S7 -- Hover en tarjeta de entidad muestra efecto sutil

**Given** un tier-group renderizado  
**When** el raton pasa sobre el grupo  
**Then** el background cambia ligeramente (hover: rgba)  
**And** transicion CSS suave (0.2s).

### S8 -- Transicion fade-in en nuevos resultados

**Given** nuevos resultados llegan al DOM  
**When** se insertan en el panel  
**Then** tienen clase `fade-in`  
**And** la animacion `fadeIn` corre 0.3s.

---

## Cierre del modulo

- **Fecha de cierre:** _(se llena al cerrar)_
- **Estado:** por implementar.
- **Validacion:**
  - `pytest tests/test_ui_professional.py -v` -- todos verdes
  - Visual review: exportar a PDF, rasterizar a PNG, inspeccionar.
  - `ruff check` -- limpio
  - `mypy --strict` -- sin errores
  - `bandit -r` -- sin High ni Medium
