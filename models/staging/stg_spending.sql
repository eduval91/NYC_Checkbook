{{ config(materialized="table") }}

select
    agency,
    department,
    industry,
    budget_code,
    payee_name,
    expense_category,
    spending_category,
    check_amount,
    mwbe_category,
    emerging_business,
    woman_owned_business,
    issue_date,
    fiscal_year,
    contract_id,
    document_id
from {{ source("nyc_spending", "spending_clean") }}
