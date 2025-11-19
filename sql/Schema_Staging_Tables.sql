CREATE SCHEMA staging;
CREATE SCHEMA dw;

CREATE TABLE staging.spending_raw (
    agency                          TEXT,
    agency_code                     VARCHAR(3),
    fiscal_year                     INTEGER,
    issue_date                      DATE,
    payee_name                      VARCHAR(100),
    payee_code                      VARCHAR(10),
    document_id                     VARCHAR(36),
    contract_id                     VARCHAR(36),
    expense_category                VARCHAR(22),
    expense_category_name           TEXT,
    spending_category               VARCHAR(22),
    check_amount                    NUMERIC(18,2),
    capital_project_code            VARCHAR(15),
    capital_project                 TEXT,
    department_code                 VARCHAR(9),
    department                      TEXT,
    mwbe_category                   VARCHAR(20),
    industry                        VARCHAR(4),
    budget_code                     VARCHAR(4),
    spending_category_name          TEXT,
    conditional_category            VARCHAR(2),
    other_government_entities_code  VARCHAR(3)
);

-- Dimension: Agency
CREATE TABLE dw.dim_agency (
    agency_id        SERIAL PRIMARY KEY,
    agency_name      TEXT,
    department       TEXT,
    industry         VARCHAR(4),
    budget_code      VARCHAR(4)
);

-- Dimension: Vendor
CREATE TABLE dw.dim_vendor (
    vendor_id            SERIAL PRIMARY KEY,
    payee_name           VARCHAR(100),
    emerging_business    VARCHAR(10),
    woman_owned_business VARCHAR(10)
);

-- Dimension: Expense Category
CREATE TABLE dw.dim_expense_category (
    expense_category_id SERIAL PRIMARY KEY,
    expense_category    VARCHAR(22),
    expense_category_name TEXT
);

-- Dimension: Spending Category
CREATE TABLE dw.dim_spending_category (
    spending_category_id SERIAL PRIMARY KEY,
    spending_category    VARCHAR(10),
    spending_category_name TEXT
);

-- Dimension: MWBE Category
CREATE TABLE dw.dim_mwbe_category (
    mwbe_category_id SERIAL PRIMARY KEY,
    mwbe_category    VARCHAR(20)
);

-- Dimension: Date
CREATE TABLE dw.dim_date (
    date_id     SERIAL PRIMARY KEY,
    full_date   DATE,
    year        INT,
    month       INT,
    day         INT,
    fiscal_year INT
);

CREATE TABLE dw.fact_spending (
    fact_spending_id     SERIAL PRIMARY KEY,
    agency_id            INT REFERENCES dw.dim_agency(agency_id),
    vendor_id            INT REFERENCES dw.dim_vendor(vendor_id),
    expense_category_id  INT REFERENCES dw.dim_expense_category(expense_category_id),
    spending_category_id INT REFERENCES dw.dim_spending_category(spending_category_id),
    mwbe_category_id     INT REFERENCES dw.dim_mwbe_category(mwbe_category_id),
    date_id              INT REFERENCES dw.dim_date(date_id),
    document_id          VARCHAR(36),
    contract_id          VARCHAR(36),
    check_amount         NUMERIC(18,2)
);