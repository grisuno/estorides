# `reliability_scoring` — Spec (Módulo 2a)

> Fuente única de verdad para el cálculo de `confidence` de una entidad
> observada por Estorides. Reemplaza el heurístico `min(1.0, c + 0.1)` que
> hoy vive en `entity_extraction.merge()` y el `MAX(existing, incoming)` de
> `fusion_store.fuse_entity()`. Tras este módulo, ambos call sites consumen
> `compute_confidence()` y `merge_confidence()`; el resto del motor
> (hypothesis engine, change detection, cross-case correlation, LLM analyst)
> usa el score que produce este módulo como input, no como heurística local.

---

## Purpose

Hoy el motor tiene **dos heurísticas incompatibles** de confidence:
- `entity_extraction.merge()`: `min(1.0, c + 0.1)` por cada duplicado
  (`estorides_core/entity_extraction.py:393`).
- `fusion_store.fuse_entity()`: `MAX(existing, incoming)` en SQL
  (`estorides_core/fusion_store.py:354`).

Ninguna de las dos incorpora **reliability de la fuente** (crt.sh ≠ paste de
pastebin), **credibilidad de la información** (confirmado por dos brokers vs.
auto-reportado por el actor), **corroboración independiente** (N fuentes
distintas) ni **frescura** (un CVE de 2012 no es igual de útil que uno de
hoy). El LLM analyst, el hypothesis engine y el change detection no pueden
trabajar con un score que no representa nada.

Este módulo implementa el modelo **NATO Admiralty System** (source
reliability A-F × information credibility 1-6) extendido con tres factores
operacionales: **source type hierarchy** (primary/secondary/tertiary con peso
diferenciado), **corroboración** (log del número de fuentes independientes)
y **frescura** (decaimiento exponencial). Es una sola función pura más sus
tablas curadas de `source_name → reliability` y `source_name → source_type`.
El resto del motor llama a `compute_confidence()` o `merge_confidence()` y no
redefine heurísticas.

La jerarquía de tipos de fuente es ortogonal al NATO Admiralty score: una
fuente primaria (registro oficial WHOIS) y una secundaria (red social) pueden
tener ambas reliability A, pero la primaria contribuye más al confidence final
porque está más cerca de la verdad institucional. Los pesos son:
- **PRIMARY** (1.00): registros oficiales, bases de datos autoritativas
- **SECONDARY** (0.85): plataformas de inteligencia curadas
- **TERTIARY** (0.60): contenido generado por usuarios, scrapers, foros

## Inputs

### `ConfidenceInput`

| Campo | Tipo | Rango | Default | Notas |
| --- | --- | --- | --- | --- |
| `source_reliability` | `SourceReliability` (enum str) | uno de `A,B,C,D,E,F` | obligatorio | Curado por fuente en `SOURCE_RELIABILITY_MAP`; fallback `C`. |
| `credibility` | `Credibility` (enum int) | uno de `1..6` | `6` (cannot be judged) | El extractor raramente tiene datos para mejorarlo. |
| `source_type` | `SourceType` (enum str) | `primary`, `secondary`, `tertiary` | `TERTIARY` | Jerarquía: primary (1.0) > secondary (0.85) > tertiary (0.6). |
| `corroboration_count` | `int` | `>= 0` | `0` | Fuentes independientes que vieron el mismo `(type, value)`. |
| `observation_age_seconds` | `float` | `>= 0.0` | `0.0` | Edad del evento origen; `0` = "ahora mismo". |
| `base_confidence` | `float` | `[0.0, 1.0]` | `1.0` | Score crudo del extractor; el módulo lo pondera, no lo inventa. |

Validación en `__post_init__`: `ValueError` si
`corroboration_count < 0`, `observation_age_seconds < 0`,
`base_confidence` fuera de `[0, 1]`, o `source_reliability`/`credibility`
`source_type` no son miembros del enum.

### `merge_confidence(existing, new_observation, …)`

| Parámetro | Tipo | Rango | Notas |
| --- | --- | --- | --- |
| `existing` | `float` | `[0, 1]` | Score ya fusionado de la entidad. |
| `new_observation` | `float` | `[0, 1]` | Score crudo del extractor para la nueva observación. |
| `new_reliability` | `SourceReliability` | enum | Reliability de la fuente que acaba de llegar. |
| `new_credibility` | `Credibility` | enum | Credibility asignada por el caller. |
| `new_source_type` | `SourceType` | enum | Jerarquía de la fuente para esta observación. |
| `corroboration_count` | `int` | `>= 1` | Total de fuentes independientes tras la nueva observación. |
| `observation_age_seconds` | `float` | `>= 0` | Edad de la nueva observación. |

### `reliability_from_name(source_name)`

| Parámetro | Tipo | Rango | Notas |
| --- | --- | --- | --- |
| `source_name` | `str` | cualquier `str` | Nombre del source en `fusion_sources`. **No se valida, no se lanza, no se loguea el contenido**: input hostil. |

### `source_type_from_name(source_name)`

| Parámetro | Tipo | Rango | Notas |
| --- | --- | --- | --- |
| `source_name` | `str` | cualquier `str` | Nombre del source en `fusion_sources`. **No se valida, no se lanza, no se loguea el contenido**: input hostil. |

Devuelve `SourceType.TERTIARY` para fuentes desconocidas (fail-soft).

## Outputs

### `ConfidenceResult` (dataclass frozen, JSON-serializable)

```json
{
  "score": 0.78,
  "reliability_weight": 0.85,
  "credibility_weight": 0.85,
  "source_type_weight": 0.85,
  "corroboration_weight": 0.70,
  "freshness_weight": 0.50,
  "source_reliability": "B",
  "credibility": 2,
  "source_type": "secondary",
  "observation_age_seconds": 2592000.0,
  "corroboration_count": 5
}
```

| Campo | Tipo | Rango | Significado |
| --- | --- | --- | --- |
| `score` | `float` | `[0, 1]` | Resultado final. |
| `reliability_weight` | `float` | `{1.00, 0.85, 0.70, 0.50, 0.30, 0.10}` | Peso del reliability de la fuente. |
| `credibility_weight` | `float` | `{1.00, 0.85, 0.60, 0.30, 0.10, 0.50}` | Peso de la credibility. |
| `source_type_weight` | `float` | `{1.00, 0.85, 0.60}` | Peso por jerarquía de tipo de fuente. |
| `corroboration_weight` | `float` | `[0, 1]` | `min(1, log10(1 + n))`. 0 fuentes = 0; 1 fuente = 0.30; 9 fuentes = 1.0. |
| `freshness_weight` | `float` | `(0, 1]` | `exp(-ln(2) * age_days / half_life_days)`. |
| `source_reliability` | `SourceReliability` | enum | Copia del input. |
| `credibility` | `Credibility` | enum | Copia del input. |
| `source_type` | `SourceType` | enum | Copia del input. |
| `observation_age_seconds` | `float` | `>= 0` | Copia del input. |
| `corroboration_count` | `int` | `>= 0` | Copia del input. |

`compute_confidence()` siempre devuelve un `ConfidenceResult` con `score` en
`[0, 1]`. `merge_confidence()` devuelve un `ConfidenceResult` cuyo `score`
es `max(existing, new_score)`, **acotado a 1.0**.

## Tabla de errores

| Modo de fallo | Código | Comportamiento |
| --- | --- | --- |
| `ConfidenceInput` con `corroboration_count < 0` | `ValueError("corroboration_count must be >= 0")` | Construye, no llama a `compute_confidence`. |
| `ConfidenceInput` con `observation_age_seconds < 0` | `ValueError("observation_age_seconds must be >= 0")` | Construye, no llama. |
| `ConfidenceInput` con `base_confidence` fuera de `[0, 1]` | `ValueError("base_confidence must be in [0, 1]")` | Construye, no llama. |
| `merge_confidence` con `existing` o `new_observation` fuera de `[0, 1]` | `ValueError` con el campo concreto | Igual. |
| `reliability_from_name` con `source_name = ""` o `None` | No lanza | Devuelve `DEFAULT_RELIABILITY`. |
| `reliability_from_name` con bytes / control chars / 10kB | No lanza | Devuelve `DEFAULT_RELIABILITY`. No se loguea el contenido. |
| `source_type_from_name` con `source_name = ""` o `None` | No lanza | Devuelve `DEFAULT_SOURCE_TYPE` (TERTIARY). |
| `source_type_from_name` con input hostil | No lanza | Devuelve `DEFAULT_SOURCE_TYPE`. No se loguea el contenido. |
| `compute_confidence` con `half_life_days <= 0` | `ValueError("half_life_days must be > 0")` | No calcula. |

## Garantías de seguridad

1. **Pureza.** `compute_confidence` y `merge_confidence` son funciones puras.
   No leen disco, no hacen red, no escriben logs, no tocan el reloj, no
   mutan input. Mismo input → mismo output bit a bit.
2. **Sin información hostil.** `reliability_from_name` no loguea, no
   normaliza con regex potencialmente ReDoS, no concatena. La tabla
   `SOURCE_RELIABILITY_MAP` se busca por `dict.get()` sobre la key
   `lower().strip()`. La key no se loguea aunque la búsqueda falle.
3. **Bounded.** No hay loops, no hay recursión. La complejidad es O(1) en
   input. Mide < 5 µs por llamada en CPython 3.11.
4. **Audit trail.** El output expone **todos** los pesos. Un analista puede
   explicar por qué una entidad tiene `score=0.13` (porque freshness=0.04
   con corroboration=0.2, no por un bug del motor).
5. **Fail-loud en input, fail-soft en lookup.** Validación de `ConfidenceInput`
   lanza `ValueError` (input del programador). `reliability_from_name` nunca
   lanza (input del operador OSINT, posiblemente adversario).
6. **Determinismo.** `sorted(set(sources))` en la lista de corroboración es
   del caller, no del módulo. El módulo no itera listas.

## Out of scope

- **Wire-up a `entity_extraction.merge()` / `fusion_store.fuse_entity()`**.
  Eso es el PR siguiente al cierre de este módulo. Este spec no rompe
  compatibilidad (los call sites siguen pasando `1.0` hasta que se wire-e).
- **Persistencia de la tabla `SOURCE_RELIABILITY_MAP` a BD.** Es una constante
  del módulo; la sobreescritura por env var es la única override soportada
  (ver `OUT` abajo).
- **Scoring Bayesiano / Beta-binomial.** El modelo es multiplicativo, no
  bayesiano. Una versión 2.0 podría usar posterior beta; ahora no.
- **Per-source calibration empírica.** La tabla es curada, no aprendida.
- **Auto-tuning de `half_life_days` por tipo de entidad.** Es global
  (`DEFAULT_HALF_LIFE_DAYS`); override por env var.
- **Multilang / transliteración de source names.** Se hace `lower().strip()`,
  nada más.
- **Auto-detección de source type desde la fuente YAML.** La tabla
  `SOURCE_TYPE_MAP` es curada; la metadata del YAML no se parsea aquí.
- **Persistencia de `SOURCE_TYPE_MAP` a BD.** Es constante del módulo.

---

## Escenarios BDD (Given-When-Then)

> Contratos. Cambian solo con acuerdo explícito. Cada uno se traduce a un
> test ejecutable en `tests/test_reliability_scoring.py`.

### S1 · Happy path: fuente A, corroborada, fresca (ATDD)

**Given** un `ConfidenceInput` con
`source_reliability=A`, `credibility=2` (probably true),
`corroboration_count=5`, `observation_age_seconds=0`,
`base_confidence=1.0`  
**When** llamo a `compute_confidence(inp)`  
**Then** `result.score` está en `[0.60, 1.0]` (banda alta; el modelo
multiplicativo con `cred=0.85` y `cor=log10(6)≈0.78` produce ~0.66)  
**And** `result.reliability_weight == 1.00`  
**And** `result.credibility_weight == 0.85`  
**And** `result.freshness_weight == 1.0`  
**And** `result.corroboration_weight == 0.78` (log10(6)).

### S2 · Edge: fuente desconocida cae al default

**Given** un `source_name="totally_unknown_xyz_123"` que no está en
`SOURCE_RELIABILITY_MAP`  
**When** llamo a `reliability_from_name(source_name)`  
**Then** devuelve `SourceReliability.C`  
**And** `compute_confidence` con esa reliability produce un score **moderado**,
no inflado ni en cero (entre 0.20 y 0.60 para corroboration=1, age=0).

### S3 · Edge: cero corroboración, fuente A, fresh — score queda en cero

**Given** un `ConfidenceInput` con `source_reliability=A`,
`corroboration_count=0`, `observation_age_seconds=0`,
`base_confidence=1.0`  
**When** llamo a `compute_confidence(inp)`  
**Then** `result.score == 0.0`  
**And** `result.corroboration_weight == 0.0`.

> El modelo no cree en una sola fuente, ni siquiera si es A. Esto es
> deliberado y opuesto a la heurística `+0.1` del módulo viejo. Una
> entidad vista **solo** por una fuente tiene score 0; el LLM analyst
> lo marcará como "unconfirmed".

### S4 · Edge: observación muy vieja (1 año, sin corroboración)

**Given** un `ConfidenceInput` con `source_reliability=A`,
`corroboration_count=1`, `observation_age_seconds=31_536_000` (365 días)  
**When** llamo a `compute_confidence(inp, half_life_days=30.0)`  
**Then** `result.freshness_weight < 0.001` (exp(-ln(2)*12) ≈ 0.0002)  
**And** `result.score < 0.01`.

### S5 · Error: input inválido del programador

**Given** que intento construir `ConfidenceInput` con
`corroboration_count=-1`  
**When** se ejecuta el constructor  
**Then** lanza `ValueError("corroboration_count must be >= 0")`.  
**And** lo mismo para `observation_age_seconds=-1`,
`base_confidence=1.5`, `base_confidence=-0.1`.

### S6 · Seguridad: nombre de fuente hostil

**Given** que llamo a `reliability_from_name` con cada uno de:
`""`, `None` (str vacía tratada como ""), `"   "`, una cadena de 10 000
caracteres, control chars (`"\x00evil"`), NUL bytes, una palabra reservada
(`"__import__"`), una cadena que parece SQL injection
(`"' OR 1=1 --"`)  
**When** se procesa  
**Then** **ninguna** llamada lanza excepción  
**And** todas devuelven `SourceReliability.C` (o el valor real si
coincide por casualidad — los tests verifican el contrato: ningún input
hostil rompe el módulo ni abre un canal de logging).

### S7 · Merge: una fuente A supera a una C

**Given** `existing=0.18` (de una fuente C, una sola corroboración,
fresh: `1*0.7*0.85*log10(2)*1*1 ≈ 0.179`)  
**And** un nuevo evento con `new_observation=1.0`,
`new_reliability=A`, `new_credibility=2`, `corroboration_count=2`,
`observation_age_seconds=0`  
**When** llamo a `merge_confidence(existing, …)`  
**Then** `result.score > existing` (~0.41)  
**And** `result.score <= 1.0`  
**And** `result.source_reliability == A` (la nueva domina porque es
más fiable).

### S8 · Merge: una fuente F no puede subir el score

**Given** `existing=0.9` (de una fuente A, corroborada)  
**And** un nuevo evento con `new_observation=1.0`,
`new_reliability=F`, `new_credibility=6`, `corroboration_count=1`,
`observation_age_seconds=0`  
**When** llamo a `merge_confidence(existing, …)`  
**Then** `result.score == existing` (la nueva no aporta).

### S9 · Determinismo

**Given** el mismo `ConfidenceInput` y la misma `half_life_days`  
**When** llamo a `compute_confidence` dos veces seguidas  
**Then** los dos `ConfidenceResult` son bitwise idénticos
(`==` por dataclass frozen, y `repr()` idéntico).

### S10 · Bounded / property-based (hypothesis)

**Given** cualquier `ConfidenceInput` con campos válidos en sus rangos  
**When** llamo a `compute_confidence`  
**Then** `0.0 <= result.score <= 1.0` (acotado)  
**And** `0.0 <= result.freshness_weight <= 1.0`  
**And** `0.0 <= result.corroboration_weight <= 1.0`  
**And** `result.reliability_weight in {1.00, 0.85, 0.70, 0.50, 0.30, 0.10}`  
**And** `result.credibility_weight in {1.00, 0.85, 0.60, 0.30, 0.10, 0.50}`.

(Implementado en `tests/properties/test_reliability_scoring_properties.py`
con `hypothesis.given` sobre estrategias acotadas.)

### S11 · Source hierarchy: PRIMARY beats SECONDARY beats TERTIARY

**Given** tres `ConfidenceInput` con el mismo `source_reliability=A`,
`credibility=2`, `corroboration_count=5`, `observation_age_seconds=0`,
`base_confidence=1.0`  
**And** el primero con `source_type=PRIMARY`, el segundo con
`source_type=SECONDARY`, el tercero con `source_type=TERTIARY`  
**When** llamo a `compute_confidence` en cada uno  
**Then** `score_primary > score_secondary > score_tertiary`  
**And** `result.source_type_weight == {1.0, 0.85, 0.6}` respectivamente.

### S12 · Source hierarchy: primary source compensates lower reliability

**Given** un `ConfidenceInput` con `source_reliability=C`,
`source_type=PRIMARY`, `credibility=2`, `corroboration_count=3`,
`observation_age_seconds=0`, `base_confidence=1.0`  
**And** otro con `source_reliability=A`, `source_type=TERTIARY`,
mismos demás parámetros  
**When** llamo a `compute_confidence` en ambos  
**Then** el score del source_type PRIMARY con reliability C puede ser
**mayor o igual** al del TERTIARY con reliability A (0.7*1.0 vs 1.0*0.6,
corroboration igual: ~0.47 vs ~0.40).

### S13 · `source_type_from_name` lookup

**Given** `source_name="rdap_domain"` que está en `SOURCE_TYPE_MAP` como PRIMARY  
**When** llamo a `source_type_from_name(source_name)`  
**Then** devuelve `SourceType.PRIMARY`.

**Given** `source_name="leakcheck_public"` que está en `SOURCE_TYPE_MAP` como TERTIARY  
**When** llamo a `source_type_from_name(source_name)`  
**Then** devuelve `SourceType.TERTIARY`.

**Given** `source_name="unknown_source_xyz"` que no está en `SOURCE_TYPE_MAP`  
**When** llamo a `source_type_from_name(source_name)`  
**Then** devuelve `DEFAULT_SOURCE_TYPE` (TERTIARY).

### S14 · Source hierarchy in merge: new PRIMARY beats existing TERTIARY

**Given** `existing=0.18` (de una fuente TERTIARY C, una corroboración,
fresh)  
**And** un nuevo evento con `new_source_type=PRIMARY`,
`new_reliability=A`, `new_credibility=2`, `corroboration_count=2`,
`observation_age_seconds=0`  
**When** llamo a `merge_confidence(existing, …)`  
**Then** `result.score > existing`  
**And** `result.source_type_weight == 1.0` (la nueva domina).

### S15 · Source hierarchy property-based invariant

**Given** cualquier `ConfidenceInput` con campos válidos en sus rangos  
**When** llamo a `compute_confidence`  
**Then** `result.source_type_weight in {1.00, 0.85, 0.60}`  
**And** si `source_type=PRIMARY` entonces `source_type_weight=1.00`  
**And** si `source_type=TERTIARY` entonces `source_type_weight=0.60`.

---



## Cierre del módulo

- **Fecha de cierre:** 2026-06-27.
- **Estado:** ✅ cerrado (todos los escenarios S1–S10 verdes).
- **Validación:**
  - `pytest tests/test_reliability_scoring.py` → 45 passed
  - `pytest tests/properties/test_reliability_scoring_properties.py` → 9 passed (~9 000 ejemplos aleatorios)
  - `ruff check` → All checks passed
  - `mypy --strict` → no issues
  - `bandit -r` → no issues (0 High, 0 Medium)
- **Performance medida (CPython 3.13, 100 k calls):**
  - `compute_confidence`: **1.95 µs**/llamada (objetivo < 5 µs ✓)
  - `reliability_from_name`: **0.14 µs**/llamada
  - Hostile 10 kB: 5.29 µs/llamada (caso patológico, no es el caso típico)
- **Cambios al motor que este módulo habilita:**
  2b (hypothesis engine) usa `ConfidenceResult.score` como peso de evidencia.
  2c (change detection) usa `reliability_from_name` para ponderar deltas.
  2d (pattern-of-life) usa `merge_confidence` en su ventana deslizante.
- **Call sites que aún no migran** (TODO documentado, no en este PR):
  `entity_extraction.merge()` sigue con `+0.1`,
  `fusion_store.fuse_entity()` sigue con `MAX()`. Migrar en el PR siguiente
  con tests de regression.
- **Lista de cambios:**
  - Creado: `estorides_core/reliability_scoring.py` (245 LoC → 320+ LoC).
  - Creado: `tests/test_reliability_scoring.py` (45 tests → 65+ tests).
  - Creado: `tests/properties/test_reliability_scoring_properties.py` (9 properties → 11 properties).
  - Creado: `tests/conftest.py` (path bootstrap).
  - Creado: `pytest.ini`.
  - Actualizado: `pyproject.toml` (`[dev]` con `ruff`, `mypy`, `bandit`,
    `hypothesis`; `[tool.ruff.lint.per-file-ignores]` para S101 en tests).
  - Creado: `CLAUDE.md` con doctrina inviolable (SDD + TDD + BDD + boy-scout).
  - Actualizado: `docs/index.html` (home page con atajos al spec/test).
  - **2026-07-09:** Añadida jerarquía de tipos de fuente (SourceType enum,
    SOURCE_TYPE_MAP, SOURCE_TYPE_WEIGHT, source_type_from_name). Nuevos
    escenarios BDD S11-S15. Añadido `source_type` a `ConfidenceInput`,
    `source_type_weight` a `ConfidenceResult`.
