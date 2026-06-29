# Issue #32: [CRITICAL] #3: Unsafe LLM timeout handling causes race condition

- **State:** closed
- **Created:** 2026-06-08T10:35:04Z
- **Updated:** 2026-06-29T16:15:32Z
- **Labels:** None

---

## Summary
The LLM analysis timeout handling at `orchestrator.py` lines 392-409 is unsafe:

```python
llm_budget = min(deadline, 10.0)
try:
    analysis = await asyncio.wait_for(
        asyncio.to_thread(
            self.llm.generate,
            f"Produce an intelligence assessment of the target '{query}'.",
            context=observations,
            request_timeout=llm_budget,
        ),
        timeout=llm_budget + 2.0,
    )
except asyncio.TimeoutError:
    log.warning("LLM analysis exceeded timeout, returning stub")
    analysis = {
        "backend": "stub", "model": "stub",
        "content": "[LLM analysis skipped — exceeded timeout]",
        "error": "llm_timeout",
    }
```

The `request_timeout` passed to `llm.generate()` is the same as the `wait_for` timeout, creating a race condition where the LLM could be killed by the timeout before the `wait_for` fires. This is particularly dangerous because:

1. The LLM may have partially generated a response that is then discarded.
2. The stub response is indistinguishable from a legitimate but slow response.
3. The timeout window is too large (12 seconds) for an OSINT tool that needs to pivot quickly.

## Location
- `estorides_core/orchestrator.py` lines 392-409

## Impact
- Partial LLM output may be discarded, leading to incomplete or misleading intelligence.
- The stub response could be used to hide failures or delays in the analysis.
- The large timeout window could delay the entire intelligence cycle unnecessarily.

## Recommended Fix
1. Reduce the timeout window to a more reasonable value (e.g., 5 seconds).
2. Use a separate timeout for the LLM call and the `wait_for` call to prevent the race condition.
3. Ensure that the stub response clearly indicates that the analysis was incomplete due to a timeout.
4. Add logging to track when the LLM analysis is skipped due to a timeout.
