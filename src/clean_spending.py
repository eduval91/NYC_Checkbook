import pandas as pd

# --------- CONFIG ---------
BUCKET = "nyc-spending-data-enriqued"
INPUT_PATH = f"gs://{BUCKET}/raw/checkbook_spending_FY2023.csv"
OUTPUT_PATH = f"gs://{BUCKET}/staging/checkbook_spending_FY2023_clean.csv"


def load_raw() -> pd.DataFrame:
    """
    Load the raw spending CSV directly from GCS into pandas.
    Requires gcsfs to be installed: pip install gcsfs
    """
    print(f"Loading raw data from {INPUT_PATH} ...")
    df = pd.read_csv(INPUT_PATH, dtype=str)  # read as strings first
    print(f"Loaded {len(df):,} rows, {len(df.columns)} columns.")
    return df


def normalize_flags(series: pd.Series) -> pd.Series:
    """
    Convert Y/N, Yes/No strings to booleans.
    Unrecognized / missing values become NaN.
    """
    if series is None:
        return series
    s = series.str.strip().str.upper()
    mapping = {
        "Y": True,
        "YES": True,
        "N": False,
        "NO": False,
    }
    return s.map(mapping)


def clean_spending(df: pd.DataFrame) -> pd.DataFrame:
    # --- Standardize column names ---
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # --- Strip whitespace and turn empty strings into NaN ---
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
            df[col] = df[col].replace({"": pd.NA})

    # --- Type conversions ---
    # issue_date -> datetime
    if "issue_date" in df.columns:
        df["issue_date"] = pd.to_datetime(df["issue_date"], errors="coerce")

    # fiscal_year -> integer (nullable)
    if "fiscal_year" in df.columns:
        df["fiscal_year"] = pd.to_numeric(df["fiscal_year"], errors="coerce").astype("Int64")

    # check_amount -> float
    if "check_amount" in df.columns:
        df["check_amount"] = (
            df["check_amount"]
            .str.replace("[,$]", "", regex=True)
            .replace({"": pd.NA})
        )
        df["check_amount"] = pd.to_numeric(df["check_amount"], errors="coerce")

    # --- Normalize flags ---
    for flag_col in ["emerging_business", "woman_owned_business"]:
        if flag_col in df.columns:
            df[flag_col] = normalize_flags(df[flag_col])

    # --- Filter out bad records ---
    # Drop rows with missing key fields
    if "agency" in df.columns:
        df = df[df["agency"].notna()]
    if "payee_name" in df.columns:
        df = df[df["payee_name"].notna()]

    # Drop rows with nonpositive or missing amounts
    if "check_amount" in df.columns:
        df = df[df["check_amount"].notna() & (df["check_amount"] > 0)]

    # --- Remove exact duplicates (based on a composite key) ---
    subset_cols = [c for c in ["agency", "payee_name", "issue_date",
                               "document_id", "check_amount"] if c in df.columns]
    if subset_cols:
        before = len(df)
        df = df.drop_duplicates(subset=subset_cols, keep="first")
        after = len(df)
        print(f"Removed {before - after:,} duplicate rows based on {subset_cols}")

    return df


def main():
    df_raw = load_raw()
    df_clean = clean_spending(df_raw)

    print(f"Saving cleaned data ({len(df_clean):,} rows) to {OUTPUT_PATH} ...")
    df_clean.to_csv(OUTPUT_PATH, index=False)
    print("Done.")


if __name__ == "__main__":
    main()