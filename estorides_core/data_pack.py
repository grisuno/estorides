"""
estorides_core.data_pack
========================
Static reference data fetched from its upstream at runtime and cached
locally — never vendored into the repository.

Why a pack instead of a file in the tree:

  * **Provenance stays with the source.** The upstream owns the data,
    its corrections and its licence notices. Estorides keeps a cache,
    not a copy, so there is nothing to re-sync by hand and nothing to
    accidentally mis-attribute.
  * **Updates arrive without a commit.** A TTL decides when to refetch;
    the operator does not have to watch somebody else's repository.
  * **Optional pinning.** ``expected_sha256`` turns a remote file into a
    verifiable artifact: if it changes upstream, the load fails closed
    and the last known-good cache keeps serving. That is the difference
    between "using a dataset" and "trusting whatever is at that URL
    today".
  * **Offline degrades, it does not break.** A network or parse failure
    returns the stale payload (any age) instead of nothing.

The download itself is transport, so it lives here and not in the pure
modules that consume the payload.

Branding: Estorides, developed by Lazy Own Red Team.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import DATA_DIR
from .ssrf_guard import assert_safe

log = logging.getLogger("estorides.datapack")

DATA_PACK_DIR: Path = DATA_DIR / "packs"
DEFAULT_TTL_S: int = 30 * 24 * 60 * 60      # a month is "reference data" age
DEFAULT_MAX_BYTES: int = 64 * 1024 * 1024
DEFAULT_TIMEOUT_S: int = 60


class DataPackError(Exception):
    """A pack could not be fetched or parsed."""


class DataPackIntegrityError(DataPackError):
    """The downloaded bytes do not match the pinned SHA-256."""


@dataclass(frozen=True)
class PackSnapshot:
    """One cached payload plus the metadata needed to trust it."""

    payload: Any
    fetched_at: float
    sha256: str | None


def sha256_hex(payload: bytes) -> str:
    """Return the lower-case hex SHA-256 of ``payload``."""
    return hashlib.sha256(payload).hexdigest()


def normalise_sha256(value: Any) -> str | None:
    """Return a comparable digest, or ``None`` when the value is unusable."""
    if not isinstance(value, str):
        return None
    text = value.strip().lower()
    if len(text) != 64 or any(char not in "0123456789abcdef" for char in text):
        return None
    return text


def read_cache(path: Path) -> PackSnapshot | None:
    """Read a pack cache file; ``None`` when missing, corrupt or foreign."""
    try:
        blob = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(blob, dict) or "payload" not in blob:
        return None
    fetched_at = blob.get("fetched_at")
    stamp = float(fetched_at) if isinstance(fetched_at, (int, float)) else 0.0
    return PackSnapshot(
        payload=blob.get("payload"),
        fetched_at=stamp,
        sha256=normalise_sha256(blob.get("sha256")),
    )


def write_cache(path: Path, payload: Any, digest: str) -> None:
    """Write the cache atomically (tmp file + replace). Never raises."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                {"fetched_at": time.time(), "sha256": digest, "payload": payload},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        os.replace(temporary, path)
    except OSError as e:
        log.debug("pack cache write failed (non-fatal): %s", e)


def fetch_bytes(
    url: str,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    timeout: int = DEFAULT_TIMEOUT_S,
) -> bytes:
    """Download ``url`` with the project User-Agent and a hard size cap."""
    import requests

    assert_safe(url)
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "Estorides/1.0 (+osint platform)"},
        stream=True,
    )
    response.raise_for_status()
    chunks: list[bytes] = []
    total = 0
    for chunk in response.iter_content(chunk_size=1 << 20):
        if not chunk:
            continue
        total += len(chunk)
        if total > max_bytes:
            raise DataPackError(f"pack at {url} exceeds {max_bytes} bytes")
        chunks.append(chunk)
    return b"".join(chunks)


def load_pack(
    name: str,
    url: str,
    parse: Callable[[bytes], Any],
    *,
    cache_path: Path | None = None,
    ttl_s: int = DEFAULT_TTL_S,
    max_bytes: int = DEFAULT_MAX_BYTES,
    expected_sha256: Any = None,
    timeout: int = DEFAULT_TIMEOUT_S,
    use_cache: bool = True,
) -> Any | None:
    """Return a parsed reference pack, fetching it when the cache is stale.

    ``parse`` receives the raw bytes and returns whatever the caller
    wants cached (a list of rows, a dict, ...). Failure modes all degrade
    to "serve what we already had":

    * a fresh cache is returned without touching the network,
    * a stale cache is refetched, and if the refetch fails (network,
      size cap, integrity pin, parser error) the stale payload is
      returned anyway,
    * with nothing cached at all the answer is ``None`` — callers treat
      that as "feature unavailable", never as "empty dataset".
    """
    path = cache_path or (DATA_PACK_DIR / f"{name}.json")
    pin = normalise_sha256(expected_sha256)
    cached = read_cache(path)
    if (
        use_cache
        and cached is not None
        and cached.fetched_at
        and (time.time() - cached.fetched_at) < max(0, ttl_s)
        and (pin is None or cached.sha256 == pin)
    ):
        return cached.payload

    stale = cached.payload if cached is not None else None
    try:
        raw = fetch_bytes(url, max_bytes=max_bytes, timeout=timeout)
        digest = sha256_hex(raw)
        if pin is not None and digest != pin:
            raise DataPackIntegrityError(
                f"pack {name}: sha256 {digest} does not match the pinned {pin}"
            )
        payload = parse(raw)
    except Exception as e:  # the layer must survive a bad download
        log.warning("pack %s unavailable: %s", name, e)
        return stale
    if payload is None:
        return stale
    write_cache(path, payload, digest)
    return payload
