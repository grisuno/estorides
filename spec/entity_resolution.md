# `entity_resolution` — Spec

> Canonical identity layer. Collapses near-duplicate and cross-script
> entities into stable canonical identities with deterministic ids,
> provenance, and auditable match methods. Replaces the v1.1 engine
> that used ``difflib.SequenceMatcher`` with type-aware normalisation,
> blocking, Jaro-Winkler scoring, and a consonant-skeleton cross-script
> booster for names.

---

## Purpose

The entity resolution module transforms a per-run list of observed
:class:`Entity` records into a list of :class:`CanonicalEntity` records,
each with:

* a **stable canonical id** derived from a type-aware normalised form,
  so the same real-world entity gets the same id on every run;
* **blocked, scored matching** — exact normalised equality is a
  deterministic merge; close-but-not-equal pairs inside the same blocking
  bucket are scored with Jaro-Winkler (and a cross-script consonant
  skeleton booster) and either merged or surfaced as a ``SAME_AS``
  candidate link;
* **provenance** — the sources, original surface forms (aliases),
  scripts, and the match method/score that justified each merge.

Deterministic types (IP, hash, CVE, ASN, crypto address) never fuzzy
match: equality of the normalised form is the only merge rule.

---

## Inputs

### `Entity` (from entity_extraction)

| Field | Type | Notes |
|-------|------|-------|
| `type` | `str` | Entity type (person, org, ipv4, domain, ...) |
| `value` | `str` | Surface form value |
| `source` | `str` | Source that produced this entity |
| `sources` | `List[str]` | All sources (preferred over `source`) |
| `confidence` | `float` | Confidence score `[0, 1]` |
| `context` | `str` | Surrounding text context |
| `attributes` | `Dict` | Extensible metadata |

### `resolve_entities(entities, *, store=None)`

| Parameter | Type | Default | Notes |
|-----------|------|---------|-------|
| `entities` | `List[Entity]` | required | Per-run entity list |
| `store` | `Optional[EntityStore]` | `None` | Cross-run persistent store |

### `EntityResolver.__init__(merge_threshold, link_threshold, max_bucket, store)`

| Parameter | Type | Range | Default |
|-----------|------|-------|---------|
| `merge_threshold` | `float` | `[0, 1]` | `ER_MERGE_THRESHOLD` (0.92) |
| `link_threshold` | `float` | `[0, 1]` | `ER_LINK_THRESHOLD` (0.84) |
| `max_bucket` | `int` | `>= 1` | `ER_MAX_BUCKET` (400) |
| `store` | `Optional[EntityStore]` | — | `None` |

## Outputs

### `ResolutionResult`

```json
{
  "entities": [
    {
      "canonical_id": "person:a1b2c3d4e5f6g789",
      "type": "person",
      "value": "Vladimir Putin",
      "normalized": "putin vladimir",
      "confidence": 0.85,
      "sources": ["wikidata", "ofac", "leak_db"],
      "aliases": ["Vladimir Putin", "Владимир Путин", "Putin, Vladimir"],
      "scripts": ["latin", "non-latin"],
      "member_count": 3,
      "match_method": "exact",
      "match_score": 1.0,
      "attributes": {
        "also_known_as": ["Владимир Путин", "Putin, Vladimir"],
        "cross_script": true
      }
    }
  ],
  "same_as": [
    {"left": "domain:abc123", "right": "domain:def456", "score": 0.88, "method": "jaro_winkler"}
  ]
}
```

| Field | Type | Meaning |
|-------|------|---------|
| `entities` | `List[CanonicalEntity]` | Fused canonical entities |
| `same_as` | `List[SameAsLink]` | Sub-threshold candidate links |

### Match methods

| Method | Score range | Meaning |
|--------|-------------|---------|
| `exact` | 1.0 | Normalised equality (deterministic) |
| `jaro_winkler` | `[0, 1]` | Jaro-Winkler string similarity |
| `consonant_skeleton` | >= 0.94 | Cross-script consonant match |
| `skeleton_jaro` | `[0, 1]` | Averaged Jaro + skeleton similarity |
| `deterministic_mismatch` | 0.0 | Deterministic type, different value |

## Type-specific merge policy

| Type | Deterministic / Fuzzy | Merge-eligible? | Notes |
|------|----------------------|-----------------|-------|
| `ipv4`, `ipv6`, `ip` | Deterministic | No | Exact normalised form only |
| `md5`, `sha1`, `sha256`, ... | Deterministic | No | Exact normalised form only |
| `cve` | Deterministic | No | Case-normalised, otherwise exact |
| `asn` | Deterministic | No | AS-prefix normalised |
| `btc_address`, `eth_address` | Deterministic | No | Exact match |
| `mac` | Deterministic | No | Exact match |
| `domain` | Fuzzy | No | Near-match → SAME_AS, never merge |
| `email` | Fuzzy | No | Near-match → SAME_AS, never merge |
| `person` | Fuzzy | Yes | Auto-merge above threshold |
| `org`, `organization` | Fuzzy | Yes | Auto-merge, suffix-stripped |
| `username` | Fuzzy | Yes | Auto-merge |
| `keyword` | Fuzzy | Yes | Auto-merge |

## Error table

| Failure mode | Behaviour |
|---|---|
| Empty entity list | Empty `ResolutionResult` returned |
| Entity with blank value | Skipped (no crash) |
| Entity with `None` value | Skipped, no crash |
| EntityStore unavailable | Falls back to in-run resolution only |

## BDD scenarios

### ER1 · Cross-script person fusion

**Given** entities for "Vladimir Putin", "Владимир Путин", and
"Putin, Vladimir" from different sources  
**When** I run `resolve_entities`  
**Then** all three fuse into one `CanonicalEntity` with `member_count=3`  
**And** `aliases` contains all three surface forms  
**And** `attributes.cross_script` is True.

### ER2 · Domain case variant merges exactly

**Given** entities for "evilcorp.com" and "EvilCorp.com"  
**When** I run `resolve_entities`  
**Then** they merge into one entity with `member_count=2`  
**And** `match_method == "exact"`.

### ER3 · Look-alike domains surface as SAME_AS

**Given** entities for "evilcorp.com" and "evil-corp.com" (not variants)  
**When** I run `resolve_entities`  
**Then** they remain separate entities  
**And** a `SameAsLink` exists between them with `method == "jaro_winkler"`.

### ER4 · Deterministic type never fuzzy matches

**Given** two md5 entities differing by one character  
**When** I run `resolve_entities`  
**Then** they remain separate entities with `member_count=1` each  
**And** no `SameAsLink` exists between them.

### ER5 · Identical IPs merge

**Given** "8.8.8.8" from two different sources  
**When** I run `resolve_entities`  
**Then** they merge into one entity with `member_count=2`.

### ER6 · Near IPs never fuse

**Given** "8.8.8.8" and "8.8.4.4"  
**When** I run `resolve_entities`  
**Then** they remain separate.

### ER7 · Org suffix folding

**Given** entities for "Evil Corp LLC" and "Evil Corp"  
**When** I run `resolve_entities`  
**Then** they merge into one entity with `member_count=2`.

### ER8 · Distinct persons stay separate

**Given** entities for "Vladimir Putin" and "Dmitry Medvedev"  
**When** I run `resolve_entities`  
**Then** they remain separate, each with `member_count=1`.

### ER9 · Canonical entity to_dict roundtrip

**Given** a resolved entity  
**When** I call `to_dict()` and reconstruct from dict  
**Then** all fields are preserved (within rounding tolerance).

### ER10 · Empty input returns empty

**Given** an empty entity list  
**When** I run `resolve_entities([])`  
**Then** `entities == []` and `same_as == []`.

### ER11 · Canonical id is deterministic

**Given** the same `(type, normalized)` pair  
**When** I compute `canonical_id` twice  
**Then** both calls return the same string.

### ER12 · Different normalised yields different id

**Given** two different `(type, normalized)` pairs  
**When** I compute their `canonical_id`  
**Then** the results differ.
