"""BDD tests for spec/map_basemap.md (CARTO basemap, no direct OSM tiles)."""
from __future__ import annotations

import re
from pathlib import Path

JS_PATH = Path(__file__).resolve().parent.parent / "static" / "js" / "estorides.js"


def _js() -> str:
    return JS_PATH.read_text(encoding="utf-8")


def test_no_direct_osm_tiles_S1() -> None:
    urls = re.findall(r"tileLayer\(\s*['\"]([^'\"]+)['\"]", _js())
    assert urls, "S1: a tileLayer URL must exist"
    for u in urls:
        assert "openstreetmap.org" not in u, \
            f"S1: direct OSM tile usage gets banned for scraping, got {u}"


def test_esri_dark_provider_S2() -> None:
    content = _js()
    base = ("https://server.arcgisonline.com/ArcGIS/rest/services/"
            "Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}")
    ref = ("https://server.arcgisonline.com/ArcGIS/rest/services/"
           "Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}")
    assert base in content, "S2: tileLayer must use Esri Dark Gray base"
    assert ref in content, "S2: reference (labels) layer must be present"
    for u in re.findall(r"tileLayer\(\s*['\"]([^'\"]+)['\"]", content):
        assert "apikey" not in u.lower() and "api_key" not in u.lower(), \
            f"S2: basemap must stay keyless, got {u}"


def test_attribution_S3() -> None:
    content = _js()
    assert "OpenStreetMap" in content and "Esri" in content, \
        "S3: attribution must credit OSM contributors and Esri"


def test_csp_allows_tile_host_S5() -> None:
    from estorides_core.web_security import WebSecurityConfig
    cfg = WebSecurityConfig()
    m = re.search(r"img-src([^;]*);", cfg.csp_policy)
    assert m is not None, "CSP must define img-src"
    src = m.group(1)
    assert "https:" in src or "arcgisonline.com" in src, \
        f"S5: img-src must allow the tile CDN, got: {src!r}"
