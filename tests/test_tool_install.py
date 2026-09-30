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


# ------------------------------------------------- path traversal (S20-S22) ----
class TestPathTraversal:
    """CodeQL #48/#49/#52: uncontrolled recipe names must never escape
    TOOL_RECIPES_DIR; clone targets must stay inside TOOLS_DIR; binary
    names are validated before any PATH probe. Only directory-listed
    recipe stems ever reach the filesystem."""

    def test_unknown_valid_name_never_touches_filesystem(self) -> None:
        with patch.object(ti, "_recipe_path",
                          side_effect=AssertionError("FS path must not be built")):
            assert ti.load_recipe("no-such-recipe-xyz") is None

    def test_install_tool_unknown_recipe_without_fs_probe(self) -> None:
        with patch.object(ti, "load_recipe",
                          side_effect=AssertionError("load_recipe must not be called")):
            res = ti.install_tool("no-such-recipe-xyz", binary="nmap", force=True)
        assert res.success is False and "no install recipe" in (res.error or "")

    @pytest.mark.parametrize("evil", [
        "../evil", "../../etc/cron", "a/b", "a\\b", "", ".", "..",
        "/abs/path", "x\x00y", "has space", "semi;colon", "a" * 200,
    ])
    def test_load_recipe_rejects_traversal(self, evil: str) -> None:
        assert ti.load_recipe(evil) is None

    def test_recipe_path_rejects_traversal(self) -> None:
        with pytest.raises(ValueError):
            ti._recipe_path("../../etc/cron")

    def test_recipe_available_rejects_traversal(self) -> None:
        assert ti.recipe_available("../evil") is False

    def test_git_clone_refuses_escape(self) -> None:
        recipe = ti.InstallRecipe(
            name="evil", repo_url="https://example.com/r.git",
            install_path="../../evil",
        )
        with patch.object(ti, "_run") as mock_run:
            ok, _out, err = ti._install_git(recipe)
        assert ok is False
        assert "tools dir" in (err or "").lower()
        mock_run.assert_not_called()

    @pytest.mark.parametrize("evil", ["/bin/sh", "../../bin/x", "a/b", "", "has space"])
    def test_install_tool_rejects_bad_binary_without_path_probe(
        self, evil: str
    ) -> None:
        with patch.object(
            ti, "_resolve_binary",
            side_effect=AssertionError("_resolve_binary must not be called"),
        ):
            res = ti.install_tool("nmap", binary=evil)
        assert res.success is False

    def test_install_tool_allowlist_checked_before_shortcut(self) -> None:
        # binary resolves on PATH but is NOT allowlisted: must still fail.
        with patch.object(ti, "_resolve_binary", return_value="/usr/bin/notallowed"):
            res = ti.install_tool("notallowed", binary="notallowed")
        assert res.success is False and "allowlist" in (res.error or "")

    def test_tool_available_rejects_bad_name(self) -> None:
        assert ti.tool_available("/bin/sh") is False
        assert ti.tool_available("../x") is False
