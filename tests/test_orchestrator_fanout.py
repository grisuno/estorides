"""M0 RED tests: fanout normalisation + callback parity + no duplicated methods."""
from __future__ import annotations

import asyncio
from typing import Any

from estorides_core import orchestrator as oc


def _src(name: str, binary: str | None = None) -> dict[str, Any]:
    tool: dict[str, Any] = {"binary": binary} if binary else {}
    return {
        "name": name, "tool": tool, "category": "test",
        "description": "d", "parser": "raw", "requires_key": False,
        "applies_to": ["any"],
    }


def test_no_duplicated_method_defs() -> None:
    import inspect

    src = inspect.getsource(oc.Orchestrator)
    assert src.count("def _extract_cursor") == 1
    assert src.count("def _infer_relationships") == 1
    assert src.count("def _write_dataset") == 1


def _norm(items: list[Any], sources: list[Any]) -> list[Any]:
    orch = oc.Orchestrator.__new__(oc.Orchestrator)
    return orch._normalise_results(items, sources)


def test_exception_becomes_error_observation() -> None:
    s = _src("s1")
    out = _norm([ValueError("boom")], [s])
    assert len(out) == 1
    assert out[0][0]["name"] == "s1"
    assert out[0][3]["error"] == "exception:ValueError"


def test_bad_shape_becomes_error_observation() -> None:
    s = _src("s1")
    out = _norm(["not-a-tuple"], [s])
    assert out[0][3]["error"].startswith("bad-result-shape")


def test_mixed_http_and_system_app_keep_own_source() -> None:
    http = _src("http1")
    sys = _src("sys1", binary="theHarvester")
    t_http = (http, {"a": 1}, {"a": 1}, {"source": "http1"})
    t_sys = (sys, {"b": 2}, None, {"source": "sys1"})
    out = _norm([t_http, t_sys], [http, sys])
    assert [o[0]["name"] for o in out] == ["http1", "sys1"]


def test_execute_source_forwards_on_done_to_system_app() -> None:
    import inspect

    sig = inspect.signature(oc.Orchestrator._run_system_app)
    assert "on_done" in sig.parameters
    sig2 = inspect.signature(oc.Orchestrator._execute_source)
    src = inspect.getsource(oc.Orchestrator._execute_source)
    assert "on_done" in src
    assert sig2.parameters["on_done"] is not None


def test_system_app_failure_fires_on_done() -> None:
    async def go() -> list[tuple]:
        fired: list[tuple] = []
        s = _src("sys1", binary="definitely-not-a-real-tool-xyz")
        orch = oc.Orchestrator.__new__(oc.Orchestrator)
        await orch._run_system_app(
            s, "example.com",
            on_done=lambda n, ok, st, ms: fired.append((n, ok)),
        )
        return fired

    fired = asyncio.run(go())
    assert fired and fired[0][0] == "sys1" and fired[0][1] is False
