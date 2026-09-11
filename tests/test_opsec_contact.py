"""
BDD tests for operator-OPSEC contact classification + passive-only filter.

Ported from the standalone ``_test_passive.py`` validator into pytest.
Offline: exercises the registry and the orchestrator selector.
"""
from __future__ import annotations

from estorides_core.config import (
    CONTACT_LEVELS,
    DEFAULT_CONTACT,
    SOURCES_DIR,
    contact_level,
)
from estorides_core.orchestrator import Orchestrator
from estorides_core.source_loader import SourceRegistry


def _registry() -> SourceRegistry:
    reg = SourceRegistry(SOURCES_DIR)
    reg.load()
    return reg


class TestContactLevel:
    def test_ordering(self) -> None:
        assert contact_level("none") < contact_level("broker") < contact_level("active")

    def test_unknown_is_active(self) -> None:
        assert contact_level("bogus") == CONTACT_LEVELS["active"]

    def test_default_is_passive(self) -> None:
        assert contact_level(DEFAULT_CONTACT) == CONTACT_LEVELS["none"]


class TestRegistryContact:
    def test_sources_load(self) -> None:
        assert len(_registry().all()) > 0

    def test_all_sources_carry_known_class(self) -> None:
        bad = [s["name"] for s in _registry().all()
               if s.get("contact") not in CONTACT_LEVELS]
        assert not bad, f"offenders={bad[:5]}"

    def test_passive_filter_excludes_broker_active(self) -> None:
        reg = _registry()
        passive = reg.filter(max_contact="none")
        leaked = [s["name"] for s in passive if contact_level(s["contact"]) > 0]
        assert not leaked, f"leaked={leaked}"
        assert len(passive) < len(reg.all())


class TestBrokerTagging:
    def test_hackertarget_probes_are_broker(self) -> None:
        broker_names = {s["name"] for s in _registry().all() if s["contact"] == "broker"}
        for expected in ("hackertarget_nping", "hackertarget_traceroute",
                         "hackertarget_http_headers"):
            assert expected in broker_names


class TestSelectorCeiling:
    def test_selector_drops_broker_even_when_named(self) -> None:
        orch = Orchestrator()
        chosen = orch._select_sources(
            ["hackertarget_nping", "crt_sh_certificates"],
            include_paid=True, max_contact="none",
        )
        names = {s["name"] for s in chosen}
        assert "hackertarget_nping" not in names
        assert "crt_sh_certificates" in names

    def test_selector_keeps_broker_without_ceiling(self) -> None:
        orch = Orchestrator()
        chosen = orch._select_sources(
            ["hackertarget_nping"], include_paid=True, max_contact=None,
        )
        assert "hackertarget_nping" in {s["name"] for s in chosen}
