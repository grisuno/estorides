# estorides_core: graph_bundle

*Community 9 | 5 files | cohesion 0.71*

## Definition

This community groups 5 file(s) rooted at `estorides_core` with dominant language py (cohesion 0.71). Central symbols: `BundleLayout`, `SphereBundleLayout`, `_assert_consistent`, `_bspline`, `_bundle_curves`, `_clusters`, `_degrees`, `_edges`. Core file: `tests/test_graph_bundle.py` (30 symbols). Documented purpose: graph_bundle: payload circle 2D + sphere 3D estilo ReadMenator.  Porta ``readmenator/_bundlegraph.py`` (``BundleGraphRenderer.build_payload``) y ``readmenator/_.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_core/graph_bundle.py` | py | utility | 18 | yes |
| `estorides_core/graph_force.py` | py | utility | 12 | yes |
| `tests/properties/test_graph_bundle_properties.py` | py | testing | 6 | yes |
| `tests/test_graph_bundle.py` | py | testing | 30 | yes |
| `tests/test_graph_force3d.py` | py | testing | 9 | yes |

## Key Symbols

- `BundleLayout` (class, `estorides_core/graph_bundle.py:37`) `class BundleLayout` - Resultado del bundling circular (igual que ReadMenator).
- `SphereBundleLayout` (class, `estorides_core/graph_bundle.py:49`) `class SphereBundleLayout` - Resultado del bundling esferico (igual que ReadMenator).
- `_req_str` (method, `estorides_core/graph_bundle.py:59`) `def _req_str(item, key, default, what)`
- `_opt_str` (method, `estorides_core/graph_bundle.py:68`) `def _opt_str(item, key, default)`
- `_opt_float` (method, `estorides_core/graph_bundle.py:73`) `def _opt_float(item, key, default)`
- `_opt_int` (method, `estorides_core/graph_bundle.py:84`) `def _opt_int(item, key, default)`
- `_opt_community` (method, `estorides_core/graph_bundle.py:94`) `def _opt_community(value)`
- `_bspline` (method, `estorides_core/graph_bundle.py:102`) `def _bspline(control, samples)` - Muestrea una B-spline cubica uniforme clamped (cualquier dimension).
- `_bundle_curves` (method, `estorides_core/graph_bundle.py:135`) `def _bundle_curves(leaves, member_group, hub, root, edges, beta, samples)` - Rutea cada arista por la jerarquia y la muestrea como B-spline.
- `hierarchical_edge_bundling` (method, `estorides_core/graph_bundle.py:171`) `def hierarchical_edge_bundling(groups, edges, center, radius, beta, samples, gro` - Hojas en un circulo por grupo; aristas por la jerarquia (Holten 2006).
- `fibonacci_sphere` (method, `estorides_core/graph_bundle.py:215`) `def fibonacci_sphere(count)` - Vectores unitarios casi uniformes en espiral de angulo dorado.
- `_unit` (method, `estorides_core/graph_bundle.py:231`) `def _unit(v)`
- `_split_caps` (method, `estorides_core/graph_bundle.py:238`) `def _split_caps(labels, sizes, points, lattice, out)` - Biseca el lattice entre runs de grupos hasta un cap contiguo por grupo.
- `spherical_edge_bundling` (method, `estorides_core/graph_bundle.py:267`) `def spherical_edge_bundling(groups, edges, radius, beta, samples, inner_ratio)` - Hojas en caps esfericos por comunidad; aristas por la jerarquia.
- `_round2` (method, `estorides_core/graph_bundle.py:316`) `def _round2(pt)`
- `_round3` (method, `estorides_core/graph_bundle.py:320`) `def _round3(pt)`
- `bundle_settings` (method, `estorides_core/graph_bundle.py:324`) `def bundle_settings()` - Defaults de la pagina bundle (fuente unica para el JS).
- `build_bundle_payload` (method, `estorides_core/graph_bundle.py:359`) `def build_bundle_payload(force_payload)` - Deriva el payload bundle desde un payload force RAW.
- `family_color_from_name` (function, `estorides_core/graph_force.py:48`) `def family_color_from_name(name, sat_base, sat_span, light_base, light_span)` - Deriva un color HSL estable desde un label (djb2, como ReadMenator).
- `node_value` (function, `estorides_core/graph_force.py:65`) `def node_value(symbols, degree, findings)` - Escala log2 del tamano de nodo (minimo 1).
- `force_settings` (function, `estorides_core/graph_force.py:70`) `def force_settings()` - Valores SETTINGS de ReadMenator graph-force.html (fuente unica).
- `_req_str` (function, `estorides_core/graph_force.py:97`) `def _req_str(item, key, default, what)` - Lee un campo string obligatorio; fail-closed ante no-str.
- `_opt_str` (function, `estorides_core/graph_force.py:107`) `def _opt_str(item, key, default)` - Lee un campo de estilo; ante no-str usa el default (no mata el grafo).
- `_opt_int` (function, `estorides_core/graph_force.py:113`) `def _opt_int(item, key, default)` - Lee un campo entero; ante basura usa el default.
- `_degrees` (function, `estorides_core/graph_force.py:124`) `def _degrees(node_ids, edges)` - Grado por nodo + edges validos (ambos extremos conocidos).
- `_is_bridge` (function, `estorides_core/graph_force.py:150`) `def _is_bridge(edge)` - Un edge es puente si lo declara o si une clusters distintos.
- `build_force_payload` (function, `estorides_core/graph_force.py:161`) `def build_force_payload(nodes, edges, clusters, max_nodes, max_edges)` - Convierte nodos/edges OSINT (`/api/graph`) al formato RAW force-graph.
- `_md_safe` (function, `estorides_core/graph_force.py:332`) `def _md_safe(text, limit)` - Neutraliza un string remoto para embeberlo en markdown extractivo.
- `_truncate_lines` (function, `estorides_core/graph_force.py:341`) `def _truncate_lines(markdown, budget)` - Corte duro por linea completa + marcador (fences nunca se emiten).
- `build_ai_context` (function, `estorides_core/graph_force.py:353`) `def build_ai_context(nodes, edges, clusters, budget_chars)` - Contexto markdown extractivo con presupuesto para la IA local.

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 16
- Cross-boundary resolved imports (EXTRACTED): 3

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in estorides_core: graph_bundle changed?
- Should estorides_core: graph_bundle be split, given cohesion 0.71?

## Sources

- `estorides_core/graph_bundle.py`
- `estorides_core/graph_force.py`
- `tests/properties/test_graph_bundle_properties.py`
- `tests/test_graph_bundle.py`
- `tests/test_graph_force3d.py`
