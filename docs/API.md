# API

## Search

`GET /search`

Executes an orchestrated metasearch query with tiered fallback and ranking.

### Parameters
- `q` (required): The search string.
- `num_results` (optional): Maximum results (default `10`, capped internally).
- `start` (optional): Offset pagination.
- `language` (optional): e.g., `en`, `es`.
- `safe` (optional): SafeSearch boolean.
- `fields` (optional): Comma-separated output filter (e.g., `url,title,description,source,rank`).
- `include_rank` (optional): Boolean.

### Response
```json
{
  "results": [
    {
      "url": "https://example.com",
      "title": "Example",
      "description": "An example description.",
      "source": "example.com"
    }
  ]
}
```

## Finance

`GET /finance/{ticker}`

Fetches market data and historical pricing for a stock ticker.

### Parameters
- `ticker` (required): Market ticker symbol (e.g., `AAPL`).
- `fields` (optional): Comma-separated fields (e.g., `price,market_cap,volume`).
- `history_days` (optional): Number of historical days to fetch.
- `start_date` / `end_date` (optional): Range bounds (YYYY-MM-DD).
- `interval` (optional): Data spacing (e.g., `1d`, `1wk`).
- `include_recommendations` (optional): Boolean.
- `adjusted` (optional): Boolean.

### Response
```json
{
  "ticker": "AAPL",
  "price": 150.00,
  "market_cap": 2500000000000,
  "historical": [
    {
      "date": "2023-10-01 00:00:00",
      "Open": 149.00,
      "High": 151.00,
      "Low": 148.50,
      "Close": 150.00,
      "Volume": 50000000
    }
  ],
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
- `from_date` / `to_date` (optional): Date bounds (YYYY-MM-DD).
- `num_results` (optional): Max results (default `10`).
- `start` (optional): Offset pagination.
- `include_sentiment` (optional): Boolean.

### Response
```json
{
  "query": "technology",
  "total_articles": 50,
  "articles": [
    {
      "title": "New Tech Released",
      "url": "https://news.com/1",
      "source": "TechNews",
      "published": "Sun, 01 Jan 2023 12:00:00 GMT",
      "description": "Summary.",
      "category": "technology",
      "language": "en",
      "region": "US"
    }
  ],
  "metadata": {
    "generated_at": "2023-01-01T12:00:00Z"
  }
}
```
