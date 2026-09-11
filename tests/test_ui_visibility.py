"""
Regression tests for the `hidden` attribute contract and output escaping.

`estorides_ui.css` enforces `[hidden] { display: none !important }`, so an
element carrying the HTML5 `hidden` attribute can only be revealed by
clearing the attribute. Toggling inline `style.display` alone leaves it
permanently invisible. These tests pin the JS to the correct pattern.

Also pins that remote-sourced fields interpolated into `innerHTML` are
escaped (XSS defence for the fusion entity detail + entity list).
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JS = ROOT / "static" / "js" / "estorides.js"
CSS = ROOT / "static" / "css" / "estorides_ui.css"


def _js() -> str:
    return JS.read_text(encoding="utf-8")


class TestHiddenContract:
    def test_css_enforces_hidden(self) -> None:
        assert "[hidden] { display: none !important; }" in CSS.read_text(encoding="utf-8")

    def test_setvisible_clears_hidden_attribute(self) -> None:
        src = _js()
        assert "function setVisible(" in src
        assert "el.hidden = !show;" in src

    def test_no_inline_display_reveal_of_hidden_overlays(self) -> None:
        """The old buggy patterns that could never reveal a hidden element."""
        src = _js()
        for pattern in (
            "overlay.style.display = 'flex'",
            "wrap.style.display = 'flex'",
            "el.style.display = 'block';",
            "menu.style.display = 'block'",
            "panel.style.display = 'block'",
            "controls.style.display = ''",
        ):
            assert pattern not in src, f"hidden-attribute element still shown via: {pattern}"

    def test_tooltip_and_menu_use_setvisible(self) -> None:
        src = _js()
        assert "setVisible($('#graph-tooltip'), false)" in src
        assert "setVisible($('#graph-context-menu'), false)" in src
        assert "setVisible(menu, true, 'block')" in src


class TestOutputEscaping:
    def test_entity_list_escapes_type_and_source(self) -> None:
        src = _js()
        assert "escapeHTML(e.type)" in src
        assert "escapeHTML(e.source)" in src

    def test_fusion_detail_escapes_intel_level_and_lists(self) -> None:
        src = _js()
        # intel level is sanitised before entering a class attribute
        assert "replace(/[^a-z_]/gi, '')" in src
        assert "escapeHTML(lvl)" in src
        # list fields are mapped through escapeHTML, not joined raw
        assert "s.sources.map(" in src
        assert "props.keys.map(" in src
        assert "rels.types.map(" in src
