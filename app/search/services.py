from googlesearch import search as google_search_lib, SearchResult
from typing import List, Dict, Any, Optional
import urllib.parse


class SearchError(Exception):
    """Custom exception for errors during a Google search."""
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
    Main service to perform a Google search, returning rich results.
    """
    if not q:
        raise EmptyQueryError("Search query cannot be empty.")

    try:
        # The googlesearch-python library is a generator-based scraper.
        # We pass advanced=True to get SearchResult objects instead of just URLs.
        try:
            results_generator = google_search_lib(
                q,
                num_results=num_results,
                lang=language,
                start_num=start,
                safe='active' if safe else 'off',
                sleep_interval=2.0,  # A short pause to avoid being rate-limited.
                advanced=True
            )
        except Exception as e:
            # If the scraping library itself fails, raise a specific error.
            raise SearchError(f"The underlying search library failed: {e}")

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

        response_list = []
        for i, result in enumerate(results_generator):
            # The library should yield SearchResult objects with advanced=True.
            if not isinstance(result, SearchResult):
                continue

            full_data = {
                "url": result.url,
                "title": result.title,
                "description": result.description,
                "source": urllib.parse.urlparse(result.url).netloc,
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
