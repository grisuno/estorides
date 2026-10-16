# `estorides_core.graph_kuzu`

> Source: [estorides_core/graph_kuzu.py:1](../../estorides_core/graph_kuzu.py#L1) | language `py` | coverage 77.8% | [API index](../index.md)

estorides_core.graph_kuzu ========================= Persistent graph backend powered by Kuzu (embedded Cypher DB).

Why Kuzu and not just another NetworkX dump:
  NetworkX on disk is read whole on every request. Kuzu gives us
  indexed Cypher queries so we can ask "every entity connected to <id>
  within 2 hops" without reloading the world. We still keep NetworkX
  as the in-memory working graph (the orchestrator depends on it for
  per-run traversal) — this module mirrors every write to a Kuzu
  database on disk so cross-run intelligence queries become fast.

Schema mirrors the in-memory graph's node kinds:

  Entity nodes: Domain, IPv4, IPv6, Email, URL, Person, Org,
                ASN, CVE, GHSA, BTCAddress, ETHAddress, Phone,
                Hash (md5/sha1/sha256/bitcoin_tx), MAC, UserAgent,
                Country, Sanction
  Source nodes: one node per OSINT source

  Edges:
    OBSERVED_BY   (Entity -> Source)   "this source produced this entity"
    CO_OCCURS     (Entity -> Entity)   "appeared in the same response"
    RESOLVED_TO   (Domain -> IPv4)     "DNS resolution"
    REGISTERED_BY (Domain -> Org)      "WHOIS registrant"
    HAS_CVE       (IP -> CVE)          "vulnerability on this host"
    LOCATED_IN    (Entity -> Country)  "geolocated entity"
    SANCTIONED    (Entity -> Sanction) "OFAC SDN match"
    SAME_AS       (Entity -> Entity)   "fuzzy cluster"

Public surface:
    kg = KuzuGraphBackend(path)
    kg.upsert_entity(type, value, source, **attrs)
    kg.upsert_relationship(src_type, src_value, rel, dst_type, dst_value, **attrs)
    kg.neighbors(node_id, hops=1, relation=None) -> [{node, edge}, ...]
    kg.cypher(query, params=None) -> rows
    kg.close()

## Contents

- **Classes:** [`KuzuGraphBackend`](#kuzugraphbackend)
- **Constants:** [`KUZU_PATH`](#kuzu_path)

## Call Graph

Solid arrows stay in this module, dashed arrows leave it.

```mermaid
flowchart LR
    n_estorides_core_graph_kuzu_py__KuzuGraphBackend_neighbors(["KuzuGraphBackend.neighbors"])
    n_estorides_core_graph_kuzu_py__KuzuGraphBackend_cypher(["KuzuGraphBackend.cypher"])
    n_estorides_core_graph_kuzu_py__KuzuGraphBackend_neighbors --> n_estorides_core_graph_kuzu_py__KuzuGraphBackend_cypher
```

## Classes

<a id="kuzugraphbackend"></a>

### `KuzuGraphBackend`

`class` | [estorides_core/graph_kuzu.py:196](../../estorides_core/graph_kuzu.py#L196)

```python
class KuzuGraphBackend
```

Thread-safe Kuzu wrapper for the Estorides knowledge graph.

The orchestrator calls this alongside the in-memory NetworkX graph.
Writes are synchronous but cheap; reads (Cypher) are also synchronous
and roughly match NetworkX traversal cost for 2-hop queries while
being dramatically faster at cross-run joins.

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#kuzugraphbackend-__init__) | constructor |  |
| [`upsert_entity`](#kuzugraphbackend-upsert_entity) | method | Insert (or merge) an entity. |
| [`upsert_relationship`](#kuzugraphbackend-upsert_relationship) | method | Insert an edge between two entities. |
| [`neighbors`](#kuzugraphbackend-neighbors) | method | Return nodes reachable from `node_id` within `hops` edges. |
| [`cypher`](#kuzugraphbackend-cypher) | method | Run a Cypher query and return rows as a list of dicts. |
| [`stats`](#kuzugraphbackend-stats) | method | Return counts of every node label and edge rel type. |
| [`close`](#kuzugraphbackend-close) | method |  |

<a id="kuzugraphbackend-__init__"></a>

#### `KuzuGraphBackend.__init__`

`constructor` | [estorides_core/graph_kuzu.py:205](../../estorides_core/graph_kuzu.py#L205)

```python
def __init__(self, path: Optional[Path] = None) -> None
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `path` | `Optional[Path]` | `None` |  |

<a id="kuzugraphbackend-upsert_entity"></a>

#### `KuzuGraphBackend.upsert_entity`

`method` | [estorides_core/graph_kuzu.py:245](../../estorides_core/graph_kuzu.py#L245)

```python
def upsert_entity(self, ent_type: str, value: str, source: Optional[str] = None, **attrs: Any) -> str
```

Insert (or merge) an entity.

Returns its canonical node id.

If `source` is given we also wire an OBSERVED_BY edge so we
can later ask "which sources saw this entity?".

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ent_type` | `str` |  |  |
| `value` | `str` |  |  |
| `source` | `Optional[str]` | `None` |  |
| `**attrs` | `Any` |  |  |

**Returns:** `str`

<a id="kuzugraphbackend-upsert_relationship"></a>

#### `KuzuGraphBackend.upsert_relationship`

`method` | [estorides_core/graph_kuzu.py:295](../../estorides_core/graph_kuzu.py#L295)

```python
def upsert_relationship(self, src_type: str, src_value: str, rel: str, dst_type: str, dst_value: str, **attrs: Any) -> None
```

Insert an edge between two entities.

Unknown relations are silently skipped — every edge type
that matters is mapped in _RELATION_TO_EDGE.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `src_type` | `str` |  |  |
| `src_value` | `str` |  |  |
| `rel` | `str` |  |  |
| `dst_type` | `str` |  |  |
| `dst_value` | `str` |  |  |
| `**attrs` | `Any` |  |  |

<a id="kuzugraphbackend-neighbors"></a>

#### `KuzuGraphBackend.neighbors`

`method` | [estorides_core/graph_kuzu.py:346](../../estorides_core/graph_kuzu.py#L346)

```python
def neighbors(self, node_id: str, hops: int = 1, relation: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]
```

Return nodes reachable from `node_id` within `hops` edges.

[`relation`](estorides_core.graph_rag_search.py.md#ragrelation-relation) optionally filters to a single edge label.
Returns a list of dicts with whatever columns the query names.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `node_id` | `str` |  |  |
| `hops` | `int` | `1` |  |
| `relation` | `Optional[str]` | `None` |  |
| `limit` | `int` | `100` |  |

**Returns:** `List[Dict[str, Any]]`

**Raises**

- `ValueError`: (raised in the body, not documented)

*Calls:* [`KuzuGraphBackend.cypher`](#kuzugraphbackend-cypher)

<a id="kuzugraphbackend-cypher"></a>

#### `KuzuGraphBackend.cypher`

`method` | [estorides_core/graph_kuzu.py:379](../../estorides_core/graph_kuzu.py#L379)

```python
def cypher(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]
```

Run a Cypher query and return rows as a list of dicts.

Column names are taken from the RETURN clause. Missing
columns (e.g. `m.kind` on a node that was never enriched) come
back as None so callers don't have to special-case.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` |  |  |
| `params` | `Optional[Dict[str, Any]]` | `None` |  |

**Returns:** `List[Dict[str, Any]]`

*Called by:* [`KuzuGraphBackend.neighbors`](#kuzugraphbackend-neighbors)

<a id="kuzugraphbackend-stats"></a>

#### `KuzuGraphBackend.stats`

`method` | [estorides_core/graph_kuzu.py:406](../../estorides_core/graph_kuzu.py#L406)

```python
def stats(self) -> Dict[str, Any]
```

Return counts of every node label and edge rel type.

**Returns:** `Dict[str, Any]`

<a id="kuzugraphbackend-close"></a>

#### `KuzuGraphBackend.close`

`method` | [estorides_core/graph_kuzu.py:436](../../estorides_core/graph_kuzu.py#L436)

```python
def close(self) -> None
```

---

## Constants

<a id="kuzu_path"></a>

### `KUZU_PATH`

`constant` | [estorides_core/graph_kuzu.py:57](../../estorides_core/graph_kuzu.py#L57)

```python
KUZU_PATH: Path
```

---
