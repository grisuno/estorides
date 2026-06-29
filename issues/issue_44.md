# Issue #44: Internal exception details (file paths, schema names, query fragments) returned to unauthenticated API clients

- **State:** open
- **Created:** 2026-06-08T11:43:21Z
- **Updated:** 2026-06-08T11:43:21Z
- **Labels:** None

---

## Summary
Exception details are leaked to API clients in three places in `estorides_web.py`. The `/api/run` handler returns `str(e)` from any unhandled exception. The `/api/intel/graph` Cypher endpoint returns `str(e)` for Kuzu execution errors. The `/api/intel/resolve` endpoint embeds `str(e)` from persistent graph neighbor lookups in the response body. These exception strings can contain internal infrastructure details including absolute file paths, database schema names, variable names, and SQL/Cypher query fragments.

## Evidence
`estorides_web.py` line 209–211:
```python
except Exception as e:  # noqa: BLE001
    log.exception("run failed")
    return jsonify({"error": str(e)}), 500   # full exception message to client
```

`estorides_web.py` line 542–543:
```python
except Exception as e:  # noqa: BLE001
    return jsonify({"error": "cypher-failed", "detail": str(e)}), 400
```

`estorides_web.py` line 506–507:
```python
except Exception as e:  # noqa: BLE001
    out["persistent_neighbors_error"] = str(e)
```

`estorides_web.py` lines 366–368 (encryption errors):
```python
except ValueError as e:
    return jsonify({"error": "invalid-encryption-key", "detail": str(e)}), 400
except RuntimeError as e:
    return jsonify({"error": "encryption-failed", "detail": str(e)}), 500
```

Example Kuzu error that would be leaked: `"Table 'Domain' does not have a column 'id'. \nFile: /home/grisun0/src_note/py/fucklantir/estorides/env/lib/python3.11/site-packages/kuzu/connection.py, line 94"`.

## Why this matters
Exception strings from Kuzu, NetworkX, Python stdlib, and aiohttp routinely contain:
- Absolute file system paths (revealing the install directory, as seen in `_multi_test.sh`)
- Database schema details (table names, column names, relationship types)
- Stack frame variable values
- Internal query fragments that help attackers craft more targeted follow-up requests

## Attack or failure scenario
1. Attacker sends `GET /api/intel/graph?q=MATCH (n:NonExistentType) RETURN n`.
2. Kuzu raises a `RuntimeError` with a message like: `Table 'NonExistentType' does not have index. File: /opt/estorides/env/lib/python3.11/site-packages/kuzu/...`.
3. Response body: `{"error": "cypher-failed", "detail": "Table 'NonExistentType'..."}`.
4. Attacker learns the install path, Python version, and Kuzu schema — all directly useful for further targeted attacks.

## Root cause
Exception messages were forwarded to clients during development for debugging convenience and were never replaced with sanitised error codes before shipping.

## Recommended fix
Replace all `str(e)` in JSON responses with a generic error code and log the detail server-side only:
```python
except Exception as e:
    log.exception("run failed: %s", e)
    return jsonify({"error": "internal-error", "code": "E001"}), 500
```

For expected user-facing errors (invalid Cypher syntax), return a categorised message without the raw exception text:
```python
except Exception as e:
    log.warning("cypher query failed: %s", e)
    return jsonify({"error": "cypher-failed", "hint": "Check query syntax"}), 400
```

## Acceptance criteria
- No `str(e)` value from an unhandled exception is present in any JSON response body.
- The `/api/run`, `/api/intel/graph`, `/api/intel/resolve`, and `/api/export` endpoints return only opaque error codes on internal failures.
- A test verifies that an intentionally-broken Kuzu query returns a 4xx/5xx with no path, class name, or variable disclosure in the body.

## Suggested labels
security, bug

## Priority
P2

## Severity
High — Internal exception details including file paths, schema names, and variable values are returned to unauthenticated API clients, directly aiding attacker reconnaissance.

## Confidence
Confirmed — the `str(e)` patterns are present at the listed lines.
