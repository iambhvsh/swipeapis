from typing import List, Dict, Any, Optional
from datetime import datetime
from app.providers.news.headlines import fetch_headlines, HeadlinesProviderError
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
    except ValueError as e:
        raise InvalidDateFormatError(f"Invalid date format for '{date_str}'. Please use YYYY-MM-DD.") from e

def validate_date_range(from_date: Optional[str], to_date: Optional[str]) -> None:
    if from_date and to_date:
        d_from = datetime.strptime(from_date, '%Y-%m-%d')
        d_to = datetime.strptime(to_date, '%Y-%m-%d')
        if d_from > d_to:
            raise InvalidDateFormatError(f"from_date '{from_date}' must be less than or equal to to_date '{to_date}'.")

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
    validate_date_range(valid_from, valid_to)

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

    # Effective query labeling
    if q:
        query_label = q
    elif category:
        query_label = category
    else:
        query_label = "top_headlines"

    return {
        "query": query_label,
        "total_articles": total_articles,
        "articles": article_list,
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
        }
    }
