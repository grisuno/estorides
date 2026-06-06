"""
estorides_llm.manager
====================
Multi-backend LLM router.

Priority: ollama (local) → openrouter (free + paid) → anthropic → openai → stub.
Each backend is tried in order; first success wins. A real backends can be
enabled/disabled via env (set ESTORIDES_DISABLE_BACKENDS=anthropic,openai).
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

from estorides_core.config import (ANTHROPIC_URL, LLM_BACKENDS, LLM_MAX_TOKENS,
                                   LLM_MODELS, LLM_REQUEST_TIMEOUT,
                                   LLM_TEMPERATURE, OLLAMA_URL, OPENAI_URL,
                                   OPENROUTER_URL)

log = logging.getLogger("estorides.llm")


SYSTEM_PROMPT = """You are Estorides, an elite OSINT analyst working in the style of
Bellingcat, Citizen Lab, and Palantir. You reason over structured
multi-source intelligence and produce factual, citation-backed
assessments. When a piece of evidence is uncertain, you say so. You
never fabricate sources. You surface surprising relationships, not the
obvious ones. You write for a senior intelligence consumer."""


def _format_context(sources: List[Dict[str, Any]]) -> str:
    blocks = []
    for s in sources:
        src = s.get("source", "unknown")
        cat = s.get("category", "")
        body = s.get("parsed") if s.get("parsed") is not None else s.get("raw")
        body_text = json.dumps(body, ensure_ascii=False, default=str)[:3500]
        blocks.append(f"=== {src} [{cat}] ===\n{body_text}")
    return "\n\n".join(blocks)


class LLMManager:
    def __init__(self) -> None:
        self.disabled: set[str] = set(
            os.environ.get("ESTORIDES_DISABLE_BACKENDS", "").split(",")
        ) - {""}

    # ----------------------------------------------------- public: generate
    def generate(
        self,
        prompt: str,
        *,
        context: Optional[List[Dict[str, Any]]] = None,
        max_tokens: int = LLM_MAX_TOKENS,
        temperature: float = LLM_TEMPERATURE,
        request_timeout: float = LLM_REQUEST_TIMEOUT,
    ) -> Dict[str, Any]:
        """Try each backend in priority order; return the first that succeeds.

        `request_timeout` caps every backend's HTTP call so a slow local model
        cannot keep a worker thread alive past the orchestrator's deadline.
        Returns a dict with keys: backend, model, content, error."""
        for backend in LLM_BACKENDS:
            if backend in self.disabled:
                continue
            try:
                content, model = self._call(
                    backend, prompt, context, max_tokens, temperature, request_timeout
                )
                if content:
                    return {
                        "backend": backend,
                        "model": model,
                        "content": content,
                        "error": None,
                    }
            except Exception as e:  # noqa: BLE001
                log.warning("LLM backend %s failed: %s", backend, e)
                continue
        return {
            "backend": "stub",
            "model": "stub",
            "content": self._stub_response(prompt, context),
            "error": "all backends failed",
        }

    # ----------------------------------------------------- private: per-bk
    def _call(
        self,
        backend: str,
        prompt: str,
        context: Optional[List[Dict[str, Any]]],
        max_tokens: int,
        temperature: float,
        request_timeout: float,
    ) -> tuple[str, str]:
        if backend == "ollama":
            return self._ollama(prompt, context, max_tokens, temperature, request_timeout)
        if backend == "openrouter":
            return self._openrouter_compatible(
                OPENROUTER_URL, "OPENROUTER_API_KEY", prompt, context, max_tokens, temperature,
                model=LLM_MODELS["openrouter"], request_timeout=request_timeout,
            )
        if backend == "anthropic":
            return self._anthropic(prompt, context, max_tokens, temperature, request_timeout)
        if backend == "openai":
            return self._openrouter_compatible(
                OPENAI_URL, "OPENAI_API_KEY", prompt, context, max_tokens, temperature,
                model=LLM_MODELS["openai"], request_timeout=request_timeout,
            )
        return "", "unknown"

    # ---- ollama (local) ----
    def _resolve_ollama_model(self, request_timeout: float) -> str:
        """Return a model that ollama actually has pulled.

        Prefers the configured model; if it isn't installed, falls back to the
        first available tag so a stale ESTORIDES_OLLAMA_MODEL can't silently
        send every run to the stub."""
        want = LLM_MODELS["ollama"]
        try:
            r = requests.get(f"{OLLAMA_URL.rstrip('/')}/api/tags",
                             timeout=min(request_timeout, 3.0))
            r.raise_for_status()
            available = [m.get("name", "") for m in r.json().get("models", [])]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"ollama unreachable: {e}") from e
        if not available:
            raise RuntimeError("ollama has no models pulled")
        if want in available:
            return want
        bare = {a.split(":")[0]: a for a in available}
        if want.split(":")[0] in bare:
            return bare[want.split(":")[0]]
        log.warning("ollama model %s not installed; using %s instead", want, available[0])
        return available[0]

    def _ollama(self, prompt, context, max_tokens, temperature, request_timeout) -> tuple[str, str]:
        model = self._resolve_ollama_model(request_timeout)
        url = f"{OLLAMA_URL.rstrip('/')}/api/generate"
        full = f"{SYSTEM_PROMPT}\n\n{_format_context(context or [])}\n\nUser question: {prompt}"
        try:
            r = requests.post(
                url,
                json={
                    "model": model,
                    "prompt": full,
                    "stream": False,
                    "options": {"temperature": temperature, "num_predict": max_tokens},
                },
                timeout=request_timeout,
            )
            r.raise_for_status()
            response = r.json().get("response", "").strip()
            if not response:
                raise RuntimeError(
                    f"model {model!r} returned no text — is it a generative model? "
                    f"(embedding-only models cannot answer; try `ollama pull llama3.1:8b`)"
                )
            return response, model
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"ollama: {e}") from e

    # ---- openai / openrouter (OpenAI-compatible) ----
    def _openrouter_compatible(self, base_url, env_key, prompt, context, max_tokens,
                               temperature, model, request_timeout) -> tuple[str, str]:
        api_key = os.environ.get(env_key)
        if not api_key:
            raise RuntimeError(f"{env_key} not set")
        url = f"{base_url.rstrip('/')}/chat/completions"
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{_format_context(context or [])}\n\nUser question: {prompt}"},
        ]
        try:
            r = requests.post(
                url,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages, "max_tokens": max_tokens,
                      "temperature": temperature},
                timeout=request_timeout,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip(), model
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"{base_url}: {e}") from e
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"{base_url}: malformed response: {e}") from e

    # ---- anthropic (separate shape) ----
    def _anthropic(self, prompt, context, max_tokens, temperature, request_timeout) -> tuple[str, str]:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        model = LLM_MODELS["anthropic"]
        url = f"{ANTHROPIC_URL.rstrip('/')}/messages"
        try:
            r = requests.post(
                url,
                headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                         "Content-Type": "application/json"},
                json={
                    "model": model,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "system": SYSTEM_PROMPT,
                    "messages": [{"role": "user",
                                  "content": f"{_format_context(context or [])}\n\nUser question: {prompt}"}],
                },
                timeout=request_timeout,
            )
            r.raise_for_status()
            data = r.json()
            text = "".join(p.get("text", "") for p in data.get("content", []) if isinstance(p, dict)).strip()
            return text, model
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"anthropic: {e}") from e

    # ---- stub fallback (no API) ----
    def _stub_response(self, prompt: str, context: Optional[List[Dict[str, Any]]]) -> str:
        n = len(context or [])
        srcs = sorted({s.get("source", "?") for s in (context or [])})
        return (
            f"[Stub LLM — set ESTORIDES_OLLAMA_URL or API keys for real analysis]\n\n"
            f"Query: {prompt}\n\n"
            f"Pulled {n} sources: {', '.join(srcs)}.\n\n"
            f"Install or configure a backend:\n"
            f"  ollama:    pip install ollama + ollama pull llama3.1:8b\n"
            f"  openai:    export OPENAI_API_KEY=...\n"
            f"  anthropic: export ANTHROPIC_API_KEY=...\n"
            f"  openrouter:export OPENROUTER_API_KEY=...\n"
        )
