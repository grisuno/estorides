# `estorides_core.openapi`

> Source: [estorides_core/openapi.py:1](../../estorides_core/openapi.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides_core.openapi ====================== Minimal OpenAPI document generated from the live Flask url map.

I expose paths, methods and auth requirements without new
dependencies and without duplicating the route table by hand.

## Contents

- **Functions:** [`build_openapi`](#build_openapi)

## Functions

<a id="build_openapi"></a>

### `build_openapi`

`function` | [estorides_core/openapi.py:14](../../estorides_core/openapi.py#L14)

```python
def build_openapi(app: Any) -> dict[str, Any]
```

Build an OpenAPI 3.0 document from Flask routes.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `app` | `Any` |  |  |

**Returns:** `dict[str, Any]`

*Called by:* [`create_app`](estorides_web.py.md#create_app)

---
