# API

## Search

`GET /search`

Executes an orchestrated metasearch query.

### Parameters
- `q` (required): The search string.
- `num_results` (optional): Maximum results (default `10`, max `100`).
- `start` (optional): Offset pagination.
- `language` (optional): e.g., `en`, `es`.
- `safe` (optional): SafeSearch boolean.
- `fields` (optional): Comma-separated output filter (`url,title,description`).

### Response
```json
{
  "results": [
    {
      "url": "https://example.com",
      "title": "Example",
      "description": "An example description."
    }
  ]
}
```

## Finance

`GET /finance/{ticker}`

Fetches market data and historical pricing for a stock ticker.

### Parameters
- `ticker` (required): Market ticker symbol (e.g., `AAPL`).
- `history_days` (optional): Number of historical days to fetch.
- `start_date` / `end_date` (optional): Range bounds.
- `interval` (optional): Data spacing (`1d`, `1wk`).
- `include_recommendations` (optional): Boolean.

### Response
```json
{
  "ticker": "AAPL",
  "price": 150.00,
  "market_cap": 2500000000000,
  "historical": [],
  "recommendations": []
}
```

## News

`GET /news`

Aggregates recent headlines.

### Parameters
- `q` (optional): Search query.
- `category` (optional): e.g., `business`, `technology`.
- `region` (optional): e.g., `US`.
- `language` (optional): e.g., `en`.
- `from_date` / `to_date` (optional): Date bounds.

### Response
```json
{
  "query": "technology",
  "total_articles": 50,
  "articles": [
    {
      "title": "New Tech Released",
      "url": "https://news.com/1",
      "published": "Sun, 01 Jan 2023 12:00:00 GMT",
      "description": "Summary."
    }
  ]
}
```
