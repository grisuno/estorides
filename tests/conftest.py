"""Pytest configuration and shared fixtures for the estorides test suite."""
from __future__ import annotations

import sys
from pathlib import Path

# Make the project importable when running `pytest` from any cwd.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
