from __future__ import annotations

import hashlib
import logging
import re
import time
from typing import Any

log = logging.getLogger("estorides.target_mgmt")


MAX_BATCH_SIZE = 200
MAX_VALUE_LENGTH = 2048
MAX_LABEL_LENGTH = 256

VALID_TYPES = frozenset({
    "domain", "ipv4", "ipv6", "email", "username", "cve",
    "btc_address", "eth_address", "asn", "md5", "sha1", "sha256",
    "url", "phone", "person", "company",
})

_IPV4_RE = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.)"
    r"{3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)
_IPV6_RE = re.compile(
    r"^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$"
    r"|^(?:[0-9a-fA-F]{1,4}:){1,7}:$"
    r"|^(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$"
    r"|^(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}$"
    r"|^(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}$"
    r"|^(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}$"
    r"|^(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}$"
    r"|^[0-9a-fA-F]{1,4}:(?::[0-9a-fA-F]{1,4}){1,6}$"
    r"|^::(?:[0-9a-fA-F]{1,4}:){0,6}[0-9a-fA-F]{1,4}$"
    r"|^::$"
)
_DOMAIN_RE = re.compile(
    r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)
_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_CVE_RE = re.compile(r"^CVE-\d{4}-\d{4,}$")
_BTC_RE = re.compile(r"^(1|3|bc1)[a-km-zA-HJ-NP-Z1-9]{25,71}$")
_ETH_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
_PHONE_RE = re.compile(r"^\+\d{6,15}$")
_ASN_RE = re.compile(r"^AS\d{1,10}$")
_MD5_RE = re.compile(r"^[a-fA-F0-9]{32}$")
_SHA1_RE = re.compile(r"^[a-fA-F0-9]{40}$")
_SHA256_RE = re.compile(r"^[a-fA-F0-9]{64}$")

_AUTO_DETECT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ipv4", _IPV4_RE),
    ("ipv6", _IPV6_RE),
    ("email", _EMAIL_RE),
    ("cve", _CVE_RE),
    ("btc_address", _BTC_RE),
    ("eth_address", _ETH_RE),
    ("phone", _PHONE_RE),
    ("asn", _ASN_RE),
    ("md5", _MD5_RE),
    ("sha1", _SHA1_RE),
    ("sha256", _SHA256_RE),
    ("url", re.compile(r"^https?://")),
    ("domain", _DOMAIN_RE),
]


def auto_detect_type(value: str) -> str:
    for etype, pattern in _AUTO_DETECT_PATTERNS:
        if pattern.search(value):
            return etype
    return "username"


def _type_validator(etype: str) -> re.Pattern[str] | None:
    mapping: dict[str, re.Pattern[str]] = {
        "domain": _DOMAIN_RE,
        "ipv4": _IPV4_RE,
        "ipv6": _IPV6_RE,
        "email": _EMAIL_RE,
        "cve": _CVE_RE,
        "btc_address": _BTC_RE,
        "eth_address": _ETH_RE,
        "phone": _PHONE_RE,
        "asn": _ASN_RE,
        "md5": _MD5_RE,
        "sha1": _SHA1_RE,
        "sha256": _SHA256_RE,
        "url": re.compile(r"^https?://"),
    }
    return mapping.get(etype)


def validate_type(etype: str) -> list[str]:
    errors: list[str] = []
    if etype not in VALID_TYPES and etype != "auto":
        valid_list = ", ".join(sorted(VALID_TYPES))
        errors.append(f"invalid type '{etype}'; valid types: {valid_list}")
    return errors


def validate_value(etype: str, value: str) -> list[str]:
    errors: list[str] = []
    if not value or not value.strip():
        errors.append("value must be non-empty")
        return errors
    if len(value) > MAX_VALUE_LENGTH:
        errors.append(f"value exceeds {MAX_VALUE_LENGTH} characters")
        return errors
    validator = _type_validator(etype)
    if validator is not None and not validator.match(value):
        errors.append(f"invalid {etype} value: '{value}'")
    return errors


def validate_target(etype: str, value: str) -> tuple[list[str], str]:
    type_errors = validate_type(etype)
    if type_errors:
        return type_errors, etype
    resolved_type = etype
    if etype == "auto":
        resolved_type = auto_detect_type(value.strip())
    value_errors = validate_value(resolved_type, value.strip())
    return value_errors, resolved_type


def make_target_id(etype: str, value: str) -> str:
    raw = f"{etype}:{value.strip().lower()}"
    return hashlib.sha1(raw.encode("utf-8"), usedforsecurity=False).hexdigest()[:16]


class TargetResult:
    __slots__ = ("case_id", "created_at", "id", "label", "type",
                 "valid", "validation_errors", "value")

    def __init__(
        self,
        *,
        target_id: str,
        etype: str,
        value: str,
        label: str = "",
        valid: bool = True,
        validation_errors: list[str] | None = None,
        case_id: str | None = None,
        created_at: float | None = None,
    ) -> None:
        self.id = target_id
        self.type = etype
        self.value = value
        self.label = label
        self.valid = valid
        self.validation_errors = validation_errors or []
        self.case_id = case_id
        self.created_at = created_at or time.time()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "value": self.value,
            "label": self.label,
            "valid": self.valid,
            "validation_errors": self.validation_errors[:],
            "case_id": self.case_id,
            "created_at": self.created_at,
        }


class BatchResult:
    __slots__ = ("errors", "invalid", "targets", "total", "valid")

    def __init__(self) -> None:
        self.total = 0
        self.valid = 0
        self.invalid = 0
        self.errors: list[dict[str, Any]] = []
        self.targets: list[TargetResult] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "valid": self.valid,
            "invalid": self.invalid,
            "errors": self.errors[:],
            "targets": [t.to_dict() for t in self.targets],
        }


class TargetManager:

    def __init__(
        self,
        fusion_store: Any = None,
        case_store: Any = None,
        entity_store: Any = None,
    ) -> None:
        self._fusion_store = fusion_store
        self._case_store = case_store
        self._entity_store = entity_store

    def add_target(
        self,
        etype: str,
        value: str,
        label: str = "",
        case_id: str | None = None,
    ) -> TargetResult:
        if not value or not value.strip():
            raise ValueError("value must be non-empty")
        value = value.strip()
        if len(value) > MAX_VALUE_LENGTH:
            raise ValueError(f"value exceeds {MAX_VALUE_LENGTH} characters")

        val_errors, resolved_type = validate_target(etype, value)
        if val_errors:
            target_id = make_target_id(resolved_type, value) if resolved_type in VALID_TYPES else "unknown"
            return TargetResult(
                target_id=target_id,
                etype=resolved_type,
                value=value,
                label=label,
                valid=False,
                validation_errors=val_errors,
                case_id=case_id,
            )

        if label and len(label) > MAX_LABEL_LENGTH:
            label = label[:MAX_LABEL_LENGTH]

        target_id = make_target_id(resolved_type, value)
        created_at = time.time()

        final_case_id: str | None = case_id
        if self._case_store is not None:
            if case_id:
                try:
                    self._case_store.add_observation(case_id, {
                        "source": "target_management",
                        "category": "manual",
                        "parser": "target_management",
                        "parsed": {
                            "entities": [{"type": resolved_type, "value": value, "label": label}],
                        },
                    })
                except Exception:
                    log.exception("case_store.add_observation failed, proceeding without case")
                    final_case_id = None
            else:
                try:
                    final_case_id = self._case_store.create_case(
                        query=value, query_type=resolved_type,
                        notes=f"Target: {label}" if label else "",
                    )
                    self._case_store.add_observation(final_case_id, {
                        "source": "target_management",
                        "category": "manual",
                        "parser": "target_management",
                        "parsed": {
                            "entities": [{"type": resolved_type, "value": value, "label": label}],
                        },
                    })
                except Exception:
                    log.exception("case_store.create_case failed, proceeding without case")
                    final_case_id = None

        if self._fusion_store is not None:
            try:
                self._fusion_store.add_observation(
                    {
                        "source": "target_management",
                        "category": "manual",
                        "parser": "target_management",
                        "parsed": {
                            "entities": [{"type": resolved_type, "value": value, "label": label}],
                        },
                        "meta": {"status": "ok", "manual": True},
                    },
                    case_id=final_case_id,
                )
            except Exception:
                log.exception("fusion_store.add_observation failed")

        if self._entity_store is not None and resolved_type in VALID_TYPES:
            try:
                from .entity_resolution import CanonicalEntity, normalize_value
                normalized = normalize_value(resolved_type, value)
                entity = CanonicalEntity(
                    canonical_id=target_id,
                    type=resolved_type,
                    value=value,
                    normalized=normalized,
                    confidence=1.0,
                    member_count=1,
                    sources=[],
                    aliases=[],
                )
                self._entity_store.upsert(entity)
            except Exception:
                log.exception("entity_store.upsert failed")

        return TargetResult(
            target_id=target_id,
            etype=resolved_type,
            value=value,
            label=label,
            valid=True,
            case_id=final_case_id,
            created_at=created_at,
        )

    def batch_import(self, text: str) -> BatchResult:
        lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
        if len(lines) > MAX_BATCH_SIZE:
            raise ValueError(f"batch exceeds max size of {MAX_BATCH_SIZE}")

        result = BatchResult()
        result.total = len(lines)

        for line_no, raw_line in enumerate(lines, 1):
            if ":" in raw_line:
                parts = raw_line.split(":", 1)
                raw_type = parts[0].strip()
                raw_value = parts[1].strip()
            else:
                raw_type = "auto"
                raw_value = raw_line

            if not raw_value:
                result.invalid += 1
                result.errors.append({"line": line_no, "reason": "empty value"})
                continue

            try:
                tr = self.add_target(raw_type, raw_value)
                if tr.valid:
                    result.valid += 1
                else:
                    result.invalid += 1
                    result.errors.append({
                        "line": line_no,
                        "reason": "; ".join(tr.validation_errors),
                    })
                result.targets.append(tr)
            except (ValueError, Exception) as exc:
                result.invalid += 1
                result.errors.append({"line": line_no, "reason": str(exc)})

        return result

    def csv_parse(self, csv_text: str) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        for line in csv_text.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 2:
                rows.append({
                    "type": parts[0], "value": parts[1],
                    "label": parts[2] if len(parts) > 2 else "",
                })
        return rows

    def batch_csv_import(self, csv_text: str) -> BatchResult:
        rows = self.csv_parse(csv_text)
        if len(rows) > MAX_BATCH_SIZE:
            raise ValueError(f"batch exceeds max size of {MAX_BATCH_SIZE}")

        result = BatchResult()
        result.total = len(rows)

        for row_no, row in enumerate(rows, 1):
            if not row.get("value"):
                result.invalid += 1
                result.errors.append({"line": row_no, "reason": "empty value"})
                continue
            try:
                tr = self.add_target(row["type"], row["value"], label=row.get("label", ""))
                if tr.valid:
                    result.valid += 1
                else:
                    result.invalid += 1
                    result.errors.append({
                        "line": row_no,
                        "reason": "; ".join(tr.validation_errors),
                    })
                result.targets.append(tr)
            except (ValueError, Exception) as exc:
                result.invalid += 1
                result.errors.append({"line": row_no, "reason": str(exc)})

        return result
