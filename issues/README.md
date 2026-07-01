# Repository: estorides

**Description:** Open-source intelligence (OSINT) aggregator and correlation engine inspired by Palantir, Bellingcat, Maltego, and Citizen Lab workflows. A pure open-source re-imagining of the original fucklantir / osint_palantir toolchain, with a much bigger source catalogue, a proper knowledge graph, structured parsers, and a multi-backend LLM analyst.

| Metric | Value |
|--------|-------|
| ⭐ Stars | 63 |
| 📥 Clones (last 14 days) | 751 |
| 🟢 Open Issues | 1 |
| 📋 Total Issues | 50 |
| 🛡 Dependabot Open Alerts | 0 |
| 🔍 CodeScan Open Alerts | 14 |

## Issues
- [#50](./issue_50.md) - RUN_STREAM_JOBS and DISCOVER_JOBS hold BufferedEventSink objects indefinitely — memory exhaustion via sustained job creation (closed)
- [#49](./issue_49.md) - estorides_core/config.py creates filesystem directories at module import time — violates project's own hard rules (closed)
- [#48](./issue_48.md) - Audit log (data/audit.jsonl) has no rotation, size cap, or retention policy — unbounded growth and privacy risk (closed)
- [#47](./issue_47.md) - /api/graph serves the last operator's full intelligence graph without authentication or session isolation (closed)
- [#46](./issue_46.md) - Latent Cypher injection in KuzuGraphBackend.neighbors() via unsanitised relation parameter (closed)
- [#45](./issue_45.md) - WiGLE source references non-existent env var WIGLE_API_NAME_WIGLE_API_API_KEY — source never authenticates (closed)
- [#44](./issue_44.md) - Internal exception details (file paths, schema names, query fragments) returned to unauthenticated API clients (closed)
- [#43](./issue_43.md) - /api/export/<fmt> creates permanent unbounded files in reports/ — unauthenticated disk exhaustion attack (closed)
- [#42](./issue_42.md) - _multi_test.sh hardcodes developer's home directory path, breaking all end-to-end tests for every other user (closed)
- [#41](./issue_41.md) - CSP includes style-src 'unsafe-inline', enabling CSS injection and data exfiltration from intelligence reports (closed)
- [#40](./issue_40.md) - All dependencies are unpinned (>=only) with no lockfile; multiple CVE ranges are reachable (aiohttp, gunicorn) (closed)
- [#39](./issue_39.md) - GitHub Actions workflow is a non-functional demo; Dependabot is misconfigured with an empty package-ecosystem (closed)
- [#38](./issue_38.md) - In-process rate limiter is multiplied by gunicorn worker count — effective limit is N_workers × 30/min (closed)
- [#37](./issue_37.md) - Reddit sources scrape the JSON API without OAuth, violating Reddit's ToS and causing IP blocking (closed)
- [#36](./issue_36.md) - Bare int() casts on user-controlled query parameters cause unhandled ValueError (500) on four endpoints (closed)
- [#35](./issue_35.md) - /api/graph, /api/status, and all /api/discover/* endpoints are missing rate limiting (closed)
- [#34](./issue_34.md) - Stored XSS via unescaped entity.type field in innerHTML template literals (closed)
- [#33](./issue_33.md) - Real OSINT investigation data (IPs, domains) committed to git in reports/bundle_1780871293.json (closed)
- [#32](./issue_32.md) - [CRITICAL] #3: Unsafe LLM timeout handling causes race condition (closed)
- [#31](./issue_31.md) - Public /api/osiris/* endpoints turn the deployment into an unauthenticated third-party reconnaissance relay (closed)
- [#30](./issue_30.md) - Unauthenticated /api/transform/run turns resolver, VirusTotal, GitHub, and breach lookups into a public enrichment relay (closed)
- [#29](./issue_29.md) - Unauthenticated /api/intel/stats leaks corpus size and internal database paths (closed)
- [#28](./issue_28.md) - /api/intel/graph accepts arbitrary expensive Cypher with no server-side timeout or enforced row cap (closed)
- [#27](./issue_27.md) - Unauthenticated /api/intel/graph exposes the persistent intelligence graph through arbitrary read-only Cypher (closed)
- [#26](./issue_26.md) - Unauthenticated /api/intel/resolve leaks cross-run intelligence and can spend VirusTotal quota (closed)
- [#25](./issue_25.md) - exif_remove_lookup is misclassified as contact=none even though the provider fetches the submitted image URL (closed)
- [#24](./issue_24.md) - pages_dev_meta is misclassified as contact=none even though Microlink fetches the submitted target URL (closed)
- [#23](./issue_23.md) - microlink is misclassified as contact=none even though it fetches and screenshots target URLs (closed)
- [#22](./issue_22.md) - screenshotmachine is misclassified as contact=none even though the provider fetches target URLs (closed)
- [#21](./issue_21.md) - tineye_reverse is misclassified as contact=none even though TinEye actively fetches the target URL (closed)
- [#20](./issue_20.md) - DISCOVER_JOBS is never evicted, allowing anonymous callers to retain unbounded job state in memory (closed)
- [#19](./issue_19.md) - Unauthenticated /api/discover/stop lets any caller cancel discovery jobs (closed)
- [#18](./issue_18.md) - Unauthenticated /api/discover/stream leaks live discovery events and case IDs (closed)
- [#17](./issue_17.md) - Unauthenticated /api/discover/jobs discloses every active discovery job and seed (closed)
- [#16](./issue_16.md) - Minimal-install deployments crash /api/discover/start when kuzu is absent (closed)
- [#15](./issue_15.md) - Unauthenticated /api/discover/start lets arbitrary callers queue background discovery crawls (closed)
- [#14](./issue_14.md) - RUN_STREAM_JOBS is never evicted, so anonymous callers can grow server memory without bound (closed)
- [#13](./issue_13.md) - Unauthenticated /api/run/stream/stop lets any caller cancel another user's deep search (closed)
- [#12](./issue_12.md) - Unauthenticated /api/run/stream leaks live deep-search events and case IDs (closed)
- [#11](./issue_11.md) - Unauthenticated /api/run/stream/start lets any caller launch deep recursive cross-search jobs (closed)
- [#10](./issue_10.md) - Client-controlled parallel, timeout, and deadline values make /api/run a single-request resource exhaustion primitive (closed)
- [#9](./issue_9.md) - Unauthenticated /api/run allows arbitrary callers to burn paid-source keys and upstream quota (closed)
- [#8](./issue_8.md) - Encrypted export leaves plaintext intelligence artifacts on disk in reports/ (closed)
- [#7](./issue_7.md) - Unauthenticated /api/export/<fmt> lets any caller download shared investigation artifacts (closed)
- [#6](./issue_6.md) - Shared global GraphML file lets /api/graph disclose the last user's investigation (closed)
- [#5](./issue_5.md) - Unauthenticated /api/cases/diff reveals deltas between arbitrary investigations (closed)
- [#4](./issue_4.md) - Unauthenticated POST /api/cases/<id>/save lets any caller overwrite case notes (closed)
- [#3](./issue_3.md) - Unauthenticated DELETE /api/cases/<id> lets any caller destroy persisted investigations (closed)
- [#2](./issue_2.md) - Unauthenticated /api/cases/<id>?full=1 exposes raw observations, entities, and analyst output (closed)
- [#1](./issue_1.md) - Unauthenticated /api/cases leaks the full historical investigation corpus (closed)

## Code Scanning Alerts
- [CodeScan #20](./codescan/alert_20.md) - js/xss-through-dom (warning) - open
- [CodeScan #19](./codescan/alert_19.md) - py/stack-trace-exposure (error) - open
- [CodeScan #18](./codescan/alert_18.md) - py/stack-trace-exposure (error) - open
- [CodeScan #17](./codescan/alert_17.md) - actions/missing-workflow-permissions (warning) - open
- [CodeScan #16](./codescan/alert_16.md) - js/xss-through-dom (warning) - open
- [CodeScan #13](./codescan/alert_13.md) - py/incomplete-url-substring-sanitization (warning) - open
- [CodeScan #12](./codescan/alert_12.md) - py/incomplete-url-substring-sanitization (warning) - open
- [CodeScan #11](./codescan/alert_11.md) - py/url-redirection (error) - open
- [CodeScan #10](./codescan/alert_10.md) - py/clear-text-logging-sensitive-data (error) - open
- [CodeScan #9](./codescan/alert_9.md) - py/stack-trace-exposure (error) - open
- [CodeScan #8](./codescan/alert_8.md) - py/stack-trace-exposure (error) - open
- [CodeScan #7](./codescan/alert_7.md) - py/stack-trace-exposure (error) - open
- [CodeScan #6](./codescan/alert_6.md) - py/stack-trace-exposure (error) - open
- [CodeScan #5](./codescan/alert_5.md) - py/stack-trace-exposure (error) - open

Total issues downloaded: 50
