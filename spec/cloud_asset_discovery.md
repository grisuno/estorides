# cloud_asset_discovery — Cloud Asset Discovery

## Purpose
Enumerate cloud infrastructure assets (S3 buckets, Azure Blob, GCP Storage,
CloudFront distributions, Firebase databases) associated with a target domain
or organisation using passive techniques: name permutations, HTTP probing,
DNS analysis, and certificate transparency logs.

## Inputs
- `domain: str` — target domain
- `org_name: str` — organisation name for bucket name permutations
- `enable_guessing: bool` — whether to probe common bucket name permutations

## Outputs
```
CloudAssetDiscoveryResult {
  assets: List[CloudAsset]
  total_assets: int
  accessible_count: int
  listing_count: int           # buckets that allow listing
}

CloudAsset {
  provider: str                # aws | azure | gcp | cloudflare | digitalocean | firebase
  resource_type: str           # bucket | cdn | database | storage
  url: str
  accessible: bool             # 200 vs 403 vs 404
  listing_enabled: bool        # if ListBucket returns results
  files: List[str]             # first 100 filenames if listing enabled
  region: Optional[str]
  confidence: float
  source: str                  # how it was discovered
}
```

## Table of errors

| Condition | Code | Behaviour |
|-----------|------|-----------|
| No assets found | `NO_ASSETS` | Empty assets list |
| Rate limited by cloud provider | `RATE_LIMITED` | Wait and retry once, then skip |
| Invalid domain for guessing | `INVALID_INPUT` | Return error |
| All permutations 404 | `NO_MATCHES` | Empty results, confidence=0 |

## Security guarantees
- No write operations (no PUT, no DELETE, no bucket creation)
- Request rate capped at 5 req/s to avoid aggressive scanning
- Only HEAD/GET requests (safe methods)
- No authentication credentials sent to cloud providers
- All probing is indistinguishable from normal crawler traffic

## Out of scope
- Cloud provider account enumeration
- IAM role discovery
- Instance metadata service probing
- Cloud SQL / RDS discovery

## BDD Scenarios

### S1 [Happy path] Public S3 bucket discovered
Given a domain "example.com" with S3 bucket "assets.example.com.s3.amazonaws.com" returning 200
When cloud_asset_discovery is run
Then it returns an AWS bucket asset
and accessible is True
and listing_enabled may be True or False

### S2 [Happy path] Bucket with listing enabled
Given an S3 bucket returning ListBucketResult with 3 files
When cloud_asset_discovery checks the bucket
Then listing_enabled is True
and files contains the 3 filenames

### S3 [Edge] No cloud assets associated
Given a domain with no cloud provider footprint
When cloud_asset_discovery is run
Then assets list is empty
and total_assets = 0

### S4 [Security] Probing does not modify resources
Given any cloud asset probing
When cloud_asset_discovery runs
Then it uses only HEAD and GET methods
and never sends PUT, POST, DELETE or PATCH

### S5 [Happy path] CloudFront detected from DNS
Given a domain with CNAME to "d123.cloudfront.net"
When cloud_asset_discovery is run
Then it returns a CloudFront CDN asset
and confidence >= 0.9

### S6 [Happy path] Firebase database discovered
Given an org name "example" with open Firebase at "example.firebaseio.com"
When cloud_asset_discovery probes Firebase permutations
Then it returns a Firebase database asset
and accessible is True

### S7 [Edge] Bucket name guessing from domain permutations
Given a domain "example.com"
When cloud_asset_discovery generates bucket names
Then it checks permutations including "example", "example-backup", "example-assets",
"example-dev", "example-staging", "example-prod", "example-data"

### S8 [Security] Rate limiting enforced
Given a domain with 100+ bucket permutations to check
When cloud_asset_discovery runs
Then the request rate does not exceed 5 req/s
