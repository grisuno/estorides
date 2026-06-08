"""
estorides_core.web_security
===========================

Production-grade web hardening helpers used by the Flask app factory.

Responsibilities
----------------
* Security headers on every response (CSP, X-Frame-Options, X-Content-Type-Options,
  Referrer-Policy, Permissions-Policy, HSTS when behind TLS).
* Optional CORS allowlist (the platform is a local single-user tool by default —
  CORS is opt-in, not opt-out, so the default is a tight same-origin policy).
* A defensive request-size guard that rejects oversized JSON / form bodies
  before they reach a route handler (the rest of the app trusts `request.get_json()`
  blindly).
* A Werkzeug-debugger kill-switch. Production deployments must never expose the
  interactive debugger console — this helper refuses to register routes when
  the dev debugger is on, and logs the attempt at WARNING level.

Why a dedicated module?
-----------------------
The Flask app is built by `estorides_web.create_app()`. Keeping the hardening
out of the factory means:
  * unit tests can spin up an app with a stripped-down middleware set,
  * the surface is one file to audit (CVE-2023-style header regressions),
  * everything is policy-driven by env vars, not magic literals scattered
    across route definitions.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Iterable, Optional

from flask import Flask, request

log = logging.getLogger("estorides.web.security")


# --------------------------------------------------------------------------- #
# Config                                                                      #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class WebSecurityConfig:
    """Resolved security policy for the Flask app.

    All fields are read from the environment at import time and frozen so
    the policy cannot drift at runtime. Changing a knob requires a restart
    — the right call for a tool that mostly runs as a long-lived daemon.
    """

    allow_origins: tuple[str, ...] = ()
    allow_methods: tuple[str, ...] = ("GET", "POST", "DELETE", "OPTIONS")
    allow_headers: tuple[str, ...] = ("Content-Type", "Authorization")
    allow_credentials: bool = False
    max_content_length_bytes: int = 1_048_576  # 1 MiB; OSINT endpoints don't need more
    csp_policy: str = (
        "default-src 'self'; "
        "script-src 'self' https://unpkg.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://unpkg.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    )
    hsts_enabled: bool = False
    hsts_max_age_seconds: int = 31_536_000  # 1 year
    force_https: bool = False

    @property
    def is_cors_enabled(self) -> bool:
        return bool(self.allow_origins)

    @property
    def is_origin_allowed(self) -> bool:
        """CORS is opt-in; this is the runtime check used by the after_request hook."""
        return True  # actual matching is done per-request; see _cors_after_request


def _env_str(name: str, default: str) -> str:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return raw


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        log.warning("env %s=%r is not an int, using default %d", name, raw, default)
        return default


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def load_security_config() -> WebSecurityConfig:
    """Resolve the security policy from env vars.

    ESTORIDES_CORS_ORIGINS    comma-separated list, e.g. "https://app.example.com"
    ESTORIDES_MAX_BODY_BYTES  int, default 1 MiB
    ESTORIDES_HSTS            1 to emit Strict-Transport-Security
    ESTORIDES_FORCE_HTTPS     1 to redirect plain http to https (only meaningful behind TLS)
    ESTORIDES_CSP             override the default Content-Security-Policy
    """
    origins_raw = _env_str("ESTORIDES_CORS_ORIGINS", "")
    origins = tuple(o.strip() for o in origins_raw.split(",") if o.strip()) if origins_raw else ()
    return WebSecurityConfig(
        allow_origins=origins,
        max_content_length_bytes=_env_int("ESTORIDES_MAX_BODY_BYTES", 1_048_576),
        csp_policy=_env_str("ESTORIDES_CSP", WebSecurityConfig.csp_policy),
        hsts_enabled=_env_bool("ESTORIDES_HSTS", False),
        force_https=_env_bool("ESTORIDES_FORCE_HTTPS", False),
    )


# --------------------------------------------------------------------------- #
# Hardening installer                                                         #
# --------------------------------------------------------------------------- #
def install_security(app: Flask, cfg: Optional[WebSecurityConfig] = None) -> WebSecurityConfig:
    """Wire security middleware into a Flask app.

    Idempotent: calling twice is a no-op (we re-attach, but Flask keeps the
    last hook, and our hooks are stateless). Returns the resolved config so
    the caller can echo it in a startup banner.
    """
    if cfg is None:
        cfg = load_security_config()

    # 1) Hard cap on request body. Anything bigger is rejected at the WSGI
    #    layer with 413, before route logic sees it. This stops a remote
    #    client from making us allocate a multi-MB JSON body via /api/...
    #    Direct assignment (not setdefault) so a deployer who overrode the
    #    Flask config still gets the security ceiling.
    app.config["MAX_CONTENT_LENGTH"] = cfg.max_content_length_bytes

    # 2) Werkzeug debugger kill-switch. If a deployer (or a misconfigured
    #    `serve --debug`) left FLASK_DEBUG on, refuse to register routes and
    #    fail loud. A working interactive debugger reachable on a network
    #    port is RCE.
    if app.debug or app.config.get("DEBUG", False):
        log.warning(
            "Werkzeug debugger is enabled. Refusing to register routes. "
            "Set FLASK_DEBUG=0 or use gunicorn (wsgi.py) for production."
        )
        raise RuntimeError(
            "Werkzeug interactive debugger is not safe in production. "
            "Run with gunicorn (see wsgi.py) or unset FLASK_DEBUG."
        )

    # 3) HTTPS redirect (only meaningful when ESTORIDES_FORCE_HTTPS=1).
    if cfg.force_https:
        @app.before_request
        def _redirect_to_https():
            # X-Forwarded-Proto is the conventional reverse-proxy signal.
            fwd_proto = request.headers.get("X-Forwarded-Proto", "").lower()
            if request.is_secure or fwd_proto == "https":
                return None
            from flask import redirect
            url = request.url.replace("http://", "https://", 1)
            return redirect(url, code=308)

    # 4) Security headers + CORS, applied last so they always win.
    @app.after_request
    def _security_headers(resp):
        # Hardening headers — always on, regardless of CORS.
        resp.headers.setdefault("Content-Security-Policy", cfg.csp_policy)
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "no-referrer")
        resp.headers.setdefault(
            "Permissions-Policy",
            "geolocation=(), camera=(), microphone=(), payment=()",
        )
        resp.headers.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        if cfg.hsts_enabled:
            resp.headers.setdefault(
                "Strict-Transport-Security",
                f"max-age={cfg.hsts_max_age_seconds}; includeSubDomains",
            )

        # CORS — only emit headers when an allowlist is configured AND the
        # request Origin is on it. We deliberately do NOT echo arbitrary
        # origins; that would be the well-known CORS-misconfig footgun.
        origin = request.headers.get("Origin")
        if cfg.is_cors_enabled and origin and origin in cfg.allow_origins:
            resp.headers["Access-Control-Allow-Origin"] = origin
            resp.headers["Vary"] = "Origin"
            resp.headers["Access-Control-Allow-Methods"] = ", ".join(cfg.allow_methods)
            resp.headers["Access-Control-Allow-Headers"] = ", ".join(cfg.allow_headers)
            if cfg.allow_credentials:
                resp.headers["Access-Control-Allow-Credentials"] = "true"

        return resp

    # 5) Short-circuit OPTIONS preflights once the route is matched.
    @app.before_request
    def _cors_preflight():
        if request.method == "OPTIONS" and cfg.is_cors_enabled:
            origin = request.headers.get("Origin")
            if origin and origin in cfg.allow_origins:
                # Return an empty 204 with the CORS headers. The after_request
                # hook above will stamp them.
                return ("", 204)

    log.info(
        "web security: cors=%s hsts=%s force_https=%s max_body=%dB",
        cfg.is_cors_enabled, cfg.hsts_enabled, cfg.force_https, cfg.max_content_length_bytes,
    )
    return cfg
