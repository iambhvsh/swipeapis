import yfinance as yf
from typing import Optional, Dict, Any


# Mapping from user-friendly field names to yfinance keys
FIELD_MAPPING = {
    "price": "regularMarketPrice",
    "market_cap": "marketCap",
    "pe_ratio": "trailingPE",
    "pb_ratio": "priceToBook",
    "beta": "beta",
    "dividend_yield": "dividendYield",
    "52_week_high": "fiftyTwoWeekHigh",
    "52_week_low": "fiftyTwoWeekLow",
    "volume": "regularMarketVolume",
    "average_volume": "averageVolume",
    "open": "regularMarketOpen",
    "previous_close": "previousClose",
    "forward_pe": "forwardPE",
    "enterprise_value": "enterpriseValue",
    "payout_ratio": "payoutRatio",
}

DEFAULT_FIELDS = [
    "price", "previous_close", "market_cap", "pe_ratio", "52_week_high", "52_week_low"
]


class TickerNotFoundError(Exception):
    """Custom exception for when a ticker is not found by yfinance."""
    pass


class YFinanceError(Exception):
    """Custom exception for errors originating from the yfinance library."""
    pass


def get_finance_data_service(
    ticker: str,
    fields: Optional[str],
    history_days: int,
    start_date: Optional[str],
    end_date: Optional[str],
    interval: str,
    include_recommendations: bool,
    adjusted: bool
) -> Dict[str, Any]:
    """
    Main service to fetch all financial data for a given ticker.
    It orchestrates calls to yfinance for different data types.
    """
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        # A ticker is considered invalid if it has no info object or no market price.
        # This is a much stricter check to avoid tickers with no real data.
        if not stock_info or 'regularMarketPrice' not in stock_info or stock_info['regularMarketPrice'] is None:
            # We double-check history as a fallback for some assets.
            if stock.history(period="1d").empty:
                raise TickerNotFoundError(
                    f"Ticker '{ticker}' not found or no valid market data available."
                )

    except Exception as e:
        # This can catch broader network issues or yfinance errors.
        raise YFinanceError(f"Error initializing ticker '{ticker}': {e}")

    response_data = {"ticker": stock_info.get('symbol', ticker.upper())}

    # Determine which fields to fetch from the .info object
    if fields:
        requested_fields = [field.strip() for field in fields.split(",")]
    else:
        requested_fields = DEFAULT_FIELDS

    # Populate response with requested fields
    for field in requested_fields:
        yf_key = FIELD_MAPPING.get(field)
        if yf_key and yf_key in stock_info and stock_info[yf_key] is not None:
            response_data[field] = stock_info[yf_key]
        else:
            response_data[field] = None

    # --- FIX: Ensure previous_close is available for change calculation ---
    # If yfinance .info doesn't provide previousClose, fetch it from history
    if "previous_close" in requested_fields and response_data.get("previous_close") is None:
        try:
            hist = stock.history(period="2d")
            if not hist.empty and len(hist) > 1:
                # The second to last entry is the previous day's close
                response_data["previous_close"] = hist['Close'].iloc[-2]
        except Exception:
            # If this fails, we still have None, which is handled by the frontend
            pass
    # --- END FIX ---

    # Separately fetch historical data if requested
    if history_days > 0 or start_date:
        try:
            # Prioritize start/end date over history_days
            if start_date:
                hist_df = stock.history(
                    start=start_date, end=end_date,
                    interval=interval, auto_adjust=adjusted
                )
            else:
                hist_df = stock.history(
                    period=f"{history_days}d", interval=interval,
                    auto_adjust=adjusted
                )

            if not hist_df.empty:
                hist_df = hist_df.reset_index()
                # Find the date column, which can have different names
                date_col = next(
                    (col for col in hist_df.columns if 'Date' in col), None
                )
                if date_col:
                    # Format date for consistent JSON output
                    hist_df[date_col] = hist_df[date_col].dt.strftime(
                        '%Y-%m-%d %H:%M:%S'
                    )
                    response_data["historical"] = hist_df.rename(
                        columns={date_col: "date"}
                    ).to_dict(orient="records")
                else:
                    response_data["historical"] = []
            else:
                response_data["historical"] = []
        except Exception as e:
            # Don't fail the whole request if history fails, just report error
            response_data["historical"] = {
                "error": f"Could not fetch historical data: {e}"
            }

    # Separately fetch recommendations if requested
    if include_recommendations:
        try:
            recs_df = stock.recommendations
            if recs_df is not None and not recs_df.empty:
                recs_df = recs_df.reset_index()
                # Find the date column, which can have different names
                date_col = next(
                    (col for col in recs_df.columns if 'Date' in col), None
                )
                if date_col:
                    recs_df[date_col] = recs_df[date_col].dt.strftime('%Y-%m-%d')
                    response_data["recommendations"] = recs_df.rename(
                        columns={date_col: "date"}
                    ).to_dict(orient="records")
                else:
                    # If no date column found, return as is but without date formatting
                    response_data["recommendations"] = recs_df.to_dict(orient="records")
            else:
                response_data["recommendations"] = []
        except Exception as e:
            # Don't fail the whole request if recommendations fail
            response_data["recommendations"] = {
                "error": f"Could not fetch recommendations: {e}"
            }

    return response_data
