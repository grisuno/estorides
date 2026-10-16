# `estorides_core.pagination`

> Source: [estorides_core/pagination.py:1](../../estorides_core/pagination.py#L1) | language `py` | coverage 62.5% | [API index](../index.md)

estorides_core.pagination ========================= Pagination strategies for source API fetches.

Pure dataclasses + iteration logic. No I/O, no asyncio, no HTTP. The
orchestrator owns the fetch loop; this module only describes *how* to
advance from one page to the next and *when* to stop.

## Contents

- **Classes:** [`PaginationConfig`](#paginationconfig)
- **Functions:** [`build_page_params`](#build_page_params), [`extract_cursor`](#extract_cursor), [`count_results`](#count_results)
- **Constants:** [`DEFAULT_MAX_PAGES`](#default_max_pages)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_estorides_core_pagination_py__PaginationConfig_from_dict(["PaginationConfig.from_dict"])
    n_estorides_core_pagination_py__PaginationConfig(["PaginationConfig"])
    n_estorides_core_pagination_py__PaginationConfig_from_dict --> n_estorides_core_pagination_py__PaginationConfig
```

## Classes

<a id="paginationconfig"></a>

### `PaginationConfig`

`class` `dataclass` | [estorides_core/pagination.py:19](../../estorides_core/pagination.py#L19)

Decorators: `@dataclass(frozen=True)`

```python
class PaginationConfig
```

Configuration for a paginated source fetch.

Parsed from the source YAML's ``pagination`` key. No fields are
required; a source with no pagination config results in a single
fetch (the current default behaviour).

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`strategy`](#paginationconfig-strategy) | `str` | `''` |  |
| [`param`](#paginationconfig-param) | `str` | `'page'` |  |
| [`page_size`](#paginationconfig-page_size) | `int` | `0` |  |
| [`max_pages`](#paginationconfig-max_pages) | `int` | `DEFAULT_MAX_PAGES` |  |
| [`cursor_param`](#paginationconfig-cursor_param) | `str` | `'cursor'` |  |
| [`cursor_path`](#paginationconfig-cursor_path) | `str` | `'next'` |  |
| [`response_list_path`](#paginationconfig-response_list_path) | `str` | `''` |  |
| [`offset_param`](#paginationconfig-offset_param) | `str` | `'offset'` |  |
| [`limit_param`](#paginationconfig-limit_param) | `str` | `'limit'` |  |

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`from_dict`](#paginationconfig-from_dict) | staticmethod |  |
| [`enabled`](#paginationconfig-enabled) | property |  |
| [`needs_page_size`](#paginationconfig-needs_page_size) | property |  |

<a id="paginationconfig-from_dict"></a>

#### `PaginationConfig.from_dict`

`staticmethod` | [estorides_core/pagination.py:38](../../estorides_core/pagination.py#L38)

Decorators: `@staticmethod`

```python
def from_dict(raw: dict[str, Any] | None) -> PaginationConfig
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `raw` | `dict[str, Any] \| None` |  |  |

**Returns:** `PaginationConfig`

*Calls:* [`PaginationConfig`](#paginationconfig)

<a id="paginationconfig-enabled"></a>

#### `PaginationConfig.enabled`

`property` | [estorides_core/pagination.py:54](../../estorides_core/pagination.py#L54)

Decorators: `@property`

```python
def enabled(self) -> bool
```

**Returns:** `bool`

<a id="paginationconfig-needs_page_size"></a>

#### `PaginationConfig.needs_page_size`

`property` | [estorides_core/pagination.py:58](../../estorides_core/pagination.py#L58)

Decorators: `@property`

```python
def needs_page_size(self) -> bool
```

**Returns:** `bool`

---

## Functions

<a id="build_page_params"></a>

### `build_page_params`

`function` | [estorides_core/pagination.py:62](../../estorides_core/pagination.py#L62)

```python
def build_page_params(cfg: PaginationConfig, page_num: int) -> dict[str, str]
```

Build URL params dict for a given page number.

Returns an empty dict for cursor strategy (the cursor is set
dynamically from the response) or when pagination is disabled.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `cfg` | `PaginationConfig` |  |  |
| `page_num` | `int` |  |  |

**Returns:** `dict[str, str]`

---

<a id="extract_cursor"></a>

### `extract_cursor`

`function` | [estorides_core/pagination.py:78](../../estorides_core/pagination.py#L78)

```python
def extract_cursor(data: Any, cfg: PaginationConfig) -> str | None
```

Extract the next-page cursor from a parsed response body.

Walks the dot-separated `[`cursor_path`](#paginationconfig-cursor_path)` into the JSON-like dict.
Returns ``None`` when the path is absent or the value is empty.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `Any` |  |  |
| `cfg` | `PaginationConfig` |  |  |

**Returns:** `str | None`

---

<a id="count_results"></a>

### `count_results`

`function` | [estorides_core/pagination.py:99](../../estorides_core/pagination.py#L99)

```python
def count_results(data: Any, cfg: PaginationConfig) -> int
```

Count results in a parsed response page.

Uses `[`response_list_path`](#paginationconfig-response_list_path)` if configured, otherwise tries common
JSON fields (``results``, ``items``, `[`data`](estorides_core.pivot_engine.py.md#pivotevent-data)`) or falls back to
``len(data)`` for a list-type response.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `data` | `Any` |  |  |
| `cfg` | `PaginationConfig` |  |  |

**Returns:** `int`

---

## Constants

<a id="default_max_pages"></a>

### `DEFAULT_MAX_PAGES`

`constant` | [estorides_core/pagination.py:15](../../estorides_core/pagination.py#L15)

```python
DEFAULT_MAX_PAGES = 10
```

---
