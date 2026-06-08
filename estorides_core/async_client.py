"""
estorides_core.async_client
===========================
Async HTTP client with:
  * per-host concurrency limits
  * exponential backoff
  * circuit breaker (per host)
  * disk-backed cache (SQLite)
  * automatic key-substitution from environment

Designed so a single query can fan out to 50+ sources in parallel
without DOSsing any of them.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

import aiohttp

from .config import (CACHE_PATH, CIRCUIT_COOLDOWN_S, CIRCUIT_FAIL_THRESHOLD,
                     HTTP_BACKOFF_BASE, HTTP_BACKOFF_FACTOR, HTTP_CACHE,
                     HTTP_MAX_RETRIES, HTTP_TIMEOUT, PROXY_REMOTE_DNS,
                     USER_AGENT, effective_proxies)
from .ssrf_guard import check_url

log = logging.getLogger("estorides.http")

_SOCKS_SCHEMES = ("socks5://", "socks5h://", "socks4://", "socks4a://")


def _is_socks(proxy: str) -> bool:
    """True when the proxy URL is a SOCKS proxy (e.g. Tor)."""
    return proxy.lower().startswith(_SOCKS_SCHEMES)


def _redact_proxy(proxy: str) -> str:
    """Strip any `user:pass@` credentials from a proxy URL before logging."""
    if "@" not in proxy:
        return proxy
    scheme, _, rest = proxy.partition("://")
    host = rest.rpartition("@")[2]
    return f"{scheme}://***@{host}" if scheme else f"***@{host}"


@dataclass
class CircuitBreaker:
    """Per-host circuit breaker."""
    failures: Dict[str, int] = field(default_factory=dict)
    open_until: Dict[str, float] = field(default_factory=dict)

    def allow(self, host: str) -> bool:
        until = self.open_until.get(host, 0.0)
        if until > time.time():
            return False
        return True

    def record_success(self, host: str) -> None:
        self.failures.pop(host, None)
        self.open_until.pop(host, None)

    def record_failure(self, host: str) -> None:
        self.failures[host] = self.failures.get(host, 0) + 1
        if self.failures[host] >= CIRCUIT_FAIL_THRESHOLD:
            self.open_until[host] = time.time() + CIRCUIT_COOLDOWN_S
            log.warning("circuit open for %s for %ds", host, CIRCUIT_COOLDOWN_S)


class ResponseCache:
    """SQLite-backed response cache. Key = (url + method + body hash).

    Entries carry their write timestamp and are only served while younger
    than `ttl_seconds`; a stale row is ignored (and lazily overwritten on
    the next live fetch) so the cache can never pin down OSINT that has
    since changed or been taken down.
    """

    def __init__(
        self,
        path: Path = CACHE_PATH,
        *,
        ttl_seconds: int = HTTP_CACHE.ttl_seconds,
        enabled: bool = HTTP_CACHE.enabled,
    ) -> None:
        self.path = path
        self.ttl_seconds = ttl_seconds
        self.enabled = enabled
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    k TEXT PRIMARY KEY,
                    v TEXT NOT NULL,
                    ts REAL NOT NULL
                )
                """
            )

    @staticmethod
    def _key(method: str, url: str, body: Optional[str]) -> str:
        h = hashlib.sha256()
        h.update(method.upper().encode())
        h.update(b"\x00")
        h.update(url.encode())
        h.update(b"\x00")
        h.update((body or "").encode())
        return h.hexdigest()

    def get(self, method: str, url: str, body: Optional[str]) -> Optional[Any]:
        if not self.enabled or self.ttl_seconds <= 0:
            return None
        k = self._key(method, url, body)
        with sqlite3.connect(self.path) as con:
            row = con.execute("SELECT v, ts FROM cache WHERE k=?", (k,)).fetchone()
        if not row:
            return None
        written_at = row[1]
        if not isinstance(written_at, (int, float)) or (time.time() - written_at) > self.ttl_seconds:
            return None
        try:
            return json.loads(row[0])
        except json.JSONDecodeError:
            return None

    def set(self, method: str, url: str, body: Optional[str], value: Any) -> None:
        if not self.enabled:
            return
        k = self._key(method, url, body)
        with sqlite3.connect(self.path) as con:
            con.execute(
                "INSERT OR REPLACE INTO cache (k, v, ts) VALUES (?, ?, ?)",
                (k, json.dumps(value, ensure_ascii=False), time.time()),
            )


class AsyncClient:
    """Async HTTP client with retries, backoff, circuit breaker, cache."""

    def __init__(
        self,
        *,
        timeout: float = HTTP_TIMEOUT,
        max_retries: int = HTTP_MAX_RETRIES,
        user_agent: str = USER_AGENT,
        cache: Optional[ResponseCache] = None,
        breaker: Optional[CircuitBreaker] = None,
        max_parallel: int = 8,
        proxies: Optional[list[str]] = None,
        proxy_remote_dns: bool = PROXY_REMOTE_DNS,
    ) -> None:
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.user_agent = user_agent
        self.cache = cache or ResponseCache()
        self.breaker = breaker or CircuitBreaker()
        self._sem = asyncio.Semaphore(max_parallel)
        self._session: Optional[aiohttp.ClientSession] = None
        # Egress anonymisation. A caller may pass an explicit pool; otherwise
        # fall back to the env-configured proxy so anonymity stays on even
        # when the client is constructed directly.
        self._proxies: list[str] = list(proxies) if proxies is not None else effective_proxies()
        self._proxy_active: bool = bool(self._proxies)
        self._proxy_remote_dns: bool = proxy_remote_dns
        self._request_proxies: list[str] = []  # HTTP proxies applied per request
        self._proxy_idx: int = 0

    # ---------------------------------------------------- session lifecycle
    async def __aenter__(self) -> "AsyncClient":
        connector: Optional[aiohttp.BaseConnector] = None
        self._request_proxies = []
        if self._proxies:
            first = self._proxies[0]
            if _is_socks(first):
                # SOCKS (Tor) is wired at the connector level. We do not fall
                # back to a direct connection on a missing dependency: the
                # operator explicitly asked for anonymised egress, so sending
                # traffic in the clear would be the exact deanonymisation we
                # are guarding against. Fail closed.
                try:
                    from aiohttp_socks import ProxyConnector
                except ImportError as e:
                    raise RuntimeError(
                        f"SOCKS proxy {_redact_proxy(first)} requested but the "
                        "'aiohttp_socks' package is not installed; refusing to "
                        "fall back to a direct (deanonymising) connection. "
                        "Install it with: pip install aiohttp_socks"
                    ) from e
                connector = ProxyConnector.from_url(first)
                if len(self._proxies) > 1:
                    log.warning(
                        "SOCKS egress uses a single proxy; %d pool entries ignored "
                        "(rotate Tor circuits via the control port instead)",
                        len(self._proxies) - 1,
                    )
                log.info("egress anonymised via SOCKS proxy %s", _redact_proxy(first))
            else:
                # HTTP/HTTPS proxies are applied per request so the pool can
                # rotate across the fan-out.
                self._request_proxies = list(self._proxies)
                log.info(
                    "egress anonymised via %d HTTP proxy(ies): %s",
                    len(self._request_proxies),
                    ", ".join(_redact_proxy(p) for p in self._request_proxies),
                )
        self._session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers={"User-Agent": self.user_agent, "Accept": "*/*"},
            connector=connector,
        )
        return self

    def _next_http_proxy(self) -> Optional[str]:
        """Round-robin the next HTTP proxy, or None (SOCKS/connector or direct)."""
        if not self._request_proxies:
            return None
        proxy = self._request_proxies[self._proxy_idx % len(self._request_proxies)]
        self._proxy_idx += 1
        return proxy

    async def __aexit__(self, *exc: Any) -> None:
        if self._session is not None:
            await self._session.close()
            self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            raise RuntimeError("AsyncClient used outside async-with block")
        return self._session

    # --------------------------------------------------------------- public
    async def fetch(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Any] = None,
        use_cache: bool = True,
    ) -> Tuple[Optional[Any], Dict[str, Any]]:
        """Fetch a URL. Returns (parsed_data, meta).

        meta contains status, content_type, cached, attempts, error.
        parsed_data is dict/list/str/None depending on content-type."""
        host = urlparse(url).netloc
        meta: Dict[str, Any] = {
            "url": url,
            "method": method,
            "host": host,
            "attempts": 0,
            "cached": False,
            "proxied": self._proxy_active,
        }

        if not self.breaker.allow(host):
            meta["error"] = "circuit_open"
            return None, meta

        # SSRF guard. The synchronous client already validated; the async
        # fan-out (the primary path, where the URL carries an interpolated
        # user query) must do the same or it is a pivot into private space.
        # check_url resolves DNS, which is blocking, so it runs in a worker
        # thread to keep the event loop free. This is the TOCTOU-resistant
        # leg: resolution happens immediately before the request goes out.
        #
        # When egress is proxied with remote DNS, resolving the host locally
        # would leak which targets the operator is investigating to the local
        # resolver, defeating Tor. In that mode the literal-host leg still
        # runs (resolve=False) and the proxy/exit node resolves the name.
        resolve_dns = not (self._proxy_active and self._proxy_remote_dns)
        guard = await asyncio.to_thread(check_url, url, resolve=resolve_dns)
        if not guard.allowed:
            log.warning("SSRF guard blocked %s: %s", url, guard.reason)
            meta["error"] = f"ssrf_blocked:{guard.reason}"
            return None, meta

        # Cache hit?
        body_str: Optional[str] = None
        if isinstance(body, (dict, list)):
            body_str = json.dumps(body, sort_keys=True)
        elif isinstance(body, str):
            body_str = body
        if use_cache and method.upper() == "GET":
            cached = self.cache.get(method, url, body_str)
            if cached is not None:
                meta["cached"] = True
                meta["status"] = 200
                return cached, meta

        last_exc: Optional[Exception] = None
        async with self._sem:
            for attempt in range(1, self.max_retries + 1):
                meta["attempts"] = attempt
                try:
                    async with self.session.request(
                        method,
                        url,
                        headers=headers or {},
                        params=params,
                        data=body if not isinstance(body, (dict, list, str)) else None,
                        json=body if isinstance(body, (dict, list)) else None,
                        proxy=self._next_http_proxy(),
                    ) as resp:
                        meta["status"] = resp.status
                        meta["content_type"] = resp.headers.get("content-type", "")
                        text = await resp.text()

                        if resp.status == 429:
                            # rate limited — backoff and retry
                            await asyncio.sleep(HTTP_BACKOFF_BASE * (HTTP_BACKOFF_FACTOR ** (attempt - 1)))
                            continue
                        if resp.status in (401, 403):
                            self.breaker.record_failure(host)
                            meta["error"] = f"http_{resp.status}"
                            return None, meta
                        if resp.status == 404:
                            meta["error"] = "http_404"
                            return None, meta
                        if resp.status >= 500:
                            last_exc = RuntimeError(f"http_{resp.status}")
                            await asyncio.sleep(HTTP_BACKOFF_BASE * (HTTP_BACKOFF_FACTOR ** (attempt - 1)))
                            continue

                        # success
                        self.breaker.record_success(host)
                        data: Any
                        ctype = meta["content_type"].lower()
                        if "application/json" in ctype or text.lstrip().startswith(("{", "[")):
                            try:
                                data = json.loads(text)
                            except json.JSONDecodeError:
                                data = {"raw_text": text}
                        else:
                            data = {"raw_text": text}

                        if use_cache and method.upper() == "GET":
                            self.cache.set(method, url, body_str, data)
                        return data, meta

                except asyncio.TimeoutError as e:
                    last_exc = e
                    meta["error"] = "timeout"
                except aiohttp.ClientError as e:
                    last_exc = e
                    meta["error"] = str(e.__class__.__name__)
                except Exception as e:  # noqa: BLE001
                    last_exc = e
                    meta["error"] = str(e)
                await asyncio.sleep(HTTP_BACKOFF_BASE * (HTTP_BACKOFF_FACTOR ** (attempt - 1)))

        self.breaker.record_failure(host)
        if last_exc is not None:
            log.debug("giving up on %s: %s", url, last_exc)
        return None, meta


# ---------------------------------------------------------------------------
# Synchronous client for the CLI / embedding paths. Uses urllib to avoid
# forcing aiohttp on callers that don't need fanout.
# ---------------------------------------------------------------------------
def sync_fetch(
    method: str,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    body: Optional[Any] = None,
    timeout: float = HTTP_TIMEOUT,
    proxy: Optional[str] = None,
    proxy_remote_dns: bool = PROXY_REMOTE_DNS,
) -> Tuple[Optional[Any], Dict[str, Any]]:
    import requests

    # Resolve the egress proxy the same way the async client does: an
    # explicit value wins, else the env-configured pool (first entry).
    proxies_pool = effective_proxies(proxy)
    egress_proxy = proxies_pool[0] if proxies_pool else None
    proxy_active = egress_proxy is not None

    meta: Dict[str, Any] = {"url": url, "method": method, "cached": False, "proxied": proxy_active}
    # SSRF guard: never let the synchronous client become a pivot into the
    # private network even when it is used from CLI or notebook contexts.
    # Skip the DNS-resolving leg when proxying with remote DNS so the local
    # resolver never learns which targets are under investigation.
    resolve_dns = not (proxy_active and proxy_remote_dns)
    guard = check_url(url, resolve=resolve_dns)
    if not guard.allowed:
        log.warning("SSRF guard rejected %s: %s", url, guard.reason)
        return None, {**meta, "error": f"ssrf_blocked:{guard.reason}"}
    requests_proxies = (
        {"http": egress_proxy, "https": egress_proxy} if egress_proxy else None
    )
    try:
        resp = requests.request(
            method=method.upper(),
            url=url,
            headers={**{"User-Agent": USER_AGENT}, **(headers or {})},
            params=params,
            json=body if isinstance(body, (dict, list)) else None,
            data=body if isinstance(body, str) else None,
            timeout=timeout,
            proxies=requests_proxies,
        )
        meta["status"] = resp.status_code
        meta["content_type"] = resp.headers.get("content-type", "")
        ctype = meta["content_type"].lower()
        if "application/json" in ctype or resp.text.lstrip().startswith(("{", "[")):
            try:
                return resp.json(), meta
            except json.JSONDecodeError:
                return {"raw_text": resp.text}, meta
        return {"raw_text": resp.text}, meta
    except requests.exceptions.RequestException as e:
        meta["error"] = str(e.__class__.__name__)
        return None, meta
