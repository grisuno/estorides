# Subsystem: estorides_llm

## estorides_llm/__init__.py
- Layer: utility
- Language: py
- Depends on: `estorides_llm/manager.py`

## estorides_llm/intelligence_prompts.py
- Layer: utility
- Language: py
- Symbols:
  - `format_context` (function, line 98) `def format_context(sources)`
- Imported by: `estorides_llm/manager.py`

## estorides_llm/manager.py
- Layer: utility
- Language: py
- Symbols:
  - `LLMBackend` (class, line 53) `class LLMBackend(Protocol)`
  - `register` (method, line 90) `def register(name)`
  - `OllamaBackend` (class, line 113) `class OllamaBackend`
  - `_OpenAICompatibleBackend` (class, line 259) `class _OpenAICompatibleBackend`
  - `OpenAIBackend` (class, line 295) `class OpenAIBackend(_OpenAICompatibleBackend)`
  - `OpenRouterBackend` (class, line 302) `class OpenRouterBackend(_OpenAICompatibleBackend)`
  - `AnthropicBackend` (class, line 309) `class AnthropicBackend`
  - `LLMManager` (class, line 349) `class LLMManager`
  - `__call__` (method, line 62) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `stream_generate` (method, line 73) `def stream_generate(self, prompt, context, model, temperature, request_timeout)`
  - `deco` (method, line 98) `def deco(backend_or_cls)`
  - `get_status` (method, line 117) `def get_status()`
  - `_resolve_model` (method, line 127) `def _resolve_model(self, request_timeout)`
  - `stream_generate` (method, line 181) `def stream_generate(self, prompt, context, model, temperature, request_timeout)`
  - `__call__` (method, line 220) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `__call__` (method, line 267) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `__call__` (method, line 312) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `__init__` (method, line 350) `def __init__(self)`
  - `generate` (method, line 366) `def generate(self, prompt)`
  - `get_ollama_status` (method, line 407) `def get_ollama_status(self)`
  - `stream` (method, line 415) `def stream(self, prompt)`
  - `_stub_response` (method, line 451) `def _stub_response(self, prompt, context)`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`
