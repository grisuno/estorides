# `estorides_llm.intelligence_prompts`

> Source: [estorides_llm/intelligence_prompts.py:1](../../estorides_llm/intelligence_prompts.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides_llm.intelligence_prompts ================================== System prompt and context-formatting helpers for the LLM analyst.

The system prompt is the single most important piece of text in
the whole stack. It is what turns "a wall of OSINT JSON" into
"a Palantir-grade intelligence brief". The previous version was a
six-line paragraph that read like a CV; this one is structured
the way senior analysts actually brief:

  * Persona is set first and never compromised
  * Output format is prescribed (BLUF, confidence-graded findings,
    recommended actions)
  * Hard constraints are explicit (no fabrication, citation required,
    "I don't know" is acceptable)

Three prompt flavours are exposed:

  * SYSTEM_PROMPT — default, used by the orchestrator
  * BLUF_PROMPT   — strict 1-paragraph + confidence-graded findings
  * TACTICAL_PROMPT — operator-grade with Course of Action (COA)
    recommendations

The chosen prompt is selected via the `prompt_style` argument to
[`LLMManager.generate`](estorides_llm.manager.py.md#llmmanager-generate). Backends that ignore the prompt style
are not affected; the new behaviour is opt-in for callers that
care.

## Contents

- **Functions:** [`format_context`](#format_context)
- **Constants:** [`SYSTEM_PROMPT`](#system_prompt), [`BLUF_PROMPT`](#bluf_prompt), [`TACTICAL_PROMPT`](#tactical_prompt), [`PROMPTS`](#prompts)

## Functions

<a id="format_context"></a>

### `format_context`

`function` | [estorides_llm/intelligence_prompts.py:97](../../estorides_llm/intelligence_prompts.py#L97)

```python
def format_context(sources: list[dict[str, Any]], *, max_chars_per_source: int = 3500, max_total_chars: int = 100000) -> str
```

Render a list of observation dicts into a context block for the LLM.

The previous implementation truncated at 3500 chars but did not
preserve source ordering, so a re-run produced a different prompt
and a different answer. This version sorts by source name (stable
order) and truncates per source so a single 100KB crt.sh response
cannot blow past the model's context window.

A hard ``max_total_chars`` cap bounds the WHOLE block. Without it a
wide run (dozens of sources) could produce a prompt that dwarfs the
model's context window, and the model would only see the first blocks
— silently dropping the data it actually needs to answer. The cap is
applied in source order so the assessment never goes blind on a large
collection.

If the orchestrator has stamped an ontology verdict on an
observation (the [`ontology`](estorides_core.observation_models.py.md#observation-ontology) key), the formatted block carries a
one-line "SANCTIONED — OFAC SDN match on <fields>" warning that
the LLM is required to surface in its assessment.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `sources` | `list[dict[str, Any]]` |  |  |
| `max_chars_per_source` | `int` | `3500` |  |
| `max_total_chars` | `int` | `100000` |  |

**Returns:** `str`

*Called by:* [`AnthropicBackend.__call__`](estorides_llm.manager.py.md#anthropicbackend-__call__), [`OllamaBackend.__call__`](estorides_llm.manager.py.md#ollamabackend-__call__), [`OllamaBackend.stream_generate`](estorides_llm.manager.py.md#ollamabackend-stream_generate)

---

## Constants

<a id="system_prompt"></a>

### `SYSTEM_PROMPT`

`constant` | [estorides_llm/intelligence_prompts.py:35](../../estorides_llm/intelligence_prompts.py#L35)

```python
SYSTEM_PROMPT
```

---

<a id="bluf_prompt"></a>

### `BLUF_PROMPT`

`constant` | [estorides_llm/intelligence_prompts.py:66](../../estorides_llm/intelligence_prompts.py#L66)

```python
BLUF_PROMPT
```

---

<a id="tactical_prompt"></a>

### `TACTICAL_PROMPT`

`constant` | [estorides_llm/intelligence_prompts.py:76](../../estorides_llm/intelligence_prompts.py#L76)

```python
TACTICAL_PROMPT
```

---

<a id="prompts"></a>

### `PROMPTS`

`constant` | [estorides_llm/intelligence_prompts.py:90](../../estorides_llm/intelligence_prompts.py#L90)

```python
PROMPTS: dict[str, str] = {'system': SYSTEM_PROMPT, 'bluf': BLUF_PROMPT, 'tactical': TACTICAL_PROMPT}
```

---
