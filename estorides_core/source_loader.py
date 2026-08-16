"""
estorides_core.source_loader
============================
Loads all YAML sources, normalises the schema, and provides a registry
the rest of the engine can iterate over.
"""
from __future__ import annotations

import logging
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

from .config import CONTACT_LEVELS, DEFAULT_CONTACT, contact_level

log = logging.getLogger("estorides.sources")


class Source(dict):
    """A source is a YAML-defined OSINT data provider.

    Stored as a dict for JSON-serialisation convenience, but exposes
    attribute access for ergonomic call sites."""

    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__(data)

    def __getattr__(self, key: str) -> Any:
        try:
            return self[key]
        except KeyError as exc:  # pragma: no cover - dunder edge
            raise AttributeError(key) from exc


class SourceRegistry:
    """Loads YAML sources from the sources/ directory and exposes them by name."""

    def __init__(self, sources_dir: Path) -> None:
        self.sources_dir: Path = sources_dir
        self._by_name: dict[str, Source] = {}
        self._by_category: dict[str, list[Source]] = {}

    # ---------------------------------------------------------------- load --
    def load(self) -> None:
        self._by_name.clear()
        self._by_category.clear()
        if not self.sources_dir.exists():
            log.error("sources dir missing: %s", self.sources_dir)
            return

        # Recurse so each addon can live in its own file inside a category
        # subdirectory (lazyaddons-style), while still supporting the legacy
        # grouped multi-document files at the top level.
        paths = sorted(
            p for ext in ("*.yaml", "*.yml")
            for p in self.sources_dir.rglob(ext)
        )
        for path in paths:
            self._load_file(path)

        # sort each category list for stable output
        for cat in self._by_category:
            self._by_category[cat].sort(key=lambda s: s["name"])

        log.info("loaded %d sources across %d categories",
                 len(self._by_name), len(self._by_category))

    def _load_file(self, path: Path) -> None:
        try:
            with path.open("r", encoding="utf-8") as fh:
                docs = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            log.error("YAML parse error in %s: %s", path.name, e)
            return
        except OSError as e:
            log.error("read error %s: %s", path, e)
            return

        if not docs:
            return
        if isinstance(docs, dict):
            docs = [docs]

        for raw in docs:
            if not isinstance(raw, dict):
                continue
            source = self._normalise(raw)
            if source is None:
                continue
            name = source["name"]
            if name in self._by_name:
                log.warning("duplicate source name %s in %s — overwriting", name, path.name)
            self._by_name[name] = source
            self._by_category.setdefault(source["category"], []).append(source)
            log.debug("registered source %s [%s]", name, source["category"])

    def _normalise(self, raw: dict[str, Any]) -> Source | None:
        name = raw.get("name")
        if not name or not isinstance(name, str):
            log.warning("source without name skipped: %s", raw)
            return None
        if not raw.get("enabled", False):
            return None

        tool = raw.get("tool", {}) or {}
        has_url = bool(tool.get("url"))
        has_body = bool(tool.get("body"))
        has_binary = bool(tool.get("binary"))
        if not has_url and not has_body and not has_binary:
            log.warning("source %s has no url/body/binary — skipped", name)
            return None

        # kind: origin kind. `system_app` sources execute a local Kali CLI
        # tool through tool_runner; `http_api` sources fetch a remote URL.
        # Derived from the tool block when omitted so legacy YAMLs keep
        # loading; an unknown explicit value falls back to the derived kind.
        kind = (raw.get("kind") or ("system_app" if has_binary else "http_api")).strip().lower()
        if kind not in ("http_api", "system_app"):
            log.warning("source %s declares unknown kind=%r; deriving from tool block", name, kind)
            kind = "system_app" if has_binary else "http_api"
        if kind == "system_app":
            args = tool.get("args")
            if args is None:
                tool["args"] = []
            elif not isinstance(args, list) or not all(isinstance(a, str) for a in args):
                log.warning("source %s: tool.args must be a list of strings — reset", name)
                tool["args"] = []
            output_format = str(tool.get("output_format") or "text").strip().lower()
            if output_format not in ("json", "text", "lines"):
                log.warning("source %s: unknown output_format=%r — treating as 'text'", name, output_format)
                output_format = "text"
            tool["output_format"] = output_format
            if tool.get("output_file") is not None and not isinstance(tool["output_file"], str):
                log.warning("source %s: output_file must be a string — dropped", name)
                del tool["output_file"]

        # applies_to: which query types does this source make sense for?
        # Accepts a list of strings, or a single string. Defaults to ['any'].
        applies_raw = raw.get("applies_to", "any")
        if isinstance(applies_raw, str):
            applies = [a.strip() for a in applies_raw.split(",") if a.strip()]
        else:
            applies = [str(a).strip() for a in applies_raw if str(a).strip()]
        if not applies:
            applies = ["any"]

        # contact: how this source's traffic reaches the target. Drives the
        # operator's passive-only guarantee. An unknown class is rejected to
        # the most exposing level (active) so a typo can never silently let a
        # target-touching source through a passive-only run.
        contact = (raw.get("contact") or DEFAULT_CONTACT).strip().lower()
        if contact not in CONTACT_LEVELS:
            log.warning(
                "source %s declares unknown contact=%r; treating as 'active'",
                name, contact,
            )

        pagination: dict[str, Any] = {}
        if isinstance(raw.get("pagination"), dict):
            pagination = {
                k: v for k, v in raw["pagination"].items()
                if v is not None
            }

        normalised: dict[str, Any] = {
            "name": name.strip(),
            "description": (raw.get("description") or "").strip(),
            "category": (raw.get("category") or "00. Misc").strip(),
            "os": (raw.get("os") or "any").strip().lower(),
            "kind": kind,
            "enabled": True,
            "requires_key": bool(raw.get("requires_key", False)),
            "key_env": (raw.get("key_env") or "").strip() or None,
            "parser": (raw.get("parser") or "raw_text").strip(),
            "entity_hints": list(raw.get("entity_hints", []) or []),
            "applies_to": applies,
            "contact": contact,
            "logs_queries": bool(raw.get("logs_queries", False)),
            "tool": tool,
            "pagination": pagination,
        }
        return Source(normalised)

    # --------------------------------------------------------------- access --
    def get(self, name: str) -> Source | None:
        return self._by_name.get(name)

    def all(self) -> list[Source]:
        return list(self._by_name.values())

    def by_category(self, category: str) -> list[Source]:
        return list(self._by_category.get(category, []))

    def categories(self) -> list[str]:
        return sorted(self._by_category.keys())

    def names(self) -> list[str]:
        return sorted(self._by_name.keys())

    def filter(
        self,
        *,
        requires_key: bool | None = None,
        max_contact: str | None = None,
    ) -> list[Source]:
        """Return sources matching the given predicates.

        `max_contact` keeps only sources whose contact class is at or below
        the given ceiling (e.g. "none" for a passive-only run, "broker" to
        also allow third-party probes). Sources with an unknown contact
        class are treated as the most exposing and thus excluded by any
        ceiling below `active`."""
        items: Iterable[Source] = list(self._by_name.values())
        if requires_key is not None:
            items = [s for s in items if bool(s["requires_key"]) == requires_key]
        if max_contact is not None:
            ceiling = contact_level(max_contact)
            items = [s for s in items if contact_level(s.get("contact", DEFAULT_CONTACT)) <= ceiling]
        return list(items)

    # -------------------------------------------------------------- save / del --
    def _category_dir_name(self, category: str) -> str:
        """Derive a filesystem-safe directory name from a category label.

        E.g. ``"06. Breach Intelligence"`` → ``"06_breach_intelligence"``.
        """
        parts = category.split(".", 1)
        if len(parts) > 1:
            prefix_parts = parts[0].strip().split()
            prefix = prefix_parts[0].strip().zfill(2) if prefix_parts else "00"
            suffix = parts[1].strip().lower()
        else:
            prefix = "00"
            suffix = parts[0].strip().lower()
        suffix = re.sub(r'[^a-z0-9]+', '_', suffix).strip('_')
        return f"{prefix}_{suffix}"

    def _source_path(self, name: str, category: str) -> Path:
        """Derive the filesystem path for a source based on its name and category."""
        category_dir = self.sources_dir / self._category_dir_name(category)
        safe_name = re.sub(r'[^a-z0-9_]', '_', name.lower().replace('-', '_'))
        return category_dir / f"{safe_name}.yaml"

    def _find_source_file(self, name: str) -> Path | None:
        """Locate a source file on disk by name, scanning all category dirs."""
        for f in self.sources_dir.rglob("*.y*ml"):
            try:
                with f.open("r", encoding="utf-8") as fh:
                    doc = yaml.safe_load(fh)
                if isinstance(doc, dict) and doc.get("name") == name:
                    return f.resolve()
            except (yaml.YAMLError, OSError):
                continue
        return None

    def write_source_file(self, data: dict[str, Any]) -> Path:
        """Write a source dict to the correct YAML file, overwriting if exists.

        This is a pure file-write operation — no normalisation, no registry
        update. The caller is responsible for reloading the registry if needed.
        Returns the path written.
        """
        name = data.get("name", "").strip()
        if not name:
            raise ValueError("source must have a non-empty 'name'")
        category = data.get("category", "00. Misc").strip()
        path = self._source_path(name, category)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Build clean serialisation — skip empty defaults, keep booleans
        out: dict[str, Any] = {}
        for key in ("name", "description", "category", "os", "parser", "key_env"):
            val = data.get(key)
            if val not in (None, ""):
                out[key] = val
        out["enabled"] = bool(data.get("enabled", True))
        out["requires_key"] = bool(data.get("requires_key", False))
        # entity_hints / applies_to: always list
        for key in ("entity_hints", "applies_to"):
            raw = data.get(key)
            if isinstance(raw, list) and raw:
                out[key] = raw
            elif isinstance(raw, str):
                out[key] = [s.strip() for s in raw.split(",") if s.strip()]
            else:
                out[key] = [] if key == "entity_hints" else ["any"]
        # contact
        contact = data.get("contact", "none")
        if contact not in ("none", "broker", "active"):
            contact = "none"
        if contact != "none":
            out["contact"] = contact
        out["logs_queries"] = bool(data.get("logs_queries", False))
        # tool block
        tool = data.get("tool", {})
        if not tool.get("url") and not tool.get("body") and not tool.get("binary"):
            raise ValueError("source must have a tool.url, tool.body, or tool.binary")
        out["tool"] = {}
        if tool.get("url"):
            out["tool"]["url"] = tool["url"]
            out["tool"]["method"] = tool.get("method", "GET")
        if tool.get("headers"):
            out["tool"]["headers"] = tool["headers"]
        if tool.get("params"):
            out["tool"]["params"] = tool["params"]
        if tool.get("body"):
            out["tool"]["body"] = tool["body"]
        if tool.get("binary"):
            out["kind"] = "system_app"
            out["tool"]["binary"] = tool["binary"]
            out["tool"]["args"] = tool.get("args", [])
            out["tool"]["timeout"] = tool.get("timeout", 300)
            if tool.get("output_format"):
                out["tool"]["output_format"] = tool["output_format"]
            if tool.get("output_file"):
                out["tool"]["output_file"] = tool["output_file"]
        # pagination
        if isinstance(data.get("pagination"), dict) and data["pagination"]:
            out["pagination"] = {k: v for k, v in data["pagination"].items() if v not in (None, "")}

        with path.open("w", encoding="utf-8") as fh:
            yaml.dump(out, fh, default_flow_style=False, allow_unicode=True, sort_keys=False)
        log.info("wrote source %s → %s", name, path)
        return path

    def delete_source_file(self, name: str) -> None:
        """Delete a source file by name. Raises KeyError if not found on disk."""
        path = self._find_source_file(name)
        if path is None:
            raise KeyError(f"no source file found for: {name}")
        path.unlink()
        log.info("deleted source file %s", path)

    # ----------------------------------------------------------------- fmt --
    def summary(self) -> dict[str, Any]:
        """Compact summary used by /api/status."""
        return {
            "total": len(self._by_name),
            "categories": [
                {"name": cat, "count": len(self._by_category[cat])}
                for cat in self.categories()
            ],
            "sources": [
                {
                    "name": s["name"],
                    "category": s["category"],
                    "kind": s.get("kind", "http_api"),
                    "requires_key": s["requires_key"],
                    "contact": s.get("contact", DEFAULT_CONTACT),
                    "logs_queries": bool(s.get("logs_queries", False)),
                    "description": s["description"],
                }
                for s in sorted(self._by_name.values(), key=lambda x: x["name"])
            ],
        }
