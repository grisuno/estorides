# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `estorides_core/config.py` (score: 88.90, imported by 43 files)
- `estorides_web.py` (score: 85.70, imported by 9 files)
- `estorides_core/orchestrator.py` (score: 57.80, imported by 8 files)
- `estorides_core/__init__.py` (score: 38.00, imported by 18 files)
- `estorides_cli.py` (score: 33.10, imported by 1 files)
- `estorides_core/entity_extraction.py` (score: 32.10, imported by 14 files)
- `estorides_core/tool_runner.py` (score: 25.50, imported by 10 files)
- `estorides_core/parsers.py` (score: 25.30, imported by 7 files)
- `static/js/estorides.js` (score: 25.20)
- `estorides_core/cases.py` (score: 22.10, imported by 7 files)

## Blast Radius (change impact)

Editing these files can break the listed number of dependents. Run their tests after any change.

- `estorides_core/config.py` -- 43 direct, 51 total dependents
- `estorides_core/entity_extraction.py` -- 14 direct, 50 total dependents
- `estorides_core/ids.py` -- 6 direct, 38 total dependents
- `estorides_core/reliability_scoring.py` -- 8 direct, 36 total dependents
- `estorides_core/sqlite_store.py` -- 5 direct, 33 total dependents
- `estorides_core/ssrf_guard.py` -- 7 direct, 32 total dependents
- `estorides_core/tool_runner.py` -- 10 direct, 32 total dependents
- `estorides_core/__init__.py` -- 18 direct, 29 total dependents
- `estorides_core/aviation.py` -- 4 direct, 29 total dependents
- `estorides_core/aerospace.py` -- 2 direct, 27 total dependents

## Hotspots (complexity + centrality)

- `static/js/estorides.js` -- complexity: 1.0, centrality: 1.0, combined: 1.0
- `static/js/graph_force.js` -- complexity: 0.6, centrality: 0.4, combined: 0.5
- `static/js/graph_bundle.js` -- complexity: 0.3, centrality: 0.3, combined: 0.3
- `estorides_web.py` -- complexity: 0.5, centrality: 0.1, combined: 0.2
- `estorides_core/parsers.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2
- `estorides_core/feeds.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `estorides_core/graph_rag_search.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `static/js/source_manager.js` -- complexity: 0.1, centrality: 0.1, combined: 0.1
- `estorides_cli.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1
- `estorides_core/scope.py` -- complexity: 0.2, centrality: 0.0, combined: 0.1

## Dependency Cycles

Circular dependencies. Refactor to break the cycle.

- `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`
- `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`
- `estorides_web.py` -> `estorides_web_tools.py` -> `estorides_web.py`

## Layer Violations

- `estorides_web.py` (presentation) -> `estorides_core/fusion_store.py` (data_access): presentation must not import data_access
- `tests/properties/test_csp_safe_styles_properties.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_aerospace.py` (testing) -> `estorides_web.py` (presentation): testing must not import presentation
- `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_graph_rag_search.py` (testing) -> `estorides_web.py` (presentation): testing must not import presentation
- `tests/test_hardening.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_map_basemap.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
