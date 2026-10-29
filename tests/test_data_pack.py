"""
Tests for :mod:`estorides_core.data_pack`.

A pack is a remote dataset consumed at runtime: these tests pin the three
promises that make that safe — a fresh cache never hits the network, a
bad download falls back to what we already had, and a pinned SHA-256
fails closed.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import pytest

from estorides_core import data_pack


def _write_cache(path: Path, payload: Any, *, age_s: float = 0.0,
                 digest: str = "0" * 64) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"fetched_at": time.time() - age_s, "sha256": digest,
                    "payload": payload}),
        encoding="utf-8",
    )


def _parse_rows(raw: bytes) -> list[str]:
    return raw.decode("utf-8").splitlines()


class TestCache:
    def test_fresh_cache_skips_network(self, tmp_path: Path,
                                       monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        _write_cache(cache, ["cached"])

        def boom(*args: Any, **kwargs: Any) -> bytes:
            raise AssertionError("network must not be touched")

        monkeypatch.setattr(data_pack, "fetch_bytes", boom)
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache) == ["cached"]

    def test_stale_cache_is_refetched(self, tmp_path: Path,
                                      monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        _write_cache(cache, ["old"], age_s=10_000)
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"new")
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache, ttl_s=60) == ["new"]
        assert data_pack.read_cache(cache).payload == ["new"]

    def test_use_cache_false_forces_refetch(self, tmp_path: Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        _write_cache(cache, ["old"])
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"fresh")
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache, use_cache=False) == ["fresh"]

    def test_corrupt_cache_is_treated_as_missing(self, tmp_path: Path,
                                                 monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text("{not json", encoding="utf-8")
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"fresh")
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache) == ["fresh"]

    def test_foreign_cache_shape_is_ignored(self, tmp_path: Path) -> None:
        cache = tmp_path / "pack.json"
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps({"airports": []}), encoding="utf-8")
        assert data_pack.read_cache(cache) is None


class TestFailureFallback:
    def test_network_failure_serves_stale(self, tmp_path: Path,
                                          monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        _write_cache(cache, ["stale"], age_s=10_000)

        def boom(*args: Any, **kwargs: Any) -> bytes:
            raise data_pack.DataPackError("down")

        monkeypatch.setattr(data_pack, "fetch_bytes", boom)
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache, ttl_s=60) == ["stale"]

    def test_network_failure_without_cache_is_none(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        def boom(*args: Any, **kwargs: Any) -> bytes:
            raise data_pack.DataPackError("down")

        monkeypatch.setattr(data_pack, "fetch_bytes", boom)
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=tmp_path / "none.json") is None

    def test_parser_failure_serves_stale(self, tmp_path: Path,
                                         monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        _write_cache(cache, ["stale"], age_s=10_000)
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"x")

        def explode(raw: bytes) -> list[str]:
            raise ValueError("bad payload")

        assert data_pack.load_pack("p", "https://example.test/x", explode,
                                   cache_path=cache, ttl_s=60) == ["stale"]

    def test_parser_returning_none_keeps_stale(self, tmp_path: Path,
                                               monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        _write_cache(cache, ["stale"], age_s=10_000)
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"x")
        assert data_pack.load_pack("p", "https://example.test/x", lambda raw: None,
                                   cache_path=cache, ttl_s=60) == ["stale"]


class TestIntegrityPin:
    def test_matching_pin_is_accepted(self, tmp_path: Path,
                                      monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        digest = data_pack.sha256_hex(b"a\nb")
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"a\nb")
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache,
                                   expected_sha256=digest.upper()) == ["a", "b"]
        assert data_pack.read_cache(cache).sha256 == digest

    def test_mismatch_fails_closed(self, tmp_path: Path,
                                   monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"tampered")
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache,
                                   expected_sha256="1" * 64) is None
        assert not cache.exists()

    def test_mismatch_keeps_the_last_known_good(self, tmp_path: Path,
                                                monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        good = data_pack.sha256_hex(b"good")
        _write_cache(cache, ["good"], age_s=10_000, digest=good)
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"tampered")
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache, ttl_s=60,
                                   expected_sha256=good) == ["good"]

    def test_pinned_cache_refetches_when_digest_changed(self, tmp_path: Path,
                                                        monkeypatch: pytest.MonkeyPatch) -> None:
        cache = tmp_path / "pack.json"
        _write_cache(cache, ["old"], digest="2" * 64)
        monkeypatch.setattr(data_pack, "fetch_bytes", lambda *a, **k: b"new")
        digest = data_pack.sha256_hex(b"new")
        assert data_pack.load_pack("p", "https://example.test/x", _parse_rows,
                                   cache_path=cache,
                                   expected_sha256=digest) == ["new"]

    @pytest.mark.parametrize("value", [None, "", "xyz", "0" * 63, 42, "0" * 65])
    def test_unusable_pin_is_ignored(self, value: Any) -> None:
        assert data_pack.normalise_sha256(value) is None

    def test_digest_is_case_insensitive(self) -> None:
        assert data_pack.normalise_sha256("A" * 64) == "a" * 64


class _FakeStream:
    def __init__(self, chunks: list[bytes]) -> None:
        self._chunks = chunks

    def raise_for_status(self) -> None:
        return None

    def iter_content(self, chunk_size: int = 1) -> Any:
        yield from self._chunks


def test_fetch_bytes_enforces_the_size_cap(monkeypatch: pytest.MonkeyPatch) -> None:
    import requests

    monkeypatch.setattr(data_pack, "assert_safe", lambda url: None)

    monkeypatch.setattr(requests, "get",
                        lambda *a, **k: _FakeStream([b"x" * 10, b"y" * 10]))
    with pytest.raises(data_pack.DataPackError):
        data_pack.fetch_bytes("https://example.test/x", max_bytes=15)


def test_fetch_bytes_joins_chunks(monkeypatch: pytest.MonkeyPatch) -> None:
    import requests

    monkeypatch.setattr(data_pack, "assert_safe", lambda url: None)

    monkeypatch.setattr(requests, "get",
                        lambda *a, **k: _FakeStream([b"ab", b"", b"cd"]))
    assert data_pack.fetch_bytes("https://example.test/x") == b"abcd"
