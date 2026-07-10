# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM.
> No LLMs. No tokens. Pure static analysis. See more [here](https://github.com/grisuno/ReadMenator) 

**Total Files Parsed:** 89 | **Total Symbols Extracted:** 1621 | **Total Imports:** 665

## Structural Knowledge Map
> **Note:** The visual graph below has been intelligently pruned to the top 300 most relevant nodes to prevent rendering crashes. Full details of all 89 files are documented below.

```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray: 5 5,color:#aaa;
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
    estorides_core_config_py["config.py (py)"]
    class estorides_core_config_py mod;
    estorides_core_config_py__env_int["_env_int"]
    class estorides_core_config_py__env_int fn;
    estorides_core_config_py --> estorides_core_config_py__env_int
    estorides_core_config_py__env_float["_env_float"]
    class estorides_core_config_py__env_float fn;
    estorides_core_config_py --> estorides_core_config_py__env_float
    estorides_core_config_py__env_bool["_env_bool"]
    class estorides_core_config_py__env_bool fn;
    estorides_core_config_py --> estorides_core_config_py__env_bool
    estorides_core_config_py_ensure_data_dirs["ensure_data_dirs"]
    class estorides_core_config_py_ensure_data_dirs fn;
    estorides_core_config_py --> estorides_core_config_py_ensure_data_dirs
    estorides_core_config_py_ensure_reports_dir["ensure_reports_dir"]
    class estorides_core_config_py_ensure_reports_dir fn;
    estorides_core_config_py --> estorides_core_config_py_ensure_reports_dir
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
    estorides_core_source_health_monitoring_py["source_health_monitoring.py (py)"]
    class estorides_core_source_health_monitoring_py mod;
    estorides_core_source_health_monitoring_py__env_float["_env_float"]
    class estorides_core_source_health_monitoring_py__env_float fn;
    estorides_core_source_health_monitoring_py --> estorides_core_source_health_monitoring_py__env_float
    estorides_core_source_health_monitoring_py__env_int["_env_int"]
    class estorides_core_source_health_monitoring_py__env_int fn;
    estorides_core_source_health_monitoring_py --> estorides_core_source_health_monitoring_py__env_int
    estorides_core_source_health_monitoring_py_SourceHealthStatus["SourceHealthStatus"]
    class estorides_core_source_health_monitoring_py_SourceHealthStatus cls;
    estorides_core_source_health_monitoring_py --> estorides_core_source_health_monitoring_py_SourceHealthStatus
    estorides_core_source_health_monitoring_py_SourceHealthConfig["SourceHealthConfig"]
    class estorides_core_source_health_monitoring_py_SourceHealthConfig cls;
    estorides_core_source_health_monitoring_py --> estorides_core_source_health_monitoring_py_SourceHealthConfig
    estorides_core_source_health_monitoring_py_SourceHealthInput["SourceHealthInput"]
    class estorides_core_source_health_monitoring_py_SourceHealthInput cls;
    estorides_core_source_health_monitoring_py --> estorides_core_source_health_monitoring_py_SourceHealthInput
    tests_test_auth_gate_py["test_auth_gate.py (py)"]
    class tests_test_auth_gate_py mod;
    tests_test_auth_gate_py_app_with_gate["app_with_gate"]
    class tests_test_auth_gate_py_app_with_gate fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_app_with_gate
    tests_test_auth_gate_py_test_gate_off_by_default["test_gate_off_by_default"]
    class tests_test_auth_gate_py_test_gate_off_by_default fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_off_by_default
    tests_test_auth_gate_py_test_gate_on_rejects_anonymous["test_gate_on_rejects_anonymous"]
    class tests_test_auth_gate_py_test_gate_on_rejects_anonymous fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_on_rejects_anonymous
    tests_test_auth_gate_py_test_gate_on_accepts_bearer_header["test_gate_on_accepts_bearer_header"]
    class tests_test_auth_gate_py_test_gate_on_accepts_bearer_header fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_on_accepts_bearer_header
    tests_test_auth_gate_py_test_gate_on_accepts_alt_header["test_gate_on_accepts_alt_header"]
    class tests_test_auth_gate_py_test_gate_on_accepts_alt_header fn;
    tests_test_auth_gate_py --> tests_test_auth_gate_py_test_gate_on_accepts_alt_header
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
    tests_properties_test_csp_safe_styles_properties_py_test_js_never_gains_a_style_attribute_in_template_literal["test_js_never_gains_a_style_attribute_in_template_literal"]
    class tests_properties_test_csp_safe_styles_properties_py_test_js_never_gains_a_style_attribute_in_template_literal fn;
    tests_properties_test_csp_safe_styles_properties_py --> tests_properties_test_csp_safe_styles_properties_py_test_js_never_gains_a_style_attribute_in_template_literal
    tests_properties_test_csp_safe_styles_properties_py_test_template_never_gains_a_style_attribute["test_template_never_gains_a_style_attribute"]
    class tests_properties_test_csp_safe_styles_properties_py_test_template_never_gains_a_style_attribute fn;
    tests_properties_test_csp_safe_styles_properties_py --> tests_properties_test_csp_safe_styles_properties_py_test_template_never_gains_a_style_attribute
    tests_properties_test_csp_safe_styles_properties_py_test_csp_style_src_never_gains_unsafe_inline["test_csp_style_src_never_gains_unsafe_inline"]
    class tests_properties_test_csp_safe_styles_properties_py_test_csp_style_src_never_gains_unsafe_inline fn;
    tests_properties_test_csp_safe_styles_properties_py --> tests_properties_test_csp_safe_styles_properties_py_test_csp_style_src_never_gains_unsafe_inline
    tests_test_reliability_scoring_py["test_reliability_scoring.py (py)"]
    class tests_test_reliability_scoring_py mod;
    tests_test_reliability_scoring_py_TestHappyPathHighReliabilityCorroboratedFresh["TestHappyPathHighReliabilityCorroboratedFresh"]
    class tests_test_reliability_scoring_py_TestHappyPathHighReliabilityCorroboratedFresh cls;
    tests_test_reliability_scoring_py --> tests_test_reliability_scoring_py_TestHappyPathHighReliabilityCorroboratedFresh
    tests_test_reliability_scoring_py_TestUnknownSourceFallsBackToDefault["TestUnknownSourceFallsBackToDefault"]
    class tests_test_reliability_scoring_py_TestUnknownSourceFallsBackToDefault cls;
    tests_test_reliability_scoring_py --> tests_test_reliability_scoring_py_TestUnknownSourceFallsBackToDefault
    tests_test_reliability_scoring_py_TestZeroCorroborationYieldsZeroScore["TestZeroCorroborationYieldsZeroScore"]
    class tests_test_reliability_scoring_py_TestZeroCorroborationYieldsZeroScore cls;
    tests_test_reliability_scoring_py --> tests_test_reliability_scoring_py_TestZeroCorroborationYieldsZeroScore
    tests_test_reliability_scoring_py_TestVeryOldObservationDecaysToZero["TestVeryOldObservationDecaysToZero"]
    class tests_test_reliability_scoring_py_TestVeryOldObservationDecaysToZero cls;
    tests_test_reliability_scoring_py --> tests_test_reliability_scoring_py_TestVeryOldObservationDecaysToZero
    tests_test_reliability_scoring_py_TestInvalidInputRaisesValueError["TestInvalidInputRaisesValueError"]
    class tests_test_reliability_scoring_py_TestInvalidInputRaisesValueError cls;
    tests_test_reliability_scoring_py --> tests_test_reliability_scoring_py_TestInvalidInputRaisesValueError
    estorides_core_parsers_py["parsers.py (py)"]
    class estorides_core_parsers_py mod;
    estorides_core_parsers_py__flat["_flat"]
    class estorides_core_parsers_py__flat fn;
    estorides_core_parsers_py --> estorides_core_parsers_py__flat
    estorides_core_parsers_py__first["_first"]
    class estorides_core_parsers_py__first fn;
    estorides_core_parsers_py --> estorides_core_parsers_py__first
    estorides_core_parsers_py_parse_dns_json["parse_dns_json"]
    class estorides_core_parsers_py_parse_dns_json fn;
    estorides_core_parsers_py --> estorides_core_parsers_py_parse_dns_json
    estorides_core_parsers_py_parse_crtsh_json["parse_crtsh_json"]
    class estorides_core_parsers_py_parse_crtsh_json fn;
    estorides_core_parsers_py --> estorides_core_parsers_py_parse_crtsh_json
    estorides_core_parsers_py_parse_rdap["parse_rdap"]
    class estorides_core_parsers_py_parse_rdap fn;
    estorides_core_parsers_py --> estorides_core_parsers_py_parse_rdap
    tests_test_probabilistic_fusion_py["test_probabilistic_fusion.py (py)"]
    class tests_test_probabilistic_fusion_py mod;
```

---

## Architecture Reference

### JS (1 files)

#### `estorides.js`
**Path:** `static/js/estorides.js`

**Classs:**
- `to` (line 301) - *Panels are keyed by the `<name>-canvas` class, not by id (the map panel's*
- `on` (line 1400) - *Geolocated entities (parsed.lat / parsed.lon) AND country codes. Many parsers stash coords on the entity itself (e.g. abuseipdb has a "countryCode"...*

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
- `replotStreamData` (line 343) - *Rebuild the geospatial + temporal views from everything seen so far. plotPoints clears and redraws from the full coord set, so feeding it the accum...*
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
- `mergeExpansionIntoGraph` (line 722) - *Merge a /api/intel/resolve response into the current D3 graph and Leaflet map. Idempotent: re-clicking the same node won't duplicate edges. Returns...*
- `drawGraphWithExtras` (line 782) - *Re-draws the D3 graph with the original nodes/edges PLUS any extras passed in (from a /api/intel/resolve call). The extras are translated to the sh...*
- `pushLink` (line 806)
- `resolverTypeFor` (line 840) - *Map a graph node's type/kind onto a resolver/transform entity type.*
- `saveLevelOverrides` (line 856)
- `levelOf` (line 860)
- `clusterColor` (line 864)
- `deriveClusters` (line 872) - *Build a clusters[] summary from a flat node list (used after a merge when the server-side clusters array isn't carried along).*
- `hideTooltip` (line 885) - *--- floating overlays (tooltip + context menu) ----*
- `showTooltipAt` (line 889)
- `hideContextMenu` (line 899)
- `showBridgeTooltip` (line 905) - *Cross-referenced tooltip for an inter-cluster (bridge) link.*
- `showNodeTooltip` (line 934)
- `showContextMenu` (line 943) - *--- context menu: transforms grouped by intel tier ----*
- `setNodeLevel` (line 1008)
- `applyLevelStyles` (line 1017) - *Re-apply level rings to every rendered node circle.*
- `focusNode` (line 1025)
- `runTransform` (line 1037) - *Run a graph pivot transform and merge the result into the graph+map.*
- `selectNode` (line 1055) - *--- side inspector panel ----*
- `renderGraphCore` (line 1114) - *--- unified force-graph renderer (clusters + rings + interactions) ----*
- `drawHulls` (line 1184)
- `_redrawGraph` (line 1215) - *Low-level D3 redraw given a flat nodes/links list (back-compat shim).*
- `setStatusDot` (line 1221) - *--- Professional UI enhancements (relevance tiers, loading) ----*
- `showWorkingIndicator` (line 1227)
- `hideWorkingIndicator` (line 1232)
- `toggleTierSection` (line 1237)
- `renderTieredResults` (line 1245)
- `escapeAttr` (line 1311)
- `buildMapCoords` (line 1347)
- `validCoord` (line 1443)
- `colorFor` (line 1447)
- `renderEntities` (line 1466)
- `renderGraphSummary` (line 1516)
- `colorForKind` (line 1545)
- `renderTimeline` (line 1553)
- `fmtTime` (line 1603)
- `filterTimeline` (line 1614)
- `drawGraph` (line 1663) - *--- D3 graph view ----*
- `loadCases` (line 1694)
- `renderCaseItem` (line 1721)
- `debounce` (line 1747)
- `escapeHTML` (line 1796) - *--- utils ----*
- `truncate` (line 1801)
- `caseActionSave` (line 1824) - *Bookmark a case. The endpoint prefixes the notes column with "[saved]" so the bookmarked case surfaces in the list at a glance.*
- `caseActionDiff` (line 1844) - *Compare this case to another. The user picks the baseline; the response is rendered inline in a diff panel under the case.*
- `renderCaseDiffPanel` (line 1862) - *Render the diff result below the case. The panel survives until the user reloads the cases list (or opens another diff).*
- `caseActionReport` (line 1903) - *Render the Markdown report. We just dump the text into a modal overlay — keeping it in-browser is enough; the CLI command produces a file copy for ...*
- `showReportModal` (line 1939)
- `loadSidebarWidth` (line 2031) - *Responsive sidebar toggle + resizable divider.*
- `saveSidebarWidth` (line 2042)
- `loadSidebarCollapsed` (line 2045)
- `saveSidebarCollapsed` (line 2053)
- `switchSidebarTab` (line 2111) - *--- Fusion tab ----*
- `loadFusionTab` (line 2120)
- `loadFusionStats` (line 2126)
- `loadFusionTopChanged` (line 2145)
- `loadFusionSearch` (line 2168)
- `doSearch` (line 2175)
- `loadFusionEntityDetail` (line 2207)
- `setStatus` (line 2272) - *The discoverer code lives outside the IIFE, so the module-private setStatus is not in scope here. Provide a global one that writes to the*
- `setDiscoverProgress` (line 2279)
- `hideDiscoverProgress` (line 2291)
- `startDiscover` (line 2296)
- `stopDiscover` (line 2370)
- `handleDiscoverEvent` (line 2387)
- `addDiscoverEntityToTab` (line 2426)
- `escapeHtml` (line 2454)
- `maybePlotDiscoverEntity` (line 2459)
- `flushDiscoverEntities` (line 2466)
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
- `labelFor` (line 908)
- `c` (line 909)
- `tr` (line 988)
- `tr` (line 1091)
- `obs` (line 1557)
- `frac` (line 1590)
- `q` (line 1695)
- `saved` (line 1725) - *Saved cases get a visible bookmark pill so the operator can scan the list for "things I came back to" at a glance.*
- `rows` (line 1870)
- `removed` (line 1873)
- `tag` (line 2001)
- `sig` (line 2431) - *Avoid duplicates with the simple in-memory check.*

### PY (86 files)

#### `_test_entity_resolution.py`
**Path:** `_test_entity_resolution.py`

**Functions:**
- `check` (line 27)
- `_ent` (line 36)
- `_by_value` (line 40)
- `test_transliteration` (line 47)
- `test_jaro_winkler` (line 63)
- `test_normalization` (line 74)
- `test_score_pair_policy` (line 98)
- `test_resolution_merge` (line 111)
- `test_to_entity_roundtrip` (line 167)
- `test_cross_run_stability` (line 182)
- `test_empty_and_edge_inputs` (line 211)
- `main` (line 219)

#### `_test_fusion.py`
**Path:** `_test_fusion.py`

**Functions:**
- `check` (line 24)
- `_fresh_store` (line 32)
- `test_deterministic_identity` (line 37)
- `test_cross_run_dedup_and_provenance` (line 45)
- `test_property_corroboration_and_conflict` (line 59)
- `test_min_sources_filter` (line 76)
- `test_relationship_fusion` (line 87)
- `test_observation_and_source_counters` (line 97)
- `test_fail_soft_open` (line 116)
- `main` (line 124)

#### `_test_hardening.py`
**Path:** `_test_hardening.py`

**Functions:**
- `_ok` (line 25)
- `test_security_headers` (line 36)
- `test_cors_default_off` (line 53) - *Without ESTORIDES_CORS_ORIGINS, CORS headers must not be emitted.*
- `test_cors_allowlist` (line 62) - *With an allowlist, only matching origins get a CORS header.*
- `test_debug_killswitch` (line 87) - *When DEBUG is on, install_security must refuse to run.*
- `test_max_body_rejection` (line 101) - *A request body larger than MAX_CONTENT_LENGTH must be rejected.*
- `test_case_diff` (line 113)
- `test_case_diff_endpoints` (line 137)
- `test_case_save_endpoint` (line 148)
- `test_report_renders` (line 165)
- `test_report_with_diff` (line 181)
- `test_console_script_help` (line 196) - *`./estorides` must run even without `pip install -e .`.*
- `main` (line 210)

#### `_test_passive.py`
**Path:** `_test_passive.py`

**Functions:**
- `check` (line 20)
- `main` (line 29)

#### `_test_people.py`
**Path:** `_test_people.py`

**Classs:**
- `_StubRunner` (line 66)

**Functions:**
- `check` (line 21)
- `_types` (line 30)
- `main` (line 37)
- `run` (line 67)

#### `_test_proxy.py`
**Path:** `_test_proxy.py`

**Functions:**
- `check` (line 21)
- `main` (line 30)
- `_enter_and_rotate` (line 52)
- `_enter_socks` (line 72)

#### `_test_scope.py`
**Path:** `_test_scope.py`

**Functions:**
- `check` (line 18)
- `main` (line 27)

#### `_validate.py`
**Path:** `_validate.py`

**Functions:**
- `main` (line 17)

#### `app.py`
**Path:** `app.py`

*No symbols extracted*

#### `estorides_cli.py`
**Path:** `estorides_cli.py`

**Functions:**
- `_setup_logging` (line 36)
- `_collect_selectors` (line 43) - *Group discovered entity values by type for the requested type set.

Used to surface the human selectors (emails, usernames, persons, orgs,
phones) a discover run found, separately from the infrastructure list.*
- `_resolve_proxy` (line 59) - *Resolve the egress proxy from the OPSEC flags.

`--tor` is a convenience alias for the default local Tor SOCKS port;
an explicit `--proxy` wins over it. Returns None when neither is set,
in which case the engine still honours the env-configured proxy pool.*
- `_add_opsec_flags` (line 72) - *Attach the shared operator-OPSEC flags to a subcommand parser.*
- `cmd_discover` (line 90) - *v1.2 — fanout the surface from a seed.

Mirrors the /api/discover/start endpoint but as a CLI subcommand
so an operator can drop a seed in a terminal and walk away.
Streams progress to stdout. The final case is dumped to
--out-json if provided.*
- `cmd_run` (line 202)
- `cmd_scope` (line 279) - *Classify discovered assets against a program's scope rules.

Reads assets (a `discover --out-json` surface or a flat host list),
applies the in/out-of-scope rules, and emits the in-scope host/IP
lists an operator pipes into the active phase. Out-of-scope assets are
surfaced explicitly so they are never targeted by accident.*
- `cmd_graph_export` (line 326)
- `cmd_export_stix` (line 349)
- `cmd_export_misp` (line 359)
- `cmd_report` (line 369) - *Render a Markdown report for a case.

Reads from the case store (so the report reflects what was persisted,
not the volatile in-memory graph). When `--diff <other_id>` is given,
the report also includes a "what's new" section vs the other case.*
- `cmd_diff` (line 410) - *Diff two cases. CLI twin of /api/cases/diff.*
- `cmd_status` (line 438)
- `cmd_fusion` (line 445) - *Query the cross-run fusion datastore.

Subactions:
  stats              size of the fused fact base
  sources            YAML catalogue with fetch/ok counters
  entities [TERM]    search fused entities (``--type``, ``--min-sources``)
  entity ID          full fused view of one entity (provenance + props)*
- `cmd_serve` (line 486)
- `build_parser` (line 503)
- `main` (line 604)
- `_on_done` (line 219)

#### `__init__.py`
**Path:** `estorides_core/__init__.py`

*No symbols extracted*

#### `async_client.py`
**Path:** `estorides_core/async_client.py`

**Classs:**
- `CircuitBreaker` (line 56) - *Per-host circuit breaker.*
- `ResponseCache` (line 78) - *SQLite-backed response cache. Key = (url + method + body hash).

Entries carry their write timestamp and are only served while younger
than `ttl_seconds`; a stale row is ignored (and lazily overwritten on
the next live fetch) so the cache can never pin down OSINT that has
since changed or been taken down.*
- `AsyncClient` (line 149) - *Async HTTP client with retries, backoff, circuit breaker, cache.*

**Functions:**
- `_is_socks` (line 41) - *True when the proxy URL is a SOCKS proxy (e.g. Tor).*
- `_redact_proxy` (line 46) - *Strip any `user:pass@` credentials from a proxy URL before logging.*
- `sync_fetch` (line 375)
- `allow` (line 61)
- `record_success` (line 67)
- `record_failure` (line 71)
- `__init__` (line 87)
- `_init_db` (line 100)
- `_key` (line 113)
- `get` (line 122)
- `set` (line 138)
- `__init__` (line 152)
- `__aenter__` (line 181)
- `_next_http_proxy` (line 225) - *Round-robin the next HTTP proxy, or None (SOCKS/connector or direct).*
- `__aexit__` (line 233)
- `session` (line 239)
- `fetch` (line 245) - *Fetch a URL. Returns (parsed_data, meta).

meta contains status, content_type, cached, attempts, error.
parsed_data is dict/list/str/None depending on content-type.*

#### `audit.py`
**Path:** `estorides_core/audit.py`

**Classs:**
- `AuditEvent` (line 55)
- `AuditLog` (line 72) - *Append-only JSONL audit log with a size cap.

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
- `RateLimiter` (line 180) - *In-process sliding-window rate limiter.

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

**Functions:**
- `to_jsonl` (line 68)
- `__init__` (line 90)
- `record` (line 104)
- `_maybe_rotate_locked` (line 115) - *If the active file is over the cap, rotate in place.

Caller must hold `self._lock`. We use a per-write stat-then-
write sequence; the race window (another process also writing)
is acceptable for a single-tenant audit log — the worst case
is a slightly oversized file, not data loss.*
- `query` (line 150)
- `__init__` (line 201)
- `allow` (line 214) - *Return (allowed, retry_after_seconds).

`retry_after_seconds` is 0 when allowed, otherwise the number of
seconds the caller should wait before retrying.

The configured `max_requests` is re-read from the environment on
every call so an operator can hot-tune the limit without a
process restart. (The window itself is stable for a process
lifetime, which is fine for our deployment shape.)*
- `reset` (line 238)

#### `cases.py`
**Path:** `estorides_core/cases.py`

**Classs:**
- `CaseStore` (line 112) - *Thread-safe SQLite-backed case repository.

SQLite is plenty for OSINT-sized workloads (a few thousand cases
per operator per month) and avoids a separate service. The
underlying file is shared with the cache if you point both env
vars at the same path; otherwise we live in `estorides_cases.sqlite`
next to it.*

**Functions:**
- `__init__` (line 121)
- `_init_schema` (line 135)
- `_tx` (line 141)
- `create_case` (line 152) - *Open a new case and return its id (8-char slug).*
- `add_observation` (line 168) - *Persist a single observation row.

The full parsed/raw payload is JSON-encoded so we can
reconstruct the run later without re-running the source.*
- `add_entities` (line 202) - *Persist the merged entity list. Duplicate (type, value) rows
for the same case are silently ignored — the PK is the guard.*
- `finalise` (line 225)
- `delete_case` (line 255)
- `get_case` (line 260)
- `list_observations` (line 273)
- `list_entities` (line 296)
- `diff_entities` (line 311) - *Compare two cases by entity (type, value) keys.

Returns the symmetric difference plus counts and the per-type
breakdown. The "added" set is what case B learned that A did
not have; "removed" is the inverse. This is the OSINT analogue
of `git diff A B` and is the building block for the
"what's new since last run" UI the analyst wants to see.

Both cases are looked up in a single connection hold so the
diff is consistent even if the case store is being written
to concurrently.*
- `search_cases` (line 358) - *Lightweight case search. LIKE on `query` (not indexed, but
acceptable for the OSINT scale of a few thousand cases).*
- `search_by_entity` (line 388) - *Find every case that observed a given entity.

This is the cross-run memory query — the heart of "have I
seen this before?".*
- `stats` (line 416)
- `_row_to_case` (line 424)
- `_safe_json` (line 442)
- `close` (line 450)
- `_per_type` (line 332)
- `_serialise` (line 338)

#### `change_detection.py`
**Path:** `estorides_core/change_detection.py`

**Classs:**
- `Edge` (line 58) - *Outgoing edge: typed destination + relation name.*
- `SnapshotEntity` (line 66) - *One entity as captured at snapshot time.

Mirrors the fields the fusion store already persists
(``first_seen``/``last_seen``/``confidence``/``sources``), so a
Snapshot can be built directly from a fused row.*
- `Snapshot` (line 96) - *An immutable view of an investigation at one point in time.*
- `ChangeConfig` (line 104) - *Tuning for :func:`detect_changes`.*
- `Diff` (line 125) - *Structured description of a single change's delta.*
- `Change` (line 134) - *One detected change.*
- `ChangeSummary` (line 151) - *Aggregate stats for a :class:`ChangeReport`.*
- `ChangeReport` (line 168) - *Top-N changes + summary stats for a single diff operation.*

**Functions:**
- `_truncate_key` (line 176)
- `_change_id` (line 183)
- `_reliability_weight` (line 188) - *Reliability weight via 2a, with 0 fallback for the impossible
case where the enum value is not a letter A-F.*
- `_reliability_floor` (line 205) - *A=1, B=2, ..., F=6. For 'min_reliability' comparison.*
- `_filter_sources_by_reliability` (line 210)
- `_property_diff` (line 223) - *Compute the per-key add/change/remove between two property maps.*
- `_edge_set` (line 242)
- `_union_sources` (line 246) - *Sorted union of two entities' source lists.

Used in every per-entity Change (property_changed, source_added,
source_removed, edge_added, edge_removed, confidence_shifted) as
the ``sources`` field of the audit trail — the analyst should be
able to see every source that touched the entity, not just the
trigger of the change.*
- `_make_change` (line 258) - *Build a :class:`Change` with the deterministic id derived from
``kind + entity_id + sig``. Centralised so the eight change kinds
can never disagree on the field set or the id format.*
- `_below_min_reliability` (line 291) - *True if a source's reliability is strictly *worse* than the
configured minimum (i.e. it should be filtered out).*
- `detect_changes` (line 301) - *Diff two snapshots. Pure: no I/O, deterministic, bounded.

Parameters
----------
snapshot_before, snapshot_after
    The two snapshots to diff. Either may be ``None``:
    ``before=None`` ⇒ first run, every entity is ``new``;
    ``after=None`` ⇒ no future data, empty report.
config
    Optional tuning. See :class:`ChangeConfig`.*
- `__post_init__` (line 84)
- `__post_init__` (line 115)

#### `config.py`
**Path:** `estorides_core/config.py`

**Classs:**
- `CacheConfig` (line 329) - *Disk response-cache behaviour.*
- `PivotPolicyConfig` (line 342) - *Which entity types are worth pivoting on, and how leads are scored.

The recursive cross-search expands the highest-scoring leads first.
`type_weights` lets a high-signal selector (an email, a wallet) outrank
a low-signal one (a shared CDN IP) at the same depth. `depth_decay`
discounts every additional hop so the frontier stays close to the seed.*
- `PivotConfig` (line 367) - *Bounds and defaults for the recursive pivot engine.

`*_cap` values are the absolute ceilings applied to any caller-supplied
override (e.g. an API request body), so an untrusted client can never
request an unbounded crawl.*
- `StreamConfig` (line 412) - *Server-Sent-Events streaming knobs (buffer size, cadence).*
- `ReconFusionConfig` (line 424) - *Centralised tunables for the passive recon fusion engine.

Controls how raw OSINT results are grouped, deduplicated and classified
into relevance tiers. Every field has an env var equivalent so the
operator can adjust behaviour without touching code.

This is the SINGLE source of truth. The engine module imports from here
and never defines its own copy.*
- `WebConfig` (line 456) - *Per-endpoint defaults and render limits for the Flask layer.*

**Functions:**
- `_env_int` (line 32) - *Read an int env var, falling back to `default` on absence/parse error.*
- `_env_float` (line 44) - *Read a float env var, falling back to `default` on absence/parse error.*
- `_env_bool` (line 56) - *Read a boolean env var. Truthy tokens: 1/true/yes/on (case-insensitive).*
- `ensure_data_dirs` (line 86) - *Idempotently create DATA_DIR.

Replaces the import-time mkdir that issue #49 reported. Call
this from the app factory and from any code path that actually
needs to write to DATA_DIR. Idempotent: exist_ok=True so a
pre-existing directory is fine.*
- `ensure_reports_dir` (line 97) - *Idempotently create REPORTS_DIR.

Same posture as ensure_data_dirs(). /api/export/<fmt> used to
write through this path; issue #43 moved export artefacts to a
tempfile, but the directory is still useful for operator-facing
exports.*
- `contact_level` (line 185) - *Map a contact class to its numeric severity, unknown values to active.

An unrecognised class is treated as the most exposing (`active`) so a
typo in a source YAML can never silently downgrade an operator's
passive-only guarantee.*
- `effective_proxies` (line 211) - *Resolve the proxy rotation pool from an explicit value or the env.

Precedence: an explicit caller value (CLI flag) wins; otherwise the
pool env var, otherwise the single-proxy env var. Returns an empty
list when no anonymising egress is configured.*
- `_pivot_weight_map` (line 470) - *Default per-type lead weights for the pivot scorer.

Strong, single-owner selectors rank above shared infrastructure.*
- `_csv_frozenset` (line 487) - *Read a comma-separated env var into a frozenset, else the default.*
- `is_active` (line 336) - *Cache is only consulted when enabled and the TTL is positive.*
- `is_pivotable` (line 356) - *True when an entity of `entity_type` should be re-queried.*
- `lead_score` (line 360) - *Priority of expanding this lead. Higher expands sooner.*
- `clamp_depth` (line 390) - *Clamp a requested depth into [1, max_depth_cap].*
- `clamp_steps` (line 394) - *Clamp a requested step budget into [1, max_steps_cap].*
- `clamp_entities` (line 398) - *Clamp a requested entity budget into [1, max_entities_cap].*
- `clamp_parallel` (line 402) - *Clamp a requested fan-out width into [1, parallel_cap].*
- `clamp_deadline` (line 406) - *Clamp a requested per-target deadline into (0, deadline_cap_seconds].*
- `__post_init__` (line 445)

#### `discoverer.py`
**Path:** `estorides_core/discoverer.py`

**Classs:**
- `DiscoverJob` (line 50) - *One background discovery session.

Lives in `DISCOVER_JOBS` keyed by job_id; survives the SSE handler
exiting (so a UI reload reconnects and resumes).*
- `_DiscoverJobSink` (line 95) - *Adapts engine `PivotEvent`s to the legacy DiscoverJob event dicts.

The UI and CLI consume `step_start`, `node_found`, `step_done`,
`finished` and `error`; this translator preserves those shapes so the
engine swap is invisible to every existing consumer.*

**Functions:**
- `_new_job_id` (line 189) - *Monotonic-ish id with a timestamp prefix for natural sort.*
- `create_discover_job` (line 194) - *Create and register a discovery job synchronously.

This does only fast, loop-free work (a case-store insert and some
bookkeeping), so it is safe to call straight from a Flask request
thread. The asyncio worker that actually crawls is scheduled
separately by `start_discover` / `start_discover_threadsafe`, so the
caller never blocks on the shared background loop.*
- `start_discover` (line 252) - *Create a discovery job and schedule its worker on the current loop.

Kept as the coroutine entry point for callers that already own a
running loop (the CLI). Web callers use `start_discover_threadsafe`,
which never blocks the request thread on the background loop.*
- `start_discover_threadsafe` (line 285) - *Create the job in the calling thread, fire its worker on `loop`.

Returns immediately. The worker is queued with
`run_coroutine_threadsafe` and runs whenever the loop is next free, so
a busy loop (a concurrent deep-run) can never make this call time out.*
- `_run_discoverer` (line 319) - *The background loop. One asyncio task per job, driving the engine.*
- `list_jobs` (line 349) - *Snapshot of the recent jobs for the /api/discover/jobs endpoint.*
- `stop` (line 78)
- `should_stop` (line 81)
- `push_event` (line 84) - *Append an event and keep the buffer bounded.*
- `__init__` (line 103)
- `emit` (line 106)
- `_on_started` (line 113)
- `_on_target_start` (line 116)
- `_on_entity` (line 126)
- `_on_target_done` (line 141)
- `_on_target_error` (line 153)
- `_on_stopping` (line 160)
- `_on_finished` (line 163)
- `_on_fatal` (line 174)

#### `entity_extraction.py`
**Path:** `estorides_core/entity_extraction.py`

**Classs:**
- `Entity` (line 22)

**Functions:**
- `detect_query_type` (line 63) - *Return the detected type of a free-form query.

Falls back to 'domain' for anything that looks like a hostname
(contains a dot, no spaces), and to 'keyword' for everything else.*
- `_is_valid_domain` (line 84)
- `_context` (line 97)
- `extract_from_text` (line 103) - *Find every recognised entity in a raw text blob.

`types` optionally restricts which kinds of entity to look for.*
- `_ip_in_textual_context` (line 155) - *Heuristic: only count a numeric match as an IP if it isn't part of a
version number or timestamp (preceded/followed by `version`, `v`, or `:`).*
- `extract_from_json` (line 165) - *Pull entities out of a JSON-like structure.

Earlier this recursed into every string and ran all patterns on each one,
so a response with thousands of entries (crt.sh subdomains, wayback URLs)
triggered hundreds of thousands of regex passes. We now flatten the payload
to a single capped string and scan it once; entities span keys and values
just as well, and the cost is bounded by `extract_from_text`.*
- `_clean_scalar` (line 233) - *Return a stripped string for a scalar leaf, or None for non-scalars.*
- `_looks_like_person` (line 243) - *True when a value reads like a human name (has a space, mostly letters).*
- `_looks_like_username` (line 254) - *True when a value reads like a handle (no spaces, handle charset).*
- `_classify_keyed_value` (line 261) - *Map a (key, scalar value) pair to a human-selector entity type, or None.*
- `extract_structured` (line 285) - *Extract human selectors (email, username, person, org, phone) by key.

Walks the JSON structure and types values by the key they sit under,
which is the only reliable way to recover usernames and person names
(they have no lexical signature for a regex to catch). Bounded by
`ENTITY_MAX_PER_TYPE` per type and a node-visit cap so a pathological
response cannot turn this into a CPU stall.*
- `merge` (line 337) - *Deduplicate by (type, value) and merge sources / contexts.

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
- `_fuzzy_cluster` (line 431) - *Group entities of the same type by string similarity and merge.

Uses `difflib.SequenceMatcher.ratio()`. We compare normalised
(lowercased, hyphen-stripped) forms so `evil-corp.com` and
`evilcorp.com` collide cleanly. Only domain / email / person /
org types are eligible — IPs, hashes, and CVEs have exact
semantics where fuzzy would be a bug, not a feature.*
- `to_dict` (line 34)
- `visit` (line 299)
- `find` (line 452)
- `union` (line 458)
- `norm` (line 463)

#### `entity_resolution.py`
**Path:** `estorides_core/entity_resolution.py`

**Classs:**
- `MatchScore` (line 296) - *The result of comparing two entity values of the same type.*
- `CanonicalEntity` (line 342) - *A resolved identity fused from one or more observed entities.*
- `SameAsLink` (line 402) - *A suggested-but-unmerged identity link between two canonical ids.*
- `ResolutionResult` (line 420) - *Output of a resolve() call: fused entities plus candidate links.*
- `_UnionFind` (line 433) - *Disjoint-set over integer indices with path compression.*
- `EntityResolver` (line 455) - *Resolve a per-run entity list into canonical identities.

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
- `jaro` (line 83) - *Return the Jaro similarity of two strings in ``[0, 1]``.*
- `jaro_winkler` (line 126) - *Jaro-Winkler similarity: Jaro with a shared-prefix bonus.

The prefix bonus (up to 4 leading characters) rewards strings that
agree at the start, which is the common shape of name and domain
variants. ``prefix_weight`` is capped at 0.25 to keep the result in
``[0, 1]``.*
- `_soundex` (line 146) - *Return a 4-character Soundex code for a Latin token.

Used only as a blocking key: it groups phonetically similar tokens so
the expensive pairwise scorer runs on plausible candidates rather than
the whole list. Empty or non-alphabetic input yields ``"0000"``.*
- `_normalize_domain` (line 178)
- `_normalize_name` (line 187) - *Order-independent transliterated key for persons and orgs.

The surface form is transliterated to Latin, punctuation dropped, and
the tokens sorted, so ``"Putin, Vladimir"`` and ``"Владимир Путин"``
converge on the same normalised string and merge deterministically.
Cross-script spellings that survive transliteration with different
vowels (abjad scripts) are caught later by the skeleton scorer.*
- `normalize_value` (line 206) - *Return the canonical normalised form of an entity value.

The normalised form is the merge key for deterministic types and the
seed of the stable canonical id for every type. It is intentionally
lossy (case, ordering, ornament removed) but never collapses distinct
objects of a deterministic type.*
- `canonical_id` (line 246) - *Stable, content-addressed id for a normalised entity.

Same ``(type, normalized)`` always yields the same id, so a canonical
entity keeps its identity for as long as its normalised form is stable.
The persistent store additionally maps known aliases onto an existing
id so a never-before-seen surface form still resolves to the same node.*
- `blocking_keys` (line 258) - *Return the blocking keys that bucket an entity for comparison.

Two entities are only ever scored against each other if they share at
least one blocking key. The keys are chosen to be high-recall (so true
matches land together) while keeping buckets small enough that the
in-bucket pairwise scan stays cheap.*
- `score_pair` (line 303) - *Score how likely two same-type entities denote the same object.

Deterministic types return 1.0 only on normalised equality and 0.0
otherwise. Fuzzy types layer Jaro-Winkler over the normalised form with
a cross-script consonant-skeleton booster for names, so a Cyrillic and
a Latin spelling of one person can clear the link bar even when their
transliterated vowels differ.*
- `_script_of` (line 451)
- `resolve_entities` (line 728) - *Module-level convenience wrapper around :class:`EntityResolver`.*
- `to_dict` (line 358)
- `to_entity` (line 374) - *Project back onto the legacy :class:`Entity` shape.

Lets the resolver drop into the existing orchestrator, knowledge
graph, and case-store paths without changing their interfaces while
carrying the new identity metadata in ``attributes``.*
- `to_dict` (line 410)
- `to_dict` (line 426)
- `__init__` (line 436)
- `find` (line 439)
- `union` (line 445)
- `__init__` (line 470)
- `resolve` (line 483) - *Resolve ``entities`` into canonical identities and links.*
- `_build_records` (line 499)
- `_exact_merge` (line 514)
- `_fuzzy_merge` (line 526) - *Block, score, merge at threshold, and collect link candidates.

Merges (union) happen eagerly as pairs clear the merge bar. Pairs
that only clear the lower link bar are returned as ``(a, b, score)``
index triples for the caller to translate into canonical-id links
once clusters are materialised.*
- `_build_links` (line 567) - *Translate index-pair link candidates into canonical-id links.

Pairs whose clusters ended up merged (a later, stronger edge pulled
them together) are dropped; the rest are deduplicated per
canonical-id pair, keeping the highest-scoring justification.*
- `_materialise` (line 595)
- `_representative` (line 662) - *Pick a stable representative for a cluster.

Preference order: most corroborated (appears in most sources), then
a Latin surface form over a non-Latin one (more broadly readable in
reports), then the lexicographically smallest value. The result is
deterministic for a given member set, which keeps the canonical id
stable run to run.*
- `_best_internal_match` (line 680) - *Return the (method, score) of the strongest non-exact pair.

Surfaces *why* a multi-member cluster was fused, so the analyst can
see whether the merge rested on an exact key or a probabilistic
name match. Bounded to the first handful of members to stay cheap on
large clusters.*
- `_reconcile_with_store` (line 706) - *Map canonicals onto persisted ids and record their aliases.

Looked up alias-first so a brand-new surface form of a known entity
adopts the existing canonical id instead of minting a new one. The
store call is best-effort: any failure leaves the freshly computed
id in place rather than aborting the run.*
- `rank` (line 671)

#### `entity_store.py`
**Path:** `estorides_core/entity_store.py`

**Classs:**
- `EntityStore` (line 62) - *Thread-safe SQLite repository of canonical identities and aliases.*

**Functions:**
- `open_store` (line 184) - *Open the store, returning None instead of raising on failure.

The resolver calls this so that an unwritable or locked data directory
degrades the cross-run identity feature to in-run-only resolution rather
than aborting an investigation.*
- `__init__` (line 65)
- `_init_schema` (line 75)
- `_tx` (line 81)
- `lookup` (line 91) - *Return an existing canonical id for any known form, or None.

Checks every normalised key the entity can present — its own and
each alias's — against both the canonical ``entities`` table and the
``aliases`` table. The first established id wins, so a never-before
spelling of a known target still resolves to its prior identity.*
- `upsert` (line 129) - *Persist (insert or update) a canonical entity and its aliases.

``first_seen`` is preserved across updates; ``last_seen``,
``member_count``, ``source_count``, ``value``, and ``confidence``
track the latest resolution. Every alias is recorded with its
normalised key so future lookups can route any surface form back to
this id.*
- `stats` (line 168) - *Return a one-glance summary of store size.*
- `close` (line 179)

#### `feeds.py`
**Path:** `estorides_core/feeds.py`

**Classs:**
- `FeedPoint` (line 54) - *Normalised point for the map layer.

`kind` discriminates the marker on the map (flight / quake / fire /
news / vessel). `extra` is an open dict for source-specific fields
the frontend may want to render in the popup.*
- `Feed` (line 74) - *Base class for a real-time feed.*
- `EarthquakesFeed` (line 148) - *USGS M2.5+ earthquakes, last 24h, worldwide.*
- `FiresFeed` (line 190) - *NASA FIRMS active fire hotspots (VIIRS_NOAA20_NRT, last 24h).

FIRMS retired its keyless CSV download in 2024. The new endpoint
at `api/data/active_fire/csv/...` requires a MAP_KEY (free with
NASA Earthdata registration) which is read from the
`ESTORIDES_FIRMS_KEY` env var. If the key is missing the feed
silently returns zero points and logs a warning — it never
breaks the rest of the platform.*
- `NewsFeed` (line 251) - *GDELT 2.0 — global news articles (article-list API).

The GeoJSON endpoint we used in the previous version was retired.
The current keyless endpoint is the article-list API at
`/api/v2/doc/doc` which returns a JSON `articles` array. We
attempt to geocode the article URL via the embedded
`socialimage` or `domain` field when coordinates aren't in the
payload — falling back to the article's source domain
coordinates is intentionally out of scope for this version, so
a record without explicit coordinates is dropped.*

**Functions:**
- `list_feeds` (line 313) - *Return public feed descriptions for the /api/feeds endpoint.*
- `get_feed` (line 321)
- `fetch_all` (line 325) - *Fetch every registered feed (optionally clipped to a bbox).

Used by /api/feeds to populate the map in one round-trip.

bbox = (min_lon, min_lat, max_lon, max_lat). Points outside the
bbox are dropped before the response is returned.*
- `to_dict` (line 69)
- `__init__` (line 82)
- `_fetch` (line 87) - *Subclass implementation: hit the upstream and return points.*
- `fetch` (line 90) - *Public entrypoint. Reads/writes the on-disk cache.

The cache is a simple `{fetched_at, points}` JSON blob —
good enough for a self-hosted deployment. A real production
system would want a TTL'd Redis layer, but that pulls in a
network dependency.*
- `point` (line 135) - *Default: return (lat, lon) if both present.*
- `_fetch` (line 156)
- `_fetch` (line 209)
- `_fetch` (line 271)

#### `fusion_analytics.py`
**Path:** `estorides_core/fusion_analytics.py`

**Classs:**
- `FusionAnalytics` (line 31) - *Read-only analytics queries over the fusion store.

Every method is parameterized SQL — no string interpolation.
A ``store`` of ``None`` is silently handled (all methods return
empty results) so the caller never needs to guard against a
missing datastore.*

**Functions:**
- `__init__` (line 40)
- `entity_timeline` (line 46)
- `entity_summary` (line 132)
- `source_stats` (line 213)
- `multi_source_consensus` (line 290)
- `corroborated_properties` (line 343)
- `entity_search` (line 374)
- `top_changed` (line 432)
- `source_corroboration_matrix` (line 477)
- `_resolve_entity_value` (line 509)
- `_resolve_entity_type` (line 520)
- `_intel_level` (line 532)
- `_deduplicate_relationships` (line 540)

#### `fusion_store.py`
**Path:** `estorides_core/fusion_store.py`

**Classs:**
- `FusionStore` (line 191) - *Thread-safe SQLite-backed fusion datastore.

One serialised connection guarded by a lock, WAL journalling, and
``ON DELETE CASCADE`` foreign keys so dropping an entity reaps its
provenance, properties and edges.*

**Functions:**
- `entity_id` (line 178) - *Deterministic, run-independent id for an entity.

Derived from the type and the normalised value so the same real-world
entity always hashes to the same id no matter which run or source first
produced it — the property that makes cross-run fusion automatic.*
- `open_store` (line 753) - *Open the fusion store, returning None instead of raising on failure.

The orchestrator calls this so an unwritable or locked data directory
degrades the fusion layer to a no-op rather than aborting an
investigation.*
- `__init__` (line 199)
- `_init_schema` (line 210)
- `_tx` (line 216)
- `_ensure_entity_stub` (line 227) - *Insert a minimal entity row if absent and return its id.

Used for relationship endpoints (a country, an ASN, a port) that no
entity-extraction pass produced, so an edge is always navigable from
both ends. Runs inside the caller's transaction; never overwrites an
already-fused entity (``INSERT OR IGNORE``).*
- `register_sources` (line 247) - *Mirror the YAML source catalogue into the store.

Idempotent: an existing source keeps its ``first_seen`` and its
accumulated counters; only the descriptive columns are refreshed so
the catalogue tracks edits to the YAML without losing fetch history.*
- `add_observation` (line 284) - *Fuse a single source response into the cross-run observation log
and bump the source's fetch/ok counters.*
- `fuse_entity` (line 325) - *Fuse one entity into the canonical store and return its id.

The ``(type, normalized)`` pair is the dedup key. On a repeat sighting
the row's ``last_seen``, confidence (Bayesian merge), and observation
count advance, and every contributing source is recorded in
``fusion_entity_sources`` so provenance survives the merge.

Confidence uses the :mod:`reliability_scoring` pipeline: source
reliability, source type hierarchy, and corroboration count are
factored into the score instead of a raw ``MAX()``. A tertiary or
unreliable source cannot override a well-corroborated primary one.*
- `fuse_entities` (line 428) - *Fuse a batch of entities, returning the list of fused ids.*
- `fuse_properties` (line 441) - *Fuse the flat scalar attributes of a parsed observation onto an
entity, attributed to ``source``.

Only one nesting level of scalar values is taken: deep structures are
the observation payload's job, not an entity attribute's. Returns the
number of properties written. The ``(entity_id, key, value, source)``
primary key means re-running the same source is idempotent while a
*different* source asserting the same key/value adds corroboration.*
- `fuse_relationship` (line 487) - *Fuse one directed edge between two entities, attributed to source.

Both endpoints are resolved to their deterministic fusion ids so the
edge joins the same canonical entities the entity table holds.
Confidence uses the :mod:`reliability_scoring` pipeline instead of a
raw ``MAX()``, so a low-reliability source cannot inflate the score
of a well-corroborated edge.*
- `fuse_graph` (line 557) - *Mirror the analytic edges of a knowledge graph into the store.

Reads node ``type``/``value`` off each endpoint and skips the pure
plumbing relations (``observed_by``, ``co_occurs``, ``mentions``) and
any edge touching a ``source`` node, so only pivot-worthy facts land.
Returns the number of edges fused. Best-effort: a malformed graph is
swallowed rather than aborting a run.*
- `get_entity` (line 593) - *Return one fused entity with its provenance, properties and edges.*
- `search_entities` (line 639) - *Search fused entities by value substring and/or type.

``min_sources`` filters to entities corroborated by at least N feeds —
the fusion-native "only show me what more than one source agrees on"
query. Ordered by source breadth then recency.*
- `corroborated_properties` (line 682) - *Return an entity's properties that at least ``min_sources`` distinct
feeds independently asserted — the fusion store's confidence signal.*
- `list_sources` (line 699) - *Return the source catalogue with accumulated fetch/ok counters.*
- `stats` (line 717) - *One-glance dashboard of the fused store's size.*
- `close` (line 745)
- `normalize_value` (line 74)
- `_count` (line 720)

#### `graph_kuzu.py`
**Path:** `estorides_core/graph_kuzu.py`

**Classs:**
- `KuzuGraphBackend` (line 196) - *Thread-safe Kuzu wrapper for the Estorides knowledge graph.

The orchestrator calls this alongside the in-memory NetworkX graph.
Writes are synchronous but cheap; reads (Cypher) are also synchronous
and roughly match NetworkX traversal cost for 2-hop queries while
being dramatically faster at cross-run joins.*

**Functions:**
- `_label_for` (line 124)
- `_node_id` (line 133) - *Canonical id used as PRIMARY KEY in Kuzu.

Mirrors the in-memory convention in KnowledgeGraph._node_id so a
`Domain:evilcorp.com` row means the same thing in both stores.*
- `__init__` (line 205)
- `_init_schema` (line 233)
- `upsert_entity` (line 245) - *Insert (or merge) an entity. Returns its canonical node id.

If `source` is given we also wire an OBSERVED_BY edge so we
can later ask "which sources saw this entity?".*
- `upsert_relationship` (line 295) - *Insert an edge between two entities.

Unknown relations are silently skipped — every edge type
that matters is mapped in _RELATION_TO_EDGE.*
- `neighbors` (line 346) - *Return nodes reachable from `node_id` within `hops` edges.

`relation` optionally filters to a single edge label.
Returns a list of dicts with whatever columns the query names.*
- `cypher` (line 379) - *Run a Cypher query and return rows as a list of dicts.

Column names are taken from the RETURN clause. Missing
columns (e.g. `m.kind` on a node that was never enriched) come
back as None so callers don't have to special-case.*
- `stats` (line 406) - *Return counts of every node label and edge rel type.*
- `close` (line 436)

#### `hypothesis_engine.py`
**Path:** `estorides_core/hypothesis_engine.py`

**Classs:**
- `EntityRef` (line 54) - *A typed reference to an entity involved in a hypothesis.*
- `Evidence` (line 62) - *One piece of supporting or contradicting evidence.*
- `Hypothesis` (line 73) - *A typed, scored, auditable intelligence conclusion.*
- `HypothesisGenerator` (line 207) - *Strategy: turn a (observations, entities) snapshot into hypotheses.*

**Functions:**
- `_truncate` (line 110) - *Stringify a value, bounded to ``_VALUE_MAX_CHARS``.*
- `_is_mapping` (line 120)
- `_entity_lookup` (line 124) - *Build ``{type: {value, value, ...}}`` from the entity list.

Tolerates both ``Entity`` dataclass instances and plain dicts
(the orchestrator returns both shapes depending on the call site).*
- `_hypothesis_id` (line 145) - *Deterministic 16-char hex id for a hypothesis.*
- `_score` (line 163) - *Net-support score in (0, 1].

``supporting / (supporting + contradicting + floor)`` — the floor
prevents division by zero and prevents a single weak item from
producing a "1.0 certain" score.*
- `_confidence` (line 177) - *Reliability-weighted confidence via :mod:`reliability_scoring`.*
- `_clip_claim` (line 198)
- `_domain_belongsto_actor` (line 217) - *`domain-belongsto-actor`: a domain's WHOIS/issuer/hosting org matches an entity.*
- `_domains_in_obs` (line 309) - *Best-effort: extract domain-like values from a single observation.

The orchestrator doesn't always stamp the queried domain on the
observation, so this is a soft hint. Returns ``[]`` if nothing
looks like a domain.*
- `_email_aliases_person` (line 342) - *`email-aliasto-person`: an email and a person name appear together in one obs.*
- `_extract_email` (line 402) - *Find a value that looks like an email anywhere in the parsed dict.*
- `_extract_person_name` (line 413) - *Find a value that looks like a person name (has a space, no @, no path).*
- `_ip_shared_infra` (line 424) - *`ip-shared-infra`: >=2 domains resolve to the same IP.*
- `_extract_ips` (line 505) - *Best-effort: pull IPv4-looking values out of a parsed payload.*
- `_looks_like_ipv4` (line 520)
- `_asn_shared_infra` (line 533) - *`asn-shared-infra`: >=3 entities of the run live in the same ASN.*
- `_extract_asn` (line 597) - *Best-effort: pull an AS-number-ish value out of the parsed payload.*
- `generate_hypotheses` (line 622) - *Generate typed, scored, auditable hypotheses for a run.

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
- `__call__` (line 210)

#### `intel_resolver.py`
**Path:** `estorides_core/intel_resolver.py`

**Classs:**
- `_TTLCache` (line 120)
- `EntityResolver` (line 156) - *Cross-feed entity resolution.

Composes Wikidata SPARQL, the OFAC SDN index (via the existing
`OntologyEngine.sanctions`), and a couple of free IP-intel
services into a single response shape suitable for both the UI
(entity graph panel) and the orchestrator (knowledge graph
enrichment).*

**Functions:**
- `_run_sparql` (line 90) - *Execute a SPARQL SELECT against the Wikidata endpoint.

Returns the list of result rows. SSRF-guarded via the URL.*
- `_val` (line 111) - *Pull a string value out of a SPARQL JSON row.*
- `_norm` (line 789)
- `_is_valid_ipv4` (line 793)
- `_escape_sparql` (line 801)
- `__init__` (line 121)
- `get` (line 127)
- `put` (line 140)
- `stats` (line 148)
- `__init__` (line 165)
- `resolve` (line 174)
- `_vt_get` (line 214) - *GET a VirusTotal v3 path, returning parsed JSON or None.

Reads the API key from `VT_API_KEY`; if it is absent the call
is a silent no-op so the resolver degrades cleanly without a
key. SSRF-guarded via the constructed URL.*
- `_vt_add_relationship` (line 245) - *Expand one VirusTotal relationship endpoint into nodes/links.

`attr_field` pulls the related value from `attributes` (e.g.
`host_name` for IP resolutions) instead of the raw object id.*
- `_vt_flag_malicious` (line 290) - *Stamp a node with VirusTotal detection stats (counter-intel signal).*
- `_resolve_ip` (line 306)
- `_resolve_domain` (line 412)
- `_resolve_file` (line 473) - *Resolve a file hash via VirusTotal relationships.

Surfaces the network footprint of a sample (contacted IPs and
domains, dropped/bundled files) and stamps the detection count
so a malicious sample lights up the counter-intelligence tier.*
- `_resolve_company` (line 510)
- `_resolve_person` (line 569)
- `_resolve_country` (line 638)
- `_resolve_cve` (line 678)
- `_resolve_btc` (line 750)
- `_resolve_eth` (line 753)
- `_resolve_crypto` (line 756)

#### `job_registry.py`
**Path:** `estorides_core/job_registry.py`

**Classs:**
- `BoundedJobRegistry` (line 40) - *A dict-like registry with size and time bounds.

`max_size` and `ttl_seconds` are read at construction and not
mutated — the registry is "configured once, used many times",
which matches how the web app's STREAM config is loaded at
import time.*

**Functions:**
- `__init__` (line 49)
- `register` (line 60) - *Insert (or replace) a job, evicting expired and overflow entries.

Returns the value so the caller can use it inline:
    job = registry.register("abc", _RunStreamJob(...))*
- `get` (line 80) - *Return the value for `key` or None. Refreshes the LRU order.*
- `pop` (line 95) - *Remove and return the value for `key`, or None.*
- `keys` (line 101)
- `values` (line 105)
- `__len__` (line 109)
- `evict_expired` (line 113) - *Sweep and drop TTL-expired entries. Returns the number dropped.*
- `_evict_expired_locked` (line 119)

#### `knowledge_graph.py`
**Path:** `estorides_core/knowledge_graph.py`

**Classs:**
- `KnowledgeGraph` (line 90)

**Functions:**
- `_node_sources` (line 73) - *Read the distinct source set off a node, tolerating GraphML's
JSON-string serialisation of the original Python set/list.*
- `__init__` (line 91)
- `add_entity` (line 97) - *Insert an entity. Returns the node id used.*
- `add_observation` (line 127) - *Add every entity + every co-occurrence edge within the same response.*
- `add_relationship` (line 142)
- `export_graphml` (line 164)
- `export_json` (line 183)
- `summary` (line 197)
- `top_entities` (line 215)
- `communities` (line 235) - *Partition entity nodes into communities (clusters).

Runs greedy modularity on the undirected projection, restricted
to `nodes` when given and always excluding `source` nodes (whose
fan-out would otherwise collapse every cluster into one). Returns
a `node_id -> community index` map. Falls back to connected
components when modularity cannot be computed (e.g. no edges).*
- `intel_level` (line 266) - *Classify a node into the intelligence pipeline tier.

data                  single corroborating source
information           >= 2 distinct sources
intelligence          cross-cluster bridge or resolved relation
counter_intelligence  sanction/threat/VirusTotal-malicious signal

Higher tiers win. `bridge_nodes` is the set of nodes that sit on
an inter-cluster edge (computed once by the caller).*
- `ego_subgraph` (line 311)
- `neighbours` (line 322)
- `_node_id` (line 338)
- `_source_node` (line 341)
- `_node_color` (line 351)

#### `mitre_attack.py`
**Path:** `estorides_core/mitre_attack.py`

**Functions:**
- `_scan_keywords` (line 156) - *Scan a text blob for ATT&CK-relevant keywords.*
- `map_observation` (line 170) - *Return ATT&CK techniques associated with an observation.

Output:
    {
      "techniques": [
        {"id": "T1595", "label": "Active Scanning", "via": "source:shodan_internetdb"},
        ...
      ],
      "tactic_ids": ["TA0043"],  # not populated yet — future
    }*
- `map_observations` (line 213) - *Bulk mapper. Stamps each observation in place with `_mitre` key.

Returns the list of observations (for chaining). Mutates in place
for performance — the orchestrator doesn't keep references to the
pre-mapping list, so a side effect is safe.*
- `all_techniques_for` (line 229) - *Aggregate: unique techniques across all observations, sorted by id.*

#### `ontology.py`
**Path:** `estorides_core/ontology.py`

**Classs:**
- `SanctionEntry` (line 70)
- `SanctionsIndex` (line 96) - *In-memory OFAC SDN index with 24h lazy refresh and single-flight load.

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
- `WikidataCache` (line 268) - *Bounded LRU cache for Wikidata SPARQL queries.

Keyed by `(query_kind, normalised_value)`. Values are `(fetched_at, payload)`.
Exposes `lookup_label(label)` and `lookup_org(label)` — the two
most common lookups in OSINT workflows.*
- `OntologyEngine` (line 314) - *Public façade. Hands out the sanction index and wikidata cache.*

**Functions:**
- `_normalise_name` (line 84) - *Lower-case, strip punctuation/diacritics, collapse whitespace.

Used for both index keys and incoming query normalisation so the
same string yields the same key on both sides.*
- `to_dict` (line 79)
- `__init__` (line 115)
- `is_ready` (line 131)
- `entries` (line 134) - *Return the current snapshot, loading if necessary.*
- `lookup` (line 141) - *Find sanction entries whose name or alias matches `name`.*
- `lookup_crypto` (line 151) - *Cross-check a BTC/ETH address against the SDN list.

The OpenSanctions CSV includes a `crypto_address` (BTC) field
on a subset of entries. ETH addresses are stored in the
`ethereum_address` field. The current implementation matches
by alias string for simplicity — the upstream coverage of
crypto is sparse and not the focus of this version. Returns
the entries whose alias list contains the literal address.*
- `size` (line 168)
- `_refresh` (line 172)
- `_download` (line 201)
- `_persist` (line 213) - *Best-effort write of the raw CSV for offline re-use.

Failures are non-fatal; the in-memory index is the source of
truth while the process is alive.*
- `_parse` (line 226) - *Parse the OpenSanctions simple CSV into SanctionEntry records.*
- `_index` (line 255) - *Build a normalised-name → entries lookup.*
- `__init__` (line 276)
- `get` (line 282)
- `put` (line 296)
- `stats` (line 304)
- `clear` (line 308)
- `__init__` (line 317)
- `check_observation` (line 321) - *Run a single observation through the ontology.

Returns a dict describing the sanctions verdict:

  {
    "sanctioned": bool,
    "hits": [SanctionEntry.to_dict(), ...],
    "fields": ["registrant_name", "isp", ...]  # which fields matched
  }

The orchestrator attaches this to each observation before the
LLM analyst stage so the system prompt can include a verdict
line ("SANCTIONED — OFAC SDN match on registrant").*
- `_candidate_fields` (line 359) - *Return (field_name, value) pairs to check against sanctions.

Different sources expose different field names. Rather than
a giant if/elif, this is a small dispatch table — adding a
new source is a one-line edit.*

#### `orchestrator.py`
**Path:** `estorides_core/orchestrator.py`

**Classs:**
- `Orchestrator` (line 132)

**Functions:**
- `_safe_format` (line 100) - *Format a string template with {key} placeholders.

Non-string values (int, list, dict) are returned as-is so YAMLs that
use raw integers or list literals in params/body don't blow up.*
- `_resolve_auth` (line 112) - *Look up the API key for a source that needs one.*
- `_domain_from_query` (line 122) - *Heuristic: if the query looks like a domain, return it; if it's an IP, return None.*
- `repl` (line 107)
- `__init__` (line 133)
- `run` (line 148) - *Run a full intelligence cycle. Returns a structured result.

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
- `_select_sources` (line 619)
- `_execute_source` (line 652)
- `_extract_cursor` (line 757) - *Extract the next-page cursor from a parsed response body.*
- `_infer_relationships` (line 762) - *Delegate each observation to its registered inferer.

The previous version of this method was a 90-line `if/elif`
chain hard-coded to specific source names. The new version
walks the inferer registry; sources with no inferer are
silently skipped. Adding a new inferer is now: write a
function and `@register_inferer("source_name")` it. No edits
to this method.*
- `_write_dataset` (line 775)

#### `osiris_sources.py`
**Path:** `estorides_core/osiris_sources.py`

**Functions:**
- `_cached_get` (line 81) - *GET with a small on-disk JSON cache. Returns parsed JSON or None.

Used for the slow-changing feeds (CISA KEV, malware lists) so a
burst of operator clicks doesn't hammer the upstream.*
- `fetch_bgp` (line 119) - *Look up an IP or AS number against bgpview.io (free, no key).*
- `fetch_mac` (line 184) - *Look up a MAC address against macvendors.co (free, no key).*
- `fetch_phone` (line 231) - *Best-effort phone geolocation.

The implementation is intentionally simple (regex + region
table). It does NOT replace libphonenumber; it provides a
same-shape response without the dep so the API stays consistent
with Osiris' /api/osint/phone.*
- `fetch_github_user` (line 300) - *Look up a GitHub user (keyless, rate-limited).*
- `fetch_leaks` (line 353) - *Breach analytics for `email` via xposedornot (free, no key).*
- `fetch_cisa_kev` (line 396) - *Recently-added CVEs from the CISA KEV feed (authoritative).*
- `fetch_malware_c2` (line 448) - *Active botnet C2 (Feodo) + recent malware URLs (URLhaus).

Both abuse.ch, both keyless. Each entry is geolocated against the
country centroid table with deterministic jitter so multiple
threats in the same country don't stack on the same pixel.*

#### `pagination.py`
**Path:** `estorides_core/pagination.py`

**Classs:**
- `PaginationConfig` (line 19) - *Configuration for a paginated source fetch.

Parsed from the source YAML's ``pagination`` key. No fields are
required; a source with no pagination config results in a single
fetch (the current default behaviour).*

**Functions:**
- `build_page_params` (line 62) - *Build URL params dict for a given page number.

Returns an empty dict for cursor strategy (the cursor is set
dynamically from the response) or when pagination is disabled.*
- `extract_cursor` (line 78) - *Extract the next-page cursor from a parsed response body.

Walks the dot-separated ``cursor_path`` into the JSON-like dict.
Returns ``None`` when the path is absent or the value is empty.*
- `count_results` (line 99) - *Count results in a parsed response page.

Uses ``response_list_path`` if configured, otherwise tries common
JSON fields (``results``, ``items``, ``data``) or falls back to
``len(data)`` for a list-type response.*
- `from_dict` (line 38)
- `enabled` (line 54)
- `needs_page_size` (line 58)

#### `parsers.py`
**Path:** `estorides_core/parsers.py`

**Functions:**
- `_flat` (line 30) - *Recursively flatten a dict/list into a list of leaf values.*
- `_first` (line 44) - *Recursively dig into a JSON-ish structure to find the first matching key.*
- `parse_dns_json` (line 62) - *Google/Cloudflare DNS-over-HTTPS response.*
- `parse_crtsh_json` (line 77) - *crt.sh CT log response.*
- `parse_rdap` (line 95) - *RDAP (RFC 7483) domain object.

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
- `parse_ipapi` (line 170) - *ip-api.com response.*
- `parse_ipinfo` (line 196)
- `parse_ipapi_co` (line 211)
- `parse_shodan_internetdb` (line 220) - *internetdb.shodan.io — IP service summary.*
- `parse_greynoise` (line 234)
- `parse_ipwhois` (line 249)
- `parse_abuseipdb` (line 267)
- `_vt_stats` (line 283) - *Flatten VirusTotal v3 last_analysis_stats into a compact dict.*
- `parse_vt_ip` (line 297) - *VirusTotal v3 — IP address object.*
- `parse_vt_domain` (line 318) - *VirusTotal v3 — domain object.*
- `parse_vt_file` (line 345) - *VirusTotal v3 — file object.*
- `parse_ripe_stat` (line 369)
- `parse_nominatim` (line 380)
- `parse_urlscan` (line 398)
- `parse_wayback_cdx` (line 420) - *CDX returns a list where the first row is the header.*
- `parse_wayback_avail` (line 433)
- `parse_threatfox` (line 442)
- `parse_urlhaus` (line 451)
- `parse_urlhaus_payloads` (line 460)
- `parse_malwarebazaar` (line 469)
- `parse_otx` (line 478)
- `parse_hibp_breach` (line 502)
- `parse_hibp_paste` (line 520)
- `parse_phonebook` (line 536)
- `parse_wikipedia` (line 557)
- `parse_wikidata` (line 566)
- `parse_openalex` (line 578)
- `parse_crossref` (line 598)
- `parse_arxiv` (line 618) - *arXiv returns Atom XML; we expect callers to have converted to a dict.*
- `parse_nvd_cve` (line 639)
- `parse_github_advisories` (line 661)
- `parse_blockchain_btc` (line 685)
- `parse_blockstream` (line 701)
- `parse_ethplorer` (line 717)
- `parse_microlink` (line 733)
- `parse_github_user` (line 753)
- `parse_github_search` (line 773)
- `parse_reddit` (line 788)
- `parse_mastodon` (line 818)
- `parse_keybase` (line 834)
- `parse_hackernews` (line 858)
- `parse_reddit_search` (line 870)
- `parse_dev_to` (line 884)
- `parse_text_lines` (line 899) - *Generic: split raw_text by newlines, drop empties.*
- `parse_raw_text` (line 910)
- `parse_http_headers` (line 918) - *hackertarget returns text; expect a one-line-per-header response.*
- `parse_whois_text` (line 934)
- `get_parser` (line 1024) - *Return the parser function for `name`, or a passthrough lambda.

Unknown parser names deliberately fall through to `parse_raw_text`
so a source YAML with a typo in the `parser` field never crashes
the run — it just produces a less-structured observation.*
- `register_parser` (line 1037) - *Decorator: register `func` as a parser under `name`.

Used by addon authors and tests to extend the catalog without
touching the central `PARSERS` dict. Idempotent: re-registering
the same name overwrites the previous entry, with a debug log so
a typo doesn't silently drop a parser.*
- `list_parsers` (line 1053) - *Return (name, description) tuples for every registered parser.

Used by the CLI `status` endpoint to advertise the available
parser names, and by tests to assert that a custom parser made it
into the registry.*
- `deco` (line 1045)

#### `pivot_engine.py`
**Path:** `estorides_core/pivot_engine.py`

**Classs:**
- `PivotEvent` (line 47) - *A single, transport-neutral progress event.

`type` is a stable vocabulary token; `data` is a JSON-serialisable
payload. Sinks translate these to their own wire format.*
- `EventSink` (line 59) - *Receives engine progress events. Implementations must not raise.*
- `ListEventSink` (line 67) - *In-memory sink. Useful for tests and synchronous embedding.*
- `BufferedEventSink` (line 77) - *Bounded sink that flattens events to JSON-ready dicts for SSE drain.

Each stored item is `{"type": ..., "ts": ..., **data}`. When the buffer
exceeds `capacity` the oldest items are dropped and a `heartbeat` marker
records how many were lost, so a slow client degrades gracefully instead
of stalling the producer. The terminal `finished`/`fatal` event also
flips `done` so a poller knows when to stop without parsing payloads.*
- `EntityRunner` (line 113) - *Runs the OSINT fan-out for a single target.

The engine depends on this narrow port rather than the concrete
Orchestrator, so it can be driven by a stub in tests.*
- `PivotBudget` (line 139) - *Mutable accounting for one cross-search.

Holds the three hard ceilings (steps, entities, wall-clock) and the
monotonic clock the deadline is measured against. `exhausted()` returns
a human reason string the moment any ceiling is hit, else None.*
- `PivotLead` (line 172) - *A target waiting in the frontier.*
- `PivotResult` (line 184) - *Terminal summary of a completed cross-search.*
- `PivotEngine` (line 195) - *Drives the recursive, scored, asynchronous cross-search.*

**Functions:**
- `emit` (line 62) - *Publish one event. A slow or failing sink must never break a run.*
- `__init__` (line 70)
- `emit` (line 73)
- `__init__` (line 87)
- `emit` (line 94)
- `run` (line 120)
- `time_left` (line 155) - *Seconds remaining before the global wall-clock deadline.*
- `exhausted` (line 159) - *Reason the run must stop, or None while budget remains.*
- `__init__` (line 198)
- `_emit` (line 246) - *Build and publish an event, swallowing any sink failure.*
- `_heap_push` (line 255) - *Push a lead as a max-heap by score (negated for heapq).*
- `run` (line 264) - *Execute the cross-search from `(seed_type, seed_value)`.

Returns a `PivotResult`. Progress is published incrementally
through the injected sink while the coroutine is in flight.*
- `_expand_lead` (line 341) - *Run the fan-out for one lead and enqueue its scored children.*
- `_ingest_children` (line 411) - *Score the entities a target produced and enqueue the best ones.

Returns the number of leads actually added to the frontier. The
per-step breadth cap keeps a single popular target (a CDN, a
registrar) from flooding the queue.*
- `_on_source_done` (line 356)
- `_on_source_result` (line 366)

#### `recon_fusion.py`
**Path:** `estorides_core/recon_fusion.py`

**Classs:**
- `RelevanceTier` (line 24) - *Relevance classification for grouped reconnaissance results.

Ordered from most to least relevant for UI rendering.*
- `GroupedEntity` (line 43) - *One canonical entity grouped across all sources that observed it.*
- `FusionResult` (line 81) - *Complete output of the recon fusion engine.*
- `ReconFusionEngine` (line 177) - *Stateless engine that classifies raw OSINT results into relevance tiers.

Thread-safe (no mutable state). Reusable across requests.*

**Functions:**
- `_normalize_value` (line 104) - *Deterministic normalisation matching fusion_store.entity_id.*
- `_canonical_id` (line 109) - *Deterministic sha1-based entity id matching fusion_store convention.*
- `_reliability_weight` (line 115) - *Map a source name to its numeric reliability weight.

Uses overrides first, then the curated reliability_scoring map.
Returns 0.7 (C, fairly reliable) as default for unknown sources.*
- `_corroboration_factor` (line 134) - *Logarithmic corroboration weight: min(1, log10(1 + n)).*
- `_freshness_factor` (line 141) - *Linear freshness decay from 1.0 (fresh) to 0.1 (stale).*
- `_direct_match_query` (line 149) - *True if the entity value matches the original query.*
- `_extract_key_findings` (line 154) - *Extract textual key findings from a list of observations.*
- `_reliability_weight_for_letter` (line 443) - *Convert a reliability letter (A-F) to its numeric weight.*
- `ordered` (line 37) - *Return tiers in canonical display order.*
- `to_dict` (line 61)
- `to_dict` (line 92)
- `__init__` (line 183)
- `classify` (line 186) - *Classify raw observations and entities into relevance-tiered groups.

Args:
    query: The original operator query (non-empty).
    query_type: Detected type of the query.
    observations: Raw observation dicts from the orchestrator.
    entities: Raw entity dicts from entity extraction.

Returns:
    FusionResult with tiered, grouped, deduplicated results.

Raises:
    ValueError: If query is empty.*
- `_deduplicate` (line 236) - *Remove exact duplicates based on config dedup keys.

Two observations are identical if they share the same values for all
exact_dedup_keys. The first occurrence is kept.*
- `_group_by_entity` (line 254) - *Group observations and entities by canonical entity id.

Primary grouping key is the explicit entity list. Observations are
attached to groups when the entity value appears in the observation's
parsed data or the observation source matches the entity's sources.*
- `_classify_groups` (line 338) - *Assign each group a relevance tier and score.*
- `_assign_tier` (line 403) - *Determine the relevance tier based on source count and reliability.

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

**Classs:**
- `RelationshipInferer` (line 36) - *Translate a single observation into one or more knowledge-graph edges.

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

**Functions:**
- `register_inferer` (line 63) - *Decorator: register `func` as the inferer for `source_name`.

Re-registration is a debug log + overwrite; the orchestrator picks
the LAST registered inferer for a given source name, so a test
can monkey-patch an inferer without monkey-patching the source.*
- `infer_relationship` (line 78) - *Dispatch an observation to its inferer (if any).

Returns True if an inferer ran, False otherwise. An inferer that
raises is logged at WARNING and returns False; the orchestrator
keeps going so one bad source doesn't poison the whole run.*
- `_infer_dns` (line 105)
- `_infer_crtsh` (line 114)
- `_infer_shodan` (line 122)
- `_infer_greynoise` (line 134)
- `_infer_abuseipdb` (line 143)
- `_infer_whois` (line 152)
- `_infer_urlscan` (line 163)
- `_infer_phonebook` (line 175)
- `_infer_ipapi` (line 186)
- `_infer_otx` (line 195)
- `_infer_nvd` (line 208)
- `__call__` (line 51)
- `deco` (line 70)

#### `reliability_scoring.py`
**Path:** `estorides_core/reliability_scoring.py`

**Classs:**
- `SourceReliability` (line 36) - *NATO Admiralty source-reliability rating (A-F).*
- `Credibility` (line 47) - *NATO Admiralty information-credibility rating (1-6).*
- `SourceType` (line 58) - *Source type hierarchy: primary > secondary > tertiary.

Orthogonal to NATO reliability: a primary source (official WHOIS) and a
secondary source (social media) can both be rated A, but the primary
contributes more weight because it is institutionally closer to the truth.*
- `ConfidenceInput` (line 199) - *Validated input to :func:`compute_confidence`.*
- `ConfidenceResult` (line 219) - *Auditable output of :func:`compute_confidence` / :func:`merge_confidence`.*

**Functions:**
- `_corroboration_weight` (line 236) - *``min(1, log10(1 + n))``.  0 sources → 0; 1 → 0.30; 9 → 1.0.*
- `_freshness_weight` (line 243) - *Exponential decay.  age=0 → 1.0; one half-life → 0.5.*
- `_validate_score` (line 253)
- `_clamp01` (line 258) - *Clamp to the closed unit interval.*
- `compute_confidence` (line 268) - *Compute the audit-trailed confidence score for one observation.

Pure: no I/O, no logging, no clock. Identical input identical output
bit-by-bit. Bounded to [0, 1]. The formula is:

    score = base * reliability_weight * credibility_weight
          * source_type_weight * corroboration_weight * freshness_weight*
- `merge_confidence` (line 306) - *Merge a new observation's confidence into an existing entity score.

The result is ``max(existing, new_score)`` clamped to ``[0, 1]``. An
unreliable new observation cannot raise a strongly-corroborated
existing one; a reliable new observation can lift a weakly-attested
one. The :class:`ConfidenceResult` exposes the weights of the *new*
observation so the audit trail is intact.*
- `reliability_from_name` (line 356) - *Look up the reliability for a source by name; never raises.

Operator input is potentially adversarial. We do not log, do not
validate beyond ``lower().strip()``, and never raise. Unknown names
fall back to :data:`DEFAULT_RELIABILITY`.*
- `source_type_from_name` (line 371) - *Look up the source type hierarchy for a source by name; never raises.

Operator input is potentially adversarial. Same contract as
:func:`reliability_from_name`: no logging, no raising, no ReDoS.
Unknown names fall back to :data:`DEFAULT_SOURCE_TYPE` (TERTIARY).*
- `__post_init__` (line 209)

#### `scope.py`
**Path:** `estorides_core/scope.py`

**Classs:**
- `ScopeRule` (line 89) - *A single scope predicate. Implementations match exactly one grammar.*
- `WildcardRule` (line 102) - *`*.example.com` — the apex and any subdomain of it.*
- `ExactHostRule` (line 117) - *A single fully-qualified host, matched verbatim.*
- `CidrRule` (line 130) - *An IPv4/IPv6 network; matches any address inside it.*
- `RegexRule` (line 148) - *A compiled regex matched against the raw normalised asset.*
- `ScopeMatcher` (line 234) - *Classifies assets against in-scope and out-of-scope rule sets.

Out-of-scope is evaluated first and wins outright, so an asset that
matches both a broad in-scope wildcard and a narrow out-of-scope rule
is reported as out-of-scope.*
- `ScopeReport` (line 344) - *Classified assets plus the flat lists an operator pipes onward.*

**Functions:**
- `normalise_asset` (line 52) - *Reduce a raw asset string to a comparable host or IP literal.

Strips an optional scheme, any path/query, a port, surrounding
whitespace and a trailing dot, and lowercases the result. A value that
is already a bare host or IP passes through unchanged (bar casing).*
- `is_ip` (line 79) - *True when `asset` parses as a bare IPv4 or IPv6 address.*
- `_wildcard_factory` (line 161)
- `_regex_factory` (line 168)
- `_cidr_factory` (line 179)
- `_ip_factory` (line 188)
- `_exact_host_factory` (line 195)
- `parse_rule` (line 211) - *Parse one rule line into a ScopeRule, or None for blank/comment/invalid.*
- `parse_rules` (line 223) - *Parse many rule lines, skipping blanks, comments and invalid entries.*
- `load_rules_file` (line 285) - *Build a matcher from a rules file, honouring the out-of-scope divider.

Lines above a ``## out-of-scope`` divider (case-insensitive) are
in-scope; lines below are out-of-scope. A file with no divider is all
in-scope.*
- `load_assets` (line 303) - *Read assets from a file: a discover surface JSON or a flat host list.

A JSON document is mined for assets in `domains`, `entities` (values of
host/ip types) and any top-level list of strings. Anything else is read
as one asset per line.*
- `_assets_from_json` (line 322) - *Extract candidate assets from a parsed discover/result JSON document.*
- `build_report` (line 371) - *Classify `assets` with `matcher` and return a :class:`ScopeReport`.*
- `write_flat_lists` (line 381) - *Write newline-delimited flat lists for piping into active tooling.

Produces `in_scope_hosts.txt`, `in_scope_ips.txt` and `unknown.txt`
under `out_dir`. Returns the map of label to written path.*
- `matches` (line 93) - *True when `asset` (already normalised) is covered by this rule.*
- `describe` (line 97) - *Human-readable form of the rule, for reports and audit.*
- `matches` (line 107)
- `describe` (line 112)
- `matches` (line 122)
- `describe` (line 125)
- `matches` (line 135)
- `describe` (line 143)
- `matches` (line 153)
- `describe` (line 156)
- `__init__` (line 242)
- `in_rules` (line 251)
- `out_rules` (line 255)
- `classify` (line 258) - *Return IN_SCOPE, OUT_OF_SCOPE or UNKNOWN for a single asset.*
- `partition` (line 269) - *Bucket many assets, returning sorted, de-duplicated lists.

Keys are IN_SCOPE, OUT_OF_SCOPE and UNKNOWN. De-duplication is on
the normalised form so `HTTPS://Example.com/` and `example.com`
collapse to one entry.*
- `hosts` (line 352) - *In-scope hostnames (everything in-scope that is not an IP).*
- `ips` (line 357) - *In-scope bare IP addresses.*
- `to_dict` (line 361)

#### `search_telemetry.py`
**Path:** `estorides_core/search_telemetry.py`

**Classs:**
- `SearchTelemetryError` (line 37) - *Base class for every error raised by this module.*
- `UnknownPhaseError` (line 41) - *Raised when a phase key is not part of the configured vocabulary.*
- `InvalidTelemetryConfigError` (line 45) - *Raised when a :class:`TelemetryConfig` violates a construction rule.*
- `KeyboardShortcut` (line 117) - *A single keyboard shortcut: the key chord and what it does.*
- `SplashTip` (line 125) - *A single onboarding tip: a short title and a one-line body.*
- `SearchPhase` (line 133) - *A search lifecycle phase: a stable key, a human label and activity flag.

``active`` is ``True`` while work is in flight (the UI shows a spinner) and
``False`` for the resting states ``idle``, ``done`` and ``error``.*
- `ProgressView` (line 146) - *Immutable, render-ready snapshot of search progress.

Carries the clamped counters, the percentage, the human label and the ARIA
attributes a screen reader needs to announce a live progress region.*
- `TelemetryConfig` (line 177) - *Frozen catalog: brand, tagline, shortcuts, tips and phase vocabulary.

``__post_init__`` enforces every invariant in spec/search_telemetry.md so an
invalid catalog can never reach the UI. All construction failures raise
:class:`InvalidTelemetryConfigError`.*
- `SearchTelemetry` (line 217) - *Service over a :class:`TelemetryConfig`: progress math and catalog views.

Stateless and side-effect free; safe to instantiate or share per request.*

**Functions:**
- `disallowed_brands_in` (line 75) - *Return the third-party brand tokens found in ``text``.

Matching is case-insensitive and word-boundary aware so an ordinary word
that merely contains a brand as a substring does not produce a false
positive. The returned tuple holds the canonical lowercase brand names in
first-seen order, de-duplicated.*
- `emoji_in` (line 89) - *Return the emoji glyphs found in ``text``, de-duplicated in order.

Emoji are codepoints in the pictographic blocks (Miscellaneous Symbols,
Dingbats, regional indicators, the supplementary pictographic planes) and
the emoji variation selector. Geometric line-symbols outside those blocks
are permitted iconography and are not flagged.*
- `percent_encoded_emoji_in` (line 103) - *Return percent-encoded supplementary-plane emoji sequences in ``text``.

Catches an emoji smuggled into a ``data:`` URI (for example an emoji
favicon) as the UTF-8 lead bytes ``%F0%9F`` followed by two continuation
bytes. The returned tuple holds the matched sequences in first-seen order.*
- `_assert_clean` (line 167) - *Raise :class:`InvalidTelemetryConfigError` if any text leaks brand/emoji.*
- `_default_config` (line 309) - *Build the canonical Estorides telemetry catalog.*
- `__post_init__` (line 191)
- `__init__` (line 223)
- `shortcuts` (line 229) - *Return the keyboard-shortcut catalog.*
- `tips` (line 233) - *Return the onboarding tips catalog.*
- `phases` (line 237) - *Return the search-phase vocabulary.*
- `phase` (line 241) - *Return the phase for ``key`` or raise :class:`UnknownPhaseError`.*
- `progress` (line 249) - *Compute a clamped, render-ready :class:`ProgressView`.

Out-of-range counters are clamped, never rejected; only an unknown
``phase_key`` raises (:class:`UnknownPhaseError`). When ``total`` is not
yet known (``<= 0``) and the phase is active the view is indeterminate.*
- `context` (line 288) - *Return the JSON-serialisable catalog for template/JS injection.*

#### `source_health_monitoring.py`
**Path:** `estorides_core/source_health_monitoring.py`

**Classs:**
- `SourceHealthStatus` (line 53) - *Operational health classification for an OSINT source.*
- `SourceHealthConfig` (line 64) - *Thresholds for source health classification.

Every field has a corresponding ``ESTORIDES_HEALTH_*`` environment
variable override at import time. The defaults are conservative:
three failures in ten = degrading; a week offline = stale.*
- `SourceHealthInput` (line 120) - *Raw per-source data for health computation.

All fields are required; the caller (orchestrator, fusion analytics)
extracts these from the fusion store or its own tracking.*
- `SourceHealthResult` (line 156) - *Health assessment for a single source.*
- `DashboardSummary` (line 182) - *Aggregate dashboard statistics.*
- `HealthDashboard` (line 195) - *Grouped health view: hot sources, degrading sources, aggregate stats.*

**Functions:**
- `_env_float` (line 28) - *Read a float env var, falling back to default on absence/error.*
- `_env_int` (line 40) - *Read an int env var, falling back to default on absence/error.*
- `_clamp01` (line 224)
- `_classify` (line 232) - *Classify a source's health status based on thresholds.*
- `compute_health` (line 257) - *Compute the health assessment for a single source.

Pure: no I/O, no logging, deterministic. The formula is::

    success_weight = success_rate ^ 2
    latency_weight = clamp(1 - avg_latency_s / degrading_latency_s, 0, 1)
    freshness_weight = clamp(1 - freshness_hours / stale_hours, 0, 1)
    health_score = 0.5 * success_weight + 0.3 * latency_weight + 0.2 * freshness_weight*
- `build_dashboard` (line 317) - *Build a health dashboard from per-source health inputs.

Groups sources into hot (healthy), degrading (degrading + stale), and
unknown lists. Computes aggregate summary statistics.*
- `__post_init__` (line 80)
- `__post_init__` (line 134)
- `to_dict` (line 168)
- `to_dict` (line 206)

#### `source_loader.py`
**Path:** `estorides_core/source_loader.py`

**Classs:**
- `Source` (line 22) - *A source is a YAML-defined OSINT data provider.

Stored as a dict for JSON-serialisation convenience, but exposes
attribute access for ergonomic call sites.*
- `SourceRegistry` (line 38) - *Loads YAML sources from the sources/ directory and exposes them by name.*

**Functions:**
- `__init__` (line 28)
- `__getattr__` (line 31)
- `__init__` (line 41)
- `load` (line 47)
- `_load_file` (line 71)
- `_normalise` (line 100)
- `get` (line 160)
- `all` (line 163)
- `by_category` (line 166)
- `categories` (line 169)
- `names` (line 172)
- `filter` (line 175) - *Return sources matching the given predicates.

`max_contact` keeps only sources whose contact class is at or below
the given ceiling (e.g. "none" for a passive-only run, "broker" to
also allow third-party probes). Sources with an unknown contact
class are treated as the most exposing and thus excluded by any
ceiling below `active`.*
- `summary` (line 197) - *Compact summary used by /api/status.*

#### `ssrf_guard.py`
**Path:** `estorides_core/ssrf_guard.py`

**Classs:**
- `GuardResult` (line 99)
- `SSRFError` (line 277) - *Raised when an outbound URL fails the SSRF guard.*

**Functions:**
- `_is_blocked_v4` (line 110)
- `_is_blocked_v6` (line 114) - *Match an IPv6 textual address against the prefix table.

Lower-cased, leading zeros collapsed, no scope-id parsing required.*
- `_normalise_host` (line 134) - *Lowercase, strip brackets from IPv6 literals, return None if empty.*
- `_is_host_in_blocked_literal` (line 142) - *If `host` is a literal IP in a blocked range, return a reason string.
Otherwise return None.*
- `_resolve` (line 163) - *Resolve `host` to its A + AAAA records. Empty on failure.*
- `_matches_allowlist` (line 180) - *Return True if `host` matches any entry in the allowlist.

An entry like `osiris.example.com` matches the host itself and any
subdomain. An entry like `*` matches everything (escape hatch).*
- `_load_allowlist` (line 197)
- `check_url` (line 202) - *Validate a URL for outbound fetch.

Args:
    url: the URL string the source YAML wants us to hit.
    resolve: when True (default) also resolve hostnames and reject
        if any answer lands in a reserved range. Disable only in
        tests with mocked DNS.

Returns:
    GuardResult with allowed/reason. Use as a bool.*
- `assert_safe` (line 270) - *Raise SSRFError if `url` is not safe to fetch.*
- `__bool__` (line 105)

#### `target_management.py`
**Path:** `estorides_core/target_management.py`

**Classs:**
- `TargetResult` (line 133)
- `BatchResult` (line 171)
- `TargetManager` (line 191)

**Functions:**
- `auto_detect_type` (line 69)
- `_type_validator` (line 76)
- `validate_type` (line 95)
- `validate_value` (line 103)
- `validate_target` (line 117)
- `make_target_id` (line 128)
- `__init__` (line 137)
- `to_dict` (line 158)
- `__init__` (line 174)
- `to_dict` (line 181)
- `__init__` (line 193)
- `add_target` (line 203)
- `batch_import` (line 313)
- `csv_parse` (line 352)
- `batch_csv_import` (line 366)

#### `transforms.py`
**Path:** `estorides_core/transforms.py`

**Classs:**
- `Transform` (line 41) - *One named transform applicable to a set of entity types.*
- `TransformRegistry` (line 190) - *Holds every transform and dispatches by id.*

**Functions:**
- `_empty` (line 61)
- `_resolver_filtered` (line 65) - *Resolve `(ent_type, value)` and keep only links whose relation is
in `relations` (or every link when `relations` is None). The root
node plus any node touched by a kept link is returned.*
- `_filter_runner` (line 86)
- `_norm` (line 95)
- `_osiris` (line 100)
- `_run_bgp` (line 108)
- `_run_leaks` (line 134)
- `_run_github` (line 159)
- `_T` (line 230)
- `summary` (line 51)
- `run` (line 87)
- `__init__` (line 193)
- `register` (line 196)
- `for_type` (line 199)
- `run` (line 209)

#### `transliteration.py`
**Path:** `estorides_core/transliteration.py`

**Functions:**
- `_strip_diacritics` (line 76) - *Drop combining marks via NFKD decomposition.

Folds ``é`` -> ``e``, ``ü`` -> ``u``, full-width forms to ASCII, and so
on. Characters that have no compatibility decomposition pass through
unchanged and are handled by the per-script map instead.*
- `to_latin` (line 87) - *Return a lowercased, diacritic-free Latin transliteration.

The pipeline is: casefold -> NFKD diacritic strip (so accented Greek
and Latin fold to their base letters) -> per-character script map
(Cyrillic/Greek/Arabic) -> keep only ``[a-z0-9 ]``. Casefolding and
stripping run *before* the map so that uppercase and accented source
letters reach the lowercase, accent-free keys the map is written for.
Whitespace is collapsed to single spaces and the result is trimmed.
Non-mappable characters (e.g. unmapped CJK) are dropped, which is the
safe failure mode for fuzzy matching.*
- `consonant_skeleton` (line 112) - *Return the Latin transliteration with vowels and spaces removed.

This is the vowel-insensitive comparison key. Abjad scripts (Arabic,
Hebrew) routinely omit short vowels, so two spellings of the same name
can only be reconciled on their consonant skeletons. The first
character is preserved even if it is a vowel, because name-initial
vowels are usually written and carry signal.

Adjacent duplicate letters are collapsed so that gemination written as
a doubled Latin consonant (``Muhammad`` -> ``mhmmd``) reconciles with a
script that marks it with a diacritic instead of doubling the letter
(Arabic ``محمد`` -> ``mhmd``).*
- `is_non_latin` (line 139) - *True if any character is outside the Basic Latin / Latin-1 range.

Used by the resolver to decide whether the cross-script path is worth
taking for a given value before paying for transliteration of both
sides of a comparison.*

#### `validation.py`
**Path:** `estorides_core/validation.py`

**Classs:**
- `QueryValidationError` (line 55) - *Raised when a query fails validation. The reason is in `.reason`.*
- `Query` (line 63) - *A validated, normalised query string.*

**Functions:**
- `_strip_and_collapse` (line 73)
- `validate_query` (line 85) - *Validate and normalise a user query string.

Args:
    raw: the user-supplied query, exactly as received.
    max_length: hard cap on the normalised length. Default 512.

Raises:
    QueryValidationError if the query is empty, oversized, contains
    forbidden characters, or resolves to a type the engine cannot
    dispatch on.

Returns:
    A `Query` with the normalised text and detected type.*
- `__init__` (line 57)
- `__str__` (line 69)

#### `web_security.py`
**Path:** `estorides_core/web_security.py`

**Classs:**
- `WebSecurityConfig` (line 53) - *Resolved security policy for the Flask app.

All fields are read from the environment at import time and frozen so
the policy cannot drift at runtime. Changing a knob requires a restart
— the right call for a tool that mostly runs as a long-lived daemon.*
- `AuthGate` (line 301) - *Bearer-token gate applied to sensitive routes.

`required_token` is the single shared secret. `None` disables the gate
(local-trust mode). Comparison is constant-time.*

**Functions:**
- `_env_str` (line 102)
- `_env_int` (line 109)
- `_env_bool` (line 120)
- `load_security_config` (line 127) - *Resolve the security policy from env vars.

ESTORIDES_CORS_ORIGINS    comma-separated list, e.g. "https://app.example.com"
ESTORIDES_MAX_BODY_BYTES  int, default 1 MiB
ESTORIDES_HSTS            1 to emit Strict-Transport-Security
ESTORIDES_FORCE_HTTPS     1 to redirect plain http to https (only meaningful behind TLS)
ESTORIDES_CSP             override the default Content-Security-Policy*
- `install_security` (line 150) - *Wire security middleware into a Flask app.

Idempotent: calling twice is a no-op (we re-attach, but Flask keeps the
last hook, and our hooks are stateless). Returns the resolved config so
the caller can echo it in a startup banner.*
- `_extract_bearer_token` (line 264) - *Pull the bearer token from header, alt-header, or cookie.

Header order matters: an explicit `Authorization: Bearer` always wins
over a cookie (the cookie is the fallback for the browser UI; the
header is what scripts and curl will use). We never trust query-string
tokens — they leak into access logs and referer headers.*
- `make_auth_gate` (line 284) - *Build the auth gate from the current environment.

`ESTORIDES_AUTH_TOKEN` unset → `enabled=False`, `require_auth` is a no-op
pass-through. This preserves the local-trust single-user default and keeps
existing tests working without an auth header.

When set, the gate is enabled. The token is also exposed to `index.html`
so the UI can auto-attach it (see `auth_meta_for_index()`).*
- `require_auth` (line 348) - *Decorator: enforce the bearer-token gate on a view.

Behaviour:
  * gate disabled (no env var) → pass-through, no overhead.
  * gate enabled, token missing → 401 with `WWW-Authenticate: Bearer`.
  * gate enabled, token present but wrong → 401 (same shape, constant-
    time compare on the server side).

Use on every endpoint that reads or mutates operator-private data:
cases, run, run/stream/*, discover/*, export, intel/*, transform/*,
osiris/*, graph, status.*
- `install_auth_gate` (line 381) - *Attach the gate to a Flask app and a module-level slot.

Two consumers read the gate: the `require_auth` decorator (module
slot, so it works even when called outside a request context) and
`auth_meta_for_index()` (so `index.html` can be rendered with the
token embedded for the UI to pick up).*
- `_current_gate` (line 399)
- `is_cors_enabled` (line 93)
- `is_origin_allowed` (line 97) - *CORS is opt-in; this is the runtime check used by the after_request hook.*
- `_security_headers` (line 195)
- `_cors_preflight` (line 228)
- `enabled` (line 311)
- `check` (line 314)
- `auth_meta_for_index` (line 322) - *Token to embed in `index.html` so the UI can auto-authenticate.

Returns `None` when the gate is off (the UI then omits the meta
tag and every call goes through anonymously, which is the
local-trust default).*
- `issue_session_cookie_kwargs` (line 331) - *Arguments for `set_cookie` to install the session cookie.

`Secure` is set when the request itself is over HTTPS or the operator
requested ESTORIDES_FORCE_HTTPS=1 (in that case we know they're behind
TLS). `SameSite=Lax` keeps the cookie from cross-site POSTs.*
- `wrapper` (line 362)
- `_redirect_to_https` (line 184)

#### `__init__.py`
**Path:** `estorides_export/__init__.py`

*No symbols extracted*

#### `encryption.py`
**Path:** `estorides_export/encryption.py`

**Functions:**
- `_have_age` (line 47)
- `encrypt_file` (line 51) - *Encrypt `plaintext_path` to `<plaintext_path>.age` for the recipient.

Returns the ciphertext path. Raises RuntimeError if `age` is
missing or the encryption subprocess fails — the orchestrator
catches and falls back to plaintext. Raises ValueError if
`recipient_pubkey` doesn't look like an age public key.

Validation order is: key shape (cheap, no exec) → binary
presence (filesystem stat) → subprocess. A malformed key is
always a programmer error and surfaces as ValueError; a missing
binary is an environment problem and surfaces as RuntimeError.*
- `export_stix_encrypted` (line 100) - *Build the STIX bundle, write to disk, encrypt to <path>.age.

`path` is the plaintext filename; the returned path is the
encrypted artefact next to it. The plaintext is removed once
encryption succeeds so reports/ never accumulates raw intel
bundles — that was the disk-residue problem fixed for issue #8.*
- `export_misp_encrypted` (line 128)

#### `misp.py`
**Path:** `estorides_export/misp.py`

**Functions:**
- `event_from_graph` (line 36)
- `_category` (line 65)
- `export` (line 79)

#### `report.py`
**Path:** `estorides_export/report.py`

**Functions:**
- `_tldr` (line 37) - *Top-of-page executive summary. 6-10 lines max.*
- `_iocs` (line 77) - *The sections the next responder (CTI team, SOC) actually pastes
into a ticket. Domains, IPs, emails, hashes, CVEs, crypto addresses.*
- `_diff_section` (line 121) - *The "what's new since last run" block. Empty when no baseline.*
- `_analysis` (line 156) - *The LLM analysis (or stub) embedded verbatim in a code block.*
- `_meta_footer` (line 177)
- `render_markdown_report` (line 194) - *Build a Markdown report for `case`.

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
- `_id` (line 28)
- `_now` (line 32)
- `bundle_from_graph` (line 55)
- `export` (line 145)

#### `__init__.py`
**Path:** `estorides_llm/__init__.py`

*No symbols extracted*

#### `intelligence_prompts.py`
**Path:** `estorides_llm/intelligence_prompts.py`

**Functions:**
- `format_context` (line 98) - *Render a list of observation dicts into a context block for the LLM.

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

**Classs:**
- `LLMBackend` (line 37) - *Minimal contract for an LLM backend.

Implementations MUST be total: raise on failure (the manager
catches and moves on) or return ("", "") to signal "I can't
answer, try the next backend".*
- `OllamaBackend` (line 86)
- `_OpenAICompatibleBackend` (line 143) - *Shared implementation for OpenAI-shaped APIs (openai, openrouter, …).

Subclasses set `name`, `env_key`, and `base_url`.*
- `OpenAIBackend` (line 179)
- `OpenRouterBackend` (line 186)
- `AnthropicBackend` (line 193)
- `LLMManager` (line 233)

**Functions:**
- `register` (line 63) - *Decorator: register a backend under `name`.

Accepts both an instance and a class. If a class is given, the
decorator instantiates it with no arguments — which is the
common case for stateless backends that hold no per-instance
state. The class must therefore have a no-arg constructor.*
- `__call__` (line 46) - *Return (content, model_id). Empty content means "skip me".*
- `deco` (line 71)
- `_resolve_model` (line 89) - *Pick a model ollama actually has pulled.

Prefers the configured model; falls back to the first available
tag so a stale config can't silently degrade every run to the
stub. (Previous behaviour; preserved here.)*
- `__call__` (line 116)
- `__call__` (line 151)
- `__call__` (line 196)
- `__init__` (line 234)
- `generate` (line 250) - *Try each backend in priority order; return the first that succeeds.

`request_timeout` caps every backend's HTTP call so a slow
local model cannot keep a worker thread alive past the
orchestrator's deadline. Returns a dict with keys:
backend, model, content, error.*
- `_stub_response` (line 292)

#### `estorides_web.py`
**Path:** `estorides_web.py`

**Classs:**
- `_RunStreamJob` (line 109) - *A live deep-run cross-search whose events feed an SSE stream.

Wraps a `BufferedEventSink` (the engine writes to it) and a cooperative
stop flag the UI can set. Status and terminal state are read straight
off the sink so there is one source of truth.*

**Functions:**
- `_client_ip` (line 62) - *Best-effort client IP extraction.

Trusts X-Forwarded-For only when behind a known proxy
(ESTORIDES_TRUST_PROXY=1). Without that, falls back to
`request.remote_addr`. This avoids the classic
"set X-Forwarded-For to bypass rate limits" mistake on a
directly-exposed deployment.*
- `_arg_int` (line 79) - *Read an int query-string arg, falling back to `default` on parse error.

Guards every endpoint that previously did `int(request.args.get(...))`
directly, where a non-numeric value raised ValueError and surfaced as
an unhandled 500 to the client.*
- `_send_and_cleanup` (line 95) - *Send `p` as an attachment, then nuke `tmpdir` regardless of outcome.

Used by /api/export/<fmt> so reports/ doesn't accumulate a copy of
every exported bundle — see issue #43. The `finally` runs even when
the client disconnects mid-stream, which is the realistic failure
case for the exhaustion attack.*
- `_new_stream_job_id` (line 147) - *Timestamp-prefixed id so jobs sort chronologically.*
- `_rate_limit_decorator` (line 152) - *Decorator: enforce per-IP rate limit, write an audit row either way.

Catches the rate-limit denial BEFORE doing real work, so a flood
can't tie up the orchestrator. Audit row written for both allow
and deny so the trail is complete.*
- `create_app` (line 196)
- `_serve_loop` (line 1161)
- `_shape_for_ui` (line 1174) - *Trim raw responses for the UI and reformat observations.*
- `__init__` (line 117)
- `stop` (line 126)
- `should_stop` (line 129)
- `status` (line 133)
- `done` (line 137)
- `deco` (line 159)
- `index` (line 212)
- `api_status` (line 228)
- `api_run` (line 234)
- `api_graph` (line 290)
- `api_feeds` (line 366) - *Return real-time feed points (quakes, fires, news) for the map.

Optional query string:
  bbox=min_lon,min_lat,max_lon,max_lat — drop points outside.
  no_cache=1 — bypass the on-disk cache.*
- `api_export` (line 397)
- `api_cases_list` (line 472)
- `api_cases_get` (line 486)
- `api_cases_delete` (line 501)
- `api_cases_save` (line 510) - *Bookmark a case from the UI.

Sets a `notes` prefix so the case is easy to spot in the cases
list, then echoes the updated case back. The store is
append-only for observations, but `notes` is a free-text column
we can overwrite. This is the "I want to come back to this"
gesture: in v1 the only durable artefact was the case id; in
v1.3 we want the user to be able to tag their wins.*
- `api_cases_diff` (line 539) - *Symmetric diff between two cases by entity (type, value).

Query string: ?a=<case_id>&b=<case_id>
Returns the entities present in B but not in A ("added"), the
inverse ("removed"), and the per-type breakdown. The UI uses
this to show "what's new since last run" without a re-query.*
- `api_intel_resolve` (line 565) - *Cross-feed entity resolution (Osiris-style /resolve).

Examples:
  GET /api/intel/resolve?type=ip&id=1.1.1.1
  GET /api/intel/resolve?type=person&id=Tim%20Cook
  GET /api/intel/resolve?type=cve&id=CVE-2024-3094*
- `api_intel_graph` (line 605) - *Cypher query against the Kùzu persistent graph.

Examples:
  GET /api/intel/graph?q=MATCH%20(n%3AEnt)%20RETURN%20n.id%20LIMIT%2010*
- `api_intel_stats` (line 647) - *Stats for both the case store and the Kùzu graph.*
- `api_fusion_stats` (line 663) - *One-glance dashboard of the fused, cross-run fact base.*
- `api_fusion_sources` (line 672) - *The YAML source catalogue with accumulated fetch/ok counters.*
- `api_fusion_entities` (line 682) - *Search fused entities.

Example: GET /api/fusion/entities?q=google&type=domain&min_sources=2
``min_sources`` is the fusion-native filter: only entities that at
least N distinct feeds corroborate.*
- `api_fusion_entity` (line 704) - *Full fused view of one entity: provenance, properties, edges.

``min_sources`` (default 2) also returns the corroborated properties:
attributes that independent feeds agree on.*
- `api_fusion_analytics_entity_timeline` (line 723)
- `api_fusion_analytics_entity_summary` (line 734)
- `api_fusion_analytics_source_stats` (line 745)
- `api_fusion_analytics_consensus` (line 756)
- `api_fusion_analytics_top_changed` (line 767)
- `api_fusion_analytics_corroboration_matrix` (line 777)
- `api_transforms` (line 791) - *List the transforms applicable to an entity type.

Example: GET /api/transforms?type=ip*
- `api_transform_run` (line 806) - *Run one transform and return nodes/links for graph merge.

Body: {"transform_id": "...", "type": "ip", "value": "1.2.3.4"}*
- `api_osiris_bgp` (line 830)
- `api_osiris_mac` (line 841)
- `api_osiris_phone` (line 852)
- `api_osiris_github` (line 863)
- `api_osiris_leaks` (line 874)
- `api_osiris_kev` (line 885)
- `api_osiris_malware` (line 895)
- `api_osiris_threats` (line 902)
- `api_discover_start` (line 915)
- `api_discover_jobs` (line 961)
- `api_discover_stop` (line 967)
- `api_discover_stream` (line 979) - *Server-Sent Events for a discoverer job.

The browser opens `EventSource('/api/discover/stream?job_id=...')`
and we keep the connection open, pushing one event per
JSON line as the background worker discovers things. The
stream closes when the job finishes (status=done|error|stopped).*
- `api_run_stream_start` (line 1034)
- `api_run_stream_stop` (line 1101)
- `api_run_stream` (line 1113)
- `wrapper` (line 161)
- `gen` (line 992)
- `_drive` (line 1064)
- `gen` (line 1119)

#### `conftest.py`
**Path:** `tests/conftest.py`

*No symbols extracted*

#### `test_change_detection_properties.py`
**Path:** `tests/properties/test_change_detection_properties.py`

**Functions:**
- `test_scores_always_bounded` (line 69)
- `test_max_changes_respected` (line 77)
- `test_id_is_16_char_hex` (line 86)
- `test_idempotent` (line 95)
- `test_first_run_reports_all_as_new` (line 105)
- `test_after_none_returns_empty` (line 113)
- `test_before_vs_no_after_empty` (line 121)
- `test_summary_consistency` (line 132) - *Whatever the input, the summary fields must agree with the
``changes`` list: ``total == len(changes)``, ``by_kind`` counts
each kind exactly, ``score_max/mean`` are derived from the actual
changes, and ``entities_compared == len(before.entities)`` (or 0 if
``before`` is None).*

#### `test_csp_safe_styles_properties.py`
**Path:** `tests/properties/test_csp_safe_styles_properties.py`

**Functions:**
- `test_js_never_gains_a_style_attribute_in_template_literal` (line 58) - *Hypothetical: a future patch appends the given string somewhere
in the JS. The codebase should still be free of `style="…"` in any
backtick-delimited template literal.

Strategy: simulate the patch as the insertion landing in any random
position of the file, then re-check the invariant. With 1000
random `insertion` x random offset combinations, the test exercises
the structural property: there is no `style="…"` substring inside
any backtick literal in the current file.*
- `test_template_never_gains_a_style_attribute` (line 105) - *Hypothetical: a future patch adds the given string somewhere in
the template. The contract is that `style="…"` does not exist in
any static markup of `templates/index.html`.

Jinja expressions `{{ … }}` and `{% … %}` are stripped before
scanning so we test the static part of the document.*
- `test_csp_style_src_never_gains_unsafe_inline` (line 137) - *Hypothetical: a future patch sets `style-src` to
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
- `test_scores_always_bounded` (line 54)
- `test_claim_length_under_cap` (line 66)
- `test_reasoning_length_under_cap` (line 77)
- `test_sources_sorted_unique` (line 88)
- `test_id_is_deterministic_hex` (line 99)
- `test_idempotent` (line 112)
- `test_max_hypotheses_caps_output` (line 123)
- `test_min_score_filters` (line 134)
- `test_hostile_observation_does_not_crash` (line 147)

#### `test_recon_fusion_properties.py`
**Path:** `tests/properties/test_recon_fusion_properties.py`

**Classs:**
- `TestPropertyScoreBounds` (line 48) - *P1 -- Scores are always in [0, 1].*
- `TestPropertyTotalCounts` (line 68) - *P2 -- total_observations and total_entities match input.*
- `TestPropertyTierSumMatches` (line 93) - *P3 -- tier_summary counts match actual tier list lengths.*
- `TestPropertyDeterminism` (line 114) - *P4 -- Same input always produces same output (time-independent fields excluded).*
- `TestPropertyNoDuplicates` (line 135) - *P5 -- No duplicate canonical_id within the same tier.*
- `TestPropertyTierKeysOrder` (line 155) - *P6 -- result.tiers dict preserves canonical tier key order.*
- `TestPropertyEmptyQueryRejected` (line 176) - *P7 -- Empty query always raises ValueError.*
- `TestPropertySafeWithBadInputs` (line 196) - *P8 -- None observations/entities never crash.*

**Functions:**
- `test_all_scores_in_unit_interval` (line 58)
- `test_counts_match_input` (line 78)
- `test_tier_summary_matches` (line 103)
- `test_deterministic_output` (line 124)
- `test_no_duplicate_ids_in_tier` (line 145)
- `test_tier_keys_in_canonical_order` (line 165)
- `test_empty_query_raises` (line 185)
- `test_none_inputs_safe` (line 201)
- `test_entities_none_is_safe` (line 214)

#### `test_reliability_scoring_properties.py`
**Path:** `tests/properties/test_reliability_scoring_properties.py`

**Functions:**
- `test_score_always_bounded` (line 56)
- `test_corroboration_weight_in_unit_interval` (line 73)
- `test_freshness_monotone_in_age` (line 87)
- `test_reliability_from_name_never_raises` (line 110)
- `test_merge_confidence_bounded` (line 126)
- `test_reliability_weight_set_is_curated` (line 141)
- `test_credibility_weight_set_is_curated` (line 146)
- `test_corroboration_is_monotone_in_count` (line 159)
- `test_higher_reliability_dominates` (line 184)
- `test_source_type_from_name_never_raises` (line 202)
- `test_source_type_weight_always_curated` (line 219)
- `test_source_type_weight_set_is_curated` (line 241)

#### `test_search_telemetry_properties.py`
**Path:** `tests/properties/test_search_telemetry_properties.py`

**Functions:**
- `test_progress_invariants_hold` (line 32)
- `test_progress_rejects_unknown_phase` (line 46)
- `test_brand_predicate_is_total` (line 56)
- `test_emoji_predicate_is_total` (line 65)
- `test_percent_encoded_emoji_predicate_is_total` (line 74)
- `test_brand_predicate_flags_embedded_brand` (line 84)

#### `test_source_health_monitoring_properties.py`
**Path:** `tests/properties/test_source_health_monitoring_properties.py`

**Functions:**
- `_valid_input` (line 21) - *Build a valid SourceHealthInput, clamping ok <= fetch.*
- `test_health_score_always_bounded` (line 49)
- `test_status_always_valid_enum` (line 63)
- `test_success_rate_bounds` (line 78)
- `test_unknown_when_below_min_fetches` (line 89)
- `valid_health_inputs` (line 97)
- `test_dashboard_summary_counts_match` (line 112) - *Dashboard summary counts must sum to total.*

#### `test_target_management_properties.py`
**Path:** `tests/properties/test_target_management_properties.py`

**Functions:**
- `test_p1_add_target_never_raises` (line 21)
- `test_p2_validated_id_is_deterministic` (line 31)
- `test_p3_make_target_id_stable_under_case` (line 40)
- `test_p4_valid_domains_validate` (line 56)
- `test_p5_valid_ipv4_validate` (line 68)
- `test_p6_valid_emails_validate` (line 77)
- `test_p7_auto_detect_never_fails` (line 83)
- `test_p8_validate_target_never_raises` (line 89)
- `test_p9_batch_import_idempotent` (line 105)
- `test_p10_batch_import_never_raises` (line 116)

#### `test_audit_log.py`
**Path:** `tests/test_audit_log.py`

**Functions:**
- `_ev` (line 12)
- `test_audit_log_appends` (line 22)
- `test_audit_log_rotates_when_cap_exceeded` (line 31)
- `test_audit_log_rotation_respects_keep_count` (line 48)
- `test_audit_log_no_rotation_when_disabled` (line 61)

#### `test_auth_gate.py`
**Path:** `tests/test_auth_gate.py`

**Functions:**
- `app_with_gate` (line 22) - *A Flask app with the auth gate enabled, token 'sek'.

Each test gets a fresh app so the module-level _GATE slot is clean.*
- `test_gate_off_by_default` (line 41)
- `test_gate_on_rejects_anonymous` (line 49)
- `test_gate_on_accepts_bearer_header` (line 57)
- `test_gate_on_accepts_alt_header` (line 64)
- `test_gate_on_accepts_cookie` (line 70)
- `test_gate_on_rejects_wrong_token` (line 77)
- `test_gate_on_does_not_leak_token_in_meta_when_off` (line 83)
- `test_gate_on_exposes_token_for_index_meta` (line 89)
- `private` (line 34)

#### `test_change_detection.py`
**Path:** `tests/test_change_detection.py`

**Classs:**
- `TestNewEntity` (line 56) - *S1 del spec.*
- `TestPropertyChanged` (line 99) - *S2 del spec.*
- `TestFirstRunBeforeIsNone` (line 125) - *S3 del spec.*
- `TestAfterIsNone` (line 147) - *S4 del spec.*
- `TestDisappearedWithGrace` (line 166) - *S5 del spec.*
- `TestSourceAdded` (line 199) - *S6 del spec.*
- `TestMinReliabilityFiltersSources` (line 226) - *S7 del spec.*
- `TestMaxChangesBounds` (line 255) - *S8 del spec.*
- `TestProgrammerErrorRaises` (line 281) - *S9 del spec.*
- `TestHostilePropertyKey` (line 310) - *S10 del spec.*
- `TestDeterminism` (line 346) - *S11 del spec.*
- `TestSourceRemoved` (line 386) - *S13 del spec: una source que antes veía la entity ya no la ve.*
- `TestEdgeChanges` (line 436) - *S14 del spec: edges salientes que aparecen/desaparecen.*
- `TestConfidenceShifted` (line 488) - *S15 del spec: |confidence_after - confidence_before| > 0.20.*
- `TestBoundedSmoke` (line 528) - *S12 del spec: smoke test del dataclass.*

**Functions:**
- `_entity` (line 28)
- `test_one_new_entity_emits_one_new_change` (line 59)
- `test_new_change_score_in_high_band` (line 84)
- `test_property_change_emits_one_change` (line 102)
- `test_before_none_reports_all_as_new` (line 128)
- `test_after_none_returns_empty_report` (line 150)
- `test_disappeared_within_grace_is_ignored` (line 169)
- `test_disappeared_outside_grace_emits_change` (line 181)
- `test_new_source_on_existing_entity_emits_source_added` (line 202)
- `test_min_reliability_e_excludes_f_source` (line 229)
- `test_max_changes_caps_output` (line 258)
- `test_entity_id_empty_raises` (line 284)
- `test_entity_type_empty_raises` (line 288)
- `test_entity_value_empty_raises` (line 292)
- `test_min_change_score_out_of_range_raises` (line 296)
- `test_max_changes_too_small_raises` (line 302)
- `test_hostile_key_does_not_crash` (line 322)
- `test_same_input_same_ids_and_scores` (line 349)
- `test_input_order_does_not_affect_output` (line 366)
- `test_source_removed_emits_change` (line 389)
- `test_source_removed_filtered_by_min_score` (line 410)
- `test_edge_added_emits_change` (line 439)
- `test_edge_removed_emits_change` (line 462)
- `test_large_confidence_shift_emits_change` (line 491)
- `test_small_confidence_shift_ignored` (line 509)
- `test_change_is_frozen` (line 531)
- `test_diff_is_frozen` (line 541)
- `test_change_report_is_frozen` (line 546)

#### `test_csp_safe_styles.py`
**Path:** `tests/test_csp_safe_styles.py`

**Functions:**
- `_strip_template_jinja` (line 41) - *Replace `{{ ... }}` and `{% ... %}` with empty so the file is grep-able.

We only care whether the *static markup* contains `style="..."`. A
`{{ estorides_auth_token or '' }}` cannot produce a `style="` because
the auth token is a short opaque string and Jinja escapes it
(autoescape=on by default for .html). Even if the token were
malicious, a separate test (S7) covers the injection vector.*
- `_strip_js_comments_and_strings_outside_templates` (line 55) - *Return the *template-literal contents* of the JS file as a single string.

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
- `test_index_html_has_no_style_attribute` (line 90) - *S1 — `style="..."` must not appear anywhere in the rendered template.

Browsers reject inline style attributes under the locked-down
`style-src` policy. The fix is to use CSS classes (or `hidden`) —
not to relax the policy.*
- `test_estorides_js_has_no_style_in_template_literals` (line 111) - *S2 — `style="..."` must not appear in any template literal in the JS.

JS uses `innerHTML = `…`` to inject HTML. The literal text must
not contain `style="…"` because the browser will then try to
apply that style attribute and CSP will block it.*
- `test_offscreen_element_uses_hidden_attribute` (line 145) - *S3 — Each offscreen element must have the HTML5 `hidden` attribute.

The browser's user-agent stylesheet already turns `[hidden]` into
`display: none`, so we don't need a literal `style="display:none"`.*
- `test_css_has_required_class` (line 189) - *The CSS file must define the new classes the refactor relies on.*
- `test_csp_policy_does_not_relax_for_unsafe_inline` (line 201) - *S5 — The locked-down CSP must stay locked down.

The whole point of the refactor is that we don't have to relax
`style-src` to make the UI work. If this test ever fails, the
previous fix was reverted to `'unsafe-inline'` — a regression.*
- `test_csp_policy_is_unchanged_after_refactor` (line 225) - *S6 — The default CSP string is byte-identical to the pre-refactor value.

The fix is in the frontend, not in the policy. If this test fails,
the policy was changed instead of refactored.*
- `test_dynamic_cluster_color_uses_cssom_assignment` (line 252) - *S4 — The bridge-tooltip chip must set background via CSSOM.

We assert that the JS code *does* set `chip.style.background = cs`
(or `span.style.backgroundColor = cs`) and that the HTML string
for the chip is built without a `style="background:…"` attribute.*
- `test_dynamic_kind_color_uses_cssom_assignment` (line 272) - *S4 (kind) — `colorForKind(e.kind)` must reach CSSOM, not innerHTML.*
- `test_rendered_template_has_no_style_attribute_and_uses_hidden` (line 289) - *End-to-end: render `index.html` and assert no inline styles leak.*

#### `test_encrypted_export.py`
**Path:** `tests/test_encrypted_export.py`

**Classs:**
- `_FakeCompleted` (line 21)

**Functions:**
- `_kg_with_one_node` (line 27)
- `_patch_age_ok` (line 33) - *Pretend `age` is on PATH and that `age -e -r ...` produced ciphertext.*
- `test_stix_encrypted_removes_plaintext` (line 43)
- `test_misp_encrypted_removes_plaintext` (line 52)
- `test_stix_encrypted_removes_plaintext_on_failure` (line 61) - *Even when age fails, the plaintext must be removed.*
- `__init__` (line 22)
- `_run` (line 35)
- `_run_fail` (line 66)

#### `test_entity_resolution.py`
**Path:** `tests/test_entity_resolution.py`

**Classs:**
- `TestTransliteration` (line 42) - *Cyrillic, Greek, Arabic, diacritic folding.*
- `TestJaroWinkler` (line 68) - *Jaro-Winkler similarity invariants.*
- `TestNormalization` (line 89) - *Type-aware normalisation.*
- `TestCanonicalId` (line 133) - *Deterministic content-addressed ids.*
- `TestCrossScriptPersonFusion` (line 155) - *ER1: latin + cyrillic + comma-variant → one identity.*
- `TestDomainCaseVariantMerge` (line 194) - *ER2: EvilCorp.com and evilcorp.com → exact merge.*
- `TestLookAlikeDomainsSurfaceAsLink` (line 221) - *ER3: evilcorp.com vs evil-corp.com → SAME_AS link, not merged.*
- `TestDeterministicTypeNoFuzzyMatch` (line 246) - *ER4: md5 differing by one char → separate entities.*
- `TestIdenticalIpsMerge` (line 272) - *ER5: same IP from two sources → merged.*
- `TestNearIpsNeverFuse` (line 289) - *ER6: 8.8.8.8 and 8.8.4.4 → separate.*
- `TestOrgSuffixFolding` (line 309) - *ER7: Evil Corp LLC + Evil Corp → merged.*
- `TestDistinctPersonsStaySeparate` (line 326) - *ER8: Putin and Medvedev → separate identities.*
- `TestCanonicalEntityRoundtrip` (line 347) - *ER9: to_dict and to_entity preserve data.*
- `TestEmptyInput` (line 382) - *ER10: empty list → empty result.*
- `TestCanonicalIdDeterministic` (line 394) - *ER11: same input → same id.*
- `TestDifferentInputDifferentId` (line 406) - *ER12: different input → different id.*
- `TestEdgeCases` (line 418) - *Additional edge cases beyond the spec scenarios.*
- `TestCrossRunStability` (line 448) - *Canonical id stays stable across runs via persistent store.*

**Functions:**
- `_ent` (line 28)
- `_by_value` (line 32)
- `test_cyrillic_to_latin` (line 45)
- `test_greek_accented_to_latin` (line 48)
- `test_diacritic_fold` (line 51)
- `test_consonant_skeleton_arabic_matches_latin` (line 54)
- `test_consonant_skeleton_gemination` (line 57)
- `test_distinct_names_have_distinct_skeletons` (line 60)
- `test_non_latin_detector` (line 63)
- `test_identical_strings_score_one` (line 71)
- `test_empty_pair_scores_zero` (line 74)
- `test_classic_jaro_winkler_bound` (line 77)
- `test_dissimilar_strings_score_low` (line 81)
- `test_scores_stay_in_unit_interval` (line 84)
- `test_ipv4_normalised` (line 92)
- `test_ipv6_compressed` (line 95)
- `test_hash_lowered` (line 101)
- `test_cve_uppered` (line 107)
- `test_domain_strips_scheme_www_path` (line 110)
- `test_person_order_independent` (line 116)
- `test_org_suffix_stripped` (line 121)
- `test_asn_normalised` (line 126)
- `test_email_lowered` (line 129)
- `test_deterministic` (line 136)
- `test_different_values_different_ids` (line 141)
- `test_id_format` (line 146)
- `test_three_spellings_fuse` (line 158)
- `test_fused_identity_carries_all_sources` (line 169)
- `test_cross_script_flagged_in_attributes` (line 180)
- `test_domain_case_variants_merge` (line 197)
- `test_domain_merge_is_exact` (line 207)
- `test_look_alike_domains_stay_separate` (line 224)
- `test_look_alike_domains_produce_same_as_link` (line 233)
- `test_deterministic_near_miss_never_matches` (line 249)
- `test_score_pair_deterministic_mismatch` (line 259)
- `test_identical_ips_merge` (line 275)
- `test_near_ips_stay_separate` (line 292)
- `test_org_suffix_variants_merge` (line 312)
- `test_distinct_persons_not_absorbed` (line 329)
- `test_to_dict_serialises` (line 350)
- `test_to_entity_projects_legacy` (line 361)
- `test_resolution_result_has_one_entity` (line 373)
- `test_empty_input_returns_empty` (line 385)
- `test_same_normalised_same_id` (line 397)
- `test_different_normalised_different_id` (line 409)
- `test_blank_value_does_not_crash` (line 421)
- `test_whitespace_only_handled` (line 425)
- `test_single_entity_produces_one_canonical` (line 429)
- `test_confidence_boosted_by_multiple_sources` (line 434)
- `test_cross_run_id_stability` (line 451)

#### `test_fusion_analytics.py`
**Path:** `tests/test_fusion_analytics.py`

**Classs:**
- `TestEntityTimeline` (line 64)
- `TestEntitySummary` (line 87)
- `TestEntityTimelineNonexistent` (line 109)
- `TestSourceStats` (line 118)
- `TestMultiSourceConsensus` (line 155)
- `TestCorroboratedProperties` (line 176)
- `TestEntitySearch` (line 195)
- `TestTopChanged` (line 230)
- `TestSourceCorroborationMatrix` (line 250)
- `TestWithNoneStore` (line 268)
- `TestBoundaryConditions` (line 281)

**Functions:**
- `store_and_analytics` (line 27)
- `_populate_evilcorp` (line 42)
- `_register_source` (line 57)
- `test_returns_full_timeline` (line 65)
- `test_nonexistent_eid_returns_none` (line 79)
- `test_returns_summary_stats` (line 88)
- `test_nonexistent_eid_returns_none` (line 101)
- `test_returns_none` (line 110)
- `test_returns_source_metrics` (line 119)
- `test_nonexistent_source_returns_none` (line 135)
- `test_success_rate_correct` (line 139)
- `test_consensus_picks_majority_value` (line 156)
- `test_nonexistent_key_returns_empty` (line 165)
- `test_filters_by_min_sources` (line 177)
- `test_min_sources_one_returns_all` (line 185)
- `test_search_by_term` (line 196)
- `test_search_no_results` (line 208)
- `test_search_filter_by_type` (line 213)
- `test_search_with_confidence_and_source_filters` (line 219)
- `test_returns_recently_active_entities` (line 231)
- `test_empty_window_returns_empty` (line 241)
- `test_returns_pairs_with_shared_counts` (line 251)
- `test_all_methods_return_empty` (line 269)
- `test_min_sources_zero_treated_as_one` (line 282)
- `test_negative_days_treated_as_one` (line 288)

#### `test_hypothesis_engine.py`
**Path:** `tests/test_hypothesis_engine.py`

**Classs:**
- `TestHappyPathDomainBelongsToActor` (line 39) - *S1 del spec.*
- `TestEmptyInputProducesEmptyOutput` (line 113) - *S2 del spec.*
- `TestMalformedObservationsAreSkipped` (line 138) - *S3 del spec.*
- `TestUnknownSourceFallsBackToReliabilityC` (line 176) - *S4 del spec.*
- `TestMinScoreFiltersHypotheses` (line 199) - *S5 del spec.*
- `TestMaxHypothesesBounds` (line 230) - *S6 del spec.*
- `TestProgrammerErrorRaisesValueOrTypeError` (line 253) - *S7 del spec.*
- `TestHostileObservationPayloadIsHandled` (line 280) - *S8 del spec.*
- `TestDeterminism` (line 309) - *S9 del spec.*
- `TestBoundedSmoke` (line 351) - *S10 del spec: smoke test del dataclass.*

**Functions:**
- `_obs` (line 23) - *Build a minimal observation dict that matches the orchestrator shape.*
- `generate_hypothences_safe` (line 127)
- `test_emits_domain_belongsto_actor_hypothesis` (line 42)
- `test_score_in_high_band` (line 61)
- `test_supporting_has_three_items` (line 76)
- `test_sources_sorted_and_unique` (line 95)
- `test_empty_observations_empty_entities` (line 116)
- `test_empty_observations_only` (line 119)
- `test_empty_entities_only` (line 122)
- `test_observation_with_none_parsed_is_ignored` (line 141)
- `test_observation_without_source_is_ignored` (line 155)
- `test_unknown_source_uses_reliability_c` (line 179)
- `test_min_score_zero_returns_all` (line 202)
- `test_min_score_one_filters_everything` (line 214)
- `test_max_hypotheses_caps_output` (line 233)
- `test_observations_must_be_sequence` (line 256)
- `test_entities_must_be_sequence` (line 260)
- `test_min_score_out_of_range_raises` (line 264)
- `test_max_hypotheses_too_small_raises` (line 270)
- `test_hostile_value_is_truncated_or_skipped` (line 292)
- `test_same_input_same_ids_and_scores` (line 312)
- `test_input_order_does_not_affect_output` (line 333)
- `test_hypothesis_dataclass_is_frozen` (line 354)
- `test_evidence_dataclass_is_frozen` (line 370)
- `test_entity_ref_is_frozen` (line 382)

#### `test_job_registry.py`
**Path:** `tests/test_job_registry.py`

**Functions:**
- `test_register_returns_value` (line 11)
- `test_size_cap_evicts_oldest` (line 17)
- `test_get_refreshes_lru_order` (line 28)
- `test_ttl_eviction` (line 39)
- `test_pop_removes_entry` (line 53)
- `test_keys_values_consistent` (line 61)
- `test_invalid_construction` (line 69)
- `test_replacement_does_not_evict` (line 76) - *Re-registering the same key keeps the size stable and LRU order intact.*

#### `test_pagination.py`
**Path:** `tests/test_pagination.py`

**Classs:**
- `TestPageStrategy` (line 21) - *PG1: page param increments with each page number.*
- `TestOffsetStrategy` (line 48) - *PG2: offset advances by page_size each page.*
- `TestCursorStrategy` (line 78) - *PG3: cursor extracted from response body.*
- `TestNoPagination` (line 128) - *PG4: default config means disabled.*
- `TestPartialPage` (line 151) - *PG5: fewer results than page_size signals last page.*
- `TestMaxPages` (line 180) - *PG6: max_pages limits total requests.*
- `TestFromDict` (line 205) - *PaginationConfig construction from raw dict.*

**Functions:**
- `test_first_page_is_one` (line 24)
- `test_second_page_increments` (line 29)
- `test_default_param_name` (line 34)
- `test_no_pagination_returns_empty` (line 39)
- `test_first_page_offset_zero` (line 51)
- `test_second_page_offset_25` (line 56)
- `test_third_page_offset_50` (line 61)
- `test_custom_param_names` (line 66)
- `test_extracts_cursor_from_simple_path` (line 81)
- `test_extracts_cursor_from_nested_path` (line 86)
- `test_missing_path_returns_none` (line 91)
- `test_empty_cursor_returns_none` (line 95)
- `test_null_cursor_returns_none` (line 99)
- `test_non_dict_response_returns_none` (line 103)
- `test_disabled_strategy_returns_none` (line 107)
- `test_build_params_empty_for_cursor` (line 111)
- `test_cursor_custom_param` (line 116)
- `test_default_config_disabled` (line 131)
- `test_empty_dict_disabled` (line 135)
- `test_none_disabled` (line 139)
- `test_enabled_when_strategy_set` (line 143)
- `test_partial_page_detected` (line 154)
- `test_full_page_not_detected_as_partial` (line 159)
- `test_list_response_counted_directly` (line 164)
- `test_using_custom_response_list_path` (line 168)
- `test_default_max_pages` (line 183)
- `test_custom_max_pages` (line 187)
- `test_zero_page_size_means_no_check` (line 193)
- `test_all_fields_mapped` (line 208)
- `test_partial_dict_uses_defaults` (line 230)
- `test_empty_string_strategy_disabled` (line 236)

#### `test_probabilistic_fusion.py`
**Path:** `tests/test_probabilistic_fusion.py`

**Classs:**
- `TestPrimarySourceRaisesLowConf` (line 48) - *PF1: tertiary first sighting → primary raises score.*
- `TestTertiaryCannotOverride` (line 77) - *PF2: untrusted_webscraper (F) cannot beat 0.9 existing.*
- `TestCorroborationLiftsScore` (line 110) - *PF3: multiple independent sources raise the score.*
- `TestMergeMonotonic` (line 142) - *PF4: a lower-confidence sighting never decreases the score.*
- `TestFirstSightingWeighted` (line 170) - *PF5: untrusted_webscraper first sighting is heavily discounted.*
- `TestRelationshipBayesian` (line 192) - *PF6: relationship from untrusted source cannot override primary.*
- `TestFusionStoreRegression` (line 217) - *Existing fusion store invariants must still hold.*

**Functions:**
- `_fs` (line 17)
- `_teardown` (line 23)
- `_entity` (line 30)
- `test_primary_source_raises_score` (line 51)
- `test_untrusted_source_cannot_override` (line 80)
- `test_two_sources_are_better_than_one` (line 113)
- `test_lower_confidence_never_decreases` (line 145)
- `test_untrusted_first_sighting_discounted` (line 173)
- `test_relationship_untrusted_cannot_override` (line 195)
- `test_entity_id_deterministic` (line 220)
- `test_entity_source_count_tracks` (line 229)
- `test_observation_count_advances` (line 243)
- `test_empty_type_returns_empty` (line 259)
- `test_empty_value_returns_empty` (line 267)
- `test_add_observation_and_stats` (line 275)
- `test_register_sources` (line 290)
- `test_search_entities` (line 305)
- `test_corroborated_properties` (line 320)
- `test_get_entity_nonexistent` (line 333)
- `test_open_store_closes_gracefully` (line 340)

#### `test_recon_fusion.py`
**Path:** `tests/test_recon_fusion.py`

**Classs:**
- `TestS1CriticalCorroborated` (line 46) - *S1 -- Happy path: corroborated by 5 sources -> CRITICAL.*
- `TestS2TwoReliableSources` (line 65) - *S2 -- 2 sources with A/B reliability -> CRITICAL (via 2+ src + high rel).*
- `TestS3SingleHighReliability` (line 82) - *S3 -- Single high-reliability source -> MEDIUM.*
- `TestS4SingleLowReliability` (line 102) - *S4 -- Single F-reliability source -> NOISE.*
- `TestS5EmptyInput` (line 117) - *S5 -- No observations or entities -> empty result.*
- `TestS6DirectMatchBoost` (line 130) - *S6 -- Direct match entity has boosted score.*
- `TestS7EmptyQuery` (line 147) - *S7 -- Empty query raises ValueError.*
- `TestS8BadConfig` (line 157) - *S8 -- Inconsistent thresholds raise ValueError.*
- `TestS9NoneObservations` (line 173) - *S9 -- None observations handled safely.*
- `TestS10EntityWithoutType` (line 183) - *S10 -- Entity without type is ignored.*
- `TestS11Dedup` (line 195) - *S11 -- Identical observations deduped to one.*
- `TestS12Ordering` (line 212) - *S12 -- Tiers ordered by relevance_score descending.*
- `TestIntegrationMultiEntity` (line 227) - *Integration: multiple entities classified across tiers.*
- `TestFusionResultDataclass` (line 252) - *FusionResult dataclass structural tests.*
- `TestRelevanceTierEnum` (line 267) - *RelevanceTier enum members and ordering.*

**Functions:**
- `_observation` (line 14)
- `_entity` (line 31)
- `test_critical_with_5_sources` (line 49)
- `test_two_reliable_sources_critical` (line 68)
- `test_single_a_source_is_medium` (line 85)
- `test_single_f_source_is_noise` (line 105)
- `test_empty_observations_and_entities` (line 120)
- `test_direct_match_boosts_score` (line 133)
- `test_empty_query_raises` (line 150)
- `test_bad_thresholds_raise` (line 160)
- `test_none_observations_safe` (line 176)
- `test_entity_without_type_ignored` (line 186)
- `test_identical_observations_deduped` (line 198)
- `test_tier_ordered_by_score` (line 215)
- `test_mixed_entities_across_tiers` (line 230)
- `test_fusion_result_serialisable` (line 255)
- `test_enum_members` (line 270)
- `test_enum_order_list` (line 277)

#### `test_reliability_scoring.py`
**Path:** `tests/test_reliability_scoring.py`

**Classs:**
- `TestHappyPathHighReliabilityCorroboratedFresh` (line 45) - *S1 del spec.*
- `TestUnknownSourceFallsBackToDefault` (line 109) - *S2 del spec.*
- `TestZeroCorroborationYieldsZeroScore` (line 169) - *S3 del spec: una sola fuente, no importa lo fiable que sea, score = 0.*
- `TestVeryOldObservationDecaysToZero` (line 188) - *S4 del spec.*
- `TestInvalidInputRaisesValueError` (line 225) - *S5 del spec.*
- `TestHostileSourceNameIsHandledSafely` (line 270) - *S6 del spec: input del operador, posiblemente adversario, no rompe.*
- `TestMergeReliableBeatsLessReliable` (line 299) - *S7 del spec.*
- `TestMergeUnreliableCannotRaise` (line 366) - *S8 del spec.*
- `TestDeterminism` (line 412) - *S9 del spec: misma entrada → misma salida, bit a bit.*
- `TestBoundedSmoke` (line 453) - *S10 del spec: smoke test del contrato de cota.*
- `TestSourceHierarchyPrimaryBeatsSecondaryBeatsTertiary` (line 483) - *S11 del spec: mismo reliability, distinto source_type.*
- `TestSourceHierarchyPrimaryCBeatsTertiaryA` (line 550) - *S12 del spec: source type compensates for lower reliability.*
- `TestSourceTypeFromName` (line 594) - *S13 del spec: lookup known and unknown source names.*
- `TestSourceHierarchyInMerge` (line 628) - *S14 del spec: merge with source type hierarchy.*
- `TestSourceTypeWeightsBounded` (line 662) - *S15 del spec: source_type_weight is always in {1.00, 0.85, 0.60}.*

**Functions:**
- `test_score_in_high_band` (line 48)
- `test_reliability_weight_is_one` (line 67)
- `test_freshness_weight_is_one_when_age_zero` (line 76)
- `test_corroboration_weight_matches_log10` (line 86)
- `test_credibility_weight_for_probably_true` (line 95)
- `test_unknown_source_returns_default` (line 120)
- `test_unknown_source_produces_weak_score_with_one_corroboration` (line 126)
- `test_unknown_source_with_many_corroborators_reaches_high_band` (line 146)
- `test_zero_corroboration_collapses_score` (line 172)
- `test_one_year_old_with_low_corroboration_decays` (line 191)
- `test_freshness_is_monotonically_decreasing` (line 204) - *Una observación más vieja siempre tiene freshness menor o igual.*
- `test_negative_corroboration_count_raises` (line 228)
- `test_negative_observation_age_raises` (line 235)
- `test_base_confidence_out_of_range_raises` (line 243)
- `test_half_life_zero_raises` (line 250)
- `test_half_life_negative_raises` (line 258)
- `test_hostile_name_does_not_raise` (line 288)
- `test_new_a_source_raises_score` (line 302)
- `test_merge_takes_max_of_existing_and_new` (line 319)
- `test_merge_keeps_existing_when_new_is_weaker` (line 335)
- `test_merge_result_is_always_bounded` (line 350)
- `test_f_source_against_strong_existing_keeps_existing` (line 369)
- `test_merge_existing_out_of_range_raises` (line 384)
- `test_merge_new_observation_out_of_range_raises` (line 396)
- `test_compute_confidence_is_pure` (line 415)
- `test_merge_confidence_is_pure` (line 428)
- `test_reliability_weights_match_nato_admiralty` (line 456)
- `test_credibility_weights_match_nato_admiralty` (line 465)
- `test_default_half_life_is_thirty_days` (line 473)
- `test_default_credibility_is_cannot_be_judged` (line 476)
- `test_primary_tertiary_score_order` (line 486)
- `test_primary_weight_is_one` (line 519)
- `test_secondary_weight_is_085` (line 528)
- `test_tertiary_weight_is_060` (line 537)
- `test_primary_c_beats_tertiary_a` (line 553)
- `test_primary_c_weight` (line 580)
- `test_rdap_is_primary` (line 597)
- `test_leakcheck_is_tertiary` (line 600)
- `test_wikidata_is_secondary` (line 603)
- `test_shodan_is_secondary` (line 606)
- `test_unknown_falls_back_to_default` (line 609)
- `test_none_falls_back` (line 612)
- `test_empty_falls_back` (line 615)
- `test_hostile_input_does_not_raise` (line 618)
- `test_new_primary_raises_score` (line 631)
- `test_new_tertiary_does_not_raise_weak_existing` (line 644)
- `test_source_type_weights_are_exact` (line 665)
- `test_primary_always_gives_one` (line 670)
- `test_tertiary_always_gives_060` (line 679)

#### `test_search_telemetry.py`
**Path:** `tests/test_search_telemetry.py`

**Functions:**
- `_render_index` (line 36) - *Render `index.html` exactly as the web layer does, telemetry included.*
- `test_s1_determinate_progress_midsearch` (line 52)
- `test_s2_indeterminate_progress` (line 67)
- `test_s3_completion_stops_spinner` (line 79)
- `test_s4_out_of_range_is_clamped` (line 90)
- `test_s5_unknown_phase_rejected` (line 103)
- `test_s6_catalog_is_brand_and_emoji_clean` (line 114)
- `test_s7_rendered_template_has_no_third_party_brand` (line 132)
- `test_s8_rendered_chrome_has_no_emoji` (line 141)
- `test_s9_brand_predicate_boundaries` (line 153)
- `_valid_kwargs` (line 163)
- `test_s10_empty_brand_rejected` (line 178)
- `test_s10_no_tips_rejected` (line 185)
- `test_s10_duplicate_phase_rejected` (line 192)
- `test_s10_emoji_in_catalog_rejected` (line 205)
- `test_s10_brand_collision_rejected` (line 212)
- `test_s10_missing_sentinel_phase_rejected` (line 219)
- `test_s11_template_renders_from_catalog` (line 233)
- `test_default_telemetry_is_a_shared_instance` (line 247)

#### `test_source_health_monitoring.py`
**Path:** `tests/test_source_health_monitoring.py`

**Classs:**
- `TestHealthySource` (line 29) - *H1: high success rate, low latency -> HEALTHY.*
- `TestDegradingLowSuccess` (line 97) - *H2: low success rate -> DEGRADING.*
- `TestDegradingHighLatency` (line 141) - *H3: high latency -> DEGRADING.*
- `TestStaleSource` (line 186) - *H4: long since last seen -> STALE.*
- `TestUnknownSource` (line 217) - *H5: fetch_count < min_fetches -> UNKNOWN.*
- `TestDashboard` (line 248) - *H6: dashboard filters by status.*
- `TestValidation` (line 348) - *H7: invalid inputs raise ValueError.*
- `TestDeterminism` (line 411) - *H8: same input -> same output.*
- `TestScoreBounded` (line 441) - *H9 smoke: health_score is always in [0, 1].*
- `TestStatusAlwaysValid` (line 472) - *H10: status is always a valid enum member.*
- `TestDataclassContract` (line 492) - *All public types are frozen dataclasses with to_dict.*

**Functions:**
- `test_healthy_status` (line 32)
- `test_success_rate_computed` (line 44)
- `test_avg_latency_computed` (line 56)
- `test_freshness_hours_computed` (line 68)
- `test_health_score_high_band` (line 80)
- `test_degrading_status` (line 100)
- `test_success_rate_reflects_failures` (line 112)
- `test_health_score_low_band` (line 124)
- `test_degrading_status_for_latency` (line 144)
- `test_avg_latency_high` (line 156)
- `test_health_score_penalised` (line 168)
- `test_stale_status` (line 189)
- `test_freshness_hours_exceeds_stale` (line 201)
- `test_unknown_status` (line 220)
- `test_zero_fetches_is_unknown` (line 232)
- `_healthy` (line 252)
- `_degrading` (line 263)
- `_stale` (line 274)
- `_unknown` (line 285)
- `test_hot_sources_are_healthy` (line 295)
- `test_degrading_includes_degrading_and_stale` (line 306)
- `test_unknown_sources_separate` (line 319)
- `test_summary_counts` (line 329)
- `test_ok_exceeds_fetch_raises` (line 351)
- `test_negative_fetch_raises` (line 362)
- `test_negative_latency_raises` (line 373)
- `test_empty_name_raises` (line 384)
- `test_config_min_fetches_less_than_one_raises` (line 395)
- `test_config_stale_hours_zero_raises` (line 399)
- `test_config_degrading_rate_out_of_range_raises` (line 403)
- `test_compute_health_is_pure` (line 414)
- `test_build_dashboard_is_pure` (line 428)
- `test_perfect_source_scores_one` (line 444)
- `test_broken_source_scores_low` (line 456)
- `test_status_is_enum` (line 475)
- `test_health_input_is_dataclass` (line 495)
- `test_health_result_is_dataclass` (line 498)
- `test_config_is_dataclass` (line 501)
- `test_dashboard_is_dataclass` (line 505)
- `test_result_to_dict` (line 508)
- `test_dashboard_to_dict` (line 523)

#### `test_target_management.py`
**Path:** `tests/test_target_management.py`

**Classs:**
- `TestS1HappyPath` (line 21)
- `TestS2AutoDetect` (line 46)
- `TestS3InvalidValue` (line 113)
- `TestS4UnknownType` (line 140)
- `TestS5EmptyValue` (line 156)
- `TestS6CaseStoreUnavailable` (line 174)
- `TestS7Batch` (line 186)
- `TestS8MaxBatch` (line 211)
- `TestS9XSS` (line 228)
- `TestS10Determinism` (line 246)
- `TestValidateType` (line 266)
- `TestValidateValue` (line 280)
- `TestMakeTargetId` (line 333)
- `TestAutoDetectType` (line 344)
- `TestBatchResultSerialization` (line 367)
- `TestTargetResultSerialization` (line 379)
- `TestCsvImport` (line 410)

**Functions:**
- `test_valid_target_returns_result` (line 22)
- `test_has_case_id` (line 30)
- `test_id_deterministic` (line 35)
- `test_ipv4_auto` (line 47)
- `test_ipv6_auto` (line 52)
- `test_email_auto` (line 57)
- `test_cve_auto` (line 62)
- `test_btc_auto` (line 67)
- `test_eth_auto` (line 72)
- `test_domain_auto` (line 77)
- `test_username_fallback` (line 82)
- `test_phone_auto` (line 87)
- `test_asn_auto` (line 92)
- `test_md5_auto` (line 97)
- `test_sha256_auto` (line 102)
- `test_invalid_email` (line 114)
- `test_invalid_ipv4` (line 119)
- `test_invalid_domain_script` (line 123)
- `test_invalid_url` (line 127)
- `test_invalid_phone` (line 131)
- `test_unknown_type` (line 141)
- `test_unknown_type_via_manager` (line 146)
- `test_empty_raises` (line 157)
- `test_whitespace_raises` (line 161)
- `test_validate_value_empty` (line 165)
- `test_ephemeral_no_case_store` (line 175)
- `test_mixed_batch` (line 187)
- `test_simple_lines_no_type` (line 201)
- `test_exceeds_max` (line 212)
- `test_at_max` (line 217)
- `test_script_in_domain_rejected` (line 229)
- `test_onclick_in_domain_rejected` (line 233)
- `test_sql_injection_in_email_rejected` (line 237)
- `test_same_id` (line 247)
- `test_same_id_normalised` (line 255)
- `test_valid_types_pass` (line 267)
- `test_auto_passes` (line 272)
- `test_invalid_fails` (line 275)
- `test_domain_valid` (line 281)
- `test_domain_invalid` (line 285)
- `test_ipv4_valid` (line 289)
- `test_ipv4_invalid_octet` (line 293)
- `test_email_valid` (line 297)
- `test_url_only_http_https` (line 301)
- `test_username_no_regex` (line 306)
- `test_cve_valid` (line 310)
- `test_btc_valid` (line 313)
- `test_eth_valid` (line 316)
- `test_phone_valid` (line 319)
- `test_asn_valid` (line 322)
- `test_md5_valid` (line 325)
- `test_sha256_valid` (line 328)
- `test_length` (line 334)
- `test_deterministic` (line 337)
- `test_case_sensitive_normalised` (line 340)
- `test_ipv4` (line 345)
- `test_ipv6` (line 348)
- `test_email` (line 351)
- `test_domain` (line 354)
- `test_url` (line 357)
- `test_cve` (line 360)
- `test_username_fallback` (line 363)
- `test_to_dict` (line 368)
- `test_to_dict` (line 380)
- `test_to_dict_invalid` (line 397)
- `test_basic_csv` (line 411)
- `test_csv_invalid` (line 418)
- `test_csv_max_batch` (line 425)
- `test_csv_exceeds_max` (line 431)

#### `test_ui_professional.py`
**Path:** `tests/test_ui_professional.py`

**Classs:**
- `TestS1LoadingAnimation` (line 64) - *S1 -- Loading indicator elements exist in the DOM.*
- `TestS2CriticalExpanded` (line 93) - *S2 -- CRITICAL tier renders expanded with correct badge count.*
- `TestS3NoiseCollapsed` (line 119)
- `TestS4ToggleExpandCollapse` (line 143)
- `TestS5FallbackFlatView` (line 157)
- `TestS6LoadingTimeout` (line 175)
- `TestS7HoverEffect` (line 184)
- `TestS8FadeInTransition` (line 197)
- `TestS9SecurityCSP` (line 211)
- `TestS10XSSSafe` (line 244)
- `TestIntegrationTierPipeline` (line 262)

**Functions:**
- `_render_index` (line 27)
- `_simulate_tiered_data` (line 39)
- `test_loading_elements_exist` (line 67)
- `test_loading_css_defined` (line 74)
- `test_js_show_working_indicator_exists` (line 83)
- `test_critical_tier_data` (line 96)
- `test_critical_css_classes_exist` (line 105)
- `test_noise_tier_data` (line 120)
- `test_noise_css_classes_exist` (line 127)
- `test_js_toggle_function_exists` (line 134)
- `test_aria_attributes_in_js` (line 144)
- `test_toggle_uses_role_button` (line 149)
- `test_js_fallback_logic` (line 158)
- `test_tiers_missing_returns_empty` (line 163)
- `test_show_toast_exists` (line 176)
- `test_tier_group_hover_css` (line 185)
- `test_transition_on_tier_group` (line 189)
- `test_fade_in_css_exists` (line 198)
- `test_results_use_fade_in` (line 203)
- `test_no_inline_style_in_tier_badge` (line 212)
- `test_no_inline_style_in_template` (line 222)
- `test_no_onclick_attributes` (line 233)
- `test_escape_html_function_exists` (line 245)
- `test_escape_html_properly_defined` (line 249)
- `test_tier_label_uses_text_content` (line 254)
- `test_tier_summary_accuracy` (line 263)
- `test_every_group_has_required_fields` (line 268)
- `test_scores_are_normalised` (line 280)

#### `split_sources.py`
**Path:** `tools/split_sources.py`

**Functions:**
- `main` (line 19)

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

**Functions:**
- `install_full` (line 51) - *3) Two install passes: full first, minimal fallback. We don't want a single Cython build error to leave the user with a half-installed project — be...*
- `install_minimal` (line 55)
