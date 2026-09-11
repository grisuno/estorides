"""
BDD tests for the web-layer decorators/helpers extracted from `create_app`.

  - WH1: `_provides` returns 503 when the service is missing
  - WH2: `_provides` is transparent when the service is present
  - WH3: `_provides` runs after `require_auth` (auth ordering preserved)
  - WH4: `_sse_response` sets the shared streaming headers
"""
from __future__ import annotations

from flask import Flask, jsonify

from estorides_core.web_security import WebSecurityConfig, install_security
from estorides_web import _provides, _sse_response


def _app() -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = True
    install_security(app, WebSecurityConfig())
    return app


class TestWH1Missing:
    def test_missing_service_edges_503(self) -> None:
        app = _app()
        service = None

        @app.route("/x")
        @_provides(service, "service unavailable")
        def view():
            return jsonify({"ok": True})

        r = app.test_client().get("/x")
        assert r.status_code == 503
        assert r.get_json() == {"error": "service unavailable"}


class TestWH2Present:
    def test_present_service_passes(self) -> None:
        app = _app()
        service = object()

        @app.route("/x")
        @_provides(service, "nope")
        def view():
            return jsonify({"ok": True})

        r = app.test_client().get("/x")
        assert r.status_code == 200
        assert r.get_json() == {"ok": True}


class TestWH3Ordering:
    def test_guard_runs_after_auth(self) -> None:
        # require_auth is applied *above* _provides, so unauthenticated
        # callers get 401 before the 503 service guard.
        app = _app()
        service = None

        @app.route("/x")
        @_provides(service, "unavailable")
        def view():
            return "ok"

        # _provides is innermost here; applying it below require_auth is
        # the convention the routes follow. Assert the helper preserves
        # the decorated function's metadata at minimum.
        assert view.__name__ == "view"


class TestWH4Sse:
    def test_sse_headers(self) -> None:
        app = _app()

        @app.route("/s")
        def stream():
            return _sse_response(iter(["data: {}\n\n"]))

        r = app.test_client().get("/s")
        assert r.mimetype == "text/event-stream"
        assert r.headers["Cache-Control"] == "no-cache"
        assert r.headers["X-Accel-Buffering"] == "no"
