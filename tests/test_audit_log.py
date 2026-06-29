"""AuditLog rotation: file size cap, in-place .N rotation (issue #48)."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from estorides_core.audit import AuditEvent, AuditLog


def _ev(ts: str = "2026-06-29T00:00:00Z") -> AuditEvent:
    return AuditEvent(
        timestamp=ts,
        event="test",
        remote_ip="127.0.0.1",
        method="GET",
        path="/api/test",
    )


def test_audit_log_appends(tmp_path):
    log = AuditLog(tmp_path / "audit.jsonl")
    log._max_bytes = 0  # disable rotation for this test
    log.record(_ev())
    log.record(_ev())
    lines = (tmp_path / "audit.jsonl").read_text().strip().splitlines()
    assert len(lines) == 2


def test_audit_log_rotates_when_cap_exceeded(tmp_path):
    path = tmp_path / "audit.jsonl"
    log = AuditLog(path)
    # Tiny cap so the next write triggers rotation.
    log._max_bytes = 100
    # Pre-fill past the cap.
    path.write_text("x" * 200 + "\n")
    log.record(_ev("2026-06-29T00:00:01Z"))
    # The original (200-byte) file was rotated to .1; the active file
    # is now a fresh JSON line of normal size.
    assert (tmp_path / "audit.jsonl.1").exists()
    assert (tmp_path / "audit.jsonl.1").stat().st_size >= 200
    assert path.exists()
    # The active file should be much smaller than the rotation.
    assert path.stat().st_size < 300


def test_audit_log_rotation_respects_keep_count(tmp_path):
    path = tmp_path / "audit.jsonl"
    log = AuditLog(path)
    log._max_bytes = 50
    log._keep_rotations = 2
    for i in range(5):
        path.write_text("x" * 100)  # force rotation
        log.record(_ev(f"2026-06-29T00:00:0{i}Z"))
    # Only .1 and .2 should exist; .3 (and beyond) was dropped.
    assert (tmp_path / "audit.jsonl.1").exists() or (tmp_path / "audit.jsonl.2").exists()
    assert not (tmp_path / "audit.jsonl.3").exists()


def test_audit_log_no_rotation_when_disabled(tmp_path):
    path = tmp_path / "audit.jsonl"
    log = AuditLog(path)
    log._max_bytes = 0  # 0 disables rotation
    path.write_text("x" * 10_000)  # way over a normal cap
    log.record(_ev())
    assert not (tmp_path / "audit.jsonl.1").exists()
    # The file is still over the (hypothetical) cap because rotation is off.
    assert path.stat().st_size > 10_000
