# tests

*Community 8 | 4 files | cohesion 0.43*

## Definition

This community groups 4 file(s) rooted at `tests` with dominant language py (cohesion 0.43). Central symbols: `InstallRecipe`, `InstallResult`, `TestElevation`, `TestInstallFlow`, `TestPathTraversal`, `TestRecipes`, `ToolStatus`, `_check_shell_command`. Core file: `tests/test_tool_install.py` (28 symbols). Documented purpose: estorides_core.tool_install.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/tool_install.py` | py | utility | 27 | yes |
| `tests/test_central_config.py` | py | testing | 3 | yes |
| `tests/test_tool_doctor.py` | py | testing | 4 | yes |
| `tests/test_tool_install.py` | py | testing | 28 | yes |

## Key Symbols

- `InstallRecipe` (class, `estorides_core/tool_install.py:81`) `class InstallRecipe` - One tool's install recipe, loaded from ``tool_recipes/<name>.yaml``.
- `has_apt` (method, `estorides_core/tool_install.py:95`) `def has_apt(self)`
- `has_git` (method, `estorides_core/tool_install.py:98`) `def has_git(self)`
- `InstallResult` (class, `estorides_core/tool_install.py:103`) `class InstallResult` - Outcome of one ``install_tool`` invocation. Failures are values.
- `to_dict` (method, `estorides_core/tool_install.py:113`) `def to_dict(self)`
- `_elevate` (method, `estorides_core/tool_install.py:117`) `def _elevate(cmd)` - Prepend an elevation wrapper when required.
- `_run` (method, `estorides_core/tool_install.py:132`) `def _run(cmd)` - Run a subprocess as an argument list, capping output.
- `_check_shell_command` (method, `estorides_core/tool_install.py:148`) `def _check_shell_command(command)` - Reject hostile tokens in a trusted recipe's install_command.
- `_needs_elevation` (method, `estorides_core/tool_install.py:154`) `def _needs_elevation(command)` - True when an install_command writes system-wide and needs root.
- `is_valid_recipe_name` (method, `estorides_core/tool_install.py:169`) `def is_valid_recipe_name(name)` - True when ``name`` is a safe recipe/tool identifier (no separators).
- `is_valid_binary` (method, `estorides_core/tool_install.py:174`) `def is_valid_binary(name)` - True when ``name`` is a plausible bare binary name (no path).
- `_recipe_table` (method, `estorides_core/tool_install.py:179`) `def _recipe_table()` - Map recipe stem to its file from the directory listing.
- `_recipe_path` (method, `estorides_core/tool_install.py:193`) `def _recipe_path(name)`
- `load_recipe` (method, `estorides_core/tool_install.py:210`) `def load_recipe(name)` - Load a tool recipe from ``tool_recipes/<name>.yaml`` (or ``None``).
- `recipe_available` (method, `estorides_core/tool_install.py:254`) `def recipe_available(name)` - True when a recipe exists for ``name`` (the UI gates the button on this).
- `tool_available` (method, `estorides_core/tool_install.py:259`) `def tool_available(binary)` - True when the binary resolves on PATH (mirrors system_app_sources).
- `list_recipes` (method, `estorides_core/tool_install.py:270`) `def list_recipes()` - Names of all tool recipe files in ``tool_recipes/`` (sorted).
- `ToolStatus` (class, `estorides_core/tool_install.py:278`) `class ToolStatus` - One binary's install/readiness state for the doctor report.
- `to_dict` (method, `estorides_core/tool_install.py:287`) `def to_dict(self)`
- `_system_app_binaries` (method, `estorides_core/tool_install.py:297`) `def _system_app_binaries(sources_dir)` - Map binary -> source names from the system_app YAML catalog.
- `doctor` (method, `estorides_core/tool_install.py:321`) `def doctor(sources_dir)` - Read-only readiness report over system_app binaries + recipes.
- `_install_apt` (method, `estorides_core/tool_install.py:358`) `def _install_apt(recipe)` - Install an apt package via the elevation wrapper (run0/sudo).
- `_tools_root` (method, `estorides_core/tool_install.py:371`) `def _tools_root()`
- `_install_git` (method, `estorides_core/tool_install.py:375`) `def _install_git(recipe)` - Clone the repo (as operator) and run install_command (elevated if system-wide).
- `install_tool` (method, `estorides_core/tool_install.py:414`) `def install_tool(tool_name)` - Install a missing tool from its recipe (if any).
- `_verify` (method, `estorides_core/tool_install.py:506`) `def _verify(binary)` - Post-install check: can the binary now be resolved?
- `main` (method, `estorides_core/tool_install.py:516`) `def main(argv)` - Minimal CLI: ``python -m estorides_core.tool_install <tool> [--force]``.
- `test_config_defaults` (function, `tests/test_central_config.py:7`) `def test_config_defaults()`
- `test_run_defaults_track_config` (function, `tests/test_central_config.py:20`) `def test_run_defaults_track_config()`
- `test_tool_install_survives_malformed_env` (function, `tests/test_central_config.py:29`) `def test_tool_install_survives_malformed_env(monkeypatch)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 6
- Cross-boundary resolved imports (EXTRACTED): 5

## Connections

- [EXTRACTED] depends_on community 8 <-> 6 (strength 0.9): Extracted import edge crosses communities: estorides_core/tool_install.py imports estorides_core/config.py.
- [EXTRACTED] depends_on community 1 <-> 8 (strength 0.9): Extracted import edge crosses communities: estorides_web_tools.py imports estorides_core/tool_install.py.
- [INFERRED] shares_context community 0 <-> 8 (strength 0.5): Inferred shared context (language py) with no import path between community 0 (root) and community 8 (tests).

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in tests changed?
- Should tests be split, given cohesion 0.43?

## Sources

- `estorides_core/tool_install.py`
- `tests/test_central_config.py`
- `tests/test_tool_doctor.py`
- `tests/test_tool_install.py`
