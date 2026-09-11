"""BDD tests for the shared env readers (spec/envutil.md)."""
from __future__ import annotations

from estorides_core.envutil import env_bool, env_csv, env_float, env_int


class TestEnvInt:
    def test_parse(self, monkeypatch) -> None:
        monkeypatch.setenv("EU_INT", "42")
        assert env_int("EU_INT", 1) == 42

    def test_malformed(self, monkeypatch) -> None:
        monkeypatch.setenv("EU_INT", "abc")
        assert env_int("EU_INT", 7) == 7

    def test_absent(self) -> None:
        assert env_int("EU_ABSENT", 9) == 9


class TestEnvFloat:
    def test_parse_and_malformed(self, monkeypatch) -> None:
        monkeypatch.setenv("EU_F", "2.5")
        assert env_float("EU_F", 1.0) == 2.5
        monkeypatch.setenv("EU_F", "hot")
        assert env_float("EU_F", 3.0) == 3.0


class TestEnvBool:
    def test_tokens(self, monkeypatch) -> None:
        monkeypatch.setenv("EU_B", "yes")
        assert env_bool("EU_B", False) is True
        monkeypatch.setenv("EU_B", "off")
        assert env_bool("EU_B", True) is False

    def test_unknown_uses_default(self, monkeypatch) -> None:
        monkeypatch.setenv("EU_B", "maybe")
        assert env_bool("EU_B", True) is True


class TestEnvCsv:
    def test_strip_and_filter(self, monkeypatch) -> None:
        monkeypatch.setenv("EU_CSV", "a, b ,,c")
        assert env_csv("EU_CSV") == ("a", "b", "c")

    def test_default(self) -> None:
        assert env_csv("EU_CSV_ABSENT", ("x",)) == ("x",)
