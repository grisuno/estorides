"""
estorides_core.job_registry
===========================

Bounded, TTL-aware registry for in-memory job objects (RUN_STREAM_JOBS,
DISCOVER_JOBS, etc.). The plain `Dict[str, _Job]` pattern that the project
shipped with had no eviction at all — see issues #14, #20, #50 — which
let an unauthenticated caller grow server memory without bound by
repeatedly starting short-lived jobs.

Eviction policy
---------------
* **LRU by insertion order** — when the registry hits `max_size`, the
  oldest job is dropped. Python 3.7+ dicts guarantee insertion order so
  `next(iter(reg))` is the oldest.
* **TTL** — every job has a `created_at`; a sweep on every `register()`
  drops jobs older than `ttl_seconds`. Cheap when the set is small, and
  a sweep is unnecessary when the set is empty or the entries are
  fresh, so the worst-case extra cost is `O(n)` per call, which is
  dominated by the per-call `register()` itself.

Thread safety
-------------
The Flask request handlers that touch these registries run in worker
threads (gunicorn forks, multi-worker wsgi). The `register()` /
`get()` / `evict_expired()` / `pop()` methods hold a single
`threading.Lock` so a sweep and a `get()` cannot race. The cost is
the lock acquire on every call, which is negligible compared to the
JSON serialisation that follows.
"""
from __future__ import annotations

import threading
import time
from typing import Generic, TypeVar

V = TypeVar("V")


class BoundedJobRegistry(Generic[V]):
    """A dict-like registry with size and time bounds.

    `max_size` and `ttl_seconds` are read at construction and not
    mutated — the registry is "configured once, used many times",
    which matches how the web app's STREAM config is loaded at
    import time.
    """

    def __init__(self, *, max_size: int, ttl_seconds: float) -> None:
        if max_size < 1:
            raise ValueError("max_size must be >= 1")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")
        self._max_size = max_size
        self._ttl = float(ttl_seconds)
        self._items: dict[str, tuple[float, V]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ core
    def register(self, key: str, value: V) -> V:
        """Insert (or replace) a job, evicting expired and overflow entries.

        Returns the value so the caller can use it inline:
            job = registry.register("abc", _RunStreamJob(...))
        """
        now = time.time()
        with self._lock:
            self._evict_expired_locked(now)
            if key in self._items:
                # Replace in place to keep insertion order stable; the
                # existing job was the most-recently-touched anyway.
                self._items[key] = (now, value)
            else:
                self._items[key] = (now, value)
                while len(self._items) > self._max_size:
                    oldest = next(iter(self._items))
                    self._items.pop(oldest, None)
        return value

    def get(self, key: str) -> V | None:
        """Return the value for `key` or None. Refreshes the LRU order."""
        with self._lock:
            entry = self._items.get(key)
            if entry is None:
                return None
            ts, value = entry
            if time.time() - ts > self._ttl:
                self._items.pop(key, None)
                return None
            # Move-to-end: re-insert to mark as recently used.
            self._items.pop(key, None)
            self._items[key] = (ts, value)
            return value

    def pop(self, key: str) -> V | None:
        """Remove and return the value for `key`, or None."""
        with self._lock:
            entry = self._items.pop(key, None)
            return None if entry is None else entry[1]

    def keys(self) -> list[str]:
        with self._lock:
            return list(self._items.keys())

    def values(self) -> list[V]:
        with self._lock:
            return [v for _, v in self._items.values()]

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)

    def evict_expired(self) -> int:
        """Sweep and drop TTL-expired entries. Returns the number dropped."""
        with self._lock:
            return self._evict_expired_locked(time.time())

    # ---------------------------------------------------------------- helpers
    def _evict_expired_locked(self, now: float) -> int:
        dropped = 0
        for k in list(self._items.keys()):
            ts, _ = self._items[k]
            if now - ts > self._ttl:
                self._items.pop(k, None)
                dropped += 1
        return dropped
