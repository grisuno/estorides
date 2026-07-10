# `paged_results` — Spec

> Multi-page fetch loop for source APIs that return paginated results.
> Supports three strategies: page-number, offset, and cursor-based.

---

## Purpose

Source APIs (GitHub, Shodan, urlscan.io, VirusTotal) return paginated
results. The orchestrator currently fires one request per source and
ignores subsequent pages. This module adds a configurable pagination
loop to the source fetch pipeline, so a single source can harvest
multiple pages from a single query without changing the downstream
processing.

The pagination loop is transparent to the rest of the pipeline: each
page is parsed, fused, and streamed to subscribers independently, but
the orchestrator's response looks like a single merged result.

---

## Pagination strategies

### `page` — numeric page param

The simplest strategy. Increments a URL parameter (default `page`):

```
GET /api/search?q=evilcorp&page=1&per_page=30
GET /api/search?q=evilcorp&page=2&per_page=30
```

Stops when a page returns fewer results than `page_size` (partial page
= last page) or `max_pages` is reached.

### `offset` — offset + limit param

For APIs that use `offset`/`limit` (or `skip`/`take`) style:

```
GET /api/search?q=evilcorp&offset=0&limit=50
GET /api/search?q=evilcorp&offset=50&limit=50
```

Stops when a page returns fewer results than `limit`.

### `cursor` — response-driven next token

Extracts a cursor/next-page token from the JSON response body at a
configurable path (dot-notation) and sends it as a URL parameter on the
next request:

```
GET /api/search?q=evilcorp&cursor=abc123
```

Stops when the response contains no cursor, the cursor is empty, or
`max_pages` is reached.

---

## Source YAML schema

```yaml
name: github_repos
pagination:
  strategy: page          # "page" | "offset" | "cursor"
  param: page             # URL param name (default: "page")
  page_size: 30           # results per page for stop condition
  max_pages: 5            # safety cap (default: 10)
  # cursor-only:
  cursor_param: cursor    # URL param name for cursor (default: "cursor")
  cursor_path: next       # JSON dot-path to next cursor value (default: "next")
  response_list_path: items  # JSON dot-path to the result list for page-size check
  # offset-only:
  offset_param: offset    # URL param name for offset (default: "offset")
  limit_param: limit      # URL param name for limit (default: "limit")
```

All fields optional. `page_size` is required for the `page` and `offset`
stop condition. `max_pages` defaults to 10.

---

## Behaviour

| Condition | Action |
|---|---|
| No `pagination` in source | Single fetch (current behaviour) |
| `page_size` not specified for `page`/`offset` | Single fetch, no loop |
| `max_pages` reached | Stop, log debug message |
| Empty page (no results) | Stop |
| Partial page (< page_size) | Stop (last page detected) |
| Parse error on a page | Log warning, continue to next page |
| HTTP error on a page | Log warning, stop pagination |
| Cursor path not found in response | Stop |
| Empty cursor value | Stop |

## Inputs

Source dict with optional `pagination` key containing strategy config.

## Outputs

Each page produces a separate `on_result` callback. The final return
value is a merged result: the *last* page's parsed data is the primary
return, but all pages' data is available via `on_result`.

## BDD scenarios

### PG1 · Page strategy increments param

**Given** a source with `pagination.strategy=page`, `param=pg`,
`page_size=10`, `max_pages=3`  
**When** the source is executed  
**Then** the first request uses `pg=1`, the second `pg=2`, the third
`pg=3`, and no fourth request is made.

### PG2 · Offset strategy advances by page_size

**Given** a source with `pagination.strategy=offset`, `page_size=25`,
`max_pages=2`  
**When** the source is executed  
**Then** the first request uses `offset=0&limit=25`, the second
`offset=25&limit=25`.

### PG3 · Cursor strategy reads next token from response

**Given** a source with `pagination.strategy=cursor`,
`cursor_path=next_page`  
**When** the source returns `{"next_page": "token_abc"}`  
**Then** the second request includes `cursor=token_abc`.

### PG4 · No pagination = no loop

**Given** a source without a `pagination` key  
**When** executed  
**Then** exactly one HTTP request is made.

### PG5 · Partial page stops loop

**Given** `page_size=10`, `max_pages=10`  
**When** a page returns only 3 results  
**Then** no further pages are requested.

### PG6 · Max pages caps the loop

**Given** `max_pages=2` and every page returns `page_size` results  
**When** executed  
**Then** exactly 2 requests are made.

### PG7 · Empty cursor stops loop

**Given** `strategy=cursor`  
**When** the cursor value in the response is empty/null  
**Then** no further pages are requested.
