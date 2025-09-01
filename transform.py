from pydantic import BaseModel


class SearchItem(BaseModel):
    productId: str  # noqa: N815
    displayName: str  # noqa: N815
    division: str
    price: float

class SearchResults(BaseModel):
    count: int
    startIndex: int  # noqa: N815
    searchTerm: str  # noqa: N815
    items: list[SearchItem]

class Transform:
    @staticmethod
    def search_results(data: dict) -> SearchResults:
        return SearchResults(**data)
