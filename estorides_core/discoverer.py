"""Background subdomain/domain discoverer.

Runs alongside the regular `run` to **fan out recursively** as new
domain entities surface. Inspired by the Palantir / Skynet pattern
of "drop a seed, walk the surface" — but kept dead-simple: we
just keep a queue of (type, value) to resolve, pull entities out
of every result, and enqueue the new domain entities we haven't
seen before.

Design notes:

  * No new HTTP / orchestration layer — we reuse the existing
    `Orchestrator` and `case_store.add_entities`. The discoverer
    is just a long-lived asyncio task that owns its own queue.
  * SSE-friendly: every time we enqueue something, append an
    observation, or finish a step, we push an event into a list
    that the SSE handler drains. The /api/discover/stream
    endpoint polls that list.
  * Bounded: the queue is capped and the global step counter is
    capped. The discoverer will never run away.
  * Idempotent: re-queuing the same (type, value) is a no-op.
  * Status persists across worker restarts (a process restart can
    pick the same case back up because the queue is reconstructed
    from the case_entities table).
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .cases import store as case_store
from .entity_extraction import detect_query_type
from .orchestrator import Orchestrator

log = logging.getLogger("estorides.discoverer")


# Maximum depth of the recursive fanout. 2 means: start with the
# seed, resolve it, enqueue the new domains it found, resolve
# those too, then stop. Bumping this makes the surface explode
# quadratically; 2 is the safe default.
DEFAULT_MAX_DEPTH = 2

# Hard cap on total steps (one step = one orchestrator run with a
# single target) so the background worker can't run forever on a
# popular target like google.com.
DEFAULT_MAX_STEPS = 50

# Stop the run when more than this many entities have been
# collected. Same rationale as above.
DEFAULT_MAX_ENTITIES = 5000

# SSE event buffer per job. If a client doesn't keep up, older
# events are dropped rather than blocking the worker.
_SSE_BUFFER_CAP = 200


@dataclass
class DiscoverJob:
    """One background discovery session.

    Lives in `DISCOVER_JOBS` keyed by job_id; survives the SSE
    handler exiting (so a UI reload reconnects and resumes).
    """
    job_id: str
    case_id: str
    seed_type: str
    seed_value: str
    max_depth: int = DEFAULT_MAX_DEPTH
    max_steps: int = DEFAULT_MAX_STEPS
    max_entities: int = DEFAULT_MAX_ENTITIES
    deadline_s: float = 30.0
    parallel: int = 4
    started_at: float = field(default_factory=time.time)
    status: str = "queued"  # queued | running | done | error | stopped
    steps_done: int = 0
    entities_seen: int = 0
    queue: List[Tuple[str, str, int]] = field(default_factory=list)
    seen: Set[Tuple[str, str]] = field(default_factory=set)
    events: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None
    # Stop flag the UI sets to request a graceful halt.
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
        if len(self.events) > _SSE_BUFFER_CAP:
            # Drop the oldest; the SSE client gets a "missed-N" hint
            # so it can decide whether to re-fetch the full state.
            dropped = len(self.events) - _SSE_BUFFER_CAP
            self.events = self.events[dropped:]
            self.events.append({
                "type": "heartbeat",
                "missed": dropped,
            })


# In-process registry. A single web worker is the only writer
# (the background task is owned by the request that started it),
# so we don't need a lock — but a `dict` access is atomic enough
# in CPython and we never mutate keys in place.
DISCOVER_JOBS: Dict[str, DiscoverJob] = {}


def _new_job_id() -> str:
    """Monotonic-ish id with a timestamp prefix for natural sort."""
    return f"d{int(time.time() * 1000) % 10**11:011d}"


async def start_discover(
    seed_type: str,
    seed_value: str,
    *,
    max_depth: int = DEFAULT_MAX_DEPTH,
    max_steps: int = DEFAULT_MAX_STEPS,
    max_entities: int = DEFAULT_MAX_ENTITIES,
    deadline_s: float = 30.0,
    parallel: int = 4,
) -> DiscoverJob:
    """Spawn a background discovery worker for `(seed_type, seed_value)`.

    Returns the DiscoverJob — the UI can immediately subscribe to
    /api/discover/stream?job_id=... to start receiving events.
    """
    # Always create a case so the discovered entities persist
    # across web worker restarts. The case_id is also the join key
    # between the case store and the discoverer state.
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
        max_depth=max_depth,
        max_steps=max_steps,
        max_entities=max_entities,
        deadline_s=deadline_s,
        parallel=parallel,
    )
    job.queue.append((seed_type, seed_value, 0))
    job.seen.add((seed_type, seed_value))
    DISCOVER_JOBS[job.job_id] = job
    job.push_event({
        "type": "started",
        "job_id": job.job_id,
        "case_id": case_id,
        "seed": {"type": seed_type, "value": seed_value},
        "max_depth": max_depth,
        "max_steps": max_steps,
    })
    # Schedule the worker but don't await it. The caller (the
    # HTTP handler) returns the job_id immediately so the UI can
    # connect the SSE stream.
    # The long-lived `serve` (if any) holds the on-disk Kuzu
    # lock for the duration of the web process. Initialising a
    # second KuzuGraphBackend against the same path would either
    # hang waiting for the lock or, with our recent fallback,
    # silently fall back to in-memory. We skip Kùzu entirely on
    # the discoverer side: the discoverer persists via the
    # case_store (SQLite, no global lock), and the regular
    # NetworkX KnowledgeGraph in the Orchestrator still builds
    # the in-memory attack surface for the entities.
    import estorides_core.graph_kuzu as _gk
    _gk.backend = None  # type: ignore[assignment]
    import estorides_core.orchestrator as _oc
    _oc.kuzu_backend = None  # type: ignore[assignment]
    asyncio.create_task(_run_discoverer(job))
    return job


async def _run_discoverer(job: DiscoverJob) -> None:
    """The background loop. One asyncio task per job."""
    job.status = "running"
    orch = Orchestrator()
    try:
        while job.queue and not job.should_stop():
            if job.steps_done >= job.max_steps:
                job.push_event({
                    "type": "stopping",
                    "reason": f"hit max_steps={job.max_steps}",
                })
                break
            if job.entities_seen >= job.max_entities:
                job.push_event({
                    "type": "stopping",
                    "reason": f"hit max_entities={job.max_entities}",
                })
                break
            ent_type, ent_value, depth = job.queue.pop(0)
            job.push_event({
                "type": "step_start",
                "target": {"type": ent_type, "value": ent_value},
                "depth": depth,
                "step": job.steps_done + 1,
                "queue_remaining": len(job.queue),
            })
            try:
                result = await orch.run(
                    ent_value,
                    parallel=job.parallel,
                    timeout=8,
                    deadline=job.deadline_s,
                )
            except Exception as e:  # noqa: BLE001
                job.push_event({
                    "type": "step_error",
                    "target": {"type": ent_type, "value": ent_value},
                    "error": f"{type(e).__name__}: {e}",
                })
                job.steps_done += 1
                continue
            # Persist every observation + entity back into the case
            # so the UI can later GET /api/cases/{id} and see them.
            try:
                for o in result.get("observations") or []:
                    case_store.add_observation(job.case_id, o)
                case_store.add_entities(
                    job.case_id,
                    [
                        {
                            "type": e.get("type", ""),
                            "value": e.get("value", ""),
                            "source": e.get("source", ""),
                            "confidence": e.get("confidence", 1.0),
                            "sources": e.get("sources") or [e.get("source", "")],
                        }
                        for e in (result.get("entities") or [])
                    ],
                )
            except Exception as e:  # noqa: BLE001
                log.warning("case_store write failed: %s", e)
            # Enqueue newly-discovered domain entities that are
            # below the depth cap. We focus on `domain` and `ipv4`
            # / `ipv6` because those are the ones the discovery
            # graph expands into (a `cve` or `asn` doesn't have
            # well-defined next steps in the passive sources).
            new_count = 0
            for e in result.get("entities") or []:
                t = e.get("type", "")
                v = e.get("value", "")
                if t not in ("domain", "ipv4", "ipv6"):
                    continue
                key = (t, v.lower())
                if key in job.seen:
                    continue
                job.seen.add(key)
                job.entities_seen += 1
                if depth + 1 > job.max_depth:
                    # Still record it as "seen" so the UI knows
                    # it exists, but don't recurse into it.
                    job.push_event({
                        "type": "leaf",
                        "entity": {"type": t, "value": v, "source": e.get("source", "")},
                        "from": {"type": ent_type, "value": ent_value},
                        "depth": depth + 1,
                    })
                    continue
                job.queue.append((t, v, depth + 1))
                new_count += 1
                # Mirror the new entity over SSE so the UI can
                # draw it before the next step completes.
                job.push_event({
                    "type": "node_found",
                    "entity": {"type": t, "value": v, "source": e.get("source", "")},
                    "from": {"type": ent_type, "value": ent_value},
                    "depth": depth + 1,
                })
            job.steps_done += 1
            job.push_event({
                "type": "step_done",
                "target": {"type": ent_type, "value": ent_value},
                "entities_in_step": len(result.get("entities") or []),
                "new_to_queue": new_count,
                "queue_remaining": len(job.queue),
                "step": job.steps_done,
            })
        job.status = "stopped" if job.should_stop() else "done"
        job.push_event({
            "type": "finished",
            "status": job.status,
            "steps_done": job.steps_done,
            "entities_seen": job.entities_seen,
        })
    except Exception as e:  # noqa: BLE001
        log.exception("discoverer crashed for %s", job.job_id)
        job.status = "error"
        job.error = f"{type(e).__name__}: {e}"
        job.push_event({
            "type": "error",
            "error": job.error,
        })


def list_jobs(limit: int = 20) -> List[Dict[str, Any]]:
    """Snapshot of the recent jobs for the /api/discover/jobs endpoint."""
    out: List[Dict[str, Any]] = []
    # Sort by started_at descending; cap at `limit` so the UI
    # list doesn't grow unbounded.
    items = sorted(
        DISCOVER_JOBS.values(),
        key=lambda j: j.started_at,
        reverse=True,
    )[:limit]
    for j in items:
        out.append({
            "job_id": j.job_id,
            "case_id": j.case_id,
            "seed": {"type": j.seed_type, "value": j.seed_value},
            "status": j.status,
            "steps_done": j.steps_done,
            "entities_seen": j.entities_seen,
            "queue_remaining": len(j.queue),
            "started_at": j.started_at,
            "error": j.error,
        })
    return out
