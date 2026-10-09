# GraphRAG Community Reports

Entities: 3171 | Relationships: 9472 | Communities: 11 | Themes: 4 | Text units: 3038

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

162 files in 11 communities and 4 themes. Highest-impact communities: estorides_core: config (7.0), estorides_core: estorides_web (4.1), estorides_core: parsers (3.9). God nodes: estorides_core/config.py, estorides_web.py, estorides_core/orchestrator.py, estorides_cli.py, estorides_core/entity_extraction.py.

- [estorides_core: config] rating 7.0: `estorides_core/config.py` ranks 1 by PageRank, 50 importers, 26 symbols: estorides.config
- [estorides_core: estorides_web] rating 4.1: `estorides_web.py` ranks 1 by PageRank, 11 importers, 95 symbols: estorides.web
- [estorides_core: parsers] rating 3.9: `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- [estorides_core: estorides] rating 3.5: `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 7 symbols: estorides_core.sqlite_store
- [estorides_core: hypothesis_engine] rating 2.7: `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- [estorides_core: people_intel] rating 2.0: `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- [estorides_core: tool_install] rating 1.6: `estorides_core/tool_runner.py` ranks 1 by PageRank, 9 importers, 15 symbols.
- [estorides_core: entity_resolution] rating 1.6: `estorides_core/entity_extraction.py` ranks 1 by PageRank, 15 importers, 21 symbols: estorides_core.entity_extraction
- Key entities: file:tests/test_security_remediation.py, file:estorides_core/config.py, file:estorides_web.py, sym:estorides_web.py::create_app@256, file:tests/test_socmint.py, file:estorides_core/parsers.py
- Children: t0, t1, t2, t3
- Root rating = highest community rating.

## estorides_core: config + estorides_core: estorides_web +6 (`t0`, theme, rating 7.0)

Theme of 8 communities and 133 files: estorides_core: config (19 files, rating 7.0); estorides_core: estorides_web (26 files, rating 4.1); estorides_core: parsers (26 files, rating 3.9); estorides_core: estorides (22 files, rating 3.5); estorides_core: hypothesis_engine (15 files, rating 2.7); estorides_core: tool_install (10 files, rating 1.6); estorides_core: entity_resolution (7 files, rating 1.6); estorides_export (8 files, rating 1.4).

- [estorides_core: config] `estorides_core/config.py` ranks 1 by PageRank, 50 importers, 26 symbols: estorides.config
- [estorides_core: config] `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- [estorides_core: estorides_web] `estorides_web.py` ranks 1 by PageRank, 11 importers, 95 symbols: estorides.web
- [estorides_core: estorides_web] `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- [estorides_core: parsers] `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- [estorides_core: parsers] `estorides_core/parsers.py` ranks 2 by PageRank, 8 importers, 65 symbols: estorides_core.parsers
- [estorides_core: estorides] `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 7 symbols: estorides_core.sqlite_store
- [estorides_core: estorides] `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- Key entities: file:tests/test_security_remediation.py, file:estorides_core/config.py, file:estorides_web.py, sym:estorides_web.py::create_app@256, file:tests/test_socmint.py, file:estorides_core/parsers.py, file:static/js/estorides.js, file:estorides_core/scope.py
- Children: c3, c0, c1, c2, c4, c6, c8, c7
- Theme rating = highest child community rating.

## estorides_core: people_intel (`t1`, theme, rating 2.0)

Theme of 1 communities and 15 files: estorides_core: people_intel (15 files, rating 2.0).

- [estorides_core: people_intel] `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- [estorides_core: people_intel] `estorides_core/code_exposure.py` ranks 2 by PageRank, 2 importers, 10 symbols.
- Key entities: file:tests/test_code_exposure.py, file:tests/test_cloud_asset_discovery.py
- Children: c5
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 1.0)

Theme of 1 communities and 11 files: unassigned files (11 files, rating 1.0).

- [unassigned files] `_multi_test.sh` ranks 1 by PageRank, 0 importers, 0 symbols.
- [unassigned files] `install.sh` ranks 2 by PageRank, 0 importers, 2 symbols: Bootstrap a venv and install the runtime + optional test dependencies.
- Key entities: file:tests/test_target_management.py, file:static/js/graph_force.js
- Children: c10
- Theme rating = highest child community rating.

## estorides_core: source_health_monitoring (`t3`, theme, rating 0.4)

Theme of 1 communities and 3 files: estorides_core: source_health_monitoring (3 files, rating 0.4).

- [estorides_core: source_health_monitoring] `estorides_core/source_health_monitoring.py` ranks 1 by PageRank, 2 importers, 14 symbols: estorides_core.source_health_monitoring
- [estorides_core: source_health_monitoring] `tests/properties/test_source_health_monitoring_properties.py` ranks 2 by PageRank, 0 importers, 7 symbols: Property-based invariants for estorides_core.source_health_monitoring.
- Key entities: file:tests/test_source_health_monitoring.py, sym:estorides_core/source_health_monitoring.py::SourceHealthInput@98
- Children: c9
- Theme rating = highest child community rating.

## estorides_core: config (`c3`, community, rating 7.0)

19 files under estorides_core (py 19), mostly testing. Core file estorides_core/config.py (PageRank 0.1468, imported by 50 files): estorides.config Key abstractions: CacheConfig, PivotPolicyConfig, PivotConfig, StreamConfig, ReconFusionConfig, SchemaConfig. Depends on estorides_core: estorides_web (1), estorides_core: parsers (1), estorides_core: estorides (1). Used by estorides_core: parsers (12), estorides_core: estorides (9), estorides_core: estorides_web (8).

- `estorides_core/config.py` ranks 1 by PageRank, 50 importers, 26 symbols: estorides.config
- `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- `estorides_core/__init__.py` ranks 3 by PageRank, 10 importers, 0 symbols: estorides_core.__init__
- Hotspot `tests/test_security_remediation.py`: 67 symbols, 56 connections (score 0.18).
- Hotspot `tests/test_monitoring.py`: 35 symbols, 13 connections (score 0.09).
- 1 layer violations, e.g. test_security_remediation.py (testing) -> web_security.py (presentation).
- Taint: 18 paths reach this group via requests, urllib.request.
- Key entities: file:tests/test_security_remediation.py, file:estorides_core/config.py, file:tests/test_monitoring.py, file:tests/test_observation_models.py, file:estorides_core/pivot_engine.py, file:estorides_core/async_client.py, file:estorides_core/feeds.py, file:estorides_core/alerter.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 42.

## estorides_core: estorides_web (`c0`, community, rating 4.1)

26 files under tests (py 26), mostly testing. Core file estorides_web.py (PageRank 0.0218, imported by 11 files): estorides.web Key abstractions: deco, wrapper, stop, should_stop, status, done. Depends on estorides_core: estorides (12), estorides_core: config (8), estorides_core: parsers (6). Used by estorides_core: estorides (2), estorides_core: config (1), estorides_core: hypothesis_engine (1).

- `estorides_web.py` ranks 1 by PageRank, 11 importers, 95 symbols: estorides.web
- `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- `estorides_core/search_telemetry.py` ranks 3 by PageRank, 5 importers, 22 symbols: estorides.search_telemetry.
- Hotspot `estorides_web.py`: 95 symbols, 106 connections (score 0.27).
- Hotspot `estorides_core/graph_rag_search.py`: 44 symbols, 9 connections (score 0.11).
- Dependency cycle: estorides_web.py -> estorides_web_tools.py -> estorides_web.py.
- 15 layer violations, e.g. estorides_web.py (presentation) -> fusion_store.py (data_access).
- Surprising bridge: app.py <-> test_change_detection_properties.py (6 hops across communities).
- Key entities: file:estorides_web.py, sym:estorides_web.py::create_app@256, sym:estorides_web.py::_rate_limit_decorator@190, file:estorides_core/web_security.py, file:estorides_core/graph_rag_search.py, sym:estorides_web.py::_provides@81, file:estorides_core/search_telemetry.py, sym:estorides_core/graph_rag_search.py::search@644
- Rating 4.1/10 = 7 x PageRank share 0.58 + 3 x risk 0.00. Internal imports: 41.

## estorides_core: parsers (`c1`, community, rating 3.9)

26 files under estorides_core (py 26), mostly utility. Core file estorides_core/orchestrator.py (PageRank 0.0110, imported by 13 files): estorides_core.orchestrator Key abstractions: Orchestrator, pending_system_app_tasks, repl, run, parse_dns_json, parse_crtsh_json. Depends on estorides_core: config (12), estorides_core: estorides (4), estorides_core: tool_install (4). Used by estorides_core: estorides_web (6), estorides_core: estorides (3), estorides_core: config (1).

- `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- `estorides_core/parsers.py` ranks 2 by PageRank, 8 importers, 65 symbols: estorides_core.parsers
- `estorides_core/intel_resolver.py` ranks 3 by PageRank, 4 importers, 26 symbols: estorides_core.intel_resolver
- Hotspot `tests/test_socmint.py`: 72 symbols, 17 connections (score 0.18).
- Hotspot `estorides_core/parsers.py`: 65 symbols, 14 connections (score 0.16).
- Taint: 2 paths reach this group via requests.
- Key entities: file:tests/test_socmint.py, file:estorides_core/parsers.py, sym:estorides_core/system_app_sources.py::execute@396, file:tests/test_system_app_sources.py, file:estorides_core/orchestrator.py, file:estorides_core/system_app_sources.py, file:tests/test_pagination.py, file:estorides_core/ontology.py
- Rating 3.9/10 = 7 x PageRank share 0.56 + 3 x risk 0.00. Internal imports: 60.

## estorides_core: estorides (`c2`, community, rating 3.5)

22 files under estorides_core (py 21, js 1), mostly utility. Core file estorides_core/sqlite_store.py (PageRank 0.0149, imported by 5 files): estorides_core.sqlite_store Key abstractions: SqliteStore, DictMixin, close, to_dict, CaseStore, fts_available. Depends on estorides_core: config (9), estorides_core: parsers (3), estorides_core: entity_resolution (3). Used by estorides_core: estorides_web (12), estorides_core: parsers (4), estorides_core: config (1).

- `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 7 symbols: estorides_core.sqlite_store
- `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- `estorides_core/monitoring.py` ranks 3 by PageRank, 18 importers, 26 symbols: estorides_core.monitoring
- Hotspot `static/js/estorides.js`: 165 symbols, 1559 connections (score 1.00).
- Hotspot `estorides_cli.py`: 31 symbols, 70 connections (score 0.10).
- 1 layer violations, e.g. test_hardening.py (testing) -> web_security.py (presentation).
- Key entities: file:static/js/estorides.js, file:estorides_core/scope.py, file:estorides_cli.py, file:tests/test_fusion_analytics.py, file:estorides_core/monitoring.py, file:estorides_core/discoverer.py, file:estorides_core/cases.py, file:estorides_core/fusion_store.py
- Rating 3.5/10 = 7 x PageRank share 0.50 + 3 x risk 0.00. Internal imports: 43.

## estorides_core: hypothesis_engine (`c4`, community, rating 2.7)

15 files under tests (py 15), mostly testing. Core file estorides_core/reliability_scoring.py (PageRank 0.0215, imported by 15 files): estorides_core.reliability_scoring Key abstractions: SourceReliability, Credibility, SourceType, ConfidenceInput, ConfidenceResult, compute_confidence. Depends on estorides_core: config (3), estorides_core: estorides_web (1). Used by estorides_core: estorides (2), estorides_core: parsers (1), estorides_core: entity_resolution (1).

- `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- `estorides_core/ids.py` ranks 2 by PageRank, 6 importers, 1 symbols: estorides_core.ids
- `estorides_core/recon_fusion.py` ranks 3 by PageRank, 4 importers, 19 symbols: estorides_core.recon_fusion
- Hotspot `tests/test_reliability_scoring.py`: 70 symbols, 6 connections (score 0.17).
- Hotspot `tests/test_change_detection.py`: 43 symbols, 6 connections (score 0.11).
- Surprising bridge: test_change_detection_properties.py <-> test_recon_report.py (7 hops across communities).
- Key entities: file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py, file:tests/test_change_detection.py, file:tests/test_recon_fusion.py, file:tests/test_hypothesis_engine.py, file:estorides_core/recon_fusion.py, sym:estorides_core/change_detection.py::detect_changes@284, sym:estorides_core/reliability_scoring.py::compute_confidence@312
- Rating 2.7/10 = 7 x PageRank share 0.38 + 3 x risk 0.00. Internal imports: 25.

## estorides_core: people_intel (`c5`, community, rating 2.0)

15 files under estorides_core (py 15), mostly utility. Core file estorides_core/cloud_asset_discovery.py (PageRank 0.0062, imported by 3 files). Key abstractions: CloudAsset, CloudAssetDiscoveryResult, CloudAssetDiscoveryError, to_dict, to_dict, generate_bucket_names.

- `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- `estorides_core/code_exposure.py` ranks 2 by PageRank, 2 importers, 10 symbols.
- `estorides_core/pdns_monitor.py` ranks 3 by PageRank, 3 importers, 11 symbols.
- Hotspot `tests/test_code_exposure.py`: 21 symbols, 3 connections (score 0.05).
- Hotspot `tests/test_cloud_asset_discovery.py`: 18 symbols, 5 connections (score 0.05).
- Key entities: file:tests/test_code_exposure.py, file:tests/test_cloud_asset_discovery.py, file:tests/test_people_intel.py, file:tests/test_pdns_monitor.py, file:tests/test_tech_fingerprint.py, file:tests/test_supply_chain.py, file:tests/test_vuln_correlation.py, file:estorides_core/supply_chain.py
- Rating 2.0/10 = 7 x PageRank share 0.29 + 3 x risk 0.00. Internal imports: 16.

## estorides_core: tool_install (`c6`, community, rating 1.6)

10 files under tests (py 10), mostly testing. Core file estorides_core/tool_runner.py (PageRank 0.0183, imported by 9 files). Key abstractions: ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError, ToolResult. Depends on estorides_core: config (6), estorides_core: entity_resolution (2), estorides_core: parsers (1). Used by estorides_core: parsers (4), estorides_core: estorides_web (2), estorides_core: estorides (1).

- `estorides_core/tool_runner.py` ranks 1 by PageRank, 9 importers, 15 symbols.
- `estorides_core/tool_install.py` ranks 2 by PageRank, 7 importers, 27 symbols: estorides_core.tool_install
- `estorides_core/validation.py` ranks 3 by PageRank, 3 importers, 6 symbols: estorides_core.validation
- Hotspot `estorides_core/tool_install.py`: 27 symbols, 26 connections (score 0.08).
- Hotspot `tests/test_tool_runner.py`: 29 symbols, 10 connections (score 0.07).
- Surprising bridge: active_recon.py <-> test_change_detection_properties.py (6 hops across communities).
- Key entities: file:estorides_core/tool_install.py, file:tests/test_tool_runner.py, file:tests/test_tool_install.py, file:estorides_core/active_recon.py, file:tests/test_active_recon.py, sym:estorides_core/tool_runner.py::run_tool@156, file:estorides_core/tool_runner.py, sym:estorides_core/tool_install.py::install_tool@414
- Rating 1.6/10 = 7 x PageRank share 0.23 + 3 x risk 0.00. Internal imports: 13.

## estorides_core: entity_resolution (`c8`, community, rating 1.6)

7 files under estorides_core (py 7), mostly business_logic. Core file estorides_core/entity_extraction.py (PageRank 0.0303, imported by 15 files): estorides_core.entity_extraction Key abstractions: Entity, to_dict, normalize_query, detect_query_type, extract_from_text, extract_from_json. Depends on estorides_core: config (3), estorides_core: estorides (1), estorides_core: hypothesis_engine (1). Used by estorides_core: parsers (4), estorides_core: estorides (3), estorides_core: estorides_web (2).

- `estorides_core/entity_extraction.py` ranks 1 by PageRank, 15 importers, 21 symbols: estorides_core.entity_extraction
- `estorides_core/entity_resolution.py` ranks 2 by PageRank, 4 importers, 35 symbols: estorides_core.entity_resolution
- `estorides_core/transliteration.py` ranks 3 by PageRank, 2 importers, 4 symbols: estorides_core.transliteration
- Hotspot `tests/test_entity_resolution.py`: 68 symbols, 11 connections (score 0.17).
- Hotspot `estorides_core/entity_resolution.py`: 35 symbols, 17 connections (score 0.09).
- Key entities: file:tests/test_entity_resolution.py, file:estorides_core/entity_resolution.py, file:estorides_core/entity_extraction.py, sym:estorides_core/entity_resolution.py::resolve_entities@727, sym:tests/test_entity_resolution.py::_ent@28, file:estorides_core/entity_store.py, file:estorides_core/transliteration.py, sym:estorides_core/entity_extraction.py::detect_query_type@100
- Rating 1.6/10 = 7 x PageRank share 0.23 + 3 x risk 0.00. Internal imports: 9.

## estorides_export (`c7`, community, rating 1.4)

8 files under estorides_export (py 8), mostly utility. Core file estorides_core/knowledge_graph.py (PageRank 0.0107, imported by 8 files): estorides_core.knowledge_graph Key abstractions: KnowledgeGraph, add_entity, add_observation, add_relationship, export_graphml, export_json. Depends on estorides_core: config (3), estorides_core: entity_resolution (2), estorides_core: estorides (1). Used by estorides_core: estorides_web (4), estorides_core: estorides (2), estorides_core: parsers (1).

- `estorides_core/knowledge_graph.py` ranks 1 by PageRank, 8 importers, 17 symbols: estorides_core.knowledge_graph
- `estorides_export/__init__.py` ranks 2 by PageRank, 4 importers, 0 symbols: estorides_export
- `estorides_export/recon_report.py` ranks 3 by PageRank, 3 importers, 11 symbols.
- Hotspot `estorides_core/knowledge_graph.py`: 17 symbols, 21 connections (score 0.05).
- Hotspot `tests/test_recon_report.py`: 19 symbols, 6 connections (score 0.05).
- Dependency cycle: __init__.py -> encryption.py -> __init__.py.
- Surprising bridge: test_change_detection_properties.py <-> test_recon_report.py (7 hops across communities).
- Key entities: file:estorides_core/knowledge_graph.py, file:tests/test_recon_report.py, file:estorides_export/recon_report.py, file:estorides_export/encryption.py, file:tests/test_encrypted_export.py, sym:estorides_core/knowledge_graph.py::add_relationship@142, file:estorides_export/stix.py, file:estorides_export/misp.py
- Rating 1.4/10 = 7 x PageRank share 0.20 + 3 x risk 0.00. Internal imports: 15.

## unassigned files (`c10`, community, rating 1.0)

11 files under tests (py 7, js 2, sh 2), mostly testing. Core file _multi_test.sh (PageRank 0.0031, imported by 0 files). Key abstractions: install_full, install_minimal, short, esc, toast, fail.

- `_multi_test.sh` ranks 1 by PageRank, 0 importers, 0 symbols.
- `install.sh` ranks 2 by PageRank, 0 importers, 2 symbols: Bootstrap a venv and install the runtime + optional test dependencies.
- `static/js/graph_force.js` ranks 3 by PageRank, 0 importers, 69 symbols: Estorides force-graph module (spec/graph_force3d.md).
- Hotspot `static/js/graph_force.js`: 69 symbols, 482 connections (score 0.35).
- Hotspot `tests/test_target_management.py`: 86 symbols, 4 connections (score 0.21).
- Key entities: file:tests/test_target_management.py, file:static/js/graph_force.js, sym:static/js/graph_force.js::settings@59, file:static/js/source_manager.js, file:tests/test_target_scoring.py, file:tests/test_envutil.py, file:tests/properties/test_target_management_properties.py, file:tests/test_ui_visibility.py
- Rating 1.0/10 = 7 x PageRank share 0.14 + 3 x risk 0.00. Internal imports: 0.

## estorides_core: source_health_monitoring (`c9`, community, rating 0.4)

3 files under tests/properties (py 3), mostly testing. Core file estorides_core/source_health_monitoring.py (PageRank 0.0084, imported by 2 files): estorides_core.source_health_monitoring Key abstractions: SourceHealthStatus, SourceHealthConfig, SourceHealthInput, SourceHealthResult, DashboardSummary, HealthDashboard.

- `estorides_core/source_health_monitoring.py` ranks 1 by PageRank, 2 importers, 14 symbols: estorides_core.source_health_monitoring
- `tests/properties/test_source_health_monitoring_properties.py` ranks 2 by PageRank, 0 importers, 7 symbols: Property-based invariants for estorides_core.source_health_monitoring.
- `tests/test_source_health_monitoring.py` ranks 3 by PageRank, 0 importers, 52 symbols: BDD tests for estorides_core.source_health_monitoring.
- Hotspot `tests/test_source_health_monitoring.py`: 52 symbols, 5 connections (score 0.13).
- Hotspot `estorides_core/source_health_monitoring.py`: 14 symbols, 8 connections (score 0.04).
- Key entities: file:tests/test_source_health_monitoring.py, sym:estorides_core/source_health_monitoring.py::SourceHealthInput@98, sym:estorides_core/source_health_monitoring.py::compute_health@235, file:estorides_core/source_health_monitoring.py, file:tests/properties/test_source_health_monitoring_properties.py, sym:estorides_core/source_health_monitoring.py::build_dashboard@295, sym:tests/test_source_health_monitoring.py::test_hot_sources_are_healthy@295, sym:estorides_core/source_health_monitoring.py::SourceHealthConfig@42
- Rating 0.4/10 = 7 x PageRank share 0.06 + 3 x risk 0.00. Internal imports: 2.
