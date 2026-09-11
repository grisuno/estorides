"""
estorides_core.ids
==================
Deterministic content-addressed identifiers.

Six modules (fusion_store, entity_resolution, recon_fusion,
change_detection, hypothesis_engine, target_management) each hand-rolled the
same `sha1(payload.encode("utf-8"), usedforsecurity=False).hexdigest()[:16]`
idiom. SHA-1 here is a content hash for deduplication, **not** a security
primitive, hence `usedforsecurity=False` (also silences FIPS-mode concerns).

`stable_id` is the single implementation. Callers own the payload shape
(`f"{type}:{normalized}"`, `"|".join([...])`, …) so existing ids are
byte-for-byte preserved.
"""
from __future__ import annotations

import hashlib


def stable_id(payload: str, length: int = 16) -> str:
    """Deterministic hex id of `length` chars for a UTF-8 payload."""
    digest = hashlib.sha1(
        payload.encode("utf-8"), usedforsecurity=False
    ).hexdigest()
    return digest[:length]


__all__ = ["stable_id"]
