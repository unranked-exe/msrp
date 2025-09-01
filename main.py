import asyncio
import json
import os
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
from pydantic import BaseModel
from rnet import Client, Impersonate

data_path = Path("data_store")
datasheet_csv = data_path / "datasheet.csv"

# FOR SCRAPING Manufacturer Website
# Check for required environment variables
try:
    PRODUCT_API_URL = os.environ.get("PRODUCT_API_URL")
    SEARCH_QUERY_BASE_URL = os.environ.get("SEARCH_QUERY_BASE_URL")

except KeyError as e:
    raise ValueError(f"Missing environment variable: {e}")


#DATA MODEL FOR SHOES (TRANSFORM)
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

#EXTRACTOR
def prepare_query() -> str:
    # Prepare the search query
    params = {
        "multi_age_gender": "men",
        "v_size_en_gb": "10",
    }
    return f"{SEARCH_QUERY_BASE_URL}&{urlencode(params)}"

def get_datasheet(data_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(data_path)
    except pd.errors.EmptyDataError as e:
        print(f"Datasheet is empty: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except Exception as e:
        print(f"Error reading datasheet: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

#TRANSFORM
def get_json(data_path: Path) -> dict:
    try:
        with Path.open(data_path / "search_res.json") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(f"JSON file not found: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}

#EXTRACTOR
def create_client() -> Client:
    return Client(impersonate=Impersonate.Chrome137)

#MIX OF EXTRACTOR AND TRANSFORM
async def search_api(client: Client) -> None:
    # THIS IS TO PREVENT EXCESS QUERIES BEING SENT TO API SO SAVED JSON LOCALLY ON FILE
    #response = await client.get(SEARCH_QUERY_URL)
    #print(response.status_code)
    #print(response.json())
    json_res = get_json(data_path)
    print(json_res)
    #TRANSFORM
    print(json_res["raw"]["itemList"])
    return SearchResults(**json_res["raw"]["itemList"])

async def product_api(client: Client, search_item: SearchItem) -> None:
    url = f"{PRODUCT_API_URL}{search_item.productId}"
    response = await client.get(url)
    print(response.status_code)
    print(response.json())


# TO REDO AND REDESIGN WITH NEW PROJECT IDEA
async def main() -> None:
    #datasheet_df = get_datasheet(datasheet_csv)
    # Process the DataFrame
    # print(datasheet_df.head())

    # print(datasheet_df["Cat Description"].value_counts())

    # print(datasheet_df.isna().sum())

    # print(datasheet_df.duplicated().sum())
    # print(datasheet_df[datasheet_df[["STYLE Description","GBP G - MSRP"]].duplicated()])

    client = create_client()
    search_results = await search_api(client)
    product_api(client, search_results.items[0])


if __name__ == "__main__":
    #run this for testing
    #await main()
    print(PRODUCT_API_URL)
    print(prepare_query())
    asyncio.run(main())
    print(PRODUCT_API_URL)
