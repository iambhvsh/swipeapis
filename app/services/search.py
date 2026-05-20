from typing import List, Dict, Any, Optional
from app.providers.search.duckduckgo import fetch_duckduckgo_results, DuckDuckGoProviderError

class SearchError(Exception):
    pass

class EmptyQueryError(Exception):
    pass

ALL_FIELDS = ["url", "title", "description", "source", "rank"]

def search_service(
    q: str,
    num_results: int,
    start: int,
    language: str,
    safe: bool,
    include_rank: bool,
    fields: Optional[str]
) -> List[Dict[str, Any]]:
    if not q:
        raise EmptyQueryError("Search query cannot be empty.")

    if fields:
        requested_fields = {field.strip() for field in fields.split(",")}
        if not requested_fields.issubset(ALL_FIELDS):
            invalid_fields = requested_fields - set(ALL_FIELDS)
            raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}")
    else:
        requested_fields = set(ALL_FIELDS)

    region_map = {
        'en': 'us-en', 'es': 'es-es', 'fr': 'fr-fr', 'de': 'de-de',
        'ja': 'jp-jp', 'zh': 'cn-zh', 'ru': 'ru-ru', 'pt': 'br-pt', 'it': 'it-it'
    }
    region = region_map.get(language, 'us-en')
    safesearch = 'moderate' if safe else 'off'

    try:
        # Aggregation layer (calling providers)
        raw_results = fetch_duckduckgo_results(
            q=q, region=region, safesearch=safesearch,
            start=start, num_results=num_results
        )
    except DuckDuckGoProviderError as e:
        raise SearchError(str(e))

    # Normalization, Deduplication and Ranking
    seen_urls = set()
    response_list = []

    # Actually deduplicate
    for i, result in enumerate(raw_results):
        url = result['url']
        if url in seen_urls:
            continue
        seen_urls.add(url)

        # Rank Orchestration Layer
        result['rank'] = start + len(response_list) + 1

        # Format unified response
        res_dict = {
            key: value for key, value in result.items()
            if key in requested_fields
        }

        if not include_rank and "rank" in res_dict:
            del res_dict["rank"]

        response_list.append(res_dict)

    return response_list
