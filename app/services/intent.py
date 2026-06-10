import re
from typing import List
from urllib.parse import urlparse
from app.config import settings

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
TRANSACTIONAL_KEYWORDS = {
    "buy",
    "price",
    "pricing",
    "cheap",
    "discount",
    "deal",
    "order",
    "shop",
    "purchase",
}
LOCAL_KEYWORDS = {
    "near me",
    "nearby",
    "closest",
    "restaurant",
    "hotel",
    "cafe",
    "hospital",
    "pharmacy",
    "coffee",
}
FRESHNESS_KEYWORDS = {
    "news",
    "latest",
    "today",
    "breaking",
    "update",
    "updates",
    "recent",
}


def tokenize(text: str) -> List[str]:
    return re.findall(r"\w+", text.lower())


def classify_query(query: str) -> str:
    query = query.strip().lower()
    if not query:
        return "informational"

    terms = tokenize(query)

    if any(keyword in query for keyword in FRESHNESS_KEYWORDS):
        return "freshness"
    if any(keyword in query for keyword in LOCAL_KEYWORDS):
        return "local"
    if any(keyword in query for keyword in TRANSACTIONAL_KEYWORDS):
        return "transactional"
    if any(keyword in query for keyword in NAVIGATIONAL_KEYWORDS):
        return "navigational"
    if any(keyword in query for keyword in INFORMATIONAL_KEYWORDS):
        return "informational"

    # Treat short queries as potentially ambiguous entity queries
    if len(terms) <= 2:
        return "ambiguous"

    return "informational"


def extract_domain(url: str) -> str:
    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
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

    # Domain match is the strongest signal for navigational/entity queries.
    # If the user searches "apple", apple.com should be boosted massively to beat Wikipedia.
    domain_parts = domain.split(".")
    for term in query_terms:
        if term in domain_parts:
            score += settings.NAV_DOMAIN_MATCH

    return score
