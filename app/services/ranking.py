from typing import List, Dict, Any

from app.services.query_classifier import (
    classify_query,
    calculate_navigation_boost,
)

from app.services.relevance import (
    calculate_relevance,
)

from app.services.quality import (
    calculate_quality_score,
)

from app.services.diversity import (
    diversify_results,
)


PROVIDER_WEIGHTS = {
    "bing": 100,
    "brave": 95,
    "duckduckgo": 90,
    "yahoo": 85,
}

RRF_K = 60


def calculate_rrf(rank: int) -> float:
    """
    Reciprocal Rank Fusion (RRF).

    Higher-ranked results receive a larger score.
    """

    return 1.0 / (RRF_K + max(rank, 1))


def calculate_provider_score(
    provider: str,
) -> float:
    """
    Provider confidence score.
    """

    return PROVIDER_WEIGHTS.get(
        provider.lower(),
        80,
    )


def calculate_frequency_score(
    frequency: int,
) -> float:
    """
    Reward results that appear
    across multiple providers.
    """

    return frequency * 50


def rank_results(
    results: List[Dict[str, Any]],
    query: str,
) -> List[Dict[str, Any]]:
    """
    Atlas ranking pipeline.

    Signals:

    1. Relevance
    2. Quality
    3. Provider confidence
    4. Cross-provider agreement
    5. Reciprocal Rank Fusion
    6. Entity / Navigation boost
    7. Diversity
    """

    query_type = classify_query(query)

    scored_results: List[Dict[str, Any]] = []

    for result in results:
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

        provider = str(
            result.get(
                "provider",
                "duckduckgo",
            )
        )

        frequency = int(
            result.get(
                "frequency",
                1,
            )
        )

        original_rank = int(
            result.get(
                "original_rank",
                1,
            )
        )

        score = 0.0

        # ----------------------------------
        # Relevance
        # ----------------------------------

        score += calculate_relevance(
            query=query,
            title=title,
            description=description,
            url=url,
        )

        # ----------------------------------
        # Quality
        # ----------------------------------

        score += calculate_quality_score(
            result,
        )

        # ----------------------------------
        # Provider Confidence
        # ----------------------------------

        score += calculate_provider_score(
            provider,
        )

        # ----------------------------------
        # Cross Provider Agreement
        # ----------------------------------

        score += calculate_frequency_score(
            frequency,
        )

        # ----------------------------------
        # Reciprocal Rank Fusion
        # ----------------------------------

        score += calculate_rrf(original_rank) * 1000

        # ----------------------------------
        # Entity / Navigation Boost
        # ----------------------------------

        if query_type in {
            "entity",
            "navigational",
        }:
            score += calculate_navigation_boost(
                query=query,
                title=title,
                url=url,
            )

        # ----------------------------------
        # Safety Checks
        # ----------------------------------

        if not title.strip():
            score -= 100

        if not url.strip():
            score -= 100

        if not description.strip():
            score -= 25

        result["score"] = round(
            score,
            3,
        )

        scored_results.append(result)

    # ----------------------------------
    # Initial Sort
    # ----------------------------------

    scored_results.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    # ----------------------------------
    # Diversity
    # ----------------------------------

    final_results = diversify_results(
        scored_results,
    )

    # ----------------------------------
    # Final Sort
    # ----------------------------------

    final_results.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    # ----------------------------------
    # Assign Ranks
    # ----------------------------------

    for idx, result in enumerate(
        final_results,
        start=1,
    ):
        result["rank"] = idx

    return final_results
