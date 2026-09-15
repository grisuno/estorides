# Subsystem: estorides_llm

## estorides_llm/__init__.py
- Layer: utility
- Language: py
- Depends on: `estorides_llm/manager.py`

## estorides_llm/intelligence_prompts.py
- Layer: utility
- Language: py
- Symbols:
  - `format_context` (function, line 97) `def format_context(sources)`
- Imported by: `estorides_llm/manager.py`

## estorides_llm/manager.py
- Layer: utility
- Language: py
- Symbols:
  - `LLMBackend` (class, line 60) `class LLMBackend(Protocol)`
  - `register` (method, line 97) `def register(name)`
  - `OllamaBackend` (class, line 120) `class OllamaBackend`
  - `_OpenAICompatibleBackend` (class, line 266) `class _OpenAICompatibleBackend`
  - `OpenAIBackend` (class, line 302) `class OpenAIBackend(_OpenAICompatibleBackend)`
  - `OpenRouterBackend` (class, line 309) `class OpenRouterBackend(_OpenAICompatibleBackend)`
  - `AnthropicBackend` (class, line 316) `class AnthropicBackend`
  - `LLMManager` (class, line 356) `class LLMManager`
  - `__call__` (method, line 69) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `stream_generate` (method, line 80) `def stream_generate(self, prompt, context, model, temperature, request_timeout)`
  - `deco` (method, line 105) `def deco(backend_or_cls)`
  - `get_status` (method, line 124) `def get_status()`
  - `_resolve_model` (method, line 134) `def _resolve_model(self, request_timeout)`
  - `stream_generate` (method, line 188) `def stream_generate(self, prompt, context, model, temperature, request_timeout)`
  - `__call__` (method, line 227) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `__call__` (method, line 274) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `__call__` (method, line 319) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
  - `__init__` (method, line 357) `def __init__(self)`
  - `generate` (method, line 373) `def generate(self, prompt)`
  - `get_ollama_status` (method, line 414) `def get_ollama_status(self)`
  - `stream` (method, line 422) `def stream(self, prompt)`
  - `_stub_response` (method, line 459) `def _stub_response(self, prompt, context)`
- Depends on: `estorides_core/config.py`, `estorides_llm/intelligence_prompts.py`
- Imported by: `estorides_llm/__init__.py`
