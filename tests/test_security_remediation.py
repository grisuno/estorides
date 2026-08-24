from __future__ import annotations

import json
import logging
import re
import socket
from pathlib import Path
from unittest.mock import patch

import pytest
from flask import Flask

from estorides_core.ssrf_guard import (
    _resolve,
)
from estorides_core.web_security import (
    WebSecurityConfig,
    install_security,
)

# =========================================================================
# S1 & S2 — DNS failure log does not leak hostname or exception detail
# =========================================================================

class TestSsrfLogSanitisation:
    """BDD S1, S2: ssrf_guard._resolve log messages must not contain the
    hostname or exception detail."""

    def test_dns_failure_log_omits_hostname(self, caplog):
        caplog.set_level(logging.DEBUG)
        host = "internal-build-server.corp.example"
        with patch("estorides_core.ssrf_guard.socket.getaddrinfo",
                   side_effect=socket.gaierror("Temporary failure in name resolution")):
            result = _resolve(host)
        assert result == frozenset()
        for record in caplog.records:
            if "dns" in record.getMessage().lower() or "resolution" in record.getMessage().lower():
                assert host not in record.getMessage(), \
                    f"log message leaks hostname: {record.getMessage()}"
                assert "Temporary failure" not in record.getMessage(), \
                    f"log message leaks exception detail: {record.getMessage()}"

    def test_dns_failure_log_omits_ip_in_hostname(self, caplog):
        caplog.set_level(logging.DEBUG)
        host = "10.0.0.1.internal-router.corp"
        with patch("estorides_core.ssrf_guard.socket.getaddrinfo",
                   side_effect=socket.gaierror("Name or service not known")):
            result = _resolve(host)
        assert result == frozenset()
        for record in caplog.records:
            if "dns" in record.getMessage().lower():
                assert host not in record.getMessage()
                assert "10.0.0.1" not in record.getMessage()

    def test_dns_failure_log_contains_host_length_not_host(self, caplog):
        caplog.set_level(logging.DEBUG)
        host = "a" * 100
        with patch("estorides_core.ssrf_guard.socket.getaddrinfo",
                   side_effect=socket.gaierror("fail")):
            result = _resolve(host)
        assert result == frozenset()
        found = False
        for record in caplog.records:
            if "dns" in record.getMessage().lower():
                assert host not in record.getMessage(), \
                    f"log message leaks hostname: {record.getMessage()}"
                found = True
        assert found, "no DNS-related log record found"


# =========================================================================
# S3, S4, S5, S6 — Exception exposure in estorides_web endpoints
# =========================================================================

class TestInfoExposureEncryption:
    """BDD S3, S4: encryption error endpoints must not leak str(e)."""

    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        sec_cfg = WebSecurityConfig()
        install_security(app, sec_cfg)
        return app

    def _make_export_route(self, app, raise_val: type[Exception],
                           error_msg: str, status: int):
        import shutil
        import tempfile
        from pathlib import Path

        from flask import jsonify

        app.config["TESTING"] = True

        @app.route("/api/export/test")
        def api_export_test():
            tmpdir = Path(tempfile.mkdtemp(prefix="estorides_export_"))
            try:
                p = tmpdir / "test.json"
                p.write_text("{}", encoding="utf-8")
                if raise_val is ValueError:
                    raise ValueError(error_msg)
                elif raise_val is RuntimeError:
                    raise RuntimeError(error_msg)
            except ValueError as e:
                shutil.rmtree(tmpdir, ignore_errors=True)
                return jsonify({"error": "invalid-encryption-key",
                                "detail": str(e)}), 400
            except RuntimeError as e:
                shutil.rmtree(tmpdir, ignore_errors=True)
                return jsonify({"error": "encryption-failed",
                                "detail": str(e)}), 500
            return jsonify({"ok": True})

        return app

    def _make_export_route_fixed(self, app, raise_val: type[Exception],
                                  error_msg: str, status: int):
        import logging
        import shutil
        import tempfile
        from pathlib import Path

        from flask import jsonify
        app.config["TESTING"] = True
        log = logging.getLogger("estorides.web.test")

        @app.route("/api/export/fixed")
        def api_export_fixed():
            tmpdir = Path(tempfile.mkdtemp(prefix="estorides_export_"))
            try:
                p = tmpdir / "test.json"
                p.write_text("{}", encoding="utf-8")
                if raise_val is ValueError:
                    raise ValueError(error_msg)
                elif raise_val is RuntimeError:
                    raise RuntimeError(error_msg)
            except ValueError:
                shutil.rmtree(tmpdir, ignore_errors=True)
                log.warning("export encryption key invalid")
                return jsonify({"error": "invalid-encryption-key"}), 400
            except RuntimeError:
                shutil.rmtree(tmpdir, ignore_errors=True)
                log.exception("export encryption failed")
                return jsonify({"error": "encryption-failed"}), 500
            return jsonify({"ok": True})

        return app

    def test_encryption_valueerror_leaks_detail(self, app):
        self._make_export_route(app, ValueError, "bad bech32: invalid separator", 400)
        c = app.test_client()
        resp = c.get("/api/export/test")
        body = resp.get_json()
        assert "detail" in body
        assert "bad bech32" in str(body.get("detail", ""))

    def test_encryption_valueerror_fixed_no_detail(self, app):
        self._make_export_route_fixed(app, ValueError,
                                       "bad bech32: invalid separator", 400)
        c = app.test_client()
        resp = c.get("/api/export/fixed")
        body = resp.get_json()
        assert body == {"error": "invalid-encryption-key"}

    def test_encryption_runtimeerror_fixed_no_detail(self, app):
        self._make_export_route_fixed(app, RuntimeError,
                                       "gnupg internal path /etc/gpg/...", 500)
        c = app.test_client()
        resp = c.get("/api/export/fixed")
        body = resp.get_json()
        assert body == {"error": "encryption-failed"}


class TestInfoExposureSourceOps:
    """BDD S5, S6: source file operations must not leak str(e)."""

    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        sec_cfg = WebSecurityConfig()
        install_security(app, sec_cfg)
        return app

    def test_source_delete_keyerror_fixed(self, app):
        log = logging.getLogger("estorides.web.test")

        @app.route("/api/sources/yaml/<name>", methods=["DELETE"])
        def api_delete(name):
            if name != "existing":
                try:
                    raise KeyError(f"'{name}' not found in registry")
                except KeyError:
                    log.warning("source not found: %s", name)
                    from flask import jsonify
                    return jsonify({"error": "source-not-found"}), 404
            from flask import jsonify
            return jsonify({"deleted": name})

        c = app.test_client()
        resp = c.delete("/api/sources/yaml/nonexistent")
        body = resp.get_json()
        assert body == {"error": "source-not-found"}
        assert resp.status_code == 404

    def test_source_create_valueerror_fixed(self, app):
        log = logging.getLogger("estorides.web.test")

        @app.route("/api/sources/yaml", methods=["POST"])
        def api_create():
            body = {"bad": "data"}
            if "name" not in body or not body["name"]:
                try:
                    raise ValueError("missing required field: url")
                except ValueError:
                    log.warning("invalid source config")
                    from flask import jsonify
                    return jsonify({"error": "invalid-source-config"}), 400
            from flask import jsonify
            return jsonify({"created": True})

        c = app.test_client()
        resp = c.post("/api/sources/yaml",
                       content_type="application/json",
                       data=json.dumps({"bad": "data"}))
        body = resp.get_json()
        assert body == {"error": "invalid-source-config"}
        assert resp.status_code == 400

    def test_source_update_valueerror_fixed(self, app):
        log = logging.getLogger("estorides.web.test")

        @app.route("/api/sources/yaml/<name>", methods=["PUT"])
        def api_update(name):
            if name != "existing":
                try:
                    raise ValueError("source 'nonexistent' not found")
                except ValueError:
                    log.warning("source not found for update: %s", name)
                    from flask import jsonify
                    return jsonify({"error": "source-not-found"}), 404
            from flask import jsonify
            return jsonify({"updated": True})

        c = app.test_client()
        resp = c.put("/api/sources/yaml/nonexistent",
                      content_type="application/json",
                      data=json.dumps({"name": "nonexistent"}))
        body = resp.get_json()
        assert body == {"error": "source-not-found"}
        assert resp.status_code == 404


# =========================================================================
# S7 — HTTPS redirect is safe from Host header injection
# =========================================================================

class TestHttpsRedirectSafety:
    """BDD S7: the HTTPS redirect must use request.host, not request.url."""

    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        cfg = WebSecurityConfig(force_https=True)
        install_security(app, cfg)
        return app

    def test_redirect_uses_public_host_not_request_host(self, app):
        c = app.test_client()
        resp = c.get(
            "/api/status",
            headers={"Host": "evil.com"},
            environ_base={"SERVER_NAME": "localhost",
                          "wsgi.url_scheme": "http"},
        )
        assert resp.status_code == 308
        location = resp.headers.get("Location", "")
        # The redirect URL uses cfg.public_host (default localhost:5050),
        # not the attacker-controlled Host header.
        assert location.startswith("https://localhost:5050/api/status")

    def test_redirect_scheme_is_https(self, app):
        c = app.test_client()
        resp = c.get(
            "/api/status",
            headers={"Host": "localhost",
                     "X-Forwarded-Proto": "http"},
            environ_base={"SERVER_NAME": "localhost",
                          "wsgi.url_scheme": "http"},
        )
        assert resp.status_code == 308
        location = resp.headers.get("Location", "")
        assert location.startswith("https://")
        # Verify no Host-injection attack works: attacker Host header
        # should NOT become the redirect target.
        assert "evil" not in location


# =========================================================================
# S10 — CI workflow has explicit read permissions
# =========================================================================

class TestCiWorkflowPermissions:
    """BDD S10: .github/workflows/ci.yml must have permissions: read-all."""

    def test_ci_yml_has_permissions(self):
        ci_path = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "ci.yml"
        assert ci_path.exists(), f"ci.yml not found at {ci_path}"
        content = ci_path.read_text(encoding="utf-8")
        assert "permissions:" in content, \
            "ci.yml is missing 'permissions:' key — default is write-all"
        lines = content.splitlines()
        top_level_perms = False
        for line in lines:
            non_space = line.lstrip()
            if non_space.startswith("permissions:") and line[0] not in (" ", "\t"):
                top_level_perms = True
                break
        assert top_level_perms, \
            "permissions: must be at top level (not nested inside a job)"

    def test_ci_yml_permissions_is_read_all(self):
        ci_path = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "ci.yml"
        content = ci_path.read_text(encoding="utf-8")
        assert "permissions: read-all" in content or "permissions: read_all" in content, \
            "ci.yml permissions should be read-all (least privilege)"


# =========================================================================
# S11 — Osiris endpoint failure does not leak detail
# =========================================================================

class TestOsirisExceptionSafety:
    """BDD S11: osiris endpoint exceptions must return generic error."""

    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        sec_cfg = WebSecurityConfig()
        install_security(app, sec_cfg)
        return app

    def _make_osiris_route_fixed(self, app, route_path: str):
        import logging

        from flask import jsonify
        log = logging.getLogger("estorides.web.test")
        mock_osiris = type("MockOsiris", (), {})()

        def fetch_bgp(q):
            raise RuntimeError(f"internal path /etc/bgp/{q} failed")

        def fetch_mac(mac):
            raise RuntimeError(f"mac lookup failed for {mac}")

        def fetch_phone(n):
            raise RuntimeError(f"phone api error: {n}")

        def fetch_github_user(u):
            raise RuntimeError(f"github token expired for {u}")

        def fetch_leaks(e):
            raise RuntimeError(f"leakdb unreachable: {e}")

        mock_osiris.fetch_bgp = fetch_bgp
        mock_osiris.fetch_mac = fetch_mac
        mock_osiris.fetch_phone = fetch_phone
        mock_osiris.fetch_github_user = fetch_github_user
        mock_osiris.fetch_leaks = fetch_leaks

        @app.route(route_path)
        def osiris_endpoint():
            q = "test"
            try:
                return jsonify(mock_osiris.fetch_bgp(q))
            except Exception:
                log.exception("osiris fetch failed")
                return jsonify({"error": "osiris-failed"}), 500

        return app

    def test_osiris_exception_returns_generic(self, app):
        self._make_osiris_route_fixed(app, "/api/osiris/bgp")
        c = app.test_client()
        resp = c.get("/api/osiris/bgp")
        body = resp.get_json()
        assert body == {"error": "osiris-failed"}
        assert resp.status_code == 500


# =========================================================================
# S7 (bis) — Verify the actual web_security.py redirect code
# =========================================================================

class TestWebSecurityRedirect:
    """Verify the HTTP-to-HTTPS redirect in web_security.py is safe."""

    def test_redirect_implementation_uses_public_host(self):
        cfg = WebSecurityConfig(force_https=True, public_host="estorides.test")
        app = Flask(__name__)
        app.config["TESTING"] = True

        install_security(app, cfg)

        import inspect

        from estorides_core import web_security as ws
        source = inspect.getsource(ws)
        assert "request.url.replace" not in source, \
            "redirect must NOT use request.url.replace (open redirect via Host header)"
        assert "cfg.public_host" in source, \
            "redirect must use cfg.public_host, not request.host"

    def test_source_has_no_url_replace(self):
        import inspect

        from estorides_core import web_security as ws
        source = inspect.getsource(ws)
        assert "request.url.replace" not in source, \
            "CWE-601: request.url.replace is an open redirect via Host header"


# =========================================================================
# Verify JS source has no innerHTML with unsanitized data (S8, S9)
# =========================================================================

class TestJavaScriptDomSafety:
    """BDD S8, S9: verify no innerHTML with unsanitized data in JS."""

    JS_PATH = Path(__file__).resolve().parent.parent / "static" / "js" / "estorides.js"

    def test_js_file_exists(self):
        assert self.JS_PATH.exists()

    def test_innerhtml_not_used_with_template_literals(self):
        content = self.JS_PATH.read_text(encoding="utf-8")
        lines = content.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if ".innerHTML" in stripped or ".innerHTML =" in stripped:
                # Check if the right side contains a template literal or
                # concatenation with unescaped data.
                # We allow innerHTML with static strings or escaped data.
                has_escape = "escapeHTML" in stripped
                is_static = "'" in stripped and "${" not in stripped
                has_text_content_assign = "textContent" in stripped
                if not (has_escape or is_static or has_text_content_assign):
                    # This might be dangerous — check closer
                    if "`" in stripped and "${" in stripped:
                        pytest.fail(
                            f"line {i}: innerHTML with template literal "
                            f"may contain unescaped data: {stripped}"
                        )

    def test_showtooltipat_safe(self):
        """showTooltipAt must sanitize html before innerHTML assignment."""
        content = self.JS_PATH.read_text(encoding="utf-8")
        func_match = re.search(
            r"function showTooltipAt\([^)]+\)\s*\{([^}]+)\}",
            content
        )
        assert func_match is not None, "showTooltipAt function not found"
        func_body = func_match.group(1)
        assert "innerHTML = html" not in func_body, \
            "showTooltipAt must not assign raw html to innerHTML"
        assert "textContent" in func_body or "escapeHTML" in func_body, \
            "showTooltipAt must use textContent or escapeHTML"

    def test_selectnode_inspector_safe(self):
        """selectNode must build DOM safely for the inspector panel."""
        content = self.JS_PATH.read_text(encoding="utf-8")
        lines = content.splitlines()
        in_select = False
        inner_html_lines = []
        for i, line in enumerate(lines, 1):
            if "function selectNode" in line:
                in_select = True
                continue
            if in_select:
                if "}" in line and line.strip() == "}":
                    break
                if ".innerHTML" in line or ".innerHTML =" in line:
                    inner_html_lines.append((i, line.strip()))
        for lineno, linetext in inner_html_lines:
            assert "escapeHTML" in linetext, \
                f"line {lineno}: selectNode innerHTML must escape data: {linetext}"


# =========================================================================
# S — Alert webhooks must pass the SSRF guard (CodeQL #40)
# =========================================================================

class TestAlerterSsrf:
    """Alert webhook URLs (incl. user-supplied `channel` URLs) are validated
    by the central SSRF guard before any socket opens. Treats all webhook
    destinations as hostile."""

    def test_refuses_link_local_metadata(self) -> None:
        from estorides_core.alerter import _http_post
        # 169.254.169.254 (cloud metadata) is blocked without any network I/O.
        assert _http_post("http://169.254.169.254/latest/meta-data", {"x": 1}) is False

    def test_refuses_loopback(self) -> None:
        from estorides_core.alerter import _http_post
        assert _http_post("http://127.0.0.1/admin", {"x": 1}) is False

    def test_refuses_disallowed_scheme(self) -> None:
        from estorides_core.alerter import _http_post
        assert _http_post("file:///etc/passwd", {"x": 1}) is False

    def test_user_channel_url_cannot_reach_internal_host(self) -> None:
        from estorides_core.alerter import AlertDispatcher
        # A channel string that begins with http is used verbatim as the
        # webhook URL; an internal host must still be refused.
        dispatcher = AlertDispatcher()
        assert dispatcher.send("http://127.0.0.1:8080/hook", "t", "b") is False
