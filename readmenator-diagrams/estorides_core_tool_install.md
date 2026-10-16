# estorides_core: tool_install

estorides_core: tool_install groups 12 files (py) around ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError. estorides_core.lan_runner

```mermaid
graph LR
    estorides_core["estorides_core"]
    tests["tests"]
    tests -- "calls into" --> estorides_core
```

## estorides_core (9.1)

estorides_core groups 5 files (py) around ToolError, ToolNotAllowedError, ToolInjectionError, ToolNotFoundError, ToolTimeoutError. estorides_core.lan_runner

## tests (9.2)

tests groups 7 files (py) around test_check_injection_safe_strings_silent, test_check_injection_detects_all_metacharacters, test_run_tool_never_raises, TestNmapResult, test_run_nmap_returns_result. Property-based invariants for estorides_core.tool_runner.

**Files**:

- estorides_core/active_recon.py
- estorides_core/lan_runner.py
- estorides_core/tool_install.py
- estorides_core/tool_runner.py
- estorides_core/validation.py
- tests/properties/test_tool_runner_properties.py
- tests/test_active_recon.py
- tests/test_central_config.py
- tests/test_lan_runner.py
- tests/test_tool_doctor.py
- tests/test_tool_install.py
- tests/test_tool_runner.py
