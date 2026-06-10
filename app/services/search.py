import asyncio
import logging
from typing import Any, Dict, List, Optional, cast

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


ALL_FIELDS = ["url", "title", "description", "source", "rank", "provider", "score"]

MAX_PROVIDER_RESULTS = 100


def deduplicate_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen_urls = set()
    deduped_results: List[Dict[str, Any]] = []

    for idx, result in enumerate(results, start=1):
        raw_url = result.get("url")

        if not raw_url:
            continue

        normalized = normalize_url(raw_url)

        if "original_rank" not in result:
            result["original_rank"] = idx

        if normalized in seen_urls:
            for existing in deduped_results:
                existing_url = existing.get("url")

                if existing_url and normalize_url(existing_url) == normalized:
                    existing["frequency"] = existing.get("frequency", 1) + 1
                    break

            continue

        seen_urls.add(normalized)
        result["frequency"] = 1
        deduped_results.append(result)

    return deduped_results


async def search_service(
    q: str, num_results: int, start: int, language: str, safe: bool, include_rank: bool, fields: Optional[str]
) -> List[Dict[str, Any]]:

    q = q.strip()

    if not q:
        raise EmptyQueryError("Search query cannot be empty.")

    if fields:
        requested_fields = {field.strip() for field in fields.split(",")}

        if not requested_fields.issubset(ALL_FIELDS):
            invalid_fields = requested_fields - set(ALL_FIELDS)

            raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}")
    else:
        requested_fields = {"url", "title", "description", "source", "rank"}

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

    provider_num_results = min(MAX_PROVIDER_RESULTS, max(10, num_results + start))

    bing_task = asyncio.wait_for(fetch_bing_results(q, region, safesearch, provider_num_results), timeout=10.0)

    brave_task = asyncio.wait_for(fetch_brave_results(q, region, safesearch, provider_num_results), timeout=10.0)

    bing_result, brave_result = await asyncio.gather(bing_task, brave_task, return_exceptions=True)

    raw_results: List[Dict[str, Any]] = []

    if isinstance(bing_result, Exception):
        logger.warning("Bing failed: %r (%s)", bing_result, type(bing_result).__name__)
    else:
        raw_results.extend(cast(List[Dict[str, Any]], bing_result))

    if isinstance(brave_result, Exception):
        logger.warning("Brave failed: %r (%s)", brave_result, type(brave_result).__name__)
    else:
        raw_results.extend(cast(List[Dict[str, Any]], brave_result))

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
                raw_results.extend(cast(List[Dict[str, Any]], result))

    if not raw_results:
        raise SearchError("All search providers failed to return results.")

    processed_results = process_results(raw_results)

    ranked_results = rank_results(processed_results, q)

    paginated = ranked_results[start:start + num_results]

    final_response: List[Dict[str, Any]] = []

    for res in paginated:
        filtered = res.model_dump_filtered(requested_fields)
        if not include_rank and "rank" in filtered:
            del filtered["rank"]
        final_response.append(filtered)

    return final_response
