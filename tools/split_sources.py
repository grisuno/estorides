#!/usr/bin/env python3
"""Split legacy grouped source files into one addon per file.

Reads every multi-document ``sources/NN_xxx.yaml`` and writes each source as
``sources/NN_xxx/<name>.yaml``, then removes the original grouped file. The
runtime loader recurses, so the tree is picked up automatically (lazyaddons
style). Re-running is safe: existing per-addon files are overwritten in place.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

SOURCES_DIR = Path(__file__).resolve().parent.parent / "sources"


def main() -> int:
    grouped = sorted(p for p in SOURCES_DIR.glob("*.yaml") if p.is_file())
    if not grouped:
        print("no grouped *.yaml files at the top level — nothing to split")
        return 0

    written = 0
    for path in grouped:
        with path.open("r", encoding="utf-8") as fh:
            docs = yaml.safe_load(fh)
        if isinstance(docs, dict):
            docs = [docs]
        if not docs:
            continue

        target_dir = SOURCES_DIR / path.stem
        target_dir.mkdir(parents=True, exist_ok=True)
        for raw in docs:
            if not isinstance(raw, dict) or not raw.get("name"):
                continue
            name = str(raw["name"]).strip()
            out = target_dir / f"{name}.yaml"
            with out.open("w", encoding="utf-8") as fh:
                yaml.safe_dump(raw, fh, sort_keys=False, allow_unicode=True,
                               default_flow_style=False)
            written += 1
        path.unlink()
        print(f"split {path.name} -> {target_dir.name}/ ({len(docs)} addons)")

    print(f"done: {written} addon files written under {SOURCES_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
