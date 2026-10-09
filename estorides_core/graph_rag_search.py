"""graph_rag_search: GraphRAG local/global para la IA local (sin LLM).

Porta ``readmenator/_graphrag.py`` + ``_rank.py`` al grafo OSINT:
indice tipado (entidades, relaciones, text units, reportes de comunidad),
BM25 lexico, PageRank global, Personalized PageRank (busqueda local) y
map-reduce sobre reportes (busqueda global). Todo extractivo,
determinista, puro y sin I/O.
"""

from __future__ import annotations

import math
import re
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from typing import Any

from estorides_core.envutil import env_float, env_int

SCHEMA_VERSION = 1
MAX_LABEL_CHARS = 512
MAX_DETAIL_CHARS = 2000
MAX_BUDGET_CHARS = 200000
CONTEXT_LABEL_CHARS = 200

RELATION_WEIGHTS: dict[str, float] = {
    "resolves-to": 1.0,
    "same-as": 1.0,
    "contains": 0.9,
    "related-to": 0.8,
    "member_of": 0.5,
    "layered_as": 0.4,
}
DEFAULT_REL_WEIGHT = 0.6

GLOBAL_HINTS = frozenset({
    "overview", "summary", "summarize", "summarise", "all", "everything",
    "landscape", "themes", "whole", "entire", "corpus", "briefing",
})

STOPWORDS = frozenset({
    "the", "and", "for", "with", "from", "that", "this", "what",
    "which", "where", "when", "does", "show", "list", "about",
    "are", "has", "have", "all", "any", "our", "your", "como",
    "para", "que", "los", "las", "una", "este", "esta",
})

_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*")
_CAMEL_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")


@dataclass(frozen=True)
class GraphRagConfig:
    """Presupuestos y pesos de retrieval (env `ESTORIDES_GRAPHRAG_*`)."""

    bm25_k1: float = 1.2
    bm25_b: float = 0.75
    min_token_len: int = 3
    alpha: float = 0.85
    ppr_alpha: float = 0.85
    max_iter: int = 100
    tolerance: float = 1e-6
    seed_top_k: int = 8
    local_top_entities: int = 12
    local_top_relations: int = 20
    local_top_reports: int = 3
    local_top_units: int = 8
    global_top_reports: int = 4
    context_budget_tokens: int = 1500
    chars_per_token: int = 4
    report_max_findings: int = 6
    report_key_entities: int = 8


def graph_rag_config_from_env() -> GraphRagConfig:
    """Construye la config desde env; malformada → defaults (nunca raise)."""
    return GraphRagConfig(
        bm25_k1=env_float("ESTORIDES_GRAPHRAG_BM25_K1", 1.2),
        bm25_b=env_float("ESTORIDES_GRAPHRAG_BM25_B", 0.75),
        min_token_len=env_int("ESTORIDES_GRAPHRAG_MIN_TOKEN_LEN", 3),
        alpha=env_float("ESTORIDES_GRAPHRAG_ALPHA", 0.85),
        ppr_alpha=env_float("ESTORIDES_GRAPHRAG_PPR_ALPHA", 0.85),
        max_iter=env_int("ESTORIDES_GRAPHRAG_MAX_ITER", 100),
        tolerance=env_float("ESTORIDES_GRAPHRAG_TOLERANCE", 1e-6),
        seed_top_k=env_int("ESTORIDES_GRAPHRAG_SEED_TOP_K", 8),
        local_top_entities=env_int("ESTORIDES_GRAPHRAG_LOCAL_TOP_ENTITIES", 12),
        local_top_relations=env_int("ESTORIDES_GRAPHRAG_LOCAL_TOP_RELATIONS", 20),
        local_top_reports=env_int("ESTORIDES_GRAPHRAG_LOCAL_TOP_REPORTS", 3),
        local_top_units=env_int("ESTORIDES_GRAPHRAG_LOCAL_TOP_UNITS", 8),
        global_top_reports=env_int("ESTORIDES_GRAPHRAG_GLOBAL_TOP_REPORTS", 4),
        context_budget_tokens=env_int("ESTORIDES_GRAPHRAG_CONTEXT_BUDGET_TOKENS", 1500),
        chars_per_token=env_int("ESTORIDES_GRAPHRAG_CHARS_PER_TOKEN", 4),
        report_max_findings=env_int("ESTORIDES_GRAPHRAG_REPORT_MAX_FINDINGS", 6),
        report_key_entities=env_int("ESTORIDES_GRAPHRAG_REPORT_KEY_ENTITIES", 8),
    )


def tokenize(text: str, min_len: int, stopwords: set[str]) -> list[str]:
    """Parte en tokens minusculos; camelCase se divide y se conserva entero."""
    out: list[str] = []
    for raw in _TOKEN_RE.findall(text or ""):
        parts = [p.lower() for p in _CAMEL_RE.split(raw) if p]
        whole = raw.lower()
        if len(parts) > 1 and len(whole) >= min_len and whole not in stopwords:
            out.append(whole)
        for part in parts:
            if len(part) >= min_len and part not in stopwords and not part.isdigit():
                out.append(part)
    return out


class Bm25Index:
    """Okapi BM25 sobre un corpus fijo de listas de tokens."""

    def __init__(self, documents: Sequence[Sequence[str]], k1: float, b: float) -> None:
        self._k1 = k1
        self._b = b
        self._tf: list[dict[str, int]] = []
        self._len: list[int] = []
        df: dict[str, int] = {}
        for doc in documents:
            counts: dict[str, int] = {}
            for token in doc:
                counts[token] = counts.get(token, 0) + 1
            self._tf.append(counts)
            self._len.append(len(doc))
            for token in counts:
                df[token] = df.get(token, 0) + 1
        total = len(self._tf)
        self._avg = (sum(self._len) / total) if total else 0.0
        self._idf = {
            token: math.log(1.0 + (total - freq + 0.5) / (freq + 0.5))
            for token, freq in df.items()
        }

    def scores(self, query: Sequence[str]) -> list[float]:
        """Un score BM25 por documento, en orden de corpus."""
        unique = sorted(set(query))
        out: list[float] = []
        avg = self._avg or 1.0
        for counts, length in zip(self._tf, self._len, strict=True):
            score = 0.0
            norm = self._k1 * (1.0 - self._b + self._b * length / avg)
            for token in unique:
                tf = counts.get(token)
                if not tf:
                    continue
                score += self._idf.get(token, 0.0) * tf * (self._k1 + 1.0) / (tf + norm)
            out.append(score)
        return out


def _stochastic(
    ids: list[str], edges: Sequence[tuple[str, str, float]]
) -> tuple[list[list[tuple[int, float]]], list[int]]:
    """Filas estocasticas (indice, prob) + nodos dangling, orden determinista."""
    index = {nid: i for i, nid in enumerate(ids)}
    mass: list[dict[int, float]] = [{} for _ in ids]
    for src, dst, weight in edges:
        i, j = index.get(src, -1), index.get(dst, -1)
        if i < 0 or j < 0 or i == j or weight <= 0:
            continue
        mass[i][j] = mass[i].get(j, 0.0) + weight
    rows: list[list[tuple[int, float]]] = []
    dangling: list[int] = []
    for i, row in enumerate(mass):
        total = sum(row.values())
        if total <= 0:
            dangling.append(i)
            rows.append([])
        else:
            rows.append(sorted(((j, w / total) for j, w in row.items())))
    return rows, dangling


def pagerank(
    ids: Sequence[str],
    edges: Sequence[tuple[str, str, float]],
    alpha: float = 0.85,
    max_iter: int = 100,
    tolerance: float = 1e-6,
) -> dict[str, float]:
    """PageRank dirigido y pesado; los scores suman 1 (determinista)."""
    ordered = sorted(ids)
    n = len(ordered)
    if not n:
        return {}
    rows, dangling = _stochastic(ordered, edges)
    rank = [1.0 / n] * n
    for _ in range(max(1, max_iter)):
        new_rank = [0.0] * n
        dangling_sum = sum(rank[i] for i in dangling)
        for i, row in enumerate(rows):
            if row:
                for j, prob in row:
                    new_rank[j] += alpha * rank[i] * prob
        teleport = (1.0 - alpha) / n + alpha * dangling_sum / n
        for i in range(n):
            new_rank[i] += teleport
        if sum(abs(new_rank[i] - rank[i]) for i in range(n)) < tolerance:
            rank = new_rank
            break
        rank = new_rank
    return dict(zip(ordered, rank, strict=True))


def personalized_pagerank(
    ids: Sequence[str],
    edges: Sequence[tuple[str, str, float]],
    seeds: dict[str, float],
    alpha: float = 0.85,
    max_iter: int = 100,
    tolerance: float = 1e-6,
) -> dict[str, float]:
    """PPR con teletransporte al seed; seeds ajenos se ignoran."""
    ordered = sorted(ids)
    n = len(ordered)
    if not n:
        return {}
    rows, dangling = _stochastic(ordered, edges)
    index = {nid: i for i, nid in enumerate(ordered)}
    personal = [0.0] * n
    for nid, w in seeds.items():
        i = index.get(nid)
        if i is not None and w > 0:
            personal[i] = w
    total = sum(personal)
    if total <= 0:
        personal = [1.0 / n] * n
    else:
        personal = [w / total for w in personal]
    rank = [1.0 / n] * n
    for _ in range(max(1, max_iter)):
        new_rank = [0.0] * n
        dangling_sum = sum(rank[i] for i in dangling)
        for i, row in enumerate(rows):
            if row:
                for j, prob in row:
                    new_rank[j] += alpha * rank[i] * prob
        spread = (1.0 - alpha) + alpha * dangling_sum
        for i in range(n):
            new_rank[i] += spread * personal[i]
        if sum(abs(new_rank[i] - rank[i]) for i in range(n)) < tolerance:
            rank = new_rank
            break
        rank = new_rank
    return dict(zip(ordered, rank, strict=True))


def _md_safe(text: str, limit: int = CONTEXT_LABEL_CHARS) -> str:
    """Gemelo de graph_force._md_safe: neutraliza markdown hostil."""
    clean = text.replace("\r", " ").replace("`", "'").replace("```", "'''")
    clean = " ".join(clean.split())
    if len(clean) > limit:
        clean = clean[:limit] + "…"
    return clean


@dataclass(frozen=True)
class RagEntity:
    entity_id: str
    name: str
    kind: str
    cluster: int
    degree: int
    rank: float
    description: str


@dataclass(frozen=True)
class RagRelation:
    source: str
    target: str
    relation: str
    weight: float
    confidence: str
    description: str


@dataclass(frozen=True)
class RagTextUnit:
    unit_id: str
    entity_id: str
    location: str
    text: str


@dataclass
class RagCommunity:
    community_id: str
    level: int
    parent: str
    children: list[str]
    title: str
    member_ids: list[str]
    summary: str
    findings: list[str]
    key_entities: list[str]
    key_relations: list[str]
    rating: float
    rating_explanation: str


@dataclass
class RagContext:
    query: str
    mode: str
    entities: list[tuple[str, float]]
    relations: list[str]
    reports: list[str]
    text_units: list[str]
    markdown: str
    approx_tokens: int


@dataclass
class GraphRagIndex:
    entities: list[RagEntity] = field(default_factory=list)
    relationships: list[RagRelation] = field(default_factory=list)
    communities: list[RagCommunity] = field(default_factory=list)
    text_units: list[RagTextUnit] = field(default_factory=list)
    meta: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {
            "meta": dict(self.meta),
            "entities": [asdict(e) for e in self.entities],
            "relationships": [asdict(r) for r in self.relationships],
            "communities": [asdict(c) for c in self.communities],
            "text_units": [asdict(t) for t in self.text_units],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> GraphRagIndex:
        def rows(name: str) -> list[dict[str, Any]]:
            value = data.get(name, [])
            if not isinstance(value, list):
                return []
            return [r for r in value if isinstance(r, dict)]

        def meta() -> dict[str, object]:
            value = data.get("meta", {})
            return dict(value) if isinstance(value, dict) else {}

        return cls(
            entities=[RagEntity(**e) for e in rows("entities")],
            relationships=[RagRelation(**r) for r in rows("relationships")],
            communities=[RagCommunity(**c) for c in rows("communities")],
            text_units=[RagTextUnit(**t) for t in rows("text_units")],
            meta=meta(),
        )


def _req_str(item: dict[str, Any], key: str, default: str, what: str) -> str:
    value = item.get(key, default)
    if value is None:
        return default
    if isinstance(value, str):
        return value
    raise TypeError(f"graph_rag_search: {what} field {key!r} is not a string")


def _opt_str(item: dict[str, Any], key: str, default: str) -> str:
    value = item.get(key, default)
    return value if isinstance(value, str) else default


def _opt_int(item: dict[str, Any], key: str, default: int) -> int:
    value = item.get(key, default)
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _rel_weight(relation: str) -> float:
    return RELATION_WEIGHTS.get(relation, DEFAULT_REL_WEIGHT)


def build_index(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    clusters: list[dict[str, Any]] | None = None,
    config: GraphRagConfig | None = None,
) -> GraphRagIndex:
    """Indice extractivo desde nodos/edges estilo `/api/graph` (puro)."""
    cfg = config or GraphRagConfig()
    clean: list[dict[str, Any]] = []
    for raw in nodes:
        if not isinstance(raw, dict):
            raise TypeError("graph_rag_search: node is not a dict")
        nid = _req_str(raw, "id", "", "node")
        label = _req_str(raw, "label", nid, "node")[:MAX_LABEL_CHARS] or nid
        kind = _opt_str(raw, "kind", _opt_str(raw, "type", "unknown"))
        detail = _opt_str(raw, "detail", "")
        if "detail" in raw and not isinstance(raw["detail"], str):
            raise TypeError("graph_rag_search: node field 'detail' is not a string")
        clean.append({
            "id": nid, "label": label, "kind": kind,
            "cluster": _opt_int(raw, "cluster", -1),
            "level": _opt_str(raw, "level", "data"),
            "detail": detail[:MAX_DETAIL_CHARS],
        })
    known = {n["id"] for n in clean}
    degree: dict[str, int] = {nid: 0 for nid in known}
    weighted: list[tuple[str, str, float]] = []
    relations: dict[tuple[str, str, str], RagRelation] = {}
    dropped = 0
    for raw in edges:
        if not isinstance(raw, dict):
            dropped += 1
            continue
        try:
            src = _req_str(raw, "source", "", "edge")
            dst = _req_str(raw, "target", "", "edge")
        except TypeError:
            dropped += 1
            continue
        if src not in known or dst not in known or src == dst:
            dropped += 1
            continue
        relation = _opt_str(raw, "relation", "related-to")
        weight = round(_rel_weight(relation), 3)
        key = (src, dst, relation)
        if key not in relations:
            relations[key] = RagRelation(
                src, dst, relation, weight, "EXTRACTED",
                f"{src} --{relation}--> {dst}",
            )
        weighted.append((src, dst, weight))
        degree[src] += 1
        degree[dst] += 1

    rank = pagerank(sorted(known), weighted, cfg.alpha, cfg.max_iter, cfg.tolerance)
    max_rank = max(rank.values()) if rank else 0.0

    cluster_label: dict[int, str] = {}
    for raw in clusters or []:
        if isinstance(raw, dict):
            cid = _opt_int(raw, "id", -999)
            if cid >= 0:
                cluster_label[cid] = _opt_str(raw, "label", f"cluster {cid}")

    def where(cid: int) -> str:
        if cid < 0:
            return "unassigned"
        return cluster_label.get(cid, f"cluster {cid}")

    entities = [
        RagEntity(
            entity_id=n["id"], name=n["label"], kind=n["kind"],
            cluster=n["cluster"], degree=degree[n["id"]],
            rank=round(rank.get(n["id"], 0.0), 6),
            description=(
                f"{n['kind']} '{n['label']}' in {where(n['cluster'])}, "
                f"level {n['level']}, degree {degree[n['id']]}."
            ),
        )
        for n in sorted(clean, key=lambda x: x["id"])
    ]
    units = [
        RagTextUnit(
            unit_id=f"{n['id']}#u0", entity_id=n["id"], location=n["label"],
            text=n["detail"] or (
                f"{n['kind']} {n['label']} (cluster {n['cluster']}, "
                f"level {n['level']}, degree {degree[n['id']]})"
            ),
        )
        for n in sorted(clean, key=lambda x: x["id"])
    ]
    communities = _reports(clean, degree, rank, max_rank, weighted, cluster_label, cfg)
    kind_counts: dict[str, int] = {}
    for entity in entities:
        kind_counts[entity.kind] = kind_counts.get(entity.kind, 0) + 1
    meta: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "entities": len(entities),
        "relationships": len(relations),
        "communities": sum(1 for c in communities if c.level == 0),
        "text_units": len(units),
        "dropped_edges": dropped,
        "entity_kinds": dict(sorted(kind_counts.items())),
    }
    return GraphRagIndex(entities, sorted(
        relations.values(), key=lambda r: (r.source, r.target, r.relation),
    ), communities, units, meta)


def _reports(
    nodes: list[dict[str, Any]],
    degree: dict[str, int],
    rank: dict[str, float],
    top_mass: float,
    weighted: list[tuple[str, str, float]],
    cluster_label: dict[int, str],
    cfg: GraphRagConfig,
) -> list[RagCommunity]:
    """Un reporte extractivo por cluster + raiz (determinista)."""
    groups: dict[int, list[str]] = {}
    for node in nodes:
        groups.setdefault(node["cluster"], []).append(node["id"])
    by_id = {n["id"]: n for n in nodes}
    crossing: dict[str, int] = {}
    internal: dict[int, list[tuple[str, str, str]]] = {}
    bridge_total = 0
    for src, dst, _w in weighted:
        a, b = by_id[src]["cluster"], by_id[dst]["cluster"]
        if a == b:
            internal.setdefault(a, []).append((src, dst, ""))
        else:
            crossing[f"c{a}"] = crossing.get(f"c{a}", 0) + 1
            crossing[f"c{b}"] = crossing.get(f"c{b}", 0) + 1
            bridge_total += 1
    mass = {
        cid: sum(rank.get(i, 0.0) for i in members)
        for cid, members in groups.items()
    }
    top = max(mass.values()) if mass else 0.0
    max_cross = max(crossing.values()) if crossing else 0
    reports: list[RagCommunity] = []
    for cid in sorted(groups):
        members = sorted(groups[cid], key=lambda i: (-rank.get(i, 0.0), i))
        cid_str = f"c{cid}" if cid >= 0 else "unassigned"
        title = cluster_label.get(cid, f"cluster {cid}") if cid >= 0 else "unassigned"
        ranked_labels = sorted(members, key=lambda i: (-rank.get(i, 0.0), i))
        findings = [
            f"`{by_id[i]['label']}` [{by_id[i]['kind']}] degree "
            f"{degree.get(i, 0)}, level {by_id[i]['level']}."
            for i in ranked_labels[:3]
        ]
        bridges = [
            f"`{by_id[s]['label']}` links `{by_id[t]['label']}` "
            f"(to {cluster_label.get(by_id[t]['cluster'], 'unassigned')})."
            for s, t, _w in sorted(weighted)
            if (by_id[s]["cluster"] == cid) != (by_id[t]["cluster"] == cid)
        ][:2]
        findings.extend(bridges)
        key_relations = [
            f"{s} -> {t}" for s, t, _r in sorted(internal.get(cid, []))
        ][: cfg.report_key_entities]
        rating = round(
            8.0 * (mass[cid] / top if top > 0 else 0.0)
            + 2.0 * (crossing.get(cid_str, 0) / max_cross if max_cross else 0.0),
            1,
        )
        summary = (
            f"{len(members)} entities"
            + (f" in {title}" if cid >= 0 else "")
            + f". Core: `{by_id[members[0]]['label']}` "
            f"(rank {rank.get(members[0], 0.0):.4f})."
            if members else "Empty community."
        )
        reports.append(RagCommunity(
            community_id=cid_str, level=0, parent="root", children=[],
            title=title, member_ids=sorted(members), summary=summary,
            findings=findings[: cfg.report_max_findings],
            key_entities=members[: cfg.report_key_entities],
            key_relations=key_relations, rating=rating,
            rating_explanation=(
                f"Rating {rating}/10 = 8 x PageRank share "
                f"{(mass[cid] / top if top > 0 else 0.0):.2f} + 2 x bridge share "
                f"{(crossing.get(cid_str, 0) / max_cross if max_cross else 0.0):.2f} "
                f"({bridge_total} crossing edges)."
            ),
        ))
    for report in reports:
        report.parent = "root"
    top_reports = sorted(reports, key=lambda r: (-r.rating, r.community_id))
    root = RagCommunity(
        community_id="root", level=2, parent="",
        children=[r.community_id for r in reports],
        title="Project overview",
        member_ids=sorted(by_id),
        summary=(
            f"{len(by_id)} entities in {len(reports)} communities. "
            + ("Highest-impact: " + ", ".join(
                f"{r.title} ({r.rating})" for r in top_reports[:3]) + "." if top_reports else "Empty graph.")
        ),
        findings=[
            f"[{r.title}] rating {r.rating}: {r.findings[0]}"
            for r in top_reports if r.findings
        ][: cfg.report_max_findings],
        key_entities=[e for r in top_reports[:3] for e in r.key_entities[:2]],
        key_relations=[k for r in top_reports[:3] for k in r.key_relations[:2]],
        rating=top_reports[0].rating if top_reports else 0.0,
        rating_explanation="Root rating = highest community rating.",
    )
    return [*reports, root]


class GraphRagSearcher:
    """BM25 + PPR (local) y map-reduce sobre reportes (global)."""

    def __init__(
        self, config: GraphRagConfig | None, index: GraphRagIndex,
    ) -> None:
        self._config = config or GraphRagConfig()
        self._index = index
        self._stop = set(STOPWORDS)
        self._entities = {e.entity_id: e for e in index.entities}
        self._ids = [e.entity_id for e in index.entities]
        self._units_by_entity: dict[str, list[int]] = {}
        for i, unit in enumerate(index.text_units):
            self._units_by_entity.setdefault(unit.entity_id, []).append(i)
        self._reports = {c.community_id: c for c in index.communities}
        self._level0 = [c for c in index.communities if c.level == 0]
        cfg = self._config
        self._entity_bm25 = Bm25Index(
            [self._entity_doc(e) for e in index.entities], cfg.bm25_k1, cfg.bm25_b)
        self._unit_bm25 = Bm25Index(
            [self._tok(u.location + " " + u.text) for u in index.text_units],
            cfg.bm25_k1, cfg.bm25_b)
        self._report_bm25 = Bm25Index(
            [self._tok(" ".join([c.title, c.summary, *c.findings, *c.member_ids]))
             for c in self._level0],
            cfg.bm25_k1, cfg.bm25_b)
        self._sym_edges = self._symmetric_edges()

    def _tok(self, text: str) -> list[str]:
        return tokenize(text, self._config.min_token_len, self._stop)

    def _entity_doc(self, entity: RagEntity) -> list[str]:
        name = self._tok(entity.name)
        return name + name + self._tok(entity.kind) + self._tok(entity.description)

    def _symmetric_edges(self) -> list[tuple[str, str, float]]:
        out: list[tuple[str, str, float]] = []
        for rel in self._index.relationships:
            out.append((rel.source, rel.target, rel.weight))
            out.append((rel.target, rel.source, rel.weight))
        return sorted(out)

    def choose_mode(self, query: str) -> str:
        raw = set(tokenize(query, 1, set()))
        if raw & GLOBAL_HINTS:
            return "global"
        tokens = self._tok(query)
        if not tokens or not any(s > 0 for s in self._entity_bm25.scores(tokens)):
            return "global"
        return "local"

    def search(
        self, query: str, mode: str = "auto", budget_tokens: int = 0,
    ) -> RagContext:
        chosen = self.choose_mode(query) if mode == "auto" else mode
        if chosen == "global":
            return self.global_search(query, budget_tokens)
        return self.local_search(query, budget_tokens)

    def _budget_chars(self, budget_tokens: int) -> int:
        tokens = budget_tokens or self._config.context_budget_tokens
        if tokens <= 0:
            raise ValueError("graph_rag_search: budget_tokens must be positive")
        return min(max(1, tokens) * max(1, self._config.chars_per_token), MAX_BUDGET_CHARS)

    def local_search(self, query: str, budget_tokens: int = 0) -> RagContext:
        cfg = self._config
        tokens = self._tok(query)
        entity_scores = self._entity_bm25.scores(tokens) if tokens else []
        unit_scores = self._unit_bm25.scores(tokens) if tokens else []
        seeds: dict[str, float] = {}
        ranked_entities = sorted(
            (i for i, s in enumerate(entity_scores) if s > 0),
            key=lambda i: (-entity_scores[i], self._ids[i]),
        )[: cfg.seed_top_k]
        for i in ranked_entities:
            seeds[self._ids[i]] = entity_scores[i]
        ranked_units = sorted(
            (i for i, s in enumerate(unit_scores) if s > 0),
            key=lambda i: (-unit_scores[i], self._index.text_units[i].unit_id),
        )[: cfg.seed_top_k]
        top_unit = unit_scores[ranked_units[0]] if ranked_units else 1.0
        top_entity = entity_scores[ranked_entities[0]] if ranked_entities else 1.0
        for i in ranked_units:
            eid = self._index.text_units[i].entity_id
            seeds[eid] = seeds.get(eid, 0.0) + 0.5 * top_entity * unit_scores[i] / (top_unit or 1.0)
        # Boost determinista al nombre exacto: buscar "example.com" debe
        # devolver example.com primero aunque un hub acumule mas PPR.
        norm_q = " ".join(query.lower().split())
        exact: set[str] = set()
        if norm_q:
            for eid in self._ids:
                if self._entities[eid].name.lower().strip() == norm_q:
                    exact.add(eid)
                    seeds[eid] = seeds.get(eid, top_entity or 1.0) * 3.0
        if not seeds:
            text = f"# GraphRAG local context: {_md_safe(query)}\n\nNo entity matches `{_md_safe(query, 60)}`. Try global mode.\n"
            return RagContext(query, "local", [], [], [], [], text, len(text) // 4)
        ppr = personalized_pagerank(
            self._ids, self._sym_edges, seeds,
            cfg.ppr_alpha, cfg.max_iter, cfg.tolerance)
        ranked = sorted(
            ((eid, score) for eid, score in ppr.items() if score > 0),
            key=lambda kv: (-kv[1], kv[0]),
        )
        # Pin top-1: el nombre exacto abre la lista (entre exactos, por
        # score). El resto sigue orden PPR puro.
        pinned = sorted(
            ((eid, score) for eid, score in ranked if eid in exact),
            key=lambda kv: (-kv[1], kv[0]),
        )
        rest = [(eid, score) for eid, score in ranked if eid not in exact]
        top = (pinned + rest)[: cfg.local_top_entities]
        chosen = {eid for eid, _ in top}
        relations = sorted(
            (r for r in self._index.relationships
             if r.source in chosen and r.target in chosen),
            key=lambda r: (-(ppr.get(r.source, 0.0) + ppr.get(r.target, 0.0)) * r.weight,
                           r.source, r.target),
        )[: cfg.local_top_relations]
        report_mass: dict[str, float] = {}
        for eid, score in top:
            entity = self._entities[eid]
            for report in self._level0:
                if eid in report.member_ids and entity.cluster >= -999:
                    report_mass[report.community_id] = report_mass.get(report.community_id, 0.0) + score
                    break
        reports = [cid for cid, _m in sorted(
            report_mass.items(), key=lambda kv: (-kv[1], kv[0]))][: cfg.local_top_reports]
        unit_rank: dict[int, float] = {}
        for eid, score in top:
            for ui in self._units_by_entity.get(eid, []):
                unit_rank[ui] = score * (1.0 + (unit_scores[ui] / top_unit if unit_scores else 0.0))
        units = [i for i, _s in sorted(
            unit_rank.items(), key=lambda kv: (-kv[1], kv[0]))][: cfg.local_top_units]
        sections = [
            ("Entities", [
                f"- `{_md_safe(self._entities[eid].name)}` "
                f"[{self._entities[eid].kind}] cluster={self._entities[eid].cluster} "
                f"score={score:.4f}: {_md_safe(self._entities[eid].description)}"
                for eid, score in top
            ]),
            ("Relationships", [
                f"- {_md_safe(self._entities[r.source].name)} "
                f"--{r.relation}--> {_md_safe(self._entities[r.target].name)} "
                f"({r.confidence}, w={r.weight})"
                for r in relations
                if r.source in self._entities and r.target in self._entities
            ]),
            ("Community reports", [self._report_block(self._reports[cid]) for cid in reports]),
            ("Sources", [self._unit_block(self._index.text_units[i]) for i in units]),
        ]
        markdown, used = self._pack(
            f"# GraphRAG local context: {_md_safe(query, 120)}",
            sections, budget_tokens, (0.4, 0.25, 0.2, 0.15))
        return RagContext(
            query, "local", top,
            [f"{r.source} --{r.relation}--> {r.target}" for r in relations],
            reports, [self._index.text_units[i].unit_id for i in units],
            markdown, used)

    def global_search(self, query: str, budget_tokens: int = 0) -> RagContext:
        cfg = self._config
        tokens = self._tok(query)
        scores = self._report_bm25.scores(tokens) if tokens else [0.0] * len(self._level0)
        order = sorted(
            range(len(self._level0)),
            key=lambda i: (-scores[i], -self._level0[i].rating, self._level0[i].community_id),
        )[: cfg.global_top_reports]
        query_set = set(tokens)
        mapped: list[str] = []
        chosen: list[str] = []
        for i in order:
            report = self._level0[i]
            chosen.append(report.community_id)
            matching = [f for f in report.findings if query_set & set(self._tok(f))]
            points = matching or report.findings[:2]
            mapped.append(
                f"### {_md_safe(report.title)} (`{report.community_id}`, "
                f"rating {report.rating}, relevance {scores[i]:.2f})\n"
                + _md_safe(report.summary) + "\n"
                + "\n".join(f"- {_md_safe(p)}" for p in points)
            )
        root = self._reports.get("root")
        overview: list[str] = []
        if root is not None:
            overview.append(_md_safe(root.summary))
        for report in self._level0:
            overview.append(
                f"- `{report.community_id}` {_md_safe(report.title)}: "
                f"{len(report.member_ids)} entities, rating {report.rating}")
        sections = [
            ("Overview", overview),
            ("Relevant communities (map-reduce)", mapped),
        ]
        markdown, used = self._pack(
            f"# GraphRAG global context: {_md_safe(query, 120)}",
            sections, budget_tokens, (0.4, 0.6))
        return RagContext(query, "global", [], [], chosen, [], markdown, used)

    @staticmethod
    def _report_block(report: RagCommunity) -> str:
        lines = [f"### {_md_safe(report.title)} (`{report.community_id}`, "
                 f"rating {report.rating})", _md_safe(report.summary, 500)]
        lines.extend(f"- {_md_safe(item, 300)}" for item in report.findings)
        return "\n".join(lines)

    @staticmethod
    def _unit_block(unit: RagTextUnit) -> str:
        return f"`{_md_safe(unit.location, 80)}`\n```\n{_md_safe(unit.text, 800)}\n```"

    def _pack(
        self, header: str, sections: list[tuple[str, list[str]]],
        budget_tokens: int, shares: Sequence[float],
    ) -> tuple[str, int]:
        budget = self._budget_chars(budget_tokens)
        text, dropped = self._pack_with(header, sections, shares, budget)
        if dropped:
            # Segunda pasada con guarda para el marcador + posible cierre
            # de fence; si nada se pierde, no hay marcador (honesto).
            text2, dropped2 = self._pack_with(header, sections, shares, budget - 32)
            if dropped2:
                text = text2
                if text.count("```") % 2 == 1:
                    text += "\n```"
                text += "\n…truncated\n"
            else:
                text = text2
        return text, len(text) // max(1, self._config.chars_per_token)

    def _pack_with(
        self, header: str, sections: list[tuple[str, list[str]]],
        shares: Sequence[float], budget: int,
    ) -> tuple[str, bool]:
        """Empaqueta por shares; devuelve (texto, hubo_recorte)."""
        out = [header, ""]
        used = len(header) + 2
        carry = 0
        dropped = False
        total_share = sum(shares[: len(sections)]) or 1.0
        for position, (title, items) in enumerate(sections):
            share = shares[position] if position < len(shares) else 0.0
            allowance = int((budget - len(header) - 2) * share / total_share) + carry
            heading = f"## {title}"
            spent = len(heading) + 2
            kept: list[str] = []
            for item in items:
                if spent + len(item) + 1 > allowance or used + spent + len(item) + 1 > budget:
                    dropped = True
                    break
                kept.append(item)
                spent += len(item) + 1
            if kept:
                out.append(heading)
                out.extend(kept)
                out.append("")
                used += spent
                carry = max(0, allowance - spent)
            else:
                carry = allowance
        text = "\n".join(out).rstrip() + "\n"
        return text, dropped


def ask_context(
    query: str,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    clusters: list[dict[str, Any]] | None = None,
    budget_tokens: int = 0,
    mode: str = "auto",
    config: GraphRagConfig | None = None,
) -> RagContext:
    """One-shot: build + search (el camino que usa la capa IA local)."""
    cfg = config or GraphRagConfig()
    return GraphRagSearcher(cfg, build_index(nodes, edges, clusters, cfg)).search(
        query, mode, budget_tokens)


def _scalar_detail(attrs: dict[str, Any]) -> str:
    """Detalle extractivo desde atributos escalares (no escalares se ignoran)."""
    parts: list[str] = []
    for key in sorted(attrs):
        if key in ("id", "value", "type"):
            continue
        value = attrs[key]
        if isinstance(value, (str, int, float, bool)):
            parts.append(f"{key}={value}")
        if sum(len(p) for p in parts) > MAX_DETAIL_CHARS:
            break
    return "; ".join(parts)[:MAX_DETAIL_CHARS]


def graph_context_block(
    query: str,
    nx_graph: Any,
    cluster_of: dict[str, int],
    budget_tokens: int = 400,
    mode: str = "auto",
    config: GraphRagConfig | None = None,
) -> str:
    """Bloque markdown para el prompt LLM desde un grafo networkx (duck-typing).

    Grafo vacío → `""` (el caller deja el prompt intacto).
    """
    cfg = config or GraphRagConfig()
    if budget_tokens <= 0:
        raise ValueError("graph_rag_search: budget_tokens must be positive")
    raw_nodes = list(nx_graph.nodes(data=True))
    if not raw_nodes:
        return ""
    nodes: list[dict[str, Any]] = []
    for nid, attrs in raw_nodes:
        if not isinstance(nid, str):
            continue
        data = attrs if isinstance(attrs, dict) else {}
        label = data.get("value", nid)
        nodes.append({
            "id": nid,
            "label": label if isinstance(label, str) else nid,
            "type": data.get("type", "unknown") if isinstance(data.get("type", "unknown"), str) else "unknown",
            "cluster": cluster_of.get(nid, -1),
            "level": data.get("level", "data") if isinstance(data.get("level", "data"), str) else "data",
            "detail": _scalar_detail(data),
        })
    edges: list[dict[str, Any]] = []
    for src, dst, data in nx_graph.edges(data=True):
        if not isinstance(src, str) or not isinstance(dst, str):
            continue
        info = data if isinstance(data, dict) else {}
        relation = info.get("relation", "related-to")
        edges.append({
            "source": src, "target": dst,
            "relation": relation if isinstance(relation, str) else "related-to",
        })
    if not nodes:
        return ""
    return ask_context(query, nodes, edges, None, budget_tokens, mode, cfg).markdown
