import pytest
from app.utils.urls import normalize_url

def test_manual_dedup_flow():
    raw_results = [
        {"url": "https://www.example.com/", "provider": "bing"},
        {"url": "https://example.com?utm_source=123", "provider": "brave"},
        {"url": "https://example.com/unique", "provider": "duckduckgo"},
        {"url": "", "provider": "yahoo"} # malformed
    ]

    seen_urls = set()
    deduped_results = []

    for idx, result in enumerate(raw_results, start=1):
        raw_url = result.get('url')
        if not raw_url:
            continue

        normalized = normalize_url(raw_url)
        if 'original_rank' not in result:
            result['original_rank'] = idx

        if normalized in seen_urls:
            for existing in deduped_results:
                existing_url = existing.get('url')
                if existing_url and normalize_url(existing_url) == normalized:
                    existing['frequency'] = existing.get('frequency', 1) + 1
                    break
            continue

        seen_urls.add(normalized)
        result['frequency'] = 1
        deduped_results.append(result)

    assert len(deduped_results) == 2
    assert deduped_results[0]['frequency'] == 2
    assert deduped_results[0]['provider'] == "bing"
    assert deduped_results[1]['frequency'] == 1
    assert deduped_results[1]['provider'] == "duckduckgo"
