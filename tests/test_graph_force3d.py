"""graph_force3d: port del sistema de grafos ReadMenator + contexto IA.

Escenarios del contrato `spec/graph_force3d.md`:
S1 happy path (payload RAW), S2 edge (vacio), S3 error/truncacion
determinista con puentes primero, S4 seguridad (no JSON-safe -> TypeError),
S5 seguridad (contexto IA acotado y sin inyeccion markdown), S6 settings y
colores deterministas.
"""
from __future__ import annotations

import json

from estorides_core.graph_force import (
    build_ai_context,
    build_force_payload,
    family_color_from_name,
    force_settings,
    node_value,
)


def _nodes():
    return [
        {"id": "a", "label": "example.com", "type": "domain", "kind": "domain",
         "color": "#5B8FF9", "cluster": 0, "cluster_color": "#5fb4ff",
         "level": "information", "size": 7},
        {"id": "b", "label": "1.2.3.4", "type": "ipv4", "kind": "ip",
         "color": "#F6BD16", "cluster": 0, "cluster_color": "#5fb4ff",
         "level": "data", "size": 8},
        {"id": "c", "label": "x@y.com", "type": "email", "kind": "person",
         "color": "#9270CA", "cluster": 1, "cluster_color": "#ff9e64",
         "level": "intelligence", "size": 7},
    ]


def _edges():
    return [
        {"source": "a", "target": "b", "relation": "resolves-to",
         "inter_cluster": False, "clusters": None},
        {"source": "b", "target": "c", "relation": "related-to",
         "inter_cluster": True, "clusters": [0, 1]},
    ]


def _clusters():
    return [
        {"id": 0, "size": 2, "color": "#5fb4ff", "label": "example.com"},
        {"id": 1, "size": 1, "color": "#ff9e64", "label": "x@y.com"},
    ]


# S1 — happy path: payload OSINT con forma RAW                            #
def test_s1_build_force_payload_shape():
    """S1 — 3 nodos + 2 edges producen entidades, comunidades y tiers."""
    payload = build_force_payload(_nodes(), _edges(), _clusters())
    by_id = {n["id"]: n for n in payload["nodes"]}
    # 3 entidades + 2 comunidades + 2 tiers (information, data,
    # intelligence -> 3 tiers en realidad).
    entities = [n for n in payload["nodes"] if n["type"] == "entity"]
    assert len(entities) == 3
    assert "community:0" in by_id and "community:1" in by_id
    assert "tier:information" in by_id
    # family compartida dentro del cluster.
    assert by_id["a"]["family"] == by_id["b"]["family"]
    assert by_id["a"]["family"] != by_id["c"]["family"]
    # Grados y rank: b tiene grado 2 -> rank_pos 1.
    assert by_id["b"]["degree"] == 2
    assert by_id["a"]["degree"] == 1
    assert by_id["c"]["degree"] == 1
    assert by_id["b"]["rank_pos"] == 1
    # Edges OSINT + member_of + layered_as presentes.
    types = {e["type"] for e in payload["edges"]}
    assert {"resolves-to", "related-to", "member_of", "layered_as"} <= types
    # node_value usado en val.
    assert by_id["b"]["val"] == node_value(0, 2)


# S2 — edge: grafo vacio                                                  #
def test_s2_empty_graph_no_raise():
    """S2 — payload vacio y contexto 'empty graph' sin excepciones."""
    payload = build_force_payload([], [], [])
    assert payload["nodes"] == [] and payload["edges"] == []
    assert payload["meta"]["node_count"] == 0
    ctx = build_ai_context([], [], [])
    assert ctx["entities"] == [] and ctx["relations"] == []
    assert "empty graph" in ctx["markdown"]


# S3 — error: truncacion determinista, puentes primero                    #
def test_s3_truncation_deterministic_bridge_first():
    """S3 — dos pasadas identicas; el puente sobrevive al corte."""
    nodes = [
        {"id": f"n{i}", "label": f"n{i}", "type": "domain",
         "cluster": 0 if i < 9 else 1}
        for i in range(10)
    ]
    edges = [
        {"source": f"n{i}", "target": f"n{i+1}", "relation": "related-to"}
        for i in range(8)
    ] + [{"source": "n8", "target": "n9", "relation": "related-to",
           "inter_cluster": True, "clusters": [0, 1]}]
    first = build_force_payload(nodes, edges, [], max_nodes=5, max_edges=4)
    second = build_force_payload(nodes, edges, [], max_nodes=5, max_edges=4)
    assert first == second, "la truncacion debe ser determinista"
    assert first["meta"]["truncated"] is True
    kept = {n["id"] for n in first["nodes"] if n["type"] == "entity"}
    assert "n8" in kept and "n9" in kept, "el puente debe sobrevivir"
    assert len(kept) <= 5


# S4 — seguridad: input no JSON-safe falla cerrado                         #
def test_s4_non_json_safe_raises_typeerror():
    """S4 — set/bytes en labels -> TypeError, nunca payload parcial."""
    bad = [
        {"id": "x", "label": {"evil", "set"}, "type": "domain"},
        {"id": "y", "label": b"bytes", "type": "ipv4"},
    ]
    try:
        build_force_payload(bad, [], [])
        raised = False
    except TypeError:
        raised = True
    assert raised, "input no JSON-safe debe fallar cerrado con TypeError"
    # Un payload valido siempre serializa.
    ok = build_force_payload(_nodes(), _edges(), _clusters())
    json.dumps(ok)


# S5 — seguridad: contexto IA acotado y sin inyeccion                     #
def test_s5_ai_context_budget_and_no_markdown_injection():
    """S5 — budget duro, fences pares, marcador truncated."""
    nodes = [
        {
            "id": f"e{i}",
            "label": "# hacked\n```\n[click](javascript:alert(1))\n" + "A" * 5000,
            "type": "domain",
            "cluster": 0,
        }
        for i in range(10)
    ]
    ctx = build_ai_context(nodes, [], [], budget_chars=500)
    assert len(ctx["markdown"]) <= 500
    assert ctx["markdown"].count("```") % 2 == 0, "fences sin cerrar"
    assert "…truncated" in ctx["markdown"]
    assert ctx["approx_tokens"] > 0


# S6 — determinismo de colores y settings                                  #
def test_s6_family_color_deterministic_and_settings_match_readmenator():
    """S6 — mismo HSL siempre; settings con los 19 valores ReadMenator."""
    assert family_color_from_name("c0") == family_color_from_name("c0")
    import re

    color = family_color_from_name("c0")
    assert re.fullmatch(r"hsl\(\d{1,3}, 5[5-9]|6[0-7]%, 5[89]|6[0-8]%\)", color) or \
        re.fullmatch(r"hsl\(\d+, \d+%, \d+%\)", color)
    hue, sat, light = (int(x) for x in re.findall(r"\d+", color)[:3])
    assert 0 <= hue < 360 and 55 <= sat <= 67 and 58 <= light <= 68
    settings = force_settings()
    assert settings["charge"] == -300
    assert settings["linkDistance"] == 120
    assert settings["linkStrength"] == 0.3
    assert settings["nodeRelSize"] == 4
    assert settings["particles"] == 4
    assert settings["labelTopN"] == 30
    assert settings["labelZoom"] == 1.6
    assert settings["clusterStrength"] == 0.6
    assert settings["flyMs"] == 700
