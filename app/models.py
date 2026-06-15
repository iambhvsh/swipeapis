from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field


SearchField = Literal[
    "url",
    "title",
    "description",
    "source",
    "rank",
    "provider",
    "providers",
    "score",
    "published_date",
]


class RawSearchResult(TypedDict, total=False):
    title: str
    url: str
    description: str
    source: str
    provider: str
    published_date: str | None


class SearchResult(BaseModel):
    title: str = ""
    url: str = ""
    description: str = ""
    source: str = ""
    provider: str = ""
    frequency: int = 1
    original_rank: int = 1
    providers: list[str] = Field(default_factory=list)
    score: float = 0.0
    rank: int = 0
    published_date: str | None = None

    def model_dump_filtered(self, fields: set[SearchField]) -> dict[str, Any]:
        return {k: v for k, v in self.model_dump().items() if k in fields}


class SearchResponse(BaseModel):
    total_count: int
    results: list[dict[str, Any]]
