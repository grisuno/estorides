"""
estorides_core.cases
====================
Run persistence — every intelligence query becomes a "case" that
survives across sessions.

Why a separate module:
  The orchestrator already writes a JSONL dataset line per run, but
  that format is append-only and has no indexes. We need cheap
  lookups by query, by entity, by date range, and a way to
  reconstruct a previous case (observations + entities + graph +
  analysis) without grepping a file.

Schema:

  cases         (id, query, query_type, created_at, status, notes,
                source_count, obs_count, entity_count, mitre_json,
                analysis_json, kg_path)
  observations  (id, case_id, source, category, parser, parsed_json,
                raw_text, meta_json, ontology_json, mitre_json)
  case_entities (case_id, type, value, source, confidence, sources_json)

`cases` is the parent; observations and case_entities have FK to it
via ON DELETE CASCADE so dropping a case cleans up.

Public surface:

    store = CaseStore()
    case_id = store.create_case(query, query_type)
    store.add_observation(case_id, observation)
    store.add_entities(case_id, entities)
    store.finalise(case_id, analysis, kg_path, status="ok")
    case = store.get_case(case_id)
    rows = store.search_cases(query_substring, limit=20)
"""
from __future__ import annotations

import json
import logging
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

from .config import DATA_DIR

log = logging.getLogger("estorides.cases")

# DB lives next to the cache: data/estorides_cases.sqlite.
DB_PATH: Path = Path(
    __import__("os").environ.get(
        "ESTORIDES_CASES_DB", str(DATA_DIR / "estorides_cases.sqlite")
    )
)


# ---------------------------------------------------------------------------
# DDL
# ---------------------------------------------------------------------------
_DDL: List[str] = [
    """CREATE TABLE IF NOT EXISTS cases (
        id              TEXT PRIMARY KEY,
        query           TEXT NOT NULL,
        query_type      TEXT,
        created_at      REAL NOT NULL,
        finalised_at    REAL,
        status          TEXT NOT NULL DEFAULT 'pending',
        notes           TEXT,
        source_count    INTEGER DEFAULT 0,
        obs_count       INTEGER DEFAULT 0,
        entity_count    INTEGER DEFAULT 0,
        mitre_json      TEXT,
        analysis_json   TEXT,
        kg_path         TEXT
    )""",
    "CREATE INDEX IF NOT EXISTS idx_cases_created ON cases(created_at DESC)",
    "CREATE INDEX IF NOT EXISTS idx_cases_query ON cases(query)",
    "CREATE INDEX IF NOT EXISTS idx_cases_qtype ON cases(query_type)",
    """CREATE TABLE IF NOT EXISTS observations (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id         TEXT NOT NULL,
        source          TEXT NOT NULL,
        category        TEXT,
        parser          TEXT,
        parsed_json     TEXT,
        raw_excerpt     TEXT,
        meta_json       TEXT,
        ontology_json   TEXT,
        mitre_json      TEXT,
        FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE CASCADE
    )""",
    "CREATE INDEX IF NOT EXISTS idx_obs_case ON observations(case_id)",
    "CREATE INDEX IF NOT EXISTS idx_obs_source ON observations(source)",
    """CREATE TABLE IF NOT EXISTS case_entities (
        case_id         TEXT NOT NULL,
        type            TEXT NOT NULL,
        value           TEXT NOT NULL,
        source          TEXT,
        confidence      REAL DEFAULT 1.0,
        sources_json    TEXT,
        PRIMARY KEY(case_id, type, value),
        FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE CASCADE
    )""",
    "CREATE INDEX IF NOT EXISTS idx_ent_value ON case_entities(value)",
    "CREATE INDEX IF NOT EXISTS idx_ent_type_value ON case_entities(type, value)",
]


class CaseStore:
    """Thread-safe SQLite-backed case repository.

    SQLite is plenty for OSINT-sized workloads (a few thousand cases
    per operator per month) and avoids a separate service. The
    underlying file is shared with the cache if you point both env
    vars at the same path; otherwise we live in `estorides_cases.sqlite`
    next to it."""

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = Path(path) if path else DB_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        # check_same_thread=False: SQLite is in serialised mode by
        # default in Python 3.12+, and we hold our own lock for
        # cross-thread write ordering.
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
    def _tx(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            try:
                self._conn.execute("BEGIN")
                yield self._conn
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    # ----------------------------------------------------------- write API
    def create_case(
        self,
        query: str,
        query_type: str = "",
        notes: str = "",
    ) -> str:
        """Open a new case and return its id (8-char slug)."""
        case_id = uuid.uuid4().hex[:8]
        with self._tx() as c:
            c.execute(
                "INSERT INTO cases(id, query, query_type, created_at, status, notes) "
                "VALUES (?, ?, ?, ?, 'pending', ?)",
                (case_id, query, query_type, time.time(), notes),
            )
        return case_id

    def add_observation(self, case_id: str, observation: Dict[str, Any]) -> None:
        """Persist a single observation row.

        The full parsed/raw payload is JSON-encoded so we can
        reconstruct the run later without re-running the source."""
        parsed = observation.get("parsed")
        raw = observation.get("raw")
        # Truncate raw to keep the DB lean; the parsed view is the
        # useful shape and the raw is just for forensics.
        raw_excerpt: Optional[str] = None
        if raw is not None:
            try:
                raw_excerpt = json.dumps(raw, ensure_ascii=False, default=str)[:4000]
            except (TypeError, ValueError):
                raw_excerpt = str(raw)[:4000]
        with self._tx() as c:
            c.execute(
                "INSERT INTO observations"
                "(case_id, source, category, parser, parsed_json, raw_excerpt, "
                " meta_json, ontology_json, mitre_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    case_id,
                    observation.get("source", ""),
                    observation.get("category", ""),
                    observation.get("parser", ""),
                    json.dumps(parsed, ensure_ascii=False, default=str) if parsed is not None else None,
                    raw_excerpt,
                    json.dumps(observation.get("meta") or {}, ensure_ascii=False, default=str),
                    json.dumps(observation.get("ontology") or {}, ensure_ascii=False, default=str),
                    json.dumps(observation.get("mitre") or {}, ensure_ascii=False, default=str),
                ),
            )

    def add_entities(self, case_id: str, entities: Iterable[Dict[str, Any]]) -> None:
        """Persist the merged entity list. Duplicate (type, value) rows
        for the same case are silently ignored — the PK is the guard."""
        rows = []
        for e in entities:
            rows.append((
                case_id,
                e.get("type", ""),
                e.get("value", ""),
                e.get("source", ""),
                float(e.get("confidence", 1.0)),
                json.dumps(e.get("sources") or [], ensure_ascii=False),
            ))
        if not rows:
            return
        with self._tx() as c:
            c.executemany(
                "INSERT OR IGNORE INTO case_entities"
                "(case_id, type, value, source, confidence, sources_json) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                rows,
            )

    def finalise(
        self,
        case_id: str,
        analysis: Optional[Dict[str, Any]] = None,
        kg_path: Optional[str] = None,
        mitre: Optional[Dict[str, Any]] = None,
        source_count: int = 0,
        obs_count: int = 0,
        entity_count: int = 0,
        status: str = "ok",
    ) -> None:
        with self._tx() as c:
            c.execute(
                "UPDATE cases SET finalised_at=?, status=?, "
                "analysis_json=?, kg_path=?, mitre_json=?, "
                "source_count=?, obs_count=?, entity_count=? "
                "WHERE id=?",
                (
                    time.time(),
                    status,
                    json.dumps(analysis, ensure_ascii=False, default=str) if analysis is not None else None,
                    kg_path,
                    json.dumps(mitre, ensure_ascii=False, default=str) if mitre is not None else None,
                    source_count,
                    obs_count,
                    entity_count,
                    case_id,
                ),
            )

    def delete_case(self, case_id: str) -> None:
        with self._tx() as c:
            c.execute("DELETE FROM cases WHERE id=?", (case_id,))

    # ----------------------------------------------------------- read API
    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            row = self._conn.execute(
                "SELECT id, query, query_type, created_at, finalised_at, status, "
                "notes, source_count, obs_count, entity_count, "
                "mitre_json, analysis_json, kg_path "
                "FROM cases WHERE id=?",
                (case_id,),
            ).fetchone()
        if not row:
            return None
        return self._row_to_case(row)

    def list_observations(self, case_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT id, source, category, parser, parsed_json, raw_excerpt, "
                "meta_json, ontology_json, mitre_json "
                "FROM observations WHERE case_id=? ORDER BY id",
                (case_id,),
            ).fetchall()
        out = []
        for r in rows:
            out.append({
                "id": r[0],
                "source": r[1],
                "category": r[2],
                "parser": r[3],
                "parsed": self._safe_json(r[4]),
                "raw_excerpt": r[5],
                "meta": self._safe_json(r[6]),
                "ontology": self._safe_json(r[7]),
                "mitre": self._safe_json(r[8]),
            })
        return out

    def list_entities(self, case_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT type, value, source, confidence, sources_json "
                "FROM case_entities WHERE case_id=? ORDER BY type, value",
                (case_id,),
            ).fetchall()
        return [
            {
                "type": r[0], "value": r[1], "source": r[2],
                "confidence": r[3], "sources": self._safe_json(r[4]) or [],
            }
            for r in rows
        ]

    def search_cases(
        self,
        query_substring: str = "",
        limit: int = 20,
        query_type: str = "",
    ) -> List[Dict[str, Any]]:
        """Lightweight case search. LIKE on `query` (not indexed, but
        acceptable for the OSINT scale of a few thousand cases)."""
        sql = (
            "SELECT id, query, query_type, created_at, finalised_at, status, "
            "notes, source_count, obs_count, entity_count, "
            "mitre_json, analysis_json, kg_path "
            "FROM cases"
        )
        clauses: List[str] = []
        params: List[Any] = []
        if query_substring:
            clauses.append("query LIKE ?")
            params.append(f"%{query_substring}%")
        if query_type:
            clauses.append("query_type = ?")
            params.append(query_type)
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(int(limit))
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_case(r) for r in rows]

    def search_by_entity(
        self,
        ent_type: str,
        value: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Find every case that observed a given entity.

        This is the cross-run memory query — the heart of "have I
        seen this before?"."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT c.id, c.query, c.query_type, c.created_at, c.status, "
                "c.source_count, c.obs_count, c.entity_count "
                "FROM case_entities e JOIN cases c ON c.id = e.case_id "
                "WHERE e.type = ? AND lower(e.value) = lower(?) "
                "ORDER BY c.created_at DESC LIMIT ?",
                (ent_type, value, int(limit)),
            ).fetchall()
        return [
            {
                "case_id": r[0], "query": r[1], "query_type": r[2],
                "created_at": r[3], "status": r[4],
                "source_count": r[5], "obs_count": r[6], "entity_count": r[7],
            }
            for r in rows
        ]

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            total = self._conn.execute("SELECT count(*) FROM cases").fetchone()[0]
            ents = self._conn.execute("SELECT count(*) FROM case_entities").fetchone()[0]
            obs = self._conn.execute("SELECT count(*) FROM observations").fetchone()[0]
        return {"cases": total, "entities": ents, "observations": obs, "db": str(self.path)}

    # ----------------------------------------------------------- helpers
    def _row_to_case(self, row: sqlite3.Row) -> Dict[str, Any]:
        return {
            "id": row[0],
            "query": row[1],
            "query_type": row[2],
            "created_at": row[3],
            "finalised_at": row[4],
            "status": row[5],
            "notes": row[6],
            "source_count": row[7],
            "obs_count": row[8],
            "entity_count": row[9],
            "mitre": self._safe_json(row[10]),
            "analysis": self._safe_json(row[11]),
            "kg_path": row[12],
        }

    @staticmethod
    def _safe_json(text: Optional[str]) -> Any:
        if not text:
            return None
        try:
            return json.loads(text)
        except (TypeError, ValueError):
            return None

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:  # noqa: BLE001
            pass


# Module-level singleton
store = CaseStore()
