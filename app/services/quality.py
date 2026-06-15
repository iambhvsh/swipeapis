from urllib.parse import urlparse
from app.models import SearchResult


def calculate_title_quality(title: str) -> float:
    title = title.strip()
    if not title:
        return -100.0
    length = len(title)
    if length < 3:
        return -50.0
    if 5 <= length <= 120:
        return 20.0
    if length <= 200:
        return 10.0
    return 0.0


def calculate_description_quality(description: str) -> float:
    description = description.strip()
    if not description:
        return -25.0
    length = len(description)
    if length < 20:
        return -10.0
    if 50 <= length <= 500:
        return 20.0
    if length <= 1000:
        return 10.0
    return 0.0


def calculate_url_quality(url: str) -> float:
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return -25.0

        score = 10.0
        if len(url) > 300:
            score -= 10.0

        path_depth = len([segment for segment in parsed.path.split("/") if segment])
        if path_depth > 10:
            score -= 10.0

        return score
    except Exception:
        return -25.0


def calculate_metadata_quality(result: SearchResult) -> float:
    score = 0.0
    if result.title:
        score += 5.0
    if result.description:
        score += 5.0
    if result.url:
        score += 5.0
    if result.source:
        score += 5.0
    return score


def calculate_quality_score(result: SearchResult) -> float:
    score = 0.0
    score += calculate_title_quality(result.title)
    score += calculate_description_quality(result.description)
    score += calculate_url_quality(result.url)
    score += calculate_metadata_quality(result)
    return round(score, 3)
