# `estorides_core.intel_resolver`

> Source: [estorides_core/intel_resolver.py:1](../../estorides_core/intel_resolver.py#L1) | language `py` | coverage 50.0% | [API index](../index.md)

estorides_core.intel_resolver ============================= Cross-feed entity resolver.

Inspired by Osiris' `intel/server.js` (simplifaisoul/osiris), the resolver is the single entry point that takes a `(type, id)` pair and returns nodes + edges connecting it across every feed we have a primitive for:

type=ip         -> ASN, ISP, organisation, country (Wikidata + IP-API)
  type=domain     -> registrant org, ASN, country, sanctions cross-check
  type=company    -> parent org, country, sanctions (Wikidata + OFAC SDN)
  type=person     -> employer, nationality, sanctions (Wikidata + OFAC SDN)
  type=country    -> region, neighbours, risk score
  type=cve        -> affected vendors, exploits (NVD/EPSS cross-check)

The resolver never *fetches* the source. It composes the local cache
([`SanctionsIndex`](estorides_core.ontology.py.md#sanctionsindex), [`WikidataCache`](estorides_core.ontology.py.md#wikidatacache)) with on-demand SPARQL queries
when a node is missing. The orchestrator's post-process stage can
call this once per significant entity and wire the result into the
knowledge graph + Kuzu backend.

Public surface:

    resolver = EntityResolver()
    out = resolver.resolve("ip", "1.2.3.4")
    out = resolver.resolve("company", "Acme Corp")
    out = resolver.resolve("person", "Vladimir Putin")

Return shape (matches Osiris' [`nodes`](static.js.graph_force.js.md#nodes)/[`links`](static.js.graph_force.js.md#links) for drop-in reuse):

    {
      "type": "ip", "id": "1.2.3.4",
      "root_id": "ip:1.2.3.4",
      "nodes": [
        {"id": "ip:1.2.3.4", "label": "1.2.3.4", "type": "ip", "kind": "ip", "properties": {...}},
        {"id": "company:Cloudflare", "label": "Cloudflare", "type": "company", ...},
        ...
      ],
      "links": [
        {"source": "ip:1.2.3.4", "target": "company:Cloudflare", "relation": "hosted_by"},
        ...
      ],
      "sources": ["ip-api.com", "wikidata", "ofac_sdn"],
      "fetched_at": 1700000000.0,
    }

Adding a new resolver is one method + a decorator. No central
registry to edit; the [`resolve`](#entityresolver-resolve) dispatcher uses a small typed
table.

## Contents

- **Classes:** [`EntityResolver`](#entityresolver)
- **Constants:** [`WIKIDATA_ENDPOINT`](#wikidata_endpoint), [`WIKIDATA_UA`](#wikidata_ua), [`IP_API_URL`](#ip_api_url), [`RIPE_STAT_URL`](#ripe_stat_url), [`VT_API_BASE`](#vt_api_base), [`VT_KEY_ENV`](#vt_key_env), [`CACHE_TTL`](#cache_ttl), [`CACHE_MAX`](#cache_max)

## Classes

<a id="entityresolver"></a>

### `EntityResolver`

`class` | [estorides_core/intel_resolver.py:156](../../estorides_core/intel_resolver.py#L156)

```python
class EntityResolver
```

Cross-feed entity resolution.

Composes Wikidata SPARQL, the OFAC SDN index (via the existing
`OntologyEngine.sanctions`), and a couple of free IP-intel
services into a single response shape suitable for both the UI
(entity graph panel) and the orchestrator (knowledge graph
enrichment).

**Members**

| Member | Kind | Summary |
|---|---|---|
| [`__init__`](#entityresolver-__init__) | constructor |  |
| [`resolve`](#entityresolver-resolve) | method |  |

<a id="entityresolver-__init__"></a>

#### `EntityResolver.__init__`

`constructor` | [estorides_core/intel_resolver.py:165](../../estorides_core/intel_resolver.py#L165)

```python
def __init__(self) -> None
```

<a id="entityresolver-resolve"></a>

#### `EntityResolver.resolve`

`method` | [estorides_core/intel_resolver.py:174](../../estorides_core/intel_resolver.py#L174)

```python
def resolve(self, ent_type: str, ent_id: str) -> Dict[str, Any]
```

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `ent_type` | `str` |  |  |
| `ent_id` | `str` |  |  |

**Returns:** `Dict[str, Any]`

---

## Constants

<a id="wikidata_endpoint"></a>

### `WIKIDATA_ENDPOINT`

`constant` | [estorides_core/intel_resolver.py:70](../../estorides_core/intel_resolver.py#L70)

```python
WIKIDATA_ENDPOINT = 'https://query.wikidata.org/sparql'
```

---

<a id="wikidata_ua"></a>

### `WIKIDATA_UA`

`constant` | [estorides_core/intel_resolver.py:71](../../estorides_core/intel_resolver.py#L71)

```python
WIKIDATA_UA = 'Estorides/1.0 (+open-source OSINT platform; cross-feed resolver)'
```

---

<a id="ip_api_url"></a>

### `IP_API_URL`

`constant` | [estorides_core/intel_resolver.py:72](../../estorides_core/intel_resolver.py#L72)

```python
IP_API_URL = 'https://ip-api.com/json/{ip}'
```

---

<a id="ripe_stat_url"></a>

### `RIPE_STAT_URL`

`constant` | [estorides_core/intel_resolver.py:73](../../estorides_core/intel_resolver.py#L73)

```python
RIPE_STAT_URL = 'https://stat.ripe.net/data/whois/data.json?resource={ip}'
```

---

<a id="vt_api_base"></a>

### `VT_API_BASE`

`constant` | [estorides_core/intel_resolver.py:74](../../estorides_core/intel_resolver.py#L74)

```python
VT_API_BASE = 'https://www.virustotal.com/api/v3'
```

---

<a id="vt_key_env"></a>

### `VT_KEY_ENV`

`constant` | [estorides_core/intel_resolver.py:75](../../estorides_core/intel_resolver.py#L75)

```python
VT_KEY_ENV = 'VT_API_KEY'
```

---

<a id="cache_ttl"></a>

### `CACHE_TTL`

`constant` | [estorides_core/intel_resolver.py:77](../../estorides_core/intel_resolver.py#L77)

```python
CACHE_TTL = 24 * 60 * 60
```

---

<a id="cache_max"></a>

### `CACHE_MAX`

`constant` | [estorides_core/intel_resolver.py:78](../../estorides_core/intel_resolver.py#L78)

```python
CACHE_MAX = 5000
```

---
