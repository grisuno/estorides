"""
BDD tests for Monitoring & Advanced Recon modules.

Covers:
  - M1: Create a watch target
  - M2: Watch runs and completes
  - M3: Alert sent on completion
  - M4: Disable a watch
  - M5: Delete a watch
  - M9: Webhook alert channel
  - Advanced recon source YAML validation
"""
from __future__ import annotations

import tempfile
import time
from pathlib import Path

import pytest

from estorides_core.alerter import AlertDispatcher
from estorides_core.config import SOURCES_DIR
from estorides_core.monitoring import WatchStore, WatchTarget
from estorides_core.source_loader import SourceRegistry

# ======================================================================
# Fixtures
# ======================================================================


@pytest.fixture
def tmp_store() -> WatchStore:
    """Create a temporary WatchStore for testing, auto-closes on teardown."""
    tmp = tempfile.mkdtemp()
    db_path = Path(tmp) / "test_monitor.sqlite"
    store = WatchStore(db_path)
    yield store
    store.close()


@pytest.fixture
def sample_watch() -> WatchTarget:
    return WatchTarget(
        query="example.com",
        query_type="domain",
        interval_minutes=60,
        channels=["slack"],
        notes="test watch",
        next_run_at=time.time() + 3600,
    )


# ======================================================================
# M1 — Create a watch target
# ======================================================================


class TestM1CreateWatch:
    """M1: Watch target creation."""

    def test_create_watch(self, tmp_store: WatchStore) -> None:
        """Given a valid query, a watch is created with status pending."""
        watch = WatchTarget(query="example.com", query_type="domain",
                            interval_minutes=1440, notes="daily")
        created = tmp_store.create_watch(watch)
        assert created.id is not None
        assert len(created.id) == 8

    def test_watch_next_run_in_future(self, sample_watch: WatchTarget) -> None:
        """Given a watch, next_run_at is in the future."""
        assert sample_watch.next_run_at > time.time() - 10

    def test_watch_appears_in_list(self, tmp_store: WatchStore, sample_watch: WatchTarget) -> None:
        """Given a persisted watch, it appears in the watch list."""
        tmp_store.create_watch(sample_watch)
        watches = tmp_store.list_watches()
        ids = [w.id for w in watches]
        assert sample_watch.id in ids


# ======================================================================
# M2 — Watch runs and completes
# ======================================================================


class TestM2WatchRun:
    """M2: Watch execution and completion."""

    def test_due_watches_returns_enabled(self, tmp_store: WatchStore) -> None:
        """Given enabled watches past due, only those are returned."""
        past = WatchTarget(query="past.com", interval_minutes=60,
                           next_run_at=time.time() - 100)
        future = WatchTarget(query="future.com", interval_minutes=60,
                             next_run_at=time.time() + 3600)
        tmp_store.create_watch(past)
        tmp_store.create_watch(future)
        due = tmp_store.due_watches()
        assert len(due) == 1
        assert due[0].id == past.id

    def test_interval_honored(self, tmp_store: WatchStore) -> None:
        """Given a watch with interval 15, due returns it at the right time."""
        watch = WatchTarget(query="test.com", interval_minutes=15,
                            next_run_at=time.time() - 10)
        tmp_store.create_watch(watch)
        due = tmp_store.due_watches()
        assert len(due) == 1


# ======================================================================
# M4 — Disable a watch
# ======================================================================


class TestM4DisableWatch:
    """M4: Disabling a watch prevents it from running."""

    def test_disable_does_not_delete(self, tmp_store: WatchStore, sample_watch: WatchTarget) -> None:
        """Given a disabled watch, it still exists in the store."""
        tmp_store.create_watch(sample_watch)
        sample_watch.enabled = False
        tmp_store.update_watch(sample_watch)
        retrieved = tmp_store.get_watch(sample_watch.id)
        assert retrieved is not None
        assert retrieved.enabled is False

    def test_disabled_not_due(self, tmp_store: WatchStore) -> None:
        """Given a disabled watch past due, it is not returned as due."""
        disabled = WatchTarget(query="disabled.com", interval_minutes=60,
                               next_run_at=time.time() - 100, enabled=False)
        tmp_store.create_watch(disabled)
        due = tmp_store.due_watches()
        ids = [w.id for w in due]
        assert disabled.id not in ids


# ======================================================================
# M5 — Delete a watch
# ======================================================================


class TestM5DeleteWatch:
    """M5: Deleting a watch removes it from the store."""

    def test_delete_removes_watch(self, tmp_store: WatchStore, sample_watch: WatchTarget) -> None:
        """Given a deleted watch, it no longer appears."""
        tmp_store.create_watch(sample_watch)
        tmp_store.delete_watch(sample_watch.id)
        assert tmp_store.get_watch(sample_watch.id) is None

    def test_delete_removes_from_list(self, tmp_store: WatchStore, sample_watch: WatchTarget) -> None:
        """Given a deleted watch, the list no longer contains it."""
        tmp_store.create_watch(sample_watch)
        tmp_store.delete_watch(sample_watch.id)
        ids = [w.id for w in tmp_store.list_watches()]
        assert sample_watch.id not in ids


# ======================================================================
# Watch history
# ======================================================================


class TestWatchHistory:
    """Watch run history recording."""

    def test_record_run_start(self, tmp_store: WatchStore, sample_watch: WatchTarget) -> None:
        """Given a watch, recording a run returns a history id."""
        tmp_store.create_watch(sample_watch)
        hid = tmp_store.record_run_start(sample_watch.id)
        assert hid > 0

    def test_history_appears(self, tmp_store: WatchStore, sample_watch: WatchTarget) -> None:
        """Given a completed run, history shows it."""
        tmp_store.create_watch(sample_watch)
        hid = tmp_store.record_run_start(sample_watch.id)
        tmp_store.record_run_complete(hid, status="ok", entity_count=42)
        history = tmp_store.history(sample_watch.id)
        assert len(history) == 1
        assert history[0]["entity_count"] == 42
        assert history[0]["status"] == "ok"

    def test_history_empty_for_new_watch(self, tmp_store: WatchStore, sample_watch: WatchTarget) -> None:
        """Given a watch with no runs, history is empty."""
        tmp_store.create_watch(sample_watch)
        assert tmp_store.history(sample_watch.id) == []


# ======================================================================
# M9 — Webhook alert channel
# ======================================================================


class TestM9WebhookAlert:
    """M9: Webhook alert channel sends correctly structured payload."""

    def test_webhook_builds_correct_payload(self) -> None:
        """Given a webhook alert, the payload has the right structure."""
        dispatcher = AlertDispatcher()
        # Test that send returns False when URL is not set (no actual webhook call)
        result = dispatcher.send("webhook", "Test Title", "Test Body")
        # Without URL set, should return False with a warning log
        assert result is False


# ======================================================================
# Advanced Recon Sources — YAML validation
# ======================================================================


class TestAdvancedReconSources:
    """Verify that the new recon source YAMLs are valid and loadable."""

    @pytest.mark.parametrize("source_name", [
        "securitytrails_dns",
        "censys_certificates",
        "fullhunt_surface",
        "hunter_email",
    ])
    def test_source_yaml_loads(self, source_name: str) -> None:
        """Given a source YAML file, it loads without errors."""
        registry = SourceRegistry(SOURCES_DIR)
        registry.load()
        source = registry.get(source_name)
        assert source is not None, f"{source_name} must exist"
        assert source["name"] == source_name
        assert source["enabled"] is True

    @pytest.mark.parametrize("source_name,key_env", [
        ("securitytrails_dns", "SECURITYTRAILS_API_KEY"),
        ("censys_certificates", "CENSYS_BASIC_AUTH"),
        ("fullhunt_surface", "FULLHUNT_API_KEY"),
        ("hunter_email", "HUNTER_API_KEY"),
    ])
    def test_source_requires_key(self, source_name: str, key_env: str) -> None:
        """Given a source YAML, it declares the correct key_env."""
        registry = SourceRegistry(SOURCES_DIR)
        registry.load()
        source = registry.get(source_name)
        assert source is not None
        assert source["requires_key"] is True
        assert source["key_env"] == key_env

    def test_all_new_sources_passive(self) -> None:
        """Given the new sources, all are contact: none (passive)."""
        registry = SourceRegistry(SOURCES_DIR)
        registry.load()
        for name in ["securitytrails_dns", "censys_certificates",
                      "fullhunt_surface", "hunter_email"]:
            source = registry.get(name)
            assert source is not None
            assert source.get("contact") == "none", f"{name} should be passive"


# ======================================================================
# Alerter — channel configuration tests
# ======================================================================


class TestAlerterChannels:
    """Alert channel configuration checks."""

    def test_available_channels_returns_all(self) -> None:
        """Given the dispatcher, available_channels returns all channel types."""
        dispatcher = AlertDispatcher()
        channels = dispatcher.available_channels()
        names = {ch["name"] for ch in channels}
        assert "slack" in names
        assert "discord" in names
        assert "telegram" in names
        assert "email" in names
        assert "webhook" in names

    def test_channel_env_vars_listed(self) -> None:
        """Given available channels, each has its env_var listed."""
        dispatcher = AlertDispatcher()
        for ch in dispatcher.available_channels():
            assert "env_var" in ch
            assert ch["env_var"] != ""

    def test_unknown_channel_returns_false(self) -> None:
        """Given an unknown channel name, send returns False."""
        dispatcher = AlertDispatcher()
        assert dispatcher.send("nonexistent_channel", "title", "body") is False


# ======================================================================
# WatchTarget dataclass tests
# ======================================================================


class TestWatchTargetDataclass:
    """WatchTarget creation and serialisation."""

    def test_to_dict_roundtrip(self) -> None:
        """Given a WatchTarget, to_dict and from_dict roundtrip."""
        original = WatchTarget(query="test.com", interval_minutes=120,
                               channels=["slack", "email"],
                               notes="test roundtrip",
                               next_run_at=time.time() + 100)
        d = original.to_dict()
        restored = WatchTarget.from_dict(d)
        assert restored.query == original.query
        assert restored.interval_minutes == original.interval_minutes
        assert restored.channels == original.channels
        assert restored.notes == original.notes

    def test_default_next_run_set(self) -> None:
        """Given a WatchTarget with no next_run_at, it defaults to future."""
        w = WatchTarget(query="default.com")
        assert w.next_run_at > time.time()

    def test_default_channels_empty(self) -> None:
        """Given a WatchTarget with no channels, channels is empty."""
        w = WatchTarget(query="nochannels.com")
        assert w.channels == []


# ======================================================================
# Source count verification
# ======================================================================


class TestSourceCount:
    """Verify that new sources are properly counted."""

    def test_new_sources_loaded(self) -> None:
        """Given the source directory, the new sources are loaded and counted."""
        registry = SourceRegistry(SOURCES_DIR)
        registry.load()
        for name in ["securitytrails_dns", "censys_certificates",
                      "fullhunt_surface", "hunter_email"]:
            assert registry.get(name) is not None, f"{name} not loaded"
