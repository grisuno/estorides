"""
estorides_core.entity_store
===========================
Cross-run canonical identity store.

The resolver in :mod:`estorides_core.entity_resolution` produces stable
canonical ids *within* a run from content-addressed normalised forms. That
is not enough for state-level work, where the same target recurs across
investigations: a person seen as ``Vladimir Putin`` in one case and only as
``Владимир Путин`` in the next must keep one identifier so the graph,
watchlists, and case history all join on it.

This store closes that gap. It persists every canonical entity and *all*
the surface forms (aliases) ever observed for it, each indexed by its
normalised key. On a later run the resolver asks :meth:`lookup` whether any
of a freshly computed entity's normalised forms — its own or any of its
aliases — has been seen before, and if so adopts the established canonical
id instead of minting a new one.

It is a thin SQLite layer, matching :mod:`estorides_core.cases`: WAL mode,
a single serialised connection behind a lock, and a fail-soft contract —
the resolver treats any store error as "no prior knowledge" and proceeds,
so a read-only or missing data directory degrades to in-run resolution
rather than breaking a run.
"""
from __future__ import annotations

import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator, List, Optional

from .config import ENTITY_STORE_PATH
from .entity_resolution import CanonicalEntity, normalize_value

_DDL: tuple = (
    """CREATE TABLE IF NOT EXISTS entities (
        canonical_id  TEXT PRIMARY KEY,
        type          TEXT NOT NULL,
        value         TEXT NOT NULL,
        normalized    TEXT NOT NULL,
        confidence    REAL NOT NULL DEFAULT 1.0,
        member_count  INTEGER NOT NULL DEFAULT 1,
        source_count  INTEGER NOT NULL DEFAULT 0,
        first_seen    REAL NOT NULL,
        last_seen     REAL NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS aliases (
        canonical_id     TEXT NOT NULL,
        type             TEXT NOT NULL,
        alias            TEXT NOT NULL,
        alias_normalized TEXT NOT NULL,
        PRIMARY KEY (canonical_id, alias_normalized)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_entities_norm ON entities(type, normalized)",
    "CREATE INDEX IF NOT EXISTS idx_aliases_norm ON aliases(type, alias_normalized)",
)


class EntityStore:
    """Thread-safe SQLite repository of canonical identities and aliases."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = Path(path) if path else ENTITY_STORE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(
            str(self.path), check_same_thread=False, isolation_level=None
        )
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            for stmt in _DDL:
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

    def lookup(
        self, etype: str, normalized: str, aliases: Iterable[str]
    ) -> Optional[str]:
        """Return an existing canonical id for any known form, or None.

        Checks every normalised key the entity can present — its own and
        each alias's — against both the canonical ``entities`` table and the
        ``aliases`` table. The first established id wins, so a never-before
        spelling of a known target still resolves to its prior identity.
        """
        keys: List[str] = []
        if normalized:
            keys.append(normalized)
        for alias in aliases:
            key = normalize_value(etype, alias)
            if key and key not in keys:
                keys.append(key)
        if not keys:
            return None

        placeholders = ",".join("?" for _ in keys)
        with self._lock:
            row = self._conn.execute(
                f"SELECT canonical_id FROM entities "
                f"WHERE type=? AND normalized IN ({placeholders}) LIMIT 1",
                (etype, *keys),
            ).fetchone()
            if row:
                return row[0]
            row = self._conn.execute(
                f"SELECT canonical_id FROM aliases "
                f"WHERE type=? AND alias_normalized IN ({placeholders}) LIMIT 1",
                (etype, *keys),
            ).fetchone()
            if row:
                return row[0]
        return None

    def upsert(self, entity: CanonicalEntity) -> None:
        """Persist (insert or update) a canonical entity and its aliases.

        ``first_seen`` is preserved across updates; ``last_seen``,
        ``member_count``, ``source_count``, ``value``, and ``confidence``
        track the latest resolution. Every alias is recorded with its
        normalised key so future lookups can route any surface form back to
        this id.
        """
        now = time.time()
        with self._tx() as conn:
            conn.execute(
                "INSERT INTO entities("
                "canonical_id, type, value, normalized, confidence, "
                "member_count, source_count, first_seen, last_seen) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(canonical_id) DO UPDATE SET "
                "value=excluded.value, normalized=excluded.normalized, "
                "confidence=excluded.confidence, "
                "member_count=excluded.member_count, "
                "source_count=excluded.source_count, "
                "last_seen=excluded.last_seen",
                (
                    entity.canonical_id, entity.type, entity.value,
                    entity.normalized, entity.confidence, entity.member_count,
                    len(entity.sources), now, now,
                ),
            )
            for alias in entity.aliases:
                alias_norm = normalize_value(entity.type, alias)
                if not alias_norm:
                    continue
                conn.execute(
                    "INSERT OR IGNORE INTO aliases("
                    "canonical_id, type, alias, alias_normalized) "
                    "VALUES (?, ?, ?, ?)",
                    (entity.canonical_id, entity.type, alias, alias_norm),
                )

    def stats(self) -> dict:
        """Return a one-glance summary of store size."""
        with self._lock:
            entities = self._conn.execute(
                "SELECT COUNT(*) FROM entities"
            ).fetchone()[0]
            aliases = self._conn.execute(
                "SELECT COUNT(*) FROM aliases"
            ).fetchone()[0]
        return {"entities": entities, "aliases": aliases, "db": str(self.path)}

    def close(self) -> None:
        with self._lock:
            self._conn.close()


def open_store(path: Optional[Path] = None) -> Optional[EntityStore]:
    """Open the store, returning None instead of raising on failure.

    The resolver calls this so that an unwritable or locked data directory
    degrades the cross-run identity feature to in-run-only resolution rather
    than aborting an investigation.
    """
    try:
        return EntityStore(path)
    except Exception:  # noqa: BLE001
        return None
