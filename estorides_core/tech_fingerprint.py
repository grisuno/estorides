from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.tech_fingerprint")

MAX_HTML_BYTES = 102_400
MAX_HEADER_BYTES = 10_240

HEADER_PATTERNS: dict[str, list[tuple[re.Pattern[Any], str, str | None, str]]] = {
    "server": [
        (re.compile(r"nginx(?:/([\d.]+))?", re.I), "nginx", None, "server"),
        (re.compile(r"Apache(?:/([\d.]+))?", re.I), "Apache HTTPD", None, "server"),
        (re.compile(r"Microsoft-IIS/([\d.]+)", re.I), "IIS", None, "server"),
        (re.compile(r"OpenResty/([\d.]+)", re.I), "OpenResty", None, "server"),
        (re.compile(r"Caddy(?:/([\d.]+))?", re.I), "Caddy", None, "server"),
        (re.compile(r"cloudflare", re.I), "Cloudflare", None, "cdn"),
        (re.compile(r"CloudFront", re.I), "Amazon CloudFront", None, "cdn"),
    ],
    "x-powered-by": [
        (re.compile(r"PHP(?:/([\d.]+))?", re.I), "PHP", None, "language"),
        (re.compile(r"ASP\.NET(?:/([\d.]+))?", re.I), "ASP.NET", None, "framework"),
        (re.compile(r"Express(?:/([\d.]+))?", re.I), "Express", None, "framework"),
        (re.compile(r"Django(?:/([\d.]+))?", re.I), "Django", None, "framework"),
        (re.compile(r"Rails(?:/([\d.]+))?", re.I), "Ruby on Rails", None, "framework"),
    ],
    "x-generator": [
        (re.compile(r"WordPress ([\d.]+)", re.I), "WordPress", None, "cms"),
        (re.compile(r"Drupal ([\d.]+)", re.I), "Drupal", None, "cms"),
        (re.compile(r"Joomla(?: ([\d.]+))?", re.I), "Joomla", None, "cms"),
        (re.compile(r"Ghost ([\d.]+)", re.I), "Ghost", None, "cms"),
    ],
}

CDN_HEADERS: dict[str, list[tuple[re.Pattern[Any], str]]] = {
    "cf-ray": [(re.compile(r"."), "Cloudflare")],
    "cf-cache-status": [(re.compile(r"."), "Cloudflare")],
    "x-amz-cf-id": [(re.compile(r"."), "Amazon CloudFront")],
    "x-cache": [(re.compile(r"cloudfront", re.I), "Amazon CloudFront")],
    "x-sucuri-id": [(re.compile(r"."), "Sucuri")],
    "x-akamai-*": [(re.compile(r"."), "Akamai")],
    "x-accel-*": [(re.compile(r"."), "Nginx Accelerator")],
}

HTML_META_PATTERNS: list[tuple[re.Pattern[Any], str | None, str | None, str, str | None]] = [
    (re.compile(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', re.I), None, None, "cms", None),
    (re.compile(r'wp-content', re.I), "WordPress", None, "cms", None),
    (re.compile(r'wp-includes', re.I), "WordPress", None, "cms", None),
]

HTML_JS_PATTERNS: list[tuple[re.Pattern[Any], str, str | None, str, re.Pattern[Any] | None]] = [
    (re.compile(r'jquery[-.]?([\d.]+)?(?:\.min)?\.js', re.I), "jQuery", None, "js_library", None),
    (re.compile(r'react(?:\.([\d]+))?(?:\.min)?\.js', re.I), "React", None, "js_library", None),
    (re.compile(r'vue(?:\.([\d]+))?(?:\.min)?\.js', re.I), "Vue.js", None, "js_library", None),
    (re.compile(r'angular(?:\.([\d]+))?(?:\.min)?\.js', re.I), "Angular", None, "js_library", None),
    (re.compile(r'bootstrap(?:\.([\d.]+))?(?:\.min)?\.css', re.I), "Bootstrap", None, "css_framework", None),
    (re.compile(r'font-awesome(?:\.([\d.]+))?(?:\.min)?\.css', re.I), "Font Awesome", None, "css_framework", None),
    (re.compile(r'lodash(?:\.([\d.]+))?(?:\.min)?\.js', re.I), "Lodash", None, "js_library", None),
    (re.compile(r'moment(?:\.([\d.]+))?(?:\.min)?\.js', re.I), "Moment.js", None, "js_library", None),
    (re.compile(r'datatables(?:\.([\d.]+))?(?:\.min)?\.(?:js|css)', re.I), "DataTables", None, "js_library", None),
    (re.compile(r'chart\.(?:min\.)?js', re.I), "Chart.js", None, "js_library", None),
    (re.compile(r'd3\.(?:min\.)?js', re.I), "D3.js", None, "js_library", None),
    (re.compile(r'three\.(?:min\.)?js', re.I), "Three.js", None, "js_library", None),
    (re.compile(r'swiper(?:\.([\d.]+))?(?:\.min)?\.js', re.I), "Swiper", None, "js_library", None),
]

CMS_META_REGEX = re.compile(
    r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']', re.I
)
META_TECH_MAP: dict[str, tuple[str, str]] = {
    "WordPress": ("WordPress", "cms"),
    "Drupal": ("Drupal", "cms"),
    "Joomla": ("Joomla", "cms"),
    "Ghost": ("Ghost", "cms"),
    "Wix": ("Wix", "cms"),
    "Squarespace": ("Squarespace", "cms"),
    "Shopify": ("Shopify", "ecommerce"),
    "Magento": ("Magento", "ecommerce"),
    "WooCommerce": ("WooCommerce", "ecommerce"),
    "MediaWiki": ("MediaWiki", "wiki"),
    "phpBB": ("phpBB", "forum"),
}


@dataclass
class Tech:
    name: str
    category: str
    version: str | None = None
    confidence: float = 0.7
    cve_candidates: list[str] = field(default_factory=list)
    first_seen_in: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class TechFingerprintResult:
    technologies: list[Tech] = field(default_factory=list)
    confidence: float = 0.0
    source_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"technologies": [t.to_dict() for t in self.technologies],
                "confidence": self.confidence, "source_count": self.source_count}


_TRUNCATED_HTML: str = ""


def fingerprint(
    headers: dict[str, str],
    html: str,
    cookies: list[str] | None = None,
    status: int = 200,
) -> TechFingerprintResult:
    global _TRUNCATED_HTML

    html = html[:MAX_HTML_BYTES]
    _TRUNCATED_HTML = html

    tech_map: dict[str, Tech] = {}
    sources: set[str] = set()

    def _add(name: str, category: str, version: str | None, source: str, confidence: float = 0.7) -> None:
        if name in tech_map:
            existing = tech_map[name]
            if version and not existing.version:
                existing.version = version
            existing.confidence = max(existing.confidence, confidence)
            existing.first_seen_in += f",{source}"
        else:
            tech_map[name] = Tech(
                name=name, category=category, version=version,
                confidence=confidence, first_seen_in=source,
            )
        sources.add(source)

    for header_name, patterns in HEADER_PATTERNS.items():
        val = headers.get(header_name, headers.get(header_name.replace("x-", "X-", 1), ""))
        if not val:
            val = headers.get("-".join(p.capitalize() for p in header_name.split("-")), "")
        if val:
            for pat, name, default_ver, cat in patterns:
                m = pat.search(str(val))
                if m:
                    ver = m.group(1) if m.lastindex and m.group(1) else default_ver
                    _add(name, cat, ver, f"header:{header_name}")

    for header_name, cdn_patterns in CDN_HEADERS.items():
        for actual_key in headers:
            if header_name.rstrip("*") in actual_key.lower() or header_name.rstrip("*") == actual_key.lower():
                for pat, name in cdn_patterns:
                    if pat.search(str(headers[actual_key])) or pat.search("."):
                        _add(name, "cdn", None, f"header:{actual_key}", confidence=0.85)
                        break

    meta_match = CMS_META_REGEX.search(html)
    if meta_match:
        content = meta_match.group(1).strip()
        for key, (name, cat) in META_TECH_MAP.items():
            if key.lower() in content.lower():
                ver = content.split(key, 1)[1].strip() if key in content else None
                ver = ver.strip() if ver else None
                _add(name, cat, ver, "html:meta_generator")

    for pat, name, default_ver, cat, _ in HTML_JS_PATTERNS:
        for m in pat.finditer(html):
            ver = None
            if m.lastindex and m.group(1):
                ver = m.group(1)
            elif default_ver:
                ver = default_ver
            _add(name, cat, ver, "html:script_src")

    x_powered = str(headers.get("X-Powered-By", ""))
    if x_powered:
        for pat, name, default_ver, cat in HEADER_PATTERNS.get("x-powered-by", []):
            m = pat.search(x_powered)
            if m:
                ver = m.group(1) if m.lastindex and m.group(1) else default_ver
                _add(name, cat, ver, "header:X-Powered-By")

    set_cookie = str(headers.get("Set-Cookie", ""))
    if set_cookie:
        cookie_techs = [
            (re.compile(r"PHPSESSID", re.I), "PHP", "language"),
            (re.compile(r"ASP\.NET_SessionId", re.I), "ASP.NET", "framework"),
            (re.compile(r"JSESSIONID", re.I), "Java", "language"),
            (re.compile(r"laravel_session", re.I), "Laravel", "framework"),
            (re.compile(r"symfony", re.I), "Symfony", "framework"),
            (re.compile(r"rails", re.I), "Ruby on Rails", "framework"),
            (re.compile(r"django", re.I), "Django", "framework"),
            (re.compile(r"nginx", re.I), "nginx", "server"),
            (re.compile(r"cloudflare", re.I), "Cloudflare", "cdn"),
        ]
        for pat, name, cat in cookie_techs:
            if pat.search(set_cookie):
                _add(name, cat, None, "header:Set-Cookie", confidence=0.6)

    result = TechFingerprintResult(
        technologies=sorted(tech_map.values(), key=lambda t: t.confidence, reverse=True),
        source_count=len(sources),
    )

    if result.technologies:
        avg_conf = sum(t.confidence for t in result.technologies) / len(result.technologies)
        result.confidence = min(1.0, avg_conf * (1 + 0.1 * min(len(result.technologies), 5)))

    return result
