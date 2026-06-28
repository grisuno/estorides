# Issue #47: /api/graph serves the last operator's full intelligence graph without authentication or session isolation

- **State:** open
- **Created:** 2026-06-08T11:43:35Z
- **Updated:** 2026-06-08T11:43:35Z
- **Labels:** None

---

## Summary
The `/api/graph` endpoint reads the entire `data/estorides_graph.graphml` file from disk, deserialises it with NetworkX, runs Louvain community detection, and serialises the result on every request. This file is shared across all users of the deployment — whoever ran the last query owns the graph. An anonymous caller requesting `/api/graph` receives the full intelligence graph from the last investigation run by any operator. There is also no rate limit on this endpoint (separate issue), so it can be called indefinitely.

## Evidence
`estorides_web.py` lines 232–305:
```python
@app.route("/api/graph")
def api_graph() -> Any:
    if not GRAPH_PATH.exists():
        return jsonify({"nodes": [], "edges": []})
    import networkx as nx
    kg = KnowledgeGraph()
    kg.graph = nx.read_graphml(GRAPH_PATH)   # reads shared file
    ...
    return jsonify({"nodes": nodes, "edges": edges, ...})
```

`GRAPH_PATH` is defined in `estorides_core/config.py` line 77:
```python
GRAPH_PATH: Path = DATA_DIR / "estorides_graph.graphml"
```

This is a single file, written by the last `/api/run` call, readable by any HTTP client that hits `/api/graph`.

## Why this matters
In a multi-user or shared deployment, `/api/graph` leaks the entire intelligence graph of the previous investigator's query to any subsequent caller, including anonymous ones. This exposes:
- All entity types and values (IPs, domains, emails, CVEs) from the previous investigation
- Relationship structure between entities
- Which OSINT sources observed which entities

## Attack or failure scenario
1. Security researcher uses the platform to investigate a confidential threat actor.
2. A second party (attacker or competitor) immediately calls `GET /api/graph`.
3. They receive the full intelligence picture of the researcher's investigation without any authentication.

## Root cause
The graph file is a global singleton written without a per-session or per-case namespace. This was acceptable for a single-user local tool but becomes a data disclosure issue in any multi-user or web-accessible deployment.

## Recommended fix
1. Namespace the graph file per case: `data/graphs/<case_id>.graphml`.
2. Require the caller to pass a `?case_id=<id>` parameter; validate that the file exists and serve only that case's graph.
3. If backward compatibility is needed, keep the global graph file for CLI use but refuse to serve it via the web API without a case parameter.
4. Add authentication before any `/api/graph` response.

## Acceptance criteria
- `/api/graph` requires a `case_id` parameter.
- Each `/api/run` call stores its graph under a case-scoped filename.
- No anonymous caller can retrieve another user's intelligence graph via `/api/graph`.
- The UI passes the active case ID when requesting the graph.

## Suggested labels
security, privacy, architecture

## Priority
P1

## Severity
High — Any caller can retrieve the complete intelligence graph of the most recent investigation, including all discovered entities and relationships, without authentication.

## Confidence
Confirmed — the shared global graph file path is hardcoded in config.py and served without access control.
