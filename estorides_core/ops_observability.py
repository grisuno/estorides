"""
estorides_core.ops_observability
================================
Single user operational visibility without external dependencies.

I provide unauthenticated liveness, authenticated readiness and
Prometheus text metrics plus an opt in JSON log formatter. I keep
all counters in process behind a lock so threaded Flask workers
cannot corrupt them. I sanitize every label so a hostile source
name cannot inject newlines into the scrape output.
"""
from __future__ import annotations

import json
import re
import threading
import time
from dataclasses import dataclass
from typing import Any

from .config import PROJECT_ROOT

_LABEL_BAD_RE = re.compile(r"[^a-zA-Z0-9_/:.\-]")
_MAX_LABEL_LEN = 200


@dataclass(frozen=True)
class OpsConfig:
    """Centralized bounds for observability output."""

    app_version: str = "1.3.0"
    max_label_len: int = _MAX_LABEL_LEN
    metrics_content_type: str = "text/plain; version=0.0.4"


OPS = OpsConfig()

_requests: dict[tuple[str, str], int] = {}
_source_errors: dict[str, int] = {}
_lock = threading.Lock()


def _clean_label(value: str) -> str:
    """Return a Prometheus safe label fragment without newlines."""
    cleaned = _LABEL_BAD_RE.sub("_", value or "other")
    cleaned = cleaned.replace("\n", "_").replace("\r", "_")
    return cleaned[: OPS.max_label_len] or "other"


def health_payload() -> tuple[dict[str, str], int]:
    """Return liveness body and status code."""
    return {"status": "ok", "version": OPS.app_version}, 200


def ready_payload(source_count: int, sources_dir_ok: bool) -> tuple[dict[str, Any], int]:
    """Return readiness body and status code for registry state."""
    ready = bool(sources_dir_ok and source_count > 0)
    code = 200 if ready else 503
    return {"ready": ready, "sources": int(source_count)}, code


def record_request(endpoint: str, status: str) -> None:
    """Count one HTTP response by normalized endpoint and status."""
    ep = endpoint if endpoint.startswith("/") else "other"
    ep = _clean_label(ep)
    st = _clean_label(str(status))
    with _lock:
        key = (ep, st)
        _requests[key] = _requests.get(key, 0) + 1


def record_source(source: str, ok: bool) -> None:
    """Count one source execution failure when ok is False."""
    if not source:
        return
    if ok:
        return
    name = _clean_label(source)
    with _lock:
        _source_errors[name] = _source_errors.get(name, 0) + 1


def reset_metrics() -> None:
    """Clear all in memory counters for tests and process restart."""
    with _lock:
        _requests.clear()
        _source_errors.clear()


def render_metrics() -> str:
    """Render counters in Prometheus exposition text format."""
    lines = [
        "# HELP estorides_requests_total Total HTTP responses.",
        "# TYPE estorides_requests_total counter",
    ]
    with _lock:
        req_items = sorted(_requests.items())
        err_items = sorted(_source_errors.items())
    for (endpoint, status), count in req_items:
        lines.append(
            f'estorides_requests_total{{endpoint="{endpoint}",status="{status}"}} {count}'
        )
    lines += [
        "# HELP estorides_source_errors_total Total failed source runs.",
        "# TYPE estorides_source_errors_total counter",
    ]
    for source, count in err_items:
        lines.append(f'estorides_source_errors_total{{source="{source}"}} {count}')
    return "\n".join(lines) + "\n"


def format_event(fields: dict[str, Any], as_json: bool = False) -> str:
    """Format one log event as JSON when opted in else legacy plain text."""
    if not as_json:
        event = str(fields.get("event", "event"))
        rest = " ".join(f"{k}={v}" for k, v in fields.items() if k != "event")
        return f"{event} {rest}".strip()
    payload: dict[str, Any] = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": str(fields.get("level", "info")),
    }
    for key, value in fields.items():
        if key not in payload:
            payload[key] = value
    if "event" not in payload:
        payload["event"] = "event"
    return json.dumps(payload, ensure_ascii=False)


def project_root() -> str:
    """Expose project root without hardcoding absolute paths in callers."""
    return str(PROJECT_ROOT)


__all__ = [
    "OPS",
    "OpsConfig",
    "format_event",
    "health_payload",
    "project_root",
    "ready_payload",
    "record_request",
    "record_source",
    "render_metrics",
    "reset_metrics",
]
