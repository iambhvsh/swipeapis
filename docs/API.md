# API Reference

Atlas exposes a single, straightforward search endpoint.

## The Search Endpoint

`GET /search`

Executes a federated search across all active providers, deduplicates the results, ranks them according to configured heuristics, and returns a paginated JSON response.

### Query Parameters

| Parameter | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `q` | string | Yes | None | The search query string. Cannot be empty. |
| `num_results` | integer | No | 10 | The maximum number of results to return. Minimum is 1, maximum is 100. |
| `start` | integer | No | 0 | The starting index of the results. Used for pagination. |
| `language` | string | No | "en" | The language code to use for the search. Supports en, es, fr, de, ja, zh, ru, pt, it. |
| `safe` | boolean | No | True | Enables or disables SafeSearch upstream. |
| `include_rank` | boolean | No | False | Includes the absolute rank index when the `rank` field is selected. |
| `fields` | string | No | None | Comma separated list of fields to return. Overrides default fields. Available fields: url, title, description, source, rank, provider, providers, score, published_date. |

### Responses

#### 200 OK

Returns the structured search results.

```json
{
  "total_count": 1,
  "results": [
    {
      "url": "https://en.wikipedia.org/wiki/Atlas",
      "title": "Atlas",
      "description": "An atlas is a collection of maps...",
      "source": "en.wikipedia.org"
    }
  ]
}
```

#### 400 Bad Request

Returned when the query is empty or invalid fields are requested.

```json
{
  "detail": "Search query cannot be empty."
}
```

#### 429 Too Many Requests

Returned when the rate limit of 30 requests per minute is exceeded.

#### 503 Service Unavailable

Returned when all upstream search providers completely fail or time out.

```json
{
  "detail": "All search providers failed to return results."
}
```
