"""estorides.search_telemetry.

Single source of truth for the operator-facing telemetry surface: the
search-in-progress model, the onboarding catalog (keyboard shortcuts and tips)
and the brand/emoji integrity invariants.

The module is pure: no Flask import, no I/O, no mutable global state. The web
layer injects ``SearchTelemetry.context()`` into the Jinja render so the server
and the browser share one vocabulary; the test suite asserts the served chrome
honours the invariants. Numbers, copy and the brand vocabulary all resolve from
the frozen ``TelemetryConfig`` instance, never from scattered literals.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Final

__all__ = [
    "DEFAULT_TELEMETRY",
    "DISALLOWED_BRANDS",
    "InvalidTelemetryConfigError",
    "KeyboardShortcut",
    "ProgressView",
    "SearchPhase",
    "SearchTelemetry",
    "SearchTelemetryError",
    "SplashTip",
    "TelemetryConfig",
    "UnknownPhaseError",
    "disallowed_brands_in",
    "emoji_in",
    "percent_encoded_emoji_in",
]


class SearchTelemetryError(Exception):
    """Base class for every error raised by this module."""


class UnknownPhaseError(SearchTelemetryError, KeyError):
    """Raised when a phase key is not part of the configured vocabulary."""


class InvalidTelemetryConfigError(SearchTelemetryError, ValueError):
    """Raised when a :class:`TelemetryConfig` violates a construction rule."""


DISALLOWED_BRANDS: Final[tuple[str, ...]] = (
    "palantir",
    "maltego",
    "gotham",
    "foundry",
    "spiderfoot",
    "recon-ng",
    "theharvester",
)

_REQUIRED_PHASES: Final[frozenset[str]] = frozenset({"idle", "done", "error"})

_BRAND_RE: Final[re.Pattern[str]] = re.compile(
    r"\b(" + "|".join(re.escape(brand) for brand in DISALLOWED_BRANDS) + r")\b",
    re.IGNORECASE,
)

_EMOJI_RE: Final[re.Pattern[str]] = re.compile(
    "[\u2600-\u27bf\U0001f000-\U0001faff\ufe0f]"
)

_PERCENT_EMOJI_RE: Final[re.Pattern[str]] = re.compile(
    r"%f0%9f(?:%[0-9a-f]{2}){2}", re.IGNORECASE
)


def disallowed_brands_in(text: str) -> tuple[str, ...]:
    """Return the third-party brand tokens found in ``text``.

    Matching is case-insensitive and word-boundary aware so an ordinary word
    that merely contains a brand as a substring does not produce a false
    positive. The returned tuple holds the canonical lowercase brand names in
    first-seen order, de-duplicated.
    """
    seen: dict[str, None] = {}
    for match in _BRAND_RE.finditer(text):
        seen.setdefault(match.group(0).lower(), None)
    return tuple(seen)


def emoji_in(text: str) -> tuple[str, ...]:
    """Return the emoji glyphs found in ``text``, de-duplicated in order.

    Emoji are codepoints in the pictographic blocks (Miscellaneous Symbols,
    Dingbats, regional indicators, the supplementary pictographic planes) and
    the emoji variation selector. Geometric line-symbols outside those blocks
    are permitted iconography and are not flagged.
    """
    seen: dict[str, None] = {}
    for match in _EMOJI_RE.finditer(text):
        seen.setdefault(match.group(0), None)
    return tuple(seen)


def percent_encoded_emoji_in(text: str) -> tuple[str, ...]:
    """Return percent-encoded supplementary-plane emoji sequences in ``text``.

    Catches an emoji smuggled into a ``data:`` URI (for example an emoji
    favicon) as the UTF-8 lead bytes ``%F0%9F`` followed by two continuation
    bytes. The returned tuple holds the matched sequences in first-seen order.
    """
    seen: dict[str, None] = {}
    for match in _PERCENT_EMOJI_RE.finditer(text):
        seen.setdefault(match.group(0), None)
    return tuple(seen)


@dataclass(frozen=True)
class KeyboardShortcut:
    """A single keyboard shortcut: the key chord and what it does."""

    keys: str
    description: str


@dataclass(frozen=True)
class SplashTip:
    """A single onboarding tip: a short title and a one-line body."""

    title: str
    body: str


@dataclass(frozen=True)
class SearchPhase:
    """A search lifecycle phase: a stable key, a human label and activity flag.

    ``active`` is ``True`` while work is in flight (the UI shows a spinner) and
    ``False`` for the resting states ``idle``, ``done`` and ``error``.
    """

    key: str
    label: str
    active: bool


@dataclass(frozen=True)
class ProgressView:
    """Immutable, render-ready snapshot of search progress.

    Carries the clamped counters, the percentage, the human label and the ARIA
    attributes a screen reader needs to announce a live progress region.
    """

    completed: int
    total: int
    percent: int
    phase_key: str
    phase_label: str
    active: bool
    indeterminate: bool
    label: str
    aria_busy: bool
    aria_valuenow: int | None
    aria_valuemax: int
    aria_valuetext: str


def _assert_clean(label: str, *texts: str) -> None:
    """Raise :class:`InvalidTelemetryConfigError` if any text leaks brand/emoji."""
    for text in texts:
        if disallowed_brands_in(text):
            raise InvalidTelemetryConfigError(f"{label} brand leak: {text!r}")
        if emoji_in(text) or percent_encoded_emoji_in(text):
            raise InvalidTelemetryConfigError(f"{label} emoji: {text!r}")


@dataclass(frozen=True)
class TelemetryConfig:
    """Frozen catalog: brand, tagline, shortcuts, tips and phase vocabulary.

    ``__post_init__`` enforces every invariant in spec/search_telemetry.md so an
    invalid catalog can never reach the UI. All construction failures raise
    :class:`InvalidTelemetryConfigError`.
    """

    brand: str
    tagline: str
    shortcuts: tuple[KeyboardShortcut, ...]
    tips: tuple[SplashTip, ...]
    phases: tuple[SearchPhase, ...]

    def __post_init__(self) -> None:
        if not self.brand.strip():
            raise InvalidTelemetryConfigError("brand must be non-empty")
        if disallowed_brands_in(self.brand):
            raise InvalidTelemetryConfigError(f"brand collides with a third-party brand: {self.brand!r}")
        if not self.shortcuts:
            raise InvalidTelemetryConfigError("shortcuts must be non-empty")
        if not self.tips:
            raise InvalidTelemetryConfigError("tips must be non-empty")
        if not self.phases:
            raise InvalidTelemetryConfigError("phases must be non-empty")
        keys = [phase.key for phase in self.phases]
        if len(keys) != len(set(keys)):
            raise InvalidTelemetryConfigError(f"duplicate phase key in {keys}")
        missing = _REQUIRED_PHASES - set(keys)
        if missing:
            raise InvalidTelemetryConfigError(f"missing required phase(s): {sorted(missing)}")
        _assert_clean("tagline", self.tagline)
        for shortcut in self.shortcuts:
            _assert_clean("shortcut", shortcut.keys, shortcut.description)
        for tip in self.tips:
            _assert_clean("tip", tip.title, tip.body)
        for phase in self.phases:
            _assert_clean("phase", phase.label)


class SearchTelemetry:
    """Service over a :class:`TelemetryConfig`: progress math and catalog views.

    Stateless and side-effect free; safe to instantiate or share per request.
    """

    def __init__(self, config: TelemetryConfig | None = None) -> None:
        self._config = config if config is not None else DEFAULT_TELEMETRY
        self._phase_index: dict[str, SearchPhase] = {
            phase.key: phase for phase in self._config.phases
        }

    def shortcuts(self) -> tuple[KeyboardShortcut, ...]:
        """Return the keyboard-shortcut catalog."""
        return self._config.shortcuts

    def tips(self) -> tuple[SplashTip, ...]:
        """Return the onboarding tips catalog."""
        return self._config.tips

    def phases(self) -> tuple[SearchPhase, ...]:
        """Return the search-phase vocabulary."""
        return self._config.phases

    def phase(self, key: str) -> SearchPhase:
        """Return the phase for ``key`` or raise :class:`UnknownPhaseError`."""
        phase = self._phase_index.get(key)
        if phase is None:
            valid = ", ".join(sorted(self._phase_index))
            raise UnknownPhaseError(f"unknown phase {key!r}; valid phases: {valid}")
        return phase

    def progress(self, completed: int, total: int, phase_key: str) -> ProgressView:
        """Compute a clamped, render-ready :class:`ProgressView`.

        Out-of-range counters are clamped, never rejected; only an unknown
        ``phase_key`` raises (:class:`UnknownPhaseError`). When ``total`` is not
        yet known (``<= 0``) and the phase is active the view is indeterminate.
        """
        phase = self.phase(phase_key)
        safe_total = max(total, 0)
        if safe_total > 0:
            safe_completed = min(max(completed, 0), safe_total)
            percent = min(max(round(100 * safe_completed / safe_total), 0), 100)
        else:
            safe_completed = 0
            percent = 0
        indeterminate = phase.active and safe_total <= 0
        if phase.active and not indeterminate:
            label = f"{phase.label} - {safe_completed}/{safe_total}"
            aria_valuetext = f"{safe_completed} of {safe_total} sources, {percent}%"
            aria_valuenow: int | None = percent
        else:
            label = phase.label
            aria_valuetext = phase.label
            aria_valuenow = None if indeterminate else percent
        return ProgressView(
            completed=safe_completed,
            total=safe_total,
            percent=percent,
            phase_key=phase.key,
            phase_label=phase.label,
            active=phase.active,
            indeterminate=indeterminate,
            label=label,
            aria_busy=phase.active,
            aria_valuenow=aria_valuenow,
            aria_valuemax=100,
            aria_valuetext=aria_valuetext,
        )

    def context(self) -> dict[str, Any]:
        """Return the JSON-serialisable catalog for template/JS injection."""
        from .config import CLUSTER_PALETTE
        return {
            "brand": self._config.brand,
            "tagline": self._config.tagline,
            "shortcuts": [
                {"keys": shortcut.keys, "description": shortcut.description}
                for shortcut in self._config.shortcuts
            ],
            "tips": [
                {"title": tip.title, "body": tip.body} for tip in self._config.tips
            ],
            "phases": [
                {"key": phase.key, "label": phase.label, "active": phase.active}
                for phase in self._config.phases
            ],
            "cluster_palette": list(CLUSTER_PALETTE),
        }


def _default_config() -> TelemetryConfig:
    """Build the canonical Estorides telemetry catalog."""
    return TelemetryConfig(
        brand="Estorides",
        tagline="State-level OSINT, fully open source",
        shortcuts=(
            KeyboardShortcut("/", "Focus the query box"),
            KeyboardShortcut("Ctrl+Enter", "Run the current query"),
            KeyboardShortcut("Esc", "Clear the input or close an overlay"),
            KeyboardShortcut("?", "Show this keyboard-shortcut help"),
            KeyboardShortcut("1-6", "Switch between the sidebar tabs"),
            KeyboardShortcut("G", "Show the graph canvas"),
            KeyboardShortcut("M", "Show the map canvas"),
            KeyboardShortcut("T", "Show the timeline canvas"),
        ),
        tips=(
            SplashTip(
                "Query any indicator",
                "Enter a domain, IP, email, person, CVE or crypto address; the type is detected automatically.",
            ),
            SplashTip(
                "Watch the fan-out",
                "Sources run in parallel; the progress bar and live status show how many have answered.",
            ),
            SplashTip(
                "Pivot in the graph",
                "Open the Graph canvas, expand a node, run a transform and follow the dashed cross-references.",
            ),
            SplashTip(
                "Promote data to intelligence",
                "Entities are scored and fused across sources, climbing from data to information to intelligence.",
            ),
            SplashTip(
                "Export when ready",
                "Export the picture as STIX 2.1, MISP, GraphML or JSON for downstream tooling.",
            ),
        ),
        phases=(
            SearchPhase("idle", "Idle", active=False),
            SearchPhase("detect", "Detecting indicator type", active=True),
            SearchPhase("query", "Querying sources", active=True),
            SearchPhase("extract", "Extracting entities", active=True),
            SearchPhase("correlate", "Correlating graph", active=True),
            SearchPhase("done", "Done", active=False),
            SearchPhase("error", "Error", active=False),
        ),
    )


DEFAULT_TELEMETRY: Final[TelemetryConfig] = _default_config()
