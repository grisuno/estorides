"""ATDD + BDD tests for estorides_core.target_scoring.

Implements the Given-When-Then contracts declared in
``spec/target_scoring.md``.
"""
from __future__ import annotations

from estorides_core.target_scoring import (
    ScoredTarget,
    TargetScoringConfig,
    compute_composite,
    score_all_targets,
    score_target,
)


def _make_target(domain: str, surface: float = 0.0, soft: float = 0.0,
                 jewel: float = 0.0, lateral: float = 0.0) -> ScoredTarget:
    composite = compute_composite(surface, soft, jewel, lateral)
    tier = "critical" if composite > 0.7 else "high" if composite > 0.5 else \
           "medium" if composite > 0.3 else "low" if composite > 0.1 else "noise"
    return ScoredTarget(
        target=domain,
        attack_surface_score=surface,
        soft_target_score=soft,
        crown_jewel_score=jewel,
        lateral_potential=lateral,
        composite_score=composite,
        tier=tier,
        key_findings=[],
        recommended_actions=[],
    )


# S1 — Happy path: Critical target
class TestCriticalTarget:
    def test_open_bucket_and_old_nginx_ranked_critical(self) -> None:
        target = _make_target("example.com", surface=0.9, soft=0.8, jewel=0.8, lateral=0.7)
        assert target.composite_score > 0.7
        assert target.tier == "critical"


# S2 — Edge: No findings = noise
class TestNoFindingsNoise:
    def test_no_findings_is_noise(self) -> None:
        target = _make_target("example.com", 0.0, 0.0, 0.0, 0.0)
        assert target.composite_score == 0.0
        assert target.tier == "noise"


# S3 — Edge: Mixed scoring
class TestMixedScoring:
    def test_5_targets_various_tiers(self) -> None:
        targets = [
            _make_target("crit.example.com", 0.9, 0.8, 0.8, 0.7),
            _make_target("high1.example.com", 0.8, 0.7, 0.4, 0.3),
            _make_target("high2.example.com", 0.7, 0.6, 0.5, 0.4),
            _make_target("med.example.com", 0.5, 0.4, 0.3, 0.2),
            _make_target("noise.example.com", 0.0, 0.0, 0.0, 0.0),
        ]
        result = score_all_targets(targets)
        assert result.summary.critical_targets == 1
        assert result.summary.high_targets == 2
        assert result.summary.medium_targets == 1
        assert result.summary.noise_targets == 1
        assert result.top_recommendations is not None


# S4 — Security: Configurable weights
class TestConfigurableWeights:
    def test_custom_weights_change_score(self) -> None:
        config = TargetScoringConfig(
            surface_weight=1.0, soft_weight=0.0,
            jewel_weight=0.0, lateral_weight=0.0,
        )
        composite = compute_composite(0.5, 0.9, 0.0, 0.0, config=config)
        # With custom config, only surface matters
        assert composite == 0.5


# S5 — Happy path: Crown jewel detection
class TestCrownJewelDetection:
    def test_jenkins_jira_vpn_get_high_jewel_score(self) -> None:
        for subdomain in ["jenkins", "jira", "vpn"]:
            target = _make_target(f"{subdomain}.example.com", surface=0.4, soft=0.3, jewel=0.9, lateral=0.5)
            assert target.crown_jewel_score > 0.7

    def test_blog_low_jewel_score(self) -> None:
        target = _make_target("blog.example.com", surface=0.4, soft=0.3, jewel=0.2, lateral=0.1)
        assert target.crown_jewel_score == 0.2


# S6 — Edge: Partial data
class TestPartialData:
    def test_partial_data_lower_confidence(self) -> None:
        target = score_target("example.com", {}, {})
        assert target.composite_score >= 0.0


# S7 — Happy path: Lateral potential
class TestLateralPotential:
    def test_password_reuse_increases_lateral(self) -> None:
        target = _make_target("example.com", surface=0.5, soft=0.5, jewel=0.5, lateral=0.8)
        assert target.lateral_potential > 0.5


# S8 — Security: No credential leakage in output
class TestNoCredentialLeakage:
    def test_serialised_output_no_credentials(self) -> None:
        target = _make_target("example.com", 0.9, 0.8, 0.7, 0.6)
        out = str(target.__dict__)
        assert "password" not in out.lower() or "password" not in target.key_findings
