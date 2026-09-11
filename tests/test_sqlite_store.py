"""
BDD tests for the shared SQLite store base (spec/sqlite_store.md).

  - SS1: schema applied, default path honoured
  - SS2: `_tx` commits
  - SS3: `_tx` rolls back and re-raises
  - SS4: `close` is idempotent
  - SS5: DictMixin maps a dataclass to a dict
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from estorides_core.sqlite_store import DictMixin, SqliteStore


class _Store(SqliteStore):
    _DDL = ("CREATE TABLE IF NOT EXISTS t (id INTEGER PRIMARY KEY, v TEXT)",)


class TestSS1Schema:
    def test_default_path_and_schema(self, tmp_path: Path) -> None:
        _Store._DEFAULT_PATH = tmp_path / "x.sqlite"
        store = _Store()
        try:
            assert store.path == tmp_path / "x.sqlite"
            store._conn.execute("INSERT INTO t(v) VALUES ('a')")
            assert store._conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1
        finally:
            store.close()

    def test_missing_path_raises(self) -> None:
        class NoPath(SqliteStore):
            _DDL = ()

        with pytest.raises(ValueError):
            NoPath()


class TestSS2Commit:
    def test_tx_commits(self, tmp_path: Path) -> None:
        store = _Store(tmp_path / "c.sqlite")
        try:
            with store._tx() as c:
                c.execute("INSERT INTO t(v) VALUES ('x')")
            assert store._conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 1
        finally:
            store.close()


class TestSS3Rollback:
    def test_tx_rolls_back_and_reraises(self, tmp_path: Path) -> None:
        store = _Store(tmp_path / "r.sqlite")
        try:
            with pytest.raises(RuntimeError):
                with store._tx() as c:
                    c.execute("INSERT INTO t(v) VALUES ('y')")
                    raise RuntimeError("boom")
            assert store._conn.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 0
        finally:
            store.close()


class TestSS4Close:
    def test_close_idempotent(self, tmp_path: Path) -> None:
        store = _Store(tmp_path / "cl.sqlite")
        store.close()
        store.close()  # must not raise


class TestSS5DictMixin:
    def test_to_dict(self) -> None:
        @dataclass
        class Row(DictMixin):
            a: int
            b: str

        assert Row(1, "x").to_dict() == {"a": 1, "b": "x"}
