# Gotchas

## God Nodes (high connectivity)

These files have the most connections. Changes here have high blast radius.

- `estorides_core/config.py` (score: 78.60)
- `estorides_web.py` (score: 62.70)
- `estorides_core/orchestrator.py` (score: 47.30)
- `estorides_cli.py` (score: 31.10)
- `estorides_core/entity_extraction.py` (score: 27.90)
- `estorides_core/tool_runner.py` (score: 21.50)
- `estorides_core/fusion_store.py` (score: 20.20)
- `estorides_core/discoverer.py` (score: 20.10)
- `static/js/estorides.js` (score: 19.80)
- `estorides_core/knowledge_graph.py` (score: 19.70)

## Hotspots (complexity + centrality)

- `static/js/estorides.js` -- complexity: 1.0, centrality: 1.0, combined: 1.0
- `estorides_web.py` -- complexity: 0.6, centrality: 0.1, combined: 0.3
- `tests/test_target_management.py` -- complexity: 0.5, centrality: 0.0, combined: 0.2
- `tests/test_socmint.py` -- complexity: 0.5, centrality: 0.0, combined: 0.2
- `tests/test_entity_resolution.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2
- `tests/test_reliability_scoring.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2
- `estorides_core/parsers.py` -- complexity: 0.4, centrality: 0.0, combined: 0.2
- `tests/test_security_remediation.py` -- complexity: 0.3, centrality: 0.0, combined: 0.1
- `tests/test_source_health_monitoring.py` -- complexity: 0.3, centrality: 0.0, combined: 0.1
- `tests/test_system_app_sources.py` -- complexity: 0.3, centrality: 0.0, combined: 0.1

## Layer Violations

- `_test_entity_resolution.py` (testing) -> `estorides_core/entity_extraction.py` (presentation): testing must not import presentation
- `_test_people.py` (testing) -> `estorides_core/entity_extraction.py` (presentation): testing must not import presentation
- `estorides_web.py` (presentation) -> `estorides_core/fusion_store.py` (data_access): presentation must not import data_access
- `estorides_web.py` (presentation) -> `estorides_core/transforms.py` (data_access): presentation must not import data_access
- `tests/properties/test_csp_safe_styles_properties.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_auth_gate.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_csp_safe_styles.py` (testing) -> `estorides_core/web_security.py` (presentation): testing must not import presentation
- `tests/test_encrypted_export.py` (testing) -> `estorides_core/entity_extraction.py` (presentation): testing must not import presentation
