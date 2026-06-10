from typing import List, Dict, Any
import asyncio
from app.providers.search.base import fetch_provider_sync


class DuckDuckGoProviderError(Exception):
    pass


def fetch_duckduckgo_sync(q: str, region: str, safesearch: str, num_results: int) -> List[Dict[str, Any]]:
    return fetch_provider_sync(q, region, safesearch, num_results, "duckduckgo", "duckduckgo", DuckDuckGoProviderError)


async def fetch_duckduckgo_results(
    q: str, region: str = "us-en", safesearch: str = "moderate", num_results: int = 10
) -> List[Dict[str, Any]]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_duckduckgo_sync, q, region, safesearch, num_results)
