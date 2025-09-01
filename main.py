import asyncio
import os
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
from extract import Extractor
from loguru import logger
from transform import SearchResults, Transform

data_path = Path("data_store")
datasheet_csv = data_path / "datasheet.csv"

# FOR SCRAPING Manufacturer Website
# Check for required environment variables
try:
    PRODUCT_API_URL = os.environ.get("PRODUCT_API_URL")
    SEARCH_QUERY_BASE_URL = os.environ.get("SEARCH_QUERY_BASE_URL")

except KeyError as e:
    raise ValueError(f"Missing environment variable: {e}")

e = Extractor(data_path)
t = Transform()

#DATA MODEL FOR SHOES (TRANSFORM)


#EXTRACTOR
def prepare_query() -> str:
    # Prepare the search query
    params = {
        "multi_age_gender": "men",
        "v_size_en_gb": "10",
    }
    return f"{SEARCH_QUERY_BASE_URL}&{urlencode(params)}"

def test_url() -> str:
    return f"{SEARCH_QUERY_BASE_URL}/p"
# def get_datasheet(data_path: Path) -> pd.DataFrame:
#     try:
#         return pd.read_csv(data_path)
#     except pd.errors.EmptyDataError as e:
#         print(f"Datasheet is empty: {e}")
#         return pd.DataFrame()  # Return an empty DataFrame on error
#     except Exception as e:
#         print(f"Error reading datasheet: {e}")
#         return pd.DataFrame()  # Return an empty DataFrame on error

#MIX OF EXTRACTOR AND TRANSFORM
def search_api() -> SearchResults:
    # THIS IS TO PREVENT EXCESS QUERIES BEING SENT TO API SO SAVED JSON LOCALLY ON FILE
    #response = await client.get(SEARCH_QUERY_URL)
    #print(response.status_code)
    #print(response.json())
    #json_res = get_json(data_path)
    #print(json_res)
    #DEVELOPMENT
    logger.info("Fetching local JSON")
    json_res = e.fetch_local_json("search_res.json") #TESTS IF LOCAL FILE CONTAINING SEARCH_API RES CAN BE READ FROM EXTRACTOR CLASS

    #json_real_res = e.fetch_json(test_url()) #FETches testurl
    results = t.search_results(json_res["raw"]["itemList"])
    logger.info(f"Transformed {results.count} items from search results.")
    logger.info(type(results))
    return results

# TO REDO AND REDESIGN WITH NEW PROJECT IDEA
async def main() -> None:

    logger.info(search_api())
    #product_api(client, search_results.items[0])


if __name__ == "__main__":
    #run this for testing
    #await main()
    print(test_url())
    print(PRODUCT_API_URL)
    print(prepare_query())
    asyncio.run(main())
    # print(PRODUCT_API_URL)
