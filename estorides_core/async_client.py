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
                     HTTP_BACKOFF_BASE, HTTP_BACKOFF_FACTOR, HTTP_MAX_RETRIES,
                     HTTP_TIMEOUT, USER_AGENT)
from .ssrf_guard import SSRFError, assert_safe, check_url

log = logging.getLogger("estorides.http")


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
    """SQLite-backed response cache. Key = (url + method + body hash)."""

    def __init__(self, path: Path = CACHE_PATH) -> None:
        self.path = path
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
        k = self._key(method, url, body)
        with sqlite3.connect(self.path) as con:
            row = con.execute("SELECT v, ts FROM cache WHERE k=?", (k,)).fetchone()
        if not row:
            return None
        try:
            return json.loads(row[0])
        except json.JSONDecodeError:
            return None

    def set(self, method: str, url: str, body: Optional[str], value: Any) -> None:
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
    ) -> None:
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self.user_agent = user_agent
        self.cache = cache or ResponseCache()
        self.breaker = breaker or CircuitBreaker()
        self._sem = asyncio.Semaphore(max_parallel)
        self._session: Optional[aiohttp.ClientSession] = None

    # ---------------------------------------------------- session lifecycle
    async def __aenter__(self) -> "AsyncClient":
        self._session = aiohttp.ClientSession(
            timeout=self.timeout,
            headers={"User-Agent": self.user_agent, "Accept": "*/*"},
        )
        return self

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
        }

        if not self.breaker.allow(host):
            meta["error"] = "circuit_open"
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
) -> Tuple[Optional[Any], Dict[str, Any]]:
    import requests

    meta: Dict[str, Any] = {"url": url, "method": method, "cached": False}
    # SSRF guard: never let the synchronous client become a pivot into the
    # private network even when it is used from CLI or notebook contexts.
    try:
        assert_safe(url)
    except SSRFError as e:
        log.warning("SSRF guard rejected %s: %s", url, e)
        return None, {**meta, "error": f"ssrf_blocked:{e}"}
    try:
        resp = requests.request(
            method=method.upper(),
            url=url,
            headers={**{"User-Agent": USER_AGENT}, **(headers or {})},
            params=params,
            json=body if isinstance(body, (dict, list)) else None,
            data=body if isinstance(body, str) else None,
            timeout=timeout,
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
