#!/usr/bin/env python3
"""Tests for the operator-OPSEC contact classification + passive-only filter.

Offline only: exercises the source registry and the orchestrator source
selector without any network. Prints PASS/FAIL lines; exits non-zero on any
failure so CI can `grep FAIL`.
"""
from __future__ import annotations

import sys

from estorides_core.config import (CONTACT_LEVELS, DEFAULT_CONTACT,
                                    SOURCES_DIR, contact_level)
from estorides_core.orchestrator import Orchestrator
from estorides_core.source_loader import SourceRegistry

_failures = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global _failures
    if cond:
        print(f"PASS: {name}")
    else:
        _failures += 1
        print(f"FAIL: {name} {detail}")


def main() -> int:
    # contact_level: known levels ordered, unknown == active (most exposing).
    check("contact none < broker < active",
          contact_level("none") < contact_level("broker") < contact_level("active"))
    check("unknown contact treated as active",
          contact_level("bogus") == CONTACT_LEVELS["active"])
    check("default contact is passive",
          contact_level(DEFAULT_CONTACT) == CONTACT_LEVELS["none"])

    reg = SourceRegistry(SOURCES_DIR)
    reg.load()
    all_sources = reg.all()
    check("sources load", len(all_sources) > 0, f"got {len(all_sources)}")

    # Every source has a valid contact class after normalisation.
    bad = [s["name"] for s in all_sources if s.get("contact") not in CONTACT_LEVELS]
    check("all sources carry a known contact class", not bad, f"offenders={bad[:5]}")

    # passive-only registry filter never returns a target-touching source.
    passive = reg.filter(max_contact="none")
    leaked = [s["name"] for s in passive if contact_level(s["contact"]) > 0]
    check("registry passive filter excludes broker/active", not leaked, f"leaked={leaked}")
    check("passive subset is strictly smaller (brokers exist)",
          len(passive) < len(all_sources))

    # The three hackertarget active-probe sources are tagged broker.
    broker_names = {s["name"] for s in all_sources if s["contact"] == "broker"}
    for expected in ("hackertarget_nping", "hackertarget_traceroute", "hackertarget_http_headers"):
        check(f"{expected} tagged broker", expected in broker_names)

    # Orchestrator selector honours passive-only even for explicit --only-sources.
    orch = Orchestrator()
    chosen = orch._select_sources(
        ["hackertarget_nping", "crt_sh_certificates"],
        include_paid=True, max_contact="none",
    )
    chosen_names = {s["name"] for s in chosen}
    check("selector drops broker even when named explicitly",
          "hackertarget_nping" not in chosen_names)
    check("selector keeps passive source when named",
          "crt_sh_certificates" in chosen_names)

    # Without the ceiling, the broker source is selectable again.
    chosen_open = orch._select_sources(
        ["hackertarget_nping"], include_paid=True, max_contact=None,
    )
    check("selector keeps broker when no ceiling set",
          "hackertarget_nping" in {s["name"] for s in chosen_open})

    print(f"\n{'ALL PASS' if _failures == 0 else f'{_failures} FAILURES'}")
    return 1 if _failures else 0


if __name__ == "__main__":
    sys.exit(main())
