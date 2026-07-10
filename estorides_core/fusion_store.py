"""
estorides_core.fusion_store
===========================
The data-fusion datastore — the single place where everything every
source (loaded from the YAML catalogue) ever produced is fused, cross-run,
into one queryable intelligence picture.

Why this exists
---------------
The case store (:mod:`estorides_core.cases`) keeps a *per-run silo*: each
investigation writes its own copy of the observations and entities it saw,
keyed by ``case_id``. The same real-world entity seen across fifty runs
becomes fifty rows, and nothing in the relational store answers "show me
everything we know about X, from every source, across every case".

The fusion store closes that gap. It is the relational analogue of the
Kùzu graph: a normalised, deduplicated, source-attributed fact base that
accumulates across runs. The fusion is provenance-preserving — when two
sources corroborate the same entity or property, the record is merged but
*every* contributing source is retained, so confidence is grounded in how
many independent feeds agree.

Schema (five tables)
--------------------
  fusion_sources         the YAML source catalogue, with fetch counters
  fusion_entities        canonical, cross-run, deduplicated entities
  fusion_entity_sources  which sources corroborated each entity (provenance)
  fusion_observations    every source response, fused across runs
  fusion_properties      attribute key/value per entity, attributed to source
  fusion_relationships   edges between entities, attributed to source

Entity identity
---------------
Each entity gets a deterministic id, ``sha1(type + ":" + normalized)``,
so the *same* entity computed in two different runs lands on the *same*
row without coordination. The resolver's ``canonical_id`` is recorded
alongside for cross-reference but is never the dedup key, so a resolver
that mints a fresh id per run can never fork an entity in the fusion store.

Operational contract
---------------------
Mirrors :mod:`estorides_core.cases` and :mod:`estorides_core.entity_store`:
WAL mode, one serialised connection behind a lock, and fail-soft — every
public write swallows its own errors and the orchestrator treats the whole
subsystem as best-effort, so a read-only or missing data directory degrades
to "no fusion" rather than breaking a run.
"""
from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

from .config import FUSION_DB_PATH
from .reliability_scoring import (
    ConfidenceInput,
    Credibility,
    DEFAULT_HALF_LIFE_DAYS,
    compute_confidence,
    merge_confidence,
    reliability_from_name,
    source_type_from_name,
)

try:
    from .entity_resolution import normalize_value
except Exception:  # noqa: BLE001 — resolver is optional; fall back to casefold
    def normalize_value(etype: str, value: str) -> str:  # type: ignore[misc]
        return (value or "").strip().lower()

log = logging.getLogger("estorides.fusion")

# Edge relations that are pure graph plumbing rather than analytic facts.
# They are skipped when mirroring the knowledge graph so the fusion store
# holds only relationships an analyst would pivot on.
_NON_FUSION_RELATIONS: frozenset = frozenset({"observed_by", "co_occurs", "mentions"})

# Cap on how many flat scalar properties a single observation contributes,
# so one pathological source returning a thousand-key blob cannot dominate
# an entity's property set.
_MAX_PROPS_PER_OBSERVATION: int = 64

# Cap on a single fused property value's length. Anything longer is a blob,
# not an attribute, and belongs in the observation payload instead.
_MAX_PROPERTY_VALUE_LEN: int = 500


_DDL: List[str] = [
    """CREATE TABLE IF NOT EXISTS fusion_sources (
        name          TEXT PRIMARY KEY,
        category      TEXT,
        description   TEXT,
        parser        TEXT,
        contact       TEXT,
        requires_key  INTEGER DEFAULT 0,
        first_seen    REAL NOT NULL,
        last_seen     REAL NOT NULL,
        fetch_count   INTEGER DEFAULT 0,
        ok_count      INTEGER DEFAULT 0
    )""",
    """CREATE TABLE IF NOT EXISTS fusion_entities (
        id                TEXT PRIMARY KEY,
        type              TEXT NOT NULL,
        value             TEXT NOT NULL,
        normalized        TEXT NOT NULL,
        canonical_id      TEXT,
        confidence        REAL DEFAULT 1.0,
        source_count      INTEGER DEFAULT 0,
        observation_count INTEGER DEFAULT 0,
        case_count        INTEGER DEFAULT 0,
        first_seen        REAL NOT NULL,
        last_seen         REAL NOT NULL,
        UNIQUE(type, normalized)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_fent_type ON fusion_entities(type)",
    "CREATE INDEX IF NOT EXISTS idx_fent_norm ON fusion_entities(type, normalized)",
    "CREATE INDEX IF NOT EXISTS idx_fent_value ON fusion_entities(value)",
    "CREATE INDEX IF NOT EXISTS idx_fent_seen ON fusion_entities(last_seen DESC)",
    """CREATE TABLE IF NOT EXISTS fusion_entity_sources (
        entity_id   TEXT NOT NULL,
        source      TEXT NOT NULL,
        first_seen  REAL NOT NULL,
        last_seen   REAL NOT NULL,
        seen_count  INTEGER DEFAULT 1,
        PRIMARY KEY (entity_id, source),
        FOREIGN KEY (entity_id) REFERENCES fusion_entities(id) ON DELETE CASCADE
    )""",
    "CREATE INDEX IF NOT EXISTS idx_fes_source ON fusion_entity_sources(source)",
    """CREATE TABLE IF NOT EXISTS fusion_observations (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        query         TEXT,
        query_type    TEXT,
        source        TEXT NOT NULL,
        category      TEXT,
        parser        TEXT,
        status        TEXT,
        parsed_json   TEXT,
        meta_json     TEXT,
        ontology_json TEXT,
        case_id       TEXT,
        observed_at   REAL NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_fobs_source ON fusion_observations(source)",
    "CREATE INDEX IF NOT EXISTS idx_fobs_query ON fusion_observations(query)",
    "CREATE INDEX IF NOT EXISTS idx_fobs_seen ON fusion_observations(observed_at DESC)",
    """CREATE TABLE IF NOT EXISTS fusion_properties (
        entity_id   TEXT NOT NULL,
        key         TEXT NOT NULL,
        value       TEXT NOT NULL,
        source      TEXT,
        confidence  REAL DEFAULT 1.0,
        observed_at REAL NOT NULL,
        PRIMARY KEY (entity_id, key, value, source),
        FOREIGN KEY (entity_id) REFERENCES fusion_entities(id) ON DELETE CASCADE
    )""",
    "CREATE INDEX IF NOT EXISTS idx_fprop_entity ON fusion_properties(entity_id)",
    "CREATE INDEX IF NOT EXISTS idx_fprop_key ON fusion_properties(key, value)",
    """CREATE TABLE IF NOT EXISTS fusion_relationships (
        src_id      TEXT NOT NULL,
        relation    TEXT NOT NULL,
        dst_id      TEXT NOT NULL,
        source      TEXT,
        confidence  REAL DEFAULT 1.0,
        observed_at REAL NOT NULL,
        PRIMARY KEY (src_id, relation, dst_id, source)
    )""",
    "CREATE INDEX IF NOT EXISTS idx_frel_src ON fusion_relationships(src_id)",
    "CREATE INDEX IF NOT EXISTS idx_frel_dst ON fusion_relationships(dst_id)",
]


def entity_id(etype: str, value: str, normalized: Optional[str] = None) -> str:
    """Deterministic, run-independent id for an entity.

    Derived from the type and the normalised value so the same real-world
    entity always hashes to the same id no matter which run or source first
    produced it — the property that makes cross-run fusion automatic.
    """
    norm = normalized if normalized is not None else normalize_value(etype, value)
    if not norm:
        norm = (value or "").strip().lower()
    return hashlib.sha1(f"{etype}:{norm}".encode("utf-8")).hexdigest()[:16]


class FusionStore:
    """Thread-safe SQLite-backed fusion datastore.

    One serialised connection guarded by a lock, WAL journalling, and
    ``ON DELETE CASCADE`` foreign keys so dropping an entity reaps its
    provenance, properties and edges.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        self.path = Path(path) if path else FUSION_DB_PATH
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
    def _tx(self) -> Iterator[sqlite3.Connection]:
        with self._lock:
            try:
                self._conn.execute("BEGIN")
                yield self._conn
                self._conn.execute("COMMIT")
            except Exception:
                self._conn.execute("ROLLBACK")
                raise

    @staticmethod
    def _ensure_entity_stub(conn: sqlite3.Connection, etype: str, value: str) -> str:
        """Insert a minimal entity row if absent and return its id.

        Used for relationship endpoints (a country, an ASN, a port) that no
        entity-extraction pass produced, so an edge is always navigable from
        both ends. Runs inside the caller's transaction; never overwrites an
        already-fused entity (``INSERT OR IGNORE``)."""
        norm = normalize_value(etype, value) or value.strip().lower()
        eid = entity_id(etype, value, norm)
        now = time.time()
        conn.execute(
            "INSERT OR IGNORE INTO fusion_entities("
            "id, type, value, normalized, canonical_id, confidence, "
            "source_count, observation_count, case_count, first_seen, last_seen) "
            "VALUES (?, ?, ?, ?, '', 1.0, 0, 0, 0, ?, ?)",
            (eid, etype, value, norm, now, now),
        )
        return eid

    # ------------------------------------------------------------- catalogue
    def register_sources(self, sources: Iterable[Dict[str, Any]]) -> None:
        """Mirror the YAML source catalogue into the store.

        Idempotent: an existing source keeps its ``first_seen`` and its
        accumulated counters; only the descriptive columns are refreshed so
        the catalogue tracks edits to the YAML without losing fetch history.
        """
        now = time.time()
        rows = []
        for s in sources:
            name = s.get("name")
            if not name:
                continue
            rows.append((
                name,
                s.get("category", ""),
                s.get("description", ""),
                s.get("parser", ""),
                s.get("contact", "none"),
                1 if s.get("requires_key") else 0,
                now, now,
            ))
        if not rows:
            return
        with self._tx() as c:
            c.executemany(
                "INSERT INTO fusion_sources("
                "name, category, description, parser, contact, requires_key, "
                "first_seen, last_seen) VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(name) DO UPDATE SET "
                "category=excluded.category, description=excluded.description, "
                "parser=excluded.parser, contact=excluded.contact, "
                "requires_key=excluded.requires_key, last_seen=excluded.last_seen",
                rows,
            )

    # ----------------------------------------------------------- observations
    def add_observation(
        self,
        observation: Dict[str, Any],
        *,
        query: str = "",
        query_type: str = "",
        case_id: Optional[str] = None,
    ) -> None:
        """Fuse a single source response into the cross-run observation log
        and bump the source's fetch/ok counters."""
        meta = observation.get("meta") or {}
        status = str(meta.get("status", "")) if isinstance(meta, dict) else ""
        ok = observation.get("parsed") is not None or observation.get("raw") is not None
        source = observation.get("source", "")
        parsed = observation.get("parsed")
        now = time.time()
        with self._tx() as c:
            c.execute(
                "INSERT INTO fusion_observations("
                "query, query_type, source, category, parser, status, "
                "parsed_json, meta_json, ontology_json, case_id, observed_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    query, query_type, source,
                    observation.get("category", ""),
                    observation.get("parser", ""),
                    status,
                    json.dumps(parsed, ensure_ascii=False, default=str) if parsed is not None else None,
                    json.dumps(meta, ensure_ascii=False, default=str),
                    json.dumps(observation.get("ontology") or {}, ensure_ascii=False, default=str),
                    case_id, now,
                ),
            )
            if source:
                c.execute(
                    "UPDATE fusion_sources SET fetch_count=fetch_count+1, "
                    "ok_count=ok_count+?, last_seen=? WHERE name=?",
                    (1 if ok else 0, now, source),
                )

    # ------------------------------------------------------------- entities
    def fuse_entity(
        self,
        entity: Dict[str, Any],
        *,
        case_id: Optional[str] = None,
    ) -> str:
        """Fuse one entity into the canonical store and return its id.

        The ``(type, normalized)`` pair is the dedup key. On a repeat sighting
        the row's ``last_seen``, confidence (Bayesian merge), and observation
        count advance, and every contributing source is recorded in
        ``fusion_entity_sources`` so provenance survives the merge.

        Confidence uses the :mod:`reliability_scoring` pipeline: source
        reliability, source type hierarchy, and corroboration count are
        factored into the score instead of a raw ``MAX()``. A tertiary or
        unreliable source cannot override a well-corroborated primary one.
        """
        etype = entity.get("type", "")
        value = entity.get("value", "")
        if not etype or value in (None, ""):
            return ""
        value = str(value)
        normalized = normalize_value(etype, value) or value.strip().lower()
        eid = entity_id(etype, value, normalized)
        canonical = ""
        attrs = entity.get("attributes") or {}
        if isinstance(attrs, dict):
            canonical = str(attrs.get("canonical_id") or "")
        confidence = float(entity.get("confidence", 1.0) or 1.0)
        sources = entity.get("sources") or []
        if not sources and entity.get("source"):
            sources = [entity["source"]]
        source_name = sources[0] if sources else ""
        rel = reliability_from_name(source_name)
        st = source_type_from_name(source_name)
        n_sources = len(set(sources))
        now = time.time()
        with self._tx() as c:
            row = c.execute(
                "SELECT confidence FROM fusion_entities WHERE id=?", (eid,)
            ).fetchone()
            if row is not None:
                existing_conf = float(row[0])
                result = merge_confidence(
                    existing=existing_conf,
                    new_observation=confidence,
                    new_reliability=rel,
                    new_credibility=Credibility.CONFIRMED,
                    new_source_type=st,
                    corroboration_count=max(n_sources, 1),
                    observation_age_seconds=0.0,
                    half_life_days=DEFAULT_HALF_LIFE_DAYS,
                )
                fused_conf = result.score
                c.execute(
                    "UPDATE fusion_entities SET "
                    "value=?, "
                    "canonical_id=COALESCE(NULLIF(?,''), canonical_id), "
                    "confidence=?, observation_count=observation_count+1, "
                    "last_seen=? WHERE id=?",
                    (value, canonical, fused_conf, now, eid),
                )
            else:
                inp = ConfidenceInput(
                    source_reliability=rel,
                    credibility=Credibility.CONFIRMED,
                    source_type=st,
                    corroboration_count=n_sources,
                    observation_age_seconds=0.0,
                    base_confidence=confidence,
                )
                result = compute_confidence(inp, half_life_days=DEFAULT_HALF_LIFE_DAYS)
                fused_conf = result.score
                c.execute(
                    "INSERT INTO fusion_entities("
                    "id, type, value, normalized, canonical_id, confidence, "
                    "source_count, observation_count, case_count, first_seen, last_seen) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?)",
                    (
                        eid, etype, value, normalized, canonical, fused_conf,
                        n_sources, 1 if case_id else 0, now, now,
                    ),
                )
            for src in dict.fromkeys(sources):
                if not src:
                    continue
                c.execute(
                    "INSERT INTO fusion_entity_sources("
                    "entity_id, source, first_seen, last_seen, seen_count) "
                    "VALUES (?, ?, ?, ?, 1) "
                    "ON CONFLICT(entity_id, source) DO UPDATE SET "
                    "seen_count=seen_count+1, last_seen=excluded.last_seen",
                    (eid, src, now, now),
                )
            c.execute(
                "UPDATE fusion_entities SET source_count="
                "(SELECT COUNT(*) FROM fusion_entity_sources WHERE entity_id=?) "
                "WHERE id=?",
                (eid, eid),
            )
        return eid

    def fuse_entities(
        self,
        entities: Iterable[Dict[str, Any]],
        *,
        case_id: Optional[str] = None,
    ) -> List[str]:
        """Fuse a batch of entities, returning the list of fused ids."""
        return [
            eid for eid in (
                self.fuse_entity(e, case_id=case_id) for e in entities
            ) if eid
        ]

    def fuse_properties(
        self,
        eid: str,
        parsed: Any,
        source: str,
    ) -> int:
        """Fuse the flat scalar attributes of a parsed observation onto an
        entity, attributed to ``source``.

        Only one nesting level of scalar values is taken: deep structures are
        the observation payload's job, not an entity attribute's. Returns the
        number of properties written. The ``(entity_id, key, value, source)``
        primary key means re-running the same source is idempotent while a
        *different* source asserting the same key/value adds corroboration.
        """
        if not eid or not isinstance(parsed, dict):
            return 0
        now = time.time()
        rows = []
        for key, raw in parsed.items():
            if len(rows) >= _MAX_PROPS_PER_OBSERVATION:
                break
            if raw is None or isinstance(raw, (list, dict, tuple)):
                continue
            if isinstance(raw, bool):
                val = "true" if raw else "false"
            else:
                val = str(raw)
            val = val.strip()
            if not val or len(val) > _MAX_PROPERTY_VALUE_LEN:
                continue
            rows.append((eid, str(key)[:120], val, source, 1.0, now))
        if not rows:
            return 0
        with self._tx() as c:
            c.executemany(
                "INSERT INTO fusion_properties("
                "entity_id, key, value, source, confidence, observed_at) "
                "VALUES (?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(entity_id, key, value, source) DO UPDATE SET "
                "observed_at=excluded.observed_at",
                rows,
            )
        return len(rows)

    # ---------------------------------------------------------- relationships
    def fuse_relationship(
        self,
        src_type: str, src_value: str,
        relation: str,
        dst_type: str, dst_value: str,
        *,
        source: str = "",
        confidence: float = 1.0,
    ) -> None:
        """Fuse one directed edge between two entities, attributed to source.

        Both endpoints are resolved to their deterministic fusion ids so the
        edge joins the same canonical entities the entity table holds.
        Confidence uses the :mod:`reliability_scoring` pipeline instead of a
        raw ``MAX()``, so a low-reliability source cannot inflate the score
        of a well-corroborated edge.
        """
        if not (src_value and dst_value and relation):
            return
        sid = entity_id(src_type, str(src_value))
        did = entity_id(dst_type, str(dst_value))
        if sid == did:
            return
        rel = reliability_from_name(source)
        st = source_type_from_name(source)
        now = time.time()
        with self._tx() as c:
            self._ensure_entity_stub(c, src_type, str(src_value))
            self._ensure_entity_stub(c, dst_type, str(dst_value))
            row = c.execute(
                "SELECT confidence FROM fusion_relationships "
                "WHERE src_id=? AND relation=? AND dst_id=? AND source=?",
                (sid, relation, did, source),
            ).fetchone()
            if row is not None:
                result = merge_confidence(
                    existing=float(row[0]),
                    new_observation=float(confidence),
                    new_reliability=rel,
                    new_credibility=Credibility.CONFIRMED,
                    new_source_type=st,
                    corroboration_count=1,
                    observation_age_seconds=0.0,
                    half_life_days=DEFAULT_HALF_LIFE_DAYS,
                )
                fused_conf = result.score
                c.execute(
                    "UPDATE fusion_relationships SET "
                    "confidence=?, observed_at=? "
                    "WHERE src_id=? AND relation=? AND dst_id=? AND source=?",
                    (fused_conf, now, sid, relation, did, source),
                )
            else:
                inp = ConfidenceInput(
                    source_reliability=rel,
                    credibility=Credibility.CONFIRMED,
                    source_type=st,
                    corroboration_count=1,
                    observation_age_seconds=0.0,
                    base_confidence=float(confidence),
                )
                result = compute_confidence(inp, half_life_days=DEFAULT_HALF_LIFE_DAYS)
                fused_conf = result.score
                c.execute(
                    "INSERT INTO fusion_relationships("
                    "src_id, relation, dst_id, source, confidence, observed_at) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (sid, relation, did, source, fused_conf, now),
                )

    def fuse_graph(self, kg: Any) -> int:
        """Mirror the analytic edges of a knowledge graph into the store.

        Reads node ``type``/``value`` off each endpoint and skips the pure
        plumbing relations (``observed_by``, ``co_occurs``, ``mentions``) and
        any edge touching a ``source`` node, so only pivot-worthy facts land.
        Returns the number of edges fused. Best-effort: a malformed graph is
        swallowed rather than aborting a run.
        """
        graph = getattr(kg, "graph", None)
        if graph is None:
            return 0
        count = 0
        try:
            for u, v, attrs in graph.edges(data=True):
                relation = attrs.get("relation", "")
                if relation in _NON_FUSION_RELATIONS or not relation:
                    continue
                un = graph.nodes.get(u, {})
                vn = graph.nodes.get(v, {})
                if un.get("type") == "source" or vn.get("type") == "source":
                    continue
                ut, uv = un.get("type"), un.get("value")
                vt, vv = vn.get("type"), vn.get("value")
                if not (ut and uv and vt and vv):
                    continue
                self.fuse_relationship(
                    ut, uv, relation, vt, vv,
                    source=str(attrs.get("source", "")),
                )
                count += 1
        except Exception as e:  # noqa: BLE001
            log.debug("fuse_graph partial failure after %d edges: %s", count, e)
        return count

    # ----------------------------------------------------------- read surface
    def get_entity(self, eid: str) -> Optional[Dict[str, Any]]:
        """Return one fused entity with its provenance, properties and edges."""
        with self._lock:
            row = self._conn.execute(
                "SELECT id, type, value, normalized, canonical_id, confidence, "
                "source_count, observation_count, first_seen, last_seen "
                "FROM fusion_entities WHERE id=?",
                (eid,),
            ).fetchone()
            if not row:
                return None
            srcs = self._conn.execute(
                "SELECT source, seen_count, last_seen FROM fusion_entity_sources "
                "WHERE entity_id=? ORDER BY seen_count DESC",
                (eid,),
            ).fetchall()
            props = self._conn.execute(
                "SELECT key, value, source, confidence FROM fusion_properties "
                "WHERE entity_id=? ORDER BY key",
                (eid,),
            ).fetchall()
            rels = self._conn.execute(
                "SELECT src_id, relation, dst_id, source, confidence "
                "FROM fusion_relationships WHERE src_id=? OR dst_id=? "
                "ORDER BY observed_at DESC LIMIT 200",
                (eid, eid),
            ).fetchall()
        return {
            "id": row[0], "type": row[1], "value": row[2],
            "normalized": row[3], "canonical_id": row[4], "confidence": row[5],
            "source_count": row[6], "observation_count": row[7],
            "first_seen": row[8], "last_seen": row[9],
            "sources": [
                {"source": s[0], "seen_count": s[1], "last_seen": s[2]} for s in srcs
            ],
            "properties": [
                {"key": p[0], "value": p[1], "source": p[2], "confidence": p[3]}
                for p in props
            ],
            "relationships": [
                {"src_id": r[0], "relation": r[1], "dst_id": r[2],
                 "source": r[3], "confidence": r[4]}
                for r in rels
            ],
        }

    def search_entities(
        self,
        term: str = "",
        etype: str = "",
        *,
        min_sources: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """Search fused entities by value substring and/or type.

        ``min_sources`` filters to entities corroborated by at least N feeds —
        the fusion-native "only show me what more than one source agrees on"
        query. Ordered by source breadth then recency.
        """
        sql = (
            "SELECT id, type, value, confidence, source_count, "
            "observation_count, last_seen FROM fusion_entities"
        )
        clauses: List[str] = []
        params: List[Any] = []
        if term:
            clauses.append("(value LIKE ? OR normalized LIKE ?)")
            params.extend([f"%{term}%", f"%{term.lower()}%"])
        if etype:
            clauses.append("type=?")
            params.append(etype)
        if min_sources > 0:
            clauses.append("source_count>=?")
            params.append(int(min_sources))
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY source_count DESC, last_seen DESC LIMIT ?"
        params.append(int(limit))
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [
            {
                "id": r[0], "type": r[1], "value": r[2], "confidence": r[3],
                "source_count": r[4], "observation_count": r[5], "last_seen": r[6],
            }
            for r in rows
        ]

    def corroborated_properties(self, eid: str, min_sources: int = 2) -> List[Dict[str, Any]]:
        """Return an entity's properties that at least ``min_sources`` distinct
        feeds independently asserted — the fusion store's confidence signal."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT key, value, COUNT(DISTINCT source) AS n, "
                "GROUP_CONCAT(DISTINCT source) FROM fusion_properties "
                "WHERE entity_id=? GROUP BY key, value HAVING n>=? "
                "ORDER BY n DESC",
                (eid, int(min_sources)),
            ).fetchall()
        return [
            {"key": r[0], "value": r[1], "source_count": r[2],
             "sources": (r[3] or "").split(",")}
            for r in rows
        ]

    def list_sources(self, limit: int = 200) -> List[Dict[str, Any]]:
        """Return the source catalogue with accumulated fetch/ok counters."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT name, category, contact, requires_key, fetch_count, "
                "ok_count, last_seen FROM fusion_sources "
                "ORDER BY fetch_count DESC, name LIMIT ?",
                (int(limit),),
            ).fetchall()
        return [
            {
                "name": r[0], "category": r[1], "contact": r[2],
                "requires_key": bool(r[3]), "fetch_count": r[4],
                "ok_count": r[5], "last_seen": r[6],
            }
            for r in rows
        ]

    def stats(self) -> Dict[str, Any]:
        """One-glance dashboard of the fused store's size."""
        with self._lock:
            def _count(table: str) -> int:
                return self._conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            entities = _count("fusion_entities")
            sources = _count("fusion_sources")
            observations = _count("fusion_observations")
            properties = _count("fusion_properties")
            relationships = _count("fusion_relationships")
            by_type = self._conn.execute(
                "SELECT type, COUNT(*) FROM fusion_entities "
                "GROUP BY type ORDER BY COUNT(*) DESC LIMIT 20"
            ).fetchall()
            multi = self._conn.execute(
                "SELECT COUNT(*) FROM fusion_entities WHERE source_count>=2"
            ).fetchone()[0]
        return {
            "entities": entities,
            "entities_multi_source": multi,
            "sources": sources,
            "observations": observations,
            "properties": properties,
            "relationships": relationships,
            "by_type": {t: n for t, n in by_type},
            "db": str(self.path),
        }

    def close(self) -> None:
        with self._lock:
            try:
                self._conn.close()
            except Exception:  # noqa: BLE001
                pass


def open_store(path: Optional[Path] = None) -> Optional[FusionStore]:
    """Open the fusion store, returning None instead of raising on failure.

    The orchestrator calls this so an unwritable or locked data directory
    degrades the fusion layer to a no-op rather than aborting an
    investigation.
    """
    try:
        return FusionStore(path)
    except Exception as e:  # noqa: BLE001
        log.warning("fusion store unavailable, running without fusion: %s", e)
        return None
