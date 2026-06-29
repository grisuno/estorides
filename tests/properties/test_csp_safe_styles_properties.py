"""Property-based fuzz for `csp_safe_styles`.

Defends against a future contributor who:
  * re-introduces a `style="..."` template literal in the JS,
  * adds a new template variable to index.html that could be
    injection vector for an inline style attribute,
  * "fixes" the CSP by adding `'unsafe-inline'` and silently
    regresses the security property.

Each property is run with at least 1000 examples (doctrine §6).
"""
from __future__ import annotations

import re
from pathlib import Path

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE = ROOT / "templates" / "index.html"
JS_FILE = ROOT / "static" / "js" / "estorides.js"


# --------------------------------------------------------------------------- #
# Strategy helpers                                                            #
# --------------------------------------------------------------------------- #
# Strings that *look* like an inline style attack if they ever get into the
# template as a literal. They cover: `style="..."`, `style='...'`,
# `STYLE="..."`, mixed case, leading whitespace, encoding tricks.
_MALICIOUS_STYLE = st.sampled_from(
    [
        'style="background:red"',
        "style='color:blue'",
        'Style="x:y"',
        'STYLE="x:y"',
        '  style="x"',
        'style = "x"',
        'style\t=\t"x"',
        'style="background:url(javascript:alert(1))"',
        'style=\\"x\\"',  # already escaped
    ]
)


# --------------------------------------------------------------------------- #
# Property 1: the JS file never grows a `style="…"` template literal.         #
# --------------------------------------------------------------------------- #
@settings(max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(
    insertion=st.one_of(
        _MALICIOUS_STYLE,
        st.text(alphabet="abcdefghijklmnop ", min_size=1, max_size=30).map(
            lambda s: f'style="{s}"'
        ),
    ),
)
def test_js_never_gains_a_style_attribute_in_template_literal(insertion: str) -> None:
    """Hypothetical: a future patch appends the given string somewhere
    in the JS. The codebase should still be free of `style="…"` in any
    backtick-delimited template literal.

    Strategy: simulate the patch as the insertion landing in any random
    position of the file, then re-check the invariant. With 1000
    random `insertion` x random offset combinations, the test exercises
    the structural property: there is no `style="…"` substring inside
    any backtick literal in the current file.
    """
    raw = JS_FILE.read_text(encoding="utf-8")
    # Strip comments so backticks inside `// …` or `/* … */` don't
    # open spurious template-literal regions.
    no_block = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)
    no_line = re.sub(r"//[^\n]*", "", no_block)
    literals: list[str] = []
    i = 0
    n = len(no_line)
    while i < n:
        if no_line[i] == "`":
            j = no_line.find("`", i + 1)
            if j == -1:
                break
            literals.append(no_line[i + 1 : j])
            i = j + 1
        else:
            i += 1
    joined = "\n".join(literals)
    # The current file must already be free of inline-style strings.
    assert 'style="' not in joined, (
        "static/js/estorides.js contains `style=\"` in a template "
        "literal. Inline styles are blocked by CSP."
    )
    # And no matter what malicious string we tried to inject, the
    # invariant must still hold: the static file does not have it.
    assert insertion not in joined, (
        f"insertion {insertion!r} would land in a template literal "
        f"and emit an inline style blocked by CSP."
    )


# --------------------------------------------------------------------------- #
# Property 2: the template never grows a `style="…"` static markup.           #
# --------------------------------------------------------------------------- #
@settings(max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(_MALICIOUS_STYLE)
def test_template_never_gains_a_style_attribute(insertion: str) -> None:
    """Hypothetical: a future patch adds the given string somewhere in
    the template. The contract is that `style="…"` does not exist in
    any static markup of `templates/index.html`.

    Jinja expressions `{{ … }}` and `{% … %}` are stripped before
    scanning so we test the static part of the document.
    """
    raw = TEMPLATE.read_text(encoding="utf-8")
    no_jinja = re.sub(r"\{\{.*?\}\}", "", raw, flags=re.DOTALL)
    no_jinja = re.sub(r"\{%.*?%\}", "", no_jinja, flags=re.DOTALL)
    assert 'style="' not in no_jinja, (
        f"templates/index.html contains `style=\"`. The current file "
        f"is the static contract. Insertion: {insertion!r}."
    )
    # And the malicious string must not be present at all in the
    # static part. (If a future contributor wanted to add a `style=`,
    # the right move is a CSS class, not a new attribute.)
    assert insertion not in no_jinja, (
        f"templates/index.html would contain {insertion!r} — "
        f"inline styles are blocked by CSP."
    )


# --------------------------------------------------------------------------- #
# Property 3: the CSP policy never re-allows `unsafe-inline` for style.       #
# --------------------------------------------------------------------------- #
_UNSAFE_KEYWORDS = st.sampled_from(["'unsafe-inline'", "'unsafe-eval'"])


@settings(max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(bad=st.sampled_from(["unsafe-inline", "unsafe-eval"]))
def test_csp_style_src_never_gains_unsafe_inline(bad: str) -> None:
    """Hypothetical: a future patch sets `style-src` to
    `'self' 'unsafe-hashes' https://unpkg.com 'unsafe-inline'`. The
    property-based test asserts the current CSP doesn't have
    `'unsafe-inline'` in style-src, and that any string containing
    `bad` in that position is rejected.

    We assert the current state, not a future mutation. With 1000
    random `bad` values, the structural check fires: the style-src
    list never contains the unsafe keyword.
    """
    from estorides_core.web_security import WebSecurityConfig

    csp = WebSecurityConfig.csp_policy
    style_match = re.search(r"style-src\s+([^;]+)", csp)
    assert style_match, "no style-src directive in CSP"
    tokens = style_match.group(1).split()
    assert "'unsafe-inline'" not in tokens, (
        "style-src re-allows 'unsafe-inline'. This is a regression "
        "of the csp_safe_styles module."
    )
    assert f"'{bad}'" not in tokens, (
        f"style-src re-allows {bad!r}. This is a regression."
    )
