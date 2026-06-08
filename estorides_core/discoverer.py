"""Background subdomain/domain discoverer.

Drops a seed and walks the passive attack surface recursively. As of
v1.3 the recursion itself lives in `pivot_engine.PivotEngine`; this
module is the thin adapter that:

  * owns the long-lived `DiscoverJob` registry the SSE/CLI layers poll,
  * drives the engine with the infrastructure-only pivot policy (domains
    and IPs, the historical discoverer surface), and
  * translates engine `PivotEvent`s into the legacy event dicts the UI
    and CLI already understand (`started`, `step_start`, `node_found`,
    `step_done`, `finished`, `error`, ...).

Keeping one engine and many adapters is the DRY win: the deep-run SSE
endpoint and this background discoverer share identical recursion,
scoring and budgeting code; only the policy and the event shape differ.

Design guarantees preserved from v1.2:

  * No new HTTP layer — the engine reuses the existing `Orchestrator`.
  * Persistence is via the case store; every hop appends to one case.
  * Bounded: depth, steps and entity ceilings come from config caps.
  * Idempotent: re-queuing the same (type, value) is a no-op (engine).
"""
from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from .cases import store as case_store
from .config import PIVOT, PIVOT_POLICY_INFRA, STREAM
from .pivot_engine import EventSink, PivotEngine, PivotEvent

log = logging.getLogger("estorides.discoverer")


# Defaults are sourced from the central PivotConfig so the discoverer and
# the deep-run share one set of bounds. Re-exported as module constants for
# backward compatibility with callers that imported them by name.
DEFAULT_MAX_DEPTH: int = PIVOT.max_depth
DEFAULT_MAX_STEPS: int = PIVOT.max_steps
DEFAULT_MAX_ENTITIES: int = PIVOT.max_entities


@dataclass
class DiscoverJob:
    """One background discovery session.

    Lives in `DISCOVER_JOBS` keyed by job_id; survives the SSE handler
    exiting (so a UI reload reconnects and resumes).
    """

    job_id: str
    case_id: str
    seed_type: str
    seed_value: str
    max_depth: int = DEFAULT_MAX_DEPTH
    max_steps: int = DEFAULT_MAX_STEPS
    max_entities: int = DEFAULT_MAX_ENTITIES
    deadline_s: float = PIVOT.per_target_timeout_seconds
    parallel: int = PIVOT.parallel
    passive_only: bool = False
    proxy: Optional[str] = None
    started_at: float = field(default_factory=time.time)
    status: str = "queued"  # queued | running | done | error | stopped
    steps_done: int = 0
    entities_seen: int = 0
    queue_remaining: int = 0
    seen: Set[Tuple[str, str]] = field(default_factory=set)
    events: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    _stop: bool = False

    def stop(self) -> None:
        self._stop = True

    def should_stop(self) -> bool:
        return self._stop

    def push_event(self, ev: Dict[str, Any]) -> None:
        """Append an event and keep the buffer bounded."""
        ev = dict(ev)
        ev.setdefault("ts", time.time())
        self.events.append(ev)
        if len(self.events) > STREAM.sse_buffer_cap:
            dropped = len(self.events) - STREAM.sse_buffer_cap
            self.events = self.events[dropped:]
            self.events.append({"type": "heartbeat", "missed": dropped})


class _DiscoverJobSink:
    """Adapts engine `PivotEvent`s to the legacy DiscoverJob event dicts.

    The UI and CLI consume `step_start`, `node_found`, `step_done`,
    `finished` and `error`; this translator preserves those shapes so the
    engine swap is invisible to every existing consumer.
    """

    def __init__(self, job: DiscoverJob) -> None:
        self._job = job

    def emit(self, event: PivotEvent) -> None:
        handler = getattr(self, f"_on_{event.type}", None)
        if handler is not None:
            handler(event.data)

    # The job already announced "started" in start_discover; ignore the
    # engine's duplicate so the UI sees exactly one.
    def _on_started(self, data: Dict[str, Any]) -> None:
        self._job.status = "running"

    def _on_target_start(self, data: Dict[str, Any]) -> None:
        target = data.get("target") or {}
        self._job.push_event({
            "type": "step_start",
            "target": target,
            "depth": data.get("depth", 0),
            "step": data.get("step", self._job.steps_done + 1),
            "queue_remaining": self._job.queue_remaining,
        })

    def _on_entity(self, data: Dict[str, Any]) -> None:
        self._job.entities_seen += 1
        # Every surfaced entity is reported as node_found so the UI renders
        # it in the entities tab — including non-pivotable human selectors
        # (email, username, person, phone, org) that are the OSINT trail on
        # people. The `pivoted` flag lets a consumer tell a re-queried node
        # from a leaf the operator must follow manually.
        self._job.push_event({
            "type": "node_found",
            "entity": data.get("entity") or {},
            "from": data.get("from") or {},
            "depth": data.get("depth", 0),
            "pivoted": bool(data.get("pivoted", True)),
        })

    def _on_target_done(self, data: Dict[str, Any]) -> None:
        self._job.steps_done = int(data.get("step", self._job.steps_done))
        self._job.queue_remaining = int(data.get("queue_remaining", 0))
        self._job.push_event({
            "type": "step_done",
            "target": data.get("target") or {},
            "entities_in_step": data.get("entities_in_step", 0),
            "new_to_queue": data.get("new_to_queue", 0),
            "queue_remaining": self._job.queue_remaining,
            "step": self._job.steps_done,
        })

    def _on_target_error(self, data: Dict[str, Any]) -> None:
        self._job.push_event({
            "type": "step_error",
            "target": data.get("target") or {},
            "error": data.get("error", "unknown"),
        })

    def _on_stopping(self, data: Dict[str, Any]) -> None:
        self._job.push_event({"type": "stopping", "reason": data.get("reason", "")})

    def _on_finished(self, data: Dict[str, Any]) -> None:
        self._job.status = str(data.get("status", "done"))
        self._job.steps_done = int(data.get("steps_done", self._job.steps_done))
        self._job.entities_seen = int(data.get("entities_seen", self._job.entities_seen))
        self._job.push_event({
            "type": "finished",
            "status": self._job.status,
            "steps_done": self._job.steps_done,
            "entities_seen": self._job.entities_seen,
        })

    def _on_fatal(self, data: Dict[str, Any]) -> None:
        self._job.status = "error"
        self._job.error = str(data.get("error", "unknown"))
        self._job.push_event({"type": "error", "error": self._job.error})


# In-process registry. A single web worker is the only writer, so a plain
# dict is safe (key writes are atomic in CPython and never mutated in place).
DISCOVER_JOBS: Dict[str, DiscoverJob] = {}


def _new_job_id() -> str:
    """Monotonic-ish id with a timestamp prefix for natural sort."""
    return f"d{int(time.time() * 1000) % 10 ** 11:011d}"


def create_discover_job(
    seed_type: str,
    seed_value: str,
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_steps: int = DEFAULT_MAX_STEPS,
    max_entities: int = DEFAULT_MAX_ENTITIES,
    deadline_s: float = PIVOT.per_target_timeout_seconds,
    parallel: int = PIVOT.parallel,
    passive_only: bool = False,
    proxy: Optional[str] = None,
) -> DiscoverJob:
    """Create and register a discovery job synchronously.

    This does only fast, loop-free work (a case-store insert and some
    bookkeeping), so it is safe to call straight from a Flask request
    thread. The asyncio worker that actually crawls is scheduled
    separately by `start_discover` / `start_discover_threadsafe`, so the
    caller never blocks on the shared background loop.
    """
    case_id = case_store.create_case(
        query=seed_value,
        query_type=seed_type,
        notes=f"background discover seed={seed_type}:{seed_value}",
    )
    job = DiscoverJob(
        job_id=_new_job_id(),
        case_id=case_id,
        seed_type=seed_type,
        seed_value=seed_value,
        max_depth=PIVOT.clamp_depth(max_depth),
        max_steps=PIVOT.clamp_steps(max_steps),
        max_entities=PIVOT.clamp_entities(max_entities),
        deadline_s=PIVOT.clamp_deadline(deadline_s),
        parallel=PIVOT.clamp_parallel(parallel),
        passive_only=passive_only,
        proxy=proxy,
    )
    DISCOVER_JOBS[job.job_id] = job
    job.push_event({
        "type": "started",
        "job_id": job.job_id,
        "case_id": case_id,
        "seed": {"type": seed_type, "value": seed_value},
        "max_depth": job.max_depth,
        "max_steps": job.max_steps,
    })
    # The long-lived web process may hold the on-disk Kùzu lock. A second
    # backend against the same path would block, so the discoverer persists
    # only through the case store (SQLite, no global lock) and keeps the
    # in-memory NetworkX graph the Orchestrator builds per run.
    import estorides_core.graph_kuzu as _gk
    _gk.backend = None  # type: ignore[assignment]
    import estorides_core.orchestrator as _oc
    _oc.kuzu_backend = None  # type: ignore[assignment]
    return job


async def start_discover(
    seed_type: str,
    seed_value: str,
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_steps: int = DEFAULT_MAX_STEPS,
    max_entities: int = DEFAULT_MAX_ENTITIES,
    deadline_s: float = PIVOT.per_target_timeout_seconds,
    parallel: int = PIVOT.parallel,
    passive_only: bool = False,
    proxy: Optional[str] = None,
) -> DiscoverJob:
    """Create a discovery job and schedule its worker on the current loop.

    Kept as the coroutine entry point for callers that already own a
    running loop (the CLI). Web callers use `start_discover_threadsafe`,
    which never blocks the request thread on the background loop.
    """
    job = create_discover_job(
        seed_type,
        seed_value,
        max_depth=max_depth,
        max_steps=max_steps,
        max_entities=max_entities,
        deadline_s=deadline_s,
        parallel=parallel,
        passive_only=passive_only,
        proxy=proxy,
    )
    asyncio.create_task(_run_discoverer(job))
    return job


def start_discover_threadsafe(
    loop: asyncio.AbstractEventLoop,
    seed_type: str,
    seed_value: str,
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_steps: int = DEFAULT_MAX_STEPS,
    max_entities: int = DEFAULT_MAX_ENTITIES,
    deadline_s: float = PIVOT.per_target_timeout_seconds,
    parallel: int = PIVOT.parallel,
    passive_only: bool = False,
    proxy: Optional[str] = None,
) -> DiscoverJob:
    """Create the job in the calling thread, fire its worker on `loop`.

    Returns immediately. The worker is queued with
    `run_coroutine_threadsafe` and runs whenever the loop is next free, so
    a busy loop (a concurrent deep-run) can never make this call time out.
    """
    job = create_discover_job(
        seed_type,
        seed_value,
        max_depth=max_depth,
        max_steps=max_steps,
        max_entities=max_entities,
        deadline_s=deadline_s,
        parallel=parallel,
        passive_only=passive_only,
        proxy=proxy,
    )
    asyncio.run_coroutine_threadsafe(_run_discoverer(job), loop)
    return job


async def _run_discoverer(job: DiscoverJob) -> None:
    """The background loop. One asyncio task per job, driving the engine."""
    from .orchestrator import Orchestrator

    job.status = "running"
    sink: EventSink = _DiscoverJobSink(job)
    # Constructing an Orchestrator loads the sanctions index and every
    # source YAML — seconds of synchronous CPU. Build it off the event loop
    # so it never stalls the loop (and the dispatch of other jobs).
    orchestrator = await asyncio.to_thread(Orchestrator)
    engine = PivotEngine(
        runner=orchestrator,
        sink=sink,
        config=PIVOT,
        policy=PIVOT_POLICY_INFRA,
        max_depth=job.max_depth,
        max_steps=job.max_steps,
        max_entities=job.max_entities,
        per_target_timeout=job.deadline_s,
        deadline_seconds=PIVOT.deadline_cap_seconds,
        parallel=job.parallel,
        case_id=job.case_id,
        should_stop=job.should_stop,
        persist=True,
        passive_only=job.passive_only,
        proxy=job.proxy,
    )
    await engine.run(job.seed_type, job.seed_value)


def list_jobs(limit: int = 20) -> List[Dict[str, Any]]:
    """Snapshot of the recent jobs for the /api/discover/jobs endpoint."""
    items = sorted(
        DISCOVER_JOBS.values(),
        key=lambda j: j.started_at,
        reverse=True,
    )[:limit]
    return [
        {
            "job_id": j.job_id,
            "case_id": j.case_id,
            "seed": {"type": j.seed_type, "value": j.seed_value},
            "status": j.status,
            "steps_done": j.steps_done,
            "entities_seen": j.entities_seen,
            "queue_remaining": j.queue_remaining,
            "started_at": j.started_at,
            "error": j.error,
        }
        for j in items
    ]
