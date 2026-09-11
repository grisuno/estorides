# `sqlite_store` — shared SQLite store plumbing

**Spec version:** 1.0
**Date:** 2026-09-11
**Status:** closed

---

## Purpose

The four hand-rolled SQLite repositories (`monitoring.WatchStore`,
`cases.CaseStore`, `entity_store.EntityStore`, `fusion_store.FusionStore`)
carried byte-identical copies of connection setup, `_init_schema`, `_tx`
and `close`. This module is the single source of truth for that plumbing so
a fix (e.g. a pragma, a rollback guard) is made once. It also carries
`DictMixin` for the dataclasses whose `to_dict` was literally `asdict(self)`.

## Inputs

- `path: Optional[Path]` — database file. `None` falls back to the
  subclass's `_DEFAULT_PATH` class attribute.
- Subclass class attributes:
  - `_DDL: tuple[str, ...] | list[str]` — schema statements, idempotent.
  - `_DEFAULT_PATH: Optional[Path]`.
  - `_PRAGMAS: tuple[str, ...]` — defaults to `journal_mode=WAL` +
    `foreign_keys=ON`.

## Outputs

- `SqliteStore(path).path -> Path` (parent directory created).
- `store._conn -> sqlite3.Connection` (isolation_level=None).
- `store._tx()` — context manager yielding the connection inside a
  `BEGIN`/`COMMIT`, rolling back on any exception.
- `store.close()` — closes the connection, never raises.
- `DictMixin.to_dict() -> dict` — `asdict(self)`.

## Error table

| Modo | Comportamiento |
| --- | --- |
| path `None` y `_DEFAULT_PATH` `None` | `ValueError("SqliteStore requires a path or _DEFAULT_PATH")` |
| `_tx` body raises | `ROLLBACK` propagado, excepción original re-lanzada |
| `close` sobre conexión ya cerrada | se traga el error (idempotente) |
| DDL inválido | excepción de `sqlite3` propaga (error de programación) |

## Security guarantees

- No `eval`/`exec`, no SQL construido con input externo. El DDL es estático.
- Conexión serializada bajo `threading.Lock` → sin escrituras entrelazadas.

## Out of scope

- Migraciones de esquema (los stores declaran `CREATE TABLE IF NOT EXISTS`).
- Pool de conexiones; un store = una conexión.

## BDD scenarios

### SS1 [Happy path] Schema created
Given a subclass with `_DDL` and `_DEFAULT_PATH`
When the store is constructed with no path
Then `path` equals `_DEFAULT_PATH` and every DDL statement is applied.

### SS2 [Edge] Transaction commits
Given an open store
When `_tx` is used to insert a row and exits cleanly
Then the row is visible.

### SS3 [Error] Transaction rolls back
Given an open store
When `_tx` raises inside the block
Then the change is not persisted and the original exception propagates.

### SS4 [Security] Close is idempotent
Given an open store
When `close()` is called twice
Then no exception is raised.

### SS5 [Happy path] DictMixin
Given a dataclass inheriting `DictMixin`
When `to_dict()` is called
Then it returns the `asdict` representation.
