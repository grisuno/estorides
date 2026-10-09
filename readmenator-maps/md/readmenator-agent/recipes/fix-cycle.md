# Recipe: Fix a Dependency Cycle

Target cycle: `estorides_export/__init__.py` -> `estorides_export/encryption.py` -> `estorides_export/__init__.py`

1. Read the imports between these files: `grep -n '^import\|^from\|#include' estorides_export/__init__.py`, `grep -n '^import\|^from\|#include' estorides_export/encryption.py`
2. Move the shared symbols into a new leaf module both sides import
3. Verify: `readmenator . && grep -c 'Dependency Cycles' readmenator-agent/GOTCHAS.md`
