"""
BDD / regression tests for the v1.5 keyless-origins batch.

  - KO1: every new YAML loads, needs no key, and points at a real parser
  - KO2: each parser extracts the field the source exists for
  - KO3: every new parser is total (hostile payloads never raise)
"""
from __future__ import annotations

from pathlib import Path

import pytest

from estorides_core.parsers import PARSERS, get_parser
from estorides_core.source_loader import SourceRegistry

ROOT = Path(__file__).resolve().parent.parent

NEW_SOURCES = {
    # 01 DNS
    "hstspreload_status": "hstspreload",
    "team_cymru_origin_asn": "dns_json",
    # 02 IP & infrastructure
    "ip_guide": "ip_guide",
    "dbip_free": "dbip_ip",
    "geojs_ip": "geojs_ip",
    "ipapi_is": "ipapi_is",
    "maclookup": "maclookup",
    "peeringdb_net_search": "peeringdb",
    "tranco_rank": "tranco",
    "sans_isc_ip": "sans_isc_ip",
    "tor_exit_nodes": "text_lines",
    # 03 web
    "ssl_labs_analyze": "ssl_labs",
    "gdelt_news": "gdelt",
    "archive_org_search": "archive_org",
    # 04 social
    "bluesky_profile": "bluesky",
    "lemmy_user": "lemmy",
    "gitlab_user": "gitlab_user",
    "codeberg_user": "forgejo_user",
    # 05 threat
    "epss_score": "epss",
    "osv_vulnerability": "osv",
    "cve_org_record": "cve_record",
    "ransomware_live_recent": "ransomware_live",
    "yaraify_search": "yaraify",
    # 06 breach
    "hudsonrock_email": "hudsonrock",
    "disify_email": "disify",
    "gravatar_hash": "gravatar",
    # 07 geolocation
    "photon_geocode": "photon",
    # 08 knowledge
    "openlibrary_search": "openlibrary",
    "pubmed_search": "pubmed",
    "europepmc_search": "europepmc",
    "doaj_search": "doaj",
    # 09 wireless
    "radio_browser_search": "radio_browser",
    # 10 blockchain
    "ofac_sanctions_eth": "address_list",
    # 18 supply chain
    "npm_package": "npm_package",
    "pypi_package": "pypi_package",
    "dockerhub_search": "dockerhub_search",
    "huggingface_models": "huggingface",
    # 21 aerospace
    "adsbfi_aircraft_by_hex": "adsblol_aircraft",
    "planespotters_photos": "planespotters",
    "satnogs_satellite": "satnogs",
    "spaceflightnews_search": "spaceflightnews",
}

BROKER_SOURCES = {"ssl_labs_analyze", "hudsonrock_email", "disify_email"}


@pytest.fixture(scope="module")
def registry() -> dict[str, dict]:
    reg = SourceRegistry(ROOT / "sources")
    reg.load()
    return {s["name"]: s for s in reg.all()}


class TestKO1Registry:
    @pytest.mark.parametrize("name,parser_name", sorted(NEW_SOURCES.items()))
    def test_source_loads_keyless(self, registry: dict, name: str, parser_name: str) -> None:
        assert name in registry, f"{name} did not load"
        src = registry[name]
        assert src["requires_key"] is False
        assert src["parser"] == parser_name
        assert parser_name in PARSERS
        assert src["applies_to"], "applies_to must not be empty"
        assert src["tool"].get("url"), "source needs a url"

    @pytest.mark.parametrize("name", sorted(NEW_SOURCES))
    def test_contact_is_deliberate(self, registry: dict, name: str) -> None:
        expected = "broker" if name in BROKER_SOURCES else "none"
        assert registry[name]["contact"] == expected


class TestKO2Extraction:
    def test_epss(self) -> None:
        out = get_parser("epss")({"data": [{"cve": "CVE-2024-3094", "epss": "0.9", "percentile": "0.99"}]})
        assert out["cve"] == "CVE-2024-3094" and out["epss"] == 0.9

    def test_osv(self) -> None:
        out = get_parser("osv")({
            "id": "CVE-1", "aliases": ["GHSA-x"],
            "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N"}],
            "affected": [{"package": {"ecosystem": "Maven", "name": "log4j"},
                          "ranges": [{"repo": "https://github.com/x/y",
                                      "events": [{"fixed": "2.17.1"}]}]}],
        })
        assert out["packages"] == ["Maven/log4j"]
        assert out["fixed"] == ["2.17.1"]
        assert out["repos"] == ["https://github.com/x/y"]

    def test_cve_record(self) -> None:
        out = get_parser("cve_record")({
            "cveMetadata": {"cveId": "CVE-2024-3094", "state": "PUBLISHED"},
            "containers": {"cna": {
                "title": "xz backdoor",
                "descriptions": [{"lang": "en", "value": "Malicious code"}],
                "metrics": [{"cvssV3_1": {"baseScore": 9.8, "baseSeverity": "CRITICAL",
                                          "vectorString": "CVSS:3.1/AV:N"}}],
                "affected": [{"vendor": "xz", "product": "xz",
                              "versions": [{"version": "5.6.0"}]}],
            }},
        })
        assert out["cve_id"] == "CVE-2024-3094"
        assert out["cvss_score"] == 9.8 and out["severity"] == "CRITICAL"
        assert out["products"] == ["xz/xz"] and out["versions"] == ["5.6.0"]

    def test_hudsonrock(self) -> None:
        out = get_parser("hudsonrock")({
            "message": "infected",
            "stealers": [{
                "total_user_services": 3, "date_compromised": "2024-05-01T00:00:00Z",
                "computer_name": "DESKTOP-1", "malware_path": "C:/x.exe",
                "antiviruses": ["Defender"], "ip": "10.0.*.*",
            }],
        })
        assert out["stealer_count"] == 1
        assert out["computers"] == ["DESKTOP-1"]
        assert out["last_compromised"] == "2024-05-01"

    def test_ip_guide(self) -> None:
        out = get_parser("ip_guide")({
            "ip": "8.8.8.8",
            "network": {"cidr": "8.8.8.0/24",
                        "autonomous_system": {"asn": 15169, "organization": "Google LLC",
                                              "country": "US", "rir": "ARIN"}},
            "location": {"country": "United States", "timezone": "America/Chicago"},
        })
        assert out["cidr"] == "8.8.8.0/24" and out["asn"] == 15169
        assert out["organization"] == "Google LLC"

    def test_maclookup(self) -> None:
        out = get_parser("maclookup")({"found": True, "macPrefix": "00000C",
                                       "company": "Cisco Systems", "country": "US"})
        assert out["found"] is True and out["company"] == "Cisco Systems"

    def test_tranco(self) -> None:
        out = get_parser("tranco")({"ranks": [{"date": "2024-01-01", "rank": 42}]})
        assert out["rank"] == 42 and out["date"] == "2024-01-01"

    def test_sans_isc_ip(self) -> None:
        out = get_parser("sans_isc_ip")({"ip": {
            "number": "1.2.3.4", "as": 64500, "asname": "EXAMPLE",
            "threatfeeds": {"miner": {"firstseen": "2020-01-01", "lastseen": "2020-02-01"}},
        }})
        assert out["ip"] == "1.2.3.4" and out["asn"] == 64500
        assert out["threat_feeds"][0]["name"] == "miner"

    def test_bluesky(self) -> None:
        out = get_parser("bluesky")({
            "did": "did:plc:abc", "handle": "alice.bsky.social",
            "displayName": "Alice", "followersCount": 10, "postsCount": 3,
        })
        assert out["did"] == "did:plc:abc" and out["followers"] == 10

    def test_lemmy(self) -> None:
        out = get_parser("lemmy")({
            "person_view": {
                "person": {"name": "alice", "bio": "hi", "actor_id": "https://l/u/alice"},
                "counts": {"post_count": 5, "comment_count": 7},
                "is_admin": True,
            },
        })
        assert out["username"] == "alice" and out["posts"] == 5 and out["is_admin"] is True

    def test_forgejo_and_gitlab(self) -> None:
        forgejo = get_parser("forgejo_user")({"login": "alice", "full_name": "Alice",
                                              "followers_count": 2, "email": "a@x.io"})
        gitlab = get_parser("gitlab_user")([{"username": "alice", "name": "Alice",
                                             "followers": 4, "state": "active"}])
        assert forgejo["followers"] == 2 and forgejo["email"] == "a@x.io"
        assert gitlab["username"] == "alice" and gitlab["followers"] == 4

    def test_gdelt_and_archive(self) -> None:
        gdelt = get_parser("gdelt")({"articles": [{"url": "https://n.example/a",
                                                   "domain": "n.example", "language": "English"}]})
        archive = get_parser("archive_org")({"response": {"numFound": 3, "docs": [
            {"identifier": "item-1", "title": "T", "mediatype": "texts"}]}})
        assert gdelt["count"] == 1 and gdelt["domains"] == ["n.example"]
        assert archive["count"] == 3
        assert archive["items"][0]["url"] == "https://archive.org/details/item-1"

    def test_ssl_labs(self) -> None:
        out = get_parser("ssl_labs")({"host": "x.io", "status": "READY", "endpoints": [
            {"grade": "A", "ipAddress": "1.1.1.1"},
            {"grade": "C", "ipAddress": "1.1.1.2", "hasWarnings": True}]})
        assert out["grade"] == "C" and out["endpoint_count"] == 2
        assert out["has_warnings"] is True

    def test_hstspreload(self) -> None:
        out = get_parser("hstspreload")({"name": "x.io", "status": "preloaded",
                                         "errors": [{"code": "x", "summary": "s"}]})
        assert out["status"] == "preloaded" and out["error_count"] == 1

    def test_gravatar_and_disify(self) -> None:
        grav = get_parser("gravatar")({"entry": [{"displayName": "Alice",
                                                   "accounts": [{"shortname": "github",
                                                                 "username": "alice"}]}]})
        dis = get_parser("disify")({"domain": "x.io", "disposable": True, "dns": True})
        assert grav["found"] is True and grav["accounts"][0]["username"] == "alice"
        assert dis["disposable"] is True

    def test_package_registries(self) -> None:
        npm = get_parser("npm_package")({"name": "left-pad", "version": "1.0.0",
                                          "maintainers": [{"name": "alice"}],
                                          "dependencies": {"b": "1", "a": "2"}})
        pypi = get_parser("pypi_package")({"info": {"name": "requests",
                                                      "version": "2.0",
                                                      "author_email": "a@x.io"},
                                           "releases": {"2.0": []}})
        docker = get_parser("dockerhub_search")({"count": 1, "results": [
            {"repo_name": "nginx", "is_official": True, "pull_count": 10}]})
        hf = get_parser("huggingface")([{"id": "bert", "likes": 3, "downloads": 9}])
        assert npm["maintainers"] == ["alice"] and npm["dependencies"] == ["a", "b"]
        assert pypi["name"] == "requests" and pypi["releases"] == 1
        assert docker["repositories"][0]["official"] is True
        assert hf["models"][0]["id"] == "bert"

    def test_aerospace_batch(self) -> None:
        photos = get_parser("planespotters")({"photos": [{"id": "1",
                                                            "photographer": "P"}]})
        sat = get_parser("satnogs")([{"name": "ISS", "norad_cat_id": 25544,
                                       "status": "in orbit", "operator": "NASA"}])
        news = get_parser("spaceflightnews")({"count": 1, "results": [
            {"title": "Launch", "news_site": "NASASpaceflight"}]})
        assert photos["count"] == 1
        assert sat["norad_ids"] == [25544] and sat["status"] == "in orbit"
        assert news["articles"][0]["news_site"] == "NASASpaceflight"

    def test_photon_and_radio(self) -> None:
        photon = get_parser("photon")({"features": [{
            "properties": {"name": "Madrid", "country": "Spain"},
            "geometry": {"coordinates": [-3.7, 40.4]}}]})
        radio = get_parser("radio_browser")([{"name": "BBC R1", "country": "GB",
                                               "votes": 5}])
        assert photon["places"][0]["latitude"] == 40.4
        assert radio["stations"][0]["country"] == "GB"

    def test_address_list(self) -> None:
        out = get_parser("address_list")({"raw_text": "0xabc\n0xdef 0x123"})
        assert out["count"] == 3 and out["addresses"] == ["0xabc", "0xdef", "0x123"]


class TestKO3Totality:
    @pytest.mark.parametrize("parser_name", sorted(set(NEW_SOURCES.values())))
    def test_parser_is_total(self, parser_name: str) -> None:
        fn = get_parser(parser_name)
        hostile = (None, "x", 42, [], {}, {"data": None}, {"results": [None]},
                   {"entry": None}, {"features": [None]})
        for payload in hostile:
            assert fn(payload) is not None
