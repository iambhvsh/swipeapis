from ddgs import DDGS
from typing import List, Dict, Any, Type
import urllib.parse


def fetch_provider_sync(
    q: str,
    region: str,
    safesearch: str,
    num_results: int,
    backend: str,
    provider_name: str,
    error_class: Type[Exception],
) -> List[Dict[str, Any]]:
    try:
        ddgs = DDGS()
        results = []
        for r in ddgs.text(
            query=q,
            region=region,
            safesearch=safesearch,
            backend=backend,
            max_results=num_results,
        ):
            if len(results) >= num_results:
                break
            url = r.get("href", r.get("url", ""))
            if url:
                results.append(
                    {
                        "url": url,
                        "title": r.get("title", ""),
                        "description": r.get("body", r.get("description", "")),
                        "source": urllib.parse.urlparse(url).netloc,
                        "provider": provider_name,
                    }
                )
        return results
    except Exception as e:
        raise error_class(f"{provider_name.capitalize()} search failed: {e}") from e
