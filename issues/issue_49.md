# Issue #49: estorides_core/config.py creates filesystem directories at module import time — violates project's own hard rules

- **State:** open
- **Created:** 2026-06-08T11:43:44Z
- **Updated:** 2026-06-08T11:43:44Z
- **Labels:** None

---

## Summary
The `estorides_core/config.py` module creates `data/` and `reports/` directories at module import time via `DATA_DIR.mkdir(parents=True, exist_ok=True)` and `REPORTS_DIR.mkdir(parents=True, exist_ok=True)`. This is a side effect at import time, which violates the stated hard rule in the project's own `AGENTS.md`: "No side effects at import time unless explicitly justified." In practice, this means importing any module that transitively imports `estorides_core.config` will create filesystem directories — including in test environments, CI, linting, and any other context where directory creation is unexpected or undesired.

## Evidence
`estorides_core/config.py` lines 73–74:
```python
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
```

These lines execute unconditionally at import time. Every test in `_test_hardening.py`, `_test_ssrf.py`, etc. triggers these side effects. The `_test_hardening.py` test works around this by overriding `ESTORIDES_DATA_DIR` before import, but the override only works if the tests are written carefully — other test authors may not know to do this.

## Why this matters
1. **Import side effects**: Running `ruff check .`, `mypy`, or any other static analysis tool that imports the module will create directories on the filesystem.
2. **Test pollution**: Tests that don't override `ESTORIDES_DATA_DIR` write to the production `data/` directory, potentially corrupting the operator's cache or audit log.
3. **Principle of least surprise**: A developer who imports `from estorides_core.config import FLASK_PORT` to read a constant should not trigger filesystem mutations.

## Attack or failure scenario
1. A developer writes a new test: `from estorides_core.config import HTTP_TIMEOUT`.
2. The test runs in a CI environment where `estorides/data/` does not exist.
3. `DATA_DIR.mkdir()` creates the directory with default permissions (umask-dependent), which may be world-readable.
4. Subsequent CI steps write cache and audit data to this directory; the CI artifacts contain potentially sensitive investigation data.

## Root cause
The side effect was added for operational convenience (the application shouldn't crash on first run because `data/` doesn't exist). This is a legitimate concern but should be solved at application startup, not at module import time.

## Recommended fix
1. Remove the `mkdir` calls from module-level code.
2. Move directory initialisation to an explicit `ensure_dirs()` function:
   ```python
   def ensure_dirs() -> None:
       """Create runtime directories. Call once at application startup."""
       DATA_DIR.mkdir(parents=True, exist_ok=True)
       REPORTS_DIR.mkdir(parents=True, exist_ok=True)
   ```
3. Call `ensure_dirs()` from `wsgi.py` and `estorides_cli.py` startup, not from the config module.
4. Update `_test_hardening.py` and other tests to call `ensure_dirs()` explicitly if they need the directories.

## Acceptance criteria
- Importing `estorides_core.config` creates no filesystem directories.
- An explicit `ensure_dirs()` function is called at application entry points.
- All tests pass without requiring `ESTORIDES_DATA_DIR` to be set.
- A ruff rule or a test verifies no `mkdir` calls exist at module scope in `config.py`.

## Suggested labels
bug, architecture, technical-debt

## Priority
P3

## Severity
Medium — Import-time side effects violate the project's own stated hard rules and cause test pollution, but do not directly enable exploitation. Risk is elevated in shared CI environments.

## Confidence
Confirmed — the `mkdir` calls at module level are present at lines 73–74 of `estorides_core/config.py`.
