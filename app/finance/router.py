from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional
from .services import get_finance_data_service, TickerNotFoundError, \
    YFinanceError

router = APIRouter()


@router.get("/{ticker}", response_model=dict)
async def get_finance_data(
    ticker: str = Path(..., description="The stock ticker symbol (e.g., AAPL, GOOGL)."),
    fields: Optional[str] = Query(
        None,
        description="A comma-separated list of fields to return. "
                    "If not specified, a default set of fields is returned. "
                    "Check the main API documentation for available fields."
    ),
    history_days: int = Query(
        0, ge=0, description="The number of days of historical price data to fetch."
    ),
    interval: str = Query(
        "1d",
        description="The interval for historical data (e.g., '1m', '5m', '1d', '1wk')."
    ),
    include_recommendations: bool = Query(
        False, description="Set to true to include analyst recommendations."
    ),
    adjusted: bool = Query(
        True, description="Set to false to get unadjusted historical data."
    )
):
    """
    Fetches a wide range of financial data for a given stock ticker.

    This endpoint provides real-time data fields, historical price data,
    and analyst recommendations.
    """
    try:
        data = get_finance_data_service(
            ticker=ticker,
            fields=fields,
            history_days=history_days,
            interval=interval,
            include_recommendations=include_recommendations,
            adjusted=adjusted
        )
        return data
    except TickerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except YFinanceError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
