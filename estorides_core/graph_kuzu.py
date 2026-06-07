"""
estorides_core.graph_kuzu
=========================
Persistent graph backend powered by Kuzu (embedded Cypher DB).

Why Kuzu and not just another NetworkX dump:
  NetworkX on disk is read whole on every request. Kuzu gives us
  indexed Cypher queries so we can ask "every entity connected to <id>
  within 2 hops" without reloading the world. We still keep NetworkX
  as the in-memory working graph (the orchestrator depends on it for
  per-run traversal) — this module mirrors every write to a Kuzu
  database on disk so cross-run intelligence queries become fast.

Schema mirrors the in-memory graph's node kinds:

  Entity nodes: Domain, IPv4, IPv6, Email, URL, Person, Org,
                ASN, CVE, GHSA, BTCAddress, ETHAddress, Phone,
                Hash (md5/sha1/sha256/bitcoin_tx), MAC, UserAgent,
                Country, Sanction
  Source nodes: one node per OSINT source

  Edges:
    OBSERVED_BY   (Entity -> Source)   "this source produced this entity"
    CO_OCCURS     (Entity -> Entity)   "appeared in the same response"
    RESOLVED_TO   (Domain -> IPv4)     "DNS resolution"
    REGISTERED_BY (Domain -> Org)      "WHOIS registrant"
    HAS_CVE       (IP -> CVE)          "vulnerability on this host"
    LOCATED_IN    (Entity -> Country)  "geolocated entity"
    SANCTIONED    (Entity -> Sanction) "OFAC SDN match"
    SAME_AS       (Entity -> Entity)   "fuzzy cluster"

Public surface:
    kg = KuzuGraphBackend(path)
    kg.upsert_entity(type, value, source, **attrs)
    kg.upsert_relationship(src_type, src_value, rel, dst_type, dst_value, **attrs)
    kg.neighbors(node_id, hops=1, relation=None) -> [{node, edge}, ...]
    kg.cypher(query, params=None) -> rows
    kg.close()
"""
from __future__ import annotations

import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import kuzu

from .config import DATA_DIR

log = logging.getLogger("estorides.kuzu")

# Default DB lives in data/estorides_graph.kuzu; override with env var.
KUZU_PATH: Path = Path(
    os.environ.get("ESTORIDES_KUZU_PATH", str(DATA_DIR / "estorides_graph.kuzu"))
)


# Kuzu is strict about types and labels: keep a canonical mapping from
# our internal Entity.type strings to Kuzu node label names. Anything
# not in here gets normalised to the catch-all "Entity" label.
_TYPE_TO_LABEL: Dict[str, str] = {
    "domain": "Domain",
    "ipv4": "IPv4",
    "ipv6": "IPv6",
    "email": "Email",
    "url": "URL",
    "phone_e164": "Phone",
    "asn": "ASN",
    "cve": "CVE",
    "ghsa": "GHSA",
    "btc_address": "BTCAddress",
    "eth_address": "ETHAddress",
    "md5": "Hash",
    "sha1": "Hash",
    "sha256": "Hash",
    "bitcoin_tx": "Hash",
    "mac": "MAC",
    "user_agent": "UserAgent",
    "person": "Person",
    "org": "Org",
    "country": "Place",
    "sanction": "Sanction",
    "source": "Source",
}

# Edge labels — keep in sync with the in-memory graph in
# estorides_core/knowledge_graph.py AND the inferers in
# estorides_core/relationship_inference.py. Anything missing here
# is silently dropped on the Kuzu side (the in-memory NetworkX
# graph still keeps the edge).
_RELATION_TO_EDGE: Dict[str, str] = {
    "observed_by": "OBSERVED_BY",
    "co_occurs": "CO_OCCURS",
    "resolved_to": "RESOLVED_TO",
    "resolves_to": "RESOLVED_TO",
    "registered_by": "REGISTERED_BY",
    "has_cve": "HAS_CVE",
    "located_in": "LOCATED_IN",
    "sanctioned": "SANCTIONED",
    "same_as": "SAME_AS",
    # Edge labels for the inferer registry. These map the free-form
    # relation names used by relationship_inference.py onto Kuzu
    # REL TABLEs. We use generic Ent -> Ent relations so a single
    # MATCH (a)-[r:RELATED_TO]->(b) catches every semantic edge the
    # inferers emit, while the `relation` attribute is preserved on
    # the edge for the UI.
    "has_subdomain": "RELATED_TO",
    "exposes_port": "RELATED_TO",
    "classified_as": "RELATED_TO",
    "abuse_score": "RELATED_TO",
    "registered_with_email": "RELATED_TO",
    "uses_technology": "RELATED_TO",
    "associated_with_person": "RELATED_TO",
    "linked_to_threat_actor": "RELATED_TO",
    "mapped_to_technique": "RELATED_TO",
    "matches_cve": "HAS_CVE",
}


def _label_for(ent_type: str) -> str:
    # `Ent` not `Entity` — `Entity` is a reserved Cypher keyword
    # in Kuzu and CREATE NODE TABLE Entity() fails with
    # "Entity already exists in catalog" even on a fresh DB.
    if ent_type in _TYPE_TO_LABEL:
        return _TYPE_TO_LABEL[ent_type]
    return "Ent"


def _node_id(type_: str, value: str) -> str:
    """Canonical id used as PRIMARY KEY in Kuzu.

    Mirrors the in-memory convention in KnowledgeGraph._node_id so a
    `Domain:evilcorp.com` row means the same thing in both stores."""
    return f"{type_}:{value.lower()}"


# ---------------------------------------------------------------------------
# DDL — run once on first open. Idempotent via IF NOT EXISTS.
# ---------------------------------------------------------------------------
_DDL: List[str] = [
    # Catch-all Ent table for anything not in the typed labels.
    # `Ent` not `Entity` — `Entity` is a reserved Cypher keyword
    # in Kuzu.
    """CREATE NODE TABLE IF NOT EXISTS Ent (
        id STRING, type STRING, value STRING, kind STRING,
        seen_count INT64, first_seen DOUBLE,
        PRIMARY KEY(id)
    )""",
    "CREATE NODE TABLE IF NOT EXISTS Source (id STRING, name STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS Place (id STRING, name STRING, code STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS Sanction (id STRING, name STRING, schema STRING, PRIMARY KEY(id))",
    # Typed entity labels
    "CREATE NODE TABLE IF NOT EXISTS Domain (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS IPv4 (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS IPv6 (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS Email (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS URL (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS Phone (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS ASN (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS CVE (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS GHSA (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS BTCAddress (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS ETHAddress (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS Hash (id STRING, value STRING, algo STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS MAC (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS UserAgent (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS Person (id STRING, value STRING, PRIMARY KEY(id))",
    "CREATE NODE TABLE IF NOT EXISTS Org (id STRING, value STRING, PRIMARY KEY(id))",
    # Edges. All relationships are `Ent -> Ent` rather than typed
    # label pairs (e.g. `Domain -> IPv4`). The reason: an entity can
    # be multi-label (a row is BOTH `Ent` and `Domain`), and Kuzu's
    # binder fails on the second-merge path if a relation is declared
    # with typed labels and one endpoint is a typed+Ent combo. Using
    # `Ent -> Ent` for the *binder* and reading the typed label from
    # the node properties works uniformly.
    "CREATE REL TABLE IF NOT EXISTS OBSERVED_BY(FROM Ent TO Source)",
    "CREATE REL TABLE IF NOT EXISTS CO_OCCURS(FROM Ent TO Ent)",
    "CREATE REL TABLE IF NOT EXISTS RESOLVED_TO(FROM Ent TO Ent)",
    "CREATE REL TABLE IF NOT EXISTS REGISTERED_BY(FROM Ent TO Ent)",
    "CREATE REL TABLE IF NOT EXISTS HAS_CVE(FROM Ent TO Ent)",
    "CREATE REL TABLE IF NOT EXISTS LOCATED_IN(FROM Ent TO Place)",
    "CREATE REL TABLE IF NOT EXISTS SANCTIONED(FROM Ent TO Sanction)",
    "CREATE REL TABLE IF NOT EXISTS SAME_AS(FROM Ent TO Ent)",
    # Catch-all edge for any relation that doesn't have a typed REL.
    # The `relation` attribute on the edge preserves the original
    # name (e.g. "uses_technology") so a UI query can still group
    # related edges.
    "CREATE REL TABLE IF NOT EXISTS RELATED_TO(FROM Ent TO Ent)",
]


class KuzuGraphBackend:
    """Thread-safe Kuzu wrapper for the Estorides knowledge graph.

    The orchestrator calls this alongside the in-memory NetworkX graph.
    Writes are synchronous but cheap; reads (Cypher) are also synchronous
    and roughly match NetworkX traversal cost for 2-hop queries while
    being dramatically faster at cross-run joins.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        # Lazy import: graph_kuzu is initialised once at module load,
        # and we must never let one import path crash the whole CLI.
        self.path = Path(path) if path else KUZU_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Try to open the on-disk DB. If another process already
        # holds the lock (e.g. the long-lived `serve` is running),
        # fall back to an in-memory DB so the current run still
        # works (just without cross-process persistence). Kuzu's
        # default error here is unhelpful; we wrap the open to make
        # the failure mode explicit.
        try:
            self._db: Any = kuzu.Database(str(self.path))
        except Exception as e:  # noqa: BLE001
            log.warning(
                "could not lock on-disk Kuzu DB at %s (%s) — "
                "falling back to in-memory for this process. "
                "If the long-lived `serve` is running, that's "
                "the holder of the lock; either stop it or "
                "point ESTORIDES_KUZU_PATH at a fresh path.",
                self.path, e,
            )
            self._db = kuzu.Database(":memory:")
        self._conn: Any = kuzu.Connection(self._db)
        self._lock = threading.Lock()
        self._init_schema()

    # ------------------------------------------------------------------ ddl
    def _init_schema(self) -> None:
        with self._lock:
            for stmt in _DDL:
                try:
                    self._conn.execute(stmt)
                except Exception as e:  # noqa: BLE001
                    # IF NOT EXISTS should prevent duplicates, but if
                    # the user pointed us at an older DB we don't want
                    # to crash the import path.
                    log.debug("DDL skipped: %s — %s", stmt.split("\n", 1)[0], e)

    # --------------------------------------------------------------- write
    def upsert_entity(
        self,
        ent_type: str,
        value: str,
        source: Optional[str] = None,
        **attrs: Any,
    ) -> str:
        """Insert (or merge) an entity. Returns its canonical node id.

        If `source` is given we also wire an OBSERVED_BY edge so we
        can later ask "which sources saw this entity?"."""
        nid = _node_id(ent_type, value)
        label = _label_for(ent_type)
        kind = attrs.get("kind") or ent_type
        first_seen = float(attrs.get("first_seen", time.time()))

        with self._lock:
            # MERGE handles "insert if missing, else leave alone".
            self._conn.execute(
                f"MERGE (n:{label} {{id: $id}}) "
                f"SET n.value = $value",
                {"id": nid, "value": str(value)},
            )
            # Keep the catch-all Ent row in sync so cross-label
            # queries (e.g. MATCH (n:Ent) RETURN n) work uniformly.
            self._conn.execute(
                "MERGE (n:Ent {id: $id}) "
                "SET n.type = $type, n.value = $value, n.kind = $kind, "
                "n.seen_count = COALESCE(n.seen_count, 0) + 1, "
                "n.first_seen = COALESCE(n.first_seen, $first_seen)",
                {
                    "id": nid,
                    "type": ent_type,
                    "value": str(value),
                    "kind": kind,
                    "first_seen": first_seen,
                },
            )
            if source:
                self._conn.execute(
                    "MERGE (s:Source {id: $sid}) SET s.name = $sname",
                    {"sid": f"source:{source}", "sname": source},
                )
                self._conn.execute(
                    "MATCH (n:Ent {id: $nid}), (s:Source {id: $sid}) "
                    "MERGE (n)-[:OBSERVED_BY]->(s)",
                    {"nid": nid, "sid": f"source:{source}"},
                )
        return nid

    def upsert_relationship(
        self,
        src_type: str,
        src_value: str,
        rel: str,
        dst_type: str,
        dst_value: str,
        **attrs: Any,
    ) -> None:
        """Insert an edge between two entities.

        Unknown relations are silently skipped — every edge type
        that matters is mapped in _RELATION_TO_EDGE."""
        src_id = _node_id(src_type, src_value)
        dst_id = _node_id(dst_type, dst_value)
        edge = _RELATION_TO_EDGE.get(rel)
        if not edge:
            return
        with self._lock:
            # Ensure both endpoints exist inline — do NOT call
            # `upsert_entity` here because that would re-acquire the
            # lock and deadlock (this method holds the lock already).
            for ent_type, ent_id, val in (
                (src_type, src_id, src_value),
                (dst_type, dst_id, dst_value),
            ):
                label = _label_for(ent_type)
                self._conn.execute(
                    f"MERGE (n:{label} {{id: $id}}) SET n.value = $value",
                    {"id": ent_id, "value": str(val)},
                )
                self._conn.execute(
                    "MERGE (n:Ent {id: $id}) "
                    "SET n.type = $type, n.value = $value, n.kind = $kind, "
                    "n.seen_count = COALESCE(n.seen_count, 0) + 1, "
                    "n.first_seen = COALESCE(n.first_seen, $fs)",
                    {
                        "id": ent_id,
                        "type": ent_type,
                        "value": str(val),
                        "kind": ent_type,
                        "fs": time.time(),
                    },
                )
            self._conn.execute(
                f"MATCH (a:Ent {{id: $src}}), (b:Ent {{id: $dst}}) "
                f"MERGE (a)-[:{edge}]->(b)",
                {"src": src_id, "dst": dst_id},
            )

    # ---------------------------------------------------------------- read
    def neighbors(
        self,
        node_id: str,
        hops: int = 1,
        relation: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Return nodes reachable from `node_id` within `hops` edges.

        `relation` optionally filters to a single edge label.
        Returns a list of dicts with whatever columns the query names."""
        rel_filter = f":{relation}" if relation else ""
        q = (
            f"MATCH (n:Ent {{id: $id}})-[{rel_filter}*1..{int(hops)}]"
            f"-(m:Ent) "
            f"RETURN DISTINCT m.id, m.type, m.value, m.kind "
            f"LIMIT {int(limit)}"
        )
        return self.cypher(q, {"id": node_id})

    def cypher(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Run a Cypher query and return rows as a list of dicts.

        Column names are taken from the RETURN clause. Missing
        columns (e.g. `m.kind` on a node that was never enriched) come
        back as None so callers don't have to special-case."""
        with self._lock:
            result = self._conn.execute(query, params or {})
            cols = (
                result.get_column_names()
                if hasattr(result, "get_column_names")
                else []
            )
            out: List[Dict[str, Any]] = []
            while result.has_next():
                row = result.get_next()
                if cols:
                    out.append({c: row[i] for i, c in enumerate(cols)})
                else:
                    out.append({"row": list(row)})
            return out

    # ----------------------------------------------------------- introspection
    def stats(self) -> Dict[str, Any]:
        """Return counts of every node label and edge rel type."""
        out: Dict[str, Any] = {"path": str(self.path), "labels": {}, "rels": {}}
        try:
            label_set = sorted(
                set(_TYPE_TO_LABEL.values())
                | {"Ent", "Source", "Place", "Sanction"}
            )
            for label in label_set:
                try:
                    r = self._conn.execute(
                        f"MATCH (n:{label}) RETURN count(n)"
                    )
                    if r.has_next():
                        out["labels"][label] = int(r.get_next()[0])
                except Exception:
                    pass
            for rel in sorted(set(_RELATION_TO_EDGE.values())):
                try:
                    r = self._conn.execute(
                        f"MATCH ()-[r:{rel}]->() RETURN count(r)"
                    )
                    if r.has_next():
                        out["rels"][rel] = int(r.get_next()[0])
                except Exception:
                    pass
        except Exception as e:  # noqa: BLE001
            out["error"] = str(e)
        return out

    def close(self) -> None:
        # Kuzu has no explicit close; the destructor does it. Drop the
        # connection/db refs so a future open() can take the lock.
        self._conn = None  # type: ignore[assignment]
        self._db = None    # type: ignore[assignment]


# Module-level singleton — orchestrator imports this directly.
backend = KuzuGraphBackend()
