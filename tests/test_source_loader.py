"""
BDD / regression tests for SourceRegistry loading.

  - SL1: a multi-document YAML file loads every document
  - SL2: a document holding a list of sources loads every entry
  - SL3: a duplicate name overwrites cleanly and category counts stay consistent
  - SL4: an unknown `contact` value is normalised to `active`
  - SL5: an undecodable file is skipped without aborting the load
"""
from __future__ import annotations

from pathlib import Path

from estorides_core.source_loader import SourceRegistry


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _source(name: str, category: str = "01. DNS", extra: str = "") -> str:
    return (
        f"name: {name}\n"
        f"category: \"{category}\"\n"
        f"enabled: true\n"
        f"{extra}"
        "tool:\n  url: \"https://example.com/x\"\n"
    )


class TestSL1MultiDocument:
    def test_two_documents_load(self, tmp_path: Path) -> None:
        _write(tmp_path / "grouped.yaml",
               "---\n" + _source("doc_a") + "---\n" + _source("doc_b"))
        reg = SourceRegistry(tmp_path)
        reg.load()
        assert reg.get("doc_a") is not None
        assert reg.get("doc_b") is not None


class TestSL2ListDocument:
    def test_list_of_sources_loads(self, tmp_path: Path) -> None:
        body = (
            "- " + _source("list_a").replace("\n", "\n  ").rstrip()
            + "\n- " + _source("list_b").replace("\n", "\n  ").rstrip() + "\n"
        )
        _write(tmp_path / "list.yaml", body)
        reg = SourceRegistry(tmp_path)
        reg.load()
        assert reg.get("list_a") is not None
        assert reg.get("list_b") is not None


class TestSL3DuplicateName:
    def test_duplicate_overwrites_counts(self, tmp_path: Path) -> None:
        # Directory names control load order; the second registration wins.
        _write(tmp_path / "a" / "one.yaml", _source("dup", "01. DNS"))
        _write(tmp_path / "b" / "two.yaml", _source("dup", "02. IP"))
        reg = SourceRegistry(tmp_path)
        reg.load()
        assert reg.summary()["total"] == 1
        assert reg.get("dup")["category"] == "02. IP"
        # No stale entry left in the old category.
        cats = {c["name"]: c["count"] for c in reg.summary()["categories"]}
        assert cats.get("01. DNS", 0) == 0
        assert cats.get("02. IP") == 1


class TestSL4UnknownContact:
    def test_unknown_contact_becomes_active(self, tmp_path: Path) -> None:
        _write(tmp_path / "c.yaml", _source("c1", extra="contact: bogus\n"))
        reg = SourceRegistry(tmp_path)
        reg.load()
        assert reg.get("c1")["contact"] == "active"


class TestSL5UndecodableFile:
    def test_bad_encoding_does_not_abort_load(self, tmp_path: Path) -> None:
        (tmp_path / "bad.yaml").write_bytes(b"name: \xff\xfe\nenabled: true\n")
        _write(tmp_path / "good.yaml", _source("good"))
        reg = SourceRegistry(tmp_path)
        reg.load()
        assert reg.get("good") is not None
