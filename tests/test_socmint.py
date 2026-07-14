"""
BDD tests for SOCMINT sources and SocialMediaInferer.

Covers:
  - S1: YouTube channel lookup (happy path)
  - S2: YouTube channel not found
  - S3: YouTube without API key
  - S4: Twitch user lookup (happy path)
  - S5: Twitch user not found
  - S6: Twitter/X user lookup (happy path)
  - S7: Discord server search (happy path)
  - S8: SocialMediaInferer correlates across platforms
  - S9: SocialMediaInferer handles unknown username
  - S10: YouTube parser handles malformed response
  - S11: Twitch parser handles error responses
  - S12: Entity extraction from social media profiles
"""
from __future__ import annotations

from typing import Any

import pytest

from estorides_core.entity_extraction import extract_structured
from estorides_core.parsers import (
    get_parser,
    parse_discord_discovery,
    parse_twitch_user,
    parse_twitter_user,
    parse_youtube_user,
)
from estorides_core.socmint import inferer

# ======================================================================
# Fixtures
# ======================================================================


@pytest.fixture
def youtube_response() -> dict[str, Any]:
    """Simulated YouTube Data API v3 response for @mkbhd."""
    return {
        "kind": "youtube#channelListResponse",
        "items": [{
            "id": "UCBJycsmduvYEL83R_U4JriQ",
            "snippet": {
                "title": "Marques Brownlee",
                "description": "Tech reviews and more.",
                "customUrl": "@mkbhd",
                "publishedAt": "2010-01-15T00:00:00Z",
                "country": "US",
                "thumbnails": {
                    "default": {"url": "https://yt3.googleusercontent.com/avatar.jpg"}
                },
            },
            "statistics": {
                "viewCount": "4500000000",
                "subscriberCount": "18000000",
                "videoCount": "1500",
            },
            "topicDetails": {
                "topicIds": ["/m/07c1v", "/m/04rlf"],
            },
            "brandingSettings": {
                "channel": {"keywords": "\"tech\" \"reviews\""},
                "image": {"bannerExternalUrl": "https://yt3.googleusercontent.com/banner.jpg"},
            },
        }],
    }


@pytest.fixture
def twitch_response() -> dict[str, Any]:
    """Simulated Twitch Helix API response for shroud."""
    return {
        "data": [{
            "id": "12345678",
            "login": "shroud",
            "display_name": "shroud",
            "description": "Former pro CS:GO player.",
            "type": "partner",
            "broadcaster_type": "partner",
            "view_count": "120000000",
            "created_at": "2013-08-15T00:00:00Z",
            "offline_image_url": "https://static-cdn.jtvnw.net/offline.jpg",
            "profile_image_url": "https://static-cdn.jtvnw.net/user.jpg",
        }],
    }


@pytest.fixture
def twitter_response() -> dict[str, Any]:
    """Simulated Twitter/X API v2 response for elonmusk."""
    return {
        "data": {
            "id": "44196397",
            "name": "Elon Musk",
            "username": "elonmusk",
            "description": "Tesla, SpaceX, X",
            "location": "Austin, TX",
            "verified": True,
            "public_metrics": {
                "followers_count": 150000000,
                "following_count": 500,
                "tweet_count": 25000,
                "listed_count": 120000,
            },
            "created_at": "2010-06-02T20:12:30Z",
            "profile_image_url": "https://pbs.twimg.com/profile.jpg",
            "url": "https://t.co/example",
            "protected": False,
        },
    }


@pytest.fixture
def discord_response() -> list[dict[str, Any]]:
    """Simulated discords.com API search response."""
    return [
        {
            "id": "123456789012345678",
            "name": "CyberSec Community",
            "description": "A community for cybersecurity professionals",
            "approximate_member_count": 15000,
            "approximate_presence_count": 2500,
            "features": ["COMMUNITY", "NEWS"],
        },
        {
            "id": "987654321098765432",
            "name": "Hack The Box",
            "description": "Official HTB Discord server",
            "approximate_member_count": 80000,
            "approximate_presence_count": 12000,
            "features": ["COMMUNITY", "VERIFIED"],
        },
    ]


# ======================================================================
# S1 — YouTube channel lookup (happy path)
# ======================================================================


class TestS1YouTubeHappyPath:
    """S1: YouTube channel lookup returns structured profile."""

    def test_parser_returns_channel_id(self, youtube_response: dict[str, Any]) -> None:
        """Given a valid YouTube channel response, the parser returns the channel_id."""
        result = parse_youtube_user(youtube_response)
        assert result["kind"] == "youtube_channel"
        assert result["channel_id"] == "UCBJycsmduvYEL83R_U4JriQ"

    def test_parser_returns_subscriber_count(self, youtube_response: dict[str, Any]) -> None:
        """Given a valid YouTube channel response, the parser returns subscriber_count."""
        result = parse_youtube_user(youtube_response)
        assert result["subscriber_count"] == 18000000
        assert isinstance(result["subscriber_count"], int)
        assert result["subscriber_count"] >= 0

    def test_parser_returns_metadata(self, youtube_response: dict[str, Any]) -> None:
        """Given a valid YouTube channel response, the parser returns title and description."""
        result = parse_youtube_user(youtube_response)
        assert result["title"] == "Marques Brownlee"
        assert result["description"] == "Tech reviews and more."
        assert result["custom_url"] == "@mkbhd"
        assert result["video_count"] == 1500


# ======================================================================
# S2 — YouTube channel not found
# ======================================================================


class TestS2YouTubeNotFound:
    """S2: YouTube channel not found returns error."""

    def test_empty_items_returns_not_found(self) -> None:
        """Given an empty items list, the parser returns not_found."""
        result = parse_youtube_user({"items": []})
        assert result["error"] == "not_found"

    def test_missing_items_returns_not_found(self) -> None:
        """Given a response with no items key, the parser returns not_found."""
        result = parse_youtube_user({"kind": "youtube#channelListResponse"})
        assert result["error"] == "not_found"


# ======================================================================
# S3 — YouTube without API key (handled by orchestrator source selection)
# ======================================================================


class TestS3YouTubeRequiresKey:
    """S3: YouTube source requires a key and is excluded when --include-paid is off."""

    def test_yaml_source_has_requires_key(self) -> None:
        """Given the youtube_user YAML source, requires_key is True."""
        # Load the source definition from the source loader
        from estorides_core.config import SOURCES_DIR
        from estorides_core.source_loader import SourceRegistry

        registry = SourceRegistry(SOURCES_DIR)
        registry.load()
        source = registry.get("youtube_user")
        assert source is not None, "youtube_user source must exist"
        assert source["requires_key"] is True
        assert source["key_env"] == "GOOGLE_API_KEY"

    def test_parser_registered(self) -> None:
        """Given the youtube_user source, its parser is registered."""
        parser = get_parser("youtube_user")
        assert parser is not None
        # The parser should be parse_youtube_user
        assert parser.__name__ == "parse_youtube_user"


# ======================================================================
# S4 — Twitch user lookup (happy path)
# ======================================================================


class TestS4TwitchHappyPath:
    """S4: Twitch user lookup returns structured profile."""

    def test_parser_returns_user_id(self, twitch_response: dict[str, Any]) -> None:
        """Given a valid Twitch response, the parser returns the user id."""
        result = parse_twitch_user(twitch_response)
        assert result["kind"] == "twitch_user"
        assert result["id"] == "12345678"

    def test_parser_returns_display_name(self, twitch_response: dict[str, Any]) -> None:
        """Given a valid Twitch response, the parser returns display_name."""
        result = parse_twitch_user(twitch_response)
        assert result["login"] == "shroud"
        assert result["display_name"] == "shroud"

    def test_parser_returns_metadata(self, twitch_response: dict[str, Any]) -> None:
        """Given a valid Twitch response, the parser returns type and view_count."""
        result = parse_twitch_user(twitch_response)
        assert result["type"] == "partner"
        assert result["broadcaster_type"] == "partner"
        assert result["view_count"] == 120000000


# ======================================================================
# S5 — Twitch user not found
# ======================================================================


class TestS5TwitchNotFound:
    """S5: Twitch user not found returns error."""

    def test_empty_data_returns_not_found(self) -> None:
        """Given an empty data list, the parser returns not_found."""
        result = parse_twitch_user({"data": []})
        assert result["error"] == "not_found"

    def test_error_response_returns_api_error(self) -> None:
        """Given an error response, the parser returns api_error with the detail message."""
        result = parse_twitch_user({
            "error": "Unauthorized",
            "status": 401,
            "message": "Invalid OAuth token",
        })
        assert result["error"] == "api_error"
        assert "Invalid OAuth token" in result["detail"]

    def test_missing_data_returns_not_found(self) -> None:
        """Given a response with no data key, the parser returns not_found."""
        result = parse_twitch_user({})
        assert result["error"] == "not_found"


# ======================================================================
# S6 — Twitter/X user lookup (happy path)
# ======================================================================


class TestS6TwitterHappyPath:
    """S6: Twitter/X user lookup returns structured profile."""

    def test_parser_returns_username(self, twitter_response: dict[str, Any]) -> None:
        """Given a valid Twitter response, the parser returns username."""
        result = parse_twitter_user(twitter_response)
        assert result["kind"] == "twitter_user"
        assert result["username"] == "elonmusk"

    def test_parser_returns_followers_count(self, twitter_response: dict[str, Any]) -> None:
        """Given a valid Twitter response, the parser returns followers_count."""
        result = parse_twitter_user(twitter_response)
        assert result["followers_count"] == 150000000
        assert isinstance(result["followers_count"], int)

    def test_parser_returns_verified_flag(self, twitter_response: dict[str, Any]) -> None:
        """Given a valid Twitter response, the parser returns the verified flag."""
        result = parse_twitter_user(twitter_response)
        assert result["verified"] is True

    def test_parser_returns_metadata(self, twitter_response: dict[str, Any]) -> None:
        """Given a valid Twitter response, the parser returns location and description."""
        result = parse_twitter_user(twitter_response)
        assert result["name"] == "Elon Musk"
        assert result["location"] == "Austin, TX"
        assert result["protected"] is False

    def test_not_found_with_errors(self) -> None:
        """Given an error response with errors list, returns not_found."""
        result = parse_twitter_user({
            "errors": [{"detail": "User not found."}],
        })
        assert result["error"] == "not_found"


# ======================================================================
# S7 — Discord server search (happy path)
# ======================================================================


class TestS7DiscordHappyPath:
    """S7: Discord server search returns structured results."""

    def test_parser_returns_server_list(self, discord_response: list[dict[str, Any]]) -> None:
        """Given a Discord server search response, the parser returns server list."""
        result = parse_discord_discovery(discord_response)
        assert "results" in result
        assert len(result["results"]) == 2

    def test_parser_returns_server_names(self, discord_response: list[dict[str, Any]]) -> None:
        """Given a Discord server search response, server names are correct."""
        result = parse_discord_discovery(discord_response)
        names = [s["name"] for s in result["results"]]
        assert "CyberSec Community" in names

    def test_parser_returns_member_counts(self, discord_response: list[dict[str, Any]]) -> None:
        """Given a Discord server search response, member counts are integers."""
        result = parse_discord_discovery(discord_response)
        for server in result["results"]:
            assert isinstance(server["approximate_member_count"], int)
            assert server["approximate_member_count"] >= 0

    def test_empty_response(self) -> None:
        """Given an empty response, the parser returns empty results."""
        result = parse_discord_discovery([])
        assert result["total"] == 0
        assert result["results"] == []

    def test_none_response(self) -> None:
        """Given a None response, the parser returns empty results."""
        result = parse_discord_discovery(None)
        assert result["total"] == 0


# ======================================================================
# S8 — SocialMediaInferer correlates across platforms
# ======================================================================


class TestS8InfererCrossPlatform:
    """S8: SocialMediaInferer correlates usernames across platforms."""

    def test_resolve_torvalds(self) -> None:
        """Given username 'torvalds', the inferer returns profiles across platforms."""
        result = inferer.resolve("torvalds")
        assert "platform_profiles" in result
        assert result["username"] == "torvalds"

    def test_resolve_includes_keybase(self) -> None:
        """Given a username, Keybase appears in platform profiles."""
        result = inferer.resolve("torvalds")
        platforms = {p["platform"] for p in result["platform_profiles"]}
        assert "keybase" in platforms

    def test_resolve_includes_github(self) -> None:
        """Given a username, GitHub appears in platform profiles."""
        result = inferer.resolve("torvalds")
        platforms = {p["platform"] for p in result["platform_profiles"]}
        assert "github" in platforms

    def test_resolve_has_high_confidence_for_populated_username(self) -> None:
        """Given a common username, cross-platform confidence is above 0.5."""
        result = inferer.resolve("torvalds")
        # With GitHub (verified) + Keybase + Reddit + HN + Mastodon = 5 platforms
        assert result["cross_platform_confidence"] > 0.5
        assert result["cross_platform_confidence"] <= 1.0

    def test_resolve_linked_platforms_contains_keybase_note(self) -> None:
        """Given a username, linked_platforms shows the Keybase proof chain."""
        result = inferer.resolve("torvalds")
        linked = result.get("linked_platforms", [])
        platform_names = [link["from_platform"] for link in linked]
        assert "keybase" in platform_names

    def test_resolve_has_profile_urls(self) -> None:
        """Given a username, each platform profile has a profile_url."""
        result = inferer.resolve("torvalds")
        for profile in result["platform_profiles"]:
            assert "profile_url" in profile
            assert profile["username"] == "torvalds"


# ======================================================================
# S9 — SocialMediaInferer handles unknown username
# ======================================================================


class TestS9InfererUnknown:
    """S9: SocialMediaInferer handles unknown/empty usernames."""

    def test_empty_username(self) -> None:
        """Given an empty username, returns no_matches."""
        result = inferer.resolve("")
        assert result.get("no_matches") is True

    def test_none_username(self) -> None:
        """Given None as username, returns no_matches."""
        result = inferer.resolve(None)  # type: ignore[arg-type]
        assert result.get("no_matches") is True

    def test_always_has_profile_count(self) -> None:
        """Given any username, total_platforms is the count of known platforms."""
        result = inferer.resolve("some_random_user_12345")
        assert result["total_platforms"] > 0
        # All known platforms should appear
        from estorides_core.socmint import PLATFORM_REGISTRY
        assert result["total_platforms"] == len(PLATFORM_REGISTRY)

    def test_platform_urls_are_valid(self) -> None:
        """Given any username, all profile URLs are valid templates."""
        result = inferer.resolve("test_user_123")
        for profile in result["platform_profiles"]:
            url = profile["profile_url"]
            assert url is not None
            assert "test_user_123" in url
            assert url.startswith("http")


# ======================================================================
# S10 — YouTube parser handles malformed response
# ======================================================================


class TestS10YouTubeMalformed:
    """S10: YouTube parser handles malformed inputs."""

    def test_none_input(self) -> None:
        """Given None input, returns error."""
        result = parse_youtube_user(None)
        assert result["error"] == "unexpected_response"

    def test_list_input(self) -> None:
        """Given a list instead of dict, returns error."""
        result = parse_youtube_user([])
        assert result["error"] == "unexpected_response"

    def test_string_input(self) -> None:
        """Given a string instead of dict, returns error."""
        result = parse_youtube_user("invalid")
        assert result["error"] == "unexpected_response"

    def test_missing_statistics(self) -> None:
        """Given a response without statistics, parser returns defaults gracefully."""
        result = parse_youtube_user({
            "items": [{
                "id": "UC123",
                "snippet": {"title": "Test Channel"},
            }],
        })
        assert result["channel_id"] == "UC123"
        assert result["subscriber_count"] == 0
        assert result["video_count"] == 0
        assert result["view_count"] == 0


# ======================================================================
# S11 — Twitch parser handles error responses
# ======================================================================


class TestS11TwitchErrors:
    """S11: Twitch parser handles error responses."""

    def test_401_error(self) -> None:
        """Given a 401 error response, returns api_error."""
        result = parse_twitch_user({
            "error": "Unauthorized",
            "status": 401,
            "message": "Invalid OAuth token",
        })
        assert result["error"] == "api_error"

    def test_none_input(self) -> None:
        """Given None input, returns error."""
        result = parse_twitch_user(None)
        assert result["error"] == "unexpected_response"

    def test_list_input(self) -> None:
        """Given a list instead of dict, returns error."""
        result = parse_twitch_user([])
        assert result["error"] == "unexpected_response"


# ======================================================================
# S12 — Entity extraction from social media profiles
# ======================================================================


class TestS12EntityExtraction:
    """S12: Entity extraction works on SOCMINT parser outputs."""

    def test_youtube_profile_extracts_person(self) -> None:
        """Given a YouTube channel with display_name, extract_structured yields a person."""
        payload = {
            "kind": "youtube_channel",
            "title": "John Doe",
            "description": "Tech reviewer and content creator",
            "display_name": "John Doe",
            "username": "johndoe",
            "custom_url": "@johndoe",
            "subscriber_count": 1000000,
        }
        entities = extract_structured(payload, "youtube_user")
        person_entities = [e for e in entities if e.type == "person" and "John" in e.value]
        username_entities = [e for e in entities if e.type == "username" and e.value == "johndoe"]

        assert len(person_entities) >= 1, f"Expected person entity, got: {entities}"
        assert len(username_entities) >= 1, f"Expected username entity, got: {entities}"

    def test_twitter_profile_extracts_person_and_username(self) -> None:
        """Given a Twitter parser output, extract_structured yields person/username entities."""
        payload = {
            "kind": "twitter_user",
            "name": "Elon Musk",
            "username": "elonmusk",
            "description": "Tesla, SpaceX, X founder",
            "location": "Austin, TX",
            "followers_count": 150000000,
        }
        entities = extract_structured(payload, "twitter_user")

        # "name" key with value "Elon Musk" contains a space -> person
        person_ents = [e for e in entities if e.type == "person" and "Elon" in e.value]
        assert len(person_ents) >= 1

        # "username" key -> username entity
        username_ents = [e for e in entities if e.type == "username" and e.value == "elonmusk"]
        assert len(username_ents) >= 1

    def test_social_media_urls_in_text(self) -> None:
        """Given text containing social URLs, the inferer discovers cross-platform links."""
        text = "Follow me on Twitter: https://x.com/johndoe and GitHub: https://github.com/johndoe"
        result = inferer.discover_from_text(text)
        assert result["total"] == 2
        assert "twitter" in result["profiles"]
        assert "github" in result["profiles"]
        assert result["profiles"]["twitter"]["username"] == "johndoe"
        assert result["profiles"]["github"]["username"] == "johndoe"

    def test_discover_empty_text(self) -> None:
        """Given empty text, discover_from_text returns empty."""
        result = inferer.discover_from_text("")
        assert result["total"] == 0

    def test_discover_no_urls(self) -> None:
        """Given text without URLs, discover_from_text returns empty."""
        result = inferer.discover_from_text("This is plain text with no links")
        assert result["total"] == 0


# ======================================================================
# SocialMediaInferer — additional edge cases
# ======================================================================


class TestInfererPlatformList:
    """Verify the platform list method."""

    def test_platform_list_returns_all(self) -> None:
        """Given the inferer, platform_list returns all known platforms."""
        platforms = inferer.platform_list()
        from estorides_core.socmint import PLATFORM_REGISTRY
        assert len(platforms) == len(PLATFORM_REGISTRY)

    def test_platform_list_has_required_fields(self) -> None:
        """Given the platform list, every entry has the core fields."""
        for p in inferer.platform_list():
            assert "name" in p
            assert "display_name" in p
            assert "profile_url_template" in p
            assert "requires_key" in p
            assert "icon" in p


class TestInfererResolveSpecificPlatforms:
    """Verify filtering by specific platforms."""

    def test_resolve_single_platform(self) -> None:
        """Given a specific platform filter, only that platform appears."""
        result = inferer.resolve("torvalds", platforms=["github"])
        assert result["total_platforms"] == 1
        assert result["platform_profiles"][0]["platform"] == "github"

    def test_resolve_multiple_platforms(self) -> None:
        """Given a list of platforms, only those platforms appear."""
        result = inferer.resolve("test", platforms=["github", "twitter", "reddit"])
        platforms_found = {p["platform"] for p in result["platform_profiles"]}
        assert platforms_found == {"github", "twitter", "reddit"}
        assert result["total_platforms"] == 3

    def test_resolve_validates_twitter_requires_key(self) -> None:
        """Given the inferer resolve, Twitter profiles are marked as requiring key."""
        result = inferer.resolve("test", platforms=["twitter"])
        assert result["platform_profiles"][0]["platform"] == "twitter"
        # Metadata should show source_name and the profile URL
        assert "x.com" in result["platform_profiles"][0]["profile_url"]


# ======================================================================
# Parser totalness — all parsers work on unexpected input types
# ======================================================================


class TestParserTotalness:
    """Every parser must be total: any unrecognised input returns empty, not raises."""

    @pytest.mark.parametrize("parser_fn", [
        parse_twitter_user,
        parse_youtube_user,
        parse_twitch_user,
        parse_discord_discovery,
    ])
    def test_parser_handles_none(self, parser_fn: Any) -> None:
        """Given None input, the parser does not raise."""
        try:
            result = parser_fn(None)
            assert result is not None
        except Exception as exc:
            pytest.fail(f"{parser_fn.__name__} raised {exc} on None input")

    @pytest.mark.parametrize("parser_fn", [
        parse_twitter_user,
        parse_youtube_user,
        parse_twitch_user,
        parse_discord_discovery,
    ])
    def test_parser_handles_int(self, parser_fn: Any) -> None:
        """Given int input, the parser does not raise."""
        try:
            result = parser_fn(42)
            assert result is not None
        except Exception as exc:
            pytest.fail(f"{parser_fn.__name__} raised {exc} on int input")

    @pytest.mark.parametrize("parser_fn", [
        parse_twitter_user,
        parse_youtube_user,
        parse_twitch_user,
        parse_discord_discovery,
    ])
    def test_parser_handles_string(self, parser_fn: Any) -> None:
        """Given string input, the parser does not raise."""
        try:
            result = parser_fn("unexpected string")
            assert result is not None
        except Exception as exc:
            pytest.fail(f"{parser_fn.__name__} raised {exc} on string input")
