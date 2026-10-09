# orphans

*Community 10 | 11 files | cohesion 0.00*

## Definition

This community groups 11 file(s) rooted at `tests` with dominant language py (cohesion 0.00). Central symbols: `TestAutoDetectType`, `TestBatchResultSerialization`, `TestConfigurableWeights`, `TestCriticalTarget`, `TestCrownJewelDetection`, `TestCsvImport`, `TestEnvBool`, `TestEnvCsv`. Core file: `tests/test_target_management.py` (86 symbols). Documented purpose: Bootstrap a venv and install the runtime + optional test dependencies.  Idempotent: re-running on an existing venv is a no-op for the venv step. Tries the full .

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `_multi_test.sh` | sh | testing | 0 | no |
| `install.sh` | sh | utility | 2 | yes |
| `static/js/graph_force.js` | js | utility | 69 | yes |
| `static/js/source_manager.js` | js | utility | 18 | yes |
| `tests/conftest.py` | py | testing | 0 | yes |
| `tests/properties/test_target_management_properties.py` | py | testing | 10 | no |
| `tests/test_envutil.py` | py | testing | 12 | yes |
| `tests/test_target_management.py` | py | testing | 86 | no |
| `tests/test_target_scoring.py` | py | testing | 18 | yes |
| `tests/test_ui_visibility.py` | py | testing | 9 | yes |
| `tools/split_sources.py` | py | utility | 1 | yes |

## Key Symbols

- `install_full` (function, `install.sh:51`) - 3) Two install passes: full first, minimal fallback. We don't want a single Cython build error to le
- `install_minimal` (function, `install.sh:55`)
- `short` (function, `static/js/graph_force.js:21`)
- `esc` (function, `static/js/graph_force.js:25`)
- `toast` (function, `static/js/graph_force.js:44`)
- `fail` (function, `static/js/graph_force.js:52`)
- `settings` (function, `static/js/graph_force.js:59`)
- `adaptLocal` (function, `static/js/graph_force.js:66`) - --- adapt /api/graph nodes to RAW force-graph shape (fallback when the server did not send data.forc
- `ordered` (function, `static/js/graph_force.js:80`)
- `cid` (function, `static/js/graph_force.js:88`)
- `fam` (function, `static/js/graph_force.js:89`)
- `currentRaw` (function, `static/js/graph_force.js:121`)
- `rebuildRaw` (function, `static/js/graph_force.js:137`)
- `src` (function, `static/js/graph_force.js:146`)
- `indexRaw` (function, `static/js/graph_force.js:163`)
- `s` (function, `static/js/graph_force.js:173`)
- `t` (function, `static/js/graph_force.js:174`)
- `entities` (function, `static/js/graph_force.js:179`)
- `lkey` (function, `static/js/graph_force.js:193`)
- `colorOf` (function, `static/js/graph_force.js:194`)
- `dimmed` (function, `static/js/graph_force.js:195`)
- `hiddenKind` (function, `static/js/graph_force.js:196`)
- `visiblePayload` (function, `static/js/graph_force.js:201`)
- `s` (function, `static/js/graph_force.js:211`)
- `t` (function, `static/js/graph_force.js:212`)
- `computeHighlight` (function, `static/js/graph_force.js:218`)
- `tip` (function, `static/js/graph_force.js:241`)
- `refreshFamList` (function, `static/js/graph_force.js:258`)
- `famAnchor` (function, `static/js/graph_force.js:263`)
- `a` (function, `static/js/graph_force.js:270`)

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 3 file(s) lack file-level docs (e.g. `_multi_test.sh`)? What purpose do they serve?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.00?

## Sources

- `_multi_test.sh`
- `install.sh`
- `static/js/graph_force.js`
- `static/js/source_manager.js`
- `tests/conftest.py`
- `tests/properties/test_target_management_properties.py`
- `tests/test_envutil.py`
- `tests/test_target_management.py`
- `tests/test_target_scoring.py`
- `tests/test_ui_visibility.py`
- `tools/split_sources.py`
