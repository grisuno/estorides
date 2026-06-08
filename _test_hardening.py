#!/usr/bin/env python3
"""Offline tests for the v1.3 hardening + report + diff surface.

Run via `_validate.py` (the project's offline test runner). No network.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Isolate the case DB so the test never touches the user's data.
_TMP = tempfile.mkdtemp(prefix="estorides_test_")
os.environ["ESTORIDES_CASES_DB"] = str(Path(_TMP) / "cases.sqlite")
os.environ["ESTORIDES_DATA_DIR"] = _TMP
os.environ.setdefault("ESTORIDES_CORS_ORIGINS", "")

FAIL = 0


def _ok(name: str, ok: bool, detail: str = "") -> None:
    global FAIL
    mark = "OK  " if ok else "FAIL"
    print(f"  [{mark}] {name}{(': ' + detail) if detail else ''}")
    if not ok:
        FAIL += 1


# ---------------------------------------------------------------------------
# Web security
# ---------------------------------------------------------------------------
def test_security_headers() -> None:
    from wsgi import app  # noqa: F401 — forces config + env to resolve first
    with app.test_client() as c:
        r = c.get("/api/status")
        _ok("CSP set", bool(r.headers.get("Content-Security-Policy")))
        _ok("X-Frame-Options DENY", r.headers.get("X-Frame-Options") == "DENY")
        _ok("X-Content-Type-Options nosniff",
            r.headers.get("X-Content-Type-Options") == "nosniff")
        _ok("Referrer-Policy no-referrer",
            r.headers.get("Referrer-Policy") == "no-referrer")
        _ok("Permissions-Policy restricts sensors",
            "geolocation=()" in (r.headers.get("Permissions-Policy") or ""))
        _ok("debug is off", app.debug is False)
        _ok("MAX_CONTENT_LENGTH is 1 MiB",
            app.config.get("MAX_CONTENT_LENGTH") == 1_048_576)


def test_cors_default_off() -> None:
    """Without ESTORIDES_CORS_ORIGINS, CORS headers must not be emitted."""
    from wsgi import app
    with app.test_client() as c:
        r = c.get("/api/status", headers={"Origin": "https://evil.example.com"})
        _ok("no CORS header when allowlist empty",
            "Access-Control-Allow-Origin" not in r.headers)


def test_cors_allowlist() -> None:
    """With an allowlist, only matching origins get a CORS header."""
    os.environ["ESTORIDES_CORS_ORIGINS"] = "https://app.example.com"
    # Reload config — env was set after the app was already created.
    from importlib import reload
    from estorides_core import web_security
    reload(web_security)
    from wsgi import create_app  # noqa: F401
    # We can't simply reimport `wsgi` because it caches `app`. Build a
    # fresh app and re-install security.
    from flask import Flask
    test_app = Flask(__name__)
    test_app.config["DEBUG"] = False
    web_security.install_security(test_app)
    with test_app.test_client() as c:
        r = c.get("/", headers={"Origin": "https://app.example.com"})
        _ok("CORS header on allowlisted origin",
            r.headers.get("Access-Control-Allow-Origin") == "https://app.example.com")
        r = c.get("/", headers={"Origin": "https://evil.example.com"})
        _ok("CORS header absent on rogue origin",
            "Access-Control-Allow-Origin" not in r.headers)
    # Reset for downstream tests.
    os.environ["ESTORIDES_CORS_ORIGINS"] = ""


def test_debug_killswitch() -> None:
    """When DEBUG is on, install_security must refuse to run."""
    from flask import Flask
    from estorides_core import web_security
    test_app = Flask(__name__)
    test_app.config["DEBUG"] = True
    raised = False
    try:
        web_security.install_security(test_app)
    except RuntimeError:
        raised = True
    _ok("debug killswitch raises RuntimeError", raised)


def test_max_body_rejection() -> None:
    """A request body larger than MAX_CONTENT_LENGTH must be rejected."""
    from wsgi import app
    with app.test_client() as c:
        huge = b"x" * (2 * 1_048_576)  # 2 MiB > 1 MiB cap
        r = c.post("/api/run", data=huge, content_type="application/octet-stream")
        _ok("oversize body rejected (413)", r.status_code in (413, 400))


# ---------------------------------------------------------------------------
# Case diff
# ---------------------------------------------------------------------------
def test_case_diff() -> None:
    from estorides_core.cases import store as case_store
    a = case_store.create_case(query="example.com", query_type="domain", notes="baseline")
    b = case_store.create_case(query="example.com", query_type="domain", notes="newer")
    case_store.add_entities(a, [
        {"type": "domain", "value": "example.com", "source": "x", "confidence": 0.9},
        {"type": "ipv4", "value": "1.1.1.1", "source": "x", "confidence": 0.9},
    ])
    case_store.add_entities(b, [
        {"type": "domain", "value": "example.com", "source": "x", "confidence": 0.9},
        {"type": "domain", "value": "new.example.com", "source": "x", "confidence": 0.9},
        {"type": "ipv4", "value": "2.2.2.2", "source": "x", "confidence": 0.9},
    ])
    diff = case_store.diff_entities(a, b)
    _ok("diff added_count == 2", diff["added_count"] == 2)
    _ok("diff common_count == 1", diff["common_count"] == 1)
    # 1.1.1.1 was in `a` but not in `b` (replaced by 2.2.2.2), so it shows
    # up in the removed set — that is the OSINT "what disappeared" signal.
    _ok("diff removed_count == 1", diff["removed_count"] == 1)
    added_values = sorted(e["value"] for e in diff["added"])
    _ok("added includes new.example.com", "new.example.com" in added_values)
    _ok("added includes 2.2.2.2", "2.2.2.2" in added_values)


def test_case_diff_endpoints() -> None:
    from wsgi import app
    with app.test_client() as c:
        r = c.get("/api/cases/diff")
        _ok("diff without args -> 400", r.status_code == 400)
        r = c.get("/api/cases/diff?a=x&b=x")
        _ok("diff same id -> 400", r.status_code == 400)
        r = c.get("/api/cases/diff?a=nope&b=nope2")
        _ok("diff unknown -> 404", r.status_code == 404)


def test_case_save_endpoint() -> None:
    from estorides_core.cases import store as case_store
    from wsgi import app
    case_id = case_store.create_case(query="save-test.example", query_type="domain")
    with app.test_client() as c:
        r = c.post(f"/api/cases/{case_id}/save", json={"note": "important"})
        _ok("save ok", r.status_code == 200)
        # Re-fetch and confirm the notes prefix
        row = case_store.get_case(case_id)
        _ok("notes updated", "[saved]" in (row.get("notes") or ""))
        r = c.post("/api/cases/nonexistent/save", json={})
        _ok("save unknown case -> 404", r.status_code == 404)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def test_report_renders() -> None:
    from estorides_export.report import render_markdown_report
    case = {
        "id": "c1", "query": "x.com", "query_type": "domain",
        "status": "ok", "created_at": 1730000000.0,
        "entity_count": 1, "obs_count": 1, "notes": "",
    }
    md = render_markdown_report(
        case, entities=[{"type": "domain", "value": "x.com"}],
        sources_queried=5, sources_succeeded=3,
    )
    _ok("title present", "x.com" in md and "# " in md)
    _ok("IOCs section present", "## IOCs" in md)
    _ok("TL;DR present", "## TL;DR" in md)


def test_report_with_diff() -> None:
    from estorides_export.report import render_markdown_report
    case = {"id": "c2", "query": "y.com", "query_type": "domain",
            "status": "ok", "created_at": 1.0, "entity_count": 0, "obs_count": 0}
    diff = {"case_a": "a", "case_b": "c2", "added": [{"type": "ipv4", "value": "9.9.9.9"}],
            "removed": [], "common_count": 0, "added_count": 1, "removed_count": 0,
            "by_type": {"added": {"ipv4": 1}, "removed": {}}}
    md = render_markdown_report(case, entities=[], diff=diff)
    _ok("diff section rendered", "## Diff vs previous run" in md)
    _ok("sample of new entities present", "9.9.9.9" in md)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def test_console_script_help() -> None:
    """`./estorides` must run even without `pip install -e .`."""
    import subprocess
    res = subprocess.run(
        [str(HERE / "estorides"), "--help"],
        capture_output=True, text=True, timeout=10,
    )
    _ok("entry-point exit 0", res.returncode == 0)
    _ok("entry-point shows subcommands", "report" in res.stdout and "diff" in res.stdout)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def main() -> int:
    tests = [
        test_security_headers,
        test_cors_default_off,
        test_cors_allowlist,
        test_debug_killswitch,
        test_max_body_rejection,
        test_case_diff,
        test_case_diff_endpoints,
        test_case_save_endpoint,
        test_report_renders,
        test_report_with_diff,
        test_console_script_help,
    ]
    for t in tests:
        print(f"\n--- {t.__name__} ---")
        try:
            t()
        except Exception as e:  # noqa: BLE001
            global FAIL
            FAIL += 1
            print(f"  [FAIL] {t.__name__} raised: {e!r}")
    print(f"\n{'=' * 60}\nfailures: {FAIL}\n{'=' * 60}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
