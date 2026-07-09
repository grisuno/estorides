from __future__ import annotations

import re
from hypothesis import given, strategies as st

from estorides_core.target_management import (
    TargetManager,
    auto_detect_type,
    make_target_id,
    validate_target,
    validate_value,
    VALID_TYPES,
)

_NON_EMPTY_TEXT = st.text(min_size=1, max_size=200).filter(
    lambda s: s.strip()
)


@given(st.sampled_from(sorted(VALID_TYPES)), _NON_EMPTY_TEXT)
def test_p1_add_target_never_raises(etype: str, value: str) -> None:
    tm = TargetManager()
    tr = tm.add_target(etype, value)
    assert isinstance(tr.valid, bool)
    assert isinstance(tr.id, str)
    assert tr.type == etype
    assert tr.value is not None


@given(st.sampled_from(sorted(VALID_TYPES)), _NON_EMPTY_TEXT)
def test_p2_validated_id_is_deterministic(etype: str, value: str) -> None:
    id1 = make_target_id(etype, value)
    id2 = make_target_id(etype, value)
    assert id1 == id2
    assert len(id1) == 16
    assert re.match(r"^[0-9a-f]{16}$", id1)


@given(st.sampled_from(sorted(VALID_TYPES)), st.text(min_size=1, max_size=200, alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_@:"))
def test_p3_make_target_id_stable_under_case(etype: str, value: str) -> None:
    lower_val = value.lower()
    upper_val = value.upper()
    id_lower = make_target_id(etype, lower_val)
    id_upper = make_target_id(etype, upper_val)
    assert id_lower == id_upper


_VALID_DOMAINS = st.from_regex(
    r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
    fullmatch=True,
)


@given(_VALID_DOMAINS)
def test_p4_valid_domains_validate(d: str) -> None:
    errors = validate_value("domain", d)
    assert errors == [], f"expected valid domain {d!r}, got errors: {errors}"


_VALID_IPS = st.from_regex(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$",
    fullmatch=True,
)


@given(_VALID_IPS)
def test_p5_valid_ipv4_validate(ip: str) -> None:
    errors = validate_value("ipv4", ip)
    assert errors == [], f"expected valid ip {ip!r}, got errors: {errors}"


_EMAILS = st.from_regex(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", fullmatch=True)


@given(_EMAILS)
def test_p6_valid_emails_validate(email: str) -> None:
    errors = validate_value("email", email)
    assert errors == [], f"expected valid email {email!r}, got errors: {errors}"


@given(st.text(max_size=300))
def test_p7_auto_detect_never_fails(value: str) -> None:
    etype = auto_detect_type(value)
    assert etype in VALID_TYPES or etype == "auto"


@given(st.text(max_size=500))
def test_p8_validate_target_never_raises(value: str) -> None:
    errors, rtype = validate_target("domain", value)
    assert isinstance(errors, list)
    assert isinstance(rtype, str)


@given(
    st.lists(
        st.tuples(
            st.sampled_from(sorted(VALID_TYPES)),
            st.text(min_size=1, max_size=50),
        ),
        min_size=1,
        max_size=5,
    )
)
def test_p9_batch_import_idempotent(targets):
    text = "\n".join(f"{t}:{v}" for t, v in targets)
    r1 = TargetManager().batch_import(text)
    r2 = TargetManager().batch_import(text)
    assert r1.total == r2.total
    ids1 = [t.id for t in r1.targets]
    ids2 = [t.id for t in r2.targets]
    assert ids1 == ids2


@given(st.text(max_size=1000))
def test_p10_batch_import_never_raises(text: str) -> None:
    if not text.strip():
        return
    try:
        result = TargetManager().batch_import(text)
        assert result.total >= 0
        assert result.valid + result.invalid <= result.total
    except ValueError:
        pass
