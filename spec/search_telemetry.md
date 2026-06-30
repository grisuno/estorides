# Spec — `search_telemetry` (item 2f)

Status: in_progress
Opened: 2026-06-29

## Purpose

Estorides runs long, fan-out OSINT searches across 100+ sources. The operator
must never be left wondering whether a search is actually executing, nor be
dropped into the product with no idea how to drive it. This module is the
**single source of truth** for the operator-facing telemetry surface:

1. The **search-in-progress** model — a pure, deterministic mapping from
   `(completed, total, phase)` to an immutable `ProgressView` carrying the
   percentage, a human label and the ARIA attributes a screen reader needs to
   announce live progress. The web layer and the browser both read their phase
   vocabulary from here, so the server and the client can never drift.
2. The **onboarding catalog** — the canonical keyboard-shortcut list and the
   "how to get the best out of Estorides" tips that the splash screen renders.
   Today these live hardcoded and duplicated inside the HTML template; this
   module makes them a single immutable catalog the template consumes.
3. The **brand / emoji integrity invariants** — pure predicates that decide
   whether a user-facing string leaks a third-party product brand or an emoji
   glyph. Estorides is a serious open-source platform: the only brand the UI
   names is Estorides, and the chrome carries no emoji decoration.

The module is pure Python: no Flask import, no I/O, no global mutable state.
The web layer (`estorides_web.py`) injects `SearchTelemetry.context()` into the
Jinja render; the tests assert the served template honours the invariants.

## Inputs

| Input | Type | Range / format | Empty / edge handling |
| --- | --- | --- | --- |
| `progress(completed, total, phase_key)` | `int, int, str` | `completed`, `total` any int (incl. negative); `phase_key` one of the catalog keys | `total <= 0` → indeterminate; `completed` clamped to `[0, total]`; unknown `phase_key` → `UnknownPhaseError` |
| `phase(key)` | `str` | a catalog phase key | unknown key → `UnknownPhaseError` |
| `disallowed_brands_in(text)` | `str` | any text, incl. empty | empty → `()`; matching is case-insensitive, word-ish boundary |
| `emoji_in(text)` | `str` | any text, incl. empty | empty → `()` |
| `TelemetryConfig(...)` | dataclass | non-empty brand, ≥1 shortcut, ≥1 tip, ≥1 phase, unique phase keys, exactly one `done`, one `error`, one `idle` sentinel phase | invalid → `InvalidTelemetryConfigError` |

The phase vocabulary (default catalog): `idle`, `detect`, `query`, `extract`,
`correlate`, `done`, `error`. Each phase carries `active: bool` — `idle`,
`done`, `error` are inactive (no spinner); the rest are active.

## Outputs

`ProgressView` is a frozen dataclass:

```
ProgressView(
  completed: int,        # clamped to [0, total] when total > 0, else >= 0
  total: int,            # max(total, 0)
  percent: int,          # round(100 * completed / total), clamped [0, 100]; 0 when total <= 0
  phase_key: str,        # echoed input key
  phase_label: str,      # human label, e.g. "Querying sources"
  active: bool,          # phase.active
  indeterminate: bool,   # active and total <= 0 (unknown denominator)
  label: str,            # "Querying sources - 12/40" (determinate) or "Querying sources" (else)
  aria_busy: bool,       # == active
  aria_valuenow: int|None,  # percent when determinate, else None
  aria_valuemax: int,    # 100
  aria_valuetext: str,   # "12 of 40 sources, 30%" determinate; phase_label otherwise
)
```

`SearchTelemetry.context()` returns a JSON-serialisable dict:

```
{
  "brand": "Estorides",
  "tagline": "<one line>",
  "shortcuts": [{"keys": "/", "description": "Focus the query box"}, ...],
  "tips":      [{"title": "...", "body": "..."}, ...],
  "phases":    [{"key": "query", "label": "Querying sources", "active": true}, ...]
}
```

Every string emitted by `context()` is guaranteed brand-clean and emoji-clean
(enforced by a self-consistency test and by `TelemetryConfig.__post_init__`).

## Error table

| Condition | Exception | Message contains | Behaviour |
| --- | --- | --- | --- |
| Unknown phase key in `progress`/`phase` | `UnknownPhaseError` | the bad key, the valid keys | raised; no partial `ProgressView` |
| Empty brand in config | `InvalidTelemetryConfigError` | `"brand must be non-empty"` | construction fails |
| Brand itself matches a disallowed brand | `InvalidTelemetryConfigError` | `"brand collides"` | construction fails |
| No shortcuts / tips / phases | `InvalidTelemetryConfigError` | the empty field name | construction fails |
| Duplicate phase keys | `InvalidTelemetryConfigError` | `"duplicate phase"` | construction fails |
| Missing `idle`/`done`/`error` sentinel | `InvalidTelemetryConfigError` | the missing key | construction fails |
| Catalog string leaks brand or emoji | `InvalidTelemetryConfigError` | `"brand leak"` / `"emoji"` | construction fails |

`progress()` never raises on numeric inputs: out-of-range integers are clamped,
not rejected. The only raising path is an unknown `phase_key`.

## Security guarantees

- **No third-party brand surface.** `disallowed_brands_in` flags any of the
  curated third-party intelligence-platform brands. The served template, the
  JS bundle's user-facing strings and the catalog are tested clean. This closes
  the open leaks (`Palantir`, `Maltego-style`, `Osiris-style`) in the UI and
  source comments.
- **No emoji in chrome.** `emoji_in` flags codepoints in the pictographic
  blocks (Miscellaneous Symbols `U+2600-26FF`, Dingbats `U+2700-27BF`, regional
  indicators `U+1F1E6-1F1FF`, supplementary pictographic planes
  `U+1F000-1FAFF`) and the emoji variation selector `U+FE0F`, plus the
  percent-encoded supplementary-plane lead bytes (`%F0%9F`) used to smuggle an
  emoji into a `data:` favicon. Geometric line-symbols outside those blocks
  (e.g. the hexagon brand mark `U+2B22`) are permitted iconography.
- **No injection.** The module emits only static catalog data. The web layer
  serialises `context()` with `json.dumps` into a `<script type="application/
  json">` block (no `<script>` interpolation, no `|safe` on attacker data).
- **Deterministic, side-effect free.** Pure functions only; safe to call on any
  request without locks or shared state. No `eval`/`exec`/`os.system`.

## Out of scope

- Rendering the splash/progress DOM (that is template + CSS wiring, validated
  by the parsing tests, not owned as logic here).
- Server-Sent Events transport and the orchestrator run loop (existing).
- Renaming internal identifiers, routes or modules that functionally reference
  data sources (e.g. the `osiris_sources` module, `/api/osiris/*` routes,
  `data-osiris` attributes). Only **operator-visible text** is de-branded.
- Theming / colour palette redesign beyond replacing the emoji favicon with a
  neutral hexagon mark.
- Persistence of "onboarding seen" state (stays in `localStorage`).

## BDD scenarios (Given-When-Then)

These are contracts. They change only by explicit agreement.

### S1 — happy path: determinate progress mid-search
- **Given** the default telemetry and an active `query` phase
- **When** `progress(completed=12, total=40, phase_key="query")` is computed
- **Then** `percent == 30`, `active is True`, `indeterminate is False`,
  `label == "Querying sources - 12/40"`, `aria_busy is True`,
  `aria_valuenow == 30`, `aria_valuetext == "12 of 40 sources, 30%"`.

### S2 — edge: indeterminate progress (total unknown yet)
- **Given** an active `detect` phase before the source count is known
- **When** `progress(completed=0, total=0, phase_key="detect")`
- **Then** `indeterminate is True`, `percent == 0`, `aria_valuenow is None`,
  `aria_busy is True`, and `label == "Detecting indicator type"`.

### S3 — edge: completion settles the bar to 100 and stops the spinner
- **Given** the terminal `done` phase
- **When** `progress(completed=40, total=40, phase_key="done")`
- **Then** `percent == 100`, `active is False`, `aria_busy is False`,
  `indeterminate is False`.

### S4 — edge: out-of-range integers are clamped, never raised
- **Given** the `query` phase
- **When** `progress(completed=999, total=40, phase_key="query")` and
  `progress(completed=-5, total=40, phase_key="query")`
- **Then** the first yields `completed == 40`, `percent == 100`; the second
  yields `completed == 0`, `percent == 0`; neither raises.

### S5 — error: unknown phase key is rejected
- **Given** the default telemetry
- **When** `progress(0, 10, phase_key="bogus")` is called
- **Then** `UnknownPhaseError` is raised and its message names `bogus` and the
  valid phase keys.

### S6 — security: catalog is brand-clean and emoji-clean
- **Given** `SearchTelemetry().context()`
- **When** every brand and emoji predicate is run over every string in it
- **Then** `disallowed_brands_in` and `emoji_in` return `()` for all of them.

### S7 — security: the served template names no third-party brand
- **Given** the Flask app renders `index.html`
- **When** the visible text of the response is scanned
- **Then** no curated third-party brand token appears.

### S8 — security: the served chrome carries no emoji
- **Given** the rendered `index.html` and the JS bundle
- **When** `emoji_in` and the `%F0%9F` percent-encoding check run over them
- **Then** both are clean (the emoji favicon is replaced by a hexagon SVG).

### S9 — security: brand predicate is case-insensitive and boundary-aware
- **Given** the strings `"Powered by PALANTIR"`, `"maltego-style"` and the
  benign `"foundryside novel"` is **not** a target (curated list excludes it)
- **When** `disallowed_brands_in` runs
- **Then** the first two flag their brand; an unrelated substring inside an
  ordinary word does not produce a false positive for a multi-word brand.

### S10 — config: invalid telemetry config is rejected at construction
- **Given** a `TelemetryConfig` with an empty brand, or no tips, or a duplicate
  phase key, or a catalog string containing an emoji
- **When** it is constructed
- **Then** `InvalidTelemetryConfigError` is raised with a message naming the
  violated rule.

### S11 — single source of truth: shortcuts/tips appear once in the template
- **Given** the rendered template
- **When** the shortcut keys and tip titles from `context()` are searched for
- **Then** each appears, and the template contains no second hardcoded copy of
  the shortcut `<dl>` divorced from the catalog (the catalog drives the render).

### S12 — property: progress invariants hold for all integer inputs
- **Given** any `(completed, total)` integers and any valid phase
- **When** `progress` runs
- **Then** `0 <= percent <= 100`, `0 <= completed <= max(total, 0)`,
  `total == max(total_in, 0)`, `aria_valuemax == 100`, and the call never
  raises.

## Acceptance criteria ("done")

- `pytest tests/test_search_telemetry.py -v` — green (S1-S11).
- `pytest tests/properties/test_search_telemetry_properties.py -v` — green
  (≥1000 examples per property, S12 + brand/emoji predicate properties).
- `ruff check estorides_core/search_telemetry.py tests/test_search_telemetry.py`
  — clean.
- `mypy --strict estorides_core/search_telemetry.py` — clean.
- `bandit -r estorides_core/search_telemetry.py` — no High/Medium.
- Full suite (`pytest tests/`) — no regressions.
- Visual review: splash + in-progress bar rendered headless to PDF/PNG and read.
