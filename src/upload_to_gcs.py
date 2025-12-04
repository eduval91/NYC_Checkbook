from google.cloud import storage
from pathlib import Path

# Service account JSON (in your project root)
SERVICE_ACCOUNT = "gcp-service-account.json"

# Your GCS bucket name
BUCKET_NAME = "nyc-spending-data-enriqued"


def upload_raw_file(local_path: str, gcs_path: str) -> None:
    """
    Upload a local file to Google Cloud Storage.
    local_path: path to file on your machine
    gcs_path:   key (path) inside the bucket, e.g. "raw/file.csv"
    """
    # Create a client using the service account
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT)

    # Get bucket + blob
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(gcs_path)

    # Upload the local file
    blob.upload_from_filename(local_path)

    print(f"Uploaded {local_path} -> gs://{BUCKET_NAME}/{gcs_path}")


def main():
    # Local CSV you generated from the API
    local_file = Path("data/raw/checkbook_spending_FY2023.csv")

    # Where it should live in the bucket
    gcs_key = "raw/checkbook_spending_FY2023.csv"

    if not local_file.exists():
        raise FileNotFoundError(f"Local file not found: {local_file}")

    upload_raw_file(str(local_file), gcs_key)


if __name__ == "__main__":
    main()