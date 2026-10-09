# Symbols (page 5 of 6)
Previous: [SYMBOLS_p4.md](SYMBOLS_p4.md)

| Symbol | Kind | File:Line | Signature |
|--------|------|-----------|-----------|
| `test_delete_removes_watch` | method | `tests/test_monitoring.py:145` | `def test_delete_removes_watch(self, tmp_store, sample_watch)` |
| `test_disable_does_not_delete` | method | `tests/test_monitoring.py:118` | `def test_disable_does_not_delete(self, tmp_store, sample_watch)` |
| `test_disabled_not_due` | method | `tests/test_monitoring.py:127` | `def test_disabled_not_due(self, tmp_store)` |
| `test_due_watches_returns_enabled` | method | `tests/test_monitoring.py:89` | `def test_due_watches_returns_enabled(self, tmp_store)` |
| `test_history_appears` | method | `tests/test_monitoring.py:173` | `def test_history_appears(self, tmp_store, sample_watch)` |
| `test_history_empty_for_new_watch` | method | `tests/test_monitoring.py:183` | `def test_history_empty_for_new_watch(self, tmp_store, sample_watch)` |
| `test_interval_honored` | method | `tests/test_monitoring.py:101` | `def test_interval_honored(self, tmp_store)` |
| `test_new_sources_loaded` | method | `tests/test_monitoring.py:327` | `def test_new_sources_loaded(self)` |
| `test_record_run_start` | method | `tests/test_monitoring.py:167` | `def test_record_run_start(self, tmp_store, sample_watch)` |
| `test_source_requires_key` | method | `tests/test_monitoring.py:235` | `def test_source_requires_key(self, source_name, key_env)` |
| `test_source_yaml_loads` | method | `tests/test_monitoring.py:220` | `def test_source_yaml_loads(self, source_name)` |
| `test_to_dict_roundtrip` | method | `tests/test_monitoring.py:295` | `def test_to_dict_roundtrip(self)` |
| `test_unknown_channel_returns_false` | method | `tests/test_monitoring.py:281` | `def test_unknown_channel_returns_false(self)` |
| `test_watch_appears_in_list` | method | `tests/test_monitoring.py:73` | `def test_watch_appears_in_list(self, tmp_store, sample_watch)` |
| `test_watch_next_run_in_future` | method | `tests/test_monitoring.py:69` | `def test_watch_next_run_in_future(self, sample_watch)` |
| `test_webhook_builds_correct_payload` | method | `tests/test_monitoring.py:197` | `def test_webhook_builds_correct_payload(self)` |
| `tmp_store` | function | `tests/test_monitoring.py:32` | `def tmp_store()` |
| `_store` | function | `tests/test_obs_fts.py:5` | `def _store(tmp_path, monkeypatch)` |
| `test_fts_empty_and_injection_safe` | function | `tests/test_obs_fts.py:33` | `def test_fts_empty_and_injection_safe(tmp_path, monkeypatch)` |
| `test_fts_finds_rare_word` | function | `tests/test_obs_fts.py:16` | `def test_fts_finds_rare_word(tmp_path, monkeypatch)` |
| `_Hostile` | class | `tests/test_observation_models.py:227` | `class _Hostile` |
| `_Hostile` | class | `tests/test_observation_models.py:238` | `class _Hostile` |
| `_WeirdName` | class | `tests/test_observation_models.py:249` | `class _WeirdName` |
| `_WeirdName` | class | `tests/test_observation_models.py:272` | `class _WeirdName` |
| `_full_meta` | function | `tests/test_observation_models.py:25` | `def _full_meta()` |
| `_full_obs` | function | `tests/test_observation_models.py:39` | `def _full_obs()` |
| `test_length_caps_are_positive` | function | `tests/test_observation_models.py:287` | `def test_length_caps_are_positive()` |
| `test_o1_full_observation_validates` | function | `tests/test_observation_models.py:57` | `def test_o1_full_observation_validates()` |
| `test_o2_error_observation_validates` | function | `tests/test_observation_models.py:72` | `def test_o2_error_observation_validates()` |
| `test_o3_missing_required_field_fails` | function | `tests/test_observation_models.py:85` | `def test_o3_missing_required_field_fails()` |
| `test_o4_unknown_meta_key_forbidden` | function | `tests/test_observation_models.py:96` | `def test_o4_unknown_meta_key_forbidden()` |
| `test_o5_wrong_typed_field_fails` | function | `tests/test_observation_models.py:106` | `def test_o5_wrong_typed_field_fails()` |
| `test_o6_error_message_does_not_embed_hostile_value` | function | `tests/test_observation_models.py:134` | `def test_o6_error_message_does_not_embed_hostile_value()` |
| `test_o6_oversized_url_truncated_not_failed` | function | `tests/test_observation_models.py:116` | `def test_o6_oversized_url_truncated_not_failed()` |
| `test_o6_oversized_value_rejected` | function | `tests/test_observation_models.py:124` | `def test_o6_oversized_value_rejected()` |
| `test_o7_confidence_at_bounds_accepted` | function | `tests/test_observation_models.py:152` | `def test_o7_confidence_at_bounds_accepted()` |
| `test_o7_confidence_out_of_range_rejected` | function | `tests/test_observation_models.py:146` | `def test_o7_confidence_out_of_range_rejected(confidence)` |
| `test_o8_run_result_aggregates` | function | `tests/test_observation_models.py:163` | `def test_o8_run_result_aggregates()` |
| `test_o8_run_result_with_error_surfaces_error` | function | `tests/test_observation_models.py:182` | `def test_o8_run_result_with_error_surfaces_error()` |
| `test_security_arbitrary_object_message_exact` | function | `tests/test_observation_models.py:270` | `def test_security_arbitrary_object_message_exact()` |
| `test_security_arbitrary_object_message_names_the_type` | function | `tests/test_observation_models.py:247` | `def test_security_arbitrary_object_message_names_the_type()` |
| `test_security_arbitrary_object_rejected` | function | `tests/test_observation_models.py:226` | `def test_security_arbitrary_object_rejected()` |
| `test_security_bytes_top_level_parsed_rejected` | function | `tests/test_observation_models.py:212` | `def test_security_bytes_top_level_parsed_rejected()` |
| `test_security_nested_object_inside_list_rejected` | function | `tests/test_observation_models.py:236` | `def test_security_nested_object_inside_list_rejected()` |
| `test_security_non_json_safe_attributes_rejected` | function | `tests/test_observation_models.py:205` | `def test_security_non_json_safe_attributes_rejected()` |
| `test_security_non_json_safe_value_rejected` | function | `tests/test_observation_models.py:198` | `def test_security_non_json_safe_value_rejected(field)` |
| `test_security_non_string_dict_key_rejected` | function | `tests/test_observation_models.py:219` | `def test_security_non_string_dict_key_rejected()` |
| `test_security_non_string_key_message_names_the_problem` | function | `tests/test_observation_models.py:260` | `def test_security_non_string_key_message_names_the_problem()` |
| `test_openapi_lists_healthz_without_auth_and_run_with_auth` | function | `tests/test_openapi.py:5` | `def test_openapi_lists_healthz_without_auth_and_run_with_auth()` |
| `test_healthz_no_auth_ok` | function | `tests/test_ops_observability.py:8` | `def test_healthz_no_auth_ok()` |
| `test_json_logs_opt_in_and_legacy` | function | `tests/test_ops_observability.py:61` | `def test_json_logs_opt_in_and_legacy()` |
| `test_metrics_counters_and_render` | function | `tests/test_ops_observability.py:26` | `def test_metrics_counters_and_render()` |
| `test_metrics_label_sanitised_no_newline` | function | `tests/test_ops_observability.py:44` | `def test_metrics_label_sanitised_no_newline()` |
| `test_metrics_thread_safe` | function | `tests/test_ops_observability.py:74` | `def test_metrics_thread_safe()` |
| `test_readyz_ready_and_not_ready` | function | `tests/test_ops_observability.py:17` | `def test_readyz_ready_and_not_ready()` |
| `TestBrokerTagging` | class | `tests/test_opsec_contact.py:53` | `class TestBrokerTagging` |
| `TestContactLevel` | class | `tests/test_opsec_contact.py:25` | `class TestContactLevel` |
| `TestRegistryContact` | class | `tests/test_opsec_contact.py:36` | `class TestRegistryContact` |
| `TestSelectorCeiling` | class | `tests/test_opsec_contact.py:61` | `class TestSelectorCeiling` |
| `_registry` | function | `tests/test_opsec_contact.py:19` | `def _registry()` |
| `test_all_sources_carry_known_class` | method | `tests/test_opsec_contact.py:40` | `def test_all_sources_carry_known_class(self)` |
| `test_default_is_passive` | method | `tests/test_opsec_contact.py:32` | `def test_default_is_passive(self)` |
| `test_hackertarget_probes_are_broker` | method | `tests/test_opsec_contact.py:54` | `def test_hackertarget_probes_are_broker(self)` |
| `test_ordering` | method | `tests/test_opsec_contact.py:26` | `def test_ordering(self)` |
| `test_passive_filter_excludes_broker_active` | method | `tests/test_opsec_contact.py:45` | `def test_passive_filter_excludes_broker_active(self)` |
| `test_selector_drops_broker_even_when_named` | method | `tests/test_opsec_contact.py:62` | `def test_selector_drops_broker_even_when_named(self)` |
| `test_selector_keeps_broker_without_ceiling` | method | `tests/test_opsec_contact.py:72` | `def test_selector_keeps_broker_without_ceiling(self)` |
| `test_sources_load` | method | `tests/test_opsec_contact.py:37` | `def test_sources_load(self)` |
| `test_unknown_is_active` | method | `tests/test_opsec_contact.py:29` | `def test_unknown_is_active(self)` |
| `_norm` | function | `tests/test_orchestrator_fanout.py:28` | `def _norm(items, sources)` |
| `_src` | function | `tests/test_orchestrator_fanout.py:10` | `def _src(name, binary)` |
| `go` | function | `tests/test_orchestrator_fanout.py:68` | `def go()` |
| `test_bad_shape_becomes_error_observation` | function | `tests/test_orchestrator_fanout.py:41` | `def test_bad_shape_becomes_error_observation()` |
| `test_exception_becomes_error_observation` | function | `tests/test_orchestrator_fanout.py:33` | `def test_exception_becomes_error_observation()` |
| `test_execute_source_forwards_on_done_to_system_app` | function | `tests/test_orchestrator_fanout.py:56` | `def test_execute_source_forwards_on_done_to_system_app()` |
| `test_mixed_http_and_system_app_keep_own_source` | function | `tests/test_orchestrator_fanout.py:47` | `def test_mixed_http_and_system_app_keep_own_source()` |
| `test_no_duplicated_method_defs` | function | `tests/test_orchestrator_fanout.py:19` | `def test_no_duplicated_method_defs()` |
| `test_system_app_failure_fires_on_done` | function | `tests/test_orchestrator_fanout.py:67` | `def test_system_app_failure_fires_on_done()` |
| `TestCursorStrategy` | class | `tests/test_pagination.py:78` | `class TestCursorStrategy` |
| `TestFromDict` | class | `tests/test_pagination.py:205` | `class TestFromDict` |
| `TestMaxPages` | class | `tests/test_pagination.py:180` | `class TestMaxPages` |
| `TestNoPagination` | class | `tests/test_pagination.py:128` | `class TestNoPagination` |
| `TestOffsetStrategy` | class | `tests/test_pagination.py:48` | `class TestOffsetStrategy` |
| `TestPageStrategy` | class | `tests/test_pagination.py:21` | `class TestPageStrategy` |
| `TestPartialPage` | class | `tests/test_pagination.py:151` | `class TestPartialPage` |
| `test_all_fields_mapped` | method | `tests/test_pagination.py:208` | `def test_all_fields_mapped(self)` |
| `test_build_params_empty_for_cursor` | method | `tests/test_pagination.py:111` | `def test_build_params_empty_for_cursor(self)` |
| `test_cursor_custom_param` | method | `tests/test_pagination.py:116` | `def test_cursor_custom_param(self)` |
| `test_custom_max_pages` | method | `tests/test_pagination.py:187` | `def test_custom_max_pages(self)` |
| `test_custom_param_names` | method | `tests/test_pagination.py:66` | `def test_custom_param_names(self)` |
| `test_default_config_disabled` | method | `tests/test_pagination.py:131` | `def test_default_config_disabled(self)` |
| `test_default_max_pages` | method | `tests/test_pagination.py:183` | `def test_default_max_pages(self)` |
| `test_default_param_name` | method | `tests/test_pagination.py:34` | `def test_default_param_name(self)` |
| `test_disabled_strategy_returns_none` | method | `tests/test_pagination.py:107` | `def test_disabled_strategy_returns_none(self)` |
| `test_empty_cursor_returns_none` | method | `tests/test_pagination.py:95` | `def test_empty_cursor_returns_none(self)` |
| `test_empty_dict_disabled` | method | `tests/test_pagination.py:135` | `def test_empty_dict_disabled(self)` |
| `test_empty_string_strategy_disabled` | method | `tests/test_pagination.py:236` | `def test_empty_string_strategy_disabled(self)` |
| `test_enabled_when_strategy_set` | method | `tests/test_pagination.py:143` | `def test_enabled_when_strategy_set(self)` |
| `test_extracts_cursor_from_nested_path` | method | `tests/test_pagination.py:86` | `def test_extracts_cursor_from_nested_path(self)` |
| `test_extracts_cursor_from_simple_path` | method | `tests/test_pagination.py:81` | `def test_extracts_cursor_from_simple_path(self)` |
| `test_first_page_is_one` | method | `tests/test_pagination.py:24` | `def test_first_page_is_one(self)` |
| `test_first_page_offset_zero` | method | `tests/test_pagination.py:51` | `def test_first_page_offset_zero(self)` |
| `test_full_page_not_detected_as_partial` | method | `tests/test_pagination.py:159` | `def test_full_page_not_detected_as_partial(self)` |
| `test_list_response_counted_directly` | method | `tests/test_pagination.py:164` | `def test_list_response_counted_directly(self)` |
| `test_missing_path_returns_none` | method | `tests/test_pagination.py:91` | `def test_missing_path_returns_none(self)` |
| `test_no_pagination_returns_empty` | method | `tests/test_pagination.py:39` | `def test_no_pagination_returns_empty(self)` |
| `test_non_dict_response_returns_none` | method | `tests/test_pagination.py:103` | `def test_non_dict_response_returns_none(self)` |
| `test_none_disabled` | method | `tests/test_pagination.py:139` | `def test_none_disabled(self)` |
| `test_null_cursor_returns_none` | method | `tests/test_pagination.py:99` | `def test_null_cursor_returns_none(self)` |
| `test_partial_dict_uses_defaults` | method | `tests/test_pagination.py:230` | `def test_partial_dict_uses_defaults(self)` |
| `test_partial_page_detected` | method | `tests/test_pagination.py:154` | `def test_partial_page_detected(self)` |
| `test_second_page_increments` | method | `tests/test_pagination.py:29` | `def test_second_page_increments(self)` |
| `test_second_page_offset_25` | method | `tests/test_pagination.py:56` | `def test_second_page_offset_25(self)` |
| `test_third_page_offset_50` | method | `tests/test_pagination.py:61` | `def test_third_page_offset_50(self)` |
| `test_using_custom_response_list_path` | method | `tests/test_pagination.py:168` | `def test_using_custom_response_list_path(self)` |
| `test_zero_page_size_means_no_check` | method | `tests/test_pagination.py:193` | `def test_zero_page_size_means_no_check(self)` |
| `TestP1Totality` | class | `tests/test_parsers.py:19` | `class TestP1Totality` |
| `TestP2NoRegression` | class | `tests/test_parsers.py:50` | `class TestP2NoRegression` |
| `test_ethplorer_valid` | method | `tests/test_parsers.py:72` | `def test_ethplorer_valid(self)` |
| `test_keybase_missing_them` | method | `tests/test_parsers.py:43` | `def test_keybase_missing_them(self)` |
| `test_keybase_valid` | method | `tests/test_parsers.py:58` | `def test_keybase_valid(self)` |
| `test_otx_null_entry_skipped` | method | `tests/test_parsers.py:39` | `def test_otx_null_entry_skipped(self)` |
| `test_otx_valid` | method | `tests/test_parsers.py:51` | `def test_otx_valid(self)` |
| `test_parser_is_total` | method | `tests/test_parsers.py:35` | `def test_parser_is_total(self, parser_name, payload)` |
| `test_wayback_non_list_header` | method | `tests/test_parsers.py:46` | `def test_wayback_non_list_header(self)` |
| `TestCtLogSubdomains` | class | `tests/test_pdns_monitor.py:18` | `class TestCtLogSubdomains` |
| `TestIPHistory` | class | `tests/test_pdns_monitor.py:32` | `class TestIPHistory` |
| `TestMonitorPollInterval` | class | `tests/test_pdns_monitor.py:111` | `class TestMonitorPollInterval` |
| `TestNewCertificates` | class | `tests/test_pdns_monitor.py:55` | `class TestNewCertificates` |
| `TestNoAxfr` | class | `tests/test_pdns_monitor.py:76` | `class TestNoAxfr` |
| `TestNoData` | class | `tests/test_pdns_monitor.py:47` | `class TestNoData` |
| `TestSubdomainStatusClassification` | class | `tests/test_pdns_monitor.py:102` | `class TestSubdomainStatusClassification` |
| `TestWildcardCert` | class | `tests/test_pdns_monitor.py:85` | `class TestWildcardCert` |
| `test_active_status_when_resolves` | method | `tests/test_pdns_monitor.py:103` | `def test_active_status_when_resolves(self)` |
| `test_empty_when_no_history` | method | `tests/test_pdns_monitor.py:48` | `def test_empty_when_no_history(self)` |
| `test_inactive_when_no_resolution` | method | `tests/test_pdns_monitor.py:106` | `def test_inactive_when_no_resolution(self)` |
| `test_minimum_poll_interval` | method | `tests/test_pdns_monitor.py:112` | `def test_minimum_poll_interval(self)` |
| `test_new_cert_with_san` | method | `tests/test_pdns_monitor.py:56` | `def test_new_cert_with_san(self)` |
| `test_no_zone_transfer_attempted` | method | `tests/test_pdns_monitor.py:77` | `def test_no_zone_transfer_attempted(self)` |
| `test_returns_subdomains_from_ct` | method | `tests/test_pdns_monitor.py:19` | `def test_returns_subdomains_from_ct(self)` |
| `test_tracks_ip_changes` | method | `tests/test_pdns_monitor.py:33` | `def test_tracks_ip_changes(self)` |
| `test_wildcard_cert_detected` | method | `tests/test_pdns_monitor.py:86` | `def test_wildcard_cert_detected(self)` |
| `TestBreachPasswordContext` | class | `tests/test_people_intel.py:57` | `class TestBreachPasswordContext` |
| `TestCrossBreachCorrelation` | class | `tests/test_people_intel.py:108` | `class TestCrossBreachCorrelation` |
| `TestEmailPatternInference` | class | `tests/test_people_intel.py:81` | `class TestEmailPatternInference` |
| `TestHappyPathEmployeeDiscovery` | class | `tests/test_people_intel.py:28` | `class TestHappyPathEmployeeDiscovery` |
| `TestInvalidDomain` | class | `tests/test_people_intel.py:50` | `class TestInvalidDomain` |
| `TestNoEmployees` | class | `tests/test_people_intel.py:42` | `class TestNoEmployees` |
| `TestNoRawPasswords` | class | `tests/test_people_intel.py:128` | `class TestNoRawPasswords` |
| `TestSingleEmailAmbiguous` | class | `tests/test_people_intel.py:101` | `class TestSingleEmailAmbiguous` |
| `_make_emp` | function | `tests/test_people_intel.py:18` | `def _make_emp(name, role, email)` |
| `test_breach_with_password_is_critical` | method | `tests/test_people_intel.py:58` | `def test_breach_with_password_is_critical(self)` |
| `test_empty_when_no_employees` | method | `tests/test_people_intel.py:43` | `def test_empty_when_no_employees(self)` |
| `test_infers_first_dot_last_pattern` | method | `tests/test_people_intel.py:82` | `def test_infers_first_dot_last_pattern(self)` |
| `test_infers_firstinitial_last_pattern` | method | `tests/test_people_intel.py:91` | `def test_infers_firstinitial_last_pattern(self)` |
| `test_multiple_breaches_increase_risk` | method | `tests/test_people_intel.py:109` | `def test_multiple_breaches_increase_risk(self)` |
| `test_passwords_not_in_serialised_output` | method | `tests/test_people_intel.py:129` | `def test_passwords_not_in_serialised_output(self)` |
| `test_rejects_invalid_domain` | method | `tests/test_people_intel.py:51` | `def test_rejects_invalid_domain(self)` |
| `test_returns_employees_from_domain` | method | `tests/test_people_intel.py:29` | `def test_returns_employees_from_domain(self)` |
| `test_single_email_low_confidence` | method | `tests/test_people_intel.py:102` | `def test_single_email_low_confidence(self)` |
| `TestCorroborationLiftsScore` | class | `tests/test_probabilistic_fusion.py:110` | `class TestCorroborationLiftsScore` |
| `TestFirstSightingWeighted` | class | `tests/test_probabilistic_fusion.py:170` | `class TestFirstSightingWeighted` |
| `TestFusionStoreRegression` | class | `tests/test_probabilistic_fusion.py:217` | `class TestFusionStoreRegression` |
| `TestMergeMonotonic` | class | `tests/test_probabilistic_fusion.py:142` | `class TestMergeMonotonic` |
| `TestPrimarySourceRaisesLowConf` | class | `tests/test_probabilistic_fusion.py:48` | `class TestPrimarySourceRaisesLowConf` |
| `TestRelationshipBayesian` | class | `tests/test_probabilistic_fusion.py:192` | `class TestRelationshipBayesian` |
| `TestTertiaryCannotOverride` | class | `tests/test_probabilistic_fusion.py:77` | `class TestTertiaryCannotOverride` |
| `_entity` | function | `tests/test_probabilistic_fusion.py:30` | `def _entity(etype, value, source, confidence)` |
| `_fs` | function | `tests/test_probabilistic_fusion.py:17` | `def _fs()` |
| `_teardown` | function | `tests/test_probabilistic_fusion.py:23` | `def _teardown(store, tmp)` |
| `test_add_observation_and_stats` | method | `tests/test_probabilistic_fusion.py:275` | `def test_add_observation_and_stats(self)` |
| `test_corroborated_properties` | method | `tests/test_probabilistic_fusion.py:320` | `def test_corroborated_properties(self)` |
| `test_empty_type_returns_empty` | method | `tests/test_probabilistic_fusion.py:259` | `def test_empty_type_returns_empty(self)` |
| `test_empty_value_returns_empty` | method | `tests/test_probabilistic_fusion.py:267` | `def test_empty_value_returns_empty(self)` |
| `test_entity_id_deterministic` | method | `tests/test_probabilistic_fusion.py:220` | `def test_entity_id_deterministic(self)` |
| `test_entity_source_count_tracks` | method | `tests/test_probabilistic_fusion.py:229` | `def test_entity_source_count_tracks(self)` |
| `test_get_entity_nonexistent` | method | `tests/test_probabilistic_fusion.py:333` | `def test_get_entity_nonexistent(self)` |
| `test_lower_confidence_never_decreases` | method | `tests/test_probabilistic_fusion.py:145` | `def test_lower_confidence_never_decreases(self)` |
| `test_observation_count_advances` | method | `tests/test_probabilistic_fusion.py:243` | `def test_observation_count_advances(self)` |
| `test_open_store_closes_gracefully` | method | `tests/test_probabilistic_fusion.py:340` | `def test_open_store_closes_gracefully(self)` |
| `test_primary_source_raises_score` | method | `tests/test_probabilistic_fusion.py:51` | `def test_primary_source_raises_score(self)` |
| `test_register_sources` | method | `tests/test_probabilistic_fusion.py:290` | `def test_register_sources(self)` |
| `test_relationship_untrusted_cannot_override` | method | `tests/test_probabilistic_fusion.py:195` | `def test_relationship_untrusted_cannot_override(self)` |
| `test_search_entities` | method | `tests/test_probabilistic_fusion.py:305` | `def test_search_entities(self)` |
| `test_two_sources_are_better_than_one` | method | `tests/test_probabilistic_fusion.py:113` | `def test_two_sources_are_better_than_one(self)` |
| `test_untrusted_first_sighting_discounted` | method | `tests/test_probabilistic_fusion.py:173` | `def test_untrusted_first_sighting_discounted(self)` |
| `test_untrusted_source_cannot_override` | method | `tests/test_probabilistic_fusion.py:80` | `def test_untrusted_source_cannot_override(self)` |
| `test_at_handle` | function | `tests/test_query_intent.py:17` | `def test_at_handle()` |
| `test_backward_compat` | function | `tests/test_query_intent.py:31` | `def test_backward_compat()` |
| `test_btc_uppercase_bech32` | function | `tests/test_query_intent.py:27` | `def test_btc_uppercase_bech32()` |
| `test_mac` | function | `tests/test_query_intent.py:12` | `def test_mac()` |
| `test_phone` | function | `tests/test_query_intent.py:7` | `def test_phone()` |
| `test_url_normalises_to_host` | function | `tests/test_query_intent.py:22` | `def test_url_normalises_to_host()` |
| `TestFusionResultDataclass` | class | `tests/test_recon_fusion.py:252` | `class TestFusionResultDataclass` |
| `TestIntegrationMultiEntity` | class | `tests/test_recon_fusion.py:227` | `class TestIntegrationMultiEntity` |
| `TestRelevanceTierEnum` | class | `tests/test_recon_fusion.py:267` | `class TestRelevanceTierEnum` |
| `TestS10EntityWithoutType` | class | `tests/test_recon_fusion.py:183` | `class TestS10EntityWithoutType` |
| `TestS11Dedup` | class | `tests/test_recon_fusion.py:195` | `class TestS11Dedup` |
| `TestS12Ordering` | class | `tests/test_recon_fusion.py:212` | `class TestS12Ordering` |
| `TestS1CriticalCorroborated` | class | `tests/test_recon_fusion.py:46` | `class TestS1CriticalCorroborated` |
| `TestS2TwoReliableSources` | class | `tests/test_recon_fusion.py:65` | `class TestS2TwoReliableSources` |
| `TestS3SingleHighReliability` | class | `tests/test_recon_fusion.py:82` | `class TestS3SingleHighReliability` |
| `TestS4SingleLowReliability` | class | `tests/test_recon_fusion.py:102` | `class TestS4SingleLowReliability` |
| `TestS5EmptyInput` | class | `tests/test_recon_fusion.py:117` | `class TestS5EmptyInput` |
| `TestS6DirectMatchBoost` | class | `tests/test_recon_fusion.py:130` | `class TestS6DirectMatchBoost` |
| `TestS7EmptyQuery` | class | `tests/test_recon_fusion.py:147` | `class TestS7EmptyQuery` |
| `TestS8BadConfig` | class | `tests/test_recon_fusion.py:157` | `class TestS8BadConfig` |
| `TestS9NoneObservations` | class | `tests/test_recon_fusion.py:173` | `class TestS9NoneObservations` |
| `_entity` | function | `tests/test_recon_fusion.py:31` | `def _entity(etype, value, confidence, sources)` |
| `_observation` | function | `tests/test_recon_fusion.py:14` | `def _observation(source, category, parser, status, parsed)` |
| `test_bad_thresholds_raise` | method | `tests/test_recon_fusion.py:160` | `def test_bad_thresholds_raise(self)` |
| `test_critical_with_5_sources` | method | `tests/test_recon_fusion.py:49` | `def test_critical_with_5_sources(self)` |
| `test_direct_match_boosts_score` | method | `tests/test_recon_fusion.py:133` | `def test_direct_match_boosts_score(self)` |
| `test_empty_observations_and_entities` | method | `tests/test_recon_fusion.py:120` | `def test_empty_observations_and_entities(self)` |
| `test_empty_query_raises` | method | `tests/test_recon_fusion.py:150` | `def test_empty_query_raises(self)` |
| `test_entity_without_type_ignored` | method | `tests/test_recon_fusion.py:186` | `def test_entity_without_type_ignored(self)` |
| `test_enum_members` | method | `tests/test_recon_fusion.py:270` | `def test_enum_members(self)` |
| `test_enum_order_list` | method | `tests/test_recon_fusion.py:277` | `def test_enum_order_list(self)` |
| `test_fusion_result_serialisable` | method | `tests/test_recon_fusion.py:255` | `def test_fusion_result_serialisable(self)` |
| `test_identical_observations_deduped` | method | `tests/test_recon_fusion.py:198` | `def test_identical_observations_deduped(self)` |
| `test_mixed_entities_across_tiers` | method | `tests/test_recon_fusion.py:230` | `def test_mixed_entities_across_tiers(self)` |
| `test_none_observations_safe` | method | `tests/test_recon_fusion.py:176` | `def test_none_observations_safe(self)` |
| `test_single_a_source_is_medium` | method | `tests/test_recon_fusion.py:85` | `def test_single_a_source_is_medium(self)` |
| `test_single_f_source_is_noise` | method | `tests/test_recon_fusion.py:105` | `def test_single_f_source_is_noise(self)` |
| `test_tier_ordered_by_score` | method | `tests/test_recon_fusion.py:215` | `def test_tier_ordered_by_score(self)` |
| `test_two_reliable_sources_critical` | method | `tests/test_recon_fusion.py:68` | `def test_two_reliable_sources_critical(self)` |
| `TestCredentialsRedacted` | class | `tests/test_recon_report.py:106` | `class TestCredentialsRedacted` |
| `TestExecutiveSummaryFindings` | class | `tests/test_recon_report.py:42` | `class TestExecutiveSummaryFindings` |
| `TestFullReport` | class | `tests/test_recon_report.py:28` | `class TestFullReport` |
| `TestMinimalReport` | class | `tests/test_recon_report.py:57` | `class TestMinimalReport` |
| `TestRecommendationsOrdered` | class | `tests/test_recon_report.py:98` | `class TestRecommendationsOrdered` |
| `TestSingleFindingReport` | class | `tests/test_recon_report.py:133` | `class TestSingleFindingReport` |
| `TestSubdomainTree` | class | `tests/test_recon_report.py:119` | `class TestSubdomainTree` |
| `TestTlpClassification` | class | `tests/test_recon_report.py:72` | `class TestTlpClassification` |
| `_make_meta` | function | `tests/test_recon_report.py:18` | `def _make_meta()` |
| `test_ascii_tree_generated` | method | `tests/test_recon_report.py:120` | `def test_ascii_tree_generated(self)` |
| `test_aws_key_redacted` | method | `tests/test_recon_report.py:107` | `def test_aws_key_redacted(self)` |
| `test_classification_propagates_to_exec_summary` | method | `tests/test_recon_report.py:81` | `def test_classification_propagates_to_exec_summary(self)` |
| `test_contains_all_sections` | method | `tests/test_recon_report.py:29` | `def test_contains_all_sections(self)` |
| `test_critical_first` | method | `tests/test_recon_report.py:99` | `def test_critical_first(self)` |
| `test_mentions_critical_findings` | method | `tests/test_recon_report.py:43` | `def test_mentions_critical_findings(self)` |
| `test_minimal_report_with_no_findings` | method | `tests/test_recon_report.py:58` | `def test_minimal_report_with_no_findings(self)` |
| `test_password_redacted` | method | `tests/test_recon_report.py:112` | `def test_password_redacted(self)` |
| `test_single_finding_prominent` | method | `tests/test_recon_report.py:134` | `def test_single_finding_prominent(self)` |
| `test_tlp_amber_in_header` | method | `tests/test_recon_report.py:73` | `def test_tlp_amber_in_header(self)` |
| `TestBoundedSmoke` | class | `tests/test_reliability_scoring.py:455` | `class TestBoundedSmoke` |
| `TestDeterminism` | class | `tests/test_reliability_scoring.py:414` | `class TestDeterminism` |
| `TestHappyPathHighReliabilityCorroboratedFresh` | class | `tests/test_reliability_scoring.py:47` | `class TestHappyPathHighReliabilityCorroboratedFresh` |
| `TestHostileSourceNameIsHandledSafely` | class | `tests/test_reliability_scoring.py:272` | `class TestHostileSourceNameIsHandledSafely` |
| `TestInvalidInputRaisesValueError` | class | `tests/test_reliability_scoring.py:227` | `class TestInvalidInputRaisesValueError` |
| `TestMergeReliableBeatsLessReliable` | class | `tests/test_reliability_scoring.py:301` | `class TestMergeReliableBeatsLessReliable` |
| `TestMergeUnreliableCannotRaise` | class | `tests/test_reliability_scoring.py:368` | `class TestMergeUnreliableCannotRaise` |
| `TestReliabilityWeightHelpers` | class | `tests/test_reliability_scoring.py:694` | `class TestReliabilityWeightHelpers` |
| `TestSourceHierarchyInMerge` | class | `tests/test_reliability_scoring.py:630` | `class TestSourceHierarchyInMerge` |
| `TestSourceHierarchyPrimaryBeatsSecondaryBeatsTertiary` | class | `tests/test_reliability_scoring.py:485` | `class TestSourceHierarchyPrimaryBeatsSecondaryBeatsTertiary` |
| `TestSourceHierarchyPrimaryCBeatsTertiaryA` | class | `tests/test_reliability_scoring.py:552` | `class TestSourceHierarchyPrimaryCBeatsTertiaryA` |
| `TestSourceTypeFromName` | class | `tests/test_reliability_scoring.py:596` | `class TestSourceTypeFromName` |
| `TestSourceTypeWeightsBounded` | class | `tests/test_reliability_scoring.py:664` | `class TestSourceTypeWeightsBounded` |
| `TestUnknownSourceFallsBackToDefault` | class | `tests/test_reliability_scoring.py:111` | `class TestUnknownSourceFallsBackToDefault` |
| `TestVeryOldObservationDecaysToZero` | class | `tests/test_reliability_scoring.py:190` | `class TestVeryOldObservationDecaysToZero` |
| `TestZeroCorroborationYieldsZeroScore` | class | `tests/test_reliability_scoring.py:171` | `class TestZeroCorroborationYieldsZeroScore` |
| `test_base_confidence_out_of_range_raises` | method | `tests/test_reliability_scoring.py:245` | `def test_base_confidence_out_of_range_raises(self, bad)` |
| `test_compute_confidence_is_pure` | method | `tests/test_reliability_scoring.py:417` | `def test_compute_confidence_is_pure(self)` |
| `test_corroboration_weight_matches_log10` | method | `tests/test_reliability_scoring.py:88` | `def test_corroboration_weight_matches_log10(self)` |
| `test_credibility_weight_for_probably_true` | method | `tests/test_reliability_scoring.py:97` | `def test_credibility_weight_for_probably_true(self)` |
| `test_credibility_weights_match_nato_admiralty` | method | `tests/test_reliability_scoring.py:467` | `def test_credibility_weights_match_nato_admiralty(self)` |
| `test_default_credibility_is_cannot_be_judged` | method | `tests/test_reliability_scoring.py:478` | `def test_default_credibility_is_cannot_be_judged(self)` |
| `test_default_half_life_is_thirty_days` | method | `tests/test_reliability_scoring.py:475` | `def test_default_half_life_is_thirty_days(self)` |
| `test_empty_falls_back` | method | `tests/test_reliability_scoring.py:617` | `def test_empty_falls_back(self)` |
| `test_f_source_against_strong_existing_keeps_existing` | method | `tests/test_reliability_scoring.py:371` | `def test_f_source_against_strong_existing_keeps_existing(self)` |
| `test_freshness_is_monotonically_decreasing` | method | `tests/test_reliability_scoring.py:206` | `def test_freshness_is_monotonically_decreasing(self)` |
| `test_freshness_weight_is_one_when_age_zero` | method | `tests/test_reliability_scoring.py:78` | `def test_freshness_weight_is_one_when_age_zero(self)` |
| `test_half_life_negative_raises` | method | `tests/test_reliability_scoring.py:260` | `def test_half_life_negative_raises(self)` |
| `test_half_life_zero_raises` | method | `tests/test_reliability_scoring.py:252` | `def test_half_life_zero_raises(self)` |
| `test_hostile_input_does_not_raise` | method | `tests/test_reliability_scoring.py:620` | `def test_hostile_input_does_not_raise(self)` |
| `test_hostile_name_does_not_raise` | method | `tests/test_reliability_scoring.py:290` | `def test_hostile_name_does_not_raise(self, hostile)` |
| `test_invalid_override_falls_back` | method | `tests/test_reliability_scoring.py:711` | `def test_invalid_override_falls_back(self)` |
| `test_known_source_letter` | method | `tests/test_reliability_scoring.py:698` | `def test_known_source_letter(self)` |
| `test_leakcheck_is_tertiary` | method | `tests/test_reliability_scoring.py:602` | `def test_leakcheck_is_tertiary(self)` |
| `test_letter_helper` | method | `tests/test_reliability_scoring.py:716` | `def test_letter_helper(self)` |
| `test_merge_confidence_is_pure` | method | `tests/test_reliability_scoring.py:430` | `def test_merge_confidence_is_pure(self)` |
| `test_merge_existing_out_of_range_raises` | method | `tests/test_reliability_scoring.py:386` | `def test_merge_existing_out_of_range_raises(self)` |
| `test_merge_keeps_existing_when_new_is_weaker` | method | `tests/test_reliability_scoring.py:337` | `def test_merge_keeps_existing_when_new_is_weaker(self)` |
| `test_merge_new_observation_out_of_range_raises` | method | `tests/test_reliability_scoring.py:398` | `def test_merge_new_observation_out_of_range_raises(self)` |
| `test_merge_result_is_always_bounded` | method | `tests/test_reliability_scoring.py:352` | `def test_merge_result_is_always_bounded(self)` |
| `test_merge_takes_max_of_existing_and_new` | method | `tests/test_reliability_scoring.py:321` | `def test_merge_takes_max_of_existing_and_new(self)` |
| `test_negative_corroboration_count_raises` | method | `tests/test_reliability_scoring.py:230` | `def test_negative_corroboration_count_raises(self)` |
| `test_negative_observation_age_raises` | method | `tests/test_reliability_scoring.py:237` | `def test_negative_observation_age_raises(self)` |
| `test_new_a_source_raises_score` | method | `tests/test_reliability_scoring.py:304` | `def test_new_a_source_raises_score(self)` |
| `test_new_primary_raises_score` | method | `tests/test_reliability_scoring.py:633` | `def test_new_primary_raises_score(self)` |
| `test_new_tertiary_does_not_raise_weak_existing` | method | `tests/test_reliability_scoring.py:646` | `def test_new_tertiary_does_not_raise_weak_existing(self)` |
| `test_none_falls_back` | method | `tests/test_reliability_scoring.py:614` | `def test_none_falls_back(self)` |
| `test_one_year_old_with_low_corroboration_decays` | method | `tests/test_reliability_scoring.py:193` | `def test_one_year_old_with_low_corroboration_decays(self)` |
| `test_override_wins` | method | `tests/test_reliability_scoring.py:708` | `def test_override_wins(self)` |
| `test_primary_always_gives_one` | method | `tests/test_reliability_scoring.py:672` | `def test_primary_always_gives_one(self)` |
| `test_primary_c_beats_tertiary_a` | method | `tests/test_reliability_scoring.py:555` | `def test_primary_c_beats_tertiary_a(self)` |
| `test_primary_c_weight` | method | `tests/test_reliability_scoring.py:582` | `def test_primary_c_weight(self)` |
| `test_primary_tertiary_score_order` | method | `tests/test_reliability_scoring.py:488` | `def test_primary_tertiary_score_order(self)` |
| `test_primary_weight_is_one` | method | `tests/test_reliability_scoring.py:521` | `def test_primary_weight_is_one(self)` |
| `test_rdap_is_primary` | method | `tests/test_reliability_scoring.py:599` | `def test_rdap_is_primary(self)` |
| `test_reliability_weight_is_one` | method | `tests/test_reliability_scoring.py:69` | `def test_reliability_weight_is_one(self)` |
| `test_reliability_weights_match_nato_admiralty` | method | `tests/test_reliability_scoring.py:458` | `def test_reliability_weights_match_nato_admiralty(self)` |
| `test_score_in_high_band` | method | `tests/test_reliability_scoring.py:50` | `def test_score_in_high_band(self)` |
| `test_secondary_weight_is_085` | method | `tests/test_reliability_scoring.py:530` | `def test_secondary_weight_is_085(self)` |
| `test_shodan_is_secondary` | method | `tests/test_reliability_scoring.py:608` | `def test_shodan_is_secondary(self)` |
| `test_source_type_weights_are_exact` | method | `tests/test_reliability_scoring.py:667` | `def test_source_type_weights_are_exact(self)` |
| `test_tertiary_always_gives_060` | method | `tests/test_reliability_scoring.py:681` | `def test_tertiary_always_gives_060(self)` |
| `test_tertiary_weight_is_060` | method | `tests/test_reliability_scoring.py:539` | `def test_tertiary_weight_is_060(self)` |
| `test_unknown_falls_back_to_default` | method | `tests/test_reliability_scoring.py:611` | `def test_unknown_falls_back_to_default(self)` |
| `test_unknown_source_falls_back_to_default` | method | `tests/test_reliability_scoring.py:703` | `def test_unknown_source_falls_back_to_default(self)` |
| `test_unknown_source_produces_weak_score_with_one_corroboration` | method | `tests/test_reliability_scoring.py:128` | `def test_unknown_source_produces_weak_score_with_one_corroboration(self)` |
| `test_unknown_source_returns_default` | method | `tests/test_reliability_scoring.py:122` | `def test_unknown_source_returns_default(self, name)` |
| `test_unknown_source_with_many_corroborators_reaches_high_band` | method | `tests/test_reliability_scoring.py:148` | `def test_unknown_source_with_many_corroborators_reaches_high_band(self)` |
| `test_wikidata_is_secondary` | method | `tests/test_reliability_scoring.py:605` | `def test_wikidata_is_secondary(self)` |
| `test_zero_corroboration_collapses_score` | method | `tests/test_reliability_scoring.py:174` | `def test_zero_corroboration_collapses_score(self)` |
| `test_client_defaults_to_central_policy` | function | `tests/test_retry_policy.py:14` | `def test_client_defaults_to_central_policy()` |
| `test_delays_geometric_and_capped` | function | `tests/test_retry_policy.py:5` | `def test_delays_geometric_and_capped()` |
| `TestBuildReport` | class | `tests/test_scope.py:79` | `class TestBuildReport` |
| `TestClassify` | class | `tests/test_scope.py:48` | `class TestClassify` |
| `TestNormaliseAsset` | class | `tests/test_scope.py:32` | `class TestNormaliseAsset` |
| `TestParseRules` | class | `tests/test_scope.py:43` | `class TestParseRules` |
| `test_cidr_and_single_ip` | method | `tests/test_scope.py:59` | `def test_cidr_and_single_ip(self)` |
| `test_dedup_hosts_ips_and_buckets` | method | `tests/test_scope.py:80` | `def test_dedup_hosts_ips_and_buckets(self)` |
| `test_empty_asset_unknown` | method | `tests/test_scope.py:74` | `def test_empty_asset_unknown(self)` |
| `test_foreign_host_unknown` | method | `tests/test_scope.py:70` | `def test_foreign_host_unknown(self)` |
| `test_ipv6_brackets_stripped` | method | `tests/test_scope.py:39` | `def test_ipv6_brackets_stripped(self)` |
| `test_out_of_scope_precedence` | method | `tests/test_scope.py:65` | `def test_out_of_scope_precedence(self)` |
| `test_regex_rule` | method | `tests/test_scope.py:54` | `def test_regex_rule(self)` |
| `test_skips_blanks_and_comments` | method | `tests/test_scope.py:44` | `def test_skips_blanks_and_comments(self)` |
| `test_strip_scheme_path_port` | method | `tests/test_scope.py:33` | `def test_strip_scheme_path_port(self)` |
| `test_strip_trailing_dot` | method | `tests/test_scope.py:36` | `def test_strip_trailing_dot(self)` |
| `test_wildcard_matches_subdomain_and_apex` | method | `tests/test_scope.py:49` | `def test_wildcard_matches_subdomain_and_apex(self)` |
| `_render_index` | function | `tests/test_search_telemetry.py:36` | `def _render_index()` |
| `_valid_kwargs` | function | `tests/test_search_telemetry.py:163` | `def _valid_kwargs()` |
| `test_default_telemetry_is_a_shared_instance` | function | `tests/test_search_telemetry.py:247` | `def test_default_telemetry_is_a_shared_instance()` |
| `test_s10_brand_collision_rejected` | function | `tests/test_search_telemetry.py:212` | `def test_s10_brand_collision_rejected()` |
| `test_s10_duplicate_phase_rejected` | function | `tests/test_search_telemetry.py:192` | `def test_s10_duplicate_phase_rejected()` |
| `test_s10_emoji_in_catalog_rejected` | function | `tests/test_search_telemetry.py:205` | `def test_s10_emoji_in_catalog_rejected()` |
| `test_s10_empty_brand_rejected` | function | `tests/test_search_telemetry.py:178` | `def test_s10_empty_brand_rejected()` |
| `test_s10_missing_sentinel_phase_rejected` | function | `tests/test_search_telemetry.py:219` | `def test_s10_missing_sentinel_phase_rejected()` |
| `test_s10_no_tips_rejected` | function | `tests/test_search_telemetry.py:185` | `def test_s10_no_tips_rejected()` |
| `test_s11_template_renders_from_catalog` | function | `tests/test_search_telemetry.py:233` | `def test_s11_template_renders_from_catalog()` |
| `test_s1_determinate_progress_midsearch` | function | `tests/test_search_telemetry.py:52` | `def test_s1_determinate_progress_midsearch()` |
| `test_s2_indeterminate_progress` | function | `tests/test_search_telemetry.py:67` | `def test_s2_indeterminate_progress()` |
| `test_s3_completion_stops_spinner` | function | `tests/test_search_telemetry.py:79` | `def test_s3_completion_stops_spinner()` |
| `test_s4_out_of_range_is_clamped` | function | `tests/test_search_telemetry.py:90` | `def test_s4_out_of_range_is_clamped()` |
| `test_s5_unknown_phase_rejected` | function | `tests/test_search_telemetry.py:103` | `def test_s5_unknown_phase_rejected()` |
| `test_s6_catalog_is_brand_and_emoji_clean` | function | `tests/test_search_telemetry.py:114` | `def test_s6_catalog_is_brand_and_emoji_clean()` |
| `test_s7_rendered_template_has_no_third_party_brand` | function | `tests/test_search_telemetry.py:132` | `def test_s7_rendered_template_has_no_third_party_brand()` |
| `test_s8_rendered_chrome_has_no_emoji` | function | `tests/test_search_telemetry.py:141` | `def test_s8_rendered_chrome_has_no_emoji()` |
| `test_s9_brand_predicate_boundaries` | function | `tests/test_search_telemetry.py:153` | `def test_s9_brand_predicate_boundaries()` |
| `TestAlerterNoRedirect` | class | `tests/test_security_remediation.py:538` | `class TestAlerterNoRedirect` |
| `TestAlerterSsrf` | class | `tests/test_security_remediation.py:498` | `class TestAlerterSsrf` |
| `TestCiWorkflowPermissions` | class | `tests/test_security_remediation.py:306` | `class TestCiWorkflowPermissions` |
| `TestHttpsRedirectSafety` | class | `tests/test_security_remediation.py:260` | `class TestHttpsRedirectSafety` |
| `TestInfoExposureEncryption` | class | `tests/test_security_remediation.py:75` | `class TestInfoExposureEncryption` |
| `TestInfoExposureSourceOps` | class | `tests/test_security_remediation.py:176` | `class TestInfoExposureSourceOps` |
| `TestJavaScriptDomSafety` | class | `tests/test_security_remediation.py:431` | `class TestJavaScriptDomSafety` |
| `TestOsirisExceptionSafety` | class | `tests/test_security_remediation.py:336` | `class TestOsirisExceptionSafety` |
| `TestSsrfLogSanitisation` | class | `tests/test_security_remediation.py:25` | `class TestSsrfLogSanitisation` |
| `TestTooltipSinkHardening` | class | `tests/test_security_remediation.py:592` | `class TestTooltipSinkHardening` |
| `TestWebSecurityRedirect` | class | `tests/test_security_remediation.py:399` | `class TestWebSecurityRedirect` |
| `_Fake302` | class | `tests/test_security_remediation.py:555` | `class _Fake302` |
| `_FakeOpener` | class | `tests/test_security_remediation.py:564` | `class _FakeOpener` |
| `__enter__` | method | `tests/test_security_remediation.py:558` | `def __enter__(self)` |
| `__exit__` | method | `tests/test_security_remediation.py:561` | `def __exit__(self)` |
| `_fake_build_opener` | method | `tests/test_security_remediation.py:571` | `def _fake_build_opener()` |
| `_make_export_route` | method | `tests/test_security_remediation.py:86` | `def _make_export_route(self, app, raise_val, error_msg, status)` |
| `_make_export_route_fixed` | method | `tests/test_security_remediation.py:118` | `def _make_export_route_fixed(self, app, raise_val, error_msg, status)` |
| `_make_osiris_route_fixed` | method | `tests/test_security_remediation.py:347` | `def _make_osiris_route_fixed(self, app, route_path)` |
| `api_create` | method | `tests/test_security_remediation.py:212` | `def api_create()` |
| `api_delete` | method | `tests/test_security_remediation.py:191` | `def api_delete(name)` |
| `api_export_fixed` | method | `tests/test_security_remediation.py:130` | `def api_export_fixed()` |
| `api_export_test` | method | `tests/test_security_remediation.py:97` | `def api_export_test()` |
| `api_update` | method | `tests/test_security_remediation.py:236` | `def api_update(name)` |
| `app` | method | `tests/test_security_remediation.py:79` | `def app(self)` |
| `app` | method | `tests/test_security_remediation.py:180` | `def app(self)` |
| `app` | method | `tests/test_security_remediation.py:264` | `def app(self)` |
| `app` | method | `tests/test_security_remediation.py:340` | `def app(self)` |
| `fetch_bgp` | method | `tests/test_security_remediation.py:354` | `def fetch_bgp(q)` |
| `fetch_github_user` | method | `tests/test_security_remediation.py:363` | `def fetch_github_user(u)` |
| `fetch_leaks` | method | `tests/test_security_remediation.py:366` | `def fetch_leaks(e)` |
| `fetch_mac` | method | `tests/test_security_remediation.py:357` | `def fetch_mac(mac)` |
| `fetch_phone` | method | `tests/test_security_remediation.py:360` | `def fetch_phone(n)` |
| `open` | method | `tests/test_security_remediation.py:565` | `def open(self, req, timeout)` |
| `osiris_endpoint` | method | `tests/test_security_remediation.py:376` | `def osiris_endpoint()` |
| `test_ci_yml_has_permissions` | method | `tests/test_security_remediation.py:309` | `def test_ci_yml_has_permissions(self)` |
| `test_ci_yml_permissions_is_read_all` | method | `tests/test_security_remediation.py:325` | `def test_ci_yml_permissions_is_read_all(self)` |
| `test_dns_failure_log_contains_host_length_not_host` | method | `tests/test_security_remediation.py:55` | `def test_dns_failure_log_contains_host_length_not_host(self, caplog)` |
| `test_dns_failure_log_omits_hostname` | method | `tests/test_security_remediation.py:29` | `def test_dns_failure_log_omits_hostname(self, caplog)` |
| `test_dns_failure_log_omits_ip_in_hostname` | method | `tests/test_security_remediation.py:43` | `def test_dns_failure_log_omits_ip_in_hostname(self, caplog)` |
| `test_encryption_runtimeerror_fixed_no_detail` | method | `tests/test_security_remediation.py:167` | `def test_encryption_runtimeerror_fixed_no_detail(self, app)` |
| `test_encryption_valueerror_fixed_no_detail` | method | `tests/test_security_remediation.py:159` | `def test_encryption_valueerror_fixed_no_detail(self, app)` |
| `test_encryption_valueerror_leaks_detail` | method | `tests/test_security_remediation.py:151` | `def test_encryption_valueerror_leaks_detail(self, app)` |
| `test_http_post_does_not_follow_redirect` | method | `tests/test_security_remediation.py:547` | `def test_http_post_does_not_follow_redirect(self)` |
| `test_innerhtml_not_used_with_template_literals` | method | `tests/test_security_remediation.py:439` | `def test_innerhtml_not_used_with_template_literals(self)` |
| `test_js_file_exists` | method | `tests/test_security_remediation.py:436` | `def test_js_file_exists(self)` |
| `test_no_html_string_round_trip` | method | `tests/test_security_remediation.py:636` | `def test_no_html_string_round_trip(self)` |
| `test_no_innerhtml_markdown_sink` | method | `tests/test_security_remediation.py:630` | `def test_no_innerhtml_markdown_sink(self)` |
| `test_no_insert_adjacent_html_in_tooltip` | method | `tests/test_security_remediation.py:601` | `def test_no_insert_adjacent_html_in_tooltip(self)` |
| `test_osiris_exception_returns_generic` | method | `tests/test_security_remediation.py:386` | `def test_osiris_exception_returns_generic(self, app)` |
| `test_raw_channel_url_refused_even_for_safe_host` | method | `tests/test_security_remediation.py:523` | `def test_raw_channel_url_refused_even_for_safe_host(self)` |
| `test_redirect_handler_refuses` | method | `tests/test_security_remediation.py:542` | `def test_redirect_handler_refuses(self)` |
| `test_redirect_implementation_uses_public_host` | method | `tests/test_security_remediation.py:402` | `def test_redirect_implementation_uses_public_host(self)` |
| `test_redirect_scheme_is_https` | method | `tests/test_security_remediation.py:285` | `def test_redirect_scheme_is_https(self, app)` |
| `test_redirect_uses_public_host_not_request_host` | method | `tests/test_security_remediation.py:271` | `def test_redirect_uses_public_host_not_request_host(self, app)` |
| `test_refuses_disallowed_scheme` | method | `tests/test_security_remediation.py:512` | `def test_refuses_disallowed_scheme(self)` |
| `test_refuses_link_local_metadata` | method | `tests/test_security_remediation.py:503` | `def test_refuses_link_local_metadata(self)` |
| `test_refuses_loopback` | method | `tests/test_security_remediation.py:508` | `def test_refuses_loopback(self)` |
| `test_sanitizer_blocks_dangerous_schemes_and_style` | method | `tests/test_security_remediation.py:618` | `def test_sanitizer_blocks_dangerous_schemes_and_style(self)` |
| `test_selectnode_inspector_safe` | method | `tests/test_security_remediation.py:474` | `def test_selectnode_inspector_safe(self)` |
| `test_showtooltipat_safe` | method | `tests/test_security_remediation.py:459` | `def test_showtooltipat_safe(self)` |
| `test_source_create_valueerror_fixed` | method | `tests/test_security_remediation.py:208` | `def test_source_create_valueerror_fixed(self, app)` |
| `test_source_delete_keyerror_fixed` | method | `tests/test_security_remediation.py:187` | `def test_source_delete_keyerror_fixed(self, app)` |
| `test_source_has_no_url_replace` | method | `tests/test_security_remediation.py:418` | `def test_source_has_no_url_replace(self)` |
| `test_source_update_valueerror_fixed` | method | `tests/test_security_remediation.py:232` | `def test_source_update_valueerror_fixed(self, app)` |
| `test_user_channel_url_cannot_reach_internal_host` | method | `tests/test_security_remediation.py:516` | `def test_user_channel_url_cannot_reach_internal_host(self)` |
| `test_vendored_dompurify_wired_with_fallback` | method | `tests/test_security_remediation.py:643` | `def test_vendored_dompurify_wired_with_fallback(self)` |
| `TestInfererPlatformList` | class | `tests/test_socmint.py:574` | `class TestInfererPlatformList` |
| `TestInfererResolveSpecificPlatforms` | class | `tests/test_socmint.py:593` | `class TestInfererResolveSpecificPlatforms` |
| `TestParserTotalness` | class | `tests/test_socmint.py:622` | `class TestParserTotalness` |
| `TestS10YouTubeMalformed` | class | `tests/test_socmint.py:442` | `class TestS10YouTubeMalformed` |
| `TestS11TwitchErrors` | class | `tests/test_socmint.py:479` | `class TestS11TwitchErrors` |
| `TestS12EntityExtraction` | class | `tests/test_socmint.py:507` | `class TestS12EntityExtraction` |
| `TestS1YouTubeHappyPath` | class | `tests/test_socmint.py:144` | `class TestS1YouTubeHappyPath` |
| `TestS2YouTubeNotFound` | class | `tests/test_socmint.py:174` | `class TestS2YouTubeNotFound` |
| `TestS3YouTubeRequiresKey` | class | `tests/test_socmint.py:193` | `class TestS3YouTubeRequiresKey` |
| `TestS4TwitchHappyPath` | class | `tests/test_socmint.py:222` | `class TestS4TwitchHappyPath` |
| `TestS5TwitchNotFound` | class | `tests/test_socmint.py:250` | `class TestS5TwitchNotFound` |
| `TestS6TwitterHappyPath` | class | `tests/test_socmint.py:279` | `class TestS6TwitterHappyPath` |
| `TestS7DiscordHappyPath` | class | `tests/test_socmint.py:319` | `class TestS7DiscordHappyPath` |
| `TestS8InfererCrossPlatform` | class | `tests/test_socmint.py:358` | `class TestS8InfererCrossPlatform` |
| `TestS9InfererUnknown` | class | `tests/test_socmint.py:406` | `class TestS9InfererUnknown` |
| `discord_response` | function | `tests/test_socmint.py:117` | `def discord_response()` |
| `test_401_error` | method | `tests/test_socmint.py:482` | `def test_401_error(self)` |
| `test_always_has_profile_count` | method | `tests/test_socmint.py:419` | `def test_always_has_profile_count(self)` |
| `test_discover_empty_text` | method | `tests/test_socmint.py:558` | `def test_discover_empty_text(self)` |
| `test_discover_no_urls` | method | `tests/test_socmint.py:563` | `def test_discover_no_urls(self)` |
| `test_empty_data_returns_not_found` | method | `tests/test_socmint.py:253` | `def test_empty_data_returns_not_found(self)` |
| `test_empty_items_returns_not_found` | method | `tests/test_socmint.py:177` | `def test_empty_items_returns_not_found(self)` |
| `test_empty_response` | method | `tests/test_socmint.py:341` | `def test_empty_response(self)` |
| `test_empty_username` | method | `tests/test_socmint.py:409` | `def test_empty_username(self)` |
| `test_error_response_returns_api_error` | method | `tests/test_socmint.py:258` | `def test_error_response_returns_api_error(self)` |
| `test_list_input` | method | `tests/test_socmint.py:450` | `def test_list_input(self)` |
| `test_list_input` | method | `tests/test_socmint.py:496` | `def test_list_input(self)` |
| `test_missing_data_returns_not_found` | method | `tests/test_socmint.py:268` | `def test_missing_data_returns_not_found(self)` |
| `test_missing_items_returns_not_found` | method | `tests/test_socmint.py:182` | `def test_missing_items_returns_not_found(self)` |
| `test_missing_statistics` | method | `tests/test_socmint.py:460` | `def test_missing_statistics(self)` |
| `test_none_input` | method | `tests/test_socmint.py:445` | `def test_none_input(self)` |
| `test_none_input` | method | `tests/test_socmint.py:491` | `def test_none_input(self)` |
| `test_none_response` | method | `tests/test_socmint.py:347` | `def test_none_response(self)` |
| `test_none_username` | method | `tests/test_socmint.py:414` | `def test_none_username(self)` |
| `test_not_found_with_errors` | method | `tests/test_socmint.py:306` | `def test_not_found_with_errors(self)` |
| `test_parser_handles_int` | method | `tests/test_socmint.py:645` | `def test_parser_handles_int(self, parser_fn)` |
| `test_parser_handles_none` | method | `tests/test_socmint.py:631` | `def test_parser_handles_none(self, parser_fn)` |
| `test_parser_handles_string` | method | `tests/test_socmint.py:659` | `def test_parser_handles_string(self, parser_fn)` |
| `test_parser_registered` | method | `tests/test_socmint.py:209` | `def test_parser_registered(self)` |
| `test_parser_returns_channel_id` | method | `tests/test_socmint.py:147` | `def test_parser_returns_channel_id(self, youtube_response)` |
| `test_parser_returns_display_name` | method | `tests/test_socmint.py:231` | `def test_parser_returns_display_name(self, twitch_response)` |
| `test_parser_returns_followers_count` | method | `tests/test_socmint.py:288` | `def test_parser_returns_followers_count(self, twitter_response)` |
| `test_parser_returns_member_counts` | method | `tests/test_socmint.py:334` | `def test_parser_returns_member_counts(self, discord_response)` |
| `test_parser_returns_metadata` | method | `tests/test_socmint.py:160` | `def test_parser_returns_metadata(self, youtube_response)` |
| `test_parser_returns_metadata` | method | `tests/test_socmint.py:237` | `def test_parser_returns_metadata(self, twitch_response)` |
| `test_parser_returns_metadata` | method | `tests/test_socmint.py:299` | `def test_parser_returns_metadata(self, twitter_response)` |
| `test_parser_returns_server_list` | method | `tests/test_socmint.py:322` | `def test_parser_returns_server_list(self, discord_response)` |
| `test_parser_returns_server_names` | method | `tests/test_socmint.py:328` | `def test_parser_returns_server_names(self, discord_response)` |
| `test_parser_returns_subscriber_count` | method | `tests/test_socmint.py:153` | `def test_parser_returns_subscriber_count(self, youtube_response)` |
| `test_parser_returns_user_id` | method | `tests/test_socmint.py:225` | `def test_parser_returns_user_id(self, twitch_response)` |
| `test_parser_returns_username` | method | `tests/test_socmint.py:282` | `def test_parser_returns_username(self, twitter_response)` |
| `test_parser_returns_verified_flag` | method | `tests/test_socmint.py:294` | `def test_parser_returns_verified_flag(self, twitter_response)` |
| `test_platform_list_has_required_fields` | method | `tests/test_socmint.py:583` | `def test_platform_list_has_required_fields(self)` |
| `test_platform_list_returns_all` | method | `tests/test_socmint.py:577` | `def test_platform_list_returns_all(self)` |
| `test_platform_urls_are_valid` | method | `tests/test_socmint.py:427` | `def test_platform_urls_are_valid(self)` |
| `test_resolve_has_high_confidence_for_populated_username` | method | `tests/test_socmint.py:379` | `def test_resolve_has_high_confidence_for_populated_username(self)` |
| `test_resolve_has_profile_urls` | method | `tests/test_socmint.py:393` | `def test_resolve_has_profile_urls(self)` |
| `test_resolve_includes_github` | method | `tests/test_socmint.py:373` | `def test_resolve_includes_github(self)` |
| `test_resolve_includes_keybase` | method | `tests/test_socmint.py:367` | `def test_resolve_includes_keybase(self)` |
| `test_resolve_linked_platforms_contains_keybase_note` | method | `tests/test_socmint.py:386` | `def test_resolve_linked_platforms_contains_keybase_note(self)` |
| `test_resolve_multiple_platforms` | method | `tests/test_socmint.py:602` | `def test_resolve_multiple_platforms(self)` |
| `test_resolve_single_platform` | method | `tests/test_socmint.py:596` | `def test_resolve_single_platform(self)` |
| `test_resolve_torvalds` | method | `tests/test_socmint.py:361` | `def test_resolve_torvalds(self)` |
| `test_resolve_validates_twitter_requires_key` | method | `tests/test_socmint.py:609` | `def test_resolve_validates_twitter_requires_key(self)` |
| `test_social_media_urls_in_text` | method | `tests/test_socmint.py:548` | `def test_social_media_urls_in_text(self)` |
| `test_string_input` | method | `tests/test_socmint.py:455` | `def test_string_input(self)` |
| `test_twitter_profile_extracts_person_and_username` | method | `tests/test_socmint.py:528` | `def test_twitter_profile_extracts_person_and_username(self)` |
| `test_yaml_source_has_requires_key` | method | `tests/test_socmint.py:196` | `def test_yaml_source_has_requires_key(self)` |
| `test_youtube_profile_extracts_person` | method | `tests/test_socmint.py:510` | `def test_youtube_profile_extracts_person(self)` |
| `twitch_response` | function | `tests/test_socmint.py:73` | `def twitch_response()` |
| `twitter_response` | function | `tests/test_socmint.py:92` | `def twitter_response()` |
| `youtube_response` | function | `tests/test_socmint.py:40` | `def youtube_response()` |
| `TestDashboard` | class | `tests/test_source_health_monitoring.py:248` | `class TestDashboard` |
| `TestDataclassContract` | class | `tests/test_source_health_monitoring.py:492` | `class TestDataclassContract` |
| `TestDegradingHighLatency` | class | `tests/test_source_health_monitoring.py:141` | `class TestDegradingHighLatency` |

Next: [SYMBOLS_p6.md](SYMBOLS_p6.md)
