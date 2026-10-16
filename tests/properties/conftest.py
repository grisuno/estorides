"""Directory guard for property-based (hypothesis) tests.

``hypothesis`` is a dev-only extra (``pip install -e ".[dev]"``; CI installs
it). Generic runners such as ``deploynator release`` (``python -m pytest
tests/ -q`` with the system interpreter) only have runtime deps, so a hard
``from hypothesis import ...`` at module top turns into 13 collection
*errors* that abort the whole deploy gate.

When the extra is missing (or broken: e.g. a leftover directory without
``__init__`` that imports as an empty namespace package) the property files
are excluded from collection (``collect_ignore_glob`` — the pytest-native
mechanism for this); when it is installed (CI / ``.[dev]``) this file is a
no-op and the full fuzz matrix runs. ``pytest.importorskip`` cannot be used
here: raised inside a conftest it surfaces as a collection *error*, not a
skip.
"""
from __future__ import annotations

try:
    from hypothesis import given  # noqa: F401
except ImportError:
    collect_ignore_glob = ["test_*_properties.py"]
