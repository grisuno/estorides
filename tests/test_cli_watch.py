"""
BDD / regression tests for the `estorides watch add` CLI path.

Context (boy-scout fix): `cmd_watch_add` used to crash with
`AttributeError` (the `watch add` subparser never declared `--proxy` /
`--passive-only`) and then `NameError` (`SCHEDULER_ENABLED` undefined).
These tests pin the contract so the path can never silently rot again.

  - CW1: parser accepts the OPSEC flags on `watch add`
  - CW2: `cmd_watch_add` persists the watch and starts the scheduler
  - CW3: a malformed interval < 15 is rejected before any side effect
  - CW4: the scheduler runner is wired exactly once (idempotent)
"""
from __future__ import annotations

from argparse import Namespace

import pytest

from estorides_cli import build_parser, cmd_watch_add
from estorides_core.monitoring import WatchStore


class _FakeScheduler:
    """Minimal stand-in for WatchScheduler: records calls, no threads."""

    def __init__(self) -> None:
        self._runner = None
        self.running = False
        self.started = 0
        self.runner_set = 0

    @property
    def has_runner(self) -> bool:
        return self._runner is not None

    def set_runner(self, runner: object) -> None:
        self._runner = runner
        self.runner_set += 1

    def start(self) -> None:
        self.started += 1
        self.running = True


@pytest.fixture
def cli_env(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Isolate the CLI from the real singletons."""
    import estorides_core.monitoring as monitoring

    store = WatchStore(tmp_path / "watch.sqlite")
    sched = _FakeScheduler()
    monkeypatch.setattr(monitoring, "store", store)
    monkeypatch.setattr(monitoring, "scheduler", sched)
    yield store, sched
    store.close()


class TestCW1Parser:
    def test_watch_add_accepts_opsec_flags(self) -> None:
        args = build_parser().parse_args(
            ["watch", "add", "example.com", "--interval", "30",
             "--proxy", "socks5://127.0.0.1:9050"]
        )
        assert args.proxy == "socks5://127.0.0.1:9050"
        assert args.passive_only is False


class TestCW2Command:
    def test_watch_add_persists_and_starts(self, cli_env) -> None:
        store, sched = cli_env
        parser = build_parser()
        args = parser.parse_args(["watch", "add", "example.com", "--interval", "30"])
        rc = cmd_watch_add(args)
        assert rc == 0
        watches = store.list_watches()
        assert len(watches) == 1
        assert watches[0].query == "example.com"
        assert sched.runner_set == 1
        assert sched.started == 1

    def test_watch_add_wires_runner_once(self, cli_env) -> None:
        _store, sched = cli_env
        args = build_parser().parse_args(["watch", "add", "a.com"])
        cmd_watch_add(args)
        cmd_watch_add(Namespace(query="b.com", type="auto", interval=30,
                                channels="", notes="", proxy=None,
                                passive_only=False))
        assert sched.runner_set == 1


class TestCW3Validation:
    def test_interval_below_minimum_rejected(self, cli_env) -> None:
        store, sched = cli_env
        args = build_parser().parse_args(["watch", "add", "example.com", "--interval", "5"])
        rc = cmd_watch_add(args)
        assert rc == 2
        assert store.list_watches() == []
        assert sched.started == 0


class TestCW4RunnerFactory:
    def test_runner_factory_returns_awaitable_callable(self, cli_env) -> None:
        from estorides_cli import _watch_runner_factory

        runner = _watch_runner_factory(proxy=None, passive_only=True)
        assert callable(runner)

    def test_scheduler_has_runner_property(self, tmp_path) -> None:
        from estorides_core.monitoring import WatchScheduler

        store = WatchStore(tmp_path / "sched.sqlite")
        try:
            sched = WatchScheduler(store=store)
            assert sched.has_runner is False
            sched.set_runner(lambda w: {})
            assert sched.has_runner is True
        finally:
            store.close()
