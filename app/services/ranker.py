from typing import List

from app.services.intent import classify_query, calculate_navigation_boost
from app.services.relevance import calculate_relevance
from app.services.quality import calculate_quality_score
from app.services.diversity import diversify_results
from app.services.freshness import calculate_freshness_score
from app.models import SearchResult
from app.config import settings


def calculate_rrf(rank: int) -> float:
    return 1.0 / (settings.RRF_K + max(rank, 1))


def calculate_provider_score(provider: str) -> float:
    return settings.PROVIDER_WEIGHTS.get(provider.lower(), 80)


def calculate_frequency_score(frequency: int) -> float:
    return frequency * settings.FREQUENCY_MULTIPLIER


def rank_results(results: List[SearchResult], query: str) -> List[SearchResult]:
    query_type = classify_query(query)

    for result in results:
        score = 0.0

        score += calculate_relevance(
            query=query,
            title=result.title,
            description=result.description,
            url=result.url,
        )

        score += calculate_quality_score(result)
        score += calculate_provider_score(result.provider)
        score += calculate_frequency_score(result.frequency)
        score += calculate_rrf(result.original_rank) * settings.RRF_SCALE_FACTOR

        if query_type in {"entity", "navigational", "ambiguous"}:
            score += calculate_navigation_boost(query=query, title=result.title, url=result.url)

        # Freshness is calculated regardless, but weight changes if intent is freshness
        score += calculate_freshness_score(result, query_type)

        if not result.title:
            score += settings.MISSING_TITLE_PENALTY
        if not result.url:
            score += settings.MISSING_URL_PENALTY
        if not result.description:
            score += settings.MISSING_DESCRIPTION_PENALTY

        result.score = round(score, 3)

    results.sort(key=lambda x: x.score, reverse=True)
    results = diversify_results(results)
    results.sort(key=lambda x: x.score, reverse=True)

    for idx, result in enumerate(results, start=1):
        result.rank = idx

    return results
