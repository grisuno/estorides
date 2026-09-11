"""
BDD tests for the v1.3 hardening surface, case diff and report.

Ported from the standalone ``_test_hardening.py`` validator into pytest so
CI runs it. Offline.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from flask import Flask

from estorides_core.cases import CaseStore
from estorides_core.web_security import WebSecurityConfig, install_security
from estorides_export.report import render_markdown_report

ROOT = Path(__file__).resolve().parent.parent


def _secured_app(cfg: WebSecurityConfig | None = None) -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = False
    install_security(app, cfg or WebSecurityConfig())

    @app.route("/api/status")
    def status():
        return {"ok": True}

    return app


class TestSecurityHeaders:
    def test_headers_and_body_cap(self) -> None:
        app = _secured_app()
        r = app.test_client().get("/api/status")
        assert r.headers.get("Content-Security-Policy")
        assert r.headers.get("X-Frame-Options") == "DENY"
        assert r.headers.get("X-Content-Type-Options") == "nosniff"
        assert r.headers.get("Referrer-Policy") == "no-referrer"
        assert "geolocation=()" in (r.headers.get("Permissions-Policy") or "")
        assert app.debug is False
        assert app.config.get("MAX_CONTENT_LENGTH") == 16 * 1024 * 1024


class TestCors:
    def test_default_off(self) -> None:
        app = _secured_app()
        r = app.test_client().get("/api/status", headers={"Origin": "https://evil.example.com"})
        assert "Access-Control-Allow-Origin" not in r.headers

    def test_allowlist(self) -> None:
        cfg = WebSecurityConfig(allow_origins=("https://app.example.com",))
        app = _secured_app(cfg)
        client = app.test_client()
        ok = client.get("/api/status", headers={"Origin": "https://app.example.com"})
        assert ok.headers.get("Access-Control-Allow-Origin") == "https://app.example.com"
        rogue = client.get("/api/status", headers={"Origin": "https://evil.example.com"})
        assert "Access-Control-Allow-Origin" not in rogue.headers


class TestDebugKillswitch:
    def test_debug_raises(self) -> None:
        app = Flask(__name__)
        app.config["DEBUG"] = True
        with pytest.raises(RuntimeError):
            install_security(app)


class TestCaseDiff:
    def test_diff_counts(self, tmp_path: Path) -> None:
        store = CaseStore(tmp_path / "cases.sqlite")
        try:
            a = store.create_case(query="example.com", query_type="domain", notes="baseline")
            b = store.create_case(query="example.com", query_type="domain", notes="newer")
            store.add_entities(a, [
                {"type": "domain", "value": "example.com", "source": "x", "confidence": 0.9},
                {"type": "ipv4", "value": "1.1.1.1", "source": "x", "confidence": 0.9},
            ])
            store.add_entities(b, [
                {"type": "domain", "value": "example.com", "source": "x", "confidence": 0.9},
                {"type": "domain", "value": "new.example.com", "source": "x", "confidence": 0.9},
                {"type": "ipv4", "value": "2.2.2.2", "source": "x", "confidence": 0.9},
            ])
            diff = store.diff_entities(a, b)
            assert diff["added_count"] == 2
            assert diff["common_count"] == 1
            assert diff["removed_count"] == 1
            added = sorted(e["value"] for e in diff["added"])
            assert "new.example.com" in added
            assert "2.2.2.2" in added
        finally:
            store.close()

    def test_set_notes(self, tmp_path: Path) -> None:
        store = CaseStore(tmp_path / "cases2.sqlite")
        try:
            cid = store.create_case(query="save-test.example", query_type="domain")
            store.set_notes(cid, "[saved] important")
            assert "[saved]" in (store.get_case(cid).get("notes") or "")
        finally:
            store.close()


class TestReport:
    def test_renders_sections(self) -> None:
        case = {
            "id": "c1", "query": "x.com", "query_type": "domain",
            "status": "ok", "created_at": 1730000000.0,
            "entity_count": 1, "obs_count": 1, "notes": "",
        }
        md = render_markdown_report(
            case, entities=[{"type": "domain", "value": "x.com"}],
            sources_queried=5, sources_succeeded=3,
        )
        assert "x.com" in md and "# " in md
        assert "## IOCs" in md
        assert "## TL;DR" in md

    def test_with_diff(self) -> None:
        case = {"id": "c2", "query": "y.com", "query_type": "domain",
                "status": "ok", "created_at": 1.0, "entity_count": 0, "obs_count": 0}
        diff = {
            "case_a": "a", "case_b": "c2",
            "added": [{"type": "ipv4", "value": "9.9.9.9"}],
            "removed": [], "common_count": 0,
            "added_count": 1, "removed_count": 0,
            "by_type": {"added": {"ipv4": 1}, "removed": {}},
        }
        md = render_markdown_report(case, entities=[], diff=diff)
        assert "## Diff vs previous run" in md
        assert "9.9.9.9" in md


class TestConsoleScript:
    def test_help(self) -> None:
        res = subprocess.run(  # noqa: S603 - trusted interpreter, test-owned args
            [sys.executable, str(ROOT / "estorides_cli.py"), "--help"],
            capture_output=True, text=True, timeout=30, cwd=str(ROOT),
        )
        assert res.returncode == 0
        assert "report" in res.stdout and "diff" in res.stdout
