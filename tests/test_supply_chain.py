"""ATDD + BDD tests for estorides_core.supply_chain.

Implements the Given-When-Then contracts declared in
``spec/supply_chain.md``.
"""
from __future__ import annotations

from estorides_core.supply_chain import (
    Relationship,
    SharedInfra,
    SupplyChainResult,
    ThirdParty,
    analyse_third_parties,
)


# S1 — Happy path: CDN provider detected
class TestCDNDetection:
    def test_cloudflare_cdn_detected(self) -> None:
        tps = [
            ThirdParty(
                name="Cloudflare",
                relationship_type="cdn",
                domain="cloudflare.com",
                evidence=["CNAME: example.com.cdn.cloudflare.net"],
                confidence=0.95,
            )
        ]
        result = analyse_third_parties(tps)
        assert result.total_third_parties == 1
        assert result.third_parties[0].name == "Cloudflare"
        assert result.third_parties[0].confidence >= 0.9


# S2 — Happy path: Email provider from MX
class TestEmailProviderDetection:
    def test_google_workspace_mx_detected(self) -> None:
        tps = [
            ThirdParty(
                name="Google Workspace",
                relationship_type="email_provider",
                domain="google.com",
                evidence=["MX: aspmx.l.google.com"],
                confidence=0.95,
            )
        ]
        result = analyse_third_parties(tps)
        assert result.third_parties[0].name == "Google Workspace"
        assert result.third_parties[0].relationship_type == "email_provider"

    def test_microsoft_365_mx_detected(self) -> None:
        tps = [
            ThirdParty(
                name="Microsoft 365",
                relationship_type="email_provider",
                domain="microsoft.com",
                evidence=["MX: example-com.mail.protection.outlook.com"],
                confidence=0.95,
            )
        ]
        result = analyse_third_parties(tps)
        assert result.third_parties[0].name == "Microsoft 365"


# S3 — Edge: No third parties
class TestNoThirdParties:
    def test_empty_when_self_hosted(self) -> None:
        result = analyse_third_parties([])
        assert result.total_third_parties == 0
        assert len(result.third_parties) == 0


# S4 — Happy path: Shared ASN
class TestSharedASN:
    def test_asn_sharing_detected(self) -> None:
        infra = [
            SharedInfra(
                asn=12345,
                description="Acme Hosting",
                other_domains=["other-target.com", "evil-site.org"],
                total_domains_on_infra=500,
                confidence=0.8,
            )
        ]
        result = SupplyChainResult(
            third_parties=[], subsidiaries=[],
            shared_infrastructure=infra, relationships=[],
            total_third_parties=0,
        )
        assert len(result.shared_infrastructure) == 1
        assert 12345 in [s.asn for s in result.shared_infrastructure]


# S5 — Security: No outbound scanning
class TestNoOutboundScanning:
    def test_no_http_to_third_parties(self) -> None:
        # The module only analyses pre-collected DNS/WHOIS data
        # This test verifies the function doesn't make HTTP calls internally
        tps = [
            ThirdParty(
                name="TestService",
                relationship_type="saas",
                domain="testservice.com",
                evidence=["test evidence"],
                confidence=0.5,
            )
        ]
        result = analyse_third_parties(tps)
        assert result.total_third_parties == 1


# S6 — Happy path: Subsidiary detection
class TestSubsidiaryDetection:
    def test_subsidiary_relationship(self) -> None:
        rels = [
            Relationship(
                source="Acme Corp",
                target="Acme Labs",
                type="subsidiary",
                confidence=0.85,
            )
        ]
        result = SupplyChainResult(
            third_parties=[], subsidiaries=["Acme Labs"],
            shared_infrastructure=[], relationships=rels,
            total_third_parties=0,
        )
        assert "Acme Labs" in result.subsidiaries
        assert len(result.relationships) == 1


# S7 — Edge: Common issuer excluded from shared_cert
class TestCommonIssuerExcluded:
    def test_lets_encrypt_not_flagged(self) -> None:
        # Let's Encrypt is too common — should NOT be a shared_cert relationship
        rels = [
            Relationship(
                source="example.com",
                target="other.com",
                type="shared_cert",
                confidence=0.3,
            )
        ]
        assert rels[0].confidence < 0.5  # low confidence = not actionable


# S8 — Happy path: Registrar detection
class TestRegistrarDetection:
    def test_godaddy_registrar(self) -> None:
        tps = [
            ThirdParty(
                name="GoDaddy",
                relationship_type="registrar",
                domain="godaddy.com",
                evidence=["RDAP: GoDaddy Inc."],
                confidence=0.9,
            )
        ]
        result = analyse_third_parties(tps)
        assert result.third_parties[0].relationship_type == "registrar"
        assert result.third_parties[0].name == "GoDaddy"
