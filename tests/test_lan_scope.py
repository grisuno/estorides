"""BDD tests for lan_scope (spec/lan_scope.md). Written before code."""

from estorides_core import lan_scope


def test_s1_v4_parses_to_network():
    assert (
        lan_scope.parse_interface_addr({"address": "192.168.1.10/24"})
        == "192.168.1.0/24"
    )


def test_s2_v6_ula_accepted():
    out = lan_scope.parse_interface_addr({"address": "fd00::5/64"})
    assert out is not None and out.endswith("/64")


def test_s3_mixed_keeps_private_only():
    cidrs = lan_scope.select_private_cidrs(
        [
            {"address": "192.168.1.10/24"},
            {"address": "8.8.8.8/24"},
            {"address": "127.0.0.1/8"},
        ]
    )
    assert cidrs == ["192.168.1.0/24"]


def test_s4_garbage_returns_none():
    assert lan_scope.parse_interface_addr({"address": "not-an-ip"}) is None


def test_s5_public_returns_none():
    assert lan_scope.parse_interface_addr({"address": "8.8.8.8/24"}) is None


def test_s6_wide_scope_rejected():
    assert lan_scope.parse_interface_addr({"address": "10.0.0.1/4"}) is None


def test_s7_empty_default_none():
    assert lan_scope.default_scope([]) is None


def test_s8_reader_fail_soft(monkeypatch):
    monkeypatch.setattr(lan_scope.shutil, "which", lambda _b: None)
    assert lan_scope.read_local_interfaces() == []
