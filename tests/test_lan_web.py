"""BDD tests for lan_web (spec/lan_web.md). Written before code."""

from estorides_core import lan_web


def test_s1_passive_permitted():
    v = lan_web.guard({"lan_consent": True})
    assert v.permitted is True and v.status == 200
    assert v.max_contact == "none"


def test_s2_active_permitted(monkeypatch):
    monkeypatch.setenv("ESTORIDES_LAN_ALLOW_ACTIVE", "1")
    v = lan_web.guard(
        {"lan_consent": True, "allow_active": True,
         "requested_contact": "active"}
    )
    assert v.permitted is True and v.max_contact == "active"


def test_s3_checkbox_without_ceiling_degrades(monkeypatch):
    monkeypatch.setenv("ESTORIDES_LAN_ALLOW_ACTIVE", "0")
    v = lan_web.guard(
        {"lan_consent": True, "allow_active": True,
         "requested_contact": "active"}
    )
    assert v.permitted is True and v.status == 200
    assert v.max_contact == "none"
    assert v.notice == "active-unavailable"


def test_s3b_pure_passive_has_no_notice():
    v = lan_web.guard({"lan_consent": True})
    assert v.permitted is True and v.notice is None


def test_s4_no_consent_refused():
    v = lan_web.guard({"lan_consent": False})
    assert v.permitted is False and v.status == 403
    assert v.error == "lan-consent-required"


def test_s5_bad_scope_400():
    v = lan_web.guard({"lan_consent": True, "scope_cidr": "8.8.8.0/24"})
    assert v.permitted is False and v.status == 400
    assert v.error == "lan-scope-invalid"


def test_s6_string_consent_refused():
    v = lan_web.guard({"lan_consent": "yes"})
    assert v.permitted is False and v.status == 403


def test_s7_body_not_dict():
    v = lan_web.guard(["lan_consent"])
    assert v.permitted is False and v.status == 403


def test_s9_lan_request_detection():
    assert lan_web.is_lan_request({"lan_consent": True}) is True
    assert lan_web.is_lan_request({}, "192.168.1.0/24") is True
    assert lan_web.is_lan_request({}, "example.com") is False
    assert lan_web.is_lan_request({"value": "192.168.1.5"}, "192.168.1.5") is True


def test_s10_scope_payload():
    payload = lan_web.scope_payload([{"address": "192.168.1.10/24"}])
    assert payload["cidrs"] == ["192.168.1.0/24"]
    assert payload["scope"] == "192.168.1.0/24"
    empty = lan_web.scope_payload([{"address": "8.8.8.8/24"}])
    assert empty == {"cidrs": [], "scope": None}


def test_s11_active_intent_permitted(monkeypatch):
    monkeypatch.setenv("ESTORIDES_LAN_ALLOW_ACTIVE", "1")
    v = lan_web.guard(
        {"lan_consent": True, "allow_active": True,
         "scope_cidr": "192.168.1.0/24",
         "requested_contact": "active"}
    )
    assert v.permitted is True and v.max_contact == "active"


def test_s8_scope_echo_normalized():
    v = lan_web.guard(
        {"lan_consent": True, "scope_cidr": " 192.168.1.0/24 "}
    )
    assert v.permitted is True
    assert v.scope_cidr == "192.168.1.0/24"
