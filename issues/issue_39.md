# Issue #39: GitHub Actions workflow is a non-functional demo; Dependabot is misconfigured with an empty package-ecosystem

- **State:** open
- **Created:** 2026-06-08T11:42:58Z
- **Updated:** 2026-06-08T11:42:58Z
- **Labels:** None

---

## Summary
The GitHub Actions workflow at `workflows/github-actions-demo.yml` is a copy-paste demo that runs no tests, no linting, no security scanning, and no dependency auditing. It only runs `echo` and `ls` commands. A second workflow file at `.github/workflows/` (if one existed) would be needed for any real CI. The Dependabot configuration at `.github/dependabot.yml` has an empty `package-ecosystem: ""` field, rendering it non-functional — Dependabot will never open PRs for vulnerable dependencies.

## Evidence
`workflows/github-actions-demo.yml` (note: this file is in `workflows/` not `.github/workflows/`, so it does not trigger GitHub Actions at all):
```yaml
name: GitHub Actions Demo
on: [push]
jobs:
  Explore-GitHub-Actions:
    steps:
      - run: echo "The job was automatically triggered..."
      - run: echo "This job is running on..."
      - name: List files in the repository
        run: ls ${{ github.workspace }}
```

`.github/dependabot.yml`:
```yaml
version: 2
updates:
  - package-ecosystem: ""   # EMPTY — Dependabot is disabled
    directory: "/"
    schedule:
      interval: "weekly"
```

The workflow file is at `workflows/github-actions-demo.yml` (no `.github/` prefix), so GitHub never executes it. There is no real CI pipeline in `.github/workflows/`.

## Why this matters
No automated checks run on any commit:
- Vulnerable dependencies are never flagged (e.g. `aiohttp>=3.9` allows installation of versions with known CVEs).
- No linting catches the `int(request.args.get(...))` antipattern before it ships.
- No security scanning (Bandit, Semgrep) catches XSS or injection patterns.
- New contributors have no automated feedback loop.

## Attack or failure scenario
A contributor adds a route with a bare `eval()` call, an SQL injection in a `format()` string, or a new hardcoded credential. No CI check fails. The code ships to anyone who clones or forks the repository.

## Root cause
The demo workflow was never moved to `.github/workflows/` and was never replaced with a real CI configuration. Dependabot was configured from a template that was never completed.

## Recommended fix
1. Move or create a real workflow at `.github/workflows/ci.yml` that runs:
   - `python -m pytest` (all test suites)
   - `python -m ruff check .` (lint)
   - `python -m bandit -r estorides_core/ estorides_llm/ estorides_export/` (SAST)
   - `pip-audit --requirement requirements.txt` (dependency CVE audit)
2. Fix `.github/dependabot.yml` to set `package-ecosystem: "pip"`.
3. Delete `workflows/github-actions-demo.yml` or move it to `.github/workflows/` once real checks are in place.

## Acceptance criteria
- A functional workflow exists at `.github/workflows/ci.yml` and is triggered on `push` and `pull_request`.
- The workflow runs at least: tests, lint, and dependency CVE audit.
- `.github/dependabot.yml` has `package-ecosystem: "pip"` and is valid.
- Dependabot opens its first PR within a week of merge.

## Suggested labels
ci-cd, security, technical-debt

## Priority
P1

## Severity
High — No CI pipeline means no automated security or quality gate on any commit. The Dependabot misconfiguration means vulnerable dependency PRs are never opened.

## Confidence
Confirmed — the workflow file location and Dependabot configuration are directly verifiable.
