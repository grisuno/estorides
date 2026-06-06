"""
estorides.config
================
Central configuration. Everything tunable lives here.
"""
from __future__ import annotations

import os
from pathlib import Path

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
CIRCUIT_FAIL_THRESHOLD: int = 5
CIRCUIT_COOLDOWN_S: int = 300

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
FLASK_PORT: int = int(os.environ.get("ESTORIDES_PORT", 5050))
FLASK_DEBUG: bool = os.environ.get("ESTORIDES_DEBUG", "0") == "1"
