from typing import Dict, Any
from urllib.parse import urlparse


def calculate_title_quality(
    title: str,
) -> float:
    """
    Generic title quality.

    Measures:
    - Presence
    - Reasonable length

    Does NOT inspect content.
    """

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


def calculate_description_quality(
    description: str,
) -> float:
    """
    Generic description quality.

    Measures:
    - Presence
    - Reasonable length

    Does NOT inspect content.
    """

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


def calculate_url_quality(
    url: str,
) -> float:
    """
    URL structure quality.

    Measures:
    - Validity
    - Reasonable URL length
    - Reasonable path depth

    Does NOT inspect domain names.
    """

    try:
        parsed = urlparse(url)

        if not parsed.scheme:
            return -25.0

        if not parsed.netloc:
            return -25.0

        score = 10.0

        url_length = len(url)

        if url_length > 300:
            score -= 10.0

        path_depth = len([segment for segment in parsed.path.split("/") if segment])

        if path_depth > 10:
            score -= 10.0

        return score

    except Exception:
        return -25.0


def calculate_metadata_quality(
    result: Dict[str, Any],
) -> float:
    """
    Metadata completeness.

    Measures whether the result
    has useful metadata.
    """

    score = 0.0

    if result.get("title"):
        score += 5.0

    if result.get("description"):
        score += 5.0

    if result.get("url"):
        score += 5.0

    if result.get("source"):
        score += 5.0

    return score


def calculate_quality_score(
    result: Dict[str, Any],
) -> float:
    """
    Generic quality score.

    Quality != Relevance.

    This only evaluates whether a result
    appears structurally complete and healthy.

    Content understanding belongs elsewhere.
    """

    title = str(
        result.get(
            "title",
            "",
        )
    )

    description = str(
        result.get(
            "description",
            "",
        )
    )

    url = str(
        result.get(
            "url",
            "",
        )
    )

    score = 0.0

    score += calculate_title_quality(
        title,
    )

    score += calculate_description_quality(
        description,
    )

    score += calculate_url_quality(
        url,
    )

    score += calculate_metadata_quality(
        result,
    )

    return round(
        score,
        3,
    )
