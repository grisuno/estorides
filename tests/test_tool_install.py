"""Tests for estorides_core.tool_install (lazyaddon-style tool installation).

Covers recipe loading, elevation choice (run0 preferred over sudo, none when
root), apt vs git install methods, and the TOOL_NOT_FOUND install flow.
All subprocess calls are mocked so no network or root access is required.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

import estorides_core.tool_install as ti


@pytest.fixture
def no_network() -> None:
    """Make every _run call a no-op success so tests never touch the network."""
    with patch.object(ti, "_run", return_value=(0, "mock-out", "")):
        yield


# ------------------------------------------------------------------- recipes ----
class TestRecipes:
    def test_recipe_available_for_known_tool(self) -> None:
        assert ti.recipe_available("nmap") is True

    def test_recipe_unavailable_for_unknown_tool(self) -> None:
        assert ti.recipe_available("no_such_tool_xyz") is False

    def test_load_apt_recipe(self) -> None:
        r = ti.load_recipe("nmap")
        assert r is not None and r.apt == "nmap"

    def test_load_git_recipe(self) -> None:
        r = ti.load_recipe("sherlock")
        assert r is not None and r.repo_url is not None

    def test_list_recipes_is_nonempty(self) -> None:
        assert "nmap" in ti.list_recipes()


# ------------------------------------------------------------------ elevation ----
class TestElevation:
    def test_run0_preferred_over_sudo(self) -> None:
        with patch.object(ti.shutil, "which", side_effect=lambda name: {"run0": "/run/run0", "sudo": "/usr/bin/sudo"}[name]):
            with patch.object(ti.os, "geteuid", return_value=1000):
                assert ti._elevate(["apt-get", "install"]) == ["run0", "apt-get", "install"]

    def test_sudo_fallback_when_no_run0(self) -> None:
        with patch.object(ti.shutil, "which", side_effect=lambda name: "/usr/bin/sudo" if name == "sudo" else None):
            with patch.object(ti.os, "geteuid", return_value=1000):
                assert ti._elevate(["apt-get", "install"]) == ["sudo", "apt-get", "install"]

    def test_no_elevation_when_root(self) -> None:
        with patch.object(ti.os, "geteuid", return_value=0):
            assert ti._elevate(["apt-get", "install"]) == ["apt-get", "install"]


# ------------------------------------------------------------------- install ----
class TestInstallFlow:
    def test_already_installed_noop(self, no_network) -> None:
        with patch.object(ti, "_resolve_binary", return_value="/usr/bin/file"):
            res = ti.install_tool("file", binary="file")
        assert res.success is True and res.method == "none"

    def test_not_in_allowlist_rejected(self) -> None:
        with patch.object(ti, "_resolve_binary", side_effect=ti.ToolNotFoundError("missing")):
            res = ti.install_tool("evil_tool", binary="evil_tool")
        assert res.success is False and "allowlist" in (res.error or "")

    def test_no_recipe_rejected(self) -> None:
        # pyinstaller is in the allowlist but has no tool_recipes/*.yaml.
        with patch.object(ti, "_resolve_binary", side_effect=ti.ToolNotFoundError("missing")):
            res = ti.install_tool("pyinstaller", binary="pyinstaller")
        assert res.success is False and "no install recipe" in (res.error or "")

    def test_apt_install_success(self) -> None:
        missing = ti.ToolNotFoundError("missing")
        with patch.object(ti, "_resolve_binary", side_effect=[missing, "/usr/bin/nmap"]) as rb:
            with patch.object(ti, "_run", return_value=(0, "ok", "")) as mock_run:
                with patch.object(ti, "_elevate", side_effect=lambda cmd: ["run0", *cmd]):
                    res = ti.install_tool("nmap", binary="nmap")
        assert res.success is True and res.method == "verify"
        assert rb.call_count == 2  # initial availability check + post-install verify
        apt_calls = [c for c in mock_run.call_args_list if "apt-get" in str(c)]
        assert apt_calls, "apt-get install should have been attempted"

    def test_verify_fails_after_install(self, no_network) -> None:
        with patch.object(ti, "_resolve_binary", side_effect=ti.ToolNotFoundError("missing")):
            with patch.object(ti, "_verify", return_value=(False, "", "still missing")):
                res = ti.install_tool("nmap", binary="nmap")
        assert res.success is False

    def test_git_install_runs_clone(self) -> None:
        with patch.object(ti, "_resolve_binary", side_effect=ti.ToolNotFoundError("missing")):
            with patch.object(ti, "_verify", return_value=(True, "found", None)):
                with patch.object(ti, "_run", return_value=(0, "", "")) as mock_run:
                    with patch.object(ti, "_elevate", side_effect=lambda cmd: cmd):
                        res = ti.install_tool("sherlock", binary="sherlock")
        assert res.success is True
        assert any("git" in str(c) and "clone" in str(c) for c in mock_run.call_args_list)
