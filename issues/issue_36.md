# Issue #36: Bare int() casts on user-controlled query parameters cause unhandled ValueError (500) on four endpoints

- **State:** open
- **Created:** 2026-06-08T11:42:44Z
- **Updated:** 2026-06-08T11:42:44Z
- **Labels:** None

---

## Summary
`/api/osiris/cisa-kev` and `/api/osiris/malware` pass query parameters `limit` and `days` directly to `int()` without using the validated `_arg_int()` helper that exists in the same file. A non-numeric value causes an unhandled `ValueError` that propagates up through Flask's error handler as a 500, leaking a Python traceback. A similar issue affects `/api/discover/jobs` at line 726.

## Evidence
`estorides_web.py` lines 657–658 (cisa-kev handler):
```python
limit = int(request.args.get("limit", 10))   # unguarded — ValueError on "abc"
days = int(request.args.get("days", 30))      # unguarded — ValueError on "abc"
return jsonify(osiris_sources.fetch_cisa_kev(limit=limit, days=days))
```

`estorides_web.py` line 666 (malware handler):
```python
limit = int(request.args.get("limit", 200))  # unguarded — ValueError on "abc"
```

`estorides_web.py` line 726 (discover/jobs handler):
```python
return jsonify({"jobs": list_discover_jobs(limit=int(request.args.get("limit", 20)))})
```

The safe helper exists at line 70:
```python
def _arg_int(name: str, default: int) -> int:
    ...
    try:
        return int(raw)
    except ValueError:
        return default
```

Flask's `PROPAGATE_EXCEPTIONS = False` means the 500 is returned but the full Python traceback (including file paths and variable names) is logged server-side. The response body in default Flask will also include a generic error page that reveals the application type.

## Why this matters
Non-numeric limit values cause unhandled exceptions. In production behind gunicorn the 500 response leaks the application framework identity. With `app.config["DEBUG"] = False` the interactive debugger is off, but the log file receives full tracebacks including absolute paths — which are useful for attackers who gain log access.

## Attack or failure scenario
1. Attacker requests `GET /api/osiris/cisa-kev?limit=; DROP TABLE cases;--`
2. Server raises `ValueError: invalid literal for int() with base 10: '; DROP TABLE cases;--'`
3. Flask returns HTTP 500 with an HTML error page identifying the server as Flask/Werkzeug.
4. A flood of such requests fills error logs with tracebacks and triggers monitoring false positives.

## Root cause
The `_arg_int()` helper was added to guard earlier endpoints but was not used consistently when the osiris and discoverer endpoints were added in a later commit. No linting rule enforces use of the helper.

## Recommended fix
Replace all bare `int(request.args.get(...))` calls with `_arg_int(name, default)`:
```python
# Before:
limit = int(request.args.get("limit", 10))
# After:
limit = _arg_int("limit", 10)
```

Apply to: `api_osiris_kev` (limit, days), `api_osiris_malware` (limit), `api_discover_jobs` (limit).

Add a Ruff/AST lint rule or a grep pre-commit hook that fails on `int(request.args` patterns.

## Acceptance criteria
- No bare `int(request.args.get(...))` or `int(request.args[...])` calls remain in `estorides_web.py`.
- Sending `?limit=notanumber` to each affected endpoint returns a 200 with the default value, not a 500.
- A unit test covers all four endpoints with non-numeric limit/days values and asserts a 200 or 400 (not 500).

## Suggested labels
bug, security, reliability

## Priority
P2

## Severity
Medium — Unhandled `ValueError` produces 500 responses that identify the server framework, fill error logs with tracebacks, and can be used to trigger monitoring noise at scale. Not directly exploitable for data access.

## Confidence
Confirmed — the bare `int()` calls are present at the listed lines; `_arg_int()` is defined and used elsewhere in the same file.
