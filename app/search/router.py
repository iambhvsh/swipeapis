from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from .services import google_search_service, SearchError, EmptyQueryError, \
    ALL_FIELDS

router = APIRouter()


@router.get("/", response_model=List[Dict[str, Any]])
async def perform_search(
    q: str = Query(..., description="The search query string."),
    num_results: int = Query(
        10, ge=1, le=100, description="The maximum number of results to return."
    ),
    start: int = Query(
        0, ge=0, description="The starting index of the results (for pagination)."
    ),
    language: str = Query(
        "en", description="The language to use for the search (e.g., 'en', 'es')."
    ),
    safe: bool = Query(
        True, description="Set to false to disable Google's SafeSearch."
    ),
    include_rank: bool = Query(
        False, description="Set to true to include the search result rank."
    ),
    fields: Optional[str] = Query(
        None,
        description="A comma-separated list of fields to return. "
                    f"Available fields: {', '.join(ALL_FIELDS)}. "
                    "Defaults to all fields."
    )
):
    """
    Performs a Google search and returns a list of results.

    This endpoint provides the URL, title, and description for each result.
    """
    try:
        results = google_search_service(
            q=q,
            num_results=num_results,
            start=start,
            language=language,
            safe=safe,
            include_rank=include_rank,
            fields=fields
        )
        return results
    except EmptyQueryError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SearchError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
