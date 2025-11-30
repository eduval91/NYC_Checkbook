{{ config(materialized='table') }}

with base as (
    select distinct
        cast(issue_date as date) as issue_date,
        fiscal_year
    from {{ ref('stg_spending') }}
    where issue_date is not null
)

select
    -- date_id as yyyymmdd string for easy joins
    format_date('%Y%m%d', issue_date) as date_id,
    issue_date as full_date,
    extract(year  from issue_date) as calendar_year,
    extract(month from issue_date) as month,
    extract(day   from issue_date) as day,
    fiscal_year
from base