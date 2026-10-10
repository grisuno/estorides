"""graph_bundle: payload circle 2D + sphere 3D estilo ReadMenator.

Porta ``readmenator/_bundlegraph.py`` (``BundleGraphRenderer.build_payload``)
y ``readmenator/_graphlayout.py`` (``hierarchical_edge_bundling`` +
``spherical_edge_bundling`` + Fibonacci + B-spline, Holten 2006) al grafo
OSINT de Estorides.

Puro y sin I/O: consume el payload RAW de
``estorides_core.graph_force.build_force_payload`` y devuelve el payload
bundle ``{nodes, groups, edges}`` con la misma forma que ReadMenator (para
que el JS porteado sea casi verbatim). Todo input hostil se valida
fail-closed (``TypeError``) o se trunca a limites fijos. Nunca genera HTML.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from estorides_core.envutil import env_float, env_int
from estorides_core.graph_force import family_color_from_name

MAX_LABEL_CHARS = 512
COORD_DIGITS = 5
UNASSIGNED_KEY = "unassigned"
DEFAULT_UNASSIGNED_COLOR = "#4f8ef7"

SCAFFOLD_TYPES = frozenset({"member_of", "layered_as"})

Point = tuple[float, float]
Point3 = tuple[float, float, float]


@dataclass(frozen=True)
class BundleLayout:
    """Resultado del bundling circular (igual que ReadMenator)."""

    leaves: dict[str, Point]
    angles: dict[str, float]
    groups: list[tuple[str, float, float, int]]
    curves: list[tuple[str, str, list[tuple[float, ...]]]]
    center: Point
    radius: float


@dataclass(frozen=True)
class SphereBundleLayout:
    """Resultado del bundling esferico (igual que ReadMenator)."""

    leaves: dict[str, Point3]
    groups: list[tuple[str, Point3, int]]
    hubs: dict[str, Point3]
    curves: list[tuple[str, str, list[tuple[float, ...]]]]
    radius: float


def _req_str(item: dict[str, Any], key: str, default: str, what: str) -> str:
    value = item.get(key, default)
    if value is None:
        return default
    if isinstance(value, str):
        return value
    raise TypeError(f"graph_bundle: {what} field {key!r} is not a string")


def _opt_str(item: dict[str, Any], key: str, default: str) -> str:
    value = item.get(key, default)
    return value if isinstance(value, str) else default


def _opt_float(item: dict[str, Any], key: str, default: float) -> float:
    value = item.get(key, default)
    if isinstance(value, bool):
        return default
    try:
        out = float(value)
    except (TypeError, ValueError):
        return default
    return out if math.isfinite(out) else default


def _opt_int(item: dict[str, Any], key: str, default: int) -> int:
    value = item.get(key, default)
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _opt_community(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int) and value >= 0:
        return value
    return None


def _bspline(
    control: Sequence[tuple[float, ...]], samples: int
) -> list[tuple[float, ...]]:
    """Muestrea una B-spline cubica uniforme clamped (cualquier dimension)."""
    dims = range(len(control[0]))
    if len(control) < 3:
        a, b = control[0], control[-1]
        return [
            tuple(a[i] + (b[i] - a[i]) * k / samples for i in dims)
            for k in range(samples + 1)
        ]
    pts = [control[0], control[0], *control, control[-1], control[-1]]
    segments = len(pts) - 3
    out: list[tuple[float, ...]] = []
    per = max(2, samples // max(1, segments))
    for s in range(segments):
        p0, p1, p2, p3 = pts[s], pts[s + 1], pts[s + 2], pts[s + 3]
        extra = 1 if s == segments - 1 else 0
        for k in range(per + extra):
            t = k / per
            t2, t3 = t * t, t * t * t
            b0 = (1 - t) ** 3 / 6
            b1 = (3 * t3 - 6 * t2 + 4) / 6
            b2 = (-3 * t3 + 3 * t2 + 3 * t + 1) / 6
            b3 = t3 / 6
            out.append(
                tuple(
                    b0 * p0[i] + b1 * p1[i] + b2 * p2[i] + b3 * p3[i] for i in dims
                )
            )
    return out


def _bundle_curves(
    leaves: Mapping[str, tuple[float, ...]],
    member_group: dict[str, str],
    hub: Mapping[str, tuple[float, ...]],
    root: tuple[float, ...],
    edges: Sequence[tuple[str, str]],
    beta: float,
    samples: int,
) -> list[tuple[str, str, list[tuple[float, ...]]]]:
    """Rutea cada arista por la jerarquia y la muestrea como B-spline."""
    beta = max(0.0, min(1.0, beta))
    curves: list[tuple[str, str, list[tuple[float, ...]]]] = []
    for a, b in edges:
        if a not in leaves or b not in leaves or a == b:
            continue
        la, lb = leaves[a], leaves[b]
        dims = range(len(la))
        ga, gb = member_group[a], member_group[b]
        if ga == gb:
            mid = hub[ga]
            inner = tuple((mid[i] + la[i] + lb[i]) / 3 for i in dims)
            control = [la, inner, lb]
        else:
            control = [la, hub[ga], root, hub[gb], lb]
        m = len(control) - 1
        straightened = [
            tuple(
                beta * p[i] + (1 - beta) * (la[i] + j / m * (lb[i] - la[i]))
                for i in dims
            )
            for j, p in enumerate(control)
        ]
        curves.append((a, b, _bspline(straightened, samples)))
    return curves


def hierarchical_edge_bundling(
    groups: dict[str, list[str]],
    edges: Sequence[tuple[str, str]],
    center: Point,
    radius: float,
    beta: float = 0.85,
    samples: int = 24,
    group_gap: float = 0.04,
    inner_ratio: float = 0.55,
) -> BundleLayout:
    """Hojas en un circulo por grupo; aristas por la jerarquia (Holten 2006)."""
    cx, cy = center
    labels = [g for g in groups if groups[g]]
    total = sum(len(groups[g]) for g in labels)
    if total == 0:
        return BundleLayout({}, {}, [], [], center, radius)
    usable = 2 * math.pi - group_gap * len(labels)
    step = usable / total
    angle = -math.pi / 2
    leaves: dict[str, Point] = {}
    angles: dict[str, float] = {}
    arcs: list[tuple[str, float, float, int]] = []
    hub: dict[str, Point] = {}
    member_group: dict[str, str] = {}
    for label in labels:
        start = angle
        for nid in groups[label]:
            a = angle + step / 2
            leaves[nid] = (cx + radius * math.cos(a), cy + radius * math.sin(a))
            angles[nid] = a
            member_group[nid] = label
            angle += step
        end = angle
        mid = (start + end) / 2
        hub[label] = (
            cx + radius * inner_ratio * math.cos(mid),
            cy + radius * inner_ratio * math.sin(mid),
        )
        arcs.append((label, start, end, len(groups[label])))
        angle += group_gap
    curves = _bundle_curves(leaves, member_group, hub, (cx, cy), edges, beta, samples)
    return BundleLayout(leaves, angles, arcs, curves, center, radius)


def fibonacci_sphere(count: int) -> list[Point3]:
    """Vectores unitarios casi uniformes en espiral de angulo dorado."""
    if count <= 0:
        return []
    if count == 1:
        return [(0.0, -1.0, 0.0)]
    golden = math.pi * (3.0 - math.sqrt(5.0))
    out: list[Point3] = []
    for i in range(count):
        y = 1.0 - 2.0 * (i + 0.5) / count
        ring = math.sqrt(max(0.0, 1.0 - y * y))
        theta = golden * i
        out.append((ring * math.cos(theta), y, ring * math.sin(theta)))
    return out


def _unit(v: Sequence[float]) -> Point3:
    norm = math.sqrt(sum(c * c for c in v))
    if norm < 1e-12:
        return (0.0, -1.0, 0.0)
    return (v[0] / norm, v[1] / norm, v[2] / norm)


def _split_caps(
    labels: list[str],
    sizes: dict[str, int],
    points: list[int],
    lattice: list[Point3],
    out: dict[str, list[int]],
) -> None:
    """Biseca el lattice entre runs de grupos hasta un cap contiguo por grupo."""
    if len(labels) == 1:
        out[labels[0]] = points
        return
    total = sum(sizes[label] for label in labels)
    best, cut, running = total, 1, 0
    for i in range(1, len(labels)):
        running += sizes[labels[i - 1]]
        gap = abs(2 * running - total)
        if gap < best:
            best, cut = gap, i
    left_count = sum(sizes[label] for label in labels[:cut])
    spread = []
    for k in range(3):
        values = [lattice[pi][k] for pi in points]
        spread.append(max(values) - min(values))
    axis = max(range(3), key=lambda k: (spread[k], -k))
    ordered = sorted(points, key=lambda pi: (lattice[pi][axis], pi))
    _split_caps(labels[:cut], sizes, ordered[:left_count], lattice, out)
    _split_caps(labels[cut:], sizes, ordered[left_count:], lattice, out)


def spherical_edge_bundling(
    groups: dict[str, list[str]],
    edges: Sequence[tuple[str, str]],
    radius: float = 1.0,
    beta: float = 0.85,
    samples: int = 24,
    inner_ratio: float = 0.55,
) -> SphereBundleLayout:
    """Hojas en caps esfericos por comunidad; aristas por la jerarquia."""
    labels = [g for g in groups if groups[g]]
    total = sum(len(groups[g]) for g in labels)
    if total == 0:
        return SphereBundleLayout({}, [], {}, [], radius)
    lattice = fibonacci_sphere(total)
    regions: dict[str, list[int]] = {}
    _split_caps(
        labels,
        {label: len(groups[label]) for label in labels},
        list(range(total)),
        lattice,
        regions,
    )
    leaves: dict[str, Point3] = {}
    hubs: dict[str, Point3] = {}
    caps: list[tuple[str, Point3, int]] = []
    member_group: dict[str, str] = {}
    for label in labels:
        region = regions[label]
        center = _unit([sum(lattice[pi][k] for pi in region) for k in range(3)])
        points = sorted(
            region,
            key=lambda pi: (-sum(lattice[pi][k] * center[k] for k in range(3)), pi),
        )
        for nid, pi in zip(groups[label], points, strict=True):
            p = lattice[pi]
            leaves[nid] = (p[0] * radius, p[1] * radius, p[2] * radius)
            member_group[nid] = label
        hubs[label] = (
            center[0] * radius * inner_ratio,
            center[1] * radius * inner_ratio,
            center[2] * radius * inner_ratio,
        )
        caps.append((label, center, len(groups[label])))
    curves = _bundle_curves(
        leaves, member_group, hubs, (0.0, 0.0, 0.0), edges, beta, samples
    )
    return SphereBundleLayout(leaves, caps, hubs, curves, radius)


def _round2(pt: Point) -> list[float]:
    return [round(pt[0], COORD_DIGITS), round(pt[1], COORD_DIGITS)]


def _round3(pt: Point3) -> list[float]:
    return [round(pt[0], COORD_DIGITS), round(pt[1], COORD_DIGITS), round(pt[2], COORD_DIGITS)]


def bundle_settings() -> dict[str, Any]:
    """Defaults de la pagina bundle (fuente unica para el JS).

    Mismos valores que ``readmenator/_config.py`` BUNDLEGRAPH_*; cada uno
    se puede afinar por entorno sin romper el import (env malformada →
    default, nunca raise). Los colores viajan por nodo/grupo (campos
    ``c``), asi que no hay mapa separado.
    """
    return {
        "mode": "2d",
        "beta": env_float("ESTORIDES_BUNDLE_BETA", 0.85),
        "samples": env_int("ESTORIDES_BUNDLE_SAMPLES", 20),
        "innerRatio": env_float("ESTORIDES_BUNDLE_INNER_RATIO", 0.55),
        "groupGap": env_float("ESTORIDES_BUNDLE_GROUP_GAP", 0.04),
        "edgeAlpha": env_float("ESTORIDES_BUNDLE_EDGE_ALPHA", 0.30),
        "dimAlpha": env_float("ESTORIDES_BUNDLE_DIM_ALPHA", 0.035),
        "labelAllMax": env_int("ESTORIDES_BUNDLE_LABEL_ALL_MAX", 140),
        "labelTopN": env_int("ESTORIDES_BUNDLE_LABEL_TOP_N", 24),
        "labelMax": env_int("ESTORIDES_BUNDLE_LABEL_MAX_CHARS", 26),
        "nodeMin": env_float("ESTORIDES_BUNDLE_NODE_MIN_PX", 2.0),
        "nodeMax": env_float("ESTORIDES_BUNDLE_NODE_MAX_PX", 7.0),
        "hitPx": env_float("ESTORIDES_BUNDLE_HIT_PX", 9.0),
        "rotateSpeed": env_float("ESTORIDES_BUNDLE_ROTATE_SPEED", 0.12),
        "perspective": env_float("ESTORIDES_BUNDLE_PERSPECTIVE", 3.0),
        "depthFade": env_float("ESTORIDES_BUNDLE_DEPTH_FADE", 0.7),
        "particles": env_int("ESTORIDES_BUNDLE_PARTICLES", 3),
        "revealMs": env_int("ESTORIDES_BUNDLE_REVEAL_MS", 1400),
        "flowTopN": env_int("ESTORIDES_BUNDLE_FLOW_TOP_N", 8),
        "listMax": env_int("ESTORIDES_BUNDLE_LIST_MAX", 40),
        "searchResults": env_int("ESTORIDES_BUNDLE_SEARCH_RESULTS", 8),
        "groupColors": {},
        "unassignedKey": UNASSIGNED_KEY,
    }


def build_bundle_payload(force_payload: dict[str, Any]) -> dict[str, Any]:
    """Deriva el payload bundle desde un payload force RAW.

    Las comunidades conservan el orden del analizador (id asc) y los nodos
    sin comunidad forman el grupo trailing ``unassigned``. Dentro de cada
    grupo los nodos van por ``rank`` desc (hubs al centro del arco/cap).
    Solo viajan aristas entidad→entidad de relacion (el scaffolding
    ``member_of``/``layered_as`` se queda fuera: la jerarquia ya lo pinta).
    """
    if not isinstance(force_payload, dict):
        raise TypeError("graph_bundle: force_payload is not a dict")
    raw_nodes = force_payload.get("nodes", [])
    raw_edges = force_payload.get("edges", [])
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        raise TypeError("graph_bundle: force_payload nodes/edges are not lists")

    settings = bundle_settings()
    inner_ratio = float(settings["innerRatio"])
    group_gap = float(settings["groupGap"])

    entities: list[dict[str, Any]] = []
    for raw in raw_nodes:
        if not isinstance(raw, dict):
            raise TypeError("graph_bundle: node is not a dict")
        if raw.get("type") != "entity":
            continue
        nid = _req_str(raw, "id", "", "node")
        label = _req_str(raw, "label", nid, "node")[:MAX_LABEL_CHARS] or nid
        entities.append(
            {
                "id": nid,
                "label": label,
                "kind": _opt_str(raw, "kind", "unknown"),
                "layer": _opt_str(raw, "layer", "data"),
                "color": _opt_str(raw, "color", ""),
                "community": _opt_community(raw.get("community")),
                "community_label": _opt_str(raw, "community_label", ""),
                "family": _opt_str(raw, "family", ""),
                "rank": _opt_float(raw, "rank", 0.0),
                "rank_pos": _opt_int(raw, "rank_pos", 0),
                "findings": _opt_int(raw, "findings", 0),
                "doc": _opt_str(raw, "doc", ""),
            }
        )
    if not entities:
        return {"nodes": [], "groups": [], "edges": []}

    comm_color: dict[int, str] = {}
    for raw in raw_nodes:
        if not isinstance(raw, dict) or raw.get("type") != "community":
            continue
        raw_id = raw.get("id", "")
        if not isinstance(raw_id, str) or not raw_id.startswith("community:"):
            continue
        try:
            num = int(raw_id.split(":", 1)[1])
        except ValueError:
            continue
        color = _opt_str(raw, "color", "")
        if color:
            comm_color[num] = color

    group_key: dict[str, str] = {}
    group_label: dict[str, str] = {}
    order: list[tuple[float, str]] = []
    for ent in entities:
        cid = ent["community"]
        key = f"community:{cid}" if cid is not None else UNASSIGNED_KEY
        group_key[ent["id"]] = key
        if key not in group_label:
            if cid is not None:
                group_label[key] = ent["community_label"] or f"cluster {cid}"
                order.append((float(cid), key))
            else:
                group_label[key] = UNASSIGNED_KEY
                order.append((math.inf, key))
    keys = [key for _, key in sorted(order)]

    members: dict[str, list[str]] = {key: [] for key in keys}
    ranked = sorted(entities, key=lambda n: (-n["rank"], n["id"]))
    for ent in ranked:
        members[group_key[ent["id"]]].append(ent["id"])

    circle = hierarchical_edge_bundling(
        members, [], (0.0, 0.0), 1.0,
        group_gap=group_gap, inner_ratio=inner_ratio,
    )
    sphere = spherical_edge_bundling(members, [], 1.0, inner_ratio=inner_ratio)
    caps = {label: center for label, center, _count in sphere.groups}
    group_index = {key: i for i, key in enumerate(keys)}

    groups: list[dict[str, Any]] = []
    for label, start, end, count in circle.groups:
        mid = (start + end) / 2
        name = group_label[label]
        if label == UNASSIGNED_KEY:
            color = DEFAULT_UNASSIGNED_COLOR
        else:
            color = ""
            if label.startswith("community:"):
                try:
                    color = comm_color.get(int(label.split(":", 1)[1]), "")
                except ValueError:
                    color = ""
            if not color:
                color = family_color_from_name(name)
        groups.append(
            {
                "k": label,
                "l": name,
                "c": color,
                "n": count,
                "a0": round(start, COORD_DIGITS),
                "a1": round(end, COORD_DIGITS),
                "h2": _round2(
                    (inner_ratio * math.cos(mid), inner_ratio * math.sin(mid))
                ),
                "h3": _round3(sphere.hubs[label]),
                "u": _round3(caps[label]),
            }
        )

    ordered_ids = sorted(group_key.keys())
    index = {nid: i for i, nid in enumerate(ordered_ids)}
    by_id = {ent["id"]: ent for ent in entities}
    nodes: list[dict[str, Any]] = []
    for nid in ordered_ids:
        ent = by_id[nid]
        color = ent["color"] or family_color_from_name(ent["family"] or ent["kind"])
        nodes.append(
            {
                "id": nid,
                "f": ent["label"],
                "l": ent["label"],
                "g": group_index[group_key[nid]],
                "c": color,
                "ly": ent["layer"],
                "lg": ent["kind"],
                "r": ent["rank"],
                "rp": ent["rank_pos"],
                "fd": ent["findings"],
                "d": ent["doc"],
                "a": round(circle.angles[nid], COORD_DIGITS),
                "p": _round3(sphere.leaves[nid]),
            }
        )

    pairs = sorted(
        {
            (index[e["source"]], index[e["target"]])
            for e in raw_edges
            if isinstance(e, dict)
            and isinstance(e.get("source"), str)
            and isinstance(e.get("target"), str)
            and e.get("type") not in SCAFFOLD_TYPES
            and e["source"] in index
            and e["target"] in index
            and e["source"] != e["target"]
        }
    )
    return {"nodes": nodes, "groups": groups, "edges": [list(p) for p in pairs]}
