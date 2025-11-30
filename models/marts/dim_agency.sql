{{ config(materialized="table") }}

with
    base as (
        select distinct agency, department, industry, budget_code
        from {{ ref("stg_spending") }}
        where agency is not null
    )

select
    -- stable surrogate key using BigQuery farm_fingerprint
    cast(
        farm_fingerprint(
            concat(
                coalesce(agency, ''),
                '|',
                coalesce(department, ''),
                '|',
                coalesce(industry, ''),
                '|',
                coalesce(budget_code, '')
            )
        ) as string
    ) as agency_id,
    agency,
    department,
    industry,
    budget_code
from base
