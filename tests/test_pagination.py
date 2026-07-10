"""
BDD tests for estorides_core.pagination.

These tests verify the pagination strategy config, param building,
cursor extraction, and result counting — all pure functions, no I/O.
"""
from __future__ import annotations

from estorides_core.pagination import (
    DEFAULT_MAX_PAGES,
    PaginationConfig,
    build_page_params,
    count_results,
    extract_cursor,
)


# ---------------------------------------------------------------------------
# PG1 · Page strategy increments param
# ---------------------------------------------------------------------------
class TestPageStrategy:
    """PG1: page param increments with each page number."""

    def test_first_page_is_one(self) -> None:
        cfg = PaginationConfig(strategy="page", param="pg", page_size=10)
        params = build_page_params(cfg, 1)
        assert params == {"pg": "1"}

    def test_second_page_increments(self) -> None:
        cfg = PaginationConfig(strategy="page", param="pg", page_size=10)
        params = build_page_params(cfg, 2)
        assert params == {"pg": "2"}

    def test_default_param_name(self) -> None:
        cfg = PaginationConfig(strategy="page", page_size=10)
        params = build_page_params(cfg, 3)
        assert params == {"page": "3"}

    def test_no_pagination_returns_empty(self) -> None:
        cfg = PaginationConfig()
        params = build_page_params(cfg, 1)
        assert params == {}


# ---------------------------------------------------------------------------
# PG2 · Offset strategy advances by page_size
# ---------------------------------------------------------------------------
class TestOffsetStrategy:
    """PG2: offset advances by page_size each page."""

    def test_first_page_offset_zero(self) -> None:
        cfg = PaginationConfig(strategy="offset", page_size=25)
        params = build_page_params(cfg, 1)
        assert params == {"offset": "0", "limit": "25"}

    def test_second_page_offset_25(self) -> None:
        cfg = PaginationConfig(strategy="offset", page_size=25)
        params = build_page_params(cfg, 2)
        assert params == {"offset": "25", "limit": "25"}

    def test_third_page_offset_50(self) -> None:
        cfg = PaginationConfig(strategy="offset", page_size=25)
        params = build_page_params(cfg, 3)
        assert params == {"offset": "50", "limit": "25"}

    def test_custom_param_names(self) -> None:
        cfg = PaginationConfig(
            strategy="offset", page_size=10,
            offset_param="start", limit_param="count",
        )
        params = build_page_params(cfg, 2)
        assert params == {"start": "10", "count": "10"}


# ---------------------------------------------------------------------------
# PG3 · Cursor strategy reads next token from response
# ---------------------------------------------------------------------------
class TestCursorStrategy:
    """PG3: cursor extracted from response body."""

    def test_extracts_cursor_from_simple_path(self) -> None:
        cfg = PaginationConfig(strategy="cursor", cursor_path="next_cursor")
        data = {"next_cursor": "token_abc", "results": []}
        assert extract_cursor(data, cfg) == "token_abc"

    def test_extracts_cursor_from_nested_path(self) -> None:
        cfg = PaginationConfig(strategy="cursor", cursor_path="meta.next")
        data = {"meta": {"next": "cursor_xyz"}}
        assert extract_cursor(data, cfg) == "cursor_xyz"

    def test_missing_path_returns_none(self) -> None:
        cfg = PaginationConfig(strategy="cursor", cursor_path="meta.next")
        assert extract_cursor({"meta": {}}, cfg) is None

    def test_empty_cursor_returns_none(self) -> None:
        cfg = PaginationConfig(strategy="cursor", cursor_path="next")
        assert extract_cursor({"next": ""}, cfg) is None

    def test_null_cursor_returns_none(self) -> None:
        cfg = PaginationConfig(strategy="cursor", cursor_path="next")
        assert extract_cursor({"next": None}, cfg) is None

    def test_non_dict_response_returns_none(self) -> None:
        cfg = PaginationConfig(strategy="cursor", cursor_path="next")
        assert extract_cursor([1, 2, 3], cfg) is None

    def test_disabled_strategy_returns_none(self) -> None:
        cfg = PaginationConfig()
        assert extract_cursor({"next": "abc"}, cfg) is None

    def test_build_params_empty_for_cursor(self) -> None:
        cfg = PaginationConfig(strategy="cursor", cursor_param="c")
        params = build_page_params(cfg, 1)
        assert params == {}

    def test_cursor_custom_param(self) -> None:
        cfg = PaginationConfig(
            strategy="cursor", cursor_param="page_token", cursor_path="next"
        )
        data = {"next": "tok_123"}
        cur = extract_cursor(data, cfg)
        assert cur == "tok_123"


# ---------------------------------------------------------------------------
# PG4 · No pagination = no loop
# ---------------------------------------------------------------------------
class TestNoPagination:
    """PG4: default config means disabled."""

    def test_default_config_disabled(self) -> None:
        cfg = PaginationConfig()
        assert not cfg.enabled

    def test_empty_dict_disabled(self) -> None:
        cfg = PaginationConfig.from_dict({})
        assert not cfg.enabled

    def test_none_disabled(self) -> None:
        cfg = PaginationConfig.from_dict(None)
        assert not cfg.enabled

    def test_enabled_when_strategy_set(self) -> None:
        cfg = PaginationConfig.from_dict({"strategy": "page"})
        assert cfg.enabled


# ---------------------------------------------------------------------------
# PG5 · Partial page stops loop
# ---------------------------------------------------------------------------
class TestPartialPage:
    """PG5: fewer results than page_size signals last page."""

    def test_partial_page_detected(self) -> None:
        cfg = PaginationConfig(strategy="page", page_size=10)
        data = {"results": [1, 2, 3]}
        assert count_results(data, cfg) == 3

    def test_full_page_not_detected_as_partial(self) -> None:
        cfg = PaginationConfig(strategy="page", page_size=10)
        data = {"results": list(range(10))}
        assert count_results(data, cfg) == 10

    def test_list_response_counted_directly(self) -> None:
        cfg = PaginationConfig(strategy="page", page_size=5)
        assert count_results([1, 2, 3], cfg) == 3

    def test_using_custom_response_list_path(self) -> None:
        cfg = PaginationConfig(
            strategy="page", page_size=5,
            response_list_path="data.items",
        )
        data = {"data": {"items": [1, 2]}}
        assert count_results(data, cfg) == 2


# ---------------------------------------------------------------------------
# PG6 · Max pages caps the loop
# ---------------------------------------------------------------------------
class TestMaxPages:
    """PG6: max_pages limits total requests."""

    def test_default_max_pages(self) -> None:
        cfg = PaginationConfig(strategy="page", page_size=10)
        assert cfg.max_pages == DEFAULT_MAX_PAGES

    def test_custom_max_pages(self) -> None:
        cfg = PaginationConfig.from_dict({
            "strategy": "page", "page_size": 10, "max_pages": 3,
        })
        assert cfg.max_pages == 3

    def test_zero_page_size_means_no_check(self) -> None:
        cfg = PaginationConfig(strategy="page", page_size=0)
        assert cfg.needs_page_size


# ---------------------------------------------------------------------------
# PG7 · Empty cursor stops loop (covered in TestCursorStrategy)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# PaginationConfig from_dict
# ---------------------------------------------------------------------------
class TestFromDict:
    """PaginationConfig construction from raw dict."""

    def test_all_fields_mapped(self) -> None:
        cfg = PaginationConfig.from_dict({
            "strategy": "cursor",
            "param": "p",
            "page_size": 50,
            "max_pages": 5,
            "cursor_param": "c",
            "cursor_path": "data.meta.cursor",
            "response_list_path": "items",
            "offset_param": "ofs",
            "limit_param": "lim",
        })
        assert cfg.strategy == "cursor"
        assert cfg.param == "p"
        assert cfg.page_size == 50
        assert cfg.max_pages == 5
        assert cfg.cursor_param == "c"
        assert cfg.cursor_path == "data.meta.cursor"
        assert cfg.response_list_path == "items"
        assert cfg.offset_param == "ofs"
        assert cfg.limit_param == "lim"

    def test_partial_dict_uses_defaults(self) -> None:
        cfg = PaginationConfig.from_dict({"strategy": "page"})
        assert cfg.param == "page"
        assert cfg.max_pages == DEFAULT_MAX_PAGES
        assert cfg.cursor_param == "cursor"

    def test_empty_string_strategy_disabled(self) -> None:
        cfg = PaginationConfig.from_dict({"strategy": ""})
        assert not cfg.enabled
