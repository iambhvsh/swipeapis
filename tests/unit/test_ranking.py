import pytest
from app.services.ranking import rank_results

def test_provider_weighting():
    results = [
        {"url": "1", "provider": "yahoo", "original_rank": 1, "frequency": 1},
        {"url": "2", "provider": "bing", "original_rank": 1, "frequency": 1},
        {"url": "3", "provider": "duckduckgo", "original_rank": 1, "frequency": 1},
    ]
    ranked = rank_results(results)

    assert ranked[0]["provider"] == "bing"
    assert ranked[1]["provider"] == "duckduckgo"
    assert ranked[2]["provider"] == "yahoo"

def test_duplicate_frequency_scoring():
    results = [
        {"url": "1", "provider": "bing", "original_rank": 1, "frequency": 1}, # base 100 - 2 + 0 = 98
        {"url": "2", "provider": "brave", "original_rank": 1, "frequency": 3}, # base 90 - 2 + 30 = 118
    ]
    ranked = rank_results(results)

    assert ranked[0]["provider"] == "brave"
    assert ranked[1]["provider"] == "bing"

def test_original_rank_penalty():
    results = [
        {"url": "1", "provider": "bing", "original_rank": 5, "frequency": 1}, # 100 - 10 = 90
        {"url": "2", "provider": "bing", "original_rank": 1, "frequency": 1}, # 100 - 2 = 98
    ]
    ranked = rank_results(results)

    assert ranked[0]["url"] == "2"
    assert ranked[1]["url"] == "1"

def test_stable_assignment():
    results = [
        {"url": "1", "provider": "bing", "original_rank": 1, "frequency": 1},
    ]
    ranked = rank_results(results)

    assert ranked[0]["rank"] == 1
    assert "score" in ranked[0]
