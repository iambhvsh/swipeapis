from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routes.finance import router as finance_router
from app.routes.search import router as search_router
from app.routes.news import router as news_router
from app.middleware.limits import limiter

app = FastAPI(
    title="Atlas",
    description="A modern self-hosted API infrastructure toolkit.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
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

app.include_router(finance_router, prefix="/finance", tags=["Finance"])
app.include_router(search_router, prefix="/search", tags=["Search"])
app.include_router(news_router, prefix="/news", tags=["News"])

@app.get("/", response_class=JSONResponse, tags=["Root"])
@limiter.limit("100/minute")
async def read_root(request: Request):
    return {
        "name": "Atlas",
        "description": "A modern self-hosted API infrastructure toolkit.",
        "version": "1.0.0"
    }
