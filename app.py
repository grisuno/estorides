#!/usr/bin/env python3
"""
Deprecated entry point. Use:

  - the `estorides` console script (installed by `pip install -e .`), or
  - `python3 estorides_cli.py serve` for the dev server, or
  - `gunicorn -w 4 wsgi:app` for production.

This file is kept as a redirect so old launchers that import `app` from
this module keep working. It intentionally does NOT start a server on
import.
"""
from __future__ import annotations

import warnings as _warnings

_warnings.warn(
    "Importing 'app' from the project root is deprecated. "
    "Use 'wsgi:app' for gunicorn or 'estorides_cli.py serve' for the dev server.",
    DeprecationWarning,
    stacklevel=2,
)

from wsgi import app  # noqa: E402,F401  re-export for legacy launchers
