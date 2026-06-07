"""
estorides_core.audit
====================
Append-only audit log + per-IP rate limiter for the web layer.

Two responsibilities:

  AuditLog
    Every API call (query, run, export) gets a JSON line appended to
    `sessions/audit.jsonl` (one line per request) with: timestamp,
    remote IP, query, sources used, observation count, status, runtime
    ms, result size. This is the compliance trail that "state level"
    platforms must produce on demand.

    The log is append-only and best-effort: a disk error never breaks
    the request, it just records the failure and moves on. Concurrent
    writers are safe via a process-level lock (we only have one web
    process in the default deployment; for multi-worker setups we'd
    switch to a queue, but the file size stays small enough that the
    current model is fine).

  RateLimiter
    Simple sliding-window rate limiter, in-memory. Default: 30 requests
    per minute per IP. Configurable via env. The window is sliding
    rather than fixed-bucket so a burst of 30 right at the boundary
    doesn't get a free second batch.

This module is dependency-free. It does NOT replace a real WAF or
production-grade rate limiter (Redis-backed, distributed). It is a
defensible default for self-hosted deployments and a starting point
that real platforms can swap out without touching the rest of the code.
"""
from __future__ import annotations

import json
import logging
import os
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Deque, Dict, Optional, Tuple

from .config import DATA_DIR

log = logging.getLogger("estorides.audit")

AUDIT_PATH: Path = DATA_DIR / "audit.jsonl"


# ---------------------------------------------------------------------- audit
@dataclass
class AuditEvent:
    timestamp: str
    event: str
    remote_ip: str
    method: str
    path: str
    query: str = ""
    sources: int = 0
    observations: int = 0
    status: str = "ok"
    runtime_ms: float = 0.0
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_jsonl(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, default=str)


class AuditLog:
    """Append-only JSONL audit log.

    Thread-safe via a process-level lock. The on-disk file is opened
    per-write so a long-running process never holds an exclusive handle
    (which would defeat any out-of-band log rotation tooling)."""

    def __init__(self, path: Path = AUDIT_PATH) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def record(self, event: AuditEvent) -> None:
        line = event.to_jsonl()
        with self._lock:
            try:
                with self.path.open("a", encoding="utf-8") as fh:
                    fh.write(line + "\n")
            except OSError as e:
                # Never let an audit write fail a user request; just log.
                log.warning("audit log write failed: %s", e)

    def query(
        self,
        event: str,
        *,
        remote_ip: str,
        method: str,
        path: str,
        query: str = "",
        sources: int = 0,
        observations: int = 0,
        status: str = "ok",
        runtime_ms: float = 0.0,
        **extra: Any,
    ) -> None:
        self.record(AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            event=event,
            remote_ip=remote_ip,
            method=method,
            path=path,
            query=query,
            sources=sources,
            observations=observations,
            status=status,
            runtime_ms=runtime_ms,
            extra=extra,
        ))


# ---------------------------------------------------------------- rate limit
class RateLimiter:
    """In-process sliding-window rate limiter.

    For a multi-worker deployment swap this for a Redis-backed
    implementation; the call sites only depend on `allow()` returning
    a bool, so the swap is local to this module.
    """

    def __init__(
        self,
        *,
        max_requests: int = 30,
        window_seconds: int = 60,
    ) -> None:
        self.max_requests = int(
            os.environ.get("ESTORIDES_RATE_LIMIT", str(max_requests))
        )
        self.window_seconds = window_seconds
        self._buckets: Dict[str, Deque[float]] = {}
        self._lock = threading.Lock()

    def allow(self, key: str) -> Tuple[bool, int]:
        """Return (allowed, retry_after_seconds).

        `retry_after_seconds` is 0 when allowed, otherwise the number of
        seconds the caller should wait before retrying.

        The configured `max_requests` is re-read from the environment on
        every call so an operator can hot-tune the limit without a
        process restart. (The window itself is stable for a process
        lifetime, which is fine for our deployment shape.)"""
        max_req = int(os.environ.get("ESTORIDES_RATE_LIMIT", str(self.max_requests)))
        now = time.monotonic()
        with self._lock:
            bucket = self._buckets.setdefault(key, deque())
            # Drop entries outside the window.
            cutoff = now - self.window_seconds
            while bucket and bucket[0] < cutoff:
                bucket.popleft()
            if len(bucket) >= max_req:
                retry = max(1, int(self.window_seconds - (now - bucket[0])))
                return False, retry
            bucket.append(now)
            return True, 0

    def reset(self, key: Optional[str] = None) -> None:
        with self._lock:
            if key is None:
                self._buckets.clear()
            else:
                self._buckets.pop(key, None)


# ---------------------------------------------------------------- module singleton
# One audit log + one rate limiter per process. Tests can monkey-patch
# `audit_log` and `rate_limiter` to inject fakes.
audit_log = AuditLog()
rate_limiter = RateLimiter()
