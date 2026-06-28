# `change_detection` — Spec (Módulo 2c)

> Detecta deltas entre dos snapshots del estado de una investigación
> (entities, properties, source corroborations, edge weights) y emite
> un `ChangeReport` auditable, con score por reliability y filtros
> configurables. Es la pieza que responde "¿qué cambió en este target
> desde la última vez?" y la que abre la puerta a alertas en tiempo
> cuasi-real (webhooks, RSS de cambios) y a la vista de diff en la UI.

---

## Purpose

Hoy el fusion store (`estorides_core/fusion_store.py`) ya persiste
`first_seen`/`last_seen` por entity, `seen_count` por (entity,
source), y `confidence` por entity. Pero **nadie mira** esa
información. Cada run empieza de cero: vuelve a ver las mismas 50
subdominios de crt.sh, las mismas IP, los mismos ASNs, y el LLM
analyst no tiene forma de decir "esto es nuevo desde ayer" o "este
registrant cambió de email".

Este módulo introduce el **concepto de snapshot** y la operación
**diff**. Un snapshot es una vista inmutable del estado de un target
en un instante. La diff es la operación pura `(snapshot_before,
snapshot_after) -> ChangeReport`. El motor usa la diff para:

- **Alertas**: si una entity `A` cambia de ASN, score alto → webhook.
- **Vista de diff en UI**: "what's new in this case" (verde=nuevo,
  rojo=desaparecido, amarillo=cambió).
- **Recurrence pivots**: si un IOC aparece y desaparece, eso es
  señal de bulletproof handoff → flag para el pivot engine.
- **Audit trail**: el change report se serializa al case store como
  un evento `change` con timestamp, para reconstruir historia.

El módulo es la pieza "temporal" del layer de information. No
almacena estado: eso es el fusion store. No genera hipótesis: eso
es 2b. No dispara alertas: eso es el orchestrator/web layer.
**Solo diff**.

## Inputs

### `detect_changes(snapshot_before, snapshot_after, *, config)`

| Parámetro | Tipo | Default | Notas |
| --- | --- | --- | --- |
| `snapshot_before` | `Snapshot` | obligatorio | El estado anterior. Si es `None`, se trata como "todo es nuevo" (first run). |
| `snapshot_after` | `Snapshot` | obligatorio | El estado actual. Si es `None`, devuelve `ChangeReport` vacío (no se puede diff contra nada). |
| `config` | `ChangeConfig` | `ChangeConfig()` | Filtros y tuning. Ver abajo. |

### `Snapshot` (dataclass frozen)

```json
{
  "entities": [
    {"id": "abc", "type": "domain", "value": "example.com",
     "sources": ["crt_sh_certificates", "hackertarget_whois"],
     "properties": {"registrant_organization": "EvilCorp", "asn": "AS15169"},
     "edges": [{"dst": "ip:1.2.3.4", "rel": "resolves_to"}],
     "first_seen": 1700000000.0,
     "last_seen": 1700100000.0,
     "confidence": 0.78}
  ],
  "snapshot_at": 1700200000.0
}
```

| Campo | Tipo | Notas |
| --- | --- | --- |
| `entities` | `Sequence[SnapshotEntity]` | Inmutable. Vacío permitido. |
| `snapshot_at` | `float` (epoch seconds) | Cuándo se tomó el snapshot. |

### `SnapshotEntity` (dataclass frozen)

| Campo | Tipo | Notas |
| --- | --- | --- |
| `id` | `str` | Id canónico (mismo que `fusion_store.entity_id`). |
| `type` | `str` | `domain`, `ipv4`, etc. |
| `value` | `str` | El valor. |
| `sources` | `Sequence[str]` | Source names que vieron la entity. Sorted. |
| `properties` | `Mapping[str, str]` | Atributos clave-valor. |
| `edges` | `Sequence[Edge]` | Edges salientes (este módulo no inspecciona edges entrantes en v1). |
| `first_seen` | `float` | epoch. |
| `last_seen` | `float` | epoch. |
| `confidence` | `float` | `[0, 1]`. |

### `Edge` (dataclass frozen)

```json
{"dst": "ip:1.2.3.4", "rel": "resolves_to"}
```

### `ChangeConfig` (dataclass frozen)

| Campo | Tipo | Default | Notas |
| --- | --- | --- | --- |
| `min_reliability` | `SourceReliability` | `C` | Sources con reliability < min_reliability no se cuentan en el score del change. |
| `min_change_score` | `float` | `0.10` | Cambios con score final bajo este umbral se filtran. `[0, 1]`. |
| `disappear_grace_days` | `float` | `7.0` | Si una entity "desaparece" pero su `last_seen` en before era hace < grace_days, no se reporta como disappearance (probable miss transitorio). |
| `include_disappeared` | `bool` | `True` | Incluir `kind=disappeared` en el report. |
| `include_property_changes` | `bool` | `True` | Incluir `kind=property_changed` en el report. |
| `include_source_added` | `bool` | `True` | Incluir `kind=source_added` en el report. |
| `max_changes` | `int` | `500` | Tope duro. Devuelve los N de mayor score. |

## Outputs

### `Change` (dataclass frozen, JSON-serializable)

```json
{
  "id": "sha1:abc...",
  "kind": "new" | "disappeared" | "property_changed" | "source_added" | "source_removed" | "edge_added" | "edge_removed" | "confidence_shifted",
  "entity_id": "abc123",
  "entity_type": "domain",
  "entity_value": "example.com",
  "before": null,
  "after": {"sources": ["crt_sh_certificates"], "properties": {"asn": "AS15169"}},
  "diff": {"added": ["registrant_organization"], "changed": {"asn": ["AS13335", "AS15169"]}, "removed": []},
  "score": 0.78,
  "sources": ["crt_sh_certificates", "hackertarget_whois"],
  "detected_at": 1700200000.0
}
```

| Campo | Tipo | Rango | Significado |
| --- | --- | --- | --- |
| `id` | `str` | sha1 hex 16 | Determinístico: `sha1(kind + entity_id + diff_signature)[:16]`. |
| `kind` | `str` | uno de los `CHANGE_KINDS` | Ver tabla. |
| `entity_id` | `str` | — | Id de la entity afectada. |
| `entity_type` | `str` | — | Copia. |
| `entity_value` | `str` | — | Copia. |
| `before` | `Mapping` o `None` | — | Estado anterior (relevante para diff). `None` para `kind=new`. |
| `after` | `Mapping` o `None` | — | Estado nuevo. `None` para `kind=disappeared`. |
| `diff` | `Mapping` | — | Estructura tipada del delta. Ver abajo. |
| `score` | `float` | `[0, 1]` | Importancia del cambio. |
| `sources` | `list[str]` | — | Source names que aportaron (sorted). |
| `detected_at` | `float` | epoch | Cuándo se computó el change. |

### `Diff` (dataclass frozen, JSON-serializable)

```json
{
  "added": ["new_prop_key"],
  "changed": {"asn": ["old_value", "new_value"]},
  "removed": ["old_prop_key"]
}
```

| Campo | Tipo | Notas |
| --- | --- | --- |
| `added` | `list[str]` | Keys de properties que aparecieron en after. |
| `changed` | `dict[str, list[str]]` | key → `[old, new]`. |
| `removed` | `list[str]` | Keys que desaparecieron en after. |

### `ChangeReport` (dataclass frozen)

```json
{
  "changes": [Change, ...],
  "summary": {
    "total": 5,
    "by_kind": {"new": 1, "property_changed": 2, "disappeared": 1, "source_added": 1},
    "entities_compared": 50,
    "entities_added": 1,
    "entities_removed": 1,
    "properties_changed": 2,
    "score_max": 0.92,
    "score_mean": 0.55,
    "computed_at": 1700200000.0,
    "snapshot_before_at": 1700000000.0,
    "snapshot_after_at": 1700200000.0
  }
}
```

| Campo | Tipo | Notas |
| --- | --- | --- |
| `changes` | `list[Change]` | Top por score, capped por `max_changes`. |
| `summary` | `ChangeSummary` | Conteos y stats. |

## Tabla de errores

| Modo de falla | Comportamiento |
| --- | --- |
| `snapshot_before = None` | Reporta **todo** lo de after como `kind=new`. |
| `snapshot_after = None` | Devuelve `ChangeReport` vacío (no se puede diff). |
| `snapshot_before.at > snapshot_after.at` | Log warning; diff en orden de timestamps sin asumir causalidad. No falla. |
| `SnapshotEntity.id` vacío | `ValueError` (programmer error: cada entity debe tener id). |
| `ChangeConfig.min_change_score` fuera de `[0,1]` | `ValueError`. |
| `ChangeConfig.max_changes < 1` | `ValueError`. |
| `ChangeConfig.min_reliability` no es enum | `TypeError`. |
| Entity con `type` o `value` vacíos | `ValueError` (programmer error). |
| Hostile property key (control chars, 1 MB) | El `diff` se emite igual; la key se trunca a 200 chars. |

## Garantías de seguridad

1. **Pure.** `detect_changes` es puro: no I/O, no DB, no logging del
   contenido. Mismo input → mismo output.
2. **No eval / exec.** Los values se serializan a str, nunca se
   interpretan.
3. **Bounded.** `max_changes` acota la salida. Iteración O(N entities +
   M properties). Memoria acotada por el input.
4. **Deterministic ids.** El `Change.id` es un hash del contenido
   (`kind`, `entity_id`, `diff_signature`). Re-ejecución con el mismo
   input produce el mismo id.
5. **Reliability-weighted scores.** El `score` de un change pondera
   cada source que contribuyó a la entity, filtrando las que caen
   por debajo de `min_reliability`. Una ASN change reportada solo
   por una source `F` queda con score 0.10; reportada por 3 sources
   `B/A/A` queda con score ~0.85.
6. **Fail-loud en programmer input, fail-soft en data upstream.**
   Validación de tipos/rangos lanza. Hostile property keys se
   truncan, no fallan.
7. **Audit trail completo.** Cada change expone `before`/`after`/
   `diff`/`sources`/`score`/`detected_at`. Un analista puede
   reconstruir la historia.

## Out of scope

- **Persistencia.** El `ChangeReport` vive en memoria. Su
  serialización al case store como evento `change` es el PR de wire-up
  a `orchestrator.run()`.
- **Generación de alertas.** El módulo produce el report; quien
  dispara webhooks/Slack/email es el orchestrator/web layer.
- **Cross-case correlation.** Diffs entre dos casos distintos (no
  entre dos runs del mismo caso) es el módulo 2f.
- **Schema migration.** Si la shape de un property cambia entre
  versiones de Estorides, eso no es change detection, eso es un
  feature flag.
- **Time series / forecasting.** "esto va a cambiar en 7 días" es
  el módulo 2d (pattern-of-life).
- **Diff de grafo completo.** Solo inspeccionamos edges *salientes*
  declarados en `SnapshotEntity.edges`. Edges de NetworkX no
  disponibles en v1.

---

## CHANGE_KINDS (vocabulario estable)

> Los kinds son **contratos**. Cambian solo con acuerdo explícito.
> Persistir en `fusion_store` requiere migración.

| `kind` | Trigger | Score base |
| --- | --- | --- |
| `new` | Entity en after, no en before. | `reliability_max` (mejor source) |
| `disappeared` | Entity en before, no en after, fuera de grace. | `1 - confidence_before` (cuanto más fiable era antes, más raro es que desaparezca) |
| `property_changed` | Misma entity, mismo key, distinto value. | `0.5 + 0.5 * corroboration` (cuanto más corroborado, más serio el cambio) |
| `source_added` | Misma entity, nueva source que la vio. | `reliability_weight` de la nueva source. |
| `source_removed` | Misma entity, source que la veía ya no. (raro) | `0.3` (señal débil, posible miss) |
| `edge_added` | Nueva edge saliente. | `0.5` (sin más info) |
| `edge_removed` | Edge que existía, ya no. | `0.5` |
| `confidence_shifted` | `confidence_after - confidence_before` > 0.20. | `|delta|` |

El score final = `min(1.0, score_base * corroboration_factor *
freshness_factor)`. El `freshness_factor` decae con la edad del
snapshot: un change que ocurrió hace 30 días es menos urgente que
uno de hace 1 hora.

---

## Escenarios BDD (Given-When-Then)

### S1 · Happy path: una entity nueva

**Given** `snapshot_before` con 1 entity `(domain, example.com)`.  
**And** `snapshot_after` con esa misma + 1 nueva entity `(ipv4,
1.2.3.4)`.  
**When** llamo a `detect_changes(before, after)`.  
**Then** el report tiene exactamente 1 change.  
**And** su `kind == "new"`.  
**And** su `entity_type == "ipv4"`, `entity_value == "1.2.3.4"`.  
**And** `score >= 0.5` (porque ipv4 sources suelen ser reliability B).

### S2 · Happy path: property changed

**Given** `before` con entity `(domain, example.com)` y property
`asn=AS13335`.  
**And** `after` con la misma entity y `asn=AS15169`.  
**When** llamo a `detect_changes(...)`.  
**Then** hay 1 change de `kind=property_changed`.  
**And** `diff.changed["asn"] == ["AS13335", "AS15169"]`.  
**And** `score >= 0.5`.

### S3 · Edge: first run (before = None)

**Given** `snapshot_before = None`.  
**And** `snapshot_after` con 5 entities.  
**When** llamo a `detect_changes(None, after)`.  
**Then** el report tiene 5 changes, todos `kind=new`.  
**And** `summary.entities_added == 5`.

### S4 · Edge: after = None (nada que comparar)

**Given** `snapshot_after = None`.  
**When** llamo a `detect_changes(before, None)`.  
**Then** el report tiene 0 changes.  
**And** no lanza.

### S5 · Edge: disappeared con grace

**Given** `before` con entity `(domain, foo.com)` y `last_seen = T-2d`.  
**And** `after` sin esa entity.  
**When** llamo a `detect_changes(..., config=ChangeConfig(disappear_grace_days=7.0))`.  
**Then** no hay `kind=disappeared` (dentro del grace, probablemente
miss transitorio).  
**And** con `disappear_grace_days=1.0`, sí hay `kind=disappeared`.

### S6 · Edge: source_added

**Given** `before` con entity `(domain, example.com)` y `sources=["crt_sh"]`.  
**And** `after` con misma entity y `sources=["crt_sh", "rdap_domain"]`.  
**When** llamo a `detect_changes(...)`.  
**Then** hay 1 change de `kind=source_added` con
`after.sources == ["rdap_domain"]` (la nueva).  
**And** `score == reliability_weight["rdap_domain"]` (≈ 0.85).

### S7 · Edge: min_reliability filtra source_added ruidosos

**Given** `before` con entity sin source `F`.  
**And** `after` con la entity + source `F` (cualquier source con
reliability `F`).  
**When** `config.min_reliability = E`.  
**Then** el `source_added` para F se filtra (E < F, queda fuera).

### S8 · Edge: max_changes acota la salida

**Given** input que produce 100 changes.  
**When** `config.max_changes = 10`.  
**Then** `len(changes) == 10` (los de mayor score).

### S9 · Error: programmer input inválido

**Given** que llamo a `detect_changes` con:
- `snapshot_before.at = "not a number"`
- `SnapshotEntity` con `id = ""`  
- `ChangeConfig(min_change_score=1.5)`
- `ChangeConfig(max_changes=0)`  
**When** se ejecuta  
**Then** cada uno lanza `ValueError` o `TypeError` con mensaje claro.

### S10 · Seguridad: property key hostil

**Given** una entity con `properties` que tienen keys de 1 MB, control
chars, NUL bytes, HTML, SQL.  
**When** llamo a `detect_changes(...)`.  
**Then** el change se emite igual.  
**And** las keys se truncan a 200 chars en el `diff`.  
**And** no hay crash, no se ejecuta nada, no se loguea el contenido.

### S11 · Determinismo

**Given** un par `(before, after)` fijo.  
**When** llamo a `detect_changes` dos veces.  
**Then** los dos `ChangeReport` son idénticos (mismos `id`s, scores,
order). Reordenar `before.entities` o `after.entities` no cambia la
salida (el módulo ordena internamente antes de hashear).

### S12 · Bounded / property-based (hypothesis)

**Given** snapshots aleatorios con N entities (N acotado).  
**When** llamo a `detect_changes`.  
**Then**:
- `0.0 <= score <= 1.0` para todo change.
- `len(changes) <= max_changes`.
- `summary.entities_compared == len(before.entities)` (o 0 si before is None).
- `summary.total == len(changes)`.
- `summary.by_kind` cuenta cada kind exactamente el número de veces
  que aparece en `changes`.

(Implementado en `tests/properties/test_change_detection_properties.py`.)

### S13 · Edge: source_removed

**Given** `before` con entity `(domain, example.com)` y
`sources=["crt_sh_certificates", "rdap_domain"]`.  
**And** `after` con misma entity y `sources=["crt_sh_certificates"]`.  
**When** llamo a `detect_changes(...)`.  
**Then** hay 1 change de `kind=source_removed` con `"rdap_domain"` en
`diff.removed`.  
**And** `score == 0.30` (señal débil: probable miss transitorio).  
**And** con `min_change_score=0.5` el change se filtra.

### S14 · Edge: edge_added / edge_removed

**Given** `before` con entity que tiene edge `(ipv4:2.2.2.2, resolves_to)`.  
**And** `after` con la misma entity sin ese edge.  
**When** llamo a `detect_changes(...)`.  
**Then** hay 1 change de `kind=edge_removed` con
`"2.2.2.2"` en `diff.removed`.  
**And** el simétrico (entidad gana edge) emite `kind=edge_added` con
`score=0.5`.

### S15 · Edge: confidence_shifted (delta > 0.20)

**Given** `before` con entity con `confidence=0.4`.  
**And** `after` con la misma entity y `confidence=0.8` (delta=0.4).  
**When** llamo a `detect_changes(...)`.  
**Then** hay 1 change de `kind=confidence_shifted` con
`diff.changed["confidence"] == ["0.4000", "0.8000"]`.  
**And** `score == 0.4`.  
**And** con `confidence` 0.50→0.55 (delta=0.05) no se emite.

---

## Cierre del módulo

- **Fecha de cierre:** 2026-06-27.
- **Estado:** closed.
- **Cambios sobre la versión inicial (cierre):**
  - Test S7 corregido: usaba `psbdmp_ws` (D) y se cambió a `untrusted_webscraper` (F)
    para reflejar fielmente la semántica del spec ("min_reliability filtra
    fuentes con reliability peor que el mínimo").
  - `_truncate_key` ajustado a 199 chars + "…" (200 total) para cumplir
    literalmente la garantía "se truncan a 200 chars".
  - Añadido `untrusted_webscraper`: `SourceReliability.F` al
    `SOURCE_RELIABILITY_MAP` (módulo 2a) — fuente de prueba para el caso
    "min_reliability filtra F".
  - Refactor boy-scout: extraído `_make_change` (8 builders → 1 helper),
    `_union_sources` y `_below_min_reliability` para eliminar
    duplicación. 121 tests verdes; ruff + mypy --strict + bandit clean.
  - Property test S12 cubre 8 invariantes con 1000 ejemplos cada uno
    (cumple la doctrina "mínimo 1000 por propiedad invariante" de
    CLAUDE.md §6): bounded scores, max_changes, id format,
    idempotencia, first run, after=None, before-vs-no-after,
    summary-consistency (total/by_kind/entities_added/
    entities_removed/properties_changed/entities_compared/
    score_max/score_mean deben coincidir con `changes`).
  - Añadidos BDD S13 (source_removed), S14 (edge_added/edge_removed)
    y S15 (confidence_shifted) — cobertura explícita de los kinds
    que no tenían escenario dedicado. Cobertura: 30 BDD tests
    totales (S1-S15).
- **Cambios al motor que este módulo habilita:**
  - Webhook de changes: cuando `len(changes) > 0`, el orchestrator
    emite un SSE/email.
  - UI "What's new": vista Cases → Diff (verde/rojo/amarillo).
  - Pivot engine: cambios en ASN/registrant/email disparan re-pivots.
  - Audit trail: `ChangeReport` se serializa al case store.
- **Call sites que aún no migran** (documentado, no en este PR):
  `orchestrator.run()` no invoca `detect_changes` todavía. El wire-up
  es el PR siguiente, con un nuevo endpoint `/api/cases/<id>/diff`.
