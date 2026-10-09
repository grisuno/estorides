# Project Memory

> Cross-session context for agents. Sections 1-6 are regenerated from the source tree with zero LLM tokens: declared rules are quoted verbatim with `file:line`, measured baselines come from the scan. Section 7 is written by agents and humans and is preserved across rebuilds.

Generated from 160 files at commit `d4bf14f6d178`. Read this first, then `readmenator-wiki/index.md`, then `readmenator . ask "<question>"` for anything specific.

## 1. Purpose and domain

- What it is: From the creators of LazyOwn Redteam Framework comes a free and open-source (`README.md:16`)
- Domain vocabulary (term, files): `estorides` (115), `not` (66), `run` (65), `source` (64), `single` (50), `bdd` (50), `one` (49), `sources` (46), `entity` (42), `same` (40), `module` (40), `name` (39), `type` (39), `result` (39), `error` (39)
- Subsystem `estorides_core: estorides_web`: 27 files, core `estorides_web.py`: estorides.web
- Subsystem `estorides_core: parsers`: 23 files, core `estorides_core/parsers.py`: estorides_core.parsers
- Subsystem `estorides_core: config`: 22 files, core `estorides_core/config.py`: estorides.config
- Subsystem `estorides_core: hypothesis_engine`: 19 files, core `estorides_core/hypothesis_engine.py`: estorides_core.hypothesis_engine
- Subsystem `estorides_core: people_intel`: 15 files, core `estorides_core/people_intel.py`
- Subsystem `estorides_core: estorides`: 14 files, core `static/js/estorides.js`: Estorides front-end controller
- Subsystem `estorides_core: tool_install`: 10 files, core `estorides_core/tool_install.py`: estorides_core.tool_install
- Subsystem `estorides_core: entity_resolution`: 8 files, core `estorides_core/entity_resolution.py`: estorides_core.entity_resolution
- Business rules that the code cannot show live in section 7: record them there.

## 2. Workflow

Detected commands:
- `python -m pytest -q` (pyproject.toml)
- `estorides --help` (pyproject.toml [project.scripts])
- `CI workflow ci.yml` (.github/workflows/ci.yml)
- `CI workflow static.yml` (.github/workflows/static.yml)

Session protocol:
1. Start: read this file, then `readmenator . fresh` (exit 1 means run `readmenator . --rebuild`).
2. Orient: `readmenator-wiki/index.md`; for a question use `readmenator . ask "<question>"` (local = entities + sources, `--global` = community reports).
3. Before editing a file: `grep -n '<file>' readmenator-agent/GOTCHAS.md readmenator-agent/SECURITY.md`.
4. After the change: run the tests above, then `readmenator . --rebuild` so the maps, wiki, and this file stay true.
5. End: record decisions, business rules, and gotchas with `readmenator . remember "<note>" --kind decision`.

## 3. Rules and constraints

Declared:
- none declared in instruction files (add them to AGENTS.md or record them in section 7)

Measured baseline:
- Security findings at medium or above: 0 (see `readmenator-agent/SECURITY.md`); do not add new ones.
- Dependency cycles: 3; layer violations: 16 (see `readmenator-agent/GOTCHAS.md`).

## 4. Style norms

Declared:
- none declared in instruction files (add them to AGENTS.md or record them in section 7)

Measured baseline:
- py: 155 files, 2581 symbols; docstrings on 33% of symbols; functions snake_case (100%); types PascalCase (100%); median file 160 lines, max 1732.
- js: 3 files, 252 symbols; docstrings on 25% of symbols; functions camelCase (72%); types PascalCase (0%); median file 941 lines, max 3250.
- sh: 2 files, 2 symbols; docstrings on 50% of symbols; functions snake_case (100%); median file 100 lines, max 100.
- Tests: 78 files under tests, tests/properties; follow the existing naming (e.g. `conftest.py`).

## 5. Minimum deliverables

Declared:
- none declared in instruction files (add them to AGENTS.md or record them in section 7)

Measured baseline:
- Tests pass: `python -m pytest -q`.
- Docstring coverage stays at or above 32%.
- No new security findings at medium or above (current: 0).
- No new dependency cycles (current: 3).
- Files stay under 300 lines where possible (`readmenator . lint`).
- Docs refreshed: `readmenator . --rebuild`, and decisions recorded in section 7.

## 6. Risks to respect

- God nodes (changes ripple widely): `estorides_core/config.py`, `estorides_web.py`, `estorides_core/orchestrator.py`, `estorides_cli.py`, `estorides_core/entity_extraction.py`
- Hotspots (complex and central): `static/js/estorides.js`, `static/js/graph_force.js`, `estorides_web.py`, `tests/test_target_management.py`, `tests/test_security_remediation.py`
- Cycle: `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`
- Cycle: `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`
- Cycle: `estorides_web.py` -> `estorides_web_tools.py` -> `estorides_web.py`
- Full blast radius: `readmenator-agent/GOTCHAS.md`; findings: `readmenator-agent/SECURITY.md`.

## 7. Session log (preserved across rebuilds)

Append with `readmenator . remember "<note>" --kind <kind>` (kinds: business, decision, rule, workflow, style, deliverable, gotcha, todo, note) or the MCP tool `readmenator.remember`. Record business rules, decisions and their reasons, workflow changes, and anything the next session must not rediscover.

<!-- readmenator:memory:notes:begin -->
<!-- readmenator:memory:notes:end -->
