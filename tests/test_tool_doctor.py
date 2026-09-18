"""M4 RED tests: tool doctor."""
from __future__ import annotations


def test_doctor_covers_system_app_binaries() -> None:
    from estorides_core.tool_install import doctor

    rep = doctor()
    names = {t["name"] for t in rep["tools"]}
    for binary in ("theHarvester", "phoneinfoga", "sherlock", "amass"):
        assert binary in names
    entry = next(t for t in rep["tools"] if t["name"] == "phoneinfoga")
    assert "kali_phoneinfoga" in entry["sources"]


def test_doctor_flags_path_binary() -> None:
    from estorides_core.tool_install import doctor

    rep = doctor()
    entry = next(t for t in rep["tools"] if t["name"] == "sh")
    assert entry["available"] is True
    assert entry["installable"] is False


def test_doctor_installable_when_missing_with_recipe() -> None:
    from estorides_core.tool_install import doctor

    rep = doctor()
    missing = [t for t in rep["tools"] if not t["available"] and t["recipe"]]
    assert missing
    assert all(t["installable"] for t in missing)
    assert rep["summary"]["installable"] == len(missing)


def test_doctor_summary_consistent() -> None:
    from estorides_core.tool_install import doctor

    rep = doctor()
    s = rep["summary"]
    assert s["total"] == len(rep["tools"])
    assert s["available"] + s["missing"] == s["total"]
