from typing import List
import re


def tokenize(text: str) -> List[str]:
    """
    Normalize and tokenize text.
    """

    return re.findall(
        r"\w+",
        text.lower(),
    )


def calculate_query_coverage(
    query: str,
    title: str,
) -> float:
    """
    Measures how much of the query
    appears in the title.
    """

    query_terms = set(tokenize(query))

    title_terms = set(tokenize(title))

    if not query_terms:
        return 0.0

    overlap = len(query_terms & title_terms)

    return (overlap / len(query_terms)) * 150


def calculate_title_purity(
    query: str,
    title: str,
) -> float:
    """
    Penalizes noisy titles.

    Example:

    Query:
        react

    Good:
        React

    Worse:
        React Tutorial Guide Course Learn React
    """

    query_terms = tokenize(query)
    title_terms = tokenize(title)

    if not title_terms:
        return 0.0

    overlap = len(set(query_terms) & set(title_terms))

    purity = overlap / len(title_terms)

    return purity * 200


def calculate_exact_match_score(
    query: str,
    title: str,
) -> float:

    query = query.lower().strip()
    title = title.lower().strip()

    if title == query:
        return 500.0

    if title.startswith(query):
        return 150.0

    return 0.0


def calculate_title_score(
    query: str,
    title: str,
) -> float:

    score = 0.0

    query_terms = tokenize(query)

    title_terms = set(tokenize(title))

    for term in query_terms:
        if term in title_terms:
            score += 25

    return score


def calculate_url_score(
    query: str,
    url: str,
) -> float:

    score = 0.0

    query_terms = tokenize(query)

    url = url.lower()

    for term in query_terms:
        if term in url:
            score += 25

    return score


def calculate_description_score(
    query: str,
    description: str,
) -> float:

    score = 0.0

    query_terms = tokenize(query)

    description = description.lower()

    for term in query_terms:
        if term in description:
            score += 10

    return score


def calculate_phrase_match_score(
    query: str,
    title: str,
    description: str,
) -> float:

    score = 0.0

    query = query.lower().strip()

    title = title.lower()
    description = description.lower()

    if query in title:
        score += 100

    if query in description:
        score += 30

    return score


def calculate_relevance(
    query: str,
    title: str,
    description: str,
    url: str,
) -> float:
    """
    Main relevance pipeline.

    Signals:

    - Exact title match
    - Query coverage
    - Phrase matching
    - Title matching
    - URL matching
    - Description matching
    - Title purity
    """

    score = 0.0

    score += calculate_exact_match_score(
        query,
        title,
    )

    score += calculate_query_coverage(
        query,
        title,
    )

    score += calculate_phrase_match_score(
        query,
        title,
        description,
    )

    score += calculate_title_score(
        query,
        title,
    )

    score += calculate_url_score(
        query,
        url,
    )

    score += calculate_description_score(
        query,
        description,
    )

    score += calculate_title_purity(
        query,
        title,
    )

    return round(
        score,
        3,
    )
