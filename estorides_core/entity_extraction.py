"""
estorides_core.entity_extraction
================================
Single source of truth for finding entities (IPs, domains, emails, CVEs,
crypto addresses, etc.) anywhere in any JSON / text response.

This is the function that turns a wall of OSINT JSON into nodes
the knowledge graph can wire up.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .config import (DOMAIN_BLACKLIST, ENTITY_MAX_PER_TYPE,
                     ENTITY_MAX_SCAN_CHARS, ENTITY_REGEX)


@dataclass
class Entity:
    type: str
    value: str
    source: str                # the OSINT source that produced it
    context: str = ""          # ~80 chars of surrounding text
    confidence: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Pre-compile every pattern once.
_COMPILED: Dict[str, re.Pattern[str]] = {
    name: re.compile(pat) for name, pat in ENTITY_REGEX.items()
}


# Type detection of a free-form query — used to auto-skip sources that
# cannot meaningfully process the target. This is the difference between
# "national state level" and "fire 90 sources blindly".
_QUERY_TYPE_PATTERNS: List[Tuple[str, re.Pattern[str]]] = [
    ("ipv4", re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")),
    ("ipv6", re.compile(r"^[0-9a-fA-F:]+::?[\w:]+$")),
    ("url", re.compile(r"^https?://", re.IGNORECASE)),
    ("email", re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")),
    ("btc_address", re.compile(r"^(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{11,71})$")),
    ("eth_address", re.compile(r"^0x[a-fA-F0-9]{40}$")),
    ("md5", re.compile(r"^[a-fA-F0-9]{32}$")),
    ("sha1", re.compile(r"^[a-fA-F0-9]{40}$")),
    ("sha256", re.compile(r"^[a-fA-F0-9]{64}$")),
    ("cve", re.compile(r"^CVE-\d{4}-\d{4,7}$", re.IGNORECASE)),
    ("asn", re.compile(r"^AS\d+$", re.IGNORECASE)),
    ("user_agent", re.compile(r"^Mozilla/\d", re.IGNORECASE)),
]


def detect_query_type(query: str) -> str:
    """Return the detected type of a free-form query.

    Falls back to 'domain' for anything that looks like a hostname
    (contains a dot, no spaces), and to 'keyword' for everything else."""
    q = (query or "").strip()
    if not q:
        return "empty"
    for type_name, pat in _QUERY_TYPE_PATTERNS:
        if pat.match(q):
            return type_name
    if " " in q:
        return "keyword"
    if "." in q:
        return "domain"
    return "username"


_VALID_DOMAIN_RE: re.Pattern[str] = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")


def _is_valid_domain(candidate: str) -> bool:
    cand = candidate.lower().rstrip(".")
    if cand in DOMAIN_BLACKLIST:
        return False
    # all-numeric labels with one dot = IPv4 misfire
    parts = cand.split(".")
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        return False
    if not _VALID_DOMAIN_RE.match(cand):
        return False
    return True


def _context(text: str, start: int, end: int, window: int = 40) -> str:
    a = max(0, start - window)
    b = min(len(text), end + window)
    return text[a:b].replace("\n", " ").strip()


def extract_from_text(
    text: str,
    source: str,
    *,
    types: Optional[List[str]] = None,
) -> List[Entity]:
    """Find every recognised entity in a raw text blob.

    `types` optionally restricts which kinds of entity to look for.
    """
    if not text:
        return []
    # Hard cap on how much text any single pattern scans. A 5 MB crt.sh dump
    # multiplied by 17 patterns plus per-match validation is what used to pin a
    # core for ~80 seconds; truncation makes the stage bounded and predictable.
    if len(text) > ENTITY_MAX_SCAN_CHARS:
        text = text[:ENTITY_MAX_SCAN_CHARS]
    out: List[Entity] = []
    active = types or list(_COMPILED.keys())
    seen: set[Tuple[str, str]] = set()

    for ent_type in active:
        pat = _COMPILED.get(ent_type)
        if pat is None:
            continue
        kept = 0
        for m in pat.finditer(text):
            if kept >= ENTITY_MAX_PER_TYPE:
                break
            raw = m.group(0)
            if ent_type == "domain" and not _is_valid_domain(raw):
                continue
            if ent_type in ("ipv4", "ipv6") and not _ip_in_textual_context(text, m.start()):
                # avoid matching version numbers and timestamps
                continue
            key = (ent_type, raw.lower())
            if key in seen:
                continue
            seen.add(key)
            kept += 1
            out.append(
                Entity(
                    type=ent_type,
                    value=raw,
                    source=source,
                    context=_context(text, m.start(), m.end()),
                )
            )
    return out


def _ip_in_textual_context(text: str, idx: int) -> bool:
    """Heuristic: only count a numeric match as an IP if it isn't part of a
    version number or timestamp (preceded/followed by `version`, `v`, or `:`)."""
    before = text[max(0, idx - 12):idx]
    after = text[idx:idx + 32]
    bad_before = re.search(r"v(?:ersion)?[\s=:_-]?$", before, re.IGNORECASE)
    bad_after = re.match(r"^\d{1,2}:\d{2}:\d{2}", after)  # timestamp
    return not (bad_before or bad_after)


def extract_from_json(
    payload: Any,
    source: str,
    *,
    types: Optional[List[str]] = None,
) -> List[Entity]:
    """Pull entities out of a JSON-like structure.

    Earlier this recursed into every string and ran all patterns on each one,
    so a response with thousands of entries (crt.sh subdomains, wayback URLs)
    triggered hundreds of thousands of regex passes. We now flatten the payload
    to a single capped string and scan it once; entities span keys and values
    just as well, and the cost is bounded by `extract_from_text`."""
    if payload is None:
        return []
    if isinstance(payload, (int, float, bool)):
        return []
    if isinstance(payload, str):
        text = payload
    else:
        try:
            text = json.dumps(payload, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            text = str(payload)
    return extract_from_text(text, source, types=types)


def merge(*entity_lists: Iterable[Entity]) -> List[Entity]:
    """Deduplicate by (type, value) and merge attributes."""
    by_key: Dict[Tuple[str, str], Entity] = {}
    for lst in entity_lists:
        for e in lst:
            key = (e.type, e.value.lower())
            if key not in by_key:
                by_key[key] = Entity(
                    type=e.type, value=e.value, source=e.source,
                    context=e.context, confidence=e.confidence,
                    attributes=dict(e.attributes),
                )
            else:
                cur = by_key[key]
                cur.sources = getattr(cur, "sources", [cur.source])  # type: ignore[attr-defined]
                # gather all source names
                if not hasattr(cur, "_src"):
                    cur._src = {cur.source}  # type: ignore[attr-defined]
                cur._src.add(e.source)  # type: ignore[attr-defined]
                cur.confidence = min(1.0, cur.confidence + 0.1)
                if e.context and e.context not in cur.context:
                    cur.context = (cur.context + " | " + e.context)[:200]
    out: List[Entity] = []
    for e in by_key.values():
        srcs = sorted(getattr(e, "_src", {e.source}))
        if len(srcs) > 1:
            e.attributes["also_seen_in"] = srcs
        out.append(e)
    return out
