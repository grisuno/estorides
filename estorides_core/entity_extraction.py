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
    # New field: a list of source names that have observed this entity.
    # Populated by `merge()` to make "seen in N places" a first-class
    # property of the entity instead of a hidden side-channel.
    sources: List[str] = field(default_factory=list)

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
                    sources=[source],
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
    """Deduplicate by (type, value) and merge sources / contexts.

    Two entities with the same (type, value) collapse into a single
    record. Their `sources` lists are unioned (preserving the first
    seen order), `context` is concatenated up to a 200-char window,
    and `confidence` is bumped by 0.1 for each extra observation
    (capped at 1.0) — a simple "corroboration bonus".

    The `sources` field is the canonical "all the places this was
    seen" record. The previous implementation stored it in a
    private attribute (`_src`) that was never serialised and broke
    `asdict()` (TypeError on `dataclasses.asdict` for non-dataclass
    attributes). This version is a real, declared field.

    v1.1: After exact-key dedup, run a second pass with
    `difflib.SequenceMatcher` to catch near-misses like
    `EvilCorp.com` vs `evil-corp.com`. Anything above the
    `FUZZY_THRESHOLD` ratio collapses into a single record.
    Returns the deduped list, with cluster groups available via
    `fuzzy_clusters` if the caller wants them.
    """
    by_key: Dict[Tuple[str, str], Entity] = {}
    for lst in entity_lists:
        for e in lst:
            key = (e.type, e.value.lower())
            if key not in by_key:
                # Fresh entity: copy the source list so the original
                # isn't aliased into the deduped record.
                cloned_sources = list(e.sources) if e.sources else [e.source]
                by_key[key] = Entity(
                    type=e.type,
                    value=e.value,
                    source=e.source,
                    context=e.context,
                    confidence=e.confidence,
                    attributes=dict(e.attributes),
                    sources=cloned_sources,
                )
                continue

            cur = by_key[key]
            # Union the source names into the canonical sources list.
            new_seen = e.sources if e.sources else [e.source]
            for s in new_seen:
                if s not in cur.sources:
                    cur.sources.append(s)
            # Corroboration bonus: each duplicate observation nudges
            # confidence up by 0.1, capped at 1.0.
            cur.confidence = min(1.0, cur.confidence + 0.1)
            # Concatenate unique context snippets, capped at 200 chars.
            if e.context and e.context not in cur.context:
                combined = (cur.context + " | " + e.context).strip(" |")
                cur.context = combined[:200]

    # Cross-source observations are a "you can trust this" signal —
    # expose the source list as an attribute for consumers that
    # serialise via to_dict() and don't want to walk `sources`
    # themselves.
    for e in by_key.values():
        if len(e.sources) > 1:
            e.attributes["also_seen_in"] = list(e.sources)

    # ---- Fuzzy second pass (v1.1) ----
    # Group entities of the same type by close-string similarity
    # using stdlib difflib so we don't add a hard dep on rapidfuzz.
    # The threshold is conservative: catches `EvilCorp.com` vs
    # `evilcorp.com` (ratio = 1.0 case-insensitive) and
    # `EvilCorp.com` vs `evil-corp.com` (ratio ~ 0.92) but not
    # `evilcorp.com` vs `apple.com` (ratio ~ 0.42).
    out: List[Entity] = list(by_key.values())
    try:
        out = _fuzzy_cluster(out)
    except Exception:  # noqa: BLE001
        # Fuzzy pass is best-effort; an exact-key dedup is still
        # a valid result.
        pass
    return out


# v1.1 — fuzzy clustering threshold. 0.85 catches typos and
# hyphen/underscore variants without collapsing distinct
# organisations.
FUZZY_THRESHOLD: float = 0.85


def _fuzzy_cluster(entities: List[Entity]) -> List[Entity]:
    """Group entities of the same type by string similarity and merge.

    Uses `difflib.SequenceMatcher.ratio()`. We compare normalised
    (lowercased, hyphen-stripped) forms so `evil-corp.com` and
    `evilcorp.com` collide cleanly. Only domain / email / person /
    org types are eligible — IPs, hashes, and CVEs have exact
    semantics where fuzzy would be a bug, not a feature."""
    import difflib
    eligible_types = {"domain", "email", "person", "org"}
    by_type: Dict[str, List[Entity]] = {}
    for e in entities:
        if e.type in eligible_types:
            by_type.setdefault(e.type, []).append(e)
    non_fuzzy = [e for e in entities if e.type not in eligible_types]

    merged: List[Entity] = []
    for ent_type, items in by_type.items():
        # Union-find by ratio.
        parent: Dict[int, int] = {i: i for i in range(len(items))}

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        def norm(v: str) -> str:
            return v.lower().replace("-", "").replace("_", "").replace(".", "")

        keys = [norm(e.value) for e in items]
        # O(n^2) is fine for the per-run entity list (cap ~hundreds).
        # The orchestrator's co-occurrence cap keeps each run small.
        n = len(keys)
        for i in range(n):
            for j in range(i + 1, n):
                if not keys[i] or not keys[j]:
                    continue
                r = difflib.SequenceMatcher(None, keys[i], keys[j]).ratio()
                if r >= FUZZY_THRESHOLD:
                    union(i, j)
        # Collapse by cluster.
        clusters: Dict[int, List[int]] = {}
        for i in range(n):
            clusters.setdefault(find(i), []).append(i)
        for ids in clusters.values():
            if len(ids) == 1:
                merged.append(items[ids[0]])
                continue
            # Merge: keep the shortest, most-observed value as canonical.
            canon = min((items[i] for i in ids),
                        key=lambda e: (len(e.sources), len(e.value)))
            seen_sources: List[str] = []
            for i in ids:
                for s in (items[i].sources or [items[i].source]):
                    if s not in seen_sources:
                        seen_sources.append(s)
            canon.sources = seen_sources
            canon.confidence = min(1.0, canon.confidence + 0.05 * (len(ids) - 1))
            # Record what got collapsed so the analyst can audit.
            merged_aliases = sorted({items[i].value for i in ids if items[i].value != canon.value})
            if merged_aliases:
                canon.attributes["fuzzy_aliases"] = merged_aliases
            merged.append(canon)
    return merged + non_fuzzy
