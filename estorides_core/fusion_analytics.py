"""
estorides_core.fusion_analytics
===============================
Intelligence analytics layer over the fusion store.

Provides the "dashboard" queries that Palantir's Athena delivers:
multi-source consensus, entity timelines, source reliability stats,
and corroboration analytics. All read-only, all parameterized SQL,
all fail-soft.

Public surface:
    analytics = FusionAnalytics(fusion_store_instance)
    analytics.entity_timeline(eid) -> dict | None
    analytics.entity_summary(eid) -> dict | None
    analytics.source_stats(source_name) -> dict | None
    analytics.multi_source_consensus(eid, key) -> dict
    analytics.corroborated_properties(eid, min_sources=2) -> list
    analytics.entity_search(term, ...) -> list
    analytics.top_changed(days=7, limit=20) -> list
    analytics.source_corroboration_matrix(limit=20) -> list
"""
from __future__ import annotations

import logging
import time
from typing import Any

log = logging.getLogger("estorides.fusion_analytics")


class FusionAnalytics:
    """Read-only analytics queries over the fusion store.

    Every method is parameterized SQL — no string interpolation.
    A ``store`` of ``None`` is silently handled (all methods return
    empty results) so the caller never needs to guard against a
    missing datastore.
    """

    def __init__(self, store: Any) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Entity timeline — full temporal picture of one entity
    # ------------------------------------------------------------------
    def entity_timeline(self, eid: str) -> dict[str, Any] | None:
        if self._store is None:
            return None
        conn = self._store._conn
        try:
            row = conn.execute(
                "SELECT id, type, value, first_seen, last_seen "
                "FROM fusion_entities WHERE id=?",
                (eid,),
            ).fetchone()
            if not row:
                return None

            observations = [
                {"source": r[0], "observed_at": r[1], "status": "ok", "key_findings": []}
                for r in conn.execute(
                    "SELECT source, last_seen FROM fusion_entity_sources "
                    "WHERE entity_id=? ORDER BY last_seen DESC",
                    (eid,),
                )
            ]

            properties: list[dict[str, Any]] = []
            for r in conn.execute(
                "SELECT key, value, observed_at FROM fusion_properties "
                "WHERE entity_id=? ORDER BY key, observed_at",
                (eid,),
            ):
                if not any(p["key"] == r[0] and p["value"] == r[1] for p in properties):
                    src_rows = conn.execute(
                        "SELECT DISTINCT source FROM fusion_properties "
                        "WHERE entity_id=? AND key=? AND value=?",
                        (eid, r[0], r[1]),
                    ).fetchall()
                    properties.append({
                        "key": r[0],
                        "value": r[1],
                        "sources": [s[0] for s in src_rows if s[0]],
                        "first_seen": r[2],
                        "last_seen": r[2],
                    })

            relationships = [
                {
                    "relation": r[1],
                    "dst_value": self._resolve_entity_value(r[2]),
                    "dst_type": self._resolve_entity_type(r[2]),
                    "sources": [r[3]] if r[3] else [],
                    "observed_at": r[4],
                }
                for r in conn.execute(
                    "SELECT src_id, relation, dst_id, source, observed_at "
                    "FROM fusion_relationships WHERE src_id=? OR dst_id=? "
                    "ORDER BY observed_at DESC LIMIT 100",
                    (eid, eid),
                )
            ]

            source_timeline = [
                {"source": r[0], "first_seen": r[1], "last_seen": r[2], "seen_count": r[3]}
                for r in conn.execute(
                    "SELECT source, first_seen, last_seen, seen_count "
                    "FROM fusion_entity_sources WHERE entity_id=? "
                    "ORDER BY seen_count DESC",
                    (eid,),
                )
            ]

            return {
                "entity_id": row[0],
                "type": row[1],
                "value": row[2],
                "first_seen": row[3],
                "last_seen": row[4],
                "observations": observations,
                "properties": properties,
                "relationships": self._deduplicate_relationships(relationships),
                "source_timeline": source_timeline,
            }
        except Exception as e:
            log.debug("entity_timeline failed for %s: %s", eid, e)
            return None

    # ------------------------------------------------------------------
    # Entity summary — one-glance aggregate
    # ------------------------------------------------------------------
    def entity_summary(self, eid: str) -> dict[str, Any] | None:
        if self._store is None:
            return None
        conn = self._store._conn
        try:
            row = conn.execute(
                "SELECT id, type, value, normalized, confidence, "
                "source_count, observation_count, first_seen, last_seen "
                "FROM fusion_entities WHERE id=?",
                (eid,),
            ).fetchone()
            if not row:
                return None

            prop_count = conn.execute(
                "SELECT COUNT(*) FROM fusion_properties WHERE entity_id=?", (eid,)
            ).fetchone()[0]
            corr_count = conn.execute(
                "SELECT COUNT(DISTINCT key || ':' || value) FROM fusion_properties "
                "WHERE entity_id=? AND entity_id IN (SELECT entity_id FROM fusion_properties "
                "GROUP BY key, value HAVING COUNT(DISTINCT source) >= 2)",
                (eid,),
            ).fetchone()[0]
            prop_keys = [
                r[0] for r in conn.execute(
                    "SELECT DISTINCT key FROM fusion_properties WHERE entity_id=? ORDER BY key", (eid,)
                )
            ]
            rel_count = conn.execute(
                "SELECT COUNT(*) FROM fusion_relationships WHERE src_id=? OR dst_id=?", (eid, eid)
            ).fetchone()[0]
            rel_types = [
                r[0] for r in conn.execute(
                    "SELECT DISTINCT relation FROM fusion_relationships "
                    "WHERE src_id=? OR dst_id=? ORDER BY relation", (eid, eid)
                )
            ]
            rel_targets = conn.execute(
                "SELECT COUNT(DISTINCT CASE WHEN src_id=? THEN dst_id ELSE src_id END) "
                "FROM fusion_relationships WHERE src_id=? OR dst_id=?",
                (eid, eid, eid),
            ).fetchone()[0]
            sources = [
                r[0] for r in conn.execute(
                    "SELECT source FROM fusion_entity_sources WHERE entity_id=? ORDER BY source",
                    (eid,),
                )
            ]

            intel_level = self._intel_level(row[5], sources)

            return {
                "entity_id": row[0],
                "type": row[1],
                "value": row[2],
                "normalized": row[3],
                "confidence": row[4],
                "source_count": row[5],
                "observation_count": row[6],
                "first_seen": row[7],
                "last_seen": row[8],
                "properties_summary": {
                    "total": prop_count,
                    "corroborated": corr_count,
                    "keys": prop_keys,
                },
                "relationships_summary": {
                    "total": rel_count,
                    "types": rel_types,
                    "distinct_targets": rel_targets,
                },
                "sources": sources,
                "intel_level": intel_level,
            }
        except Exception as e:
            log.debug("entity_summary failed for %s: %s", eid, e)
            return None

    # ------------------------------------------------------------------
    # Source stats
    # ------------------------------------------------------------------
    def source_stats(self, source_name: str) -> dict[str, Any] | None:
        if self._store is None:
            return None
        conn = self._store._conn
        try:
            row = conn.execute(
                "SELECT name, category, first_seen, last_seen, "
                "fetch_count, ok_count FROM fusion_sources WHERE name=?",
                (source_name,),
            ).fetchone()
            if not row:
                return None

            fetch_count = row[4] or 0
            ok_count = row[5] or 0
            success_rate = ok_count / fetch_count if fetch_count > 0 else 0.0

            unique_ents = conn.execute(
                "SELECT COUNT(DISTINCT entity_id) FROM fusion_entity_sources WHERE source=?",
                (source_name,),
            ).fetchone()[0]

            type_rows = conn.execute(
                "SELECT e.type, COUNT(*) FROM fusion_entity_sources es "
                "JOIN fusion_entities e ON es.entity_id=e.id "
                "WHERE es.source=? GROUP BY e.type ORDER BY COUNT(*) DESC",
                (source_name,),
            ).fetchall()

            unique_props = conn.execute(
                "SELECT COUNT(DISTINCT key) FROM fusion_properties WHERE source=?",
                (source_name,),
            ).fetchone()[0]

            unique_rels = conn.execute(
                "SELECT COUNT(DISTINCT relation) FROM fusion_relationships WHERE source=?",
                (source_name,),
            ).fetchone()[0]

            obs_per_fetch = conn.execute(
                "SELECT COUNT(*) FROM fusion_observations WHERE source=?", (source_name,)
            ).fetchone()[0]

            avg_obs = obs_per_fetch / fetch_count if fetch_count > 0 else 0.0

            # Corroboration rate: fraction of this source's entities that
            # are also seen by at least one other source.
            only_this = conn.execute(
                "SELECT COUNT(*) FROM (SELECT entity_id FROM fusion_entity_sources "
                "WHERE source=? AND entity_id NOT IN "
                "(SELECT entity_id FROM fusion_entity_sources WHERE source!=?))",
                (source_name, source_name),
            ).fetchone()[0]
            corr_rate = 1.0 - (only_this / unique_ents) if unique_ents > 0 else 0.0

            return {
                "source_name": row[0],
                "category": row[1],
                "first_seen": row[2],
                "last_seen": row[3],
                "fetch_count": fetch_count,
                "ok_count": ok_count,
                "success_rate": success_rate,
                "unique_entities": unique_ents,
                "entity_types": {t: n for t, n in type_rows},
                "unique_properties_contributed": unique_props,
                "unique_relationships_contributed": unique_rels,
                "avg_observations_per_fetch": round(avg_obs, 2),
                "corroboration_rate": round(corr_rate, 4),
            }
        except Exception as e:
            log.debug("source_stats failed for %s: %s", source_name, e)
            return None

    # ------------------------------------------------------------------
    # Multi-source consensus for a single property key
    # ------------------------------------------------------------------
    def multi_source_consensus(self, eid: str, key: str) -> dict[str, Any]:
        result: dict[str, Any] = {
            "entity_id": eid,
            "property_key": key,
            "values": [],
            "consensus_value": "",
            "consensus_strength": 0.0,
            "total_sources": 0,
        }
        if self._store is None:
            return result
        conn = self._store._conn
        try:
            rows = conn.execute(
                "SELECT value, COUNT(DISTINCT source) AS n, "
                "GROUP_CONCAT(DISTINCT source) AS srcs, "
                "AVG(confidence) AS avg_conf "
                "FROM fusion_properties WHERE entity_id=? AND key=? "
                "GROUP BY value ORDER BY n DESC, avg_conf DESC",
                (eid, key),
            ).fetchall()
            if not rows:
                return result

            values = []
            total_sources = sum(r[1] for r in rows)
            for r in rows:
                src_list = (r[2] or "").split(",") if r[2] else []
                values.append({
                    "value": r[0],
                    "sources": [s for s in src_list if s],
                    "count": r[1],
                    "weighted_confidence": round(r[3], 4) if r[3] else 0.0,
                })

            top = values[0]
            consensus_strength = top["count"] / total_sources if total_sources > 0 else 0.0

            return {
                "entity_id": eid,
                "property_key": key,
                "values": values,
                "consensus_value": top["value"],
                "consensus_strength": round(consensus_strength, 4),
                "total_sources": total_sources,
            }
        except Exception as e:
            log.debug("multi_source_consensus failed for %s/%s: %s", eid, key, e)
            return result

    # ------------------------------------------------------------------
    # Corroborated properties
    # ------------------------------------------------------------------
    def corroborated_properties(
        self, eid: str, min_sources: int = 2
    ) -> list[dict[str, Any]]:
        if self._store is None:
            return []
        min_sources = max(1, int(min_sources))
        conn = self._store._conn
        try:
            rows = conn.execute(
                "SELECT key, value, COUNT(DISTINCT source) AS n, "
                "GROUP_CONCAT(DISTINCT source) "
                "FROM fusion_properties WHERE entity_id=? "
                "GROUP BY key, value HAVING n>=? ORDER BY n DESC",
                (eid, min_sources),
            ).fetchall()
            return [
                {
                    "key": r[0],
                    "value": r[1],
                    "source_count": r[2],
                    "sources": (r[3] or "").split(",") if r[3] else [],
                }
                for r in rows
            ]
        except Exception as e:
            log.debug("corroborated_properties failed for %s: %s", eid, e)
            return []

    # ------------------------------------------------------------------
    # Entity search
    # ------------------------------------------------------------------
    def entity_search(
        self,
        term: str = "",
        etype: str = "",
        *,
        min_confidence: float = 0.0,
        min_sources: int = 0,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        if self._store is None:
            return []
        limit = max(1, min(200, int(limit)))
        min_sources = max(0, int(min_sources))
        min_confidence = max(0.0, min(1.0, float(min_confidence)))

        clauses: list[str] = []
        params: list[Any] = []
        if term:
            clauses.append("(value LIKE ? OR normalized LIKE ?)")
            params.extend([f"%{term}%", f"%{term.lower()}%"])
        if etype:
            clauses.append("type=?")
            params.append(etype)
        if min_confidence > 0.0:
            clauses.append("confidence>=?")
            params.append(min_confidence)
        if min_sources > 0:
            clauses.append("source_count>=?")
            params.append(min_sources)

        sql = "SELECT id, type, value, confidence, source_count, observation_count, last_seen FROM fusion_entities"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY source_count DESC, last_seen DESC LIMIT ?"
        params.append(limit)

        conn = self._store._conn
        try:
            rows = conn.execute(sql, params).fetchall()
            return [
                {
                    "id": r[0],
                    "type": r[1],
                    "value": r[2],
                    "confidence": r[3],
                    "source_count": r[4],
                    "observation_count": r[5],
                    "last_seen": r[6],
                }
                for r in rows
            ]
        except Exception as e:
            log.debug("entity_search failed: %s", e)
            return []

    # ------------------------------------------------------------------
    # Top changed entities in a time window
    # ------------------------------------------------------------------
    def top_changed(self, days: int = 7, limit: int = 20) -> list[dict[str, Any]]:
        if self._store is None:
            return []
        days = max(1, int(days))
        limit = max(1, min(200, int(limit)))
        cutoff = time.time() - days * 86400
        conn = self._store._conn
        try:
            rows = conn.execute(
                "SELECT e.id, e.type, e.value, e.source_count, e.last_seen, "
                "(SELECT COUNT(*) FROM fusion_observations o WHERE o.observed_at>=? "
                " AND o.source IN (SELECT source FROM fusion_entity_sources es WHERE es.entity_id=e.id)) "
                "AS new_obs, "
                "0 AS new_sources, "
                "(SELECT COUNT(*) FROM fusion_properties p WHERE p.entity_id=e.id AND p.observed_at>=?) "
                "AS new_props, "
                "(SELECT COUNT(*) FROM fusion_relationships r WHERE "
                " (r.src_id=e.id OR r.dst_id=e.id) AND r.observed_at>=?) "
                "AS new_rels "
                "FROM fusion_entities e "
                "WHERE e.last_seen>=? "
                "ORDER BY new_obs DESC, e.last_seen DESC LIMIT ?",
                (cutoff, cutoff, cutoff, cutoff, limit),
            ).fetchall()
            return [
                {
                    "entity_id": r[0],
                    "type": r[1],
                    "value": r[2],
                    "source_count": r[3],
                    "last_seen": r[4],
                    "new_observations": r[5],
                    "new_sources": r[6],
                    "new_properties": r[7],
                    "new_relationships": r[8],
                }
                for r in rows
            ]
        except Exception as e:
            log.debug("top_changed failed: %s", e)
            return []

    # ------------------------------------------------------------------
    # Source corroboration matrix
    # ------------------------------------------------------------------
    def source_corroboration_matrix(self, limit: int = 20) -> list[dict[str, Any]]:
        if self._store is None:
            return []
        limit = max(1, min(100, int(limit)))
        conn = self._store._conn
        try:
            rows = conn.execute(
                "SELECT a.source AS src_a, b.source AS src_b, "
                "COUNT(DISTINCT a.entity_id) AS shared_entities, "
                "0 AS shared_properties "
                "FROM fusion_entity_sources a "
                "JOIN fusion_entity_sources b ON a.entity_id=b.entity_id AND a.source<b.source "
                "GROUP BY a.source, b.source "
                "ORDER BY shared_entities DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [
                {
                    "source_a": r[0],
                    "source_b": r[1],
                    "shared_entities": r[2],
                    "shared_properties": r[3],
                }
                for r in rows
            ]
        except Exception as e:
            log.debug("source_corroboration_matrix failed: %s", e)
            return []

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _resolve_entity_value(self, eid: str) -> str:
        if self._store is None:
            return eid
        try:
            row = self._store._conn.execute(
                "SELECT value FROM fusion_entities WHERE id=?", (eid,)
            ).fetchone()
            return row[0] if row else eid
        except Exception:
            return eid

    def _resolve_entity_type(self, eid: str) -> str:
        if self._store is None:
            return ""
        try:
            row = self._store._conn.execute(
                "SELECT type FROM fusion_entities WHERE id=?", (eid,)
            ).fetchone()
            return row[0] if row else ""
        except Exception:
            return ""

    @staticmethod
    def _intel_level(source_count: int, sources: list[str]) -> str:
        if source_count >= 3:
            return "intelligence"
        if source_count >= 2:
            return "information"
        return "data"

    @staticmethod
    def _deduplicate_relationships(
        rels: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        seen: set[tuple[str, str]] = set()
        out = []
        for r in rels:
            key = (r["relation"], r["dst_value"])
            if key not in seen:
                seen.add(key)
                out.append(r)
        return out
