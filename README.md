# 🚀 Swipe APIs

Welcome to Swipe APIs - your comprehensive solution for financial data, web search, and news aggregation. Built for developers who demand reliability, speed, and comprehensive data coverage.

[![API Status](https://img.shields.io/badge/status-production-brightgreen)](https://swipeapis.vercel.app)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://swipeapis.vercel.app)
[![Uptime](https://img.shields.io/badge/uptime-99.9%25-brightgreen)](https://swipeapis.vercel.app)

## 🎯 Overview

Swipe APIs provides three powerful endpoints designed for production use:

- **📈 Finance API** - Real-time stock data, historical prices, and market analytics
- **🔍 Search API** - Google-powered search with customizable parameters
- **📰 News API** - Global news aggregation with sentiment analysis

### Base URL
```
https://swipeapis.vercel.app
```

### Authentication
No authentication required - all endpoints are publicly accessible.

---

## 📈 Finance API

Comprehensive financial data provider supporting thousands of global stock symbols.

### Endpoint
```http
GET /finance/{ticker}
```

### Features
- ✅ Real-time stock prices and market data
- ✅ Historical price data with flexible intervals
- ✅ Market capitalization and trading volumes
- ✅ Analyst recommendations and ratings
- ✅ Corporate fundamentals and key metrics

### Path Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `ticker` | string | ✅ **Yes** | Stock ticker symbol | `AAPL`, `TSLA`, `GOOGL` |

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fields` | string | All fields | Comma-separated list of specific fields to return |
| `history_days` | integer | `0` | Number of days of historical data. Deprecated if `start_date` is used. |
| `start_date` | string | - | Start date for historical data (YYYY-MM-DD). Overrides `history_days`. |
| `end_date` | string | - | End date for historical data (YYYY-MM-DD). Defaults to today. |
| `interval` | string | `1d` | Data interval: `1m`, `5m`, `15m`, `30m`, `1h`, `1d`, `1wk`, `1mo` |
| `include_recommendations` | boolean | `false` | Include analyst recommendations and price targets |
| `adjusted` | boolean | `true` | Return dividend/split adjusted prices |

### Available Fields
- `price` - Current stock price
- `market_cap` - Market capitalization
- `volume` - Trading volume
- `pe_ratio` - Price-to-earnings ratio
- `dividend_yield` - Annual dividend yield
- `52_week_high` - 52-week high price
- `52_week_low` - 52-week low price
- `beta` - Stock volatility measure
- `pb_ratio` - Price-to-book ratio
- `forward_pe` - Forward price-to-earnings ratio
- `enterprise_value` - Enterprise value
- `payout_ratio` - Payout ratio
- `average_volume` - Average trading volume
- `open` - Market opening price
- `previous_close` - Previous day's closing price

### Example Requests

**Basic stock quote:**
```bash
curl "https://swipeapis.vercel.app/finance/AAPL"
```

**Specific fields with historical data:**
```bash
curl "https://swipeapis.vercel.app/finance/TSLA?fields=price,market_cap,volume&history_days=30&interval=1d"
```

**With analyst recommendations:**
```bash
curl "https://swipeapis.vercel.app/finance/MSFT?include_recommendations=true"
```

**With a specific date range:**
```bash
curl "https://swipeapis.vercel.app/finance/NVDA?start_date=2024-08-01&end_date=2024-08-20"
```

### Response Example
```json
{
  "ticker": "MSFT",
  "price": 507.23,
  "market_cap": 3770326974464,
  "pe_ratio": 37.18695,
  "52_week_high": 555.45,
  "52_week_low": 344.79,
  "recommendations": [
    {
      "date": "2024-05-13",
      "firm": "Morgan Stanley",
      "to_grade": "Overweight",
      "from_grade": "",
      "action": "main"
    },
    {
      "date": "2024-05-10",
      "firm": "Barclays",
      "to_grade": "Overweight",
      "from_grade": "",
      "action": "main"
    }
  ]
}
```

> **Note**: The `recommendations` field is only returned when `include_recommendations=true`. The bug causing an error in this field was fixed on August 24, 2025.

---

## 🔍 Search API

Google-powered search engine with advanced filtering and pagination capabilities.

### Endpoint
```http
GET /search/
```

### Features
- ✅ Google search results with high relevancy
- ✅ Advanced filtering and pagination
- ✅ Multi-language support (50+ languages)
- ✅ SafeSearch controls
- ✅ Customizable result fields

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | - | **Required.** Search query string |
| `num_results` | integer | `10` | Maximum results to return (1-100) |
| `start` | integer | `0` | Starting index for pagination |
| `language` | string | `en` | Language code (ISO 639-1) |
| `safe` | boolean | `true` | Enable Google SafeSearch filtering |
| `include_rank` | boolean | `false` | Include search result ranking |
| `fields` | string | All fields | Comma-separated field selection |

### Available Fields
- `url` - Result webpage URL
- `title` - Page title
- `description` - Meta description or snippet
- `source` - Domain source
- `rank` - Search result position
- `date` - Last modified date (when available)

### Language Codes
| Code | Language | Code | Language | Code | Language |
|------|----------|------|----------|------|----------|
| `en` | English | `es` | Spanish | `fr` | French |
| `de` | German | `ja` | Japanese | `zh` | Chinese |
| `ru` | Russian | `pt` | Portuguese | `it` | Italian |

### Example Requests

**Basic search:**
```bash
curl "https://swipeapis.vercel.app/search/?q=machine+learning+tutorials"
```

**Paginated results:**
```bash
curl "https://swipeapis.vercel.app/search/?q=Python+FastAPI&num_results=20&start=10"
```

**Specific fields in Spanish:**
```bash
curl "https://swipeapis.vercel.app/search/?q=inteligencia+artificial&fields=url,title&language=es"
```

### Response Example
```json
{
  "query": "machine learning tutorials",
  "total_results": 1000000,
  "results": [
    {
      "rank": 1,
      "url": "https://example.com/ml-tutorial",
      "title": "Complete Machine Learning Tutorial for Beginners",
      "description": "Learn machine learning from scratch with practical examples...",
      "source": "example.com"
    }
  ],
  "pagination": {
    "current_page": 1,
    "results_per_page": 10,
    "has_next": true
  }
}
```

---

## 📰 News API

Global news aggregation with advanced filtering and sentiment analysis capabilities.

### Endpoint
```http
GET /news/
```

### Features
- ✅ Global news from 50,000+ sources
- ✅ Real-time top headlines
- ✅ Advanced search and filtering
- ✅ Sentiment analysis powered by AI
- ✅ Multi-language and regional support
- ✅ Category-based filtering

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | - | Search query for specific topics (optional) |
| `num_results` | integer | `10` | Number of articles to return (1-100) |
| `start` | integer | `0` | Starting index for pagination |
| `from_date` | string | - | Start date filter (YYYY-MM-DD) |
| `to_date` | string | - | End date filter (YYYY-MM-DD) |
| `language` | string | `en` | Article language (ISO 639-1) |
| `region` | string | `US` | Geographic region for news |
| `category` | string | - | News category filter |
| `include_sentiment` | boolean | `false` | Enable AI sentiment analysis |

### Supported Categories
- `business` - Business and finance news
- `technology` - Tech industry updates
- `science` - Scientific discoveries and research
- `health` - Health and medical news
- `sports` - Sports news and updates
- `entertainment` - Entertainment and celebrity news
- `politics` - Political news and analysis

### Supported Regions
| Code | Region | Code | Region | Code | Region |
|------|---------|------|---------|------|---------|
| `US` | United States | `GB` | United Kingdom | `CA` | Canada |
| `AU` | Australia | `IN` | India | `DE` | Germany |
| `FR` | France | `JP` | Japan | `BR` | Brazil |

### Example Requests

**Top headlines:**
```bash
curl "https://swipeapis.vercel.app/news/"
```

**Technology news with sentiment:**
```bash
curl "https://swipeapis.vercel.app/news/?category=technology&include_sentiment=true&num_results=15"
```

**Search with date range:**
```bash
curl "https://swipeapis.vercel.app/news/?q=artificial+intelligence&from_date=2025-08-01&to_date=2025-08-24"
```

**Regional news in specific language:**
```bash
curl "https://swipeapis.vercel.app/news/?region=DE&language=de&category=business"
```

### Response Example
```json
{
  "query": "artificial intelligence",
  "total_articles": 15420,
  "articles": [
    {
      "title": "AI Revolution in Healthcare: New Breakthrough in Diagnosis",
      "description": "Researchers announce major advancement in AI-powered medical diagnosis...",
      "url": "https://example.com/ai-healthcare",
      "source": "Tech News Daily",
      "published_at": "2025-08-24T14:30:00Z",
      "author": "Dr. Sarah Johnson",
      "category": "technology",
      "region": "US",
      "language": "en",
      "sentiment": {
        "score": 0.85,
        "label": "positive",
        "confidence": 0.92
      }
    }
  ],
  "metadata": {
    "generated_at": "2025-08-24T15:00:00Z",
    "processing_time_ms": 245
  }
}
```

---

## 📊 Usage & Access

### Current Access
- **Public API**: No authentication required
- **No rate limits**: Use responsibly for fair access
- **Production ready**: Built for high availability

---

## 🔒 Error Handling

All endpoints return standardized error responses:

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_TICKER",
    "message": "The provided ticker symbol is invalid or not found",
    "details": "Ticker 'INVALID' not found in our database",
    "timestamp": "2025-08-24T15:00:00Z"
  }
}
```

### Common Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_TICKER` | 400 | Invalid or unknown stock ticker |
| `MISSING_QUERY` | 400 | Required query parameter missing |
| `RATE_LIMIT_EXCEEDED` | 429 | Service temporarily unavailable |
| `INTERNAL_ERROR` | 500 | Server processing error |

---

## 🛠️ SDKs & Libraries

### Python
```python
import requests

# Finance API
response = requests.get('https://swipeapis.vercel.app/finance/AAPL')
data = response.json()

# Search API
response = requests.get('https://swipeapis.vercel.app/search/', 
                       params={'q': 'Python tutorials'})
results = response.json()

# News API
response = requests.get('https://swipeapis.vercel.app/news/', 
                       params={'category': 'technology'})
articles = response.json()
```

### JavaScript/Node.js
```javascript
// Using fetch API
const getStockData = async (ticker) => {
  const response = await fetch(`https://swipeapis.vercel.app/finance/${ticker}`);
  return response.json();
};

const searchWeb = async (query) => {
  const response = await fetch(`https://swipeapis.vercel.app/search/?q=${query}`);
  return response.json();
};

const getNews = async (category) => {
  const response = await fetch(`https://swipeapis.vercel.app/news/?category=${category}`);
  return response.json();
};
```

### cURL Examples
```bash
# Get stock quote
curl -H "Accept: application/json" \
     "https://swipeapis.vercel.app/finance/AAPL"

# Search the web
curl -H "Accept: application/json" \
     "https://swipeapis.vercel.app/search/?q=machine+learning"

# Get tech news
curl -H "Accept: application/json" \
     "https://swipeapis.vercel.app/news/?category=technology"
```

---

## 🚀 Getting Started

1. **Choose your endpoint** based on your needs
2. **Review the parameters** and response formats
3. **Make your first request** using cURL or your preferred HTTP client
4. **Implement error handling** for robust applications
5. **Use responsibly** to ensure fair access for everyone

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/swipeapis/issues)
- **Mail**: [iambhvshh@outlook.com](mailto:iambhvshh@outlook.com)

---

*Built with ❤️ by [iambhvsh](https://iambhvsh.vercel.app)*
