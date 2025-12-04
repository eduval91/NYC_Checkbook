from google.cloud import bigquery


PROJECT_ID = "nyc-gov-spending"
DATASET_ID = "nyc_spending"

# GCS paths for your CSVs
RAW_URI = "gs://nyc-spending-data-enriqued/raw/checkbook_spending_FY2023.csv"
CLEAN_URI = "gs://nyc-spending-data-enriqued/staging/checkbook_spending_FY2023_clean.csv"


def load_csv_to_bq(uri: str, table_name: str) -> None:
    """
    Load a CSV file from GCS into a BigQuery table.

    - Overwrites the table each run (WRITE_TRUNCATE)
    - Autodetects schema (fine for this assignment)
    """
    client = bigquery.Client(project=PROJECT_ID)

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # header row
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    print(f"Starting load job for {table_id} from {uri} ...")
    load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    load_job.result()  # wait for completion

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows into {table_id}.")


def main() -> None:
    # Load raw data
    load_csv_to_bq(RAW_URI, "spending_raw")

    # Load cleaned data
    load_csv_to_bq(CLEAN_URI, "spending_clean")


if __name__ == "__main__":
    main()