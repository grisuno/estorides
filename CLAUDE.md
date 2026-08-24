# Estorides — Inviolable Development Rules (CLAUDE.md)

Este archivo es la **doctrina** del proyecto. Cualquier contribución (humana o
agente) debe respetarla. Si una regla entra en conflicto con la velocidad, gana
la regla. Si una regla entra en conflicto con la funcionalidad pedida, gana la
regla y se discute la regla.

> Estas reglas son **inviolables**. No son recomendaciones. No son nice-to-have.
> No se saltan "porque es un cambio pequeño". No se saltan "porque total el
> usuario no se va a enterar". El ciclo completo es por módulo, no por PR.

---

## 0 · Glosario

- **SDD** — Spec-Driven Development. La especificación se escribe **antes** del
  código. No se escribe código sin `spec/<modulo>.md` aprobado.
- **TDD** — Test-Driven Development. El test se escribe **antes** del código de
  producción. Debe fallar (rojo) antes de escribirse la implementación.
- **BDD** — Behaviour-Driven Development. Los tests se redactan como escenarios
  *Given-When-Then* y describen comportamiento observable, no implementación.
- **ATDD** — Acceptance Test-Driven Development. Un test de aceptación expresa
  el criterio de "hecho" y debe pasar antes de cerrar el módulo.
- **Boy-scout** — Extinguir deuda técnica vista al pasar. Nunca fuera de scope.
- **WIP** — Work In Progress. Solo un módulo en `in_progress` a la vez por hilo
  de trabajo.

---

## 1 · El ciclo inviolable (orden estricto)

Para cada módulo nuevo, **en este orden**:

1. **Spec** — `spec/<modulo>.md`. Secciones obligatorias:
   - **Purpose** (1 párrafo, qué problema resuelve y por qué).
   - **Inputs** (tipos, rangos, formato, casos vacíos).
   - **Outputs** (forma exacta del retorno, en pseudo-tipo o JSON-schema).
   - **Tabla de errores** (cada modo de fallo, código, mensaje, comportamiento).
   - **Garantías de seguridad** (qué se valida, qué se rechaza, qué se loguea).
   - **Out of scope** (lo que el módulo **no** hace; lo que se deja a otros).
   - **Escenarios BDD Given-When-Then** (mínimo 4: happy path, edge, error,
     seguridad). Los escenarios son contratos. Cambian solo con acuerdo
     explícito.

   El spec se escribe **antes** del primer test. Documentar antes de validar
   es documentar lo que todavía no es verdad.

2. **Test (rojo)** — `tests/test_<modulo>.py` con `pytest`. Debe fallar al
   ejecutarlo contra la implementación inexistente. Sin esto no hay paso 3.
   **ATDD explícito**: el test de aceptación se redacta como escenario
   *Given-When-Then* en `spec/<modulo>.md` (sección "Escenarios BDD") y se
   traduce a un test ejecutable en este paso. El test debe poder leerse
   como una frase del spec, sin pegarse a la implementación. Cubrir mínimo
   4 escenarios: happy path, edge, error, seguridad. Los escenarios son
   **contratos** y cambian solo con acuerdo explícito.

3. **Code (verde)** — Mínimo código que haga pasar los tests. **Una sola
   preocupación por módulo**. Si el código necesita tocar otra capa, se abre
   un módulo nuevo con su propio spec.

4. **Refactor** — Endurecer: límites, validación, legibilidad. **Boy-scout
   obligatorio**: si en el refactor se ve código duplicado, se unifica. Si se
   ve una falla de seguridad, se arregla. Si se puede hacer en 10 líneas lo
   que se hacía en 40, se hace. La extinción de deuda técnica y
   vulnerabilidades **nunca está fuera de scope** mientras se respeta SOLID,
   DRY y no se pierde funcionalidad. La regla de reducción de líneas aplica
   también al código de tests: un helper de 4 líneas que se usa en 5 tests
   vale más que 5 copias de 8 líneas. **No se introduce código inseguro**:
   un refactor que cierra una vulnerabilidad es un refactor válido aunque
   toque código fuera del módulo que se está cerrando.

5. **Validación** — Antes de declarar el módulo "hecho":
   - `pytest tests/test_<modulo>.py -v` → todos verdes.
   - `pytest tests/properties/test_<modulo>_properties.py -v` → verdes.
   - `ruff check estorides_core/<modulo>.py tests/test_<modulo>.py` → limpio.
   - `mypy --strict estorides_core/<modulo>.py` → sin errores.
   - `bandit -r estorides_core/<modulo>.py` → sin `High` ni `Medium`.
   - **Mutación obligatoria** — `mutmut run` sobre `estorides_core/<modulo>.py`
     (config `[tool.mutmut]` ya presente en `pyproject.toml`). Objetivo: **0
     supervivientes**. Un mutante que sobrevive significa que hay un
     comportamiento del módulo que ningún test vigila; se añaden tests hasta
     que cada mutante muera o se justifique como mutante equivalente en el
     spec. Este es el cierre del primer módulo con mutación al 100%
     (`observation_models`, 79/79), y desde entonces es requisito para cerrar
     cualquier módulo.
   - Si el módulo toca la GUI: export a PDF + rasterizar a PNG + revisar
     visualmente. Toolchain visual: `chromium --headless --print-to-pdf=...`
     o `firefox --print-to-pdf=...`, `mutool draw -r 96 -o frame.png frame.pdf`,
     `Read frame.png`. El path completo está en `spec/visual_review.md`.
   - Si el módulo toca red o parseo de contenido remoto: ver paso 6.

   **Validación visual (skill `/visual-review`)**: si el módulo renderiza
   HTML/Jinja, la GUI necesita Wayland (no siempre disponible para un agente).
   El render se inspecciona **headless** exportando a PDF y rasterizando.
   Pasos exactos:
     a. Exporta a PDF: `./build/freedom --download-pdf=$SP/frame.pdf <URL-o-html>`
        (`$SP` = el scratchpad de la sesión, NO `/tmp` ni el árbol del repo).
     b. Rasteriza a PNG: `mutool draw -r 96 -o $SP/frame.png $SP/frame.pdf 1`
        (o `-o $SP/frame-%d.png` sin número para todas las páginas).
     c. Lee con `Read $SP/frame.png` (fallback: `Read` del PDF con `pages`).
     d. Verifica: ¿texto legible? ¿posicionamiento correcto (no
        superpuesto)? ¿colores/temas aplicados? ¿artefactos?
     e. Compara con screenshot de referencia si existe.

6. **Fuzzing** — Si el módulo procesa input no confiable (HTTP, JSON remoto,
   archivos subidos, queries), se fuzzea con `hypothesis` (property-based) o
   `atheris` (Python-native libFuzzer). Mínimo 1000 ejemplos aleatorios por
   propiedad invariante. Cero crashes / leaks / UB antes de cerrar.

7. **Documentación** — **Recién después de validar y fuzzear** se documenta:
   - `spec/<modulo>.md` se actualiza con la fecha de cierre, lista de cambios.
   - Este `CLAUDE.md` se actualiza con el hito cerrado y la doctrina nueva.
   - `docs/index.html` se actualiza con el nuevo atajo / enlace al spec /
     enlace al test. **Casi lo más importante**: la home page refleja el
     estado real del proyecto, con todos los atajos y enlaces a specs/tests.
   - `README.md` se actualiza si el módulo cambia funcionalidad visible.
   - Memoria de sesión: cualquier insight reusable se persiste.

   Documentar antes de validar es documentar lo que todavía no es verdad.

> **Excepción de seguridad inquebrantable (no aplica a Python puro):** las
> primitivas que bypasean syscall filtering (`io_uring`, `seccomp` bypass,
> `userfaultfd`) están prohibidas dentro de cualquier worker confinado que
> procese contenido remoto. En Estorides todo el código corre en un solo
> proceso Python: la regla equivalente es que **ningún parser ni inferer
> ejecuta código externo, descarga binarios, ni hace `eval`/`exec`/`os.system`
> sobre datos que no sean del operador**. La SSRF guard (`ssrf_guard.py`)
> y `validation.py` son las paredes; no se relajan.
>
> **Equivalencias C → Python** (para auditoría cruzada con código foráneo
> que cita el ciclo original):
> | C (libre/BSD) | Estorides (Python) | Rol |
> | --- | --- | --- |
> | CMocka / Unity | `pytest` | ATDD + TDD + BDD |
> | libFuzzer / AFL++ | `hypothesis` (property-based) | Fuzzing |
> | cppcheck | `ruff` | Linter |
> | ASan / UBSan | `mypy --strict` | Type-checker (UBSan análogo) |
> | valgrind | `mypy --strict` + `bandit` | Memory + leak (refcount+GIL + scan) |
> | `io_uring` | `asyncio` | I/O asíncrono del lado confiable |
> | `make asan` | `pytest -q` | Build + tests |

---

## 2 · Reglas transversales (todo el proyecto)

- **No se commitea código sin tests verdes.** El CI corre `pytest` + `ruff` +
  `mypy --strict` + `bandit`. Si falla, el PR se cierra.
- **No se introduce código duplicado.** Si dos módulos hacen lo mismo, se
  extrae. Si un helper se usa en 3+ sitios, va a un módulo compartido con su
  propio spec.
- **No se introduce código inseguro.** `bandit` y `mypy --strict` son la red
  mínima. Cualquier excepción se justifica en el spec del módulo afectado.
- **Todo input del usuario/remoto es hostil.** Nunca se trata input de un
  operador o de contenido remoto como fuente confiable: toda URL que se
  abre (`urlopen`, `requests`, webhooks, redirects) pasa por el `ssrf_guard`
  (`check_url`) antes de tocar un socket; todo string remoto que llega a la
  GUI pasa por `escapeHTML`/`escapeAttr`/`safeColor` antes de entrar en HTML,
  atributo o CSS; las rutas se anclan con boundaries en vez de `startswith`/
  `in` de subcadena. Si un fix de seguridad amplía una primitiva, se amplía
  la doctrina (no al revés): el código nuevo sigue la regla, la doctrina se
  actualiza en el mismo cambio.
- **Elevación gráfica con `run0`, no `sudo`.** Estorides es una app GUI en su
  mayoría; la gestión de usuarios debe ser gráfica. Toda elevación de
  privilegios (instalación de tools, etc.) usa `run0` (prompt polkit de
  escritorio). `sudo` solo como fallback si `run0` no existe; si el proceso
  ya es root, no se eleva. Ver `estorides_core/tool_install.py`.
- **No se documenta antes de validar.** El spec se escribe antes del código
  (eso es SDD); la documentación de cierre (changelog, índice, README) va
  después de validar y fuzzear.
- **El spec es contrato.** Cambios de comportamiento rompen el spec. Cambios
  de spec rompen los tests. Los dos a la vez rompen el módulo y se vuelve a
  empezar.
- **Boy-scout sin excusas.** Si en el refactor se ve `TODO` viejo, deuda,
  copia de `os.path.join` mal hecho, falta de validación de input, se arregla
  en el mismo PR. El scope boy-scout es **obligatorio** y **nunca se aplaza**.
- **Solo un módulo en progreso por hilo.** `todowrite` debe mostrar exactamente
  un `in_progress`. El resto, `pending` o `completed`.

---

## 3 · Toolchain (versiones y comandos)

| Herramienta | Propósito | Comando |
| --- | --- | --- |
| `pytest` | TDD/BDD/ATDD | `pytest tests/test_<modulo>.py -v` |
| `hypothesis` | Property-based fuzzing (libFuzzer análogo) | embebido en `tests/test_<modulo>_properties.py` |
| `ruff` | Linter (cppcheck análogo) | `ruff check <path>` |
| `mypy --strict` | Type checker (UBSan análogo) | `mypy --strict <path>` |
| `bandit` | Security scanner | `bandit -r <path>` |
| `mutool` | PDF→PNG (visual review headless) | `mutool draw -r 96 -o frame.png frame.pdf 1` |
| `chromium` | HTML→PDF headless (visual review) | `chromium --headless --disable-gpu --print-to-pdf=out.pdf in.html` |
| `firefox` | Alternativa HTML→PDF | `firefox --print-to-pdf=out.pdf in.html` |

Activación del venv del proyecto: `source .venv/bin/activate`.

---

## 4 · Estructura de directorios

```
estorides/
├── CLAUDE.md                  # este archivo (doctrina)
├── README.md                  # marketing + quickstart
├── docs/
│   └── index.html             # home page con TODOS los atajos y enlaces a specs
├── spec/                      # specs SDD (uno por módulo)
│   └── <modulo>.md
├── tests/                     # tests TDD/BDD/ATDD
│   ├── test_<modulo>.py
│   └── properties/
│       └── test_<modulo>_properties.py
├── estorides_core/            # implementación
│   └── <modulo>.py
└── .scratchpad/              # artefactos temporales de la sesión (PDFs, PNGs)
```

`/tmp` y el árbol del repo **nunca** se usan como scratchpad. Si necesitas
escribir algo durante la sesión: `.scratchpad/`.

---

## 5 · Hitos cerrados (changelog doctrinal)

| Fecha | Módulo | Spec | Tests | Notas |
| --- | --- | --- | --- | --- |
| 2026-06-27 | `reliability_scoring` (item 2a) | `spec/reliability_scoring.md` | `tests/test_reliability_scoring.py` | Bootstrap del ciclo SDD+TDD+BDD. Fuente única de verdad para `confidence` en `entity_extraction.merge`, `fusion_store.fuse_entity`, `entity_resolution.resolve_entities`, `intel_resolver.resolve`. |
| 2026-06-27 | `hypothesis_engine` (item 2b) | `spec/hypothesis_engine.md` | `tests/test_hypothesis_engine.py` | Capa "data → information". 4 generadores (domain-belongsto-actor, email-aliasto-person, ip-shared-infra, asn-shared-infra). Ids deterministas, audit trail completo. Wire-up a `orchestrator.run()` en el PR siguiente. |
| 2026-06-27 | `change_detection` (item 2c) | `spec/change_detection.md` | `tests/test_change_detection.py` | Capa "temporal": diff entre dos `Snapshot` del mismo target. 8 kinds tipados, score reliability-weighted, ids sha1, audit trail completo. Puro, sin I/O, acotado por `max_changes`. 30 BDD (S1-S15) + 8 properties (1000 ex. c/u, cumple doctrina §6). Refactor boy-scout extrajo `_make_change`, `_union_sources`, `_below_min_reliability` (8 builders → 1 helper). Source F (`untrusted_webscraper`) añadido al mapa 2a para habilitar S7. |
| 2026-06-29 | `csp_safe_styles` (item 2d) | `spec/csp_safe_styles.md` | `tests/test_csp_safe_styles.py` + `tests/properties/test_csp_safe_styles_properties.py` | Cierra el regression de `45c3af5` (CSP `'unsafe-hashes'` rompió la UI por `style="…"` estáticos y dinámicos). 11 inline styles estáticos del template migrados a `hidden` HTML5 / clases CSS (`.stop-btn-sm`, `.meta-row-spaced`, `.empty-entities`, `.graph-top-title`, `.timeline-title`, `.timeline-meta`, `.kbd-actions`). 4 inline styles dinámicos del JS migrados a CSSOM (`el.style.background = cs`, `el.style.color = colorForKind(...)`). CSP intacta (`'unsafe-inline'` jamás vuelve a `style-src`). 22 tests BDD + 3 properties (1000 ex. c/u). Bug colateral encontrado en visual review: `[hidden] { display: none !important }` (las reglas `display: flex` de `.onboarding-overlay` y `.kbd-overlay` pisaban al user-agent default). |
| 2026-06-29 | `fusion_analytics` (item 2e) | `spec/fusion_analytics.md` | `tests/test_fusion_analytics.py` | Capa de inteligencia agregada sobre el fusion_store. Proporciona entity timeline, multi-source consensus, source stats, corroborated properties, entity search con filtros facetados, top changed entities, source corroboration matrix, y entity summary con intel level. 22 tests BDD. Solo lectura sobre SQLite del fusion_store — parameterized queries. Sin regresiones: 197 tests totales verdes (22 nuevos + 175 existentes). |
| 2026-07-08 | `search_telemetry` (item 2f) | `spec/search_telemetry.md` | `tests/test_search_telemetry.py` + `tests/properties/test_search_telemetry_properties.py` | Capa "operator experience": search-in-progress model, onboarding catalog, brand/emoji integrity invariants. 6 property tests (1000 ex. c/u). |
| 2026-07-08 | `recon_fusion` (item 2g) | `spec/recon_fusion.md` | `tests/test_recon_fusion.py` + `tests/properties/test_recon_fusion_properties.py` | Config centralizada sin código duplicado (ReconFusionConfig importada de config.py). 8 property tests (1000 ex. c/u). Boy-scout: eliminado `ReconFusionConfig` duplicado de `recon_fusion.py`, enrutado orquestador a `RECON_FUSION` de config. |
| 2026-07-08 | `ui_professional` (item 2h) | `spec/ui_professional.md` | `tests/test_ui_professional.py` | 26 tests BDD cubriendo loading animations, tiered result display, toggle/expand/collapse con ARIA, CSP security (no inline styles ni onclick), XSS safety. Boy-scout: CSP inline style y onclick violations reparadas en `estorides.js`. |
| 2026-07-08 | `target_management` (item 2i) | `spec/target_management.md` | `tests/test_target_management.py` + `tests/properties/test_target_management_properties.py` | Gestión ligera de targets sin necesidad de full OSINT run. Validación de tipos (16 tipos ontológicos), auto-detección de tipo, batch import (texto/CSV), IDs deterministas sha1, integración opcional con fusion_store + entity_store + case_store. 69 tests BDD + 10 properties (1000 ex. c/u). boy-scout: IPv6 :: shorthand + IPv4 octet range fixing. |
| 2026-07-10 | `source_hierarchy` (item 1, extension) | `spec/reliability_scoring.md` (S11-S15) | `tests/test_reliability_scoring.py` (+ 19 BDD) + `tests/properties/test_reliability_scoring_properties.py` (+ 3 property) | SourceType enum (PRIMARY/SECONDARY/TERTIARY), SOURCE_TYPE_MAP (42 curated sources), SOURCE_TYPE_WEIGHT, source_type_from_name(). Extends ConfidenceInput/Result + compute_confidence/merge_confidence with source_type_weight. |
| 2026-07-10 | `source_health_monitoring` (item 2) | `spec/source_health_monitoring.md` | `tests/test_source_health_monitoring.py` + `tests/properties/test_source_health_monitoring_properties.py` | Source health monitoring module: SourceHealthStatus enum, compute_health() (0.5*success_weight + 0.3*latency_weight + 0.2*freshness_weight), build_dashboard() with tiered stats. 37 BDD + 5 properties. |
| 2026-07-10 | `entity_resolution` (item 3, spec+tests) | `spec/entity_resolution.md` | `tests/test_entity_resolution.py` | Proper spec + 48 BDD pytest tests for existing entity_resolution module. Transliteration, Jaro-Winkler, normalisation, canonical ids, cross-script fusion, domain merging, SAME_AS links, deterministic vs fuzzy, cross-run stability. |
| 2026-07-10 | `probabilistic_fusion` (item 4) | `spec/probabilistic_fusion.md` | `tests/test_probabilistic_fusion.py` | Replaces MAX() in FusionStore.fuse_entity and fuse_relationship with reliability_scoring merge_confidence(). Source-weighted Bayesian merging prevents tertiary sources from inflating well-corroborated entities. 17 BDD tests. |
| 2026-07-10 | `paged_results` (item 5) | `spec/paged_results.md` | `tests/test_pagination.py` | Pagination module (PaginationConfig, build_page_params, extract_cursor, count_results) with three strategies (page, offset, cursor). Integrated into orchestrator._execute_source. Source YAML pagination key in source_loader.py. 31 BDD tests. |
| 2026-07-13 | `security_remediation` (round 1) | `spec/security_remediation.md` | `tests/test_security_remediation.py` | Closed 17 CodeQL findings: CWE-532 (ssrf_guard.py DNS log sanitisation), CWE-79 (estorides.js sanitizeHTML helper + DOM construction in selectNode/showTooltipAt), CWE-209 (10 endpoints in estorides_web.py — no str(e) to client), CWE-601 (web_security.py safe HTTPS redirect via request.host), CWE-266 (ci.yml permissions: read-all). Boy-scout: sanitizeHTML helper, setInnerSafe pattern, DOM API refactor of selectNode. 20 BDD tests, 530 total green. |
| 2026-07-13 | `security_remediation` (round 2) | `spec/security_remediation.md` (updated) | `tests/test_security_remediation.py` (+ updated) | Fixed 10 additional CodeQL findings from fresh scan: CWE-79 (estorides.js sanitizeHTML replaced regex with DOMParser-based approach — closes #37/36/35), CWE-601 (web_security.py - replaces request.host with configured cfg.public_host via ESTORIDES_PUBLIC_HOST env var — closes #27), CWE-209 (transforms.py osiris_sources.py graph_kuzu.py — removed 6 str(e) return dicts that the web layer jsonified — closes #28/29/30/31/32/22). Boy-scout: removed unused noqa BLE001 directives, upgraded log.debug to log.exception in osiris_sources/transforms. 530/530 green. |
| 2026-07-17 | `passive_recon_suite` (10 modules) | `spec/tech_fingerprint.md`, `spec/vuln_correlation.md`, `spec/cloud_asset_discovery.md`, `spec/people_intel.md`, `spec/code_exposure.md`, `spec/supply_chain.md`, `spec/pdns_monitor.md`, `spec/target_scoring.md`, `spec/recon_report.md` | `tests/test_tech_fingerprint.py`, `tests/test_people_intel.py`, `tests/test_code_exposure.py`, `tests/test_cloud_asset_discovery.py`, `tests/test_supply_chain.py`, `tests/test_pdns_monitor.py`, `tests/test_vuln_correlation.py`, `tests/test_target_scoring.py`, `tests/test_recon_report.py` | Complete passive reconnaissance suite for red-team/pentesting phase 1. 10 modules: tech_fingerprint (Nginx/PHP/jQuery/WAF/CMS detection from headers+HTML), vuln_correlation (CVE/exploit/msf/default-creds correlation w/ 10-tech embedded DB), cloud_asset_discovery (bucket permutations for AWS/Azure/GCP/Firebase), people_intel (employee discovery, email pattern inference, cross-breach correlation), code_exposure (GitHub dorking — AWS keys, private keys, internal URLs, .env files, placeholder detection), supply_chain (MX/NS/CDN/registrar provider detection), pdns_monitor (CT log subdomains, IP history, cert SANs, wildcard detection), target_scoring (composite scoring: surface+soft+jewel+lateral, configurable weights), recon_report (executive markdown report w/ TLP classification, redaction, subdomain tree), recon_pipeline (orchestrator). 82 new BDD tests, 703 total green. ruff/mypy/bandit clean. |
 | 2026-07-28 | `tool_runner` + `active_recon` | `spec/tool_runner.md`, `spec/active_recon.md` | `tests/test_tool_runner.py`, `tests/properties/test_tool_runner_properties.py`, `tests/test_active_recon.py` | Safe CLI tool execution engine for Kali OSINT tools (nmap, nikto, sqlmap, dnsrecon, theHarvester, etc.) with zero command injection risk. 10-layer defence: argument-list-only (no shell=True), tool allowlist, metacharacter blocking, path resolution, timeout enforcement, output size cap, audit logging, input validation, no eval/exec, subprocess isolation. 17 BDD tests + 3 property tests (1000 examples each) + 10 active_recon BDD tests. 740 total green. ruff/mypy/bandit clean for new files. |
 | 2026-08-16 | `system_app_sources` | `spec/system_app_sources.md` | `tests/test_system_app_sources.py` + `tests/properties/test_system_app_sources_properties.py` | Kali OSINT CLI tools as first-class sources (`kind: system_app`): nuevo tipo de origen "app de sistema" con esquema YAML propio (`tool.binary` + `tool.args` con placeholders `{query}`/`{outdir}` + `output_format`/`output_file`), ejecutado a través del sandbox `tool_runner` y alimentando el **mismo** pipeline de agregación (observations → entity extraction → fusion → reliability_scoring → recon tiers). 19 YAMLs en `sources/20_system_tools/` (theHarvester, amass enum -passive, dnsrecon, dnsenum, fierce, sublist3r, dmitry, urlcrazy, sherlock, maigret, holehe, usufy, mailfy, phonefy, searchfy, metagoofil, whatweb, wafw00f, phoneinfoga). 19 parsers de salida registrados (factory DRY `_line_filter_parser`, fallback genérico nunca-raise), mapa reliability/type por herramienta (dns tools→PRIMARY, agregadores→SECONDARY, checks de plataforma→TERTIARY), contacto conservador (AXFR/whatweb/wafw00f/metagoofil→active — la garantía passive-only intacta), outdir privado TemporalDirectory auto-limpiado + `cwd` del subprocess, fallos como error-observations (nunca excepciones). S9: ejecución offloaded a worker thread (`asyncio.to_thread`) — un tool lento no congela el event loop del fanout; UI muestra `meta.error_detail` (stderr) en las cards fallidas. 24 BDD (S1-S9) + 6 properties (1000 ex. c/u). 770 tests totales verdes. ruff/mypy/bandit limpios en archivos nuevos; 0 violaciones nuevas en archivos tocados. Visual review headless del badge `sys` en source manager. |
| 2026-08-23 | `observation_models` | `spec/observation_models.md` | `tests/test_observation_models.py` + `tests/properties/test_observation_models_properties.py` | Capa de contrato de datos (gap crítico #1 del roadmap: validación de esquema estricta). Modelos Pydantic v2 (`ObservationMeta`, `Observation`, `ObservedEntity`, `RunResult`) con `strict=True` + `extra="forbid"`, validación recursiva JSON-safe (`set`/`bytes`/objetos arbitrarios/keys no-string rechazados), límites centralizados en `SchemaConfig` de `config.py` (env-tunable, nada hardcodeado). **Primer módulo del proyecto cerrado con mutación**: `mutmut` 79/79 mutantes muertos, 0 supervivientes. 24 BDD + 4 properties (4000 ex. fuzzing). Boy-scout: 8 mutantes supervivientes iniciales revelaron que la garantía JSON-safe del spec no estaba testeada → +9 tests de seguridad. `pydantic>=2.0,<3.0` añadido a deps. Sin wire-up (el PR siguiente conecta `orchestrator`/`fusion_store`/`case_store` con tests de regression). 770→798 verdes. |
| 2026-08-23 | `tool_install` (one-click) | `spec/tool_install.md` | `tests/test_tool_install.py` | Instalación de tools Kali/OSINT desde la sección **Results**: cuando una card falla con `TOOL_NOT_FOUND` muestra un botón "Install tool" → `POST /api/tools/<name>/install` → background thread → recetas estilo lazyaddon en `tool_recipes/*.yaml` (54 recetas: apt primario + git/pip fallback para sherlock/maigret/holehe/phoneinfoga/sublist3r/theHarvester/usufy/mailfy/phonefy/searchfy). **Elevación gráfica con `run0`** (polkit), `sudo` solo fallback, nunca si root. Todo subprocess es argument-list (shell=False, shlex-split del install_command) — cero inyección. Doctrina nueva: todo input hostil + elevación `run0`. 14 BDD. 798→812 verdes. |
| 2026-08-23 | `llm_local_fix` (análisis async) | — | — | `[Stub LLM — no backends available]` desaparece con modelos locales: `LLM_REQUEST_TIMEOUT` default 120s→**600s** (10 min, los qwen3.8:27b tardan minutos en un análisis completo, y corre offloaded/async), auto-detección de modelo prefiere el local rápido (`deepseek-r1:1.5b`) en vez de `available[0]` (qwen 27b lento que estallaba el timeout), reintento con doble `num_predict` si un modelo de razonamiento gasta su presupuesto de tokens en el preamble y devuelve vacío. `ESTORIDES_OLLAMA_MODEL` para forzar modelo. |
| 2026-08-23 | `security_remediation` (round 3) | `spec/security_remediation.md` (updated) | `tests/test_security_remediation.py` (+ TestAlerterSsrf) | Cerró CodeQL round 3: **#40** CRITICAL SSRF en `alerter._http_post` — toda URL de webhook (incl. `channel` con `http*`) pasa por `ssrf_guard.check_url` antes de `urlopen` (bloquea loopback/metadata/esquema no-http). **#38** HIGH DOM-reinterpreted-as-HTML en `estorides.js` — popup del mapa ahora escapa `label/type/value/sources/expandKey.type`, y `safeColor()` sanitiza colores remotos (`CLUSTER_PALETTE`, `cluster_color`) a hex/rgb CSS-safe. **#27** MEDIUM open redirect en `web_security._redirect_to_https` — nuevo `build_https_url()` construye/valida el target (solo GET/HEAD, esquema https + host = `public_host`, path percent-encoded, fallback a raíz). **#45/#44/#43/#42/#41** HIGH "incomplete URL substring sanitization" en tests — asserts de dominio ahora boundary-anchored (regex `(?<![\w.-])…\.com(?![\w-])`, `startswith("example.com.")`). Doctrina endurecida: **todo input es hostil** (URLs→ssrf_guard, strings→escape/safeColor, rutas→boundaries). 812→816 verdes. |
