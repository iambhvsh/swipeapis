# Architecture

Atlas utilizes a strict, infrastructure-oriented architectural flow:

`Route -> Service -> Provider`

This ensures a clear separation of concerns where HTTP boundaries do not leak into business logic, and business logic does not directly interface with external network calls.

## Components

### Routes (`app/routes/`)
Routes are exclusively responsible for:
- Path and query parameter validation
- Invoking the underlying service layer
- Handling and wrapping service exceptions into HTTP responses

### Services (`app/services/`)
Services manage the core orchestration.
- **Aggregation**: Executing multiple provider tasks (often asynchronously).
- **Normalization**: Standardizing data shapes and validating cross-parameters (e.g., date ranges).
- **Deduplication**: Removing identical results (e.g., canonical URL matching).
- **Ranking**: Scoring and ordering results globally.

### Providers (`app/providers/`)
Providers are low-level backend adapters.
- Fetching raw data from an upstream source (e.g., Yahoo, DuckDuckGo, PyGoogleNews).
- Applying provider-specific pagination logic.
- Returning raw, standardized dictionaries to the service.

## Orchestration Flow

### Search
1. `Route` validates parameters.
2. `Service` fires `asyncio.gather` on primary `Providers` (e.g., Bing, Brave).
3. If primary results are sparse, the `Service` fires fallback `Providers`.
4. `Service` normalizes URLs and strips tracking parameters.
5. `Service` scores and ranks results.
6. `Route` returns the final paginated JSON to the client.

### Finance
1. `Route` validates parameters (e.g., ticker symbol).
2. `Service` calls the Yahoo Finance provider adapter.
3. `Provider` handles safe dict access, gracefully falling back to historical 1-day/2-day averages if exact current prices are missing.
4. `Service` maps and normalizes requested fields.
5. `Route` returns the structured market data.

### News
1. `Route` validates parameter shapes.
2. `Service` strictly enforces logical boundaries (e.g., `from_date <= to_date`).
3. `Provider` (Headlines) aggregates headlines via PyGoogleNews logic.
4. `Service` tags items with proper category contexts (e.g., falling back to `"top"`).
5. `Route` returns the structured JSON and metadata.
