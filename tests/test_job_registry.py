"""BoundedJobRegistry: size cap + TTL eviction (issues #14, #20, #50)."""
from __future__ import annotations

import time

import pytest

from estorides_core.job_registry import BoundedJobRegistry


def test_register_returns_value():
    r = BoundedJobRegistry[str](max_size=2, ttl_seconds=60)
    assert r.register("a", "value-a") == "value-a"
    assert r.get("a") == "value-a"


def test_size_cap_evicts_oldest():
    r = BoundedJobRegistry[str](max_size=2, ttl_seconds=60)
    r.register("a", "A")
    r.register("b", "B")
    r.register("c", "C")
    assert len(r) == 2
    assert r.get("a") is None  # oldest evicted
    assert r.get("b") == "B"
    assert r.get("c") == "C"


def test_get_refreshes_lru_order():
    r = BoundedJobRegistry[str](max_size=2, ttl_seconds=60)
    r.register("a", "A")
    r.register("b", "B")
    # Touch 'a' so it becomes the most-recently-used.
    assert r.get("a") == "A"
    r.register("c", "C")
    assert r.get("a") == "A"
    assert r.get("b") is None  # 'b' was oldest at insert of 'c'


def test_ttl_eviction():
    r = BoundedJobRegistry[str](max_size=10, ttl_seconds=0.05)
    r.register("a", "A")
    time.sleep(0.06)
    # `get` evicts on read; `evict_expired` is the bulk path that
    # doesn't return values. After the TTL has passed, both should
    # see the entry as gone.
    assert r.get("a") is None
    # Re-register a fresh entry and verify that the now-empty
    # registry reports 0 expired on a subsequent sweep.
    r.register("b", "B")
    assert r.evict_expired() == 0


def test_pop_removes_entry():
    r = BoundedJobRegistry[str](max_size=2, ttl_seconds=60)
    r.register("a", "A")
    assert r.pop("a") == "A"
    assert r.get("a") is None
    assert r.pop("missing") is None


def test_keys_values_consistent():
    r = BoundedJobRegistry[str](max_size=2, ttl_seconds=60)
    r.register("a", "A")
    r.register("b", "B")
    assert set(r.keys()) == {"a", "b"}
    assert set(r.values()) == {"A", "B"}


def test_invalid_construction():
    with pytest.raises(ValueError):
        BoundedJobRegistry(max_size=0, ttl_seconds=60)
    with pytest.raises(ValueError):
        BoundedJobRegistry(max_size=2, ttl_seconds=0)


def test_replacement_does_not_evict():
    """Re-registering the same key keeps the size stable and LRU order intact."""
    r = BoundedJobRegistry[str](max_size=2, ttl_seconds=60)
    r.register("a", "A1")
    r.register("b", "B")
    r.register("a", "A2")  # replace, not insert
    assert len(r) == 2
    assert r.get("a") == "A2"
    assert r.get("b") == "B"
