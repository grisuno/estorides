"""BDD tests for spec/transforms.md — Maltego-style pivoting.

S1 happy, S2 edge vacío, S3 error id, S4 runner-roto,
S5 metadata rica, S6 validación input + stream shape, S7 yaml sin código.
Rojo hasta que transforms.py gane input_types/output_types/cost + límites.
"""
from estorides_core.transforms import Transform, registry


def _mock_resolver(monkeypatch, nodes, links, root_id="ip:1.2.3.4"):
    import estorides_core.intel_resolver as ir

    class Fake:
        def resolve(self, t, v):
            return {"nodes": nodes, "links": links,
                    "root_id": root_id, "sources": ["vt"]}
    monkeypatch.setattr(ir, "resolver", Fake())


def test_s1_ip_to_bgp_happy(monkeypatch):
    import estorides_core.transforms as tr
    monkeypatch.setattr(tr, "_osiris", lambda: type("O", (), {
        "fetch_bgp": staticmethod(lambda q: {"asn": "15169", "holder": "Google"}),
    }))
    res = registry.run("ip_to_bgp", "ip", "8.8.8.8")
    assert "error" not in res
    ids = {n["id"] for n in res["nodes"]}
    assert "ip:8.8.8.8" in ids
    rels = {link["relation"] for link in res["links"]}
    assert {"announced_by", "hosted_by"} <= rels
    assert res["sources"] == ["bgp"]
    assert res["transform"] == "ip_to_bgp"


def test_s2_empty_osiris_no_raise(monkeypatch):
    import estorides_core.transforms as tr
    monkeypatch.setattr(tr, "_osiris", lambda: None)
    res = registry.run("ip_to_bgp", "ip", "1.2.3.4")
    assert res["nodes"] == [] and res["links"] == []
    monkeypatch.setattr(tr, "_osiris", lambda: type("O", (), {
        "fetch_bgp": staticmethod(lambda q: {}),
    }))
    res2 = registry.run("ip_to_bgp", "ip", "1.2.3.4")
    assert res2["links"] == [] and res2["sources"] == []


def test_s3_unknown_transform_id():
    res = registry.run("nope_missing", "ip", "1.2.3.4")
    assert "unknown transform" in res["error"]
    assert res["nodes"] == [] and res["links"] == []


def test_s4_runner_exception_fail_closed():
    registry.register(Transform(
        id="tmp_boom", label="Boom", tier="data",
        applies={"ip"}, runner=lambda t, v: 1 / 0,
        description="boom",
    ))
    try:
        res = registry.run("tmp_boom", "ip", "1.2.3.4")
        assert res["error"] == "transform-run-failed"
        assert res["nodes"] == [] and res["links"] == []
    finally:
        del registry._by_id["tmp_boom"]


def test_s5_rich_metadata_sorted():
    trs = registry.for_type("ip")
    assert len(trs) >= 5
    for t in trs:
        for k in ("id", "label", "tier", "description",
                  "input_types", "output_types", "cost"):
            assert k in t, f"missing {k} in {t.get('id')}"
    tiers = [t["tier"] for t in trs]
    order = ["data", "information", "intelligence", "counter_intelligence"]
    assert tiers == sorted(tiers, key=lambda x: order.index(x)
                           if x in order else 9)


def test_s6_input_limits_and_stream_shape():
    # value gigante / tid malformado → error, nunca I/O
    res = registry.run("ip_to_bgp", "ip", "x" * 600)
    assert "error" in res and res["nodes"] == []
    res2 = registry.run("evil id!", "ip", "1.2.3.4")
    assert "error" in res2
    # shape SSE-ready: run dict ya trae lo que el stream trocea
    import estorides_core.transforms as tr
    assert hasattr(tr, "iter_sse_events"), "falta iter_sse_events para /stream"
    evs = list(tr.iter_sse_events("ip_to_bgp", "ip", "8.8.8.8",
                                  runner=lambda t, v: {"nodes": [{"id": "a"}],
                                                       "links": [], "sources": []}))
    kinds = [k for k, _ in evs]
    assert "node" in kinds and kinds[-1] == "done"


def test_s7_yaml_transform_no_code(monkeypatch, tmp_path):
    import estorides_core.transforms as tr
    y = tmp_path / "mi_pivot.yaml"
    y.write_text(
        "id: tmp_yaml_pivot\nlabel: tmp yaml pivot\ntier: intelligence\n"
        "description: yaml test\ninput_types: [domain]\noutput_types: [ip]\n"
        "cost: free\nengine: resolver\nrelations: [resolves_to]\n",
        encoding="utf-8",
    )
    (tmp_path / "broken.yaml").write_text("id: [unclosed\n", encoding="utf-8")
    _mock_resolver(
        monkeypatch,
        [{"id": "domain:x.com"}, {"id": "ip:1.2.3.4"}],
        [{"source": "domain:x.com", "target": "ip:1.2.3.4",
          "relation": "resolves_to"},
         {"source": "domain:x.com", "target": "file:aaa",
          "relation": "communicates_with"}],
        root_id="domain:x.com",
    )
    n = tr.registry.load_yaml_dir(tmp_path)
    try:
        assert n == 1
        listed = [t["id"] for t in tr.registry.for_type("domain")]
        assert "tmp_yaml_pivot" in listed
        meta = next(t for t in tr.registry.for_type("domain")
                    if t["id"] == "tmp_yaml_pivot")
        assert meta["output_types"] == ["ip"] and meta["cost"] == "free"
        res = tr.registry.run("tmp_yaml_pivot", "domain", "x.com")
        assert "error" not in res
        assert {lk["relation"] for lk in res["links"]} == {"resolves_to"}
    finally:
        tr.registry._by_id.pop("tmp_yaml_pivot", None)


def _repo_transforms_dir():
    from pathlib import Path
    return Path(__file__).resolve().parent.parent / "transforms"


def test_s8_yaml_catalog_complete_and_substituted():
    """Every transforms/*.yaml ships full metadata; static pivots run
    offline with zero '{query}' leftovers, even inside properties."""
    import yaml

    import estorides_core.transforms as tr
    d = _repo_transforms_dir()
    files = sorted(d.glob("*.yaml"))
    assert len(files) >= 13, f"expected 13+ yaml pivots, got {len(files)}"
    for path in files:
        with path.open(encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        assert isinstance(raw, dict), f"{path.name} must be one mapping"
        for k in ("id", "label", "tier", "description", "input_types",
                  "output_types", "cost", "engine"):
            assert raw.get(k), f"{path.name} missing {k}"
        assert raw["tier"] in ("data", "information", "intelligence",
                               "counter_intelligence"), path.name
        tid = raw["id"]
        assert tid in tr.registry._by_id, f"{tid} not registered"
        assert tr.registry._by_id[tid].runner is not None
    # static pivots: offline, fully substituted at every depth
    cases = [("domain_to_wayback", "domain", "example.com",
              "https://web.archive.org/web/*/example.com"),
             ("cve_to_nvd", "cve", "CVE-2024-0001",
              "https://nvd.nist.gov/vuln/detail/CVE-2024-0001"),
             ("abuse_contact_hint", "domain", "example.com",
              "abuse@example.com")]
    for tid, typ, val, needle in cases:
        res = tr.registry.run(tid, typ, val)
        assert "error" not in res, (tid, res)
        blob = str(res["nodes"]) + str(res["links"])
        assert "{query}" not in blob, (tid, blob)
        assert needle in blob, (tid, needle)
