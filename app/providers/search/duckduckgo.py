from ddgs import DDGS
from typing import List, Dict, Any, Optional
import urllib.parse

class DuckDuckGoProviderError(Exception):
    pass

def fetch_duckduckgo_results(
    q: str,
    region: str = 'us-en',
    safesearch: str = 'moderate',
    start: int = 0,
    num_results: int = 10
) -> List[Dict[str, Any]]:
    try:
        ddgs = DDGS()
        page_results_list = []
        seen_urls = set()
        current_page = 1

        while len(page_results_list) < start + num_results:
            try:
                page_data = ddgs.text(
                    query=q,
                    region=region,
                    safesearch=safesearch,
                    page=current_page,
                    backend="auto"
                )
            except Exception:
                break

            if not page_data:
                break

            for result in page_data:
                url = result.get('href', result.get('url', ''))
                if url and url not in seen_urls:
                    seen_urls.add(url)

                    # Formatting logic in provider
                    page_results_list.append({
                        "url": url,
                        "title": result.get('title', ''),
                        "description": result.get('body', result.get('description', '')),
                        "source": urllib.parse.urlparse(url).netloc if url else '',
                    })

            current_page += 1
            if current_page > 15:
                break

        return page_results_list[start : start + num_results]

    except Exception as e:
        raise DuckDuckGoProviderError(f"DuckDuckGo search failed: {e}")
