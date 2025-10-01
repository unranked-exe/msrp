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

# class SQLAttributes(BaseModel):
#     """Data model for a sql attributes."""
#     name: str
#     data_type: str
#     primary_key: None | str
#     is_nullable: None | str
#     unique: None | str
#     foreign_key: None | str

# class SearchItemTable(BaseModel):
#     """Data model for individual search items."""

#     productId: SQLAttributes  # noqa: N815
#     displayName: SQLAttributes  # noqa: N815
#     division: SQLAttributes
#     price: SQLAttributes
#     salePrice: SQLAttributes  # noqa: N815

# def create_models():
#     product_id = SQLAttributes(
#         name="product_id",
#         data_type="VARCHAR(9)",
#         primary_key="PRIMARY KEY",
#     )
#     display_name = SQLAttributes(
#         name="display_name",
#         data_type="VARCHAR(255)",
#     )
#     division = SQLAttributes(
#         name="division",
#         data_type="VARCHAR(100)",
#     )
#     price = SQLAttributes(
#         name="price",
#         data_type="FLOAT",
#     )
#     sale_price = SQLAttributes(
#         name="sale_price",
#         data_type="FLOAT",
#         is_nullable="NULL"
#     )

#     search_item_table = SearchItemTable(
#         productId=product_id,
#         displayName=display_name,
#         division=division,
#         price=price,
#         salePrice=sale_price,
#     )
#     return search_item_table


# table = create_models()
# # Tables to create in the database
# dict_of__staging_tables = {
#     "search_results": """id SERIAL PRIMARY KEY,
#                       searchTerm VARCHAR(255),
#                       startIndex INTEGER,
#                       time_of_request TIMESTAMP""",
#     "products": f"""{table.productId.name} {table.productId.data_type} {table.productId.primary_key},
#                    {table.displayName.name} {table.displayName.data_type} {table.displayName.primary_key},
#                    {table.division.name} {table.division.data_type} {table.division.primary_key},
#                    {table.price.name} {table.price.data_type} {table.price.primary_key},
#                    {table.salePrice.name} {table.salePrice.data_type} {table.salePrice.primary_key}""",
# }
    
#    """INSERT INTO dev.products (product_id, display_name, division, price, sale_price)
 #        VALUES ({}, {}, {}, {}, {})




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


# def get_datasheet(data_path: Path) -> pd.DataFrame:
#     try:
#         return pd.read_csv(data_path)
#     except pd.errors.EmptyDataError as e:
#         print(f"Datasheet is empty: {e}")
#         return pd.DataFrame()  # Return an empty DataFrame on error
#     except Exception as e:
#         print(f"Error reading datasheet: {e}")
#         return pd.DataFrame()  # Return an empty DataFrame on error


# MIX OF EXTRACTOR AND TRANSFORM
def search_api() -> dict:
    """Fetches JSON response from search API
    \nADDS time of request to the dict"""
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

    essential_items = json_res["raw"]["itemList"]
    # Adds timestamp to the dict
    essential_items["time_of_request"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return essential_items
    # json_real_res = e.fetch_json(test_url()) #FETches testurl
    #results = t.search_results(essential_items)



    # results.time_of_request = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    #logger.info(f"Transformed {results.count} items from search results.")
    #logger.info(type(results))
    #return results

#def items_api():

def insert_search_res_into_db(essential_items: dict) -> None | int:

    obj = l.insert_into_db("search_results", {
        "search_term": essential_items["searchTerm"],
        "start_index": essential_items["startIndex"],
        "count": essential_items["count"],
        "time_of_request": essential_items["time_of_request"]
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

# TO REDO AND REDESIGN WITH NEW PROJECT IDEA
async def main() -> None:
    
    # CREATE TABLES IN THE DATABASE
    # for table_name, attributes in dict_of__staging_tables.items():
    #     l.create_raw_table(table_name, attributes)

    res = search_api()
    print(res['searchTerm'], res['count'], res['startIndex'], res['time_of_request'])
    search_res_fk = insert_search_res_into_db(res)
    logger.info("Search results inserted into database.")
    items = res['items']
    logger.info(f"Processing {len(items)} items.")
    insert_products_into_db(items, search_res_fk)
    logger.info("Products inserted into database.")



    # logger.info("Attempting to convert search results to DataFrame")
    # search_results: dict[str, any] = dict(res)
    # search_items: list[SearchItem] = search_results.pop("items")

    # logger.info(f"Extracted {len(search_items)} search items.")

    # search_res_df = t.create_df([search_results], search_results.keys())
    # l.load_into_parquet(search_res_df, "search_results")

    # print(search_res_df)

    # search_items: list[dict[str, any]] = [dict(item) for item in search_items]
    # logger.info(type(search_items))
    # logger.info(search_items[0])
    # products_df = t.create_df(search_items, SearchItem.model_fields.keys())
    # print(products_df)
    # l.load_into_parquet(products_df, "products")
    # #l.save_to_db(products_df, "products")
    # logger.info("DataFrames loaded complete")
    # l.create_table("products")
    # logger.info("Table creation attempted")


if __name__ == "__main__":
    # run this for testing
    # await main()
    print(test_url())
    print(PRODUCT_API_URL)
    print(prepare_query())
    asyncio.run(main())
    # print(PRODUCT_API_URL)
