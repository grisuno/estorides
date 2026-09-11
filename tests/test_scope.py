"""
BDD tests for the bug-bounty scope classifier (`estorides_core.scope`).

Ported from the standalone ``_test_scope.py`` validator into the pytest
suite so CI actually runs it.
"""
from __future__ import annotations

from estorides_core.scope import (
    IN_SCOPE,
    OUT_OF_SCOPE,
    UNKNOWN,
    ScopeMatcher,
    build_report,
    normalise_asset,
    parse_rules,
)

RULES = parse_rules([
    "# comment",
    "",
    "*.example.com",
    "api.example.com",
    "192.0.2.0/24",
    "198.51.100.7",
    r"re:^staging-[0-9]+\.example\.com$",
    "not a [valid regex",
])
OUT_RULES = parse_rules(["blog.example.com", "192.0.2.200"])


class TestNormaliseAsset:
    def test_strip_scheme_path_port(self) -> None:
        assert normalise_asset("HTTPS://Shop.Example.com:8443/cart?x=1") == "shop.example.com"

    def test_strip_trailing_dot(self) -> None:
        assert normalise_asset("example.com.") == "example.com"

    def test_ipv6_brackets_stripped(self) -> None:
        assert normalise_asset("[2001:db8::1]") == "2001:db8::1"


class TestParseRules:
    def test_skips_blanks_and_comments(self) -> None:
        assert len(RULES) == 6


class TestClassify:
    def test_wildcard_matches_subdomain_and_apex(self) -> None:
        m = ScopeMatcher(RULES, OUT_RULES)
        assert m.classify("www.example.com") == IN_SCOPE
        assert m.classify("example.com") == IN_SCOPE

    def test_regex_rule(self) -> None:
        m = ScopeMatcher(RULES, OUT_RULES)
        assert m.classify("staging-7.example.com") == IN_SCOPE
        assert m.classify("staging-x.example.com") == IN_SCOPE

    def test_cidr_and_single_ip(self) -> None:
        m = ScopeMatcher(RULES, OUT_RULES)
        assert m.classify("192.0.2.10") == IN_SCOPE
        assert m.classify("198.51.100.7") == IN_SCOPE
        assert m.classify("203.0.113.5") == UNKNOWN

    def test_out_of_scope_precedence(self) -> None:
        m = ScopeMatcher(RULES, OUT_RULES)
        assert m.classify("blog.example.com") == OUT_OF_SCOPE
        assert m.classify("192.0.2.200") == OUT_OF_SCOPE

    def test_foreign_host_unknown(self) -> None:
        m = ScopeMatcher(RULES, OUT_RULES)
        assert m.classify("evil.com") == UNKNOWN

    def test_empty_asset_unknown(self) -> None:
        m = ScopeMatcher(RULES, OUT_RULES)
        assert m.classify("   ") == UNKNOWN


class TestBuildReport:
    def test_dedup_hosts_ips_and_buckets(self) -> None:
        m = ScopeMatcher(RULES, OUT_RULES)
        report = build_report(m, [
            "https://www.example.com/", "WWW.EXAMPLE.COM", "192.0.2.10",
            "blog.example.com", "evil.com",
        ])
        assert report.in_scope.count("www.example.com") == 1
        assert report.hosts == ["www.example.com"]
        assert report.ips == ["192.0.2.10"]
        assert report.out_of_scope == ["blog.example.com"]
        assert report.unknown == ["evil.com"]
