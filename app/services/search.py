import asyncio
import logging
from typing import Any, cast

from app.config import settings
from app.models import RawSearchResult, SearchField, SearchResponse
from app.providers.search.bing import fetch_bing_results
from app.providers.search.brave import fetch_brave_results
from app.providers.search.duckduckgo import fetch_duckduckgo_results
from app.providers.search.yahoo import fetch_yahoo_results
from app.services.ranker import rank_results
from app.services.dedupe import process_results
from app.utils.urls import normalize_url

logger = logging.getLogger(__name__)


class SearchError(Exception):
    pass


class EmptyQueryError(Exception):
    pass


ALL_FIELDS: tuple[SearchField, ...] = (
    "url",
    "title",
    "description",
    "source",
    "rank",
    "provider",
    "providers",
    "score",
    "published_date",
)

DEFAULT_FIELDS: set[SearchField] = {"url", "title", "description", "source", "rank"}


def parse_requested_fields(fields: str | None) -> set[SearchField]:
    if not fields:
        return set(DEFAULT_FIELDS)

    requested = {field.strip() for field in fields.split(",") if field.strip()}
    available = set(ALL_FIELDS)

    if not requested:
        raise ValueError("Fields cannot be empty.")
    if not requested.issubset(available):
        invalid_fields = sorted(requested - available)
        raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}")

    return cast(set[SearchField], requested)


async def search_service(
    q: str,
    num_results: int,
    start: int,
    language: str,
    safe: bool,
    include_rank: bool,
    fields: str | None,
) -> SearchResponse:

    q = q.strip()

    if not q:
        raise EmptyQueryError("Search query cannot be empty.")

    requested_fields = parse_requested_fields(fields)

    region_map = {
        "en": "us-en",
        "es": "es-es",
        "fr": "fr-fr",
        "de": "de-de",
        "ja": "jp-jp",
        "zh": "cn-zh",
        "ru": "ru-ru",
        "pt": "br-pt",
        "it": "it-it",
    }

    region = region_map.get(language, "us-en")

    safesearch = "moderate" if safe else "off"

    provider_num_results = min(settings.MAX_PROVIDER_RESULTS, max(10, num_results + start))

    bing_task = asyncio.wait_for(fetch_bing_results(q, region, safesearch, provider_num_results), timeout=10.0)

    brave_task = asyncio.wait_for(fetch_brave_results(q, region, safesearch, provider_num_results), timeout=10.0)

    bing_result, brave_result = await asyncio.gather(bing_task, brave_task, return_exceptions=True)

    raw_results: list[RawSearchResult] = []

    if isinstance(bing_result, Exception):
        logger.warning("Bing failed: %r (%s)", bing_result, type(bing_result).__name__)
    else:
        raw_results.extend(cast(list[RawSearchResult], bing_result))

    if isinstance(brave_result, Exception):
        logger.warning("Brave failed: %r (%s)", brave_result, type(brave_result).__name__)
    else:
        raw_results.extend(cast(list[RawSearchResult], brave_result))

    unique_urls_tier1 = len({normalize_url(url) for r in raw_results if (url := r.get("url"))})

    if unique_urls_tier1 < provider_num_results:
        logger.info("Tier 1 yielded only %s unique results. Executing Tier 2.", unique_urls_tier1)

        tier2_tasks = [
            asyncio.wait_for(fetch_duckduckgo_results(q, region, safesearch, provider_num_results), timeout=15.0),
            asyncio.wait_for(fetch_yahoo_results(q, region, safesearch, provider_num_results), timeout=15.0),
        ]

        tier2_results = await asyncio.gather(*tier2_tasks, return_exceptions=True)

        providers = {"DuckDuckGo": tier2_results[0], "Yahoo": tier2_results[1]}

        for provider_name, result in providers.items():
            if isinstance(result, Exception):
                logger.warning("%s failed: %r (%s)", provider_name, result, type(result).__name__)
            else:
                raw_results.extend(cast(list[RawSearchResult], result))

    if not raw_results:
        raise SearchError("All search providers failed to return results.")

    processed_results = process_results(raw_results)

    ranked_results = rank_results(processed_results, q)

    paginated = ranked_results[start : start + num_results]

    final_results: list[dict[str, Any]] = []

    for res in paginated:
        filtered = res.model_dump_filtered(requested_fields)
        if not include_rank and "rank" in filtered:
            del filtered["rank"]
        final_results.append(filtered)

    return SearchResponse(total_count=len(ranked_results), results=final_results)
