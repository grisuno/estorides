#!/bin/bash
set -e
# Issue #42: replace the developer's hardcoded home-directory path
# with a portable BASH_SOURCE-derived path. This pattern is identical
# to the one already used in install.sh.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== TEST 1: IP query (8.8.8.8) ==="
timeout 50 python3 estorides_cli.py run 8.8.8.8 --parallel 4 2>&1 | grep -E "query_type|sources queried|sources succeeded|Top entities|backend" | head -8
echo ""
echo "=== TEST 2: Domain query (example.com) ==="
timeout 50 python3 estorides_cli.py run example.com --parallel 4 2>&1 | grep -E "query_type|sources queried|sources succeeded|Top entities|backend" | head -8
echo ""
echo "=== TEST 3: Email query (user@example.com) ==="
timeout 50 python3 estorides_cli.py run user@example.com --parallel 4 2>&1 | grep -E "query_type|sources queried|sources succeeded|Top entities|backend" | head -8
echo ""
echo "=== TEST 4: BTC query ==="
timeout 50 python3 estorides_cli.py run 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa --parallel 4 2>&1 | grep -E "query_type|sources queried|sources succeeded|Top entities|backend" | head -8
echo ""
echo "=== TEST 5: CVE query ==="
timeout 50 python3 estorides_cli.py run CVE-2024-3094 --parallel 4 2>&1 | grep -E "query_type|sources queried|sources succeeded|Top entities|backend" | head -8
echo ""
echo "ALL TESTS DONE"
