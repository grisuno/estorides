"""
estorides_core.validation
=========================
Input validation for free-form queries.

OSINT platforms ingest user-controlled text and turn it into network
requests. A bare string is a free pass for: control characters, billion-
laughing-doesn't-laugh payloads, ReDoS-inducing regex inputs, billion-
byte blobs, and "clever" Unicode lookalikes that break downstream
parsers. This module is the first line of defence: every public entry
point (`api_run`, the CLI `run` subcommand) should pass the user query
through `validate_query` before it touches a source.

Rules:

  * Trim, collapse internal whitespace, strip control chars.
  * Cap length: 1-512 chars. Long enough for an indictment, short
    enough that no single run can become a DoS.
  * Reject ASCII control chars (except space, tab).
  * Reject Unicode bidi overrides (U+202A-202E, U+2066-2069) — these
    are the classic "swap the file extension" phishing trick and they
    have no business in an OSINT query.
  * Detect query type via the existing detector and require it to be
    one of the recognised shapes; reject anything that smells like a
    free-form text dump.
  * Return a typed `Query` object so callers don't have to redo the
    detection step.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Optional

from .entity_extraction import detect_query_type

# Match ASCII control chars except tab (\x09), LF (\x0a), CR (\x0d).
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# Unicode bidi overrides — used in filename-spoofing attacks, never
# legitimate in an OSINT query.
_BIDI_OVERRIDE_RE = re.compile(r"[\u202a-\u202e\u2066-\u2069]")

# Allowed types: these are the typed handles the rest of the engine
# knows how to dispatch on. "username" is included for handles like
# "@jane_doe" once the @ is stripped.
_ALLOWED_TYPES: frozenset[str] = frozenset((
    "ipv4", "ipv6", "url", "email", "btc_address", "eth_address",
    "md5", "sha1", "sha256", "cve", "asn", "domain", "username",
    "phone", "keyword",  # 'keyword' is for free-form text searches
))


class QueryValidationError(ValueError):
    """Raised when a query fails validation. The reason is in `.reason`."""
    def __init__(self, reason: str, message: str = "") -> None:
        super().__init__(message or reason)
        self.reason = reason


@dataclass(frozen=True)
class Query:
    """A validated, normalised query string."""
    raw: str          # what the user typed
    normalised: str   # after trim + collapse
    type: str         # detect_query_type output

    def __str__(self) -> str:
        return self.normalised


def _strip_and_collapse(text: str) -> str:
    # Normalise to NFC so visually-identical Unicode that compiles to
    # different codepoints (e.g. composed vs decomposed é) collapses
    # to one form. The detection regexes then match consistently.
    text = unicodedata.normalize("NFC", text)
    text = _CONTROL_CHAR_RE.sub("", text)
    text = _BIDI_OVERRIDE_RE.sub("", text)
    # Collapse internal whitespace runs to a single space and trim.
    text = " ".join(text.split())
    return text.strip()


def validate_query(raw: str, *, max_length: int = 512) -> Query:
    """Validate and normalise a user query string.

    Args:
        raw: the user-supplied query, exactly as received.
        max_length: hard cap on the normalised length. Default 512.

    Raises:
        QueryValidationError if the query is empty, oversized, contains
        forbidden characters, or resolves to a type the engine cannot
        dispatch on.

    Returns:
        A `Query` with the normalised text and detected type.
    """
    if raw is None:
        raise QueryValidationError("empty", "query is required")

    normalised = _strip_and_collapse(raw)
    if not normalised:
        raise QueryValidationError("empty", "query is empty after normalisation")

    # If the input had any forbidden characters we stripped, the
    # cleaned form might look like a legitimate domain — but the
    # original was adversarial. Reject the input outright so the
    # normalisation never silently "fixes" a payload.
    if _CONTROL_CHAR_RE.search(raw) or _BIDI_OVERRIDE_RE.search(raw):
        raise QueryValidationError(
            "forbidden-characters",
            "query contains control or bidi-override characters",
        )

    if len(normalised) > max_length:
        raise QueryValidationError(
            "too-long",
            f"query length {len(normalised)} exceeds max {max_length}",
        )

    qtype = detect_query_type(normalised)
    if qtype == "empty":
        raise QueryValidationError("empty", "query resolved to empty type")
    if qtype not in _ALLOWED_TYPES:
        # 'empty' is filtered above, so anything that isn't in the
        # allow-list is either a free-form name we couldn't classify
        # or a junk token; both are rejected at the API surface.
        raise QueryValidationError(
            "unsupported-type",
            f"query type {qtype!r} is not dispatchable",
        )

    return Query(raw=raw, normalised=normalised, type=qtype)
