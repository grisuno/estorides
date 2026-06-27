# `hypothesis_engine` — Spec (Módulo 2b)

> El módulo que convierte **datos** (observaciones, entidades, edges del
> grafo) en **información accionable** (hipótesis tipadas con score,
> evidencia supporting/contradicting y razonamiento auditable). Es la
> capa que el LLM analyst cita ("hipótesis H3: este dominio es operado
> por EvilCorp, score 0.78, basada en WHOIS + ASN + cert issuer
> coincidentes") y la que el hypothesis dashboard renderiza.

---

## Purpose

Hoy el motor cierra el ciclo de un run con:
- `observations` (lista cruda, una por source)
- `entities` (lista deduplicada, con `confidence` heredada de `+0.1` o `MAX()`)
- `graph` (NetworkX con edges inferidos)
- `analysis` (LLM prompt con todo el contexto, response free-form)

El LLM analyst recibe el muro y tiene que **razonar** por su cuenta. El
resultado es: BLUF inconsistente entre runs, scores arbitrarios, e
imposible auditar "¿por qué el LLM dijo H3?". Este módulo reemplaza el
razonamiento implícito por un motor de hipótesis **declarativo**:
el motor produce 5–10 hipótesis tipadas, cada una con claim, score, y
una lista explícita de evidence items. El LLM analyst solo tiene que
redactar (formato); el motor hace el trabajo analítico.

El módulo es la primera pieza del **layer de información** del pipeline
"data → information → intelligence → counter-intelligence" descrito en
`knowledge_graph.INTEL_LEVELS`. Consume los items del nivel `data`
(observations + entities + graph) y emite items del nivel `intelligence`
(hipótesis con score). El counter-intelligence (sources adversariales
confirmadas) queda fuera de scope; lo maneja el módulo 2e (anomaly
scoring).

## Inputs

### `generate_hypotheses(observations, entities, kg, …)`

| Parámetro | Tipo | Default | Notas |
| --- | --- | --- | --- |
| `observations` | `Sequence[Mapping[str, Any]]` | obligatorio | Lista de dicts produced por `orchestrator.run()`. Cada uno tiene al menos `source` y `parsed`. |
| `entities` | `Sequence[Entity]` | obligatorio | Lista de entidades deduplicadas del run. Cada `Entity` tiene `type`, `value`, `sources`, `confidence`. |
| `kg` | `Any` (protocol-like) | `None` | El knowledge graph (NetworkX). Es opcional; los generadores que lo necesitan reciben `None` y saltan. |
| `min_score` | `float` en `[0, 1]` | `0.10` | Filtro de salida: hipótesis con score final bajo este umbral no se incluyen. |
| `max_hypotheses` | `int` | `50` | Tope duro. Devuelve las N de mayor score. |

### Formato esperado de `observations`

Cada observation es un dict con la shape que produce el orchestrator
(ver `orchestrator.py:359`):

```json
{
  "source": "crt_sh_certificates",
  "category": "01. DNS Intelligence",
  "parser": "crtsh_json",
  "parsed": { "...": "..." },
  "raw": { "...": "..." },
  "meta": { "...": "..." }
}
```

El motor **no falla** si la shape es distinta: cada generador mira las
keys que necesita (`parsed.get(...)`) y omite la observación si no las
encuentra. Esto es por el contrato fail-soft del orchestrator.

## Outputs

### `Hypothesis` (dataclass frozen, JSON-serializable)

```json
{
  "id": "sha1:abc123...",
  "type": "domain-belongsto-actor",
  "claim": "example.com is likely operated by EvilCorp",
  "score": 0.78,
  "confidence": 0.62,
  "supporting": [
    {"source": "hackertarget_whois", "field": "registrant_organization",
     "value": "EvilCorp", "weight": 0.85}
  ],
  "contradicting": [],
  "entities": [
    {"type": "domain", "value": "example.com"},
    {"type": "org", "value": "EvilCorp"}
  ],
  "reasoning": "WHOIS registrant matches known org entity; same cert issuer; ASN aligns.",
  "sources": ["hackertarget_whois", "crt_sh_certificates", "ipapi_co_full"]
}
```

| Campo | Tipo | Rango | Significado |
| --- | --- | --- | --- |
| `id` | `str` | sha1 hex | Determinístico: `sha1(type + sorted(entities) + sorted(supporting sources))[:16]`. Misma hipótesis en runs distintos ⇒ mismo id. |
| `type` | `str` | uno de los `HYPOTHESIS_TYPES` | Tipada. Estable. |
| `claim` | `str` | utf-8, ≤ 280 chars | Frase humana. |
| `score` | `float` | `[0, 1]` | Soporte neto: `f(supporting) / (f(supporting) + f(contradicting) + ε)`, ponderado por reliability de cada source. |
| `confidence` | `float` | `[0, 1]` | Reliability-weighted confidence de la claim. `compute_confidence` aplicado a `(reliability agregada, corroboration, age=0)`. |
| `supporting` | `list[Evidence]` | — | Evidence items a favor. |
| `contradicting` | `list[Evidence]` | — | Evidence items en contra. |
| `entities` | `list[EntityRef]` | — | Pares `(type, value)` que la claim conecta. |
| `reasoning` | `str` | utf-8, ≤ 500 chars | Cadena humana explicando el cómputo. |
| `sources` | `list[str]` | — | Source names únicos que aportaron cualquier evidence (sorted). |

### `Evidence` (dataclass frozen)

```json
{
  "source": "hackertarget_whois",
  "field": "registrant_organization",
  "value": "EvilCorp",
  "weight": 0.85,
  "reliability": "B"
}
```

| Campo | Tipo | Rango | Significado |
| --- | --- | --- | --- |
| `source` | `str` | — | Nombre del source. |
| `field` | `str` | — | Key del `parsed` que produjo la evidencia. |
| `value` | `Any` | — | Valor extraído. Se serializa a str. |
| `weight` | `float` | `[0, 1]` | Peso del evidence item: `reliability_weight` de la fuente (1.0 para A, 0.10 para F). |
| `reliability` | `SourceReliability` | enum | Copia del enum resuelto por `reliability_from_name`. |

### `EntityRef` (dataclass frozen)

```json
{"type": "domain", "value": "example.com"}
```

## Tabla de errores

| Modo de falla | Comportamiento |
| --- | --- |
| `observations` no es lista | `TypeError` con mensaje claro (programmer error). |
| `entities` no es lista | `TypeError` (programmer error). |
| `min_score` fuera de `[0, 1]` | `ValueError`. |
| `max_hypotheses < 1` | `ValueError`. |
| Observation sin `source` o sin `parsed` | El generador que la recibe la ignora silenciosamente (data error del upstream). |
| Observation con `source` desconocido | `reliability_from_name` devuelve `C`; el generador la incluye con peso 0.70. No falla. |
| `kg` ausente o `None` | Los generadores que lo necesitan se saltan; los demás siguen. |
| Hostile payload (control chars, 1 MB strings) | No falla; los generadores se saltan items malformados. |

## Garantías de seguridad

1. **Trusted side.** Este módulo corre en el orquestador (lado confiable).
   No toca HTTP ni parsea contenido remoto. El input viene del pipeline
   interno ya saneado por `validation.py` y `parsers.py`. La regla "no
   ejecutar contenido hostil" aplica a parsers, no aquí.
2. **Pure.** `generate_hypotheses()` es pura: no escribe DB, no hace I/O,
   no loguea, no toca el reloj. Mismo input → mismo output.
3. **No eval / exec / os.system.** Ningún evidence item se evalúa como
   código; el `value` se serializa a str para el claim/reasoning.
4. **Bounded.** `max_hypotheses` acota la salida. La generación interna
   itera a lo sumo O(N generators × M observations) y cada generador
   emite a lo sumo 1 hipótesis por par único. Memoria acotada por el
   input.
5. **Deterministic ids.** El `Hypothesis.id` es un hash del contenido
   (no `id()` ni timestamp). Re-ejecución con el mismo input produce el
   mismo id; el fusion store puede deduplicar.
6. **Fail-loud en input del programador, fail-soft en data upstream.**
   Validación de tipos y rangos lanza `ValueError`/`TypeError`. Data
   malformada (observation sin `source`, parsed vacío) se ignora sin
   crash.
7. **Audit trail completo.** Cada hypothesis expone su evidence
   completa. Un analista puede reproducir el score a mano.

## Out of scope

- **LLM-redaction del claim.** El `claim` se genera por template, no
  se pasa al LLM. El LLM analyst (otro módulo) los reformula. Si el
  template produce texto con datos sensibles, eso es bug del template,
  no del motor.
- **Persistencia.** Las hipótesis viven en memoria del run. Su
  persistencia en fusion store es el PR siguiente (módulo 2f cross-case
  correlation).
- **Counter-intelligence.** Hipótesis tipo "este domain es C2" se
  generan en 2e (anomaly scoring), no aquí.
- **Multi-run / temporal.** Las hipótesis son del run actual. El diff
  entre runs es el módulo 2c.
- **Sources no YAML.** Solo se ingieren sources del catálogo. Un
  generator que necesite `vt_domain` no generará hipótesis si VT no
  respondió.
- **Hipótesis de más de 3 entidades.** La v1 emite hipótesis binarias
  (A-B) o ternarias (A-B-C). N-arias (>3) son out of scope; agregar
  cuando haya demanda.

---

## Tipos de hipótesis v1 (HYPOTHESIS_TYPES)

> Los tipos son **contratos**. Cambian solo con acuerdo explícito y un
> PR de migration (los IDs antiguos en BD dejan de generarse; los
> nuevos se persiguen en paralelo una release).

| `type` | Generador | Plantilla de claim |
| --- | --- | --- |
| `domain-belongsto-actor` | `DomainBelongsToActor` | `"<domain> is likely operated by <actor>"` |
| `email-aliasto-person` | `EmailAliasesPerson` | `"<email> is a likely alias of <person>"` |
| `ip-shared-infra` | `IPSharedInfra` | `"<ip> is shared infrastructure between <domain_a> and <domain_b>"` |
| `asn-shared-infra` | `ASNSharedInfra` | `"<asn> hosts <n> entities from the same investigation"` |

### `domain-belongsto-actor`

**Trigger.** Una observation (WHOIS, crt.sh, IP-API) produce un
`(registrant_organization | issuer_organization | asn_organization)`
que matchea una entity `(org | person)` ya presente en el run.

**Evidence sources.**
- `hackertarget_whois` → `parsed.registrant_organization` (A: B)
- `rdap_domain` → `parsed.entities[*].roles=registrar` (A: A)
- `crt_sh_certificates` → `parsed.issuer_name` (A: A)
- `ipapi_co_full` → `parsed.org` (B: B)
- `wikidata_search` → `parsed.results[*].label` (B: B)

**Score.** `supporting_score / (supporting_score + contradicting_score + 0.1)`.

### `email-aliasto-person`

**Trigger.** Una observation produce un par `(email, person_name)` con
matching de handle o display name en la misma observation, o un email
matchea el patrón `<handle>@<provider>` donde `<handle>` ya está
registrado como username entity.

**Evidence sources.**
- `github_user` → `parsed.login` + `parsed.name` (B: B)
- `reddit_about` → `parsed.name` + `parsed.subreddit` (B: B)
- `keybase_lookup` → `parsed.profiles.full_name` + `key` (B: B)
- `dehashed_email` → `parsed.results[*].email` + `parsed.results[*].name` (C: C)

**Score.** Mismo: `supporting_score / (supporting + contradicting + 0.1)`.

### `ip-shared-infra`

**Trigger.** Dos o más domains resuelven al mismo IP en el run
(observaciones de DNS-over-HTTPS, hackertarget, etc.).

**Evidence sources.** Cualquier source que produzca
`parsed.answers[].data` (DNS) o `parsed.ip` (reverso). Si dos
observations de DNS distintas dicen "domain A → 1.2.3.4" y "domain B
→ 1.2.3.4", el generador emite la hipótesis.

**Score.** `min(1, log10(1 + n_domains_sharing_ip) / log10(1 + 5))` ×
`reliability_weight` del mejor source.

### `asn-shared-infra`

**Trigger.** Tres o más entities de la investigación tienen ASN conocido
y todos caen en el mismo ASN.

**Evidence sources.**
- `ipapi_co_full` → `parsed.asn` (B: B)
- `hackertarget_aslookup` → `parsed.as` (B: B)
- `abuseipdb_check` → `parsed.isp` + `parsed.usageType` (B: B)

**Score.** `min(1, n_entities_in_asn / 5) × reliability_weight`.

---

## Escenarios BDD (Given-When-Then)

> Contratos. Cambian solo con acuerdo explícito. Cada uno se traduce a
> un test ejecutable en `tests/test_hypothesis_engine.py`.

### S1 · Happy path: 1 domain, 3 sources concuerdan

**Given** `observations` con:
- `hackertarget_whois` → `parsed.registrant_organization = "EvilCorp"`
- `crt_sh_certificates` → `parsed.issuer_name = "EvilCorp CA"`
- `ipapi_co_full` → `parsed.org = "EvilCorp"`  
**And** `entities` con `(type=domain, value=example.com)` y
`(type=org, value=EvilCorp)`  
**When** llamo a `generate_hypotheses(observations, entities)`  
**Then** la lista de salida contiene **al menos** una hipótesis de tipo
`domain-belongsto-actor` con `entities` = `[(domain, example.com), (org,
EvilCorp)]`  
**And** `score >= 0.60`  
**And** `supporting` tiene 3 items (uno por source)  
**And** `sources` = `["crt_sh_certificates", "hackertarget_whois", "ipapi_co_full"]` (sorted).

### S2 · Edge: input vacío

**Given** `observations = []` y `entities = []`  
**When** llamo a `generate_hypotheses(...)`  
**Then** la lista de salida es `[]`  
**And** no lanza.

### S3 · Edge: observación con `parsed = None`

**Given** una observation con `source = "x"`, `parsed = None`  
**When** la paso al motor  
**Then** la observation se ignora, no genera hipótesis, no lanza.

### S4 · Edge: source desconocido cae a reliability C

**Given** una observation con `source = "totally_made_up_source"` y
`parsed.registrant_organization = "EvilCorp"`  
**And** una entity `(org, EvilCorp)`  
**When** genero hipótesis  
**Then** la hipótesis sale con `supporting[0].reliability == C`  
**And** el score se calcula con `reliability_weight = 0.70`.

### S5 · Edge: `min_score` filtra hipótesis débiles

**Given** un generador que produce una hipótesis con `score = 0.05`  
**When** llamo a `generate_hypotheses(..., min_score=0.10)`  
**Then** esa hipótesis no aparece en la salida.

### S6 · Edge: `max_hypotheses` acota la salida

**Given** input que produce 100 hipótesis  
**When** llamo a `generate_hypotheses(..., max_hypotheses=10)`  
**Then** la salida tiene exactamente 10 items, los de mayor score.

### S7 · Error: input del programador inválido

**Given** que llamo a `generate_hypotheses(observations="not a list", ...)`  
**When** se ejecuta  
**Then** lanza `TypeError("observations must be a sequence")`.  
**And** lo mismo para `min_score=1.5`, `max_hypotheses=0`,
`min_score=-0.1`.

### S8 · Seguridad: observation hostil

**Given** una observation con `parsed` que contiene NUL bytes, 100kB de
texto random, control chars, una string que parece pickle,
`__import__("os").system("rm -rf /")`  
**When** la paso al motor  
**Then** no hay crash, no hay RCE (obvio — no se ejecuta nada), y la
observation o se ignora o se incluye con `value` truncado a 200 chars
para el `Evidence.value`.

### S9 · Determinismo: misma entrada, misma hipótesis

**Given** un input fijo (observations + entities)  
**When** llamo a `generate_hypotheses` dos veces  
**Then** las dos listas tienen el mismo `len`, los mismos `id`s, y los
mismos scores. Reordenar las observations en el input no cambia la
salida (el motor ordena internamente antes de hashear).

### S10 · Bounded / property-based (hypothesis)

**Given** cualquier input válido en sus rangos  
**When** llamo a `generate_hypotheses`  
**Then** `0.0 <= score <= 1.0` para toda hipótesis  
**And** `0.0 <= confidence <= 1.0`  
**And** `len(supporting) >= 1` (un generador no emite hipótesis sin al
menos 1 evidence a favor)  
**And** `sources` es siempre `sorted(set(...))` (sin duplicados, ordenado)
**And** `len(claim) <= 280`  
**And** `len(reasoning) <= 500`.

(Implementado en `tests/properties/test_hypothesis_engine_properties.py`
con `hypothesis.given` sobre estrategias acotadas.)

---

## Cierre del módulo

- **Fecha de cierre:** 2026-06-27.
- **Estado:** ✅ cerrado (todos los escenarios S1–S10 verdes).
- **Validación:**
  - `pytest tests/test_hypothesis_engine.py` → 26 passed
  - `pytest tests/properties/test_hypothesis_engine_properties.py` → 9 passed
  - `ruff check` → All checks passed
  - `mypy --strict` → no issues
  - `bandit -r` → no issues (0 High, 0 Medium)
- **Performance medida (CPython 3.13, 1 000 calls, 20 obs / 10 entities):**
  - `generate_hypotheses`: **460 µs**/llamada (≈ 2 170 runs/segundo)
- **Cambios al motor que este módulo habilita:**
  El LLM analyst consume `Hypothesis` objects en lugar de redactar
  análisis libre. El frontend (Cases → Hypotheses tab) renderiza la
  lista con drill-down a evidence.
- **Call sites que aún no migran** (documentado, no en este PR):
  `orchestrator.run()` no invoca `generate_hypotheses` todavía; el
  wire-up es el PR siguiente, junto con la persistencia en
  `fusion_store`.
- **Lista de cambios:**
  - Creado: `estorides_core/hypothesis_engine.py` (700 LoC).
  - Creado: `tests/test_hypothesis_engine.py` (26 tests, BDD Given-When-Then).
  - Creado: `tests/properties/test_hypothesis_engine_properties.py` (9 properties).
