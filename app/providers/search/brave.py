from typing import List, Dict, Any
import asyncio
from app.providers.search.base import fetch_provider_sync


class BraveProviderError(Exception):
    pass


def fetch_brave_sync(q: str, region: str, safesearch: str, num_results: int) -> List[Dict[str, Any]]:
    return fetch_provider_sync(q, region, safesearch, num_results, "brave", "brave", BraveProviderError)


async def fetch_brave_results(
    q: str, region: str = "us-en", safesearch: str = "moderate", num_results: int = 10
) -> List[Dict[str, Any]]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fetch_brave_sync, q, region, safesearch, num_results)
