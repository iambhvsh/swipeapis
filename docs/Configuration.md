# Configuration

Atlas requires minimal configuration to run. Environment overrides can optionally be used for custom deployment tuning.

## Limits and Timeouts

- **Rate Limits**: Configured decoratively on `app/routes/*.py` using `@limiter.limit("60/minute")`. This applies universally across `/search`, `/finance`, and `/news`.
- **Search Provider Bounds**: The search service limits deep-page fanouts internally with a hard cap (`MAX_PROVIDER_RESULTS = 100`) to prevent infrastructure exhaustion.
- **Provider Timeouts**: Primary search providers are capped at `3.0` seconds and fallbacks at `5.0` seconds via `asyncio.wait_for`.
- **Finance Limits**: Finance gracefully captures upstream issues without crashing, defaulting arrays (e.g., `historical` or `recommendations`) to empty lists and appending to an `errors` array safely when Yahoo Finance is slow.
