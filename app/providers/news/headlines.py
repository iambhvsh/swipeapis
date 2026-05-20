from pygooglenews import GoogleNews
from typing import List, Dict, Any, Optional
import re
import html

class HeadlinesProviderError(Exception):
    pass

def clean_html(raw_html: str) -> str:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.unescape(cleantext)

def fetch_headlines(
    q: Optional[str] = None,
    language: str = "en",
    region: str = "US",
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    category: Optional[str] = None,
    start: int = 0,
    num_results: int = 10
) -> Dict[str, Any]:
    try:
        gn = GoogleNews(lang=language.lower(), country=region.upper())
        search_result = None

        use_search = q or from_date or to_date or category

        if use_search:
            search_query = q or category or "top stories"
            if q and category:
                search_query = f"{q} {category}"

            try:
                search_result = gn.search(search_query, from_=from_date, to_=to_date)
            except Exception as e:
                raise HeadlinesProviderError(f"Provider failed on search: {e}")
        else:
            try:
                search_result = gn.top_news()
            except Exception as e:
                raise HeadlinesProviderError(f"Provider failed on top_news: {e}")

        if not search_result:
            raise HeadlinesProviderError("Provider did not return a result.")

        entries = search_result.get('entries', [])
        paginated_entries = entries[start : start + num_results]

        article_list = []
        for entry in paginated_entries:
            description = clean_html(entry.get('summary', ''))
            article = {
                "title": entry.get('title'),
                "url": entry.get('link'),
                "source": entry.get('source', {}).get('title'),
                "published": entry.get('published'),
                "description": description,
            }
            article_list.append(article)

        return {
            "total_articles": len(entries),
            "articles": article_list
        }
    except HeadlinesProviderError as e:
        raise e
    except Exception as e:
        raise HeadlinesProviderError(f"Error fetching headlines: {e}")
