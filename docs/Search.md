# Search

Atlas Search acts as a lightweight modern metasearch infrastructure engine. It prioritizes the best relevance-per-latency tradeoff rather than fetching from every possible engine indiscriminately.

## Tiered Execution Flow

Rather than querying all providers at once, Atlas implements a tiered execution strategy to ensure latency remains low while fallback options exist.

1. **Primary Execution (Tier 1)**
   - Executes Bing and Brave adapters concurrently.
   - Timeout capped strictly at 3 seconds.
   - Evaluates the volume and diversity of the resulting URLs.

2. **Fallback Execution (Tier 2)**
   - If Tier 1 returns fewer than the requested number of unique results, or if primary providers fail, Tier 2 executes.
   - Executes DuckDuckGo and Yahoo adapters concurrently.
   - Timeout capped at 5 seconds.

## Concurrency Model

All provider requests use `asyncio.wait_for` to strictly enforce timeouts. The service uses `asyncio.gather(..., return_exceptions=True)` to ensure that if a single provider fails, the orchestration gracefully degrades and continues scoring the remaining results.
