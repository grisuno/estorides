# Issue #38: In-process rate limiter is multiplied by gunicorn worker count — effective limit is N_workers × 30/min

- **State:** open
- **Created:** 2026-06-08T11:42:53Z
- **Updated:** 2026-06-08T11:42:53Z
- **Labels:** None

---

## Summary
The rate limiter in `estorides_core/audit.py` is a pure in-process Python dictionary. When the application is deployed with gunicorn's default multi-worker mode (`-w 4`, as documented in `wsgi.py`), each worker process has a separate rate limiter with independent counters. An attacker can make up to `N_workers × 30 = 120` requests per minute per IP (with 4 workers) before any single process's limiter triggers, multiplied by the number of workers.

## Evidence
`estorides_core/audit.py` lines 99–127:
```python
class RateLimiter:
    """In-process sliding-window rate limiter.

    For a multi-worker deployment swap this for a Redis-backed
    implementation; the call sites only depend on `allow()` returning
    a bool, so the swap is local to this module.
    """
    def __init__(self, ...) -> None:
        ...
        self._buckets: Dict[str, Deque[float]] = {}  # in-process only
```

`wsgi.py` documents multi-worker deployment:
```
gunicorn -w 4 -b 0.0.0.0:5050 --timeout 120 --access-logfile - wsgi:app
```

With `ESTORIDES_RATE_LIMIT=30` (default), 4 workers allow 120 requests/min per IP. With the gunicorn default of worker count = `2 × CPU_count + 1`, a 4-core host allows 270 requests/min — 9× the documented limit.

## Why this matters
The rate limiter is the primary DoS protection and abuse-prevention control. In any realistic production deployment (gunicorn with multiple workers, or any reverse-proxy that load-balances across processes), the effective rate limit is multiplied by the worker count, rendering it largely ineffective against determined abuse.

## Attack or failure scenario
1. Attacker knows the deployment uses 4 gunicorn workers (easily inferred from response timing or a timing analysis of Retry-After headers from different workers).
2. Attacker distributes requests round-robin: each request hits a different worker, none of which has seen more than 7 requests from this IP.
3. Effective rate: 120/min, not 30/min. Paid API key quota is burned at 4× the expected rate.
4. Deep-run stream jobs (`/api/run/stream/start`) are particularly expensive: 4 simultaneous deep-run jobs can be launched before the first worker denies the 5th.

## Root cause
In-process rate limiters are inherently per-process. The comment in the code acknowledges this limitation but does not provide an alternative, and the `wsgi.py` startup instructions recommend multi-worker gunicorn without noting the implication for rate limiting.

## Recommended fix
1. Replace `RateLimiter` with a Redis-backed implementation using `redis.asyncio` or `redis-py` with `INCR`/`EXPIRE` sliding window.
2. Alternatively, use a shared-memory solution (e.g. `multiprocessing.Manager` dict or a named semaphore) for single-host deployments.
3. At minimum, document the limitation prominently in `wsgi.py` and `audit.py`, and recommend single-worker deployments behind a WAF or reverse proxy with its own rate limiting for production.
4. Add an environment variable `ESTORIDES_RATE_LIMIT_BACKEND=redis` that selects the backed implementation.

## Acceptance criteria
- In a gunicorn deployment with 4 workers, a single IP cannot exceed the configured `ESTORIDES_RATE_LIMIT` requests per minute across all workers combined.
- A test simulates 4 concurrent workers and verifies the aggregate rate is capped.
- `wsgi.py` documents the multi-worker rate-limit limitation and recommended mitigation.

## Suggested labels
security, architecture, production-readiness

## Priority
P1

## Severity
High — Effective rate limit is multiplied by worker count in any production deployment, rendering it meaningless against targeted abuse that burns paid API keys.

## Confidence
Confirmed — the rate limiter is clearly per-process in the code, and multi-worker deployment is documented in wsgi.py.
