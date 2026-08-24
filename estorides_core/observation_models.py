"""
estorides_core.observation_models
================================
Strict, versioned Pydantic v2 data contracts for the observation and entity
records that flow through the engine.

The engine historically modelled these as unvalidated ``Dict[str, Any]``
built inline in the orchestrator, so a missing field, a wrong-typed value, or
a hostile payload could be silently propagated into the fusion store, the
knowledge graph, or the LLM analyst. These models are the schema-contract
boundary: parsing a dict validates it up front, ``extra="forbid"`` makes
schema drift a loud, traceable failure, and ``to_legacy_dict()`` projects back
to the exact shape the current in-process call sites consume.

The module is pure (no I/O, no network, no clock reads, no logging of field
contents) and runs in the single-process architecture mandated by
``CLAUDE.md``: no Redis, no Celery, no FAISS, no OTLP collector.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import SCHEMA

__all__ = [
    "MAX_STR_LEN",
    "MAX_URL_LEN",
    "MAX_VALUE_LEN",
    "SCHEMA_VERSION",
    "Observation",
    "ObservationMeta",
    "ObservedEntity",
    "RunResult",
]

MAX_STR_LEN: int = SCHEMA.max_str_len
MAX_VALUE_LEN: int = SCHEMA.max_value_len
MAX_URL_LEN: int = SCHEMA.max_url_len
SCHEMA_VERSION: int = SCHEMA.schema_version


def _check_json_safe(value: Any) -> Any:
    """Return ``value`` if it is JSON-safe (None/bool/int/float/str/list/dict).

    Raises ``ValueError`` on ``set``, ``bytes``, and arbitrary objects so a
    hostile or structurally-invalid payload can never be retained in a
    validated record. Recurses into containers; dict keys must be strings.
    """
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, list):
        for item in value:
            _check_json_safe(item)
        return value
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("JSON object keys must be strings")
            _check_json_safe(item)
        return value
    raise ValueError(f"value is not JSON-safe: {type(value).__name__}")


class _StrictModel(BaseModel):
    """Base class: strict types, forbid unknown fields, no silent coercion."""

    model_config = ConfigDict(strict=True, extra="forbid")


class ObservationMeta(_StrictModel):
    """The ``meta`` sub-object of an observation (status, attempts, cache)."""

    url: str = Field(default="")
    method: str = Field(default="")
    host: str = Field(default="")
    attempts: int = Field(default=0, ge=0)
    cached: bool = False
    proxied: bool = False
    status: int = Field(default=0, ge=0)
    content_type: str = Field(default="")
    error: str = Field(default="")

    @field_validator("url")
    @classmethod
    def _bound_url(cls, value: str) -> str:
        return value[:MAX_URL_LEN]

    @field_validator("method")
    @classmethod
    def _upper_method(cls, value: str) -> str:
        return value.upper()

    def to_legacy_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "method": self.method,
            "host": self.host,
            "attempts": self.attempts,
            "cached": self.cached,
            "proxied": self.proxied,
            "status": self.status,
            "content_type": self.content_type,
            "error": self.error,
        }


class Observation(_StrictModel):
    """A validated per-source observation record emitted by the engine."""

    source: str = Field(min_length=1, max_length=MAX_STR_LEN)
    category: str = Field(default="", max_length=MAX_STR_LEN)
    description: str = Field(default="", max_length=MAX_STR_LEN)
    parser: str = Field(default="", max_length=MAX_STR_LEN)
    parsed: Any = None
    raw: Any = None
    meta: ObservationMeta
    observed_at: float = Field(default=0.0, ge=0.0)
    ontology: dict[str, Any] = Field(default_factory=dict)
    mitre: dict[str, Any] = Field(default_factory=dict)

    @field_validator("parsed", "raw", "ontology", "mitre")
    @classmethod
    def _json_safe(cls, value: Any) -> Any:
        return _check_json_safe(value)

    def to_legacy_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "source": self.source,
            "category": self.category,
            "description": self.description,
            "parser": self.parser,
            "parsed": self.parsed,
            "raw": self.raw,
            "meta": self.meta.to_legacy_dict(),
        }
        if self.observed_at:
            out["observed_at"] = self.observed_at
        if self.ontology:
            out["ontology"] = self.ontology
        if self.mitre:
            out["mitre"] = self.mitre
        return out


class ObservedEntity(_StrictModel):
    """A validated view of a resolved entity used across the stores."""

    type: str = Field(min_length=1, max_length=MAX_STR_LEN)
    value: str = Field(min_length=1, max_length=MAX_VALUE_LEN)
    source: str = Field(default="", max_length=MAX_STR_LEN)
    context: str = Field(default="", max_length=MAX_STR_LEN)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    attributes: dict[str, Any] = Field(default_factory=dict)
    sources: list[str] = Field(default_factory=list)

    @field_validator("attributes", "sources")
    @classmethod
    def _json_safe(cls, value: Any) -> Any:
        return _check_json_safe(value)

    def to_legacy_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "value": self.value,
            "source": self.source,
            "context": self.context,
            "confidence": self.confidence,
            "attributes": dict(self.attributes),
            "sources": list(self.sources),
        }


class RunResult(_StrictModel):
    """The top-level validated run payload."""

    entities: list[ObservedEntity] = Field(default_factory=list)
    observations: list[Observation] = Field(default_factory=list)
    sources_succeeded: int = Field(default=0, ge=0)
    error: str = Field(default="", max_length=MAX_STR_LEN)

    def to_legacy_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "entities": [e.to_legacy_dict() for e in self.entities],
            "observations": [o.to_legacy_dict() for o in self.observations],
            "sources_succeeded": self.sources_succeeded,
        }
        if self.error:
            out["error"] = self.error
        return out
