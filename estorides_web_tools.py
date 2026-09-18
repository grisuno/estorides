"""
estorides_web_tools
===================
Tools vertical slice extracted from the ``create_app`` God factory.

Owns the install-state registry and the four ``/api/tools*`` routes
with identical URLs, auth, rate-limit events and behaviours. The
factory registers :data:`tools_bp`; no tools view logic stays inline.

Import cycle note: this module is imported lazily inside
``create_app`` (call time, after ``estorides_web`` is fully loaded),
so top-level imports of the factory helpers are safe.
"""
from __future__ import annotations

import logging
import threading
from typing import Any

from flask import Blueprint, jsonify, request

from estorides_core.audit import audit_log
from estorides_core.tool_install import (
    doctor,
    install_tool,
    list_recipes,
    recipe_available,
    tool_available,
)
from estorides_core.web_security import require_auth
from estorides_web import (
    _client_ip,
    _rate_limit_decorator,
)

log = logging.getLogger("estorides.web")

tools_bp = Blueprint("tools", __name__)

_tool_install_state: dict[str, dict[str, Any]] = {}
_tool_install_lock = threading.Lock()


@tools_bp.route("/api/tools")
@_rate_limit_decorator(event="api_tools_list")
@require_auth
def api_tools_list() -> Any:
    recipes = list_recipes()
    with _tool_install_lock:
        states = dict(_tool_install_state)
    return jsonify({
        "recipes": [
            {
                "name": r,
                "available": tool_available(r),
                "install": states.get(r),
            }
            for r in recipes
        ],
    })


@tools_bp.route("/api/tools/doctor")
@_rate_limit_decorator(event="api_tools_doctor")
@require_auth
def api_tools_doctor() -> Any:
    return jsonify(doctor())


@tools_bp.route("/api/tools/<name>/install", methods=["POST"])
@_rate_limit_decorator(event="api_tool_install")
@require_auth
def api_tool_install(name: str) -> Any:
    if not recipe_available(name):
        return jsonify({"error": f"no install recipe for '{name}'"}), 404
    body = request.get_json(silent=True) or {}
    binary = body.get("binary") or name
    force = bool(body.get("force", False))
    with _tool_install_lock:
        current = _tool_install_state.get(name)
        if current and current.get("running"):
            return jsonify({"status": "running"}), 202
        _tool_install_state[name] = {"running": True, "result": None}

    def _worker() -> None:
        result = None
        try:
            result = install_tool(name, binary=binary, force=force)
        except Exception:
            log.exception("tool install %s raised", name)
        with _tool_install_lock:
            _tool_install_state[name] = {
                "running": False,
                "result": result.to_dict() if result is not None else {
                    "tool_name": name, "success": False, "method": None,
                    # CWE-209: never echo the raw exception to the client.
                    "output": "", "error": "install raised; see server logs",
                },
            }

    threading.Thread(
        target=_worker, daemon=True, name=f"estorides-install-{name}"
    ).start()
    audit_log.query(
        "api_tool_install", remote_ip=_client_ip(), method=request.method,
        path=request.path, query=binary, status="started",
    )
    return jsonify({"status": "started", "tool": name})


@tools_bp.route("/api/tools/<name>/install/status")
@_rate_limit_decorator(event="api_tool_install_status")
@require_auth
def api_tool_install_status(name: str) -> Any:
    with _tool_install_lock:
        state = _tool_install_state.get(name)
    if state is None:
        return jsonify({"status": "idle"})
    return jsonify(state)
