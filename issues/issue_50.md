# Issue #50: RUN_STREAM_JOBS and DISCOVER_JOBS hold BufferedEventSink objects indefinitely — memory exhaustion via sustained job creation

- **State:** closed
- **Created:** 2026-06-08T11:43:49Z
- **Updated:** 2026-06-29T16:06:45Z
- **Labels:** None

---

## Summary
The `RUN_STREAM_JOBS` dictionary in `estorides_web.py` and the `DISCOVER_JOBS` dictionary in `estorides_core/discoverer.py` accumulate job objects indefinitely. Issue #14 and #20 cover this problem but the deeper issue is that these dictionaries hold references to `BufferedEventSink` objects, each of which holds an in-memory list of SSE events (`STREAM.sse_buffer_cap = 2000` events max per job). With the default 30 req/min rate limit, an attacker can create 30 stream jobs per minute; each job holds up to 2,000 events in memory; the jobs are never evicted. This is a memory exhaustion attack vector separate from the disk exhaustion in the export endpoint.

## Evidence
`estorides_web.py` line 118:
```python
RUN_STREAM_JOBS: Dict[str, _RunStreamJob] = {}
```

`estorides_core/discoverer.py` line 181:
```python
DISCOVER_JOBS: Dict[str, DiscoverJob] = {}
```

Neither dictionary has any eviction, TTL, or size cap. Jobs are added but never removed. The `_RunStreamJob` contains a `BufferedEventSink` (line 100):
```python
self.sink = BufferedEventSink(STREAM.sse_buffer_cap)
```

`BufferedEventSink` stores events in a Python list (confirmed in `pivot_engine.py`). With `sse_buffer_cap=2000` events and a conservative 1KB per event, each job consumes ~2 MB. At 30 new jobs/min, that is 60 MB/min of new memory, never freed.

## Why this matters
A single IP running at the rate limit can consume 60 MB of RAM per minute. In 30 minutes, 1.8 GB of RAM is consumed, causing OOM kills on typical deployments. The `api_run_stream_start` endpoint is rate-limited, but the rate limit is per-IP, per-minute — an attacker with multiple IPs or across the multi-worker bypass window can create jobs much faster.

## Attack or failure scenario
1. Attacker uses 10 IP addresses (easily obtained from Tor exit nodes or cloud VMs).
2. Each IP creates 30 jobs/min via `/api/run/stream/start`.
3. 300 new jobs per minute, each consuming up to 2 MB = 600 MB/min.
4. Server OOM kills gunicorn workers within minutes.

## Root cause
Job lifecycle management was not implemented. The design assumed a single operator who would view each job's stream to completion. The cleanup step was deferred and never added.

## Recommended fix
1. Implement TTL-based eviction: after a job has been in `done`/`error`/`stopped` state for more than a configurable TTL (e.g. 10 minutes), remove it from the dictionary.
2. Implement a size cap: if the number of jobs exceeds a maximum (e.g. 100), evict the oldest completed jobs first.
3. Use a `collections.OrderedDict` or a bounded LRU cache for both dictionaries.
4. Run the eviction in a background thread or as a `@app.before_request` check.

Example eviction snippet:
```python
MAX_JOBS = 200
TTL_SECONDS = 600

def _evict_old_jobs() -> None:
    now = time.time()
    to_remove = [jid for jid, j in RUN_STREAM_JOBS.items()
                 if j.done and (now - j.started_at) > TTL_SECONDS]
    if len(RUN_STREAM_JOBS) > MAX_JOBS:
        to_remove += sorted(RUN_STREAM_JOBS, key=lambda k: RUN_STREAM_JOBS[k].started_at)[:len(RUN_STREAM_JOBS) - MAX_JOBS]
    for jid in to_remove:
        del RUN_STREAM_JOBS[jid]
```

## Acceptance criteria
- `RUN_STREAM_JOBS` and `DISCOVER_JOBS` are bounded to a configurable maximum size.
- Completed jobs are evicted after a configurable TTL.
- A load test demonstrates that memory usage stabilises (does not grow unboundedly) under sustained job creation.
- A unit test verifies that creating `MAX_JOBS + 1` jobs causes eviction of the oldest.

## Suggested labels
security, reliability, production-readiness

## Priority
P1

## Severity
High — Unbounded in-memory job accumulation enables memory exhaustion (OOM) from sustained job creation at the rate-limited pace.

## Confidence
Confirmed — the dictionaries have no eviction logic; the `BufferedEventSink` holds events in a bounded Python list, but the job dictionary itself is unbounded.
