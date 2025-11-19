NYC Governemnt Spending
CIS 9440
ASsignment 1

DATA SOURCING
The dataset for this project comes from the NYC Checkbook Spending API, which provides information about New York City government agency spending. I used a Python script to connect to the API via XML POST requests and retrieve Fiscal Year 2023 data. To bypass issues I had with my IP being banned, the script also converts results into a structured CSV file. The script supports pagination and extracts up to 50,000 rows for this assignment (too big of a file). A separate data dictionary (provided in an Excel Sheet) under /NYC_Checkbook/data_dictionary.

STORAGE
The raw CSV file is stored in Google Cloud Storage (GCS). I created a dedicated bucket with a folder structure that separates raw, staging, and warehouse layers. A Python script uploads the raw CSV from my local machine to the GCS bucket. This structure supports a scalable pipeline and mirrors common industry data lake patterns.

MODELING
The analytical data model follows a star schema design. I created one fact table, fact_spending, which contains spending transactions and foreign keys referencing dimension tables. The dimensions include agency, vendor, expense category, spending category, MWBE category, and date. The model supports analysis such as spending by agency, vendor, time, MWBE status, and category. I documented the schema using an ERD created in Lucidchart. SQL script is included to create the staging table and all data warehouse tables in PostgreSQL.

PIPELINE SUMMARY
The final workflow includes:

	•	Extracting data from the NYC Checkbook API using Python
	•	Storing raw data in Google Cloud Storage
	•	Designing and creating a staging table in PostgreSQL
	•	Designing and creating a dimensional star schema for analytics
	•	Documenting the full process with scripts, an ERD, and a README


HOW TO USE
The fetch script retrieves data from the API and saves it locally. The upload script sends the CSV to Google Cloud Storage. SQL files can be run in pgAdmin or psql to create the necessary schemas and tables in PostgreSQL.

TOOLS USED
Python, Google Cloud Storage, PostgreSQL, pgAdmin, Lucidchart, GitHub.