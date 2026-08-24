# `observation_models` — Spec (module contract)

> Strict Pydantic v2 schema validation for the observation and entity records
> that flow through the engine. This is the schema-contract layer that turns
> "the orchestrator returns `List[Dict[str, Any]]`" into a validated, typed
> boundary so a missing field, a wrong-typed value, or a hostile payload can
> never be silently propagated downstream into the fusion store, the knowledge
> graph, or the LLM analyst.
>
> The plan (prioritised gap #1, "Crítico Semana 1-2") called for strict schema
> validation. This module delivers it. It is single-process, pure, and does not
> require Redis, Celery, FAISS, or an OTLP collector — it stays inside the
> project doctrine (`CLAUDE.md`: all code runs in one Python process; no
> external binaries; no mandatory external services).

---

## Purpose

Today the engine models observations as unvalidated `Dict[str, Any]` built
inline in `orchestrator.py` (lines ~326-388) and entities as the loose
`Entity` dataclass in `entity_extraction.py`. Every downstream consumer —
`fusion_store.add_observation`, `case_store.add_observation`, the knowledge
graph, `reliability_scoring`, and the LLM analyst — receives a plain dict and
must defensively `.get()` every field, guessing at types. When a parser returns
a wrong-typed `parsed` or a category is dropped, the error is silent: a string
lands where a bool was expected, an `int` where a `float` was expected, and the
run "completes" with subtly corrupted data.

This module provides **strict, validated, versioned data contracts** for:

* `Observation` — the per-source record the orchestrator emits.
* `ObservationMeta` — the `meta` sub-object (status, attempts, cache, proxy).
* `ObservedEntity` — a validated view of a resolved entity used across stores.
* `RunResult` — the top-level run payload (`entities`, `observations`,
  `sources_succeeded`, `error`, …).

Validation is strict (`extra="forbid"` by default for the bounded structs), so
a newly introduced field fails loudly at the boundary instead of being silently
dropped by a consumer that doesn't know about it. Every model offers a
`to_legacy_dict()` projection back to the exact shape the current in-process
call sites consume, so wiring this module in is drop-in.

## Inputs

Each model is a Pydantic v2 `BaseModel` built from a plain dict. Field types and
bounds:

### `ObservationMeta`

| Field | Type | Bounds | Notes |
| --- | --- | --- | --- |
| `url` | `str` | len >= 0 | Truncated to `max_url_len` on input. |
| `method` | `str` | len >= 0 | Normalised to upper. |
| `host` | `str` | len >= 0 | |
| `attempts` | `int` | `>= 0` | Default `0`. |
| `cached` | `bool` | — | Default `False`. |
| `proxied` | `bool` | — | Default `False`. |
| `status` | `int` | `>= 0` | HTTP status or `0`. |
| `content_type` | `str` | len >= 0 | Default `""`. |
| `error` | `str` | len >= 0 | Default `""`. |

Unknown keys in a `meta` dict are **forbidden** (strict schema) — a new field
must be added to the contract, not smuggled through.

### `Observation`

| Field | Type | Bounds | Notes |
| --- | --- | --- | --- |
| `source` | `str` | len in `[1, max_str_len]` | Required. |
| `category` | `str` | len in `[0, max_str_len]` | Default `""`. |
| `description` | `str` | len in `[0, max_str_len]` | Default `""`. |
| `parser` | `str` | len in `[0, max_str_len]` | Default `""`. |
| `parsed` | `Any` | JSON-safe | Optional; `None` for error observations. |
| `raw` | `Any` | JSON-safe | Optional. |
| `meta` | `ObservationMeta` | — | Required. |
| `observed_at` | `float` | `>= 0.0` | Optional; epoch seconds. |
| `ontology` | `dict[str, Any]` | JSON-safe | Optional. |
| `mitre` | `dict[str, Any]` | JSON-safe | Optional. |

### `ObservedEntity`

| Field | Type | Bounds | Notes |
| --- | --- | --- | --- |
| `type` | `str` | len in `[1, max_str_len]` | Required. |
| `value` | `str` | len in `[1, max_value_len]` | Required. |
| `source` | `str` | len in `[0, max_str_len]` | Default `""`. |
| `context` | `str` | len in `[0, max_str_len]` | Default `""`. |
| `confidence` | `float` | `[0.0, 1.0]` | Default `1.0`. |
| `attributes` | `dict[str, Any]` | JSON-safe | Default `{}`. |
| `sources` | `list[str]` | each len <= `max_str_len` | Default `[]`. |

### `RunResult`

| Field | Type | Bounds | Notes |
| --- | --- | --- | --- |
| `entities` | `list[ObservedEntity]` | — | Default `[]`. |
| `observations` | `list[Observation]` | — | Default `[]`. |
| `sources_succeeded` | `int` | `>= 0` | Default `0`. |
| `error` | `str` | len in `[0, max_str_len]` | Optional. |

## Outputs

Every model provides:

* Pydantic `model_validate(dict)` — parse + validate, raising `ValidationError`
  with structured `errors()` on the first bad field.
* `to_legacy_dict()` — a plain `dict` projecting back to the exact shape the
  current in-process call sites produce (drops `extra` defaults, keeps nulls
  out of `meta.error`, etc.).
* Strict coercion only within the documented bounds: an out-of-range value
  **fails**, it is never silently clamped (except `meta.status`/`attempts` are
  clamped from `int`/`float` with `>= 0` enforced by validation, not clamping).

### Example `Observation.to_legacy_dict()`

```json
{
  "source": "crt.sh",
  "category": "DNS",
  "description": "CT log",
  "parser": "json",
  "parsed": ["example.com"],
  "raw": null,
  "meta": {"url": "https://crt.sh", "method": "GET", "host": "crt.sh",
           "attempts": 1, "cached": false, "proxied": true,
           "status": 200, "content_type": "application/json", "error": ""},
  "observed_at": 1700000000.0
}
```

## Error table

| Failure mode | Behaviour |
| --- | --- |
| Dict with a missing required field (`source`, `value`, `meta`, …) | `pydantic.ValidationError`, field listed in `errors()`. |
| `meta` dict with an unknown key | `ValidationError` (extra forbidden). |
| Wrong type (e.g. `status="200"` string, `attempts=-1`) | `ValidationError`. |
| `confidence` outside `[0.0, 1.0]` | `ValidationError`. |
| `observed_at` negative | `ValidationError`. |
| Oversized `url` | Truncated to `max_url_len` (documented, bounded), never fails. |
| Oversized `value` (> `max_value_len`) | `ValidationError` (an entity value is identity-bearing; truncation would corrupt it). |
| Non-JSON-safe `parsed`/`raw`/`attributes` (e.g. a set, an object) | `ValidationError`. |
| Empty input `None`/`""` | `ValidationError` (type error: not an object). |

## Security guarantees

1. **Pure.** All validation is pure: no disk, no network, no time-of-day reads,
   no input mutation, no logging of field contents. Same input → same result.
2. **No hostile-content logging.** `url`, `source`, `parsed` are never logged
   by this module. Truncation of `url` is a documented bound, not a logging
   channel.
3. **Bounded cost.** A single pass per field; field-length caps (`max_str_len`,
   `max_value_len`, `max_url_len`) prevent a hostile 10 MB string from being
   retained as-is in a validated record. `url` is truncated; `value` (identity
   bearing) is rejected, never processed further.
4. **Fail-loud at the boundary.** Validation errors carry a machine-readable
   `errors()` payload (field path + type), never an exception message that
   echoes untrusted input. `ValidationError` never stringifies hostile content
   into a log line by itself.
5. **Strict by default.** `extra="forbid"` on the bounded structs means a
   schema drift is a loud, traceable failure at the boundary, not a silent
   no-op downstream.
6. **Type-safe identity.** `value` and `source` are the merge/identity keys for
   downstream fusion; validating them as bounded non-empty strings prevents a
   `None` or a multi-MB blob from corrupting the `canonical_id` derivation.

## Out of scope

- **Wiring this module into `orchestrator.py` / `fusion_store.py`.** The wire-up
  is the next PR after this one closes, with regression tests. This spec does
  not change any call site.
- **Replacing the `Entity` dataclass.** `ObservedEntity` is a validated view; the
  engine's internal `Entity` dataclass stays as-is until the wire-up PR.
- **Redis/Celery/FAISS/OpenTelemetry.** Deliberately excluded (doctrine).
- **Schema versioning/migrations.** A single `SCHEMA_VERSION` constant is
  exposed; no migration framework is added.
- **Cross-model referential checks** (e.g. every `entities` source must exist in
  `observations`). That is an analysis concern, out of scope here.
- **Serialising to DB columns.** This module only validates and projects dicts.

---

## BDD scenarios (Given-When-Then)

> Contracts. Change only with explicit agreement. Each translates to an
> executable test in `tests/test_observation_models.py`.

### O1 · Happy path: a full observation validates (ATDD)

**Given** a dict shaped like a real orchestrator observation (source, category,
description, parser, parsed, raw, meta with status/cached/proxied/attempts,
observed_at, ontology, mitre)  
**When** I call `Observation.model_validate(dict)`  
**Then** it succeeds  
**And** `to_legacy_dict()` returns the same keys the orchestrator emits  
**And** `meta.method` is uppercased.

### O2 · Edge: error observation (parsed=None) validates

**Given** an observation dict with `parsed=None`, `raw=None`, and
`meta.error="circuit_open"`  
**When** I call `Observation.model_validate(dict)`  
**Then** it succeeds  
**And** `parsed is None`.

### O3 · Error: missing required field fails loudly

**Given** an observation dict missing `source`  
**When** I call `Observation.model_validate(dict)`  
**Then** it raises `pydantic.ValidationError`  
**And** `errors()[0]["loc"]` includes `"source"`.

### O4 · Error: unknown meta key is forbidden

**Given** a `meta` dict with a key the contract does not declare (e.g.
`"sneaky_field"`)  
**When** I call `ObservationMeta.model_validate(dict)`  
**Then** it raises `pydantic.ValidationError`.

### O5 · Error: wrong-typed field fails

**Given** an observation with `meta.status="200"` (string, not int)  
**When** I call `Observation.model_validate(dict)`  
**Then** it raises `pydantic.ValidationError`.

### O6 · Security: hostile/boundary inputs are bounded, never echoed

**Given** a `url` of 10 000 characters and a `value` of 10 000 characters  
**When** I validate them  
**Then** the `url` is truncated to `max_url_len` without failing  
**And** the oversized `value` raises `pydantic.ValidationError`  
**And** the validation error message does not embed the full hostile string.

### O7 · Edge: confidence bounds are enforced

**Given** an `ObservedEntity` with `confidence=1.5` and another with
`confidence=-0.1`  
**When** I call `ObservedEntity.model_validate` on each  
**Then** both raise `pydantic.ValidationError`.

### O8 · RunResult aggregates nested models

**Given** a run dict with a list of entity dicts, a list of observation dicts,
`sources_succeeded=3`  
**When** I call `RunResult.model_validate(dict)`  
**Then** it succeeds  
**And** `entities[0]` is an `ObservedEntity`  
**And** `observations[0]` is an `Observation`  
**And** `to_legacy_dict()` round-trips the top-level keys.

### O9 · Property-based invariant (hypothesis)

**Given** any observation/entity dict whose scalar fields respect the declared
ranges  
**When** I validate it and project it with `to_legacy_dict()`  
**Then** re-validating the projected dict succeeds (round-trip stability)  
**And** `confidence` stays in `[0.0, 1.0]`  
**And** no projected field exceeds the declared length caps.

(Implemented in `tests/properties/test_observation_models_properties.py`.)

---

## Cierre del módulo

- **Fecha de cierre:** 2026-08-23.
- **Estado:** cerrado (O1–O9 verdes + invariantes de propiedad).
- **Validación:**
  - `pytest tests/test_observation_models.py` → 24 passed
  - `pytest tests/properties/test_observation_models_properties.py` → 4 passed
    (4 invariantes × 1000 ejemplos = ~4000 casos fuzzing)
  - `ruff check` → All checks passed
  - `mypy --strict` → no issues
  - `bandit -r` → 0 High, 0 Medium
  - `mutmut run` → **79/79 mutantes muertos, 0 supervivientes, 0 timeout**
- **Cambios al motor que este módulo habilita:**
  - Proporciona el contrato de datos validado que el PR siguiente wire-ea en
    `orchestrator.py` / `fusion_store.py` / `case_store.py` con tests de
    regression.
- **Lista de cambios:**
  - Creado: `estorides_core/observation_models.py` (Pydantic v2 estricto:
    `ObservationMeta`, `Observation`, `ObservedEntity`, `RunResult` +
    `_check_json_safe` recursivo para JSON-safety).
  - Creado: `tests/test_observation_models.py` (24 BDD/security).
  - Creado: `tests/properties/test_observation_models_properties.py`
    (4 invariantes, hypothesis).
  - Añadido: `SchemaConfig`/`SCHEMA` en `estorides_core/config.py`
    (límites centralizados, env-var-tunable, nada hardcodeado).
  - Añadido: `pydantic>=2.0,<3.0` a `requirements.txt` y `pyproject.toml`.
  - Añadido: sección `[tool.mutmut]` a `pyproject.toml` (mutación como parte
    del ciclo de cierre de módulo).
  - Boy-scout: los mutantes supervivientes iniciales (8) revelaron que la
    garantía de seguridad "JSON-safe" del spec no estaba testeada; se añadieron
    9 tests de seguridad (objetos arbitrarios, bytes, set, keys no-string,
    anidados en listas, mensajes de error exactos) hasta alcanzar 79/79.
- **Doctrina:** confirmado que la mutación es parte del ciclo de cierre de
  módulo (ver `CLAUDE.md` §5, hitos cerrados).
