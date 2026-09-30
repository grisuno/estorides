# Recipe: Fix a Dependency Cycle

Target cycle: `estorides_web.py` -> `estorides_web_tools.py` -> `estorides_web.py`

1. Read the imports between these files: `grep -n '^import\|^from\|#include' estorides_web.py`, `grep -n '^import\|^from\|#include' estorides_web_tools.py`
2. Move the shared symbols into a new leaf module both sides import
3. Verify: `readmenator . && grep -c 'Dependency Cycles' readmenator-agent/GOTCHAS.md`
