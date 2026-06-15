import re
from typing import Literal
from urllib.parse import urlparse
from app.config import settings

QueryIntent = Literal["freshness", "local", "transactional", "navigational", "informational", "ambiguous", "entity"]

NAVIGATIONAL_KEYWORDS = {
    "login",
    "signin",
    "sign in",
    "official",
    "homepage",
    "website",
    "docs",
    "documentation",
    "github",
    "download",
}
INFORMATIONAL_KEYWORDS = {
    "what",
    "how",
    "why",
    "when",
    "where",
    "guide",
    "tutorial",
    "learn",
    "explain",
    "meaning",
    "definition",
    "examples",
    "example",
    "vs",
    "difference",
    "compare",
}
TRANSACTIONAL_KEYWORDS = {"buy", "price", "pricing", "cheap", "discount", "deal", "order", "shop", "purchase"}
LOCAL_KEYWORDS = {"near me", "nearby", "closest", "restaurant", "hotel", "cafe", "hospital", "pharmacy", "coffee"}
FRESHNESS_KEYWORDS = {"news", "latest", "today", "breaking", "update", "updates", "recent"}


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def has_entity_shape(query: str, terms: list[str]) -> bool:
    compact = "".join(terms)
    has_version_marker = any(char.isdigit() for char in query)
    has_brand_punctuation = any(char in query for char in {".", "+", "#"})
    return len(terms) <= 3 and (has_version_marker or has_brand_punctuation or len(compact) >= 4)


def classify_query(query: str) -> QueryIntent:
    query = query.strip().lower()
    if not query:
        return "informational"

    terms = tokenize(query)
    terms_set = set(terms)

    # First check multi-word keywords explicitly
    if "sign in" in query or "near me" in query:
        if "sign in" in query:
            return "navigational"
        if "near me" in query:
            return "local"

    # Then check token intersections
    if FRESHNESS_KEYWORDS & terms_set:
        return "freshness"
    if LOCAL_KEYWORDS & terms_set:
        return "local"
    if TRANSACTIONAL_KEYWORDS & terms_set:
        return "transactional"
    if NAVIGATIONAL_KEYWORDS & terms_set:
        return "navigational"
    if INFORMATIONAL_KEYWORDS & terms_set:
        return "informational"

    if has_entity_shape(query, terms):
        return "entity"

    if len(terms) <= 2:
        return "ambiguous"

    return "informational"


def extract_domain(url: str) -> str:
    if not url or not isinstance(url, str):
        return ""
    try:
        url = url.strip()
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except (AttributeError, ValueError):
        return ""


def calculate_navigation_boost(query: str, title: str, url: str) -> float:
    score = 0.0
    query = query.lower().strip()
    title = title.lower().strip()
    domain = extract_domain(url)
    query_terms = tokenize(query)

    if title == query:
        score += settings.NAV_EXACT_MATCH
    elif title.startswith(query):
        score += settings.NAV_STARTS_WITH
    elif query in title:
        score += settings.NAV_CONTAINS

    domain_parts = domain.split(".")
    for term in query_terms:
        if len(term) >= 3 and term in domain_parts:
            score += settings.NAV_DOMAIN_MATCH

    return score
