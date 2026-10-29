# estorides_core: system_app_sources

estorides_core: system_app_sources groups 13 files (py) around ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError. estorides_core.lan_runner

```mermaid
graph LR
    estorides_core["estorides_core"]
    tests["tests"]
    tests -- "calls into" --> estorides_core
```

## estorides_core (8.1)

estorides_core groups 5 files (py) around ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError. estorides_core.lan_runner

## tests (8.2)

tests groups 8 files (py) around test_tool_parsers_never_raise, test_render_args_safe_inputs_no_metachars, test_render_args_substitution_is_verbatim, test_read_capped_respects_limit, test_parse_tool_output_never_raises. Property-based invariants for estorides_core.system_app_sources.

**Files**:

- estorides_core/active_recon.py
- estorides_core/lan_runner.py
- estorides_core/system_app_sources.py
- estorides_core/tool_install.py
- estorides_core/tool_runner.py
- tests/properties/test_system_app_sources_properties.py
- tests/properties/test_tool_runner_properties.py
- tests/test_active_recon.py
- tests/test_central_config.py
- tests/test_lan_runner.py
- tests/test_system_app_sources.py
- tests/test_tool_doctor.py
- tests/test_tool_install.py
