# GraphRAG Community Reports

Entities: 3839 | Relationships: 11256 | Communities: 13 | Themes: 5 | Text units: 3688

Query with `readmenator . ask "<question>"` (local: BM25 + Personalized PageRank; global: map-reduce over these reports) or the MCP tool `readmenator.graphrag`.

## Project overview (`root`, root, rating 7.0)

199 files in 13 communities and 5 themes. Highest-impact communities: estorides_core: config (7.0), estorides_core: estorides_web (3.7), estorides_core: hypothesis_engine (3.1). God nodes: estorides_core/config.py, estorides_web.py, estorides_core/orchestrator.py, estorides_core/__init__.py, estorides_cli.py.

- [estorides_core: config] rating 7.0: `estorides_core/config.py` ranks 1 by PageRank, 52 importers, 29 symbols: estorides.config
- [estorides_core: estorides_web] rating 3.7: `estorides_web.py` ranks 1 by PageRank, 12 importers, 97 symbols: estorides.web
- [estorides_core: hypothesis_engine] rating 3.1: `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- [estorides_core: graph_bundle] rating 3.0: `estorides_core/__init__.py` ranks 1 by PageRank, 27 importers, 0 symbols: estorides_core.__init__
- [estorides_core: estorides] rating 2.5: `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 8 symbols: estorides_core.sqlite_store
- [unassigned files] rating 2.3: `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- [estorides_core: parsers] rating 2.3: `estorides_core/aviation.py` ranks 1 by PageRank, 5 importers, 18 symbols: estorides_core.aviation
- [estorides_core: system_app_sources] rating 2.0: `estorides_core/tool_runner.py` ranks 1 by PageRank, 11 importers, 15 symbols.
- Key entities: file:estorides_core/config.py, file:estorides_core/ontology.py, file:estorides_web.py, sym:estorides_web.py::create_app@258, file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py
- Children: t0, t1, t2, t3, t4
- Root rating = highest community rating.

## estorides_core: config + estorides_core: hypothesis_engine +4 (`t0`, theme, rating 7.0)

Theme of 6 communities and 84 files: estorides_core: config (16 files, rating 7.0); estorides_core: hypothesis_engine (19 files, rating 3.1); estorides_core: estorides (17 files, rating 2.5); estorides_core: manager (14 files, rating 1.9); estorides_core: entity_resolution (10 files, rating 1.9); estorides_export (8 files, rating 1.3).

- [estorides_core: config] `estorides_core/config.py` ranks 1 by PageRank, 52 importers, 29 symbols: estorides.config
- [estorides_core: config] `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- [estorides_core: hypothesis_engine] `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- [estorides_core: hypothesis_engine] `estorides_core/ids.py` ranks 2 by PageRank, 6 importers, 1 symbols: estorides_core.ids
- [estorides_core: estorides] `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 8 symbols: estorides_core.sqlite_store
- [estorides_core: estorides] `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- [estorides_core: manager] `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- [estorides_core: manager] `estorides_core/job_registry.py` ranks 2 by PageRank, 3 importers, 10 symbols: estorides_core.job_registry
- Key entities: file:estorides_core/config.py, file:estorides_core/ontology.py, file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py, file:static/js/estorides.js, file:tests/test_security_remediation.py, file:estorides_core/orchestrator.py, file:tests/test_pagination.py
- Children: c4, c2, c3, c6, c9, c10
- Theme rating = highest child community rating.

## estorides_core: estorides_web + estorides_core: graph_bundle +2 (`t1`, theme, rating 3.7)

Theme of 4 communities and 70 files: estorides_core: estorides_web (25 files, rating 3.7); estorides_core: graph_bundle (19 files, rating 3.0); estorides_core: parsers (13 files, rating 2.3); estorides_core: system_app_sources (13 files, rating 2.0).

- [estorides_core: estorides_web] `estorides_web.py` ranks 1 by PageRank, 12 importers, 97 symbols: estorides.web
- [estorides_core: estorides_web] `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- [estorides_core: graph_bundle] `estorides_core/__init__.py` ranks 1 by PageRank, 27 importers, 0 symbols: estorides_core.__init__
- [estorides_core: graph_bundle] `estorides_core/graph_force.py` ranks 2 by PageRank, 6 importers, 12 symbols: graph_force3d: payload force-graph estilo ReadMenator + contexto IA.
- [estorides_core: parsers] `estorides_core/aviation.py` ranks 1 by PageRank, 5 importers, 18 symbols: estorides_core.aviation
- [estorides_core: parsers] `estorides_core/parsers.py` ranks 2 by PageRank, 13 importers, 73 symbols: estorides_core.parsers
- [estorides_core: system_app_sources] `estorides_core/tool_runner.py` ranks 1 by PageRank, 11 importers, 15 symbols.
- [estorides_core: system_app_sources] `estorides_core/tool_install.py` ranks 2 by PageRank, 7 importers, 27 symbols: estorides_core.tool_install
- Key entities: file:estorides_web.py, sym:estorides_web.py::create_app@258, file:tests/test_aviation.py, file:tests/test_data_pack.py, file:tests/test_aerospace.py, file:tests/test_socmint.py, sym:estorides_core/system_app_sources.py::execute@396, file:tests/test_system_app_sources.py
- Children: c0, c1, c8, c7
- Theme rating = highest child community rating.

## unassigned files (`t2`, theme, rating 2.3)

Theme of 1 communities and 27 files: unassigned files (27 files, rating 2.3).

- [unassigned files] `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- [unassigned files] `.scratchpad/gfv2_bridge.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- Key entities: file:static/js/graph_force.js, file:tests/test_target_management.py
- Children: c12
- Theme rating = highest child community rating.

## estorides_core: people_intel (`t3`, theme, rating 1.9)

Theme of 1 communities and 15 files: estorides_core: people_intel (15 files, rating 1.9).

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
- Children: c11
- Theme rating = highest child community rating.

## estorides_core: config (`c4`, community, rating 7.0)

16 files under estorides_core (py 16), mostly utility. Core file estorides_core/config.py (PageRank 0.1453, imported by 52 files): estorides.config Key abstractions: CacheConfig, PivotPolicyConfig, PivotConfig, StreamConfig, ReconFusionConfig, SchemaConfig. Depends on estorides_core: entity_resolution (1). Used by estorides_core: estorides_web (8), estorides_core: manager (8), estorides_core: estorides (7).

- `estorides_core/config.py` ranks 1 by PageRank, 52 importers, 29 symbols: estorides.config
- `estorides_core/ssrf_guard.py` ranks 2 by PageRank, 8 importers, 12 symbols: estorides_core.ssrf_guard
- `estorides_core/observation_models.py` ranks 3 by PageRank, 2 importers, 14 symbols: estorides_core.observation_models
- Hotspot `estorides_core/config.py`: 29 symbols, 62 connections (score 0.08).
- Hotspot `estorides_core/intel_resolver.py`: 26 symbols, 21 connections (score 0.06).
- Taint: 9 paths reach this group via requests, urllib.request.
- Key entities: file:estorides_core/config.py, file:estorides_core/ontology.py, file:tests/test_observation_models.py, file:estorides_core/pivot_engine.py, file:estorides_core/async_client.py, file:estorides_core/intel_resolver.py, file:estorides_core/transforms.py, file:estorides_core/observation_models.py
- Rating 7.0/10 = 7 x PageRank share 1.00 + 3 x risk 0.00. Internal imports: 34.

## estorides_core: estorides_web (`c0`, community, rating 3.7)

25 files under tests (py 25), mostly testing. Core file estorides_web.py (PageRank 0.0183, imported by 12 files): estorides.web Key abstractions: deco, wrapper, stop, should_stop, status, done. Depends on estorides_core: config (8), estorides_core: manager (7), estorides_core: estorides (6). Used by estorides_core: estorides (3), estorides_core: hypothesis_engine (1), estorides_core: parsers (1).

- `estorides_web.py` ranks 1 by PageRank, 12 importers, 97 symbols: estorides.web
- `estorides_core/web_security.py` ranks 2 by PageRank, 11 importers, 22 symbols: estorides_core.web_security
- `estorides_core/search_telemetry.py` ranks 3 by PageRank, 5 importers, 22 symbols: estorides.search_telemetry.
- Hotspot `estorides_web.py`: 97 symbols, 121 connections (score 0.24).
- Hotspot `estorides_core/graph_rag_search.py`: 44 symbols, 9 connections (score 0.09).
- Dependency cycle: estorides_web.py -> estorides_web_tools.py -> estorides_web.py.
- 15 layer violations, e.g. estorides_web.py (presentation) -> fusion_store.py (data_access).
- Key entities: file:estorides_web.py, sym:estorides_web.py::create_app@258, sym:estorides_web.py::_rate_limit_decorator@192, file:estorides_core/web_security.py, file:estorides_core/graph_rag_search.py, sym:estorides_web.py::_provides@83, file:estorides_core/search_telemetry.py, file:estorides_core/audit.py
- Rating 3.7/10 = 7 x PageRank share 0.53 + 3 x risk 0.00. Internal imports: 42.

## estorides_core: hypothesis_engine (`c2`, community, rating 3.1)

19 files under tests (py 19), mostly testing. Core file estorides_core/reliability_scoring.py (PageRank 0.0178, imported by 15 files): estorides_core.reliability_scoring Key abstractions: SourceReliability, Credibility, SourceType, ConfidenceInput, ConfidenceResult, compute_confidence. Depends on estorides_core: config (4), estorides_core: estorides_web (1), estorides_core: estorides (1). Used by estorides_core: manager (3), estorides_core: estorides_web (2), estorides_core: estorides (1).

- `estorides_core/reliability_scoring.py` ranks 1 by PageRank, 15 importers, 16 symbols: estorides_core.reliability_scoring
- `estorides_core/ids.py` ranks 2 by PageRank, 6 importers, 1 symbols: estorides_core.ids
- `estorides_core/recon_fusion.py` ranks 3 by PageRank, 4 importers, 19 symbols: estorides_core.recon_fusion
- Hotspot `tests/test_reliability_scoring.py`: 70 symbols, 6 connections (score 0.15).
- Hotspot `tests/test_change_detection.py`: 43 symbols, 6 connections (score 0.09).
- Surprising bridge: lan_inventory.py <-> test_change_detection_properties.py (7 hops across communities).
- Key entities: file:tests/test_reliability_scoring.py, file:tests/test_ui_professional.py, file:tests/test_change_detection.py, file:tests/test_recon_fusion.py, file:tests/test_hypothesis_engine.py, file:tests/test_fusion_analytics.py, file:estorides_core/recon_fusion.py, file:estorides_core/fusion_store.py
- Rating 3.1/10 = 7 x PageRank share 0.44 + 3 x risk 0.00. Internal imports: 31.

## estorides_core: graph_bundle (`c1`, community, rating 3.0)

19 files under tests (py 19), mostly testing. Core file estorides_core/__init__.py (PageRank 0.0315, imported by 27 files): estorides_core.__init__ Key abstractions: family_color_from_name, node_value, force_settings, build_force_payload, build_ai_context, BundleLayout. Depends on estorides_core: config (3). Used by estorides_core: estorides_web (5), estorides_core: estorides (4), estorides_core: system_app_sources (3).

- `estorides_core/__init__.py` ranks 1 by PageRank, 27 importers, 0 symbols: estorides_core.__init__
- `estorides_core/graph_force.py` ranks 2 by PageRank, 6 importers, 12 symbols: graph_force3d: payload force-graph estilo ReadMenator + contexto IA.
- `estorides_core/graph_bundle.py` ranks 3 by PageRank, 11 importers, 18 symbols: graph_bundle: payload circle 2D + sphere 3D estilo ReadMenator.
- Hotspot `tests/test_aviation.py`: 41 symbols, 5 connections (score 0.09).
- Hotspot `tests/test_graph_bundle.py`: 30 symbols, 34 connections (score 0.07).
- Surprising bridge: lan_inventory.py <-> test_change_detection_properties.py (7 hops across communities).
- Key entities: file:tests/test_aviation.py, file:tests/test_data_pack.py, file:tests/test_graph_bundle.py, sym:estorides_core/graph_bundle.py::build_bundle_payload@359, file:estorides_core/graph_bundle.py, file:tests/test_airports.py, file:estorides_core/lan_inventory.py, file:estorides_core/__init__.py
- Rating 3.0/10 = 7 x PageRank share 0.43 + 3 x risk 0.00. Internal imports: 31.

## estorides_core: estorides (`c3`, community, rating 2.5)

17 files under tests (py 16, js 1), mostly testing. Core file estorides_core/sqlite_store.py (PageRank 0.0122, imported by 5 files): estorides_core.sqlite_store Key abstractions: SqliteStore, DictMixin, close, to_dict, CaseStore, fts_available. Depends on estorides_core: config (7), estorides_core: graph_bundle (4), estorides_core: estorides_web (3). Used by estorides_core: estorides_web (6), estorides_core: manager (2), estorides_core: hypothesis_engine (1).

- `estorides_core/sqlite_store.py` ranks 1 by PageRank, 5 importers, 8 symbols: estorides_core.sqlite_store
- `estorides_core/cases.py` ranks 2 by PageRank, 9 importers, 21 symbols: estorides_core.cases
- `estorides_core/monitoring.py` ranks 3 by PageRank, 18 importers, 26 symbols: estorides_core.monitoring
- Hotspot `static/js/estorides.js`: 192 symbols, 1762 connections (score 1.00).
- Hotspot `tests/test_security_remediation.py`: 67 symbols, 56 connections (score 0.16).
- 2 layer violations, e.g. test_hardening.py (testing) -> web_security.py (presentation).
- Taint: 2 paths reach this group via urllib.request.
- Key entities: file:static/js/estorides.js, file:tests/test_security_remediation.py, file:estorides_core/scope.py, file:estorides_cli.py, file:tests/test_monitoring.py, file:estorides_core/monitoring.py, file:estorides_core/cases.py, file:estorides_core/alerter.py
- Rating 2.5/10 = 7 x PageRank share 0.36 + 3 x risk 0.00. Internal imports: 42.

## unassigned files (`c12`, community, rating 2.3)

27 files under .scratchpad (py 22, js 3, sh 2), mostly utility. Core file .scratchpad/gb_shots.py (PageRank 0.0026, imported by 0 files). Key abstractions: LanPolicyRequest, LanPolicyDecision, to_dict, requires_consent, max_contact_for, evaluate.

- `.scratchpad/gb_shots.py` ranks 1 by PageRank, 0 importers, 0 symbols.
- `.scratchpad/gfv2_bridge.py` ranks 2 by PageRank, 0 importers, 0 symbols.
- `.scratchpad/gfv2_click.py` ranks 3 by PageRank, 0 importers, 0 symbols.
- Hotspot `static/js/graph_force.js`: 115 symbols, 737 connections (score 0.49).
- Hotspot `static/js/graph_bundle.js`: 66 symbols, 573 connections (score 0.33).
- Key entities: file:static/js/graph_force.js, file:tests/test_target_management.py, file:static/js/graph_bundle.js, sym:static/js/graph_force.js::settings@72, file:static/js/source_manager.js, file:tests/test_target_scoring.py, file:tests/test_envutil.py, file:tests/properties/test_target_management_properties.py
- Rating 2.3/10 = 7 x PageRank share 0.33 + 3 x risk 0.00. Internal imports: 0.

## estorides_core: parsers (`c8`, community, rating 2.3)

13 files under estorides_core (py 13), mostly utility. Core file estorides_core/aviation.py (PageRank 0.0161, imported by 5 files): estorides_core.aviation Key abstractions: normalize_type_code, classify_aircraft, aircraft_class_label, normalize_squawk, emergency_status, is_emergency. Depends on estorides_core: config (5), estorides_core: graph_bundle (2), estorides_core: manager (2). Used by estorides_core: system_app_sources (4), estorides_core: estorides_web (2), estorides_core: manager (2).

- `estorides_core/aviation.py` ranks 1 by PageRank, 5 importers, 18 symbols: estorides_core.aviation
- `estorides_core/parsers.py` ranks 2 by PageRank, 13 importers, 73 symbols: estorides_core.parsers
- `estorides_core/aerospace.py` ranks 3 by PageRank, 7 importers, 27 symbols: estorides_core.aerospace
- Hotspot `tests/test_aerospace.py`: 121 symbols, 28 connections (score 0.26).
- Hotspot `estorides_core/parsers.py`: 73 symbols, 35 connections (score 0.16).
- 1 layer violations, e.g. test_aerospace.py (testing) -> estorides_web.py (presentation).
- Taint: 9 paths reach this group via requests.
- Key entities: file:tests/test_aerospace.py, file:tests/test_socmint.py, file:estorides_core/parsers.py, file:estorides_core/feeds.py, file:estorides_core/source_loader.py, file:estorides_core/aerospace.py, sym:estorides_core/source_loader.py::all@203, file:estorides_core/aviation.py
- Rating 2.3/10 = 7 x PageRank share 0.33 + 3 x risk 0.00. Internal imports: 31.

## estorides_core: system_app_sources (`c7`, community, rating 2.0)

13 files under tests (py 13), mostly testing. Core file estorides_core/tool_runner.py (PageRank 0.0184, imported by 11 files). Key abstractions: ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError, ToolResult. Depends on estorides_core: config (5), estorides_core: manager (4), estorides_core: parsers (4). Used by estorides_core: manager (2), estorides_core: estorides_web (1), estorides_core: entity_resolution (1).

- `estorides_core/tool_runner.py` ranks 1 by PageRank, 11 importers, 15 symbols.
- `estorides_core/tool_install.py` ranks 2 by PageRank, 7 importers, 27 symbols: estorides_core.tool_install
- `estorides_core/system_app_sources.py` ranks 3 by PageRank, 11 importers, 32 symbols: estorides_core.system_app_sources
- Hotspot `tests/test_system_app_sources.py`: 42 symbols, 38 connections (score 0.10).
- Hotspot `estorides_core/system_app_sources.py`: 32 symbols, 31 connections (score 0.08).
- Key entities: sym:estorides_core/system_app_sources.py::execute@396, file:tests/test_system_app_sources.py, file:estorides_core/system_app_sources.py, file:estorides_core/tool_install.py, file:tests/test_tool_install.py, file:estorides_core/active_recon.py, file:tests/test_active_recon.py, sym:estorides_core/tool_runner.py::run_tool@156
- Rating 2.0/10 = 7 x PageRank share 0.28 + 3 x risk 0.00. Internal imports: 26.

## estorides_core: people_intel (`c5`, community, rating 1.9)

15 files under estorides_core (py 15), mostly utility. Core file estorides_core/cloud_asset_discovery.py (PageRank 0.0051, imported by 3 files). Key abstractions: CloudAsset, CloudAssetDiscoveryResult, CloudAssetDiscoveryError, to_dict, to_dict, generate_bucket_names.

- `estorides_core/cloud_asset_discovery.py` ranks 1 by PageRank, 3 importers, 7 symbols.
- `estorides_core/code_exposure.py` ranks 2 by PageRank, 2 importers, 10 symbols.
- `estorides_core/pdns_monitor.py` ranks 3 by PageRank, 3 importers, 11 symbols.
- Hotspot `tests/test_code_exposure.py`: 21 symbols, 3 connections (score 0.04).
- Hotspot `tests/test_cloud_asset_discovery.py`: 18 symbols, 5 connections (score 0.04).
- Key entities: file:tests/test_code_exposure.py, file:tests/test_cloud_asset_discovery.py, file:tests/test_people_intel.py, file:tests/test_pdns_monitor.py, file:tests/test_tech_fingerprint.py, file:tests/test_supply_chain.py, file:tests/test_vuln_correlation.py, file:estorides_core/supply_chain.py
- Rating 1.9/10 = 7 x PageRank share 0.27 + 3 x risk 0.00. Internal imports: 16.

## estorides_core: manager (`c6`, community, rating 1.9)

14 files under estorides_core (py 14), mostly utility. Core file estorides_core/orchestrator.py (PageRank 0.0078, imported by 13 files): estorides_core.orchestrator Key abstractions: Orchestrator, pending_system_app_tasks, repl, run, BoundedJobRegistry, register. Depends on estorides_core: config (8), estorides_core: hypothesis_engine (3), estorides_core: entity_resolution (3). Used by estorides_core: estorides_web (7), estorides_core: system_app_sources (4), estorides_core: estorides (3).

- `estorides_core/orchestrator.py` ranks 1 by PageRank, 13 importers, 18 symbols: estorides_core.orchestrator
- `estorides_core/job_registry.py` ranks 2 by PageRank, 3 importers, 10 symbols: estorides_core.job_registry
- `estorides_core/pagination.py` ranks 3 by PageRank, 3 importers, 7 symbols: estorides_core.pagination
- Hotspot `tests/test_pagination.py`: 38 symbols, 3 connections (score 0.08).
- Hotspot `estorides_core/orchestrator.py`: 18 symbols, 68 connections (score 0.06).
- Key entities: file:estorides_core/orchestrator.py, file:tests/test_pagination.py, file:estorides_llm/manager.py, sym:estorides_core/job_registry.py::values@105, file:estorides_core/discoverer.py, file:estorides_core/graph_kuzu.py, sym:estorides_core/pagination.py::PaginationConfig@19, sym:estorides_core/orchestrator.py::run@190
- Rating 1.9/10 = 7 x PageRank share 0.28 + 3 x risk 0.00. Internal imports: 20.

## estorides_core: entity_resolution (`c9`, community, rating 1.9)

10 files under estorides_core (py 10), mostly testing. Core file estorides_core/entity_extraction.py (PageRank 0.0276, imported by 18 files): estorides_core.entity_extraction Key abstractions: Entity, to_dict, normalize_query, detect_query_type, extract_from_text, extract_from_json. Depends on estorides_core: config (4), estorides_core: manager (2), estorides_core: hypothesis_engine (1). Used by estorides_core: estorides_web (4), estorides_core: estorides (3), estorides_core: manager (3).

- `estorides_core/entity_extraction.py` ranks 1 by PageRank, 18 importers, 21 symbols: estorides_core.entity_extraction
- `estorides_core/entity_resolution.py` ranks 2 by PageRank, 4 importers, 35 symbols: estorides_core.entity_resolution
- `estorides_core/transliteration.py` ranks 3 by PageRank, 2 importers, 4 symbols: estorides_core.transliteration
- Hotspot `tests/test_entity_resolution.py`: 68 symbols, 11 connections (score 0.15).
- Hotspot `estorides_core/entity_resolution.py`: 35 symbols, 17 connections (score 0.08).
- Key entities: file:tests/test_entity_resolution.py, file:estorides_core/entity_resolution.py, file:estorides_core/entity_extraction.py, file:tests/test_tool_runner.py, sym:estorides_core/entity_resolution.py::resolve_entities@727, sym:tests/test_entity_resolution.py::_ent@28, file:estorides_core/entity_store.py, file:estorides_core/validation.py
- Rating 1.9/10 = 7 x PageRank share 0.28 + 3 x risk 0.00. Internal imports: 13.

## estorides_export (`c10`, community, rating 1.3)

8 files under estorides_export (py 8), mostly utility. Core file estorides_core/knowledge_graph.py (PageRank 0.0087, imported by 8 files): estorides_core.knowledge_graph Key abstractions: KnowledgeGraph, add_entity, add_observation, add_relationship, export_graphml, export_json. Depends on estorides_core: config (3), estorides_core: entity_resolution (2), estorides_core: estorides (1). Used by estorides_core: estorides_web (4), estorides_core: estorides (2), estorides_core: manager (1).

- `estorides_core/knowledge_graph.py` ranks 1 by PageRank, 8 importers, 18 symbols: estorides_core.knowledge_graph
- `estorides_export/__init__.py` ranks 2 by PageRank, 4 importers, 0 symbols: estorides_export
- `estorides_export/recon_report.py` ranks 3 by PageRank, 3 importers, 11 symbols.
- Hotspot `estorides_core/knowledge_graph.py`: 18 symbols, 21 connections (score 0.04).
- Hotspot `tests/test_recon_report.py`: 19 symbols, 6 connections (score 0.04).
- Dependency cycle: __init__.py -> encryption.py -> __init__.py.
- Surprising bridge: test_change_detection_properties.py <-> test_recon_report.py (7 hops across communities).
- Key entities: file:estorides_core/knowledge_graph.py, file:tests/test_recon_report.py, file:estorides_export/recon_report.py, file:estorides_export/encryption.py, file:tests/test_encrypted_export.py, file:estorides_export/stix.py, sym:estorides_core/knowledge_graph.py::add_relationship@142, file:estorides_export/misp.py
- Rating 1.3/10 = 7 x PageRank share 0.18 + 3 x risk 0.00. Internal imports: 15.

## estorides_core: source_health_monitoring (`c11`, community, rating 0.4)

3 files under tests/properties (py 3), mostly testing. Core file estorides_core/source_health_monitoring.py (PageRank 0.0070, imported by 2 files): estorides_core.source_health_monitoring Key abstractions: SourceHealthStatus, SourceHealthConfig, SourceHealthInput, SourceHealthResult, DashboardSummary, HealthDashboard.

- `estorides_core/source_health_monitoring.py` ranks 1 by PageRank, 2 importers, 14 symbols: estorides_core.source_health_monitoring
- `tests/properties/test_source_health_monitoring_properties.py` ranks 2 by PageRank, 0 importers, 7 symbols: Property-based invariants for estorides_core.source_health_monitoring.
- `tests/test_source_health_monitoring.py` ranks 3 by PageRank, 0 importers, 52 symbols: BDD tests for estorides_core.source_health_monitoring.
- Hotspot `tests/test_source_health_monitoring.py`: 52 symbols, 5 connections (score 0.11).
- Hotspot `estorides_core/source_health_monitoring.py`: 14 symbols, 8 connections (score 0.03).
- Key entities: file:tests/test_source_health_monitoring.py, sym:estorides_core/source_health_monitoring.py::SourceHealthInput@98, sym:estorides_core/source_health_monitoring.py::compute_health@235, file:estorides_core/source_health_monitoring.py, file:tests/properties/test_source_health_monitoring_properties.py, sym:estorides_core/source_health_monitoring.py::build_dashboard@295, sym:tests/test_source_health_monitoring.py::test_hot_sources_are_healthy@295, sym:estorides_core/source_health_monitoring.py::SourceHealthConfig@42
- Rating 0.4/10 = 7 x PageRank share 0.06 + 3 x risk 0.00. Internal imports: 2.
