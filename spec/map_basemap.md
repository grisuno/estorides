# map_basemap — fondo de mapa del tab geoespacial

## Purpose

El tab de mapa (Leaflet) pegaba directo a `tile.openstreetmap.org`, cuyos
términos prohíben el uso pesado/scraping y devuelven baneos (HTTP 403/429
con imagen de "tile scraping not allowed"). Este módulo fija el proveedor
de teselas al más curado listo-para-prod sin API key ni rewrite: **Esri
Dark Gray Canvas** (`server.arcgisonline.com`, capa base
`Canvas/World_Dark_Gray_Base` + capa de etiquetas
`Canvas/World_Dark_Gray_Reference`, estilo oscuro acorde a la UI de
Estorides, sin key, sin cuenta, sin billing).

Descartado en visual review: **CARTO basemaps** exigía API key (teselas
marcadas con "API KEY REQUIRED", ver `.scratchpad/map_carto.png`).
Descartados por diseño: proveedores con API key y billing (MapTiler,
Radar, Mapbox, Stadia, Thunderforest) y el rewrite a vector
(MapLibre).

## Inputs

- Ninguno en runtime: la URL del proveedor es constante en
  `static/js/estorides.js` (función de init del mapa Leaflet).
- Coordenadas de `plotPoints(coords)` — fuera de scope (las dibuja el
  módulo de grafo/geoespacial, no el basemap).

## Outputs

- `L.tileLayer` base con URL
  `https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}`
  (notar orden Esri `{z}/{y}/{x}`), `maxZoom: 16` (zoom nativo del
  servicio).
- `L.tileLayer` de referencia (etiquetas) con URL
  `.../Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}`.
- Atribución: `Powered by Esri | © OpenStreetMap contributors` (exigida
  por los términos de Esri).

## Tabla de errores

| Condición | Comportamiento |
| --- | --- |
| CDN CARTO caído / sin red | Leaflet muestra fondo gris; los marcadores y popups siguen funcionando (capa de datos intacta) |
| URL con typo de estilo (`dark_all`) | Teselas 404; mismo degradado graceful, sin excepción JS |
| CSP `img-src` | `server.arcgisonline.com` debe estar permitido (`https:` genérico lo cubre); si no, teselas bloqueadas (ver garantías) |

## Garantías de seguridad

- Cero datos de operador salen al proveedor: las teselas son GET
  anónimos sin query params (sin API key que fugar, sin tracking de
  coordenadas en URL más allá del z/x/y inherente al tile).
- Sin `eval`/innerHTML nuevo: el cambio es solo la constante de URL +
  atribución; los popups siguen pasando por `escapeHTML`/`escapeAttr`.
- Atribución OSM+CARTO siempre visible (requisito legal, no decorativo).

## Out of scope

- MapLibre/vector tiles (rewrite mayor, sin ganancia para el caso de uso).
- Proveedores con API key y billing (MapTiler, Radar, Mapbox): añaden
  secreto que custodiar y superficie de fuga; reconsiderar solo si CARTO
  rate-limitea.
- Tiles offline / self-hosted (coste de infra fuera del scope actual).
- Geocoding / routing (el mapa solo visualiza puntos).

## Escenarios BDD Given-When-Then

### S1 — sin rastro de OSM directo
Given: `static/js/estorides.js`
When: se inspecciona el `tileLayer`
Then: no contiene `tile.openstreetmap.org`.

### S2 — proveedor Esri dark
Given: el init del mapa Leaflet
When: se crean los `tileLayer`
Then: las URLs son las de `Canvas/World_Dark_Gray_Base` y
  `Canvas/World_Dark_Gray_Reference` en `server.arcgisonline.com` con
  orden `{z}/{y}/{x}` y sin marcas de "API KEY REQUIRED".

### S3 — atribución legal
Given: el `tileLayer` base
When: se lee su `attribution`
Then: menciona `Esri` y `OpenStreetMap`.

### S4 — degradado sin red
Given: el CDN inalcanzable
When: se abre el tab de mapa
Then: no hay excepción JS no capturada; `plotPoints` sigue dibujando
  marcadores (la capa de datos no depende de la de teselas).

### S5 — CSP no rompe teselas
Given: la política CSP de la app
When: el mapa pide teselas
Then: `img-src` permite `https://*.basemaps.cartocdn.com` (o el mapa
  documenta el ajuste necesario).
