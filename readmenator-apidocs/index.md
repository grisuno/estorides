# estorides API Reference

> Generated offline by readmenator: 104 modules, 2443 documented entities, documentation coverage 48.1% (643/1338 public items). Deterministic, zero tokens: signatures from source, docs parsed from Google, NumPy, reST, Javadoc/JSDoc/Doxygen, C# XML, and Rustdoc comments.

Navigate: [Interactive architecture and flows](flows.html) | [Architecture and flows (Mermaid)](architecture.md) | [Class hierarchy](classes.md) | [General index](genindex.md) | [Coverage and warnings](COVERAGE.md) | [`api/index.json`](api/index.json) | [HTML browser](index.html)

Languages: js (4), py (99), sh (1)

## Modules

### `.`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`app`](modules/app.py.md) | Deprecated entry point. | 0 | 0 | 100.0% |
| [`estorides_cli`](modules/estorides_cli.py.md) | estorides CLI. | 0 | 24 | 36.0% |
| [`estorides_web`](modules/estorides_web.py.md) | estorides.web ============= Flask app providing: * 2D map (Leaflet) * knowledge graph (D3.js force-directed) * timeline * source results panel * multi-LLM... | 0 | 1 | 50.0% |
| [`estorides_web_tools`](modules/estorides_web_tools.py.md) | estorides_web_tools =================== Tools vertical slice extracted from the ``create_app`` God factory. | 0 | 4 | 20.0% |
| [`install.sh`](modules/install.sh.md) | Bootstrap a venv and install the runtime + optional test dependencies. | 0 | 2 | 66.7% |
| [`web`](modules/web.py.md) | Deprecated entry point. | 0 | 0 | 100.0% |
| [`wsgi`](modules/wsgi.py.md) | estorides.wsgi ============== | 0 | 0 | 100.0% |

### `.scratchpad`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`.scratchpad.gb_shots`](modules/scratchpad.gb_shots.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_bridge`](modules/scratchpad.gfv2_bridge.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_click`](modules/scratchpad.gfv2_click.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_data`](modules/scratchpad.gfv2_data.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_debug`](modules/scratchpad.gfv2_debug.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_dom`](modules/scratchpad.gfv2_dom.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_func`](modules/scratchpad.gfv2_func.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_raw`](modules/scratchpad.gfv2_raw.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_shots`](modules/scratchpad.gfv2_shots.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_step`](modules/scratchpad.gfv2_step.py.md) |  | 0 | 0 | 0.0% |
| [`.scratchpad.gfv2_time`](modules/scratchpad.gfv2_time.py.md) |  | 0 | 0 | 0.0% |

### `estorides_core`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`estorides_core`](modules/estorides_core.__init__.py.md) | estorides_core.__init__ | 0 | 0 | 100.0% |
| [`estorides_core.active_recon`](modules/estorides_core.active_recon.py.md) |  | 5 | 15 | 0.0% |
| [`estorides_core.aerospace`](modules/estorides_core.aerospace.py.md) | estorides_core.aerospace ======================== Pure normalisers and orbital helpers for the free air-and-space intelligence layer set. | 0 | 16 | 100.0% |
| [`estorides_core.airports`](modules/estorides_core.airports.py.md) | estorides_core.airports ======================= Public-domain airport reference data and a nearest-airport index. | 1 | 8 | 90.0% |
| [`estorides_core.alerter`](modules/estorides_core.alerter.py.md) | estorides_core.alerter ====================== Alert channel dispatcher for watch target notifications. | 1 | 4 | 100.0% |
| [`estorides_core.async_client`](modules/estorides_core.async_client.py.md) | estorides_core.async_client =========================== Async HTTP client with: * per-host concurrency limits * exponential backoff * circuit breaker (per... | 3 | 10 | 35.7% |
| [`estorides_core.audit`](modules/estorides_core.audit.py.md) | estorides_core.audit ==================== Append-only audit log + per-IP rate limiter for the web layer. | 3 | 7 | 36.4% |
| [`estorides_core.aviation`](modules/estorides_core.aviation.py.md) | estorides_core.aviation ======================= Pure aircraft-intelligence helpers shared by the aerospace sources and the real-time map feeds. | 0 | 14 | 100.0% |
| [`estorides_core.case_crypto`](modules/estorides_core.case_crypto.py.md) | estorides_core.case_crypto ========================== Opt in field encryption for case notes and analysis at rest. | 0 | 3 | 100.0% |
| [`estorides_core.cases`](modules/estorides_core.cases.py.md) | estorides_core.cases ==================== Run persistence — every intelligence query becomes a "case" that survives across sessions. | 1 | 15 | 64.7% |
| [`estorides_core.change_detection`](modules/estorides_core.change_detection.py.md) | estorides_core.change_detection =============================== The temporal layer: "what changed in this investigation since the last run?". | 8 | 1 | 100.0% |
| [`estorides_core.cloud_asset_discovery`](modules/estorides_core.cloud_asset_discovery.py.md) |  | 3 | 4 | 0.0% |
| [`estorides_core.code_exposure`](modules/estorides_core.code_exposure.py.md) |  | 3 | 6 | 0.0% |
| [`estorides_core.config`](modules/estorides_core.config.py.md) | estorides.config ================ Central configuration. | 8 | 14 | 100.0% |
| [`estorides_core.discoverer`](modules/estorides_core.discoverer.py.md) | Background subdomain/domain discoverer. | 1 | 7 | 77.8% |
| [`estorides_core.entity_extraction`](modules/estorides_core.entity_extraction.py.md) | estorides_core.entity_extraction ================================ Single source of truth for finding entities (IPs, domains, emails, CVEs, crypto addresses... | 1 | 7 | 77.8% |
| [`estorides_core.entity_resolution`](modules/estorides_core.entity_resolution.py.md) | estorides_core.entity_resolution ================================ Canonical identity layer. | 5 | 13 | 78.9% |
| [`estorides_core.entity_store`](modules/estorides_core.entity_store.py.md) | estorides_core.entity_store =========================== Cross-run canonical identity store. | 1 | 4 | 100.0% |
| [`estorides_core.event_bus`](modules/estorides_core.event_bus.py.md) | estorides_core.event_bus ======================== In process publish subscribe channel for orchestrator lifecycle events. | 1 | 7 | 100.0% |
| [`estorides_core.feeds`](modules/estorides_core.feeds.py.md) | estorides_core.feeds ==================== Real-time intelligence feeds, polled and cached locally. | 10 | 9 | 85.0% |
| [`estorides_core.fusion_analytics`](modules/estorides_core.fusion_analytics.py.md) | estorides_core.fusion_analytics =============================== Intelligence analytics layer over the fusion store. | 1 | 9 | 18.2% |
| [`estorides_core.fusion_store`](modules/estorides_core.fusion_store.py.md) | estorides_core.fusion_store =========================== The data-fusion datastore — the single place where everything every source (loaded from the YAML... | 1 | 14 | 100.0% |
| [`estorides_core.graph_bundle`](modules/estorides_core.graph_bundle.py.md) | graph_bundle: payload circle 2D + sphere 3D estilo ReadMenator. | 2 | 5 | 100.0% |
| [`estorides_core.graph_force`](modules/estorides_core.graph_force.py.md) | graph_force3d: payload force-graph estilo ReadMenator + contexto IA. | 0 | 5 | 100.0% |
| [`estorides_core.graph_kuzu`](modules/estorides_core.graph_kuzu.py.md) | estorides_core.graph_kuzu ========================= Persistent graph backend powered by Kuzu (embedded Cypher DB). | 1 | 7 | 77.8% |
| [`estorides_core.graph_rag_search`](modules/estorides_core.graph_rag_search.py.md) | graph_rag_search: GraphRAG local/global para la IA local (sin LLM). | 9 | 16 | 46.2% |
| [`estorides_core.hypothesis_engine`](modules/estorides_core.hypothesis_engine.py.md) | estorides_core.hypothesis_engine ================================ The "data → information" layer. | 3 | 1 | 100.0% |
| [`estorides_core.ids`](modules/estorides_core.ids.py.md) | estorides_core.ids ================== Deterministic content-addressed identifiers. | 0 | 1 | 100.0% |
| [`estorides_core.intel_resolver`](modules/estorides_core.intel_resolver.py.md) | estorides_core.intel_resolver ============================= Cross-feed entity resolver. | 1 | 2 | 50.0% |
| [`estorides_core.job_registry`](modules/estorides_core.job_registry.py.md) | estorides_core.job_registry =========================== | 1 | 7 | 66.7% |
| [`estorides_core.knowledge_graph`](modules/estorides_core.knowledge_graph.py.md) | estorides_core.knowledge_graph ============================== Persistent in-memory knowledge graph backed by NetworkX. | 1 | 13 | 40.0% |
| [`estorides_core.lan_bundle`](modules/estorides_core.lan_bundle.py.md) | estorides_core.lan_bundle ========================= LAN output deliverables for automation. | 1 | 5 | 85.7% |
| [`estorides_core.lan_inventory`](modules/estorides_core.lan_inventory.py.md) | estorides_core.lan_inventory ============================ Passive-first LAN device inventory. | 1 | 10 | 91.7% |
| [`estorides_core.lan_policy`](modules/estorides_core.lan_policy.py.md) | estorides_core.lan_policy ========================= Authorization and contact ceiling for LAN discovery runs. | 2 | 4 | 85.7% |
| [`estorides_core.lan_runner`](modules/estorides_core.lan_runner.py.md) | estorides_core.lan_runner ========================= Real LAN scan execution: passive readers plus one gated active tool. | 1 | 5 | 85.7% |
| [`estorides_core.lan_scope`](modules/estorides_core.lan_scope.py.md) | estorides_core.lan_scope ======================== Private local scope auto-detection. | 0 | 5 | 100.0% |
| [`estorides_core.lan_web`](modules/estorides_core.lan_web.py.md) | estorides_core.lan_web ====================== Backend guard for LAN discovery runs from the web layer. | 1 | 5 | 85.7% |
| [`estorides_core.mitre_attack`](modules/estorides_core.mitre_attack.py.md) | estorides_core.mitre_attack =========================== Lightweight MITRE ATT&CK mapper. | 0 | 3 | 100.0% |
| [`estorides_core.monitoring`](modules/estorides_core.monitoring.py.md) | estorides_core.monitoring ========================= Watch targets and scheduling for recurring OSINT monitoring. | 3 | 20 | 41.7% |
| [`estorides_core.observation_models`](modules/estorides_core.observation_models.py.md) | estorides_core.observation_models ================================ Strict, versioned Pydantic v2 data contracts for the observation and entity records that... | 4 | 4 | 55.6% |
| [`estorides_core.ontology`](modules/estorides_core.ontology.py.md) | estorides_core.ontology ======================= The "centralized ontology engine" — the brain of the platform. | 4 | 14 | 42.1% |
| [`estorides_core.openapi`](modules/estorides_core.openapi.py.md) | estorides_core.openapi ====================== Minimal OpenAPI document generated from the live Flask url map. | 0 | 1 | 100.0% |
| [`estorides_core.ops_observability`](modules/estorides_core.ops_observability.py.md) | estorides_core.ops_observability ================================ Single user operational visibility without external dependencies. | 1 | 8 | 100.0% |
| [`estorides_core.orchestrator`](modules/estorides_core.orchestrator.py.md) | estorides_core.orchestrator ============================ The main entry point. | 1 | 3 | 60.0% |
| [`estorides_core.osiris_sources`](modules/estorides_core.osiris_sources.py.md) | estorides_core.osiris_sources ============================= Extra OSINT endpoints borrowed from the Osiris project (simplifaisoul/osiris). | 0 | 7 | 100.0% |
| [`estorides_core.pagination`](modules/estorides_core.pagination.py.md) | estorides_core.pagination ========================= Pagination strategies for source API fetches. | 1 | 6 | 62.5% |
| [`estorides_core.parsers`](modules/estorides_core.parsers.py.md) | estorides_core.parsers ====================== A small library of structured parsers. | 0 | 66 | 44.8% |
| [`estorides_core.pdns_monitor`](modules/estorides_core.pdns_monitor.py.md) |  | 4 | 7 | 0.0% |
| [`estorides_core.people_intel`](modules/estorides_core.people_intel.py.md) |  | 4 | 7 | 0.0% |
| [`estorides_core.pivot_engine`](modules/estorides_core.pivot_engine.py.md) | estorides_core.pivot_engine =========================== Recursive, asynchronous cross-search engine — the Palantir-style core. | 9 | 10 | 70.0% |
| [`estorides_core.recon_fusion`](modules/estorides_core.recon_fusion.py.md) | estorides_core.recon_fusion =========================== Passive reconnaissance fusion engine: groups, deduplicates and classifies OSINT results by relevance... | 4 | 5 | 70.0% |
| [`estorides_core.recon_pipeline`](modules/estorides_core.recon_pipeline.py.md) |  | 0 | 1 | 0.0% |
| [`estorides_core.relationship_inference`](modules/estorides_core.relationship_inference.py.md) | estorides_core.relationship_inference ===================================== Strategy registry for deriving higher-level knowledge-graph edges from raw... | 1 | 3 | 80.0% |
| [`estorides_core.reliability_scoring`](modules/estorides_core.reliability_scoring.py.md) | estorides_core.reliability_scoring ================================== Single source of truth for the ``confidence`` of an observation. | 5 | 6 | 100.0% |
| [`estorides_core.scope`](modules/estorides_core.scope.py.md) | estorides_core.scope ===================== Bug-bounty scope classification. | 7 | 26 | 88.2% |
| [`estorides_core.search_telemetry`](modules/estorides_core.search_telemetry.py.md) | estorides.search_telemetry. | 9 | 10 | 95.0% |
| [`estorides_core.socmint`](modules/estorides_core.socmint.py.md) | estorides_core.socmint ====================== Social Media Intelligence (SOCMINT) module. | 4 | 6 | 72.7% |
| [`estorides_core.source_health_monitoring`](modules/estorides_core.source_health_monitoring.py.md) | estorides_core.source_health_monitoring ======================================= Per-source operational health tracking. | 6 | 4 | 81.8% |
| [`estorides_core.source_loader`](modules/estorides_core.source_loader.py.md) | estorides_core.source_loader ============================ Loads all YAML sources, normalises the schema, and provides a registry the rest of the engine can... | 2 | 12 | 46.7% |
| [`estorides_core.sqlite_store`](modules/estorides_core.sqlite_store.py.md) | estorides_core.sqlite_store =========================== Shared plumbing for the hand-rolled SQLite stores. | 2 | 3 | 50.0% |
| [`estorides_core.ssrf_guard`](modules/estorides_core.ssrf_guard.py.md) | estorides_core.ssrf_guard ========================= SSRF / SSRF-rebound protection for outbound HTTP. | 2 | 2 | 80.0% |
| [`estorides_core.supply_chain`](modules/estorides_core.supply_chain.py.md) |  | 4 | 9 | 0.0% |
| [`estorides_core.system_app_sources`](modules/estorides_core.system_app_sources.py.md) | estorides_core.system_app_sources ================================= Kali OSINT CLI tools as first-class sources (`kind: system_app`). | 1 | 25 | 37.0% |
| [`estorides_core.tech_fingerprint`](modules/estorides_core.tech_fingerprint.py.md) |  | 2 | 3 | 0.0% |
| [`estorides_core.tool_install`](modules/estorides_core.tool_install.py.md) | estorides_core.tool_install =========================== One-click installation for missing Kali/OSINT CLI tools, modelled on the LazyOwn lazyaddon mechanism... | 3 | 13 | 76.5% |
| [`estorides_core.tool_runner`](modules/estorides_core.tool_runner.py.md) |  | 7 | 4 | 0.0% |
| [`estorides_core.transforms`](modules/estorides_core.transforms.py.md) | estorides_core.transforms ========================= Maltego-style transform registry. | 2 | 7 | 50.0% |
| [`estorides_core.transliteration`](modules/estorides_core.transliteration.py.md) | estorides_core.transliteration ============================== Cross-script name normalisation for entity resolution. | 0 | 3 | 100.0% |
| [`estorides_core.validation`](modules/estorides_core.validation.py.md) | estorides_core.validation ========================= Input validation for free-form queries. | 2 | 2 | 80.0% |
| [`estorides_core.vuln_correlation`](modules/estorides_core.vuln_correlation.py.md) |  | 3 | 6 | 0.0% |
| [`estorides_core.web_security`](modules/estorides_core.web_security.py.md) | estorides_core.web_security =========================== | 2 | 13 | 81.2% |

### `estorides_export`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`estorides_export`](modules/estorides_export.__init__.py.md) | estorides_export | 0 | 0 | 100.0% |
| [`estorides_export.encryption`](modules/estorides_export.encryption.py.md) | estorides_export.encryption =========================== Optional age-encrypted report export. | 0 | 3 | 75.0% |
| [`estorides_export.misp`](modules/estorides_export.misp.py.md) | estorides_export.misp ===================== Minimal MISP event JSON. | 0 | 2 | 33.3% |
| [`estorides_export.recon_report`](modules/estorides_export.recon_report.py.md) |  | 3 | 7 | 0.0% |
| [`estorides_export.report`](modules/estorides_export.report.py.md) | estorides_export.report ======================= | 0 | 1 | 100.0% |
| [`estorides_export.stix`](modules/estorides_export.stix.py.md) | estorides_export.stix ===================== STIX 2.1 bundle export. | 0 | 2 | 33.3% |

### `estorides_llm`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`estorides_llm`](modules/estorides_llm.__init__.py.md) | estorides_llm | 0 | 0 | 100.0% |
| [`estorides_llm.intelligence_prompts`](modules/estorides_llm.intelligence_prompts.py.md) | estorides_llm.intelligence_prompts ================================== System prompt and context-formatting helpers for the LLM analyst. | 0 | 1 | 100.0% |
| [`estorides_llm.manager`](modules/estorides_llm.manager.py.md) | estorides_llm.manager ===================== Multi-backend LLM router with pluggable backends. | 6 | 11 | 55.6% |

### `static/js`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`static/js/estorides.js`](modules/static.js.estorides.js.md) | Estorides front-end controller | 4 | 183 | 25.0% |
| [`static/js/graph_bundle.js`](modules/static.js.graph_bundle.js.md) | Estorides Bundles — circle 2D + sphere 3D hierarchical edge bundling. | 0 | 66 | 1.5% |
| [`static/js/graph_force.js`](modules/static.js.graph_force.js.md) | Estorides force-graph module (spec/graph_force3d.md). | 0 | 115 | 7.8% |
| [`static/js/source_manager.js`](modules/static.js.source_manager.js.md) | Estorides Source Manager — form-based YAML editor | 1 | 18 | 75.0% |

### `tools`

| Module | Summary | Types | Callables | Coverage |
|---|---|---|---|---|
| [`tools.split_sources`](modules/tools.split_sources.py.md) | Split legacy grouped source files into one addon per file. | 0 | 1 | 50.0% |
| [`tools.sync_docs`](modules/tools.sync_docs.py.md) | tools.sync_docs =============== Generate docs manifest from source truth and fail on drift. | 0 | 2 | 100.0% |
