"""graph_bundle S6: assets frontend (fuera del sandbox mutmut).

Este archivo NO entra en la seleccion de mutmut (solo mira
tests/test_graph_bundle.py): el sandbox `mutants/` no copia
templates/static y estos asserts fallarian alli por FileNotFound.
"""
from __future__ import annotations

from pathlib import Path

import pytest

# Blindaje deliberado (precedente: graph_rag_search S7): este archivo no
# abre DBs; con `filterwarnings=error` el GC puede atribuirle conexiones
# sqlite sin cerrar dejadas por otros tests (victima aleatoria).
pytestmark = pytest.mark.filterwarnings("ignore::ResourceWarning")


def test_s6_frontend_assets_exist_and_are_csp_clean():
    """S6 — tab Bundles + JS sin innerHTML/eval + CSS con tokens."""
    root = Path(__file__).resolve().parent.parent
    html = (root / "templates" / "index.html").read_text(encoding="utf-8")
    assert 'data-canvas="bundles"' in html
    assert 'id="bundles-canvas"' in html
    assert 'class="bundles-canvas"' in html
    assert 'id="gb-c"' in html and 'id="gb-stage"' in html
    assert 'data-view="2d"' in html and 'data-view="3d"' in html
    assert 'graph_bundle.js' in html
    js = (root / "static" / "js" / "graph_bundle.js").read_text(encoding="utf-8")
    assert "innerHTML" not in js.replace("never touch innerHTML", "")
    assert "eval(" not in js
    assert 'style="' not in js.replace('through style="..." markup', "")
    css = (root / "static" / "css" / "estorides_ui.css").read_text(encoding="utf-8")
    assert "--gb-accent" in css and ".gb-stage" in css and ".gb-tip" in css
