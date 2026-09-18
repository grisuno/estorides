"""M1 RED tests: query intent v2."""
from __future__ import annotations

from estorides_core.entity_extraction import detect_query_type, normalize_query


def test_phone() -> None:
    assert detect_query_type("+1 (415) 555-0132") == "phone"
    assert detect_query_type("+34 612 345 678") == "phone"


def test_mac() -> None:
    assert detect_query_type("AA:BB:CC:DD:EE:FF") == "mac"
    assert detect_query_type("aa-bb-cc-dd-ee-ff") == "mac"


def test_at_handle() -> None:
    assert detect_query_type("@octocat") == "username"
    assert normalize_query("@octocat") == "octocat"


def test_url_normalises_to_host() -> None:
    assert detect_query_type("https://Example.COM:443/a?b=c") == "url"
    assert normalize_query("https://Example.COM:443/a?b=c") == "example.com"


def test_btc_uppercase_bech32() -> None:
    assert detect_query_type("BC1QW508D6QEJXTDG4Y5R3ZARVARY0C5XW7KV8F3T4") == "btc_address"


def test_backward_compat() -> None:
    assert detect_query_type("putin") == "username"
    assert detect_query_type("1.2.3.4") == "ipv4"
    assert detect_query_type("a@b.com") == "email"
    assert detect_query_type("CVE-2021-44228") == "cve"
    assert detect_query_type("example.com") == "domain"
    assert detect_query_type("") == "empty"
    assert normalize_query("  example.com  ") == "example.com"
