import asyncio
import logging
from typing import List, Dict, Any, Optional

from app.providers.search.bing import fetch_bing_results
from app.providers.search.brave import fetch_brave_results
from app.providers.search.duckduckgo import fetch_duckduckgo_results
from app.providers.search.yahoo import fetch_yahoo_results
from app.utils.urls import normalize_url
from app.services.ranking import rank_results

logger = logging.getLogger(__name__)

class SearchError(Exception):
    pass

class EmptyQueryError(Exception):
    pass

ALL_FIELDS = ["url", "title", "description", "source", "rank", "provider", "score"]

async def search_service(
    q: str,
    num_results: int,
    start: int,
    language: str,
    safe: bool,
    include_rank: bool,
    fields: Optional[str]
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
        requested_fields = set(["url", "title", "description", "source", "rank"])

    region_map = {
        'en': 'us-en', 'es': 'es-es', 'fr': 'fr-fr', 'de': 'de-de',
        'ja': 'jp-jp', 'zh': 'cn-zh', 'ru': 'ru-ru', 'pt': 'br-pt', 'it': 'it-it'
    }
    region = region_map.get(language, 'us-en')
    safesearch = 'moderate' if safe else 'off'

    # Optimization: fetch just enough results per provider to be fast
    provider_num_results = max(10, num_results + start)

    # Tier 1 execution (Bing + Brave)
    tier1_tasks = [
        asyncio.wait_for(fetch_bing_results(q, region, safesearch, provider_num_results), timeout=3.0),
        asyncio.wait_for(fetch_brave_results(q, region, safesearch, provider_num_results), timeout=3.0)
    ]

    tier1_results = await asyncio.gather(*tier1_tasks, return_exceptions=True)

    raw_results = []

    for res in tier1_results:
        if isinstance(res, Exception):
            logger.warning(f"Tier 1 provider failed or timed out: {res}")
        elif isinstance(res, list):
            raw_results.extend(res)

    # Evaluate if we need Tier 2
    # Fallback triggers: low result count or low diversity
    unique_urls_tier1 = len(set(normalize_url(r['url']) for r in raw_results))

    if unique_urls_tier1 < provider_num_results:
        logger.info(f"Tier 1 yielded only {unique_urls_tier1} unique results, executing Tier 2.")
        tier2_tasks = [
            asyncio.wait_for(fetch_duckduckgo_results(q, region, safesearch, provider_num_results), timeout=5.0),
            asyncio.wait_for(fetch_yahoo_results(q, region, safesearch, provider_num_results), timeout=5.0)
        ]
        tier2_results = await asyncio.gather(*tier2_tasks, return_exceptions=True)

        for res in tier2_results:
            if isinstance(res, Exception):
                logger.warning(f"Tier 2 provider failed or timed out: {res}")
            elif isinstance(res, list):
                raw_results.extend(res)

    if not raw_results:
        raise SearchError("All search providers failed to return results.")

    # Deduplication and Normalization
    seen_urls = set()
    deduped_results = []

    for result in raw_results:
        normalized = normalize_url(result['url'])

        # Keep original rank for position penalty scoring
        if 'original_rank' not in result:
            result['original_rank'] = raw_results.index(result) + 1

        if normalized in seen_urls:
            # Increase frequency for ranking bonus
            for existing in deduped_results:
                if normalize_url(existing['url']) == normalized:
                    existing['frequency'] = existing.get('frequency', 1) + 1
                    break
            continue

        seen_urls.add(normalized)
        # Add tracking data
        result['frequency'] = 1
        deduped_results.append(result)

    # Rank results
    ranked_results = rank_results(deduped_results)

    # Paginate and Format Response
    paginated = ranked_results[start : start + num_results]

    final_response = []
    for res in paginated:
        res_dict = {
            key: value for key, value in res.items()
            if key in requested_fields
        }

        if not include_rank and "rank" in res_dict:
            del res_dict["rank"]

        final_response.append(res_dict)

    return final_response
