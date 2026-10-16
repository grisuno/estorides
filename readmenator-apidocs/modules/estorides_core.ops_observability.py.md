# `estorides_core.ops_observability`

> Source: [estorides_core/ops_observability.py:1](../../estorides_core/ops_observability.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides_core.ops_observability ================================ Single user operational visibility without external dependencies.

I provide unauthenticated liveness, authenticated readiness and
Prometheus text metrics plus an opt in JSON log formatter. I keep
all counters in process behind a lock so threaded Flask workers
cannot corrupt them. I sanitize every label so a hostile source
name cannot inject newlines into the scrape output.

## Contents

- **Classes:** [`OpsConfig`](#opsconfig)
- **Functions:** [`health_payload`](#health_payload), [`ready_payload`](#ready_payload), [`record_request`](#record_request), [`record_source`](#record_source), [`reset_metrics`](#reset_metrics), [`render_metrics`](#render_metrics), [`format_event`](#format_event), [`project_root`](#project_root)
- **Constants:** [`OPS`](#ops)

## Classes

<a id="opsconfig"></a>

### `OpsConfig`

`class` `dataclass` | [estorides_core/ops_observability.py:28](../../estorides_core/ops_observability.py#L28)

Decorators: `@dataclass(frozen=True)`

```python
class OpsConfig
```

Centralized bounds for observability output.

**Attributes**

| Name | Type | Default | Description |
|---|---|---|---|
| [`app_version`](#opsconfig-app_version) | `str` | `'1.3.0'` |  |
| [`max_label_len`](#opsconfig-max_label_len) | `int` | `_MAX_LABEL_LEN` |  |
| [`metrics_content_type`](#opsconfig-metrics_content_type) | `str` | `'text/plain; version=0.0.4'` |  |

---

## Functions

<a id="health_payload"></a>

### `health_payload`

`function` | [estorides_core/ops_observability.py:50](../../estorides_core/ops_observability.py#L50)

```python
def health_payload() -> tuple[dict[str, str], int]
```

Return liveness body and status code.

**Returns:** `tuple[dict[str, str], int]`

*Called by:* [`create_app`](estorides_web.py.md#create_app)

---

<a id="ready_payload"></a>

### `ready_payload`

`function` | [estorides_core/ops_observability.py:55](../../estorides_core/ops_observability.py#L55)

```python
def ready_payload(source_count: int, sources_dir_ok: bool) -> tuple[dict[str, Any], int]
```

Return readiness body and status code for registry state.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `source_count` | `int` |  |  |
| `sources_dir_ok` | `bool` |  |  |

**Returns:** `tuple[dict[str, Any], int]`

*Called by:* [`create_app`](estorides_web.py.md#create_app)

---

<a id="record_request"></a>

### `record_request`

`function` | [estorides_core/ops_observability.py:62](../../estorides_core/ops_observability.py#L62)

```python
def record_request(endpoint: str, status: str) -> None
```

Count one HTTP response by normalized endpoint and status.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `endpoint` | `str` |  |  |
| `status` | `str` |  |  |

---

<a id="record_source"></a>

### `record_source`

`function` | [estorides_core/ops_observability.py:72](../../estorides_core/ops_observability.py#L72)

```python
def record_source(source: str, ok: bool) -> None
```

Count one source execution failure when ok is False.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `source` | `str` |  |  |
| `ok` | `bool` |  |  |

---

<a id="reset_metrics"></a>

### `reset_metrics`

`function` | [estorides_core/ops_observability.py:83](../../estorides_core/ops_observability.py#L83)

```python
def reset_metrics() -> None
```

Clear all in memory counters for tests and process restart.

---

<a id="render_metrics"></a>

### `render_metrics`

`function` | [estorides_core/ops_observability.py:90](../../estorides_core/ops_observability.py#L90)

```python
def render_metrics() -> str
```

Render counters in Prometheus exposition text format.

**Returns:** `str`

*Called by:* [`create_app`](estorides_web.py.md#create_app)

---

<a id="format_event"></a>

### `format_event`

`function` | [estorides_core/ops_observability.py:112](../../estorides_core/ops_observability.py#L112)

```python
def format_event(fields: dict[str, Any], as_json: bool = False) -> str
```

Format one log event as JSON when opted in else legacy plain text.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `fields` | `dict[str, Any]` |  |  |
| `as_json` | `bool` | `False` |  |

**Returns:** `str`

---

<a id="project_root"></a>

### `project_root`

`function` | [estorides_core/ops_observability.py:130](../../estorides_core/ops_observability.py#L130)

```python
def project_root() -> str
```

Expose project root without hardcoding absolute paths in callers.

**Returns:** `str`

---

## Constants

<a id="ops"></a>

### `OPS`

`constant` | [estorides_core/ops_observability.py:36](../../estorides_core/ops_observability.py#L36)

```python
OPS = OpsConfig()
```

---
