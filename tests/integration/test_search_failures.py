import pytest
from unittest.mock import patch
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@patch('app.services.search.fetch_bing_results')
@patch('app.services.search.fetch_brave_results')
@patch('app.services.search.fetch_duckduckgo_results')
@patch('app.services.search.fetch_yahoo_results')
def test_search_partial_failure(mock_yahoo, mock_ddg, mock_brave, mock_bing):
    # Bing fails
    mock_bing.side_effect = Exception("Bing timed out")

    # Brave succeeds but returns only 1
    mock_brave.return_value = [{"url": "https://example.com/2", "title": "Title 2", "description": "Desc", "provider": "brave"}]

    # Tier 2 succeeds
    mock_ddg.return_value = [{"url": "https://example.com/3", "title": "Title 3", "description": "Desc", "provider": "duckduckgo"}]
    mock_yahoo.return_value = []

    response = client.get("/search/?q=test&num_results=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 2

    # Result from Brave and DDG should be present
    urls = [r["url"] for r in data["results"]]
    assert "https://example.com/2" in urls
    assert "https://example.com/3" in urls

@patch('app.services.search.fetch_bing_results')
@patch('app.services.search.fetch_brave_results')
@patch('app.services.search.fetch_duckduckgo_results')
@patch('app.services.search.fetch_yahoo_results')
def test_search_total_failure(mock_yahoo, mock_ddg, mock_brave, mock_bing):
    # All providers fail
    mock_bing.side_effect = Exception("Fail")
    mock_brave.side_effect = Exception("Fail")
    mock_ddg.side_effect = Exception("Fail")
    mock_yahoo.side_effect = Exception("Fail")

    response = client.get("/search/?q=test")

    # Service throws SearchError, route maps to 503
    assert response.status_code == 503
    assert "All search providers failed" in response.json()["detail"]

def test_search_empty_query():
    response = client.get("/search/?q=")
    assert response.status_code == 400
    assert "Search query cannot be empty" in response.json()["detail"]
