"""
estorides_core.pagination
=========================
Pagination strategies for source API fetches.

Pure dataclasses + iteration logic. No I/O, no asyncio, no HTTP. The
orchestrator owns the fetch loop; this module only describes *how* to
advance from one page to the next and *when* to stop.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEFAULT_MAX_PAGES = 10


@dataclass(frozen=True)
class PaginationConfig:
    """Configuration for a paginated source fetch.

    Parsed from the source YAML's ``pagination`` key. No fields are
    required; a source with no pagination config results in a single
    fetch (the current default behaviour).
    """

    strategy: str = ""
    param: str = "page"
    page_size: int = 0
    max_pages: int = DEFAULT_MAX_PAGES
    cursor_param: str = "cursor"
    cursor_path: str = "next"
    response_list_path: str = ""
    offset_param: str = "offset"
    limit_param: str = "limit"

    @staticmethod
    def from_dict(raw: dict[str, Any] | None) -> PaginationConfig:
        if not raw:
            return PaginationConfig()
        return PaginationConfig(
            strategy=str(raw.get("strategy", "")).strip().lower(),
            param=str(raw.get("param", "page")),
            page_size=int(raw.get("page_size", 0) or 0),
            max_pages=int(raw.get("max_pages", DEFAULT_MAX_PAGES) or DEFAULT_MAX_PAGES),
            cursor_param=str(raw.get("cursor_param", "cursor")),
            cursor_path=str(raw.get("cursor_path", "next")),
            response_list_path=str(raw.get("response_list_path", "")),
            offset_param=str(raw.get("offset_param", "offset")),
            limit_param=str(raw.get("limit_param", "limit")),
        )

    @property
    def enabled(self) -> bool:
        return bool(self.strategy)

    @property
    def needs_page_size(self) -> bool:
        return self.strategy in ("page", "offset")


def build_page_params(cfg: PaginationConfig, page_num: int) -> dict[str, str]:
    """Build URL params dict for a given page number.

    Returns an empty dict for cursor strategy (the cursor is set
    dynamically from the response) or when pagination is disabled.
    """
    if not cfg.enabled:
        return {}
    if cfg.strategy == "page":
        return {cfg.param: str(page_num)}
    if cfg.strategy == "offset":
        offset = (page_num - 1) * cfg.page_size
        return {cfg.offset_param: str(offset), cfg.limit_param: str(cfg.page_size)}
    return {}


def extract_cursor(data: Any, cfg: PaginationConfig) -> str | None:
    """Extract the next-page cursor from a parsed response body.

    Walks the dot-separated ``cursor_path`` into the JSON-like dict.
    Returns ``None`` when the path is absent or the value is empty.
    """
    if not cfg.enabled or cfg.strategy != "cursor" or not isinstance(data, dict):
        return None
    parts = cfg.cursor_path.split(".")
    current: Any = data
    for part in parts:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
        if current is None:
            return None
    if isinstance(current, str) and current.strip():
        return current.strip()
    return None


def count_results(data: Any, cfg: PaginationConfig) -> int:
    """Count results in a parsed response page.

    Uses ``response_list_path`` if configured, otherwise tries common
    JSON fields (``results``, ``items``, ``data``) or falls back to
    ``len(data)`` for a list-type response.
    """
    if not isinstance(data, (dict, list)):
        return 0
    if isinstance(data, list):
        return len(data)
    if cfg.response_list_path:
        parts = cfg.response_list_path.split(".")
        current: Any = data
        for part in parts:
            if not isinstance(current, dict):
                return 0
            current = current.get(part)
        if isinstance(current, list):
            return len(current)
        return 0
    for key in ("results", "items", "data", "records"):
        val = data.get(key)
        if isinstance(val, list):
            return len(val)
    return 0
