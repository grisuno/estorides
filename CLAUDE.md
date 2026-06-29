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
