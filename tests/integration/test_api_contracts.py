import pytest
from unittest.mock import patch
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_contract():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "description" in data
    assert "version" in data

@patch('app.services.search.fetch_bing_results')
@patch('app.services.search.fetch_brave_results')
def test_search_contract(mock_brave, mock_bing):
    mock_bing.return_value = [{"url": "https://a.com", "title": "A", "description": "D", "source": "a.com", "provider": "bing"}]
    mock_brave.return_value = []

    response = client.get("/search/?q=atlas")
    assert response.status_code == 200

    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    if len(data["results"]) > 0:
        item = data["results"][0]
        assert "url" in item
        assert "title" in item
        assert "description" in item

@patch('app.services.finance.fetch_yahoo_finance_data')
def test_finance_contract(mock_yahoo):
    mock_yahoo.return_value = {
        "info": {"currentPrice": 1.0, "marketCap": 2},
        "historical": [],
        "recommendations": []
    }

    response = client.get("/finance/AAPL")
    assert response.status_code == 200

    data = response.json()
    assert "ticker" in data
    assert "price" in data
    assert "market_cap" in data
    assert isinstance(data.get("historical", []), list)

@patch('app.services.news.fetch_headlines')
def test_news_contract(mock_headlines):
    mock_headlines.return_value = {
        "total_articles": 0,
        "articles": []
    }

    response = client.get("/news/?category=tech")
    assert response.status_code == 200

    data = response.json()
    assert "query" in data
    assert "total_articles" in data
    assert "articles" in data
    assert "metadata" in data
