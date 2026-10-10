"""graph_bundle: pestana Bundles circular 2D + esferica 3D estilo ReadMenator.

Escenarios del contrato `spec/graph_bundle.md`:
S1 happy path (dos comunidades), S2 edge (vacio + unassigned),
S3 error (scaffolding/rotas fuera, no-dict falla cerrado),
S4 seguridad (truncado + JSON-safe), S5 determinismo + settings.
"""
from __future__ import annotations

import json
import math

import pytest

from estorides_core.graph_bundle import (
    build_bundle_payload,
    bundle_settings,
)

# Blindaje deliberado (precedente: graph_rag_search S7): este archivo no
# abre DBs; con `filterwarnings=error` el GC puede atribuirle conexiones
# sqlite sin cerrar dejadas por otros tests (victima aleatoria).
pytestmark = pytest.mark.filterwarnings("ignore::ResourceWarning")


def _force():
    return {
        "nodes": [
            {"id": "a", "label": "example.com", "type": "entity", "kind": "domain",
             "degree": 1, "findings": 0, "community": 0, "community_label": "c0",
             "family": "c0", "layer": "information", "color": "#5fb4ff",
             "rank": 0.5, "rank_pos": 2, "val": 1.0, "doc": "witness-a"},
            {"id": "b", "label": "1.2.3.4", "type": "entity", "kind": "ip",
             "degree": 2, "findings": 0, "community": 0, "community_label": "c0",
             "family": "c0", "layer": "data", "color": "#5fb4ff",
             "rank": 1.0, "rank_pos": 1, "val": 1.5, "doc": ""},
            {"id": "c", "label": "x@y.com", "type": "entity", "kind": "person",
             "degree": 1, "findings": 0, "community": 1, "community_label": "c1",
             "family": "c1", "layer": "intelligence", "color": "#ff9e64",
             "rank": 0.5, "rank_pos": 3, "val": 1.0, "doc": ""},
            {"id": "community:0", "label": "c0", "type": "community",
             "community_id": 0, "size": 2, "color": "#5fb4ff", "val": 4.0},
            {"id": "community:1", "label": "c1", "type": "community",
             "community_id": 1, "size": 1, "color": "#ff9e64", "val": 4.0},
        ],
        "edges": [
            {"source": "a", "target": "b", "type": "resolves-to", "weight": 1,
             "color": "rgba(79,239,142,.35)"},
            {"source": "b", "target": "c", "type": "related-to", "weight": 1,
             "color": "rgba(148,163,184,.45)"},
            {"source": "a", "target": "community:0", "type": "member_of",
             "weight": 1, "color": "rgba(255,255,255,.15)"},
            {"source": "a", "target": "tier:data", "type": "layered_as",
             "weight": 1, "color": "rgba(255,255,255,.15)"},
        ],
        "meta": {"node_count": 3, "edge_count": 4, "truncated": False,
                 "dropped_edges": 0},
    }


# S1 — happy path: dos comunidades #
def test_s1_two_communities_circle_and_sphere():
    """S1 — 3 entidades en 2 grupos, 2 aristas, angulos y esferas validos."""
    out = build_bundle_payload(_force())
    assert len(out["groups"]) == 2
    assert out["groups"][0]["k"] == "community:0" and out["groups"][0]["n"] == 2
    assert out["groups"][1]["k"] == "community:1" and out["groups"][1]["n"] == 1
    assert len(out["nodes"]) == 3
    by_id = {n["id"]: n for n in out["nodes"]}
    # Hub (rank 1.0) primero de su grupo: va primero en el arco.
    assert by_id["b"]["r"] == 1.0
    assert by_id["b"]["g"] == 0
    assert by_id["b"]["a"] < by_id["a"]["a"]
    for n in out["nodes"]:
        assert math.isfinite(n["a"])
        x, y, z = n["p"]
        assert abs(math.sqrt(x * x + y * y + z * z) - 1.0) < 2e-5
    assert out["edges"] == [[0, 1], [1, 2]]
    json.dumps(out)


# S2 — edge: vacio y sin comunidad #
def test_s2_empty_and_unassigned():
    """S2 — vacio sin raise; sin comunidad forma grupo trailing."""
    empty = build_bundle_payload({"nodes": [], "edges": []})
    assert empty == {"nodes": [], "groups": [], "edges": []}
    force = {
        "nodes": [
            {"id": "x", "label": "x", "type": "entity", "kind": "domain",
             "community": None, "rank": 0.0, "rank_pos": 1, "color": "#888",
             "layer": "data", "findings": 0, "doc": ""},
            {"id": "y", "label": "y", "type": "entity", "kind": "ip",
             "community": None, "rank": 0.0, "rank_pos": 2, "color": "#888",
             "layer": "data", "findings": 0, "doc": ""},
        ],
        "edges": [],
    }
    out = build_bundle_payload(force)
    assert len(out["groups"]) == 1 and out["groups"][0]["k"] == "unassigned"
    assert out["groups"][0]["n"] == 2


# S3 — error: scaffolding fuera, input roto falla cerrado #
def test_s3_scaffolding_dropped_and_bad_node_raises():
    """S3 — member_of/layered_as/huerfanas/self-loop fuera; no-dict TypeError."""
    force = _force()
    force["edges"] = force["edges"] + [
        {"source": "a", "target": "ghost", "type": "related-to", "weight": 1},
        {"source": "a", "target": "a", "type": "related-to", "weight": 1},
    ]
    out = build_bundle_payload(force)
    assert out["edges"] == [[0, 1], [1, 2]]
    bad = {"nodes": [{"id": "x", "label": {"evil", "set"}, "type": "entity"}],
           "edges": []}
    try:
        build_bundle_payload(bad)
        raised = False
    except TypeError:
        raised = True
    assert raised


# S4 — seguridad: truncado y JSON-safe #
def test_s4_hostile_labels_truncated_and_bytes_raise():
    """S4 — label 5KB truncado a <=512; bytes hace TypeError; dumps OK."""
    evil = "# h\n```\n[x](javascript:alert(1))\n" + "A" * 5000
    force = {
        "nodes": [{"id": "e", "label": evil, "type": "entity", "kind": "domain",
                   "community": 0, "community_label": "c0", "rank": 1.0,
                   "rank_pos": 1, "color": "#fff", "layer": "data",
                   "findings": 0, "doc": ""}],
        "edges": [],
    }
    out = build_bundle_payload(force)
    assert len(out["nodes"][0]["l"]) <= 512
    assert len(out["nodes"][0]["f"]) <= 512
    json.dumps(out)
    bad = {"nodes": [{"id": "e", "label": b"bytes", "type": "entity"}],
           "edges": []}
    try:
        build_bundle_payload(bad)
        raised = False
    except TypeError:
        raised = True
    assert raised


# S5 — determinismo + settings #
def test_s5_deterministic_and_settings_match_readmenator():
    """S5 — dos pasadas identicas; p/u unitarios; settings con defaults."""
    first = build_bundle_payload(_force())
    second = build_bundle_payload(_force())
    assert first == second
    for n in first["nodes"]:
        x, y, z = n["p"]
        assert abs(math.sqrt(x * x + y * y + z * z) - 1.0) < 2e-5
    for g in first["groups"]:
        x, y, z = g["u"]
        assert abs(math.sqrt(x * x + y * y + z * z) - 1.0) < 2e-5
    s = bundle_settings()
    assert s["beta"] == 0.85
    assert s["samples"] == 20
    assert s["innerRatio"] == 0.55
    assert s["mode"] == "2d"
    assert s["unassignedKey"] == "unassigned"


# S7 — layout directo: curvas, beta, esferas, fibonacci                    #
def test_s7_circle_curves_endpoints_and_beta():
    """S7 — curvas con extremos cerca de las hojas; beta=0 pega al acorde."""
    from estorides_core.graph_bundle import hierarchical_edge_bundling

    groups = {"g1": ["a", "b"], "g2": ["c"]}
    edges = [("a", "b"), ("a", "c"), ("a", "a"), ("ghost", "a")]
    full = hierarchical_edge_bundling(groups, edges, (0.0, 0.0), 1.0, beta=1.0)
    assert len(full.curves) == 2
    (sa, ta, pa), (sb, tb, pb) = full.curves
    assert (sa, ta) == ("a", "b") and (sb, tb) == ("a", "c")
    assert len(pa) == len(pb) == 2 * 12 + 1
    for (src, tgt, pts) in full.curves:
        first = (pts[0][0], pts[0][1])
        last = (pts[-1][0], pts[-1][1])
        assert math.dist(first, full.leaves[src]) < 0.25
        assert math.dist(last, full.leaves[tgt]) < 0.25
    straight = hierarchical_edge_bundling(groups, edges, (0.0, 0.0), 1.0, beta=0.0)
    for (src, tgt, pts) in straight.curves:
        la, lb = straight.leaves[src], straight.leaves[tgt]
        seg = math.dist(la, lb) or 1.0
        for k in range(0, len(pts), 2):
            px, py = pts[k][0], pts[k][1]
            t = ((px - la[0]) * (lb[0] - la[0]) + (py - la[1]) * (lb[1] - la[1])) / (seg * seg)
            proj = (la[0] + t * (lb[0] - la[0]), la[1] + t * (lb[1] - la[1]))
            assert math.dist((px, py), proj) < 1e-9
    bundled = hierarchical_edge_bundling(groups, [("a", "c")], (0.0, 0.0), 1.0, beta=1.0)
    la, lb = bundled.leaves["a"], bundled.leaves["c"]
    seg = math.dist(la, lb) or 1.0
    assert max(
        abs((p[0] - la[0]) * (lb[1] - la[1]) - (p[1] - la[1]) * (lb[0] - la[0])) / seg
        for p in bundled.curves[0][2]
    ) > 0.05
    empty = hierarchical_edge_bundling({"g": []}, [], (0.0, 0.0), 1.0)
    assert empty.leaves == {} and empty.curves == []


def test_s7_sphere_caps_hubs_and_fibonacci():
    """S7 — caps exactos, hubs dentro, hojas unitarias, fibonacci borde."""
    from estorides_core.graph_bundle import fibonacci_sphere, spherical_edge_bundling

    assert fibonacci_sphere(0) == []
    assert fibonacci_sphere(1) == [(0.0, -1.0, 0.0)]
    for pt in fibonacci_sphere(7):
        assert abs(math.sqrt(sum(c * c for c in pt)) - 1.0) < 1e-12
    groups = {"g1": ["a", "b", "c"], "g2": ["d"]}
    lay = spherical_edge_bundling(groups, [("a", "d"), ("b", "b")], 1.0)
    assert len(lay.leaves) == 4
    assert [c for _, _, c in lay.groups] == [3, 1]
    assert len(lay.curves) == 1
    for _label, center, _n in lay.groups:
        assert abs(math.sqrt(sum(c * c for c in center)) - 1.0) < 1e-9
    for _label, hub in lay.hubs.items():
        assert abs(math.sqrt(sum(c * c for c in hub)) - 0.55) < 1e-9
    for _nid, leaf in lay.leaves.items():
        assert abs(math.sqrt(sum(c * c for c in leaf)) - 1.0) < 1e-9
    empty = spherical_edge_bundling({"g": []}, [], 1.0)
    assert empty.leaves == {} and empty.groups == [] and empty.curves == []


def test_s7_helpers_unit():
    """S7 — _unit(0)=polo, _round digitos, _opt/_req ramas."""
    from estorides_core import graph_bundle as gb

    assert gb._unit([0.0, 0.0, 0.0]) == (0.0, -1.0, 0.0)
    assert gb._unit([0.0, 2.0, 0.0]) == (0.0, 1.0, 0.0)
    assert gb._round2((0.123456789, -0.987654321)) == [0.12346, -0.98765]
    assert gb._round3((0.1, 0.2, 0.3)) == [0.1, 0.2, 0.3]
    assert gb._req_str({"id": None}, "id", "dflt", "node") == "dflt"
    assert gb._opt_str({"c": 7}, "c", "dflt") == "dflt"
    assert gb._opt_str({"c": "x"}, "c", "dflt") == "x"
    assert gb._opt_float({"r": True}, "r", 0.5) == 0.5
    assert gb._opt_float({"r": float("nan")}, "r", 0.5) == 0.5
    assert gb._opt_float({"r": "xx"}, "r", 0.5) == 0.5
    assert gb._opt_float({"r": 2}, "r", 0.5) == 2.0
    assert gb._opt_int({"n": True}, "n", 3) == 3
    assert gb._opt_int({"n": "xx"}, "n", 3) == 3
    assert gb._opt_int({"n": "4"}, "n", 3) == 4
    assert gb._opt_community(True) is None
    assert gb._opt_community(-1) is None
    assert gb._opt_community("0") is None
    assert gb._opt_community(2) == 2


# S8 — settings completos + env, y salida exacta del payload              #
def test_s8_settings_full_defaults_and_env(monkeypatch):
    """S8 — dict exacto con env limpio; override y malformado no tumban."""
    for var in (
        "ESTORIDES_BUNDLE_BETA", "ESTORIDES_BUNDLE_SAMPLES",
        "ESTORIDES_BUNDLE_INNER_RATIO", "ESTORIDES_BUNDLE_GROUP_GAP",
        "ESTORIDES_BUNDLE_EDGE_ALPHA", "ESTORIDES_BUNDLE_DIM_ALPHA",
        "ESTORIDES_BUNDLE_LABEL_ALL_MAX", "ESTORIDES_BUNDLE_LABEL_TOP_N",
        "ESTORIDES_BUNDLE_LABEL_MAX_CHARS", "ESTORIDES_BUNDLE_NODE_MIN_PX",
        "ESTORIDES_BUNDLE_NODE_MAX_PX", "ESTORIDES_BUNDLE_HIT_PX",
        "ESTORIDES_BUNDLE_ROTATE_SPEED", "ESTORIDES_BUNDLE_PERSPECTIVE",
        "ESTORIDES_BUNDLE_DEPTH_FADE", "ESTORIDES_BUNDLE_PARTICLES",
        "ESTORIDES_BUNDLE_REVEAL_MS", "ESTORIDES_BUNDLE_FLOW_TOP_N",
        "ESTORIDES_BUNDLE_LIST_MAX", "ESTORIDES_BUNDLE_SEARCH_RESULTS",
    ):
        monkeypatch.delenv(var, raising=False)
    assert bundle_settings() == {
        "mode": "2d", "beta": 0.85, "samples": 20,
        "innerRatio": 0.55, "groupGap": 0.04,
        "edgeAlpha": 0.3, "dimAlpha": 0.035,
        "labelAllMax": 140, "labelTopN": 24, "labelMax": 26,
        "nodeMin": 2.0, "nodeMax": 7.0, "hitPx": 9.0,
        "rotateSpeed": 0.12, "perspective": 3.0, "depthFade": 0.7,
        "particles": 3, "revealMs": 1400, "flowTopN": 8, "listMax": 40,
        "searchResults": 8, "groupColors": {}, "unassignedKey": "unassigned",
    }
    monkeypatch.setenv("ESTORIDES_BUNDLE_BETA", "0.5")
    monkeypatch.setenv("ESTORIDES_BUNDLE_SAMPLES", "7")
    assert bundle_settings()["beta"] == 0.5
    assert bundle_settings()["samples"] == 7
    monkeypatch.setenv("ESTORIDES_BUNDLE_BETA", "not-a-float")
    monkeypatch.setenv("ESTORIDES_BUNDLE_SAMPLES", "not-an-int")
    assert bundle_settings()["beta"] == 0.85
    assert bundle_settings()["samples"] == 20


def test_s8_exact_payload_shape():
    """S8 — grupos/nodos/edges byte-exactos sobre el fixture S1."""
    out = build_bundle_payload(_force())
    assert [g["k"] for g in out["groups"]] == ["community:0", "community:1"]
    assert [g["n"] for g in out["groups"]] == [2, 1]
    assert [g["l"] for g in out["groups"]] == ["c0", "c1"]
    assert [g["c"] for g in out["groups"]] == ["#5fb4ff", "#ff9e64"]
    assert [(n["id"], n["g"]) for n in out["nodes"]] == [("a", 0), ("b", 0), ("c", 1)]
    assert [(n["ly"], n["lg"]) for n in out["nodes"]] == [
        ("information", "domain"), ("data", "ip"), ("intelligence", "person")]
    assert [(n["r"], n["rp"], n["fd"]) for n in out["nodes"]] == [
        (0.5, 2, 0), (1.0, 1, 0), (0.5, 3, 0)]
    assert [n["c"] for n in out["nodes"]] == ["#5fb4ff", "#5fb4ff", "#ff9e64"]
    assert [n["d"] for n in out["nodes"]] == ["witness-a", "", ""]
    assert out["edges"] == [[0, 1], [1, 2]]
    assert out["nodes"][0]["a"] == 1.5308
    assert out["groups"][0]["a0"] == -1.5708
    assert out["groups"][0]["h2"] == [0.48348, 0.2622]


def test_s8_lenient_fields_and_ignored_nodes():
    """S8 — None/no-str van a defaults; tiers y communities raras fuera."""
    force = {
        "nodes": [
            {"id": "community:x", "label": "bad", "type": "community", "color": "#fff"},
            {"id": "tier:data", "label": "data", "type": "tier", "color": "#000"},
            {"id": "e", "label": None, "type": "entity", "kind": None,
             "community": True, "rank": True, "rank_pos": "x",
             "color": 7, "layer": None, "findings": "x", "doc": None},
        ],
        "edges": [
            {"source": "e", "target": "e", "type": "related-to"},
            "not-a-dict",
            {"source": 7, "target": "e", "type": "related-to"},
            {"source": "e", "target": "missing", "type": "related-to"},
        ],
    }
    out = build_bundle_payload(force)
    assert len(out["nodes"]) == 1
    node = out["nodes"][0]
    assert node["l"] == "e" and node["f"] == "e"
    assert node["lg"] == "unknown" and node["ly"] == "data"
    assert node["r"] == 0.0 and node["rp"] == 0 and node["fd"] == 0
    assert node["d"] == "" and node["g"] == 0
    assert out["groups"][0]["k"] == "unassigned"
    assert out["groups"][0]["c"] == "#4f8ef7"
    assert out["edges"] == []
    for bad in ({"nodes": "x", "edges": []}, {"nodes": [], "edges": {}}, [1, 2]):
        try:
            build_bundle_payload(bad)  # type: ignore[arg-type]
            raised = False
        except TypeError:
            raised = True
        assert raised
    try:
        build_bundle_payload({"nodes": [{"id": "x", "type": "entity", "label": "ok", "no": 1}, 7], "edges": []})
        raised = False
    except TypeError:
        raised = True
    assert raised


# S9 — caza-mutantes: mensajes, defaults ausentes, env total, checksums   #
def test_s9_typeerror_messages_asserted():
    """S9 — los TypeError llevan el mensaje exacto (mata mutantes de texto)."""
    for payload, exact in (
        ("nope", "graph_bundle: force_payload is not a dict"),
        ({"nodes": "x", "edges": []},
         "graph_bundle: force_payload nodes/edges are not lists"),
        ({"nodes": [], "edges": {}},
         "graph_bundle: force_payload nodes/edges are not lists"),
        ({"nodes": [{"id": 7, "type": "entity"}], "edges": []},
         "graph_bundle: node field 'id' is not a string"),
        ({"nodes": [{"id": "x", "label": {"s"}, "type": "entity"}], "edges": []},
         "graph_bundle: node field 'label' is not a string"),
        ({"nodes": [{"id": "x", "type": "entity"}, 7], "edges": []},
         "graph_bundle: node is not a dict"),
    ):
        try:
            build_bundle_payload(payload)  # type: ignore[arg-type]
            raised = ""
        except TypeError as exc:
            raised = str(exc)
        assert raised == exact, f"{payload!r} debe fallar con {exact!r}"


def test_s9_bare_entity_defaults_and_idless():
    """S9 — entidad pelada usa todos los defaults; sin id el id es ''."""
    from estorides_core.graph_force import family_color_from_name

    out = build_bundle_payload({"nodes": [{"id": "bare", "type": "entity"}], "edges": []})
    (node,) = out["nodes"]
    assert node["l"] == "bare" and node["f"] == "bare"
    assert node["lg"] == "unknown" and node["ly"] == "data"
    assert node["c"] == family_color_from_name("unknown")
    assert node["r"] == 0.0 and node["rp"] == 0 and node["fd"] == 0
    assert node["d"] == "" and node["g"] == 0
    assert out["groups"][0]["k"] == "unassigned"
    out2 = build_bundle_payload({"nodes": [{"type": "entity"}], "edges": []})
    assert out2["nodes"][0]["id"] == ""
    assert out2["nodes"][0]["l"] == ""
    out3 = build_bundle_payload({"nodes": []})
    assert out3 == {"nodes": [], "groups": [], "edges": []}
    out3b = build_bundle_payload({"edges": []})
    assert out3b == {"nodes": [], "groups": [], "edges": []}
    out4 = build_bundle_payload({"nodes": [], "edges": [], "extra": 1})
    assert out4 == {"nodes": [], "groups": [], "edges": []}


def test_s9_family_fallback_color_and_order():
    """S9 — sin color manda family; comunidad alta antes que unassigned."""
    out = build_bundle_payload({
        "nodes": [
            {"id": "u", "label": "u", "type": "entity", "kind": "domain",
             "family": "myfam", "rank": 1.0, "rank_pos": 1},
            {"id": "v", "label": "v", "type": "entity", "kind": "ip",
             "community": 5, "community_label": "five", "rank": 0.0, "rank_pos": 2},
        ],
        "edges": [{"source": "u", "target": "v", "type": "related-to"}],
    })
    from estorides_core.graph_force import family_color_from_name

    by_id = {n["id"]: n for n in out["nodes"]}
    assert by_id["u"]["c"] == family_color_from_name("myfam")
    assert by_id["v"]["c"] == family_color_from_name("ip")
    assert [g["k"] for g in out["groups"]] == ["community:5", "unassigned"]
    assert [g["l"] for g in out["groups"]] == ["five", "unassigned"]
    assert out["edges"] == [[0, 1]]


def test_s9_unit_edge_norms():
    """S9 — _unit en normas limite (mata <= frente a <)."""
    from estorides_core import graph_bundle as gb

    assert gb._unit([0.5, 0.0, 0.0]) == (1.0, 0.0, 0.0)
    assert gb._unit([1e-12, 0.0, 0.0]) == (1.0, 0.0, 0.0)
    assert gb._unit([0.0, 0.0, 0.0]) == (0.0, -1.0, 0.0)


def test_s9_fibonacci_exact():
    """S9 — lattice exacto (angulo dorado y reparto vertical pineados)."""
    from estorides_core.graph_bundle import fibonacci_sphere

    assert fibonacci_sphere(0) == []
    assert fibonacci_sphere(1) == [(0.0, -1.0, 0.0)]
    two = fibonacci_sphere(2)
    assert two[0] == (0.8660254037844386, 0.5, 0.0)
    assert two[1][0] == math.cos(2.399963229728653) * math.sqrt(0.75)
    seven = fibonacci_sphere(7)
    assert [round(p[1], 12) for p in seven] == [
        round(1.0 - 2.0 * (i + 0.5) / 7, 12) for i in range(7)]
    assert seven[0][2] == 0.0
    assert seven[1][0] != seven[2][0]


def test_s9_sphere_caps_exact_and_defaults():
    """S9 — caps exactos; llamada sin radius usa 1.0."""
    from estorides_core.graph_bundle import spherical_edge_bundling

    lay = spherical_edge_bundling({"g1": ["a", "b", "c"], "g2": ["d"]}, [("a", "d")])
    assert [c for _, _, c in lay.groups] == [3, 1]
    assert lay.groups[0][1][0] == lay.hubs["g1"][0] / 0.55
    assert abs(lay.groups[0][1][0] - 0.9152034835137118) < 1e-9
    assert abs(lay.hubs["g2"][1] - 0.1375) < 1e-9
    assert lay.radius == 1.0
    for leaf in lay.leaves.values():
        assert abs(math.sqrt(sum(c * c for c in leaf)) - 1.0) < 1e-12


def test_s9_default_layout_checksum_and_length():
    """S9 — checksum de curva con defaults (beta/samples/inner_ratio pineados)."""
    from estorides_core.graph_bundle import (
        hierarchical_edge_bundling,
        spherical_edge_bundling,
    )

    h = hierarchical_edge_bundling({"g": ["a", "b"]}, [("a", "b")], (0.0, 0.0), 1.0)
    pts = h.curves[0][2]
    assert len(pts) == 25
    assert round(sum(c for p in pts for c in p), 6) == 1.191121
    s = spherical_edge_bundling({"g1": ["a", "b", "c"], "g2": ["d"]}, [("a", "d")])
    pts = s.curves[0][2]
    assert len(pts) == 25
    assert round(sum(c for p in pts for c in p), 6) == -5.915253


def test_s9_all_env_vars_propagate(monkeypatch):
    """S9 — cada ESTORIDES_BUNDLE_* llega a su clave (nombres pineados)."""
    pairs = {
        "ESTORIDES_BUNDLE_BETA": ("beta", "0.11"),
        "ESTORIDES_BUNDLE_SAMPLES": ("samples", "9"),
        "ESTORIDES_BUNDLE_INNER_RATIO": ("innerRatio", "0.11"),
        "ESTORIDES_BUNDLE_GROUP_GAP": ("groupGap", "0.11"),
        "ESTORIDES_BUNDLE_EDGE_ALPHA": ("edgeAlpha", "0.11"),
        "ESTORIDES_BUNDLE_DIM_ALPHA": ("dimAlpha", "0.11"),
        "ESTORIDES_BUNDLE_LABEL_ALL_MAX": ("labelAllMax", "11"),
        "ESTORIDES_BUNDLE_LABEL_TOP_N": ("labelTopN", "11"),
        "ESTORIDES_BUNDLE_LABEL_MAX_CHARS": ("labelMax", "11"),
        "ESTORIDES_BUNDLE_NODE_MIN_PX": ("nodeMin", "1.5"),
        "ESTORIDES_BUNDLE_NODE_MAX_PX": ("nodeMax", "9.5"),
        "ESTORIDES_BUNDLE_HIT_PX": ("hitPx", "11.5"),
        "ESTORIDES_BUNDLE_ROTATE_SPEED": ("rotateSpeed", "1.5"),
        "ESTORIDES_BUNDLE_PERSPECTIVE": ("perspective", "4.5"),
        "ESTORIDES_BUNDLE_DEPTH_FADE": ("depthFade", "0.11"),
        "ESTORIDES_BUNDLE_PARTICLES": ("particles", "9"),
        "ESTORIDES_BUNDLE_REVEAL_MS": ("revealMs", "911"),
        "ESTORIDES_BUNDLE_FLOW_TOP_N": ("flowTopN", "9"),
        "ESTORIDES_BUNDLE_LIST_MAX": ("listMax", "9"),
        "ESTORIDES_BUNDLE_SEARCH_RESULTS": ("searchResults", "9"),
    }
    for var, (_, val) in pairs.items():
        monkeypatch.setenv(var, val)
    got = bundle_settings()
    for var, (key, val) in pairs.items():
        assert got[key] == float(val) if isinstance(got[key], float) else got[key] == int(val), var



# S10 — remate mutacion: literales, defaults con env, layout absoluto     #
def test_s10_full_literal_output():
    """S10 — payload S1 byte-exacto (cada clave/valor pineado)."""
    out = build_bundle_payload(_force())
    assert out == {
        "nodes": [
            {"id": "a", "f": "example.com", "l": "example.com", "g": 0,
             "c": "#5fb4ff", "ly": "information", "lg": "domain",
             "r": 0.5, "rp": 2, "fd": 0, "d": "witness-a",
             "a": 1.5308, "p": [0.06516, -0.66667, -0.7425]},
            {"id": "b", "f": "1.2.3.4", "l": "1.2.3.4", "g": 0,
             "c": "#5fb4ff", "ly": "data", "lg": "ip",
             "r": 1.0, "rp": 1, "fd": 0, "d": "",
             "a": -0.53693, "p": [-0.73737, 0.0, 0.67549]},
            {"id": "c", "f": "x@y.com", "l": "x@y.com", "g": 1,
             "c": "#ff9e64", "ly": "intelligence", "lg": "person",
             "r": 0.5, "rp": 3, "fd": 0, "d": "",
             "a": 3.63852, "p": [0.74536, 0.66667, 0.0]},
        ],
        "groups": [
            {"k": "community:0", "l": "c0", "c": "#5fb4ff", "n": 2,
             "a0": -1.5708, "a1": 2.56466,
             "h2": [0.48348, 0.2622], "h3": [-0.38954, -0.38633, -0.03883],
             "u": [-0.70825, -0.70242, -0.07061]},
            {"k": "community:1", "l": "c1", "c": "#ff9e64", "n": 1,
             "a0": 2.60466, "a1": 4.67239,
             "h2": [-0.48348, -0.2622], "h3": [0.40995, 0.36667, 0.0],
             "u": [0.74536, 0.66667, 0.0]},
        ],
        "edges": [[0, 1], [1, 2]],
    }


def test_s10_empty_label_falls_back_to_id_and_findings():
    """S10 — label '' usa el id; findings no-cero viaja."""
    out = build_bundle_payload({
        "nodes": [
            {"id": "x", "label": "", "type": "entity", "findings": 3,
             "rank_pos": 4, "rank": 2.5},
        ],
        "edges": [],
    })
    (node,) = out["nodes"]
    assert node["l"] == "x" and node["f"] == "x"
    assert node["fd"] == 3 and node["rp"] == 4 and node["r"] == 2.5


def test_s10_odd_community_ids():
    """S10 — 'community:9:9' se descarta; sin label el grupo es 'cluster N'."""
    from estorides_core.graph_force import family_color_from_name

    out = build_bundle_payload({
        "nodes": [
            {"id": "community:9:9", "type": "community", "color": "#123456",
             "label": "trap"},
            {"id": "community:6", "type": "community", "label": "six"},
            {"id": "e3", "type": "entity", "community": 3, "rank": 1.0,
             "rank_pos": 1},
            {"id": "e9", "type": "entity", "community": 9, "rank": 0.5,
             "rank_pos": 2},
            {"id": "e6", "type": "entity", "community": 6, "rank": 0.0,
             "rank_pos": 3},
        ],
        "edges": [],
    })
    by_k = {g["k"]: g for g in out["groups"]}
    assert by_k["community:9"]["l"] == "cluster 9"
    assert by_k["community:9"]["c"] == family_color_from_name("cluster 9")
    assert by_k["community:3"]["l"] == "cluster 3"
    assert by_k["community:6"]["c"] == family_color_from_name("cluster 6")
    assert by_k["community:6"]["l"] == "cluster 6"
    assert by_k["community:3"]["l"] == "cluster 3"


def test_s10_scaffold_between_entities_dropped():
    """S10 — member_of entre entidades se filtra por tipo, no por extremos."""
    out = build_bundle_payload({
        "nodes": [
            {"id": "a", "type": "entity", "community": 0, "rank": 1.0,
             "rank_pos": 1},
            {"id": "b", "type": "entity", "community": 0, "rank": 0.5,
             "rank_pos": 2},
        ],
        "edges": [
            {"source": "b", "target": "a", "type": "member_of"},
            {"source": "b", "target": "a", "type": "layered_as"},
            {"source": "a", "target": "b", "type": "related-to"},
            {"source": "a", "target": "b", "type": "related-to"},
        ],
    })
    assert out["edges"] == [[0, 1]]


def test_s10_community_colors_survive_bad_id():
    """S10 — un id malo no aborta el resto (continue, no break)."""
    out = build_bundle_payload({
        "nodes": [
            {"id": "oops", "type": "community", "color": "#000000",
             "label": "trap"},
            {"id": "e7", "type": "entity", "community": 7, "rank": 1.0,
             "rank_pos": 1},
            {"id": "community:7", "type": "community", "color": "#abcdef",
             "label": "seven"},
            {"id": "community:x", "type": "community", "color": "#999999",
             "label": "bad"},
            {"id": "community:8", "type": "community", "color": "#123456",
             "label": "eight"},
            {"id": "e8", "type": "entity", "community": 8, "rank": 0.5,
             "rank_pos": 2},
        ],
        "edges": [],
    })
    by_k = {g["k"]: g for g in out["groups"]}
    assert by_k["community:7"]["c"] == "#abcdef"
    assert by_k["community:8"]["c"] == "#123456"


def test_s10_env_divergence_changes_layout(monkeypatch):
    """S10 — GROUP_GAP/INNER_RATIO del env mandan (kwargs no opcionales)."""
    monkeypatch.setenv("ESTORIDES_BUNDLE_GROUP_GAP", "0.9")
    monkeypatch.setenv("ESTORIDES_BUNDLE_INNER_RATIO", "0.9")
    out = build_bundle_payload(_force())
    assert out["groups"][0]["a1"] != 2.56466
    for group in out["groups"]:
        x, y = group["h2"]
        assert abs(math.sqrt(x * x + y * y) - 0.9) < 2e-5
        x, y, z = group["h3"]
        assert abs(math.sqrt(x * x + y * y + z * z) - 0.9) < 1e-4


def test_s10_bspline_short_branch_exact():
    """S10 — rama <3 puntos: interpolacion lineal exacta + longitudes."""
    from estorides_core.graph_bundle import _bspline

    assert _bspline([(0.0, 0.0), (4.0, 0.0)], 4) == [
        (0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (3.0, 0.0), (4.0, 0.0)]
    assert _bspline([(1.0, 2.0, 3.0), (5.0, 6.0, 7.0)], 2) == [
        (1.0, 2.0, 3.0), (3.0, 4.0, 5.0), (5.0, 6.0, 7.0)]
    assert len(_bspline([(0.0, 0.0), (1.0, 1.0)], 5)) == 6
    assert len(_bspline([(0.0, 0.0), (1.0, 1.0)], 6)) == 7
    four = [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (3.0, 1.0)]
    assert len(_bspline(four, 5)) == 11
    assert len(_bspline(four, 15)) == 16


def test_s10_beta_clamp_and_skip_order():
    """S10 — beta>1 se clamp a 1; arista mala primera no aborta."""
    from estorides_core.graph_bundle import _bundle_curves, hierarchical_edge_bundling

    groups = {"g": ["a", "b"]}
    one = hierarchical_edge_bundling(groups, [("a", "b")], (0.0, 0.0), 1.0, beta=1.0)
    two = hierarchical_edge_bundling(groups, [("a", "b")], (0.0, 0.0), 1.0, beta=2.0)
    assert one.curves[0][2] == two.curves[0][2]
    leaves = {"a": (0.0, 0.0), "b": (1.0, 0.0)}
    member = {"a": "g", "b": "g"}
    hub = {"g": (0.5, 0.5)}
    curves = _bundle_curves(leaves, member, hub, (0.0, 0.0),
                            [("ghost", "a"), ("a", "a"), ("a", "b")],
                            0.5, 8)
    assert [(s, t) for s, t, _ in curves] == [("a", "b")]


def test_s10_empty_layouts_full_and_absolute_leaves():
    """S10 — layouts vacios exactos; hojas absolutas (centro/radio pineados)."""
    from estorides_core.graph_bundle import (
        BundleLayout,
        SphereBundleLayout,
        hierarchical_edge_bundling,
        spherical_edge_bundling,
    )

    assert hierarchical_edge_bundling({"g": []}, [], (0.0, 0.0), 1.0) == BundleLayout(
        {}, {}, [], [], (0.0, 0.0), 1.0)
    assert spherical_edge_bundling({"g": []}, [], 1.0) == SphereBundleLayout(
        {}, [], {}, [], 1.0)
    h = hierarchical_edge_bundling({"g1": ["a", "b"], "g2": ["c"]}, [], (0.0, 0.0), 1.0)
    assert h.center == (0.0, 0.0) and h.radius == 1.0
    assert h.leaves["a"] == (0.8592819557514266, -0.5115022194673287)
    assert h.leaves["c"] == (-0.8790492550301631, -0.4767309589599938)
    s = spherical_edge_bundling({"g1": ["a", "b", "c"], "g2": ["d"]}, [], 2.0)
    assert s.radius == 2.0
    assert s.leaves["a"] == (0.16929918792944987, -0.5, -1.9290769256217932)
    for hub in s.hubs.values():
        assert abs(math.sqrt(sum(c * c for c in hub)) - 1.1) < 1e-9


def test_s10_three_group_caps_and_tie_and_axis():
    """S10 — 3 grupos: reparto exacto; empate [1,4,1] corta en 1; eje con lattice sintetico."""
    from estorides_core.graph_bundle import _split_caps, fibonacci_sphere, spherical_edge_bundling

    lay = spherical_edge_bundling(
        {"g1": ["a", "b"], "g2": ["c"], "g3": ["d", "e", "f"]}, [])
    assert [c for _, _, c in lay.groups] == [2, 1, 3]
    assert len(lay.leaves) == 6
    assert lay.hubs["g1"][0] == lay.groups[0][1][0] * 0.55
    assert lay.hubs["g1"] == (-0.29943348132944775, -0.13020251503552516, -0.44259111529418566)
    assert lay.hubs["g2"] == (0.2565218083787724, -0.45833333333333337, -0.16317817679346702)
    assert lay.hubs["g3"] == (0.15124260868199846, 0.343207631124688, 0.4022862106222932)
    out: dict = {}
    _split_caps(["x", "y", "z"], {"x": 1, "y": 4, "z": 1}, list(range(6)),
                fibonacci_sphere(6), out)
    assert out == {"x": [2], "y": [5, 4, 3, 1], "z": [0]}
    out2: dict = {}
    _split_caps(["a", "b"], {"a": 1, "b": 1},
                [0, 1], [(10.0, 0.0, 0.0), (-10.0, 0.0, 0.0)], out2)
    assert out2 == {"a": [1], "b": [0]}
    out3: dict = {}
    _split_caps(["a", "b"], {"a": 1, "b": 1},
                [0, 1], [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)], out3)
    assert out3 == {"a": [1], "b": [0]}
