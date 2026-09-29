"""M1 ops_observability — BDD red. Debe fallar hasta implementar módulo."""
from __future__ import annotations

import json
import threading


def test_healthz_no_auth_ok():
    from estorides_core.ops_observability import health_payload

    body, code = health_payload()
    assert code == 200
    assert body["status"] == "ok"
    assert "version" in body


def test_readyz_ready_and_not_ready():
    from estorides_core.ops_observability import ready_payload

    body, code = ready_payload(source_count=5, sources_dir_ok=True)
    assert code == 200 and body == {"ready": True, "sources": 5}
    body, code = ready_payload(source_count=0, sources_dir_ok=False)
    assert code == 503 and body["ready"] is False


def test_metrics_counters_and_render():
    from estorides_core.ops_observability import (
        record_request,
        record_source,
        render_metrics,
        reset_metrics,
    )

    reset_metrics()
    record_request("/api/run", "200")
    record_request("/api/run", "200")
    record_request("/api/run", "200")
    record_source("crtsh", ok=False)
    out = render_metrics()
    assert 'estorides_requests_total{endpoint="/api/run",status="200"} 3' in out
    assert 'estorides_source_errors_total{source="crtsh"} 1' in out


def test_metrics_label_sanitised_no_newline():
    from estorides_core.ops_observability import (
        record_source,
        render_metrics,
        reset_metrics,
    )

    reset_metrics()
    record_source("crtsh\nINJECT:x", ok=False)
    out = render_metrics()
    assert "\nINJECT" not in out
    # una línea por serie (más HELP/TYPE)
    for line in out.splitlines():
        if line.startswith("estorides_source_errors_total{"):
            assert "\n" not in line and "\r" not in line


def test_json_logs_opt_in_and_legacy():
    from estorides_core.ops_observability import format_event

    line = format_event({"event": "source_executed", "source": "crtsh"}, as_json=True)
    parsed = json.loads(line)
    assert parsed["event"] == "source_executed"
    assert "ts" in parsed and "level" in parsed
    plain = format_event({"event": "x"}, as_json=False)
    assert "x" in plain
    with __import__("pytest").raises(json.JSONDecodeError):
        json.loads(plain + "{unclosed")


def test_metrics_thread_safe():
    from estorides_core.ops_observability import (
        record_request,
        render_metrics,
        reset_metrics,
    )

    reset_metrics()
    threads = [
        threading.Thread(target=lambda: [record_request("/api/run", "200") for _ in range(100)])
        for _ in range(10)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert '} 1000' in render_metrics()
