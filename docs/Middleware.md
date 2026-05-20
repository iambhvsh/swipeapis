# Middleware

Atlas incorporates lightweight middleware designed to protect the infrastructure while remaining stateless.

## Rate Limiting

Rate limiting is enforced globally using `slowapi` (`app/middleware/limits.py`).
- Routes are restricted on a per-IP basis.
- Standard limits are applied at the route level (e.g., `60/minute`).
- Triggers a standard `429 Too Many Requests` when exceeded.

## CORS

Atlas applies a strict, stateless CORS policy via FastAPI's `CORSMiddleware`:
- `allow_origins=["*"]`: Open access for public querying.
- `allow_credentials=False`: Enforces a stateless architecture with no cookies or sessions allowed.

## Graceful Degradation

If underlying providers fail, HTTP routes are instructed to catch standard internal `SearchError` or `FinanceServiceError` exceptions and downgrade them to a generic `503 Service Unavailable`, without leaking internal stack traces.
