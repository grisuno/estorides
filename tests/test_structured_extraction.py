"""
BDD tests for structured human-selector extraction + pivot leaf surfacing.

Ported from the standalone ``_test_people.py`` validator into pytest.
Offline.
"""
from __future__ import annotations

import asyncio
from typing import Any

from estorides_core.config import PIVOT, PIVOT_POLICY_INFRA
from estorides_core.entity_extraction import extract_structured
from estorides_core.pivot_engine import ListEventSink, PivotEngine

PAYLOAD = {
    "login": "torvalds",
    "name": "Linus Torvalds",
    "email": "torvalds@kernel.org",
    "company": "Linux Foundation",
    "items": [
        {"author": "gregkh"},
        {"screen_name": "dhh", "real_name": "David Hansson"},
        {"phone": "+1 415 555 2671"},
        {"name": "README.md"},
        {"author": "[deleted]"},
        {"username": "x"},
    ],
}


def _types(payload: Any) -> dict[str, set]:
    by_type: dict[str, set] = {}
    for e in extract_structured(payload, "test"):
        by_type.setdefault(e.type, set()).add(e.value)
    return by_type


class TestExtractStructured:
    def test_happy_path_selectors(self) -> None:
        got = _types(PAYLOAD)
        assert "torvalds" in got.get("username", set())
        assert "gregkh" in got.get("username", set())
        assert "dhh" in got.get("username", set())
        assert "Linus Torvalds" in got.get("person", set())
        assert "David Hansson" in got.get("person", set())
        assert "torvalds@kernel.org" in got.get("email", set())
        assert "Linux Foundation" in got.get("org", set())
        assert "+1 415 555 2671" in got.get("phone_e164", set())

    def test_noise_rejected(self) -> None:
        got = _types(PAYLOAD)
        assert "README.md" not in got.get("username", set())
        assert "[deleted]" not in got.get("username", set())
        assert "x" not in got.get("username", set())


class _StubRunner:
    async def run(self, query: str, **kwargs: Any) -> dict[str, Any]:
        return {"entities": [
            {"type": "email", "value": "ceo@target.com", "source": "s"},
            {"type": "username", "value": "ceo_handle", "source": "s"},
            {"type": "domain", "value": "sub.target.com", "source": "s"},
        ], "analysis": None, "graph": None}


class TestPivotLeafSurfacing:
    def test_non_pivotable_selectors_surface_as_leaves(self) -> None:
        sink = ListEventSink()
        engine = PivotEngine(
            runner=_StubRunner(), sink=sink, config=PIVOT, policy=PIVOT_POLICY_INFRA,
            max_depth=1, max_steps=1, max_entities=100, persist=False,
        )
        asyncio.run(engine.run("domain", "target.com"))
        entity_events = [e.data for e in sink.events if e.type == "entity"]
        leaf_types = {ev["entity"]["type"] for ev in entity_events if not ev.get("pivoted")}
        assert "email" in leaf_types
        assert "username" in leaf_types
