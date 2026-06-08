#!/usr/bin/env python3
"""Tests for egress anonymisation wiring.

Offline only: exercises proxy resolution, credential redaction, SOCKS
detection, the per-request rotation cursor and the fail-closed behaviour
when a SOCKS proxy is requested without aiohttp_socks. No socket is opened.
"""
from __future__ import annotations

import asyncio
import os
import sys

from estorides_core import async_client as ac
from estorides_core.async_client import AsyncClient, _is_socks, _redact_proxy
from estorides_core.config import effective_proxies

_failures = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global _failures
    if cond:
        print(f"PASS: {name}")
    else:
        _failures += 1
        print(f"FAIL: {name} {detail}")


def main() -> int:
    # SOCKS scheme detection.
    check("socks5 detected", _is_socks("socks5://127.0.0.1:9050"))
    check("socks5h detected", _is_socks("socks5h://127.0.0.1:9050"))
    check("http not socks", not _is_socks("http://127.0.0.1:8080"))

    # Credential redaction never leaks user:pass.
    red = _redact_proxy("socks5://user:secret@host:9050")
    check("redaction hides credentials", "secret" not in red and "user" not in red, red)
    check("redaction keeps host", "host:9050" in red, red)
    check("redaction passthrough without creds",
          _redact_proxy("http://127.0.0.1:8080") == "http://127.0.0.1:8080")

    # effective_proxies precedence: explicit > pool env > single env.
    for var in ("ESTORIDES_HTTP_PROXY", "ESTORIDES_HTTP_PROXY_POOL"):
        os.environ.pop(var, None)
    check("explicit proxy wins", effective_proxies("http://p:1") == ["http://p:1"])
    check("no proxy by default", effective_proxies() == [])

    # Per-request HTTP proxy rotation cursor.
    client = AsyncClient(proxies=["http://a:1", "http://b:2"])

    async def _enter_and_rotate() -> list:
        async with client:
            return [client._next_http_proxy() for _ in range(4)]

    rotated = asyncio.run(_enter_and_rotate())
    check("http proxy pool rotates round-robin",
          rotated == ["http://a:1", "http://b:2", "http://a:1", "http://b:2"], str(rotated))

    # Direct client yields no per-request proxy.
    direct = AsyncClient(proxies=[])
    check("direct client has no proxy", direct._next_http_proxy() is None)
    check("direct client reports not proxied", direct._proxy_active is False)

    # Fail-closed: SOCKS requested but aiohttp_socks unavailable must raise,
    # never silently send in the clear. Simulate absence by hiding the module.
    saved = sys.modules.get("aiohttp_socks")
    sys.modules["aiohttp_socks"] = None  # type: ignore[assignment]
    try:
        socks_client = AsyncClient(proxies=["socks5://127.0.0.1:9050"])

        async def _enter_socks() -> None:
            async with socks_client:
                pass

        raised = False
        try:
            asyncio.run(_enter_socks())
        except RuntimeError:
            raised = True
        check("SOCKS without aiohttp_socks fails closed", raised)
    finally:
        if saved is not None:
            sys.modules["aiohttp_socks"] = saved
        else:
            sys.modules.pop("aiohttp_socks", None)

    print(f"\n{'ALL PASS' if _failures == 0 else f'{_failures} FAILURES'}")
    return 1 if _failures else 0


if __name__ == "__main__":
    sys.exit(main())
