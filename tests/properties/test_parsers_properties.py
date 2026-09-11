"""
Property-based fuzzing for the parser totality contract (doctrine §6).

Every registered parser must be total: any JSON-shaped input returns a
value instead of raising. We fuzz all 75 parsers with arbitrary nested
primitives, lists and dicts (1000 examples per property).
"""
from __future__ import annotations

from typing import Any

from hypothesis import given, settings
from hypothesis import strategies as st

from estorides_core.parsers import PARSERS

JSON_SCALARS = st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text()
JSON_VALUES = st.recursive(
    JSON_SCALARS,
    lambda children: st.lists(children, max_size=5)
    | st.dictionaries(st.text(max_size=8), children, max_size=5),
    max_leaves=25,
)

# Normalize registry entries: values may be a callable or (callable, desc).
_PARSER_FUNCS = [
    spec[0] if isinstance(spec, tuple) else spec
    for spec in PARSERS.values()
    if callable(spec) or (isinstance(spec, tuple) and spec and callable(spec[0]))
]


@settings(max_examples=1000, deadline=None)
@given(payload=JSON_VALUES)
def test_all_parsers_are_total(payload: Any) -> None:
    for fn in _PARSER_FUNCS:
        fn(payload)  # must not raise for any JSON-shaped input
