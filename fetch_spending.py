import requests
import xml.etree.ElementTree as ET
from pathlib import Path
import csv

API_URL = "https://www.checkbooknyc.com/api"
PAGE_SIZE = 1000
ROW_LIMIT = 50000

def build_request_xml(fiscal_year: int, record_from: int, max_records: int) -> str:
    return f"""
    <request>
      <type_of_data>Spending</type_of_data>
      <records_from>{record_from}</records_from>
      <max_records>{max_records}</max_records>
      <search_criteria>
        <criteria>
          <name>fiscal_year</name>
          <type>value</type>
          <value>{fiscal_year}</value>
        </criteria>
      </search_criteria>
      <response_columns>
        <column>agency</column>
        <column>fiscal_year</column>
        <column>issue_date</column>
        <column>payee_name</column>
        <column>document_id</column>
        <column>contract_id</column>
        <column>expense_category</column>
        <column>spending_category</column>
        <column>check_amount</column>
        <column>department</column>
        <column>mwbe_category</column>
        <column>industry</column>
        <column>emerging_business</column>
        <column>woman_owned_business</column>
        <column>budget_code</column>
      </response_columns>
    </request>
    """.strip()

def fetch_page(year, start, size):
    xml_body = build_request_xml(year, start, size)
    headers = {"Content-Type": "application/xml"}
    resp = requests.post(API_URL, data=xml_body.encode("utf-8"), headers=headers)
    resp.raise_for_status()
    return resp.text

def parse_response(xml_text):
    root = ET.fromstring(xml_text)
    result_records = root.find(".//result_records")
    if result_records is None:
        return [], None

    rows = []
    for rec in result_records:
        row = {child.tag: (child.text or "").strip() for child in rec}
        rows.append(row)

    total_elem = root.find(".//record_count")
    total_count = int(total_elem.text) if total_elem is not None else None

    return rows, total_count

def main():
    fiscal_year = 2023
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    all_rows = []
    record_from = 1

    while True:
        print(f"Fetching {PAGE_SIZE} rows from record {record_from}...")
        xml_text = fetch_page(fiscal_year, record_from, PAGE_SIZE)
        rows, total = parse_response(xml_text)

        if not rows:
            break

        all_rows.extend(rows)
        record_from += PAGE_SIZE

        if len(all_rows) >= ROW_LIMIT:
            print(f"Reached limit of {ROW_LIMIT}, stopping early.")
            break

        if total and record_from > total:
            break

    csv_path = raw_dir / f"checkbook_spending_FY{fiscal_year}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Saved {len(all_rows)} rows → {csv_path}")

if __name__ == "__main__":
    main()
