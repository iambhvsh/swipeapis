from pygooglenews import GoogleNews
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
import html

# Initialize VADER once at the module level to avoid re-creation on each call.
sia = SentimentIntensityAnalyzer()


class NewsFetchingError(Exception):
    """Custom exception for errors during news fetching."""
    pass


class InvalidDateFormatError(Exception):
    """Custom exception for invalid date string formats."""
    pass


def clean_html(raw_html: str) -> str:
    """A simple utility to strip HTML tags from a string."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.unescape(cleantext)


def validate_date_format(date_str: Optional[str]) -> Optional[str]:
    """Ensures that a date string is in the 'YYYY-MM-DD' format."""
    if date_str is None:
        return None
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        raise InvalidDateFormatError(
            f"Invalid date format for '{date_str}'. Please use YYYY-MM-DD."
        )


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
    """
    Main service to fetch news. It uses pygooglenews to either search for
    a specific query or get the top headlines.
    """
    valid_from = validate_date_format(from_date)
    valid_to = validate_date_format(to_date)

    try:
        gn = GoogleNews(lang=language.lower(), country=region.upper())
        search_result = None

        # Logic to switch between a targeted search and fetching top news.
        if q:
            full_query = q
            if category:
                full_query += f" when:{category}"
            try:
                search_result = gn.search(full_query, from_=valid_from, to_=valid_to)
            except Exception as e:
                raise NewsFetchingError(f"The underlying news library failed on search: {e}")
        else:
            try:
                search_result = gn.top_news()
            except Exception as e:
                raise NewsFetchingError(f"The underlying news library failed on top_news: {e}")

        if not search_result:
             raise NewsFetchingError("News service did not return a result.")

        entries = search_result.get('entries', [])

        # Paginate the results
        paginated_entries = search_result.entries[start : start + num_results]

        article_list = []
        for entry in paginated_entries:
            description = clean_html(entry.get('summary', ''))
            article = {
                "title": entry.get('title'),
                "url": entry.get('link'),
                "source": entry.get('source', {}).get('title'),
                "published": entry.get('published'),
                "description": description,
                "image": None,  # Image URLs are not provided by this library.
                "category": category if q else "top",
            }
            if include_sentiment:
                sentiment_text = f"{article['title']}. {description}"
                article['sentiment'] = sia.polarity_scores(sentiment_text)
            article_list.append(article)

        return {"articles": article_list}

    except Exception as e:
        raise NewsFetchingError(f"Error fetching news results: {e}")
