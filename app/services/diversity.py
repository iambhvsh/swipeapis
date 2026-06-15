from collections import defaultdict
from urllib.parse import urlparse
from app.models import SearchResult
from app.config import settings


def extract_domain(url: str) -> str:
    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except Exception:
        return ""


def apply_domain_diversity(results: list[SearchResult]) -> list[SearchResult]:
    domain_seen = defaultdict(int)
    diversified_results = []

    for result in results:
        domain = extract_domain(result.url)
        penalty = domain_seen[domain] * settings.DEFAULT_DUPLICATE_PENALTY
        result.score = round(result.score - penalty, 3)
        domain_seen[domain] += 1
        diversified_results.append(result)

    return diversified_results


def remove_excessive_domain_results(results: list[SearchResult]) -> list[SearchResult]:
    filtered_results = []
    domain_counts = defaultdict(int)

    for result in results:
        domain = extract_domain(result.url)
        if domain_counts[domain] >= settings.DEFAULT_MAX_RESULTS_PER_DOMAIN:
            continue
        domain_counts[domain] += 1
        filtered_results.append(result)

    return filtered_results


def diversify_results(results: list[SearchResult]) -> list[SearchResult]:
    results = remove_excessive_domain_results(results)
    results = apply_domain_diversity(results)
    results.sort(key=lambda x: x.score, reverse=True)
    return results
