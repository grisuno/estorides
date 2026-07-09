from __future__ import annotations

import pytest

from estorides_core.target_management import (
    MAX_BATCH_SIZE,
    VALID_TYPES,
    TargetManager,
    TargetResult,
    auto_detect_type,
    make_target_id,
    validate_target,
    validate_type,
    validate_value,
)

# ---------------------------------------------------------------------------
# S1 -- Happy path: single target created
# ---------------------------------------------------------------------------

class TestS1HappyPath:
    def test_valid_target_returns_result(self) -> None:
        tm = TargetManager()
        tr = tm.add_target("domain", "evilcorp.com")
        assert tr.valid is True
        assert len(tr.id) == 16
        assert tr.type == "domain"
        assert tr.value == "evilcorp.com"

    def test_has_case_id(self) -> None:
        tm = TargetManager()
        tr = tm.add_target("ipv4", "8.8.8.8")
        assert tr.case_id is None  # no case_store injected

    def test_id_deterministic(self) -> None:
        tm = TargetManager()
        a = tm.add_target("domain", "evilcorp.com")
        b = tm.add_target("domain", "evilcorp.com")
        assert a.id == b.id


# ---------------------------------------------------------------------------
# S2 -- Edge: type auto-detected from value
# ---------------------------------------------------------------------------

class TestS2AutoDetect:
    def test_ipv4_auto(self) -> None:
        tr = TargetManager().add_target("auto", "8.8.8.8")
        assert tr.type == "ipv4"
        assert tr.valid is True

    def test_ipv6_auto(self) -> None:
        tr = TargetManager().add_target("auto", "2001:db8::1")
        assert tr.type == "ipv6"
        assert tr.valid is True

    def test_email_auto(self) -> None:
        tr = TargetManager().add_target("auto", "user@example.com")
        assert tr.type == "email"
        assert tr.valid is True

    def test_cve_auto(self) -> None:
        tr = TargetManager().add_target("auto", "CVE-2024-12345")
        assert tr.type == "cve"
        assert tr.valid is True

    def test_btc_auto(self) -> None:
        tr = TargetManager().add_target("auto", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        assert tr.type == "btc_address"
        assert tr.valid is True

    def test_eth_auto(self) -> None:
        tr = TargetManager().add_target("auto", "0x1234567890abcdef1234567890abcdef12345678")
        assert tr.type == "eth_address"
        assert tr.valid is True

    def test_domain_auto(self) -> None:
        tr = TargetManager().add_target("auto", "example.com")
        assert tr.type == "domain"
        assert tr.valid is True

    def test_username_fallback(self) -> None:
        tr = TargetManager().add_target("auto", "some_random_guy")
        assert tr.type == "username"
        assert tr.valid is True

    def test_phone_auto(self) -> None:
        tr = TargetManager().add_target("auto", "+15551234567")
        assert tr.type == "phone"
        assert tr.valid is True

    def test_asn_auto(self) -> None:
        tr = TargetManager().add_target("auto", "AS12345")
        assert tr.type == "asn"
        assert tr.valid is True

    def test_md5_auto(self) -> None:
        tr = TargetManager().add_target("auto", "d41d8cd98f00b204e9800998ecf8427e")
        assert tr.type == "md5"
        assert tr.valid is True

    def test_sha256_auto(self) -> None:
        h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        tr = TargetManager().add_target("auto", h)
        assert tr.type == "sha256"
        assert tr.valid is True


# ---------------------------------------------------------------------------
# S3 -- Edge: invalid value by type
# ---------------------------------------------------------------------------

class TestS3InvalidValue:
    def test_invalid_email(self) -> None:
        tr = TargetManager().add_target("email", "not-an-email")
        assert tr.valid is False
        assert len(tr.validation_errors) > 0

    def test_invalid_ipv4(self) -> None:
        tr = TargetManager().add_target("ipv4", "999.999.999.999")
        assert tr.valid is False

    def test_invalid_domain_script(self) -> None:
        tr = TargetManager().add_target("domain", "<script>alert(1)</script>")
        assert tr.valid is False

    def test_invalid_url(self) -> None:
        tr = TargetManager().add_target("url", "ftp://evil.com")
        assert tr.valid is False

    def test_invalid_phone(self) -> None:
        tr = TargetManager().add_target("phone", "12345")
        assert tr.valid is False


# ---------------------------------------------------------------------------
# S4 -- Edge: unknown type
# ---------------------------------------------------------------------------

class TestS4UnknownType:
    def test_unknown_type(self) -> None:
        errors, _ = validate_target("alien_artifact", "x")
        assert len(errors) > 0
        assert "invalid type" in errors[0]

    def test_unknown_type_via_manager(self) -> None:
        tr = TargetManager().add_target("alien_artifact", "x")
        assert tr.valid is False
        assert len(tr.validation_errors) > 0


# ---------------------------------------------------------------------------
# S5 -- Error: empty value
# ---------------------------------------------------------------------------

class TestS5EmptyValue:
    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must be non-empty"):
            TargetManager().add_target("domain", "")

    def test_whitespace_raises(self) -> None:
        with pytest.raises(ValueError, match="must be non-empty"):
            TargetManager().add_target("domain", "   ")

    def test_validate_value_empty(self) -> None:
        errors = validate_value("domain", "")
        assert len(errors) > 0


# ---------------------------------------------------------------------------
# S6 -- Error: case store unavailable (ephemeral mode)
# ---------------------------------------------------------------------------

class TestS6CaseStoreUnavailable:
    def test_ephemeral_no_case_store(self) -> None:
        tm = TargetManager(case_store=None)
        tr = tm.add_target("domain", "test.com")
        assert tr.case_id is None
        assert tr.valid is True


# ---------------------------------------------------------------------------
# S7 -- Batch: 3 valid + 1 invalid
# ---------------------------------------------------------------------------

class TestS7Batch:
    def test_mixed_batch(self) -> None:
        text = (
            "domain:evilcorp.com\n"
            "ipv4:8.8.8.8\n"
            "email:user@example.com\n"
            "email:not-an-email\n"
        )
        result = TargetManager().batch_import(text)
        assert result.total == 4
        assert result.valid == 3
        assert result.invalid == 1
        assert all(t.valid for t in result.targets[:3])
        assert not result.targets[3].valid

    def test_simple_lines_no_type(self) -> None:
        result = TargetManager().batch_import("8.8.8.8\nexample.com")
        assert result.total == 2
        assert result.valid == 2


# ---------------------------------------------------------------------------
# S8 -- Security: max batch size enforced
# ---------------------------------------------------------------------------

class TestS8MaxBatch:
    def test_exceeds_max(self) -> None:
        lines = "\n".join(f"domain:test{i}.com" for i in range(MAX_BATCH_SIZE + 1))
        with pytest.raises(ValueError, match="batch exceeds max size"):
            TargetManager().batch_import(lines)

    def test_at_max(self) -> None:
        lines = "\n".join(f"domain:test{i}.com" for i in range(MAX_BATCH_SIZE))
        result = TargetManager().batch_import(lines)
        assert result.total == MAX_BATCH_SIZE
        assert result.valid == MAX_BATCH_SIZE


# ---------------------------------------------------------------------------
# S9 -- Security: XSS attempt in value is rejected
# ---------------------------------------------------------------------------

class TestS9XSS:
    def test_script_in_domain_rejected(self) -> None:
        tr = TargetManager().add_target("domain", "<script>alert(1)</script>")
        assert tr.valid is False

    def test_onclick_in_domain_rejected(self) -> None:
        tr = TargetManager().add_target("domain", "onclick=alert(1)")
        assert tr.valid is False

    def test_sql_injection_in_email_rejected(self) -> None:
        tr = TargetManager().add_target("email", "'; DROP TABLE targets;--@x.com")
        assert tr.valid is False


# ---------------------------------------------------------------------------
# S10 -- Determinism: same input same output
# ---------------------------------------------------------------------------

class TestS10Determinism:
    def test_same_id(self) -> None:
        tm = TargetManager()
        a = tm.add_target("domain", "test.com")
        b = tm.add_target("domain", "test.com")
        assert a.id == b.id
        assert a.type == b.type
        assert a.value == b.value

    def test_same_id_normalised(self) -> None:
        tm = TargetManager()
        a = tm.add_target("domain", "Test.COM")
        b = tm.add_target("domain", "test.com")
        assert a.id == b.id


# ---------------------------------------------------------------------------
# Pure validation unit tests
# ---------------------------------------------------------------------------

class TestValidateType:
    def test_valid_types_pass(self) -> None:
        for t in VALID_TYPES:
            errors = validate_type(t)
            assert errors == [], f"type {t} should be valid"

    def test_auto_passes(self) -> None:
        assert validate_type("auto") == []

    def test_invalid_fails(self) -> None:
        errors = validate_type("nope")
        assert len(errors) == 1


class TestValidateValue:
    def test_domain_valid(self) -> None:
        errors = validate_value("domain", "example.com")
        assert errors == []

    def test_domain_invalid(self) -> None:
        errors = validate_value("domain", "-bad-.com")
        assert len(errors) > 0

    def test_ipv4_valid(self) -> None:
        errors = validate_value("ipv4", "192.168.1.1")
        assert errors == []

    def test_ipv4_invalid_octet(self) -> None:
        errors = validate_value("ipv4", "192.168.1.300")
        assert len(errors) > 0

    def test_email_valid(self) -> None:
        errors = validate_value("email", "a@b.co")
        assert errors == []

    def test_url_only_http_https(self) -> None:
        assert validate_value("url", "https://x.com") == []
        assert validate_value("url", "http://x.com") == []
        assert len(validate_value("url", "ftp://x.com")) > 0

    def test_username_no_regex(self) -> None:
        errors = validate_value("username", "  some user  ")
        assert errors == []  # only trimmed, no regex

    def test_cve_valid(self) -> None:
        assert validate_value("cve", "CVE-2024-12345") == []

    def test_btc_valid(self) -> None:
        assert validate_value("btc_address", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa") == []

    def test_eth_valid(self) -> None:
        assert validate_value("eth_address", "0x1234567890abcdef1234567890abcdef12345678") == []

    def test_phone_valid(self) -> None:
        assert validate_value("phone", "+15551234567") == []

    def test_asn_valid(self) -> None:
        assert validate_value("asn", "AS12345") == []

    def test_md5_valid(self) -> None:
        assert validate_value("md5", "d41d8cd98f00b204e9800998ecf8427e") == []

    def test_sha256_valid(self) -> None:
        h = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        assert validate_value("sha256", h) == []


class TestMakeTargetId:
    def test_length(self) -> None:
        assert len(make_target_id("domain", "example.com")) == 16

    def test_deterministic(self) -> None:
        assert make_target_id("ipv4", "8.8.8.8") == make_target_id("ipv4", "8.8.8.8")

    def test_case_sensitive_normalised(self) -> None:
        assert make_target_id("domain", "Example.COM") == make_target_id("domain", "example.com")


class TestAutoDetectType:
    def test_ipv4(self) -> None:
        assert auto_detect_type("8.8.8.8") == "ipv4"

    def test_ipv6(self) -> None:
        assert auto_detect_type("2001:db8::1") == "ipv6"

    def test_email(self) -> None:
        assert auto_detect_type("a@b.com") == "email"

    def test_domain(self) -> None:
        assert auto_detect_type("example.com") == "domain"

    def test_url(self) -> None:
        assert auto_detect_type("https://evil.com") == "url"

    def test_cve(self) -> None:
        assert auto_detect_type("CVE-2024-12345") == "cve"

    def test_username_fallback(self) -> None:
        assert auto_detect_type("some_user_123") == "username"


class TestBatchResultSerialization:
    def test_to_dict(self) -> None:
        from estorides_core.target_management import BatchResult
        br = BatchResult()
        d = br.to_dict()
        assert d["total"] == 0
        assert d["valid"] == 0
        assert d["invalid"] == 0
        assert d["errors"] == []
        assert d["targets"] == []


class TestTargetResultSerialization:
    def test_to_dict(self) -> None:
        tr = TargetResult(
            target_id="abc123",
            etype="domain",
            value="x.com",
            valid=True,
        )
        d = tr.to_dict()
        assert d["id"] == "abc123"
        assert d["type"] == "domain"
        assert d["value"] == "x.com"
        assert d["valid"] is True
        assert "label" in d
        assert "validation_errors" in d
        assert "case_id" in d
        assert "created_at" in d

    def test_to_dict_invalid(self) -> None:
        tr = TargetResult(
            target_id="bad",
            etype="domain",
            value="<script>",
            valid=False,
            validation_errors=["invalid domain"],
        )
        d = tr.to_dict()
        assert d["valid"] is False
        assert d["validation_errors"] == ["invalid domain"]


class TestCsvImport:
    def test_basic_csv(self) -> None:
        csv = "domain,evilcorp.com,Primary\nipv4,8.8.8.8,DNS\n"
        result = TargetManager().batch_csv_import(csv)
        assert result.total == 2
        assert result.valid == 2
        assert result.targets[0].label == "Primary"

    def test_csv_invalid(self) -> None:
        csv = "email,not-an-email\n"
        result = TargetManager().batch_csv_import(csv)
        assert result.total == 1
        assert result.valid == 0
        assert result.invalid == 1

    def test_csv_max_batch(self) -> None:
        rows = "\n".join(f"domain,test{i}.com" for i in range(MAX_BATCH_SIZE))
        result = TargetManager().batch_csv_import(rows)
        assert result.total == MAX_BATCH_SIZE
        assert result.valid == MAX_BATCH_SIZE

    def test_csv_exceeds_max(self) -> None:
        rows = "\n".join(f"domain,test{i}.com" for i in range(MAX_BATCH_SIZE + 1))
        with pytest.raises(ValueError, match="batch exceeds max size"):
            TargetManager().batch_csv_import(rows)
