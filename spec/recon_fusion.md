# `recon_fusion` -- Spec (Modulo 2g)

> Capa de fusion de reconocimiento pasivo: agrupa, elimina duplicados y
> clasifica los resultados de 100+ fuentes OSINT segun su relevancia.
> Convierte el "monton de datos crudos" en un cuadro de mandos ordenado
> por fiabilidad, sin perder acceso a ningun resultado.

---

## Purpose

El motor de Estorides lanza 100+ fuentes OSINT en paralelo para cada
consulta. Cada fuente devuelve observaciones estructuradas (parsed),
entidades extraidas, metadatos y estado. El operador recibe todo mezclado:
resultados de crt.sh al lado de pastebins de dudosa procedencia, sin
ningun criterio de prioridad.

Este modulo cierra esa brecha. Toma el array plano de observaciones y
entidades que el orquestador produce y:

1. **Agrupa** por entidad canonica (type + normalized value), fusionando
   todas las fuentes que vieron lo mismo.
2. **Elimina duplicados** dentro de cada grupo, quedandose con la
   observacion de mayor confianza por fuente.
3. **Clasifica** cada grupo en un `RelevanceTier` segun:
   - Fiabilidad de las fuentes (NATO Admiralty, via `reliability_scoring`).
   - Numero de fuentes independientes que corroboran el dato.
   - Frescura del dato (edad en segundos).
   - Relevancia directa: si el valor coincide exactamente con la consulta
     original (match directo) o es un hallazgo indirecto (pivoted).
4. **Ordena** los grupos por relevancia descendente, con los mas utiles
   primero.
5. **Expone** los resultados por tiers para que la UI pueda renderizar
   secciones plegables: CRITICAL primero, HIGH despues, etc.

El modulo es puro (sin I/O), determinista, y no depende del fusion_store
(aunque usa sus mismos principios de normalizacion). Es una funcion de
transformacion: `List[Observation] + List[Entity] + Query -> FusionResult`.

## Inputs

### Constructor

`ReconFusionEngine(config: ReconFusionConfig)` -- recibe una configuracion
congelada con los umbrales y pesos. No tiene estado mutable.

### `classify(query: str, query_type: str, observations: list, entities: list) -> FusionResult`

| Parametro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `query` | `str` | 1-512 chars | Consulta original del operador, normalizada. |
| `query_type` | `str` | uno de `ipv4, domain, email, cve, ...` | Tipo detectado de la consulta. |
| `observations` | `list[dict]` | 0-N | Array plano de observaciones del orquestador. Cada una tiene `source`, `category`, `parsed`, `meta`, `status`. |
| `entities` | `list[dict]` | 0-N | Array plano de entidades extraidas. Cada una tiene `type`, `value`, `confidence`, `sources`. |

### `ReconFusionConfig`

| Campo | Tipo | Default | Env var | Notas |
|-------|------|---------|---------|-------|
| `critical_min_sources` | `int` | `3` | `ESTORIDES_RF_CRITICAL_SRC` | Minimo fuentes independientes para CRITICAL. |
| `high_min_sources` | `int` | `2` | `ESTORIDES_RF_HIGH_SRC` | Minimo fuentes independientes para HIGH. |
| `high_min_reliability` | `str` | `"B"` | `ESTORIDES_RF_HIGH_REL` | Reliability minima (letra) para HIGH sin corroboracion. |
| `medium_min_reliability` | `str` | `"D"` | `ESTORIDES_RF_MEDIUM_REL` | Reliability minima (letra) para MEDIUM. |
| `noise_max_reliability` | `str` | `"F"` | `ESTORIDES_RF_NOISE_REL` | Reliability maxima para considerar NOISE. |
| `freshness_max_hours` | `float` | `72.0` | `ESTORIDES_RF_FRESH_H` | Edad maxima en horas para bonus de frescura. |
| `direct_match_boost` | `float` | `0.15` | `ESTORIDES_RF_DIRECT_BOOST` | Boost adicional si la entidad coincide con la query. |
| `exact_dedup_keys` | `tuple[str, ...]` | ver abajo | `ESTORIDES_RF_DEDUP_KEYS` | Claves del parsed que definen "mismo resultado". |
| `source_reliability_overrides` | `dict[str, str]` | `{}` | -- | Override de reliability para fuentes especificas. |

`exact_dedup_keys` default: `("source", "parser", "status")`.

## Outputs

### `FusionResult` (dataclass frozen)

```json
{
  "query": "evilcorp.com",
  "query_type": "domain",
  "total_observations": 85,
  "total_entities": 42,
  "tiers": {
    "critical": [
      {
        "canonical_id": "domain:evilcorp.com",
        "type": "domain",
        "value": "evilcorp.com",
        "relevance_score": 0.93,
        "tier": "critical",
        "source_count": 5,
        "sources": ["crt_sh_certificates", "rdap_domain", ...],
        "max_confidence": 0.95,
        "direct_match": true,
        "first_seen": 1700000000.0,
        "last_seen": 1700100000.0,
        "top_observations": [ ... ],
        "key_findings": ["MX: mail.evilcorp.com", "A: 192.0.2.1"]
      }
    ],
    "high": [ ... ],
    "medium": [ ... ],
    "low": [ ... ],
    "noise": [ ... ]
  },
  "tier_summary": {
    "critical": 2,
    "high": 8,
    "medium": 15,
    "low": 12,
    "noise": 5
  },
  "generated_at": 1700100000.0
}
```

### `RelevanceTier` (enum str)

| Miembro | Valor | Significado |
|---------|-------|-------------|
| `CRITICAL` | `"critical"` | Corroborado por 3+ fuentes, o 2+ fuentes de alta fiabilidad. Match directo con la query. |
| `HIGH` | `"high"` | Corroborado por 2+ fuentes, o fuente unica con reliability A/B y match directo. |
| `MEDIUM` | `"medium"` | Fuente unica con reliability C/D, o corroborado por 2+ fuentes de baja fiabilidad. |
| `LOW` | `"low"` | Fuente unica con reliability E/F, o dato sin corroborar y sin match directo. |
| `NOISE` | `"noise"` | Fuente F sin corroboracion, o dato que fallo validacion, o contradicho por fuentes superiores. |

### `GroupedEntity` (dataclass frozen)

| Campo | Tipo | Notas |
|-------|------|-------|
| `canonical_id` | `str` | `sha1(type + ":" + normalized)[:16]`. |
| `type` | `str` | Tipo de entidad. |
| `value` | `str` | Valor original. |
| `normalized` | `str` | Valor normalizado. |
| `relevance_score` | `float` | `[0, 1]`. Score compuesto de relevancia. |
| `tier` | `str` | Uno de los 5 tiers. |
| `source_count` | `int` | Fuentes independientes que corroboran. |
| `sources` | `list[str]` | Nombres de fuentes. |
| `max_confidence` | `float` | Maxima confianza entre observaciones. |
| `direct_match` | `bool` | True si el valor coincide con la query original. |
| `first_seen` | `float` | Timestamp Unix de la primera observacion. |
| `last_seen` | `float` | Timestamp Unix de la ultima observacion. |
| `top_observations` | `list[dict]` | Hasta 3 observaciones mas relevantes. |
| `key_findings` | `list[str]` | Hallazgos textuales resumidos. |

## Tabla de errores

| Modo de fallo | Comportamiento |
|---------------|----------------|
| `observations` `None` | Tratado como `[]`. |
| `entities` `None` | Tratado como `[]`. |
| `query` vacio o `None` | `ValueError("query must be non-empty")`. |
| Observacion sin `source` | Ignorada (no entra en grupos). |
| Entidad sin `type` o `value` | Ignorada. |
| `ReconFusionConfig` con tier thresholds inconsistentes (e.g. critical_min_sources <= high_min_sources) | `ValueError` en `__post_init__`. |
| `source_reliability_overrides` con valor no valido | Ignora el override, usa el valor por defecto. |
| `freshness_max_hours <= 0` | Clampeado a `1.0`. |

## Garantias de seguridad

1. **Sin I/O.** El modulo es una funcion de transformacion pura. No lee
   disco, no hace red, no escribe logs.
2. **Sin inyeccion.** No evalua strings, no usa `eval`/`exec`/`os.system`.
   Las comparaciones son hash-based o directas.
3. **Acotado.** Numero de grupos acotado por numero de entidades unicas.
   `top_observations` limitado a 3 items por grupo.
4. **Input hostil.** Entradas `None`, listas vacias, valores corruptos no
   causan excepciones no controladas. Fallan suavemente.
5. **Sin logging de contenido.** No se loguean los valores de las entidades
   ni las queries.

## Out of scope

- **Escritura a fusion_store.** Eso es responsabilidad de `FusionStore`.
- **Persistencia.** Los resultados son efimeros, por request.
- **Visualizacion.** Este modulo produce datos estructurados; la UI
  (Flask/Jinja/CSS/JS) los renderiza.
- **Re-scoring con LLM.** La clasificacion es basada en reglas, no en LLM.
- **Aprendizaje de pesos.** Los pesos son configurados por el operador via
  env vars, no aprendidos.

---

## Escenarios BDD (Given-When-Then)

> Contratos. Cambian solo con acuerdo explicito.

### S1 -- Happy path: entidad corroborada por 3+ fuentes es CRITICAL

**Given** una query `"evilcorp.com"`  
**And** 5 observaciones de fuentes independientes que contienen la entidad
`domain:evilcorp.com` con reliability A, B, B, C, C  
**When** `engine.classify(query, "domain", observations, entities)`  
**Then** `result.tiers["critical"]` contiene la entidad  
**And** `result.tier_summary["critical"] == 1`  
**And** `direct_match == True`  
**And** `source_count >= 3`.

### S2 -- Happy path: entidad con 2 fuentes es HIGH

**Given** una query `"8.8.8.8"`  
**And** 2 observaciones de fuentes independientes para `ipv4:8.8.8.8`
con reliability B y B  
**When** `engine.classify(query, "ipv4", observations, entities)`  
**Then** `result.tiers["high"]` contiene la entidad  
**And** `result.tier_summary["high"] == 1`.

### S3 -- Edge: fuente unica con reliability alta es MEDIUM

**Given** una entidad observada solo por `crtsh_certificates` (reliability A)  
**And** sin corroboracion de otras fuentes  
**When** `engine.classify(query, "domain", observations, entities)`  
**Then** la entidad aparece en `tiers["medium"]`  
**And** `source_count == 1`  
**And** `max_confidence > 0.5`.

### S4 -- Edge: fuente unica con reliability F es NOISE

**Given** una entidad observada solo por `untrusted_webscraper` (reliability F)  
**And** sin corroboracion  
**When** `engine.classify(query, "domain", observations, entities)`  
**Then** la entidad aparece en `tiers["noise"]`  
**And** `source_count == 1`.

### S5 -- Edge: sin observaciones ni entidades devuelve resultado vacio

**Given** `observations=[]` y `entities=[]`  
**When** `engine.classify(query, "domain", [], [])`  
**Then** `result.total_observations == 0`  
**And** `result.total_entities == 0`  
**And** todos los `tiers.*` estan vacios.

### S6 -- Edge: entidad con match directo tiene boost

**Given** una entidad cuyo valor coincide exactamente con la query  
**And** misma fuente, mismo reliability que otra entidad sin match directo  
**When** `engine.classify(query, "domain", observations, entities)`  
**Then** la entidad con match directo tiene `relevance_score` mayor  
**And** `direct_match == True`.

### S7 -- Error: query vacia lanza ValueError

**Given** una query vacia `""`  
**When** `engine.classify("", "domain", [], [])`  
**Then** lanza `ValueError("query must be non-empty")`.

### S8 -- Error: config con thresholds inconsistentes

**Given** `ReconFusionConfig(critical_min_sources=2, high_min_sources=3)`  
**When** se construye  
**Then** lanza `ValueError` porque `critical_min_sources <= high_min_sources`.

### S9 -- Seguridad: None en observations no lanza

**Given** `observations=None`  
**When** `engine.classify(query, "domain", None, [])`  
**Then** no lanza excepcion  
**And** `total_observations == 0`.

### S10 -- Seguridad: entidad sin type es ignorada

**Given** entidades con `{"value": "test"}` (sin `type`)  
**When** `engine.classify(query, "domain", [], entities)`  
**Then** la entidad no aparece en ningun tier  
**And** no lanza excepcion.

### S11 -- Dedup: misma fuente, mismo parser, mismo status = una sola entrada

**Given** 3 observaciones identicas de la misma fuente con el mismo parser
y status  
**When** `engine.classify(query, "domain", observations, [])`  
**Then** solo 1 observacion aparece en `top_observations` del grupo  
**And** `source_count == 1`.

### S12 -- Orden: tiers ordenados por relevance_score descendente

**Given** multiples entidades en un mismo tier  
**When** se inspeccionan los grupos del tier  
**Then** estan ordenados por `relevance_score` descendente  
**And** `relevance_score` esta en `[0, 1]`.

---

## Cierre del modulo

- **Fecha de cierre:** _(se llena al cerrar)_
- **Estado:** por implementar.
- **Validacion:**
  - `pytest tests/test_recon_fusion.py -v` -- todos verdes
  - `ruff check estorides_core/recon_fusion.py tests/test_recon_fusion.py` -- limpio
  - `mypy --strict estorides_core/recon_fusion.py` -- sin errores
  - `bandit -r estorides_core/recon_fusion.py` -- sin High ni Medium
