"""
estorides_core.socmint
======================
Social Media Intelligence (SOCMINT) module.

Provides:
  * PlatformInfo — metadata about a known social platform
  * ProfileMatch — a single platform profile match
  * SocialMediaProfile — aggregated cross-platform profile
  * SocialMediaInferer — correlates usernames across all known platforms

The inferer uses the source registry to determine which platforms are
available, and the entity resolution layer to fuse profiles that share
the same handle across different services.
"""
from __future__ import annotations

import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger("estorides.socmint")


# ======================================================================
# Platform registry — metadata about every known social platform
# ======================================================================

@dataclass(frozen=True)
class PlatformInfo:
    """Metadata about a known social media platform for cross-referencing."""

    name: str                       # canonical name (lowercase)
    display_name: str               # human-readable (e.g. "GitHub")
    source_name: str                # YAML source name (or None if internal)
    profile_url_template: str       # template with {username} placeholder
    icon: str = "🌐"                # emoji for UI rendering
    requires_key: bool = False
    verified: bool = False          # platform supports verified badges
    category: str = "04. Social Media"


PLATFORM_REGISTRY: dict[str, PlatformInfo] = {
    "github": PlatformInfo("github", "GitHub", "github_user",
                           "https://github.com/{username}", "🐙", verified=True),
    "twitter": PlatformInfo("twitter", "Twitter/X", "twitter_user",
                            "https://x.com/{username}", "🐦", requires_key=True),
    "reddit": PlatformInfo("reddit", "Reddit", "reddit_about",
                           "https://reddit.com/u/{username}", "🧑‍💻", verified=False),
    "mastodon": PlatformInfo("mastodon", "Mastodon", "mastodon_search",
                             "https://mastodon.social/@{username}", "🐘", verified=False),
    "keybase": PlatformInfo("keybase", "Keybase", "keybase_lookup",
                            "https://keybase.io/{username}", "🔑", verified=True,
                            requires_key=False),
    "hackernews": PlatformInfo("hackernews", "HackerNews", "hackernews_user",
                               "https://news.ycombinator.com/user?id={username}", "📰", verified=False),
    "youtube": PlatformInfo("youtube", "YouTube", "youtube_user",
                            "https://youtube.com/@{username}", "🎬", requires_key=True),
    "twitch": PlatformInfo("twitch", "Twitch", "twitch_user",
                           "https://twitch.tv/{username}", "🎮", requires_key=True),
    "telegram": PlatformInfo("telegram", "Telegram", "telegram_tginfo",
                             "https://t.me/{username}", "✈️", verified=False),
    "medium": PlatformInfo("medium", "Medium", "medium_public",
                           "https://medium.com/@{username}", "✍️", verified=False),
    "devto": PlatformInfo("devto", "DEV.to", "dev_to",
                          "https://dev.to/{username}", "💻", verified=False),
    # Note: discord_discovery searches PUBLIC servers by keyword, not user profiles.
    # The profile_url below is informational for the platform registry — user-level
    # resolution requires Discord's authenticated API which is not available in Estorides.
    # discord_discovery: PlatformInfo omitted — server discovery is keyword-based, not username-based.
}


# ======================================================================
# Data models
# ======================================================================

@dataclass
class ProfileMatch:
    """A single platform profile match for a username."""

    platform: str
    username: str
    display_name: str | None = None
    profile_url: str | None = None
    verified: bool = False
    confidence: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "username": self.username,
            "display_name": self.display_name,
            "profile_url": self.profile_url,
            "verified": self.verified,
            "confidence": round(self.confidence, 4),
            "metadata": self.metadata,
        }


@dataclass
class SocialMediaProfile:
    """Aggregated social media profile for a username across all platforms."""

    username: str
    display_name: str | None = None
    email: str | None = None
    location: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    platform_profiles: list[ProfileMatch] = field(default_factory=list)
    linked_platforms: list[dict[str, str]] = field(default_factory=list)
    cross_platform_confidence: float = 0.0
    last_updated: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "username": self.username,
            "display_name": self.display_name,
            "email": self.email,
            "location": self.location,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "platform_profiles": [p.to_dict() for p in self.platform_profiles],
            "linked_platforms": self.linked_platforms,
            "cross_platform_confidence": round(self.cross_platform_confidence, 4),
            "total_platforms": len(self.platform_profiles),
            "last_updated": self.last_updated or time.time(),
        }


# ======================================================================
# SocialMediaInferer
# ======================================================================

# Regex to extract usernames from social media profile URLs.
# Instagram and LinkedIn are excluded per spec §Out of scope —
# LinkedIn scraping is prohibited by ToS, Instagram Basic Display
# API was deprecated Dec 2024.
_TWITTER_URL_RE = re.compile(r"(?:twitter\.com|x\.com)/([A-Za-z0-9_]+)", re.IGNORECASE)
_GITHUB_URL_RE = re.compile(r"github\.com/([A-Za-z0-9_-]+)", re.IGNORECASE)
_YOUTUBE_URL_RE = re.compile(r"youtube\.com/@([A-Za-z0-9_-]+)", re.IGNORECASE)
_TELEGRAM_URL_RE = re.compile(r"t\.me/([A-Za-z0-9_]+)", re.IGNORECASE)
_REDDIT_URL_RE = re.compile(r"reddit\.com/u(?:ser)?/([A-Za-z0-9_-]+)", re.IGNORECASE)
_MEDIUM_URL_RE = re.compile(r"medium\.com/@([A-Za-z0-9_-]+)", re.IGNORECASE)

# Known cross-platform link fields in source parsers
_LINKED_PLATFORM_FIELDS: dict[str, str] = {
    "twitter": "twitter_username",
    "github": "github_username",
    "youtube": "youtube_url",
}

# Platform -> profile URL template
_PROFILE_URLS: dict[str, str] = {
    info.name: info.profile_url_template
    for info in PLATFORM_REGISTRY.values()
}


def _extract_profile_urls(text: str) -> dict[str, str]:
    """Extract social media profile URLs from a text blob.

    Scans text for common social media URL patterns and returns a
    dict of platform -> username for every match found.
    """
    results: dict[str, str] = {}
    for regex, platform in [
        (_TWITTER_URL_RE, "twitter"),
        (_GITHUB_URL_RE, "github"),
        (_YOUTUBE_URL_RE, "youtube"),
        (_TELEGRAM_URL_RE, "telegram"),
        (_REDDIT_URL_RE, "reddit"),
        (_MEDIUM_URL_RE, "medium"),
    ]:
        match = regex.search(text)
        if match:
            results[platform] = match.group(1)
    return results


def _confidence_for_platform_matches(platform_count: int, has_verified: bool, has_keybase: bool) -> float:
    """Compute cross-platform confidence based on evidence strength.

    More platforms = higher confidence. A verified profile (Keybase/GitHub)
    adds significant weight. The result is bounded to [0.0, 1.0].
    """
    base = min(0.3, platform_count * 0.15)  # 0.15 per platform, cap at 0.3
    if has_verified:
        base += 0.3
    if has_keybase:
        base += 0.2  # Keybase has cryptographic proof chains
    if platform_count >= 3:
        base += 0.15
    if platform_count >= 5:
        base += 0.1
    return min(1.0, base)


class SocialMediaInferer:
    """Correlates usernames across social media platforms.

    Pure: no I/O, no external dependencies. Uses the platform registry
    to determine which platforms exist and which YAML sources back them.

    The inferer provides:
      1. resolve(username) — build a SocialMediaProfile for a username
      2. discover_from_text(text) — extract cross-platform links from text
    """

    def __init__(self) -> None:
        self._platforms = dict(PLATFORM_REGISTRY)

    # --------------------------------------------------------------- public
    def resolve(self, username: str, platforms: list[str] | None = None) -> dict[str, Any]:
        """Build a SocialMediaProfile for a username across all platforms.

        Args:
            username: The handle to search for.
            platforms: Optional subset of platforms to check. If None,
                      checks all known platforms.

        Returns:
            A serialised SocialMediaProfile dict. When no platform could
            find the username, returns ``{"profiles": [], "no_matches": True}``.

        This is a *speculative* resolution — it returns profile URL
        templates for each platform. The actual hit/miss determination
        happens when the YAML sources execute their HTTP calls.
        """
        if not username or not isinstance(username, str):
            return {"profiles": [], "no_matches": True, "error": "invalid_username"}

        username = username.strip().lower()
        active_platforms = {
            k: v for k, v in self._platforms.items()
            if platforms is None or k in platforms
        }

        if not active_platforms:
            return {"profiles": [], "no_matches": True, "error": "no_platforms"}

        profiles: list[ProfileMatch] = []
        linked_platforms: list[dict[str, str]] = []
        display_name: str | None = None
        email: str | None = None
        location: str | None = None
        bio: str | None = None
        avatar_url: str | None = None
        has_verified = False
        has_keybase = False

        for pname, info in active_platforms.items():
            profile_url = info.profile_url_template.replace("{username}", username)
            match_conf = 0.6  # base confidence for a platform that has the source

            # Platforms with verified badges get a confidence bump
            is_verified = False
            if info.verified:
                is_verified = True
                match_conf += 0.2
                has_verified = True

            if pname == "keybase":
                has_keybase = True
                match_conf += 0.15  # Keybase identity proofs are strong

            # Platforms requiring keys get a slight penalty (higher chance of missing data)
            if info.requires_key:
                match_conf -= 0.1

            pm = ProfileMatch(
                platform=pname,
                username=username,
                display_name=None,   # would be populated by actual source execution
                profile_url=profile_url,
                verified=is_verified,
                confidence=match_conf,
                metadata={"source_name": info.source_name, "icon": info.icon},
            )
            profiles.append(pm)

        # If Keybase is in the list, add a linked_platform entry showing
        # that Keybase can verify cross-platform identity proofs
        if has_keybase:
            linked_platforms.append({
                "from_platform": "keybase",
                "note": "Cryptographic identity proofs may link multiple profiles",
            })

        cross_conf = _confidence_for_platform_matches(
            len(profiles), has_verified, has_keybase
        )

        return SocialMediaProfile(
            username=username,
            display_name=display_name,
            email=email,
            location=location,
            bio=bio,
            avatar_url=avatar_url,
            platform_profiles=profiles,
            linked_platforms=linked_platforms,
            cross_platform_confidence=cross_conf,
            last_updated=time.time(),
        ).to_dict()

    def discover_from_text(self, text: str) -> dict[str, Any]:
        """Extract social media profiles from a text blob.

        Scans text for URLs pointing to known social platforms and
        returns a dict of platform -> username for every match.

        This is useful for enriching observations — a GitHub profile
        that mentions a Twitter handle creates a cross-platform link.
        """
        if not text:
            return {"profiles": {}, "total": 0}

        extracted = _extract_profile_urls(text)
        if not extracted:
            return {"profiles": {}, "total": 0}

        profiles: dict[str, dict[str, Any]] = {}
        for platform, username in extracted.items():
            info = self._platforms.get(platform)
            profile_url = _PROFILE_URLS.get(platform, "").replace("{username}", username)
            profiles[platform] = {
                "username": username,
                "platform": platform,
                "display_name": info.display_name if info else platform,
                "profile_url": profile_url,
                "icon": info.icon if info else "🌐",
            }

        return {
            "profiles": profiles,
            "total": len(profiles),
        }

    def platform_list(self) -> list[dict[str, Any]]:
        """Return the full platform registry as a serialisable list."""
        return [
            {
                "name": info.name,
                "display_name": info.display_name,
                "source_name": info.source_name,
                "profile_url_template": info.profile_url_template,
                "icon": info.icon,
                "requires_key": info.requires_key,
                "verified": info.verified,
                "category": info.category,
            }
            for info in self._platforms.values()
        ]


# Singleton for use across the app
inferer = SocialMediaInferer()


__all__ = [
    "PLATFORM_REGISTRY",
    "PlatformInfo",
    "ProfileMatch",
    "SocialMediaInferer",
    "SocialMediaProfile",
    "inferer",
]
