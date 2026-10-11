"""BDD tests for lan_inventory (spec/lan_inventory.md). Written before code."""

from estorides_core import lan_inventory


def test_s1_arp_parses():
    text = "192.168.1.1 dev eth0 lladdr AA:BB:CC:DD:EE:FF REACHABLE\n"
    out = lan_inventory.parse_arp_table(text)
    assert out and out[0]["ip"] == "192.168.1.1"
    assert out[0]["mac"] == "aa:bb:cc:dd:ee:ff"


def test_s2_dhcp_parses_hostname():
    text = "0 aa:bb:cc:dd:ee:ff 192.168.1.20 laptop *\n"
    out = lan_inventory.parse_dhcp_leases(text)
    assert out and out[0]["hostname"] == "laptop"


def test_s3_merge_same_mac():
    devs = lan_inventory.merge_devices(
        [
            {"ip": "192.168.1.20", "mac": "aa:bb:cc:dd:ee:ff",
             "hostname": None, "source": "ip-neigh"},
            {"ip": "192.168.1.21", "mac": "AA-BB-CC-DD-EE-FF",
             "hostname": "laptop", "source": "dhcp-leases"},
        ]
    )
    assert len(devs) == 1
    assert "192.168.1.20" in devs[0].ips
    assert "laptop" in devs[0].hostnames


def test_s4_merge_no_mac_by_ip():
    devs = lan_inventory.merge_devices(
        [
            {"ip": "192.168.1.30", "mac": None,
             "hostname": None, "source": "ip-neigh"},
            {"ip": "192.168.1.30", "mac": None,
             "hostname": "printer", "source": "dhcp-leases"},
        ]
    )
    assert len(devs) == 1
    assert devs[0].device_id == "ip:192.168.1.30"


def test_s5_garbage_empty():
    assert lan_inventory.parse_arp_table("hello world\n") == []
    assert lan_inventory.parse_dhcp_leases("hello world\n") == []


def test_s6_public_dropped():
    out = lan_inventory.parse_arp_table(
        "8.8.8.8 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE\n"
    )
    assert out == []


def test_s7_mac_formats_equal():
    a = lan_inventory.normalize_mac("AA-BB-CC-DD-EE-FF")
    b = lan_inventory.normalize_mac("aabb.ccdd.eeff")
    assert a == b == "aa:bb:cc:dd:ee:ff"


def test_s9_dead_entries_dropped():
    text = (
        "192.168.1.50 dev eth0 lladdr aa:bb:cc:dd:ee:01 FAILED\n"
        "192.168.1.51 dev eth0 INCOMPLETE\n"
        "192.168.1.1 dev eth0 lladdr AA:BB:CC:DD:EE:FF REACHABLE\n"
    )
    out = lan_inventory.parse_arp_table(text)
    assert [s["ip"] for s in out] == ["192.168.1.1"]


NMAP_XML = """<?xml version="1.0"?>
<nmaprun>
<host><status state="up" reason="arp-response"/>
<address addr="192.168.1.98" addrtype="ipv4"/>
<address addr="1A:14:B0:14:08:6E" addrtype="mac" vendor="Unknown"/>
<hostnames><hostname name="phone" type="PTR"/></hostnames>
</host>
<host><status state="up" reason="arp-response"/>
<address addr="192.168.1.220" addrtype="ipv4"/>
<address addr="EC:C3:02:B0:4C:97" addrtype="mac" vendor="Humax"/>
</host>
<host><status state="down" reason="no-response"/>
<address addr="192.168.1.99" addrtype="ipv4"/>
</host>
</nmaprun>
"""

NMAP_GREP = """# Nmap 7.99 scan
Host: 192.168.1.98 ()\tStatus: Up
Host: 192.168.1.98 ()\tMAC Address: 1A:14:B0:14:08:6E (Unknown)
Host: 192.168.1.120 (None.None)\tStatus: Up
Host: 192.168.1.99 ()\tStatus: Down
"""


def test_s10_nmap_xml():
    out = lan_inventory.parse_nmap_xml(NMAP_XML)
    by_ip = {s["ip"]: s for s in out}
    assert set(by_ip) == {"192.168.1.98", "192.168.1.220"}
    assert by_ip["192.168.1.98"]["mac"] == "1a:14:b0:14:08:6e"
    assert by_ip["192.168.1.220"]["hostname"] == "Humax"


def test_s11_nmap_grepable():
    out = lan_inventory.parse_nmap_grepable(NMAP_GREP)
    by_ip = {s["ip"]: s for s in out}
    assert set(by_ip) == {"192.168.1.98", "192.168.1.120"}
    assert by_ip["192.168.1.98"]["mac"] == "1a:14:b0:14:08:6e"


def test_s12_dispatch_tags_source():
    assert all(
        s["source"] == "nmap"
        for s in lan_inventory.parse_active_output(NMAP_XML, "nmap")
    )
    assert lan_inventory.parse_active_output(NMAP_GREP, "nmap")[0]["source"] == "nmap"
    assert lan_inventory.parse_active_output(
        "192.168.1.1 dev eth0 lladdr AA:BB:CC:DD:EE:FF REACHABLE\n", "arp-scan"
    )[0]["source"] == "arp-scan"


def test_s13_hostile_xml_rejected():
    big = "<!DOCTYPE x [" + "<!ENTITY a '12345678'>" * 400000 + "]><x>&a;</x>"
    assert lan_inventory.parse_nmap_xml(big) == []


def test_s10_cross_source_fold():
    devs = lan_inventory.merge_devices(
        [
            {"ip": "192.168.1.98", "mac": None,
             "hostname": None, "source": "nmap"},
            {"ip": "192.168.1.98", "mac": "1a:14:b0:14:08:6e",
             "hostname": None, "source": "ip-neigh"},
        ]
    )
    assert len(devs) == 1
    assert devs[0].device_id == "mac:1a:14:b0:14:08:6e"
    assert set(devs[0].sources) == {"nmap", "ip-neigh"}


def test_s8_contact_map():
    assert lan_inventory.contact_for_tool("nmap") == "active"
    assert lan_inventory.contact_for_tool("ip-neigh") == "none"
    assert lan_inventory.contact_for_tool("mystery-tool") == "active"
