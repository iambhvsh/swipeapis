from collections import defaultdict
from urllib.parse import urlparse

from app.models import RawSearchResult, SearchResult
from app.utils.urls import normalize_url
from app.services.normalize import normalize_title, normalize_description

GENERIC_DUPLICATE_TITLES = {"", "home", "homepage", "login", "sign in", "documentation", "docs"}


def enrich_results(results: list[SearchResult]) -> list[SearchResult]:
    for result in results:
        result.title = result.title.strip()
        result.description = normalize_description(result.description)
    return results


def merge_duplicate_urls(results: list[SearchResult]) -> list[SearchResult]:
    merged: dict[str, SearchResult] = {}

    for idx, result in enumerate(results, start=1):
        if not result.url:
            continue

        normalized_url = normalize_url(result.url)
        result.url = normalized_url
        result.source = urlparse(normalized_url).netloc

        if normalized_url not in merged:
            result.frequency = 1
            result.providers = [result.provider]
            result.original_rank = idx
            merged[normalized_url] = result
        else:
            existing = merged[normalized_url]
            existing.frequency += 1
            if result.provider not in existing.providers:
                existing.providers.append(result.provider)

    for res in merged.values():
        res.providers.sort()

    return list(merged.values())


def merge_duplicate_titles(results: list[SearchResult]) -> list[SearchResult]:
    grouped: defaultdict[str, list[SearchResult]] = defaultdict(list)
    final_results: list[SearchResult] = []

    for result in results:
        norm_title = normalize_title(result.title)
        if norm_title in GENERIC_DUPLICATE_TITLES:
            final_results.append(result)
            continue
        grouped[norm_title].append(result)

    for items in grouped.values():
        if len(items) == 1:
            final_results.append(items[0])
            continue
        best = max(items, key=lambda item: (item.frequency, len(item.description)))
        final_results.append(best)

    return final_results


def process_results(raw_results: list[RawSearchResult]) -> list[SearchResult]:
    models = [SearchResult(**r) for r in raw_results]

    results = enrich_results(models)
    results = merge_duplicate_urls(results)
    results = merge_duplicate_titles(results)
    return results
