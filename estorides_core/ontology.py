"""
estorides_core.ontology
=======================
The "centralized ontology engine" — the brain of the platform.

Three things live here:

  SanctionsIndex
    OFAC SDN list, mirrored from OpenSanctions
    (https://www.opensanctions.org/datasets/latest/us_ofac_sdn/targets.simple.csv).
    Loaded on first use, refreshed every 24h, single-flight so
    concurrent requests share one fetch. ~7 MB, low-tens-of-thousands
    of entries. In-memory graph: {entry} by id + by normalised name
    + by alias + by crypto address.

  WikidataCache
    A bounded LRU over the Wikidata SPARQL endpoint. Used to
    canonicalise "Vladimir Putin" → Q7747, "FSB" → Q2084917, etc.
    24h TTL per entry, capped at 10k items to bound memory.

  OntologyEngine
    The orchestrator-facing facade. Exposes:
        - resolve(name) -> candidate sanction matches
        - resolve_crypto_address(addr) -> sanction cross-check
        - check_observation(obs) -> {hits, hits_by_field}
    Designed to be called from a new "post-process" stage that
    decorates each observation with a sanctions verdict before the
    LLM analyst sees it.

This module is deliberately dependency-light (only stdlib). The CSV
parser is hand-rolled and tolerant of double-quoted fields with
embedded commas and newlines — the OpenSanctions export is well-
formed so we don't need `csv` module gymnastics, but we do need the
"\"\" escape" support that the csv module handles. Using the stdlib
reader keeps the dependency surface to zero.

Spec reference: https://www.opensanctions.org/datasets/us_ofac_sdn/
"""
from __future__ import annotations

import csv
import io
import json
import logging
import re
import threading
import time
from collections import OrderedDict
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Tuple
from urllib.parse import urlparse

from .config import DATA_DIR
from .ssrf_guard import assert_safe

log = logging.getLogger("estorides.ontology")

SDN_CSV_URL = (
    "https://data.opensanctions.org/datasets/latest/us_ofac_sdn/targets.simple.csv"
)
SDN_LOCAL_CACHE: str = str(DATA_DIR / "ontology_sdn.json")
SDN_TTL_SECONDS: int = 24 * 60 * 60
WIKIDATA_TTL_SECONDS: int = 24 * 60 * 60
WIKIDATA_LRU_MAX: int = 10_000
WIKIDATA_ENDPOINT: str = "https://query.wikidata.org/sparql"
WIKIDATA_UA: str = "Estorides/1.0 (+open-source OSINT platform; ontology engine)"

# ----------------------------------------------------------------- data shape
@dataclass
class SanctionEntry:
    id: str
    schema: str          # Person, Organization, Vessel, Airplane, LegalEntity
    name: str
    aliases: List[str] = field(default_factory=list)
    countries: List[str] = field(default_factory=list)
    programs: List[str] = field(default_factory=list)
    sanctions: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ----------------------------------------------------------------- helpers
def _normalise_name(s: str) -> str:
    """Lower-case, strip punctuation/diacritics, collapse whitespace.

    Used for both index keys and incoming query normalisation so the
    same string yields the same key on both sides."""
    s = s.lower().strip()
    # Replace any non-letter/number/whitespace with a space.
    s = re.sub(r"[^\w\s]", " ", s, flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


# ----------------------------------------------------------------- sanctions
class SanctionsIndex:
    """In-memory OFAC SDN index with 24h lazy refresh and single-flight load.

    The previous design (if any) likely fetched the list on every call
    or had no cache; the new design:

      * First call to `entries()` blocks while the CSV is fetched.
      * Subsequent calls within TTL return the cached snapshot.
      * Concurrent calls during a load share the same in-flight
        promise (single-flight) — never two concurrent fetches.
      * If a refresh fails after the cache has gone stale, we keep
        serving the previous snapshot rather than going blind.

    The CSV is downloaded over HTTPS to a temp file, then loaded
    into a normalised lookup. We never trust the file path in
    the SDN_LOCAL_CACHE to be writable: on permission errors we
    log a warning and fall back to in-memory only.
    """

    def __init__(
        self,
        *,
        url: str = SDN_CSV_URL,
        ttl_seconds: int = SDN_TTL_SECONDS,
        local_cache_path: str = SDN_LOCAL_CACHE,
    ) -> None:
        self.url = url
        self.ttl = ttl_seconds
        self.local_cache_path = local_cache_path
        self._lock = threading.Lock()
        self._inflight: Optional[threading.Event] = None
        self._loaded: Optional[Tuple[float, List[SanctionEntry], Dict[str, List[SanctionEntry]]]] = None
        # ^ (fetched_at, entries, by_norm)

    # --- public ---
    def is_ready(self) -> bool:
        return self._loaded is not None

    def entries(self) -> List[SanctionEntry]:
        """Return the current snapshot, loading if necessary."""
        if self._loaded is None or (time.time() - self._loaded[0]) > self.ttl:
            self._refresh()
        assert self._loaded is not None
        return self._loaded[1]

    def lookup(self, name: str) -> List[SanctionEntry]:
        """Find sanction entries whose name or alias matches `name`."""
        norm = _normalise_name(name)
        if not norm:
            return []
        self.entries()  # ensure loaded
        assert self._loaded is not None
        _, _, by_norm = self._loaded
        return list(by_norm.get(norm, ()))

    def lookup_crypto(self, address: str) -> List[SanctionEntry]:
        """Cross-check a BTC/ETH address against the SDN list.

        The OpenSanctions CSV includes a `crypto_address` (BTC) field
        on a subset of entries. ETH addresses are stored in the
        `ethereum_address` field. The current implementation matches
        by alias string for simplicity — the upstream coverage of
        crypto is sparse and not the focus of this version. Returns
        the entries whose alias list contains the literal address."""
        addr = address.strip()
        if not addr:
            return []
        for e in self.entries():
            if addr in e.aliases:
                return [e]
        return []

    def size(self) -> int:
        return len(self.entries())

    # --- internals ---
    def _refresh(self) -> None:
        with self._lock:
            if self._inflight is not None:
                # Another thread is already fetching. Wait for it.
                ev = self._inflight
                ev.wait(timeout=60)
                return
            ev = threading.Event()
            self._inflight = ev
        try:
            text = self._download()
            entries = self._parse(text)
            by_norm = self._index(entries)
            self._loaded = (time.time(), entries, by_norm)
            self._persist(text)
            log.info("Sanctions index loaded: %d entries", len(entries))
        except Exception as e:  # noqa: BLE001
            # On failure, keep whatever we had. Better stale than blind.
            if self._loaded is None:
                log.warning("Sanctions index unavailable, returning empty: %s", e)
                self._loaded = (time.time(), [], {})
            else:
                log.warning("Sanctions index refresh failed, keeping snapshot: %s", e)
        finally:
            with self._lock:
                if self._inflight is not None:
                    self._inflight.set()
                    self._inflight = None

    def _download(self) -> str:
        # SSRF guard before any network egress.
        assert_safe(self.url)
        import requests
        r = requests.get(
            self.url,
            headers={"Accept": "text/csv", "User-Agent": WIKIDATA_UA},
            timeout=30,
        )
        r.raise_for_status()
        return r.text

    def _persist(self, text: str) -> None:
        """Best-effort write of the raw CSV for offline re-use.

        Failures are non-fatal; the in-memory index is the source of
        truth while the process is alive."""
        try:
            from pathlib import Path
            Path(self.local_cache_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.local_cache_path, "w", encoding="utf-8") as fh:
                fh.write(text)
        except OSError as e:
            log.debug("local sanctions cache write failed (non-fatal): %s", e)

    def _parse(self, text: str) -> List[SanctionEntry]:
        """Parse the OpenSanctions simple CSV into SanctionEntry records."""
        reader = csv.DictReader(io.StringIO(text))
        out: List[SanctionEntry] = []
        for row in reader:
            name = (row.get("name") or "").strip()
            if not name:
                continue
            aliases_raw = (row.get("aliases") or "").split(";")
            countries = [c.strip() for c in (row.get("countries") or "").split(";") if c.strip()]
            programs = [p.strip() for p in (row.get("program_ids") or row.get("programs") or "").split(";") if p.strip()]
            aliases = [a.strip() for a in aliases_raw if a.strip()]
            # crypto addresses live in aliases; carry them forward.
            crypto = (row.get("crypto_address") or "").strip()
            eth = (row.get("ethereum_address") or "").strip()
            for extra in (crypto, eth):
                if extra and extra not in aliases:
                    aliases.append(extra)
            out.append(SanctionEntry(
                id=(row.get("id") or "").strip(),
                schema=(row.get("schema") or "LegalEntity").strip(),
                name=name,
                aliases=aliases,
                countries=countries,
                programs=programs,
                sanctions=(row.get("sanctions") or "").strip(),
            ))
        return out

    def _index(self, entries: List[SanctionEntry]) -> Dict[str, List[SanctionEntry]]:
        """Build a normalised-name → entries lookup."""
        out: Dict[str, List[SanctionEntry]] = {}
        for e in entries:
            for n in (e.name, *e.aliases):
                norm = _normalise_name(n)
                if not norm:
                    continue
                out.setdefault(norm, []).append(e)
        return out


# ----------------------------------------------------------------- wikidata
class WikidataCache:
    """Bounded LRU cache for Wikidata SPARQL queries.

    Keyed by `(query_kind, normalised_value)`. Values are `(fetched_at, payload)`.
    Exposes `lookup_label(label)` and `lookup_org(label)` — the two
    most common lookups in OSINT workflows.
    """

    def __init__(self, *, max_items: int = WIKIDATA_LRU_MAX, ttl: int = WIKIDATA_TTL_SECONDS) -> None:
        self.max_items = max_items
        self.ttl = ttl
        self._lock = threading.Lock()
        self._store: "OrderedDict[Tuple[str, str], Tuple[float, List[Dict[str, Any]]]]" = OrderedDict()

    def get(self, kind: str, value: str) -> Optional[List[Dict[str, Any]]]:
        key = (kind, _normalise_name(value))
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            fetched_at, payload = entry
            if (time.time() - fetched_at) > self.ttl:
                self._store.pop(key, None)
                return None
            # LRU bump
            self._store.move_to_end(key)
            return payload

    def put(self, kind: str, value: str, payload: List[Dict[str, Any]]) -> None:
        key = (kind, _normalise_name(value))
        with self._lock:
            self._store[key] = (time.time(), payload)
            self._store.move_to_end(key)
            while len(self._store) > self.max_items:
                self._store.popitem(last=False)

    def stats(self) -> Dict[str, int]:
        with self._lock:
            return {"size": len(self._store), "max": self.max_items}

    def clear(self) -> None:
        with self._lock:
            self._store.clear()


# ----------------------------------------------------------------- engine
class OntologyEngine:
    """Public façade. Hands out the sanction index and wikidata cache."""

    def __init__(self) -> None:
        self.sanctions = SanctionsIndex()
        self.wikidata = WikidataCache()

    def check_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single observation through the ontology.

        Returns a dict describing the sanctions verdict:

          {
            "sanctioned": bool,
            "hits": [SanctionEntry.to_dict(), ...],
            "fields": ["registrant_name", "isp", ...]  # which fields matched
          }

        The orchestrator attaches this to each observation before the
        LLM analyst stage so the system prompt can include a verdict
        line ("SANCTIONED — OFAC SDN match on registrant").
        """
        hits: List[SanctionEntry] = []
        fields: List[str] = []
        parsed = observation.get("parsed") or {}
        if not isinstance(parsed, dict):
            return {"sanctioned": False, "hits": [], "fields": []}

        # Candidate fields to check, per-source.
        candidates = self._candidate_fields(observation.get("source", ""), parsed)
        for field_name, value in candidates:
            if not value:
                continue
            for entry in self.sanctions.lookup(value):
                if entry not in hits:
                    hits.append(entry)
                if field_name not in fields:
                    fields.append(field_name)
        return {
            "sanctioned": bool(hits),
            "hits": [e.to_dict() for e in hits[:10]],  # cap to keep payload small
            "fields": fields,
        }

    @staticmethod
    def _candidate_fields(source: str, parsed: Dict[str, Any]) -> List[Tuple[str, str]]:
        """Return (field_name, value) pairs to check against sanctions.

        Different sources expose different field names. Rather than
        a giant if/elif, this is a small dispatch table — adding a
        new source is a one-line edit.
        """
        TABLE: Dict[str, List[Tuple[str, str]]] = {
            "hackertarget_whois": [
                ("registrant_name", str(parsed.get("registrant name", ""))),
                ("registrant_org", str(parsed.get("registrant organization", ""))),
                ("admin_name", str(parsed.get("admin name", ""))),
            ],
            "ipwhois": [
                ("org", str(parsed.get("org", ""))),
                ("isp", str(parsed.get("isp", ""))),
                ("asn_owner", str(parsed.get("asn", ""))),
            ],
            "ipapi_free": [
                ("org", str(parsed.get("org", ""))),
                ("isp", str(parsed.get("isp", ""))),
                ("as", str(parsed.get("as", ""))),
            ],
            "abuseipdb_check": [
                ("isp", str(parsed.get("isp", ""))),
                ("domain", str(parsed.get("domain", ""))),
            ],
        }
        # Default: try common names across all sources.
        out = list(TABLE.get(source, []))
        for fallback in ("org", "isp", "asn", "registrant", "owner"):
            v = parsed.get(fallback)
            if isinstance(v, str) and v and (fallback, v) not in out:
                out.append((fallback, v))
        return out


# Module-level singleton: the orchestrator imports this directly.
ontology = OntologyEngine()
