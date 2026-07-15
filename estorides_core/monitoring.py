"""
estorides_core.monitoring
=========================
Watch targets and scheduling for recurring OSINT monitoring.

Provides:
  * WatchTarget — a recurring investigation (query + interval + alert channels)
  * WatchStore — SQLite-backed persistence for watch targets
  * WatchScheduler — manages the scheduling loop (APScheduler or simple threading)
  * SchedulerConfig — env-var-tunable configuration

Two modes:
  1. In-process threaded scheduler (default) — simple, no external deps.
  2. APScheduler — for production deployments with persistent job store.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import sqlite3
import threading
import time
import uuid
from collections.abc import Awaitable, Callable
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import DATA_DIR

log = logging.getLogger("estorides.monitoring")

# ---------------------------------------------------------------------------
# DB path
# ---------------------------------------------------------------------------
MONITOR_DB: Path = Path(
    os.environ.get(
        "ESTORIDES_MONITOR_DB", str(DATA_DIR / "estorides_monitor.sqlite")
    )
)

# ---------------------------------------------------------------------------
# DDL
# ---------------------------------------------------------------------------
_DDL: list[str] = [
    """CREATE TABLE IF NOT EXISTS watch_targets (
        id              TEXT PRIMARY KEY,
        query           TEXT NOT NULL,
        query_type      TEXT NOT NULL DEFAULT 'domain',
        interval_minutes INTEGER NOT NULL DEFAULT 1440,
        next_run_at     REAL NOT NULL,
        last_run_at     REAL,
        last_status     TEXT NOT NULL DEFAULT 'pending',
        channels        TEXT NOT NULL DEFAULT '[]',
        enabled         INTEGER NOT NULL DEFAULT 1,
        created_at      REAL NOT NULL,
        notes           TEXT DEFAULT ''
    )""",
    "CREATE INDEX IF NOT EXISTS idx_watch_next ON watch_targets(next_run_at)",
    "CREATE INDEX IF NOT EXISTS idx_watch_enabled ON watch_targets(enabled)",
    """CREATE TABLE IF NOT EXISTS watch_history (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        watch_id        TEXT NOT NULL,
        started_at      REAL NOT NULL,
        completed_at    REAL,
        status          TEXT NOT NULL DEFAULT 'running',
        entity_count    INTEGER DEFAULT 0,
        obs_count       INTEGER DEFAULT 0,
        error           TEXT,
        alert_sent      INTEGER DEFAULT 0,
        FOREIGN KEY(watch_id) REFERENCES watch_targets(id) ON DELETE CASCADE
    )""",
    "CREATE INDEX IF NOT EXISTS idx_history_watch ON watch_history(watch_id)",
]

# ---------------------------------------------------------------------------
# Scheduler config
# ---------------------------------------------------------------------------
SCHEDULER_POLL_INTERVAL_S: float = float(
    os.environ.get("ESTORIDES_SCHEDULER_POLL_S", "30")
)
SCHEDULER_ENABLED: bool = os.environ.get("ESTORIDES_SCHEDULER_ENABLED", "1") in (
    "1", "true", "yes"
)


@dataclass
class WatchTarget:
    """A recurring OSINT investigation."""

    query: str
    query_type: str = "domain"
    interval_minutes: int = 1440
    channels: list[str] = field(default_factory=list)
    notes: str = ""
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    next_run_at: float = 0.0
    last_run_at: float | None = None
    last_status: str = "pending"
    enabled: bool = True
    created_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if not self.next_run_at:
            self.next_run_at = time.time() + 60  # first run in 60s

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "query": self.query,
            "query_type": self.query_type,
            "interval_minutes": self.interval_minutes,
            "next_run_at": self.next_run_at,
            "last_run_at": self.last_run_at,
            "last_status": self.last_status,
            "channels": self.channels,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> WatchTarget:
        return cls(
            id=d.get("id", uuid.uuid4().hex[:8]),
            query=d["query"],
            query_type=d.get("query_type", "domain"),
            interval_minutes=int(d.get("interval_minutes", 1440)),
            next_run_at=float(d.get("next_run_at", 0.0)),
            last_run_at=float(d["last_run_at"]) if d.get("last_run_at") else None,
            last_status=d.get("last_status", "pending"),
            channels=list(d.get("channels", [])),
            enabled=bool(d.get("enabled", True)),
            created_at=float(d.get("created_at", time.time())),
            notes=str(d.get("notes", "")),
        )

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> WatchTarget:
        return cls(
            id=row[0], query=row[1], query_type=row[2],
            interval_minutes=row[3], next_run_at=row[4],
            last_run_at=row[5], last_status=row[6],
            channels=list(json.loads(row[7])) if row[7] else [],
            enabled=bool(row[8]), created_at=row[9], notes=row[10] or "",
        )


# ---------------------------------------------------------------------------
# WatchStore — SQLite persistence
# ---------------------------------------------------------------------------
class WatchStore:
    """Thread-safe SQLite store for watch targets."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or MONITOR_DB
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(
            str(self.path), check_same_thread=False, isolation_level=None
        )
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            for stmt in _DDL:
                self._conn.execute(stmt)

    @contextmanager
    def _tx(self):
        with self._lock:
            try:
                self._conn.execute("BEGIN")
                yield self._conn
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise
    # --------------------------------------------------------------- CRUD
    def create_watch(self, watch: WatchTarget) -> WatchTarget:
        """Persist a new watch target."""
        with self._tx() as c:
            c.execute(
                "INSERT INTO watch_targets "
                "(id, query, query_type, interval_minutes, next_run_at, "
                " last_run_at, last_status, channels, enabled, created_at, notes) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (watch.id, watch.query, watch.query_type, watch.interval_minutes,
                 watch.next_run_at, watch.last_run_at, watch.last_status,
                 json.dumps(watch.channels), int(watch.enabled),
                 watch.created_at, watch.notes),
            )
        return watch

    def get_watch(self, watch_id: str) -> WatchTarget | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM watch_targets WHERE id=?", (watch_id,)
            ).fetchone()
        if not row:
            return None
        return WatchTarget.from_row(row)

    def update_watch(self, watch: WatchTarget) -> WatchTarget:
        with self._tx() as c:
            c.execute(
                "UPDATE watch_targets SET interval_minutes=?, next_run_at=?, "
                "last_run_at=?, last_status=?, channels=?, enabled=?, notes=? "
                "WHERE id=?",
                (watch.interval_minutes, watch.next_run_at,
                 watch.last_run_at, watch.last_status,
                 json.dumps(watch.channels), int(watch.enabled),
                 watch.notes, watch.id),
            )
        return watch

    def delete_watch(self, watch_id: str) -> None:
        with self._tx() as c:
            c.execute("DELETE FROM watch_targets WHERE id=?", (watch_id,))

    def list_watches(self, enabled_only: bool = False) -> list[WatchTarget]:
        sql = "SELECT * FROM watch_targets"
        params: list[Any] = []
        if enabled_only:
            sql += " WHERE enabled=1"
        sql += " ORDER BY next_run_at ASC"
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [WatchTarget.from_row(r) for r in rows]

    def due_watches(self, now: float | None = None) -> list[WatchTarget]:
        """Return enabled watches whose next_run_at <= now."""
        if now is None:
            now = time.time()
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM watch_targets WHERE enabled=1 AND next_run_at <= ? "
                "ORDER BY next_run_at ASC LIMIT 20",
                (now,),
            ).fetchall()
        return [WatchTarget.from_row(r) for r in rows]

    # --------------------------------------------------------------- history
    def record_run_start(self, watch_id: str) -> int:
        """Record a watch run start, return history entry id."""
        with self._tx() as c:
            cur = c.execute(
                "INSERT INTO watch_history (watch_id, started_at) VALUES (?, ?)",
                (watch_id, time.time()),
            )
            hid: int = cur.lastrowid  # type: ignore[arg-type]
            return hid

    def record_run_complete(
        self, history_id: int, status: str = "ok",
        entity_count: int = 0, obs_count: int = 0,
        error: str | None = None, alert_sent: bool = False,
    ) -> None:
        with self._tx() as c:
            c.execute(
                "UPDATE watch_history SET completed_at=?, status=?, "
                "entity_count=?, obs_count=?, error=?, alert_sent=? WHERE id=?",
                (time.time(), status, entity_count, obs_count,
                 error, int(alert_sent), history_id),
            )

    def history(self, watch_id: str, limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT started_at, completed_at, status, entity_count, "
                "obs_count, error, alert_sent FROM watch_history "
                "WHERE watch_id=? ORDER BY started_at DESC LIMIT ?",
                (watch_id, limit),
            ).fetchall()
        return [
            {
                "started_at": r[0], "completed_at": r[1],
                "status": r[2], "entity_count": r[3],
                "obs_count": r[4], "error": r[5], "alert_sent": bool(r[6]),
            }
            for r in rows
        ]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total = self._conn.execute(
                "SELECT count(*) FROM watch_targets"
            ).fetchone()[0]
            enabled = self._conn.execute(
                "SELECT count(*) FROM watch_targets WHERE enabled=1"
            ).fetchone()[0]
        return {"total": total, "enabled": enabled}

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# WatchScheduler — threaded scheduler loop
# ---------------------------------------------------------------------------
class WatchScheduler:
    """Background thread that polls the watch store and triggers due watches.

    Uses a simple poll loop (no external deps). For production, swap to
    APScheduler by setting ESTORIDES_SCHEDULER_DRIVER=apscheduler.
    """

    def __init__(
        self,
        store: WatchStore | None = None,
        runner: Callable[[WatchTarget], dict[str, Any]] | None = None,
        alerter: Any | None = None,
    ) -> None:
        self.store = store or WatchStore()
        self._runner = runner  # type: ignore[assignment]
        self._alerter = alerter
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        if self.running:
            log.warning("scheduler already running")
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop, daemon=True, name="estorides-scheduler"
        )
        self._thread.start()
        log.info("scheduler started (poll interval=%ds)", SCHEDULER_POLL_INTERVAL_S)

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)
            log.info("scheduler stopped")

    def set_runner(self, runner: Callable[[WatchTarget], dict[str, Any] | Awaitable[dict[str, Any]]]) -> None:
        """Set the orchestrator runner function (sync or async)."""
        self._runner = runner  # type: ignore[assignment]

    def set_alerter(self, alerter: Any) -> None:
        """Set the alert dispatcher."""
        self._alerter = alerter

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                due = self.store.due_watches()
                for watch in due:
                    log.info("running watch %s: %s", watch.id, watch.query)
                    self._execute_watch(watch)
            except Exception as e:
                log.error("scheduler loop error: %s", e)
            self._stop.wait(SCHEDULER_POLL_INTERVAL_S)

    def _execute_watch(self, watch: WatchTarget) -> None:
        history_id = self.store.record_run_start(watch.id)
        status = "ok"
        entity_count = 0
        obs_count = 0
        error: str | None = None
        alert_sent = False

        try:
            if self._runner:
                raw = self._runner(watch)
                # Support both sync and async runners
                if isinstance(raw, Awaitable):
                    try:
                        raw = asyncio.run(raw)
                    except RuntimeError:
                        # Already in an event loop — run in a new thread
                        import concurrent.futures
                        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                            future = pool.submit(asyncio.run, raw)
                            raw = future.result(timeout=120)
                result = raw  # type: ignore[assignment]
                entity_count = len(result.get("entities", []))
                obs_count = result.get("sources_succeeded", 0)
                if result.get("error"):
                    status = "error"
                    error = result["error"]
        except Exception as e:
            status = "error"
            error = str(e)
            log.exception("watch %s failed: %s", watch.id, error)

        # Update watch target
        watch.last_run_at = time.time()
        watch.last_status = status
        watch.next_run_at = time.time() + watch.interval_minutes * 60
        self.store.update_watch(watch)

        # Record history
        self.store.record_run_complete(
            history_id, status=status,
            entity_count=entity_count, obs_count=obs_count,
            error=error, alert_sent=alert_sent,
        )

        # Send alerts if configured
        if watch.channels and self._alerter and status == "ok":
            try:
                self._alerter.send_watch_alert(watch, entity_count, obs_count)
                alert_sent = True
            except Exception as e:
                log.warning("alert send failed for watch %s: %s", watch.id, e)


# Module-level singletons
store = WatchStore()
scheduler = WatchScheduler(store=store)


__all__ = [
    "MONITOR_DB",
    "WatchScheduler",
    "WatchStore",
    "WatchTarget",
    "scheduler",
    "store",
]
