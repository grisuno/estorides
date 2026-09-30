# orphans

*Community 4 | 12 files | cohesion 0.00*

## Definition

This community groups 12 file(s) rooted at `tests` with dominant language py (cohesion 0.00). Central symbols: `TestAutoDetectType`, `TestBatchResultSerialization`, `TestConfigurableWeights`, `TestCriticalTarget`, `TestCrownJewelDetection`, `TestCsvImport`, `TestEnvBool`, `TestEnvCsv`. Core file: `tests/test_target_management.py` (86 symbols). Documented purpose: Bootstrap a venv and install the runtime + optional test dependencies.  Idempotent: re-running on an existing venv is a no-op for the venv step. Tries the full .

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `_multi_test.sh` | sh | testing | 0 | no |
| `install.sh` | sh | utility | 2 | yes |
| `static/js/source_manager.js` | js | utility | 18 | yes |
| `tests/conftest.py` | py | testing | 0 | yes |
| `tests/properties/test_target_management_properties.py` | py | testing | 10 | no |
| `tests/test_envutil.py` | py | testing | 12 | yes |
| `tests/test_orchestrator_fanout.py` | py | testing | 9 | yes |
| `tests/test_parsers.py` | py | testing | 9 | yes |
| `tests/test_target_management.py` | py | testing | 86 | no |
| `tests/test_target_scoring.py` | py | testing | 18 | yes |
| `tests/test_ui_visibility.py` | py | testing | 9 | yes |
| `tools/split_sources.py` | py | utility | 1 | yes |

## Key Symbols

- `install_full` (function, `install.sh:51`) - 3) Two install passes: full first, minimal fallback. We don't want a single Cython build error to le
- `install_minimal` (function, `install.sh:55`)
- `authHeaders` (function, `static/js/source_manager.js:7`) - /* Estorides Source Manager — form-based YAML editor (function () { 'use strict'; /* ─── auth ───
- `apiFetch` (function, `static/js/source_manager.js:15`)
- `getCheckedTags` (function, `static/js/source_manager.js:67`) - contact: $('field-contact'), logsQueries: $('field-logs-queries'), toolUrl: $('field-tool-url'), too
- `setCheckedTags` (function, `static/js/source_manager.js:74`)
- `readForm` (function, `static/js/source_manager.js:84`) - var checks = container.querySelectorAll('input[type="checkbox"]:checked'); return Array.from(checks)
- `writeForm` (function, `static/js/source_manager.js:120`) - try { var b = JSON.parse(fields.toolBody.value.trim() \|\| '{}'); if (Object.keys(b).length) s.tool.bo
- `updateYamlPreview` (function, `static/js/source_manager.js:183`) - fields.pagCursorPath.value = pag.cursor_path \|\| ''; setCheckedTags('field-applies-to', s.applies_to)
- `renderList` (function, `static/js/source_manager.js:193`) - updateYamlPreview(); } /* ─── update YAML preview ─── function updateYamlPreview() { try { var s = r
- `escHtml` (function, `static/js/source_manager.js:223`) - var keyBadge = s.requires_key ? '<span class="src-item-key-badge">key</span>' : ''; var sysBadge = s
- `escAttr` (function, `static/js/source_manager.js:224`)
- `toast` (function, `static/js/source_manager.js:227`) - '<div class="src-item-info">' + '<div class="src-item-name">' + escHtml(s.name) + sysBadge + keyBadg
- `loadSources` (function, `static/js/source_manager.js:236`) - /* ─── helpers ─── function escHtml(s) { return String(s).replace(/[&<>"]/g, function (m) { return (
- `clearEditor` (function, `static/js/source_manager.js:251`) - apiFetch('/api/sources/yaml').then(function (data) { sources = data.sources \|\| []; srcCount.textCont
- `from` (class, `static/js/source_manager.js:255`)
- `selectSource` (function, `static/js/source_manager.js:261`) - }); } /* ─── clear editor ─── function clearEditor() { form.hidden = true; editorEmpty.hidden = fals
- `saveSource` (function, `static/js/source_manager.js:273`) - /* ─── select source ─── function selectSource(name) { var s = sources.filter(function (s) { return
- `deleteSource` (function, `static/js/source_manager.js:304`) - toast('Source "' + data.name + '" saved', 'ok'); formStatus.textContent = 'Saved'; formStatus.classN
- `newSource` (function, `static/js/source_manager.js:334`) - overlay.remove(); apiFetch('/api/sources/yaml/' + encodeURIComponent(currentName), { method: 'DELETE
- `test_p1_add_target_never_raises` (function, `tests/properties/test_target_management_properties.py:21`) `def test_p1_add_target_never_raises(etype, value)`
- `test_p2_validated_id_is_deterministic` (function, `tests/properties/test_target_management_properties.py:31`) `def test_p2_validated_id_is_deterministic(etype, value)`
- `test_p3_make_target_id_stable_under_case` (function, `tests/properties/test_target_management_properties.py:40`) `def test_p3_make_target_id_stable_under_case(etype, value)`
- `test_p4_valid_domains_validate` (function, `tests/properties/test_target_management_properties.py:56`) `def test_p4_valid_domains_validate(d)`
- `test_p5_valid_ipv4_validate` (function, `tests/properties/test_target_management_properties.py:68`) `def test_p5_valid_ipv4_validate(ip)`
- `test_p6_valid_emails_validate` (function, `tests/properties/test_target_management_properties.py:77`) `def test_p6_valid_emails_validate(email)`
- `test_p7_auto_detect_never_fails` (function, `tests/properties/test_target_management_properties.py:83`) `def test_p7_auto_detect_never_fails(value)`
- `test_p8_validate_target_never_raises` (function, `tests/properties/test_target_management_properties.py:89`) `def test_p8_validate_target_never_raises(value)`
- `test_p9_batch_import_idempotent` (function, `tests/properties/test_target_management_properties.py:105`) `def test_p9_batch_import_idempotent(targets)`
- `test_p10_batch_import_never_raises` (function, `tests/properties/test_target_management_properties.py:116`) `def test_p10_batch_import_never_raises(text)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- [INFERRED] shares_context community 0 <-> 4 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 0 (estorides_core) and community 4 (orphans).
- [INFERRED] shares_context community 1 <-> 4 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 1 (estorides_core) and community 4 (orphans).
- [INFERRED] shares_context community 2 <-> 4 (strength 0.5): Inferred shared context (language py and layer testing) with no import path between community 2 (tests/properties) and community 4 (orphans).
- [INFERRED] shares_context community 3 <-> 4 (strength 0.5): Inferred shared context (language py) with no import path between community 3 (estorides_llm) and community 4 (orphans).

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `_multi_test.sh`)? What purpose do they serve?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.00?

## Sources

- `_multi_test.sh`
- `install.sh`
- `static/js/source_manager.js`
- `tests/conftest.py`
- `tests/properties/test_target_management_properties.py`
- `tests/test_envutil.py`
- `tests/test_orchestrator_fanout.py`
- `tests/test_parsers.py`
- `tests/test_target_management.py`
- `tests/test_target_scoring.py`
- `tests/test_ui_visibility.py`
- `tools/split_sources.py`
