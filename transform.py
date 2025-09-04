import time

import pandas as pd
from pydantic import BaseModel


class SearchItem(BaseModel):
    """Data model for individual search items."""

    productId: str  # noqa: N815
    displayName: str  # noqa: N815
    division: str
    price: float
    salePrice: float  # noqa: N815

class SearchResults(BaseModel):
    """Data model for search results."""

    count: int
    startIndex: int  # noqa: N815
    searchTerm: str  # noqa: N815
    items: list[SearchItem]
    time_of_request: str

class Transform:
    @staticmethod
    def search_results(data: dict) -> SearchResults:
        """Transform search results data into a SearchResults model."""
        data["time_of_request"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        return SearchResults(**data)

    @staticmethod
    def create_df(data: list[dict], columns: list) -> pd.DataFrame:
        return pd.DataFrame(data, columns=columns)


    @staticmethod
    def append_to_df(df: pd.DataFrame, data: dict[str, any]) -> pd.DataFrame:
        print(data)
        return pd.concat([df, pd.DataFrame([data])], ignore_index=True)
