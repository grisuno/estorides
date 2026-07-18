"""ATDD + BDD tests for estorides_core.tech_fingerprint.

Implements the Given-When-Then contracts declared in
``spec/tech_fingerprint.md``. Property-based invariants live in
``tests/properties/test_tech_fingerprint_properties.py``.
"""
from __future__ import annotations

from estorides_core.tech_fingerprint import (
    fingerprint,
)


# S1 — Happy path: Detect Nginx + PHP + jQuery from headers + HTML
class TestHappyPathFullStack:
    def test_detects_nginx_php_jquery(self) -> None:
        headers = {
            "Server": "nginx/1.18.0",
            "X-Powered-By": "PHP/7.4.33",
        }
        html = '<script src="jquery-3.6.0.min.js"></script>'
        result = fingerprint(headers, html)
        techs = {t.name: t for t in result.technologies}
        assert techs["nginx"].version == "1.18.0"
        assert techs["PHP"].version == "7.4.33"
        assert techs["jQuery"].version == "3.6.0"
        assert result.confidence > 0.7


# S2 — Edge case: Empty response
class TestEmptyResponse:
    def test_returns_empty_on_no_input(self) -> None:
        result = fingerprint({}, "")
        assert len(result.technologies) == 0
        assert result.confidence == 0.0


# S3 — Error case: Malformed version string
class TestMalformedVersion:
    def test_handles_binary_garbage_in_version(self) -> None:
        headers = {"Server": "nginx\x00\x00\x00"}
        result = fingerprint(headers, "")
        techs = {t.name: t for t in result.technologies}
        assert "nginx" in techs
        assert techs["nginx"].version is None


# S4 — Security: No script injection as version
class TestNoScriptInjection:
    def test_does_not_parse_script_as_tech(self) -> None:
        html = '<script>alert("jQuery-1.0.0")</script>'
        result = fingerprint({}, html)
        techs = {t.name: t for t in result.technologies}
        assert "jQuery" not in techs


# S5 — Happy path: WAF detection via headers
class TestWafDetection:
    def test_detects_cloudflare_from_headers(self) -> None:
        headers = {"cf-ray": "abc123", "cf-cache-status": "HIT"}
        result = fingerprint(headers, "")
        techs = {t.name: t for t in result.technologies}
        assert "Cloudflare" in techs
        assert techs["Cloudflare"].category == "cdn"
        assert techs["Cloudflare"].confidence > 0.8


# S6 — Happy path: CMS detection from HTML meta
class TestCmsDetection:
    def test_detects_wordpress_from_meta(self) -> None:
        html = '<meta name="generator" content="WordPress 6.2" />'
        result = fingerprint({}, html)
        techs = {t.name: t for t in result.technologies}
        assert "WordPress" in techs
        assert techs["WordPress"].category == "cms"
        assert techs["WordPress"].version == "6.2"


# S7 — Edge: Deduplication
class TestDeduplication:
    def test_same_tech_from_multiple_signals_appears_once(self) -> None:
        headers = {"Server": "nginx/1.18.0"}
        cookies = ["nginx_sticky_session=abc"]
        result = fingerprint(headers, "", cookies=cookies)
        nginx_matches = [t for t in result.technologies if t.name == "nginx"]
        assert len(nginx_matches) == 1


# S8 — Security: Input size bounded
class TestInputSizeBound:
    def test_only_processes_first_100kb(self) -> None:
        headers = {"Server": "nginx/1.18.0"}
        html = "a" * 200000 + '<meta name="generator" content="WordPress 6.2" />'
        result = fingerprint(headers, html)
        techs = {t.name: t for t in result.technologies}
        assert "nginx" in techs
        assert "WordPress" not in techs
