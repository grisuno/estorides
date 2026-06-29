# Issue #48: Audit log (data/audit.jsonl) has no rotation, size cap, or retention policy — unbounded growth and privacy risk

- **State:** closed
- **Created:** 2026-06-08T11:43:40Z
- **Updated:** 2026-06-29T16:35:49Z
- **Labels:** None

---

## Summary
The `estorides_core/audit.py` module uses `sessions/audit.jsonl` in its docstring but the actual path is `data/audit.jsonl`. Both the docstring and the in-memory `RateLimiter` use `DATA_DIR` as their backing store. More importantly, the audit log records every query including the full query string, remote IP, and source counts in an unbounded append-only file. There is no log rotation, no size cap, no retention policy, and no access control on the file — it accumulates indefinitely and can be read by anyone with file system access to `data/`.

## Evidence
`estorides_core/audit.py` line 10:
```python
Every API call ... gets a JSON line appended to
`sessions/audit.jsonl` (one line per request)
```

Actual path, `estorides_core/audit.py` line 50:
```python
AUDIT_PATH: Path = DATA_DIR / "audit.jsonl"
```

The `AuditEvent` fields include `query` (the full OSINT query string), `remote_ip`, `path`, and `extra` which contains `query_type`. In a law enforcement or threat intelligence context, the queries themselves are sensitive — they reveal what targets are being investigated.

No log rotation, compression, or TTL-based deletion is implemented. In a busy deployment at 30 req/min, the log grows by ~86,400 lines/day and will eventually fill the disk.

## Why this matters
1. **Privacy**: The audit log records every query (target IP, domain, email, BTC address) and the IP of the querying operator. If the `data/` directory is accessible to the web server process, a path traversal or misconfiguration could expose the full investigation history.
2. **Disk exhaustion**: No rotation means the file grows forever.
3. **Documentation inconsistency**: The path referenced in the docstring (`sessions/audit.jsonl`) does not match the actual path (`data/audit.jsonl`), indicating the module was refactored without updating the documentation — a reliability signal.

## Attack or failure scenario
1. Deployment accumulates 6 months of audit logs.
2. `data/audit.jsonl` reaches multiple GBs and fills the disk.
3. Application crashes (cannot write to log or temp files).
4. Alternatively: a file path disclosure bug allows the audit log to be downloaded; the full investigation history of all operators is exposed.

## Root cause
The audit log was implemented as a simple append-only JSONL file without the operational infrastructure needed for production use (rotation, compression, retention). The documentation inconsistency suggests the code was moved after the docstring was written.

## Recommended fix
1. Fix the docstring to reference the correct path.
2. Implement log rotation using Python's `logging.handlers.RotatingFileHandler` or equivalent:
   - Max file size: 100 MB
   - Keep last 5 rotations
3. Add a configurable retention policy (`ESTORIDES_AUDIT_RETENTION_DAYS`).
4. Consider moving to structured logging via `logging` instead of manual JSONL writing.
5. Ensure `data/` is not served as static content and is outside the web root.

## Acceptance criteria
- The audit log file does not grow beyond a configurable maximum size.
- Old log entries are rotated and compressed automatically.
- The docstring matches the actual file path.
- `data/audit.jsonl` is explicitly excluded from any static file serving configuration.

## Suggested labels
reliability, privacy, production-readiness

## Priority
P2

## Severity
High — Unbounded audit log growth can cause disk exhaustion; the log contains sensitive investigation targets (full query strings and operator IPs) with no access control or retention policy.

## Confidence
Confirmed — the unbounded append pattern is in the code; the docstring mismatch is verified.
