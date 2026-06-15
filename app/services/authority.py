import re
from urllib.parse import urlparse

from app.config import settings

HIGH_AUTHORITY_DOMAINS: dict[str, float] = {
    "react.dev": 180.0,
    "nextjs.org": 180.0,
    "apple.com": 180.0,
    "mercury.com": 150.0,
    "wikipedia.org": 95.0,
    "github.com": 90.0,
    "npmjs.com": 85.0,
    "developer.mozilla.org": 85.0,
    "vercel.com": 80.0,
    "microsoft.com": 75.0,
    "nasa.gov": 100.0,
    "esa.int": 85.0,
    "britannica.com": 75.0,
}

LOW_AUTHORITY_DOMAINS: dict[str, float] = {
    "grokipedia.com": settings.LOW_AUTHORITY_SOURCE_PENALTY,
}

GENERIC_TITLES = {"home", "homepage", "login", "sign in", "documentation", "docs"}


def normalize_query_key(text: str) -> str:
    return "".join(re.findall(r"[a-z0-9]+", text.lower()))


def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    return domain[4:] if domain.startswith("www.") else domain


def extract_domain_stem(domain: str) -> str:
    parts = domain.split(".")
    if len(parts) < 2:
        return domain
    return parts[-2]


def domain_score(domain: str) -> float:
    if domain in LOW_AUTHORITY_DOMAINS:
        return LOW_AUTHORITY_DOMAINS[domain]

    for trusted_domain, score in HIGH_AUTHORITY_DOMAINS.items():
        if domain == trusted_domain or domain.endswith(f".{trusted_domain}"):
            return score

    if domain.endswith(".gov"):
        return settings.HIGH_AUTHORITY_SOURCE_BONUS
    if domain.endswith(".edu"):
        return settings.HIGH_AUTHORITY_SOURCE_BONUS * 0.75

    return 0.0


def has_noisy_title(title: str) -> bool:
    title = title.strip()
    if len(title) > 140:
        return True
    return title.count("|") + title.count(" - ") + title.count("...") >= 4


def calculate_authority_score(query: str, title: str, url: str, query_intent: str) -> float:
    domain = extract_domain(url)
    if not domain:
        return 0.0

    score = domain_score(domain)
    query_key = normalize_query_key(query)
    domain_stem = extract_domain_stem(domain)
    parsed = urlparse(url)
    is_homepage = parsed.path in {"", "/"}

    if query_key and query_key == normalize_query_key(domain_stem):
        score += settings.OFFICIAL_DOMAIN_MATCH
        if is_homepage:
            score += settings.HOMEPAGE_AUTHORITY_BONUS
    elif query_intent in {"entity", "navigational", "ambiguous"}:
        for term in re.findall(r"[a-z0-9]+", query.lower()):
            if len(term) >= 3 and term in domain_stem:
                score += settings.PARTIAL_DOMAIN_MATCH

    normalized_title = title.strip().lower()
    if normalized_title in GENERIC_TITLES and not is_homepage:
        score += settings.TITLE_NOISE_PENALTY
    if has_noisy_title(title):
        score += settings.TITLE_NOISE_PENALTY

    return round(score, 3)
