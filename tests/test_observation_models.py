"""
estorides_core.observation_models — BDD/TDD contract tests.

Each test is the executable translation of a BDD scenario in
`spec/observation_models.md` (O1-O8). The module under test does not exist yet;
these tests must fail (import error) until the implementation lands.
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from estorides_core.observation_models import (
    MAX_STR_LEN,
    MAX_URL_LEN,
    MAX_VALUE_LEN,
    SCHEMA_VERSION,
    Observation,
    ObservationMeta,
    ObservedEntity,
    RunResult,
)


def _full_meta() -> dict:
    return {
        "url": "https://crt.sh/?q=example.com",
        "method": "get",
        "host": "crt.sh",
        "attempts": 1,
        "cached": False,
        "proxied": True,
        "status": 200,
        "content_type": "application/json",
        "error": "",
    }


def _full_obs() -> dict:
    return {
        "source": "crt.sh",
        "category": "DNS",
        "description": "CT log",
        "parser": "json",
        "parsed": ["example.com", "www.example.com"],
        "raw": None,
        "meta": _full_meta(),
        "observed_at": 1_700_000_000.0,
        "ontology": {"sanctioned": False, "hits": []},
        "mitre": {"techniques": []},
    }


# ---------------------------------------------------------------------------
# O1 · Happy path: a full observation validates
# ---------------------------------------------------------------------------
def test_o1_full_observation_validates() -> None:
    obs = Observation.model_validate(_full_obs())
    legacy = obs.to_legacy_dict()
    assert legacy["source"] == "crt.sh"
    assert legacy["parsed"] == ["example.com", "www.example.com"]
    assert legacy["meta"]["method"] == "GET"          # uppercased
    assert legacy["meta"]["status"] == 200
    assert legacy["meta"]["cached"] is False
    assert legacy["meta"]["proxied"] is True
    assert legacy["observed_at"] == 1_700_000_000.0


# ---------------------------------------------------------------------------
# O2 · Edge: error observation (parsed=None) validates
# ---------------------------------------------------------------------------
def test_o2_error_observation_validates() -> None:
    err = _full_obs()
    err["parsed"] = None
    err["raw"] = None
    err["meta"]["error"] = "circuit_open"
    obs = Observation.model_validate(err)
    assert obs.parsed is None
    assert obs.to_legacy_dict()["parsed"] is None


# ---------------------------------------------------------------------------
# O3 · Error: missing required field fails loudly
# ---------------------------------------------------------------------------
def test_o3_missing_required_field_fails() -> None:
    bad = _full_obs()
    del bad["source"]
    with pytest.raises(ValidationError) as exc:
        Observation.model_validate(bad)
    assert "source" in [str(loc[-1]) for loc in (e["loc"] for e in exc.value.errors())]


# ---------------------------------------------------------------------------
# O4 · Error: unknown meta key is forbidden
# ---------------------------------------------------------------------------
def test_o4_unknown_meta_key_forbidden() -> None:
    meta = _full_meta()
    meta["sneaky_field"] = "value"
    with pytest.raises(ValidationError):
        ObservationMeta.model_validate(meta)


# ---------------------------------------------------------------------------
# O5 · Error: wrong-typed field fails
# ---------------------------------------------------------------------------
def test_o5_wrong_typed_field_fails() -> None:
    bad = _full_obs()
    bad["meta"]["status"] = "200"          # str, not int
    with pytest.raises(ValidationError):
        Observation.model_validate(bad)


# ---------------------------------------------------------------------------
# O6 · Security: hostile/boundary inputs bounded, never echoed
# ---------------------------------------------------------------------------
def test_o6_oversized_url_truncated_not_failed() -> None:
    meta = _full_meta()
    meta["url"] = "x" * 10_000
    m = ObservationMeta.model_validate(meta)
    assert len(m.url) <= MAX_URL_LEN
    assert len(m.url) == MAX_URL_LEN


def test_o6_oversized_value_rejected() -> None:
    ent = {
        "type": "domain",
        "value": "y" * 10_000,
        "source": "crt.sh",
    }
    with pytest.raises(ValidationError):
        ObservedEntity.model_validate(ent)


def test_o6_error_message_does_not_embed_hostile_value() -> None:
    ent = {"type": "domain", "value": "Z" * 10_000, "source": "crt.sh"}
    with pytest.raises(ValidationError) as exc:
        ObservedEntity.model_validate(ent)
    msg = str(exc.value)
    assert ("Z" * 10_000) not in msg


# ---------------------------------------------------------------------------
# O7 · Edge: confidence bounds are enforced
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("confidence", [1.5, -0.1])
def test_o7_confidence_out_of_range_rejected(confidence: float) -> None:
    ent = {"type": "person", "value": "Alice", "source": "x", "confidence": confidence}
    with pytest.raises(ValidationError):
        ObservedEntity.model_validate(ent)


def test_o7_confidence_at_bounds_accepted() -> None:
    for c in (0.0, 1.0):
        ent = ObservedEntity.model_validate(
            {"type": "person", "value": "Bob", "source": "x", "confidence": c}
        )
        assert 0.0 <= ent.confidence <= 1.0


# ---------------------------------------------------------------------------
# O8 · RunResult aggregates nested models
# ---------------------------------------------------------------------------
def test_o8_run_result_aggregates() -> None:
    run = {
        "entities": [
            {"type": "domain", "value": "example.com", "source": "crt.sh"}
        ],
        "observations": [_full_obs()],
        "sources_succeeded": 3,
    }
    result = RunResult.model_validate(run)
    assert isinstance(result.entities[0], ObservedEntity)
    assert isinstance(result.observations[0], Observation)
    legacy = result.to_legacy_dict()
    assert legacy["sources_succeeded"] == 3
    assert "entities" in legacy and "observations" in legacy
    # Re-validation of the projected dict round-trips.
    reloaded = RunResult.model_validate(legacy)
    assert len(reloaded.entities) == len(result.entities)


def test_o8_run_result_with_error_surfaces_error() -> None:
    run = {"entities": [], "observations": [], "sources_succeeded": 0,
           "error": "circuit_open"}
    result = RunResult.model_validate(run)
    assert result.error == "circuit_open"
    legacy = result.to_legacy_dict()
    assert legacy["error"] == "circuit_open"
    # Round-trips.
    reloaded = RunResult.model_validate(legacy)
    assert reloaded.error == "circuit_open"


# ---------------------------------------------------------------------------
# Security: JSON-safety of parsed/raw/attributes/ontology/mitre
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("field", ["parsed", "raw"])
def test_security_non_json_safe_value_rejected(field: str) -> None:
    obs = _full_obs()
    obs[field] = {"nested": {"set_obj": {1, 2, 3}}}   # set is not JSON-safe
    with pytest.raises(ValidationError):
        Observation.model_validate(obs)


def test_security_non_json_safe_attributes_rejected() -> None:
    ent = {"type": "domain", "value": "example.com", "source": "x",
           "attributes": {"bad": b"bytes"}}
    with pytest.raises(ValidationError):
        ObservedEntity.model_validate(ent)


def test_security_bytes_top_level_parsed_rejected() -> None:
    obs = _full_obs()
    obs["parsed"] = b"raw bytes"
    with pytest.raises(ValidationError):
        Observation.model_validate(obs)


def test_security_non_string_dict_key_rejected() -> None:
    obs = _full_obs()
    obs["parsed"] = {1: "integer key"}
    with pytest.raises(ValidationError):
        Observation.model_validate(obs)


def test_security_arbitrary_object_rejected() -> None:
    class _Hostile:
        pass

    obs = _full_obs()
    obs["parsed"] = _Hostile()
    with pytest.raises(ValidationError):
        Observation.model_validate(obs)


def test_security_nested_object_inside_list_rejected() -> None:
    """A hostile object nested inside a list must also be rejected (recursion)."""
    class _Hostile:
        pass

    obs = _full_obs()
    obs["parsed"] = [{"ok": 1}, [_Hostile()]]
    with pytest.raises(ValidationError):
        Observation.model_validate(obs)


def test_security_arbitrary_object_message_names_the_type() -> None:
    """The rejection message must name the offending type, not the input content."""
    class _WeirdName:
        pass

    ent = {"type": "domain", "value": "example.com", "source": "x",
           "attributes": {"bad": _WeirdName()}}
    with pytest.raises(ValidationError) as exc:
        ObservedEntity.model_validate(ent)
    msg = str(exc.value)
    assert "_WeirdName" in msg


def test_security_non_string_key_message_names_the_problem() -> None:
    obs = _full_obs()
    obs["parsed"] = {1: "integer key"}
    with pytest.raises(ValidationError) as exc:
        Observation.model_validate(obs)
    errors = exc.value.errors()
    ctx_error = errors[0]["ctx"]["error"]
    assert str(ctx_error) == "JSON object keys must be strings"


def test_security_arbitrary_object_message_exact() -> None:
    """The rejection message for an arbitrary object is the exact contract text."""
    class _WeirdName:
        pass

    ent = {"type": "domain", "value": "example.com", "source": "x",
           "attributes": {"bad": _WeirdName()}}
    with pytest.raises(ValidationError) as exc:
        ObservedEntity.model_validate(ent)
    errors = exc.value.errors()
    ctx_error = errors[0]["ctx"]["error"]
    assert "value is not JSON-safe: _WeirdName" == str(ctx_error)


# ---------------------------------------------------------------------------
# Cross-cutting: length caps are exported config, not magic numbers
# ---------------------------------------------------------------------------
def test_length_caps_are_positive() -> None:
    assert SCHEMA_VERSION > 0
    assert MAX_STR_LEN > 0
    assert MAX_VALUE_LEN > 0
    assert MAX_URL_LEN > 0
    # An entity `value` is identity-bearing (drives canonical_id), so it must
    # be strictly tighter than a free-form string field.
    assert MAX_VALUE_LEN < MAX_STR_LEN
