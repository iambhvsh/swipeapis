from ddgs import DDGS
from typing import List, Dict, Any
import urllib.parse
import asyncio

class BingProviderError(Exception):
    pass

def fetch_bing_sync(q: str, region: str, safesearch: str, num_results: int) -> List[Dict[str, Any]]:
    try:
        ddgs = DDGS()
        results = []
        # ddgs text yields results.
        # We only want to fetch up to num_results to optimize latency.
        # DDGS automatically handles backend and pagination.
        count = 0
        for r in ddgs.text(query=q, region=region, safesearch=safesearch, backend="bing", max_results=num_results):
            if count >= num_results:
                break
            url = r.get('href', r.get('url', ''))
            if url:
                results.append({
                    "url": url,
                    "title": r.get('title', ''),
                    "description": r.get('body', r.get('description', '')),
                    "source": urllib.parse.urlparse(url).netloc,
                    "provider": "bing"
                })
            count += 1
        return results
    except Exception as e:
        raise BingProviderError(f"Bing search failed: {e}") from e

async def fetch_bing_results(q: str, region: str = 'us-en', safesearch: str = 'moderate', num_results: int = 10) -> List[Dict[str, Any]]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_bing_sync, q, region, safesearch, num_results)
