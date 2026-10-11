# lan_web — LAN consent gate for the web layer

## Purpose

Backend guard for LAN discovery runs. Validates the web request fields
`lan_consent`, `allow_active`, and `scope_cidr` through `lan_policy`
and maps the decision to an HTTP outcome. Keeps `estorides_web.py`
thin: the route builds a request object, calls one function, and
returns 403 or 400 on denial.

## Inputs

- `LanWebRequest` fields:
  - `lan_consent: bool` — modal Yes state. Strict True required.
  - `allow_active: bool` — checkbox state. Default False.
  - `scope_cidr: str | None` — optional explicit scope.
  - `requested_contact: str` — default `none`; `active` when the run
    needs active tools.
- Body parsing is lenient: missing keys default to blocked values.
  Non-dict bodies yield a blocked decision, never raise.

## Outputs

- `LanWebVerdict` frozen dataclass:
  - `permitted: bool`
  - `notice: str | None` — `active-unavailable` when active was
    requested but the triple gate failed, so the run degraded to
    passive. The UI shows it as a warning, never an error.
  - `status: int` — 200 permitted, 403 consent denied,
    400 invalid scope. Active-unavailable is NOT a denial.
  - `error: str | None` — machine code: `lan-consent-required`,
    `lan-active-denied`, `lan-scope-invalid`.
  - `message: str` — English, no emojis, safe to show in UI.
  - `max_contact: str`, `scope_cidr: str | None`.
  - `to_dict()` and `to_response()` (body dict plus status).

## Error table

| Case | Status | Error | Behavior |
|---|---|---|---|
| consent not True | 403 | `lan-consent-required` | run refused |
| active requested without triple gate | 200 | None (`notice: active-unavailable`) | passive runs, UI warns |
| scope invalid or public | 400 | `lan-scope-invalid` | run refused |
| body not a dict | 403 | `lan-consent-required` | refuse |
| permitted passive | 200 | None | run proceeds with `max_contact=none` |
| permitted active | 200 | None | run proceeds with `max_contact=active` |

## Security guarantees

- Default deny on every malformed field.
- Strict booleans: `"true"` string never counts.
- Messages are static templates; scope echo is normalized CIDR only,
  never raw input, so no log or HTML injection.
- Pure: no I/O, no sockets. Reads env ceiling only via `lan_policy`.

## Out of scope

- HTML, CSS, JS rendering (template and static files consume this).
- Tool execution, graph writes, exports.
- Scope auto-detection (belongs to `lan_scope`; caller fills empty
  scope before calling this guard when desired).

## Fix 2026-10-11 (consent-required after checkbox + no LAN button)

- Root causes: the Discover path sent no consent fields and
  `/api/discover/start` had no gate (bypass); `lanRunFields` never set
  `requested_contact`, so the checkbox governed nothing; the Run
  fallback masked 403 denials as stream failures; no dedicated LAN
  entry point existed.
- Changes: gate on `/api/discover/start`; new `GET /api/lan/scope`
  (pure `scope_payload` plus thin route); `requested_contact`
  derived from the checkbox; denials surface instead of falling back;
  dedicated Scan LAN button (query-box scope or auto-detect, then the
  standard Run path); consent modal shows the active mode line;
  Discover helpers exposed via `window.EstoridesLan` (separate IIFE
  scope). Verified live: scope lists real private CIDRs, consent
  passive/active start jobs, no-consent and Discover-without-consent
  return 403, plain OSINT unaffected.

## Scenarios BDD Given-When-Then

- S1 happy passive: Given consent True and no active, When guarded,
  Then permitted with status 200 and max_contact none.
- S2 happy active: Given consent True, checkbox True, env ceiling
  True, requested active, When guarded, Then permitted active.
- S3 degrade to passive: Given checkbox True but env ceiling False
  and active requested, When guarded, Then permitted with status 200,
  `max_contact` none, and `notice` active-unavailable. The scan always
  runs; the checkbox never blocks, it only caps the ceiling.
- S4 error no consent: Given consent False, When guarded, Then 403
  lan-consent-required.
- S5 error bad scope: Given public scope, When guarded, Then 400
  lan-scope-invalid.
- S6 security string consent: Given consent `"yes"`, When guarded,
  Then 403 lan-consent-required.
- S7 body not dict: Given a list body, When guarded, Then 403.
- S8 scope echo safe: Given scope with whitespace, When denied or
  permitted, Then echoed scope is normalized or None, never raw.
- S9 discover seed guarded: Given a discover body with a LAN seed
  value, When `is_lan_request` is evaluated, Then True so the route
  enforces the same gate as `/api/run`.
- S10 scope payload: Given interface addresses, When `scope_payload`
  is built, Then it carries sorted private `cidrs` plus the first as
  `scope`, or empty plus None when no private network exists.
- S11 active intent: Given consent True, checkbox True, env ceiling
  True, and requested_contact active, When guarded, Then permitted
  with `max_contact` active so active tools actually engage.
