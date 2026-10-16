# Subsystem: tests (page 5 of 5)
Previous: [KB_tests_p4.md](KB_tests_p4.md)

## tests/test_ui_visibility.py
- Doc: Regression tests for the `hidden` attribute contract and output escaping.
- Layer: testing
- Language: py
- Symbols:
  - `_js` (function, line 21) `def _js()`
  - `TestHiddenContract` (class, line 25) `class TestHiddenContract`
  - `TestOutputEscaping` (class, line 54) `class TestOutputEscaping`
  - `test_css_enforces_hidden` (method, line 26) `def test_css_enforces_hidden(self)`
  - `test_setvisible_clears_hidden_attribute` (method, line 29) `def test_setvisible_clears_hidden_attribute(self)`
  - `test_no_inline_display_reveal_of_hidden_overlays` (method, line 34) `def test_no_inline_display_reveal_of_hidden_overlays(self)`
  - `test_tooltip_and_menu_use_setvisible` (method, line 47) `def test_tooltip_and_menu_use_setvisible(self)`
  - `test_entity_list_escapes_type_and_source` (method, line 55) `def test_entity_list_escapes_type_and_source(self)`
  - `test_fusion_detail_escapes_intel_level_and_lists` (method, line 60) `def test_fusion_detail_escapes_intel_level_and_lists(self)`

## tests/test_vuln_correlation.py
- Doc: ATDD + BDD tests for estorides_core.vuln_correlation.
- Layer: testing
- Language: py
- Symbols:
  - `_make_tech` (function, line 16) `def _make_tech(name, version)`
  - `TestNginxCveMatch` (class, line 21) `class TestNginxCveMatch`
  - `TestMetasploitAvailable` (class, line 31) `class TestMetasploitAvailable`
  - `TestUnknownTechnology` (class, line 41) `class TestUnknownTechnology`
  - `TestDefaultCredentials` (class, line 50) `class TestDefaultCredentials`
  - `TestCriticalPrioritised` (class, line 62) `class TestCriticalPrioritised`
  - `TestNoVersionMatch` (class, line 71) `class TestNoVersionMatch`
  - `TestAttackReadiness` (class, line 81) `class TestAttackReadiness`
  - `TestLocalCveLookup` (class, line 94) `class TestLocalCveLookup`
  - `test_returns_cves_for_nginx` (method, line 22) `def test_returns_cves_for_nginx(self)`
  - `test_apache_struts_has_metasploit` (method, line 32) `def test_apache_struts_has_metasploit(self)`
  - `test_unknown_tech_returns_empty` (method, line 42) `def test_unknown_tech_returns_empty(self)`
  - `test_jenkins_has_default_admin` (method, line 51) `def test_jenkins_has_default_admin(self)`
  - `test_most_critical_is_highest_cvss` (method, line 63) `def test_most_critical_is_highest_cvss(self)`
  - `test_no_version_reduces_confidence` (method, line 72) `def test_no_version_reduces_confidence(self)`
  - `test_exploit_available_increases_score` (method, line 82) `def test_exploit_available_increases_score(self)`
  - `test_known_tech_in_local_table` (method, line 95) `def test_known_tech_in_local_table(self)`
- Depends on: `estorides_core/vuln_correlation.py`

## tests/test_web_helpers.py
- Doc: BDD tests for the web-layer decorators/helpers extracted from `create_app`.  - WH1: `_provides`...
- Layer: testing
- Language: py
- Symbols:
  - `_app` (function, line 17) `def _app()`
  - `TestWH1Missing` (class, line 24) `class TestWH1Missing`
  - `TestWH2Present` (class, line 39) `class TestWH2Present`
  - `TestWH3Ordering` (class, line 54) `class TestWH3Ordering`
  - `TestWH4Sse` (class, line 72) `class TestWH4Sse`
  - `test_missing_service_edges_503` (method, line 25) `def test_missing_service_edges_503(self)`
  - `test_present_service_passes` (method, line 40) `def test_present_service_passes(self)`
  - `test_guard_runs_after_auth` (method, line 55) `def test_guard_runs_after_auth(self)`
  - `test_sse_headers` (method, line 73) `def test_sse_headers(self)`
  - `view` (method, line 31) `def view()`
  - `view` (method, line 46) `def view()`
  - `view` (method, line 63) `def view()`
  - `stream` (method, line 77) `def stream()`
- Depends on: `estorides_core/web_security.py`, `estorides_web.py`

## tests/test_web_tools_blueprint.py
- Doc: M5 RED tests: tools blueprint slice.
- Layer: testing
- Language: py
- Symbols:
  - `test_tools_rules_present` (function, line 5) `def test_tools_rules_present()`
  - `test_blueprint_registered` (function, line 16) `def test_blueprint_registered()`
  - `test_unknown_tool_install_reaches_view` (function, line 23) `def test_unknown_tool_install_reaches_view()`
  - `test_install_route_rejects_bad_binary` (function, line 34) `def test_install_route_rejects_bad_binary()`
- Depends on: `estorides_web.py`

