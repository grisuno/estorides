"""M5 RED tests: tools blueprint slice."""
from __future__ import annotations


def test_tools_rules_present() -> None:
    from estorides_web import create_app

    app = create_app()
    rules = {r.rule for r in app.url_map.iter_rules()}
    assert "/api/tools" in rules
    assert "/api/tools/doctor" in rules
    assert "/api/tools/<name>/install" in rules
    assert "/api/tools/<name>/install/status" in rules


def test_blueprint_registered() -> None:
    from estorides_web import create_app

    app = create_app()
    assert "tools" in app.blueprints


def test_unknown_tool_install_reaches_view() -> None:
    from estorides_web import create_app

    app = create_app()
    client = app.test_client()
    r = client.post("/api/tools/no-such-tool-xyz/install", json={})
    assert r.status_code in (401, 404, 429)
    if r.status_code == 404:
        assert "no install recipe" in (r.get_json() or {}).get("error", "")
