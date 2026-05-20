# Atlas

A modern self-hosted API infrastructure toolkit.

Atlas is an elegant, minimal, and modular API framework focused on search, finance, and news aggregation. Designed with safe defaults, configurable limits, and a clean developer experience, it provides robust infrastructure without the complexity of enterprise bloat or SaaS lock-in.

## Architecture

Atlas relies on a clear separation of concerns, utilizing an extensible architecture:

- **Routes**: Request validation and response orchestration.
- **Services**: Aggregation, normalization, deduplication, and ranking.
- **Providers**: Modular backend integrations handling specific data fetching (e.g., DuckDuckGo for Search, Yahoo for Finance).

### Modules

- **Search**: Multi-engine search infrastructure with clean normalization and deduplication.
- **Finance**: Financial market data fetching and formatting.
- **News**: Headline aggregation across multiple regions and categories.

## Guiding Principles

- **Minimal and Intentional**: No unnecessary enterprise abstractions.
- **Self-Host First**: Designed to run securely on your own infrastructure.
- **Calm Developer Experience**: Predictable endpoints, clear responses, and minimal friction.
- **Safe Defaults**: Built-in rate limiting and safe parsing.

## API Documentation

Once deployed, the API exposes the following core endpoints:

### Search
`GET /search`

Query multiple search engines with safe defaults and robust deduplication.

**Parameters:**
- `q`: Search query string
- `num_results`: Number of results to return
- `language`: Language code (e.g., 'en', 'es')

### Finance
`GET /finance/{ticker}`

Retrieve stock quotes, historical data, and corporate fundamentals.

**Parameters:**
- `ticker`: Stock ticker symbol (e.g., `AAPL`)
- `interval`: Data interval (`1d`, `1wk`, `1mo`)
- `history_days`: Days of historical data

### News
`GET /news`

Aggregate top headlines across various categories and regions.

**Parameters:**
- `q`: Topic query
- `category`: Category filter (`technology`, `business`)
- `region`: Region code (`US`, `GB`)

## Deployment

Atlas is built to be easily deployed via standard tools like Docker. A provided `docker-compose.yml` ensures a quick start.

```bash
docker-compose up -d
```

For manual execution:
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## License

MIT
