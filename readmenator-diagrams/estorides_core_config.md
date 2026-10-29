# estorides_core: config

estorides_core: config groups 16 files (py) around _installed_share, _resolve_dir, _resolve_writable_dir, ensure_data_dirs, ensure_reports_dir. estorides_core.async_client

```mermaid
graph LR
    estorides_core["estorides_core"]
    tests["tests"]
    tests -- "calls into" --> estorides_core
```

## estorides_core (5.1)

estorides_core groups 10 files (py) around _installed_share, _resolve_dir, _resolve_writable_dir, ensure_data_dirs, ensure_reports_dir. estorides_core.async_client

## tests (5.2)

tests groups 6 files (py) around meta_strategy, obs_strategy, entity_strategy, test_observation_round_trip_stability, test_observation_bounded_fields. Property-based invariants for estorides_core.observation_models.

**Files**:

- estorides_core/async_client.py
- estorides_core/config.py
- estorides_core/intel_resolver.py
- estorides_core/lan_bundle.py
- estorides_core/observation_models.py
- estorides_core/ontology.py
- estorides_core/osiris_sources.py
- estorides_core/pivot_engine.py
- estorides_core/ssrf_guard.py
- estorides_core/transforms.py
- tests/properties/test_observation_models_properties.py
- tests/test_async_client.py
- tests/test_config_env.py
- tests/test_observation_models.py
- tests/test_structured_extraction.py
- tests/test_transforms.py
