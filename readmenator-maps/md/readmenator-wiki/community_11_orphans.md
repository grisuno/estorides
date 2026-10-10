# orphans

*Community 11 | 24 files | cohesion 0.00*

## Definition

This community groups 24 file(s) rooted at `.scratchpad` with dominant language py (cohesion 0.00). Central symbols: `TestAutoDetectType`, `TestBatchResultSerialization`, `TestConfigurableWeights`, `TestCriticalTarget`, `TestCrownJewelDetection`, `TestCsvImport`, `TestEnvBool`, `TestEnvCsv`. Core file: `static/js/graph_force.js` (109 symbols). Documented purpose: Bootstrap a venv and install the runtime + optional test dependencies.  Idempotent: re-running on an existing venv is a no-op for the venv step. Tries the full .

## Files

### `.scratchpad` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `.scratchpad/gb_shots.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_bridge.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_click.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_data.py` | py | data_access | 0 | no |
| `.scratchpad/gfv2_debug.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_dom.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_func.py` | py | utility | 0 | no |

### `tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 0 | yes |
| `tests/test_envutil.py` | py | testing | 12 | yes |
| `tests/test_graph_bundle_assets.py` | py | testing | 1 | yes |
| `tests/test_target_management.py` | py | testing | 86 | no |
| `tests/test_target_scoring.py` | py | testing | 18 | yes |
| `tests/test_ui_visibility.py` | py | testing | 9 | yes |

### `static/js` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/graph_bundle.js` | js | utility | 62 | yes |
| `static/js/graph_force.js` | js | utility | 109 | yes |
| `static/js/source_manager.js` | js | utility | 18 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `_multi_test.sh` | sh | testing | 0 | no |
| `install.sh` | sh | utility | 2 | yes |

### `tests/properties` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/test_target_management_properties.py` | py | testing | 10 | no |

### `tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/split_sources.py` | py | utility | 1 | yes |

*... and 4 more files in this community.*


## Key Symbols

- `install_full` (function, `install.sh:51`) - 3) Two install passes: full first, minimal fallback. We don't want a single Cython build error to le
- `install_minimal` (function, `install.sh:55`)
- `djb2KindColor` (function, `static/js/graph_bundle.js:32`)
- `mk` (function, `static/js/graph_bundle.js:60`)
- `clip` (function, `static/js/graph_bundle.js:66`)
- `tabActive` (function, `static/js/graph_bundle.js:70`)
- `ink` (function, `static/js/graph_bundle.js:74`)
- `v` (function, `static/js/graph_bundle.js:78`)
- `colorOf` (function, `static/js/graph_bundle.js:88`)
- `keyOf` (function, `static/js/graph_bundle.js:94`)
- `bspline` (function, `static/js/graph_bundle.js:99`)
- `curve` (function, `static/js/graph_bundle.js:120`)
- `buildCurves` (function, `static/js/graph_bundle.js:137`)
- `resize` (function, `static/js/graph_bundle.js:148`)
- `radius` (function, `static/js/graph_bundle.js:160`)
- `center` (function, `static/js/graph_bundle.js:164`)
- `makeProjector` (function, `static/js/graph_bundle.js:165`)
- `depthAlpha` (function, `static/js/graph_bundle.js:175`)
- `focusState` (function, `static/js/graph_bundle.js:177`)
- `edgeState` (function, `static/js/graph_bundle.js:185`)
- `nodeLit` (function, `static/js/graph_bundle.js:205`)
- `strokeCurve` (function, `static/js/graph_bundle.js:216`)
- `pointOn` (function, `static/js/graph_bundle.js:226`)
- `g` (function, `static/js/graph_bundle.js:229`)
- `draw` (function, `static/js/graph_bundle.js:231`)
- `t0` (function, `static/js/graph_bundle.js:275`)
- `tt` (function, `static/js/graph_bundle.js:279`)
- `drawGroups` (function, `static/js/graph_bundle.js:291`)
- `mid` (function, `static/js/graph_bundle.js:306`)
- `nodeRadius` (function, `static/js/graph_bundle.js:333`)

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 14 file(s) lack file-level docs (e.g. `.scratchpad/gb_shots.py`)? What purpose do they serve?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.00?

## Sources

- `.scratchpad/gb_shots.py`
- `.scratchpad/gfv2_bridge.py`
- `.scratchpad/gfv2_click.py`
- `.scratchpad/gfv2_data.py`
- `.scratchpad/gfv2_debug.py`
- `.scratchpad/gfv2_dom.py`
- `.scratchpad/gfv2_func.py`
- `.scratchpad/gfv2_raw.py`
- `.scratchpad/gfv2_shots.py`
- `.scratchpad/gfv2_step.py`
- `.scratchpad/gfv2_time.py`
- `_multi_test.sh`
- `install.sh`
- `static/js/graph_bundle.js`
- `static/js/graph_force.js`
- `static/js/source_manager.js`
- `tests/conftest.py`
- `tests/properties/test_target_management_properties.py`
- `tests/test_envutil.py`
- `tests/test_graph_bundle_assets.py`
- *... and 4 more*
