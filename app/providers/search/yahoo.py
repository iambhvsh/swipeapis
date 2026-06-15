import asyncio

from app.models import RawSearchResult
from app.providers.search.base import fetch_provider_sync


class YahooProviderError(Exception):
    pass


def fetch_yahoo_sync(q: str, region: str, safesearch: str, num_results: int) -> list[RawSearchResult]:
    return fetch_provider_sync(q, region, safesearch, num_results, "yahoo", "yahoo", YahooProviderError)


async def fetch_yahoo_results(
    q: str, region: str = "us-en", safesearch: str = "moderate", num_results: int = 10
) -> list[RawSearchResult]:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fetch_yahoo_sync, q, region, safesearch, num_results)
