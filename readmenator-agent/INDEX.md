# Index

| File | Purpose | Subsystem | Symbols |
|------|---------|-----------|---------|
| `_multi_test.sh` | - | root | 0 |
| `app.py` | Deprecated entry point. Use:  - the `estorides` console script (installed by `pi | root | 0 |
| `estorides_cli.py` | estorides CLI.  Usage: estorides "example.com" estorides "8.8.8.8" --include-pai | root | 31 |
| `estorides_core/__init__.py` | estorides_core.__init__ | estorides_core | 0 |
| `estorides_core/active_recon.py` | - | estorides_core | 25 |
| `estorides_core/alerter.py` | estorides_core.alerter ====================== Alert channel dispatcher for watch | estorides_core | 13 |
| `estorides_core/async_client.py` | estorides_core.async_client =========================== Async HTTP client with:  | estorides_core | 21 |
| `estorides_core/audit.py` | estorides_core.audit ==================== Append-only audit log + per-IP rate li | estorides_core | 11 |
| `estorides_core/cases.py` | estorides_core.cases ==================== Run persistence — every intelligence q | estorides_core | 18 |
| `estorides_core/change_detection.py` | estorides_core.change_detection =============================== The temporal lay | estorides_core | 20 |
| `estorides_core/cloud_asset_discovery.py` | - | estorides_core | 7 |
| `estorides_core/code_exposure.py` | - | estorides_core | 10 |
| `estorides_core/config.py` | estorides.config ================ Central configuration. Everything tunable live | estorides_core | 23 |
| `estorides_core/discoverer.py` | Background subdomain/domain discoverer.  Drops a seed and walks the passive atta | estorides_core | 21 |
| `estorides_core/entity_extraction.py` | estorides_core.entity_extraction ================================ Single source  | estorides_core | 19 |
| `estorides_core/entity_resolution.py` | estorides_core.entity_resolution ================================ Canonical iden | estorides_core | 35 |
| `estorides_core/entity_store.py` | estorides_core.entity_store =========================== Cross-run canonical iden | estorides_core | 5 |
| `estorides_core/feeds.py` | estorides_core.feeds ==================== Real-time intelligence feeds, polled a | estorides_core | 16 |
| `estorides_core/fusion_analytics.py` | estorides_core.fusion_analytics =============================== Intelligence ana | estorides_core | 14 |
| `estorides_core/fusion_store.py` | estorides_core.fusion_store =========================== The data-fusion datastor | estorides_core | 18 |
| `estorides_core/graph_kuzu.py` | estorides_core.graph_kuzu ========================= Persistent graph backend pow | estorides_core | 11 |
| `estorides_core/hypothesis_engine.py` | estorides_core.hypothesis_engine ================================ The "data → in | estorides_core | 23 |
| `estorides_core/ids.py` | estorides_core.ids ================== Deterministic content-addressed identifier | estorides_core | 1 |
| `estorides_core/intel_resolver.py` | estorides_core.intel_resolver ============================= Cross-feed entity re | estorides_core | 26 |
| `estorides_core/job_registry.py` | estorides_core.job_registry ===========================  Bounded, TTL-aware regi | estorides_core | 10 |
| `estorides_core/knowledge_graph.py` | estorides_core.knowledge_graph ============================== Persistent in-memo | estorides_core | 17 |
| `estorides_core/mitre_attack.py` | estorides_core.mitre_attack =========================== Lightweight MITRE ATT&CK | estorides_core | 4 |
| `estorides_core/monitoring.py` | estorides_core.monitoring ========================= Watch targets and scheduling | estorides_core | 26 |
| `estorides_core/observation_models.py` | estorides_core.observation_models ================================ Strict, versi | estorides_core | 14 |
| `estorides_core/ontology.py` | estorides_core.ontology ======================= The "centralized ontology engine | estorides_core | 25 |
| `estorides_core/orchestrator.py` | estorides_core.orchestrator ============================ The main entry point. G | estorides_core | 18 |
| `estorides_core/osiris_sources.py` | estorides_core.osiris_sources ============================= Extra OSINT endpoint | estorides_core | 8 |
| `estorides_core/pagination.py` | estorides_core.pagination ========================= Pagination strategies for so | estorides_core | 7 |
| `estorides_core/parsers.py` | estorides_core.parsers ====================== A small library of structured pars | estorides_core | 63 |
| `estorides_core/pdns_monitor.py` | - | estorides_core | 11 |
| `estorides_core/people_intel.py` | - | estorides_core | 13 |
| `estorides_core/pivot_engine.py` | estorides_core.pivot_engine =========================== Recursive, asynchronous  | estorides_core | 25 |
| `estorides_core/recon_fusion.py` | estorides_core.recon_fusion =========================== Passive reconnaissance f | estorides_core | 19 |
| `estorides_core/recon_pipeline.py` | - | estorides_core | 1 |
| `estorides_core/relationship_inference.py` | estorides_core.relationship_inference ===================================== Stra | estorides_core | 16 |
| `estorides_core/reliability_scoring.py` | estorides_core.reliability_scoring ================================== Single sou | estorides_core | 16 |
| `estorides_core/scope.py` | estorides_core.scope ===================== Bug-bounty scope classification.  Tak | estorides_core | 39 |
| `estorides_core/search_telemetry.py` | estorides.search_telemetry.  Single source of truth for the operator-facing tele | estorides_core | 22 |
| `estorides_core/socmint.py` | estorides_core.socmint ====================== Social Media Intelligence (SOCMINT | estorides_core | 12 |
| `estorides_core/source_health_monitoring.py` | estorides_core.source_health_monitoring =======================================  | estorides_core | 14 |
| `estorides_core/source_loader.py` | estorides_core.source_loader ============================ Loads all YAML sources | estorides_core | 20 |
| `estorides_core/sqlite_store.py` | estorides_core.sqlite_store =========================== Shared plumbing for the  | estorides_core | 7 |
| `estorides_core/ssrf_guard.py` | estorides_core.ssrf_guard ========================= SSRF / SSRF-rebound protecti | estorides_core | 12 |
| `estorides_core/supply_chain.py` | - | estorides_core | 13 |
| `estorides_core/system_app_sources.py` | estorides_core.system_app_sources ================================= Kali OSINT C | estorides_core | 32 |
| `estorides_core/tech_fingerprint.py` | - | estorides_core | 6 |
| `estorides_core/tool_install.py` | estorides_core.tool_install =========================== One-click installation f | estorides_core | 19 |
| `estorides_core/tool_runner.py` | - | estorides_core | 15 |
| `estorides_core/transforms.py` | estorides_core.transforms ========================= Maltego-style transform regi | estorides_core | 17 |
| `estorides_core/transliteration.py` | estorides_core.transliteration ============================== Cross-script name  | estorides_core | 4 |
| `estorides_core/validation.py` | estorides_core.validation ========================= Input validation for free-fo | estorides_core | 6 |
| `estorides_core/vuln_correlation.py` | - | estorides_core | 11 |
| `estorides_core/web_security.py` | estorides_core.web_security ===========================  Production-grade web ha | estorides_core | 22 |
| `estorides_export/__init__.py` | estorides_export | estorides_export | 0 |
| `estorides_export/encryption.py` | estorides_export.encryption =========================== Optional age-encrypted r | estorides_export | 4 |
| `estorides_export/misp.py` | estorides_export.misp ===================== Minimal MISP event JSON. Mirrors STI | estorides_export | 3 |
| `estorides_export/recon_report.py` | - | estorides_export | 11 |
| `estorides_export/report.py` | estorides_export.report =======================  Markdown report generation for  | estorides_export | 6 |
| `estorides_export/stix.py` | estorides_export.stix ===================== STIX 2.1 bundle export. Each unique  | estorides_export | 4 |
| `estorides_llm/__init__.py` | estorides_llm | estorides_llm | 0 |
| `estorides_llm/intelligence_prompts.py` | estorides_llm.intelligence_prompts ================================== System pro | estorides_llm | 1 |
| `estorides_llm/manager.py` | estorides_llm.manager ===================== Multi-backend LLM router with plugga | estorides_llm | 22 |
| `estorides_web.py` | estorides.web ============= Flask app providing: * 2D map     (Leaflet) * knowle | root | 91 |
| `install.sh` | Bootstrap a venv and install the runtime + optional test dependencies.  Idempote | root | 2 |
| `static/js/estorides.js` | Estorides front-end controller | js | 160 |
| `static/js/source_manager.js` | Estorides Source Manager — form-based YAML editor | js | 18 |
| `tests/conftest.py` | Pytest configuration and shared fixtures for the estorides test suite. | tests | 0 |
| `tests/properties/test_change_detection_properties.py` | Property-based invariants for estorides_core.change_detection.  Hypothesis fuzzi | properties | 8 |
| `tests/properties/test_csp_safe_styles_properties.py` | Property-based fuzz for `csp_safe_styles`.  Defends against a future contributor | properties | 3 |
| `tests/properties/test_hypothesis_engine_properties.py` | Property-based invariants for estorides_core.hypothesis_engine.  Hypothesis fuzz | properties | 9 |
| `tests/properties/test_observation_models_properties.py` | Property-based invariants for estorides_core.observation_models.  Each ``@given` | properties | 7 |
| `tests/properties/test_parsers_properties.py` | Property-based fuzzing for the parser totality contract (doctrine §6).  Every re | properties | 1 |
| `tests/properties/test_recon_fusion_properties.py` | Property-based fuzzing for recon_fusion module (doctrine section 6).  Verifies i | properties | 17 |
| `tests/properties/test_reliability_scoring_properties.py` | Property-based invariants for estorides_core.reliability_scoring.  Hypothesis re | properties | 12 |
| `tests/properties/test_search_telemetry_properties.py` | Property-based fuzzing for `search_telemetry` (spec S12 + predicate laws).  Each | properties | 6 |
| `tests/properties/test_source_health_monitoring_properties.py` | Property-based invariants for estorides_core.source_health_monitoring.  Hypothes | properties | 7 |
| `tests/properties/test_system_app_sources_properties.py` | Property-based invariants for estorides_core.system_app_sources.  Hypothesis rep | properties | 6 |
| `tests/properties/test_target_management_properties.py` | - | properties | 10 |
| `tests/properties/test_tool_runner_properties.py` | Property-based invariants for estorides_core.tool_runner.  Hypothesis replaces l | properties | 3 |
| `tests/test_active_recon.py` | ATDD + BDD tests for estorides_core.active_recon.  Implements the Given-When-The | tests | 24 |
| `tests/test_async_client.py` | BDD tests for egress anonymisation wiring (`estorides_core.async_client`).  Port | tests | 15 |
| `tests/test_audit_log.py` | AuditLog rotation: file size cap, in-place .N rotation (issue #48). | tests | 5 |
| `tests/test_auth_gate.py` | Auth gate: bearer-token protection for sensitive /api/* routes.  When `ESTORIDES | tests | 10 |
| `tests/test_change_detection.py` | ATDD + BDD tests for estorides_core.change_detection.  Implements the Given-When | tests | 43 |
| `tests/test_cli_watch.py` | BDD / regression tests for the `estorides watch add` CLI path.  Context (boy-sco | tests | 16 |
| `tests/test_cloud_asset_discovery.py` | ATDD + BDD tests for estorides_core.cloud_asset_discovery.  Implements the Given | tests | 18 |
| `tests/test_code_exposure.py` | ATDD + BDD tests for estorides_core.code_exposure.  Implements the Given-When-Th | tests | 21 |
| `tests/test_config_env.py` | BDD / regression tests for fault-tolerant configuration parsing.  Doctrine (`con | tests | 13 |
| `tests/test_csp_safe_styles.py` | CSP-safe styles: regression tests for the inline-style bug introduced by the CSP | tests | 11 |
| `tests/test_encrypted_export.py` | Encrypted export: plaintext must be removed after encryption.  Issue #8 reported | tests | 9 |
| `tests/test_entity_extraction.py` | BDD / regression tests for entity extraction and fuzzy merge.  - EE1: `types=[]` | tests | 7 |
| `tests/test_entity_resolution.py` | BDD tests for estorides_core.entity_resolution.  These tests implement the Given | tests | 68 |
| `tests/test_envutil.py` | BDD tests for the shared env readers (spec/envutil.md). | tests | 12 |
| `tests/test_fusion_analytics.py` | ATDD + BDD tests for estorides_core.fusion_analytics.  Implements the Given-When | tests | 36 |
| `tests/test_hardening.py` | BDD tests for the v1.3 hardening surface, case diff and report.  Ported from the | tests | 17 |
| `tests/test_hypothesis_engine.py` | ATDD + BDD tests for estorides_core.hypothesis_engine.  Implements the Given-Whe | tests | 35 |
| `tests/test_ids.py` | BDD tests for the shared deterministic id helper (spec/ids.md).  - ID1: determin | tests | 7 |
| `tests/test_job_registry.py` | BoundedJobRegistry: size cap + TTL eviction (issues #14, #20, #50). | tests | 8 |
| `tests/test_monitoring.py` | BDD tests for Monitoring & Advanced Recon modules.  Covers: - M1: Create a watch | tests | 35 |
| `tests/test_observation_models.py` | estorides_core.observation_models — BDD/TDD contract tests.  Each test is the ex | tests | 28 |
| `tests/test_opsec_contact.py` | BDD tests for operator-OPSEC contact classification + passive-only filter.  Port | tests | 14 |
| `tests/test_pagination.py` | BDD tests for estorides_core.pagination.  These tests verify the pagination stra | tests | 38 |
| `tests/test_parsers.py` | BDD / regression tests for the remote-JSON parser layer.  Doctrine (`parsers.py` | tests | 9 |
| `tests/test_pdns_monitor.py` | ATDD + BDD tests for estorides_core.pdns_monitor.  Implements the Given-When-The | tests | 17 |
| `tests/test_people_intel.py` | ATDD + BDD tests for estorides_core.people_intel.  Implements the Given-When-The | tests | 18 |
| `tests/test_probabilistic_fusion.py` | BDD + property tests for probabilistic fusion.  These tests verify that :meth:`F | tests | 27 |
| `tests/test_recon_fusion.py` | BDD tests for the recon_fusion module (Modulo 2g).  Each scenario maps to a Give | tests | 33 |
| `tests/test_recon_report.py` | ATDD + BDD tests for estorides_export.recon_report.  Implements the Given-When-T | tests | 19 |
| `tests/test_reliability_scoring.py` | ATDD + BDD tests for estorides_core.reliability_scoring.  These tests implement  | tests | 70 |
| `tests/test_scope.py` | BDD tests for the bug-bounty scope classifier (`estorides_core.scope`).  Ported  | tests | 15 |
| `tests/test_search_telemetry.py` | BDD/ATDD suite for the `search_telemetry` module (spec/search_telemetry.md).  Ea | tests | 19 |
| `tests/test_security_remediation.py` | - | tests | 51 |
| `tests/test_socmint.py` | BDD tests for SOCMINT sources and SocialMediaInferer.  Covers: - S1: YouTube cha | tests | 72 |
| `tests/test_source_health_monitoring.py` | BDD tests for estorides_core.source_health_monitoring.  These tests implement th | tests | 52 |
| `tests/test_source_loader.py` | BDD / regression tests for SourceRegistry loading.  - SL1: a multi-document YAML | tests | 12 |
| `tests/test_sqlite_store.py` | BDD tests for the shared SQLite store base (spec/sqlite_store.md).  - SS1: schem | tests | 14 |
| `tests/test_structured_extraction.py` | BDD tests for structured human-selector extraction + pivot leaf surfacing.  Port | tests | 8 |
| `tests/test_supply_chain.py` | ATDD + BDD tests for estorides_core.supply_chain.  Implements the Given-When-The | tests | 17 |
| `tests/test_system_app_sources.py` | BDD tests for estorides_core.system_app_sources.  Kali OSINT CLI tools as first- | tests | 42 |
| `tests/test_target_management.py` | - | tests | 86 |
| `tests/test_target_scoring.py` | ATDD + BDD tests for estorides_core.target_scoring.  Implements the Given-When-T | tests | 18 |
| `tests/test_tech_fingerprint.py` | ATDD + BDD tests for estorides_core.tech_fingerprint.  Implements the Given-When | tests | 16 |
| `tests/test_tool_install.py` | Tests for estorides_core.tool_install (lazyaddon-style tool installation).  Cove | tests | 18 |
| `tests/test_tool_runner.py` | ATDD + BDD tests for estorides_core.tool_runner.  Implements the Given-When-Then | tests | 29 |
| `tests/test_ui_professional.py` | BDD tests for the ui_professional module (spec/ui_professional.md).  Each scenar | tests | 39 |
| `tests/test_ui_visibility.py` | Regression tests for the `hidden` attribute contract and output escaping.  `esto | tests | 9 |
| `tests/test_vuln_correlation.py` | ATDD + BDD tests for estorides_core.vuln_correlation.  Implements the Given-When | tests | 17 |
| `tests/test_web_helpers.py` | BDD tests for the web-layer decorators/helpers extracted from `create_app`.  - W | tests | 13 |
| `tools/split_sources.py` | Split legacy grouped source files into one addon per file.  Reads every multi-do | misc | 1 |
| `web.py` | Deprecated entry point. Use:  - `python3 estorides_cli.py serve` for the dev ser | root | 0 |
| `wsgi.py` | estorides.wsgi ==============  WSGI entry point for production deployments.  Run | root | 0 |
