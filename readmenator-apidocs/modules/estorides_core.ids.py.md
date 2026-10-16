# `estorides_core.ids`

> Source: [estorides_core/ids.py:1](../../estorides_core/ids.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides_core.ids ================== Deterministic content-addressed identifiers.

Six modules (fusion_store, entity_resolution, recon_fusion,
change_detection, hypothesis_engine, target_management) each hand-rolled the
same `sha1(payload.encode("utf-8"), usedforsecurity=False).hexdigest()[:16]`
idiom. SHA-1 here is a content hash for deduplication, **not** a security
primitive, hence `usedforsecurity=False` (also silences FIPS-mode concerns).

[`stable_id`](#stable_id) is the single implementation. Callers own the payload shape
(`f"{type}:{normalized}"`, `"|".join([...])`, …) so existing ids are
byte-for-byte preserved.

## Contents

- **Functions:** [`stable_id`](#stable_id)

## Functions

<a id="stable_id"></a>

### `stable_id`

`function` | [estorides_core/ids.py:21](../../estorides_core/ids.py#L21)

```python
def stable_id(payload: str, length: int = 16) -> str
```

Deterministic hex id of `length` chars for a UTF-8 payload.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `payload` | `str` |  |  |
| `length` | `int` | `16` |  |

**Returns:** `str`

*Called by:* [`canonical_id`](estorides_core.entity_resolution.py.md#canonical_id), [`entity_id`](estorides_core.fusion_store.py.md#entity_id)

---
