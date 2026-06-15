import asyncio

from app.models import RawSearchResult
from app.providers.search.base import fetch_provider_sync


class BraveProviderError(Exception):
    pass


def fetch_brave_sync(q: str, region: str, safesearch: str, num_results: int) -> list[RawSearchResult]:
    return fetch_provider_sync(q, region, safesearch, num_results, "brave", "brave", BraveProviderError)


async def fetch_brave_results(
    q: str, region: str = "us-en", safesearch: str = "moderate", num_results: int = 10
) -> list[RawSearchResult]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fetch_brave_sync, q, region, safesearch, num_results)
