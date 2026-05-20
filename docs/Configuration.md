# Configuration

Atlas requires minimal configuration to run. Environment overrides can optionally be used for custom deployment tuning.

## Limits and Timeouts

- **Rate Limits**: Configured decoratively on `app/routes/*.py` using `@limiter.limit("60/minute")`.
- **Search Provider Bounds**: The search service limits deep-page fanouts internally with a hard cap (`MAX_PROVIDER_RESULTS = 100`) to prevent infrastructure exhaustion.
- **Provider Timeouts**: Primary providers are capped at `3.0` seconds and fallbacks at `5.0` seconds via `asyncio.wait_for`.
