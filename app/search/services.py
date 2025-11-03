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


def google_search_service(
    q: str,
    num_results: int,
    start: int,
    language: str,
    safe: bool,
    include_rank: bool,
    fields: Optional[str]
) -> List[Dict[str, Any]]:
    """
    Main service to perform a web search using DDGS (metasearch), returning rich results.
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

        # Use DDGS (metasearch) with appropriate parameters
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
            
            # Calculate page number and results per page
            # start is the offset, so we need to calculate which page that represents
            # DDGS uses 1-based page numbering
            page = (start // num_results) + 1 if num_results > 0 else 1
            
            # Total results to fetch (to handle offset within page)
            total_results = start + num_results
            
            # Perform the search
            ddgs = DDGS()
            search_results = ddgs.text(
                query=q,
                region=region,
                safesearch=safesearch,
                max_results=total_results,
                page=1,  # Always get from page 1 and slice locally
                backend="auto"
            )
            
        except Exception as e:
            # If the search library itself fails, raise a specific error.
            raise SearchError(f"The underlying search library failed: {e}")

        # Process and filter results
        response_list = []
        
        # Skip the first 'start' results for pagination
        results_to_process = search_results[start:start + num_results] if start < len(search_results) else []
        
        for i, result in enumerate(results_to_process):
            # DDGS returns dict with keys that vary by backend
            # Common keys: href, title, body/description
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
