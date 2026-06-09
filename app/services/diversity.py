from typing import List, Dict, Any
from collections import defaultdict
from urllib.parse import urlparse


DEFAULT_DUPLICATE_PENALTY = 12.0
DEFAULT_MAX_RESULTS_PER_DOMAIN = 5


def extract_domain(url: str) -> str:
    """
    Extract and normalize domain.

    Examples:

    https://www.github.com/foo
    -> github.com

    https://react.dev
    -> react.dev
    """

    try:
        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:
        return ""


def apply_domain_diversity(
    results: List[Dict[str, Any]],
    penalty_per_duplicate: float = DEFAULT_DUPLICATE_PENALTY,
) -> List[Dict[str, Any]]:
    """
    Soft diversity penalty.

    Example:

    Result #1 github.com
        no penalty

    Result #2 github.com
        -12

    Result #3 github.com
        -24

    Result #4 github.com
        -36
    """

    domain_seen = defaultdict(int)

    diversified_results: List[Dict[str, Any]] = []

    for result in results:
        domain = extract_domain(
            str(
                result.get(
                    "url",
                    "",
                )
            )
        )

        score = float(
            result.get(
                "score",
                0.0,
            )
        )

        penalty = domain_seen[domain] * penalty_per_duplicate

        result["score"] = round(
            score - penalty,
            3,
        )

        domain_seen[domain] += 1

        diversified_results.append(result)

    return diversified_results


def remove_excessive_domain_results(
    results: List[Dict[str, Any]],
    max_results_per_domain: int = DEFAULT_MAX_RESULTS_PER_DOMAIN,
) -> List[Dict[str, Any]]:
    """
    Prevent a single domain from
    completely dominating results.

    Example:

    github.com
    github.com
    github.com
    github.com
    github.com
    github.com

    -> keep first 5
    """

    filtered_results: List[Dict[str, Any]] = []

    domain_counts = defaultdict(int)

    for result in results:
        domain = extract_domain(
            str(
                result.get(
                    "url",
                    "",
                )
            )
        )

        if domain_counts[domain] >= max_results_per_domain:
            continue

        domain_counts[domain] += 1

        filtered_results.append(result)

    return filtered_results


def diversify_results(
    results: List[Dict[str, Any]],
    penalty_per_duplicate: float = DEFAULT_DUPLICATE_PENALTY,
    max_results_per_domain: int = DEFAULT_MAX_RESULTS_PER_DOMAIN,
) -> List[Dict[str, Any]]:
    """
    Atlas diversity pipeline.

    Steps:

    1. Limit domain dominance
    2. Apply soft diversity penalties
    3. Re-sort results
    """

    results = remove_excessive_domain_results(
        results,
        max_results_per_domain=max_results_per_domain,
    )

    results = apply_domain_diversity(
        results,
        penalty_per_duplicate=penalty_per_duplicate,
    )

    results.sort(
        key=lambda x: float(
            x.get(
                "score",
                0.0,
            )
        ),
        reverse=True,
    )

    return results
