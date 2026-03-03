import logging
from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Dict, Any, Optional
from .services import search_service, SearchError, EmptyQueryError, \
    ALL_FIELDS
from app.limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
@limiter.limit("60/minute")
async def perform_search(
    request: Request,
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
        True, description="Set to false to disable SafeSearch."
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
    Performs a web search using Bing (via DDGS) and returns a list of results.

    This endpoint provides the URL, title, and description for each result.
    """
    logger.info(f"Performing search query: {q}, language: {language}")
    try:
        results = search_service(
            q=q,
            num_results=num_results,
            start=start,
            language=language,
            safe=safe,
            include_rank=include_rank,
            fields=fields
        )
        return {"results": results}
    except EmptyQueryError as e:
        logger.warning(f"Empty query error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        logger.warning(f"Value error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except SearchError as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in search endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
