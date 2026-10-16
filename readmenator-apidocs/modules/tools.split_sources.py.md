# `tools.split_sources`

> Source: [tools/split_sources.py:1](../../tools/split_sources.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

Split legacy grouped source files into one addon per file.

Reads every multi-document ``sources/NN_xxx.yaml`` and writes each source as
``sources/NN_xxx/<name>.yaml``, then removes the original grouped file. The
runtime loader recurses, so the tree is picked up automatically (lazyaddons
style). Re-running is safe: existing per-addon files are overwritten in place.

## Contents

- **Functions:** [`main`](#main)
- **Constants:** [`SOURCES_DIR`](#sources_dir)

## Functions

<a id="main"></a>

### `main`

`function` | [tools/split_sources.py:19](../../tools/split_sources.py#L19)

```python
def main() -> int
```

**Returns:** `int`

---

## Constants

<a id="sources_dir"></a>

### `SOURCES_DIR`

`constant` | [tools/split_sources.py:16](../../tools/split_sources.py#L16)

```python
SOURCES_DIR = Path(__file__).resolve().parent.parent / 'sources'
```

---
