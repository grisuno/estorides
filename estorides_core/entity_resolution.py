"""
estorides_core.entity_resolution
================================
Canonical identity layer.

The v1.1 engine collapsed near-duplicate entities with a single
``difflib.SequenceMatcher`` ratio at 0.85. That is fine for typo folding
but it is not entity resolution: it has no stable identifier, no blocking
(so it is quietly O(n^2) over the whole entity list), no notion of which
match was deterministic versus a guess, and no cross-script awareness, so
``Владимир Путин`` and ``Vladimir Putin`` stay two unrelated nodes.

This module is the replacement. For a per-run list of :class:`Entity`
records it produces a list of :class:`CanonicalEntity` records, each with:

* a **stable canonical id** derived from a type-aware normalised form, so
  the same real-world entity gets the same id on every run (and, with the
  persistent store, across runs);
* **blocked, scored matching** — exact normalised equality is a
  deterministic merge; close-but-not-equal pairs inside the same blocking
  bucket are scored with Jaro-Winkler (and a cross-script consonant
  skeleton booster) and either merged or surfaced as a ``SAME_AS``
  candidate link, never silently fused;
* **provenance** — the sources, original surface forms (aliases), scripts,
  and the match method/score that justified each merge.

Deterministic types (IP, hash, CVE, ASN, crypto address) never fuzzy
match: for those, equality of the normalised form is the only merge rule,
because a one-character difference is a different host, file, or wallet.

The engine is stdlib-only. The optional cross-run identity store lives in
:mod:`estorides_core.entity_store` and is wired in by the resolver when
``ER_PERSIST`` is set.
"""
from __future__ import annotations

import hashlib
import ipaddress
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .config import (ER_LINK_THRESHOLD, ER_MAX_BUCKET, ER_MERGE_THRESHOLD)
from .entity_extraction import Entity
from .transliteration import consonant_skeleton, is_non_latin, to_latin

# Types whose identity is exact: a single differing character denotes a
# different object, so they are merged only on normalised equality.
DETERMINISTIC_TYPES: frozenset = frozenset({
    "ipv4", "ipv6", "ip", "md5", "sha1", "sha256", "sha512", "hash",
    "cve", "asn", "btc_address", "eth_address", "mac",
})

# Types eligible for probabilistic (name/string-similarity) matching.
FUZZY_TYPES: frozenset = frozenset({
    "domain", "email", "person", "org", "organization", "username", "keyword",
})

# Of the fuzzy types, only these are auto-*merged* into one identity when a
# pair clears the merge threshold. The rest are exact identifiers (a domain
# or an email address denotes one specific resource), so a near match is
# surfaced as a SAME_AS candidate link for an analyst to adjudicate, never
# fused. This is the difference between "looks alike" and "is the same".
MERGE_ELIGIBLE_TYPES: frozenset = frozenset({
    "person", "org", "organization", "username", "keyword",
})

# Common organisation suffixes stripped before matching so that
# "Evil Corp" and "Evil Corp LLC" share a normalised form.
_ORG_SUFFIXES: frozenset = frozenset({
    "llc", "inc", "incorporated", "ltd", "limited", "corp", "corporation",
    "co", "company", "gmbh", "ag", "sa", "srl", "bv", "plc", "llp", "lp",
    "group", "holdings", "holding", "ooo", "pao", "oao", "zao",
})

_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)
_WS_RE = re.compile(r"\s+", re.UNICODE)


# --------------------------------------------------------------------------
# String similarity (pure Python; no rapidfuzz dependency)
# --------------------------------------------------------------------------
def jaro(s1: str, s2: str) -> float:
    """Return the Jaro similarity of two strings in ``[0, 1]``."""
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0
    match_distance = max(len1, len2) // 2 - 1
    if match_distance < 0:
        match_distance = 0
    s1_matches = [False] * len1
    s2_matches = [False] * len2
    matches = 0
    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break
    if matches == 0:
        return 0.0
    transpositions = 0
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1
    transpositions //= 2
    return (
        matches / len1
        + matches / len2
        + (matches - transpositions) / matches
    ) / 3.0


def jaro_winkler(s1: str, s2: str, prefix_weight: float = 0.1) -> float:
    """Jaro-Winkler similarity: Jaro with a shared-prefix bonus.

    The prefix bonus (up to 4 leading characters) rewards strings that
    agree at the start, which is the common shape of name and domain
    variants. ``prefix_weight`` is capped at 0.25 to keep the result in
    ``[0, 1]``.
    """
    j = jaro(s1, s2)
    prefix = 0
    for a, b in zip(s1, s2):
        if a == b:
            prefix += 1
            if prefix == 4:
                break
        else:
            break
    return j + prefix * min(prefix_weight, 0.25) * (1 - j)


def _soundex(token: str) -> str:
    """Return a 4-character Soundex code for a Latin token.

    Used only as a blocking key: it groups phonetically similar tokens so
    the expensive pairwise scorer runs on plausible candidates rather than
    the whole list. Empty or non-alphabetic input yields ``"0000"``.
    """
    token = "".join(ch for ch in token.lower() if ch.isalpha())
    if not token:
        return "0000"
    codes = {
        "b": "1", "f": "1", "p": "1", "v": "1",
        "c": "2", "g": "2", "j": "2", "k": "2", "q": "2",
        "s": "2", "x": "2", "z": "2",
        "d": "3", "t": "3", "l": "4",
        "m": "5", "n": "5", "r": "6",
    }
    first = token[0].upper()
    encoded = first
    prev = codes.get(token[0], "")
    for ch in token[1:]:
        code = codes.get(ch, "")
        if code and code != prev:
            encoded += code
        if ch not in "hw":
            prev = code
    return (encoded + "000")[:4]


# --------------------------------------------------------------------------
# Type-aware normalisation
# --------------------------------------------------------------------------
def _normalize_domain(value: str) -> str:
    v = value.strip().lower()
    v = re.sub(r"^[a-z]+://", "", v)
    v = v.split("/")[0].split("?")[0]
    if v.startswith("www."):
        v = v[4:]
    return v.rstrip(".")


def _normalize_name(value: str, *, strip_suffixes: bool) -> str:
    """Order-independent transliterated key for persons and orgs.

    The surface form is transliterated to Latin, punctuation dropped, and
    the tokens sorted, so ``"Putin, Vladimir"`` and ``"Владимир Путин"``
    converge on the same normalised string and merge deterministically.
    Cross-script spellings that survive transliteration with different
    vowels (abjad scripts) are caught later by the skeleton scorer.
    """
    latin = to_latin(value)
    latin = _PUNCT_RE.sub(" ", latin)
    tokens = [t for t in _WS_RE.split(latin) if t]
    if strip_suffixes:
        stripped = [t for t in tokens if t not in _ORG_SUFFIXES]
        if stripped:
            tokens = stripped
    return " ".join(sorted(tokens))


def normalize_value(etype: str, value: str) -> str:
    """Return the canonical normalised form of an entity value.

    The normalised form is the merge key for deterministic types and the
    seed of the stable canonical id for every type. It is intentionally
    lossy (case, ordering, ornament removed) but never collapses distinct
    objects of a deterministic type.
    """
    if value is None:
        return ""
    v = value.strip()
    if not v:
        return ""
    if etype in ("ipv4", "ipv6", "ip"):
        try:
            return str(ipaddress.ip_address(v))
        except ValueError:
            return v.lower()
    if etype in ("md5", "sha1", "sha256", "sha512", "hash", "eth_address", "mac"):
        return v.lower()
    if etype == "cve":
        return v.upper()
    if etype == "asn":
        digits = re.sub(r"(?i)^as", "", v)
        return f"AS{digits}" if digits.isdigit() else v.upper()
    if etype == "btc_address":
        return v
    if etype == "domain":
        return _normalize_domain(v)
    if etype == "email":
        return v.lower()
    if etype == "username":
        return v.lstrip("@").lower()
    if etype in ("person",):
        return _normalize_name(v, strip_suffixes=False)
    if etype in ("org", "organization"):
        return _normalize_name(v, strip_suffixes=True)
    return to_latin(v) or v.lower()


def canonical_id(etype: str, normalized: str) -> str:
    """Stable, content-addressed id for a normalised entity.

    Same ``(type, normalized)`` always yields the same id, so a canonical
    entity keeps its identity for as long as its normalised form is stable.
    The persistent store additionally maps known aliases onto an existing
    id so a never-before-seen surface form still resolves to the same node.
    """
    digest = hashlib.sha1(f"{etype}:{normalized}".encode("utf-8")).hexdigest()
    return f"{etype}:{digest[:16]}"


def blocking_keys(etype: str, normalized: str, value: str) -> List[str]:
    """Return the blocking keys that bucket an entity for comparison.

    Two entities are only ever scored against each other if they share at
    least one blocking key. The keys are chosen to be high-recall (so true
    matches land together) while keeping buckets small enough that the
    in-bucket pairwise scan stays cheap.
    """
    if not normalized:
        return []
    if etype == "domain":
        labels = normalized.split(".")
        registrable = ".".join(labels[-2:]) if len(labels) >= 2 else normalized
        # Second key folds out hyphens/dots so look-alike registrations
        # ("evil-corp.com" vs "evilcorp.com") land in one bucket and get
        # scored, surfacing as a link even though they never auto-merge.
        flattened = re.sub(r"[^a-z0-9]", "", registrable)
        return [f"dom:{registrable}", f"dom~:{flattened}"]
    if etype == "email":
        local, _, domain = normalized.partition("@")
        return [f"eml:{domain}:{local[:2]}"]
    if etype == "username":
        return [f"usr:{normalized[:4]}"]
    if etype in ("person", "org", "organization"):
        keys: List[str] = []
        for token in normalized.split():
            keys.append(f"nm:{_soundex(token)}")
        skel = consonant_skeleton(value)
        if skel:
            keys.append(f"sk:{skel[:4]}")
        return keys or [f"nm:{normalized[:4]}"]
    return [f"{etype}:{normalized}"]


# --------------------------------------------------------------------------
# Pairwise scoring
# --------------------------------------------------------------------------
@dataclass
class MatchScore:
    """The result of comparing two entity values of the same type."""

    score: float
    method: str


def score_pair(etype: str, a_value: str, b_value: str,
               a_norm: str, b_norm: str) -> MatchScore:
    """Score how likely two same-type entities denote the same object.

    Deterministic types return 1.0 only on normalised equality and 0.0
    otherwise. Fuzzy types layer Jaro-Winkler over the normalised form with
    a cross-script consonant-skeleton booster for names, so a Cyrillic and
    a Latin spelling of one person can clear the link bar even when their
    transliterated vowels differ.
    """
    if a_norm and a_norm == b_norm:
        return MatchScore(1.0, "exact")
    if etype in DETERMINISTIC_TYPES:
        return MatchScore(0.0, "deterministic_mismatch")

    base = jaro_winkler(a_norm, b_norm)
    method = "jaro_winkler"

    if etype in ("person", "org", "organization"):
        skel_a = consonant_skeleton(a_value)
        skel_b = consonant_skeleton(b_value)
        if skel_a and skel_a == skel_b:
            boosted = max(base, 0.94)
            if boosted > base:
                base = boosted
                method = "consonant_skeleton"
        elif skel_a and skel_b:
            skel_sim = jaro_winkler(skel_a, skel_b)
            if skel_sim > base:
                base = (base + skel_sim) / 2.0
                method = "skeleton_jaro"

    return MatchScore(base, method)


# --------------------------------------------------------------------------
# Canonical entity + resolution result
# --------------------------------------------------------------------------
@dataclass
class CanonicalEntity:
    """A resolved identity fused from one or more observed entities."""

    canonical_id: str
    type: str
    value: str
    normalized: str
    confidence: float = 1.0
    sources: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    member_count: int = 1
    match_method: str = "exact"
    match_score: float = 1.0
    attributes: Dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        return {
            "canonical_id": self.canonical_id,
            "type": self.type,
            "value": self.value,
            "normalized": self.normalized,
            "confidence": round(self.confidence, 4),
            "sources": list(self.sources),
            "aliases": list(self.aliases),
            "scripts": list(self.scripts),
            "member_count": self.member_count,
            "match_method": self.match_method,
            "match_score": round(self.match_score, 4),
            "attributes": dict(self.attributes),
        }

    def to_entity(self) -> Entity:
        """Project back onto the legacy :class:`Entity` shape.

        Lets the resolver drop into the existing orchestrator, knowledge
        graph, and case-store paths without changing their interfaces while
        carrying the new identity metadata in ``attributes``.
        """
        attrs = dict(self.attributes)
        attrs.update({
            "canonical_id": self.canonical_id,
            "aliases": list(self.aliases),
            "scripts": list(self.scripts),
            "match_method": self.match_method,
            "match_score": round(self.match_score, 4),
            "member_count": self.member_count,
        })
        return Entity(
            type=self.type,
            value=self.value,
            source=self.sources[0] if self.sources else "",
            context="",
            confidence=self.confidence,
            attributes=attrs,
            sources=list(self.sources),
        )


@dataclass
class SameAsLink:
    """A suggested-but-unmerged identity link between two canonical ids."""

    left: str
    right: str
    score: float
    method: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "left": self.left,
            "right": self.right,
            "score": round(self.score, 4),
            "method": self.method,
        }


@dataclass
class ResolutionResult:
    """Output of a resolve() call: fused entities plus candidate links."""

    entities: List[CanonicalEntity]
    same_as: List[SameAsLink] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "entities": [e.to_dict() for e in self.entities],
            "same_as": [l.to_dict() for l in self.same_as],
        }


class _UnionFind:
    """Disjoint-set over integer indices with path compression."""

    def __init__(self, n: int) -> None:
        self._parent = list(range(n))

    def find(self, x: int) -> int:
        while self._parent[x] != x:
            self._parent[x] = self._parent[self._parent[x]]
            x = self._parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self._parent[max(ra, rb)] = min(ra, rb)


def _script_of(value: str) -> str:
    return "non-latin" if is_non_latin(value) else "latin"


class EntityResolver:
    """Resolve a per-run entity list into canonical identities.

    The resolver is deliberately stateless across calls by default; pass a
    store (see :mod:`estorides_core.entity_store`) to make canonical ids
    stable across runs. A single :meth:`resolve` call:

    1. exact-merges entities sharing a ``(type, normalized)`` key;
    2. blocks the remaining fuzzy-eligible groups and scores in-bucket
       pairs, unioning clusters at or above the merge threshold and
       recording ``SAME_AS`` candidates above the link threshold;
    3. emits one :class:`CanonicalEntity` per cluster with a deterministic
       representative and full provenance.
    """

    def __init__(
        self,
        *,
        merge_threshold: float = ER_MERGE_THRESHOLD,
        link_threshold: float = ER_LINK_THRESHOLD,
        max_bucket: int = ER_MAX_BUCKET,
        store: Optional[object] = None,
    ) -> None:
        self.merge_threshold = merge_threshold
        self.link_threshold = link_threshold
        self.max_bucket = max_bucket
        self.store = store

    def resolve(self, entities: List[Entity]) -> ResolutionResult:
        """Resolve ``entities`` into canonical identities and links."""
        if not entities:
            return ResolutionResult(entities=[])

        records = self._build_records(entities)
        uf = _UnionFind(len(records))
        self._exact_merge(records, uf)
        link_candidates = self._fuzzy_merge(records, uf)
        canonicals, root_to_cid = self._materialise(records, uf)
        if self.store is not None:
            canonicals = self._reconcile_with_store(canonicals)
        same_as = self._build_links(link_candidates, uf, root_to_cid)
        return ResolutionResult(entities=canonicals, same_as=same_as)

    # -- internals --------------------------------------------------------
    def _build_records(self, entities: List[Entity]) -> List[Dict[str, object]]:
        records: List[Dict[str, object]] = []
        for ent in entities:
            etype = ent.type
            norm = normalize_value(etype, ent.value)
            records.append({
                "entity": ent,
                "type": etype,
                "value": ent.value,
                "norm": norm,
                "block": blocking_keys(etype, norm, ent.value),
            })
        return records

    @staticmethod
    def _exact_merge(records: List[Dict[str, object]], uf: _UnionFind) -> None:
        first_by_key: Dict[Tuple[str, str], int] = {}
        for idx, rec in enumerate(records):
            key = (rec["type"], rec["norm"])
            if not rec["norm"]:
                continue
            anchor = first_by_key.get(key)
            if anchor is None:
                first_by_key[key] = idx
            else:
                uf.union(anchor, idx)

    def _fuzzy_merge(self, records: List[Dict[str, object]],
                     uf: _UnionFind) -> List[Tuple[int, int, MatchScore]]:
        """Block, score, merge at threshold, and collect link candidates.

        Merges (union) happen eagerly as pairs clear the merge bar. Pairs
        that only clear the lower link bar are returned as ``(a, b, score)``
        index triples for the caller to translate into canonical-id links
        once clusters are materialised.
        """
        buckets: Dict[str, List[int]] = {}
        for idx, rec in enumerate(records):
            if rec["type"] not in FUZZY_TYPES or not rec["norm"]:
                continue
            for key in rec["block"]:
                buckets.setdefault(key, []).append(idx)

        candidates: List[Tuple[int, int, MatchScore]] = []
        for members in buckets.values():
            if len(members) < 2:
                continue
            capped = members[: self.max_bucket]
            for i in range(len(capped)):
                for j in range(i + 1, len(capped)):
                    a, b = capped[i], capped[j]
                    if uf.find(a) == uf.find(b):
                        continue
                    rec_a, rec_b = records[a], records[b]
                    if rec_a["type"] != rec_b["type"]:
                        continue
                    ms = score_pair(
                        rec_a["type"], rec_a["value"], rec_b["value"],
                        rec_a["norm"], rec_b["norm"],
                    )
                    mergeable = rec_a["type"] in MERGE_ELIGIBLE_TYPES
                    if mergeable and ms.score >= self.merge_threshold:
                        uf.union(a, b)
                    elif ms.score >= self.link_threshold:
                        candidates.append((a, b, ms))
        return candidates

    @staticmethod
    def _build_links(
        candidates: List[Tuple[int, int, MatchScore]],
        uf: _UnionFind,
        root_to_cid: Dict[int, str],
    ) -> List[SameAsLink]:
        """Translate index-pair link candidates into canonical-id links.

        Pairs whose clusters ended up merged (a later, stronger edge pulled
        them together) are dropped; the rest are deduplicated per
        canonical-id pair, keeping the highest-scoring justification.
        """
        best: Dict[Tuple[str, str], MatchScore] = {}
        for a, b, ms in candidates:
            ra, rb = uf.find(a), uf.find(b)
            if ra == rb:
                continue
            cid_a, cid_b = root_to_cid.get(ra), root_to_cid.get(rb)
            if not cid_a or not cid_b or cid_a == cid_b:
                continue
            key = (min(cid_a, cid_b), max(cid_a, cid_b))
            prev = best.get(key)
            if prev is None or ms.score > prev.score:
                best[key] = ms
        return [
            SameAsLink(left=key[0], right=key[1], score=ms.score, method=ms.method)
            for key, ms in best.items()
        ]

    def _materialise(
        self, records: List[Dict[str, object]], uf: _UnionFind
    ) -> Tuple[List[CanonicalEntity], Dict[int, str]]:
        clusters: Dict[int, List[int]] = {}
        for idx in range(len(records)):
            clusters.setdefault(uf.find(idx), []).append(idx)

        out: List[CanonicalEntity] = []
        root_to_cid: Dict[int, str] = {}
        for root, member_ids in clusters.items():
            members = [records[i] for i in member_ids]
            rep = self._representative(members)
            etype = rep["type"]
            norm = rep["norm"]
            cid = canonical_id(etype, norm) if norm else canonical_id(
                etype, rep["value"].lower()
            )

            sources: List[str] = []
            aliases: List[str] = []
            scripts: List[str] = []
            max_conf = 0.0
            best_method = "exact"
            best_score = 1.0 if len(members) == 1 else 0.0
            for rec in members:
                ent: Entity = rec["entity"]
                for s in (ent.sources or [ent.source]):
                    if s and s not in sources:
                        sources.append(s)
                if rec["value"] not in aliases:
                    aliases.append(rec["value"])
                script = _script_of(rec["value"])
                if script not in scripts:
                    scripts.append(script)
                max_conf = max(max_conf, ent.confidence)

            if len(members) > 1:
                best_method, best_score = self._best_internal_match(members)

            extra_sources = max(0, len(sources) - 1)
            confidence = min(1.0, max(max_conf, 0.5) + 0.05 * extra_sources)

            attributes: Dict[str, object] = {}
            non_rep_aliases = [a for a in aliases if a != rep["value"]]
            if non_rep_aliases:
                attributes["also_known_as"] = non_rep_aliases
            if len(scripts) > 1:
                attributes["cross_script"] = True

            out.append(CanonicalEntity(
                canonical_id=cid,
                type=etype,
                value=rep["value"],
                normalized=norm,
                confidence=confidence,
                sources=sources,
                aliases=aliases,
                scripts=scripts,
                member_count=len(members),
                match_method=best_method,
                match_score=best_score,
                attributes=attributes,
            ))
            root_to_cid[root] = cid
        return out, root_to_cid

    @staticmethod
    def _representative(members: List[Dict[str, object]]) -> Dict[str, object]:
        """Pick a stable representative for a cluster.

        Preference order: most corroborated (appears in most sources), then
        a Latin surface form over a non-Latin one (more broadly readable in
        reports), then the lexicographically smallest value. The result is
        deterministic for a given member set, which keeps the canonical id
        stable run to run.
        """
        def rank(rec: Dict[str, object]) -> Tuple[int, int, str]:
            ent: Entity = rec["entity"]
            source_count = len(ent.sources or [ent.source])
            latin_first = 0 if _script_of(rec["value"]) == "latin" else 1
            return (-source_count, latin_first, rec["value"].lower())

        return min(members, key=rank)

    @staticmethod
    def _best_internal_match(members: List[Dict[str, object]]) -> Tuple[str, float]:
        """Return the (method, score) of the strongest non-exact pair.

        Surfaces *why* a multi-member cluster was fused, so the analyst can
        see whether the merge rested on an exact key or a probabilistic
        name match. Bounded to the first handful of members to stay cheap on
        large clusters.
        """
        best_method = "exact"
        best_score = 1.0
        capped = members[:8]
        found_non_exact = False
        for i in range(len(capped)):
            for j in range(i + 1, len(capped)):
                a, b = capped[i], capped[j]
                if a["norm"] and a["norm"] == b["norm"]:
                    continue
                ms = score_pair(
                    a["type"], a["value"], b["value"], a["norm"], b["norm"]
                )
                if not found_non_exact or ms.score > best_score:
                    best_method = ms.method
                    best_score = ms.score
                    found_non_exact = True
        return best_method, best_score

    def _reconcile_with_store(
        self, canonicals: List[CanonicalEntity]
    ) -> List[CanonicalEntity]:
        """Map canonicals onto persisted ids and record their aliases.

        Looked up alias-first so a brand-new surface form of a known entity
        adopts the existing canonical id instead of minting a new one. The
        store call is best-effort: any failure leaves the freshly computed
        id in place rather than aborting the run.
        """
        store = self.store
        for ce in canonicals:
            try:
                existing = store.lookup(ce.type, ce.normalized, ce.aliases)  # type: ignore[attr-defined]
                if existing:
                    ce.canonical_id = existing
                store.upsert(ce)  # type: ignore[attr-defined]
            except Exception:  # noqa: BLE001
                continue
        return canonicals


def resolve_entities(
    entities: List[Entity],
    *,
    store: Optional[object] = None,
) -> ResolutionResult:
    """Module-level convenience wrapper around :class:`EntityResolver`."""
    return EntityResolver(store=store).resolve(entities)
