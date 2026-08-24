"""
estorides_core.tool_install
===========================
One-click installation for missing Kali/OSINT CLI tools, modelled on the
LazyOwn lazyaddon mechanism (`lazyaddons/*.yaml`) and wired into the GUI's
results section: when a source fails with ``TOOL_NOT_FOUND`` the UI offers
an "Install tool" button that calls this module.

Each installable tool has a YAML recipe in ``tool_recipes/<name>.yaml`` with
the same shape as a LazyOwn lazyaddon:

    name: sherlock
    description: ...
    os: any
    apt: sherlock            # optional: Debian/Kali package name
    git:                     # optional: git + install_command fallback
      repo_url: https://github.com/sherlock-project/sherlock.git
      install_path: sherlock
      install_command: pip install -r requirements.txt

Install methods (tried in order when the binary is still missing):

  * ``apt`` — ``run0 apt-get update`` + ``run0 apt-get install -y <pkg>``.
  * ``git`` — ``git clone <repo_url> <install_path>`` (as the operator, no
    elevation) then ``<install_command>`` inside the clone (elevated only
    when it performs a system-wide install, e.g. ``pip install``).

Privilege elevation
-------------------
Estorides is a GUI app; user management should be graphical. The default
elevator is ``run0`` (systemd's polkit-aware runner) which pops a desktop
authentication prompt instead of demanding a terminal ``sudo`` password.
``sudo`` is used only as a fallback when ``run0`` is unavailable; if the
process is already root no elevator is used at all.

Safety (mirrors tool_runner): every subprocess runs as an argument list — the
trusted, operator-invoked ``install_command`` is shlex-split and executed
with no shell (shell=False), so a mangled recipe can never smuggle a
subcommand; the binary must still pass the allowlist; output is capped;
every run is time-boxed.
"""
from __future__ import annotations

import logging
import os
import re
import shlex
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

from .config import TOOL_ALLOWLIST, TOOL_RECIPES_DIR, TOOLS_DIR
from .tool_runner import ToolNotFoundError, _resolve_binary

log = logging.getLogger("estorides.tool_install")

_INSTALL_TIMEOUT_S: int = int(os.environ.get("ESTORIDES_TOOL_INSTALL_TIMEOUT", 1800))
_INSTALL_MAX_OUTPUT_BYTES: int = int(os.environ.get("ESTORIDES_TOOL_INSTALL_MAX_OUTPUT", 1_048_576))

# Verbatim command strings from trusted recipe YAML may carry shell syntax,
# but we run them as an argument list (shlex-split) and still refuse a few
# obviously hostile tokens so a mangled recipe can never smuggle a subcommand.
_INSTALL_SHELL_FORBIDDEN = re.compile(r";\s*\||\|\s*;|\brm\s+-rf\s+/|>\s*/dev/\w*|\$\{.*\}")

_INSTALL_VERBS = ("apt-get", "apt install", "dnf", "yum", "pip install", "gem install",
                  "npm install -g", "make install", "go install")


@dataclass(frozen=True)
class InstallRecipe:
    """One tool's install recipe, loaded from ``tool_recipes/<name>.yaml``.

    Mirrors the LazyOwn lazyaddon ``tool`` block. ``apt`` is tried first;
    ``git`` is the fallback. At least one of the two must be present.
    """

    name: str
    apt: str | None = None
    repo_url: str | None = None
    install_path: str | None = None
    install_command: str | None = None
    description: str = ""

    def has_apt(self) -> bool:
        return bool(self.apt)

    def has_git(self) -> bool:
        return bool(self.repo_url)


@dataclass(frozen=True)
class InstallResult:
    """Outcome of one ``install_tool`` invocation. Failures are values."""

    tool_name: str
    success: bool
    method: str | None
    output: str
    error: str | None = None
    duration_s: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _elevate(cmd: list[str]) -> list[str]:
    """Prepend an elevation wrapper when required.

    Priority: ``run0`` (graphical polkit prompt — the GUI-friendly default),
    then ``sudo``, then nothing when already root.
    """
    if os.geteuid() == 0:
        return cmd
    if shutil.which("run0"):
        return ["run0", *cmd]
    if shutil.which("sudo"):
        return ["sudo", *cmd]
    return cmd


def _run(cmd: list[str], *, cwd: Path | None = None) -> tuple[int, str, str]:
    """Run a subprocess as an argument list, capping output.

    Returns (exit_code, stdout, stderr). Never uses a shell: install
    commands are shlex-split by the caller and run argument-by-argument,
    so a mangled recipe cannot inject a subcommand.
    """
    proc = subprocess.run(  # noqa: S603
        cmd, shell=False, capture_output=True,  # nosec B603 - trusted recipe string, operator-invoked
        cwd=str(cwd) if cwd else None, timeout=_INSTALL_TIMEOUT_S, text=True,
    )
    out = (proc.stdout or "")[-_INSTALL_MAX_OUTPUT_BYTES:]
    err = (proc.stderr or "")[-_INSTALL_MAX_OUTPUT_BYTES:]
    return proc.returncode, out, err


def _check_shell_command(command: str) -> None:
    """Reject hostile tokens in a trusted recipe's install_command."""
    if _INSTALL_SHELL_FORBIDDEN.search(command):
        raise ValueError(f"install_command contains forbidden tokens: {command!r}")


def _needs_elevation(command: str) -> bool:
    """True when an install_command writes system-wide and needs root."""
    return any(verb in command for verb in _INSTALL_VERBS)


# ------------------------------------------------------------------ recipes ----
def _recipe_path(name: str) -> Path:
    return TOOL_RECIPES_DIR / f"{name}.yaml"


def load_recipe(name: str) -> InstallRecipe | None:
    """Load a tool recipe from ``tool_recipes/<name>.yaml`` (or ``None``).

    A malformed recipe is logged and treated as absent so one bad file can
    never break the whole registry.
    """
    path = _recipe_path(name)
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        log.warning("tool_install: bad recipe %s: %s", path, exc)
        return None
    if not isinstance(data, dict):
        return None
    git = data.get("git") or {}
    if not isinstance(git, dict):
        git = {}
    recipe = InstallRecipe(
        name=str(data.get("name") or name),
        apt=str(data["apt"]) if data.get("apt") else None,
        repo_url=str(git["repo_url"]) if git.get("repo_url") else None,
        install_path=str(git["install_path"]) if git.get("install_path") else None,
        install_command=str(git["install_command"]) if git.get("install_command") else None,
        description=str(data.get("description") or ""),
    )
    if not recipe.has_apt() and not recipe.has_git():
        log.warning("tool_install: recipe %s has neither apt nor git", name)
        return None
    return recipe


def recipe_available(name: str) -> bool:
    """True when a recipe exists for ``name`` (the UI gates the button on this)."""
    return load_recipe(name) is not None


def tool_available(binary: str) -> bool:
    """True when the binary resolves on PATH (mirrors system_app_sources)."""
    try:
        _resolve_binary(binary)
        return True
    except ToolNotFoundError:
        return False


def list_recipes() -> list[str]:
    """Names of all tool recipe files in ``tool_recipes/`` (sorted)."""
    if not TOOL_RECIPES_DIR.is_dir():
        return []
    return sorted(p.stem for p in TOOL_RECIPES_DIR.glob("*.yaml"))


# ---------------------------------------------------------------- installers ----
def _install_apt(recipe: InstallRecipe) -> tuple[bool, str, str | None]:
    """Install an apt package via the elevation wrapper (run0/sudo)."""
    t0 = time.monotonic()
    code, out, err = _run(_elevate(["apt-get", "update", "-y"]))
    if code != 0:
        return False, f"apt-get update failed (exit {code})\n{err}", err.strip()
    code, out, err = _run(_elevate(["apt-get", "install", "-y", str(recipe.apt)]))
    log.info("tool_install: apt %s -> exit %d (%.1fs)", recipe.apt, code, time.monotonic() - t0)
    if code != 0:
        return False, f"apt-get install {recipe.apt} failed (exit {code})\n{err}", err.strip()
    return True, out, None


def _install_git(recipe: InstallRecipe) -> tuple[bool, str, str | None]:
    """Clone the repo (as operator) and run install_command (elevated if system-wide)."""
    t0 = time.monotonic()
    dest = (TOOLS_DIR / (recipe.install_path or recipe.name)).resolve()
    out = ""
    if dest.is_dir():
        log.info("tool_install: clone target already exists: %s (reusing)", dest)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        code, out, err = _run(["git", "clone", "--depth", "1", str(recipe.repo_url), str(dest)])
        if code != 0:
            return False, f"git clone failed (exit {code})\n{err}", err.strip()

    if not recipe.install_command:
        return True, out, None

    _check_shell_command(recipe.install_command)
    parts = shlex.split(recipe.install_command)
    if not parts:
        return False, "empty install_command", "empty install_command"
    if _needs_elevation(recipe.install_command):
        parts = _elevate(parts)
    code, out, err = _run(parts, cwd=dest)
    log.info("tool_install: git %s install_command -> exit %d (%.1fs)",
             recipe.name, code, time.monotonic() - t0)
    if code != 0:
        return False, f"install_command failed (exit {code})\n{err}", err.strip()
    return True, out, None


# ----------------------------------------------------------------- public ----
def install_tool(
    tool_name: str,
    *,
    binary: str | None = None,
    force: bool = False,
) -> InstallResult:
    """Install a missing tool from its recipe (if any).

    If ``binary`` is given (the executable name from ``meta.tool_binary``),
    the install is skipped when it already resolves on PATH unless ``force``.
    """
    t0 = time.monotonic()

    if binary is None:
        binary = tool_name
    if not force:
        try:
            _resolve_binary(binary)
            return InstallResult(
                tool_name=tool_name, success=True, method="none",
                output=f"tool '{binary}' is already installed",
                duration_s=time.monotonic() - t0,
            )
        except ToolNotFoundError:
            pass

    if binary not in TOOL_ALLOWLIST:
        return InstallResult(
            tool_name=tool_name, success=False, method=None,
            output="", error=f"tool '{binary}' not in allowlist",
            duration_s=time.monotonic() - t0,
        )

    recipe = load_recipe(tool_name)
    if recipe is None:
        return InstallResult(
            tool_name=tool_name, success=False, method=None,
            output="", error=f"no install recipe found for '{tool_name}'",
            duration_s=time.monotonic() - t0,
        )

    methods: list[tuple[str, Any]] = []
    if recipe.has_apt():
        methods.append(("apt", _install_apt))
    if recipe.has_git():
        methods.append(("git", _install_git))
    methods.append(("verify", lambda r: _verify(binary)))

    for method, fn in methods:
        if method == "verify":
            ok, _output, err = fn(recipe)
            if ok:
                return InstallResult(
                    tool_name=tool_name, success=True, method="verify",
                    output=f"'{binary}' is now on PATH", duration_s=time.monotonic() - t0,
                )
            return InstallResult(
                tool_name=tool_name, success=False, method=None,
                output="", error=err or f"'{binary}' still not found after install",
                duration_s=time.monotonic() - t0,
            )
        try:
            ok, _output, err = fn(recipe)
        except Exception as exc:
            log.warning("tool_install: %s method %s failed: %s", tool_name, method, exc)
            continue
        if ok:
            log.info("tool_install: %s installed via %s", tool_name, method)
        # fall through to next method if this one didn't succeed

    return InstallResult(
        tool_name=tool_name, success=False, method=None,
        output="", error=f"all install methods failed for '{tool_name}'",
        duration_s=time.monotonic() - t0,
    )


def _verify(binary: str) -> tuple[bool, str, str | None]:
    """Post-install check: can the binary now be resolved?"""
    try:
        path = _resolve_binary(binary)
        return True, f"resolved {path}", None
    except ToolNotFoundError as exc:
        return False, "", str(exc)


# ------------------------------------------------------------------- cli ----
def main(argv: list[str] | None = None) -> int:
    """Minimal CLI: ``python -m estorides_core.tool_install <tool> [--force]``."""
    import argparse

    parser = argparse.ArgumentParser(prog="estorides-tool-install")
    parser.add_argument("tool")
    parser.add_argument("--binary")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--list", action="store_true", help="list recipe names")
    args = parser.parse_args(argv)

    if args.list:
        for name in list_recipes():
            print(name)
        return 0

    result = install_tool(args.tool, binary=args.binary, force=args.force)
    print(f"[{'OK' if result.success else 'FAIL'}] {args.tool} ({result.method or 'none'})")
    if result.output:
        print(result.output[-2000:])
    if result.error:
        print("ERROR:", result.error)
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
