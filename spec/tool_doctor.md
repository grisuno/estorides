# tool_doctor — Spec

## Purpose
The operator must see in one call which Kali/OSINT binaries are
installed, which are missing, which have an install recipe, and which
orchestrator sources depend on each. Previously this required joining
three surfaces by hand (`/api/tools` recipe list, `shutil.which` per
binary, and the `20_system_tools` YAML catalog); orphan recipes (35
with no source) and mis-tagged sources were invisible.

## Inputs
- `sources_dir`: path to `sources/20_system_tools` (defaults to the
  shipped catalog). Each YAML contributes `tool.binary` and its source
  name.

## Outputs
- `doctor() -> {"tools": [ToolStatus...], "summary": {...}}` where each
  entry has `name` (binary), `available` (on PATH), `recipe`
  (recipe exists), `sources` (source names using it), `installable`
  (`not available and recipe`).
- `GET /api/tools/doctor` returns the same shape as JSON.
- Summary: `total`, `available`, `missing`, `installable`.

## Error table
| Condition | Behaviour |
|---|---|
| sources dir absent | `tools` covers recipes only, `sources` empty per entry. |
| Malformed YAML | Skipped; never raises. |
| `shutil.which` raising | Treated as unavailable. |

## Security guarantees
- Read-only: no subprocess, no install, no elevation. Auth and rate
  limiting reuse the existing tools-endpoint decorators.

## Out of scope
- Installing (existing `install_tool`), version checks, apt refresh.

## BDD scenarios
- Given the shipped catalog, when `doctor()` runs, then all 19 system_app binaries appear with their source names.
- Given a binary on PATH (e.g. `sh`), when checked, then `available` is true.
- Given a missing binary with a recipe, when checked, then `installable` is true.
- Given the endpoint, when called authenticated, then it returns `tools` and `summary` keys.
