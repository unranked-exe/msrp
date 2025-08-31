import asyncio
import os
from pathlib import Path

import pandas as pd
from pydantic import BaseModel
from rnet import Client, Impersonate

data_path = Path("data_store")
datasheet_csv = data_path / "datasheet.csv"

# FOR SCRAPING Manufacturer Website
# Check for required environment variables
try:
    PRODUCT_API_URL = os.environ.get("PRODUCT_API_URL")
    SEARCH_QUERY_URL = os.environ.get("SEARCH_QUERY_URL")

except KeyError as e:
    raise ValueError(f"Missing environment variable: {e}")


#DATA MODEL FOR SHOES
class Product(BaseModel):
    sku: str
    name: str
    price: float
    image_url: str
    product_url: str

class SearchResults(BaseModel):
    products: list[Product]
    count: int
    page: int
    page_size: int


def get_datasheet(data_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(data_path)
    except pd.errors.EmptyDataError as e:
        print(f"Datasheet is empty: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except Exception as e:
        print(f"Error reading datasheet: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def create_client() -> Client:
    return Client(impersonate=Impersonate.Chrome137)


# TO REDO AND REDESIGN WITH NEW PROJECT IDEA
def main() -> None:
    datasheet_df = get_datasheet(datasheet_csv)
    # Process the DataFrame
    # print(datasheet_df.head())

    # print(datasheet_df["Cat Description"].value_counts())

    # print(datasheet_df.isna().sum())

    # print(datasheet_df.duplicated().sum())
    # print(datasheet_df[datasheet_df[["STYLE Description","GBP G - MSRP"]].duplicated()])



if __name__ == "__main__":
    main()
