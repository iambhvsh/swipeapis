# Providers

Atlas relies on a series of upstream providers to source initial search results. These providers act as headless adapters, securely formatting and executing requests to external search engines.

## Overview

Providers are located in the `app/providers/search/` directory. They isolate the core Atlas engine from the specific implementation details of external APIs.

The current implementation uses the following adapters:

* `bing.py`
* `brave.py`
* `duckduckgo.py`
* `yahoo.py`

## Tiered Execution

To maintain speed and limit rate limit exhaustion, Atlas executes provider requests in a tiered format within `app/services/search.py`.

### Tier 1
Atlas initiates concurrent, asynchronous requests to Bing and Brave. These providers are generally faster and return highly relevant initial result sets. If Tier 1 yields sufficient unique URLs to satisfy the requested payload size, the provider orchestration concludes.

### Tier 2
If the resulting unique URLs from Tier 1 fall below the configured threshold, Atlas falls back to Tier 2 providers (DuckDuckGo and Yahoo). These are executed concurrently to backfill the missing results.

## Adapter Architecture

Each provider adapter must implement a single public asynchronous function responsible for:

1. Accepting the query string, region, SafeSearch parameter, and maximum result limit.
2. Executing the remote request using `ddgs`.
3. Parsing the external response into a standardized list of dictionaries containing `title`, `url`, `description`, `source`, and `provider`.
4. Returning the parsed list to the orchestrator.

If a provider fails, times out, or returns invalid data, the exception is caught by the orchestration layer. A warning is logged, and Atlas gracefully proceeds with the results gathered from the successful providers.
