from typing import Dict, Any, List, Optional
from app.providers.finance.yahoo import fetch_yahoo_finance_data, YahooFinanceProviderError, TickerNotFoundError

class FinanceServiceError(Exception):
    pass

ALL_FIELDS = [
    "price", "market_cap", "volume", "pe_ratio", "dividend_yield",
    "52_week_high", "52_week_low", "beta", "pb_ratio", "forward_pe",
    "enterprise_value", "payout_ratio", "average_volume",
    "open", "previous_close"
]

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
    ticker = ticker.upper()

    if fields:
        requested_fields = {field.strip() for field in fields.split(",")}
        if not requested_fields.issubset(ALL_FIELDS):
            invalid_fields = requested_fields - set(ALL_FIELDS)
            raise ValueError(f"Invalid fields requested: {', '.join(invalid_fields)}")
    else:
        requested_fields = set(ALL_FIELDS)

    try:
        raw_data = fetch_yahoo_finance_data(
            ticker=ticker,
            history_days=history_days,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
            include_recommendations=include_recommendations,
            adjusted=adjusted
        )
    except TickerNotFoundError as e:
        raise e
    except YahooFinanceProviderError as e:
        raise FinanceServiceError(str(e))

    info = raw_data.get("info", {})
    response_data: Dict[str, Any] = {"ticker": ticker}

    field_mappings = {
        "price": info.get('currentPrice', info.get('regularMarketPrice', info.get('fast_price'))),
        "market_cap": info.get('marketCap'),
        "volume": info.get('volume', info.get('regularMarketVolume')),
        "pe_ratio": info.get('trailingPE'),
        "dividend_yield": info.get('dividendYield'),
        "52_week_high": info.get('fiftyTwoWeekHigh'),
        "52_week_low": info.get('fiftyTwoWeekLow'),
        "beta": info.get('beta'),
        "pb_ratio": info.get('priceToBook'),
        "forward_pe": info.get('forwardPE'),
        "enterprise_value": info.get('enterpriseValue'),
        "payout_ratio": info.get('payoutRatio'),
        "average_volume": info.get('averageVolume'),
        "open": info.get('open', info.get('regularMarketOpen')),
        "previous_close": info.get('previousClose', info.get('regularMarketPreviousClose', info.get('fallback_previous_close')))
    }

    for field in requested_fields:
        response_data[field] = field_mappings.get(field)

    if history_days > 0 or start_date:
        response_data["historical"] = raw_data.get("historical", [])

    if include_recommendations:
        response_data["recommendations"] = raw_data.get("recommendations", [])

    return response_data
