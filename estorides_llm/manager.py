"""
estorides_llm.manager
=====================
Multi-backend LLM router with pluggable backends.

A `LLMBackend` is a small Protocol that knows how to talk to one
provider (ollama, openai, anthropic, openrouter, …). Backends register
themselves in `BACKENDS` and the manager walks the list in priority
order, returning the first successful response.

This is the registry pattern in place of the old if/elif chain that
hard-coded a method per backend. Adding a new provider is now: write
a class, `@register("name")` it, done. No edits to the manager.

System prompt lives in `intelligence_prompts.py` so multiple prompts
(BLUF, tactical, standard) can be selected per call without
forking the manager.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

import requests

from estorides_core.config import (ANTHROPIC_URL, LLM_MAX_TOKENS,
                                   LLM_MODELS, LLM_REQUEST_TIMEOUT,
                                   LLM_TEMPERATURE, OLLAMA_URL, OPENAI_URL,
                                   OPENROUTER_URL)
from estorides_llm.intelligence_prompts import SYSTEM_PROMPT, format_context

log = logging.getLogger("estorides.llm")


# ------------------------------------------------------------------- Protocol
class LLMBackend(Protocol):
    """Minimal contract for an LLM backend.

    Implementations MUST be total: raise on failure (the manager
    catches and moves on) or return ("", "") to signal "I can't
    answer, try the next backend".
    """
    name: str

    def __call__(
        self,
        prompt: str,
        context: Optional[List[Dict[str, Any]]],
        max_tokens: int,
        temperature: float,
        request_timeout: float,
    ) -> Tuple[str, str]:
        """Return (content, model_id). Empty content means "skip me"."""
        ...


# ------------------------------------------------------------------- registry
BACKENDS: Dict[str, LLMBackend] = {}
"""name -> backend instance. Populated by `@register` and module import."""


def register(name: str) -> Callable[[Any], LLMBackend]:
    """Decorator: register a backend under `name`.

    Accepts both an instance and a class. If a class is given, the
    decorator instantiates it with no arguments — which is the
    common case for stateless backends that hold no per-instance
    state. The class must therefore have a no-arg constructor.
    """
    def deco(backend_or_cls: Any) -> LLMBackend:
        backend: LLMBackend
        if isinstance(backend_or_cls, type):
            backend = backend_or_cls()
        else:
            backend = backend_or_cls
        if name in BACKENDS:
            log.debug("re-registering LLM backend %r", name)
        BACKENDS[name] = backend
        return backend
    return deco


# ------------------------------------------------------------------- builtins
@register("ollama")
class OllamaBackend:
    name = "ollama"

    def _resolve_model(self, request_timeout: float) -> str:
        """Pick a model ollama actually has pulled.

        Prefers the configured model; falls back to the first available
        tag so a stale config can't silently degrade every run to the
        stub. (Previous behaviour; preserved here.)
        """
        want = LLM_MODELS["ollama"]
        try:
            r = requests.get(
                f"{OLLAMA_URL.rstrip('/')}/api/tags",
                timeout=min(request_timeout, 3.0),
            )
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

    def __call__(self, prompt, context, max_tokens, temperature, request_timeout) -> Tuple[str, str]:
        model = self._resolve_model(request_timeout)
        url = f"{OLLAMA_URL.rstrip('/')}/api/generate"
        full = f"{SYSTEM_PROMPT}\n\n{format_context(context or [])}\n\nUser question: {prompt}"
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


class _OpenAICompatibleBackend:
    """Shared implementation for OpenAI-shaped APIs (openai, openrouter, …).

    Subclasses set `name`, `env_key`, and `base_url`."""
    name: str = ""
    env_key: str = ""
    base_url: str = ""

    def __call__(self, prompt, context, max_tokens, temperature, request_timeout) -> Tuple[str, str]:
        api_key = os.environ.get(self.env_key)
        if not api_key:
            raise RuntimeError(f"{self.env_key} not set")
        model = LLM_MODELS[self.name]
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": f"{format_context(context or [])}\n\nUser question: {prompt}"},
        ]
        try:
            r = requests.post(
                url,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages,
                      "max_tokens": max_tokens, "temperature": temperature},
                timeout=request_timeout,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip(), model
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"{self.base_url}: {e}") from e
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"{self.base_url}: malformed response: {e}") from e


@register("openai")
class OpenAIBackend(_OpenAICompatibleBackend):
    name = "openai"
    env_key = "OPENAI_API_KEY"
    base_url = OPENAI_URL


@register("openrouter")
class OpenRouterBackend(_OpenAICompatibleBackend):
    name = "openrouter"
    env_key = "OPENROUTER_API_KEY"
    base_url = OPENROUTER_URL


@register("anthropic")
class AnthropicBackend:
    name = "anthropic"

    def __call__(self, prompt, context, max_tokens, temperature, request_timeout) -> Tuple[str, str]:
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
                                  "content": f"{format_context(context or [])}\n\nUser question: {prompt}"}],
                },
                timeout=request_timeout,
            )
            r.raise_for_status()
            data = r.json()
            text = "".join(
                p.get("text", "") for p in data.get("content", []) if isinstance(p, dict)
            ).strip()
            return text, model
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"anthropic: {e}") from e


# ----------------------------------------------------------------- manager
# Priority order for backend selection. The manager walks this list
# (skipping disabled backends) and returns the first non-empty result.
DEFAULT_PRIORITY: Tuple[str, ...] = ("ollama", "openrouter", "anthropic", "openai")


class LLMManager:
    def __init__(self) -> None:
        self.disabled: set[str] = set(
            os.environ.get("ESTORIDES_DISABLE_BACKENDS", "").split(",")
        ) - {""}
        # Honour an explicit priority override (comma-separated) so an
        # operator can force "ollama first" or "openai first" without
        # recompiling the source.
        override = os.environ.get("ESTORIDES_BACKEND_PRIORITY", "").strip()
        if override:
            self.priority: Tuple[str, ...] = tuple(
                b.strip() for b in override.split(",") if b.strip()
            )
        else:
            self.priority = DEFAULT_PRIORITY

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

        `request_timeout` caps every backend's HTTP call so a slow
        local model cannot keep a worker thread alive past the
        orchestrator's deadline. Returns a dict with keys:
        backend, model, content, error.
        """
        for name in self.priority:
            if name in self.disabled:
                continue
            backend = BACKENDS.get(name)
            if backend is None:
                continue
            try:
                content, model = backend(prompt, context, max_tokens, temperature, request_timeout)
                if content:
                    return {
                        "backend": name,
                        "model": model,
                        "content": content,
                        "error": None,
                    }
            except Exception as e:  # noqa: BLE001
                log.warning("LLM backend %s failed: %s", name, e)
                continue
        return {
            "backend": "stub",
            "model": "stub",
            "content": self._stub_response(prompt, context),
            "error": "all backends failed",
        }

    # ----------------------------------------------------- stub fallback
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
