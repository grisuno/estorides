"""
estorides_core.pivot_engine
===========================
Recursive, asynchronous cross-search engine — the Palantir-style core.

Given a seed selector (a domain, IP, email, ASN, wallet), the engine runs
the full OSINT fan-out, harvests the selectors that surface, scores them,
and re-queries the highest-value ones, hop by hop, until a bounded budget
is spent. Every hop appends to a single case so the cross-search reads as
one coherent investigation.

The design is deliberately decoupled (SOLID):

  * `EntityRunner`  — an abstraction over "run one target, give me the
    observations and entities". Satisfied by the existing Orchestrator.
  * `EventSink`     — an abstraction over "publish a progress event". The
    SSE layer, a test list, or a log adapter all satisfy it. The engine
    knows nothing about HTTP.
  * `PivotPolicyConfig` (in config) — decides which selectors pivot and
    how leads are scored. Swapping the policy swaps the behaviour without
    touching the engine (open/closed).
  * `PivotConfig` (in config) — every bound and default. No literal in
    this module is a tunable number.

The frontier is a max-heap by lead score, so a high-signal selector (an
email, a wallet) expands before low-signal shared infrastructure at the
same depth. Confidence decays with depth and is carried on every emitted
entity so a downstream consumer can rank or prune.
"""
from __future__ import annotations

import heapq
import itertools
import logging
import time
from dataclasses import dataclass, field
from typing import (Any, Callable, Dict, List, Optional, Protocol, Set, Tuple,
                    runtime_checkable)

from .config import PIVOT, PivotConfig, PivotPolicyConfig

log = logging.getLogger("estorides.pivot")


# --------------------------------------------------------------------- events
@dataclass(frozen=True)
class PivotEvent:
    """A single, transport-neutral progress event.

    `type` is a stable vocabulary token; `data` is a JSON-serialisable
    payload. Sinks translate these to their own wire format.
    """

    type: str
    data: Dict[str, Any]


@runtime_checkable
class EventSink(Protocol):
    """Receives engine progress events. Implementations must not raise."""

    def emit(self, event: PivotEvent) -> None:
        """Publish one event. A slow or failing sink must never break a run."""
        ...


class ListEventSink:
    """In-memory sink. Useful for tests and synchronous embedding."""

    def __init__(self) -> None:
        self.events: List[PivotEvent] = []

    def emit(self, event: PivotEvent) -> None:
        self.events.append(event)


class BufferedEventSink:
    """Bounded sink that flattens events to JSON-ready dicts for SSE drain.

    Each stored item is `{"type": ..., "ts": ..., **data}`. When the buffer
    exceeds `capacity` the oldest items are dropped and a `heartbeat` marker
    records how many were lost, so a slow client degrades gracefully instead
    of stalling the producer. The terminal `finished`/`fatal` event also
    flips `done` so a poller knows when to stop without parsing payloads.
    """

    def __init__(self, capacity: int) -> None:
        self._capacity = max(1, capacity)
        self.events: List[Dict[str, Any]] = []
        self.done: bool = False
        self.status: str = "running"
        self.error: Optional[str] = None

    def emit(self, event: PivotEvent) -> None:
        item: Dict[str, Any] = {"type": event.type, "ts": time.time()}
        item.update(event.data)
        self.events.append(item)
        if len(self.events) > self._capacity:
            dropped = len(self.events) - self._capacity
            self.events = self.events[dropped:]
            self.events.append({"type": "heartbeat", "missed": dropped, "ts": time.time()})
        if event.type == "finished":
            self.done = True
            self.status = str(event.data.get("status", "done"))
        elif event.type == "fatal":
            self.done = True
            self.status = "error"
            self.error = str(event.data.get("error", "unknown"))


# ---------------------------------------------------------------- runner port
@runtime_checkable
class EntityRunner(Protocol):
    """Runs the OSINT fan-out for a single target.

    The engine depends on this narrow port rather than the concrete
    Orchestrator, so it can be driven by a stub in tests.
    """

    async def run(
        self,
        query: str,
        *,
        parallel: int,
        timeout: float,
        deadline: float,
        on_source_done: Optional[Callable[..., None]],
        on_source_result: Optional[Callable[..., None]],
        persist: bool,
        case_id: Optional[str],
    ) -> Dict[str, Any]:
        ...


# ------------------------------------------------------------------- budget
@dataclass
class PivotBudget:
    """Mutable accounting for one cross-search.

    Holds the three hard ceilings (steps, entities, wall-clock) and the
    monotonic clock the deadline is measured against. `exhausted()` returns
    a human reason string the moment any ceiling is hit, else None.
    """

    max_depth: int
    max_steps: int
    max_entities: int
    deadline_seconds: float
    started_monotonic: float
    steps_done: int = 0
    entities_seen: int = 0

    def time_left(self) -> float:
        """Seconds remaining before the global wall-clock deadline."""
        return self.deadline_seconds - (time.monotonic() - self.started_monotonic)

    def exhausted(self) -> Optional[str]:
        """Reason the run must stop, or None while budget remains."""
        if self.steps_done >= self.max_steps:
            return f"max_steps={self.max_steps}"
        if self.entities_seen >= self.max_entities:
            return f"max_entities={self.max_entities}"
        if self.time_left() <= 0:
            return f"deadline={self.deadline_seconds:.0f}s"
        return None


# --------------------------------------------------------------------- lead
@dataclass(frozen=True)
class PivotLead:
    """A target waiting in the frontier."""

    entity_type: str
    value: str
    depth: int
    score: float
    parent_type: str
    parent_value: str


@dataclass
class PivotResult:
    """Terminal summary of a completed cross-search."""

    status: str
    steps_done: int
    entities_seen: int
    stop_reason: Optional[str] = None
    error: Optional[str] = None


# ------------------------------------------------------------------- engine
class PivotEngine:
    """Drives the recursive, scored, asynchronous cross-search."""

    def __init__(
        self,
        runner: EntityRunner,
        sink: EventSink,
        *,
        config: PivotConfig = PIVOT,
        policy: Optional[PivotPolicyConfig] = None,
        max_depth: Optional[int] = None,
        max_steps: Optional[int] = None,
        max_entities: Optional[int] = None,
        per_target_timeout: Optional[float] = None,
        deadline_seconds: Optional[float] = None,
        parallel: Optional[int] = None,
        breadth_per_step: Optional[int] = None,
        case_id: Optional[str] = None,
        should_stop: Optional[Callable[[], bool]] = None,
        persist: bool = True,
    ) -> None:
        self._runner = runner
        self._sink = sink
        self._config = config
        self._policy = policy if policy is not None else config.policy
        self._max_depth = config.clamp_depth(max_depth if max_depth is not None else config.max_depth)
        self._max_steps = config.clamp_steps(max_steps if max_steps is not None else config.max_steps)
        self._max_entities = config.clamp_entities(
            max_entities if max_entities is not None else config.max_entities
        )
        self._per_target_timeout = config.clamp_deadline(
            per_target_timeout if per_target_timeout is not None else config.per_target_timeout_seconds
        )
        self._deadline_seconds = config.clamp_deadline(
            deadline_seconds if deadline_seconds is not None else config.deadline_seconds
        )
        self._parallel = config.clamp_parallel(parallel if parallel is not None else config.parallel)
        self._breadth_per_step = max(1, breadth_per_step if breadth_per_step is not None else config.breadth_per_step)
        self._case_id = case_id
        self._should_stop = should_stop if should_stop is not None else (lambda: False)
        self._persist = persist
        self._seen: Set[Tuple[str, str]] = set()
        # Tie-break counter keeps the heap total-ordered without ever
        # comparing two PivotLead instances (which are not orderable).
        self._counter = itertools.count()

    # ------------------------------------------------------------- emit
    def _emit(self, event_type: str, **data: Any) -> None:
        """Build and publish an event, swallowing any sink failure."""
        try:
            self._sink.emit(PivotEvent(type=event_type, data=data))
        except Exception:  # noqa: BLE001 - a sink must never break a run
            log.debug("event sink raised for %s", event_type, exc_info=True)

    # ------------------------------------------------------------- frontier
    @staticmethod
    def _heap_push(
        heap: List[Tuple[float, int, PivotLead]],
        counter: "itertools.count[int]",
        lead: PivotLead,
    ) -> None:
        """Push a lead as a max-heap by score (negated for heapq)."""
        heapq.heappush(heap, (-lead.score, next(counter), lead))

    # --------------------------------------------------------------- run
    async def run(self, seed_type: str, seed_value: str) -> PivotResult:
        """Execute the cross-search from `(seed_type, seed_value)`.

        Returns a `PivotResult`. Progress is published incrementally
        through the injected sink while the coroutine is in flight.
        """
        budget = PivotBudget(
            max_depth=self._max_depth,
            max_steps=self._max_steps,
            max_entities=self._max_entities,
            deadline_seconds=self._deadline_seconds,
            started_monotonic=time.monotonic(),
        )
        seed_value = seed_value.strip()
        if not seed_value:
            self._emit("fatal", error="empty seed")
            return PivotResult(status="error", steps_done=0, entities_seen=0, error="empty seed")

        frontier: List[Tuple[float, int, PivotLead]] = []
        seed_lead = PivotLead(
            entity_type=seed_type,
            value=seed_value,
            depth=0,
            score=self._config.seed_score,
            parent_type="seed",
            parent_value="",
        )
        self._heap_push(frontier, self._counter, seed_lead)
        self._seen.add((seed_type, seed_value.lower()))

        self._emit(
            "started",
            seed={"type": seed_type, "value": seed_value},
            max_depth=self._max_depth,
            max_steps=self._max_steps,
            max_entities=self._max_entities,
        )

        stop_reason: Optional[str] = None
        try:
            while frontier:
                if self._should_stop():
                    stop_reason = "stop_requested"
                    break
                reason = budget.exhausted()
                if reason is not None:
                    stop_reason = reason
                    self._emit("stopping", reason=reason)
                    break
                _neg_score, _seq, lead = heapq.heappop(frontier)
                await self._expand_lead(lead, frontier, budget)

            status = "stopped" if (self._should_stop() or stop_reason == "stop_requested") else "done"
            self._emit(
                "finished",
                status=status,
                steps_done=budget.steps_done,
                entities_seen=budget.entities_seen,
                stop_reason=stop_reason,
            )
            return PivotResult(
                status=status,
                steps_done=budget.steps_done,
                entities_seen=budget.entities_seen,
                stop_reason=stop_reason,
            )
        except Exception as e:  # noqa: BLE001 - report, never propagate to the loop owner
            log.exception("pivot engine crashed")
            self._emit("fatal", error=f"{type(e).__name__}: {e}")
            return PivotResult(
                status="error",
                steps_done=budget.steps_done,
                entities_seen=budget.entities_seen,
                error=f"{type(e).__name__}: {e}",
            )

    # ------------------------------------------------------- expand one lead
    async def _expand_lead(
        self,
        lead: PivotLead,
        frontier: List[Tuple[float, int, PivotLead]],
        budget: PivotBudget,
    ) -> None:
        """Run the fan-out for one lead and enqueue its scored children."""
        self._emit(
            "target_start",
            target={"type": lead.entity_type, "value": lead.value},
            depth=lead.depth,
            score=round(lead.score, 4),
            step=budget.steps_done + 1,
        )

        def _on_source_done(name: str, ok: bool, status: Any, elapsed_ms: float) -> None:
            self._emit(
                "source_tick",
                target={"type": lead.entity_type, "value": lead.value},
                source=name,
                ok=bool(ok),
                status=status,
                elapsed_ms=round(float(elapsed_ms), 1),
            )

        def _on_source_result(observation: Dict[str, Any]) -> None:
            self._emit(
                "source_result",
                target={"type": lead.entity_type, "value": lead.value},
                observation=observation,
            )

        # Never let a single target run past the global wall-clock.
        per_target_deadline = max(1.0, min(self._per_target_timeout, budget.time_left()))
        try:
            result = await self._runner.run(
                lead.value,
                parallel=self._parallel,
                timeout=self._per_target_timeout,
                deadline=per_target_deadline,
                on_source_done=_on_source_done,
                on_source_result=_on_source_result,
                persist=self._persist,
                case_id=self._case_id,
            )
        except Exception as e:  # noqa: BLE001
            budget.steps_done += 1
            self._emit(
                "target_error",
                target={"type": lead.entity_type, "value": lead.value},
                error=f"{type(e).__name__}: {e}",
            )
            return

        new_to_queue = self._ingest_children(lead, result, frontier, budget)
        budget.steps_done += 1
        self._emit(
            "target_done",
            target={"type": lead.entity_type, "value": lead.value},
            entities_in_step=len(result.get("entities") or []),
            new_to_queue=new_to_queue,
            queue_remaining=len(frontier),
            step=budget.steps_done,
            analysis=result.get("analysis"),
            graph=result.get("graph"),
        )

    # ----------------------------------------------------- score and enqueue
    def _ingest_children(
        self,
        parent: PivotLead,
        result: Dict[str, Any],
        frontier: List[Tuple[float, int, PivotLead]],
        budget: PivotBudget,
    ) -> int:
        """Score the entities a target produced and enqueue the best ones.

        Returns the number of leads actually added to the frontier. The
        per-step breadth cap keeps a single popular target (a CDN, a
        registrar) from flooding the queue.
        """
        child_depth = parent.depth + 1
        enqueued = 0
        for entity in (result.get("entities") or []):
            if budget.entities_seen >= self._max_entities:
                break
            entity_type = str(entity.get("type", ""))
            value = str(entity.get("value", "")).strip()
            if not entity_type or not value:
                continue
            if not self._policy.is_pivotable(entity_type):
                continue
            key = (entity_type, value.lower())
            if key in self._seen:
                continue
            self._seen.add(key)
            budget.entities_seen += 1

            parent_confidence = float(entity.get("confidence", 1.0) or 1.0)
            score = self._policy.lead_score(entity_type, child_depth, parent.score * parent_confidence)
            entity_payload = {
                "type": entity_type,
                "value": value,
                "source": entity.get("source", ""),
                "score": round(score, 4),
            }
            from_payload = {"type": parent.entity_type, "value": parent.value}

            if child_depth > self._max_depth or enqueued >= self._breadth_per_step:
                # Known but not expanded: a leaf on the frontier edge.
                self._emit(
                    "entity",
                    entity=entity_payload,
                    **{"from": from_payload},
                    depth=child_depth,
                    pivoted=False,
                )
                continue

            self._heap_push(
                frontier,
                self._counter,
                PivotLead(
                    entity_type=entity_type,
                    value=value,
                    depth=child_depth,
                    score=score,
                    parent_type=parent.entity_type,
                    parent_value=parent.value,
                ),
            )
            enqueued += 1
            self._emit(
                "entity",
                entity=entity_payload,
                **{"from": from_payload},
                depth=child_depth,
                pivoted=True,
            )
        return enqueued
