"""
BDD / regression tests for fault-tolerant configuration parsing.

Doctrine (`config.py` docstring): a malformed env var must fall back to the
default and log, never crash the process at import time. These tests pin that
contract for every typed reader and for the import-time constant surface.

  - CE1: typed readers parse valid values
  - CE2: a malformed value falls back to the default
  - CE3: a malformed env var cannot crash `import estorides_core.config`
  - CE4: CSV lists are whitespace-stripped
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_with_env(env_overrides: dict[str, str], code: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update(env_overrides)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(  # noqa: S603 - trusted interpreter, test-owned code
        [sys.executable, "-c", code],
        capture_output=True, text=True, env=env, cwd=str(REPO_ROOT), timeout=60,
    )


class TestCE1TypedReaders:
    def test_env_int_parses(self, monkeypatch) -> None:
        from estorides_core.config import _env_int

        monkeypatch.setenv("CE_INT_OK", "42")
        assert _env_int("CE_INT_OK", 1) == 42

    def test_env_float_parses(self, monkeypatch) -> None:
        from estorides_core.config import _env_float

        monkeypatch.setenv("CE_FLOAT_OK", "2.5")
        assert _env_float("CE_FLOAT_OK", 1.0) == 2.5


class TestCE2MalformedFallsBack:
    def test_env_int_garbage(self, monkeypatch) -> None:
        from estorides_core.config import _env_int

        monkeypatch.setenv("CE_INT_BAD", "not-a-number")
        assert _env_int("CE_INT_BAD", 7) == 7

    def test_env_float_garbage(self, monkeypatch) -> None:
        from estorides_core.config import _env_float

        monkeypatch.setenv("CE_FLOAT_BAD", "abc")
        assert _env_float("CE_FLOAT_BAD", 3.5) == 3.5

    def test_env_bool_unknown_uses_default(self, monkeypatch) -> None:
        from estorides_core.config import _env_bool

        monkeypatch.setenv("CE_BOOL_BAD", "maybe")
        assert _env_bool("CE_BOOL_BAD", True) is True
        assert _env_bool("CE_BOOL_BAD", False) is False

    def test_env_bool_tokens(self, monkeypatch) -> None:
        from estorides_core.config import _env_bool

        monkeypatch.setenv("CE_BOOL_ON", "yes")
        monkeypatch.setenv("CE_BOOL_OFF", "off")
        assert _env_bool("CE_BOOL_ON", False) is True
        assert _env_bool("CE_BOOL_OFF", True) is False


class TestCE3ImportNeverCrashes:
    def test_malformed_numeric_env_does_not_break_import(self) -> None:
        overrides = {
            "ESTORIDES_TIMEOUT": "abc",
            "ESTORIDES_MAX_RETRIES": "xyz",
            "ESTORIDES_TOOL_MAX_OUTPUT": "nope",
            "ESTORIDES_LLM_MAX_TOKENS": "??",
            "ESTORIDES_LLM_TEMP": "hot",
            "ESTORIDES_ENTITY_MAX_SCAN": "many",
            "ESTORIDES_KG_MAX_COOCCUR": "lots",
        }
        proc = _run_with_env(overrides, "import estorides_core.config; print('import-ok')")
        assert proc.returncode == 0, proc.stderr
        assert "import-ok" in proc.stdout


class TestCE4CsvStripped:
    def test_exact_dedup_keys_are_stripped(self) -> None:
        code = (
            "from estorides_core.config import RECON_FUSION as R;"
            "print(','.join(R.exact_dedup_keys))"
        )
        proc = _run_with_env(
            {"ESTORIDES_RF_DEDUP_KEYS": "source, parser , status"},
            code,
        )
        assert proc.returncode == 0, proc.stderr
        assert proc.stdout.strip() == "source,parser,status"
