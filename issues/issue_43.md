# Issue #43: /api/export/<fmt> creates permanent unbounded files in reports/ — unauthenticated disk exhaustion attack

- **State:** open
- **Created:** 2026-06-08T11:43:16Z
- **Updated:** 2026-06-08T11:43:16Z
- **Labels:** None

---

## Summary
`/api/export/<fmt>` serves files via `send_from_directory(p.parent, p.name)` where `p` is constructed by joining `REPORTS_DIR` with a timestamp-named filename. While the filename itself is safe (it's built from `int(time.time())`), the `fmt` parameter from the URL path is used in a branching conditional but is never validated as a filename-safe string before being used to construct error messages exposed in the JSON response. More critically, every export operation creates a new permanent file in `reports/` with no cleanup, resulting in unbounded disk consumption.

## Evidence
`estorides_web.py` lines 337–369:
```python
@app.route("/api/export/<fmt>")
@_rate_limit_decorator(event="api_export")
def api_export(fmt: str) -> Any:
    ...
    if fmt == "stix":
        p = REPORTS_DIR / f"bundle_{int(time.time())}.json"
    elif fmt == "misp":
        p = REPORTS_DIR / f"event_{int(time.time())}.json"
    elif fmt == "graphml":
        ...
    elif fmt == "json":
        ...
    else:
        return jsonify({"error": f"unknown format {fmt}"}), 400  # fmt reflected in response
    ...
    return send_from_directory(p.parent, p.name, as_attachment=True)
```

The `fmt` value is directly embedded in the error response. While it is HTML-context-free (it's in a JSON field), it is still reflected user input in a response body.

The existing committed file `reports/bundle_1780871293.json` (6.9 MB) demonstrates that this directory grows with real use. With the rate limiter at 30/min, an attacker can create ~43,200 new files per day (30 × 60 × 24), each up to the size of the current graph. At even 100 KB per file, that is 4.3 GB/day.

## Why this matters
1. **Disk exhaustion**: Unbounded file creation in `reports/` can fill the host disk, causing the application and all other services on the host to crash.
2. **Intelligence leakage**: Exported files accumulate indefinitely. If the `reports/` directory is web-accessible or backed up to an insecure location, any user's investigation data is persistently exposed.
3. **Response reflection**: The `fmt` value is reflected in a JSON error response, establishing a pattern of input reflection that is one step away from a response injection.

## Attack or failure scenario
1. Attacker sends 30 `GET /api/export/stix` requests per minute (rate limit allows this).
2. Each request writes a new `bundle_<timestamp>.json` to `reports/`.
3. Over 24 hours, 43,200 files accumulate, consuming disk proportional to the current graph size.
4. Host disk fills up; application crashes; operator is paged at 3 AM.

## Root cause
The export endpoint was designed for interactive single-user use where the operator immediately downloads and deletes files. No TTL-based cleanup, no per-request temp file, and no cap on file count was implemented.

## Recommended fix
1. Write exports to a `tempfile.NamedTemporaryFile` and serve it with `send_file`, deleting it after the response is sent (using Flask's `after_this_request` hook or a streaming response).
2. Alternatively, implement a cleanup job that deletes export files older than 1 hour.
3. Cap the total size of `reports/` (e.g. reject new exports if the directory exceeds 1 GB).
4. Move `REPORTS_DIR` outside the repository tree to prevent accidental git commits of intelligence data.

## Acceptance criteria
- No permanent files are created in `reports/` by the export endpoint; exports are served from temporary files and deleted after the response.
- OR: A cleanup job runs at application startup and every hour, removing export files older than a configurable TTL.
- The total size of `reports/` is bounded; an export request that would exceed the limit returns 507 Insufficient Storage.
- The `fmt` value in the 400 error response is sanitised or replaced with a fixed-set error code.

## Suggested labels
security, reliability, production-readiness

## Priority
P1

## Severity
High — Unbounded file creation in `reports/` enables unauthenticated disk exhaustion via the export endpoint (30 files/min per IP with default rate limit), and accumulates sensitive intelligence artifacts indefinitely.

## Confidence
Confirmed — the file creation pattern is visible in the export handler; the `reports/bundle_1780871293.json` file in git demonstrates real file accumulation.
