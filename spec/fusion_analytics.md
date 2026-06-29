# `fusion_analytics` — Spec (Módulo 2e)

> Capa de inteligencia agregada sobre el fusion_store. Proporciona el
> "cuadro de mando" que Palantir ofrece en Athena: multi-source consensus,
> entity timelines, source reliability stats, y corroboration analytics.
> Todo es lectura sobre el SQLite del fusion_store — no hay escritura, no
> hay I/O de red, no hay dependencias nuevas.

---

## Purpose

El `fusion_store` acumula observaciones, entidades, propiedades y
relaciones con proveniencia y timestamps. Pero no hay una capa que
responda preguntas de nivel "inteligencia":

- "¿Qué propiedades de una entidad están corroboradas por N fuentes?"
- "¿Cuál es la línea de tiempo de una entidad? ¿Cuándo la vio cada fuente?"
- "¿Qué fuente es la más fiable? ¿Cuál tiene más agreement con el consenso?"
- "¿Qué entidades cambiaron más en los últimos 7 días?"
- "¿Cuál es el panorama completo de una entidad: propiedades, relaciones,
   fuentes, confianza a lo largo del tiempo?"

Este módulo implementa esas consultas como lecturas SQL parametrizadas
sobre las tablas del fusion_store. No escribe, no muta, no cachea (el
caller puede cachear si quiere). Es un lector puro.

## Inputs

### Constructor

`FusionAnalytics(store: FusionStore)` — recibe una instancia abierta del
`FusionStore`. No abre conexiones propias.

### `entity_timeline(eid: str) -> EntityTimeline`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `eid` | `str` | sha1[:16] hex digest | Entity id en fusion_entities. Si no existe → timeline vacío. |

### `entity_summary(eid: str) -> EntitySummary`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `eid` | `str` | id de entidad | Si no existe → None. |

### `source_stats(source_name: str) -> SourceStats | None`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `source_name` | `str` | nombre de source | Case-insensitive lookup. No lanza. |

### `corroborated_properties(eid: str, min_sources: int = 2) -> list`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `eid` | `str` | id de entidad | — |
| `min_sources` | `int` | >= 1 | Mínimo de fuentes distintas para considerar "corroborado". |

### `multi_source_consensus(eid: str, key: str) -> ConsensusResult`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `eid` | `str` | id de entidad | Entity id |
| `key` | `str` | property key | Ej: "country", "asn", "org". |

### `top_changed(days: int = 7, limit: int = 20) -> list`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `days` | `int` | >= 1 | Ventana temporal hacia atrás. |
| `limit` | `int` | 1..200 | Máximo de entidades a devolver. |

### `entity_search(term: str, etype: str = "", min_confidence: float = 0.0, min_sources: int = 0, limit: int = 50) -> list`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `term` | `str` | cualquier | Búsqueda LIKE sobre value y normalized. |
| `etype` | `str` | opcional | Filtro por tipo de entidad. |
| `min_confidence` | `float` | [0, 1] | Umbral mínimo de confidence. |
| `min_sources` | `int` | >= 0 | Mínimo de fuentes independientes. |
| `limit` | `int` | 1..200 | Máximo de resultados. |

### `source_corroboration_matrix(limit: int = 20) -> list`

| Parámetro | Tipo | Rango | Notas |
|-----------|------|-------|-------|
| `limit` | `int` | 1..200 | Top N fuentes más activas para la matriz. |

## Outputs

### `EntityTimeline`

```json
{
  "entity_id": "abc123def4567890",
  "type": "domain",
  "value": "evilcorp.com",
  "first_seen": 1700000000.0,
  "last_seen": 1700100000.0,
  "observations": [
    {
      "source": "crtsh_certificates",
      "observed_at": 1700000000.0,
      "status": "ok",
      "key_findings": ["subdomain:mail.evilcorp.com"]
    }
  ],
  "properties": [
    {
      "key": "country",
      "value": "RU",
      "sources": ["ipapi_free", "ipwhois"],
      "first_seen": 1700000100.0,
      "last_seen": 1700100000.0
    }
  ],
  "relationships": [
    {
      "relation": "resolves_to",
      "dst_value": "192.0.2.1",
      "dst_type": "ipv4",
      "sources": ["dns_google"],
      "observed_at": 1700000000.0
    }
  ],
  "source_timeline": [
    {"source": "crtsh_certificates", "first_seen": 1700000000.0, "last_seen": 1700100000.0, "seen_count": 3},
    {"source": "dns_google", "first_seen": 1700000000.0, "last_seen": 1700000000.0, "seen_count": 1}
  ]
}
```

### `EntitySummary`

```json
{
  "entity_id": "abc123def4567890",
  "type": "domain",
  "value": "evilcorp.com",
  "normalized": "evilcorp.com",
  "confidence": 0.85,
  "source_count": 4,
  "observation_count": 12,
  "first_seen": 1700000000.0,
  "last_seen": 1700100000.0,
  "properties_summary": {
    "total": 8,
    "corroborated": 3,
    "keys": ["country", "asn", "org", "isp"]
  },
  "relationships_summary": {
    "total": 15,
    "types": ["resolves_to", "registered_with_email", "has_subdomain"],
    "distinct_targets": 12
  },
  "sources": ["crtsh_certificates", "dns_google", "ipapi_free", "ipwhois"],
  "intel_level": "information"
}
```

### `SourceStats`

```json
{
  "source_name": "crtsh_certificates",
  "category": "03. Web Intelligence",
  "first_seen": 1700000000.0,
  "last_seen": 1700100000.0,
  "fetch_count": 150,
  "ok_count": 145,
  "success_rate": 0.967,
  "unique_entities": 320,
  "entity_types": {"domain": 300, "email": 20},
  "unique_properties_contributed": 45,
  "unique_relationships_contributed": 120,
  "avg_observations_per_fetch": 12.4,
  "corroboration_rate": 0.65
}
```

### `ConsensusResult`

```json
{
  "entity_id": "abc123...",
  "property_key": "country",
  "values": [
    {"value": "RU", "sources": ["ipapi_free", "ipwhois"], "count": 2, "weighted_confidence": 0.85},
    {"value": "US", "sources": ["abuseipdb_check"], "count": 1, "weighted_confidence": 0.5}
  ],
  "consensus_value": "RU",
  "consensus_strength": 0.67,
  "total_sources": 3
}
```

### `entity_search` results

Lista de dicts, cada uno:

```json
{
  "id": "abc...",
  "type": "domain",
  "value": "evilcorp.com",
  "confidence": 0.85,
  "source_count": 4,
  "observation_count": 12,
  "last_seen": 1700100000.0,
  "intel_level": "information"
}
```

### `top_changed` results

Lista de dicts, cada uno:

```json
{
  "entity_id": "abc...",
  "type": "domain",
  "value": "evilcorp.com",
  "source_count": 4,
  "last_seen": 1700100000.0,
  "new_observations": 3,
  "new_sources": 1,
  "new_properties": 2,
  "new_relationships": 5
}
```

### `source_corroboration_matrix` results

```json
[
  {"source_a": "crtsh_certificates", "source_b": "dns_google", "shared_entities": 45, "shared_properties": 12},
  {"source_a": "crtsh_certificates", "source_b": "ipapi_free", "shared_entities": 8, "shared_properties": 3}
]
```

## Tabla de errores

| Modo de fallo | Comportamiento |
|---------------|----------------|
| `eid` no existe en fusion_entities | `entity_timeline` / `entity_summary` devuelven `None` |
| `source_name` no existe | `source_stats` devuelve `None` |
| `key` no existe en propiedades de la entidad | `multi_source_consensus` devuelve `ConsensusResult` con `values=[]` |
| `FusionStore` con `None` (store no disponible) | Constructor acepta `None`; todos los métodos devuelven vacío |
| Base de datos bloqueada / I/O error | No lanza; log debug y devuelve vacío |
| `min_sources <= 0` | Tratado como `1` |
| `limit <= 0` | Tratado como `1` |
| `days <= 0` | Tratado como `1` |
| `min_confidence` fuera de `[0, 1]` | Clampeado a `[0, 1]` |
| Input hostil (bytes, 10MB string) | LIKE con `%term%` — SQL injection no es posible porque usamos `?` parameterized queries |

## Garantías de seguridad

1. **Solo lectura.** Ningún método escribe en el fusion_store. No hay `INSERT`, `UPDATE`, `DELETE`.
2. **Parameterized queries.** Todas las queries SQL usan `?` placeholders — nunca interpolación de cadenas.
3. **Fail soft.** Store `None` o DB bloqueada → logs debug + respuesta vacía. Nunca lanza al caller.
4. **Acotado.** Todos los resultados tienen `limit` con capping. Una entidad con 10k propiedades no puede producir una respuesta de 100 MB.
5. **Sin imports nuevos.** Solo stdlib + `FusionStore`.

## Out of scope

- **Escritura al fusion_store.** Eso es responsabilidad de `FusionStore`.
- **Cacheo de resultados.** El caller puede cachear; este módulo siempre lee fresco.
- **Visualización.** Esto devuelve data estructurada; la UI (Flask/Jinja) la renderiza.
- **Alertas / notificaciones.** Eso es el módulo `alert_engine`.
- **Fuzzing con `hypothesis` sobre el store.** Las queries SQL son I/O; el fuzzing de las consultas se hace con fixtures en memoria.

---

## Escenarios BDD (Given-When-Then)

> Contratos. Cambian solo con acuerdo explícito.

### E1 · Happy path: entity_timeline devuelve la línea de tiempo completa

**Given** un fusion_store con una entidad `domain:evilcorp.com` observada por 3 fuentes, con 2 propiedades y 2 relaciones  
**When** llamo a `analytics.entity_timeline(eid)` con el eid de esa entidad  
**Then** el resultado tiene `observations` con 3 entradas  
**And** `properties` con 2 entradas  
**And** `relationships` con 2 entradas  
**And** `source_timeline` con 3 fuentes  
**And** `first_seen <= last_seen`.

### E2 · entity_summary devuelve estadísticas agregadas

**Given** la misma entidad  
**When** llamo a `analytics.entity_summary(eid)`  
**Then** `source_count == 3`  
**And** `properties_summary.total >= 2`  
**And** `relationships_summary.total >= 2`.

### E3 · entity_timeline con eid inexistente devuelve None

**Given** un eid que no existe en `fusion_entities`  
**When** llamo a `analytics.entity_timeline(eid)`  
**Then** devuelve `None`.

### E4 · source_stats devuelve métricas de una fuente

**Given** un fusion_store con la fuente `crtsh_certificates` registrada y activa  
**When** llamo a `analytics.source_stats("crtsh_certificates")`  
**Then** `source_name == "crtsh_certificates"`  
**And** `fetch_count >= 0`  
**And** `success_rate` está en `[0.0, 1.0]`  
**And** `first_seen <= last_seen`.

### E5 · source_stats con fuente inexistente devuelve None

**Given** un source_name que no está en fusion_sources  
**When** llamo a `analytics.source_stats(source_name)`  
**Then** devuelve `None`.

### E6 · multi_source_consensus muestra el valor con más fuentes

**Given** una entidad con la property key "country" que tiene valor "RU" de 2 fuentes y "US" de 1 fuente  
**When** llamo a `analytics.multi_source_consensus(eid, "country")`  
**Then** `consensus_value == "RU"`  
**And** `consensus_strength` es 0.67 (2/3)  
**And** `values` tiene 2 entradas  
**And** `total_sources == 3`.

### E7 · multi_source_consensus con key inexistente

**Given** una entidad que no tiene la property key "nonexistent"  
**When** llamo a `analytics.multi_source_consensus(eid, "nonexistent")`  
**Then** `values == []`  
**And** `consensus_value == ""`.

### E8 · corroborated_properties filtra por min_sources

**Given** una entidad con "country=RU" de 3 fuentes y "org=EvilCorp" de 1 fuente  
**When** llamo a `analytics.corroborated_properties(eid, min_sources=2)`  
**Then** solo 1 resultado: `key == "country"`  
**And** `source_count == 3`.

### E9 · entity_search por término

**Given** un fusion_store con entidades que contienen "evil" en su valor o normalized  
**When** llamo a `analytics.entity_search("evil")`  
**Then** devuelve >= 1 resultados  
**And** cada resultado tiene `id`, `type`, `value`, `confidence`, `source_count`.

### E10 · entity_search vacío

**Given** un fusion_store con entidades  
**When** llamo a `analytics.entity_search("zzz_nonexistent_yyy")`  
**Then** devuelve lista vacía.

### E11 · top_changed devuelve entidades con actividad reciente

**Given** un fusion_store con entidades que tienen `last_seen` en los últimos 7 días  
**When** llamo a `analytics.top_changed(days=7)`  
**Then** devuelve lista de entidades ordenadas por `new_observations` descendente  
**And** cada una tiene `entity_id`, `type`, `value`.

### E12 · source_corroboration_matrix

**Given** un fusion_store con múltiples fuentes que comparten entidades  
**When** llamo a `analytics.source_corroboration_matrix()`  
**Then** devuelve lista de pares `(source_a, source_b)` con `shared_entities >= 0`.

### E13 · FusionAnalytics con store=None

**Given** `analytics = FusionAnalytics(None)`  
**When** llamo a cualquier método  
**Then** devuelve el valor vacío correspondiente (None, [], {}) sin lanzar.

### E14 · entity_search con filtro por tipo

**Given** un fusion_store con entidades de tipo "domain" y "ipv4"  
**When** llamo a `analytics.entity_search("evil", etype="domain")`  
**Then** solo devuelve entidades de tipo `domain`.

### E15 · entity_search con min_confidence y min_sources

**Given** un fusion_store con entidades de distintas confianzas y source_counts  
**When** llamo a `analytics.entity_search("evil", min_confidence=0.5, min_sources=2)`  
**Then** todos los resultados tienen `confidence >= 0.5` y `source_count >= 2`.

### E16 · entity_summary con store=None

**Given** `analytics = FusionAnalytics(None)`  
**When** llamo a `analytics.entity_summary("any_id")`  
**Then** devuelve `None`.

### E17 · source_stats devuelve success_rate correcto

**Given** una fuente con `fetch_count=10` y `ok_count=7`  
**When** llamo a `analytics.source_stats(source_name)`  
**Then** `success_rate == 0.7`  
**And** `fetch_count == 10`  
**And** `ok_count == 7`.

---

## Cierre del módulo

- **Fecha de cierre:** _(se llena al cerrar)_
- **Estado:** ⏳ en implementación.
- **Validación:**
  - `pytest tests/test_fusion_analytics.py -v` → todos verdes
  - `ruff check estorides_core/fusion_analytics.py tests/test_fusion_analytics.py` → limpio
  - `mypy --strict estorides_core/fusion_analytics.py` → sin errores
  - `bandit -r estorides_core/fusion_analytics.py` → sin High ni Medium
