# Issue #42: _multi_test.sh hardcodes developer's home directory path, breaking all end-to-end tests for every other user

- **State:** open
- **Created:** 2026-06-08T11:43:11Z
- **Updated:** 2026-06-08T11:43:11Z
- **Labels:** None

---

## Summary
`_multi_test.sh` hardcodes the developer's absolute filesystem path (`/home/grisun0/src_note/py/fucklantir/estorides`) on line 3. This file is committed to the repository and will silently fail for every user who is not the original developer, since `cd` to a non-existent path will cause `set -e` to abort the script with no test results.

## Evidence
`_multi_test.sh` line 3:
```bash
#!/bin/bash
set -e
cd /home/grisun0/src_note/py/fucklantir/estorides
```

This is the only operational step before all five `timeout 50 python3 estorides_cli.py run ...` commands. If a contributor or CI system runs this script, the `cd` fails, `set -e` terminates the script immediately, and no tests are run — with exit code 1 (cd failure), which CI will interpret as a test failure even though no test was executed.

## Why this matters
This makes end-to-end testing non-functional for every user except the original developer. Contributors who try to run the test suite and see it "fail" on the `cd` may conclude the tests are broken and give up. CI pipelines cannot use this script. It reveals the developer's home directory structure and former project name (`fucklantir`).

## Attack or failure scenario
1. A new contributor clones the repository and runs `bash _multi_test.sh`.
2. The `cd /home/grisun0/...` fails immediately (directory does not exist on their machine).
3. `set -e` aborts the script.
4. The contributor sees no test output and no feedback, and may incorrectly conclude the platform is broken.

## Root cause
The path was hardcoded during development and never replaced with a relative or portable path before the file was committed.

## Recommended fix
Replace the hardcoded path with a dynamic one:
```bash
#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
```

This is exactly the pattern already used in `install.sh` lines 8-9.

## Acceptance criteria
- `_multi_test.sh` uses a relative or `BASH_SOURCE[0]`-derived path instead of a hardcoded absolute path.
- Running `bash _multi_test.sh` from any working directory completes without a `cd` failure.
- The developer's home directory path does not appear in any committed file.

## Suggested labels
bug, testing

## Priority
P2

## Severity
Medium — Breaks all end-to-end testing for everyone except the original developer; information disclosure (developer path, prior project name).

## Confidence
Confirmed — hardcoded path is present on line 3 of the committed file.
