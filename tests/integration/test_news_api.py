import pytest
from unittest.mock import patch
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@patch('app.services.news.fetch_headlines')
def test_news_success_with_category(mock_headlines):
    mock_headlines.return_value = {
        "total_articles": 1,
        "articles": [
            {
                "title": "Tech News",
                "url": "https://example.com/tech",
                "source": "Tech Site",
                "published": "2023-01-01T00:00:00Z",
                "description": "Tech description"
            }
        ]
    }

    response = client.get("/news/?category=technology")

    assert response.status_code == 200
    data = response.json()

    assert data["query"] == "technology"
    assert data["total_articles"] == 1
    assert data["articles"][0]["category"] == "technology"
    assert data["articles"][0]["language"] == "en"

def test_news_invalid_date_range():
    response = client.get("/news/?from_date=2023-01-02&to_date=2023-01-01")

    assert response.status_code == 400
    assert "must be less than or equal to" in response.json()["detail"]

@patch('app.services.news.fetch_headlines')
def test_news_provider_failure(mock_headlines):
    from app.providers.news.headlines import HeadlinesProviderError
    mock_headlines.side_effect = HeadlinesProviderError("Upstream failure")

    response = client.get("/news/")

    assert response.status_code == 503
    assert "Upstream failure" in response.json()["detail"]
