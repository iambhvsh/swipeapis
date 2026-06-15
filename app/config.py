from types import MappingProxyType


class Settings:
    # Rate limits
    SEARCH_RATE_LIMIT = "30/minute"
    ROOT_RATE_LIMIT = "30/minute"

    # Providers
    MAX_PROVIDER_RESULTS = 100
    _PROVIDER_WEIGHTS_DATA = {
        "bing": 100,
        "brave": 95,
        "duckduckgo": 90,
        "yahoo": 85,
    }
    PROVIDER_WEIGHTS = MappingProxyType(_PROVIDER_WEIGHTS_DATA)

    # RRF (Reciprocal Rank Fusion)
    RRF_K = 60
    RRF_SCALE_FACTOR = 1000

    # Relevance Weights
    EXACT_MATCH_SCORE = 200.0
    STARTS_WITH_SCORE = 50.0
    QUERY_COVERAGE_MULTIPLIER = 100.0
    TITLE_PURITY_MULTIPLIER = 50.0
    TITLE_TERM_MATCH = 15.0
    URL_TERM_MATCH = 15.0
    DESCRIPTION_TERM_MATCH = 10.0
    PHRASE_MATCH_TITLE = 50.0
    PHRASE_MATCH_DESCRIPTION = 30.0

    # Navigation Boosts
    NAV_EXACT_MATCH = 200.0
    NAV_STARTS_WITH = 100.0
    NAV_CONTAINS = 50.0
    NAV_DOMAIN_MATCH = 300.0

    # Diversity
    DEFAULT_DUPLICATE_PENALTY = 50.0
    DEFAULT_MAX_RESULTS_PER_DOMAIN = 2

    # Safety Penalties
    MISSING_TITLE_PENALTY = -100.0
    MISSING_URL_PENALTY = -100.0
    MISSING_DESCRIPTION_PENALTY = -25.0

    # Cross Provider
    FREQUENCY_MULTIPLIER = 50.0

    # Freshness
    FRESHNESS_MULTIPLIER = 50.0

    # Authority
    OFFICIAL_DOMAIN_MATCH = 350.0
    PARTIAL_DOMAIN_MATCH = 75.0
    HOMEPAGE_AUTHORITY_BONUS = 60.0
    HIGH_AUTHORITY_SOURCE_BONUS = 90.0
    LOW_AUTHORITY_SOURCE_PENALTY = -80.0
    TITLE_NOISE_PENALTY = -70.0


settings = Settings()
