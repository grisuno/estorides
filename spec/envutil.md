# `envutil` — fault-tolerant environment readers

**Spec version:** 1.0
**Date:** 2026-09-11
**Status:** closed

---

## Purpose

`config`, `web_security` and `source_health_monitoring` each carried a
private `_env_int` / `_env_float` / `_env_bool`. `envutil` is the single
implementation so the "malformed value → default + log, never crash" rule
is enforced once.

## Inputs

- `name: str`, `default: int|float|bool|tuple[str, ...]`.
- Environment variable named `name`.

## Outputs

- `env_int(name, default) -> int`
- `env_float(name, default) -> float`
- `env_bool(name, default) -> bool` (truthy: `1/true/yes/on`; falsy: `0/false/no/off`)
- `env_csv(name, default=()) -> tuple[str, ...]`

## Error table

| Modo | Comportamiento |
| --- | --- |
| var ausente o vacía | `default` |
| int/float malformado | log WARNING, `default` |
| bool desconocido | log WARNING, `default` |
| csv con tokens vacíos | se filtran |

## Security guarantees

- Nunca ejecuta `eval`, nunca loguea el valor de secretos (solo el nombre y el
  valor crudo de la var numérica/bool que falló, que no es un secreto).

## Out of scope

- Cargar `.env`; los lectores solo leen el entorno del proceso.

## BDD scenarios

### EU1 [Happy path] Parse válido
Given `ESTORIDES_X=42` When `env_int` is called Then returns 42.

### EU2 [Error] Malformado
Given `ESTORIDES_X=abc` When `env_int` is called Then returns default and logs.

### EU3 [Edge] Bool desconocido
Given `ESTORIDES_X=maybe` When `env_bool(name, True)` is called Then returns True (default).

### EU4 [Edge] CSV
Given `ESTORIDES_X="a, b ,,c"` Then `env_csv` returns `("a","b","c")`.
