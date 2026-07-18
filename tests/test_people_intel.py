"""ATDD + BDD tests for estorides_core.people_intel.

Implements the Given-When-Then contracts declared in
``spec/people_intel.md``.
"""
from __future__ import annotations

import pytest

from estorides_core.people_intel import (
    BreachRecord,
    Employee,
    analyse_employees,
    infer_email_pattern,
)


def _make_emp(name: str, role: str, email: str) -> Employee:
    return Employee(
        name=name, role=role,
        emails=[email], phone=None,
        linkedin=None, twitter=None, github=None,
        sources=["hunter_test"], breaches=[],
    )


# S1 — Happy path: Employee discovery
class TestHappyPathEmployeeDiscovery:
    def test_returns_employees_from_domain(self) -> None:
        employees = [
            _make_emp("Alice Smith", "Engineer", "alice.smith@example.com"),
            _make_emp("Bob Jones", "Manager", "bob.jones@example.com"),
            _make_emp("Charlie Brown", "DevOps", "charlie.brown@example.com"),
        ]
        result = analyse_employees(employees, "example.com")
        assert len(result.employees) == 3
        assert result.email_pattern == "{first}.{last}@example.com"
        assert result.email_pattern_confidence >= 0.6


# S2 — Edge: No employees
class TestNoEmployees:
    def test_empty_when_no_employees(self) -> None:
        result = analyse_employees([], "unknown.org")
        assert len(result.employees) == 0
        assert result.risk_score == 0.0


# S3 — Error: Invalid domain
class TestInvalidDomain:
    def test_rejects_invalid_domain(self) -> None:
        with pytest.raises(ValueError, match="INVALID_DOMAIN"):
            analyse_employees([], "not-a-domain!")


# S4 — Security: Breach password exposure
class TestBreachPasswordContext:
    def test_breach_with_password_is_critical(self) -> None:
        emp = Employee(
            name="John Doe", role="Engineer",
            emails=["john@example.com"], phone=None,
            linkedin=None, twitter=None, github=None,
            sources=["hunter"],
            breaches=[
                BreachRecord(
                    breach_name="LinkedIn 2021",
                    email="john@example.com",
                    password="hash123",
                    data_classes=["Email", "Password"],
                    severity="critical",
                )
            ],
        )
        result = analyse_employees([emp], "example.com")
        ctx = result.breaches[0]
        assert ctx.passwords_exposed is True
        assert ctx.severity == "critical"


# S5 — Happy path: Email pattern inference
class TestEmailPatternInference:
    def test_infers_first_dot_last_pattern(self) -> None:
        pattern, conf = infer_email_pattern([
            "alice@example.com",
            "bob@example.com",
            "charlie@example.com",
        ])
        assert pattern == "{first}@{domain}"
        assert conf >= 0.6

    def test_infers_firstinitial_last_pattern(self) -> None:
        _, conf = infer_email_pattern([
            "jsmith@example.com",
            "jdoe@example.com",
            "bbrown@example.com",
        ])
        assert conf >= 0.6


# S6 — Edge: Single email ambiguous
class TestSingleEmailAmbiguous:
    def test_single_email_low_confidence(self) -> None:
        _, conf = infer_email_pattern(["jsmith@example.com"])
        assert conf < 0.5


# S7 — Happy path: Cross-breach correlation
class TestCrossBreachCorrelation:
    def test_multiple_breaches_increase_risk(self) -> None:
        emp = Employee(
            name="Jane Doe", role="Engineer",
            emails=["jane@example.com"], phone=None,
            linkedin=None, twitter=None, github=None,
            sources=["hunter"],
            breaches=[
                BreachRecord("Breach1", "jane@example.com", None, ["Email"], "high"),
                BreachRecord("Breach2", "jane@example.com", "pwdhash", ["Email", "Password"], "critical"),
                BreachRecord("Breach3", "jane@example.com", None, ["Email", "Name"], "medium"),
            ],
        )
        result = analyse_employees([emp], "example.com")
        ctx = next(c for c in result.breaches if c.email == "jane@example.com")
        assert ctx.total_breaches == 3
        assert ctx.passwords_exposed is True


# S8 — Security: No raw passwords in serialised output
class TestNoRawPasswords:
    def test_passwords_not_in_serialised_output(self) -> None:
        emp = Employee(
            name="Hacker", role="Engineer",
            emails=["hacker@example.com"], phone=None,
            linkedin=None, twitter=None, github=None,
            sources=["test"],
            breaches=[
                BreachRecord("Test", "hacker@example.com", "plaintext_pwd", ["Email", "Password"], "critical"),
            ],
        )
        result = analyse_employees([emp], "example.com")
        serialised = str(result.to_dict())
        assert "plaintext_pwd" not in serialised
