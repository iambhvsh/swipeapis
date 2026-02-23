from ddgs import DDGS
from typing import List, Dict, Any, Optional
import urllib.parse


class SearchError(Exception):
    """Custom exception for errors during a search."""
    pass


class EmptyQueryError(Exception):
    """Custom exception for when an empty query is provided."""
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
    """
    Main service to perform a web search using DDGS (metasearch), aggregating results
    from multiple backends (DuckDuckGo, Bing, Google, etc.) for better reliability.
    """
    if not q:
        raise EmptyQueryError("Search query cannot be empty.")

    try:
        # Determine which fields to return based on the 'fields' parameter.
        if fields:
            requested_fields = {field.strip() for field in fields.split(",")}
            # Ensure only valid fields are requested to prevent user confusion.
            if not requested_fields.issubset(ALL_FIELDS):
                invalid_fields = requested_fields - set(ALL_FIELDS)
                raise ValueError(
                    f"Invalid fields requested: {', '.join(invalid_fields)}"
                )
        else:
            # If no fields are specified, default to all available fields.
            requested_fields = set(ALL_FIELDS)

        # Use DDGS with appropriate parameters
        try:
            # Map language to region code
            region_map = {
                'en': 'us-en',
                'es': 'es-es',
                'fr': 'fr-fr',
                'de': 'de-de',
                'ja': 'jp-jp',
                'zh': 'cn-zh',
                'ru': 'ru-ru',
                'pt': 'br-pt',
                'it': 'it-it'
            }
            region = region_map.get(language, 'us-en')
            
            # Map safe parameter to safesearch level
            safesearch = 'moderate' if safe else 'off'
            
            # Pagination logic
            # We assume a base page size of roughly 10-20 results per page call,
            # but since we are using 'all' backends, we might get more.
            # We will fetch pages sequentially and accumulate unique results.
            
            ddgs = DDGS()
            page_results_list = []
            seen_urls = set()

            # Start fetching from page 1, regardless of 'start' parameter, because
            # we need to build our own index since different engines paginate differently.
            # However, to be efficient, we can estimate start page.
            # But with multiple engines aggregating, page 1 might return 50 results.
            # So start_page = 1 is safest to ensure we don't miss anything,
            # especially since we deduplicate.

            current_page = 1

            # Safety break to avoid infinite loops - fetch at most enough pages to cover the request
            # Heuristic: max 10 pages deep or until we have enough results
            while len(page_results_list) < start + num_results:
                # Use backend="api" which tends to cover multiple sources or "auto"
                # The user asked for "all backends". backend="html" is also an option.
                # ddgs "text" method defaults to backend="api" if not specified?
                # No, default is "auto". Let's use "auto" which uses all available engines.
                try:
                    page_data = ddgs.text(
                        query=q,
                        region=region,
                        safesearch=safesearch,
                        page=current_page,
                        backend="auto"
                    )
                except Exception:
                    # If a page fetch fails, try continuing or break?
                    # If page 1 fails completely, we might have issues.
                    # But ddgs usually handles individual engine failures.
                    break

                if not page_data:
                    break

                # Deduplicate and add to list
                for result in page_data:
                    url = result.get('href', result.get('url', ''))
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        page_results_list.append(result)

                current_page += 1

                # Safety break
                if current_page > 15:
                    break

            # Extract the slice we need
            # If we don't have enough results to cover 'start', we return empty or what we have
            if start >= len(page_results_list):
                results_to_process = []
            else:
                results_to_process = page_results_list[start : start + num_results]
            
        except Exception as e:
            # If the search library itself fails, raise a specific error.
            raise SearchError(f"The underlying search library failed: {e}")

        # Process and filter results
        response_list = []
        
        for i, result in enumerate(results_to_process):
            # DDGS returns dict with keys that vary by backend
            url = result.get('href', result.get('url', ''))
            title = result.get('title', '')
            description = result.get('body', result.get('description', ''))
            
            full_data = {
                "url": url,
                "title": title,
                "description": description,
                "source": urllib.parse.urlparse(url).netloc if url else '',
                "rank": start + i + 1
            }

            # Filter the data to only include the fields the user asked for.
            res_dict = {
                key: value for key, value in full_data.items()
                if key in requested_fields
            }

            # The 'rank' field is special; it's only included if the
            # `include_rank` flag is True, even if 'rank' is in fields.
            if not include_rank and "rank" in res_dict:
                del res_dict["rank"]

            response_list.append(res_dict)

        return response_list

    except ValueError as e:
        # Re-raise validation errors (e.g., invalid fields) to be caught
        # by the router, which will return a 400 Bad Request.
        raise e
    except Exception as e:
        # Catch any other exceptions during the search process.
        raise SearchError(f"Error fetching search results: {e}")
