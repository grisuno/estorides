"""M4 case_crypto BDD red."""
from __future__ import annotations


def _fresh_store(tmp_path, monkeypatch, key=None):
    if key is None:
        monkeypatch.delenv("ESTORIDES_CASE_KEY", raising=False)
    else:
        monkeypatch.setenv("ESTORIDES_CASE_KEY", key)
    monkeypatch.setenv("ESTORIDES_CASES_DB", str(tmp_path / "c.sqlite"))
    import importlib

    import estorides_core.case_crypto as cc

    importlib.reload(cc)
    import estorides_core.cases as cases

    importlib.reload(cases)
    return cases.CaseStore(path=tmp_path / "c.sqlite"), cc


def test_disabled_stores_plaintext(tmp_path, monkeypatch):
    store, cc = _fresh_store(tmp_path, monkeypatch, key=None)
    try:
        assert cc.crypto_status()["enabled"] is False
        cid = store.create_case("example.com", "domain", notes="hola")
        row = store._conn.execute("SELECT notes FROM cases WHERE id=?", (cid,)).fetchone()
        assert row[0] == "hola"
    finally:
        store.close()


def test_enabled_roundtrip(tmp_path, monkeypatch):
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        import pytest

        pytest.skip("cryptography missing")
    key = Fernet.generate_key().decode()
    store, cc = _fresh_store(tmp_path, monkeypatch, key=key)
    try:
        assert cc.crypto_status()["enabled"] is True
        cid = store.create_case("example.com", "domain", notes="secreto")
        store.finalise(cid, analysis={"a": 1})
        raw = store._conn.execute(
            "SELECT notes, analysis_json FROM cases WHERE id=?", (cid,)
        ).fetchone()
        assert raw[0].startswith("gAAAA")
        assert raw[1].startswith("gAAAA")
        case = store.get_case(cid)
        assert case["notes"] == "secreto"
        assert case["analysis"] == {"a": 1}
    finally:
        store.close()


def test_bad_key_falls_back(tmp_path, monkeypatch):
    store, cc = _fresh_store(tmp_path, monkeypatch, key="nope")
    try:
        assert cc.crypto_status()["enabled"] is False
        cid = store.create_case("x", notes="plain")
        row = store._conn.execute("SELECT notes FROM cases WHERE id=?", (cid,)).fetchone()
        assert row[0] == "plain"
    finally:
        store.close()


def test_mixed_rows_and_tamper(tmp_path, monkeypatch):
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        import pytest

        pytest.skip("cryptography missing")
    key = Fernet.generate_key().decode()
    store, _cc = _fresh_store(tmp_path, monkeypatch, key=None)
    try:
        cid1 = store.create_case("a", notes="old-plain")
        monkeypatch.setenv("ESTORIDES_CASE_KEY", key)
        cid2 = store.create_case("b", notes="new-secret")
        assert store.get_case(cid1)["notes"] == "old-plain"
        assert store.get_case(cid2)["notes"] == "new-secret"
        with store._tx() as c:
            c.execute("UPDATE cases SET notes=? WHERE id=?", ("gAAAA-bogus", cid1))
        assert store.get_case(cid1)["notes"] == "[decrypt-error]"
    finally:
        store.close()
