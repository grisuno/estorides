"""
estorides.config
================
Central configuration. Everything tunable lives here.

Two layers coexist on purpose:

  * Module-level constants (the original surface). Kept verbatim so the
    rest of the engine keeps importing `from .config import X` unchanged.
  * Frozen dataclass config objects (the structured surface) for the
    v1.3 subsystems: response cache TTL, the recursive pivot engine, the
    SSE streaming layer and the web tunables. These group related knobs,
    validate their own bounds at construction and expose a single
    immutable instance each. No subsystem hard-codes a number; it reads
    its field off the relevant config object.

Every tunable resolves from an environment variable with a typed,
fault-tolerant reader (a malformed env var falls back to the default and
logs, instead of crashing the whole process at import time).
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

_log = logging.getLogger("estorides.config")


def _env_int(name: str, default: int) -> int:
    """Read an int env var, falling back to `default` on absence/parse error."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        _log.warning("env %s=%r is not an int, using default %d", name, raw, default)
        return default


def _env_float(name: str, default: float) -> float:
    """Read a float env var, falling back to `default` on absence/parse error."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        _log.warning("env %s=%r is not a float, using default %s", name, raw, default)
        return default


def _env_bool(name: str, default: bool) -> bool:
    """Read a boolean env var. Truthy tokens: 1/true/yes/on (case-insensitive)."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")

# -----------------------------------------------------------------------------
# Filesystem layout
# -----------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
SOURCES_DIR: Path = Path(os.environ.get("ESTORIDES_SOURCES_DIR", str(PROJECT_ROOT / "sources")))
DATA_DIR: Path = PROJECT_ROOT / "data"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
TEMPLATES_DIR: Path = PROJECT_ROOT / "templates"
STATIC_DIR: Path = PROJECT_ROOT / "static"

DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

DATASET_PATH: Path = DATA_DIR / "estorides_dataset.jsonl"
GRAPH_PATH: Path = DATA_DIR / "estorides_graph.graphml"
CACHE_PATH: Path = DATA_DIR / "estorides_cache.sqlite"
STIX_BUNDLE_PATH: Path = DATA_DIR / "estorides_stix_bundle.json"
MISP_EVENT_PATH: Path = DATA_DIR / "estorides_misp_event.json"

# -----------------------------------------------------------------------------
# Network behaviour
# -----------------------------------------------------------------------------
HTTP_TIMEOUT: float = float(os.environ.get("ESTORIDES_TIMEOUT", 12.0))
HTTP_MAX_RETRIES: int = int(os.environ.get("ESTORIDES_MAX_RETRIES", 3))
HTTP_BACKOFF_BASE: float = float(os.environ.get("ESTORIDES_BACKOFF_BASE", 0.6))
HTTP_BACKOFF_FACTOR: float = float(os.environ.get("ESTORIDES_BACKOFF_FACTOR", 2.0))
HTTP_MAX_PARALLEL: int = int(os.environ.get("ESTORIDES_PARALLEL", 8))
USER_AGENT: str = os.environ.get("ESTORIDES_UA", "Estorides/1.0 (+open-source OSINT platform)")

# Circuit breaker — if a host fails this many times in a window, skip for cooldown.
CIRCUIT_FAIL_THRESHOLD: int = _env_int("ESTORIDES_CIRCUIT_FAIL_THRESHOLD", 5)
CIRCUIT_COOLDOWN_S: int = _env_int("ESTORIDES_CIRCUIT_COOLDOWN_S", 300)

# Response cache freshness. A cached GET older than this is treated as a
# miss and re-fetched, so the on-disk cache can never serve stale OSINT
# (a domain that changed owners, a leak that was taken down) forever.
# Set to 0 to disable the cache entirely.
HTTP_CACHE_TTL_S: int = _env_int("ESTORIDES_CACHE_TTL_S", 86_400)

# -----------------------------------------------------------------------------
# Operator OPSEC — contact classification + egress anonymisation
# -----------------------------------------------------------------------------
# Every source declares how its traffic reaches the target so an operator
# doing passive-only reconnaissance (bug-bounty scoping, threat research)
# can guarantee the engine never makes the target observe a probe.
#
#   none   — the request only hits a third-party database, resolver, or CT
#            log; the target's own infrastructure never sees anything.
#   broker — a third party performs an ACTIVE probe against the target on
#            the operator's behalf (ping, traceroute, header fetch). The
#            target is touched, but from the broker's IP, not the operator's.
#   active — the engine connects to the target's own infrastructure directly
#            from the operator's egress IP.
#
# The levels are ordered by how much the target can observe. `--passive-only`
# keeps only `none`; a caller may raise the ceiling to allow broker probes.
CONTACT_NONE: str = "none"
CONTACT_BROKER: str = "broker"
CONTACT_ACTIVE: str = "active"
CONTACT_LEVELS: dict[str, int] = {CONTACT_NONE: 0, CONTACT_BROKER: 1, CONTACT_ACTIVE: 2}
DEFAULT_CONTACT: str = CONTACT_NONE
PASSIVE_ONLY: bool = _env_bool("ESTORIDES_PASSIVE_ONLY", False)


def contact_level(contact: str) -> int:
    """Map a contact class to its numeric severity, unknown values to active.

    An unrecognised class is treated as the most exposing (`active`) so a
    typo in a source YAML can never silently downgrade an operator's
    passive-only guarantee."""
    return CONTACT_LEVELS.get(contact, CONTACT_LEVELS[CONTACT_ACTIVE])


# Egress anonymisation. When set, every outbound OSINT request is routed
# through this proxy so a broker never sees the operator's real IP. A
# comma-separated pool rotates per request to spread the footprint across
# exits. SOCKS5 (e.g. Tor at socks5://127.0.0.1:9050) needs the optional
# `aiohttp_socks` package; HTTP/HTTPS proxies work with stock aiohttp.
HTTP_PROXY: str = (os.environ.get("ESTORIDES_HTTP_PROXY") or "").strip()
HTTP_PROXY_POOL: list[str] = [
    p.strip() for p in (os.environ.get("ESTORIDES_HTTP_PROXY_POOL") or "").split(",") if p.strip()
]
# Resolving the target's name locally (for the SSRF guard's DNS leg) tells
# the operator's own resolver which targets are under investigation, which
# defeats the point of routing HTTP through Tor. When a proxy is in use,
# default to letting the proxy/exit node resolve and skip the local A/AAAA
# lookup; the literal-host canonicalisation leg of the guard still runs.
PROXY_REMOTE_DNS: bool = _env_bool("ESTORIDES_PROXY_REMOTE_DNS", True)


def effective_proxies(explicit: str | None = None) -> list[str]:
    """Resolve the proxy rotation pool from an explicit value or the env.

    Precedence: an explicit caller value (CLI flag) wins; otherwise the
    pool env var, otherwise the single-proxy env var. Returns an empty
    list when no anonymising egress is configured."""
    if explicit and explicit.strip():
        return [explicit.strip()]
    if HTTP_PROXY_POOL:
        return list(HTTP_PROXY_POOL)
    if HTTP_PROXY:
        return [HTTP_PROXY]
    return []

# -----------------------------------------------------------------------------
# LLM backends (priority order)
# -----------------------------------------------------------------------------
LLM_BACKENDS: list[str] = ["ollama", "openrouter", "anthropic", "openai", "stub"]
LLM_DEFAULT_TASK: str = "analysis"
LLM_MAX_TOKENS: int = int(os.environ.get("ESTORIDES_LLM_MAX_TOKENS", 2048))
LLM_TEMPERATURE: float = float(os.environ.get("ESTORIDES_LLM_TEMP", 0.25))
# Hard wall-clock cap (seconds) for any single LLM HTTP call. Threaded into the
# requests timeout so a slow local model can never orphan a thread that blocks
# process shutdown for minutes.
LLM_REQUEST_TIMEOUT: float = float(os.environ.get("ESTORIDES_LLM_REQUEST_TIMEOUT", 12.0))

# Model selection per backend.
LLM_MODELS: dict[str, str] = {
    "ollama": os.environ.get("ESTORIDES_OLLAMA_MODEL", "llama3.1:8b"),
    "openrouter": os.environ.get("ESTORIDES_OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet"),
    "anthropic": os.environ.get("ESTORIDES_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
    "openai": os.environ.get("ESTORIDES_OPENAI_MODEL", "gpt-4o-mini"),
    "stub": "stub",
}

# Provider endpoints.
OLLAMA_URL: str = os.environ.get("ESTORIDES_OLLAMA_URL", "http://localhost:11434")
OPENROUTER_URL: str = os.environ.get("ESTORIDES_OPENROUTER_URL", "https://openrouter.ai/api/v1")
ANTHROPIC_URL: str = os.environ.get("ESTORIDES_ANTHROPIC_URL", "https://api.anthropic.com/v1")
OPENAI_URL: str = os.environ.get("ESTORIDES_OPENAI_URL", "https://api.openai.com/v1")

# -----------------------------------------------------------------------------
# Entity extraction patterns
# -----------------------------------------------------------------------------
ENTITY_REGEX = {
    "ipv4": r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}(?:25[0-5]|2[0-4]\d|1?\d{1,2})\b",
    "ipv6": r"\b(?:[A-Fa-f0-9]{1,4}:){2,7}[A-Fa-f0-9]{1,4}\b",
    "domain": r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[A-Za-z]{2,24}\b",
    "url": r"https?://[^\s\"'<>)]+",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,24}\b",
    "btc_address": r"\b(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{11,71})\b",
    "eth_address": r"\b0x[a-fA-F0-9]{40}\b",
    "phone_e164": r"\+[1-9]\d{6,14}\b",
    "md5": r"\b[a-fA-F0-9]{32}\b",
    "sha1": r"\b[a-fA-F0-9]{40}\b",
    "sha256": r"\b[a-fA-F0-9]{64}\b",
    "cve": r"\bCVE-\d{4}-\d{4,7}\b",
    "ghsa": r"\bGHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}\b",
    "bitcoin_tx": r"\b[a-fA-F0-9]{64}\b",
    "mac": r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b",
    "asn": r"\bAS\d{1,10}\b",
    "user_agent": r"\bMozilla/\d\.\d\b",
}

# Bounds on entity extraction so a single huge response (crt.sh, wayback) can
# never turn the post-fetch stage into an 80-second CPU stall. A blob larger
# than the scan cap is truncated; no more than N matches per type are kept.
ENTITY_MAX_SCAN_CHARS: int = int(os.environ.get("ESTORIDES_ENTITY_MAX_SCAN", 120_000))
ENTITY_MAX_PER_TYPE: int = int(os.environ.get("ESTORIDES_ENTITY_MAX_PER_TYPE", 750))

# Co-occurrence is a soft "seen together" signal. Building a full clique over
# every entity in a large response is O(n^2) and produces million-edge graphs
# that swamp ranking and make GraphML export crawl. Cap the clique per source.
KG_MAX_COOCCUR_ENTITIES: int = int(os.environ.get("ESTORIDES_KG_MAX_COOCCUR", 30))

# Service-specific heuristics to filter false-positive domains (e.g. versions like "1.0.0")
DOMAIN_BLACKLIST: set[str] = {
    "example.com", "localhost", "test.com", "domain.com", "email.com",
    "yourcompany.com", "yourdomain.com",
}

# -----------------------------------------------------------------------------
# Categories used to colorize the graph / map
# -----------------------------------------------------------------------------
CATEGORY_PALETTE: dict[str, str] = {
    "01. DNS Intelligence": "#5B8FF9",
    "02. IP & Infrastructure": "#F6BD16",
    "03. Web Intelligence": "#5AD8A6",
    "04. Social Media": "#E8684A",
    "05. Threat Intelligence": "#FF6B6B",
    "06. Breach Intelligence": "#9270CA",
    "07. Geolocation": "#6DC8EC",
    "08. Knowledge": "#FF99C3",
    "09. Wireless": "#269A99",
    "10. Blockchain": "#F99F80",
    "11. Paste & Leaks": "#C25B5B",
    "12. Visual": "#9FB40F",
}

# -----------------------------------------------------------------------------
# Flask UI
# -----------------------------------------------------------------------------
FLASK_HOST: str = os.environ.get("ESTORIDES_HOST", "127.0.0.1")
FLASK_PORT: int = _env_int("ESTORIDES_PORT", 5050)
FLASK_DEBUG: bool = _env_bool("ESTORIDES_DEBUG", False)


# =============================================================================
# Structured config objects (v1.3). Each is a single frozen instance built
# from the environment. Subsystems depend on these instead of bare literals.
# =============================================================================
@dataclass(frozen=True)
class CacheConfig:
    """Disk response-cache behaviour."""

    ttl_seconds: int
    enabled: bool

    @property
    def is_active(self) -> bool:
        """Cache is only consulted when enabled and the TTL is positive."""
        return self.enabled and self.ttl_seconds > 0


@dataclass(frozen=True)
class PivotPolicyConfig:
    """Which entity types are worth pivoting on, and how leads are scored.

    The recursive cross-search expands the highest-scoring leads first.
    `type_weights` lets a high-signal selector (an email, a wallet) outrank
    a low-signal one (a shared CDN IP) at the same depth. `depth_decay`
    discounts every additional hop so the frontier stays close to the seed.
    """

    pivotable_types: frozenset[str]
    type_weights: Mapping[str, float]
    default_weight: float
    depth_decay: float

    def is_pivotable(self, entity_type: str) -> bool:
        """True when an entity of `entity_type` should be re-queried."""
        return entity_type in self.pivotable_types

    def lead_score(self, entity_type: str, depth: int, parent_score: float) -> float:
        """Priority of expanding this lead. Higher expands sooner."""
        weight = self.type_weights.get(entity_type, self.default_weight)
        return parent_score * (self.depth_decay ** max(depth, 0)) * weight


@dataclass(frozen=True)
class PivotConfig:
    """Bounds and defaults for the recursive pivot engine.

    `*_cap` values are the absolute ceilings applied to any caller-supplied
    override (e.g. an API request body), so an untrusted client can never
    request an unbounded crawl.
    """

    max_depth: int
    max_steps: int
    max_entities: int
    deadline_seconds: float
    per_target_timeout_seconds: float
    parallel: int
    breadth_per_step: int
    seed_score: float
    policy: PivotPolicyConfig
    max_depth_cap: int
    max_steps_cap: int
    max_entities_cap: int
    parallel_cap: int
    deadline_cap_seconds: float

    def clamp_depth(self, value: int) -> int:
        """Clamp a requested depth into [1, max_depth_cap]."""
        return max(1, min(int(value), self.max_depth_cap))

    def clamp_steps(self, value: int) -> int:
        """Clamp a requested step budget into [1, max_steps_cap]."""
        return max(1, min(int(value), self.max_steps_cap))

    def clamp_entities(self, value: int) -> int:
        """Clamp a requested entity budget into [1, max_entities_cap]."""
        return max(1, min(int(value), self.max_entities_cap))

    def clamp_parallel(self, value: int) -> int:
        """Clamp a requested fan-out width into [1, parallel_cap]."""
        return max(1, min(int(value), self.parallel_cap))

    def clamp_deadline(self, value: float) -> float:
        """Clamp a requested per-target deadline into (0, deadline_cap_seconds]."""
        return max(1.0, min(float(value), self.deadline_cap_seconds))


@dataclass(frozen=True)
class StreamConfig:
    """Server-Sent-Events streaming knobs (buffer size, cadence)."""

    sse_buffer_cap: int
    poll_interval_seconds: float
    heartbeat_idle_ticks: int
    start_dispatch_timeout_seconds: float


@dataclass(frozen=True)
class WebConfig:
    """Per-endpoint defaults and render limits for the Flask layer."""

    graph_render_node_limit: int
    graph_render_edge_limit: int
    graph_node_base_size: int
    graph_node_max_bonus: int
    default_parallel: int
    default_timeout_seconds: float
    default_deadline_seconds: float
    cases_default_limit: int
    intel_neighbor_hops: int


def _pivot_weight_map() -> Mapping[str, float]:
    """Default per-type lead weights for the pivot scorer.

    Strong, single-owner selectors rank above shared infrastructure.
    """
    return {
        "email": _env_float("ESTORIDES_PIVOT_W_EMAIL", 1.0),
        "btc_address": _env_float("ESTORIDES_PIVOT_W_BTC", 0.95),
        "eth_address": _env_float("ESTORIDES_PIVOT_W_ETH", 0.95),
        "username": _env_float("ESTORIDES_PIVOT_W_USERNAME", 0.9),
        "domain": _env_float("ESTORIDES_PIVOT_W_DOMAIN", 0.85),
        "asn": _env_float("ESTORIDES_PIVOT_W_ASN", 0.7),
        "ipv4": _env_float("ESTORIDES_PIVOT_W_IPV4", 0.65),
        "ipv6": _env_float("ESTORIDES_PIVOT_W_IPV6", 0.6),
    }


def _csv_frozenset(name: str, default: frozenset[str]) -> frozenset[str]:
    """Read a comma-separated env var into a frozenset, else the default."""
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return frozenset(tok.strip() for tok in raw.split(",") if tok.strip())


HTTP_CACHE: CacheConfig = CacheConfig(
    ttl_seconds=HTTP_CACHE_TTL_S,
    enabled=_env_bool("ESTORIDES_CACHE_ENABLED", True),
)

# Full cross-search policy: every strong selector pivots. Used by the
# interactive deep-run stream.
PIVOT_POLICY_FULL: PivotPolicyConfig = PivotPolicyConfig(
    pivotable_types=_csv_frozenset(
        "ESTORIDES_PIVOT_TYPES_FULL",
        frozenset({"domain", "ipv4", "ipv6", "email", "username", "asn", "btc_address", "eth_address"}),
    ),
    type_weights=_pivot_weight_map(),
    default_weight=_env_float("ESTORIDES_PIVOT_W_DEFAULT", 0.5),
    depth_decay=_env_float("ESTORIDES_PIVOT_DEPTH_DECAY", 0.6),
)

# Infrastructure-only policy: domains and IPs. Preserves the historical
# background-discoverer surface (it never recursed into emails/wallets).
PIVOT_POLICY_INFRA: PivotPolicyConfig = PivotPolicyConfig(
    pivotable_types=_csv_frozenset(
        "ESTORIDES_PIVOT_TYPES_INFRA",
        frozenset({"domain", "ipv4", "ipv6"}),
    ),
    type_weights=_pivot_weight_map(),
    default_weight=_env_float("ESTORIDES_PIVOT_W_DEFAULT", 0.5),
    depth_decay=_env_float("ESTORIDES_PIVOT_DEPTH_DECAY", 0.6),
)

PIVOT: PivotConfig = PivotConfig(
    max_depth=_env_int("ESTORIDES_PIVOT_MAX_DEPTH", 2),
    max_steps=_env_int("ESTORIDES_PIVOT_MAX_STEPS", 50),
    max_entities=_env_int("ESTORIDES_PIVOT_MAX_ENTITIES", 5000),
    deadline_seconds=_env_float("ESTORIDES_PIVOT_DEADLINE_S", 30.0),
    per_target_timeout_seconds=_env_float("ESTORIDES_PIVOT_TARGET_TIMEOUT_S", 8.0),
    parallel=_env_int("ESTORIDES_PIVOT_PARALLEL", 8),
    breadth_per_step=_env_int("ESTORIDES_PIVOT_BREADTH", 25),
    seed_score=_env_float("ESTORIDES_PIVOT_SEED_SCORE", 1.0),
    policy=PIVOT_POLICY_FULL,
    max_depth_cap=_env_int("ESTORIDES_PIVOT_MAX_DEPTH_CAP", 4),
    max_steps_cap=_env_int("ESTORIDES_PIVOT_MAX_STEPS_CAP", 200),
    max_entities_cap=_env_int("ESTORIDES_PIVOT_MAX_ENTITIES_CAP", 20_000),
    parallel_cap=_env_int("ESTORIDES_PIVOT_PARALLEL_CAP", 12),
    deadline_cap_seconds=_env_float("ESTORIDES_PIVOT_DEADLINE_CAP_S", 120.0),
)

STREAM: StreamConfig = StreamConfig(
    sse_buffer_cap=_env_int("ESTORIDES_SSE_BUFFER_CAP", 2000),
    poll_interval_seconds=_env_float("ESTORIDES_SSE_POLL_S", 1.0),
    heartbeat_idle_ticks=_env_int("ESTORIDES_SSE_HEARTBEAT_TICKS", 5),
    start_dispatch_timeout_seconds=_env_float("ESTORIDES_SSE_START_TIMEOUT_S", 15.0),
)

WEB: WebConfig = WebConfig(
    graph_render_node_limit=_env_int("ESTORIDES_WEB_GRAPH_NODES", 200),
    graph_render_edge_limit=_env_int("ESTORIDES_WEB_GRAPH_EDGES", 1000),
    graph_node_base_size=_env_int("ESTORIDES_WEB_NODE_BASE", 4),
    graph_node_max_bonus=_env_int("ESTORIDES_WEB_NODE_MAX_BONUS", 20),
    default_parallel=_env_int("ESTORIDES_WEB_DEFAULT_PARALLEL", 8),
    default_timeout_seconds=_env_float("ESTORIDES_WEB_DEFAULT_TIMEOUT_S", 8.0),
    default_deadline_seconds=_env_float("ESTORIDES_WEB_DEFAULT_DEADLINE_S", 30.0),
    cases_default_limit=_env_int("ESTORIDES_WEB_CASES_LIMIT", 20),
    intel_neighbor_hops=_env_int("ESTORIDES_WEB_INTEL_HOPS", 2),
)
