"""graph_rag_search: BM25 + PageRank/PPR + map-reduce global (contrato S1-S6)."""
from __future__ import annotations

import json

import networkx as nx
import pytest

from estorides_core.graph_rag_search import (
    GraphRagSearcher,
    build_index,
    graph_context_block,
    pagerank,
    personalized_pagerank,
)


def _nodes():
    return [
        {"id": "a", "label": "example.com", "type": "domain", "kind": "domain",
         "cluster": 0, "level": "information"},
        {"id": "b", "label": "1.2.3.4", "type": "ipv4", "kind": "ip",
         "cluster": 0, "level": "data"},
        {"id": "c", "label": "admin@example.com", "type": "email", "kind": "person",
         "cluster": 1, "level": "intelligence"},
    ]


def _edges():
    return [
        {"source": "a", "target": "b", "relation": "resolves-to"},
        {"source": "b", "target": "c", "relation": "related-to"},
    ]


def _clusters():
    return [
        {"id": 0, "label": "example.com infra"},
        {"id": 1, "label": "mail identity"},
    ]


def _searcher():
    return GraphRagSearcher(None, build_index(_nodes(), _edges(), _clusters()))


# S1 — happy path local                                                     #
def test_s1_local_match_leads():
    """S1 — query con match lexico va en local y la entidad lidera."""
    ctx = _searcher().search("example.com")
    assert ctx.mode == "local"
    assert ctx.entities and ctx.entities[0][0] == "a"
    assert ctx.relations, "debe haber relaciones entre elegidas"
    for section in ("## Entities", "## Relationships",
                    "## Community reports", "## Sources"):
        assert section in ctx.markdown, section
    assert ctx.approx_tokens > 0


# S2 — happy path global                                                    #
def test_s2_global_hints_map_reduce():
    """S2 — hints de overview eligen map-reduce con reportes."""
    ctx = _searcher().search("overview of everything")
    assert ctx.mode == "global"
    assert ctx.reports, "map-reduce debe elegir comunidades"
    assert "## Overview" in ctx.markdown
    assert "## Relevant communities (map-reduce)" in ctx.markdown


# S3 — edge: vacio                                                         #
def test_s3_empty_graph_no_raise():
    """S3 — indice vacio responde sin romper; el mensaje local es explicito."""
    searcher = GraphRagSearcher(None, build_index([], [], []))
    auto = searcher.search("anything")
    assert auto.mode == "global", "sin matches lexicos -> global"
    local = searcher.search("anything", mode="local")
    assert "No entity matches" in local.markdown
    assert local.entities == []
    assert searcher.choose_mode("") == "global"


# S4 — seguridad                                                            #
def test_s4_hostile_fails_closed_and_bounded():
    """S4 — set/bytes -> TypeError; fuzzinlinea acotado con fences pares."""
    bad = [
        {"id": "x", "label": {"evil", "set"}, "type": "domain"},
        {"id": "y", "label": b"bytes", "type": "ipv4"},
    ]
    try:
        build_index(bad, [], [])
        raised = False
    except TypeError:
        raised = True
    assert raised, "input no JSON-safe debe fallar cerrado"
    evil = [
        {"id": f"e{i}", "label": "# h\n```\n[x](javascript:q())\n" + "A" * 5000,
         "type": "domain", "cluster": 0}
        for i in range(10)
    ]
    ctx = GraphRagSearcher(None, build_index(evil, [], [])).search(
        "A" * 10, budget_tokens=125)
    assert len(ctx.markdown) <= 125 * 4
    assert ctx.markdown.count("```") % 2 == 0
    assert "…truncated" in ctx.markdown


# S5 — matematicas y determinismo                                           #
def test_s5_pagerank_sums_to_one_and_deterministic():
    """S5 — PR suma 1, seed lidera PPR, todo byte-identico entre pasadas."""
    ids = ["a", "b", "c"]
    edges = [("a", "b", 1.0), ("b", "c", 0.8), ("c", "a", 0.8)]
    pr = pagerank(ids, edges)
    assert abs(sum(pr.values()) - 1.0) < 1e-6
    ppr = personalized_pagerank(ids, edges, {"a": 1.0})
    assert sorted(ppr, key=lambda k: -ppr[k])[0] == "a"
    first = build_index(_nodes(), _edges(), _clusters()).to_dict()
    second = build_index(_nodes(), _edges(), _clusters()).to_dict()
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    s = _searcher()
    assert s.search("example.com").markdown == s.search("example.com").markdown


# S6 — wire-up desde DiGraph                                               #
def test_s6_context_block_from_digraph():
    """S6 — bloque de prompt desde nx.DiGraph, acotado; vacio -> ''."""
    g = nx.DiGraph()
    for i, (t, v) in enumerate([("domain", "example.com"), ("ipv4", "1.2.3.4"),
                                ("email", "x@y.z"), ("domain", "sub.example.com")]):
        g.add_node(f"n{i}", type=t, value=v)
    g.add_edge("n0", "n1", relation="resolves-to")
    g.add_edge("n1", "n2", relation="related-to")
    block = graph_context_block("assess example.com", g,
                                {"n0": 0, "n1": 0, "n2": 1, "n3": 0},
                                budget_tokens=400)
    assert "# GraphRAG" in block and "example.com" in block
    assert len(block) <= 400 * 4
    assert graph_context_block("q", nx.DiGraph(), {}, 400) == ""


# S7 — wire-up web: helper fail-soft sobre GRAPH_PATH real                  #
@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_s7_web_helper_uses_graph_path_fail_soft(tmp_path, monkeypatch):
    """S7 — `_graph_rag_block` lee el grafo y falla a '' sin grafo.

    El ignore de ResourceWarning es deliberado: este test no abre DBs;
    con `filterwarnings=error` el GC puede atribuirle conexiones sqlite
    sin cerrar dejadas por otros tests de la suite (víctima aleatoria).
    """
    import estorides_web as web

    g = nx.DiGraph()
    g.add_node("n0", type="domain", value="example.com")
    g.add_node("n1", type="ipv4", value="1.2.3.4")
    g.add_edge("n0", "n1", relation="resolves-to")
    target = tmp_path / "g.graphml"
    nx.write_graphml(g, target)
    monkeypatch.setattr(web, "GRAPH_PATH", target)
    block = web._graph_rag_block("assess example.com", budget_tokens=200)
    assert "# GraphRAG" in block and "example.com" in block
    assert len(block) <= 200 * 4
    monkeypatch.setattr(web, "GRAPH_PATH", tmp_path / "missing.graphml")
    assert web._graph_rag_block("assess example.com") == ""
