"""
estorides_core.envutil
======================
Fault-tolerant environment readers.

`config`, `web_security` and `source_health_monitoring` each carried their
own `_env_int` / `_env_float` / `_env_bool`. This module is the single
implementation: a malformed value falls back to the default and logs, it
never crashes the process at import time.
"""
from __future__ import annotations

import logging
import os

log = logging.getLogger("estorides.env")

_TRUE_TOKENS = frozenset(("1", "true", "yes", "on"))
_FALSE_TOKENS = frozenset(("0", "false", "no", "off"))


def env_int(name: str, default: int) -> int:
    """Read an int env var, falling back to `default` on absence/parse error."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        log.warning("env %s=%r is not an int, using default %d", name, raw, default)
        return default


def env_float(name: str, default: float) -> float:
    """Read a float env var, falling back to `default` on absence/parse error."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        log.warning("env %s=%r is not a float, using default %s", name, raw, default)
        return default


def env_bool(name: str, default: bool) -> bool:
    """Read a boolean env var. Truthy: 1/true/yes/on. Unknown -> default."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    token = raw.strip().lower()
    if token in _TRUE_TOKENS:
        return True
    if token in _FALSE_TOKENS:
        return False
    log.warning("env %s=%r is not a boolean, using default %s", name, raw, default)
    return default


def env_csv(name: str, default: tuple[str, ...] = ()) -> tuple[str, ...]:
    """Read a comma-separated env var, stripping blanks; never raises."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    return tuple(t.strip() for t in raw.split(",") if t.strip())


__all__ = ["env_bool", "env_csv", "env_float", "env_int"]
