"""
BDD tests for estorides_core.entity_resolution.

These tests implement the Given-When-Then contracts declared in
spec/entity_resolution.md. They must fail against the unwritten
implementation (red step) and pass after the green step.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from estorides_core.entity_extraction import Entity
from estorides_core.entity_resolution import (
    CanonicalEntity,
    EntityResolver,
    ResolutionResult,
    canonical_id,
    jaro_winkler,
    normalize_value,
    resolve_entities,
    score_pair,
)
from estorides_core.entity_store import EntityStore
from estorides_core.transliteration import consonant_skeleton, is_non_latin, to_latin


def _ent(etype: str, value: str, source: str, confidence: float = 1.0) -> Entity:
    return Entity(type=etype, value=value, source=source, sources=[source], confidence=confidence)


def _by_value(result: ResolutionResult, value: str) -> CanonicalEntity | None:
    for ce in result.entities:
        if ce.value == value or value in ce.aliases:
            return ce
    return None


# ---------------------------------------------------------------------------
# ER0 — Helper tests: transliteration, jaro-winkler, normalisation
# ---------------------------------------------------------------------------
class TestTransliteration:
    """Cyrillic, Greek, Arabic, diacritic folding."""

    def test_cyrillic_to_latin(self) -> None:
        assert to_latin("Владимир") == "vladimir"

    def test_greek_accented_to_latin(self) -> None:
        assert to_latin("Αλέξανδρος") == "alexandros"

    def test_diacritic_fold(self) -> None:
        assert to_latin("Müller") == "muller"

    def test_consonant_skeleton_arabic_matches_latin(self) -> None:
        assert consonant_skeleton("محمد") == consonant_skeleton("Muhammad")

    def test_consonant_skeleton_gemination(self) -> None:
        assert consonant_skeleton("Muhammad") == "mhmd"

    def test_distinct_names_have_distinct_skeletons(self) -> None:
        assert consonant_skeleton("Apple") != consonant_skeleton("Apex")

    def test_non_latin_detector(self) -> None:
        assert is_non_latin("Путин")
        assert not is_non_latin("Putin")


class TestJaroWinkler:
    """Jaro-Winkler similarity invariants."""

    def test_identical_strings_score_one(self) -> None:
        assert jaro_winkler("martha", "martha") == 1.0

    def test_empty_pair_scores_zero(self) -> None:
        assert jaro_winkler("", "abc") == 0.0

    def test_classic_jaro_winkler_bound(self) -> None:
        score = jaro_winkler("martha", "marhta")
        assert 0.95 <= score <= 0.97, f"score={score:.4f}"

    def test_dissimilar_strings_score_low(self) -> None:
        assert jaro_winkler("apple", "orange") < 0.6

    def test_scores_stay_in_unit_interval(self) -> None:
        for a, b in [("a", "b"), ("abcd", "abcd"), ("xy", "yx"), ("longword", "lon")]:
            assert 0.0 <= jaro_winkler(a, b) <= 1.0


class TestNormalization:
    """Type-aware normalisation."""

    def test_ipv4_normalised(self) -> None:
        assert normalize_value("ipv4", "8.8.8.8") == "8.8.8.8"

    def test_ipv6_compressed(self) -> None:
        assert (
            normalize_value("ipv6", "2001:0db8:0000:0000:0000:0000:0000:0001")
            == "2001:db8::1"
        )

    def test_hash_lowered(self) -> None:
        assert (
            normalize_value("md5", "D41D8CD98F00B204E9800998ECF8427E")
            == "d41d8cd98f00b204e9800998ecf8427e"
        )

    def test_cve_uppered(self) -> None:
        assert normalize_value("cve", "cve-2021-44228") == "CVE-2021-44228"

    def test_domain_strips_scheme_www_path(self) -> None:
        assert (
            normalize_value("domain", "HTTPS://www.Example.com/path?q=1")
            == "example.com"
        )

    def test_person_order_independent(self) -> None:
        assert normalize_value("person", "Putin, Vladimir") == normalize_value(
            "person", "Vladimir Putin"
        )

    def test_org_suffix_stripped(self) -> None:
        assert normalize_value("org", "Evil Corp LLC") == normalize_value(
            "org", "Evil Corp"
        )

    def test_asn_normalised(self) -> None:
        assert normalize_value("asn", "as12345") == "AS12345"

    def test_email_lowered(self) -> None:
        assert normalize_value("email", "User@Example.COM") == "user@example.com"


class TestCanonicalId:
    """Deterministic content-addressed ids."""

    def test_deterministic(self) -> None:
        assert canonical_id("person", "putin vladimir") == canonical_id(
            "person", "putin vladimir"
        )

    def test_different_values_different_ids(self) -> None:
        assert canonical_id("person", "putin vladimir") != canonical_id(
            "person", "medvedev dmitry"
        )

    def test_id_format(self) -> None:
        cid = canonical_id("person", "putin vladimir")
        assert cid.startswith("person:")
        assert len(cid) >= 17


# ---------------------------------------------------------------------------
# ER1 — Cross-script person fusion
# ---------------------------------------------------------------------------
class TestCrossScriptPersonFusion:
    """ER1: latin + cyrillic + comma-variant → one identity."""

    def test_three_spellings_fuse(self) -> None:
        ents = [
            _ent("person", "Vladimir Putin", "wikidata"),
            _ent("person", "Владимир Путин", "ofac"),
            _ent("person", "Putin, Vladimir", "leak_db"),
        ]
        res = resolve_entities(ents)
        putin = _by_value(res, "Vladimir Putin")
        assert putin is not None
        assert putin.member_count == 3

    def test_fused_identity_carries_all_sources(self) -> None:
        ents = [
            _ent("person", "Vladimir Putin", "wikidata"),
            _ent("person", "Владимир Путин", "ofac"),
            _ent("person", "Putin, Vladimir", "leak_db"),
        ]
        res = resolve_entities(ents)
        putin = _by_value(res, "Vladimir Putin")
        assert putin is not None
        assert len(putin.sources) == 3

    def test_cross_script_flagged_in_attributes(self) -> None:
        ents = [
            _ent("person", "Vladimir Putin", "wikidata"),
            _ent("person", "Владимир Путин", "ofac"),
        ]
        res = resolve_entities(ents)
        putin = _by_value(res, "Vladimir Putin")
        assert putin is not None
        assert putin.attributes.get("cross_script") is True


# ---------------------------------------------------------------------------
# ER2 — Domain case variant merges exactly
# ---------------------------------------------------------------------------
class TestDomainCaseVariantMerge:
    """ER2: EvilCorp.com and evilcorp.com → exact merge."""

    def test_domain_case_variants_merge(self) -> None:
        ents = [
            _ent("domain", "evilcorp.com", "crtsh"),
            _ent("domain", "EvilCorp.com", "urlscan"),
        ]
        res = resolve_entities(ents)
        merged = _by_value(res, "evilcorp.com")
        assert merged is not None
        assert merged.member_count == 2

    def test_domain_merge_is_exact(self) -> None:
        ents = [
            _ent("domain", "evilcorp.com", "crtsh"),
            _ent("domain", "EvilCorp.com", "urlscan"),
        ]
        res = resolve_entities(ents)
        merged = _by_value(res, "evilcorp.com")
        assert merged is not None
        assert merged.match_method == "exact"


# ---------------------------------------------------------------------------
# ER3 — Look-alike domains surface as SAME_AS
# ---------------------------------------------------------------------------
class TestLookAlikeDomainsSurfaceAsLink:
    """ER3: evilcorp.com vs evil-corp.com → SAME_AS link, not merged."""

    def test_look_alike_domains_stay_separate(self) -> None:
        ents = [
            _ent("domain", "evilcorp.com", "urlscan"),
            _ent("domain", "evil-corp.com", "wayback"),
        ]
        res = resolve_entities(ents)
        assert _by_value(res, "evilcorp.com") is not None
        assert _by_value(res, "evil-corp.com") is not None

    def test_look_alike_domains_produce_same_as_link(self) -> None:
        ents = [
            _ent("domain", "evilcorp.com", "urlscan"),
            _ent("domain", "evil-corp.com", "wayback"),
        ]
        res = resolve_entities(ents)
        assert len(res.same_as) >= 1
        assert any(link.method == "jaro_winkler" for link in res.same_as)


# ---------------------------------------------------------------------------
# ER4 — Deterministic type never fuzzy matches
# ---------------------------------------------------------------------------
class TestDeterministicTypeNoFuzzyMatch:
    """ER4: md5 differing by one char → separate entities."""

    def test_deterministic_near_miss_never_matches(self) -> None:
        md5_a = "d41d8cd98f00b204e9800998ecf8427e"
        md5_b = "d41d8cd98f00b204e9800998ecf8427f"
        ents = [
            _ent("md5", md5_a, "source_a"),
            _ent("md5", md5_b, "source_b"),
        ]
        res = resolve_entities(ents)
        assert len(res.entities) == 2

    def test_score_pair_deterministic_mismatch(self) -> None:
        md5_a = "d41d8cd98f00b204e9800998ecf8427e"
        md5_b = "d41d8cd98f00b204e9800998ecf8427f"
        na = normalize_value("md5", md5_a)
        nb = normalize_value("md5", md5_b)
        ms = score_pair("md5", md5_a, md5_b, na, nb)
        assert ms.score == 0.0
        assert ms.method == "deterministic_mismatch"


# ---------------------------------------------------------------------------
# ER5 — Identical IPs merge
# ---------------------------------------------------------------------------
class TestIdenticalIpsMerge:
    """ER5: same IP from two sources → merged."""

    def test_identical_ips_merge(self) -> None:
        ents = [
            _ent("ipv4", "8.8.8.8", "ipapi"),
            _ent("ipv4", "8.8.8.8", "shodan"),
        ]
        res = resolve_entities(ents)
        merged = _by_value(res, "8.8.8.8")
        assert merged is not None
        assert merged.member_count == 2


# ---------------------------------------------------------------------------
# ER6 — Near IPs never fuse
# ---------------------------------------------------------------------------
class TestNearIpsNeverFuse:
    """ER6: 8.8.8.8 and 8.8.4.4 → separate."""

    def test_near_ips_stay_separate(self) -> None:
        ents = [
            _ent("ipv4", "8.8.8.8", "ipapi"),
            _ent("ipv4", "8.8.4.4", "greynoise"),
        ]
        res = resolve_entities(ents)
        eight = _by_value(res, "8.8.8.8")
        four = _by_value(res, "8.8.4.4")
        assert eight is not None
        assert four is not None
        assert eight.member_count == 1
        assert four.member_count == 1


# ---------------------------------------------------------------------------
# ER7 — Org suffix folding
# ---------------------------------------------------------------------------
class TestOrgSuffixFolding:
    """ER7: Evil Corp LLC + Evil Corp → merged."""

    def test_org_suffix_variants_merge(self) -> None:
        ents = [
            _ent("org", "Evil Corp LLC", "opencorp"),
            _ent("org", "Evil Corp", "news"),
        ]
        res = resolve_entities(ents)
        org = _by_value(res, "Evil Corp")
        assert org is not None
        assert org.member_count == 2


# ---------------------------------------------------------------------------
# ER8 — Distinct persons stay separate
# ---------------------------------------------------------------------------
class TestDistinctPersonsStaySeparate:
    """ER8: Putin and Medvedev → separate identities."""

    def test_distinct_persons_not_absorbed(self) -> None:
        ents = [
            _ent("person", "Vladimir Putin", "wikidata"),
            _ent("person", "Dmitry Medvedev", "news"),
        ]
        res = resolve_entities(ents)
        putin = _by_value(res, "Vladimir Putin")
        medvedev = _by_value(res, "Dmitry Medvedev")
        assert putin is not None
        assert medvedev is not None
        assert putin.member_count == 1
        assert medvedev.member_count == 1
        assert putin.canonical_id != medvedev.canonical_id


# ---------------------------------------------------------------------------
# ER9 — Canonical entity to_dict / to_entity roundtrip
# ---------------------------------------------------------------------------
class TestCanonicalEntityRoundtrip:
    """ER9: to_dict and to_entity preserve data."""

    def test_to_dict_serialises(self) -> None:
        ents = [
            _ent("person", "Vladimir Putin", "wikidata"),
            _ent("person", "Владимир Путин", "ofac"),
        ]
        res = resolve_entities(ents)
        ce = res.entities[0]
        d = ce.to_dict()
        assert isinstance(d, dict)
        assert d["canonical_id"] == ce.canonical_id

    def test_to_entity_projects_legacy(self) -> None:
        ents = [
            _ent("person", "Vladimir Putin", "wikidata"),
            _ent("person", "Владимир Путин", "ofac"),
        ]
        res = resolve_entities(ents)
        ce = res.entities[0]
        ent = ce.to_entity()
        assert isinstance(ent, Entity)
        assert ent.attributes.get("canonical_id") == ce.canonical_id
        assert ent.attributes.get("member_count") == 2

    def test_resolution_result_has_one_entity(self) -> None:
        res = resolve_entities([_ent("person", "Vladimir Putin", "wikidata")])
        assert len(res.entities) == 1
        assert isinstance(res.entities[0], CanonicalEntity)


# ---------------------------------------------------------------------------
# ER10 — Empty input returns empty
# ---------------------------------------------------------------------------
class TestEmptyInput:
    """ER10: empty list → empty result."""

    def test_empty_input_returns_empty(self) -> None:
        res = resolve_entities([])
        assert res.entities == []
        assert res.same_as == []


# ---------------------------------------------------------------------------
# ER11 — Canonical id deterministic
# ---------------------------------------------------------------------------
class TestCanonicalIdDeterministic:
    """ER11: same input → same id."""

    def test_same_normalised_same_id(self) -> None:
        a = canonical_id("person", "putin vladimir")
        b = canonical_id("person", "putin vladimir")
        assert a == b


# ---------------------------------------------------------------------------
# ER12 — Different normalised yields different id
# ---------------------------------------------------------------------------
class TestDifferentInputDifferentId:
    """ER12: different input → different id."""

    def test_different_normalised_different_id(self) -> None:
        a = canonical_id("person", "putin vladimir")
        b = canonical_id("person", "medvedev dmitry")
        assert a != b


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    """Additional edge cases beyond the spec scenarios."""

    def test_blank_value_does_not_crash(self) -> None:
        res = resolve_entities([_ent("person", "", "src")])
        assert isinstance(res, ResolutionResult)

    def test_whitespace_only_handled(self) -> None:
        res = resolve_entities([_ent("keyword", "  ", "src")])
        assert isinstance(res.entities, list)

    def test_single_entity_produces_one_canonical(self) -> None:
        res = resolve_entities([_ent("domain", "example.com", "dns")])
        assert len(res.entities) == 1
        assert res.entities[0].member_count == 1

    def test_confidence_boosted_by_multiple_sources(self) -> None:
        ents = [
            _ent("person", "Vladimir Putin", "wikidata", 0.6),
            _ent("person", "Владимир Путин", "ofac", 0.5),
        ]
        res = resolve_entities(ents)
        putin = _by_value(res, "Vladimir Putin")
        assert putin is not None
        assert putin.confidence >= 0.5


# ---------------------------------------------------------------------------
# Cross-run stability via EntityStore (integration)
# ---------------------------------------------------------------------------
class TestCrossRunStability:
    """Canonical id stays stable across runs via persistent store."""

    def test_cross_run_id_stability(self) -> None:
        tmpdir = Path(tempfile.mkdtemp(prefix="estorides_er_"))
        store_path = tmpdir / "entities.sqlite"
        store = EntityStore(store_path)
        try:
            r1 = EntityResolver(store=store).resolve(
                [_ent("person", "Vladimir Putin", "wikidata")]
            )
            id1 = r1.entities[0].canonical_id

            r2 = EntityResolver(store=store).resolve(
                [_ent("person", "Владимир Путин", "ofac")]
            )
            assert r2.entities[0].canonical_id == id1, (
                f"cross-run id mismatch: {r2.entities[0].canonical_id} vs {id1}"
            )

            r3 = EntityResolver(store=store).resolve(
                [_ent("person", "Putin, Vladimir", "leak")]
            )
            assert r3.entities[0].canonical_id == id1, (
                f"alias should resolve to existing id: {r3.entities[0].canonical_id} vs {id1}"
            )

            r4 = EntityResolver(store=store).resolve(
                [_ent("person", "Dmitry Medvedev", "news")]
            )
            assert r4.entities[0].canonical_id != id1

            stats = store.stats()
            assert stats["entities"] >= 2
        finally:
            store.close()
            for child in sorted(tmpdir.glob("*")):
                child.unlink()
            tmpdir.rmdir()
