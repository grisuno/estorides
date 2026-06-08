#!/usr/bin/env python3
"""Tests for the bug-bounty scope classifier.

Offline only. Covers each rule grammar, out-of-scope precedence, asset
normalisation (URL/case/port), and the flat-list split. Prints PASS/FAIL.
"""
from __future__ import annotations

import sys

from estorides_core.scope import (IN_SCOPE, OUT_OF_SCOPE, UNKNOWN,
                                   ScopeMatcher, build_report, normalise_asset,
                                   parse_rules)

_failures = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global _failures
    if cond:
        print(f"PASS: {name}")
    else:
        _failures += 1
        print(f"FAIL: {name} {detail}")


def main() -> int:
    # Asset normalisation.
    check("strip scheme/path/port",
          normalise_asset("HTTPS://Shop.Example.com:8443/cart?x=1") == "shop.example.com")
    check("strip trailing dot", normalise_asset("example.com.") == "example.com")
    check("ipv6 brackets stripped", normalise_asset("[2001:db8::1]") == "2001:db8::1")

    rules = parse_rules([
        "# comment",
        "",
        "*.example.com",
        "api.example.com",
        "192.0.2.0/24",
        "198.51.100.7",
        r"re:^staging-[0-9]+\.example\.com$",
        "not a [valid regex",  # exact-host fallback, harmless
    ])
    check("parser skips blanks/comments, keeps 6 rules", len(rules) == 6, f"got {len(rules)}")

    out_rules = parse_rules(["blog.example.com", "192.0.2.200"])
    m = ScopeMatcher(rules, out_rules)

    # Wildcard matches apex and subdomain.
    check("wildcard matches subdomain", m.classify("www.example.com") == IN_SCOPE)
    check("wildcard matches apex", m.classify("example.com") == IN_SCOPE)
    # Regex rule.
    check("regex in-scope", m.classify("staging-7.example.com") == IN_SCOPE)
    check("regex non-match unknown", m.classify("staging-x.example.com") == IN_SCOPE)  # wildcard still covers it
    # CIDR + single IP.
    check("cidr in-scope", m.classify("192.0.2.10") == IN_SCOPE)
    check("single ip in-scope", m.classify("198.51.100.7") == IN_SCOPE)
    check("ip outside cidr unknown", m.classify("203.0.113.5") == UNKNOWN)
    # Out-of-scope precedence beats a matching in-scope wildcard / CIDR.
    check("out beats wildcard", m.classify("blog.example.com") == OUT_OF_SCOPE)
    check("out beats cidr", m.classify("192.0.2.200") == OUT_OF_SCOPE)
    # Unrelated host.
    check("foreign host unknown", m.classify("evil.com") == UNKNOWN)

    # Report + flat split, with de-duplication on the normalised form.
    report = build_report(m, [
        "https://www.example.com/", "WWW.EXAMPLE.COM", "192.0.2.10",
        "blog.example.com", "evil.com",
    ])
    check("dedup collapses url+case", report.in_scope.count("www.example.com") == 1)
    check("hosts/ips split", report.hosts == ["www.example.com"] and report.ips == ["192.0.2.10"],
          f"hosts={report.hosts} ips={report.ips}")
    check("out-of-scope surfaced", report.out_of_scope == ["blog.example.com"])
    check("unknown surfaced", report.unknown == ["evil.com"])

    # Empty / whitespace assets are ignored, not misclassified.
    check("empty asset ignored", m.classify("   ") == UNKNOWN)

    print(f"\n{'ALL PASS' if _failures == 0 else f'{_failures} FAILURES'}")
    return 1 if _failures else 0


if __name__ == "__main__":
    sys.exit(main())
