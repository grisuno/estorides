"""M6 RED tests: central config for orchestrator + tool_install."""
from __future__ import annotations

import inspect


def test_config_defaults() -> None:
    from estorides_core import config

    assert config.RUN_DEADLINE == 30.0
    assert config.LLM_BACKSTOP_S == 3.0
    assert config.TOOL_INSTALL_TIMEOUT_S == 1800
    assert config.TOOL_INSTALL_MAX_OUTPUT_BYTES == 1_048_576
    assert set(config.TEMPLATE_ENVS) >= {
        "TWITCH_CLIENT_ID", "GOOGLE_API_KEY",
        "TWITTER_BEARER_TOKEN", "TWITCH_ACCESS_TOKEN",
    }


def test_run_defaults_track_config() -> None:
    from estorides_core import config
    from estorides_core.orchestrator import Orchestrator

    sig = inspect.signature(Orchestrator.run)
    assert sig.parameters["timeout"].default == config.HTTP_TIMEOUT
    assert sig.parameters["deadline"].default == config.RUN_DEADLINE


def test_tool_install_survives_malformed_env(monkeypatch) -> None:
    import importlib

    monkeypatch.setenv("ESTORIDES_TOOL_INSTALL_TIMEOUT", "abc")
    monkeypatch.setenv("ESTORIDES_TOOL_INSTALL_MAX_OUTPUT", "zzz")
    import estorides_core.tool_install as ti

    importlib.reload(ti)
    assert ti._INSTALL_TIMEOUT_S == 1800
    assert ti._INSTALL_MAX_OUTPUT_BYTES == 1_048_576
    importlib.reload(ti)
