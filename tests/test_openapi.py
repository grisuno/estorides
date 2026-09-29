"""OpenAPI BDD."""
from __future__ import annotations


def test_openapi_lists_healthz_without_auth_and_run_with_auth():
    import estorides_web

    app = estorides_web.create_app()
    c = app.test_client()
    gate = app.extensions.get("estorides_auth")
    token = gate.required_token if gate is not None else None
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = c.get("/api/openapi.json", headers=headers)
    assert r.status_code == 200
    doc = r.get_json()
    assert doc["openapi"] == "3.0.0"
    assert "/healthz" in doc["paths"]
    assert doc["paths"]["/healthz"]["get"]["security"] == []
    assert "/api/run" in doc["paths"]
