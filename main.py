import pandas as pd
from pathlib import Path


data_path = Path("data_store")


def main():
    datasheet_df = pd.read_csv(data_path / "datasheet.csv")
    # Process the DataFrame
    print(datasheet_df.head())


def get_datasheet():
    return pd.read_csv(data_path / "datasheet.csv")


if __name__ == "__main__":
    main()
