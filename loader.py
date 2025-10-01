from pathlib import Path

import pandas as pd
from loguru import logger
from sqlalchemy import Table, Column, ForeignKey, Integer, Float, String, DateTime, create_engine, MetaData, Insert

class Load:
    """Class to handle loading DataFrames into Parquet files and Databases."""

    def __init__(self, res_dir: Path) -> None:
        self.res_dir = res_dir
        self.setup_results_folder()
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@db:5432/msrp_testing")
        # self.conn = self.connect_to_db()
        self.metadata = MetaData()
        self.dict_of__staging_tables = {}
        self.setup_tables()
        self.metadata.create_all(self.engine)
        logger.info("Database tables created successfully.")
        
        

    def setup_results_folder(self) -> None:
        """Create results directory if it doesn't exist."""
        Path.mkdir(self.res_dir, exist_ok=True)
        logger.info(f"Directory '{self.res_dir}' created successfully.")

    def setup_tables(self) -> None:
        search_results = Table(
            'search_results',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('search_term', String),
            Column('start_index', Integer),
            Column('count', Integer),
            Column('time_of_request', DateTime)
        )

        products = Table(
            'products',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('product_id', String(9)),
            Column('display_name', String(255)),
            Column('division', String(100)),
            Column('price', Float),
            Column('sale_price', Float, nullable=True),
            Column('search_result_id', ForeignKey('search_results.id'))
        )
        self.dict_of__staging_tables = {
            "search_results": search_results,
            "products": products
        }
        logger.info("Tables set up successfully.")

    def load_into_parquet(self, df: pd.DataFrame, table_name: str) -> None:
        """Load a DataFrame into a Parquet file."""
        try:
            df.to_parquet(self.res_dir / f"{table_name}.parquet")
            logger.info(
                f"DataFrame loaded into {self.res_dir / f'{table_name}.parquet'}"
            )
        except Exception as e:
            logger.error(f"Error loading DataFrame into Parquet: {e}")

    def insert_into_db(self, query: Insert) -> None:
        """Insert data into the database."""
        with self.engine.connect() as conn:
            conn.execute(query)
            conn.commit()
            logger.info("Data inserted into database.")

    # def save_to_db(self, df: pd.DataFrame, table_name: str) -> None:
    #     """Save a DataFrame to a PostgreSQL database."""
    #     try:
    #         df.to_sql(table_name, self.engine, if_exists='append', index=False)
    #         logger.info(f"DataFrame saved to table '{table_name}' in the database.")
    #     except Exception as e:
    #         logger.error(f"Error saving DataFrame to database: {e}")
