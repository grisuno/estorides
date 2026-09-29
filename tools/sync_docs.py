"""
tools.sync_docs
===============
Generate docs manifest from source truth and fail on drift.

I scan spec/*.md headings plus estorides_core modules plus the live
Flask route table, then write docs/MANIFEST.json. CI runs me with
--check so stale docs fail the build instead of rotting silently.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def collect() -> dict[str, object]:
    """Collect specs, core modules and web routes from the tree."""
    specs = sorted(p.stem for p in (ROOT / "spec").glob("*.md"))
    core = sorted(p.stem for p in (ROOT / "estorides_core").glob("*.py") if p.name != "__init__.py")
    routes: list[str] = []
    try:
        sys.path.insert(0, str(ROOT))
        import estorides_web

        app = estorides_web.create_app()
        routes = sorted({str(r.rule) for r in app.url_map.iter_rules() if str(r.rule).startswith("/")})
    except Exception as exc:
        routes = [f"!error: {exc}"]
    return {"specs": specs, "core_modules": core, "routes": routes}


def main(argv: list[str] | None = None) -> int:
    """Write the manifest or check it for drift."""
    parser = argparse.ArgumentParser(prog="sync-docs")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    manifest = collect()
    path = ROOT / "docs" / "MANIFEST.json"
    if args.check:
        if not path.is_file():
            print("MANIFEST.json missing, run tools/sync_docs.py")
            return 1
        current = json.loads(path.read_text(encoding="utf-8"))
        if current != manifest:
            print("docs drift detected, run tools/sync_docs.py")
            return 1
        return 0
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {path} ({len(manifest['specs'])} specs, {len(manifest['routes'])} routes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
