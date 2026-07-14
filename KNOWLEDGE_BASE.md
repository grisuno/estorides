# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM, Ruby, Swift, Kotlin, Scala, Lua, Elixir.
> No LLMs. No tokens. Pure static analysis. See more [here](https://github.com/grisuno/ReadMenator)

**Total Files Parsed:** 91 | **Total Symbols Extracted:** 1701 | **Total Imports:** 700
 | **Resolved Imports:** 196


## Table of Contents

1. [Statistics Dashboard](#statistics-dashboard)
2. [Architectural Layers](#architectural-layers)
3. [God Nodes](#god-nodes)
4. [Community Analysis](#community-analysis)
5. [Surprising Connections](#surprising-connections)
6. [Suggested Questions](#suggested-questions)
7. [Structural Knowledge Map](#structural-knowledge-map)
8. [Architecture Reference](#architecture-reference)
    - [JS (2 files)](#js-2-files)
    - [PY (87 files)](#py-87-files)
    - [SH (2 files)](#sh-2-files)

---

## Statistics Dashboard

| Metric | Value |
|--------|-------|
| Total Files | 91 |
| Total Symbols | 1701 |
| Total Imports | 700 |
| Call Edges | 9869 |
| Inheritance Edges | 34 |
| Languages | 3 |
| Avg Symbols/File | 18.7 |
| Avg Imports/File | 7.7 |
| Resolved Imports | 196 |

### Top Files by Import Count (Fan-Out)

| File | Imports | Symbols | Language |
|------|---------|---------|----------|
| `estorides_web.py` | 40 | 65 | py |
| `test_security_remediation.py` | 32 | 46 | py |
| `orchestrator.py` | 29 | 12 | py |
| `estorides_cli.py` | 27 | 18 | py |
| `_test_hardening.py` | 21 | 13 | py |
| `async_client.py` | 17 | 20 | py |
| `feeds.py` | 16 | 16 | py |
| `ontology.py` | 16 | 25 | py |
| `intel_resolver.py` | 14 | 26 | py |
| `discoverer.py` | 13 | 21 | py |

---

## Architectural Layers

Auto-detected from path patterns, naming conventions, and imported frameworks.

| Layer | Files |
|-------|-------|
| utility | 45 |
| testing | 35 |
| infrastructure | 4 |
| presentation | 3 |
| business_logic | 2 |
| data_access | 2 |

### testing

- `_multi_test.sh` (sh, 0 symbols)
- `_test_entity_resolution.py` (py, 12 symbols)
- `_test_fusion.py` (py, 10 symbols)
- `_test_hardening.py` (py, 13 symbols)
- `_test_passive.py` (py, 2 symbols)
- `_test_people.py` (py, 5 symbols)
- `_test_proxy.py` (py, 4 symbols)
- `_test_scope.py` (py, 2 symbols)
- `conftest.py` (py, 0 symbols)
- `test_change_detection_properties.py` (py, 8 symbols)
- `test_csp_safe_styles_properties.py` (py, 3 symbols)
- `test_hypothesis_engine_properties.py` (py, 9 symbols)
- `test_recon_fusion_properties.py` (py, 17 symbols)
- `test_reliability_scoring_properties.py` (py, 12 symbols)
- `test_search_telemetry_properties.py` (py, 6 symbols)
- *... and 20 more*

### utility

- `_validate.py` (py, 1 symbols)
- `app.py` (py, 0 symbols)
- `estorides_cli.py` (py, 18 symbols)
- `__init__.py` (py, 0 symbols)
- `cases.py` (py, 21 symbols)
- `change_detection.py` (py, 21 symbols)
- `feeds.py` (py, 16 symbols)
- `fusion_analytics.py` (py, 14 symbols)
- `graph_kuzu.py` (py, 11 symbols)
- `hypothesis_engine.py` (py, 23 symbols)
- `intel_resolver.py` (py, 26 symbols)
- `job_registry.py` (py, 10 symbols)
- `knowledge_graph.py` (py, 17 symbols)
- `mitre_attack.py` (py, 4 symbols)
- `ontology.py` (py, 25 symbols)
- *... and 30 more*

### infrastructure

- `async_client.py` (py, 20 symbols)
- `audit.py` (py, 11 symbols)
- `config.py` (py, 24 symbols)
- `discoverer.py` (py, 21 symbols)

### presentation

- `entity_extraction.py` (py, 19 symbols)
- `web_security.py` (py, 23 symbols)
- `estorides_web.py` (py, 65 symbols)

### business_logic

- `entity_resolution.py` (py, 35 symbols)
- `entity_store.py` (py, 9 symbols)

### data_access

- `fusion_store.py` (py, 22 symbols)
- `transforms.py` (py, 17 symbols)

---

## God Nodes

Most architecturally central files ranked by combined import/export degree and symbol richness.

| File | Score | Connections |
|------|-------|-------------|
| `config.py` | 60.4 | |
| `estorides_web.py` | 52.5 | |
| `orchestrator.py` | 43.2 | |
| `estorides_cli.py` | 25.8 | |
| `entity_extraction.py` | 23.9 | |
| `entity_resolution.py` | 21.5 | |
| `fusion_store.py` | 20.2 | |
| `discoverer.py` | 20.1 | |
| `knowledge_graph.py` | 19.7 | |
| `reliability_scoring.py` | 17.4 | |

---

## Community Analysis

Files grouped by import-based community detection. Cohesion measures how tightly connected each community is internally.

### estorides_core (Cohesion: 0.91)

**54 files** in this community:

- `_test_entity_resolution.py` (py, 12 symbols)
- `_test_fusion.py` (py, 10 symbols)
- `_test_hardening.py` (py, 13 symbols)
- `_test_passive.py` (py, 2 symbols)
- `_test_people.py` (py, 5 symbols)
- `_test_proxy.py` (py, 4 symbols)
- `app.py` (py, 0 symbols)
- `estorides_cli.py` (py, 18 symbols)
- `__init__.py` (py, 0 symbols)
- `async_client.py` (py, 20 symbols)
- `audit.py` (py, 11 symbols)
- `cases.py` (py, 21 symbols)
- `config.py` (py, 24 symbols)
- `discoverer.py` (py, 21 symbols)
- `entity_extraction.py` (py, 19 symbols)
- `entity_resolution.py` (py, 35 symbols)
- `entity_store.py` (py, 9 symbols)
- `feeds.py` (py, 16 symbols)
- `fusion_analytics.py` (py, 14 symbols)
- `fusion_store.py` (py, 22 symbols)
- ... and 34 more files

### root (Cohesion: 0.50)

**2 files** in this community:

- `_test_scope.py` (py, 2 symbols)
- `scope.py` (py, 39 symbols)

### estorides_core (Cohesion: 0.83)

**9 files** in this community:

- `change_detection.py` (py, 21 symbols)
- `hypothesis_engine.py` (py, 23 symbols)
- `reliability_scoring.py` (py, 14 symbols)
- `test_change_detection_properties.py` (py, 8 symbols)
- `test_hypothesis_engine_properties.py` (py, 9 symbols)
- `test_reliability_scoring_properties.py` (py, 12 symbols)
- `test_change_detection.py` (py, 43 symbols)
- `test_hypothesis_engine.py` (py, 35 symbols)
- `test_reliability_scoring.py` (py, 64 symbols)

### estorides_core (Cohesion: 0.50)

**2 files** in this community:

- `pagination.py` (py, 7 symbols)
- `test_pagination.py` (py, 38 symbols)

### tests (Cohesion: 0.38)

**4 files** in this community:

- `recon_fusion.py` (py, 21 symbols)
- `test_recon_fusion_properties.py` (py, 17 symbols)
- `test_recon_fusion.py` (py, 33 symbols)
- `test_ui_professional.py` (py, 39 symbols)

### estorides_core (Cohesion: 1.00)

**3 files** in this community:

- `source_health_monitoring.py` (py, 16 symbols)
- `test_source_health_monitoring_properties.py` (py, 7 symbols)
- `test_source_health_monitoring.py` (py, 52 symbols)

### estorides_core (Cohesion: 0.67)

**3 files** in this community:

- `target_management.py` (py, 18 symbols)
- `test_target_management_properties.py` (py, 10 symbols)
- `test_target_management.py` (py, 86 symbols)

### tests (Cohesion: 0.57)

**5 files** in this community:

- `web_security.py` (py, 23 symbols)
- `test_csp_safe_styles_properties.py` (py, 3 symbols)
- `test_auth_gate.py` (py, 10 symbols)
- `test_csp_safe_styles.py` (py, 11 symbols)
- `test_security_remediation.py` (py, 46 symbols)

### estorides_llm (Cohesion: 0.67)

**3 files** in this community:

- `__init__.py` (py, 0 symbols)
- `intelligence_prompts.py` (py, 1 symbols)
- `manager.py` (py, 17 symbols)

---

## Surprising Connections

Files in different communities connected through 3+ indirect hops.

- `_test_hardening.py` <-> `test_change_detection_properties.py` (6 hops, across 3 communities)
- `_test_hardening.py` <-> `test_hypothesis_engine_properties.py` (6 hops, across 3 communities)
- `_test_scope.py` <-> `test_change_detection_properties.py` (6 hops, across 3 communities)
- `_test_scope.py` <-> `test_hypothesis_engine_properties.py` (6 hops, across 3 communities)
- `_test_scope.py` <-> `test_target_management_properties.py` (6 hops, across 3 communities)

---

## Suggested Questions

Auto-generated exploration prompts based on graph structure:

- What does config.py depend on, and what depends on it? (29 connections)
- What does estorides_web.py depend on, and what depends on it? (23 connections)
- What does orchestrator.py depend on, and what depends on it? (21 connections)
- How are the 54 files in 'estorides_core' related to each other?
- Why are _test_hardening.py and test_change_detection_properties.py connected through 6 hops across 3 communities?

---

## Structural Knowledge Map

> **Note:** The visual graph below has been intelligently pruned to the top 300 most relevant nodes to prevent rendering crashes. Full details of all files are documented in the Architecture Reference.

```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray:5 5,color:#aaa;
    subgraph community_0 ["estorides_core"]
    static_js_estorides_js["estorides.js (js)"]
    class static_js_estorides_js mod;
    static_js_estorides_js_detectQueryTypeLocal["detectQueryTypeLocal"]
    class static_js_estorides_js_detectQueryTypeLocal fn;
    static_js_estorides_js --> static_js_estorides_js_detectQueryTypeLocal
    static_js_estorides_js_showToast["showToast"]
    class static_js_estorides_js_showToast fn;
    static_js_estorides_js --> static_js_estorides_js_showToast
    static_js_estorides_js_updateQueryChip["updateQueryChip"]
    class static_js_estorides_js_updateQueryChip fn;
    static_js_estorides_js --> static_js_estorides_js_updateQueryChip
    static_js_estorides_js_setRunProgress["setRunProgress"]
    class static_js_estorides_js_setRunProgress fn;
    static_js_estorides_js --> static_js_estorides_js_setRunProgress
    static_js_estorides_js_showEmptyState["showEmptyState"]
    class static_js_estorides_js_showEmptyState fn;
    static_js_estorides_js --> static_js_estorides_js_showEmptyState
    static_js_source_manager_js["source_manager.js (js)"]
    class static_js_source_manager_js mod;
    static_js_source_manager_js_authHeaders["authHeaders"]
    class static_js_source_manager_js_authHeaders fn;
    static_js_source_manager_js --> static_js_source_manager_js_authHeaders
    static_js_source_manager_js_apiFetch["apiFetch"]
    class static_js_source_manager_js_apiFetch fn;
    static_js_source_manager_js --> static_js_source_manager_js_apiFetch
    static_js_source_manager_js_getCheckedTags["getCheckedTags"]
    class static_js_source_manager_js_getCheckedTags fn;
    static_js_source_manager_js --> static_js_source_manager_js_getCheckedTags
    static_js_source_manager_js_setCheckedTags["setCheckedTags"]
    class static_js_source_manager_js_setCheckedTags fn;
    static_js_source_manager_js --> static_js_source_manager_js_setCheckedTags
    static_js_source_manager_js_readForm["readForm"]
    class static_js_source_manager_js_readForm fn;
    static_js_source_manager_js --> static_js_source_manager_js_readForm
    estorides_web_py["estorides_web.py (py)"]
    class estorides_web_py mod;
    estorides_web_py__client_ip["_client_ip"]
    class estorides_web_py__client_ip fn;
    estorides_web_py --> estorides_web_py__client_ip
    estorides_web_py__arg_int["_arg_int"]
    class estorides_web_py__arg_int fn;
    estorides_web_py --> estorides_web_py__arg_int
    estorides_web_py__send_and_cleanup["_send_and_cleanup"]
    class estorides_web_py__send_and_cleanup fn;
    estorides_web_py --> estorides_web_py__send_and_cleanup
    estorides_web_py__RunStreamJob["_RunStreamJob"]
    class estorides_web_py__RunStreamJob cls;
    estorides_web_py --> estorides_web_py__RunStreamJob
    estorides_web_py__new_stream_job_id["_new_stream_job_id"]
    class estorides_web_py__new_stream_job_id fn;
    estorides_web_py --> estorides_web_py__new_stream_job_id
    estorides_core_orchestrator_py["orchestrator.py (py)"]
    class estorides_core_orchestrator_py mod;
    estorides_core_orchestrator_py__safe_format["_safe_format"]
    class estorides_core_orchestrator_py__safe_format fn;
    estorides_core_orchestrator_py --> estorides_core_orchestrator_py__safe_format
    estorides_core_orchestrator_py__resolve_auth["_resolve_auth"]
    class estorides_core_orchestrator_py__resolve_auth fn;
    estorides_core_orchestrator_py --> estorides_core_orchestrator_py__resolve_auth
    estorides_core_orchestrator_py__domain_from_query["_domain_from_query"]
    class estorides_core_orchestrator_py__domain_from_query fn;
    estorides_core_orchestrator_py --> estorides_core_orchestrator_py__domain_from_query
    estorides_core_orchestrator_py_Orchestrator["Orchestrator"]
    class estorides_core_orchestrator_py_Orchestrator cls;
    estorides_core_orchestrator_py --> estorides_core_orchestrator_py_Orchestrator
    estorides_core_orchestrator_py_repl["repl"]
    class estorides_core_orchestrator_py_repl fn;
    estorides_core_orchestrator_py --> estorides_core_orchestrator_py_repl
    estorides_cli_py["estorides_cli.py (py)"]
    class estorides_cli_py mod;
    estorides_cli_py__setup_logging["_setup_logging"]
    class estorides_cli_py__setup_logging fn;
    estorides_cli_py --> estorides_cli_py__setup_logging
    estorides_cli_py__collect_selectors["_collect_selectors"]
    class estorides_cli_py__collect_selectors fn;
    estorides_cli_py --> estorides_cli_py__collect_selectors
    estorides_cli_py__resolve_proxy["_resolve_proxy"]
    class estorides_cli_py__resolve_proxy fn;
    estorides_cli_py --> estorides_cli_py__resolve_proxy
    estorides_cli_py__add_opsec_flags["_add_opsec_flags"]
    class estorides_cli_py__add_opsec_flags fn;
    estorides_cli_py --> estorides_cli_py__add_opsec_flags
    estorides_cli_py_cmd_discover["cmd_discover"]
    class estorides_cli_py_cmd_discover fn;
    estorides_cli_py --> estorides_cli_py_cmd_discover
    end
    subgraph community_7 ["tests"]
    tests_test_security_remediation_py["test_security_remediation.py (py)"]
    class tests_test_security_remediation_py mod;
    tests_test_security_remediation_py_TestSsrfLogSanitisation["TestSsrfLogSanitisation"]
    class tests_test_security_remediation_py_TestSsrfLogSanitisation cls;
    tests_test_security_remediation_py --> tests_test_security_remediation_py_TestSsrfLogSanitisation
    tests_test_security_remediation_py_TestInfoExposureEncryption["TestInfoExposureEncryption"]
    class tests_test_security_remediation_py_TestInfoExposureEncryption cls;
    tests_test_security_remediation_py --> tests_test_security_remediation_py_TestInfoExposureEncryption
    tests_test_security_remediation_py_TestInfoExposureSourceOps["TestInfoExposureSourceOps"]
    class tests_test_security_remediation_py_TestInfoExposureSourceOps cls;
    tests_test_security_remediation_py --> tests_test_security_remediation_py_TestInfoExposureSourceOps
    tests_test_security_remediation_py_TestHttpsRedirectSafety["TestHttpsRedirectSafety"]
    class tests_test_security_remediation_py_TestHttpsRedirectSafety cls;
    tests_test_security_remediation_py --> tests_test_security_remediation_py_TestHttpsRedirectSafety
    tests_test_security_remediation_py_TestCiWorkflowPermissions["TestCiWorkflowPermissions"]
    class tests_test_security_remediation_py_TestCiWorkflowPermissions cls;
    tests_test_security_remediation_py --> tests_test_security_remediation_py_TestCiWorkflowPermissions
    _test_hardening_py["_test_hardening.py (py)"]
    class _test_hardening_py mod;
    _test_hardening_py__ok["_ok"]
    class _test_hardening_py__ok fn;
    _test_hardening_py --> _test_hardening_py__ok
    _test_hardening_py_test_security_headers["test_security_headers"]
    class _test_hardening_py_test_security_headers fn;
    _test_hardening_py --> _test_hardening_py_test_security_headers
    _test_hardening_py_test_cors_default_off["test_cors_default_off"]
    class _test_hardening_py_test_cors_default_off fn;
    _test_hardening_py --> _test_hardening_py_test_cors_default_off
    _test_hardening_py_test_cors_allowlist["test_cors_allowlist"]
    class _test_hardening_py_test_cors_allowlist fn;
    _test_hardening_py --> _test_hardening_py_test_cors_allowlist
    _test_hardening_py_test_debug_killswitch["test_debug_killswitch"]
    class _test_hardening_py_test_debug_killswitch fn;
    _test_hardening_py --> _test_hardening_py_test_debug_killswitch
    estorides_core_discoverer_py["discoverer.py (py)"]
    class estorides_core_discoverer_py mod;
    estorides_core_discoverer_py_DiscoverJob["DiscoverJob"]
    class estorides_core_discoverer_py_DiscoverJob cls;
    estorides_core_discoverer_py --> estorides_core_discoverer_py_DiscoverJob
    estorides_core_discoverer_py__DiscoverJobSink["_DiscoverJobSink"]
    class estorides_core_discoverer_py__DiscoverJobSink cls;
    estorides_core_discoverer_py --> estorides_core_discoverer_py__DiscoverJobSink
    estorides_core_discoverer_py__new_job_id["_new_job_id"]
    class estorides_core_discoverer_py__new_job_id fn;
    estorides_core_discoverer_py --> estorides_core_discoverer_py__new_job_id
    estorides_core_discoverer_py_create_discover_job["create_discover_job"]
    class estorides_core_discoverer_py_create_discover_job fn;
    estorides_core_discoverer_py --> estorides_core_discoverer_py_create_discover_job
    estorides_core_discoverer_py_start_discover["start_discover"]
    class estorides_core_discoverer_py_start_discover fn;
    estorides_core_discoverer_py --> estorides_core_discoverer_py_start_discover
    estorides_core_async_client_py["async_client.py (py)"]
    class estorides_core_async_client_py mod;
    estorides_core_async_client_py__is_socks["_is_socks"]
    class estorides_core_async_client_py__is_socks fn;
    estorides_core_async_client_py --> estorides_core_async_client_py__is_socks
    estorides_core_async_client_py__redact_proxy["_redact_proxy"]
    class estorides_core_async_client_py__redact_proxy fn;
    estorides_core_async_client_py --> estorides_core_async_client_py__redact_proxy
    estorides_core_async_client_py_CircuitBreaker["CircuitBreaker"]
    class estorides_core_async_client_py_CircuitBreaker cls;
    estorides_core_async_client_py --> estorides_core_async_client_py_CircuitBreaker
    estorides_core_async_client_py_ResponseCache["ResponseCache"]
    class estorides_core_async_client_py_ResponseCache cls;
    estorides_core_async_client_py --> estorides_core_async_client_py_ResponseCache
    estorides_core_async_client_py_AsyncClient["AsyncClient"]
    class estorides_core_async_client_py_AsyncClient cls;
    estorides_core_async_client_py --> estorides_core_async_client_py_AsyncClient
    estorides_core_ontology_py["ontology.py (py)"]
    class estorides_core_ontology_py mod;
    estorides_core_ontology_py_SanctionEntry["SanctionEntry"]
    class estorides_core_ontology_py_SanctionEntry cls;
    estorides_core_ontology_py --> estorides_core_ontology_py_SanctionEntry
    estorides_core_ontology_py__normalise_name["_normalise_name"]
    class estorides_core_ontology_py__normalise_name fn;
    estorides_core_ontology_py --> estorides_core_ontology_py__normalise_name
    estorides_core_ontology_py_SanctionsIndex["SanctionsIndex"]
    class estorides_core_ontology_py_SanctionsIndex cls;
    estorides_core_ontology_py --> estorides_core_ontology_py_SanctionsIndex
    estorides_core_ontology_py_WikidataCache["WikidataCache"]
    class estorides_core_ontology_py_WikidataCache cls;
    estorides_core_ontology_py --> estorides_core_ontology_py_WikidataCache
    estorides_core_ontology_py_OntologyEngine["OntologyEngine"]
    class estorides_core_ontology_py_OntologyEngine cls;
    estorides_core_ontology_py --> estorides_core_ontology_py_OntologyEngine
    estorides_core_feeds_py["feeds.py (py)"]
    class estorides_core_feeds_py mod;
    estorides_core_feeds_py_FeedPoint["FeedPoint"]
    class estorides_core_feeds_py_FeedPoint cls;
    estorides_core_feeds_py --> estorides_core_feeds_py_FeedPoint
    estorides_core_feeds_py_Feed["Feed"]
    class estorides_core_feeds_py_Feed cls;
    estorides_core_feeds_py --> estorides_core_feeds_py_Feed
    estorides_core_feeds_py_EarthquakesFeed["EarthquakesFeed"]
    class estorides_core_feeds_py_EarthquakesFeed cls;
    estorides_core_feeds_py --> estorides_core_feeds_py_EarthquakesFeed
    estorides_core_feeds_py_FiresFeed["FiresFeed"]
    class estorides_core_feeds_py_FiresFeed cls;
    estorides_core_feeds_py --> estorides_core_feeds_py_FiresFeed
    estorides_core_feeds_py_NewsFeed["NewsFeed"]
    class estorides_core_feeds_py_NewsFeed cls;
    estorides_core_feeds_py --> estorides_core_feeds_py_NewsFeed
    estorides_core_intel_resolver_py["intel_resolver.py (py)"]
    class estorides_core_intel_resolver_py mod;
    estorides_core_intel_resolver_py__run_sparql["_run_sparql"]
    class estorides_core_intel_resolver_py__run_sparql fn;
    estorides_core_intel_resolver_py --> estorides_core_intel_resolver_py__run_sparql
    estorides_core_intel_resolver_py__val["_val"]
    class estorides_core_intel_resolver_py__val fn;
    estorides_core_intel_resolver_py --> estorides_core_intel_resolver_py__val
    estorides_core_intel_resolver_py__TTLCache["_TTLCache"]
    class estorides_core_intel_resolver_py__TTLCache cls;
    estorides_core_intel_resolver_py --> estorides_core_intel_resolver_py__TTLCache
    estorides_core_intel_resolver_py_EntityResolver["EntityResolver"]
    class estorides_core_intel_resolver_py_EntityResolver cls;
    estorides_core_intel_resolver_py --> estorides_core_intel_resolver_py_EntityResolver
    estorides_core_intel_resolver_py__norm["_norm"]
    class estorides_core_intel_resolver_py__norm fn;
    estorides_core_intel_resolver_py --> estorides_core_intel_resolver_py__norm
    end
    subgraph community_4 ["tests"]
    estorides_core_recon_fusion_py["recon_fusion.py (py)"]
    class estorides_core_recon_fusion_py mod;
    estorides_core_recon_fusion_py_RelevanceTier["RelevanceTier"]
    class estorides_core_recon_fusion_py_RelevanceTier cls;
    estorides_core_recon_fusion_py --> estorides_core_recon_fusion_py_RelevanceTier
    estorides_core_recon_fusion_py_GroupedEntity["GroupedEntity"]
    class estorides_core_recon_fusion_py_GroupedEntity cls;
    estorides_core_recon_fusion_py --> estorides_core_recon_fusion_py_GroupedEntity
    estorides_core_recon_fusion_py_FusionResult["FusionResult"]
    class estorides_core_recon_fusion_py_FusionResult cls;
    estorides_core_recon_fusion_py --> estorides_core_recon_fusion_py_FusionResult
    estorides_core_recon_fusion_py__normalize_value["_normalize_value"]
    class estorides_core_recon_fusion_py__normalize_value fn;
    estorides_core_recon_fusion_py --> estorides_core_recon_fusion_py__normalize_value
    estorides_core_recon_fusion_py__canonical_id["_canonical_id"]
    class estorides_core_recon_fusion_py__canonical_id fn;
    estorides_core_recon_fusion_py --> estorides_core_recon_fusion_py__canonical_id
    end
    subgraph community_2 ["estorides_core"]
    tests_properties_test_reliability_scoring_properties_py["test_reliability_scoring_properties.py (py)"]
    class tests_properties_test_reliability_scoring_properties_py mod;
    tests_properties_test_reliability_scoring_properties_py_test_score_always_bounded["test_score_always_bounded"]
    class tests_properties_test_reliability_scoring_properties_py_test_score_always_bounded fn;
    tests_properties_test_reliability_scoring_properties_py --> tests_properties_test_reliability_scoring_properties_py_test_score_always_bounded
    tests_properties_test_reliability_scoring_properties_py_test_corroboration_weight_in_unit_interval["test_corroboration_weight_in_unit_interval"]
    class tests_properties_test_reliability_scoring_properties_py_test_corroboration_weight_in_unit_interval fn;
    tests_properties_test_reliability_scoring_properties_py --> tests_properties_test_reliability_scoring_properties_py_test_corroboration_weight_in_unit_interval
    tests_properties_test_reliability_scoring_properties_py_test_freshness_monotone_in_age["test_freshness_monotone_in_age"]
    class tests_properties_test_reliability_scoring_properties_py_test_freshness_monotone_in_age fn;
    tests_properties_test_reliability_scoring_properties_py --> tests_properties_test_reliability_scoring_properties_py_test_freshness_monotone_in_age
    tests_properties_test_reliability_scoring_properties_py_test_reliability_from_name_never_raises["test_reliability_from_name_never_raises"]
    class tests_properties_test_reliability_scoring_properties_py_test_reliability_from_name_never_raises fn;
    tests_properties_test_reliability_scoring_properties_py --> tests_properties_test_reliability_scoring_properties_py_test_reliability_from_name_never_raises
    tests_properties_test_reliability_scoring_properties_py_test_merge_confidence_bounded["test_merge_confidence_bounded"]
    class tests_properties_test_reliability_scoring_properties_py_test_merge_confidence_bounded fn;
    tests_properties_test_reliability_scoring_properties_py --> tests_properties_test_reliability_scoring_properties_py_test_merge_confidence_bounded
    estorides_core_fusion_store_py["fusion_store.py (py)"]
    class estorides_core_fusion_store_py mod;
    estorides_core_fusion_store_py_entity_id["entity_id"]
    class estorides_core_fusion_store_py_entity_id fn;
    estorides_core_fusion_store_py --> estorides_core_fusion_store_py_entity_id
    estorides_core_fusion_store_py_FusionStore["FusionStore"]
    class estorides_core_fusion_store_py_FusionStore cls;
    estorides_core_fusion_store_py --> estorides_core_fusion_store_py_FusionStore
    estorides_core_fusion_store_py_open_store["open_store"]
    class estorides_core_fusion_store_py_open_store fn;
    estorides_core_fusion_store_py --> estorides_core_fusion_store_py_open_store
    estorides_core_fusion_store_py___init__["__init__"]
    class estorides_core_fusion_store_py___init__ fn;
    estorides_core_fusion_store_py --> estorides_core_fusion_store_py___init__
    estorides_core_fusion_store_py__init_schema["_init_schema"]
    class estorides_core_fusion_store_py__init_schema fn;
    estorides_core_fusion_store_py --> estorides_core_fusion_store_py__init_schema
    tests_test_encrypted_export_py["test_encrypted_export.py (py)"]
    class tests_test_encrypted_export_py mod;
    tests_test_encrypted_export_py__FakeCompleted["_FakeCompleted"]
    class tests_test_encrypted_export_py__FakeCompleted cls;
    tests_test_encrypted_export_py --> tests_test_encrypted_export_py__FakeCompleted
    tests_test_encrypted_export_py__kg_with_one_node["_kg_with_one_node"]
    class tests_test_encrypted_export_py__kg_with_one_node fn;
    tests_test_encrypted_export_py --> tests_test_encrypted_export_py__kg_with_one_node
    tests_test_encrypted_export_py__patch_age_ok["_patch_age_ok"]
    class tests_test_encrypted_export_py__patch_age_ok fn;
    tests_test_encrypted_export_py --> tests_test_encrypted_export_py__patch_age_ok
    tests_test_encrypted_export_py_test_stix_encrypted_removes_plaintext["test_stix_encrypted_removes_plaintext"]
    class tests_test_encrypted_export_py_test_stix_encrypted_removes_plaintext fn;
    tests_test_encrypted_export_py --> tests_test_encrypted_export_py_test_stix_encrypted_removes_plaintext
    tests_test_encrypted_export_py_test_misp_encrypted_removes_plaintext["test_misp_encrypted_removes_plaintext"]
    class tests_test_encrypted_export_py_test_misp_encrypted_removes_plaintext fn;
    tests_test_encrypted_export_py --> tests_test_encrypted_export_py_test_misp_encrypted_removes_plaintext
    estorides_core_osiris_sources_py["osiris_sources.py (py)"]
    class estorides_core_osiris_sources_py mod;
    estorides_core_osiris_sources_py__cached_get["_cached_get"]
    class estorides_core_osiris_sources_py__cached_get fn;
    estorides_core_osiris_sources_py --> estorides_core_osiris_sources_py__cached_get
    estorides_core_osiris_sources_py_fetch_bgp["fetch_bgp"]
    class estorides_core_osiris_sources_py_fetch_bgp fn;
    estorides_core_osiris_sources_py --> estorides_core_osiris_sources_py_fetch_bgp
    estorides_core_osiris_sources_py_fetch_mac["fetch_mac"]
    class estorides_core_osiris_sources_py_fetch_mac fn;
    estorides_core_osiris_sources_py --> estorides_core_osiris_sources_py_fetch_mac
    estorides_core_osiris_sources_py_fetch_phone["fetch_phone"]
    class estorides_core_osiris_sources_py_fetch_phone fn;
    estorides_core_osiris_sources_py --> estorides_core_osiris_sources_py_fetch_phone
    estorides_core_osiris_sources_py_fetch_github_user["fetch_github_user"]
    class estorides_core_osiris_sources_py_fetch_github_user fn;
    estorides_core_osiris_sources_py --> estorides_core_osiris_sources_py_fetch_github_user
    estorides_core_knowledge_graph_py["knowledge_graph.py (py)"]
    class estorides_core_knowledge_graph_py mod;
    estorides_core_knowledge_graph_py__node_sources["_node_sources"]
    class estorides_core_knowledge_graph_py__node_sources fn;
    estorides_core_knowledge_graph_py --> estorides_core_knowledge_graph_py__node_sources
    estorides_core_knowledge_graph_py_KnowledgeGraph["KnowledgeGraph"]
    class estorides_core_knowledge_graph_py_KnowledgeGraph cls;
    estorides_core_knowledge_graph_py --> estorides_core_knowledge_graph_py_KnowledgeGraph
    estorides_core_knowledge_graph_py___init__["__init__"]
    class estorides_core_knowledge_graph_py___init__ fn;
    estorides_core_knowledge_graph_py --> estorides_core_knowledge_graph_py___init__
    estorides_core_knowledge_graph_py_add_entity["add_entity"]
    class estorides_core_knowledge_graph_py_add_entity fn;
    estorides_core_knowledge_graph_py --> estorides_core_knowledge_graph_py_add_entity
    estorides_core_knowledge_graph_py_add_observation["add_observation"]
    class estorides_core_knowledge_graph_py_add_observation fn;
    estorides_core_knowledge_graph_py --> estorides_core_knowledge_graph_py_add_observation
    estorides_core_audit_py["audit.py (py)"]
    class estorides_core_audit_py mod;
    estorides_core_audit_py_AuditEvent["AuditEvent"]
    class estorides_core_audit_py_AuditEvent cls;
    estorides_core_audit_py --> estorides_core_audit_py_AuditEvent
    estorides_core_audit_py_AuditLog["AuditLog"]
    class estorides_core_audit_py_AuditLog cls;
    estorides_core_audit_py --> estorides_core_audit_py_AuditLog
    estorides_core_audit_py_RateLimiter["RateLimiter"]
    class estorides_core_audit_py_RateLimiter cls;
    estorides_core_audit_py --> estorides_core_audit_py_RateLimiter
    estorides_core_audit_py_to_jsonl["to_jsonl"]
    class estorides_core_audit_py_to_jsonl fn;
    estorides_core_audit_py --> estorides_core_audit_py_to_jsonl
    estorides_core_audit_py___init__["__init__"]
    class estorides_core_audit_py___init__ fn;
    estorides_core_audit_py --> estorides_core_audit_py___init__
    estorides_core_entity_resolution_py["entity_resolution.py (py)"]
    class estorides_core_entity_resolution_py mod;
    estorides_core_entity_resolution_py_jaro["jaro"]
    class estorides_core_entity_resolution_py_jaro fn;
    estorides_core_entity_resolution_py --> estorides_core_entity_resolution_py_jaro
    estorides_core_entity_resolution_py_jaro_winkler["jaro_winkler"]
    class estorides_core_entity_resolution_py_jaro_winkler fn;
    estorides_core_entity_resolution_py --> estorides_core_entity_resolution_py_jaro_winkler
    estorides_core_entity_resolution_py__soundex["_soundex"]
    class estorides_core_entity_resolution_py__soundex fn;
    estorides_core_entity_resolution_py --> estorides_core_entity_resolution_py__soundex
    estorides_core_entity_resolution_py__normalize_domain["_normalize_domain"]
    class estorides_core_entity_resolution_py__normalize_domain fn;
    estorides_core_entity_resolution_py --> estorides_core_entity_resolution_py__normalize_domain
    estorides_core_entity_resolution_py__normalize_name["_normalize_name"]
    class estorides_core_entity_resolution_py__normalize_name fn;
    estorides_core_entity_resolution_py --> estorides_core_entity_resolution_py__normalize_name
    estorides_core_cases_py["cases.py (py)"]
    class estorides_core_cases_py mod;
    estorides_core_cases_py_CaseStore["CaseStore"]
    class estorides_core_cases_py_CaseStore cls;
    estorides_core_cases_py --> estorides_core_cases_py_CaseStore
    estorides_core_cases_py___init__["__init__"]
    class estorides_core_cases_py___init__ fn;
    estorides_core_cases_py --> estorides_core_cases_py___init__
    estorides_core_cases_py__init_schema["_init_schema"]
    class estorides_core_cases_py__init_schema fn;
    estorides_core_cases_py --> estorides_core_cases_py__init_schema
    estorides_core_cases_py__tx["_tx"]
    class estorides_core_cases_py__tx fn;
    estorides_core_cases_py --> estorides_core_cases_py__tx
    estorides_core_cases_py_create_case["create_case"]
    class estorides_core_cases_py_create_case fn;
    estorides_core_cases_py --> estorides_core_cases_py_create_case
    _test_entity_resolution_py["_test_entity_resolution.py (py)"]
    class _test_entity_resolution_py mod;
    _test_entity_resolution_py_check["check"]
    class _test_entity_resolution_py_check fn;
    _test_entity_resolution_py --> _test_entity_resolution_py_check
    _test_entity_resolution_py__ent["_ent"]
    class _test_entity_resolution_py__ent fn;
    _test_entity_resolution_py --> _test_entity_resolution_py__ent
    _test_entity_resolution_py__by_value["_by_value"]
    class _test_entity_resolution_py__by_value fn;
    _test_entity_resolution_py --> _test_entity_resolution_py__by_value
    _test_entity_resolution_py_test_transliteration["test_transliteration"]
    class _test_entity_resolution_py_test_transliteration fn;
    _test_entity_resolution_py --> _test_entity_resolution_py_test_transliteration
    _test_entity_resolution_py_test_jaro_winkler["test_jaro_winkler"]
    class _test_entity_resolution_py_test_jaro_winkler fn;
    _test_entity_resolution_py --> _test_entity_resolution_py_test_jaro_winkler
    tests_test_csp_safe_styles_py["test_csp_safe_styles.py (py)"]
    class tests_test_csp_safe_styles_py mod;
    tests_test_csp_safe_styles_py__strip_template_jinja["_strip_template_jinja"]
    class tests_test_csp_safe_styles_py__strip_template_jinja fn;
    tests_test_csp_safe_styles_py --> tests_test_csp_safe_styles_py__strip_template_jinja
    tests_test_csp_safe_styles_py__strip_js_comments_and_strings_outside_templates["_strip_js_comments_and_strings_outside_templates"]
    class tests_test_csp_safe_styles_py__strip_js_comments_and_strings_outside_templates fn;
    tests_test_csp_safe_styles_py --> tests_test_csp_safe_styles_py__strip_js_comments_and_strings_outside_templates
    tests_test_csp_safe_styles_py_test_index_html_has_no_style_attribute["test_index_html_has_no_style_attribute"]
    class tests_test_csp_safe_styles_py_test_index_html_has_no_style_attribute fn;
    tests_test_csp_safe_styles_py --> tests_test_csp_safe_styles_py_test_index_html_has_no_style_attribute
    tests_test_csp_safe_styles_py_test_estorides_js_has_no_style_in_template_literals["test_estorides_js_has_no_style_in_template_literals"]
    class tests_test_csp_safe_styles_py_test_estorides_js_has_no_style_in_template_literals fn;
    tests_test_csp_safe_styles_py --> tests_test_csp_safe_styles_py_test_estorides_js_has_no_style_in_template_literals
    tests_test_csp_safe_styles_py_test_offscreen_element_uses_hidden_attribute["test_offscreen_element_uses_hidden_attribute"]
    class tests_test_csp_safe_styles_py_test_offscreen_element_uses_hidden_attribute fn;
    tests_test_csp_safe_styles_py --> tests_test_csp_safe_styles_py_test_offscreen_element_uses_hidden_attribute
    tests_test_entity_resolution_py["test_entity_resolution.py (py)"]
    class tests_test_entity_resolution_py mod;
    tests_test_entity_resolution_py__ent["_ent"]
    class tests_test_entity_resolution_py__ent fn;
    tests_test_entity_resolution_py --> tests_test_entity_resolution_py__ent
    tests_test_entity_resolution_py__by_value["_by_value"]
    class tests_test_entity_resolution_py__by_value fn;
    tests_test_entity_resolution_py --> tests_test_entity_resolution_py__by_value
    tests_test_entity_resolution_py_TestTransliteration["TestTransliteration"]
    class tests_test_entity_resolution_py_TestTransliteration cls;
    tests_test_entity_resolution_py --> tests_test_entity_resolution_py_TestTransliteration
    tests_test_entity_resolution_py_TestJaroWinkler["TestJaroWinkler"]
    class tests_test_entity_resolution_py_TestJaroWinkler cls;
    tests_test_entity_resolution_py --> tests_test_entity_resolution_py_TestJaroWinkler
    tests_test_entity_resolution_py_TestNormalization["TestNormalization"]
    class tests_test_entity_resolution_py_TestNormalization cls;
    tests_test_entity_resolution_py --> tests_test_entity_resolution_py_TestNormalization
    estorides_core_web_security_py["web_security.py (py)"]
    class estorides_core_web_security_py mod;
    estorides_core_web_security_py_WebSecurityConfig["WebSecurityConfig"]
    class estorides_core_web_security_py_WebSecurityConfig cls;
    estorides_core_web_security_py --> estorides_core_web_security_py_WebSecurityConfig
    estorides_core_web_security_py__env_str["_env_str"]
    class estorides_core_web_security_py__env_str fn;
    estorides_core_web_security_py --> estorides_core_web_security_py__env_str
    estorides_core_web_security_py__env_int["_env_int"]
    class estorides_core_web_security_py__env_int fn;
    estorides_core_web_security_py --> estorides_core_web_security_py__env_int
    estorides_core_web_security_py__env_bool["_env_bool"]
    class estorides_core_web_security_py__env_bool fn;
    estorides_core_web_security_py --> estorides_core_web_security_py__env_bool
    estorides_core_web_security_py_load_security_config["load_security_config"]
    class estorides_core_web_security_py_load_security_config fn;
    estorides_core_web_security_py --> estorides_core_web_security_py_load_security_config
    estorides_core_graph_kuzu_py["graph_kuzu.py (py)"]
    class estorides_core_graph_kuzu_py mod;
    estorides_core_graph_kuzu_py__label_for["_label_for"]
    class estorides_core_graph_kuzu_py__label_for fn;
    estorides_core_graph_kuzu_py --> estorides_core_graph_kuzu_py__label_for
    estorides_core_graph_kuzu_py__node_id["_node_id"]
    class estorides_core_graph_kuzu_py__node_id fn;
    estorides_core_graph_kuzu_py --> estorides_core_graph_kuzu_py__node_id
    estorides_core_graph_kuzu_py_KuzuGraphBackend["KuzuGraphBackend"]
    class estorides_core_graph_kuzu_py_KuzuGraphBackend cls;
    estorides_core_graph_kuzu_py --> estorides_core_graph_kuzu_py_KuzuGraphBackend
    estorides_core_graph_kuzu_py___init__["__init__"]
    class estorides_core_graph_kuzu_py___init__ fn;
    estorides_core_graph_kuzu_py --> estorides_core_graph_kuzu_py___init__
    estorides_core_graph_kuzu_py__init_schema["_init_schema"]
    class estorides_core_graph_kuzu_py__init_schema fn;
    estorides_core_graph_kuzu_py --> estorides_core_graph_kuzu_py__init_schema
    estorides_core_entity_store_py["entity_store.py (py)"]
    class estorides_core_entity_store_py mod;
    estorides_core_entity_store_py_EntityStore["EntityStore"]
    class estorides_core_entity_store_py_EntityStore cls;
    estorides_core_entity_store_py --> estorides_core_entity_store_py_EntityStore
    estorides_core_entity_store_py_open_store["open_store"]
    class estorides_core_entity_store_py_open_store fn;
    estorides_core_entity_store_py --> estorides_core_entity_store_py_open_store
    estorides_core_entity_store_py___init__["__init__"]
    class estorides_core_entity_store_py___init__ fn;
    estorides_core_entity_store_py --> estorides_core_entity_store_py___init__
    estorides_core_entity_store_py__init_schema["_init_schema"]
    class estorides_core_entity_store_py__init_schema fn;
    estorides_core_entity_store_py --> estorides_core_entity_store_py__init_schema
    estorides_core_entity_store_py__tx["_tx"]
    class estorides_core_entity_store_py__tx fn;
    estorides_core_entity_store_py --> estorides_core_entity_store_py__tx
    estorides_export_stix_py["stix.py (py)"]
    class estorides_export_stix_py mod;
    estorides_export_stix_py__id["_id"]
    class estorides_export_stix_py__id fn;
    estorides_export_stix_py --> estorides_export_stix_py__id
    estorides_export_stix_py__now["_now"]
    class estorides_export_stix_py__now fn;
    estorides_export_stix_py --> estorides_export_stix_py__now
    estorides_export_stix_py_bundle_from_graph["bundle_from_graph"]
    class estorides_export_stix_py_bundle_from_graph fn;
    estorides_export_stix_py --> estorides_export_stix_py_bundle_from_graph
    estorides_export_stix_py_export["export"]
    class estorides_export_stix_py_export fn;
    estorides_export_stix_py --> estorides_export_stix_py_export
    estorides_export_misp_py["misp.py (py)"]
    class estorides_export_misp_py mod;
    estorides_export_misp_py_event_from_graph["event_from_graph"]
    class estorides_export_misp_py_event_from_graph fn;
    estorides_export_misp_py --> estorides_export_misp_py_event_from_graph
    estorides_export_misp_py__category["_category"]
    class estorides_export_misp_py__category fn;
    estorides_export_misp_py --> estorides_export_misp_py__category
    estorides_export_misp_py_export["export"]
    class estorides_export_misp_py_export fn;
    estorides_export_misp_py --> estorides_export_misp_py_export
    tests_test_ui_professional_py["test_ui_professional.py (py)"]
    class tests_test_ui_professional_py mod;
    tests_test_ui_professional_py__render_index["_render_index"]
    class tests_test_ui_professional_py__render_index fn;
    tests_test_ui_professional_py --> tests_test_ui_professional_py__render_index
    tests_test_ui_professional_py__simulate_tiered_data["_simulate_tiered_data"]
    class tests_test_ui_professional_py__simulate_tiered_data fn;
    tests_test_ui_professional_py --> tests_test_ui_professional_py__simulate_tiered_data
    tests_test_ui_professional_py_TestS1LoadingAnimation["TestS1LoadingAnimation"]
    class tests_test_ui_professional_py_TestS1LoadingAnimation cls;
    tests_test_ui_professional_py --> tests_test_ui_professional_py_TestS1LoadingAnimation
    tests_test_ui_professional_py_TestS2CriticalExpanded["TestS2CriticalExpanded"]
    class tests_test_ui_professional_py_TestS2CriticalExpanded cls;
    tests_test_ui_professional_py --> tests_test_ui_professional_py_TestS2CriticalExpanded
    tests_test_ui_professional_py_TestS3NoiseCollapsed["TestS3NoiseCollapsed"]
    class tests_test_ui_professional_py_TestS3NoiseCollapsed cls;
    tests_test_ui_professional_py --> tests_test_ui_professional_py_TestS3NoiseCollapsed
    tests_test_fusion_analytics_py["test_fusion_analytics.py (py)"]
    class tests_test_fusion_analytics_py mod;
    tests_test_fusion_analytics_py_store_and_analytics["store_and_analytics"]
    class tests_test_fusion_analytics_py_store_and_analytics fn;
    tests_test_fusion_analytics_py --> tests_test_fusion_analytics_py_store_and_analytics
    tests_test_fusion_analytics_py__populate_evilcorp["_populate_evilcorp"]
    class tests_test_fusion_analytics_py__populate_evilcorp fn;
    tests_test_fusion_analytics_py --> tests_test_fusion_analytics_py__populate_evilcorp
    tests_test_fusion_analytics_py__register_source["_register_source"]
    class tests_test_fusion_analytics_py__register_source fn;
    tests_test_fusion_analytics_py --> tests_test_fusion_analytics_py__register_source
    tests_test_fusion_analytics_py_TestEntityTimeline["TestEntityTimeline"]
    class tests_test_fusion_analytics_py_TestEntityTimeline cls;
    tests_test_fusion_analytics_py --> tests_test_fusion_analytics_py_TestEntityTimeline
    tests_test_fusion_analytics_py_TestEntitySummary["TestEntitySummary"]
    class tests_test_fusion_analytics_py_TestEntitySummary cls;
    tests_test_fusion_analytics_py --> tests_test_fusion_analytics_py_TestEntitySummary
    _test_people_py["_test_people.py (py)"]
    class _test_people_py mod;
    _test_people_py_check["check"]
    class _test_people_py_check fn;
    _test_people_py --> _test_people_py_check
    _test_people_py__types["_types"]
    class _test_people_py__types fn;
    _test_people_py --> _test_people_py__types
    _test_people_py_main["main"]
    class _test_people_py_main fn;
    _test_people_py --> _test_people_py_main
    _test_people_py__StubRunner["_StubRunner"]
    class _test_people_py__StubRunner cls;
    _test_people_py --> _test_people_py__StubRunner
    _test_people_py_run["run"]
    class _test_people_py_run fn;
    _test_people_py --> _test_people_py_run
    _test_proxy_py["_test_proxy.py (py)"]
    class _test_proxy_py mod;
    _test_proxy_py_check["check"]
    class _test_proxy_py_check fn;
    _test_proxy_py --> _test_proxy_py_check
    _test_proxy_py_main["main"]
    class _test_proxy_py_main fn;
    _test_proxy_py --> _test_proxy_py_main
    _test_proxy_py__enter_and_rotate["_enter_and_rotate"]
    class _test_proxy_py__enter_and_rotate fn;
    _test_proxy_py --> _test_proxy_py__enter_and_rotate
    _test_proxy_py__enter_socks["_enter_socks"]
    class _test_proxy_py__enter_socks fn;
    _test_proxy_py --> _test_proxy_py__enter_socks
    estorides_export_encryption_py["encryption.py (py)"]
    class estorides_export_encryption_py mod;
    estorides_export_encryption_py__have_age["_have_age"]
    class estorides_export_encryption_py__have_age fn;
    estorides_export_encryption_py --> estorides_export_encryption_py__have_age
    estorides_export_encryption_py_encrypt_file["encrypt_file"]
    class estorides_export_encryption_py_encrypt_file fn;
    estorides_export_encryption_py --> estorides_export_encryption_py_encrypt_file
    estorides_export_encryption_py_export_stix_encrypted["export_stix_encrypted"]
    class estorides_export_encryption_py_export_stix_encrypted fn;
    estorides_export_encryption_py --> estorides_export_encryption_py_export_stix_encrypted
    estorides_export_encryption_py_export_misp_encrypted["export_misp_encrypted"]
    class estorides_export_encryption_py_export_misp_encrypted fn;
    estorides_export_encryption_py --> estorides_export_encryption_py_export_misp_encrypted
    end
    subgraph community_1 ["root"]
    estorides_core_scope_py["scope.py (py)"]
    class estorides_core_scope_py mod;
    estorides_core_scope_py_normalise_asset["normalise_asset"]
    class estorides_core_scope_py_normalise_asset fn;
    estorides_core_scope_py --> estorides_core_scope_py_normalise_asset
    estorides_core_scope_py_is_ip["is_ip"]
    class estorides_core_scope_py_is_ip fn;
    estorides_core_scope_py --> estorides_core_scope_py_is_ip
    estorides_core_scope_py_ScopeRule["ScopeRule"]
    class estorides_core_scope_py_ScopeRule cls;
    estorides_core_scope_py --> estorides_core_scope_py_ScopeRule
    estorides_core_scope_py_WildcardRule["WildcardRule"]
    class estorides_core_scope_py_WildcardRule cls;
    estorides_core_scope_py --> estorides_core_scope_py_WildcardRule
    estorides_core_scope_py_ExactHostRule["ExactHostRule"]
    class estorides_core_scope_py_ExactHostRule cls;
    estorides_core_scope_py --> estorides_core_scope_py_ExactHostRule
    estorides_core_pivot_engine_py["pivot_engine.py (py)"]
    class estorides_core_pivot_engine_py mod;
    estorides_core_pivot_engine_py_PivotEvent["PivotEvent"]
    class estorides_core_pivot_engine_py_PivotEvent cls;
    estorides_core_pivot_engine_py --> estorides_core_pivot_engine_py_PivotEvent
    estorides_core_pivot_engine_py_EventSink["EventSink"]
    class estorides_core_pivot_engine_py_EventSink cls;
    estorides_core_pivot_engine_py --> estorides_core_pivot_engine_py_EventSink
    estorides_core_pivot_engine_py_ListEventSink["ListEventSink"]
    class estorides_core_pivot_engine_py_ListEventSink cls;
    estorides_core_pivot_engine_py --> estorides_core_pivot_engine_py_ListEventSink
    estorides_core_pivot_engine_py_BufferedEventSink["BufferedEventSink"]
    class estorides_core_pivot_engine_py_BufferedEventSink cls;
    estorides_core_pivot_engine_py --> estorides_core_pivot_engine_py_BufferedEventSink
    estorides_core_pivot_engine_py_EntityRunner["EntityRunner"]
    class estorides_core_pivot_engine_py_EntityRunner cls;
    estorides_core_pivot_engine_py --> estorides_core_pivot_engine_py_EntityRunner
    estorides_core_hypothesis_engine_py["hypothesis_engine.py (py)"]
    class estorides_core_hypothesis_engine_py mod;
    estorides_core_hypothesis_engine_py_EntityRef["EntityRef"]
    class estorides_core_hypothesis_engine_py_EntityRef cls;
    estorides_core_hypothesis_engine_py --> estorides_core_hypothesis_engine_py_EntityRef
    estorides_core_hypothesis_engine_py_Evidence["Evidence"]
    class estorides_core_hypothesis_engine_py_Evidence cls;
    estorides_core_hypothesis_engine_py --> estorides_core_hypothesis_engine_py_Evidence
    estorides_core_hypothesis_engine_py_Hypothesis["Hypothesis"]
    class estorides_core_hypothesis_engine_py_Hypothesis cls;
    estorides_core_hypothesis_engine_py --> estorides_core_hypothesis_engine_py_Hypothesis
    estorides_core_hypothesis_engine_py__truncate["_truncate"]
    class estorides_core_hypothesis_engine_py__truncate fn;
    estorides_core_hypothesis_engine_py --> estorides_core_hypothesis_engine_py__truncate
    estorides_core_hypothesis_engine_py__is_mapping["_is_mapping"]
    class estorides_core_hypothesis_engine_py__is_mapping fn;
    estorides_core_hypothesis_engine_py --> estorides_core_hypothesis_engine_py__is_mapping
    estorides_core_source_loader_py["source_loader.py (py)"]
    class estorides_core_source_loader_py mod;
    estorides_core_source_loader_py_Source["Source"]
    class estorides_core_source_loader_py_Source cls;
    estorides_core_source_loader_py --> estorides_core_source_loader_py_Source
    estorides_core_source_loader_py_SourceRegistry["SourceRegistry"]
    class estorides_core_source_loader_py_SourceRegistry cls;
    estorides_core_source_loader_py --> estorides_core_source_loader_py_SourceRegistry
    estorides_core_source_loader_py___init__["__init__"]
    class estorides_core_source_loader_py___init__ fn;
    estorides_core_source_loader_py --> estorides_core_source_loader_py___init__
    estorides_core_source_loader_py___getattr__["__getattr__"]
    class estorides_core_source_loader_py___getattr__ fn;
    estorides_core_source_loader_py --> estorides_core_source_loader_py___getattr__
    estorides_core_source_loader_py___init__["__init__"]
    class estorides_core_source_loader_py___init__ fn;
    estorides_core_source_loader_py --> estorides_core_source_loader_py___init__
    end
    subgraph community_8 ["estorides_llm"]
    estorides_llm_manager_py["manager.py (py)"]
    class estorides_llm_manager_py mod;
    estorides_llm_manager_py_LLMBackend["LLMBackend"]
    class estorides_llm_manager_py_LLMBackend cls;
    estorides_llm_manager_py --> estorides_llm_manager_py_LLMBackend
    estorides_llm_manager_py_register["register"]
    class estorides_llm_manager_py_register fn;
    estorides_llm_manager_py --> estorides_llm_manager_py_register
    estorides_llm_manager_py_OllamaBackend["OllamaBackend"]
    class estorides_llm_manager_py_OllamaBackend cls;
    estorides_llm_manager_py --> estorides_llm_manager_py_OllamaBackend
    estorides_llm_manager_py__OpenAICompatibleBackend["_OpenAICompatibleBackend"]
    class estorides_llm_manager_py__OpenAICompatibleBackend cls;
    estorides_llm_manager_py --> estorides_llm_manager_py__OpenAICompatibleBackend
    estorides_llm_manager_py_OpenAIBackend["OpenAIBackend"]
    class estorides_llm_manager_py_OpenAIBackend cls;
    estorides_llm_manager_py --> estorides_llm_manager_py_OpenAIBackend
    tests_test_auth_gate_py["test_auth_gate.py (py)"]
    class tests_test_auth_gate_py mod;
    tests_test_auth_gate_py_app_with_gate["app_with_gate"]
    class tests_test_auth_gate_py_app_with_gate fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_app_with_gate
    tests_test_auth_gate_py_test_gate_auto_generates_token_when_unset["test_gate_auto_generates_token_when_unset"]
    class tests_test_auth_gate_py_test_gate_auto_generates_token_when_unset fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_auto_generates_token_when_unset
    tests_test_auth_gate_py_test_gate_on_rejects_anonymous["test_gate_on_rejects_anonymous"]
    class tests_test_auth_gate_py_test_gate_on_rejects_anonymous fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_on_rejects_anonymous
    tests_test_auth_gate_py_test_gate_on_accepts_bearer_header["test_gate_on_accepts_bearer_header"]
    class tests_test_auth_gate_py_test_gate_on_accepts_bearer_header fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_on_accepts_bearer_header
    tests_test_auth_gate_py_test_gate_on_accepts_alt_header["test_gate_on_accepts_alt_header"]
    class tests_test_auth_gate_py_test_gate_on_accepts_alt_header fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_on_accepts_alt_header
    estorides_core_entity_extraction_py["entity_extraction.py (py)"]
    class estorides_core_entity_extraction_py mod;
    estorides_core_entity_extraction_py_Entity["Entity"]
    class estorides_core_entity_extraction_py_Entity cls;
    estorides_core_entity_extraction_py --> estorides_core_entity_extraction_py_Entity
    estorides_core_entity_extraction_py_detect_query_type["detect_query_type"]
    class estorides_core_entity_extraction_py_detect_query_type fn;
    estorides_core_entity_extraction_py --> estorides_core_entity_extraction_py_detect_query_type
    estorides_core_entity_extraction_py__is_valid_domain["_is_valid_domain"]
    class estorides_core_entity_extraction_py__is_valid_domain fn;
    estorides_core_entity_extraction_py --> estorides_core_entity_extraction_py__is_valid_domain
    estorides_core_entity_extraction_py__context["_context"]
    class estorides_core_entity_extraction_py__context fn;
    estorides_core_entity_extraction_py --> estorides_core_entity_extraction_py__context
    estorides_core_entity_extraction_py_extract_from_text["extract_from_text"]
    class estorides_core_entity_extraction_py_extract_from_text fn;
    estorides_core_entity_extraction_py --> estorides_core_entity_extraction_py_extract_from_text
    end
    subgraph community_6 ["estorides_core"]
    estorides_core_target_management_py["target_management.py (py)"]
    class estorides_core_target_management_py mod;
    estorides_core_target_management_py_auto_detect_type["auto_detect_type"]
    class estorides_core_target_management_py_auto_detect_type fn;
    estorides_core_target_management_py --> estorides_core_target_management_py_auto_detect_type
    estorides_core_target_management_py__type_validator["_type_validator"]
    class estorides_core_target_management_py__type_validator fn;
    estorides_core_target_management_py --> estorides_core_target_management_py__type_validator
    estorides_core_target_management_py_validate_type["validate_type"]
    class estorides_core_target_management_py_validate_type fn;
    estorides_core_target_management_py --> estorides_core_target_management_py_validate_type
    estorides_core_target_management_py_validate_value["validate_value"]
    class estorides_core_target_management_py_validate_value fn;
    estorides_core_target_management_py --> estorides_core_target_management_py_validate_value
    estorides_core_target_management_py_validate_target["validate_target"]
    class estorides_core_target_management_py_validate_target fn;
    estorides_core_target_management_py --> estorides_core_target_management_py_validate_target
    estorides_core_ssrf_guard_py["ssrf_guard.py (py)"]
    class estorides_core_ssrf_guard_py mod;
    estorides_core_ssrf_guard_py_GuardResult["GuardResult"]
    class estorides_core_ssrf_guard_py_GuardResult cls;
    estorides_core_ssrf_guard_py --> estorides_core_ssrf_guard_py_GuardResult
    estorides_core_ssrf_guard_py__is_blocked_v4["_is_blocked_v4"]
    class estorides_core_ssrf_guard_py__is_blocked_v4 fn;
    estorides_core_ssrf_guard_py --> estorides_core_ssrf_guard_py__is_blocked_v4
    estorides_core_ssrf_guard_py__is_blocked_v6["_is_blocked_v6"]
    class estorides_core_ssrf_guard_py__is_blocked_v6 fn;
    estorides_core_ssrf_guard_py --> estorides_core_ssrf_guard_py__is_blocked_v6
    estorides_core_ssrf_guard_py__normalise_host["_normalise_host"]
    class estorides_core_ssrf_guard_py__normalise_host fn;
    estorides_core_ssrf_guard_py --> estorides_core_ssrf_guard_py__normalise_host
    estorides_core_ssrf_guard_py__is_host_in_blocked_literal["_is_host_in_blocked_literal"]
    class estorides_core_ssrf_guard_py__is_host_in_blocked_literal fn;
    estorides_core_ssrf_guard_py --> estorides_core_ssrf_guard_py__is_host_in_blocked_literal
    _test_passive_py["_test_passive.py (py)"]
    class _test_passive_py mod;
    _test_passive_py_check["check"]
    class _test_passive_py_check fn;
    _test_passive_py --> _test_passive_py_check
    _test_passive_py_main["main"]
    class _test_passive_py_main fn;
    _test_passive_py --> _test_passive_py_main
    estorides_export___init___py["__init__.py (py)"]
    class estorides_export___init___py mod;
    tests_test_probabilistic_fusion_py["test_probabilistic_fusion.py (py)"]
    class tests_test_probabilistic_fusion_py mod;
    tests_test_probabilistic_fusion_py__fs["_fs"]
    class tests_test_probabilistic_fusion_py__fs fn;
    tests_test_probabilistic_fusion_py --> tests_test_probabilistic_fusion_py__fs
    tests_test_probabilistic_fusion_py__teardown["_teardown"]
    class tests_test_probabilistic_fusion_py__teardown fn;
    tests_test_probabilistic_fusion_py --> tests_test_probabilistic_fusion_py__teardown
    tests_test_probabilistic_fusion_py__entity["_entity"]
    class tests_test_probabilistic_fusion_py__entity fn;
    tests_test_probabilistic_fusion_py --> tests_test_probabilistic_fusion_py__entity
    tests_test_probabilistic_fusion_py_TestPrimarySourceRaisesLowConf["TestPrimarySourceRaisesLowConf"]
    class tests_test_probabilistic_fusion_py_TestPrimarySourceRaisesLowConf cls;
    tests_test_probabilistic_fusion_py --> tests_test_probabilistic_fusion_py_TestPrimarySourceRaisesLowConf
    tests_test_probabilistic_fusion_py_TestTertiaryCannotOverride["TestTertiaryCannotOverride"]
    class tests_test_probabilistic_fusion_py_TestTertiaryCannotOverride cls;
    tests_test_probabilistic_fusion_py --> tests_test_probabilistic_fusion_py_TestTertiaryCannotOverride
    estorides_core_change_detection_py["change_detection.py (py)"]
    class estorides_core_change_detection_py mod;
    estorides_core_change_detection_py_Edge["Edge"]
    class estorides_core_change_detection_py_Edge cls;
    estorides_core_change_detection_py --> estorides_core_change_detection_py_Edge
    estorides_core_change_detection_py_SnapshotEntity["SnapshotEntity"]
    class estorides_core_change_detection_py_SnapshotEntity cls;
    estorides_core_change_detection_py --> estorides_core_change_detection_py_SnapshotEntity
    estorides_core_change_detection_py_Snapshot["Snapshot"]
    class estorides_core_change_detection_py_Snapshot cls;
    estorides_core_change_detection_py --> estorides_core_change_detection_py_Snapshot
    estorides_core_change_detection_py_ChangeConfig["ChangeConfig"]
    class estorides_core_change_detection_py_ChangeConfig cls;
    estorides_core_change_detection_py --> estorides_core_change_detection_py_ChangeConfig
    estorides_core_change_detection_py_Diff["Diff"]
    class estorides_core_change_detection_py_Diff cls;
    estorides_core_change_detection_py --> estorides_core_change_detection_py_Diff
    tests_test_search_telemetry_py["test_search_telemetry.py (py)"]
    class tests_test_search_telemetry_py mod;
    tests_test_search_telemetry_py__render_index["_render_index"]
    class tests_test_search_telemetry_py__render_index fn;
    tests_test_search_telemetry_py --> tests_test_search_telemetry_py__render_index
    tests_test_search_telemetry_py_test_s1_determinate_progress_midsearch["test_s1_determinate_progress_midsearch"]
    class tests_test_search_telemetry_py_test_s1_determinate_progress_midsearch fn;
    tests_test_search_telemetry_py --> tests_test_search_telemetry_py_test_s1_determinate_progress_midsearch
    tests_test_search_telemetry_py_test_s2_indeterminate_progress["test_s2_indeterminate_progress"]
    class tests_test_search_telemetry_py_test_s2_indeterminate_progress fn;
    tests_test_search_telemetry_py --> tests_test_search_telemetry_py_test_s2_indeterminate_progress
    tests_test_search_telemetry_py_test_s3_completion_stops_spinner["test_s3_completion_stops_spinner"]
    class tests_test_search_telemetry_py_test_s3_completion_stops_spinner fn;
    tests_test_search_telemetry_py --> tests_test_search_telemetry_py_test_s3_completion_stops_spinner
    tests_test_search_telemetry_py_test_s4_out_of_range_is_clamped["test_s4_out_of_range_is_clamped"]
    class tests_test_search_telemetry_py_test_s4_out_of_range_is_clamped fn;
    tests_test_search_telemetry_py --> tests_test_search_telemetry_py_test_s4_out_of_range_is_clamped
    estorides_core_transforms_py["transforms.py (py)"]
    class estorides_core_transforms_py mod;
    estorides_core_transforms_py_Transform["Transform"]
    class estorides_core_transforms_py_Transform cls;
    estorides_core_transforms_py --> estorides_core_transforms_py_Transform
    estorides_core_transforms_py__empty["_empty"]
    class estorides_core_transforms_py__empty fn;
    estorides_core_transforms_py --> estorides_core_transforms_py__empty
    estorides_core_transforms_py__resolver_filtered["_resolver_filtered"]
    class estorides_core_transforms_py__resolver_filtered fn;
    estorides_core_transforms_py --> estorides_core_transforms_py__resolver_filtered
    estorides_core_transforms_py__filter_runner["_filter_runner"]
    class estorides_core_transforms_py__filter_runner fn;
    estorides_core_transforms_py --> estorides_core_transforms_py__filter_runner
    estorides_core_transforms_py__norm["_norm"]
    class estorides_core_transforms_py__norm fn;
    estorides_core_transforms_py --> estorides_core_transforms_py__norm
    tests_properties_test_recon_fusion_properties_py["test_recon_fusion_properties.py (py)"]
    class tests_properties_test_recon_fusion_properties_py mod;
    tests_properties_test_recon_fusion_properties_py_TestPropertyScoreBounds["TestPropertyScoreBounds"]
    class tests_properties_test_recon_fusion_properties_py_TestPropertyScoreBounds cls;
    tests_properties_test_recon_fusion_properties_py --> tests_properties_test_recon_fusion_properties_py_TestPropertyScoreBounds
    tests_properties_test_recon_fusion_properties_py_TestPropertyTotalCounts["TestPropertyTotalCounts"]
    class tests_properties_test_recon_fusion_properties_py_TestPropertyTotalCounts cls;
    tests_properties_test_recon_fusion_properties_py --> tests_properties_test_recon_fusion_properties_py_TestPropertyTotalCounts
    tests_properties_test_recon_fusion_properties_py_TestPropertyTierSumMatches["TestPropertyTierSumMatches"]
    class tests_properties_test_recon_fusion_properties_py_TestPropertyTierSumMatches cls;
    tests_properties_test_recon_fusion_properties_py --> tests_properties_test_recon_fusion_properties_py_TestPropertyTierSumMatches
    tests_properties_test_recon_fusion_properties_py_TestPropertyDeterminism["TestPropertyDeterminism"]
    class tests_properties_test_recon_fusion_properties_py_TestPropertyDeterminism cls;
    tests_properties_test_recon_fusion_properties_py --> tests_properties_test_recon_fusion_properties_py_TestPropertyDeterminism
    tests_properties_test_recon_fusion_properties_py_TestPropertyNoDuplicates["TestPropertyNoDuplicates"]
    class tests_properties_test_recon_fusion_properties_py_TestPropertyNoDuplicates cls;
    tests_properties_test_recon_fusion_properties_py --> tests_properties_test_recon_fusion_properties_py_TestPropertyNoDuplicates
    tests_properties_test_change_detection_properties_py["test_change_detection_properties.py (py)"]
    class tests_properties_test_change_detection_properties_py mod;
    tests_properties_test_change_detection_properties_py_test_scores_always_bounded["test_scores_always_bounded"]
    class tests_properties_test_change_detection_properties_py_test_scores_always_bounded fn;
    tests_properties_test_change_detection_properties_py --> tests_properties_test_change_detection_properties_py_test_scores_always_bounded
    tests_properties_test_change_detection_properties_py_test_max_changes_respected["test_max_changes_respected"]
    class tests_properties_test_change_detection_properties_py_test_max_changes_respected fn;
    tests_properties_test_change_detection_properties_py --> tests_properties_test_change_detection_properties_py_test_max_changes_respected
    tests_properties_test_change_detection_properties_py_test_id_is_16_char_hex["test_id_is_16_char_hex"]
    class tests_properties_test_change_detection_properties_py_test_id_is_16_char_hex fn;
    tests_properties_test_change_detection_properties_py --> tests_properties_test_change_detection_properties_py_test_id_is_16_char_hex
    tests_properties_test_change_detection_properties_py_test_idempotent["test_idempotent"]
    class tests_properties_test_change_detection_properties_py_test_idempotent fn;
    tests_properties_test_change_detection_properties_py --> tests_properties_test_change_detection_properties_py_test_idempotent
    tests_properties_test_change_detection_properties_py_test_first_run_reports_all_as_new["test_first_run_reports_all_as_new"]
    class tests_properties_test_change_detection_properties_py_test_first_run_reports_all_as_new fn;
    tests_properties_test_change_detection_properties_py --> tests_properties_test_change_detection_properties_py_test_first_run_reports_all_as_new
    estorides_core_validation_py["validation.py (py)"]
    class estorides_core_validation_py mod;
    estorides_core_validation_py_QueryValidationError["QueryValidationError"]
    class estorides_core_validation_py_QueryValidationError cls;
    estorides_core_validation_py --> estorides_core_validation_py_QueryValidationError
    estorides_core_validation_py_Query["Query"]
    class estorides_core_validation_py_Query cls;
    estorides_core_validation_py --> estorides_core_validation_py_Query
    estorides_core_validation_py__strip_and_collapse["_strip_and_collapse"]
    class estorides_core_validation_py__strip_and_collapse fn;
    estorides_core_validation_py --> estorides_core_validation_py__strip_and_collapse
    estorides_core_validation_py_validate_query["validate_query"]
    class estorides_core_validation_py_validate_query fn;
    estorides_core_validation_py --> estorides_core_validation_py_validate_query
    estorides_core_validation_py___init__["__init__"]
    class estorides_core_validation_py___init__ fn;
    estorides_core_validation_py --> estorides_core_validation_py___init__
    tests_properties_test_csp_safe_styles_properties_py["test_csp_safe_styles_properties.py (py)"]
    class tests_properties_test_csp_safe_styles_properties_py mod;
    end
```

---

## Architecture Reference

### JS (2 files)

#### `estorides.js`
**Path:** `static/js/estorides.js`
**File Doc:** *Estorides front-end controller*

**Classes:**
- `to` (line 301) - *Panels are keyed by the `<name>-canvas` class, not by id (the map panel's*
- `on` (line 1448) - *Geolocated entities (parsed.lat / parsed.lon) AND country codes. Many parsers stash coords on the entity itself (e.g. abuseipdb has a "countryCode" field). The whole point of v1.1 is to*

**Functions:**
- `detectQueryTypeLocal` (line 44) - *--- UX helpers (v1.4) ----*
- `showToast` (line 55)
- `updateQueryChip` (line 65)
- `setRunProgress` (line 75)
- `showEmptyState` (line 96)
- `summariseObservation` (line 102)
- `buildResultCard` (line 124)
- `populateCategoryFilter` (line 170)
- `applyResultFilters` (line 176)
- `bindResultFilters` (line 188)
- `showFriendlyError` (line 196)
- `focusGraphNodeByValue` (line 209)
- `switchSidebarTab` (line 218)
- `switchCanvasTab` (line 222)
- `clearMap` (line 236)
- `plotPoints` (line 241)
- `replotStreamData` (line 343) - *Rebuild the geospatial + temporal views from everything seen so far. plotPoints clears and redraws from the full coord set, so feeding it the accumulated observations makes the map grow as sources resolve.*
- `stopRunStream` (line 355)
- `runQuery` (line 370)
- `runQueryBlocking` (line 439) - *Blocking fallback: the original one-shot render path.*
- `searchEntity` (line 472) - *Deep-search an entity through the full OSINT pipeline without clearing existing data — appends and merges into current state.*
- `handleRunStreamEvent` (line 515)
- `appendStreamObservation` (line 552)
- `appendStreamEntity` (line 574)
- `clearAll` (line 603)
- `setStatus` (line 630)
- `renderResult` (line 636) - *--- result rendering ----*
- `expandNode` (line 694)
- `mergeExpansionIntoGraph` (line 722) - *Merge a /api/intel/resolve response into the current D3 graph and Leaflet map. Idempotent: re-clicking the same node won't duplicate edges. Returns {nodes, links} counts of what was actually added.*
- `drawGraphWithExtras` (line 782) - *Re-draws the D3 graph with the original nodes/edges PLUS any extras passed in (from a /api/intel/resolve call). The extras are translated to the shape the drawGraph() function already understands (id, label, type, color, size).*
- `pushLink` (line 806)
- `resolverTypeFor` (line 840) - *Map a graph node's type/kind onto a resolver/transform entity type.*
- `saveLevelOverrides` (line 856)
- `levelOf` (line 860)
- `clusterColor` (line 864)
- `deriveClusters` (line 872) - *Build a clusters[] summary from a flat node list (used after a merge when the server-side clusters array isn't carried along).*
- `hideTooltip` (line 885) - *--- floating overlays (tooltip + context menu) ----*
- `sanitizeHTML` (line 889)
- `showTooltipAt` (line 904)
- `hideContextMenu` (line 915)
- `showBridgeTooltip` (line 921) - *Cross-referenced tooltip for an inter-cluster (bridge) link.*
- `showNodeTooltip` (line 950)
- `showContextMenu` (line 959) - *--- context menu: transforms grouped by intel tier ----*
- `setNodeLevel` (line 1024)
- `applyLevelStyles` (line 1033) - *Re-apply level rings to every rendered node circle.*
- `focusNode` (line 1041)
- `runTransform` (line 1053) - *Run a graph pivot transform and merge the result into the graph+map.*
- `selectNode` (line 1071) - *--- side inspector panel ----*
- `add` (line 1082)
- `addText` (line 1088)
- `renderGraphCore` (line 1162) - *--- unified force-graph renderer (clusters + rings + interactions) ----*
- `drawHulls` (line 1232)
- `_redrawGraph` (line 1263) - *Low-level D3 redraw given a flat nodes/links list (back-compat shim).*
- `setStatusDot` (line 1269)
- `showWorkingIndicator` (line 1275)
- `hideWorkingIndicator` (line 1280)
- `toggleTierSection` (line 1285)
- `renderTieredResults` (line 1293)
- `escapeAttr` (line 1359)
- `buildMapCoords` (line 1395)
- `validCoord` (line 1491)
- `colorFor` (line 1495)
- `renderEntities` (line 1514)
- `renderGraphSummary` (line 1564)
- `colorForKind` (line 1593)
- `renderTimeline` (line 1601)
- `fmtTime` (line 1651)
- `filterTimeline` (line 1662)
- `drawGraph` (line 1711) - *--- D3 graph view ----*
- `loadCases` (line 1742)
- `renderCaseItem` (line 1769)
- `debounce` (line 1795)
- `escapeHTML` (line 1844) - *--- utils ----*
- `truncate` (line 1849)
- `caseActionSave` (line 1872) - *Bookmark a case. The endpoint prefixes the notes column with "[saved]" so the bookmarked case surfaces in the list at a glance.*
- `caseActionDiff` (line 1892) - *Compare this case to another. The user picks the baseline; the response is rendered inline in a diff panel under the case.*
- `renderCaseDiffPanel` (line 1910) - *Render the diff result below the case. The panel survives until the user reloads the cases list (or opens another diff).*
- `caseActionReport` (line 1951) - *Render the Markdown report. We just dump the text into a modal overlay — keeping it in-browser is enough; the CLI command produces a file copy for sharing.*
- `showReportModal` (line 1987)
- `loadSidebarWidth` (line 2079) - *Responsive sidebar toggle + resizable divider.*
- `saveSidebarWidth` (line 2090)
- `loadSidebarCollapsed` (line 2093)
- `saveSidebarCollapsed` (line 2101)
- `switchSidebarTab` (line 2159) - *--- Fusion tab ----*
- `loadFusionTab` (line 2168)
- `loadFusionStats` (line 2174)
- `loadFusionTopChanged` (line 2193)
- `loadFusionSearch` (line 2216)
- `doSearch` (line 2223)
- `loadFusionEntityDetail` (line 2255)
- `_sseUrl` (line 2313)
- `setStatus` (line 2337) - *The discoverer code lives outside the IIFE, so the module-private setStatus is not in scope here. Provide a global one that writes to the*
- `setDiscoverProgress` (line 2344)
- `hideDiscoverProgress` (line 2356)
- `startDiscover` (line 2361)
- `stopDiscover` (line 2435)
- `handleDiscoverEvent` (line 2452)
- `addDiscoverEntityToTab` (line 2491)
- `escapeHtml` (line 2519)
- `maybePlotDiscoverEntity` (line 2524)
- `flushDiscoverEntities` (line 2531)
- `set` (line 21) - *Headers may be a Headers instance, an object, or absent.*
- `TELEMETRY` (line 30)
- `status` (line 132)
- `text` (line 177)
- `cat` (line 178)
- `status` (line 179)
- `sig` (line 576)
- `k` (line 735)
- `CLUSTER_PALETTE` (line 833)
- `c` (line 866)
- `cid` (line 875)
- `labelFor` (line 924)
- `c` (line 925)
- `tr` (line 1004)
- `tr` (line 1139)
- `obs` (line 1605)
- `frac` (line 1638)
- `q` (line 1743)
- `saved` (line 1773) - *Saved cases get a visible bookmark pill so the operator can scan the list for "things I came back to" at a glance.*
- `rows` (line 1918)
- `removed` (line 1921)
- `tag` (line 2049)
- `_sseAuthToken` (line 2309) - *Auth token for SSE (EventSource can't set custom headers).*
- `sig` (line 2496) - *Avoid duplicates with the simple in-memory check.*

#### `source_manager.js`
**Path:** `static/js/source_manager.js`
**File Doc:** *Estorides Source Manager — form-based YAML editor*

**Classes:**
- `from` (line 239)

**Functions:**
- `authHeaders` (line 7) - */* Estorides Source Manager — form-based YAML editor (function () { 'use strict'; /* ─── auth ───*
- `apiFetch` (line 15)
- `getCheckedTags` (line 65) - *contact: $('field-contact'), logsQueries: $('field-logs-queries'), toolUrl: $('field-tool-url'), toolMethod: $('field-tool-method'), toolHeaders: $('field-tool-headers'), toolParams: $('field-tool-params'), toolBody: $('field-tool-body'), pagStrategy: $('field-pag-strategy'), pagLimit: $('field-pag-limit'), pagParam: $('field-pag-param'), pagCursorPath: $('field-pag-cursor-path'), }; /* ─── get checked tags ───*
- `setCheckedTags` (line 72)
- `readForm` (line 82) - *var checks = container.querySelectorAll('input[type="checkbox"]:checked'); return Array.from(checks).map(function (c) { return c.value; }); } function setCheckedTags(containerId, values) { var container = $(containerId); if (!container) return; var vals = new Set(values || []); container.querySelectorAll('input[type="checkbox"]').forEach(function (c) { c.checked = vals.has(c.value); }); } /* ─── read form → source object ───*
- `writeForm` (line 118) - *try { var b = JSON.parse(fields.toolBody.value.trim() || '{}'); if (Object.keys(b).length) s.tool.body = b; } catch (e) {} Pagination var strat = fields.pagStrategy.value; if (strat) { s.pagination = { strategy: strat }; var lim = parseInt(fields.pagLimit.value, 10); if (lim > 0) s.pagination.limit = lim; if (fields.pagParam.value.trim()) s.pagination.param = fields.pagParam.value.trim(); if (fields.pagCursorPath.value.trim()) s.pagination.cursor_path = fields.pagCursorPath.value.trim(); } return s; } /* ─── write source object → form ───*
- `updateYamlPreview` (line 168) - *fields.pagCursorPath.value = pag.cursor_path || ''; setCheckedTags('field-applies-to', s.applies_to); setCheckedTags('field-entity-hints', s.entity_hints); currentName = s.name; isDirty = false; formStatus.textContent = ''; formStatus.className = 'form-status'; deleteBtn.hidden = false; updateYamlPreview(); } /* ─── update YAML preview ───*
- `renderList` (line 178) - *updateYamlPreview(); } /* ─── update YAML preview ─── function updateYamlPreview() { try { var s = readForm(); yamlPreview.textContent = JSON.stringify(s, null, 2); } catch (e) { yamlPreview.textContent = '/* cannot render preview */'; } } /* ─── render source list ───*
- `escHtml` (line 207) - *var onOff = s.enabled !== false ? 'on' : 'off'; var keyBadge = s.requires_key ? '<span class="src-item-key-badge">key</span>' : ''; html += '<div class="src-item' + active + '" data-name="' + escAttr(s.name) + '">' + '<span class="src-item-icon ' + onOff + '"></span>' + '<div class="src-item-info">' + '<div class="src-item-name">' + escHtml(s.name) + keyBadge + '</div>' + '<div class="src-item-cat">' + escHtml(s.description || '') + '</div>' + '</div></div>'; }); }); listEl.innerHTML = html || '<div style="padding:20px;text-align:center;color:var(--text-2);font-size:13px;">No sources match filter</div>'; } /* ─── helpers ───*
- `escAttr` (line 208)
- `toast` (line 211) - *'<div class="src-item-info">' + '<div class="src-item-name">' + escHtml(s.name) + keyBadge + '</div>' + '<div class="src-item-cat">' + escHtml(s.description || '') + '</div>' + '</div></div>'; }); }); listEl.innerHTML = html || '<div style="padding:20px;text-align:center;color:var(--text-2);font-size:13px;">No sources match filter</div>'; } /* ─── helpers ─── function escHtml(s) { return String(s).replace(/[&<>"]/g, function (m) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[m]; }); } function escAttr(s) { return String(s).replace(/"/g, '&quot;'); } /* ─── toast ───*
- `loadSources` (line 220) - */* ─── helpers ─── function escHtml(s) { return String(s).replace(/[&<>"]/g, function (m) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[m]; }); } function escAttr(s) { return String(s).replace(/"/g, '&quot;'); } /* ─── toast ─── function toast(msg, kind) { var el = document.createElement('div'); el.className = 'toast ' + (kind || 'info'); el.textContent = msg; document.getElementById('toast-stack').appendChild(el); setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 4000); } /* ─── load sources ───*
- `clearEditor` (line 235) - *apiFetch('/api/sources/yaml').then(function (data) { sources = data.sources || []; srcCount.textContent = data.total + ' sources'; renderList(filterInput.value); If currently selected source still exists, keep it; otherwise clear if (currentName && !data.sources.some(function (s) { return s.name === currentName; })) { clearEditor(); } }).catch(function (err) { toast('Failed to load sources: ' + err.message, 'err'); }); } /* ─── clear editor ───*
- `selectSource` (line 245) - *}); } /* ─── clear editor ─── function clearEditor() { form.hidden = true; editorEmpty.hidden = false; writeForm(null); Remove active class from all list items listEl.querySelectorAll('.src-item.active').forEach(function (el) { el.classList.remove('active'); }); currentName = null; } /* ─── select source ───*
- `saveSource` (line 257) - */* ─── select source ─── function selectSource(name) { var s = sources.filter(function (s) { return s.name === name; })[0]; if (!s) return; form.hidden = false; editorEmpty.hidden = true; writeForm(s); listEl.querySelectorAll('.src-item.active').forEach(function (el) { el.classList.remove('active'); }); var item = listEl.querySelector('.src-item[data-name="' + escAttr(name) + '"]'); if (item) item.classList.add('active'); } /* ─── save source ───*
- `deleteSource` (line 284) - *toast('Source "' + data.name + '" saved', 'ok'); formStatus.textContent = 'Saved'; formStatus.className = 'form-status ok'; loadSources(); Re-select the saved source selectSource(data.name); }).catch(function (err) { toast('Save failed: ' + err.message, 'err'); formStatus.textContent = 'Error: ' + err.message; formStatus.className = 'form-status err'; }); } /* ─── delete source ───*
- `newSource` (line 314) - *overlay.remove(); apiFetch('/api/sources/yaml/' + encodeURIComponent(currentName), { method: 'DELETE' }).then(function () { toast('Source "' + currentName + '" deleted', 'ok'); clearEditor(); loadSources(); }).catch(function (err) { toast('Delete failed: ' + err.message, 'err'); }); }); document.getElementById('confirm-cancel').addEventListener('click', function () { overlay.remove(); }); overlay.addEventListener('click', function (e) { if (e.target === overlay) overlay.remove(); }); } /* ─── new source ───*

### PY (87 files)

#### `_test_entity_resolution.py`
**Path:** `_test_entity_resolution.py`

**Functions:**
- `check` (line 27) `def check(name, cond, detail)`
- `_ent` (line 36) `def _ent(etype, value, source)`
- `_by_value` (line 40) `def _by_value(result, value)`
- `test_transliteration` (line 47) `def test_transliteration()`
- `test_jaro_winkler` (line 63) `def test_jaro_winkler()`
- `test_normalization` (line 74) `def test_normalization()`
- `test_score_pair_policy` (line 98) `def test_score_pair_policy()`
- `test_resolution_merge` (line 111) `def test_resolution_merge()`
- `test_to_entity_roundtrip` (line 167) `def test_to_entity_roundtrip()`
- `test_cross_run_stability` (line 182) `def test_cross_run_stability()`
- `test_empty_and_edge_inputs` (line 211) `def test_empty_and_edge_inputs()`
- `main` (line 219) `def main()`

#### `_test_fusion.py`
**Path:** `_test_fusion.py`

**Functions:**
- `check` (line 24) `def check(label, cond)`
- `_fresh_store` (line 32) `def _fresh_store()`
- `test_deterministic_identity` (line 37) `def test_deterministic_identity()`
- `test_cross_run_dedup_and_provenance` (line 45) `def test_cross_run_dedup_and_provenance()`
- `test_property_corroboration_and_conflict` (line 59) `def test_property_corroboration_and_conflict()`
- `test_min_sources_filter` (line 76) `def test_min_sources_filter()`
- `test_relationship_fusion` (line 87) `def test_relationship_fusion()`
- `test_observation_and_source_counters` (line 97) `def test_observation_and_source_counters()`
- `test_fail_soft_open` (line 116) `def test_fail_soft_open()`
- `main` (line 124) `def main()`

#### `_test_hardening.py`
**Path:** `_test_hardening.py`

**Functions:**
- `_ok` (line 25) `def _ok(name, ok, detail)`
- `test_security_headers` (line 36) `def test_security_headers()`
- `test_cors_default_off` (line 53) `def test_cors_default_off()` - *Without ESTORIDES_CORS_ORIGINS, CORS headers must not be emitted.*
- `test_cors_allowlist` (line 62) `def test_cors_allowlist()` - *With an allowlist, only matching origins get a CORS header.*
- `test_debug_killswitch` (line 87) `def test_debug_killswitch()` - *When DEBUG is on, install_security must refuse to run.*
- `test_max_body_rejection` (line 101) `def test_max_body_rejection()` - *A request body larger than MAX_CONTENT_LENGTH must be rejected.*
- `test_case_diff` (line 113) `def test_case_diff()`
- `test_case_diff_endpoints` (line 137) `def test_case_diff_endpoints()`
- `test_case_save_endpoint` (line 148) `def test_case_save_endpoint()`
- `test_report_renders` (line 165) `def test_report_renders()`
- `test_report_with_diff` (line 181) `def test_report_with_diff()`
- `test_console_script_help` (line 196) `def test_console_script_help()` - *`./estorides` must run even without `pip install -e .`.*
- `main` (line 210) `def main()`

#### `_test_passive.py`
**Path:** `_test_passive.py`

**Functions:**
- `check` (line 20) `def check(name, cond, detail)`
- `main` (line 29) `def main()`

#### `_test_people.py`
**Path:** `_test_people.py`

**Classes:**
- `_StubRunner` (line 66) `class _StubRunner`

**Functions:**
- `check` (line 21) `def check(name, cond, detail)`
- `_types` (line 30) `def _types(payload)`
- `main` (line 37) `def main()`

**Methods:**
- `run` (line 67) `def run(self, query)`

#### `_test_proxy.py`
**Path:** `_test_proxy.py`

**Functions:**
- `check` (line 21) `def check(name, cond, detail)`
- `main` (line 30) `def main()`
- `_enter_and_rotate` (line 52) `def _enter_and_rotate()`
- `_enter_socks` (line 72) `def _enter_socks()`

#### `_test_scope.py`
**Path:** `_test_scope.py`

**Functions:**
- `check` (line 18) `def check(name, cond, detail)`
- `main` (line 27) `def main()`

#### `_validate.py`
**Path:** `_validate.py`

**Functions:**
- `main` (line 17) `def main()`

#### `app.py`
**Path:** `app.py`

*No symbols extracted*

#### `estorides_cli.py`
**Path:** `estorides_cli.py`

**Functions:**
- `_setup_logging` (line 36) `def _setup_logging(verbose)`
- `_collect_selectors` (line 43) `def _collect_selectors(events, types)` - *Group discovered entity values by type for the requested type set.

Used to surface the human selectors (emails, usernames, persons, orgs,
phones) a discover run found, separately from the infrastructure list.*
- `_resolve_proxy` (line 59) `def _resolve_proxy(args)` - *Resolve the egress proxy from the OPSEC flags.

`--tor` is a convenience alias for the default local Tor SOCKS port;
an explicit `--proxy` wins over it. Returns None when neither is set,
in which case the engine still honours the env-configured proxy pool.*
- `_add_opsec_flags` (line 72) `def _add_opsec_flags(parser)` - *Attach the shared operator-OPSEC flags to a subcommand parser.*
- `cmd_discover` (line 90) `def cmd_discover(args)` - *v1.2 — fanout the surface from a seed.

Mirrors the /api/discover/start endpoint but as a CLI subcommand
so an operator can drop a seed in a terminal and walk away.
Streams progress to stdout. The final case is dumped to
--out-json if provided.*
- `cmd_run` (line 202) `def cmd_run(args)`
- `cmd_scope` (line 279) `def cmd_scope(args)` - *Classify discovered assets against a program's scope rules.

Reads assets (a `discover --out-json` surface or a flat host list),
applies the in/out-of-scope rules, and emits the in-scope host/IP
lists an operator pipes into the active phase. Out-of-scope assets are
surfaced explicitly so they are never targeted by accident.*
- `cmd_graph_export` (line 326) `def cmd_graph_export(args)`
- `cmd_export_stix` (line 349) `def cmd_export_stix(args)`
- `cmd_export_misp` (line 359) `def cmd_export_misp(args)`
- `cmd_report` (line 369) `def cmd_report(args)` - *Render a Markdown report for a case.

Reads from the case store (so the report reflects what was persisted,
not the volatile in-memory graph). When `--diff <other_id>` is given,
the report also includes a "what's new" section vs the other case.*
- `cmd_diff` (line 410) `def cmd_diff(args)` - *Diff two cases. CLI twin of /api/cases/diff.*
- `cmd_status` (line 438) `def cmd_status(_)`
- `cmd_fusion` (line 445) `def cmd_fusion(args)` - *Query the cross-run fusion datastore.

Subactions:
  stats              size of the fused fact base
  sources            YAML catalogue with fetch/ok counters
  entities [TERM]    search fused entities (``--type``, ``--min-sources``)
  entity ID          full fused view of one entity (provenance + props)*
- `cmd_serve` (line 486) `def cmd_serve(args)`
- `build_parser` (line 503) `def build_parser()`
- `main` (line 604) `def main(argv)`
- `_on_done` (line 219) `def _on_done(source_name, ok, status, elapsed_ms)`

#### `__init__.py`
**Path:** `estorides_core/__init__.py`

*No symbols extracted*

#### `async_client.py`
**Path:** `estorides_core/async_client.py`

**Classes:**
- `CircuitBreaker` (line 56) `class CircuitBreaker` - *Per-host circuit breaker.*
- `ResponseCache` (line 78) `class ResponseCache` - *SQLite-backed response cache. Key = (url + method + body hash).

Entries carry their write timestamp and are only served while younger
than `ttl_seconds`; a stale row is ignored (and lazily overwritten on
the next live fetch) so the cache can never pin down OSINT that has
since changed or been taken down.*
- `AsyncClient` (line 149) `class AsyncClient` - *Async HTTP client with retries, backoff, circuit breaker, cache.*

**Functions:**
- `_is_socks` (line 41) `def _is_socks(proxy)` - *True when the proxy URL is a SOCKS proxy (e.g. Tor).*
- `_redact_proxy` (line 46) `def _redact_proxy(proxy)` - *Strip any `user:pass@` credentials from a proxy URL before logging.*

**Methods:**
- `sync_fetch` (line 375) `def sync_fetch(method, url)`
- `allow` (line 61) `def allow(self, host)`
- `record_success` (line 67) `def record_success(self, host)`
- `record_failure` (line 71) `def record_failure(self, host)`
- `__init__` (line 87) `def __init__(self, path)`
- `_init_db` (line 100) `def _init_db(self)`
- `_key` (line 113) `def _key(method, url, body)`
- `get` (line 122) `def get(self, method, url, body)`
- `set` (line 138) `def set(self, method, url, body, value)`
- `__init__` (line 152) `def __init__(self)`
- `__aenter__` (line 181) `def __aenter__(self)`
- `_next_http_proxy` (line 225) `def _next_http_proxy(self)` - *Round-robin the next HTTP proxy, or None (SOCKS/connector or direct).*
- `__aexit__` (line 233) `def __aexit__(self)`
- `session` (line 239) `def session(self)`
- `fetch` (line 245) `def fetch(self, method, url)` - *Fetch a URL. Returns (parsed_data, meta).

meta contains status, content_type, cached, attempts, error.
parsed_data is dict/list/str/None depending on content-type.*

#### `audit.py`
**Path:** `estorides_core/audit.py`

**Classes:**
- `AuditEvent` (line 55) `class AuditEvent`
- `AuditLog` (line 72) `class AuditLog` - *Append-only JSONL audit log with a size cap.

Thread-safe via a process-level lock. The on-disk file is opened
per-write so a long-running process never holds an exclusive handle
(which would defeat any out-of-band log rotation tooling).

Issue #48: the log has no built-in rotation, so a busy deployment
grows the file without bound. We apply a soft size cap
(`ESTORIDES_AUDIT_MAX_BYTES`, default 50 MiB). When the cap is
hit we rotate in place: rename the current file to
`audit.jsonl.1` and start fresh. Older rotated copies are
removed so the directory doesn't grow without bound either —
only the active file and the previous rotation survive. The
cap is checked before each write so the cost is one stat per
record.*
- `RateLimiter` (line 180) `class RateLimiter` - *In-process sliding-window rate limiter.

The bucket state is a `dict[str, deque[float]]` held under a
`threading.Lock`. **The state is per-process** — when the
application is deployed with gunicorn's default multi-worker mode
(`-w 4`, as documented in `wsgi.py`), each worker process has its
own counter and the effective rate limit is `N_workers * limit`.

For a multi-worker deployment there are two safe options:

1.  Set `ESTORIDES_RATE_LIMIT = ceil(desired_total / N_workers)`,
    so the per-worker cap × worker count approximates the
    documented limit. This is the recommended shape for a
    single-tenant deployment behind a reverse proxy that does
    not share state.
2.  Swap this class for a Redis-backed implementation; the call
    sites only depend on `allow()` returning a bool, so the swap
    is local to this module. Issue #38 documents the trade-off.*

**Methods:**
- `to_jsonl` (line 68) `def to_jsonl(self)`
- `__init__` (line 90) `def __init__(self, path)`
- `record` (line 104) `def record(self, event)`
- `_maybe_rotate_locked` (line 115) `def _maybe_rotate_locked(self)` - *If the active file is over the cap, rotate in place.

Caller must hold `self._lock`. We use a per-write stat-then-
write sequence; the race window (another process also writing)
is acceptable for a single-tenant audit log — the worst case
is a slightly oversized file, not data loss.*
- `query` (line 150) `def query(self, event)`
- `__init__` (line 201) `def __init__(self)`
- `allow` (line 214) `def allow(self, key)` - *Return (allowed, retry_after_seconds).

`retry_after_seconds` is 0 when allowed, otherwise the number of
seconds the caller should wait before retrying.

The configured `max_requests` is re-read from the environment on
every call so an operator can hot-tune the limit without a
process restart. (The window itself is stable for a process
lifetime, which is fine for our deployment shape.)*
- `reset` (line 238) `def reset(self, key)`

#### `cases.py`
**Path:** `estorides_core/cases.py`

**Classes:**
- `CaseStore` (line 112) `class CaseStore` - *Thread-safe SQLite-backed case repository.

SQLite is plenty for OSINT-sized workloads (a few thousand cases
per operator per month) and avoids a separate service. The
underlying file is shared with the cache if you point both env
vars at the same path; otherwise we live in `estorides_cases.sqlite`
next to it.*

**Methods:**
- `__init__` (line 121) `def __init__(self, path)`
- `_init_schema` (line 135) `def _init_schema(self)`
- `_tx` (line 141) `def _tx(self)`
- `create_case` (line 152) `def create_case(self, query, query_type, notes)` - *Open a new case and return its id (8-char slug).*
- `add_observation` (line 168) `def add_observation(self, case_id, observation)` - *Persist a single observation row.

The full parsed/raw payload is JSON-encoded so we can
reconstruct the run later without re-running the source.*
- `add_entities` (line 202) `def add_entities(self, case_id, entities)` - *Persist the merged entity list. Duplicate (type, value) rows
for the same case are silently ignored — the PK is the guard.*
- `finalise` (line 225) `def finalise(self, case_id, analysis, kg_path, mitre, source_count, obs_count, entity_count, status)`
- `delete_case` (line 255) `def delete_case(self, case_id)`
- `get_case` (line 260) `def get_case(self, case_id)`
- `list_observations` (line 273) `def list_observations(self, case_id)`
- `list_entities` (line 296) `def list_entities(self, case_id)`
- `diff_entities` (line 311) `def diff_entities(self, case_a, case_b)` - *Compare two cases by entity (type, value) keys.

Returns the symmetric difference plus counts and the per-type
breakdown. The "added" set is what case B learned that A did
not have; "removed" is the inverse. This is the OSINT analogue
of `git diff A B` and is the building block for the
"what's new since last run" UI the analyst wants to see.

Both cases are looked up in a single connection hold so the
diff is consistent even if the case store is being written
to concurrently.*
- `search_cases` (line 358) `def search_cases(self, query_substring, limit, query_type)` - *Lightweight case search. LIKE on `query` (not indexed, but
acceptable for the OSINT scale of a few thousand cases).*
- `search_by_entity` (line 388) `def search_by_entity(self, ent_type, value, limit)` - *Find every case that observed a given entity.

This is the cross-run memory query — the heart of "have I
seen this before?".*
- `stats` (line 416) `def stats(self)`
- `_row_to_case` (line 424) `def _row_to_case(self, row)`
- `_safe_json` (line 442) `def _safe_json(text)`
- `close` (line 450) `def close(self)`
- `_per_type` (line 332) `def _per_type(pairs)`
- `_serialise` (line 338) `def _serialise(pairs)`

#### `change_detection.py`
**Path:** `estorides_core/change_detection.py`

**Classes:**
- `Edge` (line 58) `class Edge` - *Outgoing edge: typed destination + relation name.*
- `SnapshotEntity` (line 66) `class SnapshotEntity` - *One entity as captured at snapshot time.

Mirrors the fields the fusion store already persists
(``first_seen``/``last_seen``/``confidence``/``sources``), so a
Snapshot can be built directly from a fused row.*
- `Snapshot` (line 96) `class Snapshot` - *An immutable view of an investigation at one point in time.*
- `ChangeConfig` (line 104) `class ChangeConfig` - *Tuning for :func:`detect_changes`.*
- `Diff` (line 125) `class Diff` - *Structured description of a single change's delta.*
- `Change` (line 134) `class Change` - *One detected change.*
- `ChangeSummary` (line 151) `class ChangeSummary` - *Aggregate stats for a :class:`ChangeReport`.*
- `ChangeReport` (line 168) `class ChangeReport` - *Top-N changes + summary stats for a single diff operation.*

**Methods:**
- `_truncate_key` (line 176) `def _truncate_key(key)`
- `_change_id` (line 183) `def _change_id(kind, entity_id, diff_signature)`
- `_reliability_weight` (line 188) `def _reliability_weight(name)` - *Reliability weight via 2a, with 0 fallback for the impossible
case where the enum value is not a letter A-F.*
- `_reliability_floor` (line 205) `def _reliability_floor(letter)` - *A=1, B=2, ..., F=6. For 'min_reliability' comparison.*
- `_filter_sources_by_reliability` (line 210) `def _filter_sources_by_reliability(sources, min_reliability)`
- `_property_diff` (line 223) `def _property_diff(before, after)` - *Compute the per-key add/change/remove between two property maps.*
- `_edge_set` (line 242) `def _edge_set(edges)`
- `_union_sources` (line 246) `def _union_sources(a, b)` - *Sorted union of two entities' source lists.

Used in every per-entity Change (property_changed, source_added,
source_removed, edge_added, edge_removed, confidence_shifted) as
the ``sources`` field of the audit trail — the analyst should be
able to see every source that touched the entity, not just the
trigger of the change.*
- `_make_change` (line 258) `def _make_change(kind, entity_id, entity_type, entity_value, sig)` - *Build a :class:`Change` with the deterministic id derived from
``kind + entity_id + sig``. Centralised so the eight change kinds
can never disagree on the field set or the id format.*
- `_below_min_reliability` (line 291) `def _below_min_reliability(source, min_reliability)` - *True if a source's reliability is strictly *worse* than the
configured minimum (i.e. it should be filtered out).*
- `detect_changes` (line 301) `def detect_changes(snapshot_before, snapshot_after)` - *Diff two snapshots. Pure: no I/O, deterministic, bounded.

Parameters
----------
snapshot_before, snapshot_after
    The two snapshots to diff. Either may be ``None``:
    ``before=None`` ⇒ first run, every entity is ``new``;
    ``after=None`` ⇒ no future data, empty report.
config
    Optional tuning. See :class:`ChangeConfig`.*
- `__post_init__` (line 84) `def __post_init__(self)`
- `__post_init__` (line 115) `def __post_init__(self)`

#### `config.py`
**Path:** `estorides_core/config.py`

**Classes:**
- `CacheConfig` (line 329) `class CacheConfig` - *Disk response-cache behaviour.*
- `PivotPolicyConfig` (line 342) `class PivotPolicyConfig` - *Which entity types are worth pivoting on, and how leads are scored.

The recursive cross-search expands the highest-scoring leads first.
`type_weights` lets a high-signal selector (an email, a wallet) outrank
a low-signal one (a shared CDN IP) at the same depth. `depth_decay`
discounts every additional hop so the frontier stays close to the seed.*
- `PivotConfig` (line 367) `class PivotConfig` - *Bounds and defaults for the recursive pivot engine.

`*_cap` values are the absolute ceilings applied to any caller-supplied
override (e.g. an API request body), so an untrusted client can never
request an unbounded crawl.*
- `StreamConfig` (line 412) `class StreamConfig` - *Server-Sent-Events streaming knobs (buffer size, cadence).*
- `ReconFusionConfig` (line 424) `class ReconFusionConfig` - *Centralised tunables for the passive recon fusion engine.

Controls how raw OSINT results are grouped, deduplicated and classified
into relevance tiers. Every field has an env var equivalent so the
operator can adjust behaviour without touching code.

This is the SINGLE source of truth. The engine module imports from here
and never defines its own copy.*
- `WebConfig` (line 456) `class WebConfig` - *Per-endpoint defaults and render limits for the Flask layer.*

**Functions:**
- `_env_int` (line 32) `def _env_int(name, default)` - *Read an int env var, falling back to `default` on absence/parse error.*
- `_env_float` (line 44) `def _env_float(name, default)` - *Read a float env var, falling back to `default` on absence/parse error.*
- `_env_bool` (line 56) `def _env_bool(name, default)` - *Read a boolean env var. Truthy tokens: 1/true/yes/on (case-insensitive).*
- `ensure_data_dirs` (line 86) `def ensure_data_dirs()` - *Idempotently create DATA_DIR.

Replaces the import-time mkdir that issue #49 reported. Call
this from the app factory and from any code path that actually
needs to write to DATA_DIR. Idempotent: exist_ok=True so a
pre-existing directory is fine.*
- `ensure_reports_dir` (line 97) `def ensure_reports_dir()` - *Idempotently create REPORTS_DIR.

Same posture as ensure_data_dirs(). /api/export/<fmt> used to
write through this path; issue #43 moved export artefacts to a
tempfile, but the directory is still useful for operator-facing
exports.*
- `contact_level` (line 185) `def contact_level(contact)` - *Map a contact class to its numeric severity, unknown values to active.

An unrecognised class is treated as the most exposing (`active`) so a
typo in a source YAML can never silently downgrade an operator's
passive-only guarantee.*
- `effective_proxies` (line 211) `def effective_proxies(explicit)` - *Resolve the proxy rotation pool from an explicit value or the env.

Precedence: an explicit caller value (CLI flag) wins; otherwise the
pool env var, otherwise the single-proxy env var. Returns an empty
list when no anonymising egress is configured.*

**Methods:**
- `_pivot_weight_map` (line 470) `def _pivot_weight_map()` - *Default per-type lead weights for the pivot scorer.

Strong, single-owner selectors rank above shared infrastructure.*
- `_csv_frozenset` (line 487) `def _csv_frozenset(name, default)` - *Read a comma-separated env var into a frozenset, else the default.*
- `is_active` (line 336) `def is_active(self)` - *Cache is only consulted when enabled and the TTL is positive.*
- `is_pivotable` (line 356) `def is_pivotable(self, entity_type)` - *True when an entity of `entity_type` should be re-queried.*
- `lead_score` (line 360) `def lead_score(self, entity_type, depth, parent_score)` - *Priority of expanding this lead. Higher expands sooner.*
- `clamp_depth` (line 390) `def clamp_depth(self, value)` - *Clamp a requested depth into [1, max_depth_cap].*
- `clamp_steps` (line 394) `def clamp_steps(self, value)` - *Clamp a requested step budget into [1, max_steps_cap].*
- `clamp_entities` (line 398) `def clamp_entities(self, value)` - *Clamp a requested entity budget into [1, max_entities_cap].*
- `clamp_parallel` (line 402) `def clamp_parallel(self, value)` - *Clamp a requested fan-out width into [1, parallel_cap].*
- `clamp_deadline` (line 406) `def clamp_deadline(self, value)` - *Clamp a requested per-target deadline into (0, deadline_cap_seconds].*
- `__post_init__` (line 445) `def __post_init__(self)`

#### `discoverer.py`
**Path:** `estorides_core/discoverer.py`

**Classes:**
- `DiscoverJob` (line 50) `class DiscoverJob` - *One background discovery session.

Lives in `DISCOVER_JOBS` keyed by job_id; survives the SSE handler
exiting (so a UI reload reconnects and resumes).*
- `_DiscoverJobSink` (line 95) `class _DiscoverJobSink` - *Adapts engine `PivotEvent`s to the legacy DiscoverJob event dicts.

The UI and CLI consume `step_start`, `node_found`, `step_done`,
`finished` and `error`; this translator preserves those shapes so the
engine swap is invisible to every existing consumer.*

**Methods:**
- `_new_job_id` (line 189) `def _new_job_id()` - *Monotonic-ish id with a timestamp prefix for natural sort.*
- `create_discover_job` (line 194) `def create_discover_job(seed_type, seed_value)` - *Create and register a discovery job synchronously.

This does only fast, loop-free work (a case-store insert and some
bookkeeping), so it is safe to call straight from a Flask request
thread. The asyncio worker that actually crawls is scheduled
separately by `start_discover` / `start_discover_threadsafe`, so the
caller never blocks on the shared background loop.*
- `start_discover` (line 252) `def start_discover(seed_type, seed_value)` - *Create a discovery job and schedule its worker on the current loop.

Kept as the coroutine entry point for callers that already own a
running loop (the CLI). Web callers use `start_discover_threadsafe`,
which never blocks the request thread on the background loop.*
- `start_discover_threadsafe` (line 285) `def start_discover_threadsafe(loop, seed_type, seed_value)` - *Create the job in the calling thread, fire its worker on `loop`.

Returns immediately. The worker is queued with
`run_coroutine_threadsafe` and runs whenever the loop is next free, so
a busy loop (a concurrent deep-run) can never make this call time out.*
- `_run_discoverer` (line 319) `def _run_discoverer(job)` - *The background loop. One asyncio task per job, driving the engine.*
- `list_jobs` (line 349) `def list_jobs(limit)` - *Snapshot of the recent jobs for the /api/discover/jobs endpoint.*
- `stop` (line 78) `def stop(self)`
- `should_stop` (line 81) `def should_stop(self)`
- `push_event` (line 84) `def push_event(self, ev)` - *Append an event and keep the buffer bounded.*
- `__init__` (line 103) `def __init__(self, job)`
- `emit` (line 106) `def emit(self, event)`
- `_on_started` (line 113) `def _on_started(self, data)`
- `_on_target_start` (line 116) `def _on_target_start(self, data)`
- `_on_entity` (line 126) `def _on_entity(self, data)`
- `_on_target_done` (line 141) `def _on_target_done(self, data)`
- `_on_target_error` (line 153) `def _on_target_error(self, data)`
- `_on_stopping` (line 160) `def _on_stopping(self, data)`
- `_on_finished` (line 163) `def _on_finished(self, data)`
- `_on_fatal` (line 174) `def _on_fatal(self, data)`

#### `entity_extraction.py`
**Path:** `estorides_core/entity_extraction.py`

**Classes:**
- `Entity` (line 22) `class Entity`

**Methods:**
- `detect_query_type` (line 63) `def detect_query_type(query)` - *Return the detected type of a free-form query.

Falls back to 'domain' for anything that looks like a hostname
(contains a dot, no spaces), and to 'keyword' for everything else.*
- `_is_valid_domain` (line 84) `def _is_valid_domain(candidate)`
- `_context` (line 97) `def _context(text, start, end, window)`
- `extract_from_text` (line 103) `def extract_from_text(text, source)` - *Find every recognised entity in a raw text blob.

`types` optionally restricts which kinds of entity to look for.*
- `_ip_in_textual_context` (line 155) `def _ip_in_textual_context(text, idx)` - *Heuristic: only count a numeric match as an IP if it isn't part of a
version number or timestamp (preceded/followed by `version`, `v`, or `:`).*
- `extract_from_json` (line 165) `def extract_from_json(payload, source)` - *Pull entities out of a JSON-like structure.

Earlier this recursed into every string and ran all patterns on each one,
so a response with thousands of entries (crt.sh subdomains, wayback URLs)
triggered hundreds of thousands of regex passes. We now flatten the payload
to a single capped string and scan it once; entities span keys and values
just as well, and the cost is bounded by `extract_from_text`.*
- `_clean_scalar` (line 233) `def _clean_scalar(value)` - *Return a stripped string for a scalar leaf, or None for non-scalars.*
- `_looks_like_person` (line 243) `def _looks_like_person(value)` - *True when a value reads like a human name (has a space, mostly letters).*
- `_looks_like_username` (line 254) `def _looks_like_username(value)` - *True when a value reads like a handle (no spaces, handle charset).*
- `_classify_keyed_value` (line 261) `def _classify_keyed_value(key, value)` - *Map a (key, scalar value) pair to a human-selector entity type, or None.*
- `extract_structured` (line 285) `def extract_structured(payload, source)` - *Extract human selectors (email, username, person, org, phone) by key.

Walks the JSON structure and types values by the key they sit under,
which is the only reliable way to recover usernames and person names
(they have no lexical signature for a regex to catch). Bounded by
`ENTITY_MAX_PER_TYPE` per type and a node-visit cap so a pathological
response cannot turn this into a CPU stall.*
- `merge` (line 337) `def merge()` - *Deduplicate by (type, value) and merge sources / contexts.

Two entities with the same (type, value) collapse into a single
record. Their `sources` lists are unioned (preserving the first
seen order), `context` is concatenated up to a 200-char window,
and `confidence` is bumped by 0.1 for each extra observation
(capped at 1.0) — a simple "corroboration bonus".

The `sources` field is the canonical "all the places this was
seen" record. The previous implementation stored it in a
private attribute (`_src`) that was never serialised and broke
`asdict()` (TypeError on `dataclasses.asdict` for non-dataclass
attributes). This version is a real, declared field.

v1.1: After exact-key dedup, run a second pass with
`difflib.SequenceMatcher` to catch near-misses like
`EvilCorp.com` vs `evil-corp.com`. Anything above the
`FUZZY_THRESHOLD` ratio collapses into a single record.
Returns the deduped list, with cluster groups available via
`fuzzy_clusters` if the caller wants them.

v1.4: pass ``fuzzy=False`` to do exact-key dedup only. The
orchestrator does this when the canonical identity layer
(`entity_resolution`) is active, so the resolver owns every fuzzy
decision instead of inheriting a coarser difflib pre-merge that would,
for example, silently fuse two distinct domain registrations the
resolver intends to keep separate and merely *link*.*
- `_fuzzy_cluster` (line 431) `def _fuzzy_cluster(entities)` - *Group entities of the same type by string similarity and merge.

Uses `difflib.SequenceMatcher.ratio()`. We compare normalised
(lowercased, hyphen-stripped) forms so `evil-corp.com` and
`evilcorp.com` collide cleanly. Only domain / email / person /
org types are eligible — IPs, hashes, and CVEs have exact
semantics where fuzzy would be a bug, not a feature.*
- `to_dict` (line 34) `def to_dict(self)`
- `visit` (line 299) `def visit(node, key)`
- `find` (line 452) `def find(x)`
- `union` (line 458) `def union(a, b)`
- `norm` (line 463) `def norm(v)`

#### `entity_resolution.py`
**Path:** `estorides_core/entity_resolution.py`

**Classes:**
- `MatchScore` (line 296) `class MatchScore` - *The result of comparing two entity values of the same type.*
- `CanonicalEntity` (line 342) `class CanonicalEntity` - *A resolved identity fused from one or more observed entities.*
- `SameAsLink` (line 402) `class SameAsLink` - *A suggested-but-unmerged identity link between two canonical ids.*
- `ResolutionResult` (line 420) `class ResolutionResult` - *Output of a resolve() call: fused entities plus candidate links.*
- `_UnionFind` (line 433) `class _UnionFind` - *Disjoint-set over integer indices with path compression.*
- `EntityResolver` (line 455) `class EntityResolver` - *Resolve a per-run entity list into canonical identities.

The resolver is deliberately stateless across calls by default; pass a
store (see :mod:`estorides_core.entity_store`) to make canonical ids
stable across runs. A single :meth:`resolve` call:

1. exact-merges entities sharing a ``(type, normalized)`` key;
2. blocks the remaining fuzzy-eligible groups and scores in-bucket
   pairs, unioning clusters at or above the merge threshold and
   recording ``SAME_AS`` candidates above the link threshold;
3. emits one :class:`CanonicalEntity` per cluster with a deterministic
   representative and full provenance.*

**Functions:**
- `jaro` (line 83) `def jaro(s1, s2)` - *Return the Jaro similarity of two strings in ``[0, 1]``.*
- `jaro_winkler` (line 126) `def jaro_winkler(s1, s2, prefix_weight)` - *Jaro-Winkler similarity: Jaro with a shared-prefix bonus.

The prefix bonus (up to 4 leading characters) rewards strings that
agree at the start, which is the common shape of name and domain
variants. ``prefix_weight`` is capped at 0.25 to keep the result in
``[0, 1]``.*
- `_soundex` (line 146) `def _soundex(token)` - *Return a 4-character Soundex code for a Latin token.

Used only as a blocking key: it groups phonetically similar tokens so
the expensive pairwise scorer runs on plausible candidates rather than
the whole list. Empty or non-alphabetic input yields ``"0000"``.*
- `_normalize_domain` (line 178) `def _normalize_domain(value)`
- `_normalize_name` (line 187) `def _normalize_name(value)` - *Order-independent transliterated key for persons and orgs.

The surface form is transliterated to Latin, punctuation dropped, and
the tokens sorted, so ``"Putin, Vladimir"`` and ``"Владимир Путин"``
converge on the same normalised string and merge deterministically.
Cross-script spellings that survive transliteration with different
vowels (abjad scripts) are caught later by the skeleton scorer.*
- `normalize_value` (line 206) `def normalize_value(etype, value)` - *Return the canonical normalised form of an entity value.

The normalised form is the merge key for deterministic types and the
seed of the stable canonical id for every type. It is intentionally
lossy (case, ordering, ornament removed) but never collapses distinct
objects of a deterministic type.*
- `canonical_id` (line 246) `def canonical_id(etype, normalized)` - *Stable, content-addressed id for a normalised entity.

Same ``(type, normalized)`` always yields the same id, so a canonical
entity keeps its identity for as long as its normalised form is stable.
The persistent store additionally maps known aliases onto an existing
id so a never-before-seen surface form still resolves to the same node.*
- `blocking_keys` (line 258) `def blocking_keys(etype, normalized, value)` - *Return the blocking keys that bucket an entity for comparison.

Two entities are only ever scored against each other if they share at
least one blocking key. The keys are chosen to be high-recall (so true
matches land together) while keeping buckets small enough that the
in-bucket pairwise scan stays cheap.*

**Methods:**
- `score_pair` (line 303) `def score_pair(etype, a_value, b_value, a_norm, b_norm)` - *Score how likely two same-type entities denote the same object.

Deterministic types return 1.0 only on normalised equality and 0.0
otherwise. Fuzzy types layer Jaro-Winkler over the normalised form with
a cross-script consonant-skeleton booster for names, so a Cyrillic and
a Latin spelling of one person can clear the link bar even when their
transliterated vowels differ.*
- `_script_of` (line 451) `def _script_of(value)`
- `resolve_entities` (line 728) `def resolve_entities(entities)` - *Module-level convenience wrapper around :class:`EntityResolver`.*
- `to_dict` (line 358) `def to_dict(self)`
- `to_entity` (line 374) `def to_entity(self)` - *Project back onto the legacy :class:`Entity` shape.

Lets the resolver drop into the existing orchestrator, knowledge
graph, and case-store paths without changing their interfaces while
carrying the new identity metadata in ``attributes``.*
- `to_dict` (line 410) `def to_dict(self)`
- `to_dict` (line 426) `def to_dict(self)`
- `__init__` (line 436) `def __init__(self, n)`
- `find` (line 439) `def find(self, x)`
- `union` (line 445) `def union(self, a, b)`
- `__init__` (line 470) `def __init__(self)`
- `resolve` (line 483) `def resolve(self, entities)` - *Resolve ``entities`` into canonical identities and links.*
- `_build_records` (line 499) `def _build_records(self, entities)`
- `_exact_merge` (line 514) `def _exact_merge(records, uf)`
- `_fuzzy_merge` (line 526) `def _fuzzy_merge(self, records, uf)` - *Block, score, merge at threshold, and collect link candidates.

Merges (union) happen eagerly as pairs clear the merge bar. Pairs
that only clear the lower link bar are returned as ``(a, b, score)``
index triples for the caller to translate into canonical-id links
once clusters are materialised.*
- `_build_links` (line 567) `def _build_links(candidates, uf, root_to_cid)` - *Translate index-pair link candidates into canonical-id links.

Pairs whose clusters ended up merged (a later, stronger edge pulled
them together) are dropped; the rest are deduplicated per
canonical-id pair, keeping the highest-scoring justification.*
- `_materialise` (line 595) `def _materialise(self, records, uf)`
- `_representative` (line 662) `def _representative(members)` - *Pick a stable representative for a cluster.

Preference order: most corroborated (appears in most sources), then
a Latin surface form over a non-Latin one (more broadly readable in
reports), then the lexicographically smallest value. The result is
deterministic for a given member set, which keeps the canonical id
stable run to run.*
- `_best_internal_match` (line 680) `def _best_internal_match(members)` - *Return the (method, score) of the strongest non-exact pair.

Surfaces *why* a multi-member cluster was fused, so the analyst can
see whether the merge rested on an exact key or a probabilistic
name match. Bounded to the first handful of members to stay cheap on
large clusters.*
- `_reconcile_with_store` (line 706) `def _reconcile_with_store(self, canonicals)` - *Map canonicals onto persisted ids and record their aliases.

Looked up alias-first so a brand-new surface form of a known entity
adopts the existing canonical id instead of minting a new one. The
store call is best-effort: any failure leaves the freshly computed
id in place rather than aborting the run.*
- `rank` (line 671) `def rank(rec)`

#### `entity_store.py`
**Path:** `estorides_core/entity_store.py`

**Classes:**
- `EntityStore` (line 62) `class EntityStore` - *Thread-safe SQLite repository of canonical identities and aliases.*

**Methods:**
- `open_store` (line 184) `def open_store(path)` - *Open the store, returning None instead of raising on failure.

The resolver calls this so that an unwritable or locked data directory
degrades the cross-run identity feature to in-run-only resolution rather
than aborting an investigation.*
- `__init__` (line 65) `def __init__(self, path)`
- `_init_schema` (line 75) `def _init_schema(self)`
- `_tx` (line 81) `def _tx(self)`
- `lookup` (line 91) `def lookup(self, etype, normalized, aliases)` - *Return an existing canonical id for any known form, or None.

Checks every normalised key the entity can present — its own and
each alias's — against both the canonical ``entities`` table and the
``aliases`` table. The first established id wins, so a never-before
spelling of a known target still resolves to its prior identity.*
- `upsert` (line 129) `def upsert(self, entity)` - *Persist (insert or update) a canonical entity and its aliases.

``first_seen`` is preserved across updates; ``last_seen``,
``member_count``, ``source_count``, ``value``, and ``confidence``
track the latest resolution. Every alias is recorded with its
normalised key so future lookups can route any surface form back to
this id.*
- `stats` (line 168) `def stats(self)` - *Return a one-glance summary of store size.*
- `close` (line 179) `def close(self)`

#### `feeds.py`
**Path:** `estorides_core/feeds.py`

**Classes:**
- `FeedPoint` (line 54) `class FeedPoint` - *Normalised point for the map layer.

`kind` discriminates the marker on the map (flight / quake / fire /
news / vessel). `extra` is an open dict for source-specific fields
the frontend may want to render in the popup.*
- `Feed` (line 74) `class Feed(ABC)` - *Base class for a real-time feed.*
- `EarthquakesFeed` (line 148) `class EarthquakesFeed(Feed)` - *USGS M2.5+ earthquakes, last 24h, worldwide.*
- `FiresFeed` (line 190) `class FiresFeed(Feed)` - *NASA FIRMS active fire hotspots (VIIRS_NOAA20_NRT, last 24h).

FIRMS retired its keyless CSV download in 2024. The new endpoint
at `api/data/active_fire/csv/...` requires a MAP_KEY (free with
NASA Earthdata registration) which is read from the
`ESTORIDES_FIRMS_KEY` env var. If the key is missing the feed
silently returns zero points and logs a warning — it never
breaks the rest of the platform.*
- `NewsFeed` (line 251) `class NewsFeed(Feed)` - *GDELT 2.0 — global news articles (article-list API).

The GeoJSON endpoint we used in the previous version was retired.
The current keyless endpoint is the article-list API at
`/api/v2/doc/doc` which returns a JSON `articles` array. We
attempt to geocode the article URL via the embedded
`socialimage` or `domain` field when coordinates aren't in the
payload — falling back to the article's source domain
coordinates is intentionally out of scope for this version, so
a record without explicit coordinates is dropped.*

**Methods:**
- `list_feeds` (line 313) `def list_feeds()` - *Return public feed descriptions for the /api/feeds endpoint.*
- `get_feed` (line 321) `def get_feed(name)`
- `fetch_all` (line 325) `def fetch_all(bbox, use_cache)` - *Fetch every registered feed (optionally clipped to a bbox).

Used by /api/feeds to populate the map in one round-trip.

bbox = (min_lon, min_lat, max_lon, max_lat). Points outside the
bbox are dropped before the response is returned.*
- `to_dict` (line 69) `def to_dict(self)`
- `__init__` (line 82) `def __init__(self)`
- `_fetch` (line 87) `def _fetch(self)` - *Subclass implementation: hit the upstream and return points.*
- `fetch` (line 90) `def fetch(self)` - *Public entrypoint. Reads/writes the on-disk cache.

The cache is a simple `{fetched_at, points}` JSON blob —
good enough for a self-hosted deployment. A real production
system would want a TTL'd Redis layer, but that pulls in a
network dependency.*
- `point` (line 135) `def point(self, record)` - *Default: return (lat, lon) if both present.*
- `_fetch` (line 156) `def _fetch(self)`
- `_fetch` (line 209) `def _fetch(self)`
- `_fetch` (line 271) `def _fetch(self)`

#### `fusion_analytics.py`
**Path:** `estorides_core/fusion_analytics.py`

**Classes:**
- `FusionAnalytics` (line 31) `class FusionAnalytics` - *Read-only analytics queries over the fusion store.

Every method is parameterized SQL — no string interpolation.
A ``store`` of ``None`` is silently handled (all methods return
empty results) so the caller never needs to guard against a
missing datastore.*

**Methods:**
- `__init__` (line 40) `def __init__(self, store)`
- `entity_timeline` (line 46) `def entity_timeline(self, eid)`
- `entity_summary` (line 132) `def entity_summary(self, eid)`
- `source_stats` (line 213) `def source_stats(self, source_name)`
- `multi_source_consensus` (line 290) `def multi_source_consensus(self, eid, key)`
- `corroborated_properties` (line 343) `def corroborated_properties(self, eid, min_sources)`
- `entity_search` (line 374) `def entity_search(self, term, etype)`
- `top_changed` (line 432) `def top_changed(self, days, limit)`
- `source_corroboration_matrix` (line 477) `def source_corroboration_matrix(self, limit)`
- `_resolve_entity_value` (line 509) `def _resolve_entity_value(self, eid)`
- `_resolve_entity_type` (line 520) `def _resolve_entity_type(self, eid)`
- `_intel_level` (line 532) `def _intel_level(source_count, sources)`
- `_deduplicate_relationships` (line 540) `def _deduplicate_relationships(rels)`

#### `fusion_store.py`
**Path:** `estorides_core/fusion_store.py`

**Classes:**
- `FusionStore` (line 191) `class FusionStore` - *Thread-safe SQLite-backed fusion datastore.

One serialised connection guarded by a lock, WAL journalling, and
``ON DELETE CASCADE`` foreign keys so dropping an entity reaps its
provenance, properties and edges.*

**Functions:**
- `entity_id` (line 178) `def entity_id(etype, value, normalized)` - *Deterministic, run-independent id for an entity.

Derived from the type and the normalised value so the same real-world
entity always hashes to the same id no matter which run or source first
produced it — the property that makes cross-run fusion automatic.*

**Methods:**
- `open_store` (line 753) `def open_store(path)` - *Open the fusion store, returning None instead of raising on failure.

The orchestrator calls this so an unwritable or locked data directory
degrades the fusion layer to a no-op rather than aborting an
investigation.*
- `__init__` (line 199) `def __init__(self, path)`
- `_init_schema` (line 210) `def _init_schema(self)`
- `_tx` (line 216) `def _tx(self)`
- `_ensure_entity_stub` (line 227) `def _ensure_entity_stub(conn, etype, value)` - *Insert a minimal entity row if absent and return its id.

Used for relationship endpoints (a country, an ASN, a port) that no
entity-extraction pass produced, so an edge is always navigable from
both ends. Runs inside the caller's transaction; never overwrites an
already-fused entity (``INSERT OR IGNORE``).*
- `register_sources` (line 247) `def register_sources(self, sources)` - *Mirror the YAML source catalogue into the store.

Idempotent: an existing source keeps its ``first_seen`` and its
accumulated counters; only the descriptive columns are refreshed so
the catalogue tracks edits to the YAML without losing fetch history.*
- `add_observation` (line 284) `def add_observation(self, observation)` - *Fuse a single source response into the cross-run observation log
and bump the source's fetch/ok counters.*
- `fuse_entity` (line 325) `def fuse_entity(self, entity)` - *Fuse one entity into the canonical store and return its id.

The ``(type, normalized)`` pair is the dedup key. On a repeat sighting
the row's ``last_seen``, confidence (Bayesian merge), and observation
count advance, and every contributing source is recorded in
``fusion_entity_sources`` so provenance survives the merge.

Confidence uses the :mod:`reliability_scoring` pipeline: source
reliability, source type hierarchy, and corroboration count are
factored into the score instead of a raw ``MAX()``. A tertiary or
unreliable source cannot override a well-corroborated primary one.*
- `fuse_entities` (line 428) `def fuse_entities(self, entities)` - *Fuse a batch of entities, returning the list of fused ids.*
- `fuse_properties` (line 441) `def fuse_properties(self, eid, parsed, source)` - *Fuse the flat scalar attributes of a parsed observation onto an
entity, attributed to ``source``.

Only one nesting level of scalar values is taken: deep structures are
the observation payload's job, not an entity attribute's. Returns the
number of properties written. The ``(entity_id, key, value, source)``
primary key means re-running the same source is idempotent while a
*different* source asserting the same key/value adds corroboration.*
- `fuse_relationship` (line 487) `def fuse_relationship(self, src_type, src_value, relation, dst_type, dst_value)` - *Fuse one directed edge between two entities, attributed to source.

Both endpoints are resolved to their deterministic fusion ids so the
edge joins the same canonical entities the entity table holds.
Confidence uses the :mod:`reliability_scoring` pipeline instead of a
raw ``MAX()``, so a low-reliability source cannot inflate the score
of a well-corroborated edge.*
- `fuse_graph` (line 557) `def fuse_graph(self, kg)` - *Mirror the analytic edges of a knowledge graph into the store.

Reads node ``type``/``value`` off each endpoint and skips the pure
plumbing relations (``observed_by``, ``co_occurs``, ``mentions``) and
any edge touching a ``source`` node, so only pivot-worthy facts land.
Returns the number of edges fused. Best-effort: a malformed graph is
swallowed rather than aborting a run.*
- `get_entity` (line 593) `def get_entity(self, eid)` - *Return one fused entity with its provenance, properties and edges.*
- `search_entities` (line 639) `def search_entities(self, term, etype)` - *Search fused entities by value substring and/or type.

``min_sources`` filters to entities corroborated by at least N feeds —
the fusion-native "only show me what more than one source agrees on"
query. Ordered by source breadth then recency.*
- `corroborated_properties` (line 682) `def corroborated_properties(self, eid, min_sources)` - *Return an entity's properties that at least ``min_sources`` distinct
feeds independently asserted — the fusion store's confidence signal.*
- `list_sources` (line 699) `def list_sources(self, limit)` - *Return the source catalogue with accumulated fetch/ok counters.*
- `stats` (line 717) `def stats(self)` - *One-glance dashboard of the fused store's size.*
- `close` (line 745) `def close(self)`
- `normalize_value` (line 74) `def normalize_value(etype, value)`
- `_count` (line 720) `def _count(table)`

#### `graph_kuzu.py`
**Path:** `estorides_core/graph_kuzu.py`

**Classes:**
- `KuzuGraphBackend` (line 196) `class KuzuGraphBackend` - *Thread-safe Kuzu wrapper for the Estorides knowledge graph.

The orchestrator calls this alongside the in-memory NetworkX graph.
Writes are synchronous but cheap; reads (Cypher) are also synchronous
and roughly match NetworkX traversal cost for 2-hop queries while
being dramatically faster at cross-run joins.*

**Functions:**
- `_label_for` (line 124) `def _label_for(ent_type)`
- `_node_id` (line 133) `def _node_id(type_, value)` - *Canonical id used as PRIMARY KEY in Kuzu.

Mirrors the in-memory convention in KnowledgeGraph._node_id so a
`Domain:evilcorp.com` row means the same thing in both stores.*

**Methods:**
- `__init__` (line 205) `def __init__(self, path)`
- `_init_schema` (line 233) `def _init_schema(self)`
- `upsert_entity` (line 245) `def upsert_entity(self, ent_type, value, source)` - *Insert (or merge) an entity. Returns its canonical node id.

If `source` is given we also wire an OBSERVED_BY edge so we
can later ask "which sources saw this entity?".*
- `upsert_relationship` (line 295) `def upsert_relationship(self, src_type, src_value, rel, dst_type, dst_value)` - *Insert an edge between two entities.

Unknown relations are silently skipped — every edge type
that matters is mapped in _RELATION_TO_EDGE.*
- `neighbors` (line 346) `def neighbors(self, node_id, hops, relation, limit)` - *Return nodes reachable from `node_id` within `hops` edges.

`relation` optionally filters to a single edge label.
Returns a list of dicts with whatever columns the query names.*
- `cypher` (line 379) `def cypher(self, query, params)` - *Run a Cypher query and return rows as a list of dicts.

Column names are taken from the RETURN clause. Missing
columns (e.g. `m.kind` on a node that was never enriched) come
back as None so callers don't have to special-case.*
- `stats` (line 406) `def stats(self)` - *Return counts of every node label and edge rel type.*
- `close` (line 436) `def close(self)`

#### `hypothesis_engine.py`
**Path:** `estorides_core/hypothesis_engine.py`

**Classes:**
- `EntityRef` (line 54) `class EntityRef` - *A typed reference to an entity involved in a hypothesis.*
- `Evidence` (line 62) `class Evidence` - *One piece of supporting or contradicting evidence.*
- `Hypothesis` (line 73) `class Hypothesis` - *A typed, scored, auditable intelligence conclusion.*
- `HypothesisGenerator` (line 207) `class HypothesisGenerator(Protocol)` - *Strategy: turn a (observations, entities) snapshot into hypotheses.*

**Methods:**
- `_truncate` (line 110) `def _truncate(value)` - *Stringify a value, bounded to ``_VALUE_MAX_CHARS``.*
- `_is_mapping` (line 120) `def _is_mapping(value)`
- `_entity_lookup` (line 124) `def _entity_lookup(entities)` - *Build ``{type: {value, value, ...}}`` from the entity list.

Tolerates both ``Entity`` dataclass instances and plain dicts
(the orchestrator returns both shapes depending on the call site).*
- `_hypothesis_id` (line 145) `def _hypothesis_id(htype, entity_refs, supporting)` - *Deterministic 16-char hex id for a hypothesis.*
- `_score` (line 163) `def _score(supporting, contradicting)` - *Net-support score in (0, 1].

``supporting / (supporting + contradicting + floor)`` — the floor
prevents division by zero and prevents a single weak item from
producing a "1.0 certain" score.*
- `_confidence` (line 177) `def _confidence(supporting, contradicting)` - *Reliability-weighted confidence via :mod:`reliability_scoring`.*
- `_clip_claim` (line 198) `def _clip_claim(template)`
- `_domain_belongsto_actor` (line 217) `def _domain_belongsto_actor(observations, entities)` - *`domain-belongsto-actor`: a domain's WHOIS/issuer/hosting org matches an entity.*
- `_domains_in_obs` (line 309) `def _domains_in_obs(obs)` - *Best-effort: extract domain-like values from a single observation.

The orchestrator doesn't always stamp the queried domain on the
observation, so this is a soft hint. Returns ``[]`` if nothing
looks like a domain.*
- `_email_aliases_person` (line 342) `def _email_aliases_person(observations, entities)` - *`email-aliasto-person`: an email and a person name appear together in one obs.*
- `_extract_email` (line 402) `def _extract_email(parsed)` - *Find a value that looks like an email anywhere in the parsed dict.*
- `_extract_person_name` (line 413) `def _extract_person_name(parsed)` - *Find a value that looks like a person name (has a space, no @, no path).*
- `_ip_shared_infra` (line 424) `def _ip_shared_infra(observations, entities)` - *`ip-shared-infra`: >=2 domains resolve to the same IP.*
- `_extract_ips` (line 505) `def _extract_ips(parsed)` - *Best-effort: pull IPv4-looking values out of a parsed payload.*
- `_looks_like_ipv4` (line 520) `def _looks_like_ipv4(s)`
- `_asn_shared_infra` (line 533) `def _asn_shared_infra(observations, entities)` - *`asn-shared-infra`: >=3 entities of the run live in the same ASN.*
- `_extract_asn` (line 597) `def _extract_asn(parsed)` - *Best-effort: pull an AS-number-ish value out of the parsed payload.*
- `generate_hypotheses` (line 622) `def generate_hypotheses(observations, entities, kg)` - *Generate typed, scored, auditable hypotheses for a run.

Pure: no I/O, no DB writes, no logging, no clock. Same input ⇒
same output bit-by-bit. Hypothesis ids are content hashes so the
fusion store can deduplicate across runs.

Parameters
----------
observations
    Per-source observations from the orchestrator. Each one is
    expected to have at least ``source`` and ``parsed``; the
    generator skips malformed entries without raising.
entities
    The deduplicated entity list from the orchestrator. Each
    item can be a dict (``{"type": ..., "value": ...}``) or an
    ``Entity`` dataclass.
kg
    Optional knowledge graph. Reserved for future generators
    (ego-network, motif-based) — ignored in v1.
min_score
    Floor for the output: hypotheses with score below this are
    dropped. ``[0, 1]``.
max_hypotheses
    Hard cap on the returned list. Top by score.*
- `__call__` (line 210) `def __call__(self, observations, entities)`

#### `intel_resolver.py`
**Path:** `estorides_core/intel_resolver.py`

**Classes:**
- `_TTLCache` (line 120) `class _TTLCache`
- `EntityResolver` (line 156) `class EntityResolver` - *Cross-feed entity resolution.

Composes Wikidata SPARQL, the OFAC SDN index (via the existing
`OntologyEngine.sanctions`), and a couple of free IP-intel
services into a single response shape suitable for both the UI
(entity graph panel) and the orchestrator (knowledge graph
enrichment).*

**Functions:**
- `_run_sparql` (line 90) `def _run_sparql(query)` - *Execute a SPARQL SELECT against the Wikidata endpoint.

Returns the list of result rows. SSRF-guarded via the URL.*
- `_val` (line 111) `def _val(row, key)` - *Pull a string value out of a SPARQL JSON row.*

**Methods:**
- `_norm` (line 789) `def _norm(s)`
- `_is_valid_ipv4` (line 793) `def _is_valid_ipv4(s)`
- `_escape_sparql` (line 801) `def _escape_sparql(s)`
- `__init__` (line 121) `def __init__(self)`
- `get` (line 127) `def get(self, kind, key)`
- `put` (line 140) `def put(self, kind, key, value)`
- `stats` (line 148) `def stats(self)`
- `__init__` (line 165) `def __init__(self)`
- `resolve` (line 174) `def resolve(self, ent_type, ent_id)`
- `_vt_get` (line 214) `def _vt_get(self, path, limit)` - *GET a VirusTotal v3 path, returning parsed JSON or None.

Reads the API key from `VT_API_KEY`; if it is absent the call
is a silent no-op so the resolver degrades cleanly without a
key. SSRF-guarded via the constructed URL.*
- `_vt_add_relationship` (line 245) `def _vt_add_relationship(self, path)` - *Expand one VirusTotal relationship endpoint into nodes/links.

`attr_field` pulls the related value from `attributes` (e.g.
`host_name` for IP resolutions) instead of the raw object id.*
- `_vt_flag_malicious` (line 290) `def _vt_flag_malicious(self, path, node, sources)` - *Stamp a node with VirusTotal detection stats (counter-intel signal).*
- `_resolve_ip` (line 306) `def _resolve_ip(self, ip)`
- `_resolve_domain` (line 412) `def _resolve_domain(self, domain)`
- `_resolve_file` (line 473) `def _resolve_file(self, file_hash)` - *Resolve a file hash via VirusTotal relationships.

Surfaces the network footprint of a sample (contacted IPs and
domains, dropped/bundled files) and stamps the detection count
so a malicious sample lights up the counter-intelligence tier.*
- `_resolve_company` (line 510) `def _resolve_company(self, name)`
- `_resolve_person` (line 569) `def _resolve_person(self, name)`
- `_resolve_country` (line 638) `def _resolve_country(self, name)`
- `_resolve_cve` (line 678) `def _resolve_cve(self, cve_id)`
- `_resolve_btc` (line 750) `def _resolve_btc(self, addr)`
- `_resolve_eth` (line 753) `def _resolve_eth(self, addr)`
- `_resolve_crypto` (line 756) `def _resolve_crypto(self, addr, kind)`

#### `job_registry.py`
**Path:** `estorides_core/job_registry.py`

**Classes:**
- `BoundedJobRegistry` (line 40) `class BoundedJobRegistry` - *A dict-like registry with size and time bounds.

`max_size` and `ttl_seconds` are read at construction and not
mutated — the registry is "configured once, used many times",
which matches how the web app's STREAM config is loaded at
import time.*

**Methods:**
- `__init__` (line 49) `def __init__(self)`
- `register` (line 60) `def register(self, key, value)` - *Insert (or replace) a job, evicting expired and overflow entries.

Returns the value so the caller can use it inline:
    job = registry.register("abc", _RunStreamJob(...))*
- `get` (line 80) `def get(self, key)` - *Return the value for `key` or None. Refreshes the LRU order.*
- `pop` (line 95) `def pop(self, key)` - *Remove and return the value for `key`, or None.*
- `keys` (line 101) `def keys(self)`
- `values` (line 105) `def values(self)`
- `__len__` (line 109) `def __len__(self)`
- `evict_expired` (line 113) `def evict_expired(self)` - *Sweep and drop TTL-expired entries. Returns the number dropped.*
- `_evict_expired_locked` (line 119) `def _evict_expired_locked(self, now)`

#### `knowledge_graph.py`
**Path:** `estorides_core/knowledge_graph.py`

**Classes:**
- `KnowledgeGraph` (line 90) `class KnowledgeGraph`

**Functions:**
- `_node_sources` (line 73) `def _node_sources(node)` - *Read the distinct source set off a node, tolerating GraphML's
JSON-string serialisation of the original Python set/list.*

**Methods:**
- `__init__` (line 91) `def __init__(self, name)`
- `add_entity` (line 97) `def add_entity(self, entity)` - *Insert an entity. Returns the node id used.*
- `add_observation` (line 127) `def add_observation(self, source, entities)` - *Add every entity + every co-occurrence edge within the same response.*
- `add_relationship` (line 142) `def add_relationship(self, src_type, src_value, rel, dst_type, dst_value)`
- `export_graphml` (line 164) `def export_graphml(self, path)`
- `export_json` (line 183) `def export_json(self)`
- `summary` (line 197) `def summary(self)`
- `top_entities` (line 215) `def top_entities(self, n, by)`
- `communities` (line 235) `def communities(self, nodes)` - *Partition entity nodes into communities (clusters).

Runs greedy modularity on the undirected projection, restricted
to `nodes` when given and always excluding `source` nodes (whose
fan-out would otherwise collapse every cluster into one). Returns
a `node_id -> community index` map. Falls back to connected
components when modularity cannot be computed (e.g. no edges).*
- `intel_level` (line 266) `def intel_level(self, node_id, bridge_nodes)` - *Classify a node into the intelligence pipeline tier.

data                  single corroborating source
information           >= 2 distinct sources
intelligence          cross-cluster bridge or resolved relation
counter_intelligence  sanction/threat/VirusTotal-malicious signal

Higher tiers win. `bridge_nodes` is the set of nodes that sit on
an inter-cluster edge (computed once by the caller).*
- `ego_subgraph` (line 311) `def ego_subgraph(self, node_id, radius)`
- `neighbours` (line 322) `def neighbours(self, node_id, relation)`
- `_node_id` (line 338) `def _node_id(self, kind, value)`
- `_source_node` (line 341) `def _source_node(self, source)`
- `_node_color` (line 351) `def _node_color(self, ent_type)`

#### `mitre_attack.py`
**Path:** `estorides_core/mitre_attack.py`

**Functions:**
- `_scan_keywords` (line 156) `def _scan_keywords(text)` - *Scan a text blob for ATT&CK-relevant keywords.*
- `map_observation` (line 170) `def map_observation(observation)` - *Return ATT&CK techniques associated with an observation.

Output:
    {
      "techniques": [
        {"id": "T1595", "label": "Active Scanning", "via": "source:shodan_internetdb"},
        ...
      ],
      "tactic_ids": ["TA0043"],  # not populated yet — future
    }*
- `map_observations` (line 213) `def map_observations(observations)` - *Bulk mapper. Stamps each observation in place with `_mitre` key.

Returns the list of observations (for chaining). Mutates in place
for performance — the orchestrator doesn't keep references to the
pre-mapping list, so a side effect is safe.*
- `all_techniques_for` (line 229) `def all_techniques_for(observations)` - *Aggregate: unique techniques across all observations, sorted by id.*

#### `ontology.py`
**Path:** `estorides_core/ontology.py`

**Classes:**
- `SanctionEntry` (line 70) `class SanctionEntry`
- `SanctionsIndex` (line 96) `class SanctionsIndex` - *In-memory OFAC SDN index with 24h lazy refresh and single-flight load.

The previous design (if any) likely fetched the list on every call
or had no cache; the new design:

  * First call to `entries()` blocks while the CSV is fetched.
  * Subsequent calls within TTL return the cached snapshot.
  * Concurrent calls during a load share the same in-flight
    promise (single-flight) — never two concurrent fetches.
  * If a refresh fails after the cache has gone stale, we keep
    serving the previous snapshot rather than going blind.

The CSV is downloaded over HTTPS to a temp file, then loaded
into a normalised lookup. We never trust the file path in
the SDN_LOCAL_CACHE to be writable: on permission errors we
log a warning and fall back to in-memory only.*
- `WikidataCache` (line 268) `class WikidataCache` - *Bounded LRU cache for Wikidata SPARQL queries.

Keyed by `(query_kind, normalised_value)`. Values are `(fetched_at, payload)`.
Exposes `lookup_label(label)` and `lookup_org(label)` — the two
most common lookups in OSINT workflows.*
- `OntologyEngine` (line 314) `class OntologyEngine` - *Public façade. Hands out the sanction index and wikidata cache.*

**Methods:**
- `_normalise_name` (line 84) `def _normalise_name(s)` - *Lower-case, strip punctuation/diacritics, collapse whitespace.

Used for both index keys and incoming query normalisation so the
same string yields the same key on both sides.*
- `to_dict` (line 79) `def to_dict(self)`
- `__init__` (line 115) `def __init__(self)`
- `is_ready` (line 131) `def is_ready(self)`
- `entries` (line 134) `def entries(self)` - *Return the current snapshot, loading if necessary.*
- `lookup` (line 141) `def lookup(self, name)` - *Find sanction entries whose name or alias matches `name`.*
- `lookup_crypto` (line 151) `def lookup_crypto(self, address)` - *Cross-check a BTC/ETH address against the SDN list.

The OpenSanctions CSV includes a `crypto_address` (BTC) field
on a subset of entries. ETH addresses are stored in the
`ethereum_address` field. The current implementation matches
by alias string for simplicity — the upstream coverage of
crypto is sparse and not the focus of this version. Returns
the entries whose alias list contains the literal address.*
- `size` (line 168) `def size(self)`
- `_refresh` (line 172) `def _refresh(self)`
- `_download` (line 201) `def _download(self)`
- `_persist` (line 213) `def _persist(self, text)` - *Best-effort write of the raw CSV for offline re-use.

Failures are non-fatal; the in-memory index is the source of
truth while the process is alive.*
- `_parse` (line 226) `def _parse(self, text)` - *Parse the OpenSanctions simple CSV into SanctionEntry records.*
- `_index` (line 255) `def _index(self, entries)` - *Build a normalised-name → entries lookup.*
- `__init__` (line 276) `def __init__(self)`
- `get` (line 282) `def get(self, kind, value)`
- `put` (line 296) `def put(self, kind, value, payload)`
- `stats` (line 304) `def stats(self)`
- `clear` (line 308) `def clear(self)`
- `__init__` (line 317) `def __init__(self)`
- `check_observation` (line 321) `def check_observation(self, observation)` - *Run a single observation through the ontology.

Returns a dict describing the sanctions verdict:

  {
    "sanctioned": bool,
    "hits": [SanctionEntry.to_dict(), ...],
    "fields": ["registrant_name", "isp", ...]  # which fields matched
  }

The orchestrator attaches this to each observation before the
LLM analyst stage so the system prompt can include a verdict
line ("SANCTIONED — OFAC SDN match on registrant").*
- `_candidate_fields` (line 359) `def _candidate_fields(source, parsed)` - *Return (field_name, value) pairs to check against sanctions.

Different sources expose different field names. Rather than
a giant if/elif, this is a small dispatch table — adding a
new source is a one-line edit.*

#### `orchestrator.py`
**Path:** `estorides_core/orchestrator.py`

**Classes:**
- `Orchestrator` (line 132) `class Orchestrator`

**Functions:**
- `_safe_format` (line 100) `def _safe_format(template)` - *Format a string template with {key} placeholders.

Non-string values (int, list, dict) are returned as-is so YAMLs that
use raw integers or list literals in params/body don't blow up.*
- `_resolve_auth` (line 112) `def _resolve_auth(source)` - *Look up the API key for a source that needs one.*
- `_domain_from_query` (line 122) `def _domain_from_query(q)` - *Heuristic: if the query looks like a domain, return it; if it's an IP, return None.*

**Methods:**
- `repl` (line 107) `def repl(m)`
- `__init__` (line 133) `def __init__(self)`
- `run` (line 148) `def run(self, query)` - *Run a full intelligence cycle. Returns a structured result.

`deadline` is a hard wall-clock cap (seconds) for the whole fanout.
Any source that hasn't responded by then is dropped and reported as
"deadline_exceeded" so the run can never get stuck.

`persist` (default True) writes the run to the persistent case
store and mirrors every entity/edge to the Kùzu graph. Set
False for one-off ad-hoc queries (e.g. tests) where you don't
want the run to bloat the long-term memory.

`case_id`, when supplied, makes this run append to an existing
case instead of opening a new one. The recursive pivot engine
uses this so every hop of a cross-search lands in a single case.

`on_source_result`, when supplied, is invoked with the shaped
observation dict the moment each source resolves, before the
fan-out as a whole completes. This is what lets the UI populate
progressively instead of blocking on the slowest source.

`passive_only` (default False) restricts the fan-out to sources
whose contact class is `none` — the target's own infrastructure is
never touched, not even by a third-party broker probe. Use this for
bug-bounty scoping where a probe attributable to the operator's
recon window must not appear in the target's logs.

`proxy`, when supplied (e.g. `socks5://127.0.0.1:9050` for Tor),
routes every outbound request through it so the queried brokers
never see the operator's real egress IP. Falls back to the
env-configured proxy pool when omitted.*
- `_select_sources` (line 619) `def _select_sources(self, names)`
- `_execute_source` (line 652) `def _execute_source(self, client, source, query, on_done, on_result)`
- `_extract_cursor` (line 757) `def _extract_cursor(data, cfg)` - *Extract the next-page cursor from a parsed response body.*
- `_infer_relationships` (line 762) `def _infer_relationships(self, observations, query)` - *Delegate each observation to its registered inferer.

The previous version of this method was a 90-line `if/elif`
chain hard-coded to specific source names. The new version
walks the inferer registry; sources with no inferer are
silently skipped. Adding a new inferer is now: write a
function and `@register_inferer("source_name")` it. No edits
to this method.*
- `_write_dataset` (line 775) `def _write_dataset(self, query, observations, entities, analysis)`

#### `osiris_sources.py`
**Path:** `estorides_core/osiris_sources.py`

**Functions:**
- `_cached_get` (line 81) `def _cached_get(url)` - *GET with a small on-disk JSON cache. Returns parsed JSON or None.

Used for the slow-changing feeds (CISA KEV, malware lists) so a
burst of operator clicks doesn't hammer the upstream.*
- `fetch_bgp` (line 119) `def fetch_bgp(query)` - *Look up an IP or AS number against bgpview.io (free, no key).*
- `fetch_mac` (line 185) `def fetch_mac(mac)` - *Look up a MAC address against macvendors.co (free, no key).*
- `fetch_phone` (line 233) `def fetch_phone(number)` - *Best-effort phone geolocation.

The implementation is intentionally simple (regex + region
table). It does NOT replace libphonenumber; it provides a
same-shape response without the dep so the API stays consistent
with Osiris' /api/osint/phone.*
- `fetch_github_user` (line 302) `def fetch_github_user(username)` - *Look up a GitHub user (keyless, rate-limited).*
- `fetch_leaks` (line 356) `def fetch_leaks(email)` - *Breach analytics for `email` via xposedornot (free, no key).*
- `fetch_cisa_kev` (line 400) `def fetch_cisa_kev(limit, days)` - *Recently-added CVEs from the CISA KEV feed (authoritative).*
- `fetch_malware_c2` (line 452) `def fetch_malware_c2(limit)` - *Active botnet C2 (Feodo) + recent malware URLs (URLhaus).

Both abuse.ch, both keyless. Each entry is geolocated against the
country centroid table with deterministic jitter so multiple
threats in the same country don't stack on the same pixel.*

#### `pagination.py`
**Path:** `estorides_core/pagination.py`

**Classes:**
- `PaginationConfig` (line 19) `class PaginationConfig` - *Configuration for a paginated source fetch.

Parsed from the source YAML's ``pagination`` key. No fields are
required; a source with no pagination config results in a single
fetch (the current default behaviour).*

**Methods:**
- `build_page_params` (line 62) `def build_page_params(cfg, page_num)` - *Build URL params dict for a given page number.

Returns an empty dict for cursor strategy (the cursor is set
dynamically from the response) or when pagination is disabled.*
- `extract_cursor` (line 78) `def extract_cursor(data, cfg)` - *Extract the next-page cursor from a parsed response body.

Walks the dot-separated ``cursor_path`` into the JSON-like dict.
Returns ``None`` when the path is absent or the value is empty.*
- `count_results` (line 99) `def count_results(data, cfg)` - *Count results in a parsed response page.

Uses ``response_list_path`` if configured, otherwise tries common
JSON fields (``results``, ``items``, ``data``) or falls back to
``len(data)`` for a list-type response.*
- `from_dict` (line 38) `def from_dict(raw)`
- `enabled` (line 54) `def enabled(self)`
- `needs_page_size` (line 58) `def needs_page_size(self)`

#### `parsers.py`
**Path:** `estorides_core/parsers.py`

**Functions:**
- `_flat` (line 30) `def _flat(obj)` - *Recursively flatten a dict/list into a list of leaf values.*
- `_first` (line 44) `def _first(obj)` - *Recursively dig into a JSON-ish structure to find the first matching key.*
- `parse_dns_json` (line 62) `def parse_dns_json(payload)` - *Google/Cloudflare DNS-over-HTTPS response.*
- `parse_crtsh_json` (line 77) `def parse_crtsh_json(payload)` - *crt.sh CT log response.*
- `parse_rdap` (line 95) `def parse_rdap(payload)` - *RDAP (RFC 7483) domain object.

Returns a flat dict with registrar, registry handle, status flags,
event dates, and any nameserver / entity hints. The structured
result feeds two goals:

  1. Surface the registrar as an `entity` so the resolver can
     later ask "which other domains does MarkMonitor manage"
     (or whichever registrar came back) and fan out into the
     shared-infrastructure lane.
  2. Save the create / expire / updated dates so the timeline
     view can render them without a second pass.

Defensive against missing fields — RDAP responses vary across
registries and the spec allows a lot of optional bits.*
- `parse_ipapi` (line 170) `def parse_ipapi(payload)` - *ip-api.com response.*
- `parse_ipinfo` (line 196) `def parse_ipinfo(payload)`
- `parse_ipapi_co` (line 211) `def parse_ipapi_co(payload)`
- `parse_shodan_internetdb` (line 220) `def parse_shodan_internetdb(payload)` - *internetdb.shodan.io — IP service summary.*
- `parse_greynoise` (line 234) `def parse_greynoise(payload)`
- `parse_ipwhois` (line 249) `def parse_ipwhois(payload)`
- `parse_abuseipdb` (line 267) `def parse_abuseipdb(payload)`
- `_vt_stats` (line 283) `def _vt_stats(attrs)` - *Flatten VirusTotal v3 last_analysis_stats into a compact dict.*
- `parse_vt_ip` (line 297) `def parse_vt_ip(payload)` - *VirusTotal v3 — IP address object.*
- `parse_vt_domain` (line 318) `def parse_vt_domain(payload)` - *VirusTotal v3 — domain object.*
- `parse_vt_file` (line 345) `def parse_vt_file(payload)` - *VirusTotal v3 — file object.*
- `parse_ripe_stat` (line 369) `def parse_ripe_stat(payload)`
- `parse_nominatim` (line 380) `def parse_nominatim(payload)`
- `parse_urlscan` (line 398) `def parse_urlscan(payload)`
- `parse_wayback_cdx` (line 420) `def parse_wayback_cdx(payload)` - *CDX returns a list where the first row is the header.*
- `parse_wayback_avail` (line 433) `def parse_wayback_avail(payload)`
- `parse_threatfox` (line 442) `def parse_threatfox(payload)`
- `parse_urlhaus` (line 451) `def parse_urlhaus(payload)`
- `parse_urlhaus_payloads` (line 460) `def parse_urlhaus_payloads(payload)`
- `parse_malwarebazaar` (line 469) `def parse_malwarebazaar(payload)`
- `parse_otx` (line 478) `def parse_otx(payload)`
- `parse_hibp_breach` (line 502) `def parse_hibp_breach(payload)`
- `parse_hibp_paste` (line 520) `def parse_hibp_paste(payload)`
- `parse_phonebook` (line 536) `def parse_phonebook(payload)`
- `parse_wikipedia` (line 557) `def parse_wikipedia(payload)`
- `parse_wikidata` (line 566) `def parse_wikidata(payload)`
- `parse_openalex` (line 578) `def parse_openalex(payload)`
- `parse_crossref` (line 598) `def parse_crossref(payload)`
- `parse_arxiv` (line 618) `def parse_arxiv(payload)` - *arXiv returns Atom XML; we expect callers to have converted to a dict.*
- `parse_nvd_cve` (line 639) `def parse_nvd_cve(payload)`
- `parse_github_advisories` (line 661) `def parse_github_advisories(payload)`
- `parse_blockchain_btc` (line 685) `def parse_blockchain_btc(payload)`
- `parse_blockstream` (line 701) `def parse_blockstream(payload)`
- `parse_ethplorer` (line 717) `def parse_ethplorer(payload)`
- `parse_microlink` (line 733) `def parse_microlink(payload)`
- `parse_github_user` (line 753) `def parse_github_user(payload)`
- `parse_github_search` (line 773) `def parse_github_search(payload)`
- `parse_reddit` (line 788) `def parse_reddit(payload)`
- `parse_mastodon` (line 818) `def parse_mastodon(payload)`
- `parse_keybase` (line 834) `def parse_keybase(payload)`
- `parse_hackernews` (line 858) `def parse_hackernews(payload)`
- `parse_reddit_search` (line 870) `def parse_reddit_search(payload)`
- `parse_dev_to` (line 884) `def parse_dev_to(payload)`
- `parse_text_lines` (line 899) `def parse_text_lines(payload)` - *Generic: split raw_text by newlines, drop empties.*
- `parse_raw_text` (line 910) `def parse_raw_text(payload)`
- `parse_http_headers` (line 918) `def parse_http_headers(payload)` - *hackertarget returns text; expect a one-line-per-header response.*
- `parse_whois_text` (line 934) `def parse_whois_text(payload)`
- `get_parser` (line 1024) `def get_parser(name)` - *Return the parser function for `name`, or a passthrough lambda.

Unknown parser names deliberately fall through to `parse_raw_text`
so a source YAML with a typo in the `parser` field never crashes
the run — it just produces a less-structured observation.*
- `register_parser` (line 1037) `def register_parser(name, description)` - *Decorator: register `func` as a parser under `name`.

Used by addon authors and tests to extend the catalog without
touching the central `PARSERS` dict. Idempotent: re-registering
the same name overwrites the previous entry, with a debug log so
a typo doesn't silently drop a parser.*
- `list_parsers` (line 1053) `def list_parsers()` - *Return (name, description) tuples for every registered parser.

Used by the CLI `status` endpoint to advertise the available
parser names, and by tests to assert that a custom parser made it
into the registry.*
- `deco` (line 1045) `def deco(func)`

#### `pivot_engine.py`
**Path:** `estorides_core/pivot_engine.py`

**Classes:**
- `PivotEvent` (line 47) `class PivotEvent` - *A single, transport-neutral progress event.

`type` is a stable vocabulary token; `data` is a JSON-serialisable
payload. Sinks translate these to their own wire format.*
- `EventSink` (line 59) `class EventSink(Protocol)` - *Receives engine progress events. Implementations must not raise.*
- `ListEventSink` (line 67) `class ListEventSink` - *In-memory sink. Useful for tests and synchronous embedding.*
- `BufferedEventSink` (line 77) `class BufferedEventSink` - *Bounded sink that flattens events to JSON-ready dicts for SSE drain.

Each stored item is `{"type": ..., "ts": ..., **data}`. When the buffer
exceeds `capacity` the oldest items are dropped and a `heartbeat` marker
records how many were lost, so a slow client degrades gracefully instead
of stalling the producer. The terminal `finished`/`fatal` event also
flips `done` so a poller knows when to stop without parsing payloads.*
- `EntityRunner` (line 113) `class EntityRunner(Protocol)` - *Runs the OSINT fan-out for a single target.

The engine depends on this narrow port rather than the concrete
Orchestrator, so it can be driven by a stub in tests.*
- `PivotBudget` (line 139) `class PivotBudget` - *Mutable accounting for one cross-search.

Holds the three hard ceilings (steps, entities, wall-clock) and the
monotonic clock the deadline is measured against. `exhausted()` returns
a human reason string the moment any ceiling is hit, else None.*
- `PivotLead` (line 172) `class PivotLead` - *A target waiting in the frontier.*
- `PivotResult` (line 184) `class PivotResult` - *Terminal summary of a completed cross-search.*
- `PivotEngine` (line 195) `class PivotEngine` - *Drives the recursive, scored, asynchronous cross-search.*

**Methods:**
- `emit` (line 62) `def emit(self, event)` - *Publish one event. A slow or failing sink must never break a run.*
- `__init__` (line 70) `def __init__(self)`
- `emit` (line 73) `def emit(self, event)`
- `__init__` (line 87) `def __init__(self, capacity)`
- `emit` (line 94) `def emit(self, event)`
- `run` (line 120) `def run(self, query)`
- `time_left` (line 155) `def time_left(self)` - *Seconds remaining before the global wall-clock deadline.*
- `exhausted` (line 159) `def exhausted(self)` - *Reason the run must stop, or None while budget remains.*
- `__init__` (line 198) `def __init__(self, runner, sink)`
- `_emit` (line 246) `def _emit(self, event_type)` - *Build and publish an event, swallowing any sink failure.*
- `_heap_push` (line 255) `def _heap_push(heap, counter, lead)` - *Push a lead as a max-heap by score (negated for heapq).*
- `run` (line 264) `def run(self, seed_type, seed_value)` - *Execute the cross-search from `(seed_type, seed_value)`.

Returns a `PivotResult`. Progress is published incrementally
through the injected sink while the coroutine is in flight.*
- `_expand_lead` (line 341) `def _expand_lead(self, lead, frontier, budget)` - *Run the fan-out for one lead and enqueue its scored children.*
- `_ingest_children` (line 411) `def _ingest_children(self, parent, result, frontier, budget)` - *Score the entities a target produced and enqueue the best ones.

Returns the number of leads actually added to the frontier. The
per-step breadth cap keeps a single popular target (a CDN, a
registrar) from flooding the queue.*
- `_on_source_done` (line 356) `def _on_source_done(name, ok, status, elapsed_ms)`
- `_on_source_result` (line 366) `def _on_source_result(observation)`

#### `recon_fusion.py`
**Path:** `estorides_core/recon_fusion.py`

**Classes:**
- `RelevanceTier` (line 24) `class RelevanceTier(str, Enum)` - *Relevance classification for grouped reconnaissance results.

Ordered from most to least relevant for UI rendering.*
- `GroupedEntity` (line 43) `class GroupedEntity` - *One canonical entity grouped across all sources that observed it.*
- `FusionResult` (line 81) `class FusionResult` - *Complete output of the recon fusion engine.*
- `ReconFusionEngine` (line 177) `class ReconFusionEngine` - *Stateless engine that classifies raw OSINT results into relevance tiers.

Thread-safe (no mutable state). Reusable across requests.*

**Methods:**
- `_normalize_value` (line 104) `def _normalize_value(etype, value)` - *Deterministic normalisation matching fusion_store.entity_id.*
- `_canonical_id` (line 109) `def _canonical_id(etype, value)` - *Deterministic sha1-based entity id matching fusion_store convention.*
- `_reliability_weight` (line 115) `def _reliability_weight(source_name, overrides)` - *Map a source name to its numeric reliability weight.

Uses overrides first, then the curated reliability_scoring map.
Returns 0.7 (C, fairly reliable) as default for unknown sources.*
- `_corroboration_factor` (line 134) `def _corroboration_factor(source_count)` - *Logarithmic corroboration weight: min(1, log10(1 + n)).*
- `_freshness_factor` (line 141) `def _freshness_factor(age_hours, max_hours)` - *Linear freshness decay from 1.0 (fresh) to 0.1 (stale).*
- `_direct_match_query` (line 149) `def _direct_match_query(value, query)` - *True if the entity value matches the original query.*
- `_extract_key_findings` (line 154) `def _extract_key_findings(observations)` - *Extract textual key findings from a list of observations.*
- `_reliability_weight_for_letter` (line 443) `def _reliability_weight_for_letter(letter)` - *Convert a reliability letter (A-F) to its numeric weight.*
- `ordered` (line 37) `def ordered(cls)` - *Return tiers in canonical display order.*
- `to_dict` (line 61) `def to_dict(self)`
- `to_dict` (line 92) `def to_dict(self)`
- `__init__` (line 183) `def __init__(self, config)`
- `classify` (line 186) `def classify(self, query, query_type, observations, entities)` - *Classify raw observations and entities into relevance-tiered groups.

Args:
    query: The original operator query (non-empty).
    query_type: Detected type of the query.
    observations: Raw observation dicts from the orchestrator.
    entities: Raw entity dicts from entity extraction.

Returns:
    FusionResult with tiered, grouped, deduplicated results.

Raises:
    ValueError: If query is empty.*
- `_deduplicate` (line 236) `def _deduplicate(self, observations)` - *Remove exact duplicates based on config dedup keys.

Two observations are identical if they share the same values for all
exact_dedup_keys. The first occurrence is kept.*
- `_group_by_entity` (line 254) `def _group_by_entity(self, observations, entities)` - *Group observations and entities by canonical entity id.

Primary grouping key is the explicit entity list. Observations are
attached to groups when the entity value appears in the observation's
parsed data or the observation source matches the entity's sources.*
- `_classify_groups` (line 338) `def _classify_groups(self, groups, query)` - *Assign each group a relevance tier and score.*
- `_assign_tier` (line 403) `def _assign_tier(self, source_count, avg_reliability, direct_match)` - *Determine the relevance tier based on source count and reliability.

Thresholds:
    CRITICAL: source_count >= critical_min_sources (3) OR
              (source_count >= 2 AND avg_reliability >= B weight)
    HIGH:     source_count >= high_min_sources (2) OR
              (source_count >= 1 AND avg_reliability >= high_min_reliability AND direct_match)
    MEDIUM:   source_count >= 1 AND avg_reliability > noise threshold
    LOW:      source_count >= 1 AND avg_reliability <= noise threshold
    NOISE:    source_count >= 1 AND avg_reliability <= F weight
              OR no corroboration from untrusted source*

#### `relationship_inference.py`
**Path:** `estorides_core/relationship_inference.py`

**Classes:**
- `RelationshipInferer` (line 36) `class RelationshipInferer(Protocol)` - *Translate a single observation into one or more knowledge-graph edges.

Args:
    observation: the structured observation dict produced by the
        orchestrator. Has keys: source, category, parsed, raw, meta.
    query: the user's original query string. Useful for edges that
        connect a finding back to the pivot (e.g. "domain X
        resolved to IP Y for query X").
    kg: the KnowledgeGraph to mutate. The inferer adds nodes and
        edges via the existing `add_relationship()` API.

Returns:
    None. Side effects only: writes to the knowledge graph.*

**Methods:**
- `register_inferer` (line 63) `def register_inferer(source_name)` - *Decorator: register `func` as the inferer for `source_name`.

Re-registration is a debug log + overwrite; the orchestrator picks
the LAST registered inferer for a given source name, so a test
can monkey-patch an inferer without monkey-patching the source.*
- `infer_relationship` (line 78) `def infer_relationship(observation, query, kg)` - *Dispatch an observation to its inferer (if any).

Returns True if an inferer ran, False otherwise. An inferer that
raises is logged at WARNING and returns False; the orchestrator
keeps going so one bad source doesn't poison the whole run.*
- `_infer_dns` (line 105) `def _infer_dns(observation, query, kg)`
- `_infer_crtsh` (line 114) `def _infer_crtsh(observation, query, kg)`
- `_infer_shodan` (line 122) `def _infer_shodan(observation, query, kg)`
- `_infer_greynoise` (line 134) `def _infer_greynoise(observation, query, kg)`
- `_infer_abuseipdb` (line 143) `def _infer_abuseipdb(observation, query, kg)`
- `_infer_whois` (line 152) `def _infer_whois(observation, query, kg)`
- `_infer_urlscan` (line 163) `def _infer_urlscan(observation, query, kg)`
- `_infer_phonebook` (line 175) `def _infer_phonebook(observation, query, kg)`
- `_infer_ipapi` (line 186) `def _infer_ipapi(observation, query, kg)`
- `_infer_otx` (line 195) `def _infer_otx(observation, query, kg)`
- `_infer_nvd` (line 208) `def _infer_nvd(observation, query, kg)`
- `__call__` (line 51) `def __call__(self, observation, query, kg)`
- `deco` (line 70) `def deco(func)`

#### `reliability_scoring.py`
**Path:** `estorides_core/reliability_scoring.py`

**Classes:**
- `SourceReliability` (line 36) `class SourceReliability(str, Enum)` - *NATO Admiralty source-reliability rating (A-F).*
- `Credibility` (line 47) `class Credibility(int, Enum)` - *NATO Admiralty information-credibility rating (1-6).*
- `SourceType` (line 58) `class SourceType(str, Enum)` - *Source type hierarchy: primary > secondary > tertiary.

Orthogonal to NATO reliability: a primary source (official WHOIS) and a
secondary source (social media) can both be rated A, but the primary
contributes more weight because it is institutionally closer to the truth.*
- `ConfidenceInput` (line 199) `class ConfidenceInput` - *Validated input to :func:`compute_confidence`.*
- `ConfidenceResult` (line 219) `class ConfidenceResult` - *Auditable output of :func:`compute_confidence` / :func:`merge_confidence`.*

**Methods:**
- `_corroboration_weight` (line 236) `def _corroboration_weight(n)` - *``min(1, log10(1 + n))``.  0 sources → 0; 1 → 0.30; 9 → 1.0.*
- `_freshness_weight` (line 243) `def _freshness_weight(age_seconds, half_life_days)` - *Exponential decay.  age=0 → 1.0; one half-life → 0.5.*
- `_validate_score` (line 253) `def _validate_score(value, field_name)`
- `_clamp01` (line 258) `def _clamp01(value)` - *Clamp to the closed unit interval.*
- `compute_confidence` (line 268) `def compute_confidence(inp)` - *Compute the audit-trailed confidence score for one observation.

Pure: no I/O, no logging, no clock. Identical input identical output
bit-by-bit. Bounded to [0, 1]. The formula is:

    score = base * reliability_weight * credibility_weight
          * source_type_weight * corroboration_weight * freshness_weight*
- `merge_confidence` (line 306) `def merge_confidence(existing, new_observation)` - *Merge a new observation's confidence into an existing entity score.

The result is ``max(existing, new_score)`` clamped to ``[0, 1]``. An
unreliable new observation cannot raise a strongly-corroborated
existing one; a reliable new observation can lift a weakly-attested
one. The :class:`ConfidenceResult` exposes the weights of the *new*
observation so the audit trail is intact.*
- `reliability_from_name` (line 356) `def reliability_from_name(source_name)` - *Look up the reliability for a source by name; never raises.

Operator input is potentially adversarial. We do not log, do not
validate beyond ``lower().strip()``, and never raise. Unknown names
fall back to :data:`DEFAULT_RELIABILITY`.*
- `source_type_from_name` (line 371) `def source_type_from_name(source_name)` - *Look up the source type hierarchy for a source by name; never raises.

Operator input is potentially adversarial. Same contract as
:func:`reliability_from_name`: no logging, no raising, no ReDoS.
Unknown names fall back to :data:`DEFAULT_SOURCE_TYPE` (TERTIARY).*
- `__post_init__` (line 209) `def __post_init__(self)`

#### `scope.py`
**Path:** `estorides_core/scope.py`

**Classes:**
- `ScopeRule` (line 89) `class ScopeRule(ABC)` - *A single scope predicate. Implementations match exactly one grammar.*
- `WildcardRule` (line 102) `class WildcardRule(ScopeRule)` - *`*.example.com` — the apex and any subdomain of it.*
- `ExactHostRule` (line 117) `class ExactHostRule(ScopeRule)` - *A single fully-qualified host, matched verbatim.*
- `CidrRule` (line 130) `class CidrRule(ScopeRule)` - *An IPv4/IPv6 network; matches any address inside it.*
- `RegexRule` (line 148) `class RegexRule(ScopeRule)` - *A compiled regex matched against the raw normalised asset.*
- `ScopeMatcher` (line 234) `class ScopeMatcher` - *Classifies assets against in-scope and out-of-scope rule sets.

Out-of-scope is evaluated first and wins outright, so an asset that
matches both a broad in-scope wildcard and a narrow out-of-scope rule
is reported as out-of-scope.*
- `ScopeReport` (line 344) `class ScopeReport` - *Classified assets plus the flat lists an operator pipes onward.*

**Functions:**
- `normalise_asset` (line 52) `def normalise_asset(raw)` - *Reduce a raw asset string to a comparable host or IP literal.

Strips an optional scheme, any path/query, a port, surrounding
whitespace and a trailing dot, and lowercases the result. A value that
is already a bare host or IP passes through unchanged (bar casing).*
- `is_ip` (line 79) `def is_ip(asset)` - *True when `asset` parses as a bare IPv4 or IPv6 address.*

**Methods:**
- `_wildcard_factory` (line 161) `def _wildcard_factory(text)`
- `_regex_factory` (line 168) `def _regex_factory(text)`
- `_cidr_factory` (line 179) `def _cidr_factory(text)`
- `_ip_factory` (line 188) `def _ip_factory(text)`
- `_exact_host_factory` (line 195) `def _exact_host_factory(text)`
- `parse_rule` (line 211) `def parse_rule(line)` - *Parse one rule line into a ScopeRule, or None for blank/comment/invalid.*
- `parse_rules` (line 223) `def parse_rules(lines)` - *Parse many rule lines, skipping blanks, comments and invalid entries.*
- `load_rules_file` (line 285) `def load_rules_file(path)` - *Build a matcher from a rules file, honouring the out-of-scope divider.

Lines above a ``## out-of-scope`` divider (case-insensitive) are
in-scope; lines below are out-of-scope. A file with no divider is all
in-scope.*
- `load_assets` (line 303) `def load_assets(path)` - *Read assets from a file: a discover surface JSON or a flat host list.

A JSON document is mined for assets in `domains`, `entities` (values of
host/ip types) and any top-level list of strings. Anything else is read
as one asset per line.*
- `_assets_from_json` (line 322) `def _assets_from_json(doc)` - *Extract candidate assets from a parsed discover/result JSON document.*
- `build_report` (line 371) `def build_report(matcher, assets)` - *Classify `assets` with `matcher` and return a :class:`ScopeReport`.*
- `write_flat_lists` (line 381) `def write_flat_lists(report, out_dir)` - *Write newline-delimited flat lists for piping into active tooling.

Produces `in_scope_hosts.txt`, `in_scope_ips.txt` and `unknown.txt`
under `out_dir`. Returns the map of label to written path.*
- `matches` (line 93) `def matches(self, asset)` - *True when `asset` (already normalised) is covered by this rule.*
- `describe` (line 97) `def describe(self)` - *Human-readable form of the rule, for reports and audit.*
- `matches` (line 107) `def matches(self, asset)`
- `describe` (line 112) `def describe(self)`
- `matches` (line 122) `def matches(self, asset)`
- `describe` (line 125) `def describe(self)`
- `matches` (line 135) `def matches(self, asset)`
- `describe` (line 143) `def describe(self)`
- `matches` (line 153) `def matches(self, asset)`
- `describe` (line 156) `def describe(self)`
- `__init__` (line 242) `def __init__(self, in_scope, out_of_scope)`
- `in_rules` (line 251) `def in_rules(self)`
- `out_rules` (line 255) `def out_rules(self)`
- `classify` (line 258) `def classify(self, raw_asset)` - *Return IN_SCOPE, OUT_OF_SCOPE or UNKNOWN for a single asset.*
- `partition` (line 269) `def partition(self, assets)` - *Bucket many assets, returning sorted, de-duplicated lists.

Keys are IN_SCOPE, OUT_OF_SCOPE and UNKNOWN. De-duplication is on
the normalised form so `HTTPS://Example.com/` and `example.com`
collapse to one entry.*
- `hosts` (line 352) `def hosts(self)` - *In-scope hostnames (everything in-scope that is not an IP).*
- `ips` (line 357) `def ips(self)` - *In-scope bare IP addresses.*
- `to_dict` (line 361) `def to_dict(self)`

#### `search_telemetry.py`
**Path:** `estorides_core/search_telemetry.py`

**Classes:**
- `SearchTelemetryError` (line 37) `class SearchTelemetryError(Exception)` - *Base class for every error raised by this module.*
- `UnknownPhaseError` (line 41) `class UnknownPhaseError(SearchTelemetryError, KeyError)` - *Raised when a phase key is not part of the configured vocabulary.*
- `InvalidTelemetryConfigError` (line 45) `class InvalidTelemetryConfigError(SearchTelemetryError, ValueError)` - *Raised when a :class:`TelemetryConfig` violates a construction rule.*
- `KeyboardShortcut` (line 117) `class KeyboardShortcut` - *A single keyboard shortcut: the key chord and what it does.*
- `SplashTip` (line 125) `class SplashTip` - *A single onboarding tip: a short title and a one-line body.*
- `SearchPhase` (line 133) `class SearchPhase` - *A search lifecycle phase: a stable key, a human label and activity flag.

``active`` is ``True`` while work is in flight (the UI shows a spinner) and
``False`` for the resting states ``idle``, ``done`` and ``error``.*
- `ProgressView` (line 146) `class ProgressView` - *Immutable, render-ready snapshot of search progress.

Carries the clamped counters, the percentage, the human label and the ARIA
attributes a screen reader needs to announce a live progress region.*
- `TelemetryConfig` (line 177) `class TelemetryConfig` - *Frozen catalog: brand, tagline, shortcuts, tips and phase vocabulary.

``__post_init__`` enforces every invariant in spec/search_telemetry.md so an
invalid catalog can never reach the UI. All construction failures raise
:class:`InvalidTelemetryConfigError`.*
- `SearchTelemetry` (line 217) `class SearchTelemetry` - *Service over a :class:`TelemetryConfig`: progress math and catalog views.

Stateless and side-effect free; safe to instantiate or share per request.*

**Methods:**
- `disallowed_brands_in` (line 75) `def disallowed_brands_in(text)` - *Return the third-party brand tokens found in ``text``.

Matching is case-insensitive and word-boundary aware so an ordinary word
that merely contains a brand as a substring does not produce a false
positive. The returned tuple holds the canonical lowercase brand names in
first-seen order, de-duplicated.*
- `emoji_in` (line 89) `def emoji_in(text)` - *Return the emoji glyphs found in ``text``, de-duplicated in order.

Emoji are codepoints in the pictographic blocks (Miscellaneous Symbols,
Dingbats, regional indicators, the supplementary pictographic planes) and
the emoji variation selector. Geometric line-symbols outside those blocks
are permitted iconography and are not flagged.*
- `percent_encoded_emoji_in` (line 103) `def percent_encoded_emoji_in(text)` - *Return percent-encoded supplementary-plane emoji sequences in ``text``.

Catches an emoji smuggled into a ``data:`` URI (for example an emoji
favicon) as the UTF-8 lead bytes ``%F0%9F`` followed by two continuation
bytes. The returned tuple holds the matched sequences in first-seen order.*
- `_assert_clean` (line 167) `def _assert_clean(label)` - *Raise :class:`InvalidTelemetryConfigError` if any text leaks brand/emoji.*
- `_default_config` (line 309) `def _default_config()` - *Build the canonical Estorides telemetry catalog.*
- `__post_init__` (line 191) `def __post_init__(self)`
- `__init__` (line 223) `def __init__(self, config)`
- `shortcuts` (line 229) `def shortcuts(self)` - *Return the keyboard-shortcut catalog.*
- `tips` (line 233) `def tips(self)` - *Return the onboarding tips catalog.*
- `phases` (line 237) `def phases(self)` - *Return the search-phase vocabulary.*
- `phase` (line 241) `def phase(self, key)` - *Return the phase for ``key`` or raise :class:`UnknownPhaseError`.*
- `progress` (line 249) `def progress(self, completed, total, phase_key)` - *Compute a clamped, render-ready :class:`ProgressView`.

Out-of-range counters are clamped, never rejected; only an unknown
``phase_key`` raises (:class:`UnknownPhaseError`). When ``total`` is not
yet known (``<= 0``) and the phase is active the view is indeterminate.*
- `context` (line 288) `def context(self)` - *Return the JSON-serialisable catalog for template/JS injection.*

#### `source_health_monitoring.py`
**Path:** `estorides_core/source_health_monitoring.py`

**Classes:**
- `SourceHealthStatus` (line 53) `class SourceHealthStatus(str, Enum)` - *Operational health classification for an OSINT source.*
- `SourceHealthConfig` (line 64) `class SourceHealthConfig` - *Thresholds for source health classification.

Every field has a corresponding ``ESTORIDES_HEALTH_*`` environment
variable override at import time. The defaults are conservative:
three failures in ten = degrading; a week offline = stale.*
- `SourceHealthInput` (line 120) `class SourceHealthInput` - *Raw per-source data for health computation.

All fields are required; the caller (orchestrator, fusion analytics)
extracts these from the fusion store or its own tracking.*
- `SourceHealthResult` (line 156) `class SourceHealthResult` - *Health assessment for a single source.*
- `DashboardSummary` (line 182) `class DashboardSummary` - *Aggregate dashboard statistics.*
- `HealthDashboard` (line 195) `class HealthDashboard` - *Grouped health view: hot sources, degrading sources, aggregate stats.*

**Functions:**
- `_env_float` (line 28) `def _env_float(name, default)` - *Read a float env var, falling back to default on absence/error.*
- `_env_int` (line 40) `def _env_int(name, default)` - *Read an int env var, falling back to default on absence/error.*

**Methods:**
- `_clamp01` (line 224) `def _clamp01(value)`
- `_classify` (line 232) `def _classify(success_rate, avg_latency_ms, freshness_hours, fetch_count, config)` - *Classify a source's health status based on thresholds.*
- `compute_health` (line 257) `def compute_health(inp, config)` - *Compute the health assessment for a single source.

Pure: no I/O, no logging, deterministic. The formula is::

    success_weight = success_rate ^ 2
    latency_weight = clamp(1 - avg_latency_s / degrading_latency_s, 0, 1)
    freshness_weight = clamp(1 - freshness_hours / stale_hours, 0, 1)
    health_score = 0.5 * success_weight + 0.3 * latency_weight + 0.2 * freshness_weight*
- `build_dashboard` (line 317) `def build_dashboard(records, config)` - *Build a health dashboard from per-source health inputs.

Groups sources into hot (healthy), degrading (degrading + stale), and
unknown lists. Computes aggregate summary statistics.*
- `__post_init__` (line 80) `def __post_init__(self)`
- `__post_init__` (line 134) `def __post_init__(self)`
- `to_dict` (line 168) `def to_dict(self)`
- `to_dict` (line 206) `def to_dict(self)`

#### `source_loader.py`
**Path:** `estorides_core/source_loader.py`

**Classes:**
- `Source` (line 22) `class Source(dict)` - *A source is a YAML-defined OSINT data provider.

Stored as a dict for JSON-serialisation convenience, but exposes
attribute access for ergonomic call sites.*
- `SourceRegistry` (line 38) `class SourceRegistry` - *Loads YAML sources from the sources/ directory and exposes them by name.*

**Methods:**
- `__init__` (line 28) `def __init__(self, data)`
- `__getattr__` (line 31) `def __getattr__(self, key)`
- `__init__` (line 41) `def __init__(self, sources_dir)`
- `load` (line 47) `def load(self)`
- `_load_file` (line 71) `def _load_file(self, path)`
- `_normalise` (line 100) `def _normalise(self, raw)`
- `get` (line 160) `def get(self, name)`
- `all` (line 163) `def all(self)`
- `by_category` (line 166) `def by_category(self, category)`
- `categories` (line 169) `def categories(self)`
- `names` (line 172) `def names(self)`
- `filter` (line 175) `def filter(self)` - *Return sources matching the given predicates.

`max_contact` keeps only sources whose contact class is at or below
the given ceiling (e.g. "none" for a passive-only run, "broker" to
also allow third-party probes). Sources with an unknown contact
class are treated as the most exposing and thus excluded by any
ceiling below `active`.*
- `_category_dir_name` (line 197) `def _category_dir_name(self, category)` - *Derive a filesystem-safe directory name from a category label.

E.g. ``"06. Breach Intelligence"`` → ``"06_breach_intelligence"``.*
- `_source_path` (line 213) `def _source_path(self, name, category)` - *Derive the filesystem path for a source based on its name and category.*
- `_find_source_file` (line 219) `def _find_source_file(self, name)` - *Locate a source file on disk by name, scanning all category dirs.*
- `write_source_file` (line 231) `def write_source_file(self, data)` - *Write a source dict to the correct YAML file, overwriting if exists.

This is a pure file-write operation — no normalisation, no registry
update. The caller is responsible for reloading the registry if needed.
Returns the path written.*
- `delete_source_file` (line 292) `def delete_source_file(self, name)` - *Delete a source file by name. Raises KeyError if not found on disk.*
- `summary` (line 301) `def summary(self)` - *Compact summary used by /api/status.*

#### `ssrf_guard.py`
**Path:** `estorides_core/ssrf_guard.py`

**Classes:**
- `GuardResult` (line 99) `class GuardResult`
- `SSRFError` (line 277) `class SSRFError(ValueError)` - *Raised when an outbound URL fails the SSRF guard.*

**Methods:**
- `_is_blocked_v4` (line 110) `def _is_blocked_v4(ip)`
- `_is_blocked_v6` (line 114) `def _is_blocked_v6(addr)` - *Match an IPv6 textual address against the prefix table.

Lower-cased, leading zeros collapsed, no scope-id parsing required.*
- `_normalise_host` (line 134) `def _normalise_host(host)` - *Lowercase, strip brackets from IPv6 literals, return None if empty.*
- `_is_host_in_blocked_literal` (line 142) `def _is_host_in_blocked_literal(host)` - *If `host` is a literal IP in a blocked range, return a reason string.
Otherwise return None.*
- `_resolve` (line 163) `def _resolve(host)` - *Resolve `host` to its A + AAAA records. Empty on failure.*
- `_matches_allowlist` (line 180) `def _matches_allowlist(host, allowlist)` - *Return True if `host` matches any entry in the allowlist.

An entry like `osiris.example.com` matches the host itself and any
subdomain. An entry like `*` matches everything (escape hatch).*
- `_load_allowlist` (line 197) `def _load_allowlist()`
- `check_url` (line 202) `def check_url(url)` - *Validate a URL for outbound fetch.

Args:
    url: the URL string the source YAML wants us to hit.
    resolve: when True (default) also resolve hostnames and reject
        if any answer lands in a reserved range. Disable only in
        tests with mocked DNS.

Returns:
    GuardResult with allowed/reason. Use as a bool.*
- `assert_safe` (line 270) `def assert_safe(url)` - *Raise SSRFError if `url` is not safe to fetch.*
- `__bool__` (line 105) `def __bool__(self)`

#### `target_management.py`
**Path:** `estorides_core/target_management.py`

**Classes:**
- `TargetResult` (line 133) `class TargetResult`
- `BatchResult` (line 171) `class BatchResult`
- `TargetManager` (line 191) `class TargetManager`

**Functions:**
- `auto_detect_type` (line 69) `def auto_detect_type(value)`
- `_type_validator` (line 76) `def _type_validator(etype)`
- `validate_type` (line 95) `def validate_type(etype)`
- `validate_value` (line 103) `def validate_value(etype, value)`
- `validate_target` (line 117) `def validate_target(etype, value)`
- `make_target_id` (line 128) `def make_target_id(etype, value)`

**Methods:**
- `__init__` (line 137) `def __init__(self)`
- `to_dict` (line 158) `def to_dict(self)`
- `__init__` (line 174) `def __init__(self)`
- `to_dict` (line 181) `def to_dict(self)`
- `__init__` (line 193) `def __init__(self, fusion_store, case_store, entity_store)`
- `add_target` (line 203) `def add_target(self, etype, value, label, case_id)`
- `batch_import` (line 313) `def batch_import(self, text)`
- `csv_parse` (line 352) `def csv_parse(self, csv_text)`
- `batch_csv_import` (line 366) `def batch_csv_import(self, csv_text)`

#### `transforms.py`
**Path:** `estorides_core/transforms.py`

**Classes:**
- `Transform` (line 41) `class Transform` - *One named transform applicable to a set of entity types.*
- `TransformRegistry` (line 190) `class TransformRegistry` - *Holds every transform and dispatches by id.*

**Methods:**
- `_empty` (line 61) `def _empty(root_type, value)`
- `_resolver_filtered` (line 65) `def _resolver_filtered(ent_type, value, relations)` - *Resolve `(ent_type, value)` and keep only links whose relation is
in `relations` (or every link when `relations` is None). The root
node plus any node touched by a kept link is returned.*
- `_filter_runner` (line 86) `def _filter_runner(relations)`
- `_norm` (line 95) `def _norm(s)`
- `_osiris` (line 100) `def _osiris()`
- `_run_bgp` (line 108) `def _run_bgp(ent_type, value)`
- `_run_leaks` (line 134) `def _run_leaks(ent_type, value)`
- `_run_github` (line 159) `def _run_github(ent_type, value)`
- `_T` (line 230) `def _T(id, label, tier, applies, runner, description)`
- `summary` (line 51) `def summary(self)`
- `run` (line 87) `def run(ent_type, value)`
- `__init__` (line 193) `def __init__(self)`
- `register` (line 196) `def register(self, t)`
- `for_type` (line 199) `def for_type(self, ent_type)`
- `run` (line 209) `def run(self, transform_id, ent_type, value)`

#### `transliteration.py`
**Path:** `estorides_core/transliteration.py`

**Functions:**
- `_strip_diacritics` (line 76) `def _strip_diacritics(text)` - *Drop combining marks via NFKD decomposition.

Folds ``é`` -> ``e``, ``ü`` -> ``u``, full-width forms to ASCII, and so
on. Characters that have no compatibility decomposition pass through
unchanged and are handled by the per-script map instead.*
- `to_latin` (line 87) `def to_latin(text)` - *Return a lowercased, diacritic-free Latin transliteration.

The pipeline is: casefold -> NFKD diacritic strip (so accented Greek
and Latin fold to their base letters) -> per-character script map
(Cyrillic/Greek/Arabic) -> keep only ``[a-z0-9 ]``. Casefolding and
stripping run *before* the map so that uppercase and accented source
letters reach the lowercase, accent-free keys the map is written for.
Whitespace is collapsed to single spaces and the result is trimmed.
Non-mappable characters (e.g. unmapped CJK) are dropped, which is the
safe failure mode for fuzzy matching.*
- `consonant_skeleton` (line 112) `def consonant_skeleton(text)` - *Return the Latin transliteration with vowels and spaces removed.

This is the vowel-insensitive comparison key. Abjad scripts (Arabic,
Hebrew) routinely omit short vowels, so two spellings of the same name
can only be reconciled on their consonant skeletons. The first
character is preserved even if it is a vowel, because name-initial
vowels are usually written and carry signal.

Adjacent duplicate letters are collapsed so that gemination written as
a doubled Latin consonant (``Muhammad`` -> ``mhmmd``) reconciles with a
script that marks it with a diacritic instead of doubling the letter
(Arabic ``محمد`` -> ``mhmd``).*
- `is_non_latin` (line 139) `def is_non_latin(text)` - *True if any character is outside the Basic Latin / Latin-1 range.

Used by the resolver to decide whether the cross-script path is worth
taking for a given value before paying for transliteration of both
sides of a comparison.*

#### `validation.py`
**Path:** `estorides_core/validation.py`

**Classes:**
- `QueryValidationError` (line 55) `class QueryValidationError(ValueError)` - *Raised when a query fails validation. The reason is in `.reason`.*
- `Query` (line 63) `class Query` - *A validated, normalised query string.*

**Methods:**
- `_strip_and_collapse` (line 73) `def _strip_and_collapse(text)`
- `validate_query` (line 85) `def validate_query(raw)` - *Validate and normalise a user query string.

Args:
    raw: the user-supplied query, exactly as received.
    max_length: hard cap on the normalised length. Default 512.

Raises:
    QueryValidationError if the query is empty, oversized, contains
    forbidden characters, or resolves to a type the engine cannot
    dispatch on.

Returns:
    A `Query` with the normalised text and detected type.*
- `__init__` (line 57) `def __init__(self, reason, message)`
- `__str__` (line 69) `def __str__(self)`

#### `web_security.py`
**Path:** `estorides_core/web_security.py`

**Classes:**
- `WebSecurityConfig` (line 58) `class WebSecurityConfig` - *Resolved security policy for the Flask app.

All fields are read from the environment at import time and frozen so
the policy cannot drift at runtime. Changing a knob requires a restart
— the right call for a tool that mostly runs as a long-lived daemon.*
- `AuthGate` (line 328) `class AuthGate` - *Bearer-token gate applied to sensitive routes.

`required_token` is the single shared secret. `None` disables the gate
(local-trust mode). Comparison is constant-time.*

**Methods:**
- `_env_str` (line 108) `def _env_str(name, default)`
- `_env_int` (line 115) `def _env_int(name, default)`
- `_env_bool` (line 126) `def _env_bool(name, default)`
- `load_security_config` (line 133) `def load_security_config()` - *Resolve the security policy from env vars.

ESTORIDES_CORS_ORIGINS    comma-separated list, e.g. "https://app.example.com"
ESTORIDES_MAX_BODY_BYTES  int, default 1 MiB
ESTORIDES_HSTS            1 to emit Strict-Transport-Security
ESTORIDES_FORCE_HTTPS     1 to redirect plain http to https (only meaningful behind TLS)
ESTORIDES_CSP             override the default Content-Security-Policy
ESTORIDES_PUBLIC_HOST     public hostname for HTTPS redirect (default localhost:5050)*
- `install_security` (line 158) `def install_security(app, cfg)` - *Wire security middleware into a Flask app.

Idempotent: calling twice is a no-op (we re-attach, but Flask keeps the
last hook, and our hooks are stateless). Returns the resolved config so
the caller can echo it in a startup banner.*
- `_extract_bearer_token` (line 273) `def _extract_bearer_token()` - *Pull the bearer token from header, alt-header, cookie, or query param.

Header order matters: an explicit `Authorization: Bearer` always wins
over a cookie (the cookie is the fallback for the browser UI; the
header is what scripts and curl will use).

Query-param ``?token=`` is a **last resort** for Server-Sent Events
(``EventSource`` cannot set custom headers). It leaks into server
access logs — we accept this limitation because there is no other
transport for streaming endpoints in a browser. The token is never
accepted from query params on POST/PUT/DELETE requests.*
- `make_auth_gate` (line 308) `def make_auth_gate()` - *Build the auth gate from the current environment.

When `ESTORIDES_AUTH_TOKEN` is set, the gate uses that value.
When unset, the system auto-generates a random 64-hex-char token,
stores it in `AUTO_GENERATED_TOKEN` (so the startup banner can
display it), and returns an enabled gate. This guarantees API
abuse protection is always active — no login screen, no explicit
enrolment.*
- `require_auth` (line 375) `def require_auth(view)` - *Decorator: enforce the bearer-token gate on a view.

Behaviour:
  * gate disabled (no env var) → pass-through, no overhead.
  * gate enabled, token missing → 401 with `WWW-Authenticate: Bearer`.
  * gate enabled, token present but wrong → 401 (same shape, constant-
    time compare on the server side).

Use on every endpoint that reads or mutates operator-private data:
cases, run, run/stream/*, discover/*, export, intel/*, transform/*,
osiris/*, graph, status.*
- `install_auth_gate` (line 408) `def install_auth_gate(app, gate)` - *Attach the gate to a Flask app and a module-level slot.

Two consumers read the gate: the `require_auth` decorator (module
slot, so it works even when called outside a request context) and
`auth_meta_for_index()` (so `index.html` can be rendered with the
token embedded for the UI to pick up).*
- `_current_gate` (line 427) `def _current_gate()`
- `auto_generated_token` (line 431) `def auto_generated_token()` - *Return the auto-generated token (None if user set ESTORIDES_AUTH_TOKEN manually).*
- `is_cors_enabled` (line 99) `def is_cors_enabled(self)`
- `is_origin_allowed` (line 103) `def is_origin_allowed(self)` - *CORS is opt-in; this is the runtime check used by the after_request hook.*
- `_security_headers` (line 204) `def _security_headers(resp)`
- `_cors_preflight` (line 237) `def _cors_preflight()`
- `enabled` (line 338) `def enabled(self)`
- `check` (line 341) `def check(self)`
- `auth_meta_for_index` (line 349) `def auth_meta_for_index(self)` - *Token to embed in `index.html` so the UI can auto-authenticate.

Returns `None` when the gate is off (the UI then omits the meta
tag and every call goes through anonymously, which is the
local-trust default).*
- `issue_session_cookie_kwargs` (line 358) `def issue_session_cookie_kwargs(self)` - *Arguments for `set_cookie` to install the session cookie.

`Secure` is set when the request itself is over HTTPS or the operator
requested ESTORIDES_FORCE_HTTPS=1 (in that case we know they're behind
TLS). `SameSite=Lax` keeps the cookie from cross-site POSTs.*
- `wrapper` (line 389) `def wrapper()`
- `_redirect_to_https` (line 192) `def _redirect_to_https()`

#### `__init__.py`
**Path:** `estorides_export/__init__.py`

*No symbols extracted*

#### `encryption.py`
**Path:** `estorides_export/encryption.py`

**Functions:**
- `_have_age` (line 47) `def _have_age()`
- `encrypt_file` (line 51) `def encrypt_file(plaintext_path, recipient_pubkey)` - *Encrypt `plaintext_path` to `<plaintext_path>.age` for the recipient.

Returns the ciphertext path. Raises RuntimeError if `age` is
missing or the encryption subprocess fails — the orchestrator
catches and falls back to plaintext. Raises ValueError if
`recipient_pubkey` doesn't look like an age public key.

Validation order is: key shape (cheap, no exec) → binary
presence (filesystem stat) → subprocess. A malformed key is
always a programmer error and surfaces as ValueError; a missing
binary is an environment problem and surfaces as RuntimeError.*
- `export_stix_encrypted` (line 100) `def export_stix_encrypted(kg, recipient_pubkey, path)` - *Build the STIX bundle, write to disk, encrypt to <path>.age.

`path` is the plaintext filename; the returned path is the
encrypted artefact next to it. The plaintext is removed once
encryption succeeds so reports/ never accumulates raw intel
bundles — that was the disk-residue problem fixed for issue #8.*
- `export_misp_encrypted` (line 128) `def export_misp_encrypted(kg, recipient_pubkey, path)`

#### `misp.py`
**Path:** `estorides_export/misp.py`

**Functions:**
- `event_from_graph` (line 36) `def event_from_graph(kg)`
- `_category` (line 65) `def _category(ent_type)`
- `export` (line 79) `def export(kg, path)`

#### `report.py`
**Path:** `estorides_export/report.py`

**Functions:**
- `_tldr` (line 37) `def _tldr(case, entities, sources_queried, sources_succeeded, diff)` - *Top-of-page executive summary. 6-10 lines max.*
- `_iocs` (line 77) `def _iocs(entities)` - *The sections the next responder (CTI team, SOC) actually pastes
into a ticket. Domains, IPs, emails, hashes, CVEs, crypto addresses.*
- `_diff_section` (line 121) `def _diff_section(diff)` - *The "what's new since last run" block. Empty when no baseline.*
- `_analysis` (line 156) `def _analysis(case)` - *The LLM analysis (or stub) embedded verbatim in a code block.*
- `_meta_footer` (line 177) `def _meta_footer(case, sources_queried, sources_succeeded)`
- `render_markdown_report` (line 194) `def render_markdown_report(case, entities, sources_queried, sources_succeeded, diff)` - *Build a Markdown report for `case`.

Parameters
----------
case
    The case row, as returned by `CaseStore.get_case`. `analysis_json`
    is optional; if present it is embedded verbatim.
entities
    The full entity list. If omitted, only the counts in the case
    row are used (TL;DR still works, IOC section is empty).
diff
    Optional output of `CaseStore.diff_entities(a, b)`. When given,
    a "what's new" section is appended before the analysis.

Returns
-------
str
    The full Markdown document. UTF-8, LF newlines, no trailing
    newline (callers add their own if writing to a file).*

#### `stix.py`
**Path:** `estorides_export/stix.py`

**Functions:**
- `_id` (line 28) `def _id(stix_type)`
- `_now` (line 32) `def _now()`
- `bundle_from_graph` (line 55) `def bundle_from_graph(kg)`
- `export` (line 145) `def export(kg, path)`

#### `__init__.py`
**Path:** `estorides_llm/__init__.py`

*No symbols extracted*

#### `intelligence_prompts.py`
**Path:** `estorides_llm/intelligence_prompts.py`

**Functions:**
- `format_context` (line 98) `def format_context(sources)` - *Render a list of observation dicts into a context block for the LLM.

The previous implementation truncated at 3500 chars but did not
preserve source ordering, so a re-run produced a different prompt
and a different answer. This version sorts by source name (stable
order) and truncates per source so a single 100KB crt.sh response
cannot blow past the model's context window.

If the orchestrator has stamped an ontology verdict on an
observation (the `ontology` key), the formatted block carries a
one-line "SANCTIONED — OFAC SDN match on <fields>" warning that
the LLM is required to surface in its assessment.*

#### `manager.py`
**Path:** `estorides_llm/manager.py`

**Classes:**
- `LLMBackend` (line 37) `class LLMBackend(Protocol)` - *Minimal contract for an LLM backend.

Implementations MUST be total: raise on failure (the manager
catches and moves on) or return ("", "") to signal "I can't
answer, try the next backend".*
- `OllamaBackend` (line 86) `class OllamaBackend`
- `_OpenAICompatibleBackend` (line 143) `class _OpenAICompatibleBackend` - *Shared implementation for OpenAI-shaped APIs (openai, openrouter, …).

Subclasses set `name`, `env_key`, and `base_url`.*
- `OpenAIBackend` (line 179) `class OpenAIBackend(_OpenAICompatibleBackend)`
- `OpenRouterBackend` (line 186) `class OpenRouterBackend(_OpenAICompatibleBackend)`
- `AnthropicBackend` (line 193) `class AnthropicBackend`
- `LLMManager` (line 233) `class LLMManager`

**Methods:**
- `register` (line 63) `def register(name)` - *Decorator: register a backend under `name`.

Accepts both an instance and a class. If a class is given, the
decorator instantiates it with no arguments — which is the
common case for stateless backends that hold no per-instance
state. The class must therefore have a no-arg constructor.*
- `__call__` (line 46) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)` - *Return (content, model_id). Empty content means "skip me".*
- `deco` (line 71) `def deco(backend_or_cls)`
- `_resolve_model` (line 89) `def _resolve_model(self, request_timeout)` - *Pick a model ollama actually has pulled.

Prefers the configured model; falls back to the first available
tag so a stale config can't silently degrade every run to the
stub. (Previous behaviour; preserved here.)*
- `__call__` (line 116) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `__call__` (line 151) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `__call__` (line 196) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `__init__` (line 234) `def __init__(self)`
- `generate` (line 250) `def generate(self, prompt)` - *Try each backend in priority order; return the first that succeeds.

`request_timeout` caps every backend's HTTP call so a slow
local model cannot keep a worker thread alive past the
orchestrator's deadline. Returns a dict with keys:
backend, model, content, error.*
- `_stub_response` (line 292) `def _stub_response(self, prompt, context)`

#### `estorides_web.py`
**Path:** `estorides_web.py`

**Classes:**
- `_RunStreamJob` (line 112) `class _RunStreamJob` - *A live deep-run cross-search whose events feed an SSE stream.

Wraps a `BufferedEventSink` (the engine writes to it) and a cooperative
stop flag the UI can set. Status and terminal state are read straight
off the sink so there is one source of truth.*

**Functions:**
- `_client_ip` (line 65) `def _client_ip()` - *Best-effort client IP extraction.

Trusts X-Forwarded-For only when behind a known proxy
(ESTORIDES_TRUST_PROXY=1). Without that, falls back to
`request.remote_addr`. This avoids the classic
"set X-Forwarded-For to bypass rate limits" mistake on a
directly-exposed deployment.*
- `_arg_int` (line 82) `def _arg_int(name, default)` - *Read an int query-string arg, falling back to `default` on parse error.

Guards every endpoint that previously did `int(request.args.get(...))`
directly, where a non-numeric value raised ValueError and surfaced as
an unhandled 500 to the client.*
- `_send_and_cleanup` (line 98) `def _send_and_cleanup(p, tmpdir)` - *Send `p` as an attachment, then nuke `tmpdir` regardless of outcome.

Used by /api/export/<fmt> so reports/ doesn't accumulate a copy of
every exported bundle — see issue #43. The `finally` runs even when
the client disconnects mid-stream, which is the realistic failure
case for the exhaustion attack.*

**Methods:**
- `_new_stream_job_id` (line 150) `def _new_stream_job_id()` - *Timestamp-prefixed id so jobs sort chronologically.*
- `_rate_limit_decorator` (line 155) `def _rate_limit_decorator()` - *Decorator: enforce per-IP rate limit, write an audit row either way.

Catches the rate-limit denial BEFORE doing real work, so a flood
can't tie up the orchestrator. Audit row written for both allow
and deny so the trail is complete.*
- `create_app` (line 199) `def create_app()`
- `_serve_loop` (line 1314) `def _serve_loop()`
- `_shape_for_ui` (line 1327) `def _shape_for_ui(result)` - *Trim raw responses for the UI and reformat observations.*
- `__init__` (line 120) `def __init__(self, job_id, query, query_type, case_id)`
- `stop` (line 129) `def stop(self)`
- `should_stop` (line 132) `def should_stop(self)`
- `status` (line 136) `def status(self)`
- `done` (line 140) `def done(self)`
- `deco` (line 162) `def deco(view)`
- `index` (line 230) `def index()`
- `api_status` (line 251) `def api_status()`
- `api_run` (line 257) `def api_run()`
- `api_graph` (line 313) `def api_graph()`
- `api_feeds` (line 389) `def api_feeds()` - *Return real-time feed points (quakes, fires, news) for the map.

Optional query string:
  bbox=min_lon,min_lat,max_lon,max_lat — drop points outside.
  no_cache=1 — bypass the on-disk cache.*
- `api_export` (line 420) `def api_export(fmt)`
- `api_cases_list` (line 497) `def api_cases_list()`
- `api_cases_get` (line 511) `def api_cases_get(case_id)`
- `api_cases_delete` (line 526) `def api_cases_delete(case_id)`
- `api_cases_save` (line 535) `def api_cases_save(case_id)` - *Bookmark a case from the UI.

Sets a `notes` prefix so the case is easy to spot in the cases
list, then echoes the updated case back. The store is
append-only for observations, but `notes` is a free-text column
we can overwrite. This is the "I want to come back to this"
gesture: in v1 the only durable artefact was the case id; in
v1.3 we want the user to be able to tag their wins.*
- `api_cases_diff` (line 564) `def api_cases_diff()` - *Symmetric diff between two cases by entity (type, value).

Query string: ?a=<case_id>&b=<case_id>
Returns the entities present in B but not in A ("added"), the
inverse ("removed"), and the per-type breakdown. The UI uses
this to show "what's new since last run" without a re-query.*
- `api_intel_resolve` (line 590) `def api_intel_resolve()` - *Cross-feed entity resolution (Osiris-style /resolve).

Examples:
  GET /api/intel/resolve?type=ip&id=1.1.1.1
  GET /api/intel/resolve?type=person&id=Tim%20Cook
  GET /api/intel/resolve?type=cve&id=CVE-2024-3094*
- `api_intel_graph` (line 630) `def api_intel_graph()` - *Cypher query against the Kùzu persistent graph.

Examples:
  GET /api/intel/graph?q=MATCH%20(n%3AEnt)%20RETURN%20n.id%20LIMIT%2010*
- `api_intel_stats` (line 671) `def api_intel_stats()` - *Stats for both the case store and the Kùzu graph.*
- `api_fusion_stats` (line 691) `def api_fusion_stats()` - *One-glance dashboard of the fused, cross-run fact base.*
- `api_fusion_sources` (line 700) `def api_fusion_sources()` - *The YAML source catalogue with accumulated fetch/ok counters.*
- `api_fusion_entities` (line 710) `def api_fusion_entities()` - *Search fused entities.

Example: GET /api/fusion/entities?q=google&type=domain&min_sources=2
``min_sources`` is the fusion-native filter: only entities that at
least N distinct feeds corroborate.*
- `api_fusion_entity` (line 732) `def api_fusion_entity(eid)` - *Full fused view of one entity: provenance, properties, edges.

``min_sources`` (default 2) also returns the corroborated properties:
attributes that independent feeds agree on.*
- `api_fusion_analytics_entity_timeline` (line 751) `def api_fusion_analytics_entity_timeline(eid)`
- `api_fusion_analytics_entity_summary` (line 762) `def api_fusion_analytics_entity_summary(eid)`
- `api_fusion_analytics_source_stats` (line 773) `def api_fusion_analytics_source_stats(source_name)`
- `api_fusion_analytics_consensus` (line 784) `def api_fusion_analytics_consensus(eid)`
- `api_fusion_analytics_top_changed` (line 795) `def api_fusion_analytics_top_changed()`
- `admin_sources` (line 807) `def admin_sources()` - *Render the YAML source manager page.*
- `api_sources_yaml_list` (line 824) `def api_sources_yaml_list()` - *Return every YAML source with full configuration.*
- `api_sources_yaml_create` (line 849) `def api_sources_yaml_create()` - *Create a new YAML source.*
- `api_sources_yaml_update` (line 870) `def api_sources_yaml_update(name)` - *Update/replace a YAML source.*
- `api_sources_yaml_delete` (line 889) `def api_sources_yaml_delete(name)` - *Delete a YAML source.*
- `api_fusion_analytics_corroboration_matrix` (line 905) `def api_fusion_analytics_corroboration_matrix()`
- `api_transforms` (line 919) `def api_transforms()` - *List the transforms applicable to an entity type.

Example: GET /api/transforms?type=ip*
- `api_transform_run` (line 934) `def api_transform_run()` - *Run one transform and return nodes/links for graph merge.

Body: {"transform_id": "...", "type": "ip", "value": "1.2.3.4"}*
- `api_osiris_bgp` (line 963) `def api_osiris_bgp()`
- `api_osiris_mac` (line 978) `def api_osiris_mac()`
- `api_osiris_phone` (line 993) `def api_osiris_phone()`
- `api_osiris_github` (line 1008) `def api_osiris_github()`
- `api_osiris_leaks` (line 1023) `def api_osiris_leaks()`
- `api_osiris_kev` (line 1038) `def api_osiris_kev()`
- `api_osiris_malware` (line 1048) `def api_osiris_malware()`
- `api_osiris_threats` (line 1055) `def api_osiris_threats()`
- `api_discover_start` (line 1068) `def api_discover_start()`
- `api_discover_jobs` (line 1114) `def api_discover_jobs()`
- `api_discover_stop` (line 1120) `def api_discover_stop()`
- `api_discover_stream` (line 1132) `def api_discover_stream()` - *Server-Sent Events for a discoverer job.

The browser opens `EventSource('/api/discover/stream?job_id=...')`
and we keep the connection open, pushing one event per
JSON line as the background worker discovers things. The
stream closes when the job finishes (status=done|error|stopped).*
- `api_run_stream_start` (line 1187) `def api_run_stream_start()`
- `api_run_stream_stop` (line 1254) `def api_run_stream_stop()`
- `api_run_stream` (line 1266) `def api_run_stream()`
- `wrapper` (line 164) `def wrapper()`
- `gen` (line 1145) `def gen()`
- `_drive` (line 1217) `def _drive()`
- `gen` (line 1272) `def gen()`

#### `conftest.py`
**Path:** `tests/conftest.py`

*No symbols extracted*

#### `test_change_detection_properties.py`
**Path:** `tests/properties/test_change_detection_properties.py`

**Functions:**
- `test_scores_always_bounded` (line 69) `def test_scores_always_bounded(before, after)`
- `test_max_changes_respected` (line 77) `def test_max_changes_respected(before, after)`
- `test_id_is_16_char_hex` (line 86) `def test_id_is_16_char_hex(before, after)`
- `test_idempotent` (line 95) `def test_idempotent(before, after)`
- `test_first_run_reports_all_as_new` (line 105) `def test_first_run_reports_all_as_new(after)`
- `test_after_none_returns_empty` (line 113) `def test_after_none_returns_empty(before)`
- `test_before_vs_no_after_empty` (line 121) `def test_before_vs_no_after_empty(entities)`
- `test_summary_consistency` (line 132) `def test_summary_consistency(before, after)` - *Whatever the input, the summary fields must agree with the
``changes`` list: ``total == len(changes)``, ``by_kind`` counts
each kind exactly, ``score_max/mean`` are derived from the actual
changes, and ``entities_compared == len(before.entities)`` (or 0 if
``before`` is None).*

#### `test_csp_safe_styles_properties.py`
**Path:** `tests/properties/test_csp_safe_styles_properties.py`

**Functions:**
- `test_js_never_gains_a_style_attribute_in_template_literal` (line 58) `def test_js_never_gains_a_style_attribute_in_template_literal(insertion)` - *Hypothetical: a future patch appends the given string somewhere
in the JS. The codebase should still be free of `style="…"` in any
backtick-delimited template literal.

Strategy: simulate the patch as the insertion landing in any random
position of the file, then re-check the invariant. With 1000
random `insertion` x random offset combinations, the test exercises
the structural property: there is no `style="…"` substring inside
any backtick literal in the current file.*
- `test_template_never_gains_a_style_attribute` (line 105) `def test_template_never_gains_a_style_attribute(insertion)` - *Hypothetical: a future patch adds the given string somewhere in
the template. The contract is that `style="…"` does not exist in
any static markup of `templates/index.html`.

Jinja expressions `{{ … }}` and `{% … %}` are stripped before
scanning so we test the static part of the document.*
- `test_csp_style_src_never_gains_unsafe_inline` (line 137) `def test_csp_style_src_never_gains_unsafe_inline(bad)` - *Hypothetical: a future patch sets `style-src` to
`'self' 'unsafe-hashes' https://unpkg.com 'unsafe-inline'`. The
property-based test asserts the current CSP doesn't have
`'unsafe-inline'` in style-src, and that any string containing
`bad` in that position is rejected.

We assert the current state, not a future mutation. With 1000
random `bad` values, the structural check fires: the style-src
list never contains the unsafe keyword.*

#### `test_hypothesis_engine_properties.py`
**Path:** `tests/properties/test_hypothesis_engine_properties.py`

**Functions:**
- `test_scores_always_bounded` (line 54) `def test_scores_always_bounded(observations, entities)`
- `test_claim_length_under_cap` (line 66) `def test_claim_length_under_cap(observations, entities)`
- `test_reasoning_length_under_cap` (line 77) `def test_reasoning_length_under_cap(observations, entities)`
- `test_sources_sorted_unique` (line 88) `def test_sources_sorted_unique(observations, entities)`
- `test_id_is_deterministic_hex` (line 99) `def test_id_is_deterministic_hex(observations, entities)`
- `test_idempotent` (line 112) `def test_idempotent(observations, entities)`
- `test_max_hypotheses_caps_output` (line 123) `def test_max_hypotheses_caps_output(observations, entities)`
- `test_min_score_filters` (line 134) `def test_min_score_filters(observations, entities)`
- `test_hostile_observation_does_not_crash` (line 147) `def test_hostile_observation_does_not_crash(observations, entities)`

#### `test_recon_fusion_properties.py`
**Path:** `tests/properties/test_recon_fusion_properties.py`

**Classes:**
- `TestPropertyScoreBounds` (line 48) `class TestPropertyScoreBounds` - *P1 -- Scores are always in [0, 1].*
- `TestPropertyTotalCounts` (line 68) `class TestPropertyTotalCounts` - *P2 -- total_observations and total_entities match input.*
- `TestPropertyTierSumMatches` (line 93) `class TestPropertyTierSumMatches` - *P3 -- tier_summary counts match actual tier list lengths.*
- `TestPropertyDeterminism` (line 114) `class TestPropertyDeterminism` - *P4 -- Same input always produces same output (time-independent fields excluded).*
- `TestPropertyNoDuplicates` (line 135) `class TestPropertyNoDuplicates` - *P5 -- No duplicate canonical_id within the same tier.*
- `TestPropertyTierKeysOrder` (line 155) `class TestPropertyTierKeysOrder` - *P6 -- result.tiers dict preserves canonical tier key order.*
- `TestPropertyEmptyQueryRejected` (line 176) `class TestPropertyEmptyQueryRejected` - *P7 -- Empty query always raises ValueError.*
- `TestPropertySafeWithBadInputs` (line 196) `class TestPropertySafeWithBadInputs` - *P8 -- None observations/entities never crash.*

**Methods:**
- `test_all_scores_in_unit_interval` (line 58) `def test_all_scores_in_unit_interval(self, query, query_type, observations, entities)`
- `test_counts_match_input` (line 78) `def test_counts_match_input(self, query, query_type, n_obs, n_ents)`
- `test_tier_summary_matches` (line 103) `def test_tier_summary_matches(self, query, query_type, observations, entities)`
- `test_deterministic_output` (line 124) `def test_deterministic_output(self, query, query_type, observations, entities)`
- `test_no_duplicate_ids_in_tier` (line 145) `def test_no_duplicate_ids_in_tier(self, query, query_type, observations, entities)`
- `test_tier_keys_in_canonical_order` (line 165) `def test_tier_keys_in_canonical_order(self, query, query_type, observations, entities)`
- `test_empty_query_raises` (line 185) `def test_empty_query_raises(self, query_type, observations, entities)`
- `test_none_inputs_safe` (line 201) `def test_none_inputs_safe(self, query, query_type)`
- `test_entities_none_is_safe` (line 214) `def test_entities_none_is_safe(self, query, query_type, observations)`

#### `test_reliability_scoring_properties.py`
**Path:** `tests/properties/test_reliability_scoring_properties.py`

**Functions:**
- `test_score_always_bounded` (line 56) `def test_score_always_bounded(reliability, credibility, corroboration, age, base, half_life)`
- `test_corroboration_weight_in_unit_interval` (line 73) `def test_corroboration_weight_in_unit_interval(n)`
- `test_freshness_monotone_in_age` (line 87) `def test_freshness_monotone_in_age(age1, age2)`
- `test_reliability_from_name_never_raises` (line 110) `def test_reliability_from_name_never_raises(name)`
- `test_merge_confidence_bounded` (line 126) `def test_merge_confidence_bounded(existing, new_obs, new_rel, new_cred, cor, age)`
- `test_reliability_weight_set_is_curated` (line 141) `def test_reliability_weight_set_is_curated()`
- `test_credibility_weight_set_is_curated` (line 146) `def test_credibility_weight_set_is_curated()`
- `test_corroboration_is_monotone_in_count` (line 159) `def test_corroboration_is_monotone_in_count(n1, n2)`
- `test_higher_reliability_dominates` (line 184) `def test_higher_reliability_dominates(rel1, rel2)`
- `test_source_type_from_name_never_raises` (line 202) `def test_source_type_from_name_never_raises(name)`
- `test_source_type_weight_always_curated` (line 219) `def test_source_type_weight_always_curated(reliability, credibility, source_type, corroboration, age, base, half_life)`
- `test_source_type_weight_set_is_curated` (line 241) `def test_source_type_weight_set_is_curated()`

#### `test_search_telemetry_properties.py`
**Path:** `tests/properties/test_search_telemetry_properties.py`

**Functions:**
- `test_progress_invariants_hold` (line 32) `def test_progress_invariants_hold(completed, total, phase_key)`
- `test_progress_rejects_unknown_phase` (line 46) `def test_progress_rejects_unknown_phase(phase_key)`
- `test_brand_predicate_is_total` (line 56) `def test_brand_predicate_is_total(text)`
- `test_emoji_predicate_is_total` (line 65) `def test_emoji_predicate_is_total(text)`
- `test_percent_encoded_emoji_predicate_is_total` (line 74) `def test_percent_encoded_emoji_predicate_is_total(text)`
- `test_brand_predicate_flags_embedded_brand` (line 84) `def test_brand_predicate_flags_embedded_brand(prefix, suffix)`

#### `test_source_health_monitoring_properties.py`
**Path:** `tests/properties/test_source_health_monitoring_properties.py`

**Functions:**
- `_valid_input` (line 21) `def _valid_input(fetch, ok, latency, last_seen, now)` - *Build a valid SourceHealthInput, clamping ok <= fetch.*
- `test_health_score_always_bounded` (line 49) `def test_health_score_always_bounded(fetch, ok, latency, last_seen, now)`
- `test_status_always_valid_enum` (line 63) `def test_status_always_valid_enum(fetch, ok, latency, last_seen, now)`
- `test_success_rate_bounds` (line 78) `def test_success_rate_bounds(fetch, ok, latency, last_seen, now)`
- `test_unknown_when_below_min_fetches` (line 89) `def test_unknown_when_below_min_fetches(fetch, config_min)`
- `valid_health_inputs` (line 97) `def valid_health_inputs(draw)`
- `test_dashboard_summary_counts_match` (line 112) `def test_dashboard_summary_counts_match(records)` - *Dashboard summary counts must sum to total.*

#### `test_target_management_properties.py`
**Path:** `tests/properties/test_target_management_properties.py`

**Functions:**
- `test_p1_add_target_never_raises` (line 21) `def test_p1_add_target_never_raises(etype, value)`
- `test_p2_validated_id_is_deterministic` (line 31) `def test_p2_validated_id_is_deterministic(etype, value)`
- `test_p3_make_target_id_stable_under_case` (line 40) `def test_p3_make_target_id_stable_under_case(etype, value)`
- `test_p4_valid_domains_validate` (line 56) `def test_p4_valid_domains_validate(d)`
- `test_p5_valid_ipv4_validate` (line 68) `def test_p5_valid_ipv4_validate(ip)`
- `test_p6_valid_emails_validate` (line 77) `def test_p6_valid_emails_validate(email)`
- `test_p7_auto_detect_never_fails` (line 83) `def test_p7_auto_detect_never_fails(value)`
- `test_p8_validate_target_never_raises` (line 89) `def test_p8_validate_target_never_raises(value)`
- `test_p9_batch_import_idempotent` (line 105) `def test_p9_batch_import_idempotent(targets)`
- `test_p10_batch_import_never_raises` (line 116) `def test_p10_batch_import_never_raises(text)`

#### `test_audit_log.py`
**Path:** `tests/test_audit_log.py`

**Functions:**
- `_ev` (line 12) `def _ev(ts)`
- `test_audit_log_appends` (line 22) `def test_audit_log_appends(tmp_path)`
- `test_audit_log_rotates_when_cap_exceeded` (line 31) `def test_audit_log_rotates_when_cap_exceeded(tmp_path)`
- `test_audit_log_rotation_respects_keep_count` (line 48) `def test_audit_log_rotation_respects_keep_count(tmp_path)`
- `test_audit_log_no_rotation_when_disabled` (line 61) `def test_audit_log_no_rotation_when_disabled(tmp_path)`

#### `test_auth_gate.py`
**Path:** `tests/test_auth_gate.py`

**Functions:**
- `app_with_gate` (line 22) `def app_with_gate(monkeypatch)` - *A Flask app with the auth gate enabled, token 'sek'.

Each test gets a fresh app so the module-level _GATE slot is clean.*
- `test_gate_auto_generates_token_when_unset` (line 41) `def test_gate_auto_generates_token_when_unset(monkeypatch)`
- `test_gate_on_rejects_anonymous` (line 53) `def test_gate_on_rejects_anonymous(app_with_gate)`
- `test_gate_on_accepts_bearer_header` (line 61) `def test_gate_on_accepts_bearer_header(app_with_gate)`
- `test_gate_on_accepts_alt_header` (line 68) `def test_gate_on_accepts_alt_header(app_with_gate)`
- `test_gate_on_accepts_cookie` (line 74) `def test_gate_on_accepts_cookie(app_with_gate)`
- `test_gate_on_rejects_wrong_token` (line 81) `def test_gate_on_rejects_wrong_token(app_with_gate)`
- `test_gate_on_auto_generated_token_in_meta` (line 87) `def test_gate_on_auto_generated_token_in_meta(monkeypatch)`
- `test_gate_on_exposes_token_for_index_meta` (line 95) `def test_gate_on_exposes_token_for_index_meta()`
- `private` (line 34) `def private()`

#### `test_change_detection.py`
**Path:** `tests/test_change_detection.py`

**Classes:**
- `TestNewEntity` (line 56) `class TestNewEntity` - *S1 del spec.*
- `TestPropertyChanged` (line 99) `class TestPropertyChanged` - *S2 del spec.*
- `TestFirstRunBeforeIsNone` (line 125) `class TestFirstRunBeforeIsNone` - *S3 del spec.*
- `TestAfterIsNone` (line 147) `class TestAfterIsNone` - *S4 del spec.*
- `TestDisappearedWithGrace` (line 166) `class TestDisappearedWithGrace` - *S5 del spec.*
- `TestSourceAdded` (line 199) `class TestSourceAdded` - *S6 del spec.*
- `TestMinReliabilityFiltersSources` (line 226) `class TestMinReliabilityFiltersSources` - *S7 del spec.*
- `TestMaxChangesBounds` (line 255) `class TestMaxChangesBounds` - *S8 del spec.*
- `TestProgrammerErrorRaises` (line 281) `class TestProgrammerErrorRaises` - *S9 del spec.*
- `TestHostilePropertyKey` (line 310) `class TestHostilePropertyKey` - *S10 del spec.*
- `TestDeterminism` (line 346) `class TestDeterminism` - *S11 del spec.*
- `TestSourceRemoved` (line 386) `class TestSourceRemoved` - *S13 del spec: una source que antes veía la entity ya no la ve.*
- `TestEdgeChanges` (line 436) `class TestEdgeChanges` - *S14 del spec: edges salientes que aparecen/desaparecen.*
- `TestConfidenceShifted` (line 488) `class TestConfidenceShifted` - *S15 del spec: |confidence_after - confidence_before| > 0.20.*
- `TestBoundedSmoke` (line 528) `class TestBoundedSmoke` - *S12 del spec: smoke test del dataclass.*

**Functions:**
- `_entity` (line 28) `def _entity(eid, etype, value)`

**Methods:**
- `test_one_new_entity_emits_one_new_change` (line 59) `def test_one_new_entity_emits_one_new_change(self)`
- `test_new_change_score_in_high_band` (line 84) `def test_new_change_score_in_high_band(self)`
- `test_property_change_emits_one_change` (line 102) `def test_property_change_emits_one_change(self)`
- `test_before_none_reports_all_as_new` (line 128) `def test_before_none_reports_all_as_new(self)`
- `test_after_none_returns_empty_report` (line 150) `def test_after_none_returns_empty_report(self)`
- `test_disappeared_within_grace_is_ignored` (line 169) `def test_disappeared_within_grace_is_ignored(self)`
- `test_disappeared_outside_grace_emits_change` (line 181) `def test_disappeared_outside_grace_emits_change(self)`
- `test_new_source_on_existing_entity_emits_source_added` (line 202) `def test_new_source_on_existing_entity_emits_source_added(self)`
- `test_min_reliability_e_excludes_f_source` (line 229) `def test_min_reliability_e_excludes_f_source(self)`
- `test_max_changes_caps_output` (line 258) `def test_max_changes_caps_output(self)`
- `test_entity_id_empty_raises` (line 284) `def test_entity_id_empty_raises(self)`
- `test_entity_type_empty_raises` (line 288) `def test_entity_type_empty_raises(self)`
- `test_entity_value_empty_raises` (line 292) `def test_entity_value_empty_raises(self)`
- `test_min_change_score_out_of_range_raises` (line 296) `def test_min_change_score_out_of_range_raises(self)`
- `test_max_changes_too_small_raises` (line 302) `def test_max_changes_too_small_raises(self)`
- `test_hostile_key_does_not_crash` (line 322) `def test_hostile_key_does_not_crash(self, hostile_key)`
- `test_same_input_same_ids_and_scores` (line 349) `def test_same_input_same_ids_and_scores(self)`
- `test_input_order_does_not_affect_output` (line 366) `def test_input_order_does_not_affect_output(self)`
- `test_source_removed_emits_change` (line 389) `def test_source_removed_emits_change(self)`
- `test_source_removed_filtered_by_min_score` (line 410) `def test_source_removed_filtered_by_min_score(self)`
- `test_edge_added_emits_change` (line 439) `def test_edge_added_emits_change(self)`
- `test_edge_removed_emits_change` (line 462) `def test_edge_removed_emits_change(self)`
- `test_large_confidence_shift_emits_change` (line 491) `def test_large_confidence_shift_emits_change(self)`
- `test_small_confidence_shift_ignored` (line 509) `def test_small_confidence_shift_ignored(self)`
- `test_change_is_frozen` (line 531) `def test_change_is_frozen(self)`
- `test_diff_is_frozen` (line 541) `def test_diff_is_frozen(self)`
- `test_change_report_is_frozen` (line 546) `def test_change_report_is_frozen(self)`

#### `test_csp_safe_styles.py`
**Path:** `tests/test_csp_safe_styles.py`

**Functions:**
- `_strip_template_jinja` (line 41) `def _strip_template_jinja(template_text)` - *Replace `{{ ... }}` and `{% ... %}` with empty so the file is grep-able.

We only care whether the *static markup* contains `style="..."`. A
`{{ estorides_auth_token or '' }}` cannot produce a `style="` because
the auth token is a short opaque string and Jinja escapes it
(autoescape=on by default for .html). Even if the token were
malicious, a separate test (S7) covers the injection vector.*
- `_strip_js_comments_and_strings_outside_templates` (line 55) `def _strip_js_comments_and_strings_outside_templates(js_text)` - *Return the *template-literal contents* of the JS file as a single string.

We can't simply grep `style="` because of false positives in comments
and regular strings (e.g. error messages). The CSP issue is
specifically about values written into the DOM via `innerHTML`
containing `style="`. The only way to do that in this codebase is
through a template literal that gets assigned to `innerHTML`,
`outerHTML`, or inserted via `insertAdjacentHTML`.

Strategy: strip line (`// …`) and block (`/* … */`) comments
first so backticks inside comments don't confuse the template
literal scanner. Then extract every backtick-delimited template
literal and return them joined.*
- `test_index_html_has_no_style_attribute` (line 90) `def test_index_html_has_no_style_attribute()` - *S1 — `style="..."` must not appear anywhere in the rendered template.

Browsers reject inline style attributes under the locked-down
`style-src` policy. The fix is to use CSS classes (or `hidden`) —
not to relax the policy.*
- `test_estorides_js_has_no_style_in_template_literals` (line 111) `def test_estorides_js_has_no_style_in_template_literals()` - *S2 — `style="..."` must not appear in any template literal in the JS.

JS uses `innerHTML = `…`` to inject HTML. The literal text must
not contain `style="…"` because the browser will then try to
apply that style attribute and CSP will block it.*
- `test_offscreen_element_uses_hidden_attribute` (line 145) `def test_offscreen_element_uses_hidden_attribute(element_id)` - *S3 — Each offscreen element must have the HTML5 `hidden` attribute.

The browser's user-agent stylesheet already turns `[hidden]` into
`display: none`, so we don't need a literal `style="display:none"`.*
- `test_css_has_required_class` (line 189) `def test_css_has_required_class(selector)` - *The CSS file must define the new classes the refactor relies on.*
- `test_csp_policy_does_not_relax_for_unsafe_inline` (line 201) `def test_csp_policy_does_not_relax_for_unsafe_inline()` - *S5 — The locked-down CSP must stay locked down.

The whole point of the refactor is that we don't have to relax
`style-src` to make the UI work. If this test ever fails, the
previous fix was reverted to `'unsafe-inline'` — a regression.*
- `test_csp_policy_is_unchanged_after_refactor` (line 225) `def test_csp_policy_is_unchanged_after_refactor()` - *S6 — The default CSP string is byte-identical to the pre-refactor value.

The fix is in the frontend, not in the policy. If this test fails,
the policy was changed instead of refactored.*
- `test_dynamic_cluster_color_uses_cssom_assignment` (line 252) `def test_dynamic_cluster_color_uses_cssom_assignment()` - *S4 — The bridge-tooltip chip must set background via CSSOM.

We assert that the JS code *does* set `chip.style.background = cs`
(or `span.style.backgroundColor = cs`) and that the HTML string
for the chip is built without a `style="background:…"` attribute.*
- `test_dynamic_kind_color_uses_cssom_assignment` (line 272) `def test_dynamic_kind_color_uses_cssom_assignment()` - *S4 (kind) — `colorForKind(e.kind)` must reach CSSOM, not innerHTML.*
- `test_rendered_template_has_no_style_attribute_and_uses_hidden` (line 289) `def test_rendered_template_has_no_style_attribute_and_uses_hidden()` - *End-to-end: render `index.html` and assert no inline styles leak.*

#### `test_encrypted_export.py`
**Path:** `tests/test_encrypted_export.py`

**Classes:**
- `_FakeCompleted` (line 21) `class _FakeCompleted`

**Methods:**
- `_kg_with_one_node` (line 27) `def _kg_with_one_node()`
- `_patch_age_ok` (line 33) `def _patch_age_ok()` - *Pretend `age` is on PATH and that `age -e -r ...` produced ciphertext.*
- `test_stix_encrypted_removes_plaintext` (line 43) `def test_stix_encrypted_removes_plaintext(tmp_path)`
- `test_misp_encrypted_removes_plaintext` (line 52) `def test_misp_encrypted_removes_plaintext(tmp_path)`
- `test_stix_encrypted_removes_plaintext_on_failure` (line 61) `def test_stix_encrypted_removes_plaintext_on_failure(tmp_path)` - *Even when age fails, the plaintext must be removed.*
- `__init__` (line 22) `def __init__(self, rc, stderr)`
- `_run` (line 35) `def _run(cmd, stdin, stdout, stderr, check)`
- `_run_fail` (line 66) `def _run_fail(cmd, stdin, stdout, stderr, check)`

#### `test_entity_resolution.py`
**Path:** `tests/test_entity_resolution.py`

**Classes:**
- `TestTransliteration` (line 42) `class TestTransliteration` - *Cyrillic, Greek, Arabic, diacritic folding.*
- `TestJaroWinkler` (line 68) `class TestJaroWinkler` - *Jaro-Winkler similarity invariants.*
- `TestNormalization` (line 89) `class TestNormalization` - *Type-aware normalisation.*
- `TestCanonicalId` (line 133) `class TestCanonicalId` - *Deterministic content-addressed ids.*
- `TestCrossScriptPersonFusion` (line 155) `class TestCrossScriptPersonFusion` - *ER1: latin + cyrillic + comma-variant → one identity.*
- `TestDomainCaseVariantMerge` (line 194) `class TestDomainCaseVariantMerge` - *ER2: EvilCorp.com and evilcorp.com → exact merge.*
- `TestLookAlikeDomainsSurfaceAsLink` (line 221) `class TestLookAlikeDomainsSurfaceAsLink` - *ER3: evilcorp.com vs evil-corp.com → SAME_AS link, not merged.*
- `TestDeterministicTypeNoFuzzyMatch` (line 246) `class TestDeterministicTypeNoFuzzyMatch` - *ER4: md5 differing by one char → separate entities.*
- `TestIdenticalIpsMerge` (line 272) `class TestIdenticalIpsMerge` - *ER5: same IP from two sources → merged.*
- `TestNearIpsNeverFuse` (line 289) `class TestNearIpsNeverFuse` - *ER6: 8.8.8.8 and 8.8.4.4 → separate.*
- `TestOrgSuffixFolding` (line 309) `class TestOrgSuffixFolding` - *ER7: Evil Corp LLC + Evil Corp → merged.*
- `TestDistinctPersonsStaySeparate` (line 326) `class TestDistinctPersonsStaySeparate` - *ER8: Putin and Medvedev → separate identities.*
- `TestCanonicalEntityRoundtrip` (line 347) `class TestCanonicalEntityRoundtrip` - *ER9: to_dict and to_entity preserve data.*
- `TestEmptyInput` (line 382) `class TestEmptyInput` - *ER10: empty list → empty result.*
- `TestCanonicalIdDeterministic` (line 394) `class TestCanonicalIdDeterministic` - *ER11: same input → same id.*
- `TestDifferentInputDifferentId` (line 406) `class TestDifferentInputDifferentId` - *ER12: different input → different id.*
- `TestEdgeCases` (line 418) `class TestEdgeCases` - *Additional edge cases beyond the spec scenarios.*
- `TestCrossRunStability` (line 448) `class TestCrossRunStability` - *Canonical id stays stable across runs via persistent store.*

**Functions:**
- `_ent` (line 28) `def _ent(etype, value, source, confidence)`
- `_by_value` (line 32) `def _by_value(result, value)`

**Methods:**
- `test_cyrillic_to_latin` (line 45) `def test_cyrillic_to_latin(self)`
- `test_greek_accented_to_latin` (line 48) `def test_greek_accented_to_latin(self)`
- `test_diacritic_fold` (line 51) `def test_diacritic_fold(self)`
- `test_consonant_skeleton_arabic_matches_latin` (line 54) `def test_consonant_skeleton_arabic_matches_latin(self)`
- `test_consonant_skeleton_gemination` (line 57) `def test_consonant_skeleton_gemination(self)`
- `test_distinct_names_have_distinct_skeletons` (line 60) `def test_distinct_names_have_distinct_skeletons(self)`
- `test_non_latin_detector` (line 63) `def test_non_latin_detector(self)`
- `test_identical_strings_score_one` (line 71) `def test_identical_strings_score_one(self)`
- `test_empty_pair_scores_zero` (line 74) `def test_empty_pair_scores_zero(self)`
- `test_classic_jaro_winkler_bound` (line 77) `def test_classic_jaro_winkler_bound(self)`
- `test_dissimilar_strings_score_low` (line 81) `def test_dissimilar_strings_score_low(self)`
- `test_scores_stay_in_unit_interval` (line 84) `def test_scores_stay_in_unit_interval(self)`
- `test_ipv4_normalised` (line 92) `def test_ipv4_normalised(self)`
- `test_ipv6_compressed` (line 95) `def test_ipv6_compressed(self)`
- `test_hash_lowered` (line 101) `def test_hash_lowered(self)`
- `test_cve_uppered` (line 107) `def test_cve_uppered(self)`
- `test_domain_strips_scheme_www_path` (line 110) `def test_domain_strips_scheme_www_path(self)`
- `test_person_order_independent` (line 116) `def test_person_order_independent(self)`
- `test_org_suffix_stripped` (line 121) `def test_org_suffix_stripped(self)`
- `test_asn_normalised` (line 126) `def test_asn_normalised(self)`
- `test_email_lowered` (line 129) `def test_email_lowered(self)`
- `test_deterministic` (line 136) `def test_deterministic(self)`
- `test_different_values_different_ids` (line 141) `def test_different_values_different_ids(self)`
- `test_id_format` (line 146) `def test_id_format(self)`
- `test_three_spellings_fuse` (line 158) `def test_three_spellings_fuse(self)`
- `test_fused_identity_carries_all_sources` (line 169) `def test_fused_identity_carries_all_sources(self)`
- `test_cross_script_flagged_in_attributes` (line 180) `def test_cross_script_flagged_in_attributes(self)`
- `test_domain_case_variants_merge` (line 197) `def test_domain_case_variants_merge(self)`
- `test_domain_merge_is_exact` (line 207) `def test_domain_merge_is_exact(self)`
- `test_look_alike_domains_stay_separate` (line 224) `def test_look_alike_domains_stay_separate(self)`
- `test_look_alike_domains_produce_same_as_link` (line 233) `def test_look_alike_domains_produce_same_as_link(self)`
- `test_deterministic_near_miss_never_matches` (line 249) `def test_deterministic_near_miss_never_matches(self)`
- `test_score_pair_deterministic_mismatch` (line 259) `def test_score_pair_deterministic_mismatch(self)`
- `test_identical_ips_merge` (line 275) `def test_identical_ips_merge(self)`
- `test_near_ips_stay_separate` (line 292) `def test_near_ips_stay_separate(self)`
- `test_org_suffix_variants_merge` (line 312) `def test_org_suffix_variants_merge(self)`
- `test_distinct_persons_not_absorbed` (line 329) `def test_distinct_persons_not_absorbed(self)`
- `test_to_dict_serialises` (line 350) `def test_to_dict_serialises(self)`
- `test_to_entity_projects_legacy` (line 361) `def test_to_entity_projects_legacy(self)`
- `test_resolution_result_has_one_entity` (line 373) `def test_resolution_result_has_one_entity(self)`
- `test_empty_input_returns_empty` (line 385) `def test_empty_input_returns_empty(self)`
- `test_same_normalised_same_id` (line 397) `def test_same_normalised_same_id(self)`
- `test_different_normalised_different_id` (line 409) `def test_different_normalised_different_id(self)`
- `test_blank_value_does_not_crash` (line 421) `def test_blank_value_does_not_crash(self)`
- `test_whitespace_only_handled` (line 425) `def test_whitespace_only_handled(self)`
- `test_single_entity_produces_one_canonical` (line 429) `def test_single_entity_produces_one_canonical(self)`
- `test_confidence_boosted_by_multiple_sources` (line 434) `def test_confidence_boosted_by_multiple_sources(self)`
- `test_cross_run_id_stability` (line 451) `def test_cross_run_id_stability(self)`

#### `test_fusion_analytics.py`
**Path:** `tests/test_fusion_analytics.py`

**Classes:**
- `TestEntityTimeline` (line 64) `class TestEntityTimeline`
- `TestEntitySummary` (line 87) `class TestEntitySummary`
- `TestEntityTimelineNonexistent` (line 109) `class TestEntityTimelineNonexistent`
- `TestSourceStats` (line 118) `class TestSourceStats`
- `TestMultiSourceConsensus` (line 155) `class TestMultiSourceConsensus`
- `TestCorroboratedProperties` (line 176) `class TestCorroboratedProperties`
- `TestEntitySearch` (line 195) `class TestEntitySearch`
- `TestTopChanged` (line 230) `class TestTopChanged`
- `TestSourceCorroborationMatrix` (line 250) `class TestSourceCorroborationMatrix`
- `TestWithNoneStore` (line 268) `class TestWithNoneStore`
- `TestBoundaryConditions` (line 281) `class TestBoundaryConditions`

**Functions:**
- `store_and_analytics` (line 27) `def store_and_analytics(tmp_path)`
- `_populate_evilcorp` (line 42) `def _populate_evilcorp(store)`
- `_register_source` (line 57) `def _register_source(store, name)`

**Methods:**
- `test_returns_full_timeline` (line 65) `def test_returns_full_timeline(self, store_and_analytics)`
- `test_nonexistent_eid_returns_none` (line 79) `def test_nonexistent_eid_returns_none(self, store_and_analytics)`
- `test_returns_summary_stats` (line 88) `def test_returns_summary_stats(self, store_and_analytics)`
- `test_nonexistent_eid_returns_none` (line 101) `def test_nonexistent_eid_returns_none(self, store_and_analytics)`
- `test_returns_none` (line 110) `def test_returns_none(self, store_and_analytics)`
- `test_returns_source_metrics` (line 119) `def test_returns_source_metrics(self, store_and_analytics)`
- `test_nonexistent_source_returns_none` (line 135) `def test_nonexistent_source_returns_none(self, store_and_analytics)`
- `test_success_rate_correct` (line 139) `def test_success_rate_correct(self, store_and_analytics)`
- `test_consensus_picks_majority_value` (line 156) `def test_consensus_picks_majority_value(self, store_and_analytics)`
- `test_nonexistent_key_returns_empty` (line 165) `def test_nonexistent_key_returns_empty(self, store_and_analytics)`
- `test_filters_by_min_sources` (line 177) `def test_filters_by_min_sources(self, store_and_analytics)`
- `test_min_sources_one_returns_all` (line 185) `def test_min_sources_one_returns_all(self, store_and_analytics)`
- `test_search_by_term` (line 196) `def test_search_by_term(self, store_and_analytics)`
- `test_search_no_results` (line 208) `def test_search_no_results(self, store_and_analytics)`
- `test_search_filter_by_type` (line 213) `def test_search_filter_by_type(self, store_and_analytics)`
- `test_search_with_confidence_and_source_filters` (line 219) `def test_search_with_confidence_and_source_filters(self, store_and_analytics)`
- `test_returns_recently_active_entities` (line 231) `def test_returns_recently_active_entities(self, store_and_analytics)`
- `test_empty_window_returns_empty` (line 241) `def test_empty_window_returns_empty(self, store_and_analytics)`
- `test_returns_pairs_with_shared_counts` (line 251) `def test_returns_pairs_with_shared_counts(self, store_and_analytics)`
- `test_all_methods_return_empty` (line 269) `def test_all_methods_return_empty(self)`
- `test_min_sources_zero_treated_as_one` (line 282) `def test_min_sources_zero_treated_as_one(self, store_and_analytics)`
- `test_negative_days_treated_as_one` (line 288) `def test_negative_days_treated_as_one(self, store_and_analytics)`

#### `test_hypothesis_engine.py`
**Path:** `tests/test_hypothesis_engine.py`

**Classes:**
- `TestHappyPathDomainBelongsToActor` (line 39) `class TestHappyPathDomainBelongsToActor` - *S1 del spec.*
- `TestEmptyInputProducesEmptyOutput` (line 113) `class TestEmptyInputProducesEmptyOutput` - *S2 del spec.*
- `TestMalformedObservationsAreSkipped` (line 138) `class TestMalformedObservationsAreSkipped` - *S3 del spec.*
- `TestUnknownSourceFallsBackToReliabilityC` (line 176) `class TestUnknownSourceFallsBackToReliabilityC` - *S4 del spec.*
- `TestMinScoreFiltersHypotheses` (line 199) `class TestMinScoreFiltersHypotheses` - *S5 del spec.*
- `TestMaxHypothesesBounds` (line 230) `class TestMaxHypothesesBounds` - *S6 del spec.*
- `TestProgrammerErrorRaisesValueOrTypeError` (line 253) `class TestProgrammerErrorRaisesValueOrTypeError` - *S7 del spec.*
- `TestHostileObservationPayloadIsHandled` (line 280) `class TestHostileObservationPayloadIsHandled` - *S8 del spec.*
- `TestDeterminism` (line 309) `class TestDeterminism` - *S9 del spec.*
- `TestBoundedSmoke` (line 351) `class TestBoundedSmoke` - *S10 del spec: smoke test del dataclass.*

**Functions:**
- `_obs` (line 23) `def _obs(source, parsed, raw)` - *Build a minimal observation dict that matches the orchestrator shape.*

**Methods:**
- `generate_hypothences_safe` (line 127) `def generate_hypothences_safe(observations, entities)`
- `test_emits_domain_belongsto_actor_hypothesis` (line 42) `def test_emits_domain_belongsto_actor_hypothesis(self)`
- `test_score_in_high_band` (line 61) `def test_score_in_high_band(self)`
- `test_supporting_has_three_items` (line 76) `def test_supporting_has_three_items(self)`
- `test_sources_sorted_and_unique` (line 95) `def test_sources_sorted_and_unique(self)`
- `test_empty_observations_empty_entities` (line 116) `def test_empty_observations_empty_entities(self)`
- `test_empty_observations_only` (line 119) `def test_empty_observations_only(self)`
- `test_empty_entities_only` (line 122) `def test_empty_entities_only(self)`
- `test_observation_with_none_parsed_is_ignored` (line 141) `def test_observation_with_none_parsed_is_ignored(self)`
- `test_observation_without_source_is_ignored` (line 155) `def test_observation_without_source_is_ignored(self)`
- `test_unknown_source_uses_reliability_c` (line 179) `def test_unknown_source_uses_reliability_c(self)`
- `test_min_score_zero_returns_all` (line 202) `def test_min_score_zero_returns_all(self)`
- `test_min_score_one_filters_everything` (line 214) `def test_min_score_one_filters_everything(self)`
- `test_max_hypotheses_caps_output` (line 233) `def test_max_hypotheses_caps_output(self)`
- `test_observations_must_be_sequence` (line 256) `def test_observations_must_be_sequence(self)`
- `test_entities_must_be_sequence` (line 260) `def test_entities_must_be_sequence(self)`
- `test_min_score_out_of_range_raises` (line 264) `def test_min_score_out_of_range_raises(self)`
- `test_max_hypotheses_too_small_raises` (line 270) `def test_max_hypotheses_too_small_raises(self)`
- `test_hostile_value_is_truncated_or_skipped` (line 292) `def test_hostile_value_is_truncated_or_skipped(self, hostile)`
- `test_same_input_same_ids_and_scores` (line 312) `def test_same_input_same_ids_and_scores(self)`
- `test_input_order_does_not_affect_output` (line 333) `def test_input_order_does_not_affect_output(self)`
- `test_hypothesis_dataclass_is_frozen` (line 354) `def test_hypothesis_dataclass_is_frozen(self)`
- `test_evidence_dataclass_is_frozen` (line 370) `def test_evidence_dataclass_is_frozen(self)`
- `test_entity_ref_is_frozen` (line 382) `def test_entity_ref_is_frozen(self)`

#### `test_job_registry.py`
**Path:** `tests/test_job_registry.py`

**Functions:**
- `test_register_returns_value` (line 11) `def test_register_returns_value()`
- `test_size_cap_evicts_oldest` (line 17) `def test_size_cap_evicts_oldest()`
- `test_get_refreshes_lru_order` (line 28) `def test_get_refreshes_lru_order()`
- `test_ttl_eviction` (line 39) `def test_ttl_eviction()`
- `test_pop_removes_entry` (line 53) `def test_pop_removes_entry()`
- `test_keys_values_consistent` (line 61) `def test_keys_values_consistent()`
- `test_invalid_construction` (line 69) `def test_invalid_construction()`
- `test_replacement_does_not_evict` (line 76) `def test_replacement_does_not_evict()` - *Re-registering the same key keeps the size stable and LRU order intact.*

#### `test_pagination.py`
**Path:** `tests/test_pagination.py`

**Classes:**
- `TestPageStrategy` (line 21) `class TestPageStrategy` - *PG1: page param increments with each page number.*
- `TestOffsetStrategy` (line 48) `class TestOffsetStrategy` - *PG2: offset advances by page_size each page.*
- `TestCursorStrategy` (line 78) `class TestCursorStrategy` - *PG3: cursor extracted from response body.*
- `TestNoPagination` (line 128) `class TestNoPagination` - *PG4: default config means disabled.*
- `TestPartialPage` (line 151) `class TestPartialPage` - *PG5: fewer results than page_size signals last page.*
- `TestMaxPages` (line 180) `class TestMaxPages` - *PG6: max_pages limits total requests.*
- `TestFromDict` (line 205) `class TestFromDict` - *PaginationConfig construction from raw dict.*

**Methods:**
- `test_first_page_is_one` (line 24) `def test_first_page_is_one(self)`
- `test_second_page_increments` (line 29) `def test_second_page_increments(self)`
- `test_default_param_name` (line 34) `def test_default_param_name(self)`
- `test_no_pagination_returns_empty` (line 39) `def test_no_pagination_returns_empty(self)`
- `test_first_page_offset_zero` (line 51) `def test_first_page_offset_zero(self)`
- `test_second_page_offset_25` (line 56) `def test_second_page_offset_25(self)`
- `test_third_page_offset_50` (line 61) `def test_third_page_offset_50(self)`
- `test_custom_param_names` (line 66) `def test_custom_param_names(self)`
- `test_extracts_cursor_from_simple_path` (line 81) `def test_extracts_cursor_from_simple_path(self)`
- `test_extracts_cursor_from_nested_path` (line 86) `def test_extracts_cursor_from_nested_path(self)`
- `test_missing_path_returns_none` (line 91) `def test_missing_path_returns_none(self)`
- `test_empty_cursor_returns_none` (line 95) `def test_empty_cursor_returns_none(self)`
- `test_null_cursor_returns_none` (line 99) `def test_null_cursor_returns_none(self)`
- `test_non_dict_response_returns_none` (line 103) `def test_non_dict_response_returns_none(self)`
- `test_disabled_strategy_returns_none` (line 107) `def test_disabled_strategy_returns_none(self)`
- `test_build_params_empty_for_cursor` (line 111) `def test_build_params_empty_for_cursor(self)`
- `test_cursor_custom_param` (line 116) `def test_cursor_custom_param(self)`
- `test_default_config_disabled` (line 131) `def test_default_config_disabled(self)`
- `test_empty_dict_disabled` (line 135) `def test_empty_dict_disabled(self)`
- `test_none_disabled` (line 139) `def test_none_disabled(self)`
- `test_enabled_when_strategy_set` (line 143) `def test_enabled_when_strategy_set(self)`
- `test_partial_page_detected` (line 154) `def test_partial_page_detected(self)`
- `test_full_page_not_detected_as_partial` (line 159) `def test_full_page_not_detected_as_partial(self)`
- `test_list_response_counted_directly` (line 164) `def test_list_response_counted_directly(self)`
- `test_using_custom_response_list_path` (line 168) `def test_using_custom_response_list_path(self)`
- `test_default_max_pages` (line 183) `def test_default_max_pages(self)`
- `test_custom_max_pages` (line 187) `def test_custom_max_pages(self)`
- `test_zero_page_size_means_no_check` (line 193) `def test_zero_page_size_means_no_check(self)`
- `test_all_fields_mapped` (line 208) `def test_all_fields_mapped(self)`
- `test_partial_dict_uses_defaults` (line 230) `def test_partial_dict_uses_defaults(self)`
- `test_empty_string_strategy_disabled` (line 236) `def test_empty_string_strategy_disabled(self)`

#### `test_probabilistic_fusion.py`
**Path:** `tests/test_probabilistic_fusion.py`

**Classes:**
- `TestPrimarySourceRaisesLowConf` (line 48) `class TestPrimarySourceRaisesLowConf` - *PF1: tertiary first sighting → primary raises score.*
- `TestTertiaryCannotOverride` (line 77) `class TestTertiaryCannotOverride` - *PF2: untrusted_webscraper (F) cannot beat 0.9 existing.*
- `TestCorroborationLiftsScore` (line 110) `class TestCorroborationLiftsScore` - *PF3: multiple independent sources raise the score.*
- `TestMergeMonotonic` (line 142) `class TestMergeMonotonic` - *PF4: a lower-confidence sighting never decreases the score.*
- `TestFirstSightingWeighted` (line 170) `class TestFirstSightingWeighted` - *PF5: untrusted_webscraper first sighting is heavily discounted.*
- `TestRelationshipBayesian` (line 192) `class TestRelationshipBayesian` - *PF6: relationship from untrusted source cannot override primary.*
- `TestFusionStoreRegression` (line 217) `class TestFusionStoreRegression` - *Existing fusion store invariants must still hold.*

**Functions:**
- `_fs` (line 17) `def _fs()`
- `_teardown` (line 23) `def _teardown(store, tmp)`
- `_entity` (line 30) `def _entity(etype, value, source, confidence)`

**Methods:**
- `test_primary_source_raises_score` (line 51) `def test_primary_source_raises_score(self)`
- `test_untrusted_source_cannot_override` (line 80) `def test_untrusted_source_cannot_override(self)`
- `test_two_sources_are_better_than_one` (line 113) `def test_two_sources_are_better_than_one(self)`
- `test_lower_confidence_never_decreases` (line 145) `def test_lower_confidence_never_decreases(self)`
- `test_untrusted_first_sighting_discounted` (line 173) `def test_untrusted_first_sighting_discounted(self)`
- `test_relationship_untrusted_cannot_override` (line 195) `def test_relationship_untrusted_cannot_override(self)`
- `test_entity_id_deterministic` (line 220) `def test_entity_id_deterministic(self)`
- `test_entity_source_count_tracks` (line 229) `def test_entity_source_count_tracks(self)`
- `test_observation_count_advances` (line 243) `def test_observation_count_advances(self)`
- `test_empty_type_returns_empty` (line 259) `def test_empty_type_returns_empty(self)`
- `test_empty_value_returns_empty` (line 267) `def test_empty_value_returns_empty(self)`
- `test_add_observation_and_stats` (line 275) `def test_add_observation_and_stats(self)`
- `test_register_sources` (line 290) `def test_register_sources(self)`
- `test_search_entities` (line 305) `def test_search_entities(self)`
- `test_corroborated_properties` (line 320) `def test_corroborated_properties(self)`
- `test_get_entity_nonexistent` (line 333) `def test_get_entity_nonexistent(self)`
- `test_open_store_closes_gracefully` (line 340) `def test_open_store_closes_gracefully(self)`

#### `test_recon_fusion.py`
**Path:** `tests/test_recon_fusion.py`

**Classes:**
- `TestS1CriticalCorroborated` (line 46) `class TestS1CriticalCorroborated` - *S1 -- Happy path: corroborated by 5 sources -> CRITICAL.*
- `TestS2TwoReliableSources` (line 65) `class TestS2TwoReliableSources` - *S2 -- 2 sources with A/B reliability -> CRITICAL (via 2+ src + high rel).*
- `TestS3SingleHighReliability` (line 82) `class TestS3SingleHighReliability` - *S3 -- Single high-reliability source -> MEDIUM.*
- `TestS4SingleLowReliability` (line 102) `class TestS4SingleLowReliability` - *S4 -- Single F-reliability source -> NOISE.*
- `TestS5EmptyInput` (line 117) `class TestS5EmptyInput` - *S5 -- No observations or entities -> empty result.*
- `TestS6DirectMatchBoost` (line 130) `class TestS6DirectMatchBoost` - *S6 -- Direct match entity has boosted score.*
- `TestS7EmptyQuery` (line 147) `class TestS7EmptyQuery` - *S7 -- Empty query raises ValueError.*
- `TestS8BadConfig` (line 157) `class TestS8BadConfig` - *S8 -- Inconsistent thresholds raise ValueError.*
- `TestS9NoneObservations` (line 173) `class TestS9NoneObservations` - *S9 -- None observations handled safely.*
- `TestS10EntityWithoutType` (line 183) `class TestS10EntityWithoutType` - *S10 -- Entity without type is ignored.*
- `TestS11Dedup` (line 195) `class TestS11Dedup` - *S11 -- Identical observations deduped to one.*
- `TestS12Ordering` (line 212) `class TestS12Ordering` - *S12 -- Tiers ordered by relevance_score descending.*
- `TestIntegrationMultiEntity` (line 227) `class TestIntegrationMultiEntity` - *Integration: multiple entities classified across tiers.*
- `TestFusionResultDataclass` (line 252) `class TestFusionResultDataclass` - *FusionResult dataclass structural tests.*
- `TestRelevanceTierEnum` (line 267) `class TestRelevanceTierEnum` - *RelevanceTier enum members and ordering.*

**Functions:**
- `_observation` (line 14) `def _observation(source, category, parser, status, parsed)`
- `_entity` (line 31) `def _entity(etype, value, confidence, sources)`

**Methods:**
- `test_critical_with_5_sources` (line 49) `def test_critical_with_5_sources(self)`
- `test_two_reliable_sources_critical` (line 68) `def test_two_reliable_sources_critical(self)`
- `test_single_a_source_is_medium` (line 85) `def test_single_a_source_is_medium(self)`
- `test_single_f_source_is_noise` (line 105) `def test_single_f_source_is_noise(self)`
- `test_empty_observations_and_entities` (line 120) `def test_empty_observations_and_entities(self)`
- `test_direct_match_boosts_score` (line 133) `def test_direct_match_boosts_score(self)`
- `test_empty_query_raises` (line 150) `def test_empty_query_raises(self)`
- `test_bad_thresholds_raise` (line 160) `def test_bad_thresholds_raise(self)`
- `test_none_observations_safe` (line 176) `def test_none_observations_safe(self)`
- `test_entity_without_type_ignored` (line 186) `def test_entity_without_type_ignored(self)`
- `test_identical_observations_deduped` (line 198) `def test_identical_observations_deduped(self)`
- `test_tier_ordered_by_score` (line 215) `def test_tier_ordered_by_score(self)`
- `test_mixed_entities_across_tiers` (line 230) `def test_mixed_entities_across_tiers(self)`
- `test_fusion_result_serialisable` (line 255) `def test_fusion_result_serialisable(self)`
- `test_enum_members` (line 270) `def test_enum_members(self)`
- `test_enum_order_list` (line 277) `def test_enum_order_list(self)`

#### `test_reliability_scoring.py`
**Path:** `tests/test_reliability_scoring.py`

**Classes:**
- `TestHappyPathHighReliabilityCorroboratedFresh` (line 45) `class TestHappyPathHighReliabilityCorroboratedFresh` - *S1 del spec.*
- `TestUnknownSourceFallsBackToDefault` (line 109) `class TestUnknownSourceFallsBackToDefault` - *S2 del spec.*
- `TestZeroCorroborationYieldsZeroScore` (line 169) `class TestZeroCorroborationYieldsZeroScore` - *S3 del spec: una sola fuente, no importa lo fiable que sea, score = 0.*
- `TestVeryOldObservationDecaysToZero` (line 188) `class TestVeryOldObservationDecaysToZero` - *S4 del spec.*
- `TestInvalidInputRaisesValueError` (line 225) `class TestInvalidInputRaisesValueError` - *S5 del spec.*
- `TestHostileSourceNameIsHandledSafely` (line 270) `class TestHostileSourceNameIsHandledSafely` - *S6 del spec: input del operador, posiblemente adversario, no rompe.*
- `TestMergeReliableBeatsLessReliable` (line 299) `class TestMergeReliableBeatsLessReliable` - *S7 del spec.*
- `TestMergeUnreliableCannotRaise` (line 366) `class TestMergeUnreliableCannotRaise` - *S8 del spec.*
- `TestDeterminism` (line 412) `class TestDeterminism` - *S9 del spec: misma entrada → misma salida, bit a bit.*
- `TestBoundedSmoke` (line 453) `class TestBoundedSmoke` - *S10 del spec: smoke test del contrato de cota.*
- `TestSourceHierarchyPrimaryBeatsSecondaryBeatsTertiary` (line 483) `class TestSourceHierarchyPrimaryBeatsSecondaryBeatsTertiary` - *S11 del spec: mismo reliability, distinto source_type.*
- `TestSourceHierarchyPrimaryCBeatsTertiaryA` (line 550) `class TestSourceHierarchyPrimaryCBeatsTertiaryA` - *S12 del spec: source type compensates for lower reliability.*
- `TestSourceTypeFromName` (line 594) `class TestSourceTypeFromName` - *S13 del spec: lookup known and unknown source names.*
- `TestSourceHierarchyInMerge` (line 628) `class TestSourceHierarchyInMerge` - *S14 del spec: merge with source type hierarchy.*
- `TestSourceTypeWeightsBounded` (line 662) `class TestSourceTypeWeightsBounded` - *S15 del spec: source_type_weight is always in {1.00, 0.85, 0.60}.*

**Methods:**
- `test_score_in_high_band` (line 48) `def test_score_in_high_band(self)`
- `test_reliability_weight_is_one` (line 67) `def test_reliability_weight_is_one(self)`
- `test_freshness_weight_is_one_when_age_zero` (line 76) `def test_freshness_weight_is_one_when_age_zero(self)`
- `test_corroboration_weight_matches_log10` (line 86) `def test_corroboration_weight_matches_log10(self)`
- `test_credibility_weight_for_probably_true` (line 95) `def test_credibility_weight_for_probably_true(self)`
- `test_unknown_source_returns_default` (line 120) `def test_unknown_source_returns_default(self, name)`
- `test_unknown_source_produces_weak_score_with_one_corroboration` (line 126) `def test_unknown_source_produces_weak_score_with_one_corroboration(self)`
- `test_unknown_source_with_many_corroborators_reaches_high_band` (line 146) `def test_unknown_source_with_many_corroborators_reaches_high_band(self)`
- `test_zero_corroboration_collapses_score` (line 172) `def test_zero_corroboration_collapses_score(self)`
- `test_one_year_old_with_low_corroboration_decays` (line 191) `def test_one_year_old_with_low_corroboration_decays(self)`
- `test_freshness_is_monotonically_decreasing` (line 204) `def test_freshness_is_monotonically_decreasing(self)` - *Una observación más vieja siempre tiene freshness menor o igual.*
- `test_negative_corroboration_count_raises` (line 228) `def test_negative_corroboration_count_raises(self)`
- `test_negative_observation_age_raises` (line 235) `def test_negative_observation_age_raises(self)`
- `test_base_confidence_out_of_range_raises` (line 243) `def test_base_confidence_out_of_range_raises(self, bad)`
- `test_half_life_zero_raises` (line 250) `def test_half_life_zero_raises(self)`
- `test_half_life_negative_raises` (line 258) `def test_half_life_negative_raises(self)`
- `test_hostile_name_does_not_raise` (line 288) `def test_hostile_name_does_not_raise(self, hostile)`
- `test_new_a_source_raises_score` (line 302) `def test_new_a_source_raises_score(self)`
- `test_merge_takes_max_of_existing_and_new` (line 319) `def test_merge_takes_max_of_existing_and_new(self)`
- `test_merge_keeps_existing_when_new_is_weaker` (line 335) `def test_merge_keeps_existing_when_new_is_weaker(self)`
- `test_merge_result_is_always_bounded` (line 350) `def test_merge_result_is_always_bounded(self)`
- `test_f_source_against_strong_existing_keeps_existing` (line 369) `def test_f_source_against_strong_existing_keeps_existing(self)`
- `test_merge_existing_out_of_range_raises` (line 384) `def test_merge_existing_out_of_range_raises(self)`
- `test_merge_new_observation_out_of_range_raises` (line 396) `def test_merge_new_observation_out_of_range_raises(self)`
- `test_compute_confidence_is_pure` (line 415) `def test_compute_confidence_is_pure(self)`
- `test_merge_confidence_is_pure` (line 428) `def test_merge_confidence_is_pure(self)`
- `test_reliability_weights_match_nato_admiralty` (line 456) `def test_reliability_weights_match_nato_admiralty(self)`
- `test_credibility_weights_match_nato_admiralty` (line 465) `def test_credibility_weights_match_nato_admiralty(self)`
- `test_default_half_life_is_thirty_days` (line 473) `def test_default_half_life_is_thirty_days(self)`
- `test_default_credibility_is_cannot_be_judged` (line 476) `def test_default_credibility_is_cannot_be_judged(self)`
- `test_primary_tertiary_score_order` (line 486) `def test_primary_tertiary_score_order(self)`
- `test_primary_weight_is_one` (line 519) `def test_primary_weight_is_one(self)`
- `test_secondary_weight_is_085` (line 528) `def test_secondary_weight_is_085(self)`
- `test_tertiary_weight_is_060` (line 537) `def test_tertiary_weight_is_060(self)`
- `test_primary_c_beats_tertiary_a` (line 553) `def test_primary_c_beats_tertiary_a(self)`
- `test_primary_c_weight` (line 580) `def test_primary_c_weight(self)`
- `test_rdap_is_primary` (line 597) `def test_rdap_is_primary(self)`
- `test_leakcheck_is_tertiary` (line 600) `def test_leakcheck_is_tertiary(self)`
- `test_wikidata_is_secondary` (line 603) `def test_wikidata_is_secondary(self)`
- `test_shodan_is_secondary` (line 606) `def test_shodan_is_secondary(self)`
- `test_unknown_falls_back_to_default` (line 609) `def test_unknown_falls_back_to_default(self)`
- `test_none_falls_back` (line 612) `def test_none_falls_back(self)`
- `test_empty_falls_back` (line 615) `def test_empty_falls_back(self)`
- `test_hostile_input_does_not_raise` (line 618) `def test_hostile_input_does_not_raise(self)`
- `test_new_primary_raises_score` (line 631) `def test_new_primary_raises_score(self)`
- `test_new_tertiary_does_not_raise_weak_existing` (line 644) `def test_new_tertiary_does_not_raise_weak_existing(self)`
- `test_source_type_weights_are_exact` (line 665) `def test_source_type_weights_are_exact(self)`
- `test_primary_always_gives_one` (line 670) `def test_primary_always_gives_one(self)`
- `test_tertiary_always_gives_060` (line 679) `def test_tertiary_always_gives_060(self)`

#### `test_search_telemetry.py`
**Path:** `tests/test_search_telemetry.py`

**Functions:**
- `_render_index` (line 36) `def _render_index()` - *Render `index.html` exactly as the web layer does, telemetry included.*
- `test_s1_determinate_progress_midsearch` (line 52) `def test_s1_determinate_progress_midsearch()`
- `test_s2_indeterminate_progress` (line 67) `def test_s2_indeterminate_progress()`
- `test_s3_completion_stops_spinner` (line 79) `def test_s3_completion_stops_spinner()`
- `test_s4_out_of_range_is_clamped` (line 90) `def test_s4_out_of_range_is_clamped()`
- `test_s5_unknown_phase_rejected` (line 103) `def test_s5_unknown_phase_rejected()`
- `test_s6_catalog_is_brand_and_emoji_clean` (line 114) `def test_s6_catalog_is_brand_and_emoji_clean()`
- `test_s7_rendered_template_has_no_third_party_brand` (line 132) `def test_s7_rendered_template_has_no_third_party_brand()`
- `test_s8_rendered_chrome_has_no_emoji` (line 141) `def test_s8_rendered_chrome_has_no_emoji()`
- `test_s9_brand_predicate_boundaries` (line 153) `def test_s9_brand_predicate_boundaries()`
- `_valid_kwargs` (line 163) `def _valid_kwargs()`
- `test_s10_empty_brand_rejected` (line 178) `def test_s10_empty_brand_rejected()`
- `test_s10_no_tips_rejected` (line 185) `def test_s10_no_tips_rejected()`
- `test_s10_duplicate_phase_rejected` (line 192) `def test_s10_duplicate_phase_rejected()`
- `test_s10_emoji_in_catalog_rejected` (line 205) `def test_s10_emoji_in_catalog_rejected()`
- `test_s10_brand_collision_rejected` (line 212) `def test_s10_brand_collision_rejected()`
- `test_s10_missing_sentinel_phase_rejected` (line 219) `def test_s10_missing_sentinel_phase_rejected()`
- `test_s11_template_renders_from_catalog` (line 233) `def test_s11_template_renders_from_catalog()`
- `test_default_telemetry_is_a_shared_instance` (line 247) `def test_default_telemetry_is_a_shared_instance()`

#### `test_security_remediation.py`
**Path:** `tests/test_security_remediation.py`

**Classes:**
- `TestSsrfLogSanitisation` (line 25) `class TestSsrfLogSanitisation` - *BDD S1, S2: ssrf_guard._resolve log messages must not contain the
hostname or exception detail.*
- `TestInfoExposureEncryption` (line 75) `class TestInfoExposureEncryption` - *BDD S3, S4: encryption error endpoints must not leak str(e).*
- `TestInfoExposureSourceOps` (line 176) `class TestInfoExposureSourceOps` - *BDD S5, S6: source file operations must not leak str(e).*
- `TestHttpsRedirectSafety` (line 260) `class TestHttpsRedirectSafety` - *BDD S7: the HTTPS redirect must use request.host, not request.url.*
- `TestCiWorkflowPermissions` (line 306) `class TestCiWorkflowPermissions` - *BDD S10: .github/workflows/ci.yml must have permissions: read-all.*
- `TestOsirisExceptionSafety` (line 336) `class TestOsirisExceptionSafety` - *BDD S11: osiris endpoint exceptions must return generic error.*
- `TestWebSecurityRedirect` (line 399) `class TestWebSecurityRedirect` - *Verify the HTTP-to-HTTPS redirect in web_security.py is safe.*
- `TestJavaScriptDomSafety` (line 431) `class TestJavaScriptDomSafety` - *BDD S8, S9: verify no innerHTML with unsanitized data in JS.*

**Methods:**
- `test_dns_failure_log_omits_hostname` (line 29) `def test_dns_failure_log_omits_hostname(self, caplog)`
- `test_dns_failure_log_omits_ip_in_hostname` (line 43) `def test_dns_failure_log_omits_ip_in_hostname(self, caplog)`
- `test_dns_failure_log_contains_host_length_not_host` (line 55) `def test_dns_failure_log_contains_host_length_not_host(self, caplog)`
- `app` (line 79) `def app(self)`
- `_make_export_route` (line 86) `def _make_export_route(self, app, raise_val, error_msg, status)`
- `_make_export_route_fixed` (line 118) `def _make_export_route_fixed(self, app, raise_val, error_msg, status)`
- `test_encryption_valueerror_leaks_detail` (line 151) `def test_encryption_valueerror_leaks_detail(self, app)`
- `test_encryption_valueerror_fixed_no_detail` (line 159) `def test_encryption_valueerror_fixed_no_detail(self, app)`
- `test_encryption_runtimeerror_fixed_no_detail` (line 167) `def test_encryption_runtimeerror_fixed_no_detail(self, app)`
- `app` (line 180) `def app(self)`
- `test_source_delete_keyerror_fixed` (line 187) `def test_source_delete_keyerror_fixed(self, app)`
- `test_source_create_valueerror_fixed` (line 208) `def test_source_create_valueerror_fixed(self, app)`
- `test_source_update_valueerror_fixed` (line 232) `def test_source_update_valueerror_fixed(self, app)`
- `app` (line 264) `def app(self)`
- `test_redirect_uses_public_host_not_request_host` (line 271) `def test_redirect_uses_public_host_not_request_host(self, app)`
- `test_redirect_scheme_is_https` (line 285) `def test_redirect_scheme_is_https(self, app)`
- `test_ci_yml_has_permissions` (line 309) `def test_ci_yml_has_permissions(self)`
- `test_ci_yml_permissions_is_read_all` (line 325) `def test_ci_yml_permissions_is_read_all(self)`
- `app` (line 340) `def app(self)`
- `_make_osiris_route_fixed` (line 347) `def _make_osiris_route_fixed(self, app, route_path)`
- `test_osiris_exception_returns_generic` (line 386) `def test_osiris_exception_returns_generic(self, app)`
- `test_redirect_implementation_uses_public_host` (line 402) `def test_redirect_implementation_uses_public_host(self)`
- `test_source_has_no_url_replace` (line 418) `def test_source_has_no_url_replace(self)`
- `test_js_file_exists` (line 436) `def test_js_file_exists(self)`
- `test_innerhtml_not_used_with_template_literals` (line 439) `def test_innerhtml_not_used_with_template_literals(self)`
- `test_showtooltipat_safe` (line 459) `def test_showtooltipat_safe(self)` - *showTooltipAt must sanitize html before innerHTML assignment.*
- `test_selectnode_inspector_safe` (line 473) `def test_selectnode_inspector_safe(self)` - *selectNode must build DOM safely for the inspector panel.*
- `api_export_test` (line 97) `def api_export_test()`
- `api_export_fixed` (line 130) `def api_export_fixed()`
- `api_delete` (line 191) `def api_delete(name)`
- `api_create` (line 212) `def api_create()`
- `api_update` (line 236) `def api_update(name)`
- `fetch_bgp` (line 354) `def fetch_bgp(q)`
- `fetch_mac` (line 357) `def fetch_mac(mac)`
- `fetch_phone` (line 360) `def fetch_phone(n)`
- `fetch_github_user` (line 363) `def fetch_github_user(u)`
- `fetch_leaks` (line 366) `def fetch_leaks(e)`
- `osiris_endpoint` (line 376) `def osiris_endpoint()`

#### `test_source_health_monitoring.py`
**Path:** `tests/test_source_health_monitoring.py`

**Classes:**
- `TestHealthySource` (line 29) `class TestHealthySource` - *H1: high success rate, low latency -> HEALTHY.*
- `TestDegradingLowSuccess` (line 97) `class TestDegradingLowSuccess` - *H2: low success rate -> DEGRADING.*
- `TestDegradingHighLatency` (line 141) `class TestDegradingHighLatency` - *H3: high latency -> DEGRADING.*
- `TestStaleSource` (line 186) `class TestStaleSource` - *H4: long since last seen -> STALE.*
- `TestUnknownSource` (line 217) `class TestUnknownSource` - *H5: fetch_count < min_fetches -> UNKNOWN.*
- `TestDashboard` (line 248) `class TestDashboard` - *H6: dashboard filters by status.*
- `TestValidation` (line 348) `class TestValidation` - *H7: invalid inputs raise ValueError.*
- `TestDeterminism` (line 411) `class TestDeterminism` - *H8: same input -> same output.*
- `TestScoreBounded` (line 441) `class TestScoreBounded` - *H9 smoke: health_score is always in [0, 1].*
- `TestStatusAlwaysValid` (line 472) `class TestStatusAlwaysValid` - *H10: status is always a valid enum member.*
- `TestDataclassContract` (line 492) `class TestDataclassContract` - *All public types are frozen dataclasses with to_dict.*

**Methods:**
- `test_healthy_status` (line 32) `def test_healthy_status(self)`
- `test_success_rate_computed` (line 44) `def test_success_rate_computed(self)`
- `test_avg_latency_computed` (line 56) `def test_avg_latency_computed(self)`
- `test_freshness_hours_computed` (line 68) `def test_freshness_hours_computed(self)`
- `test_health_score_high_band` (line 80) `def test_health_score_high_band(self)`
- `test_degrading_status` (line 100) `def test_degrading_status(self)`
- `test_success_rate_reflects_failures` (line 112) `def test_success_rate_reflects_failures(self)`
- `test_health_score_low_band` (line 124) `def test_health_score_low_band(self)`
- `test_degrading_status_for_latency` (line 144) `def test_degrading_status_for_latency(self)`
- `test_avg_latency_high` (line 156) `def test_avg_latency_high(self)`
- `test_health_score_penalised` (line 168) `def test_health_score_penalised(self)`
- `test_stale_status` (line 189) `def test_stale_status(self)`
- `test_freshness_hours_exceeds_stale` (line 201) `def test_freshness_hours_exceeds_stale(self)`
- `test_unknown_status` (line 220) `def test_unknown_status(self)`
- `test_zero_fetches_is_unknown` (line 232) `def test_zero_fetches_is_unknown(self)`
- `_healthy` (line 252) `def _healthy(name)`
- `_degrading` (line 263) `def _degrading(name)`
- `_stale` (line 274) `def _stale(name)`
- `_unknown` (line 285) `def _unknown(name)`
- `test_hot_sources_are_healthy` (line 295) `def test_hot_sources_are_healthy(self)`
- `test_degrading_includes_degrading_and_stale` (line 306) `def test_degrading_includes_degrading_and_stale(self)`
- `test_unknown_sources_separate` (line 319) `def test_unknown_sources_separate(self)`
- `test_summary_counts` (line 329) `def test_summary_counts(self)`
- `test_ok_exceeds_fetch_raises` (line 351) `def test_ok_exceeds_fetch_raises(self)`
- `test_negative_fetch_raises` (line 362) `def test_negative_fetch_raises(self)`
- `test_negative_latency_raises` (line 373) `def test_negative_latency_raises(self)`
- `test_empty_name_raises` (line 384) `def test_empty_name_raises(self)`
- `test_config_min_fetches_less_than_one_raises` (line 395) `def test_config_min_fetches_less_than_one_raises(self)`
- `test_config_stale_hours_zero_raises` (line 399) `def test_config_stale_hours_zero_raises(self)`
- `test_config_degrading_rate_out_of_range_raises` (line 403) `def test_config_degrading_rate_out_of_range_raises(self)`
- `test_compute_health_is_pure` (line 414) `def test_compute_health_is_pure(self)`
- `test_build_dashboard_is_pure` (line 428) `def test_build_dashboard_is_pure(self)`
- `test_perfect_source_scores_one` (line 444) `def test_perfect_source_scores_one(self)`
- `test_broken_source_scores_low` (line 456) `def test_broken_source_scores_low(self)`
- `test_status_is_enum` (line 475) `def test_status_is_enum(self)`
- `test_health_input_is_dataclass` (line 495) `def test_health_input_is_dataclass(self)`
- `test_health_result_is_dataclass` (line 498) `def test_health_result_is_dataclass(self)`
- `test_config_is_dataclass` (line 501) `def test_config_is_dataclass(self)`
- `test_dashboard_is_dataclass` (line 505) `def test_dashboard_is_dataclass(self)`
- `test_result_to_dict` (line 508) `def test_result_to_dict(self)`
- `test_dashboard_to_dict` (line 523) `def test_dashboard_to_dict(self)`

#### `test_target_management.py`
**Path:** `tests/test_target_management.py`

**Classes:**
- `TestS1HappyPath` (line 21) `class TestS1HappyPath`
- `TestS2AutoDetect` (line 46) `class TestS2AutoDetect`
- `TestS3InvalidValue` (line 113) `class TestS3InvalidValue`
- `TestS4UnknownType` (line 140) `class TestS4UnknownType`
- `TestS5EmptyValue` (line 156) `class TestS5EmptyValue`
- `TestS6CaseStoreUnavailable` (line 174) `class TestS6CaseStoreUnavailable`
- `TestS7Batch` (line 186) `class TestS7Batch`
- `TestS8MaxBatch` (line 211) `class TestS8MaxBatch`
- `TestS9XSS` (line 228) `class TestS9XSS`
- `TestS10Determinism` (line 246) `class TestS10Determinism`
- `TestValidateType` (line 266) `class TestValidateType`
- `TestValidateValue` (line 280) `class TestValidateValue`
- `TestMakeTargetId` (line 333) `class TestMakeTargetId`
- `TestAutoDetectType` (line 344) `class TestAutoDetectType`
- `TestBatchResultSerialization` (line 367) `class TestBatchResultSerialization`
- `TestTargetResultSerialization` (line 379) `class TestTargetResultSerialization`
- `TestCsvImport` (line 410) `class TestCsvImport`

**Methods:**
- `test_valid_target_returns_result` (line 22) `def test_valid_target_returns_result(self)`
- `test_has_case_id` (line 30) `def test_has_case_id(self)`
- `test_id_deterministic` (line 35) `def test_id_deterministic(self)`
- `test_ipv4_auto` (line 47) `def test_ipv4_auto(self)`
- `test_ipv6_auto` (line 52) `def test_ipv6_auto(self)`
- `test_email_auto` (line 57) `def test_email_auto(self)`
- `test_cve_auto` (line 62) `def test_cve_auto(self)`
- `test_btc_auto` (line 67) `def test_btc_auto(self)`
- `test_eth_auto` (line 72) `def test_eth_auto(self)`
- `test_domain_auto` (line 77) `def test_domain_auto(self)`
- `test_username_fallback` (line 82) `def test_username_fallback(self)`
- `test_phone_auto` (line 87) `def test_phone_auto(self)`
- `test_asn_auto` (line 92) `def test_asn_auto(self)`
- `test_md5_auto` (line 97) `def test_md5_auto(self)`
- `test_sha256_auto` (line 102) `def test_sha256_auto(self)`
- `test_invalid_email` (line 114) `def test_invalid_email(self)`
- `test_invalid_ipv4` (line 119) `def test_invalid_ipv4(self)`
- `test_invalid_domain_script` (line 123) `def test_invalid_domain_script(self)`
- `test_invalid_url` (line 127) `def test_invalid_url(self)`
- `test_invalid_phone` (line 131) `def test_invalid_phone(self)`
- `test_unknown_type` (line 141) `def test_unknown_type(self)`
- `test_unknown_type_via_manager` (line 146) `def test_unknown_type_via_manager(self)`
- `test_empty_raises` (line 157) `def test_empty_raises(self)`
- `test_whitespace_raises` (line 161) `def test_whitespace_raises(self)`
- `test_validate_value_empty` (line 165) `def test_validate_value_empty(self)`
- `test_ephemeral_no_case_store` (line 175) `def test_ephemeral_no_case_store(self)`
- `test_mixed_batch` (line 187) `def test_mixed_batch(self)`
- `test_simple_lines_no_type` (line 201) `def test_simple_lines_no_type(self)`
- `test_exceeds_max` (line 212) `def test_exceeds_max(self)`
- `test_at_max` (line 217) `def test_at_max(self)`
- `test_script_in_domain_rejected` (line 229) `def test_script_in_domain_rejected(self)`
- `test_onclick_in_domain_rejected` (line 233) `def test_onclick_in_domain_rejected(self)`
- `test_sql_injection_in_email_rejected` (line 237) `def test_sql_injection_in_email_rejected(self)`
- `test_same_id` (line 247) `def test_same_id(self)`
- `test_same_id_normalised` (line 255) `def test_same_id_normalised(self)`
- `test_valid_types_pass` (line 267) `def test_valid_types_pass(self)`
- `test_auto_passes` (line 272) `def test_auto_passes(self)`
- `test_invalid_fails` (line 275) `def test_invalid_fails(self)`
- `test_domain_valid` (line 281) `def test_domain_valid(self)`
- `test_domain_invalid` (line 285) `def test_domain_invalid(self)`
- `test_ipv4_valid` (line 289) `def test_ipv4_valid(self)`
- `test_ipv4_invalid_octet` (line 293) `def test_ipv4_invalid_octet(self)`
- `test_email_valid` (line 297) `def test_email_valid(self)`
- `test_url_only_http_https` (line 301) `def test_url_only_http_https(self)`
- `test_username_no_regex` (line 306) `def test_username_no_regex(self)`
- `test_cve_valid` (line 310) `def test_cve_valid(self)`
- `test_btc_valid` (line 313) `def test_btc_valid(self)`
- `test_eth_valid` (line 316) `def test_eth_valid(self)`
- `test_phone_valid` (line 319) `def test_phone_valid(self)`
- `test_asn_valid` (line 322) `def test_asn_valid(self)`
- `test_md5_valid` (line 325) `def test_md5_valid(self)`
- `test_sha256_valid` (line 328) `def test_sha256_valid(self)`
- `test_length` (line 334) `def test_length(self)`
- `test_deterministic` (line 337) `def test_deterministic(self)`
- `test_case_sensitive_normalised` (line 340) `def test_case_sensitive_normalised(self)`
- `test_ipv4` (line 345) `def test_ipv4(self)`
- `test_ipv6` (line 348) `def test_ipv6(self)`
- `test_email` (line 351) `def test_email(self)`
- `test_domain` (line 354) `def test_domain(self)`
- `test_url` (line 357) `def test_url(self)`
- `test_cve` (line 360) `def test_cve(self)`
- `test_username_fallback` (line 363) `def test_username_fallback(self)`
- `test_to_dict` (line 368) `def test_to_dict(self)`
- `test_to_dict` (line 380) `def test_to_dict(self)`
- `test_to_dict_invalid` (line 397) `def test_to_dict_invalid(self)`
- `test_basic_csv` (line 411) `def test_basic_csv(self)`
- `test_csv_invalid` (line 418) `def test_csv_invalid(self)`
- `test_csv_max_batch` (line 425) `def test_csv_max_batch(self)`
- `test_csv_exceeds_max` (line 431) `def test_csv_exceeds_max(self)`

#### `test_ui_professional.py`
**Path:** `tests/test_ui_professional.py`

**Classes:**
- `TestS1LoadingAnimation` (line 64) `class TestS1LoadingAnimation` - *S1 -- Loading indicator elements exist in the DOM.*
- `TestS2CriticalExpanded` (line 93) `class TestS2CriticalExpanded` - *S2 -- CRITICAL tier renders expanded with correct badge count.*
- `TestS3NoiseCollapsed` (line 119) `class TestS3NoiseCollapsed`
- `TestS4ToggleExpandCollapse` (line 143) `class TestS4ToggleExpandCollapse`
- `TestS5FallbackFlatView` (line 157) `class TestS5FallbackFlatView`
- `TestS6LoadingTimeout` (line 175) `class TestS6LoadingTimeout`
- `TestS7HoverEffect` (line 184) `class TestS7HoverEffect`
- `TestS8FadeInTransition` (line 197) `class TestS8FadeInTransition`
- `TestS9SecurityCSP` (line 211) `class TestS9SecurityCSP`
- `TestS10XSSSafe` (line 244) `class TestS10XSSSafe`
- `TestIntegrationTierPipeline` (line 262) `class TestIntegrationTierPipeline`

**Functions:**
- `_render_index` (line 27) `def _render_index()`
- `_simulate_tiered_data` (line 39) `def _simulate_tiered_data()`

**Methods:**
- `test_loading_elements_exist` (line 67) `def test_loading_elements_exist(self)`
- `test_loading_css_defined` (line 74) `def test_loading_css_defined(self)`
- `test_js_show_working_indicator_exists` (line 83) `def test_js_show_working_indicator_exists(self)`
- `test_critical_tier_data` (line 96) `def test_critical_tier_data(self)`
- `test_critical_css_classes_exist` (line 105) `def test_critical_css_classes_exist(self)`
- `test_noise_tier_data` (line 120) `def test_noise_tier_data(self)`
- `test_noise_css_classes_exist` (line 127) `def test_noise_css_classes_exist(self)`
- `test_js_toggle_function_exists` (line 134) `def test_js_toggle_function_exists(self)`
- `test_aria_attributes_in_js` (line 144) `def test_aria_attributes_in_js(self)`
- `test_toggle_uses_role_button` (line 149) `def test_toggle_uses_role_button(self)`
- `test_js_fallback_logic` (line 158) `def test_js_fallback_logic(self)`
- `test_tiers_missing_returns_empty` (line 163) `def test_tiers_missing_returns_empty(self)`
- `test_show_toast_exists` (line 176) `def test_show_toast_exists(self)`
- `test_tier_group_hover_css` (line 185) `def test_tier_group_hover_css(self)`
- `test_transition_on_tier_group` (line 189) `def test_transition_on_tier_group(self)`
- `test_fade_in_css_exists` (line 198) `def test_fade_in_css_exists(self)`
- `test_results_use_fade_in` (line 203) `def test_results_use_fade_in(self)`
- `test_no_inline_style_in_tier_badge` (line 212) `def test_no_inline_style_in_tier_badge(self)`
- `test_no_inline_style_in_template` (line 222) `def test_no_inline_style_in_template(self)`
- `test_no_onclick_attributes` (line 233) `def test_no_onclick_attributes(self)`
- `test_escape_html_function_exists` (line 245) `def test_escape_html_function_exists(self)`
- `test_escape_html_properly_defined` (line 249) `def test_escape_html_properly_defined(self)`
- `test_tier_label_uses_text_content` (line 254) `def test_tier_label_uses_text_content(self)`
- `test_tier_summary_accuracy` (line 263) `def test_tier_summary_accuracy(self)`
- `test_every_group_has_required_fields` (line 268) `def test_every_group_has_required_fields(self)`
- `test_scores_are_normalised` (line 280) `def test_scores_are_normalised(self)`

#### `split_sources.py`
**Path:** `tools/split_sources.py`

**Functions:**
- `main` (line 19) `def main()`

#### `web.py`
**Path:** `web.py`

*No symbols extracted*

#### `wsgi.py`
**Path:** `wsgi.py`

*No symbols extracted*

### SH (2 files)

#### `_multi_test.sh`
**Path:** `_multi_test.sh`

*No symbols extracted*

#### `install.sh`
**Path:** `install.sh`
**File Doc:** *Bootstrap a venv and install the runtime + optional test dependencies.  Idempotent: re-running on an existing venv is a no-op for the venv step. Tries the full install first (kuzu + aiohttp_socks + gunicorn), then degrades gracefully if a native dep fails to build (e.g. ARM Kali).  Usage: ./install.sh           install everything ./install.sh --minimal install only the minimum required deps ./install.sh --dev     also install test/lint extras*

**Functions:**
- `install_full` (line 51) - *3) Two install passes: full first, minimal fallback. We don't want a single Cython build error to leave the user with a half-installed project — better to fall back to a working baseline and tell them what didn't make it.*
- `install_minimal` (line 55)
