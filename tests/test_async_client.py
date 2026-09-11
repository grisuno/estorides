"""
BDD tests for egress anonymisation wiring (`estorides_core.async_client`).

Ported from the standalone ``_test_proxy.py`` validator into pytest.
Offline: no socket is opened.
"""
from __future__ import annotations

import asyncio
import sys

from estorides_core.async_client import AsyncClient, _is_socks, _redact_proxy
from estorides_core.config import effective_proxies


class TestSocksDetection:
    def test_schemes(self) -> None:
        assert _is_socks("socks5://127.0.0.1:9050")
        assert _is_socks("socks5h://127.0.0.1:9050")
        assert not _is_socks("http://127.0.0.1:8080")


class TestRedaction:
    def test_hides_credentials_keeps_host(self) -> None:
        red = _redact_proxy("socks5://user:secret@host:9050")
        assert "secret" not in red and "user" not in red
        assert "host:9050" in red

    def test_passthrough_without_credentials(self) -> None:
        assert _redact_proxy("http://127.0.0.1:8080") == "http://127.0.0.1:8080"


class TestEffectiveProxies:
    def test_explicit_wins(self, monkeypatch) -> None:
        monkeypatch.delenv("ESTORIDES_HTTP_PROXY", raising=False)
        monkeypatch.delenv("ESTORIDES_HTTP_PROXY_POOL", raising=False)
        assert effective_proxies("http://p:1") == ["http://p:1"]

    def test_none_by_default(self, monkeypatch) -> None:
        monkeypatch.delenv("ESTORIDES_HTTP_PROXY", raising=False)
        monkeypatch.delenv("ESTORIDES_HTTP_PROXY_POOL", raising=False)
        assert effective_proxies() == []


class TestRotation:
    def test_round_robin(self) -> None:
        client = AsyncClient(proxies=["http://a:1", "http://b:2"])

        async def _enter_and_rotate() -> list:
            async with client:
                return [client._next_http_proxy() for _ in range(4)]

        assert asyncio.run(_enter_and_rotate()) == [
            "http://a:1", "http://b:2", "http://a:1", "http://b:2",
        ]

    def test_direct_has_no_proxy(self) -> None:
        direct = AsyncClient(proxies=[])
        assert direct._next_http_proxy() is None
        assert direct._proxy_active is False


class TestFailClosed:
    def test_socks_without_backend_raises(self, monkeypatch) -> None:
        monkeypatch.setitem(sys.modules, "aiohttp_socks", None)
        socks_client = AsyncClient(proxies=["socks5://127.0.0.1:9050"])

        async def _enter_socks() -> None:
            async with socks_client:
                pass

        try:
            asyncio.run(_enter_socks())
            raised = False
        except RuntimeError:
            raised = True
        assert raised, "SOCKS without aiohttp_socks must fail closed"
