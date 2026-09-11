# `ids` — deterministic content-addressed identifiers

**Spec version:** 1.0
**Date:** 2026-09-11
**Status:** closed

---

## Purpose

Six modules hand-rolled `sha1(payload, usedforsecurity=False)[:16]` for
deduplication ids. `stable_id` is the single implementation so the idiom
(and the `usedforsecurity=False` intent) lives in one place.

## Inputs

- `payload: str` — UTF-8 content. Callers own the shape
  (`f"{type}:{normalized}"`, `"|".join([...])`, …).
- `length: int = 16` — hex prefix length.

## Outputs

`str` — lowercase hex digest prefix of `length` characters.

## Error table

| Modo | Comportamiento |
| --- | --- |
| `payload` no-str | `AttributeError` (error de programación; tipo anotado) |
| `length <= 0` | `""` (slice vacío) |
| `length > 40` | digest completo (40 chars) |

## Security guarantees

- SHA-1 se usa como **content hash**, nunca como primitiva de seguridad;
  `usedforsecurity=False` lo declara explícitamente (y evita el bloqueo en
  modo FIPS).

## Out of scope

- Unicidad criptográfica; la colisión en 16 chars se acepta por diseño.

## BDD scenarios

### ID1 [Happy path] Determinista
Given the same payload
When `stable_id` is called twice
Then the ids are equal and match the legacy sha1 prefix.

### ID2 [Edge] Longitud
Given `length=8`
Then the returned id has 8 chars.

### ID3 [Happy path] Distintos
Given two different domains
Then their ids differ.
