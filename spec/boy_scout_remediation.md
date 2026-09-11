# Boy-Scout Remediation — Architecture & Quality Audit

**Spec version:** 1.0
**Date:** 2026-09-11
**Status:** closed (round 1)

---

## Purpose

A repository-wide senior architecture/quality audit was performed, followed by
the boy-scout doctrine cycle (fix bugs, remove dead code, close security gaps,
unify duplicated logic, never lose functionality). This spec records the
findings, the fixes shipped, and the prioritized backlog that remains. It is
the contract for the remediation round.

Baseline before remediation: **816 tests green**, ruff/mypy/bandit not clean.
After: **861 tests green** (+45), bandit 0 High/Medium, all changed Python
files lint/type clean.

---

## Architecture summary (as found)

- **One Flask factory, zero blueprints.** `estorides_web.create_app()` is a
  single ~1481-line function holding 64 routes; business logic (graph
  analytics, exports, SSE framing) lives in handlers. No service layer.
- **Two-layer core.** `estorides_core/` (I/O + pipeline + stores) and thin
  adapters `estorides_llm/`, `estorides_export/`. Persistence is four
  hand-rolled SQLite stores with duplicated plumbing.
- **Contract modules** (`observation_models`, `reliability_scoring`,
  `ssrf_guard`, `validation`) are the sound parts; the debt concentrates in
  `parsers.py`, `orchestrator.run`, `recon_report`, `config.py`, the front-end
  controller, and `create_app`.

## Anti-patterns found (and status)

| # | Finding | Location | Status |
| --- | --- | --- | --- |
| A1 | `estorides watch add` hard-broken (`AttributeError` + `NameError`) | `estorides_cli.py` | **fixed** |
| A2 | Malformed env var crashes the whole process at import | `config.py` | **fixed** |
| A3 | Parser totality contract violated by 26/54 parsers | `parsers.py` | **fixed** |
| A4 | Dead `_flat`/`_first` helpers | `parsers.py` | **removed** |
| A5 | `hidden` attribute + `display:!important` made 8 UI surfaces unreachable | `estorides.js` / `estorides_ui.css` | **fixed** |
| A6 | Unescaped remote data into `innerHTML` (XSS) | `estorides.js` | **fixed** |
| A7 | TLP:AMBER hardcoded in executive summary | `recon_report.py` | **fixed** |
| A8 | Multi-doc YAML silently dropped, dup name corrupts counts, unknown contact not normalised | `source_loader.py` | **fixed** |
| A9 | Fuzzy merge picked the *least*-observed canonical | `entity_extraction.py` | **fixed** |
| A10 | `types=[]` silently scanned everything | `entity_extraction.py` | **fixed** |
| A11 | Unreachable SSRF IPv4-in-IPv6 branch | `ssrf_guard.py` | **removed** |
| A12 | `_diff_section` KeyError on partial rows | `report.py` | **fixed** |
| A13 | Weak SHA1 flagged by bandit (non-security hash) | `fusion_store.py`, `entity_resolution.py` | **fixed** |
| A14 | SQL f-string false positives | `entity_store.py`, `fusion_store.py` | **annotated** |
| A15 | Documented `ESTORIDES_PASSIVE_ONLY` / `ESTORIDES_PARALLEL` envs ignored | `orchestrator.py` | **fixed** |
| A16 | Dead constants `LLM_BACKENDS`, `LLM_DEFAULT_TASK` | `config.py` | **removed** |
| A17 | God function `create_app` (64 routes), no blueprints | `estorides_web.py` | **backlog** |
| A18 | `Orchestrator.run` 488 lines, `_execute_source` 159 lines | `orchestrator.py` | **backlog** |
| A19 | Four duplicated SQLite stores (`_init_schema`/`_tx`/`close`) | stores | **backlog** |
| A20 | Reliability weights / stable-id / env-readers duplicated across modules | core | **backlog** |

## Shipped changes (round 1)

- `estorides_cli.py` — import `SCHEDULER_ENABLED`/`WatchTarget`, OPSEC flags on
  `watch add`, public `WatchScheduler.has_runner`, dropped duplicate imports.
- `config.py` — all numeric/bool readers fault-tolerant; `_env_bool` warns on
  unknown tokens; CSV keys stripped; dead constants removed.
- `parsers.py` — dead helpers deleted; `_d`/`_list`/`_text`/`_first_dict`
  guards added; all 54 parsers total under property fuzzing.
- `source_loader.py` — `safe_load_all`, list documents, duplicate-name category
  cleanup, unknown-contact → `active`, per-file decode guard.
- `recon_report.py` — `classification` threaded into `build_executive_summary`.
- `entity_extraction.py` — canonical prefers most-observed; `types=None` vs
  `types=[]`; loop-closure binding.
- `estorides.js` — `setVisible()` clears the `hidden` attribute; escape
  `type`/`source`; escape fusion-detail fields and whitelist intel level.
- `estorides_ui.css` — removed malformed rule, fixed `--err` → `--danger`.
- Security annotations for bandit (B310/B324/B608) with justification.

## New tests

`tests/test_cli_watch.py`, `tests/test_config_env.py`, `tests/test_parsers.py`,
`tests/properties/test_parsers_properties.py` (1000 examples),
`tests/test_source_loader.py`, `tests/test_entity_extraction.py`,
`tests/test_ui_visibility.py`, plus recon-report classification regression.

## Backlog (prioritized)

**High:** split `create_app` into blueprints + a services container
(`provides()`/`api_error()` decorators remove ~40 duplicated 503 guards and the
raw-exception leaks); stage `Orchestrator.run`; move blocking
`intel_resolver.resolve` off the event loop.
**Medium:** extract a shared `SqliteStore` base; unify stable-id / normalisation
/ reliability-weight / env-reader helpers; one SSE builder; drop dead CSS and
orphaned root tests into `tests/`.
**Low:** `recon_report` TLP metadata shape, STIX `ipv6-addr`, CI to cover
`estorides_cli.py` + `estorides_llm`.
