"""
_test_fusion
============
Tests for the cross-run fusion datastore (estorides_core.fusion_store).

Covers the properties that make it a *fusion* store rather than a per-run
log: deterministic cross-run entity identity, source provenance that
survives a merge, property corroboration with conflicting values preserved,
relationship fusion, and the fail-soft open_store contract.

Run standalone:  python3 _test_fusion.py
"""
from __future__ import annotations

import os
import sys
import tempfile

from estorides_core.fusion_store import FusionStore, entity_id, open_store

_failures = 0


def check(label: str, cond: bool) -> None:
    global _failures
    status = "PASS" if cond else "FAIL"
    if not cond:
        _failures += 1
    print(f"[{status}] {label}")


def _fresh_store() -> FusionStore:
    path = os.path.join(tempfile.mkdtemp(prefix="estorides_fusion_"), "fusion.sqlite")
    return FusionStore(path)


def test_deterministic_identity() -> None:
    a = entity_id("ipv4", "8.8.8.8")
    b = entity_id("ipv4", "8.8.8.8")
    c = entity_id("ipv4", "1.1.1.1")
    check("same entity hashes to same id across calls (cross-run dedup)", a == b)
    check("different entities hash to different ids", a != c)


def test_cross_run_dedup_and_provenance() -> None:
    fs = _fresh_store()
    # Two independent "runs" observe the same IP through different feeds.
    fs.fuse_entity({"type": "ipv4", "value": "8.8.8.8", "sources": ["ipapi_free"]})
    fs.fuse_entity({"type": "ipv4", "value": "8.8.8.8", "sources": ["shodan_internetdb"]})
    stats = fs.stats()
    check("two sightings fuse into one canonical entity", stats["entities"] == 1)
    eid = entity_id("ipv4", "8.8.8.8")
    ent = fs.get_entity(eid)
    check("both feeds retained as provenance", ent is not None and ent["source_count"] == 2)
    names = {s["source"] for s in ent["sources"]}
    check("provenance lists every contributing source", names == {"ipapi_free", "shodan_internetdb"})


def test_property_corroboration_and_conflict() -> None:
    fs = _fresh_store()
    eid = fs.fuse_entity({"type": "ipv4", "value": "1.1.1.1", "sources": ["a"]})
    fs.fuse_properties(eid, {"country": "Australia", "asn": 13335}, "source_a")
    fs.fuse_properties(eid, {"country": "Australia"}, "source_b")
    fs.fuse_properties(eid, {"country": "USA"}, "source_c")
    corro = fs.corroborated_properties(eid, min_sources=2)
    agreed = {(c["key"], c["value"]) for c in corro}
    check("agreed property surfaces as corroborated", ("country", "Australia") in agreed)
    check("single-source conflicting value not corroborated",
          ("country", "USA") not in agreed)
    full = fs.get_entity(eid)
    values = {(p["key"], p["value"]) for p in full["properties"]}
    check("conflicting value preserved with its provenance, not dropped",
          ("country", "USA") in values and ("country", "Australia") in values)


def test_min_sources_filter() -> None:
    fs = _fresh_store()
    fs.fuse_entity({"type": "domain", "value": "solo.example", "sources": ["one"]})
    fs.fuse_entity({"type": "domain", "value": "many.example", "sources": ["one"]})
    fs.fuse_entity({"type": "domain", "value": "many.example", "sources": ["two"]})
    multi = fs.search_entities(min_sources=2)
    vals = {e["value"] for e in multi}
    check("min_sources filter keeps multi-source entity", "many.example" in vals)
    check("min_sources filter drops single-source entity", "solo.example" not in vals)


def test_relationship_fusion() -> None:
    fs = _fresh_store()
    fs.fuse_relationship("ipv4", "1.1.1.1", "hosted_by", "asn", "AS13335", source="bgp")
    fs.fuse_relationship("ipv4", "1.1.1.1", "hosted_by", "asn", "AS13335", source="bgp")
    check("repeated identical edge is idempotent", fs.stats()["relationships"] == 1)
    ent = fs.get_entity(entity_id("ipv4", "1.1.1.1"))
    check("edge is retrievable from its source endpoint",
          ent is not None and len(ent["relationships"]) == 1)


def test_observation_and_source_counters() -> None:
    fs = _fresh_store()
    fs.register_sources([{"name": "ipapi_free", "category": "ip", "parser": "ipapi"}])
    fs.add_observation(
        {"source": "ipapi_free", "category": "ip", "parser": "ipapi",
         "parsed": {"country": "US"}, "meta": {"status": 200}},
        query="8.8.8.8", query_type="ipv4",
    )
    fs.add_observation(
        {"source": "ipapi_free", "category": "ip", "parser": "ipapi",
         "parsed": None, "raw": None, "meta": {"status": "error"}},
        query="bad", query_type="ipv4",
    )
    srcs = {s["name"]: s for s in fs.list_sources()}
    check("source fetch counter accumulates", srcs["ipapi_free"]["fetch_count"] == 2)
    check("source ok counter counts only successful fetches", srcs["ipapi_free"]["ok_count"] == 1)
    check("both observations recorded", fs.stats()["observations"] == 2)


def test_fail_soft_open() -> None:
    # A path under a file (not a directory) cannot host a SQLite DB; open_store
    # must return None rather than raise so a run degrades to "no fusion".
    with tempfile.NamedTemporaryFile() as f:
        bad = open_store(os.path.join(f.name, "nope", "fusion.sqlite"))
    check("open_store fails soft to None on an unusable path", bad is None)


def main() -> int:
    for fn in (
        test_deterministic_identity,
        test_cross_run_dedup_and_provenance,
        test_property_corroboration_and_conflict,
        test_min_sources_filter,
        test_relationship_fusion,
        test_observation_and_source_counters,
        test_fail_soft_open,
    ):
        fn()
    print()
    if _failures:
        print(f"{_failures} FAIL")
        return 1
    print("all fusion tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
