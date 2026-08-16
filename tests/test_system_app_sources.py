"""BDD tests for estorides_core.system_app_sources.

Kali OSINT CLI tools as first-class `system_app` sources: same aggregation
pipeline as HTTP sources, new YAML origin kind. Scenarios mirror
`spec/system_app_sources.md` (S1-S8).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml

from estorides_core.source_loader import SourceRegistry
from estorides_core.system_app_sources import (
    SystemAppResult,
    execute,
    render_args,
)
from estorides_core.tool_runner import ToolErrorResult, ToolResult

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

SHERLOCK_SOURCE: dict[str, Any] = {
    "name": "kali_sherlock",
    "category": "20. System Tools (Kali)",
    "kind": "system_app",
    "os": "linux",
    "requires_key": False,
    "contact": "none",
    "logs_queries": True,
    "parser": "sherlock_text",
    "entity_hints": ["username", "url"],
    "applies_to": ["username"],
    "tool": {
        "binary": "sherlock",
        "args": ["{query}", "--print-found", "--no-color", "--timeout", "30"],
        "output_format": "text",
        "timeout": 120,
    },
}


def _stub_runner(exit_code: int = 0, stdout: str = "", stderr: str = "",
                 error_code: str | None = None,
                 error_message: str | None = None,
                 on_run: Any = None) -> Any:
    def stub(binary: str, args: list[str], *, target: str = "",
             timeout: int | None = None, max_output_bytes: int = 0,
             cwd: str | None = None) -> Any:
        if on_run is not None:
            on_run(binary, args, target=target, timeout=timeout,
                   max_output_bytes=max_output_bytes)
        return ToolResult(
            tool_name=binary,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            duration_s=0.5,
            parsed_entities=[],
            confidence=0.5,
            raw_output_sha1="abcd" * 10,
            truncated=False,
            error_code=error_code,
            error_message=error_message,
        )

    return stub


# ---------------------------------------------------------------------------
# S1 · happy path
# ---------------------------------------------------------------------------

class TestS1HappyPath:
    def test_execute_renders_query_and_parses_found_lines(self) -> None:
        captured: dict[str, Any] = {}

        def on_run(binary: str, args: list[str], **kw: Any) -> None:
            captured["binary"] = binary
            captured["args"] = args

        runner = _stub_runner(
            stdout=(
                "[+] testuser: https://github.com/testuser\n"
                "[-] notfound: https://example.org/\n"
            ),
            on_run=on_run,
        )
        result = execute(SHERLOCK_SOURCE, "testuser", _runner=runner)

        assert isinstance(result, SystemAppResult)
        assert result.success is True
        assert result.exit_code == 0
        assert captured["binary"] == "sherlock"
        assert captured["args"][0] == "testuser"
        assert "--print-found" in captured["args"]
        assert any("github.com/testuser" in line for line in result.parsed)
        assert "notfound" not in " ".join(result.parsed)

    def test_execute_returns_source_and_tool_metadata(self) -> None:
        result = execute(
            SHERLOCK_SOURCE, "testuser", _runner=_stub_runner(stdout="[+] x: https://a.b/x"),
        )
        assert result.source_name == "kali_sherlock"
        assert result.tool_name == "sherlock"
        assert result.raw_output_sha1
        assert result.duration_s >= 0.0


# ---------------------------------------------------------------------------
# S2 · missing binary degrades to error observation
# ---------------------------------------------------------------------------

class TestS2MissingBinary:
    def test_execute_reports_tool_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import estorides_core.system_app_sources as sas

        monkeypatch.setattr(sas, "tool_available", lambda _binary: False)
        result = execute(SHERLOCK_SOURCE, "testuser", _runner=_stub_runner())

        assert result.success is False
        assert result.error_code == "TOOL_NOT_FOUND"
        assert result.parsed is None

    def test_execute_reports_missing_binary_declaration(self) -> None:
        broken = dict(SHERLOCK_SOURCE)
        broken["tool"] = {"args": ["{query}"]}
        result = execute(broken, "testuser", _runner=_stub_runner())
        assert result.error_code == "NO_BINARY"

    def test_execute_rejects_non_allowlisted_binary(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import estorides_core.system_app_sources as sas

        monkeypatch.setattr(sas, "tool_available", lambda _binary: True)
        rogue = dict(SHERLOCK_SOURCE)
        rogue["tool"] = dict(SHERLOCK_SOURCE["tool"])
        rogue["tool"]["binary"] = "evil-tool-9f3a2b"
        result = execute(rogue, "testuser", _runner=_stub_runner())
        assert result.error_code == "TOOL_NOT_ALLOWED"


# ---------------------------------------------------------------------------
# S3 · non-zero exit still parses best effort
# ---------------------------------------------------------------------------

class TestS3Crash:
    def test_nonzero_exit_keeps_parsed_output(self) -> None:
        runner = _stub_runner(
            exit_code=1,
            stdout="[+] partial: https://partial.example/u",
            stderr="boom",
            error_code="TOOL_CRASH",
            error_message="boom",
        )
        result = execute(SHERLOCK_SOURCE, "testuser", _runner=runner)
        assert result.success is False
        assert result.error_code == "TOOL_CRASH"
        assert result.parsed is not None
        assert any("partial.example" in line for line in result.parsed)


# ---------------------------------------------------------------------------
# S4 · metacharacter rejection
# ---------------------------------------------------------------------------

class TestS4Injection:
    def test_metachar_arg_is_rejected_by_tool_runner(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        import estorides_core.system_app_sources as sas

        monkeypatch.setattr(sas, "tool_available", lambda _binary: True)
        hostile = dict(SHERLOCK_SOURCE)
        hostile["tool"] = dict(SHERLOCK_SOURCE["tool"])
        hostile["tool"]["args"] = ["{query}", "x; rm -rf /"]
        result = execute(hostile, "testuser")  # real run_tool — never spawns
        assert result.error_code == "TOOL_INJECTION"
        assert result.success is False


# ---------------------------------------------------------------------------
# S5 · JSON file output
# ---------------------------------------------------------------------------

class TestS5JsonFileOutput:
    AMASS: dict[str, Any] = {
        "name": "kali_amass",
        "category": "20. System Tools (Kali)",
        "kind": "system_app",
        "os": "linux",
        "contact": "none",
        "parser": "amass_json",
        "applies_to": ["domain"],
        "tool": {
            "binary": "amass",
            "args": ["enum", "-passive", "-d", "{query}", "-json", "{outdir}/amass.json"],
            "output_format": "json",
            "output_file": "{outdir}/amass.json",
            "timeout": 300,
        },
    }

    def test_file_output_is_parsed_and_outdir_cleaned(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import estorides_core.system_app_sources as sas

        monkeypatch.setattr(sas, "tool_available", lambda _binary: True)
        seen: dict[str, Any] = {}

        def on_run(binary: str, args: list[str], **kw: Any) -> None:
            seen["args"] = args
            out_path = args[args.index("-json") + 1]
            Path(out_path).parent.mkdir(parents=True, exist_ok=True)
            Path(out_path).write_text(
                json.dumps(
                    {"name": "sub.example.com",
                     "domain": "example.com",
                     "addresses": [{"ip": "192.0.2.1", "cidr": "32", "asn": 64500}]}
                ) + "\n",
                encoding="utf-8",
            )

        result = execute(self.AMASS, "example.com", _runner=_stub_runner(on_run=on_run))

        assert result.success is True
        assert isinstance(result.parsed, list)
        assert result.parsed[0]["domain"] == "sub.example.com"
        outdir = str(Path(seen["args"][seen["args"].index("-json") + 1]).parent)
        assert not Path(outdir).exists()

    def test_stdout_json_is_parsed_when_no_file(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import estorides_core.system_app_sources as sas

        monkeypatch.setattr(sas, "tool_available", lambda _binary: True)
        src = dict(self.AMASS)
        src["tool"] = dict(self.AMASS["tool"])
        del src["tool"]["output_file"]
        src["tool"]["args"] = ["enum", "-passive", "-d", "{query}", "-json"]
        runner = _stub_runner(
            stdout='{"name": "a.example.com", "addresses": []}\n{"name": "b.example.com", "addresses": []}\n',
        )
        result = execute(src, "example.com", _runner=runner)
        assert [d["domain"] for d in result.parsed] == ["a.example.com", "b.example.com"]


# ---------------------------------------------------------------------------
# S6 · placeholders
# ---------------------------------------------------------------------------

class TestS6Placeholders:
    def test_query_and_outdir_substituted(self) -> None:
        out = render_args(["{query}", "--out", "{outdir}/r.json"], "example.com", "/opt/estorides/out")
        assert out == ["example.com", "--out", "/opt/estorides/out/r.json"]

    def test_unknown_tokens_survive(self) -> None:
        out = render_args(["{query}", "{env}"], "example.com", "/opt/estorides/out")
        assert out == ["example.com", "{env}"]

    def test_non_string_arg_raises(self) -> None:
        with pytest.raises(ValueError):
            render_args(["{query}", 42], "example.com", "/opt/estorides/out")  # type: ignore[list-item]


# ---------------------------------------------------------------------------
# S7 · contact ceiling
# ---------------------------------------------------------------------------

class TestS7ContactCeiling:
    def test_passive_only_drops_touching_tools_even_by_name(self) -> None:
        import estorides_core.orchestrator as orch_mod
        from estorides_core.orchestrator import Orchestrator

        orch = Orchestrator.__new__(Orchestrator)
        orch.registry = SourceRegistry(
            Path(__file__).resolve().parent.parent / "sources"
        )
        orch.registry.load()
        try:
            chosen = orch._select_sources(
                ["kali_dnsrecon", "kali_sherlock"],
                include_paid=True,
                query_type=None,
                max_contact="none",
            )
            names = {s["name"] for s in chosen}
            assert "kali_sherlock" in names
            assert "kali_dnsrecon" not in names
        finally:
            for holder in (
                getattr(orch_mod, "_fusion_store", None),
                getattr(orch_mod, "_entity_store", None),
                getattr(orch_mod, "case_store", None),
            ):
                if holder is not None and hasattr(holder, "close"):
                    holder.close()


# ---------------------------------------------------------------------------
# S8 · registry normalisation
# ---------------------------------------------------------------------------

class TestS8Registry:
    def _load(self, tmp_path: Path, yaml_text: str) -> SourceRegistry:
        d = tmp_path / "20_system_tools"
        d.mkdir(parents=True)
        (d / "t.yaml").write_text(yaml_text, encoding="utf-8")
        reg = SourceRegistry(tmp_path)
        reg.load()
        return reg

    YAML_BASE = """\
name: kali_test
enabled: true
category: 20. System Tools (Kali)
kind: system_app
contact: none
parser: sherlock_text
applies_to: [username]
tool:
  binary: sherlock
  args: ["{query}"]
  output_format: json
"""

    def test_kind_and_output_format_normalise(self, tmp_path: Path) -> None:
        reg = self._load(tmp_path, self.YAML_BASE)
        src = reg.get("kali_test")
        assert src is not None
        assert src["kind"] == "system_app"
        assert src["tool"]["output_format"] == "json"

    def test_kind_derived_from_binary_when_omitted(self, tmp_path: Path) -> None:
        reg = self._load(tmp_path, self.YAML_BASE.replace("kind: system_app\n", ""))
        src = reg.get("kali_test")
        assert src is not None and src["kind"] == "system_app"

    def test_http_source_gets_http_kind_by_default(self, tmp_path: Path) -> None:
        text = self.YAML_BASE.replace(
            "kind: system_app\n", ""
        ).replace(
            "tool:\n  binary: sherlock\n  args: [\"{query}\"]\n  output_format: json\n",
            "tool:\n  url: https://api.example.com/{query}\n",
        )
        reg = self._load(tmp_path, text)
        src = reg.get("kali_test")
        assert src is not None and src["kind"] == "http_api"

    def test_bad_output_format_falls_back_to_text(self, tmp_path: Path) -> None:
        reg = self._load(
            tmp_path, self.YAML_BASE.replace("output_format: json", "output_format: nonsense")
        )
        src = reg.get("kali_test")
        assert src is not None and src["tool"]["output_format"] == "text"

    def test_non_string_args_reset(self, tmp_path: Path) -> None:
        reg = self._load(
            tmp_path, self.YAML_BASE.replace('args: ["{query}"]', "args: [{query}, 42]")
        )
        src = reg.get("kali_test")
        assert src is not None and src["tool"]["args"] == []

    def test_unknown_kind_derives_from_block(self, tmp_path: Path) -> None:
        reg = self._load(tmp_path, self.YAML_BASE.replace("kind: system_app", "kind: weasel"))
        src = reg.get("kali_test")
        assert src is not None and src["kind"] == "system_app"

    def test_summary_exposes_kind(self, tmp_path: Path) -> None:
        reg = self._load(tmp_path, self.YAML_BASE)
        sources = reg.summary()["sources"]
        assert sources[0]["kind"] == "system_app"

    def test_real_kali_yamls_load_as_system_app(self) -> None:
        reg = SourceRegistry(Path(__file__).resolve().parent.parent / "sources")
        reg.load()
        from estorides_core.config import TOOL_ALLOWLIST

        names = [
            "kali_theharvester", "kali_amass", "kali_dnsrecon", "kali_dnsenum",
            "kali_fierce", "kali_sublist3r", "kali_dmitry", "kali_urlcrazy",
            "kali_sherlock", "kali_maigret", "kali_holehe", "kali_usufy",
            "kali_mailfy", "kali_phonefy", "kali_searchfy", "kali_metagoofil",
            "kali_whatweb", "kali_wafw00f", "kali_phoneinfoga",
        ]
        for name in names:
            src = reg.get(name)
            assert src is not None, f"{name} YAML missing or disabled"
            assert src["kind"] == "system_app", name
            assert src["tool"]["binary"] in TOOL_ALLOWLIST, name
            assert src["contact"] in ("none", "broker", "active"), name

    def test_write_source_file_roundtrip_keeps_system_app_block(self, tmp_path: Path) -> None:
        reg = SourceRegistry(tmp_path)
        path = reg.write_source_file(SHERLOCK_SOURCE)
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert doc["kind"] == "system_app"
        assert doc["tool"]["binary"] == "sherlock"
        assert doc["tool"]["args"] == SHERLOCK_SOURCE["tool"]["args"]


# ---------------------------------------------------------------------------
# ToolErrorResult passthrough
# ---------------------------------------------------------------------------

class TestRunnerErrorPassthrough:
    def test_timeout_error_is_propagated(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import estorides_core.system_app_sources as sas

        monkeypatch.setattr(sas, "tool_available", lambda _binary: True)

        def timeout_runner(binary: str, args: list[str], **kw: Any) -> ToolErrorResult:
            return ToolErrorResult(
                tool_name=binary,
                error_code="TOOL_TIMEOUT",
                message="tool exceeded 1s timeout",
                exit_code=None,
                duration_s=1.0,
            )

        result = execute(SHERLOCK_SOURCE, "testuser", _runner=timeout_runner)
        assert result.error_code == "TOOL_TIMEOUT"
        assert result.success is False
        assert result.parsed is None


# ---------------------------------------------------------------------------
# S9 · a slow system app never blocks the event loop
# ---------------------------------------------------------------------------

class TestS9LoopResponsiveness:
    def test_binary_branch_runs_in_worker_thread(
        self, monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        import asyncio
        import time as _time

        import estorides_core.system_app_sources as sas
        from estorides_core.orchestrator import Orchestrator
        from estorides_core.source_loader import Source

        def slow_execute(source: Any, query: str, **kw: Any) -> SystemAppResult:
            _time.sleep(0.6)
            return SystemAppResult(
                source_name=source["name"],
                tool_name="sherlock",
                success=True,
                exit_code=0,
                stdout="",
                stderr="",
                duration_s=0.6,
                parsed=[],
            )

        monkeypatch.setattr(sas, "execute", slow_execute)

        orch = Orchestrator.__new__(Orchestrator)
        source = Source(dict(SHERLOCK_SOURCE))
        timings: list[float] = []

        async def scenario() -> None:
            task = asyncio.create_task(
                orch._execute_source(None, source, "testuser")  # type: ignore[arg-type]
            )
            started = _time.monotonic()
            await asyncio.sleep(0.2)
            timings.append(_time.monotonic() - started)
            result = await task
            _s, parsed, raw, meta = result
            assert parsed == []
            assert meta.get("tool_binary") == "sherlock"

        asyncio.run(scenario())

        # The probe fired while slow_execute was still sleeping (0.6s): the
        # event loop stayed responsive. A blocking call would have pushed
        # the probe past the tool's return.
        assert timings[0] < 0.5
