import asyncio
import os
from pathlib import Path
from urllib.parse import urlencode

from extract import Extractor
from loader import Load
from loguru import logger
from transform import Transform
import time

data_path = Path("data_store")
results_path = data_path / "results"
datasheet_csv = data_path / "datasheet.csv"

# FOR SCRAPING Manufacturer Website
# Check for required environment variables
try:
    PRODUCT_API_URL = os.environ.get("PRODUCT_API_URL")
    SEARCH_QUERY_BASE_URL = os.environ.get("SEARCH_QUERY_BASE_URL")

except KeyError as e:
    raise ValueError(f"Missing environment variable: {e}")

e = Extractor(data_path)
l = Load(results_path)  # noqa: E741
t = Transform()

# EXTRACTOR
def prepare_query() -> str:
    # Prepare the search query
    params = {
        "multi_age_gender": "men",
        "v_size_en_gb": "10",
    }
    return f"{SEARCH_QUERY_BASE_URL}&{urlencode(params)}"


def test_url() -> str:
    return f"{SEARCH_QUERY_BASE_URL}"

# MIX OF EXTRACTOR AND TRANSFORM
def search_api() -> dict:
    """Fetches JSON response from search API
    \nAdds time of request to the dict
    Returns:
    essential items from the JSON response
    """
    # THIS IS TO PREVENT EXCESS QUERIES BEING SENT TO API SO SAVED JSON LOCALLY ON FILE
    # response = await client.get(SEARCH_QUERY_URL)
    # print(response.status_code)
    # print(response.json())
    # json_res = get_json(data_path)
    # print(json_res)
    # DEVELOPMENT
    logger.info("Fetching local JSON")
    json_res = e.fetch_local_json(
        "search_res.json"
    )  # TESTS IF LOCAL FILE CONTAINING SEARCH_API RES CAN BE READ FROM EXTRACTOR CLASS

    filt_resp = json_res["raw"]["itemList"]
    # Adds timestamp to the dict
    filt_resp["time_of_request"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return filt_resp

#def items_api():

def insert_search_res_into_db(resp: dict) -> None | int:

    obj = l.insert_into_db("search_results", {
        "search_term": resp["searchTerm"],
        "start_index": resp["startIndex"],
        "count": resp["count"],
        "time_of_request": resp["time_of_request"]
    })
    logger.info(f"Inserted search result with ID: {obj.inserted_primary_key[0]}")
    return obj.inserted_primary_key[0]


def insert_products_into_db(items: list[dict], search_res_fk: int) -> None :
    obj = l.insert_into_db("products", [
        {
            "product_id": item["productId"],
            "display_name": item["displayName"],
            "division": item["division"],
            "price": item["price"],
            "sale_price": item.get("salePrice"),  # Use .get() to handle missing salePrice
            "search_result_id": search_res_fk
        }
        for item in items
    ])
    logger.info(f"Inserted {obj.rowcount} products into the database.")

# TO REDO AND REDESIGN WITH NEW PROJECT IDEA
async def main() -> None:

    res = search_api()
    search_res_fk = insert_search_res_into_db(res)
    items = res['items']
    logger.info(f"Processing {len(items)} items.")
    insert_products_into_db(items, search_res_fk)

if __name__ == "__main__":
    # run this for testing
    # await main()
    print(test_url())
    print(PRODUCT_API_URL)
    print(prepare_query())
    asyncio.run(main())
    # print(PRODUCT_API_URL)
