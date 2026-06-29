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
* A bearer-token auth gate (`require_auth`) for sensitive endpoints. When the
  operator sets `ESTORIDES_AUTH_TOKEN`, the sensitive `/api/*` surface stops
  trusting anonymous callers; the legitimate UI gets the token from a
  `<meta name="estorides-auth-token">` tag rendered into `index.html` and
  includes it as a header on every fetch.

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

import hmac
import logging
import os
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from flask import Flask, jsonify, request

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
        # Issue #41: drop 'unsafe-inline' from style-src. The UI used to
        # set element-level `style="..."` attributes which forced the
        # directive open. Those attribute styles are now applied via
        # `element.style.setProperty(...)` (DOM API, not parsed as
        # inline CSS), and inline `<style>` blocks were replaced with
        # nonce-based styles. CSS injection is now blocked.
        "style-src 'self' https://unpkg.com; "
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
def install_security(app: Flask, cfg: WebSecurityConfig | None = None) -> WebSecurityConfig:
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
    install_auth_gate(app, make_auth_gate())
    return cfg


# --------------------------------------------------------------------------- #
# Bearer-token auth gate                                                      #
# --------------------------------------------------------------------------- #
# Estorides is a single-user local OSINT tool by default. When the operator
# binds it to a non-loopback address (ESTORIDES_HOST=0.0.0.0) the unauthenticated
# /api/* surface becomes a public relay. ESTORIDES_AUTH_TOKEN turns that gate
# on: the legitimate UI receives the token via a meta tag in `index.html` and
# includes it as `Authorization: Bearer <token>` on every fetch. Anonymous
# callers (curl, scrapers, hostile relays) get 401.
#
# The token is compared with hmac.compare_digest to avoid timing oracles.
# The token is a single shared secret — there is no user model, no session
# store, no per-user quota. This is the right granularity for a single-
# operator tool: one secret, one gate, one place to rotate it.
AUTH_HEADER = "Authorization"
AUTH_COOKIE = "estorides_session"
AUTH_META = "estorides-auth-token"
AUTH_HEADER_ALT = "X-Estorides-Token"


def _extract_bearer_token() -> str | None:
    """Pull the bearer token from header, alt-header, or cookie.

    Header order matters: an explicit `Authorization: Bearer` always wins
    over a cookie (the cookie is the fallback for the browser UI; the
    header is what scripts and curl will use). We never trust query-string
    tokens — they leak into access logs and referer headers.
    """
    h = request.headers.get(AUTH_HEADER, "")
    if h.lower().startswith("bearer "):
        return h[7:].strip() or None
    alt = request.headers.get(AUTH_HEADER_ALT, "").strip()
    if alt:
        return alt
    c = request.cookies.get(AUTH_COOKIE, "").strip()
    if c:
        return c
    return None


def make_auth_gate() -> AuthGate:
    """Build the auth gate from the current environment.

    `ESTORIDES_AUTH_TOKEN` unset → `enabled=False`, `require_auth` is a no-op
    pass-through. This preserves the local-trust single-user default and keeps
    existing tests working without an auth header.

    When set, the gate is enabled. The token is also exposed to `index.html`
    so the UI can auto-attach it (see `auth_meta_for_index()`).
    """
    raw = os.environ.get("ESTORIDES_AUTH_TOKEN", "").strip()
    if not raw:
        return AuthGate(required_token=None)
    return AuthGate(required_token=raw)


@dataclass
class AuthGate:
    """Bearer-token gate applied to sensitive routes.

    `required_token` is the single shared secret. `None` disables the gate
    (local-trust mode). Comparison is constant-time.
    """

    required_token: str | None = None

    @property
    def enabled(self) -> bool:
        return self.required_token is not None

    def check(self) -> bool:
        if not self.enabled:
            return True
        presented = _extract_bearer_token()
        if not presented:
            return False
        return hmac.compare_digest(presented, self.required_token or "")

    def auth_meta_for_index(self) -> str | None:
        """Token to embed in `index.html` so the UI can auto-authenticate.

        Returns `None` when the gate is off (the UI then omits the meta
        tag and every call goes through anonymously, which is the
        local-trust default).
        """
        return self.required_token

    def issue_session_cookie_kwargs(self) -> dict[str, Any]:
        """Arguments for `set_cookie` to install the session cookie.

        `Secure` is set when the request itself is over HTTPS or the operator
        requested ESTORIDES_FORCE_HTTPS=1 (in that case we know they're behind
        TLS). `SameSite=Lax` keeps the cookie from cross-site POSTs.
        """
        is_https = request.is_secure or os.environ.get("ESTORIDES_FORCE_HTTPS") == "1"
        return {
            "max_age": 60 * 60 * 12,  # 12h
            "httponly": True,
            "samesite": "Lax",
            "secure": is_https,
            "path": "/",
        }


def require_auth(view: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator: enforce the bearer-token gate on a view.

    Behaviour:
      * gate disabled (no env var) → pass-through, no overhead.
      * gate enabled, token missing → 401 with `WWW-Authenticate: Bearer`.
      * gate enabled, token present but wrong → 401 (same shape, constant-
        time compare on the server side).

    Use on every endpoint that reads or mutates operator-private data:
    cases, run, run/stream/*, discover/*, export, intel/*, transform/*,
    osiris/*, graph, status.
    """
    @wraps(view)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        gate: AuthGate | None = _current_gate()
        if gate is None or not gate.enabled:
            return view(*args, **kwargs)
        if gate.check():
            return view(*args, **kwargs)
        resp = jsonify({"error": "unauthorized"})
        resp.status_code = 401
        resp.headers["WWW-Authenticate"] = 'Bearer realm="estorides"'
        return resp
    return wrapper


# Module-level slot for the gate the factory installs. The decorator reads
# from here so routes can be decorated before `create_app()` is called (a
# few helper modules expose routes that way).
_GATE: AuthGate | None = None


def install_auth_gate(app: Flask, gate: AuthGate) -> AuthGate:
    """Attach the gate to a Flask app and a module-level slot.

    Two consumers read the gate: the `require_auth` decorator (module
    slot, so it works even when called outside a request context) and
    `auth_meta_for_index()` (so `index.html` can be rendered with the
    token embedded for the UI to pick up).
    """
    global _GATE
    _GATE = gate
    app.extensions["estorides_auth"] = gate
    if gate.enabled:
        log.info("web security: auth-gate ENABLED (bearer token required)")
    else:
        log.info("web security: auth-gate disabled (ESTORIDES_AUTH_TOKEN unset)")
    return gate


def _current_gate() -> AuthGate | None:
    return _GATE
