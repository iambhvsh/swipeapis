# Troubleshooting

## Provider Instability (Search)

Atlas relies on the `ddgs` library connecting to live web endpoints.
- If an endpoint consistently throws `DuckDuckGoProviderError` or timeout warnings, this indicates the upstream engine has temporarily throttled requests or altered its DOM.
- Atlas's tiered execution and deduplication ensure that single provider failures won't bring down the API. The system degrades gracefully.

## Missing Finance Data

The Yahoo adapter (`yfinance`) can occasionally return empty dictionaries for obscure tickers.
- Atlas implements a fallback checking mechanism.
- If basic price fields are missing, it attempts to fetch recent 1-day or 2-day historical closures to provide an estimated fallback `price`.
- Deeply missing data is safely isolated into the `errors` array in the response to prevent crashing.

## Debugging

To trace provider execution:
1. Ensure the server is running in development mode.
2. Monitor standard output for `logger.warning` entries indicating Tier 1 or Tier 2 task timeouts.
