
import asyncio
import json
from pathlib import Path

from loguru import logger
from rnet import BlockingClient, Client, Impersonate
from tenacity import before_log, retry, stop_after_attempt, wait_exponential


class Extractor:
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.session = Client(impersonate=Impersonate.Chrome137)
        self.blocking_session = BlockingClient(impersonate=Impersonate.Chrome137)
        logger.info("Extractor initialized with rnet Client.")


    def fetch_local_json(self, file_path: str) -> dict:
        try:
            with Path.open(self.data_path / file_path) as f:
                data = json.load(f)
                logger.info(f"Loaded JSON data from {file_path}")
                return data
        except FileNotFoundError as e:
            logger.error(f"JSON file not found: {e}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return {}

    @retry(
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before=before_log(logger=logger, log_level="WARNING"),
    )
    def fetch_json(self, url: str) -> dict:
        logger.info(f"Fetching JSON data from {url}")
        response = self.blocking_session.get(url)
        if response.status != 200:
            logger.error(f"Failed to fetch JSON data from {url}")
            msg = f"HTTP {response.status}"
            raise Exception(msg)
        return response.json()

    async def fetch_json_async(self, url: str) -> dict:
        logger.info(f"(Async) Fetching JSON data from {url}")
        response = await self.session.get(url)
        response.raise_for_status()
        return await response.json()

    async def fetch_all_json(self, urls: list[str]) -> list[dict]:
        tasks = [self.fetch_json_async(url) for url in urls]
        return await asyncio.gather(*tasks)
