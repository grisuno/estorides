# `probabilistic_fusion` — Spec

> Bayesian confidence merging in the fusion store. Replaces the simplistic
> `MAX(conf)` merge policy with the full reliability+credibility+source_type+
> corroboration+freshness model defined in `reliability_scoring`.

---

## Purpose

The fusion store's current merge policy (`MAX(existing, incoming)`) is
pathologically optimistic: a single unreliable source with inflated
confidence can override a well-corroborated existing score. Probabilistic
fusion replaces `MAX()` with the multi-factor confidence pipeline from
:mod:`reliability_scoring`, so that:

* a **primary** authoritative source (WHOIS) can raise a low-confidence
  entity;
* a **tertiary** gossip source cannot override a carefully-sourced existing
  entity;
* **corroboration** (multiple independent sources seeing the same value)
  boosts confidence above any single source;
* **freshness** decay means stale sightings lose weight over time.

The change is confined to `FusionStore.fuse_entity` and
`FusionStore.fuse_relationship` — no new tables, no schema migration, no
breaking change to the read surface.

---

## Invariant

Replacing `MAX()` with `merge_confidence()` is a strict improvement:
`merge_confidence` is **never more optimistic** than `MAX()`, because every
weight is `<= 1.0`. A well-corroborated, fresh, primary-source entity will
retain its high score. A fly-by-night source cannot lift an entity above
what its own intrinsic reliability, credibility, and source-type weight
justify.

Formally:

    merge_confidence(existing, new, ...).score <= max(existing, new)

Empirically: for a fresh, primary-source observation
`merge_confidence(0.0, 1.0, A, 1, primary)` ≈ `1.0` — the same as `MAX`.
For the adversarial case `merge_confidence(0.9, 1.0, F, 6, tertiary)` the
score is the max of `0.9` and the *new* score weighted by all the
pessimistic factors, which is `0.9` — so the bogus source cannot exploit
`MAX()` to overwrite a well-sourced entity.

---

## Changes to `FusionStore.fuse_entity`

Current (line ≈350):

    confidence=MAX(fusion_entities.confidence, excluded.confidence)

New:
1. Extract the source name(s) from the entity dict
2. Look up `reliability_from_name(source)` and `source_type_from_name(source)`
3. Read the existing row's confidence (if any) before the UPSERT
4. Compute `merge_confidence(existing_score, incoming_score, new_reliability,
   new_credibility, new_source_type, corroboration_count=n_sources,
   observation_age_seconds=0.0)` for a re-sighting
5. For a first sighting, compute `compute_confidence(ConfidenceInput(...))`
6. Use the computed `result.score` in the UPSERT instead of the raw entity
   confidence

## Changes to `FusionStore.fuse_relationship`

Current (line ≈475):

    confidence=MAX(fusion_relationships.confidence, excluded.confidence)

Same approach: look up source reliability/type for the source string, use
`merge_confidence` instead of `MAX`.

## Inputs

Same as `FusionStore.fuse_entity` / `FusionStore.fuse_relationship`. No new
parameters. The source name is extracted from `entity.get("sources", [])`
or `entity.get("source", "")` / the relationship's `source` parameter.

## Outputs

Same return types (`str` for entity id, `None` for relationship). The
`confidence` column in `fusion_entities` and `fusion_relationships` now
reflects the multi-factor score instead of the raw `MAX`.

## Error table

| Failure mode | Behaviour |
|---|---|
| No source name available | Falls back to `DEFAULT_RELIABILITY` / `DEFAULT_SOURCE_TYPE` |
| Reliability scoring module unavailable | Falls back to `MAX()` (graceful degradation) |
| Entity with empty type/value | Same as before: returns empty string, no crash |

## BDD scenarios

### PF1 · Primary source scores higher than tertiary

**Given** an entity first seen by a primary authoritative source
(rdap_domain) at 0.9 and a tertiary source (psbdmp_ws) at 0.5  
**When** fused in the store  
**Then** the primary source's confidence contribution dominates because of
its higher A reliability × PRIMARY source type weight, and the tertiary
cannot override due to `merge_confidence` using `max()` over the properly
weighted scores.

### PF2 · Tertiary source cannot override high existing score

**Given** an entity at 0.9 from multiple primary sources  
**When** an `untrusted_webscraper` with reliability F reports the same
entity  
**Then** the fused confidence stays at 0.9 (unchanged).

### PF3 · Cross-observation corroboration lifts score

**Given** an entity seen by 1 source at 0.5  
**When** the same entity is seen by 8 more independent sources (total 9)  
**Then** the fused confidence rises (corroboration_weight >= 0.3 for the
ninth sighting) but never exceeds 1.0.

### PF4 · Merge is monotonic (never decreases)

**Given** an entity at 0.6  
**When** a new observation at 0.4 (lower confidence) arrives  
**Then** the fused confidence stays at 0.6 (never drops).

### PF5 · First sighting uses source-weighted base

**Given** a new entity from `untrusted_webscraper` (reliability F)
at base confidence 1.0  
**When** fused for the first time  
**Then** the stored confidence is <= 0.2 (heavily discounted by F ×
tertiary weights).

### PF6 · Relationship merge uses Bayesian score

**Given** a relationship at 0.8 from a primary source  
**When** the same edge arrives from an untrusted_webscraper at 1.0  
**Then** the fused confidence stays at 0.8 (tertiary source cannot
override).
