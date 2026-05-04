import pandas as pd
from pathlib import Path

RAW_PATH = Path('data/raw/bq-results-last-12-months.csv')
CLEAN_DIR = Path('data/clean')
CLEAN_DIR.mkdir(parents=True, exist_ok=True)
CLEAN_PATH = CLEAN_DIR / 'bq-results-last-12-months-clean.csv'

CATEGORY_FILL = 'UNKNOWN'


def parse_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    df['SQLDATE'] = pd.to_datetime(df['SQLDATE'], format='%Y%m%d', errors='coerce')
    if 'DATEADDED' in df.columns:
        df['DATEADDED'] = pd.to_datetime(df['DATEADDED'], format='%Y%m%d%H%M%S', errors='coerce')
    return df


def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        'GoldsteinScale',
        'AvgTone',
        'NumMentions',
        'NumSources',
        'NumArticles',
        'Year',
        'MonthYear',
        'EventCode',
        'EventBaseCode',
        'EventRootCode',
        'QuadClass',
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def fill_categorical_missing(df: pd.DataFrame) -> pd.DataFrame:
    cat_cols = [
        col for col in df.columns
        if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == object
    ]
    for col in cat_cols:
        df[col] = df[col].fillna(CATEGORY_FILL).replace('', CATEGORY_FILL)
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    initial_rows = len(df)

    df = parse_date_columns(df)
    df = convert_numeric_columns(df)

    # Remove exact duplicate rows and duplicate event IDs
    df = df.drop_duplicates(ignore_index=True)
    df = df.drop_duplicates(subset=['GLOBALEVENTID'], keep='first')

    df = fill_categorical_missing(df)

    # Replace invalid SQLDATE rows if any
    invalid_dates = df['SQLDATE'].isna().sum()
    if invalid_dates > 0:
        df = df[df['SQLDATE'].notna()].reset_index(drop=True)

    final_rows = len(df)
    print(f'Initial rows: {initial_rows}')
    print(f'Final rows: {final_rows}')
    print(f'Removed rows: {initial_rows - final_rows}')

    return df


def save_cleaned_data(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
    print(f'Cleaned file saved to: {path}')


def main() -> None:
    df = pd.read_csv(RAW_PATH, dtype=str)
    cleaned = clean_dataframe(df)
    save_cleaned_data(cleaned, CLEAN_PATH)


if __name__ == '__main__':
    main()
