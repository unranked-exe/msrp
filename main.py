from pathlib import Path

import pandas as pd



data_path = Path("data_store")
datasheet_csv = data_path / "datasheet.csv"

def main() -> None:
    datasheet_df = get_datasheet(datasheet_csv)
    # Process the DataFrame
    print(datasheet_df.head())

    print(datasheet_df["Cat Description"].value_counts())

    print(datasheet_df.isna().sum())
    
    print(datasheet_df.duplicated().sum())
    print(datasheet_df[datasheet_df[["STYLE Description","GBP G - MSRP"]].duplicated()])


def get_datasheet(data_path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(data_path)
    except pd.errors.EmptyDataError as e:
        print(f"Datasheet is empty: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    except Exception as e:
        print(f"Error reading datasheet: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


if __name__ == "__main__":
    main()
