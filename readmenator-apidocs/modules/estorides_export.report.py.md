# `estorides_export.report`

> Source: [estorides_export/report.py:1](../../estorides_export/report.py#L1) | language `py` | coverage 100.0% | [API index](../index.md)

estorides_export.report =======================

Markdown report generation for finished cases.

Design choices
--------------
* Pure function. The report builder takes a case dict + a list of
  entities + (optionally) a previous case id, and returns a Markdown
  string. No I/O happens here — the caller (CLI, web, scheduled job)
  decides where the report lands. This keeps the formatter unit-
  testable in isolation.
* Progressive disclosure. The first 30 lines carry the TL;DR so a
  reviewer can decide in 10 seconds whether the case is worth a deep
  read. Full IOCs and source roster come after a `---` separator.
* Diff support. When `previous_case_id` is supplied, the report
  includes a "what's new since last run" section that mirrors
  [`CaseStore.diff_entities`](estorides_core.cases.py.md#casestore-diff_entities) — same keys, no double bookkeeping.
* No LLM dependency. A separate LLM-narrative step can be wired on
  top, but the baseline report must work even when no LLM backend
  is configured (the engine returns a stub analysis in that case).

## Contents

- **Functions:** [`render_markdown_report`](#render_markdown_report)

## Functions

<a id="render_markdown_report"></a>

### `render_markdown_report`

`function` | [estorides_export/report.py:196](../../estorides_export/report.py#L196)

```python
def render_markdown_report(case: Dict[str, Any], entities: Optional[List[Dict[str, Any]]] = None, sources_queried: int = 0, sources_succeeded: int = 0, diff: Optional[Dict[str, Any]] = None) -> str
```

Build a Markdown report for `case`.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `case` | `Dict[str, Any]` |  | The case row, as returned by [`CaseStore.get_case`](estorides_core.cases.py.md#casestore-get_case). `analysis_json` is optional; if present it is embedded verbatim. |
| `entities` | `Optional[List[Dict[str, Any]]]` | `None` | The full entity list. If omitted, only the counts in the case row are used (TL;DR still works, IOC section is empty). |
| `sources_queried` | `int` | `0` |  |
| `sources_succeeded` | `int` | `0` |  |
| `diff` | `Optional[Dict[str, Any]]` | `None` | Optional output of `CaseStore.diff_entities(a, b)`. When given, a "what's new" section is appended before the analysis. |

**Returns:** `str` - The full Markdown document. UTF-8, LF newlines, no trailing
newline (callers add their own if writing to a file).

*Called by:* [`cmd_report`](estorides_cli.py.md#cmd_report)

---
