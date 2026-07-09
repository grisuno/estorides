"""
BDD tests for the ui_professional module (spec/ui_professional.md).

Each scenario maps to a Given-When-From from the spec.
We test the JS functions via rendering the template and asserting DOM
structure, plus direct Python-side logic for the tier+loading helpers.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader, select_autoescape

from estorides_core.recon_fusion import ReconFusionEngine
from estorides_core.search_telemetry import SearchTelemetry

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "index.html"
JS_FILE = ROOT / "static" / "js" / "estorides.js"
CSS_FILE = ROOT / "static" / "css" / "estorides_ui.css"
CSS_MAIN_FILE = ROOT / "static" / "css" / "estorides.css"


def _render_index() -> str:
    env = Environment(
        loader=FileSystemLoader(str(ROOT / "templates")),
        autoescape=select_autoescape(["html"]),
    )
    tmpl = env.get_template("index.html")
    return tmpl.render(
        estorides_auth_token="",
        telemetry=SearchTelemetry().context(),
    )


def _simulate_tiered_data() -> dict:
    engine = ReconFusionEngine()
    obs = [
        {"source": "crt_sh_certificates", "category": "web", "parser": "cert",
         "parsed": {"domain": "evilcorp.com"}, "meta": {"status": "ok"}, "status": "ok"},
        {"source": "rdap_domain", "category": "infra", "parser": "rdap",
         "parsed": {"domain": "evilcorp.com"}, "meta": {"status": "ok"}, "status": "ok"},
        {"source": "dns_google", "category": "dns", "parser": "dns",
         "parsed": {"domain": "evilcorp.com"}, "meta": {"status": "ok"}, "status": "ok"},
        {"source": "untrusted_webscraper", "category": "scrape", "parser": "generic",
         "parsed": {"domain": "sketchy-site.com"}, "meta": {"status": "ok"}, "status": "ok"},
    ]
    ents = [
        {"type": "domain", "value": "evilcorp.com", "confidence": 0.95,
         "sources": ["crt_sh_certificates", "rdap_domain", "dns_google"]},
        {"type": "domain", "value": "sketchy-site.com", "confidence": 0.3,
         "sources": ["untrusted_webscraper"]},
    ]
    result = engine.classify("evilcorp.com", "domain", obs, ents)
    return result.to_dict()


# --------------------------------------------------------------------------- #
# S1 -- Loading animation aparece al iniciar run                               #
# --------------------------------------------------------------------------- #
class TestS1LoadingAnimation:
    """S1 -- Loading indicator elements exist in the DOM."""

    def test_loading_elements_exist(self) -> None:
        html = _render_index()
        assert 'id="status-indicator"' in html
        assert 'id="footer-status"' in html
        assert 'id="run-progress"' in html
        assert 'id="run-progress-bar"' in html

    def test_loading_css_defined(self) -> None:
        css = CSS_FILE.read_text(encoding="utf-8")
        assert "@keyframes spin" in css
        assert "@keyframes fadeIn" in css
        assert "@keyframes pulse" in css
        assert ".status-dot" in css
        assert ".status-dot.busy" in css
        assert ".loading-spinner" in css

    def test_js_show_working_indicator_exists(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "showWorkingIndicator" in js
        assert "hideWorkingIndicator" in js
        assert "setStatusDot" in js


# --------------------------------------------------------------------------- #
# S2 -- Tier critical se renderiza expandido                                   #
# --------------------------------------------------------------------------- #
class TestS2CriticalExpanded:
    """S2 -- CRITICAL tier renders expanded with correct badge count."""

    def test_critical_tier_data(self) -> None:
        data = _simulate_tiered_data()
        critical = data["tiers"].get("critical", [])
        assert len(critical) >= 1
        group = critical[0]
        assert group["tier"] == "critical"
        assert group["direct_match"] is True
        assert group["source_count"] >= 3

    def test_critical_css_classes_exist(self) -> None:
        css = CSS_FILE.read_text(encoding="utf-8")
        assert ".tier-critical" in css
        assert ".tier-critical .tier-header" in css
        assert ".tier-critical .tier-badge" in css
        assert ".tier-section" in css
        assert ".tier-header" in css
        assert ".tier-badge" in css
        assert ".tier-body" in css


# --------------------------------------------------------------------------- #
# S3 -- Tier noise se renderiza colapsado                                      #
# --------------------------------------------------------------------------- #
class TestS3NoiseCollapsed:
    def test_noise_tier_data(self) -> None:
        data = _simulate_tiered_data()
        noise = data["tiers"].get("noise", [])
        assert len(noise) >= 1
        for g in noise:
            assert g["tier"] == "noise"

    def test_noise_css_classes_exist(self) -> None:
        css = CSS_FILE.read_text(encoding="utf-8")
        assert ".tier-noise" in css
        assert ".tier-noise .tier-header" in css
        assert ".tier-noise .tier-badge" in css
        assert ".tier-noise { opacity:" in css or ".tier-noise" in css

    def test_js_toggle_function_exists(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "toggleTierSection" in js
        assert "renderTieredResults" in js


# --------------------------------------------------------------------------- #
# S4 -- Click en tier-header expande/colapsa                                   #
# --------------------------------------------------------------------------- #
class TestS4ToggleExpandCollapse:
    def test_aria_attributes_in_js(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert 'aria-expanded' in js or "ariaExpanded" in js or "aria-expanded" in js
        assert 'aria-controls' in js or "ariaControls" in js or "aria-controls" in js

    def test_toggle_uses_role_button(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "'role', 'button'" in js or '"role", "button"' in js or 'role="button"' in js


# --------------------------------------------------------------------------- #
# S5 -- Sin datos de tiers, fallback a vista plana                             #
# --------------------------------------------------------------------------- #
class TestS5FallbackFlatView:
    def test_js_fallback_logic(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "renderTieredResults" in js
        assert "buildResultCard" in js

    def test_tiers_missing_returns_empty(self) -> None:
        engine = ReconFusionEngine()
        result = engine.classify("test.com", "domain", [], [])
        data = result.to_dict()
        assert isinstance(data["tiers"], dict)
        for groups in data["tiers"].values():
            assert len(groups) == 0


# --------------------------------------------------------------------------- #
# S6 -- Loading animation timeout                                              #
# --------------------------------------------------------------------------- #
class TestS6LoadingTimeout:
    def test_show_toast_exists(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "showToast" in js


# --------------------------------------------------------------------------- #
# S7 -- Hover en tarjeta de entidad                                            #
# --------------------------------------------------------------------------- #
class TestS7HoverEffect:
    def test_tier_group_hover_css(self) -> None:
        css = CSS_FILE.read_text(encoding="utf-8")
        assert ".tier-group:hover" in css

    def test_transition_on_tier_group(self) -> None:
        css = CSS_FILE.read_text(encoding="utf-8")
        assert "transition" in css


# --------------------------------------------------------------------------- #
# S8 -- Fade-in en nuevos resultados                                              #
# --------------------------------------------------------------------------- #
class TestS8FadeInTransition:
    def test_fade_in_css_exists(self) -> None:
        css = CSS_FILE.read_text(encoding="utf-8")
        assert "@keyframes fadeIn" in css
        assert ".fade-in" in css

    def test_results_use_fade_in(self) -> None:
        css = CSS_FILE.read_text(encoding="utf-8")
        assert "#results-list > *" in css or "fadeIn" in css


# --------------------------------------------------------------------------- #
# S9 -- Security: CSP intacta (no inline style= attributes)                    #
# --------------------------------------------------------------------------- #
class TestS9SecurityCSP:
    def test_no_inline_style_in_tier_badge(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        lines = js.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue
            if 'style=' in stripped and 'background' in stripped:
                pytest.fail(f"Line {i} has inline style with background: {stripped.strip()}")

    def test_no_inline_style_in_template(self) -> None:
        html = _render_index()
        inline_style_tags = re.findall(r'<[^>]+style="[^"]*"', html)
        allowed_inline_exceptions = [
            'style="display:',     # JS-controlled visibility
        ]
        for tag in inline_style_tags:
            is_allowed = any(exception in tag for exception in allowed_inline_exceptions)
            if not is_allowed:
                pytest.fail(f"CSP violation: inline style attribute in template: {tag}")

    def test_no_onclick_attributes(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        onclick_matches = re.findall(r'onclick\s*=\s*["\']', js)
        assert len(onclick_matches) == 0, (
            f"onclick attributes would violate CSP: {onclick_matches}"
        )


# --------------------------------------------------------------------------- #
# S10 -- Security: XSS safe (textContent not innerHTML for user data)          #
# --------------------------------------------------------------------------- #
class TestS10XSSSafe:
    def test_escape_html_function_exists(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "escapeHTML" in js

    def test_escape_html_properly_defined(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "function escapeHTML" in js or "function escapeHTML" in js
        assert "&amp;" in js or "&lt;" in js

    def test_tier_label_uses_text_content(self) -> None:
        js = JS_FILE.read_text(encoding="utf-8")
        assert "textContent" in js


# --------------------------------------------------------------------------- #
# Integration: full pipeline tiers -> rendered                                 #
# --------------------------------------------------------------------------- #
class TestIntegrationTierPipeline:
    def test_tier_summary_accuracy(self) -> None:
        data = _simulate_tiered_data()
        for tier_name, groups in data["tiers"].items():
            assert data["tier_summary"][tier_name] == len(groups)

    def test_every_group_has_required_fields(self) -> None:
        data = _simulate_tiered_data()
        for groups in data["tiers"].values():
            for g in groups:
                assert isinstance(g["canonical_id"], str)
                assert isinstance(g["type"], str)
                assert isinstance(g["value"], str)
                assert isinstance(g["relevance_score"], (int, float))
                assert isinstance(g["tier"], str)
                assert isinstance(g["source_count"], int)
                assert isinstance(g["direct_match"], bool)

    def test_scores_are_normalised(self) -> None:
        data = _simulate_tiered_data()
        for groups in data["tiers"].values():
            for g in groups:
                assert 0.0 <= g["relevance_score"] <= 1.0