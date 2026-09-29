"""
estorides_core.case_crypto
==========================
Opt in field encryption for case notes and analysis at rest.

I read a Fernet key from ESTORIDES_CASE_KEY only. Absent, malformed
or missing backend means disabled and plaintext. I never raise on
crypto failure and I never log the key.
"""
from __future__ import annotations

import logging
import os
from typing import Any

log = logging.getLogger("estorides.case_crypto")


def _load_fernet() -> Any | None:
    """Return a Fernet instance when configured and available else None."""
    key = os.environ.get("ESTORIDES_CASE_KEY", "").strip()
    if not key:
        return None
    try:
        from cryptography.fernet import Fernet
    except ImportError:
        log.warning("case crypto disabled: cryptography package missing")
        return None
    try:
        return Fernet(key.encode("utf-8"))
    except Exception:
        log.warning("case crypto disabled: malformed ESTORIDES_CASE_KEY")
        return None


def crypto_status() -> dict[str, Any]:
    """Report whether field encryption is active and why."""
    key = os.environ.get("ESTORIDES_CASE_KEY", "").strip()
    if not key:
        return {"enabled": False, "backend": "disabled"}
    try:
        from cryptography.fernet import Fernet  # noqa: F401
    except ImportError:
        return {"enabled": False, "backend": "missing"}
    if _load_fernet() is None:
        return {"enabled": False, "backend": "disabled"}
    return {"enabled": True, "backend": "fernet"}


def encrypt_text(plain: str) -> str:
    """Encrypt plain text when enabled else return it unchanged."""
    if not plain:
        return ""
    cipher = _load_fernet()
    if cipher is None:
        return plain
    try:
        token = cipher.encrypt(plain.encode("utf-8"))
        return token.decode("utf-8")  # type: ignore[no-any-return]
    except Exception:
        log.warning("case encrypt failed, storing plaintext")
        return plain


def decrypt_text(token: str) -> str:
    """Decrypt a token, passing through plaintext and errors safely."""
    if not token:
        return ""
    if not token.startswith("gAAAA"):
        return token
    cipher = _load_fernet()
    if cipher is None:
        return token
    try:
        raw = cipher.decrypt(token.encode("utf-8"))
        return raw.decode("utf-8")  # type: ignore[no-any-return]
    except Exception:
        log.warning("case decrypt failed")
        return "[decrypt-error]"


__all__ = ["crypto_status", "decrypt_text", "encrypt_text"]
