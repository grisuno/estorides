# orchestrator_fanout — Spec

## Purpose
The Orchestrator fanout must execute every selected source exactly once,
report every source exactly once, and never duplicate method definitions.
This spec closes three defects found in audit: duplicated method trio,
result/source misalignment after the deadline path, and the missing
`on_source_done` signal for `system_app` sources.

## Inputs
- `targets: list[Source]`, ordered registry selection.
- `http_sources`, `sys_sources`: partition of `targets` by `tool.binary`.
- `tasks`: asyncio tasks, one per HTTP source, in `http_sources` order.
- `bg_tasks`: asyncio tasks, one per system_app source, in `sys_sources` order.
- Callbacks `on_source_done(name, ok, status, elapsed_ms)` and
  `on_source_result(obs)`; either may be `None`.

## Outputs
- `normalised: list[(source, parsed, raw, meta)]` with one entry per
  target, each entry carrying its own originating `source`.
- Exactly one `on_source_done` call per target when the callback is set.
- Exactly one definition each of `_extract_cursor`, `_infer_relationships`,
  `_write_dataset` on the `Orchestrator` class object.

## Error table
| Condition | Behaviour |
|---|---|
| HTTP task raises | Error observation `exception:<Cls>`, `on_source_done(name, False, ...)`. Run continues. |
| HTTP task returns non-4-tuple | Error observation `bad-result-shape:<Cls>`. Run continues. |
| Deadline exceeded | Pending HTTP tasks cancelled, reported `deadline_exceeded`, `on_source_done` fired for each. Slow system_app tasks keep running detached. |
| system_app tool missing/fails | Error observation with `TOOL_NOT_FOUND`/exit code, `on_source_done` fired with `ok=False`. Never raises. |
| Subscriber callback raises | Swallowed; run continues. |

## Security guarantees
- No new I/O or subprocess surface. Callbacks never break the run.
- Error detail strings are data only, never executed.

## Out of scope
- Query type detection, pagination semantics, LLM analysis, persistence.

## BDD scenarios
- Given one HTTP source raising ValueError, when the fanout normalises results, then one error observation with `exception:ValueError` is produced and no exception escapes.
- Given a task returning a non-tuple, when normalised, then `bad-result-shape` is reported for that source only.
- Given two HTTP sources plus one system_app source, when all succeed, then three normalised entries carry their own source names in order and `on_source_done` fires three times.
- Given a system_app source that fails, when it completes, then `on_source_done` fires with `ok=False` and the observation carries the tool error code.
