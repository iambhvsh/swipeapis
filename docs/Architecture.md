# Architecture

Atlas employs a strictly linear and modular architecture. The design prioritizes clear boundaries of responsibility. The system is stateless and relies entirely on synchronous and asynchronous orchestration of internal modules.

## Request Lifecycle

The lifecycle of an Atlas request is deterministic:

1. **Routing**: The `app/routes/search.py` module receives the incoming HTTP request. It validates query parameters, limits, and pagination variables.
2. **Orchestration**: The `search_service` within `app/services/search.py` manages the concurrent execution of upstream providers.
3. **Provider Fetching**: Providers in `app/providers/search/` (Bing, Brave, DuckDuckGo, Yahoo) translate the query into upstream requests.
4. **Processing and Deduplication**: The `app/services/dedupe.py` module cleans descriptions, normalizes URLs, and merges duplicated results to calculate provider frequency.
5. **Ranking**: The `app/services/ranker.py` module takes the deduplicated results, evaluates intent, and assigns scores based on relevance, quality, and diversity signals.
6. **Response**: The ranked results are paginated and stripped of unrequested fields before being returned as a JSON response.

## Directory Structure

* `app/config.py`: Centralized configuration variables.
* `app/main.py`: FastAPI application entry point.
* `app/models.py`: Pydantic models for type safety.
* `app/middleware/limits.py`: Rate limiting definitions.
* `app/providers/search/`: Upstream engine adapters.
* `app/routes/search.py`: HTTP endpoint definitions.
* `app/services/`: Core business logic modules.
  * `dedupe.py`: Normalization and deduplication.
  * `diversity.py`: Domain diversity constraints.
  * `freshness.py`: Recency based scoring adjustments.
  * `intent.py`: Query classification.
  * `normalize.py`: Title and description normalization.
  * `quality.py`: Structural metadata evaluation.
  * `ranker.py`: The final scoring pipeline.
  * `relevance.py`: Textual relevance and query coverage.
  * `search.py`: High level provider orchestration.
* `app/utils/urls.py`: URL parsing and normalization utilities.

Each module has a single, explicit responsibility.
