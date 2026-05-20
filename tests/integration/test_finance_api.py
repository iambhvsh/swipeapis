import pytest
from unittest.mock import patch
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@patch('app.services.finance.fetch_yahoo_finance_data')
def test_finance_success(mock_yahoo):
    mock_yahoo.return_value = {
        "info": {
            "currentPrice": 150.0,
            "marketCap": 2000000
        },
        "historical": [{"date": "2023-01-01", "Close": 149.0}],
        "recommendations": []
    }

    response = client.get("/finance/AAPL?history_days=1&fields=price,market_cap")

    assert response.status_code == 200
    data = response.json()

    assert data["ticker"] == "AAPL"
    assert data["price"] == 150.0
    assert data["market_cap"] == 2000000
    assert len(data["historical"]) == 1

@patch('app.services.finance.fetch_yahoo_finance_data')
def test_finance_not_found(mock_yahoo):
    from app.providers.finance.yahoo import TickerNotFoundError
    mock_yahoo.side_effect = TickerNotFoundError("Ticker 'INVALID' not found.")

    response = client.get("/finance/INVALID")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
