# Normalization

Consistent deduplication across varied search providers requires rigorous canonical URL normalization.

## Process

The `normalize_url` function (`app/utils/urls.py`) processes raw URLs before deduplication checks:

- **Lowercasing**: Scheme and network locations are forced to lowercase.
- **Prefix stripping**: The `www.` prefix is stripped to treat `example.com` and `www.example.com` identically.
- **Slash normalization**: Trailing slashes on root paths are stripped.
- **Tracking parameter stripping**: Parameters such as `utm_source`, `utm_medium`, `fbclid`, and `gclid` are omitted to ensure identical content with different referrer tags deduplicate correctly.
