# GraphRAG Community Reports

Entities: 3351 | Relationships: 9873 | Communities: 12 | Themes: 5 | Text units: 3203

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

178 files in 12 communities and 5 themes. Highest-impact communities: estorides_core: config (7.0), estorides_core: parsers (3.9), estorides_core: estorides_web (3.8). God nodes: estorides_core/config.py, estorides_web.py, estorides_core/orchestrator.py, estorides_cli.py, estorides_core/entity_extraction.py.

- [estorides_core: config] rating 7.0: `estorides_core/config.py` ranks 1 by PageRank, 50 importers, 26 symbols: estorides.config
- [estorides_core: parsers] rating 3.9: `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- [estorides_core: estorides_web] rating 3.8: `estorides_web.py` ranks 1 by PageRank, 11 importers, 95 symbols: estorides.web
- [estorides_core: hypothesis_engine] rating 3.2: `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- [estorides_core: estorides] rating 2.9: `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 7 symbols: estorides_core.sqlite_store
- [unassigned files] rating 2.2: `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- [estorides_core: people_intel] rating 2.0: `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- [estorides_core: tool_install] rating 1.6: `estorides_core/tool_runner.py` ranks 1 by PageRank, 9 importers, 15 symbols.
- Key entities: file:tests/test_security_remediation.py, file:estorides_core/config.py, file:tests/test_socmint.py, file:estorides_core/parsers.py, file:estorides_web.py, sym:estorides_web.py::create_app@256
- Children: t0, t1, t2, t3, t4
- Root rating = highest community rating.

## estorides_core: config + estorides_core: estorides_web +2 (`t1`, theme, rating 7.0)

Theme of 4 communities and 56 files: estorides_core: config (19 files, rating 7.0); estorides_core: estorides_web (24 files, rating 3.8); estorides_export (8 files, rating 1.4); estorides_core: graph_bundle (5 files, rating 0.9).

- [estorides_core: config] `estorides_core/config.py` ranks 1 by PageRank, 50 importers, 26 symbols: estorides.config
- [estorides_core: config] `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- [estorides_core: estorides_web] `estorides_web.py` ranks 1 by PageRank, 11 importers, 95 symbols: estorides.web
- [estorides_core: estorides_web] `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- [estorides_export] `estorides_core/knowledge_graph.py` ranks 1 by PageRank, 8 importers, 17 symbols: estorides_core.knowledge_graph
- [estorides_export] `estorides_export/__init__.py` ranks 2 by PageRank, 4 importers, 0 symbols: estorides_export
- [estorides_core: graph_bundle] `estorides_core/graph_force.py` ranks 1 by PageRank, 6 importers, 12 symbols: graph_force3d: payload force-graph estilo ReadMenator + contexto IA.
- [estorides_core: graph_bundle] `estorides_core/graph_bundle.py` ranks 2 by PageRank, 11 importers, 18 symbols: graph_bundle: payload circle 2D + sphere 3D estilo ReadMenator.
- Key entities: file:tests/test_security_remediation.py, file:estorides_core/config.py, file:estorides_web.py, sym:estorides_web.py::create_app@256, file:estorides_core/knowledge_graph.py, file:tests/test_recon_report.py, file:tests/test_graph_bundle.py, sym:estorides_core/graph_bundle.py::build_bundle_payload@359
- Children: c2, c1, c7, c9
- Theme rating = highest child community rating.

## estorides_core: parsers + estorides_core: hypothesis_engine +3 (`t0`, theme, rating 3.9)

Theme of 5 communities and 80 files: estorides_core: parsers (26 files, rating 3.9); estorides_core: hypothesis_engine (19 files, rating 3.2); estorides_core: estorides (18 files, rating 2.9); estorides_core: tool_install (10 files, rating 1.6); estorides_core: entity_resolution (7 files, rating 1.6).

- [estorides_core: parsers] `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- [estorides_core: parsers] `estorides_core/parsers.py` ranks 2 by PageRank, 8 importers, 65 symbols: estorides_core.parsers
- [estorides_core: hypothesis_engine] `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- [estorides_core: hypothesis_engine] `estorides_core/ids.py` ranks 2 by PageRank, 6 importers, 1 symbols: estorides_core.ids
- [estorides_core: estorides] `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 7 symbols: estorides_core.sqlite_store
- [estorides_core: estorides] `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- [estorides_core: tool_install] `estorides_core/tool_runner.py` ranks 1 by PageRank, 9 importers, 15 symbols.
- [estorides_core: tool_install] `estorides_core/tool_install.py` ranks 2 by PageRank, 7 importers, 27 symbols: estorides_core.tool_install
- Key entities: file:tests/test_socmint.py, file:estorides_core/parsers.py, file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py, file:static/js/estorides.js, file:estorides_core/scope.py, file:estorides_core/tool_install.py, file:tests/test_tool_runner.py
- Children: c0, c3, c4, c6, c8
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 2.2)

Theme of 1 communities and 24 files: unassigned files (24 files, rating 2.2).

- [unassigned files] `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- [unassigned files] `.scratchpad/gfv2_bridge.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:static/js/graph_force.js, file:tests/test_target_management.py
- Children: c11
- Theme rating = highest child community rating.

## estorides_core: people_intel (`t3`, theme, rating 2.0)

Theme of 1 communities and 15 files: estorides_core: people_intel (15 files, rating 2.0).

- [estorides_core: people_intel] `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- [estorides_core: people_intel] `estorides_core/code_exposure.py` ranks 2 by PageRank, 2 importers, 10 symbols.
- Key entities: file:tests/test_code_exposure.py, file:tests/test_cloud_asset_discovery.py
- Children: c5
- Theme rating = highest child community rating.

## estorides_core: source_health_monitoring (`t4`, theme, rating 0.4)

Theme of 1 communities and 3 files: estorides_core: source_health_monitoring (3 files, rating 0.4).

- [estorides_core: source_health_monitoring] `estorides_core/source_health_monitoring.py` ranks 1 by PageRank, 2 importers, 14 symbols: estorides_core.source_health_monitoring
- [estorides_core: source_health_monitoring] `tests/properties/test_source_health_monitoring_properties.py` ranks 2 by PageRank, 0 importers, 7 symbols: Property-based invariants for estorides_core.source_health_monitoring.
- Key entities: file:tests/test_source_health_monitoring.py, sym:estorides_core/source_health_monitoring.py::SourceHealthInput@98
- Children: c10
- Theme rating = highest child community rating.

## estorides_core: config (`c2`, community, rating 7.0)

19 files under estorides_core (py 19), mostly testing. Core file estorides_core/config.py (PageRank 0.1386, imported by 50 files): estorides.config Key abstractions: CacheConfig, PivotPolicyConfig, PivotConfig, StreamConfig, ReconFusionConfig, SchemaConfig. Depends on estorides_core: parsers (1), estorides_core: estorides_web (1), estorides_core: estorides (1). Used by estorides_core: parsers (12), estorides_core: estorides_web (9), estorides_core: estorides (8).

- `estorides_core/config.py` ranks 1 by PageRank, 50 importers, 26 symbols: estorides.config
- `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- `estorides_core/__init__.py` ranks 3 by PageRank, 13 importers, 0 symbols: estorides_core.__init__
- Hotspot `tests/test_security_remediation.py`: 67 symbols, 56 connections (score 0.18).
- Hotspot `tests/test_monitoring.py`: 35 symbols, 13 connections (score 0.09).
- 1 layer violations, e.g. test_security_remediation.py (testing) -> web_security.py (presentation).
- Taint: 18 paths reach this group via requests, urllib.request.
- Key entities: file:tests/test_security_remediation.py, file:estorides_core/config.py, file:tests/test_monitoring.py, file:tests/test_observation_models.py, file:estorides_core/pivot_engine.py, file:estorides_core/async_client.py, file:estorides_core/feeds.py, file:estorides_core/alerter.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 42.

## estorides_core: parsers (`c0`, community, rating 3.9)

26 files under estorides_core (py 26), mostly utility. Core file estorides_core/orchestrator.py (PageRank 0.0103, imported by 13 files): estorides_core.orchestrator Key abstractions: Orchestrator, pending_system_app_tasks, repl, run, parse_dns_json, parse_crtsh_json. Depends on estorides_core: config (12), estorides_core: tool_install (4), estorides_core: entity_resolution (4). Used by estorides_core: estorides_web (6), estorides_core: estorides (3), estorides_core: config (1).

- `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- `estorides_core/parsers.py` ranks 2 by PageRank, 8 importers, 65 symbols: estorides_core.parsers
- `estorides_core/intel_resolver.py` ranks 3 by PageRank, 4 importers, 26 symbols: estorides_core.intel_resolver
- Hotspot `tests/test_socmint.py`: 72 symbols, 17 connections (score 0.18).
- Hotspot `estorides_core/parsers.py`: 65 symbols, 14 connections (score 0.16).
- Taint: 2 paths reach this group via requests.
- Key entities: file:tests/test_socmint.py, file:estorides_core/parsers.py, sym:estorides_core/system_app_sources.py::execute@396, file:tests/test_system_app_sources.py, file:estorides_core/orchestrator.py, file:estorides_core/system_app_sources.py, file:tests/test_pagination.py, file:estorides_core/ontology.py
- Rating 3.9/10 = 7 x PageRank share 0.55 + 3 x risk 0.00. Internal imports: 60.

## estorides_core: estorides_web (`c1`, community, rating 3.8)

24 files under tests (py 24), mostly testing. Core file estorides_web.py (PageRank 0.0206, imported by 11 files): estorides.web Key abstractions: deco, wrapper, stop, should_stop, status, done. Depends on estorides_core: estorides (10), estorides_core: config (9), estorides_core: parsers (6). Used by estorides_core: estorides (2), estorides_core: config (1), estorides_core: hypothesis_engine (1).

- `estorides_web.py` ranks 1 by PageRank, 11 importers, 95 symbols: estorides.web
- `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- `estorides_core/search_telemetry.py` ranks 3 by PageRank, 5 importers, 22 symbols: estorides.search_telemetry.
- Hotspot `estorides_web.py`: 95 symbols, 108 connections (score 0.27).
- Hotspot `estorides_core/graph_rag_search.py`: 44 symbols, 9 connections (score 0.11).
- Dependency cycle: estorides_web.py -> estorides_web_tools.py -> estorides_web.py.
- 15 layer violations, e.g. estorides_web.py (presentation) -> fusion_store.py (data_access).
- Surprising bridge: app.py <-> test_change_detection_properties.py (6 hops across communities).
- Key entities: file:estorides_web.py, sym:estorides_web.py::create_app@256, sym:estorides_web.py::_rate_limit_decorator@190, file:estorides_core/web_security.py, file:estorides_core/graph_rag_search.py, sym:estorides_web.py::_provides@81, file:estorides_core/search_telemetry.py, file:estorides_core/audit.py
- Rating 3.8/10 = 7 x PageRank share 0.54 + 3 x risk 0.00. Internal imports: 39.

## estorides_core: hypothesis_engine (`c3`, community, rating 3.2)

19 files under tests (py 19), mostly testing. Core file estorides_core/reliability_scoring.py (PageRank 0.0202, imported by 15 files): estorides_core.reliability_scoring Key abstractions: SourceReliability, Credibility, SourceType, ConfidenceInput, ConfidenceResult, compute_confidence. Depends on estorides_core: config (4), estorides_core: estorides_web (1), estorides_core: estorides (1). Used by estorides_core: parsers (3), estorides_core: estorides_web (2), estorides_core: estorides (1).

- `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- `estorides_core/ids.py` ranks 2 by PageRank, 6 importers, 1 symbols: estorides_core.ids
- `estorides_core/recon_fusion.py` ranks 3 by PageRank, 4 importers, 19 symbols: estorides_core.recon_fusion
- Hotspot `tests/test_reliability_scoring.py`: 70 symbols, 6 connections (score 0.17).
- Hotspot `tests/test_change_detection.py`: 43 symbols, 6 connections (score 0.10).
- Surprising bridge: test_change_detection_properties.py <-> test_graph_bundle_properties.py (7 hops across communities).
- Key entities: file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py, file:tests/test_change_detection.py, file:tests/test_recon_fusion.py, file:tests/test_hypothesis_engine.py, file:tests/test_fusion_analytics.py, file:estorides_core/recon_fusion.py, file:estorides_core/fusion_store.py
- Rating 3.2/10 = 7 x PageRank share 0.46 + 3 x risk 0.00. Internal imports: 31.

## estorides_core: estorides (`c4`, community, rating 2.9)

18 files under estorides_core (py 17, js 1), mostly utility. Core file estorides_core/sqlite_store.py (PageRank 0.0140, imported by 5 files): estorides_core.sqlite_store Key abstractions: SqliteStore, DictMixin, close, to_dict, CaseStore, fts_available. Depends on estorides_core: config (8), estorides_core: parsers (3), estorides_core: estorides_web (2). Used by estorides_core: estorides_web (10), estorides_core: parsers (2), estorides_core: config (1).

- `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 7 symbols: estorides_core.sqlite_store
- `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- `estorides_core/monitoring.py` ranks 3 by PageRank, 18 importers, 26 symbols: estorides_core.monitoring
- Hotspot `static/js/estorides.js`: 168 symbols, 1568 connections (score 1.00).
- Hotspot `estorides_cli.py`: 31 symbols, 70 connections (score 0.10).
- 1 layer violations, e.g. test_hardening.py (testing) -> web_security.py (presentation).
- Key entities: file:static/js/estorides.js, file:estorides_core/scope.py, file:estorides_cli.py, file:estorides_core/monitoring.py, file:estorides_core/cases.py, file:estorides_core/discoverer.py, sym:estorides_core/job_registry.py::values@105, file:tests/test_hardening.py
- Rating 2.9/10 = 7 x PageRank share 0.42 + 3 x risk 0.00. Internal imports: 37.

## unassigned files (`c11`, community, rating 2.2)

24 files under .scratchpad (py 19, js 3, sh 2), mostly utility. Core file .scratchpad/gb_shots.py (PageRank 0.0029, imported by 0 files). Key abstractions: install_full, install_minimal, djb2KindColor, mk, clip, tabActive.

- `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- `.scratchpad/gfv2_bridge.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `.scratchpad/gfv2_click.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `static/js/graph_force.js`: 109 symbols, 758 connections (score 0.55).
- Hotspot `static/js/graph_bundle.js`: 62 symbols, 588 connections (score 0.37).
- Key entities: file:static/js/graph_force.js, file:tests/test_target_management.py, file:static/js/graph_bundle.js, sym:static/js/graph_force.js::settings@72, file:static/js/source_manager.js, file:tests/test_target_scoring.py, file:tests/test_envutil.py, file:tests/properties/test_target_management_properties.py
- Rating 2.2/10 = 7 x PageRank share 0.31 + 3 x risk 0.00. Internal imports: 0.

## estorides_core: people_intel (`c5`, community, rating 2.0)

15 files under estorides_core (py 15), mostly utility. Core file estorides_core/cloud_asset_discovery.py (PageRank 0.0058, imported by 3 files). Key abstractions: CloudAsset, CloudAssetDiscoveryResult, CloudAssetDiscoveryError, to_dict, to_dict, generate_bucket_names.

- `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- `estorides_core/code_exposure.py` ranks 2 by PageRank, 2 importers, 10 symbols.
- `estorides_core/pdns_monitor.py` ranks 3 by PageRank, 3 importers, 11 symbols.
- Hotspot `tests/test_code_exposure.py`: 21 symbols, 3 connections (score 0.05).
- Hotspot `tests/test_cloud_asset_discovery.py`: 18 symbols, 5 connections (score 0.04).
- Key entities: file:tests/test_code_exposure.py, file:tests/test_cloud_asset_discovery.py, file:tests/test_people_intel.py, file:tests/test_pdns_monitor.py, file:tests/test_tech_fingerprint.py, file:tests/test_supply_chain.py, file:tests/test_vuln_correlation.py, file:estorides_core/supply_chain.py
- Rating 2.0/10 = 7 x PageRank share 0.28 + 3 x risk 0.00. Internal imports: 16.

## estorides_core: tool_install (`c6`, community, rating 1.6)

10 files under tests (py 10), mostly testing. Core file estorides_core/tool_runner.py (PageRank 0.0172, imported by 9 files). Key abstractions: ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError, ToolResult. Depends on estorides_core: config (6), estorides_core: entity_resolution (2), estorides_core: parsers (1). Used by estorides_core: parsers (4), estorides_core: estorides_web (2), estorides_core: estorides (1).

- `estorides_core/tool_runner.py` ranks 1 by PageRank, 9 importers, 15 symbols.
- `estorides_core/tool_install.py` ranks 2 by PageRank, 7 importers, 27 symbols: estorides_core.tool_install
- `estorides_core/validation.py` ranks 3 by PageRank, 3 importers, 6 symbols: estorides_core.validation
- Hotspot `estorides_core/tool_install.py`: 27 symbols, 26 connections (score 0.07).
- Hotspot `tests/test_tool_runner.py`: 29 symbols, 10 connections (score 0.07).
- Key entities: file:estorides_core/tool_install.py, file:tests/test_tool_runner.py, file:tests/test_tool_install.py, file:estorides_core/active_recon.py, file:tests/test_active_recon.py, sym:estorides_core/tool_runner.py::run_tool@156, file:estorides_core/tool_runner.py, sym:estorides_core/tool_install.py::install_tool@414
- Rating 1.6/10 = 7 x PageRank share 0.23 + 3 x risk 0.00. Internal imports: 13.

## estorides_core: entity_resolution (`c8`, community, rating 1.6)

7 files under estorides_core (py 7), mostly business_logic. Core file estorides_core/entity_extraction.py (PageRank 0.0285, imported by 15 files): estorides_core.entity_extraction Key abstractions: Entity, to_dict, normalize_query, detect_query_type, extract_from_text, extract_from_json. Depends on estorides_core: config (3), estorides_core: hypothesis_engine (1), estorides_core: estorides (1). Used by estorides_core: parsers (4), estorides_core: estorides_web (2), estorides_core: estorides (2).

- `estorides_core/entity_extraction.py` ranks 1 by PageRank, 15 importers, 21 symbols: estorides_core.entity_extraction
- `estorides_core/entity_resolution.py` ranks 2 by PageRank, 4 importers, 35 symbols: estorides_core.entity_resolution
- `estorides_core/transliteration.py` ranks 3 by PageRank, 2 importers, 4 symbols: estorides_core.transliteration
- Hotspot `tests/test_entity_resolution.py`: 68 symbols, 11 connections (score 0.17).
- Hotspot `estorides_core/entity_resolution.py`: 35 symbols, 17 connections (score 0.09).
- Key entities: file:tests/test_entity_resolution.py, file:estorides_core/entity_resolution.py, file:estorides_core/entity_extraction.py, sym:estorides_core/entity_resolution.py::resolve_entities@727, sym:tests/test_entity_resolution.py::_ent@28, file:estorides_core/entity_store.py, file:estorides_core/transliteration.py, sym:estorides_core/entity_extraction.py::detect_query_type@100
- Rating 1.6/10 = 7 x PageRank share 0.23 + 3 x risk 0.00. Internal imports: 9.

## estorides_export (`c7`, community, rating 1.4)

8 files under estorides_export (py 8), mostly utility. Core file estorides_core/knowledge_graph.py (PageRank 0.0101, imported by 8 files): estorides_core.knowledge_graph Key abstractions: KnowledgeGraph, add_entity, add_observation, add_relationship, export_graphml, export_json. Depends on estorides_core: config (3), estorides_core: entity_resolution (2), estorides_core: estorides (1). Used by estorides_core: estorides_web (4), estorides_core: estorides (2), estorides_core: parsers (1).

- `estorides_core/knowledge_graph.py` ranks 1 by PageRank, 8 importers, 17 symbols: estorides_core.knowledge_graph
- `estorides_export/__init__.py` ranks 2 by PageRank, 4 importers, 0 symbols: estorides_export
- `estorides_export/recon_report.py` ranks 3 by PageRank, 3 importers, 11 symbols.
- Hotspot `estorides_core/knowledge_graph.py`: 17 symbols, 21 connections (score 0.05).
- Hotspot `tests/test_recon_report.py`: 19 symbols, 6 connections (score 0.05).
- Dependency cycle: __init__.py -> encryption.py -> __init__.py.
- Surprising bridge: test_change_detection_properties.py <-> test_recon_report.py (7 hops across communities).
- Key entities: file:estorides_core/knowledge_graph.py, file:tests/test_recon_report.py, file:estorides_export/recon_report.py, file:estorides_export/encryption.py, file:tests/test_encrypted_export.py, file:estorides_export/stix.py, sym:estorides_core/knowledge_graph.py::add_relationship@142, file:estorides_export/misp.py
- Rating 1.4/10 = 7 x PageRank share 0.19 + 3 x risk 0.00. Internal imports: 15.

## estorides_core: graph_bundle (`c9`, community, rating 0.9)

5 files under estorides_core (py 5), mostly testing. Core file estorides_core/graph_force.py (PageRank 0.0124, imported by 6 files): graph_force3d: payload force-graph estilo ReadMenator + contexto IA. Key abstractions: family_color_from_name, node_value, force_settings, build_force_payload, build_ai_context, BundleLayout. Depends on estorides_core: config (2). Used by estorides_core: estorides_web (1).

- `estorides_core/graph_force.py` ranks 1 by PageRank, 6 importers, 12 symbols: graph_force3d: payload force-graph estilo ReadMenator + contexto IA.
- `estorides_core/graph_bundle.py` ranks 2 by PageRank, 11 importers, 18 symbols: graph_bundle: payload circle 2D + sphere 3D estilo ReadMenator.
- `tests/properties/test_graph_bundle_properties.py` ranks 3 by PageRank, 0 importers, 6 symbols: Property-based invariants for estorides_core.graph_bundle.
- Hotspot `tests/test_graph_bundle.py`: 30 symbols, 34 connections (score 0.08).
- Hotspot `estorides_core/graph_bundle.py`: 18 symbols, 19 connections (score 0.05).
- Surprising bridge: test_change_detection_properties.py <-> test_graph_bundle_properties.py (7 hops across communities).
- Key entities: file:tests/test_graph_bundle.py, sym:estorides_core/graph_bundle.py::build_bundle_payload@359, file:estorides_core/graph_bundle.py, file:estorides_core/graph_force.py, file:tests/test_graph_force3d.py, sym:estorides_core/graph_force.py::build_force_payload@161, file:tests/properties/test_graph_bundle_properties.py, sym:estorides_core/graph_bundle.py::spherical_edge_bundling@267
- Rating 0.9/10 = 7 x PageRank share 0.13 + 3 x risk 0.00. Internal imports: 16.

## estorides_core: source_health_monitoring (`c10`, community, rating 0.4)

3 files under tests/properties (py 3), mostly testing. Core file estorides_core/source_health_monitoring.py (PageRank 0.0080, imported by 2 files): estorides_core.source_health_monitoring Key abstractions: SourceHealthStatus, SourceHealthConfig, SourceHealthInput, SourceHealthResult, DashboardSummary, HealthDashboard.

- `estorides_core/source_health_monitoring.py` ranks 1 by PageRank, 2 importers, 14 symbols: estorides_core.source_health_monitoring
- `tests/properties/test_source_health_monitoring_properties.py` ranks 2 by PageRank, 0 importers, 7 symbols: Property-based invariants for estorides_core.source_health_monitoring.
- `tests/test_source_health_monitoring.py` ranks 3 by PageRank, 0 importers, 52 symbols: BDD tests for estorides_core.source_health_monitoring.
- Hotspot `tests/test_source_health_monitoring.py`: 52 symbols, 5 connections (score 0.13).
- Hotspot `estorides_core/source_health_monitoring.py`: 14 symbols, 8 connections (score 0.04).
- Key entities: file:tests/test_source_health_monitoring.py, sym:estorides_core/source_health_monitoring.py::SourceHealthInput@98, sym:estorides_core/source_health_monitoring.py::compute_health@235, file:estorides_core/source_health_monitoring.py, file:tests/properties/test_source_health_monitoring_properties.py, sym:estorides_core/source_health_monitoring.py::build_dashboard@295, sym:tests/test_source_health_monitoring.py::test_hot_sources_are_healthy@295, sym:estorides_core/source_health_monitoring.py::SourceHealthConfig@42
- Rating 0.4/10 = 7 x PageRank share 0.06 + 3 x risk 0.00. Internal imports: 2.
