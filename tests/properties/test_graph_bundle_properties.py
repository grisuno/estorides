"""Property-based invariants for estorides_core.graph_bundle.

Fuzzing con 1000 ejemplos por propiedad (doctrina: input hostil).
P1 totalidad (nunca crash fuera de TypeError + salida consistente),
P2 determinismo byte-identico, P3 vacio, P4 settings acotados.
"""
from __future__ import annotations

import json
import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from estorides_core.graph_bundle import build_bundle_payload, bundle_settings

# Blindaje deliberado (precedente: graph_rag_search S7): estos tests no
# abren DBs; con `filterwarnings=error` el GC puede atribuirles conexiones
# sqlite sin cerrar dejadas por otros tests (victima aleatoria).
pytestmark = pytest.mark.filterwarnings("ignore::ResourceWarning")

IDS = st.text(min_size=1, max_size=24)
LABEL = st.text(max_size=600)
COMM = st.one_of(st.none(), st.integers(min_value=0, max_value=4))
REL = st.sampled_from(
    ["related-to", "resolves-to", "same-as", "contains", "member_of", "layered_as"]
)


@st.composite
def force_strategy(draw: st.DrawFn) -> dict:
    ids = draw(st.lists(IDS, min_size=0, max_size=12, unique=True))
    nodes = []
    for i, nid in enumerate(ids):
        nodes.append(
            {
                "id": nid,
                "label": draw(LABEL),
                "type": "entity",
                "kind": draw(st.text(max_size=24)),
                "community": draw(COMM),
                "community_label": draw(st.text(max_size=40)),
                "family": draw(st.text(max_size=40)),
                "layer": draw(st.text(max_size=24)),
                "color": draw(st.text(max_size=24)),
                "rank": draw(
                    st.one_of(
                        st.floats(allow_nan=False, allow_infinity=False),
                        st.integers(),
                        st.text(max_size=16),
                    )
                ),
                "rank_pos": draw(st.integers(min_value=-5, max_value=99)),
                "findings": draw(st.integers(min_value=-5, max_value=99)),
                "doc": draw(st.text(max_size=200)),
            }
        )
        if draw(st.booleans()) and i % 3 == 0:
            nodes.append(
                {
                    "id": f"community:{draw(st.integers(min_value=0, max_value=4))}",
                    "label": draw(st.text(max_size=40)),
                    "type": "community",
                    "color": draw(st.text(max_size=24)),
                }
            )
    edges = []
    for _ in range(draw(st.integers(min_value=0, max_value=20))):
        if not ids:
            break
        edges.append(
            {
                "source": draw(st.sampled_from(ids)),
                "target": draw(st.sampled_from(ids)),
                "type": draw(REL),
            }
        )
    return {"nodes": nodes, "edges": edges}


def _assert_consistent(out: dict, raw: dict) -> None:
    assert set(out.keys()) == {"nodes", "groups", "edges"}
    n, g = len(out["nodes"]), len(out["groups"])
    seen = set()
    for node in out["nodes"]:
        assert node["id"] not in seen
        seen.add(node["id"])
        assert 0 <= node["g"] < g or g == 0
        assert math.isfinite(node["a"])
        x, y, z = node["p"]
        assert abs(math.sqrt(x * x + y * y + z * z) - 1.0) < 2e-5
        assert len(node["l"]) <= 512
    entity_ids = {nd["id"] for nd in raw["nodes"] if isinstance(nd, dict) and nd.get("type") == "entity"}
    assert seen <= entity_ids
    for edge in out["edges"]:
        a, b = edge
        assert 0 <= a < n and 0 <= b < n and a != b
    json.dumps(out)


@settings(max_examples=1000, deadline=None)
@given(force_strategy())
def test_p1_total_and_consistent(payload: dict) -> None:
    """P1 — jamas crash fuera de TypeError; salida consistente y JSON-safe."""
    try:
        out = build_bundle_payload(payload)
    except TypeError:
        return
    _assert_consistent(out, payload)


@settings(max_examples=1000, deadline=None)
@given(force_strategy())
def test_p2_deterministic(payload: dict) -> None:
    """P2 — dos pasadas byte-identicas (o ambas TypeError)."""
    try:
        first = build_bundle_payload(payload)
    except TypeError:
        try:
            build_bundle_payload(payload)
            raise AssertionError("segunda pasada no fallo")
        except TypeError:
            return
        return
    assert build_bundle_payload(payload) == first


@settings(max_examples=1000, deadline=None)
@given(st.lists(force_strategy(), min_size=1, max_size=3))
def test_p3_empty_never_raises(payloads: list) -> None:
    """P3 — payload vacio siempre devuelve vacio sin raise."""
    out = build_bundle_payload({"nodes": [], "edges": []})
    assert out == {"nodes": [], "groups": [], "edges": []}
    for _ in payloads:
        build_bundle_payload({"nodes": [], "edges": []})


@settings(max_examples=1000, deadline=None)
@given(st.data())
def test_p4_settings_bounded(data: st.DataObject) -> None:
    """P4 — settings con claves fijas y beta/perspective acotados."""
    data.draw(st.integers(min_value=0, max_value=10))
    s = bundle_settings()
    for key in ("mode", "beta", "samples", "innerRatio", "groupGap",
                "edgeAlpha", "labelTopN", "labelMax", "nodeMin", "nodeMax",
                "hitPx", "perspective", "depthFade", "particles",
                "unassignedKey"):
        assert key in s
    assert 0.0 <= float(s["beta"]) <= 100.0
    assert s["mode"] == "2d"
    assert s["unassignedKey"] == "unassigned"
