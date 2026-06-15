import re
from app.models import SearchResult
from app.config import settings


def calculate_freshness_score(result: SearchResult, query_intent: str) -> float:
    if query_intent != "freshness":
        return 0.0

    score = 0.0

    date_pattern = (
        r"\b(19|20)\d{2}[-/.](0[1-9]|1[012])[-/.](0[1-9]|[12][0-9]|3[01])\b|"
        r"\b\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b"
    )
    hours_pattern = r"\b\d{1,2} (hour|hours|mins|min|minutes|days|day) ago\b"

    if re.search(hours_pattern, result.description) or re.search(hours_pattern, result.title):
        score += settings.FRESHNESS_MULTIPLIER * 1.5  # Extra boost for very recent items
    elif re.search(date_pattern, result.description) or re.search(date_pattern, result.title):
        score += settings.FRESHNESS_MULTIPLIER

    return score
