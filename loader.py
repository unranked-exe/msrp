from pathlib import Path

import pandas as pd
from loguru import logger


class Load:
    def __init__(self, res_dir: Path) -> None:
        self.res_dir = res_dir
        self.setup_results_folder()

    def setup_results_folder(self) -> None:
        try:
            Path.mkdir(self.res_dir)
            logger.info(f"Directory '{self.res_dir}' created successfully.")

        except FileExistsError:
            logger.info(f"Directory '{self.res_dir}' already exists.")

    def load_into_parquet(self, df: pd.DataFrame, table_name: str) -> None:
        """Load a DataFrame into a Parquet file."""
        try:
            df.to_parquet(self.res_dir / f"{table_name}.parquet")
            logger.info(f"DataFrame loaded into {self.res_dir / f'{table_name}.parquet'}")
        except Exception as e:
            logger.error(f"Error loading DataFrame into Parquet: {e}")
