from typing import List
from urllib.parse import urlparse
import re


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
}


NEWS_KEYWORDS = {
    "news",
    "latest",
    "today",
    "breaking",
    "update",
    "updates",
    "recent",
}


def tokenize(text: str) -> List[str]:
    return re.findall(
        r"\w+",
        text.lower(),
    )


def classify_query(query: str) -> str:
    """
    Returns:

    - entity
    - navigational
    - informational
    - transactional
    - local
    - news
    """

    query = query.strip().lower()

    if not query:
        return "informational"

    terms = tokenize(query)

    # ----------------------------------
    # News
    # ----------------------------------

    if any(keyword in query for keyword in NEWS_KEYWORDS):
        return "news"

    # ----------------------------------
    # Local
    # ----------------------------------

    if any(keyword in query for keyword in LOCAL_KEYWORDS):
        return "local"

    # ----------------------------------
    # Transactional
    # ----------------------------------

    if any(keyword in query for keyword in TRANSACTIONAL_KEYWORDS):
        return "transactional"

    # ----------------------------------
    # Navigational
    # ----------------------------------

    if any(keyword in query for keyword in NAVIGATIONAL_KEYWORDS):
        return "navigational"

    # ----------------------------------
    # Informational
    # ----------------------------------

    if any(keyword in query for keyword in INFORMATIONAL_KEYWORDS):
        return "informational"

    # ----------------------------------
    # Entity Detection
    # ----------------------------------

    # Single-word queries are usually
    # people, products, companies,
    # frameworks, places, etc.

    if len(terms) == 1:
        return "entity"

    # Two-word entity queries:
    #
    # will smith
    # taylor swift
    # next js
    #
    # But avoid classifying
    # informational searches as entities.

    if len(terms) == 2:
        informational_terms = (
            INFORMATIONAL_KEYWORDS | TRANSACTIONAL_KEYWORDS | NEWS_KEYWORDS
        )

        if not any(term in informational_terms for term in terms):
            return "entity"

    # ----------------------------------
    # Default
    # ----------------------------------

    return "informational"


def extract_domain(url: str) -> str:
    try:
        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:
        return ""


def calculate_navigation_boost(
    query: str,
    title: str,
    url: str,
) -> float:
    """
    Boost official-looking pages
    for entity and navigational searches.

    Examples:

    react
    nextjs
    github
    adele
    will smith
    """

    score = 0.0

    query = query.lower().strip()
    title = title.lower().strip()

    domain = extract_domain(url)

    query_terms = tokenize(query)

    # ----------------------------------
    # Exact title match
    # ----------------------------------

    if title == query:
        score += 500

    # ----------------------------------
    # Title starts with query
    # ----------------------------------

    elif title.startswith(query):
        score += 250

    # ----------------------------------
    # Query appears in title
    # ----------------------------------

    elif query in title:
        score += 150

    # ----------------------------------
    # Domain contains query term
    # ----------------------------------

    for term in query_terms:
        if term in domain:
            score += 200

    return score
