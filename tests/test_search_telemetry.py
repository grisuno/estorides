"""BDD/ATDD suite for the `search_telemetry` module (spec/search_telemetry.md).

Each test maps to a Given-When-Then scenario in the spec. The pure-logic
scenarios (S1-S6, S9, S10) exercise the module directly; the integration
scenarios (S7, S8, S11) render `index.html` through Jinja and assert the served
chrome honours the brand/emoji and single-source-of-truth invariants.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

from estorides_core.search_telemetry import (
    DEFAULT_TELEMETRY,
    DISALLOWED_BRANDS,
    InvalidTelemetryConfigError,
    KeyboardShortcut,
    SearchPhase,
    SearchTelemetry,
    SplashTip,
    TelemetryConfig,
    UnknownPhaseError,
    disallowed_brands_in,
    emoji_in,
    percent_encoded_emoji_in,
)

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "index.html"
JS_FILE = ROOT / "static" / "js" / "estorides.js"


def _render_index() -> str:
    """Render `index.html` exactly as the web layer does, telemetry included."""
    env = Environment(
        loader=FileSystemLoader(str(ROOT / "templates")),
        autoescape=select_autoescape(["html"]),
    )
    tmpl = env.get_template("index.html")
    return tmpl.render(
        estorides_auth_token="",
        telemetry=SearchTelemetry().context(),
    )


# --------------------------------------------------------------------------- #
# S1 — happy path: determinate progress mid-search                            #
# --------------------------------------------------------------------------- #
def test_s1_determinate_progress_midsearch() -> None:
    view = SearchTelemetry().progress(completed=12, total=40, phase_key="query")
    assert view.percent == 30
    assert view.active is True
    assert view.indeterminate is False
    assert view.label == "Querying sources - 12/40"
    assert view.aria_busy is True
    assert view.aria_valuenow == 30
    assert view.aria_valuemax == 100
    assert view.aria_valuetext == "12 of 40 sources, 30%"


# --------------------------------------------------------------------------- #
# S2 — edge: indeterminate progress before the source count is known          #
# --------------------------------------------------------------------------- #
def test_s2_indeterminate_progress() -> None:
    view = SearchTelemetry().progress(completed=0, total=0, phase_key="detect")
    assert view.indeterminate is True
    assert view.percent == 0
    assert view.aria_valuenow is None
    assert view.aria_busy is True
    assert view.label == "Detecting indicator type"


# --------------------------------------------------------------------------- #
# S3 — edge: completion settles the bar to 100 and stops the spinner          #
# --------------------------------------------------------------------------- #
def test_s3_completion_stops_spinner() -> None:
    view = SearchTelemetry().progress(completed=40, total=40, phase_key="done")
    assert view.percent == 100
    assert view.active is False
    assert view.aria_busy is False
    assert view.indeterminate is False


# --------------------------------------------------------------------------- #
# S4 — edge: out-of-range integers are clamped, never raised                  #
# --------------------------------------------------------------------------- #
def test_s4_out_of_range_is_clamped() -> None:
    tel = SearchTelemetry()
    high = tel.progress(completed=999, total=40, phase_key="query")
    assert high.completed == 40
    assert high.percent == 100
    low = tel.progress(completed=-5, total=40, phase_key="query")
    assert low.completed == 0
    assert low.percent == 0


# --------------------------------------------------------------------------- #
# S5 — error: unknown phase key is rejected                                   #
# --------------------------------------------------------------------------- #
def test_s5_unknown_phase_rejected() -> None:
    with pytest.raises(UnknownPhaseError) as exc:
        SearchTelemetry().progress(0, 10, phase_key="bogus")
    message = str(exc.value)
    assert "bogus" in message
    assert "query" in message


# --------------------------------------------------------------------------- #
# S6 — security: catalog is brand-clean and emoji-clean                       #
# --------------------------------------------------------------------------- #
def test_s6_catalog_is_brand_and_emoji_clean() -> None:
    context = SearchTelemetry().context()
    strings: list[str] = [context["brand"], context["tagline"]]
    for shortcut in context["shortcuts"]:
        strings.extend([shortcut["keys"], shortcut["description"]])
    for tip in context["tips"]:
        strings.extend([tip["title"], tip["body"]])
    for phase in context["phases"]:
        strings.append(phase["label"])
    for text in strings:
        assert disallowed_brands_in(text) == ()
        assert emoji_in(text) == ()
        assert percent_encoded_emoji_in(text) == ()


# --------------------------------------------------------------------------- #
# S7 — security: the served template names no third-party brand               #
# --------------------------------------------------------------------------- #
def test_s7_rendered_template_has_no_third_party_brand() -> None:
    html = _render_index()
    leaks = disallowed_brands_in(html)
    assert leaks == (), f"Rendered index.html leaks third-party brand(s): {leaks}"


# --------------------------------------------------------------------------- #
# S8 — security: the served chrome carries no emoji                           #
# --------------------------------------------------------------------------- #
def test_s8_rendered_chrome_has_no_emoji() -> None:
    html = _render_index()
    js = JS_FILE.read_text(encoding="utf-8")
    assert emoji_in(html) == (), f"Template carries emoji glyphs: {emoji_in(html)}"
    assert percent_encoded_emoji_in(html) == (), "Template smuggles a percent-encoded emoji (favicon?)"
    assert emoji_in(js) == (), f"JS bundle carries emoji glyphs: {emoji_in(js)}"
    assert percent_encoded_emoji_in(js) == ()


# --------------------------------------------------------------------------- #
# S9 — security: brand predicate is case-insensitive and boundary-aware       #
# --------------------------------------------------------------------------- #
def test_s9_brand_predicate_boundaries() -> None:
    assert "palantir" in disallowed_brands_in("Powered by PALANTIR")
    assert "maltego" in disallowed_brands_in("a maltego-style transform")
    assert disallowed_brands_in("the foundryside novel by Brandon Sanderson") == ()
    assert disallowed_brands_in("") == ()


# --------------------------------------------------------------------------- #
# S10 — config: invalid telemetry config is rejected at construction          #
# --------------------------------------------------------------------------- #
def _valid_kwargs() -> dict[str, object]:
    return {
        "brand": "Estorides",
        "tagline": "State-level OSINT, open source",
        "shortcuts": (KeyboardShortcut("/", "Focus the query box"),),
        "tips": (SplashTip("Query anything", "Enter a domain, IP or email"),),
        "phases": (
            SearchPhase("idle", "Idle", active=False),
            SearchPhase("query", "Querying sources", active=True),
            SearchPhase("done", "Done", active=False),
            SearchPhase("error", "Error", active=False),
        ),
    }


def test_s10_empty_brand_rejected() -> None:
    kwargs = _valid_kwargs()
    kwargs["brand"] = ""
    with pytest.raises(InvalidTelemetryConfigError):
        TelemetryConfig(**kwargs)  # type: ignore[arg-type]


def test_s10_no_tips_rejected() -> None:
    kwargs = _valid_kwargs()
    kwargs["tips"] = ()
    with pytest.raises(InvalidTelemetryConfigError):
        TelemetryConfig(**kwargs)  # type: ignore[arg-type]


def test_s10_duplicate_phase_rejected() -> None:
    kwargs = _valid_kwargs()
    kwargs["phases"] = (
        SearchPhase("idle", "Idle", active=False),
        SearchPhase("query", "Querying sources", active=True),
        SearchPhase("query", "Querying again", active=True),
        SearchPhase("done", "Done", active=False),
        SearchPhase("error", "Error", active=False),
    )
    with pytest.raises(InvalidTelemetryConfigError):
        TelemetryConfig(**kwargs)  # type: ignore[arg-type]


def test_s10_emoji_in_catalog_rejected() -> None:
    kwargs = _valid_kwargs()
    kwargs["tips"] = (SplashTip("Query anything", "Enter a domain \U0001f600"),)
    with pytest.raises(InvalidTelemetryConfigError):
        TelemetryConfig(**kwargs)  # type: ignore[arg-type]


def test_s10_brand_collision_rejected() -> None:
    kwargs = _valid_kwargs()
    kwargs["brand"] = "Palantir"
    with pytest.raises(InvalidTelemetryConfigError):
        TelemetryConfig(**kwargs)  # type: ignore[arg-type]


def test_s10_missing_sentinel_phase_rejected() -> None:
    kwargs = _valid_kwargs()
    kwargs["phases"] = (
        SearchPhase("idle", "Idle", active=False),
        SearchPhase("query", "Querying sources", active=True),
        SearchPhase("done", "Done", active=False),
    )
    with pytest.raises(InvalidTelemetryConfigError):
        TelemetryConfig(**kwargs)  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# S11 — single source of truth: catalog drives the rendered splash            #
# --------------------------------------------------------------------------- #
def test_s11_template_renders_from_catalog() -> None:
    context = SearchTelemetry().context()
    html = _render_index()
    for shortcut in context["shortcuts"]:
        assert shortcut["keys"] in html, f"shortcut {shortcut['keys']!r} missing"
    for tip in context["tips"]:
        assert tip["title"] in html, f"tip {tip['title']!r} missing"
    dt_count = len(re.findall(r"<dt\b", html))
    assert dt_count == len(context["shortcuts"]), (
        "keyboard-shortcut <dt> count must equal the catalog length; a divergent "
        "hardcoded shortcut list is a single-source-of-truth violation"
    )


def test_default_telemetry_is_a_shared_instance() -> None:
    assert isinstance(DEFAULT_TELEMETRY, TelemetryConfig)
    assert "palantir" in DISALLOWED_BRANDS
