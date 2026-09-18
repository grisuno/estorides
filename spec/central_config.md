# central_config — Spec

## Purpose
`Orchestrator.run` and `tool_install` carry hardcoded timeouts and a
crash-prone `int(os.environ...)` parse that duplicate (and drift from)
the central `config.py`. A malformed
`ESTORIDES_TOOL_INSTALL_TIMEOUT=abc` currently kills the import;
`run(timeout=12.0, deadline=30.0)` ignores `HTTP_TIMEOUT`; the LLM
`+3.0` backstop and the system_app `300` fallback exist only as
literals; the template-env allowlist is a hardcoded tuple.

## Inputs
- Env vars (all optional, all fault-tolerant via `envutil`):
  `ESTORIDES_TIMEOUT`, `ESTORIDES_RUN_DEADLINE`,
  `ESTORIDES_LLM_BACKSTOP_S`, `ESTORIDES_TOOL_TIMEOUT`,
  `ESTORIDES_TOOL_INSTALL_TIMEOUT`, `ESTORIDES_TOOL_INSTALL_MAX_OUTPUT`,
  `ESTORIDES_TEMPLATE_ENVS`.

## Outputs
- `config.RUN_DEADLINE`, `config.LLM_BACKSTOP_S`,
  `config.TOOL_INSTALL_TIMEOUT_S`, `config.TOOL_INSTALL_MAX_OUTPUT_BYTES`,
  `config.TEMPLATE_ENVS` (tuple).
- `Orchestrator.run` defaults track `HTTP_TIMEOUT`/`RUN_DEADLINE`;
  system_app fallback uses `TOOL_TIMEOUT`; template envs come from
  `TEMPLATE_ENVS`.
- `tool_install` limits come from config; malformed env falls back to
  defaults instead of raising at import.

## Error table
| Condition | Behaviour |
|---|---|
| Malformed numeric env | Default used; no raise at import or call. |
| Caller passes explicit timeout/deadline | Explicit value wins over config. |

## Security guarantees
- No new env intake beyond the named vars; output caps unchanged.

## Out of scope
- intel_resolver/osiris literal tables (separate slice).

## BDD scenarios
- Given `ESTORIDES_TOOL_INSTALL_TIMEOUT=abc`, when importing `tool_install`, then import succeeds with the default.
- Given defaults, when reading config, then `RUN_DEADLINE == 30.0` and `LLM_BACKSTOP_S == 3.0`.
- Given `run` signature, when inspected, then defaults equal `HTTP_TIMEOUT` and `RUN_DEADLINE`.
- Given `TEMPLATE_ENVS`, when read, then it contains the four legacy names.
