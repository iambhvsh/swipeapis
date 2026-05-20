# Providers

Providers in Atlas serve strictly as data extraction adapters. They isolate upstream dependencies (like `ddgs` or `yfinance`) from the internal core.

## Search Providers

Atlas implements the following backend adapters using the `ddgs` library. They are not direct native engine APIs, but adapters wrapping the library's scraping capabilities:
- **Bing** (Primary)
- **Brave** (Primary)
- **DuckDuckGo** (Fallback)
- **Yahoo** (Fallback)

Providers are restricted from performing deduplication or ranking. Their only responsibility is to execute network calls, handle pagination to the limit, and yield raw results.

## Finance Providers

- **Yahoo** (`yfinance` adapter). Fetches stock quotes, 52-week metrics, and graceful fallbacks for missing `previousClose` values.

## News Providers

- **Headlines** (`pygooglenews` adapter). Aggregates topical or categorical headlines. It extracts summaries and publication dates but does *not* behave as a full article-scraping engine.
