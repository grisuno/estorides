#!/usr/bin/env python3
"""Tests for structured human-selector extraction (email/username/person/org/phone).

Offline only. Verifies key-aware typing, the ambiguous-key heuristic,
stopword/filename rejection, and that non-pivotable selectors are surfaced
as leaves by the pivot engine instead of being dropped.
"""
from __future__ import annotations

import asyncio
import sys
from typing import Any, Dict

from estorides_core.config import PIVOT, PIVOT_POLICY_INFRA
from estorides_core.entity_extraction import extract_structured
from estorides_core.pivot_engine import ListEventSink, PivotEngine

_failures = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global _failures
    if cond:
        print(f"PASS: {name}")
    else:
        _failures += 1
        print(f"FAIL: {name} {detail}")


def _types(payload: Any) -> Dict[str, set]:
    by_type: Dict[str, set] = {}
    for e in extract_structured(payload, "test"):
        by_type.setdefault(e.type, set()).add(e.value)
    return by_type


def main() -> int:
    got = _types({
        "login": "torvalds",
        "name": "Linus Torvalds",
        "email": "torvalds@kernel.org",
        "company": "Linux Foundation",
        "items": [
            {"author": "gregkh"},
            {"screen_name": "dhh", "real_name": "David Hansson"},
            {"phone": "+1 415 555 2671"},
            {"name": "README.md"},        # filename — must NOT become a username
            {"author": "[deleted]"},      # stopword — must drop
            {"username": "x"},            # too short — must drop
        ],
    })
    check("username from login", "torvalds" in got.get("username", set()))
    check("username from author", "gregkh" in got.get("username", set()))
    check("username from screen_name", "dhh" in got.get("username", set()))
    check("person from name", "Linus Torvalds" in got.get("person", set()))
    check("person from real_name", "David Hansson" in got.get("person", set()))
    check("email from email key", "torvalds@kernel.org" in got.get("email", set()))
    check("org from company", "Linux Foundation" in got.get("org", set()))
    check("phone from phone key", "+1 415 555 2671" in got.get("phone_e164", set()))
    check("filename not a username", "README.md" not in got.get("username", set()))
    check("stopword author dropped", "[deleted]" not in got.get("username", set()))
    check("short username dropped", "x" not in got.get("username", set()))

    # The pivot engine surfaces non-pivotable selectors as leaves (pivoted=False)
    # under the infra policy, instead of dropping them.
    class _StubRunner:
        async def run(self, query: str, **kwargs: Any) -> Dict[str, Any]:
            return {"entities": [
                {"type": "email", "value": "ceo@target.com", "source": "s"},
                {"type": "username", "value": "ceo_handle", "source": "s"},
                {"type": "domain", "value": "sub.target.com", "source": "s"},
            ], "analysis": None, "graph": None}

    sink = ListEventSink()
    engine = PivotEngine(
        runner=_StubRunner(), sink=sink, config=PIVOT, policy=PIVOT_POLICY_INFRA,
        max_depth=1, max_steps=1, max_entities=100, persist=False,
    )
    asyncio.run(engine.run("domain", "target.com"))
    entity_events = [e.data for e in sink.events if e.type == "entity"]
    leaf_types = {ev["entity"]["type"] for ev in entity_events if not ev.get("pivoted")}
    check("email surfaced as leaf under infra policy", "email" in leaf_types)
    check("username surfaced as leaf under infra policy", "username" in leaf_types)

    print(f"\n{'ALL PASS' if _failures == 0 else f'{_failures} FAILURES'}")
    return 1 if _failures else 0


if __name__ == "__main__":
    sys.exit(main())
