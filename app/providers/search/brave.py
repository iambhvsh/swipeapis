from ddgs import DDGS
from typing import List, Dict, Any
import urllib.parse
import asyncio


class BraveProviderError(Exception):
    pass


def fetch_brave_sync(q: str, region: str, safesearch: str, num_results: int) -> List[Dict[str, Any]]:
    try:
        ddgs = DDGS()
        results = []
        count = 0
        for r in ddgs.text(
            query=q,
            region=region,
            safesearch=safesearch,
            backend="brave",
            max_results=num_results,
        ):
            if count >= num_results:
                break
            url = r.get("href", r.get("url", ""))
            if url:
                results.append(
                    {
                        "url": url,
                        "title": r.get("title", ""),
                        "description": r.get("body", r.get("description", "")),
                        "source": urllib.parse.urlparse(url).netloc,
                        "provider": "brave",
                    }
                )
            count += 1
        return results
    except Exception as e:
        raise BraveProviderError(f"Brave search failed: {e}") from e


async def fetch_brave_results(
    q: str, region: str = "us-en", safesearch: str = "moderate", num_results: int = 10
) -> List[Dict[str, Any]]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_brave_sync, q, region, safesearch, num_results)
