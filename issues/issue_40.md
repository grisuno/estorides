# Issue #40: All dependencies are unpinned (>=only) with no lockfile; multiple CVE ranges are reachable (aiohttp, gunicorn)

- **State:** open
- **Created:** 2026-06-08T11:43:02Z
- **Updated:** 2026-06-08T11:43:02Z
- **Labels:** None

---

## Summary
All Python dependencies in `requirements.txt` and `pyproject.toml` are specified with `>=` lower bounds only and no upper bounds or hash pinning. This means `pip install` always resolves to the latest available version, which can silently introduce breaking changes or newly-disclosed CVEs. The `aiohttp>=3.9` constraint alone spans versions with multiple known critical CVEs (GHSA-jwhx-xcg6-8xhj — request smuggling in <3.9.4; CVE-2024-23334 — path traversal in <3.9.2).

## Evidence
`requirements.txt`:
```
flask>=3.0
networkx>=3.0
requests>=2.31
pyyaml>=6.0
aiohttp>=3.9
aiohttp_socks>=0.8
gunicorn>=21.2
```

`pyproject.toml` `[project]` dependencies mirror the same lower-bound-only pattern.

No `requirements.lock`, no `pip-compile` output, no hash-pinned install file exists in the repository.

Known CVEs reachable from the stated ranges (as of June 2026):
- **aiohttp < 3.9.4**: GHSA-jwhx-xcg6-8xhj — HTTP request smuggling
- **aiohttp < 3.9.2**: CVE-2024-23334 — path traversal in `static_route` (low risk for this use case but applies to the dependency range)
- **aiohttp < 3.10.11**: GHSA-v6wp-4m6f-hafc — open redirect
- **requests < 2.32.0**: CVE-2024-35195 — credential leakage via proxy redirect (low risk but within the stated range)
- **gunicorn < 22.0.0**: CVE-2024-1135 — HTTP request smuggling

## Why this matters
An operator who runs `pip install -r requirements.txt` today gets the latest versions, which may be secure. But a `pip install` run 6 months from now (or in a CI that caches `pip`'s index but not exact versions) may resolve to a vulnerable version without any warning.

## Attack or failure scenario
1. A deployment uses a stale pip cache that resolves `aiohttp>=3.9` to `3.9.1`.
2. An attacker exploits CVE-2024-23334 path traversal via a crafted URL.
3. No automated check flags the vulnerable version because there is no pinning or CVE audit step.

## Root cause
The dependency specification was written for developer convenience (always get latest) without providing a production-grade lockfile. This is common in rapidly-developed projects where supply-chain security is deferred.

## Recommended fix
1. Generate a pinned lockfile: `pip-compile requirements.txt --generate-hashes -o requirements.lock`.
2. In CI, install from the lockfile: `pip install --require-hashes -r requirements.lock`.
3. Add `pip-audit --requirement requirements.txt` to CI to fail on known CVEs.
4. Run `pip-compile --upgrade` on a regular cadence (monthly or triggered by Dependabot).
5. Set minimum safe bounds: e.g. `aiohttp>=3.10.11`, `gunicorn>=22.0.0`, `requests>=2.32.0`.

## Acceptance criteria
- A `requirements.lock` file with hash-pinned packages exists in the repository.
- CI installs from the lockfile with `--require-hashes`.
- `pip-audit` runs in CI and fails on any CVSS >= 7.0 finding.
- No package in the lockfile falls within a known-CVE version range.

## Suggested labels
security, dependencies, production-readiness

## Priority
P1

## Severity
High — Unpinned dependencies with known CVE ranges in the stated lower bounds (aiohttp request smuggling, gunicorn request smuggling) can lead to silent installation of vulnerable versions.

## Confidence
Confirmed — the `>=`-only constraints are present; listed CVEs are confirmed against the aiohttp and gunicorn advisories.
