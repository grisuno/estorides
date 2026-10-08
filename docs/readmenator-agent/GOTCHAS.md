# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `estorides_core/config.py` (score: 84.60, imported by 41 files)
- `estorides_web.py` (score: 75.40, imported by 7 files)
- `estorides_core/orchestrator.py` (score: 57.80, imported by 8 files)
- `estorides_cli.py` (score: 33.10, imported by 1 files)
- `estorides_core/entity_extraction.py` (score: 30.10, imported by 13 files)
- `estorides_core/cases.py` (score: 22.10, imported by 7 files)
- `estorides_core/fusion_store.py` (score: 21.80, imported by 5 files)
- `estorides_core/tool_runner.py` (score: 21.50, imported by 8 files)
- `static/js/estorides.js` (score: 20.50)
- `estorides_core/web_security.py` (score: 20.20, imported by 9 files)

## Blast Radius (change impact)

Editing these files can break the listed number of dependents. Run their tests after any change.

- `estorides_core/config.py` -- 41 direct, 52 total dependents
- `estorides_core/entity_extraction.py` -- 13 direct, 46 total dependents
- `estorides_core/ids.py` -- 6 direct, 36 total dependents
- `estorides_core/reliability_scoring.py` -- 8 direct, 34 total dependents
- `estorides_core/sqlite_store.py` -- 5 direct, 31 total dependents
- `estorides_core/ssrf_guard.py` -- 7 direct, 30 total dependents
- `estorides_core/tool_runner.py` -- 8 direct, 28 total dependents
- `estorides_core/transliteration.py` -- 2 direct, 25 total dependents
- `estorides_core/entity_resolution.py` -- 4 direct, 24 total dependents
- `estorides_core/knowledge_graph.py` -- 7 direct, 24 total dependents

## Hotspots (complexity + centrality)

- `static/js/estorides.js` -- complexity: 1.0, centrality: 1.0, combined: 1.0
- `estorides_web.py` -- complexity: 0.6, centrality: 0.1, combined: 0.3
- `estorides_core/parsers.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2
- `static/js/source_manager.js` -- complexity: 0.1, centrality: 0.1, combined: 0.1
- `estorides_cli.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `estorides_core/scope.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `estorides_core/entity_resolution.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `estorides_core/system_app_sources.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `estorides_core/config.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `estorides_core/monitoring.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1

## Dependency Cycles

Circular dependencies. Refactor to break the cycle.

- `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`
- `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`
- `estorides_web.py` -> `estorides_web_tools.py` -> `estorides_web.py`

## Layer Violations

- `estorides_web.py` (presentation) -> `estorides_core/fusion_store.py` (data_access): presentation must not import data_access
- `tests/properties/test_csp_safe_styles_properties.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_hardening.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_map_basemap.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_openapi.py` (testing) -> `estorides_web.py` (presentation): testing must not import presentation
- `tests/test_security_remediation.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
