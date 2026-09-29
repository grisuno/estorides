"""
estorides_core.openapi
======================
Minimal OpenAPI document generated from the live Flask url map.

I expose paths, methods and auth requirements without new
dependencies and without duplicating the route table by hand.
"""
from __future__ import annotations

from typing import Any


def build_openapi(app: Any) -> dict[str, Any]:
    """Build an OpenAPI 3.0 document from Flask routes."""
    paths: dict[str, Any] = {}
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r.rule)):
        path = str(rule.rule)
        if path.startswith("/static"):
            continue
        methods = sorted(m for m in rule.methods if m in ("GET", "POST", "PUT", "DELETE"))
        if not methods:
            continue
        auth = not path.startswith("/healthz")
        ops: dict[str, Any] = {}
        for method in methods:
            ops[method.lower()] = {
                "summary": f"{method} {path}",
                "security": [{"bearerAuth": []}] if auth else [],
                "responses": {"200": {"description": "ok"}},
            }
        paths[path] = ops
    return {
        "openapi": "3.0.0",
        "info": {"title": "Estorides API", "version": "1.3.0"},
        "components": {"securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer"}}},
        "paths": paths,
    }


__all__ = ["build_openapi"]
