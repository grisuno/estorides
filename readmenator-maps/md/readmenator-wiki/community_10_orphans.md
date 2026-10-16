# orphans

*Community 10 | 28 files | cohesion 0.00*

## Definition

This community groups 28 file(s) rooted at `.scratchpad` with dominant language py (cohesion 0.00). Central symbols: `LanBundleResult`, `LanPolicyDecision`, `LanPolicyRequest`, `TestAutoDetectType`, `TestBatchResultSerialization`, `TestConfigurableWeights`, `TestCriticalTarget`, `TestCrownJewelDetection`. Core file: `static/js/graph_force.js` (115 symbols). Documented purpose: estorides_core.lan_bundle.

## Files

### `.scratchpad` (11 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `.scratchpad/gb_shots.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_bridge.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_click.py` | py | utility | 0 | no |
| `.scratchpad/gfv2_data.py` | py | data_access | 0 | no |
| `.scratchpad/gfv2_debug.py` | py | utility | 0 | no |

### `tests` (6 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/conftest.py` | py | testing | 0 | yes |
| `tests/test_envutil.py` | py | testing | 12 | yes |
| `tests/test_graph_bundle_assets.py` | py | testing | 1 | yes |
| `tests/test_target_management.py` | py | testing | 86 | no |

### `estorides_core` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/lan_bundle.py` | py | utility | 8 | yes |
| `estorides_core/lan_policy.py` | py | business_logic | 9 | yes |
| `estorides_core/lan_scope.py` | py | utility | 5 | yes |

### `static/js` (3 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `static/js/graph_bundle.js` | js | utility | 66 | yes |
| `static/js/graph_force.js` | js | utility | 115 | yes |
| `static/js/source_manager.js` | js | utility | 19 | yes |

### `.` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `_multi_test.sh` | sh | testing | 0 | no |
| `install.sh` | sh | utility | 2 | yes |

### `tests/properties` (2 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tests/properties/conftest.py` | py | testing | 0 | yes |
| `tests/properties/test_target_management_properties.py` | py | testing | 10 | no |

### `tools` (1 files)

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `tools/split_sources.py` | py | utility | 1 | yes |

*... and 8 more files in this community.*


## Key Symbols

- `sanitize_stem` (function, `estorides_core/lan_bundle.py:27`) `def sanitize_stem(stem)` - Sanitize a file stem. Bad input falls back to lan.
- `default_output_dir` (function, `estorides_core/lan_bundle.py:38`) `def default_output_dir()` - Resolve the LAN output directory from env or data default.
- `build_bundle` (function, `estorides_core/lan_bundle.py:47`) `def build_bundle(devices)` - Build all four payloads. Never raises on bad items.
- `_fmt_ts` (function, `estorides_core/lan_bundle.py:330`) `def _fmt_ts(ts)`
- `_stix_ref` (function, `estorides_core/lan_bundle.py:340`) `def _stix_ref(node_id, id_map)`
- `LanBundleResult` (class, `estorides_core/lan_bundle.py:350`) `class LanBundleResult` - Outcome of write_bundle. Failures are values, never raises.
- `to_dict` (method, `estorides_core/lan_bundle.py:358`) `def to_dict(self)`
- `write_bundle` (function, `estorides_core/lan_bundle.py:362`) `def write_bundle(devices)` - Write all four deliverables atomically. Never raises.
- `LanPolicyRequest` (class, `estorides_core/lan_policy.py:30`) `class LanPolicyRequest` - Caller intent for a LAN discovery run.
- `LanPolicyDecision` (class, `estorides_core/lan_policy.py:40`) `class LanPolicyDecision` - Outcome of policy evaluation. JSON serializable via to_dict.
- `to_dict` (method, `estorides_core/lan_policy.py:50`) `def to_dict(self)`
- `requires_consent` (function, `estorides_core/lan_policy.py:54`) `def requires_consent()` - Return the canonical consent notice for the blocking modal.
- `_env_ceiling` (function, `estorides_core/lan_policy.py:59`) `def _env_ceiling()`
- `_strict_bool` (function, `estorides_core/lan_policy.py:66`) `def _strict_bool(value)`
- `_normalize_scope` (function, `estorides_core/lan_policy.py:70`) `def _normalize_scope(raw)` - Validate scope CIDR. Returns (normalized, error_code).
- `max_contact_for` (function, `estorides_core/lan_policy.py:97`) `def max_contact_for(allow_active, consent)` - Return active only on the triple gate, else none.
- `evaluate` (function, `estorides_core/lan_policy.py:104`) `def evaluate(request)` - Evaluate a LAN policy request. Never raises on bad input.
- `parse_interface_addr` (function, `estorides_core/lan_scope.py:23`) `def parse_interface_addr(raw)` - Normalize one interface address to CIDR, or None when unsafe.
- `select_private_cidrs` (function, `estorides_core/lan_scope.py:63`) `def select_private_cidrs(interfaces)` - Keep private CIDRs only, sorted and deduped. Never raises.
- `default_scope` (function, `estorides_core/lan_scope.py:79`) `def default_scope(interfaces)` - First private CIDR, or None when no private network exists.
- `parse_ip_addr_output` (function, `estorides_core/lan_scope.py:85`) `def parse_ip_addr_output(text)` - Parse `ip addr` output into address dicts. Pure, never raises.
- `read_local_interfaces` (function, `estorides_core/lan_scope.py:92`) `def read_local_interfaces()` - Read local interface addresses. Fail-soft, no probes sent.
- `install_full` (function, `install.sh:51`) - 3) Two install passes: full first, minimal fallback. We don't want a single Cython build error to le
- `install_minimal` (function, `install.sh:55`)
- `djb2KindColor` (function, `static/js/graph_bundle.js:33`)
- `mk` (function, `static/js/graph_bundle.js:61`)
- `clip` (function, `static/js/graph_bundle.js:67`)
- `tabActive` (function, `static/js/graph_bundle.js:71`)
- `ink` (function, `static/js/graph_bundle.js:75`)
- `v` (function, `static/js/graph_bundle.js:78`)

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
- `estorides_core/lan_bundle.py`
- `estorides_core/lan_policy.py`
- `estorides_core/lan_scope.py`
- `install.sh`
- `static/js/graph_bundle.js`
- `static/js/graph_force.js`
- `static/js/source_manager.js`
- `tests/conftest.py`
- *... and 8 more*
