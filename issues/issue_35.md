# Issue #35: /api/graph, /api/status, and all /api/discover/* endpoints are missing rate limiting

- **State:** open
- **Created:** 2026-06-08T11:42:35Z
- **Updated:** 2026-06-08T11:42:35Z
- **Labels:** None

---

## Summary
`/api/graph`, `/api/status`, `/api/discover/start`, `/api/discover/stop`, `/api/discover/jobs`, `/api/discover/stream`, and `/api/run/stream` are all missing the `@_rate_limit_decorator` applied to every other endpoint. An anonymous caller can hammer these endpoints without restriction, bypassing the 30 req/min sliding-window rate limiter that protects the compute-heavy paths.

## Evidence
`estorides_web.py` — routes confirmed missing `@_rate_limit_decorator`:

| Route | Method | Missing rate limit |
|---|---|---|
| `/api/graph` | GET | Yes — loads and traverses entire GraphML file |
| `/api/status` | GET | Yes — scans YAML source registry |
| `/api/discover/start` | POST | Yes — launches background crawl job |
| `/api/discover/stop` | POST | Yes — cancels jobs |
| `/api/discover/jobs` | GET | Yes |
| `/api/discover/stream` | GET | Yes — holds open SSE connections |
| `/api/run/stream` | GET | Yes — holds open SSE connections |
| `/api/run/stream/stop` | POST | Yes |

`api_graph` is particularly dangerous: it reads the shared `data/estorides_graph.graphml` file, deserialises it with NetworkX, computes community detection, and serialises up to 200 nodes and 1000 edges on every call. With no rate limit, a caller can keep a CPU core at 100% indefinitely.

`api_discover/start` lets an attacker queue background jobs without rate limiting; combined with the already-reported unbounded `DISCOVER_JOBS` memory growth, this is an amplified DoS.

## Why this matters
The rate limiter provides the primary abuse-prevention control for the platform. Leaving the most compute-intensive endpoints (`/api/graph`) and the most operationally powerful ones (`/api/discover/start`) outside the rate limiter entirely defeats that control for an attacker who knows the surface.

## Attack or failure scenario
1. Attacker sends 1000 concurrent `GET /api/graph` requests.
2. Each request reads the GraphML from disk, deserialises it, runs NetworkX community detection, and serialises the result.
3. Server CPU pegs at 100% and the process becomes unresponsive to legitimate operators within seconds.
4. Alternatively: attacker sends 500 `POST /api/discover/start` requests, filling `DISCOVER_JOBS` and saturating the background asyncio loop.

## Root cause
The `@_rate_limit_decorator` was added to some routes in a later refactoring pass but the decorator was omitted for the graph, status, discoverer, and stream endpoints. There is no static analysis check ensuring all routes carry the decorator.

## Recommended fix
1. Apply `@_rate_limit_decorator` to `/api/graph`, `/api/status`, `/api/discover/start`, `/api/discover/stop`, `/api/discover/jobs`, `/api/discover/stream`, `/api/run/stream`, and `/api/run/stream/stop`.
2. Add a test that enumerates all `@app.route` handlers and asserts each one is wrapped with the rate-limit decorator (or is explicitly whitelisted as exempt).
3. For the SSE stream routes, add a separate concurrent-connections limit (e.g. max 10 open SSE connections per IP) to prevent connection exhaustion.

## Acceptance criteria
- All routes registered in `create_app()` either carry `@_rate_limit_decorator` or are in an explicit exemption list with documented justification.
- A CI test enumerates the route table and fails if an unprotected handler appears.
- Load test: 100 concurrent `GET /api/graph` requests are rate-limited to the configured window.

## Suggested labels
security, reliability, production-readiness

## Priority
P1

## Severity
High — Missing rate limiting on compute-heavy and job-launching endpoints enables unauthenticated CPU/memory exhaustion and background-job flooding.

## Confidence
Confirmed — the missing `@_rate_limit_decorator` annotations are visible by inspection of `estorides_web.py`.
