# Subsystem: properties

## tests/properties/test_change_detection_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_scores_always_bounded` (function, line 69) `def test_scores_always_bounded(before, after)`
  - `test_max_changes_respected` (function, line 77) `def test_max_changes_respected(before, after)`
  - `test_id_is_16_char_hex` (function, line 86) `def test_id_is_16_char_hex(before, after)`
  - `test_idempotent` (function, line 95) `def test_idempotent(before, after)`
  - `test_first_run_reports_all_as_new` (function, line 105) `def test_first_run_reports_all_as_new(after)`
  - `test_after_none_returns_empty` (function, line 113) `def test_after_none_returns_empty(before)`
  - `test_before_vs_no_after_empty` (function, line 121) `def test_before_vs_no_after_empty(entities)`
  - `test_summary_consistency` (function, line 132) `def test_summary_consistency(before, after)`
- Depends on: `estorides_core/change_detection.py`

## tests/properties/test_csp_safe_styles_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_js_never_gains_a_style_attribute_in_template_literal` (function, line 58) `def test_js_never_gains_a_style_attribute_in_template_literal(insertion)`
  - `test_template_never_gains_a_style_attribute` (function, line 105) `def test_template_never_gains_a_style_attribute(insertion)`
  - `test_csp_style_src_never_gains_unsafe_inline` (function, line 137) `def test_csp_style_src_never_gains_unsafe_inline(bad)`
- Depends on: `estorides_core/web_security.py`

## tests/properties/test_hypothesis_engine_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_scores_always_bounded` (function, line 54) `def test_scores_always_bounded(observations, entities)`
  - `test_claim_length_under_cap` (function, line 66) `def test_claim_length_under_cap(observations, entities)`
  - `test_reasoning_length_under_cap` (function, line 77) `def test_reasoning_length_under_cap(observations, entities)`
  - `test_sources_sorted_unique` (function, line 88) `def test_sources_sorted_unique(observations, entities)`
  - `test_id_is_deterministic_hex` (function, line 99) `def test_id_is_deterministic_hex(observations, entities)`
  - `test_idempotent` (function, line 112) `def test_idempotent(observations, entities)`
  - `test_max_hypotheses_caps_output` (function, line 123) `def test_max_hypotheses_caps_output(observations, entities)`
  - `test_min_score_filters` (function, line 134) `def test_min_score_filters(observations, entities)`
  - `test_hostile_observation_does_not_crash` (function, line 147) `def test_hostile_observation_does_not_crash(observations, entities)`
- Depends on: `estorides_core/hypothesis_engine.py`

## tests/properties/test_observation_models_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `meta_strategy` (function, line 45) `def meta_strategy(draw)`
  - `obs_strategy` (function, line 60) `def obs_strategy(draw)`
  - `entity_strategy` (function, line 76) `def entity_strategy(draw)`
  - `test_observation_round_trip_stability` (function, line 90) `def test_observation_round_trip_stability(payload)`
  - `test_observation_bounded_fields` (function, line 103) `def test_observation_bounded_fields(payload)`
  - `test_entity_round_trip_and_bounds` (function, line 115) `def test_entity_round_trip_and_bounds(payload)`
  - `test_meta_never_echoes_unbounded_url` (function, line 128) `def test_meta_never_echoes_unbounded_url(metas)`
- Depends on: `estorides_core/observation_models.py`

## tests/properties/test_recon_fusion_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `TestPropertyScoreBounds` (class, line 48) `class TestPropertyScoreBounds`
  - `TestPropertyTotalCounts` (class, line 68) `class TestPropertyTotalCounts`
  - `TestPropertyTierSumMatches` (class, line 93) `class TestPropertyTierSumMatches`
  - `TestPropertyDeterminism` (class, line 114) `class TestPropertyDeterminism`
  - `TestPropertyNoDuplicates` (class, line 135) `class TestPropertyNoDuplicates`
  - `TestPropertyTierKeysOrder` (class, line 155) `class TestPropertyTierKeysOrder`
  - `TestPropertyEmptyQueryRejected` (class, line 176) `class TestPropertyEmptyQueryRejected`
  - `TestPropertySafeWithBadInputs` (class, line 196) `class TestPropertySafeWithBadInputs`
  - `test_all_scores_in_unit_interval` (method, line 58) `def test_all_scores_in_unit_interval(self, query, query_type, observations, entities)`
  - `test_counts_match_input` (method, line 78) `def test_counts_match_input(self, query, query_type, n_obs, n_ents)`
  - `test_tier_summary_matches` (method, line 103) `def test_tier_summary_matches(self, query, query_type, observations, entities)`
  - `test_deterministic_output` (method, line 124) `def test_deterministic_output(self, query, query_type, observations, entities)`
  - `test_no_duplicate_ids_in_tier` (method, line 145) `def test_no_duplicate_ids_in_tier(self, query, query_type, observations, entities)`
  - `test_tier_keys_in_canonical_order` (method, line 165) `def test_tier_keys_in_canonical_order(self, query, query_type, observations, entities)`
  - `test_empty_query_raises` (method, line 185) `def test_empty_query_raises(self, query_type, observations, entities)`
  - `test_none_inputs_safe` (method, line 201) `def test_none_inputs_safe(self, query, query_type)`
  - `test_entities_none_is_safe` (method, line 214) `def test_entities_none_is_safe(self, query, query_type, observations)`
- Depends on: `estorides_core/recon_fusion.py`

## tests/properties/test_reliability_scoring_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_score_always_bounded` (function, line 56) `def test_score_always_bounded(reliability, credibility, corroboration, age, base, half_life)`
  - `test_corroboration_weight_in_unit_interval` (function, line 73) `def test_corroboration_weight_in_unit_interval(n)`
  - `test_freshness_monotone_in_age` (function, line 87) `def test_freshness_monotone_in_age(age1, age2)`
  - `test_reliability_from_name_never_raises` (function, line 110) `def test_reliability_from_name_never_raises(name)`
  - `test_merge_confidence_bounded` (function, line 126) `def test_merge_confidence_bounded(existing, new_obs, new_rel, new_cred, cor, age)`
  - `test_reliability_weight_set_is_curated` (function, line 141) `def test_reliability_weight_set_is_curated()`
  - `test_credibility_weight_set_is_curated` (function, line 146) `def test_credibility_weight_set_is_curated()`
  - `test_corroboration_is_monotone_in_count` (function, line 159) `def test_corroboration_is_monotone_in_count(n1, n2)`
  - `test_higher_reliability_dominates` (function, line 184) `def test_higher_reliability_dominates(rel1, rel2)`
  - `test_source_type_from_name_never_raises` (function, line 202) `def test_source_type_from_name_never_raises(name)`
  - `test_source_type_weight_always_curated` (function, line 219) `def test_source_type_weight_always_curated(reliability, credibility, source_type, corroboration, age, base, half_life)`
  - `test_source_type_weight_set_is_curated` (function, line 241) `def test_source_type_weight_set_is_curated()`
- Depends on: `estorides_core/reliability_scoring.py`

## tests/properties/test_search_telemetry_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_progress_invariants_hold` (function, line 32) `def test_progress_invariants_hold(completed, total, phase_key)`
  - `test_progress_rejects_unknown_phase` (function, line 46) `def test_progress_rejects_unknown_phase(phase_key)`
  - `test_brand_predicate_is_total` (function, line 56) `def test_brand_predicate_is_total(text)`
  - `test_emoji_predicate_is_total` (function, line 65) `def test_emoji_predicate_is_total(text)`
  - `test_percent_encoded_emoji_predicate_is_total` (function, line 74) `def test_percent_encoded_emoji_predicate_is_total(text)`
  - `test_brand_predicate_flags_embedded_brand` (function, line 84) `def test_brand_predicate_flags_embedded_brand(prefix, suffix)`
- Depends on: `estorides_core/search_telemetry.py`

## tests/properties/test_source_health_monitoring_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `_valid_input` (function, line 21) `def _valid_input(fetch, ok, latency, last_seen, now)`
  - `test_health_score_always_bounded` (function, line 49) `def test_health_score_always_bounded(fetch, ok, latency, last_seen, now)`
  - `test_status_always_valid_enum` (function, line 63) `def test_status_always_valid_enum(fetch, ok, latency, last_seen, now)`
  - `test_success_rate_bounds` (function, line 78) `def test_success_rate_bounds(fetch, ok, latency, last_seen, now)`
  - `test_unknown_when_below_min_fetches` (function, line 89) `def test_unknown_when_below_min_fetches(fetch, config_min)`
  - `valid_health_inputs` (function, line 97) `def valid_health_inputs(draw)`
  - `test_dashboard_summary_counts_match` (function, line 112) `def test_dashboard_summary_counts_match(records)`
- Depends on: `estorides_core/source_health_monitoring.py`

## tests/properties/test_system_app_sources_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_tool_parsers_never_raise` (function, line 37) `def test_tool_parsers_never_raise(parser_name, blob)`
  - `test_render_args_safe_inputs_no_metachars` (function, line 55) `def test_render_args_safe_inputs_no_metachars(args, query, outdir)`
  - `test_render_args_substitution_is_verbatim` (function, line 70) `def test_render_args_substitution_is_verbatim(query, outdir)`
  - `test_read_capped_respects_limit` (function, line 83) `def test_read_capped_respects_limit(blob, cap)`
  - `test_parse_tool_output_never_raises` (function, line 110) `def test_parse_tool_output_never_raises(parser_name, data)`
  - `test_adversarial_query_rejected_at_runner_boundary` (function, line 124) `def test_adversarial_query_rejected_at_runner_boundary(prefix, bad, suffix)`
- Depends on: `estorides_core/parsers.py`, `estorides_core/system_app_sources.py`, `estorides_core/tool_runner.py`

## tests/properties/test_target_management_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_p1_add_target_never_raises` (function, line 21) `def test_p1_add_target_never_raises(etype, value)`
  - `test_p2_validated_id_is_deterministic` (function, line 31) `def test_p2_validated_id_is_deterministic(etype, value)`
  - `test_p3_make_target_id_stable_under_case` (function, line 40) `def test_p3_make_target_id_stable_under_case(etype, value)`
  - `test_p4_valid_domains_validate` (function, line 56) `def test_p4_valid_domains_validate(d)`
  - `test_p5_valid_ipv4_validate` (function, line 68) `def test_p5_valid_ipv4_validate(ip)`
  - `test_p6_valid_emails_validate` (function, line 77) `def test_p6_valid_emails_validate(email)`
  - `test_p7_auto_detect_never_fails` (function, line 83) `def test_p7_auto_detect_never_fails(value)`
  - `test_p8_validate_target_never_raises` (function, line 89) `def test_p8_validate_target_never_raises(value)`
  - `test_p9_batch_import_idempotent` (function, line 105) `def test_p9_batch_import_idempotent(targets)`
  - `test_p10_batch_import_never_raises` (function, line 116) `def test_p10_batch_import_never_raises(text)`

## tests/properties/test_tool_runner_properties.py
- Layer: testing
- Language: py
- Symbols:
  - `test_check_injection_safe_strings_silent` (function, line 35) `def test_check_injection_safe_strings_silent(args)`
  - `test_check_injection_detects_all_metacharacters` (function, line 46) `def test_check_injection_detects_all_metacharacters(prefix, bad, suffix)`
  - `test_run_tool_never_raises` (function, line 63) `def test_run_tool_never_raises(target)`
- Depends on: `estorides_core/tool_runner.py`
