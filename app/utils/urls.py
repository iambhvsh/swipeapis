import urllib.parse
import re

def normalize_url(url: str) -> str:
    """
    Canonical URL normalization:
    - Lowercases scheme and netloc.
    - Removes trailing slashes.
    - Removes 'www.' prefix.
    - Removes tracking parameters (utm_, etc.).
    - Normalizes casing inconsistencies in path where possible, though keeping it simple.
    """
    if not url:
        return ""

    try:
        parsed = urllib.parse.urlparse(url)

        # Lowercase scheme and netloc
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()

        # Remove 'www.'
        if netloc.startswith("www."):
            netloc = netloc[4:]

        # Strip trailing slash from path
        path = parsed.path
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]

        # Filter tracking parameters
        query_params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        filtered_params = []
        for k, v in query_params:
            k_lower = k.lower()
            if not (k_lower.startswith("utm_") or k_lower in ("fbclid", "gclid", "ref", "source")):
                filtered_params.append((k, v))

        new_query = urllib.parse.urlencode(filtered_params)

        normalized = urllib.parse.urlunparse((
            scheme,
            netloc,
            path,
            parsed.params,
            new_query,
            "" # Ignore fragments for deduplication
        ))

        return normalized
    except Exception:
        return url
