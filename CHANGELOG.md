# Changelog

### Bug Fixes

  * fix(security): use unsafe-hashes for style-src; allow unpkg source maps (issue #41 follow-up) (45c3af5) by grisun0
  * fix(security): no side effects at import in config.py (issue #49) (7cd9063) by grisun0
  * fix(security): audit log size cap with in-place rotation (issue #48) (308fdea) by grisun0
  * fix(security): validate 'relation' against whitelist in KuzuGraphBackend.neighbors (issue #46) (3daf4da) by grisun0
  * fix(security): disable WiGLE source until Basic Auth is wired (issue #45) (53713c6) by grisun0
  * fix(security): redact exception details from /api/run, /api/intel/resolve, /api/intel/graph (issue #44) (05c85d5) by grisun0
  * fix(security): /api/export now writes to tempdir and cleans up (issue #43) (882134a) by grisun0
  * fix(security): portable BASH_SOURCE path in _multi_test.sh (issue #42) (197897f) by grisun0
  * fix(security): pin dependency upper bounds to keep CVE ranges out (issue #40) (cac36bc) by grisun0
  * fix(security): real CI workflow + working Dependabot (issue #39) (4b04c62) by grisun0
  * fix(security): set Reddit-compliant User-Agent (issue #37) (481846e) by grisun0
  * fix(security): require auth + rate-limit on /api/status (issue #35) (b7596c2) by grisun0
  * fix(security): escape e.type / entity.type in innerHTML; drop unsafe-inline (issues #34, #41) (aa00d29) by grisun0
  * fix(security): remove tracked reports/*.json with real intel (issue #33) (a359237) by grisun0
  * fix(security): LLM timeout race — separate HTTP timeout from wait_for (issue #32) (74ed128) by grisun0
  * fix(security): require auth on /api/intel/*, /api/transform/*, /api/osiris/*, /api/fusion/* (issues #26-#31) (8a8c740) by grisun0
  * fix(security): classify 5 image-fetcher sources as contact=active (issues #21-#25) (0af96f1) by grisun0
  * fix(security): require auth + rate-limit on /api/discover/* (issues #15-#19, #35) (4548398) by grisun0
  * fix(security): bound RUN_STREAM_JOBS and DISCOVER_JOBS with LRU+TTL eviction (issues #14, #20, #50) (c6c20cb) by grisun0
  * fix(security): require auth on /api/run/stream and /api/run/stream/stop (issues #12, #13) (574671f) by grisun0
  * fix(security): require auth on POST /api/run/stream/start (issue #11) (5ddd478) by grisun0
  * fix(security): clamp client-controlled parallel/timeout/deadline on /api/run (issue #10) (fc84c5d) by grisun0
  * fix(security): require auth on /api/run (issue #9) (3f64159) by grisun0
  * fix(security): remove plaintext intel bundle after encryption (issue #8) (6433313) by grisun0
  * fix(security): require auth on /api/export/<fmt> (issue #7) (e38b650) by grisun0
  * fix(security): require auth on /api/graph (issue #6) (c13bd9d) by grisun0
  * fix(security): require auth on /api/cases/diff (issue #5) (18c878d) by grisun0
  * fix(security): require auth on POST /api/cases/<id>/save (issue #4) (d0778c3) by grisun0
  * fix(security): require auth on DELETE /api/cases/<id> (issue #3) (290b280) by grisun0
  * fix(security): require auth on GET /api/cases/<id> (issue #2) (ae5cbbf) by grisun0
  * fix(security): bearer-token auth gate for /api/cases (issue #1) (ea286e8) by grisun0

### Documentation

  * docs: auto-generate knowledge base with readmenator (66b52e2) by readmenator-bot
  * docs: auto-generate knowledge base with readmenator (62d7f8e) by readmenator-bot
  * docs(security): make rate-limiter multi-worker caveat loud (issue #38) (6810072) by grisun0

### Chores

  * Update README.md (1eb59a9) by Grisuno
  * new discover (4f95f35) by grisun0
  * 3d awesome vieew in doc sphere (f93f77f) by grisun0
  * 3d awesome vieew in doc sphere and some ablation (4c41d43) by grisun0
  * 3d awesome view (6102ff9) by grisun0
  * 3d view improved (159c7c9) by grisun0
  * graphrag like context to llm (f5818ba) by grisun0
  * a brand new doc (f52ea65) by grisun0
  * Merge rescate: a brand new 3d view of graphRag (ad70fb5) by grisun0
  * a brand new 3d view of graphRag (837f162) by grisun0
  * Merge docs-export into main (40379c2) by grisun0
  * Merge security-export into main (cd3386b) by Grisuno
  * chore(security): export issues + knowledge base + agent docs + network links (2389baa) by grisuno security-export bot
  * more sources :D (d4bf14f) by grisun0
  * Merge branch 'main' of https://github.com/grisuno/estorides (d0ecb20) by grisun0
  * trasnformation like maltego and doc (8bcb543) by grisun0
  * Create static.yml (cd053a6) by Grisuno
  * sec (28ef260) by grisun0
  * doc (959a7dd) by grisun0
  * doc (c27c171) by grisun0
  * test (18dd50f) by grisun0
  * openstreetmap and security fix (ca66de4) by grisun0
  * refactorm bugfixing, and delete dead code (bb9d3aa) by grisun0
  * mejora continua (4e125f5) by grisun0
  * hardening (64d4647) by grisun0
  * new features and some of love (86c029e) by grisun0
  * Merge pull request #92 from grisuno/dependabot/github_actions/actions/setup-python-7 (1a1fcad) by Grisuno
  *  osint tools support in yaml files :D (dca044a) by grisun0
  * Best auto detection to local's models (a2d4d0b) by grisun0
  * estorides_core/source_loader.py	Accepts tool.binary blocks as valid source type (324c2a4) by grisun0
  * chore(deps): bump actions/setup-python from 6 to 7 (98b6c2f) by dependabot[bot]
  * Merge branch 'main' of https://github.com/grisuno/estorides (375c816) by grisun0
  * Doc(creation documentation) a brand new KNOWLEDGE_BASE.md (10f1abe) by grisun0
  * Merge pull request #81 from grisuno/docs-export (60e88da) by Grisuno
  * Merge pull request #86 from grisuno/security-export (52e73de) by Grisuno
  * chore(security): export issues, dependabot & codescan alerts (02a051f) by grisuno security-export bot
  * Alerts systems :D (a29135d) by grisun0
  * Doc(creation documentation) a brand new KNOWLEDGE_BASE.md (e59cad7) by grisun0
  * a brand NEW Source agregator :D (1a18753) by grisun0
  * Security fixes (b6d213d) by grisun0
  * Seecurity advisorys (e733506) by grisun0
  * Doc(creation documentation) a brand new KNOWLEDGE_BASE.md (8a40179) by grisun0
  * generate utotoken to stop unautorized use (e3d7115) by grisun0
  * Doc(creation documentation) a brand new KNOWLEDGE_BASE.md (cc2d5d1) by grisun0
  * Doc(creation documentation) a brand new KNOWLEDGE_BASE.md (698f1a9) by grisun0
  * Source hierarchy, Source health monitoring, Entity resolution, Probabilistic fusion (b847188) by grisun0
  * fussion data improvements (348b807) by grisun0
  * Merge branch 'main' of https://github.com/grisuno/estorides (8fc23b3) by grisun0
  * a new fussion data, some love in ui/ux, and persistent graph (96f68fb) by grisun0
  * Merge pull request #69 from grisuno/dependabot/pip/gunicorn-gte-22.0-and-lt-27.0 (75ae7a9) by Grisuno
  * chore(deps): update gunicorn requirement (d9eca4b) by dependabot[bot]
  * some love (8054111) by grisun0
  * Merge branch 'main' of https://github.com/grisuno/estorides (5a81dc0) by grisun0
  * hotfixing (5672a52) by grisun0
  * Merge pull request #57 from grisuno/security-export-2026-06-29-20260629_131848 (8f047de) by Grisuno
  * chore(security): export issues, dependabot & codescan alerts (ee88f1f) by grisuno security-export bot
  * Merge pull request #55 from grisuno/dependabot/github_actions/actions/checkout-7 (0155d08) by Grisuno
  * Merge pull request #56 from grisuno/dependabot/github_actions/actions/setup-python-6 (a82a9d0) by Grisuno
  * Merge pull request #51 from grisuno/security-export-2026-06-28-20260628_164956 (8e015cc) by Grisuno
  * Merge branch 'main' into security-export-2026-06-28-20260628_164956 (21aa6ce) by Grisuno
  * Merge pull request #52 from grisuno/security-export-2026-06-28-20260628_171901 (bc0ed23) by Grisuno
  * Merge branch 'main' into security-export-2026-06-28-20260628_171901 (865378b) by Grisuno
  * Merge pull request #53 from grisuno/security-export-2026-06-29-20260629_013021 (3d480d6) by Grisuno
  * Merge branch 'main' into security-export-2026-06-29-20260629_013021 (ee1f2bf) by Grisuno
  * Merge pull request #54 from grisuno/security-export-2026-06-29-20260629_061645 (be2b0aa) by Grisuno
  * hotfixing (3c0c9b6) by grisun0
  * Bump actions/setup-python from 5 to 6 (196f695) by dependabot[bot]
  * Bump actions/checkout from 4 to 7 (2b58610) by dependabot[bot]
  * chore(security): export issues, dependabot & codescan alerts (5f52aab) by grisuno security-export bot
  * chore(security): export issues, dependabot & codescan alerts (cc8c5bc) by grisuno security-export bot
  * chore(security): export issues, dependabot & codescan alerts (9633982) by grisuno security-export bot
  * chore(security): export issues, dependabot & codescan alerts (e28b71f) by grisuno security-export bot
  * more fancy css (d51c1a9) by grisun0
  * new Claude.md hardened SDD + TDD + BDD a new hypotesis engine steel is a poc. some test and love (b690301) by grisun0
  * Update README.md (d1ced35) by Grisuno
  * Estorides nuevo fusionador de información (44a2e8c) by grisun0
  * some love (f073465) by grisun0
  * Merge branch 'main' of https://github.com/grisuno/estorides (80d7052) by grisun0
  * some love to ui :D (c39ea2d) by grisun0
  * Update README.md (34485a8) by Grisuno
  * v1.3 frontend: case save/diff/report actions + diff panel + report modal (e6a0fc2) by Hermes
  * new (2f26f04) by grisun0
  * new virus total api and graph tool interactive (e5b2856) by grisun0
  * update main (c6f9b01) by grisun0
  * v1.2 — background discoverer + click-to-expand + 101 sources (ff5c980) by grisun0
  * Update README.md (3ee5d2d) by Grisuno
  * Add files via upload (3d1a406) by Grisuno
  * Add files via upload (c58f9a3) by Grisuno
  * Add files via upload (e5eb81e) by Grisuno
  * Add files via upload (b346f58) by Grisuno
  * Add files via upload (69dc771) by Grisuno
  * Add files via upload (c2df9e6) by Grisuno
  * Add files via upload (c1bd06b) by Grisuno
  * Add files via upload (caae925) by Grisuno
  * Add files via upload (010fe79) by Grisuno
  * Add files via upload (43df94f) by Grisuno
  * Add files via upload (0489cca) by Grisuno
  * Add files via upload (651b61f) by Grisuno
  * Create README.md (5b4a220) by Grisuno
  * Create README.md (91eb05f) by Grisuno
  * Create README.md (a59e67b) by Grisuno
  * Create README.md (3e83e91) by Grisuno
  * Create README.md (aeaa9e8) by Grisuno
  * Create README.md (bdf930a) by Grisuno
  * Create README.md (df1e29c) by Grisuno
  * Create README.md (3c53517) by Grisuno
  * Create README.md (bdb738a) by Grisuno
  * Create README.md (a5323e8) by Grisuno
  * Create README.md (37a947f) by Grisuno
  * Create README.md (8c373f3) by Grisuno
  * Add files via upload (7684b93) by Grisuno
  * Create README.md (ae551c9) by Grisuno
  * Add files via upload (0f67d80) by Grisuno
  * Add files via upload (8dd10f1) by Grisuno
  * Add files via upload (7a2afe9) by Grisuno
  * Add files via upload (2830bcc) by Grisuno
  * Add files via upload (fdd5827) by Grisuno
  * Create README.md (dfdfb2a) by Grisuno
  * Create README.md (4f236f3) by Grisuno
  * Add files via upload (858ba4f) by Grisuno
  * Add files via upload (172c876) by Grisuno
  * Create README.md (21afe33) by Grisuno
  * Create README.md (74127b4) by Grisuno
  * Create README.md (cad93ec) by Grisuno
  * Create README.md (aef22e7) by Grisuno
  * Create README.md (704b55b) by Grisuno
  * Create README.md (38de201) by Grisuno
  * Create README.md (b6e14ba) by Grisuno
  * Create README.md (2e8daff) by Grisuno
  * Create README.md (ad7985b) by Grisuno
  * Update README.md (75f9a28) by Grisuno
  * Add files via upload (31b36fa) by Grisuno


_Generated by [deploynator](https://github.com/grisuno/deploynator)_