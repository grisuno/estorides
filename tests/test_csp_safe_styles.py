"""CSP-safe styles: regression tests for the inline-style bug introduced by
the CSP tightening in commit 45c3af5.

The contract:

* The HTML template must not contain any `style="..."` attributes.
  Browsers block those under the locked-down `style-src` policy.
* The JS bundle must not emit `style="..."` strings in any template
  literal — those would be re-injected into the DOM as inline styles
  and blocked the same way.
* Dynamic per-cluster / per-kind colouring must go through the CSSOM
  (`el.style.background = cs`), which CSP does *not* restrict.
* The CSP itself must not have been relaxed back to `'unsafe-inline'`.
* The eight offscreen elements must use the HTML5 `hidden` attribute
  (which the browser's user-agent stylesheet turns into `display:none`),
  not a literal `style="display:none"`.

These tests parse the files on disk; they do not require a running app.
A complementary Flask-level test renders `index.html` through a test
client to confirm the same holds in the served output.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

from estorides_core.search_telemetry import SearchTelemetry

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "index.html"
JS_FILE = ROOT / "static" / "js" / "estorides.js"
CSS_FILE = ROOT / "static" / "css" / "estorides_ui.css"


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _strip_template_jinja(template_text: str) -> str:
    """Replace `{{ ... }}` and `{% ... %}` with empty so the file is grep-able.

    We only care whether the *static markup* contains `style="..."`. A
    `{{ estorides_auth_token or '' }}` cannot produce a `style="` because
    the auth token is a short opaque string and Jinja escapes it
    (autoescape=on by default for .html). Even if the token were
    malicious, a separate test (S7) covers the injection vector.
    """
    no_jinja = re.sub(r"\{\{.*?\}\}", "", template_text, flags=re.DOTALL)
    no_jinja = re.sub(r"\{%.*?%\}", "", no_jinja, flags=re.DOTALL)
    return no_jinja


def _strip_js_comments_and_strings_outside_templates(js_text: str) -> str:
    """Return the *template-literal contents* of the JS file as a single string.

    We can't simply grep `style="` because of false positives in comments
    and regular strings (e.g. error messages). The CSP issue is
    specifically about values written into the DOM via `innerHTML`
    containing `style="`. The only way to do that in this codebase is
    through a template literal that gets assigned to `innerHTML`,
    `outerHTML`, or inserted via `insertAdjacentHTML`.

    Strategy: strip line (`// …`) and block (`/* … */`) comments
    first so backticks inside comments don't confuse the template
    literal scanner. Then extract every backtick-delimited template
    literal and return them joined.
    """
    no_block = re.sub(r"/\*.*?\*/", "", js_text, flags=re.DOTALL)
    no_line = re.sub(r"//[^\n]*", "", no_block)
    chunks: list[str] = []
    i = 0
    n = len(no_line)
    while i < n:
        if no_line[i] == "`":
            j = no_line.find("`", i + 1)
            if j == -1:
                break
            chunks.append(no_line[i + 1 : j])
            i = j + 1
        else:
            i += 1
    return "\n".join(chunks)


# --------------------------------------------------------------------------- #
# S1: template has zero style="...                                            #
# --------------------------------------------------------------------------- #
def test_index_html_has_no_style_attribute():
    """S1 — `style="..."` must not appear anywhere in the rendered template.

    Browsers reject inline style attributes under the locked-down
    `style-src` policy. The fix is to use CSS classes (or `hidden`) —
    not to relax the policy.
    """
    raw = TEMPLATE.read_text(encoding="utf-8")
    static_part = _strip_template_jinja(raw)
    matches = re.findall(r'style\s*=\s*"', static_part)
    assert matches == [], (
        f"templates/index.html contains {len(matches)} inline style "
        f"attribute(s). Inline styles are blocked by the CSP "
        f"(style-src 'self' 'unsafe-hashes' https://unpkg.com). "
        f"Move them to CSS classes (see spec/csp_safe_styles.md)."
    )


# --------------------------------------------------------------------------- #
# S2: JS template literals have no style="                                    #
# --------------------------------------------------------------------------- #
def test_estorides_js_has_no_style_in_template_literals():
    """S2 — `style="..."` must not appear in any template literal in the JS.

    JS uses `innerHTML = `…`` to inject HTML. The literal text must
    not contain `style="…"` because the browser will then try to
    apply that style attribute and CSP will block it.
    """
    raw = JS_FILE.read_text(encoding="utf-8")
    literals = _strip_js_comments_and_strings_outside_templates(raw)
    matches = re.findall(r'style\s*=\s*"', literals)
    assert matches == [], (
        f"static/js/estorides.js has {len(matches)} `style=\"...\"` "
        f"occurrence(s) in template literals. CSP blocks those. "
        f"Use `el.style.X = value` (CSSOM) for dynamic styles, "
        f"or a CSS class for static ones."
    )


# --------------------------------------------------------------------------- #
# S3: 8 offscreen elements use `hidden` attribute                              #
# --------------------------------------------------------------------------- #
EXPECTED_HIDDEN_IDS = [
    "run-progress",
    "discover-progress",
    "result-filters",
    "graph-tooltip",
    "graph-context-menu",
    "graph-inspector",
    "onboarding",
    "kbd-help",
]


@pytest.mark.parametrize("element_id", EXPECTED_HIDDEN_IDS)
def test_offscreen_element_uses_hidden_attribute(element_id: str):
    """S3 — Each offscreen element must have the HTML5 `hidden` attribute.

    The browser's user-agent stylesheet already turns `[hidden]` into
    `display: none`, so we don't need a literal `style="display:none"`.
    """
    raw = TEMPLATE.read_text(encoding="utf-8")
    static_part = _strip_template_jinja(raw)
    pattern = re.compile(
        rf'<[a-zA-Z]+[^>]*\bid\s*=\s*"{re.escape(element_id)}"[^>]*>',
        re.DOTALL,
    )
    m = pattern.search(static_part)
    assert m, f"#{element_id} not found in templates/index.html"
    tag = m.group(0)
    assert "hidden" in tag, (
        f"#{element_id} should use the HTML5 `hidden` attribute "
        f"(not inline `style=\"display:none\"`). Got: {tag!r}"
    )
    assert "style=" not in tag, (
        f"#{element_id} still has a style= attribute. "
        f"Inline styles are blocked by CSP. Got: {tag!r}"
    )


# --------------------------------------------------------------------------- #
# S4: CSS file has the new classes                                            #
# --------------------------------------------------------------------------- #
EXPECTED_CSS_CLASSES = [
    # button "stop" inline style
    ".stop-btn-sm",
    # meta-row with margin-top
    ".meta-row-spaced",
    # JS-generated elements
    ".empty-entities",
    ".graph-top-title",
    ".timeline-title",
    ".timeline-meta",
    # kbd overlay action row
    ".kbd-actions",
]


@pytest.mark.parametrize("selector", EXPECTED_CSS_CLASSES)
def test_css_has_required_class(selector: str):
    """The CSS file must define the new classes the refactor relies on."""
    raw = CSS_FILE.read_text(encoding="utf-8")
    assert selector in raw, (
        f"static/css/estorides_ui.css does not define {selector!r}. "
        f"This class is required by the csp_safe_styles refactor."
    )


# --------------------------------------------------------------------------- #
# S5: CSP does not allow 'unsafe-inline' for style                            #
# --------------------------------------------------------------------------- #
def test_csp_policy_does_not_relax_for_unsafe_inline():
    """S5 — The locked-down CSP must stay locked down.

    The whole point of the refactor is that we don't have to relax
    `style-src` to make the UI work. If this test ever fails, the
    previous fix was reverted to `'unsafe-inline'` — a regression.
    """
    from estorides_core.web_security import WebSecurityConfig

    csp = WebSecurityConfig.csp_policy
    # `style-src` directive specifically must not allow inline.
    style_match = re.search(r"style-src\s+([^;]+)", csp)
    assert style_match, "no style-src directive in CSP"
    style_tokens = style_match.group(1).split()
    assert "'unsafe-inline'" not in style_tokens, (
        "style-src re-allows 'unsafe-inline'. The csp_safe_styles "
        "refactor must not be undone by relaxing the CSP."
    )
    # `default-src` doesn't need to be checked separately; we only have
    # `style-src` in this policy. But assert 'unsafe-inline' is not
    # anywhere in style-src chain anyway.
    assert "unsafe-hashes" not in style_tokens or "unsafe-inline" not in style_tokens


def test_csp_policy_is_unchanged_after_refactor():
    """S6 — The default CSP string is byte-identical to the pre-refactor value.

    The fix is in the frontend, not in the policy. If this test fails,
    the policy was changed instead of refactored.
    """
    from estorides_core.web_security import WebSecurityConfig

    expected = (
        "default-src 'self'; "
        "script-src 'self' https://unpkg.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-hashes' https://unpkg.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://unpkg.com; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    assert WebSecurityConfig.csp_policy == expected, (
        "Default CSP was changed. The csp_safe_styles fix is supposed "
        "to leave the policy alone and refactor the frontend."
    )


# --------------------------------------------------------------------------- #
# S4/S7: dynamic colour assignment via CSSOM                                  #
# --------------------------------------------------------------------------- #
def test_dynamic_cluster_color_uses_cssom_assignment():
    """S4 — The bridge-tooltip chip must set background via CSSOM.

    We assert that the JS code *does* set `chip.style.background = cs`
    (or `span.style.backgroundColor = cs`) and that the HTML string
    for the chip is built without a `style="background:…"` attribute.
    """
    raw = JS_FILE.read_text(encoding="utf-8")
    assert re.search(r"\.style\.background\s*=", raw), (
        "Dynamic cluster color is not assigned via CSSOM "
        "(`el.style.background = cs`). Refactor `showBridgeTooltip` "
        "to set the background on a created <span>, not in innerHTML."
    )
    literals = _strip_js_comments_and_strings_outside_templates(raw)
    assert "style=\"background:" not in literals, (
        "Found `style=\"background:` in a JS template literal. "
        "This string is injected into the DOM and CSP will block it."
    )


def test_dynamic_kind_color_uses_cssom_assignment():
    """S4 (kind) — `colorForKind(e.kind)` must reach CSSOM, not innerHTML."""
    raw = JS_FILE.read_text(encoding="utf-8")
    assert re.search(r"\.style\.color\s*=", raw), (
        "Dynamic per-kind color is not assigned via CSSOM "
        "(`el.style.color = colorForKind(e.kind)`)."
    )
    literals = _strip_js_comments_and_strings_outside_templates(raw)
    assert "style=\"color:${" not in literals, (
        "Found `style=\"color:${` in a JS template literal. "
        "This string is injected into the DOM and CSP will block it."
    )


# --------------------------------------------------------------------------- #
# S8: rendered template has no style= and hidden attr is on offscreen elements #
# --------------------------------------------------------------------------- #
def test_rendered_template_has_no_style_attribute_and_uses_hidden():
    """End-to-end: render `index.html` and assert no inline styles leak."""
    from flask import Flask

    app = Flask(__name__, template_folder=str(ROOT / "templates"))
    app.config["TESTING"] = True

    with app.test_request_context():
        env = Environment(
            loader=FileSystemLoader(str(ROOT / "templates")),
            autoescape=select_autoescape(["html"]),
        )
        tmpl = env.get_template("index.html")
        html = tmpl.render(
            estorides_auth_token="",
            telemetry=SearchTelemetry().context(),
        )
    assert 'style="' not in html, (
        f"Rendered index.html still contains `style=\"`. "
        f"Refactor is incomplete. First 200 chars around the first match:\n"
        f"{html[html.find('style=')-50:html.find('style=')+150]!r}"
    )
    for element_id in EXPECTED_HIDDEN_IDS:
        # Match `<tag ... id="element_id" ... >` (attribute order agnostic)
        pat = re.compile(
            rf'<[a-zA-Z]+[^>]*\bid\s*=\s*"{re.escape(element_id)}"[^>]*>',
            re.DOTALL,
        )
        m = pat.search(html)
        assert m, f"#{element_id} not found in rendered HTML"
        tag = m.group(0)
        assert "hidden" in tag, (
            f"#{element_id} lost its `hidden` attribute after render. "
            f"Got: {tag!r}"
        )
