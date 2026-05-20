# Providers

Providers in Atlas serve strictly as data extraction adapters. They isolate upstream dependencies (like `ddgs` or `yfinance`) from the internal core infrastructure.

## Search Providers

Atlas implements the following backend adapters using the `ddgs` library. They are not direct native engine APIs, but adapters wrapping the library's scraping capabilities:
- **Bing** (Primary)
- **Brave** (Primary)
- **DuckDuckGo** (Fallback)
- **Yahoo** (Fallback)

Providers are restricted from performing deduplication or ranking. Their only responsibility is to execute network calls, handle pagination to the limit, and yield raw results.

## Finance Providers

- **Yahoo** (`app/providers/finance/yahoo.py`): Built atop `yfinance`. This adapter handles real-time stock quotes, 52-week metrics, and graceful fallbacks for missing `previousClose` and `currentPrice` values via short-term historical aggregation. It strictly guarantees stable array return types.

## News Providers

- **Headlines** (`app/providers/news/headlines.py`): Built atop `pygooglenews`. Aggregates topical or categorical headlines globally. It extracts summaries and publication dates but does *not* behave as a full article-scraping engine. It focuses exclusively on headline metadata orchestration.
