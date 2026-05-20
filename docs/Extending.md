# Extending

Atlas is designed for modular extensibility.

## Adding Search Providers

To add a new DDGS backend provider:
1. Create a new adapter: `app/providers/search/new_provider.py`.
2. Implement an asynchronous fetch function that wraps the provider in an `executor`, returning a normalized list of dictionaries (with URL, Title, Description, and Source).
3. Import the fetcher into `app/services/search.py`.
4. Inject it into the tier-based execution block (`tier1_tasks` or `tier2_tasks`).

Ensure the new adapter properly handles exceptions by throwing a provider-specific error (e.g., `NewProviderError`).

## Adding Services

To add a completely new core domain (e.g., Weather):
1. Create `app/routes/weather.py`.
2. Create `app/services/weather.py`.
3. Create `app/providers/weather/source.py`.
4. Register the new router in `app/main.py`.
