# Issue #33: Real OSINT investigation data (IPs, domains) committed to git in reports/bundle_1780871293.json

- **State:** closed
- **Created:** 2026-06-08T11:42:27Z
- **Updated:** 2026-06-29T16:16:06Z
- **Labels:** None

---

## Summary
A 6.9 MB STIX 2.1 bundle containing real-domain and real-IP OSINT investigation output has been committed to the repository at `reports/bundle_1780871293.json` and is publicly accessible. The bundle contains 15,487 STIX objects including real IP addresses (e.g. `102.129.63.94`, `34.77.211.171`, `88.20.35.1`, `109.122.217.21`) and real domain names gathered during what appears to be a reconnaissance run against `dnsdumpster.com` and related infrastructure.

## Evidence
- File: `reports/bundle_1780871293.json` (tracked in git, publicly readable)
- File size: ~6.9 MB, 15,487 STIX objects
- Real IP addresses confirmed present: `102.129.63.94`, `34.77.211.171`, `107.189.24.77`, `103.165.68.187`, `101.96.200.56`, `88.20.35.1` and ~20+ others
- Real domain names: `dnsdumpster.com`, `api.dnsdumpster.com`, `dnsdumpster.bsky.social`, `threads.net`, `bsky.app` and hundreds more
- Created timestamp from bundle ID: `1780871293` (unix epoch June 2026)
- `.gitignore` does not exclude `reports/*.json`

## Why this matters
This commits real investigative intelligence data — IP addresses and domain infrastructure — to a public repository permanently. Any subjects of the investigation can discover they were investigated. The data may contain sensitive OSINT that should never be publicly archived in a git history that cannot be scrubbed without a forced push.

## Attack or failure scenario
1. An entity whose IP or domain appears in the bundle discovers the file via a Google dork or GitHub search.
2. They can now determine they were OSINT-investigated, when the investigation occurred, and what infrastructure was correlated against theirs.
3. Adversarial actors can also mine the bundle for victim infrastructure data associated with the investigation subject.

## Root cause
`reports/` is checked into git without a corresponding `.gitignore` rule to exclude generated intelligence artifacts. The export endpoint writes new files to this directory on every `/api/export/<fmt>` call, and the directory is part of the repository root.

## Recommended fix
1. Add `reports/*.json`, `reports/*.graphml`, `reports/*.age` to `.gitignore` immediately.
2. Remove the committed bundle from git history: `git filter-repo --path reports/bundle_1780871293.json --invert-paths` and force-push.
3. Update the `REPORTS_DIR` in config to default to a path outside the repository, or write exports to `tempfile.mkdtemp()`.
4. Add a CI check that fails if any file over 1 MB is staged under `reports/`.

## Acceptance criteria
- `reports/bundle_1780871293.json` is no longer present in git history.
- `.gitignore` excludes all generated report files (`*.json`, `*.graphml`, `*.age`, `*.jsonl`) under `reports/` and `data/`.
- A new commit adds pre-commit hook or CI step blocking large generated files from being committed.
- `REPORTS_DIR` defaults to a location outside the repository tree.

## Suggested labels
security, privacy, production-readiness

## Priority
P0

## Severity
Critical — Real OSINT investigation data (IP addresses, domains) is publicly committed to a permanent git history and reveals investigative targets and their infrastructure.

## Confidence
Confirmed — file is present in the repository, real IPs confirmed by inspection of the JSON content.
