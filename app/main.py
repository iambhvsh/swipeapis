from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routes.search import router as search_router
from app.middleware.limits import limiter

app = FastAPI(
    title="Atlas",
    description="A stateless, privacy-focused search engine API.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix="/search", tags=["Search"])


@app.get("/", response_class=JSONResponse, tags=["Root"])
@limiter.limit("100/minute")
async def read_root(request: Request):
    return {
        "name": "Atlas",
        "description": "A stateless, privacy-focused search engine API.",
        "version": "1.0.0",
        "endpoints": {
            "search": {
                "path": "/search",
                "method": "GET",
                "parameters": {
                    "q": "string (required) - The search query",
                    "num_results": "integer - Max results to return (default 10)",
                    "start": "integer - Pagination offset (default 0)",
                    "language": "string - Language code, e.g. 'en', 'es' (default 'en')",
                    "safe": "boolean - Enable SafeSearch (default true)",
                    "include_rank": "boolean - Set to true to include the search result rank (default false)",
                    "fields": "string - Comma-separated list of fields to return (e.g. 'title,summary') (default all)",
                },
            }
        },
    }
