"""BDD tests for lan_runner (spec/lan_runner.md). Written before code."""

from estorides_core import lan_runner

ARP = "192.168.1.1 dev eth0 lladdr AA:BB:CC:DD:EE:FF REACHABLE\n"
DHCP = "0 aa:bb:cc:dd:ee:ff 192.168.1.20 laptop *\n"
ACTIVE = "192.168.1.30\taa:bb:cc:dd:ee:00\tVendor\n"


def test_s1_passive_injected(tmp_path):
    res = lan_runner.scan(
        scope_cidr="192.168.1.0/24", consent=True,
        arp_text=ARP, dhcp_text=DHCP, output_dir=str(tmp_path),
    )
    assert res.refused is False
    assert res.device_count == 1
    assert res.entities != []
    assert res.active_used is False
    assert res.bundle.get("inventory")


def test_s2_no_consent_refused(tmp_path):
    res = lan_runner.scan(
        scope_cidr="192.168.1.0/24", consent=False,
        arp_text=ARP, dhcp_text=DHCP, output_dir=str(tmp_path),
    )
    assert res.refused is True
    assert res.block_reason == "consent_required"
    assert res.device_count == 0


def test_s3_bad_scope_refused(tmp_path):
    res = lan_runner.scan(
        scope_cidr="8.8.8.0/24", consent=True,
        arp_text=ARP, output_dir=str(tmp_path),
    )
    assert res.refused is True
    assert res.block_reason == "scope_invalid"


def test_s4_degrade_active(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTORIDES_LAN_ALLOW_ACTIVE", "0")
    res = lan_runner.scan(
        scope_cidr="192.168.1.0/24", consent=True, allow_active=True,
        arp_text=ARP, output_dir=str(tmp_path),
    )
    assert res.refused is False
    assert res.active_used is False
    assert res.notice is not None
    assert res.device_count == 1


def test_s5_active_injected(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTORIDES_LAN_ALLOW_ACTIVE", "1")
    res = lan_runner.scan(
        scope_cidr="192.168.1.0/24", consent=True, allow_active=True,
        arp_text=ARP, active_text=ACTIVE, output_dir=str(tmp_path),
    )
    assert res.active_used is True
    assert res.device_count == 2


class _FakeToolResult:
    def __init__(self, exit_code: int, stdout: str) -> None:
        self.exit_code = exit_code
        self.stdout = stdout


def test_s9_tool_order():
    from estorides_core.tool_runner import ToolErrorResult

    calls: list[str] = []

    def ok_nmap(tool: str, args: list[str], **_kw: object) -> object:
        calls.append(tool)
        return _FakeToolResult(0, "Host: 192.168.1.5 ()\tStatus: Up\n")

    tool, _out = lan_runner.run_active_scan("192.168.1.0/24", runner=ok_nmap)
    assert tool == "nmap"

    def fail_then_arp(tool: str, args: list[str], **_kw: object) -> object:
        calls.append(tool)
        if tool == "nmap":
            return ToolErrorResult(
                tool_name=tool, error_code="TOOL_CRASH", message="x",
                exit_code=1, duration_s=0.1,
            )
        return _FakeToolResult(0, "192.168.1.6 dev eth0 lladdr AA:BB:CC:DD:EE:01 REACHABLE\n")

    tool, _out = lan_runner.run_active_scan("192.168.1.0/24", runner=fail_then_arp)
    assert tool == "arp-scan"

    def both_fail(tool: str, args: list[str], **_kw: object) -> object:
        return ToolErrorResult(
            tool_name=tool, error_code="TOOL_CRASH", message="x",
            exit_code=1, duration_s=0.1,
        )

    assert lan_runner.run_active_scan("192.168.1.0/24", runner=both_fail) == ("", "")


def test_s6_empty_readers(tmp_path):
    res = lan_runner.scan(
        scope_cidr="192.168.1.0/24", consent=True,
        arp_text="", dhcp_text="", output_dir=str(tmp_path),
    )
    assert res.refused is False
    assert res.device_count == 0
    assert res.bundle.get("inventory")


def test_s7_scope_auto(tmp_path):
    res = lan_runner.scan(
        consent=True, interfaces=[{"address": "192.168.1.10/24"}],
        arp_text=ARP, output_dir=str(tmp_path),
    )
    assert res.refused is False
    assert res.scope_cidr == "192.168.1.0/24"


def test_s8_no_scope_found(tmp_path):
    res = lan_runner.scan(
        consent=True, interfaces=[], arp_text=ARP,
        output_dir=str(tmp_path),
    )
    assert res.refused is True
    assert res.block_reason == "scope_invalid"
