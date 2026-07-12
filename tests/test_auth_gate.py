"""Auth gate: bearer-token protection for sensitive /api/* routes.

When `ESTORIDES_AUTH_TOKEN` is set, the gate is on: anonymous callers get
401, callers with the right bearer token get through. When unset, the
gate is off and every call passes through (local-trust single-user mode).
"""
from __future__ import annotations

import pytest
from flask import Flask

from estorides_core.web_security import (
    AUTH_COOKIE,
    AUTH_HEADER_ALT,
    install_auth_gate,
    make_auth_gate,
    require_auth,
)


@pytest.fixture
def app_with_gate(monkeypatch):
    """A Flask app with the auth gate enabled, token 'sek'.

    Each test gets a fresh app so the module-level _GATE slot is clean.
    """
    monkeypatch.setenv("ESTORIDES_AUTH_TOKEN", "sek")
    app = Flask(__name__)
    gate = make_auth_gate()
    install_auth_gate(app, gate)

    @app.route("/api/private")
    @require_auth
    def private():
        from flask import jsonify
        return jsonify({"ok": True})

    return app


def test_gate_auto_generates_token_when_unset(monkeypatch):
    monkeypatch.delenv("ESTORIDES_AUTH_TOKEN", raising=False)
    g = make_auth_gate()
    assert g.enabled is True
    # Token should be a 64-char hex string
    token = g.auth_meta_for_index()
    assert token is not None
    assert len(token) == 64
    import re
    assert re.match(r'^[a-f0-9]{64}$', token) is not None


def test_gate_on_rejects_anonymous(app_with_gate):
    c = app_with_gate.test_client()
    r = c.get("/api/private")
    assert r.status_code == 401
    assert r.get_json() == {"error": "unauthorized"}
    assert r.headers.get("WWW-Authenticate", "").startswith("Bearer")


def test_gate_on_accepts_bearer_header(app_with_gate):
    c = app_with_gate.test_client()
    r = c.get("/api/private", headers={"Authorization": "Bearer sek"})
    assert r.status_code == 200
    assert r.get_json() == {"ok": True}


def test_gate_on_accepts_alt_header(app_with_gate):
    c = app_with_gate.test_client()
    r = c.get("/api/private", headers={AUTH_HEADER_ALT: "sek"})
    assert r.status_code == 200


def test_gate_on_accepts_cookie(app_with_gate):
    c = app_with_gate.test_client()
    c.set_cookie(AUTH_COOKIE, "sek")
    r = c.get("/api/private")
    assert r.status_code == 200


def test_gate_on_rejects_wrong_token(app_with_gate):
    c = app_with_gate.test_client()
    r = c.get("/api/private", headers={"Authorization": "Bearer wrong"})
    assert r.status_code == 401


def test_gate_on_auto_generated_token_in_meta(monkeypatch):
    monkeypatch.delenv("ESTORIDES_AUTH_TOKEN", raising=False)
    g = make_auth_gate()
    token = g.auth_meta_for_index()
    assert token is not None
    assert len(token) == 64


def test_gate_on_exposes_token_for_index_meta():
    g = make_auth_gate.__wrapped__ if hasattr(make_auth_gate, "__wrapped__") else make_auth_gate
    # Construction with a token via env-less path is impossible; we test
    # directly that auth_meta_for_index returns the configured token.
    from estorides_core.web_security import AuthGate
    g = AuthGate(required_token="sek")
    assert g.auth_meta_for_index() == "sek"
