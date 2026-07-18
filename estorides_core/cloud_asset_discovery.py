from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
from typing import Any

log = logging.getLogger("estorides.cloud_asset_discovery")

MAX_REQS_PER_SEC = 5

COMMON_BUCKET_PREFIXES = [
    "", "-backup", "-assets", "-dev", "-staging",
    "-prod", "-data", "-logs", "-media", "-static",
    "-cdn", "-files", "-uploads", "-archive", "-backups",
    "-config", "-temp", "-test", "-demo", "-old",
    "-bucket", "-storage", "-content", "-resources",
    "cdn-", "assets-", "static-", "media-", "files-",
    "uploads-", "backup-", "data-", "dev-", "stage-",
    "prod-",
]

CLOUD_ENDPOINTS: list[tuple[str, str, str]] = [
    ("aws", "s3", "https://{bucket}.s3.amazonaws.com"),
    ("aws", "s3", "https://s3.amazonaws.com/{bucket}"),
    ("azure", "blob", "https://{bucket}.blob.core.windows.net"),
    ("gcp", "storage", "https://storage.googleapis.com/{bucket}"),
    ("digitalocean", "spaces", "https://{bucket}.nyc3.digitaloceanspaces.com"),
    ("firebase", "database", "https://{bucket}.firebaseio.com"),
    ("cloudflare", "r2", "https://{bucket}.r2.cloudflarestorage.com"),
]


@dataclass
class CloudAsset:
    provider: str
    resource_type: str
    url: str
    accessible: bool
    listing_enabled: bool
    files: list[str]
    region: str | None
    confidence: float
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CloudAssetDiscoveryResult:
    assets: list[CloudAsset] = field(default_factory=list)
    total_assets: int = 0
    accessible_count: int = 0
    listing_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "assets": [a.to_dict() for a in self.assets],
            "total_assets": self.total_assets,
            "accessible_count": self.accessible_count,
            "listing_count": self.listing_count,
        }


def generate_bucket_names(domain: str) -> list[str]:
    org = domain.rsplit(".", 1)[0] if "." in domain else domain
    org = org.lower().strip()

    names: list[str] = []
    for prefix in COMMON_BUCKET_PREFIXES:
        name = f"{org}{prefix}"
        if name not in names:
            names.append(name)

    for org_part in org.split("."):
        for prefix in COMMON_BUCKET_PREFIXES[:3]:
            name = f"{org_part}{prefix}"
            if name not in names:
                names.append(name)

    return names


def assess_bucket(url: str, method: str = "GET") -> dict[str, Any]:
    safe_methods = {"GET", "HEAD"}
    return {
        "url": url,
        "method": method,
        "is_safe": method.upper() in safe_methods,
    }


class CloudAssetDiscoveryError(Exception):
    pass
