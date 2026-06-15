# Configuration

Atlas relies on a centralized configuration file located at `app/config.py`. This ensures that there are no hidden values or unexplained constants embedded directly in the business logic.

## Settings Overview

The `Settings` class dictates how Atlas governs limits, penalties, and multipliers.

### Provider Constraints

* `MAX_PROVIDER_RESULTS`: The absolute limit of results fetched per upstream provider.
* `PROVIDER_WEIGHTS`: A dictionary defining the base confidence score for each provider (Bing, Brave, DuckDuckGo, Yahoo).

### Rate Limits

* `SEARCH_RATE_LIMIT`: The public search endpoint request limit.
* `ROOT_RATE_LIMIT`: The root metadata endpoint request limit.

### Reciprocal Rank Fusion

* `RRF_K`: The constant used in the Reciprocal Rank Fusion algorithm to calculate the baseline score from a result's original provider rank.

### Relevance Multipliers

* `EXACT_MATCH_SCORE`: The score added when the result title perfectly matches the query.
* `STARTS_WITH_SCORE`: The score added when the result title begins with the query.
* `QUERY_COVERAGE_MULTIPLIER`: A multiplier applied to the percentage of query terms found in the title.
* `TITLE_PURITY_MULTIPLIER`: A multiplier that penalizes overly verbose titles.
* `TITLE_TERM_MATCH`: Points awarded per query term found in the title.
* `URL_TERM_MATCH`: Points awarded per query term found in the URL.
* `DESCRIPTION_TERM_MATCH`: Points awarded per query term found in the description.
* `PHRASE_MATCH_TITLE`: Points awarded when the exact query phrase is found within the title.
* `PHRASE_MATCH_DESCRIPTION`: Points awarded when the exact query phrase is found within the description.

### Navigational Boosts

Navigational boosts apply only to queries classified as entity or navigational intent.

* `NAV_EXACT_MATCH`: Points awarded for exact title matches on entity searches.
* `NAV_STARTS_WITH`: Points awarded for titles starting with the entity query.
* `NAV_CONTAINS`: Points awarded when the entity query is contained in the title.
* `NAV_DOMAIN_MATCH`: A significant boost awarded when the URL domain directly matches the query terms, indicating an official website.

### Diversity Constraints

* `DEFAULT_DUPLICATE_PENALTY`: A compounding score penalty applied to subsequent results originating from the same domain.
* `DEFAULT_MAX_RESULTS_PER_DOMAIN`: The absolute maximum number of results allowed from a single domain.

### Safety Penalties

* `MISSING_TITLE_PENALTY`: Penalty applied to results with an empty title string.
* `MISSING_URL_PENALTY`: Penalty applied to results with an empty URL.
* `MISSING_DESCRIPTION_PENALTY`: Penalty applied to results with an empty description.

### Secondary Signals

* `FREQUENCY_MULTIPLIER`: Points awarded per additional upstream provider that returned the exact same URL.
* `FRESHNESS_MULTIPLIER`: Points awarded when recent dates or hours are detected in the metadata of a query classified with freshness intent.

### Authority Signals

* `OFFICIAL_DOMAIN_MATCH`: Boost awarded when a compact query matches the domain stem, such as `next.js` matching `nextjs.org`.
* `PARTIAL_DOMAIN_MATCH`: Smaller boost for partial domain matches on entity and navigational queries.
* `HOMEPAGE_AUTHORITY_BONUS`: Additional score for official homepage results.
* `HIGH_AUTHORITY_SOURCE_BONUS`: Score used for trusted public-interest sources such as `.gov` and `.edu`.
* `LOW_AUTHORITY_SOURCE_PENALTY`: Penalty for configured low-authority domains.
* `TITLE_NOISE_PENALTY`: Penalty for overly long or aggregated titles.

Modifying these parameters in `app/config.py` allows administrators to adjust the ranking behavior without altering core application logic.
