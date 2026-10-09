"""graph_force3d: payload force-graph estilo ReadMenator + contexto IA.

Porta ``readmenator/_forcegraph.py`` (payload heterogeneo + SETTINGS) y el
formato RAW de ``graph-force.html`` al grafo OSINT de Estorides, mas un
constructor de contexto markdown con presupuesto de tokens para la capa
de IA local (GraphRAG extractivo, sin llamadas a LLM).

Puro y sin I/O: todo input hostil (labels remotos) se valida fail-closed
(``TypeError`` ante valores no JSON-safe) o se trunca a limites fijos.
El modulo nunca genera HTML: solo dicts JSON-safe.
"""

from __future__ import annotations

import math
from typing import Any

MAX_LABEL_CHARS = 512
MAX_NODES = 2000
MAX_EDGES = 5000
MAX_BUDGET_CHARS = 200000
DEFAULT_BUDGET_CHARS = 12000
CONTEXT_LABEL_CHARS = 200

# Paleta de edges por relacion OSINT. Mismos valores que
# readmenator FORCEGRAPH_EDGE_COLORS, renombrados a relaciones OSINT.
EDGE_COLORS: dict[str, str] = {
    "related-to": "rgba(148,163,184,.45)",
    "resolves-to": "rgba(79,239,142,.35)",
    "same-as": "rgba(239,184,79,.4)",
    "contains": "rgba(124,90,239,.45)",
    "member_of": "rgba(255,255,255,.15)",
    "layered_as": "rgba(255,255,255,.15)",
}
DEFAULT_EDGE_COLOR = "rgba(148,163,184,.18)"

# Colores de intel-tier. Espejo de LEVEL_COLORS en static/js/estorides.js
# (el JS es la fuente de verdad para display; aqui solo defaults).
TIER_COLORS: dict[str, str] = {
    "data": "#6b7280",
    "information": "#5fb4ff",
    "intelligence": "#f6bd16",
    "counter_intelligence": "#ff5c5c",
}
DEFAULT_NODE_COLOR = "#888"


def family_color_from_name(
    name: str,
    sat_base: int = 55,
    sat_span: int = 12,
    light_base: int = 58,
    light_span: int = 10,
) -> str:
    """Deriva un color HSL estable desde un label (djb2, como ReadMenator)."""
    hashed = 5381
    for char in name:
        hashed = ((hashed << 5) + hashed + ord(char)) & 0xFFFFFFFF
    hue = hashed % 360
    sat = sat_base + ((hashed >> 8) % max(1, sat_span))
    light = light_base + ((hashed >> 16) % max(1, light_span))
    return f"hsl({hue}, {sat}%, {light}%)"


def node_value(symbols: int, degree: int, findings: int = 0) -> float:
    """Escala log2 del tamano de nodo (minimo 1)."""
    return max(1.0, math.log2(float(symbols + degree + findings) + 1.0))


def force_settings() -> dict[str, Any]:
    """Valores SETTINGS de ReadMenator graph-force.html (fuente unica)."""
    return {
        "charge": -300,
        "linkDistance": 120,
        "linkStrength": 0.3,
        "nodeRelSize": 4,
        "hulls": True,
        "hullFill": 0.07,
        "hullStroke": 0.5,
        "hullPad": 18,
        "particles": 4,
        "dimNode": "rgba(80,85,110,.4)",
        "dimLink": "rgba(255,255,255,.04)",
        "mode": "2d",
        "labelTopN": 30,
        "labelZoom": 1.6,
        "labelMax": 28,
        "clusterStrength": 0.6,
        "collidePad": 4,
        "dagLevel": 60,
        "flyMs": 700,
        "flyZoom": 3.0,
        "searchResults": 8,
    }


def _req_str(item: dict[str, Any], key: str, default: str, what: str) -> str:
    """Lee un campo string obligatorio; fail-closed ante no-str."""
    value = item.get(key, default)
    if value is None:
        return default
    if isinstance(value, str):
        return value
    raise TypeError(f"graph_force: {what} field {key!r} is not a string")


def _opt_str(item: dict[str, Any], key: str, default: str) -> str:
    """Lee un campo de estilo; ante no-str usa el default (no mata el grafo)."""
    value = item.get(key, default)
    return value if isinstance(value, str) else default


def _opt_int(item: dict[str, Any], key: str, default: int) -> int:
    """Lee un campo entero; ante basura usa el default."""
    value = item.get(key, default)
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _degrees(
    node_ids: set[str], edges: list[dict[str, Any]]
) -> tuple[dict[str, int], list[dict[str, Any]]]:
    """Grado por nodo + edges validos (ambos extremos conocidos)."""
    degree: dict[str, int] = {nid: 0 for nid in node_ids}
    valid: list[dict[str, Any]] = []
    dropped = 0
    for edge in edges:
        if not isinstance(edge, dict):
            dropped += 1
            continue
        try:
            src = _req_str(edge, "source", "", "edge")
            dst = _req_str(edge, "target", "", "edge")
        except TypeError:
            dropped += 1
            continue
        if src not in node_ids or dst not in node_ids:
            dropped += 1
            continue
        valid.append(edge)
        degree[src] += 1
        degree[dst] += 1
    return degree, valid


def _is_bridge(edge: dict[str, Any]) -> bool:
    """Un edge es puente si lo declara o si une clusters distintos."""
    flag = edge.get("inter_cluster")
    if isinstance(flag, bool):
        return flag
    clusters = edge.get("clusters")
    if isinstance(clusters, (list, tuple)) and len(clusters) == 2:
        return bool(clusters[0] != clusters[1])
    return False


def build_force_payload(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    max_nodes: int = 300,
    max_edges: int = 1000,
) -> dict[str, Any]:
    """Convierte nodos/edges OSINT (`/api/graph`) al formato RAW force-graph.

    Truncacion determinista: grado desc, puentes inter-cluster primero,
    desempate por `id`. Los edges huerfanos se descartan (conteo en meta).
    """
    max_nodes = min(max(1, int(max_nodes)), MAX_NODES)
    max_edges = min(max(1, int(max_edges)), MAX_EDGES)

    clean: list[dict[str, Any]] = []
    for raw in nodes:
        if not isinstance(raw, dict):
            raise TypeError("graph_force: node is not a dict")
        nid = _req_str(raw, "id", "", "node")
        label = _req_str(raw, "label", nid, "node")[:MAX_LABEL_CHARS] or nid
        ntype = _req_str(raw, "type", "unknown", "node")
        clean.append({
            "id": nid,
            "label": label,
            "type": ntype,
            "kind": _opt_str(raw, "kind", ntype),
            "color": _opt_str(raw, "color", ""),
            "cluster_color": _opt_str(raw, "cluster_color", ""),
            "cluster": _opt_int(raw, "cluster", -1),
            "level": _opt_str(raw, "level", "data"),
        })
    node_ids = {n["id"] for n in clean}
    degree, valid_edges = _degrees(node_ids, edges)
    dropped = len(edges) - len(valid_edges)

    ordered = sorted(clean, key=lambda n: (-degree[n["id"]], n["id"]))
    # Los puentes inter-cluster se pinean primero: son la senal
    # cross-cluster (misma garantia que /api/graph, que ordena los
    # bridge edges primero para que el tope nunca los oculte).
    pinned: list[str] = sorted({
        endpoint
        for e in valid_edges
        if _is_bridge(e)
        for endpoint in (e["source"], e["target"])
        if isinstance(endpoint, str)
    })
    keep_ids: set[str] = set(pinned[:max_nodes])
    for node in ordered:
        if len(keep_ids) >= max_nodes:
            break
        keep_ids.add(node["id"])
    kept = [n for n in ordered if n["id"] in keep_ids]
    kept_ids = keep_ids
    truncated = len(ordered) > max_nodes

    cluster_label: dict[int, str] = {}
    cluster_color: dict[int, str] = {}
    for raw in clusters:
        if not isinstance(raw, dict):
            continue
        cid = _opt_int(raw, "id", -999)
        if cid < 0:
            continue
        cluster_label[cid] = _opt_str(raw, "label", f"cluster {cid}")
        cluster_color[cid] = _opt_str(raw, "color", "")

    max_deg = max(degree.values()) if degree else 0
    rank_pos = {n["id"]: i + 1 for i, n in enumerate(ordered)}

    out_nodes: dict[str, dict[str, Any]] = {}
    for node in kept:
        cid = node["cluster"]
        family = cluster_label.get(cid, node["kind"])
        color = node["cluster_color"] or node["color"]
        if not color:
            color = family_color_from_name(family)
        deg = degree[node["id"]]
        out_nodes[node["id"]] = {
            "id": node["id"],
            "label": node["label"],
            "type": "entity",
            "kind": node["kind"],
            "degree": deg,
            "findings": 0,
            "community": cid if cid >= 0 else None,
            "community_label": cluster_label.get(cid, ""),
            "family": family,
            "layer": node["level"],
            "color": color,
            "rank": round(deg / max_deg, 6) if max_deg else 0.0,
            "rank_pos": rank_pos[node["id"]],
            "val": node_value(0, deg),
            "doc": "",
        }

    for cid in sorted({n["cluster"] for n in kept if n["cluster"] >= 0}):
        size = sum(1 for n in kept if n["cluster"] == cid)
        out_nodes[f"community:{cid}"] = {
            "id": f"community:{cid}",
            "label": cluster_label.get(cid, f"cluster {cid}"),
            "type": "community",
            "community_id": cid,
            "size": size,
            "color": cluster_color.get(cid) or DEFAULT_NODE_COLOR,
            "val": max(1.0, math.log2(float(size) + 1.0)) + 3.0,
        }

    for level in sorted({n["level"] for n in kept}):
        out_nodes[f"tier:{level}"] = {
            "id": f"tier:{level}",
            "label": level,
            "type": "tier",
            "color": TIER_COLORS.get(level, DEFAULT_NODE_COLOR),
            "val": 2.0,
        }

    out_edges: list[dict[str, Any]] = []
    for node in kept:
        cid = node["cluster"]
        if cid >= 0:
            out_edges.append({
                "source": node["id"],
                "target": f"community:{cid}",
                "type": "member_of",
                "weight": 1,
                "color": EDGE_COLORS["member_of"],
            })
        out_edges.append({
            "source": node["id"],
            "target": f"tier:{node['level']}",
            "type": "layered_as",
            "weight": 1,
            "color": EDGE_COLORS["layered_as"],
        })

    survivors = [
        e for e in valid_edges
        if e.get("source") in kept_ids and e.get("target") in kept_ids
    ]
    dropped += len(valid_edges) - len(survivors)
    survivors.sort(key=lambda e: (
        not _is_bridge(e),
        str(e.get("source", "")),
        str(e.get("target", "")),
        str(e.get("relation", "")),
    ))
    for edge in survivors[:max_edges]:
        relation = _opt_str(edge, "relation", "related-to")
        out_edges.append({
            "source": edge["source"],
            "target": edge["target"],
            "type": relation,
            "weight": 1,
            "color": EDGE_COLORS.get(relation, DEFAULT_EDGE_COLOR),
        })
    if len(survivors) > max_edges:
        truncated = True

    return {
        "nodes": list(out_nodes.values()),
        "edges": out_edges,
        "meta": {
            "node_count": len(kept),
            "edge_count": len(out_edges),
            "truncated": truncated,
            "dropped_edges": dropped,
        },
    }


def _md_safe(text: str, limit: int = CONTEXT_LABEL_CHARS) -> str:
    """Neutraliza un string remoto para embeberlo en markdown extractivo."""
    clean = text.replace("\r", " ").replace("`", "'").replace("```", "'''")
    clean = " ".join(clean.split())
    if len(clean) > limit:
        clean = clean[:limit] + "…"
    return clean


def _truncate_lines(markdown: str, budget: int) -> str:
    """Corte duro por linea completa + marcador (fences nunca se emiten)."""
    if len(markdown) <= budget:
        return markdown
    marker = "\n…truncated"
    room = budget - len(marker)
    cut = markdown.rfind("\n", 0, room)
    if cut <= 0:
        cut = room
    return markdown[:cut] + marker


def build_ai_context(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
    budget_chars: int = DEFAULT_BUDGET_CHARS,
) -> dict[str, Any]:
    """Contexto markdown extractivo con presupuesto para la IA local.

    Sin llamadas a LLM: entidades top por grado, puentes inter-cluster
    primero, una linea por comunidad. Determinista y acotado.
    """
    if budget_chars <= 0:
        raise ValueError("graph_force: budget_chars must be positive")
    budget = min(int(budget_chars), MAX_BUDGET_CHARS)

    clean: list[dict[str, Any]] = []
    for raw in nodes:
        if not isinstance(raw, dict):
            raise TypeError("graph_force: node is not a dict")
        nid = _req_str(raw, "id", "", "node")
        clean.append({
            "id": nid,
            "label": _req_str(raw, "label", nid, "node"),
            "kind": _opt_str(raw, "kind", _opt_str(raw, "type", "unknown")),
            "cluster": _opt_int(raw, "cluster", -1),
            "level": _opt_str(raw, "level", "data"),
        })
    node_ids = {n["id"] for n in clean}
    degree, valid = _degrees(node_ids, edges)

    if not clean:
        markdown = "# Estorides graph context\n\nempty graph: no entities.\n"
        return {
            "markdown": markdown,
            "approx_tokens": len(markdown) // 4,
            "entities": [],
            "relations": [],
            "reports": [],
        }

    top = sorted(clean, key=lambda n: (-degree[n["id"]], n["id"]))[:50]
    entities = [(n["id"], float(degree[n["id"]])) for n in top]

    bridges = sorted(
        [e for e in valid if _is_bridge(e)],
        key=lambda e: (str(e.get("source", "")), str(e.get("target", ""))),
    )
    rest = sorted(
        [e for e in valid if not _is_bridge(e)],
        key=lambda e: (str(e.get("source", "")), str(e.get("target", ""))),
    )
    rel_lines: list[str] = []
    for edge in (bridges + rest)[:100]:
        rel = _md_safe(_opt_str(edge, "relation", "related-to"), 40)
        rel_lines.append(
            f"- {edge['source']} --{rel}--> {edge['target']}"
        )

    members: dict[int, list[str]] = {}
    for node in clean:
        members.setdefault(node["cluster"], []).append(node["id"])
    reports: list[str] = []
    report_lines: list[str] = []
    for cid in sorted(members):
        ranked = sorted(members[cid], key=lambda i: (-degree[i], i))
        name = f"cluster {cid}" if cid >= 0 else "unassigned"
        for raw in clusters:
            if isinstance(raw, dict) and _opt_int(raw, "id", -999) == cid:
                name = _md_safe(_opt_str(raw, "label", name), 60)
                break
        reports.append(name)
        head = ", ".join(ranked[:5])
        report_lines.append(f"- {name}: {len(ranked)} members, top: {head}")

    lines = [
        "# Estorides graph context",
        "",
        f"{len(clean)} entities, {len(valid)} relationships, "
        f"{len(members)} communities. Provenance: fusion_store (/api/graph).",
        "",
        "## Entities",
    ]
    for node in top:
        label = _md_safe(node["label"])
        lines.append(
            f"- '{label}' [{node['kind']}] cluster={node['cluster']} "
            f"level={node['level']} degree={degree[node['id']]}"
        )
    lines += ["", "## Relationships", *(rel_lines or ["- none"])]
    lines += ["", "## Communities", *report_lines]
    lines += ["", "## Sources", "- fusion_store graph snapshot"]
    markdown = _truncate_lines("\n".join(lines) + "\n", budget)
    return {
        "markdown": markdown,
        "approx_tokens": len(markdown) // 4,
        "entities": entities,
        "relations": [
            f"{e['source']} --{_opt_str(e, 'relation', 'related-to')}-->"
            f" {e['target']}"
            for e in (bridges + rest)[:100]
        ],
        "reports": reports,
    }
