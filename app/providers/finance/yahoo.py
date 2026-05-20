import yfinance as yf
from typing import Dict, Any, List, Optional

class YahooFinanceProviderError(Exception):
    pass

class TickerNotFoundError(Exception):
    pass

def fetch_yahoo_finance_data(
    ticker: str,
    history_days: int = 0,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = "1d",
    include_recommendations: bool = False,
    adjusted: bool = True
) -> Dict[str, Any]:
    try:
        stock = yf.Ticker(ticker)

        try:
            info = stock.info
        except Exception as e:
            raise YahooFinanceProviderError(f"Error fetching basic info: {e}")

        if not info or ('regularMarketPrice' not in info and 'currentPrice' not in info and 'previousClose' not in info):
            hist_check = stock.history(period="1d")
            if hist_check.empty:
                raise TickerNotFoundError(f"Ticker '{ticker}' not found.")

        response_data = {"info": info}

        # Fallback for price if missing
        if info.get('currentPrice') is None and info.get('regularMarketPrice') is None:
            try:
                fast_info = stock.fast_info
                if hasattr(fast_info, 'last_price'):
                    response_data["info"]["fast_price"] = fast_info.last_price
            except Exception:
                pass

        # Fallback for previous close if missing
        if info.get('previousClose') is None and info.get('regularMarketPreviousClose') is None:
            try:
                hist_2d = stock.history(period="2d")
                if len(hist_2d) >= 2:
                    response_data["info"]["fallback_previous_close"] = hist_2d['Close'].iloc[-2]
            except Exception:
                pass

        if history_days > 0 or start_date:
            try:
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
                    date_col = next((col for col in hist_df.columns if 'Date' in col), None)
                    if date_col:
                        hist_df[date_col] = hist_df[date_col].dt.strftime('%Y-%m-%d %H:%M:%S')
                        response_data["historical"] = hist_df.rename(columns={date_col: "date"}).to_dict(orient="records")
                    else:
                        response_data["historical"] = []
                else:
                    response_data["historical"] = []
            except Exception as e:
                response_data["historical"] = {"error": f"Could not fetch historical data: {e}"}

        if include_recommendations:
            try:
                recs_df = stock.recommendations
                if recs_df is not None and not recs_df.empty:
                    recs_df = recs_df.reset_index()
                    date_col = next((col for col in recs_df.columns if 'Date' in col), None)
                    if date_col:
                        recs_df[date_col] = recs_df[date_col].dt.strftime('%Y-%m-%d')
                        response_data["recommendations"] = recs_df.rename(columns={date_col: "date"}).to_dict(orient="records")
                    else:
                        response_data["recommendations"] = recs_df.to_dict(orient="records")
                else:
                    response_data["recommendations"] = []
            except Exception as e:
                response_data["recommendations"] = {"error": f"Could not fetch recommendations: {e}"}

        return response_data

    except TickerNotFoundError as e:
        raise e
    except Exception as e:
        raise YahooFinanceProviderError(f"Error fetching data for ticker {ticker}: {e}")
