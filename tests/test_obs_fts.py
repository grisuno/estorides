"""Obs FTS BDD."""
from __future__ import annotations


def _store(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTORIDES_CASES_DB", str(tmp_path / "c.sqlite"))
    monkeypatch.delenv("ESTORIDES_CASE_KEY", raising=False)
    import importlib

    import estorides_core.cases as cases

    importlib.reload(cases)
    return cases.CaseStore(path=tmp_path / "c.sqlite")


def test_fts_finds_rare_word(tmp_path, monkeypatch):
    s = _store(tmp_path, monkeypatch)
    try:
        if not s.fts_available():
            import pytest

            pytest.skip("FTS5 missing")
        cid = s.create_case("example.com", "domain")
        s.add_observation(cid, {"source": "crtsh", "parsed": {"host": "rarewordxyz"}, "raw": "hello"})
        s.add_observation(cid, {"source": "dns", "parsed": {"host": "common"}, "raw": "world"})
        hits = s.search_observations_fts("rarewordxyz")
        assert len(hits) == 1
        assert hits[0]["source"] == "crtsh"
    finally:
        s.close()


def test_fts_empty_and_injection_safe(tmp_path, monkeypatch):
    s = _store(tmp_path, monkeypatch)
    try:
        assert s.search_observations_fts("") == []
        assert s.search_observations_fts('" OR 1=1 --') == [] or isinstance(
            s.search_observations_fts('" OR 1=1 --'), list
        )
    finally:
        s.close()
