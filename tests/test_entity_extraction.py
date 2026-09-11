"""
BDD / regression tests for entity extraction and fuzzy merge.

  - EE1: `types=[]` extracts nothing (and `types=None` extracts everything)
  - EE2: fuzzy merge picks the most-observed spelling as canonical
"""
from __future__ import annotations

from estorides_core.entity_extraction import Entity, extract_from_text, merge


class TestEE1TypesFilter:
    TEXT = "mail admin@example.com or host 8.8.8.8"

    def test_none_means_all(self) -> None:
        found = extract_from_text(self.TEXT, "src", types=None)
        kinds = {e.type for e in found}
        assert "email" in kinds or "ipv4" in kinds

    def test_empty_list_means_nothing(self) -> None:
        assert extract_from_text(self.TEXT, "src", types=[]) == []

    def test_subset_restricts(self) -> None:
        found = extract_from_text(self.TEXT, "src", types=["email"])
        assert all(e.type == "email" for e in found)


class TestEE2FuzzyCanonical:
    def test_most_observed_spelling_wins(self) -> None:
        """Given two spellings of the same domain, the widely-seen one is
        canonical even when it is not the shortest."""
        many = Entity(type="domain", value="evil-corp.com",
                      source="a", sources=["a", "b", "c"])
        few = Entity(type="domain", value="evilcorp.com",
                     source="a", sources=["a"])
        merged = merge([many], [few], fuzzy=True)
        domains = [e for e in merged if e.type == "domain"]
        assert len(domains) == 1
        assert domains[0].value == "evil-corp.com"

    def test_merge_unions_sources(self) -> None:
        many = Entity(type="domain", value="evil-corp.com",
                      source="a", sources=["a", "b"])
        few = Entity(type="domain", value="evilcorp.com",
                     source="c", sources=["c"])
        merged = merge([many], [few], fuzzy=True)
        canon = next(e for e in merged if e.type == "domain")
        assert set(canon.sources) >= {"a", "b", "c"}
