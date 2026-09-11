"""
estorides_core.sqlite_store
===========================
Shared plumbing for the hand-rolled SQLite stores.

Four stores (`monitoring.WatchStore`, `cases.CaseStore`,
`entity_store.EntityStore`, `fusion_store.FusionStore`) used to carry
byte-identical copies of:

  * `__init__` — mkdir + lock + `sqlite3.connect(check_same_thread=False,
    isolation_level=None)` + WAL/foreign-keys pragmas + schema init;
  * `_init_schema` — execute every DDL statement under the lock;
  * `_tx` — `BEGIN` / `COMMIT` / `ROLLBACK` inside the lock;
  * `close` — swallow-and-close.

This module is the single source of truth for that boilerplate. A store
subclasses :class:`SqliteStore`, declares `_DDL` and `_DEFAULT_PATH`, and
overrides only its own queries.

Also exports :class:`DictMixin` for the 29 dataclasses whose `to_dict`
was literally `asdict(self)`.
"""
from __future__ import annotations

import sqlite3
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from typing import Any, ClassVar, cast


class SqliteStore:
    """Thread-safe SQLite base: one serialised connection behind a lock.

    Contract:
      * ``_DDL``          — list/tuple of schema statements, executed once.
      * ``_DEFAULT_PATH`` — path used when the constructor gets ``None``.
      * ``_PRAGMAS``      — connection pragmas applied before schema init.
    """

    _DDL: ClassVar[tuple[str, ...] | list[str]] = ()
    _DEFAULT_PATH: ClassVar[Path | None] = None
    _PRAGMAS: ClassVar[tuple[str, ...]] = (
        "PRAGMA journal_mode=WAL",
        "PRAGMA foreign_keys=ON",
    )

    def __init__(self, path: Path | None = None) -> None:
        resolved = Path(path) if path else self._DEFAULT_PATH
        if resolved is None:
            raise ValueError("SqliteStore requires a path or _DEFAULT_PATH")
        self.path: Path = resolved
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        # check_same_thread=False: SQLite is in serialised mode by default in
        # Python 3.12+; we hold our own lock for cross-thread write ordering.
        self._conn = sqlite3.connect(
            str(self.path), check_same_thread=False, isolation_level=None
        )
        for pragma in self._PRAGMAS:
            self._conn.execute(pragma)
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            for stmt in self._DDL:
                self._conn.execute(stmt)

    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            try:
                self._conn.execute("BEGIN")
                yield self._conn
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    def close(self) -> None:
        with self._lock:
            try:
                self._conn.close()
            except Exception:  # noqa: S110 - closing an already-closed DB is fine
                pass


class DictMixin:
    """`to_dict()` for dataclasses that map 1:1 to a JSON object."""

    def to_dict(self) -> dict[str, Any]:
        # Mypy cannot prove `self` is a dataclass instance; every subclass
        # is one by construction (the mixin's only contract), so this is
        # safe at runtime. `asdict` recurses into nested dataclasses.
        return asdict(cast(Any, self))


__all__ = ["DictMixin", "SqliteStore"]
