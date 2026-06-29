"""Encrypted export: plaintext must be removed after encryption.

Issue #8 reported that `export_stix_encrypted` and `export_misp_encrypted`
left a plaintext STIX/MISP bundle on disk in `reports/`. The fix is to
delete the plaintext in a `finally` block so it always goes away, even
when encryption fails. The `age` binary is mocked in these tests so the
suite is hermetic.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import patch

import pytest

from estorides_core.entity_extraction import Entity
from estorides_core.knowledge_graph import KnowledgeGraph


class _FakeCompleted:
    def __init__(self, rc: int = 0, stderr: bytes = b"") -> None:
        self.returncode = rc
        self.stderr = stderr


def _kg_with_one_node() -> KnowledgeGraph:
    kg = KnowledgeGraph()
    kg.add_entity(Entity(type="ip", value="1.1.1.1", source="unit-test"))
    return kg


def _patch_age_ok():
    """Pretend `age` is on PATH and that `age -e -r ...` produced ciphertext."""
    def _run(cmd, stdin, stdout, stderr, check):
        stdout.write(b"fake-ciphertext-bytes")
        return _FakeCompleted(rc=0)
    return patch("subprocess.run", side_effect=_run), patch(
        "estorides_export.encryption.shutil.which", return_value="/usr/bin/age"
    )


def test_stix_encrypted_removes_plaintext(tmp_path):
    from estorides_export.encryption import export_stix_encrypted
    plain_path = tmp_path / "bundle_test.json"
    with _patch_age_ok()[0], _patch_age_ok()[1]:
        out = export_stix_encrypted(_kg_with_one_node(), "age1qqqq", plain_path)
    assert out.exists()
    assert not plain_path.exists()


def test_misp_encrypted_removes_plaintext(tmp_path):
    from estorides_export.encryption import export_misp_encrypted
    plain_path = tmp_path / "event_test.json"
    with _patch_age_ok()[0], _patch_age_ok()[1]:
        out = export_misp_encrypted(_kg_with_one_node(), "age1qqqq", plain_path)
    assert out.exists()
    assert not plain_path.exists()


def test_stix_encrypted_removes_plaintext_on_failure(tmp_path):
    """Even when age fails, the plaintext must be removed."""
    from estorides_export.encryption import export_stix_encrypted
    plain_path = tmp_path / "bundle_fail.json"

    def _run_fail(cmd, stdin, stdout, stderr, check):
        return _FakeCompleted(rc=1, stderr=b"boom")

    with patch("subprocess.run", side_effect=_run_fail), patch(
        "estorides_export.encryption.shutil.which", return_value="/usr/bin/age"
    ):
        with pytest.raises(RuntimeError):
            export_stix_encrypted(_kg_with_one_node(), "age1qqqq", plain_path)
    assert not plain_path.exists()
