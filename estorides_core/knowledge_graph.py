"""
estorides_core.knowledge_graph
==============================
Persistent in-memory knowledge graph backed by NetworkX.

Nodes = entities (domain, ip, email, person, organisation, cve, etc.)
Edges = relationships discovered between them
   * "observed_by"   entity -> source
   * "resolved_to"   domain -> ip
   * "co_occurs"     entity <-> entity   (appeared in the same response)
   * "mentions"      source -> entity
   * "located_in"    entity -> place
   * "registered_by" domain -> org
   * "has_cve"       ip/port -> cve

GraphML is dumped to disk for analysis in Gephi / Cytoscape / Neo4j.
"""
from __future__ import annotations

import json
import logging
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import networkx as nx

from .config import CATEGORY_PALETTE, GRAPH_PATH, KG_MAX_COOCCUR_ENTITIES
from .entity_extraction import Entity

log = logging.getLogger("estorides.kg")


# Each entity type gets a node kind and a default visualisation color.
NODE_KIND: Dict[str, str] = {
    "ipv4": "ip", "ipv6": "ip", "asn": "infrastructure",
    "domain": "domain", "url": "url",
    "email": "person", "btc_address": "crypto", "eth_address": "crypto",
    "phone_e164": "person",
    "md5": "hash", "sha1": "hash", "sha256": "hash", "bitcoin_tx": "crypto",
    "cve": "vulnerability", "ghsa": "vulnerability",
    "mac": "device", "user_agent": "user_agent",
}

# Edges inferred from value-level co-occurrence.
CO_OCCUR_EDGE = "co_occurs"


class KnowledgeGraph:
    def __init__(self, name: str = "estorides") -> None:
        self.name = name
        self.graph = nx.MultiDiGraph()
        self._node_seq = 0

    # ---------------------------------------------------------------- ndoes
    def add_entity(self, entity: Entity) -> str:
        """Insert an entity. Returns the node id used."""
        node_id = self._node_id(entity.type, entity.value)
        if node_id in self.graph:
            # enrich metadata incrementally
            node = self.graph.nodes[node_id]
            node["seen_count"] = node.get("seen_count", 1) + 1
            srcs = node.setdefault("sources", set())
            srcs.add(entity.source)
            if entity.context and entity.context not in node.get("contexts", []):
                node.setdefault("contexts", []).append(entity.context)
        else:
            self.graph.add_node(
                node_id,
                id=node_id,
                type=entity.type,
                value=entity.value,
                kind=NODE_KIND.get(entity.type, entity.type),
                color=self._node_color(entity.type),
                seen_count=1,
                sources={entity.source},
                contexts=[entity.context] if entity.context else [],
                first_seen=time.time(),
            )
        # observed_by edge
        src_id = self._source_node(entity.source)
        self.graph.add_edge(node_id, src_id, relation="observed_by",
                            source=entity.source, target=entity.value)
        return node_id

    def add_observation(self, source: str, entities: List[Entity]) -> None:
        """Add every entity + every co-occurrence edge within the same response."""
        if not entities:
            return
        node_ids = [self.add_entity(e) for e in entities]
        # Pairwise co-occurrence, but capped: a clique over hundreds of entities
        # is O(n^2) and explodes the graph. Dedupe and keep the first N nodes so
        # the per-source contribution is bounded by KG_MAX_COOCCUR_ENTITIES^2.
        unique_ids = list(dict.fromkeys(node_ids))[:KG_MAX_COOCCUR_ENTITIES]
        for i in range(len(unique_ids)):
            for j in range(i + 1, len(unique_ids)):
                a, b = unique_ids[i], unique_ids[j]
                self.graph.add_edge(a, b, relation=CO_OCCUR_EDGE, source=source)
                self.graph.add_edge(b, a, relation=CO_OCCUR_EDGE, source=source)

    def add_relationship(self, src_type: str, src_value: str,
                         rel: str, dst_type: str, dst_value: str,
                         **attrs: Any) -> None:
        a = self._node_id(src_type, src_value)
        b = self._node_id(dst_type, dst_value)
        self.graph.add_edge(a, b, relation=rel, **attrs)

    # ----------------------------------------------------------------- io
    def export_graphml(self, path: Optional[Path] = None) -> Path:
        path = path or GRAPH_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        # NetworkX requires attribute types to be simple; we serialise sets/lists
        # to JSON strings because GraphML has no list type.
        cleaned = self.graph.copy()
        for _, data in cleaned.nodes(data=True):
            for k, v in list(data.items()):
                if isinstance(v, set):
                    data[k] = json.dumps(sorted(v))
                elif isinstance(v, (list, tuple)):
                    data[k] = json.dumps(v)
                elif isinstance(v, frozenset):
                    data[k] = json.dumps(sorted(v))
        nx.write_graphml(cleaned, str(path))
        log.info("graph exported to %s (%d nodes, %d edges)",
                 path, self.graph.number_of_nodes(), self.graph.number_of_edges())
        return path

    def export_json(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "nodes": [
                {**data, "sources": sorted(data.get("sources", []))}
                for _, data in self.graph.nodes(data=True)
            ],
            "edges": [
                {"source": u, "target": v, **attrs}
                for u, v, attrs in self.graph.edges(data=True)
            ],
        }

    # ------------------------------------------------------------- analytics
    def summary(self) -> Dict[str, Any]:
        g = self.graph
        type_counts: Counter[str] = Counter()
        for _, d in g.nodes(data=True):
            type_counts[d.get("type", "unknown")] += 1
        cat_counts: Counter[str] = Counter()
        for _, d in g.nodes(data=True):
            kind = d.get("kind", "unknown")
            cat_counts[kind] += 1
        return {
            "node_count": g.number_of_nodes(),
            "edge_count": g.number_of_edges(),
            "types": dict(type_counts.most_common(20)),
            "kinds": dict(cat_counts.most_common(20)),
            "density": nx.density(g),
            "components": nx.number_weakly_connected_components(g),
        }

    def top_entities(self, n: int = 20, by: str = "degree") -> List[Dict[str, Any]]:
        g = self.graph
        if by == "betweenness":
            scores = nx.betweenness_centrality(g)
        elif by == "pagerank":
            scores = nx.pagerank(g)
        else:
            scores = dict(g.degree())
        ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:n]
        return [
            {
                "id": nid,
                "type": g.nodes[nid].get("type"),
                "value": g.nodes[nid].get("value"),
                "score": score,
                "kind": g.nodes[nid].get("kind"),
            }
            for nid, score in ranked
        ]

    def ego_subgraph(self, node_id: str, radius: int = 1) -> "KnowledgeGraph":
        if node_id not in self.graph:
            raise KeyError(node_id)
        nodes = {node_id} | set(nx.single_source_shortest_path_length(
            self.graph.to_undirected(), node_id, cutoff=radius
        ).keys())
        sub = self.graph.subgraph(nodes).copy()
        kg = KnowledgeGraph(f"{self.name}:{node_id}")
        kg.graph = sub
        return kg

    def neighbours(self, node_id: str, relation: Optional[str] = None) -> List[Dict[str, Any]]:
        if node_id not in self.graph:
            return []
        out = []
        for _, dst, data in self.graph.out_edges(node_id, data=True):
            if relation and data.get("relation") != relation:
                continue
            out.append({
                "node": dst,
                "value": self.graph.nodes[dst].get("value"),
                "type": self.graph.nodes[dst].get("type"),
                "relation": data.get("relation"),
            })
        return out

    # ---------------------------------------------------------- internals ---
    def _node_id(self, kind: str, value: str) -> str:
        return f"{kind}:{value.lower()}"

    def _source_node(self, source: str) -> str:
        sid = f"source:{source}"
        if sid not in self.graph:
            self.graph.add_node(
                sid,
                id=sid, type="source", value=source, kind="source",
                color="#888888", seen_count=0,
            )
        return sid

    def _node_color(self, ent_type: str) -> str:
        # Pick a color based on entity type — readable in Cytoscape/Gephi.
        palette = {
            "domain": "#5B8FF9", "ipv4": "#F6BD16", "ipv6": "#F6BD16",
            "email": "#9270CA", "url": "#5AD8A6", "cve": "#FF6B6B",
            "btc_address": "#F99F80", "eth_address": "#F99F80",
            "asn": "#FF99C3", "phone_e164": "#9FB40F",
            "md5": "#C25B5B", "sha1": "#C25B5B", "sha256": "#C25B5B",
            "ghsa": "#FF6B6B", "mac": "#269A99",
        }
        return palette.get(ent_type, "#9CA3AF")
