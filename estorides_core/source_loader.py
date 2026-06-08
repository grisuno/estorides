"""
estorides_core.source_loader
============================
Loads all YAML sources, normalises the schema, and provides a registry
the rest of the engine can iterate over.
"""
from __future__ import annotations

import os
import re
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml

from .config import CONTACT_LEVELS, DEFAULT_CONTACT, contact_level

log = logging.getLogger("estorides.sources")


class Source(dict):
    """A source is a YAML-defined OSINT data provider.

    Stored as a dict for JSON-serialisation convenience, but exposes
    attribute access for ergonomic call sites."""

    def __init__(self, data: Dict[str, Any]) -> None:
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
        self._by_name: Dict[str, Source] = {}
        self._by_category: Dict[str, List[Source]] = {}

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

    def _normalise(self, raw: Dict[str, Any]) -> Optional[Source]:
        name = raw.get("name")
        if not name or not isinstance(name, str):
            log.warning("source without name skipped: %s", raw)
            return None
        if not raw.get("enabled", False):
            return None

        tool = raw.get("tool", {}) or {}
        if not tool.get("url") and not tool.get("body"):
            log.warning("source %s has no url/body — skipped", name)
            return None

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

        normalised: Dict[str, Any] = {
            "name": name.strip(),
            "description": (raw.get("description") or "").strip(),
            "category": (raw.get("category") or "00. Misc").strip(),
            "os": (raw.get("os") or "any").strip().lower(),
            "enabled": True,
            "requires_key": bool(raw.get("requires_key", False)),
            "key_env": (raw.get("key_env") or "").strip() or None,
            "parser": (raw.get("parser") or "raw_text").strip(),
            "entity_hints": list(raw.get("entity_hints", []) or []),
            "applies_to": applies,
            "contact": contact,
            "logs_queries": bool(raw.get("logs_queries", False)),
            "tool": tool,
        }
        return Source(normalised)

    # --------------------------------------------------------------- access --
    def get(self, name: str) -> Optional[Source]:
        return self._by_name.get(name)

    def all(self) -> List[Source]:
        return list(self._by_name.values())

    def by_category(self, category: str) -> List[Source]:
        return list(self._by_category.get(category, []))

    def categories(self) -> List[str]:
        return sorted(self._by_category.keys())

    def names(self) -> List[str]:
        return sorted(self._by_name.keys())

    def filter(
        self,
        *,
        requires_key: Optional[bool] = None,
        max_contact: Optional[str] = None,
    ) -> List[Source]:
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

    # ----------------------------------------------------------------- fmt --
    def summary(self) -> Dict[str, Any]:
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
                    "requires_key": s["requires_key"],
                    "contact": s.get("contact", DEFAULT_CONTACT),
                    "logs_queries": bool(s.get("logs_queries", False)),
                    "description": s["description"],
                }
                for s in sorted(self._by_name.values(), key=lambda x: x["name"])
            ],
        }
