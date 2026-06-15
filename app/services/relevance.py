import re
from app.config import settings


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def calculate_query_coverage(query: str, title: str) -> float:
    query_terms = set(tokenize(query))
    title_terms = set(tokenize(title))
    if not query_terms:
        return 0.0
    overlap = len(query_terms & title_terms)
    return (overlap / len(query_terms)) * settings.QUERY_COVERAGE_MULTIPLIER


def calculate_title_purity(query: str, title: str) -> float:
    query_terms = tokenize(query)
    title_terms = tokenize(title)
    if not title_terms:
        return 0.0
    overlap = len(set(query_terms) & set(title_terms))
    purity = overlap / len(title_terms)
    return purity * settings.TITLE_PURITY_MULTIPLIER


def calculate_exact_match_score(query: str, title: str) -> float:
    query = query.lower().strip()
    title = title.lower().strip()
    if title == query:
        return settings.EXACT_MATCH_SCORE
    if title.startswith(query):
        return settings.STARTS_WITH_SCORE
    return 0.0


def calculate_title_score(query: str, title: str) -> float:
    score = 0.0
    query_terms = tokenize(query)
    title_terms = set(tokenize(title))
    for term in query_terms:
        if term in title_terms:
            score += settings.TITLE_TERM_MATCH
    return score


def calculate_url_score(query: str, url: str) -> float:
    score = 0.0
    query_terms = tokenize(query)
    url = url.lower()
    for term in query_terms:
        if term in url:
            score += settings.URL_TERM_MATCH
    return score


def calculate_description_score(query: str, description: str) -> float:
    score = 0.0
    query_terms = tokenize(query)
    description = description.lower()
    for term in query_terms:
        if term in description:
            score += settings.DESCRIPTION_TERM_MATCH
    return score


def calculate_phrase_match_score(query: str, title: str, description: str) -> float:
    score = 0.0
    query = query.lower().strip()
    title = title.lower()
    description = description.lower()
    if query in title:
        score += settings.PHRASE_MATCH_TITLE
    if query in description:
        score += settings.PHRASE_MATCH_DESCRIPTION
    return score


def calculate_relevance(query: str, title: str, description: str, url: str) -> float:
    score = 0.0
    score += calculate_exact_match_score(query, title)
    score += calculate_query_coverage(query, title)
    score += calculate_phrase_match_score(query, title, description)
    score += calculate_title_score(query, title)
    score += calculate_url_score(query, url)
    score += calculate_description_score(query, description)
    score += calculate_title_purity(query, title)
    return round(score, 3)
