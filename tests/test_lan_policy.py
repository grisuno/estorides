"""BDD tests for lan_policy (spec/lan_policy.md). Written before code."""

from estorides_core import lan_policy


def test_s1_passive_allowed_with_consent():
    req = lan_policy.LanPolicyRequest(
        consent=True, allow_active=False, requested_contact="none"
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is True
    assert dec.max_contact == "none"
    assert dec.active_permitted is False


def test_s2_active_allowed_on_triple_gate(monkeypatch):
    monkeypatch.setenv("ESTORIDES_LAN_ALLOW_ACTIVE", "1")
    req = lan_policy.LanPolicyRequest(
        consent=True, allow_active=True, requested_contact="active"
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is True
    assert dec.active_permitted is True
    assert dec.max_contact == "active"


def test_s3_checkbox_without_env_ceiling_denies_active(monkeypatch):
    monkeypatch.setenv("ESTORIDES_LAN_ALLOW_ACTIVE", "0")
    req = lan_policy.LanPolicyRequest(
        consent=True, allow_active=True, requested_contact="active"
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is False
    assert dec.block_reason == "contact_denied"


def test_s4_valid_private_scope_echoes():
    req = lan_policy.LanPolicyRequest(
        consent=True,
        allow_active=False,
        scope_cidr="192.168.1.0/24",
        requested_contact="none",
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is True
    assert dec.scope_cidr == "192.168.1.0/24"


def test_s5_no_consent_blocks_even_passive():
    req = lan_policy.LanPolicyRequest(
        consent=False, allow_active=False, requested_contact="none"
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is False
    assert dec.block_reason == "consent_required"


def test_s6_public_scope_blocked():
    req = lan_policy.LanPolicyRequest(
        consent=True,
        allow_active=False,
        scope_cidr="8.8.8.0/24",
        requested_contact="none",
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is False
    assert dec.block_reason == "scope_invalid"


def test_s7_truthy_string_consent_blocked():
    req = lan_policy.LanPolicyRequest(
        consent="yes", allow_active=False, requested_contact="none"
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is False
    assert dec.block_reason == "consent_required"


def test_s8_unknown_contact_denied_and_capped():
    req = lan_policy.LanPolicyRequest(
        consent=True, allow_active=False, requested_contact="hyperactive"
    )
    dec = lan_policy.evaluate(req)
    assert dec.allowed is False
    assert dec.max_contact == "none"
