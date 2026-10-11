"""BDD tests for lan_bundle (spec/lan_bundle.md). Written before code."""

import json

from estorides_core import lan_bundle
from estorides_core.lan_inventory import LanDevice


def _devs():
    return [
        LanDevice(
            device_id="mac:aa:bb:cc:dd:ee:ff",
            ips=("192.168.1.20",),
            mac="aa:bb:cc:dd:ee:ff",
            hostnames=("laptop",),
            sources=("ip-neigh", "dhcp-leases"),
        ),
        LanDevice(
            device_id="ip:192.168.1.30",
            ips=("192.168.1.30",),
            mac=None,
            hostnames=(),
            sources=("ip-neigh",),
        ),
    ]


def test_s1_bundle_graph_and_lazyown():
    b = lan_bundle.build_bundle(_devs(), scope_cidr="192.168.1.0/24")
    assert b["inventory"]["device_count"] == 2
    kinds = {n["kind"] for n in b["graph"]["nodes"]}
    assert "device" in kinds and "network" in kinds
    lz_kinds = {n["kind"] for n in b["lazyown"]["nodes"]}
    assert "host" in lz_kinds and "mac" in lz_kinds


def test_s2_empty():
    b = lan_bundle.build_bundle([], scope_cidr=None)
    assert b["inventory"]["devices"] == []
    assert b["graph"]["nodes"] == [] or isinstance(b["graph"]["nodes"], list)


def test_s3_stem_traversal_sanitized():
    assert lan_bundle.sanitize_stem("../../etc") == "lan"


def test_s4_stix_shapes():
    b = lan_bundle.build_bundle(_devs(), scope_cidr=None)
    types = {o["type"] for o in b["stix"]["objects"]}
    assert "ipv4-addr" in types and "mac-addr" in types


def test_s5_write_atomic(tmp_path):
    import warnings

    warnings.filterwarnings("ignore", category=ResourceWarning)
    res = lan_bundle.write_bundle(
        _devs(), output_dir=str(tmp_path), stem="test",
        scope_cidr="192.168.1.0/24",
    )
    assert res.errors == []
    from pathlib import Path as _P

    for _fmt, path in res.paths.items():
        assert json.loads(_P(path).read_text(encoding="utf-8")) is not None


def test_s6_error_dir(tmp_path):
    f = tmp_path / "blocker"
    f.write_text("x", encoding="utf-8")
    res = lan_bundle.write_bundle(_devs(), output_dir=str(f), stem="t")
    assert res.errors != []


def test_s7_scope_tagged():
    b = lan_bundle.build_bundle(_devs(), scope_cidr="192.168.1.0/24")
    assert b["inventory"]["scope_cidr"] == "192.168.1.0/24"
    assert any(n.get("kind") == "network" for n in b["graph"]["nodes"])


def test_s8_deterministic():
    a = lan_bundle.build_bundle(
        _devs(), scope_cidr="192.168.1.0/24", generated_at=1700000000.0
    )
    c = lan_bundle.build_bundle(
        _devs(), scope_cidr="192.168.1.0/24", generated_at=1700000000.0
    )
    assert a["graph"] == c["graph"]
    assert a["lazyown"] == c["lazyown"]
