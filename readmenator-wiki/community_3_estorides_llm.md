# estorides_llm

*Community 3 | 3 files | cohesion 0.67*

## Definition

This community groups 3 file(s) rooted at `estorides_llm` with dominant language py (cohesion 0.67). Central symbols: `AnthropicBackend`, `LLMBackend`, `LLMManager`, `OllamaBackend`, `OpenAIBackend`, `OpenRouterBackend`, `_OpenAICompatibleBackend`, `__call__`. Core file: `estorides_llm/manager.py` (22 symbols). Documented purpose: estorides_llm.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `estorides_llm/__init__.py` | py | utility | 0 | yes |
| `estorides_llm/intelligence_prompts.py` | py | utility | 1 | yes |
| `estorides_llm/manager.py` | py | utility | 22 | yes |

## Key Symbols

- `format_context` (function, `estorides_llm/intelligence_prompts.py:97`) `def format_context(sources)` - Render a list of observation dicts into a context block for the LLM.
- `LLMBackend` (class, `estorides_llm/manager.py:60`) `class LLMBackend(Protocol)` - Minimal contract for an LLM backend.
- `__call__` (method, `estorides_llm/manager.py:69`) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)` - Return (content, model_id). Empty content means "skip me".
- `stream_generate` (method, `estorides_llm/manager.py:80`) `def stream_generate(self, prompt, context, model, temperature, request_timeout)` - Optional: stream (kind, text) chunks. Base backends may skip.
- `register` (method, `estorides_llm/manager.py:97`) `def register(name)` - Decorator: register a backend under `name`.
- `deco` (method, `estorides_llm/manager.py:105`) `def deco(backend_or_cls)`
- `OllamaBackend` (class, `estorides_llm/manager.py:120`) `class OllamaBackend`
- `get_status` (method, `estorides_llm/manager.py:124`) `def get_status()` - Return available ollama models and reachability status.
- `_resolve_model` (method, `estorides_llm/manager.py:134`) `def _resolve_model(self, request_timeout)` - Pick a model ollama actually has pulled.
- `stream_generate` (method, `estorides_llm/manager.py:188`) `def stream_generate(self, prompt, context, model, temperature, request_timeout)` - Stream an ollama response as (kind, text) chunks.
- `__call__` (method, `estorides_llm/manager.py:227`) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `_OpenAICompatibleBackend` (class, `estorides_llm/manager.py:266`) `class _OpenAICompatibleBackend` - Shared implementation for OpenAI-shaped APIs (openai, openrouter, …).
- `__call__` (method, `estorides_llm/manager.py:274`) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `OpenAIBackend` (class, `estorides_llm/manager.py:302`) `class OpenAIBackend(_OpenAICompatibleBackend)`
- `OpenRouterBackend` (class, `estorides_llm/manager.py:309`) `class OpenRouterBackend(_OpenAICompatibleBackend)`
- `AnthropicBackend` (class, `estorides_llm/manager.py:316`) `class AnthropicBackend`
- `__call__` (method, `estorides_llm/manager.py:319`) `def __call__(self, prompt, context, max_tokens, temperature, request_timeout)`
- `LLMManager` (class, `estorides_llm/manager.py:356`) `class LLMManager`
- `__init__` (method, `estorides_llm/manager.py:357`) `def __init__(self)`
- `generate` (method, `estorides_llm/manager.py:373`) `def generate(self, prompt)` - Try each backend in priority order; return the first that succeeds.
- `get_ollama_status` (method, `estorides_llm/manager.py:414`) `def get_ollama_status(self)` - Return ollama reachability and available models.
- `stream` (method, `estorides_llm/manager.py:422`) `def stream(self, prompt)` - Stream an analysis from a specific ollama model.
- `_stub_response` (method, `estorides_llm/manager.py:459`) `def _stub_response(self, prompt, context)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 2
- Cross-boundary resolved imports (EXTRACTED): 1

## Connections

- [EXTRACTED] depends_on community 3 <-> 0 (strength 0.9): Extracted import edge crosses communities: estorides_llm/manager.py imports estorides_core/config.py.
- [INFERRED] shares_context community 1 <-> 3 (strength 0.5): Inferred shared context (language py) with no import path between community 1 (estorides_core) and community 3 (estorides_llm).
- [INFERRED] shares_context community 2 <-> 3 (strength 0.5): Inferred shared context (language py) with no import path between community 2 (tests/properties) and community 3 (estorides_llm).
- [INFERRED] shares_context community 3 <-> 4 (strength 0.5): Inferred shared context (language py) with no import path between community 3 (estorides_llm) and community 4 (orphans).
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/__init__.py reaches tests/properties/test_change_detection_properties.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/__init__.py reaches tests/properties/test_hypothesis_engine_properties.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/__init__.py reaches tests/test_recon_report.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/intelligence_prompts.py reaches tests/properties/test_change_detection_properties.py in 6 hops.
- [INFERRED] bridges community 3 <-> 0 (strength 0.4): Inferred cross-community bridge: estorides_llm/intelligence_prompts.py reaches tests/properties/test_hypothesis_engine_properties.py in 6 hops.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in estorides_llm changed?
- Should estorides_llm be split, given cohesion 0.67?

## Sources

- `estorides_llm/__init__.py`
- `estorides_llm/intelligence_prompts.py`
- `estorides_llm/manager.py`
