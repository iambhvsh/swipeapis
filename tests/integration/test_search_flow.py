import pytest
from unittest.mock import patch
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@patch('app.services.search.fetch_bing_results')
@patch('app.services.search.fetch_brave_results')
@patch('app.services.search.fetch_duckduckgo_results')
@patch('app.services.search.fetch_yahoo_results')
def test_search_tier1_success(mock_yahoo, mock_ddg, mock_brave, mock_bing):
    # Tier 1 providers have enough unique results (mock 10 total)
    mock_bing.return_value = [{"url": f"https://example.com/{i}", "title": f"Title {i}", "description": "Desc", "provider": "bing"} for i in range(10)]
    mock_brave.return_value = []

    response = client.get("/search/?q=test&num_results=10")

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 10

    # Assert Tier 2 wasn't called because Tier 1 met the quota
    mock_ddg.assert_not_called()
    mock_yahoo.assert_not_called()

@patch('app.services.search.fetch_bing_results')
@patch('app.services.search.fetch_brave_results')
@patch('app.services.search.fetch_duckduckgo_results')
@patch('app.services.search.fetch_yahoo_results')
def test_search_tier2_fallback(mock_yahoo, mock_ddg, mock_brave, mock_bing):
    # Tier 1 providers have few unique results (mock 2 total)
    mock_bing.return_value = [{"url": f"https://example.com/1", "title": "Title 1", "description": "Desc", "provider": "bing"}]
    mock_brave.return_value = [{"url": f"https://example.com/2", "title": "Title 2", "description": "Desc", "provider": "brave"}]

    # Tier 2 fills the rest
    mock_ddg.return_value = [{"url": f"https://example.com/3", "title": "Title 3", "description": "Desc", "provider": "duckduckgo"}]
    mock_yahoo.return_value = [{"url": f"https://example.com/4", "title": "Title 4", "description": "Desc", "provider": "yahoo"}]

    response = client.get("/search/?q=test&num_results=4")

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 4

    # Assert Tier 2 was called because Tier 1 didn't meet the quota
    assert mock_ddg.called
    assert mock_yahoo.called
