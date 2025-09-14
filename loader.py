from pathlib import Path

import pandas as pd
from loguru import logger
from sqlalchemy import create_engine


class Load:
    """Class to handle loading DataFrames into Parquet files and Databases."""

    def __init__(self, res_dir: Path) -> None:
        self.res_dir = res_dir
        self.setup_results_folder()
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/msrp_testing")

    def setup_results_folder(self) -> None:
        """Create results directory if it doesn't exist."""
        Path.mkdir(self.res_dir, exist_ok=True)
        logger.info(f"Directory '{self.res_dir}' created successfully.")

    def load_into_parquet(self, df: pd.DataFrame, table_name: str) -> None:
        """Load a DataFrame into a Parquet file."""
        try:
            df.to_parquet(self.res_dir / f"{table_name}.parquet")
            logger.info(
                f"DataFrame loaded into {self.res_dir / f'{table_name}.parquet'}"
            )
        except Exception as e:
            logger.error(f"Error loading DataFrame into Parquet: {e}")
    
    def save_to_db(self, df: pd.DataFrame, table_name: str) -> None:
        """Save a DataFrame to a PostgreSQL database."""
        try:
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
            logger.info(f"DataFrame saved to table '{table_name}' in the database.")
        except Exception as e:
            logger.error(f"Error saving DataFrame to database: {e}")
