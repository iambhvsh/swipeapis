from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from .services import get_news_service, InvalidDateFormatError, \
    NewsFetchingError

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_news(
    q: Optional[str] = Query(
        None,
        description="A search query for news articles. "
                    "If left empty, the endpoint will return top headlines."
    ),
    num_results: int = Query(
        10, ge=1, le=100, description="The maximum number of articles to return."
    ),
    start: int = Query(
        0, ge=0, description="The starting index for pagination."
    ),
    from_date: Optional[str] = Query(
        None,
        description="The start date for articles (YYYY-MM-DD). "
                    "Not applicable for top headlines."
    ),
    to_date: Optional[str] = Query(
        None,
        description="The end date for articles (YYYY-MM-DD). "
                    "Not applicable for top headlines."
    ),
    language: str = Query(
        "en", description="The language of the news articles (e.g., 'en', 'de')."
    ),
    region: str = Query(
        "US", description="The region for the news (e.g., 'US', 'GB', 'IN')."
    ),
    category: Optional[str] = Query(
        None,
        description="A topic to filter by (e.g., 'business', 'technology'). "
                    "Appended to the main query."
    ),
    include_sentiment: bool = Query(
        False,
        description="Set to true to perform sentiment analysis on the title and description."
    )
):
    """
    Fetches news articles from Google News.

    You can either provide a search query `q` to find specific articles,
    or leave it empty to get the current top headlines.
    """
    try:
        articles = get_news_service(
            q=q,
            num_results=num_results,
            start=start,
            from_date=from_date,
            to_date=to_date,
            language=language,
            region=region,
            category=category,
            include_sentiment=include_sentiment
        )
        return articles
    except InvalidDateFormatError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NewsFetchingError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
