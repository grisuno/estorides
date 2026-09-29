# ops_observability — Spec

## Purpose
Operador mono-usuario necesita saber si app vive y qué pasa dentro sin Prometheus/Sentry externos. Endpoints livianos stdlib-only + logs JSON estructurados. Sin deps nuevas, sin multi-user, sin SaaS.

## Inputs
- `GET /healthz` — sin auth, sin rate-limit. Responde vivo.
- `GET /readyz` — con auth. Chequea `SOURCES_DIR` existe y registry carga >0 fuentes.
- `GET /metrics` — con auth. Texto formato Prometheus, contadores en memoria del proceso.
- `configure_structlog()` — activa JSON a stderr si `ESTORIDES_JSON_LOGS=1`.
- `record_request(endpoint, status)` / `record_source(source, ok)` — contadores thread-safe.

## Outputs
- `/healthz` → `{"status":"ok","version":"1.3.0"}` 200, `Cache-Control: no-store`.
- `/readyz` → `{"ready":true,"sources":N}` 200, o `{"ready":false,...}` 503.
- `/metrics` → `text/plain; version=0.0.4`, líneas:
  ```
  estorides_requests_total{endpoint="/api/run",status="200"} 3
  estorides_source_errors_total{source="crtsh"} 1
  ```
- Log JSON por línea: `{"ts":..,"level":..,"event":..,...}` solo cuando env activado; default logging plano intacto.

## Tabla de errores
| Condición | Código | Comportamiento |
|---|---|---|
| registry vacío / dir ausente en readyz | 503 | `{"ready":false,"sources":0}` |
| endpoint desconocido en record_request | — | normaliza a `"other"`, nunca raise |
| source vacío en record_source | — | ignora, nunca raise |
| métricas concurrentes | — | Lock, nunca corrupto |

## Garantías de seguridad
- `/healthz` sin datos sensibles: solo status+version. Sin query echo, sin paths.
- `/readyz` y `/metrics` tras `require_auth` + rate-limit existentes. No exponen IPs, queries, tokens.
- Labels Prometheus sanitizados: `[^a-zA-Z0-9_/:.-]` → `_`, cap 200 chars. Sin inyección de newlines.
- Sin eval/exec/subprocess/socket nuevo. Puro stdlib.

## Out of scope
- Prometheus server/Grafana/OTel/Sentry/Celery/Redis/Neo4j/ES/Vault/FastAPI rewrite — overkill mono-usuario, van a M2-M5 o nunca.
- Roles/permisos multi-user — usuario pidió mono-usuario explícito.
- Trazas distribuidas — un proceso, `audit.log` append-only ya existe.

## Escenarios BDD Given-When-Then
1. Given app viva, when `GET /healthz` sin token, then 200 `{"status":"ok"}` y no pide auth.
2. Given registry con N fuentes, when `GET /readyz` autenticado, then 200 `{"ready":true,"sources":N}`; given dir roto, then 503 `ready:false`.
3. Given 3 runs OK + 1 error crtsh, when `GET /metrics`, then texto contiene `estorides_requests_total` y `estorides_source_errors_total` con labels correctos.
4. Given label hostil `crtsh\nINJECT:x`, when record + scrape, then salida sin newline, sanitizada, una sola línea por serie.
5. Given `ESTORIDES_JSON_LOGS=1`, when loguea evento, then línea es JSON parseable con `ts/level/event`; given env ausente, then formato plano legacy intacto.
6. Given 10 threads x 100 records, when terminan, then contadores exactos, sin pérdida ni crash.
