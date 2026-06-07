"""
estorides_export.encryption
===========================
Optional age-encrypted report export.

The default export path produces STIX / MISP / GraphML as plaintext
JSON on disk, which is fine for a local single-user install. For
deployments where the report itself is the deliverable (analyst
hands a file to a customer, regulator, court), the file should be
encrypted at rest with a recipient's public key.

This module wraps the optional `age` encryption tool (`age` is a
modern, audited replacement for gpg; the binary is `age` from
https://age-encryption.org). If `age` is not on PATH the export
falls back to a plaintext file and logs a warning — never to a
broken file. This is the "graceful degradation" posture: the
operator decides whether encryption is required by whether the
recipient public key is set.

Three entry points:

  encrypt_file(plaintext_path, recipient_pubkey) -> ciphertext_path
    Encrypts a single file to a recipient's age public key. The
    resulting file is `<name>.age` next to the original. Returns
    the ciphertext path.

  export_stix_encrypted(kg, recipient_pubkey, path) -> ciphertext_path
  export_misp_encrypted(kg, recipient_pubkey, path) -> ciphertext_path
    Composed: build the bundle, write to a tempfile, encrypt in
    place, return the .age path.

A recipient public key looks like `age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p`.
"""
from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any

from estorides_core.knowledge_graph import KnowledgeGraph

log = logging.getLogger("estorides.export.encryption")


def _have_age() -> bool:
    return shutil.which("age") is not None


def encrypt_file(plaintext_path: Path, recipient_pubkey: str) -> Path:
    """Encrypt `plaintext_path` to `<plaintext_path>.age` for the recipient.

    Returns the ciphertext path. Raises RuntimeError if `age` is
    missing or the encryption subprocess fails — the orchestrator
    catches and falls back to plaintext. Raises ValueError if
    `recipient_pubkey` doesn't look like an age public key.

    Validation order is: key shape (cheap, no exec) → binary
    presence (filesystem stat) → subprocess. A malformed key is
    always a programmer error and surfaces as ValueError; a missing
    binary is an environment problem and surfaces as RuntimeError.
    """
    if not recipient_pubkey.startswith("age1"):
        raise ValueError(
            f"recipient public key must start with 'age1', got {recipient_pubkey!r}"
        )
    if not _have_age():
        raise RuntimeError(
            "`age` binary not found on PATH. Install from "
            "https://age-encryption.org or use plaintext export."
        )
    src = Path(plaintext_path)
    dst = src.with_suffix(src.suffix + ".age")
    try:
        # `age -e -r <pubkey>` reads plaintext from stdin and writes
        # ciphertext to stdout — the right shape for non-trusting
        # local-only execution.
        with src.open("rb") as fh_in, dst.open("wb") as fh_out:
            proc = subprocess.run(
                ["age", "-e", "-r", recipient_pubkey],
                stdin=fh_in,
                stdout=fh_out,
                stderr=subprocess.PIPE,
                check=False,
            )
        if proc.returncode != 0:
            try:
                dst.unlink()
            except OSError:
                pass
            raise RuntimeError(f"age encrypt failed: {proc.stderr.decode(errors='replace')}")
    except FileNotFoundError as e:
        raise RuntimeError(f"age binary disappeared mid-run: {e}") from e
    log.info("encrypted %s -> %s (size %d -> %d bytes)",
             src, dst, src.stat().st_size, dst.stat().st_size)
    return dst


def export_stix_encrypted(
    kg: KnowledgeGraph,
    recipient_pubkey: str,
    path: Path,
) -> Path:
    """Build the STIX bundle, write to disk, encrypt to <path>.age.

    `path` is the plaintext filename; the returned path is the
    encrypted artefact next to it."""
    from estorides_export import export_stix  # local import to avoid cycle
    plain = export_stix(kg, path=path)
    return encrypt_file(plain, recipient_pubkey)


def export_misp_encrypted(
    kg: KnowledgeGraph,
    recipient_pubkey: str,
    path: Path,
) -> Path:
    from estorides_export import export_misp
    plain = export_misp(kg, path=path)
    return encrypt_file(plain, recipient_pubkey)
