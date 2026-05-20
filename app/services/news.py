from typing import List, Dict, Any, Optional
from datetime import datetime
from app.providers.news.headlines import fetch_headlines, HeadlinesProviderError

# VADER Sentiment removed from provider and simplified, if not needed to be completely accurate to old one we could keep or drop.
# The prompt says: "If sentiment analysis is not implemented: remove 'services/sentiment.py'" and "Avoid speculative abstractions".
# The previous version had sentiment. We'll keep it here in the service level if requested.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

class NewsFetchingError(Exception):
    pass

class InvalidDateFormatError(Exception):
    pass

def validate_date_format(date_str: Optional[str]) -> Optional[str]:
    if date_str is None:
        return None
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        raise InvalidDateFormatError(f"Invalid date format for '{date_str}'. Please use YYYY-MM-DD.")

def get_news_service(
    q: Optional[str],
    num_results: int,
    start: int,
    from_date: Optional[str],
    to_date: Optional[str],
    language: str,
    region: str,
    category: Optional[str],
    include_sentiment: bool
) -> Dict[str, Any]:
    valid_from = validate_date_format(from_date)
    valid_to = validate_date_format(to_date)

    try:
        provider_data = fetch_headlines(
            q=q,
            language=language,
            region=region,
            from_date=valid_from,
            to_date=valid_to,
            category=category,
            start=start,
            num_results=num_results
        )
    except HeadlinesProviderError as e:
        raise NewsFetchingError(str(e))

    article_list = provider_data.get("articles", [])
    total_articles = provider_data.get("total_articles", 0)

    for article in article_list:
        article["category"] = category if q or category else "top"
        article["language"] = language
        article["region"] = region

        if include_sentiment:
            sentiment_text = f"{article['title']}. {article.get('description', '')}"
            article['sentiment'] = sia.polarity_scores(sentiment_text)

    return {
        "query": q or "top_headlines",
        "total_articles": total_articles,
        "articles": article_list,
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }
    }
