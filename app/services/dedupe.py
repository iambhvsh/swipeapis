from typing import List, Dict, Any
from collections import defaultdict
from app.utils.urls import normalize_url
from app.services.normalize import normalize_title, normalize_description
from app.models import SearchResult


def enrich_results(results: List[SearchResult]) -> List[SearchResult]:
    for result in results:
        result.title = result.title.strip()
        result.description = normalize_description(result.description)
    return results


def merge_duplicate_urls(results: List[SearchResult]) -> List[SearchResult]:
    merged: Dict[str, SearchResult] = {}

    for idx, result in enumerate(results, start=1):
        if not result.url:
            continue

        normalized_url = normalize_url(result.url)
        result.url = normalized_url

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


def merge_duplicate_titles(results: List[SearchResult]) -> List[SearchResult]:
    grouped = defaultdict(list)

    for result in results:
        norm_title = normalize_title(result.title)
        grouped[norm_title].append(result)

    final_results = []
    for items in grouped.values():
        best = max(items, key=lambda item: (item.frequency, len(item.description)))
        final_results.append(best)

    return final_results


def process_results(raw_results: List[Dict[str, Any]]) -> List[SearchResult]:
    models = [SearchResult(**r) for r in raw_results]

    results = enrich_results(models)
    results = merge_duplicate_urls(results)
    results = merge_duplicate_titles(results)
    return results
