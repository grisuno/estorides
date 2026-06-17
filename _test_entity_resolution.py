#!/usr/bin/env python3
"""Tests for the canonical identity layer (entity resolution).

Offline only. Covers cross-script transliteration, deterministic vs
probabilistic merge policy, blocking-driven link candidates, organisation
suffix folding, and cross-run id stability via a temporary store. Prints
PASS/FAIL and exits non-zero on any failure.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from estorides_core.entity_extraction import Entity
from estorides_core.entity_resolution import (CanonicalEntity, EntityResolver,
                                              canonical_id, jaro_winkler,
                                              normalize_value, resolve_entities,
                                              score_pair)
from estorides_core.entity_store import EntityStore
from estorides_core.transliteration import (consonant_skeleton, is_non_latin,
                                            to_latin)

_failures = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global _failures
    if cond:
        print(f"PASS: {name}")
    else:
        _failures += 1
        print(f"FAIL: {name} {detail}")


def _ent(etype: str, value: str, source: str) -> Entity:
    return Entity(type=etype, value=value, source=source, sources=[source])


def _by_value(result, value: str):
    for ce in result.entities:
        if ce.value == value or value in ce.aliases:
            return ce
    return None


def test_transliteration() -> None:
    check("cyrillic to latin", to_latin("Владимир") == "vladimir",
          to_latin("Владимир"))
    check("greek accented to latin", to_latin("Αλέξανδρος") == "alexandros",
          to_latin("Αλέξανδρος"))
    check("diacritic fold", to_latin("Müller") == "muller", to_latin("Müller"))
    check("arabic to latin skeleton matches vowelled latin",
          consonant_skeleton("محمد") == consonant_skeleton("Muhammad"),
          f'{consonant_skeleton("محمد")} vs {consonant_skeleton("Muhammad")}')
    check("gemination collapses in skeleton",
          consonant_skeleton("Muhammad") == "mhmd", consonant_skeleton("Muhammad"))
    check("distinct names keep distinct skeletons",
          consonant_skeleton("Apple") != consonant_skeleton("Apex"))
    check("non-latin detector", is_non_latin("Путин") and not is_non_latin("Putin"))


def test_jaro_winkler() -> None:
    check("identical strings score 1.0", jaro_winkler("martha", "martha") == 1.0)
    check("empty pair scores 0.0", jaro_winkler("", "abc") == 0.0)
    check("classic jaro-winkler bound", 0.95 <= jaro_winkler("martha", "marhta") <= 0.97,
          f'{jaro_winkler("martha", "marhta"):.4f}')
    check("dissimilar strings score low", jaro_winkler("apple", "orange") < 0.6)
    check("scores stay in unit interval",
          all(0.0 <= jaro_winkler(a, b) <= 1.0 for a, b in
              [("a", "b"), ("abcd", "abcd"), ("xy", "yx"), ("longword", "lon")]))


def test_normalization() -> None:
    check("ipv4 normalised", normalize_value("ipv4", "8.8.8.8") == "8.8.8.8")
    check("ipv6 compressed", normalize_value(
        "ipv6", "2001:0db8:0000:0000:0000:0000:0000:0001") == "2001:db8::1",
        normalize_value("ipv6", "2001:0db8:0000:0000:0000:0000:0000:0001"))
    check("ambiguous leading-zero ip left intact (no ssrf-style coercion)",
          normalize_value("ipv4", "08.8.8.008") == "08.8.8.008",
          normalize_value("ipv4", "08.8.8.008"))
    check("hash lowercased", normalize_value("md5", "D41D8CD98F00B204E9800998ECF8427E")
          == "d41d8cd98f00b204e9800998ecf8427e")
    check("cve upper", normalize_value("cve", "cve-2021-44228") == "CVE-2021-44228")
    check("domain strips scheme/www/path",
          normalize_value("domain", "HTTPS://www.Example.com/path?q=1") == "example.com",
          normalize_value("domain", "HTTPS://www.Example.com/path?q=1"))
    check("person order-independent",
          normalize_value("person", "Putin, Vladimir") == normalize_value("person", "Vladimir Putin"))
    check("org suffix stripped",
          normalize_value("org", "Evil Corp LLC") == normalize_value("org", "Evil Corp"))
    check("stable id is deterministic",
          canonical_id("person", "putin vladimir") == canonical_id("person", "putin vladimir"))
    check("different normalised yields different id",
          canonical_id("person", "putin vladimir") != canonical_id("person", "medvedev dmitry"))


def test_score_pair_policy() -> None:
    md5_a = "d41d8cd98f00b204e9800998ecf8427e"
    md5_b = "d41d8cd98f00b204e9800998ecf8427f"
    na = normalize_value("md5", md5_a)
    nb = normalize_value("md5", md5_b)
    check("deterministic near-miss never matches",
          score_pair("md5", md5_a, md5_b, na, nb).score == 0.0)
    pa, pb = "Vladimir Putin", "Владимир Путин"
    check("cross-script person clears merge bar",
          score_pair("person", pa, pb, normalize_value("person", pa),
                     normalize_value("person", pb)).score >= 0.92)


def test_resolution_merge() -> None:
    ents = [
        _ent("person", "Vladimir Putin", "wikidata"),
        _ent("person", "Владимир Путин", "ofac"),
        _ent("person", "Putin, Vladimir", "leak_db"),
        _ent("person", "Dmitry Medvedev", "news"),
        _ent("domain", "evilcorp.com", "crtsh"),
        _ent("domain", "EvilCorp.com", "urlscan"),
        _ent("domain", "evil-corp.com", "wayback"),
        _ent("domain", "apple.com", "dns"),
        _ent("ipv4", "8.8.8.8", "ipapi"),
        _ent("ipv4", "8.8.8.8", "shodan"),
        _ent("ipv4", "8.8.4.4", "greynoise"),
        _ent("org", "Evil Corp LLC", "opencorp"),
        _ent("org", "Evil Corp", "news"),
    ]
    res = resolve_entities(ents)

    putin = _by_value(res, "Vladimir Putin")
    check("three putin spellings fuse into one identity",
          putin is not None and putin.member_count == 3,
          f"member_count={getattr(putin, 'member_count', None)}")
    check("fused identity carries all three sources",
          putin is not None and len(putin.sources) == 3)
    check("cross-script fusion is flagged",
          putin is not None and putin.attributes.get("cross_script") is True)
    check("distinct person is not absorbed",
          _by_value(res, "Dmitry Medvedev") is not None
          and _by_value(res, "Dmitry Medvedev").member_count == 1)

    evilcorp = _by_value(res, "evilcorp.com")
    check("domain case variant merges exactly",
          evilcorp is not None and evilcorp.member_count == 2,
          f"member_count={getattr(evilcorp, 'member_count', None)}")
    check("hyphen domain variant stays a separate identity",
          _by_value(res, "evil-corp.com") is not None
          and _by_value(res, "evil-corp.com").member_count == 1)
    check("look-alike domains surfaced as same_as link (not merged)",
          len(res.same_as) >= 1 and any(l.method == "jaro_winkler" for l in res.same_as))
    check("unrelated domain untouched",
          _by_value(res, "apple.com") is not None
          and _by_value(res, "apple.com").member_count == 1)

    check("identical ips merge",
          _by_value(res, "8.8.8.8") is not None
          and _by_value(res, "8.8.8.8").member_count == 2)
    check("near ips never fuse",
          _by_value(res, "8.8.4.4") is not None
          and _by_value(res, "8.8.4.4").member_count == 1)

    org = _by_value(res, "Evil Corp")
    check("org suffix variant folds into one identity",
          org is not None and org.member_count == 2,
          f"member_count={getattr(org, 'member_count', None)}")


def test_to_entity_roundtrip() -> None:
    res = resolve_entities([
        _ent("person", "Vladimir Putin", "wikidata"),
        _ent("person", "Владимир Путин", "ofac"),
    ])
    ce = res.entities[0]
    ent = ce.to_entity()
    check("canonical entity projects to legacy Entity",
          isinstance(ent, Entity) and ent.attributes.get("canonical_id") == ce.canonical_id)
    check("legacy projection serialises", isinstance(ent.to_dict(), dict)
          and ent.to_dict()["attributes"]["canonical_id"] == ce.canonical_id)
    check("canonical entity serialises", isinstance(ce.to_dict(), dict)
          and ce.to_dict()["canonical_id"] == ce.canonical_id)


def test_cross_run_stability() -> None:
    tmpdir = Path(tempfile.mkdtemp(prefix="estorides_er_"))
    store = EntityStore(tmpdir / "entities.sqlite")
    try:
        r1 = EntityResolver(store=store).resolve([_ent("person", "Vladimir Putin", "wikidata")])
        id1 = r1.entities[0].canonical_id

        r2 = EntityResolver(store=store).resolve([_ent("person", "Владимир Путин", "ofac")])
        id2 = r2.entities[0].canonical_id
        check("canonical id stable across runs and scripts", id1 == id2,
              f"{id1} vs {id2}")

        r3 = EntityResolver(store=store).resolve([_ent("person", "Putin, Vladimir", "leak")])
        check("never-before alias adopts existing id",
              r3.entities[0].canonical_id == id1)

        r4 = EntityResolver(store=store).resolve([_ent("person", "Dmitry Medvedev", "news")])
        check("different entity gets a different id",
              r4.entities[0].canonical_id != id1)

        stats = store.stats()
        check("store accumulates entities", stats["entities"] >= 2, str(stats))
    finally:
        store.close()
        for child in sorted(tmpdir.glob("*")):
            child.unlink()
        tmpdir.rmdir()


def test_empty_and_edge_inputs() -> None:
    check("empty input yields empty result", resolve_entities([]).entities == [])
    check("blank value does not crash",
          isinstance(resolve_entities([_ent("person", "", "src")]), object))
    weird = resolve_entities([_ent("keyword", "  ", "src")])
    check("whitespace-only handled", isinstance(weird.entities, list))


def main() -> int:
    test_transliteration()
    test_jaro_winkler()
    test_normalization()
    test_score_pair_policy()
    test_resolution_merge()
    test_to_entity_roundtrip()
    test_cross_run_stability()
    test_empty_and_edge_inputs()

    print(f"\n{'-' * 40}")
    if _failures:
        print(f"FAIL: {_failures} check(s) failed")
        return 1
    print("PASS: all entity-resolution checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
