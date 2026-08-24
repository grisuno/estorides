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

import json
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

# Default auto-detection preference for local ollama models (used only when
# ESTORIDES_OLLAMA_MODEL is not set). Ordered best-to-worst: small/fast
# models go first so the first analysis answers promptly instead of falling
# through to the stub while a 27B model warms up. Override the whole thing
# with ESTORIDES_OLLAMA_MODEL to force a specific model (e.g. the big qwen
# for higher-quality assessments).
PREFERRED_OLLAMA_MODELS: tuple[str, ...] = (
    "deepseek-r1:1.5b",
    "llama3.2:3b",
    "llama3.1:8b",
    "qwen2.5:7b",
    "qwen3:8b",
    "phi3:mini",
)


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

    def stream_generate(
        self,
        prompt: str,
        context: Optional[List[Dict[str, Any]]],
        model: str,
        temperature: float,
        request_timeout: float,
    ) -> Any:
        """Optional: stream (kind, text) chunks. Base backends may skip."""
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

    @staticmethod
    def get_status() -> Dict[str, Any]:
        """Return available ollama models and reachability status."""
        try:
            r = requests.get(f"{OLLAMA_URL.rstrip('/')}/api/tags", timeout=3.0)
            r.raise_for_status()
            available = [m.get("name", "") for m in r.json().get("models", [])]
            return {"reachable": True, "models": available, "error": None}
        except requests.exceptions.RequestException as e:
            return {"reachable": False, "models": [], "error": str(e)}

    def _resolve_model(self, request_timeout: float) -> str:
        """Pick a model ollama actually has pulled.

        If ESTORIDES_OLLAMA_MODEL is set via env, use that (verify it's
        pulled). Otherwise auto-detect from /api/tags and use the first
        available model."""
        want = LLM_MODELS.get("ollama", "")
        try:
            r = requests.get(
                f"{OLLAMA_URL.rstrip('/')}/api/tags",
                timeout=min(request_timeout, 3.0),
            )
            r.raise_for_status()
            available = [m.get("name", "") for m in r.json().get("models", [])]
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"ollama unreachable at {OLLAMA_URL}. "
                f"Is ollama running? (error: {e})"
            ) from e
        if not available:
            raise RuntimeError(
                "ollama has no models pulled. "
                "Pull one with: ollama pull llama3.1:8b"
            )
        if want and want in available:
            return want
        if want:
            bare = {a.split(":")[0]: a for a in available}
            if want.split(":")[0] in bare:
                log.warning(
                    "ollama model %r not found, using %r instead",
                    want, bare[want.split(":")[0]],
                )
                return bare[want.split(":")[0]]
            raise RuntimeError(
                f"ollama model {want!r} not pulled and no matching base model "
                f"found. Available: {', '.join(available)}. "
                f"Pull it with: ollama pull {want}"
            )
        chosen = available[0]
        # Prefer a fast local model by default so the first answer is prompt.
        for pref in PREFERRED_OLLAMA_MODELS:
            for avail in available:
                if avail == pref or avail.split(":")[0] == pref.split(":")[0]:
                    chosen = avail
                    log.info(
                        "ollama: preferring fast model %r over %r (set "
                        "ESTORIDES_OLLAMA_MODEL to force another)",
                        chosen, available[0],
                    )
                    return chosen
        log.info("auto-detected ollama model: %r", chosen)
        return chosen

    def stream_generate(self, prompt, context, model, temperature, request_timeout):
        """Stream an ollama response as (kind, text) chunks.

        kind ∈ {"thinking", "content"} so the UI can render the model's
        reasoning preamble into a collapsible "thinking" panel and stream
        the final answer below it. Yields dicts, never raises; a hard
        ``request_timeout`` guards the whole stream.
        """
        url = f"{OLLAMA_URL.rstrip('/')}/api/generate"
        full = f"{SYSTEM_PROMPT}\n\n{format_context(context or [])}\n\nUser question: {prompt}"
        r = requests.post(
            url,
            json={
                "model": model,
                "prompt": full,
                "stream": True,
                "options": {"temperature": temperature, "num_predict": 8192},
            },
            timeout=request_timeout,
            stream=True,
        )
        r.raise_for_status()
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            done = obj.get("done", False)
            thinking = obj.get("thinking", "")
            if thinking:
                yield {"kind": "thinking", "text": thinking}
            resp = obj.get("response", "")
            if resp:
                yield {"kind": "content", "text": resp}
            if done:
                return

    def __call__(self, prompt, context, max_tokens, temperature, request_timeout) -> Tuple[str, str]:
        model = self._resolve_model(request_timeout)
        url = f"{OLLAMA_URL.rstrip('/')}/api/generate"
        full = f"{SYSTEM_PROMPT}\n\n{format_context(context or [])}\n\nUser question: {prompt}"
        for attempt, budget in ((1, max_tokens), (2, max(max_tokens, 512) * 2)):
            try:
                r = requests.post(
                    url,
                    json={
                        "model": model,
                        "prompt": full,
                        "stream": False,
                        "options": {"temperature": temperature, "num_predict": budget},
                    },
                    timeout=request_timeout,
                )
                r.raise_for_status()
                response = r.json().get("response", "").strip()
                if response:
                    return response, model
                # Reasoning models (deepseek-r1, qwen3) can burn the whole
                # token budget on their hidden "thinking" preamble and emit
                # an empty final answer. Retry once with a doubled budget
                # before declaring the model unusable.
                if attempt == 1:
                    log.info(
                        "ollama model %r returned empty with %d tokens; "
                        "retrying with %d", model, budget, max(max_tokens, 512) * 2,
                    )
                    continue
                raise RuntimeError(
                    f"model {model!r} returned no text even with a larger "
                    f"token budget — is it a generative model? "
                    f"(embedding-only models cannot answer; try `ollama pull llama3.1:8b`)"
                )
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

    def get_ollama_status(self) -> Dict[str, Any]:
        """Return ollama reachability and available models."""
        ollama = BACKENDS.get("ollama")
        if ollama is None:
            return {"reachable": False, "models": [], "error": "ollama backend not registered"}
        return ollama.get_status()

    # ----------------------------------------------------- streaming analysis
    def stream(
        self,
        prompt: str,
        *,
        context: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
        temperature: float = LLM_TEMPERATURE,
        request_timeout: float = LLM_REQUEST_TIMEOUT,
    ) -> Any:
        """Stream an analysis from a specific ollama model.

        Yields ``{"kind": "thinking"|"content", "text": …}`` chunks. The
        model name is treated as hostile: it must match an actual ollama
        model, else we raise before touching the network. If no model is
        given, we fall back to the auto-detected fast default.
        """
        ollama = BACKENDS.get("ollama")
        if ollama is None:
            raise RuntimeError("ollama backend not registered")
        status = ollama.get_status()
        if not status.get("reachable"):
            raise RuntimeError(f"ollama unreachable: {status.get('error')}")
        available = status.get("models") or []
        if model:
            if model not in available:
                raise RuntimeError(
                    f"model {model!r} not available on ollama. "
                    f"Available: {', '.join(available)}"
                )
        else:
            model = ollama._resolve_model(request_timeout)  # noqa: SLF001
        yield from ollama.stream_generate(
            prompt, context or [], model, temperature, request_timeout,
        )

    # ----------------------------------------------------- stub fallback
    def _stub_response(self, prompt: str, context: Optional[List[Dict[str, Any]]]) -> str:
        n = len(context or [])
        srcs = sorted({s.get("source", "?") for s in (context or [])})
        return (
            f"[Stub LLM — no backends available]\n\n"
            f"Query: {prompt}\n"
            f"Sources collected: {n} ({', '.join(srcs[:15])}{'...' if len(srcs) > 15 else ''}).\n\n"
            f"To enable analysis, either:\n"
            f"  1. Start ollama and pull a model:\n"
            f"     $ ollama serve\n"
            f"     $ ollama pull llama3.1:8b\n"
            f"  2. Or set a cloud API key:\n"
            f"     $ export OPENAI_API_KEY=sk-...\n"
            f"     $ export ANTHROPIC_API_KEY=sk-ant-...\n"
            f"     $ export OPENROUTER_API_KEY=sk-or-...\n"
        )
