from app.services.dedupe import process_results


def test_manual_dedup_flow():
    raw_results = [
        {
            "url": "https://www.example.com/",
            "provider": "bing",
            "title": "A",
            "description": "B",
        },
        {
            "url": "https://example.com?utm_source=123",
            "provider": "brave",
            "title": "A",
            "description": "B",
        },
        {
            "url": "https://example.com/unique",
            "provider": "duckduckgo",
            "title": "C",
            "description": "D",
        },
        {"url": "", "provider": "yahoo", "title": "", "description": ""},  # malformed
    ]

    deduped_results = process_results(raw_results)

    assert len(deduped_results) == 2
    assert deduped_results[0].frequency == 2
    assert deduped_results[0].provider == "bing"
    assert deduped_results[1].frequency == 1
    assert deduped_results[1].provider == "duckduckgo"
