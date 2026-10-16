# `estorides_core.fusion_analytics`

> Source: [estorides_core/fusion_analytics.py:1](../../estorides_core/fusion_analytics.py#L1) | language `py` | coverage 18.2% | [API index](../index.md)

estorides_core.fusion_analytics =============================== Intelligence analytics layer over the fusion store.

Provides the "dashboard" queries that Palantir's Athena delivers:
multi-source consensus, entity timelines, source reliability stats,
and corroboration analytics. All read-only, all parameterized SQL,
all fail-soft.

Public surface:
    analytics = FusionAnalytics(fusion_store_instance)
    analytics.entity_timeline(eid) -> dict | None
    analytics.entity_summary(eid) -> dict | None
    analytics.source_stats(source_name) -> dict | None
    analytics.multi_source_consensus(eid, key) -> dict
    analytics.corroborated_properties(eid, min_sources=2) -> list
    analytics.entity_search(term, ...) -> list
    analytics.top_changed(days=7, limit=20) -> list
    analytics.source_corroboration_matrix(limit=20) -> list

## Contents

- **Classes:** [`FusionAnalytics`](#fusionanalytics)

## Classes

<a id="fusionanalytics"></a>

### `FusionAnalytics`

`class` | [estorides_core/fusion_analytics.py:31](../../estorides_core/fusion_analytics.py#L31)

```python
class FusionAnalytics
```

Read-only analytics queries over the fusion store.

Every method is parameterized SQL — no string interpolation.
A ``store`` of ``None`` is silently handled (all methods return
empty results) so the caller never needs to guard against a
missing datastore.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#fusionanalytics-__init__) | constructor |  |
| [`entity_timeline`](#fusionanalytics-entity_timeline) | method |  |
| [`entity_summary`](#fusionanalytics-entity_summary) | method |  |
| [`source_stats`](#fusionanalytics-source_stats) | method |  |
| [`multi_source_consensus`](#fusionanalytics-multi_source_consensus) | method |  |
| [`corroborated_properties`](#fusionanalytics-corroborated_properties) | method |  |
| [`entity_search`](#fusionanalytics-entity_search) | method |  |
| [`top_changed`](#fusionanalytics-top_changed) | method |  |
| [`source_corroboration_matrix`](#fusionanalytics-source_corroboration_matrix) | method |  |

<a id="fusionanalytics-__init__"></a>

#### `FusionAnalytics.__init__`

`constructor` | [estorides_core/fusion_analytics.py:40](../../estorides_core/fusion_analytics.py#L40)

```python
def __init__(self, store: Any) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `store` | `Any` |  |  |

*Called by:* [`create_app`](estorides_web.py.md#create_app)

<a id="fusionanalytics-entity_timeline"></a>

#### `FusionAnalytics.entity_timeline`

`method` | [estorides_core/fusion_analytics.py:46](../../estorides_core/fusion_analytics.py#L46)

```python
def entity_timeline(self, eid: str) -> dict[str, Any] | None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `eid` | `str` |  |  |

**Returns:** `dict[str, Any] | None`

<a id="fusionanalytics-entity_summary"></a>

#### `FusionAnalytics.entity_summary`

`method` | [estorides_core/fusion_analytics.py:132](../../estorides_core/fusion_analytics.py#L132)

```python
def entity_summary(self, eid: str) -> dict[str, Any] | None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `eid` | `str` |  |  |

**Returns:** `dict[str, Any] | None`

<a id="fusionanalytics-source_stats"></a>

#### `FusionAnalytics.source_stats`

`method` | [estorides_core/fusion_analytics.py:213](../../estorides_core/fusion_analytics.py#L213)

```python
def source_stats(self, source_name: str) -> dict[str, Any] | None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `source_name` | `str` |  |  |

**Returns:** `dict[str, Any] | None`

<a id="fusionanalytics-multi_source_consensus"></a>

#### `FusionAnalytics.multi_source_consensus`

`method` | [estorides_core/fusion_analytics.py:290](../../estorides_core/fusion_analytics.py#L290)

```python
def multi_source_consensus(self, eid: str, key: str) -> dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `eid` | `str` |  |  |
| `key` | `str` |  |  |

**Returns:** `dict[str, Any]`

<a id="fusionanalytics-corroborated_properties"></a>

#### `FusionAnalytics.corroborated_properties`

`method` | [estorides_core/fusion_analytics.py:343](../../estorides_core/fusion_analytics.py#L343)

```python
def corroborated_properties(self, eid: str, min_sources: int = 2) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `eid` | `str` |  |  |
| `min_sources` | `int` | `2` |  |

**Returns:** `list[dict[str, Any]]`

<a id="fusionanalytics-entity_search"></a>

#### `FusionAnalytics.entity_search`

`method` | [estorides_core/fusion_analytics.py:374](../../estorides_core/fusion_analytics.py#L374)

```python
def entity_search(self, term: str = '', etype: str = '', *, min_confidence: float = 0.0, min_sources: int = 0, limit: int = 50) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `term` | `str` | `''` |  |
| `etype` | `str` | `''` |  |
| `min_confidence` | `float` | `0.0` |  |
| `min_sources` | `int` | `0` |  |
| `limit` | `int` | `50` |  |

**Returns:** `list[dict[str, Any]]`

<a id="fusionanalytics-top_changed"></a>

#### `FusionAnalytics.top_changed`

`method` | [estorides_core/fusion_analytics.py:432](../../estorides_core/fusion_analytics.py#L432)

```python
def top_changed(self, days: int = 7, limit: int = 20) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `days` | `int` | `7` |  |
| `limit` | `int` | `20` |  |

**Returns:** `list[dict[str, Any]]`

<a id="fusionanalytics-source_corroboration_matrix"></a>

#### `FusionAnalytics.source_corroboration_matrix`

`method` | [estorides_core/fusion_analytics.py:477](../../estorides_core/fusion_analytics.py#L477)

```python
def source_corroboration_matrix(self, limit: int = 20) -> list[dict[str, Any]]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `limit` | `int` | `20` |  |

**Returns:** `list[dict[str, Any]]`

---
