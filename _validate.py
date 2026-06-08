#!/usr/bin/env python3
"""Run every offline test suite and aggregate the result.

Discovers `_test_*.py` next to this file, runs each in a subprocess, and
exits 0 only when all pass. CI runners can `grep FAIL` on the output or
just check the exit code.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    suites = sorted(HERE.glob("_test_*.py"))
    if not suites:
        print("no _test_*.py suites found", file=sys.stderr)
        return 1

    failed: list[str] = []
    for suite in suites:
        print(f"\n{'=' * 60}\n=== {suite.name}\n{'=' * 60}")
        proc = subprocess.run([sys.executable, str(suite)], cwd=str(HERE))
        if proc.returncode != 0:
            failed.append(suite.name)

    print(f"\n{'=' * 60}")
    if failed:
        print(f"VALIDATION FAILED: {', '.join(failed)}")
        return 1
    print(f"VALIDATION OK: {len(suites)} suite(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
