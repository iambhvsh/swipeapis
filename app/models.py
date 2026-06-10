from pydantic import BaseModel, Field
from typing import List, Optional, Set


class SearchResult(BaseModel):
    title: str = ""
    url: str = ""
    description: str = ""
    source: str = ""
    provider: str = ""
    frequency: int = 1
    original_rank: int = 1
    providers: List[str] = Field(default_factory=list)
    score: float = 0.0
    rank: int = 0
    published_date: Optional[str] = None

    def model_dump_filtered(self, fields: Set[str]) -> dict:
        return {k: v for k, v in self.model_dump().items() if k in fields}
