# GraphRAG Community Reports

Entities: 3497 | Relationships: 10339 | Communities: 11 | Themes: 5 | Text units: 3348

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

191 files in 11 communities and 5 themes. Highest-impact communities: estorides_core: config (7.0), estorides_core: estorides_web (4.1), estorides_core: parsers (3.3). God nodes: estorides_core/config.py, estorides_web.py, estorides_core/orchestrator.py, estorides_cli.py, estorides_core/entity_extraction.py.

- [estorides_core: config] rating 7.0: `estorides_core/config.py` ranks 1 by PageRank, 52 importers, 29 symbols: estorides.config
- [estorides_core: estorides_web] rating 4.1: `estorides_web.py` ranks 1 by PageRank, 11 importers, 97 symbols: estorides.web
- [estorides_core: parsers] rating 3.3: `estorides_core/parsers.py` ranks 1 by PageRank, 8 importers, 65 symbols: estorides_core.parsers
- [estorides_core: hypothesis_engine] rating 3.1: `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- [estorides_export] rating 2.9: `estorides_core/entity_extraction.py` ranks 1 by PageRank, 16 importers, 21 symbols: estorides_core.entity_extraction
- [estorides_core: estorides] rating 2.6: `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 8 symbols: estorides_core.sqlite_store
- [unassigned files] rating 2.4: `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- [estorides_core: graph_bundle] rating 2.4: `estorides_core/__init__.py` ranks 1 by PageRank, 21 importers, 0 symbols: estorides_core.__init__
- Key entities: file:estorides_core/config.py, file:estorides_core/ontology.py, file:estorides_web.py, sym:estorides_web.py::create_app@258, file:tests/test_socmint.py, file:estorides_core/parsers.py
- Children: t0, t1, t2, t3, t4
- Root rating = highest community rating.

## estorides_core: config + estorides_core: estorides_web +2 (`t1`, theme, rating 7.0)

Theme of 4 communities and 71 files: estorides_core: config (17 files, rating 7.0); estorides_core: estorides_web (27 files, rating 4.1); estorides_core: graph_bundle (15 files, rating 2.4); estorides_core: tool_install (12 files, rating 1.9).

- [estorides_core: config] `estorides_core/config.py` ranks 1 by PageRank, 52 importers, 29 symbols: estorides.config
- [estorides_core: config] `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- [estorides_core: estorides_web] `estorides_web.py` ranks 1 by PageRank, 11 importers, 97 symbols: estorides.web
- [estorides_core: estorides_web] `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- [estorides_core: graph_bundle] `estorides_core/__init__.py` ranks 1 by PageRank, 21 importers, 0 symbols: estorides_core.__init__
- [estorides_core: graph_bundle] `estorides_core/graph_force.py` ranks 2 by PageRank, 6 importers, 12 symbols: graph_force3d: payload force-graph estilo ReadMenator + contexto IA.
- [estorides_core: tool_install] `estorides_core/tool_runner.py` ranks 1 by PageRank, 11 importers, 15 symbols.
- [estorides_core: tool_install] `estorides_core/tool_install.py` ranks 2 by PageRank, 7 importers, 27 symbols: estorides_core.tool_install
- Key entities: file:estorides_core/config.py, file:estorides_core/ontology.py, file:estorides_web.py, sym:estorides_web.py::create_app@258, file:tests/test_graph_bundle.py, sym:estorides_core/graph_bundle.py::build_bundle_payload@359, file:estorides_core/tool_install.py, file:tests/test_tool_runner.py
- Children: c4, c0, c5, c8
- Theme rating = highest child community rating.

## estorides_core: parsers + estorides_core: hypothesis_engine +2 (`t0`, theme, rating 3.3)

Theme of 4 communities and 75 files: estorides_core: parsers (24 files, rating 3.3); estorides_core: hypothesis_engine (19 files, rating 3.1); estorides_export (15 files, rating 2.9); estorides_core: estorides (17 files, rating 2.6).

- [estorides_core: parsers] `estorides_core/parsers.py` ranks 1 by PageRank, 8 importers, 65 symbols: estorides_core.parsers
- [estorides_core: parsers] `estorides_core/orchestrator.py` ranks 2 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- [estorides_core: hypothesis_engine] `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- [estorides_core: hypothesis_engine] `estorides_core/ids.py` ranks 2 by PageRank, 6 importers, 1 symbols: estorides_core.ids
- [estorides_export] `estorides_core/entity_extraction.py` ranks 1 by PageRank, 16 importers, 21 symbols: estorides_core.entity_extraction
- [estorides_export] `estorides_core/knowledge_graph.py` ranks 2 by PageRank, 8 importers, 18 symbols: estorides_core.knowledge_graph
- [estorides_core: estorides] `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 8 symbols: estorides_core.sqlite_store
- [estorides_core: estorides] `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- Key entities: file:tests/test_socmint.py, file:estorides_core/parsers.py, file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py, file:tests/test_entity_resolution.py, file:estorides_core/entity_resolution.py, file:static/js/estorides.js, file:tests/test_security_remediation.py
- Children: c1, c2, c7, c3
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 2.4)

Theme of 1 communities and 27 files: unassigned files (27 files, rating 2.4).

- [unassigned files] `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- [unassigned files] `.scratchpad/gfv2_bridge.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:static/js/graph_force.js, file:tests/test_target_management.py
- Children: c10
- Theme rating = highest child community rating.

## estorides_core: people_intel (`t3`, theme, rating 1.9)

Theme of 1 communities and 15 files: estorides_core: people_intel (15 files, rating 1.9).

- [estorides_core: people_intel] `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- [estorides_core: people_intel] `estorides_core/code_exposure.py` ranks 2 by PageRank, 2 importers, 10 symbols.
- Key entities: file:tests/test_code_exposure.py, file:tests/test_cloud_asset_discovery.py
- Children: c6
- Theme rating = highest child community rating.

## estorides_core: source_health_monitoring (`t4`, theme, rating 0.4)

Theme of 1 communities and 3 files: estorides_core: source_health_monitoring (3 files, rating 0.4).

- [estorides_core: source_health_monitoring] `estorides_core/source_health_monitoring.py` ranks 1 by PageRank, 2 importers, 14 symbols: estorides_core.source_health_monitoring
- [estorides_core: source_health_monitoring] `tests/properties/test_source_health_monitoring_properties.py` ranks 2 by PageRank, 0 importers, 7 symbols: Property-based invariants for estorides_core.source_health_monitoring.
- Key entities: file:tests/test_source_health_monitoring.py, sym:estorides_core/source_health_monitoring.py::SourceHealthInput@98
- Children: c9
- Theme rating = highest child community rating.

## estorides_core: config (`c4`, community, rating 7.0)

17 files under estorides_core (py 17), mostly utility. Core file estorides_core/config.py (PageRank 0.1459, imported by 52 files): estorides.config Key abstractions: CacheConfig, PivotPolicyConfig, PivotConfig, StreamConfig, ReconFusionConfig, SchemaConfig. Depends on estorides_export (1). Used by estorides_core: parsers (13), estorides_core: estorides_web (9), estorides_core: estorides (7).

- `estorides_core/config.py` ranks 1 by PageRank, 52 importers, 29 symbols: estorides.config
- `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- `estorides_core/observation_models.py` ranks 3 by PageRank, 2 importers, 14 symbols: estorides_core.observation_models
- Hotspot `estorides_core/config.py`: 29 symbols, 62 connections (score 0.09).
- Hotspot `estorides_core/intel_resolver.py`: 26 symbols, 21 connections (score 0.07).
- Taint: 18 paths reach this group via requests, urllib.request.
- Key entities: file:estorides_core/config.py, file:estorides_core/ontology.py, file:estorides_core/pivot_engine.py, file:tests/test_observation_models.py, file:estorides_core/intel_resolver.py, file:estorides_core/async_client.py, file:estorides_core/transforms.py, file:estorides_core/feeds.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 36.

## estorides_core: estorides_web (`c0`, community, rating 4.1)

27 files under tests (py 27), mostly testing. Core file estorides_web.py (PageRank 0.0192, imported by 11 files): estorides.web Key abstractions: deco, wrapper, stop, should_stop, status, done. Depends on estorides_core: config (9), estorides_core: parsers (7), estorides_export (7). Used by estorides_core: estorides (3), estorides_core: parsers (1), estorides_core: hypothesis_engine (1).

- `estorides_web.py` ranks 1 by PageRank, 11 importers, 97 symbols: estorides.web
- `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- `estorides_core/search_telemetry.py` ranks 3 by PageRank, 5 importers, 22 symbols: estorides.search_telemetry.
- Hotspot `estorides_web.py`: 97 symbols, 120 connections (score 0.26).
- Hotspot `estorides_core/graph_rag_search.py`: 44 symbols, 9 connections (score 0.10).
- Dependency cycle: estorides_web.py -> estorides_web_tools.py -> estorides_web.py.
- 15 layer violations, e.g. estorides_web.py (presentation) -> fusion_store.py (data_access).
- Key entities: file:estorides_web.py, sym:estorides_web.py::create_app@258, sym:estorides_web.py::_rate_limit_decorator@192, file:estorides_core/web_security.py, file:estorides_core/graph_rag_search.py, sym:estorides_core/job_registry.py::values@105, sym:estorides_web.py::_provides@83, file:estorides_core/search_telemetry.py
- Rating 4.1/10 = 7 x PageRank share 0.58 + 3 x risk 0.00. Internal imports: 44.

## estorides_core: parsers (`c1`, community, rating 3.3)

24 files under estorides_core (py 24), mostly utility. Core file estorides_core/parsers.py (PageRank 0.0095, imported by 8 files): estorides_core.parsers Key abstractions: parse_dns_json, parse_crtsh_json, parse_rdap, parse_ipapi, parse_ipinfo, parse_ipapi_co. Depends on estorides_core: config (13), estorides_export (5), estorides_core: tool_install (4). Used by estorides_core: estorides_web (7), estorides_core: estorides (4), estorides_core: tool_install (1).

- `estorides_core/parsers.py` ranks 1 by PageRank, 8 importers, 65 symbols: estorides_core.parsers
- `estorides_core/orchestrator.py` ranks 2 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- `estorides_core/source_loader.py` ranks 3 by PageRank, 7 importers, 20 symbols: estorides_core.source_loader
- Hotspot `tests/test_socmint.py`: 72 symbols, 17 connections (score 0.17).
- Hotspot `estorides_core/parsers.py`: 65 symbols, 14 connections (score 0.15).
- Key entities: file:tests/test_socmint.py, file:estorides_core/parsers.py, sym:estorides_core/system_app_sources.py::execute@396, file:tests/test_system_app_sources.py, file:estorides_core/orchestrator.py, file:estorides_core/system_app_sources.py, file:tests/test_pagination.py, file:estorides_llm/manager.py
- Rating 3.3/10 = 7 x PageRank share 0.47 + 3 x risk 0.00. Internal imports: 53.

## estorides_core: hypothesis_engine (`c2`, community, rating 3.1)

19 files under tests (py 19), mostly testing. Core file estorides_core/reliability_scoring.py (PageRank 0.0189, imported by 15 files): estorides_core.reliability_scoring Key abstractions: SourceReliability, Credibility, SourceType, ConfidenceInput, ConfidenceResult, compute_confidence. Depends on estorides_core: config (4), estorides_core: estorides_web (1), estorides_core: estorides (1). Used by estorides_core: parsers (3), estorides_core: estorides_web (2), estorides_core: estorides (1).

- `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- `estorides_core/ids.py` ranks 2 by PageRank, 6 importers, 1 symbols: estorides_core.ids
- `estorides_core/recon_fusion.py` ranks 3 by PageRank, 4 importers, 19 symbols: estorides_core.recon_fusion
- Hotspot `tests/test_reliability_scoring.py`: 70 symbols, 6 connections (score 0.16).
- Hotspot `tests/test_change_detection.py`: 43 symbols, 6 connections (score 0.10).
- Surprising bridge: lan_inventory.py <-> test_change_detection_properties.py (7 hops across communities).
- Key entities: file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py, file:tests/test_change_detection.py, file:tests/test_hypothesis_engine.py, file:tests/test_recon_fusion.py, file:tests/test_fusion_analytics.py, file:estorides_core/recon_fusion.py, file:estorides_core/fusion_store.py
- Rating 3.1/10 = 7 x PageRank share 0.45 + 3 x risk 0.00. Internal imports: 31.

## estorides_export (`c7`, community, rating 2.9)

15 files under estorides_export (py 15), mostly utility. Core file estorides_core/entity_extraction.py (PageRank 0.0282, imported by 16 files): estorides_core.entity_extraction Key abstractions: Entity, to_dict, normalize_query, detect_query_type, extract_from_text, extract_from_json. Depends on estorides_core: config (6), estorides_core: estorides (2), estorides_core: hypothesis_engine (1). Used by estorides_core: estorides_web (7), estorides_core: parsers (5), estorides_core: estorides (4).

- `estorides_core/entity_extraction.py` ranks 1 by PageRank, 16 importers, 21 symbols: estorides_core.entity_extraction
- `estorides_core/knowledge_graph.py` ranks 2 by PageRank, 8 importers, 18 symbols: estorides_core.knowledge_graph
- `estorides_export/__init__.py` ranks 3 by PageRank, 4 importers, 0 symbols: estorides_export
- Hotspot `tests/test_entity_resolution.py`: 68 symbols, 11 connections (score 0.16).
- Hotspot `estorides_core/entity_resolution.py`: 35 symbols, 17 connections (score 0.08).
- Dependency cycle: __init__.py -> encryption.py -> __init__.py.
- Surprising bridge: test_change_detection_properties.py <-> test_recon_report.py (7 hops across communities).
- Key entities: file:tests/test_entity_resolution.py, file:estorides_core/entity_resolution.py, file:estorides_core/entity_extraction.py, file:estorides_core/knowledge_graph.py, file:tests/test_recon_report.py, sym:estorides_core/entity_resolution.py::resolve_entities@727, sym:tests/test_entity_resolution.py::_ent@28, file:estorides_export/recon_report.py
- Rating 2.9/10 = 7 x PageRank share 0.42 + 3 x risk 0.00. Internal imports: 26.

## estorides_core: estorides (`c3`, community, rating 2.6)

17 files under tests (py 16, js 1), mostly testing. Core file estorides_core/sqlite_store.py (PageRank 0.0130, imported by 5 files): estorides_core.sqlite_store Key abstractions: SqliteStore, DictMixin, close, to_dict, CaseStore, fts_available. Depends on estorides_core: config (7), estorides_core: parsers (4), estorides_core: graph_bundle (4). Used by estorides_core: estorides_web (6), estorides_core: parsers (2), estorides_export (2).

- `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 8 symbols: estorides_core.sqlite_store
- `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- `estorides_core/monitoring.py` ranks 3 by PageRank, 18 importers, 26 symbols: estorides_core.monitoring
- Hotspot `static/js/estorides.js`: 180 symbols, 1674 connections (score 1.00).
- Hotspot `tests/test_security_remediation.py`: 67 symbols, 56 connections (score 0.17).
- 2 layer violations, e.g. test_hardening.py (testing) -> web_security.py (presentation).
- Taint: 2 paths reach this group via urllib.request.
- Key entities: file:static/js/estorides.js, file:tests/test_security_remediation.py, file:estorides_core/scope.py, file:estorides_cli.py, file:tests/test_monitoring.py, file:estorides_core/monitoring.py, file:estorides_core/cases.py, file:estorides_core/alerter.py
- Rating 2.6/10 = 7 x PageRank share 0.37 + 3 x risk 0.00. Internal imports: 42.

## unassigned files (`c10`, community, rating 2.4)

27 files under .scratchpad (py 22, js 3, sh 2), mostly utility. Core file .scratchpad/gb_shots.py (PageRank 0.0028, imported by 0 files). Key abstractions: LanPolicyRequest, LanPolicyDecision, to_dict, requires_consent, max_contact_for, evaluate.

- `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- `.scratchpad/gfv2_bridge.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `.scratchpad/gfv2_click.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `static/js/graph_force.js`: 109 symbols, 758 connections (score 0.51).
- Hotspot `static/js/graph_bundle.js`: 62 symbols, 588 connections (score 0.35).
- Key entities: file:static/js/graph_force.js, file:tests/test_target_management.py, file:static/js/graph_bundle.js, sym:static/js/graph_force.js::settings@72, file:static/js/source_manager.js, file:tests/test_target_scoring.py, file:tests/test_envutil.py, file:tests/properties/test_target_management_properties.py
- Rating 2.4/10 = 7 x PageRank share 0.34 + 3 x risk 0.00. Internal imports: 0.

## estorides_core: graph_bundle (`c5`, community, rating 2.4)

15 files under tests (py 15), mostly testing. Core file estorides_core/__init__.py (PageRank 0.0236, imported by 21 files): estorides_core.__init__ Key abstractions: family_color_from_name, node_value, force_settings, build_force_payload, build_ai_context, BundleLayout. Depends on estorides_core: config (3). Used by estorides_core: estorides_web (5), estorides_core: estorides (4), estorides_core: tool_install (3).

- `estorides_core/__init__.py` ranks 1 by PageRank, 21 importers, 0 symbols: estorides_core.__init__
- `estorides_core/graph_force.py` ranks 2 by PageRank, 6 importers, 12 symbols: graph_force3d: payload force-graph estilo ReadMenator + contexto IA.
- `estorides_core/graph_bundle.py` ranks 3 by PageRank, 11 importers, 18 symbols: graph_bundle: payload circle 2D + sphere 3D estilo ReadMenator.
- Hotspot `tests/test_graph_bundle.py`: 30 symbols, 34 connections (score 0.08).
- Hotspot `estorides_core/graph_bundle.py`: 18 symbols, 19 connections (score 0.05).
- Surprising bridge: lan_inventory.py <-> test_change_detection_properties.py (7 hops across communities).
- Key entities: file:tests/test_graph_bundle.py, sym:estorides_core/graph_bundle.py::build_bundle_payload@359, file:estorides_core/graph_bundle.py, file:estorides_core/lan_inventory.py, file:estorides_core/graph_force.py, file:tests/test_parsers.py, file:tests/test_lan_inventory.py, file:tests/test_lan_web.py
- Rating 2.4/10 = 7 x PageRank share 0.35 + 3 x risk 0.00. Internal imports: 27.

## estorides_core: people_intel (`c6`, community, rating 1.9)

15 files under estorides_core (py 15), mostly utility. Core file estorides_core/cloud_asset_discovery.py (PageRank 0.0054, imported by 3 files). Key abstractions: CloudAsset, CloudAssetDiscoveryResult, CloudAssetDiscoveryError, to_dict, to_dict, generate_bucket_names.

- `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- `estorides_core/code_exposure.py` ranks 2 by PageRank, 2 importers, 10 symbols.
- `estorides_core/pdns_monitor.py` ranks 3 by PageRank, 3 importers, 11 symbols.
- Hotspot `tests/test_code_exposure.py`: 21 symbols, 3 connections (score 0.05).
- Hotspot `tests/test_cloud_asset_discovery.py`: 18 symbols, 5 connections (score 0.04).
- Key entities: file:tests/test_code_exposure.py, file:tests/test_cloud_asset_discovery.py, file:tests/test_people_intel.py, file:tests/test_pdns_monitor.py, file:tests/test_tech_fingerprint.py, file:tests/test_supply_chain.py, file:tests/test_vuln_correlation.py, file:estorides_core/supply_chain.py
- Rating 1.9/10 = 7 x PageRank share 0.27 + 3 x risk 0.00. Internal imports: 16.

## estorides_core: tool_install (`c8`, community, rating 1.9)

12 files under tests (py 12), mostly testing. Core file estorides_core/tool_runner.py (PageRank 0.0196, imported by 11 files). Key abstractions: ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError, ToolResult. Depends on estorides_core: config (4), estorides_core: graph_bundle (3), estorides_export (2). Used by estorides_core: parsers (4), estorides_core: estorides_web (2), estorides_core: estorides (1).

- `estorides_core/tool_runner.py` ranks 1 by PageRank, 11 importers, 15 symbols.
- `estorides_core/tool_install.py` ranks 2 by PageRank, 7 importers, 27 symbols: estorides_core.tool_install
- `estorides_core/validation.py` ranks 3 by PageRank, 3 importers, 6 symbols: estorides_core.validation
- Hotspot `estorides_core/tool_install.py`: 27 symbols, 26 connections (score 0.07).
- Hotspot `tests/test_tool_runner.py`: 29 symbols, 10 connections (score 0.07).
- Key entities: file:estorides_core/tool_install.py, file:tests/test_tool_runner.py, file:tests/test_tool_install.py, file:estorides_core/active_recon.py, file:tests/test_active_recon.py, sym:estorides_core/tool_runner.py::run_tool@156, file:estorides_core/tool_runner.py, sym:estorides_core/lan_runner.py::scan@147
- Rating 1.9/10 = 7 x PageRank share 0.27 + 3 x risk 0.00. Internal imports: 15.

## estorides_core: source_health_monitoring (`c9`, community, rating 0.4)

3 files under tests/properties (py 3), mostly testing. Core file estorides_core/source_health_monitoring.py (PageRank 0.0074, imported by 2 files): estorides_core.source_health_monitoring Key abstractions: SourceHealthStatus, SourceHealthConfig, SourceHealthInput, SourceHealthResult, DashboardSummary, HealthDashboard.

- `estorides_core/source_health_monitoring.py` ranks 1 by PageRank, 2 importers, 14 symbols: estorides_core.source_health_monitoring
- `tests/properties/test_source_health_monitoring_properties.py` ranks 2 by PageRank, 0 importers, 7 symbols: Property-based invariants for estorides_core.source_health_monitoring.
- `tests/test_source_health_monitoring.py` ranks 3 by PageRank, 0 importers, 52 symbols: BDD tests for estorides_core.source_health_monitoring.
- Hotspot `tests/test_source_health_monitoring.py`: 52 symbols, 5 connections (score 0.12).
- Hotspot `estorides_core/source_health_monitoring.py`: 14 symbols, 8 connections (score 0.03).
- Key entities: file:tests/test_source_health_monitoring.py, sym:estorides_core/source_health_monitoring.py::SourceHealthInput@98, sym:estorides_core/source_health_monitoring.py::compute_health@235, file:estorides_core/source_health_monitoring.py, file:tests/properties/test_source_health_monitoring_properties.py, sym:estorides_core/source_health_monitoring.py::build_dashboard@295, sym:tests/test_source_health_monitoring.py::test_hot_sources_are_healthy@295, sym:estorides_core/source_health_monitoring.py::SourceHealthConfig@42
- Rating 0.4/10 = 7 x PageRank share 0.06 + 3 x risk 0.00. Internal imports: 2.
