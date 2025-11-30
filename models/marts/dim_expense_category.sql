{{ config(materialized='table') }}

with base as (
    select distinct
        expense_category
    from {{ ref('stg_spending') }}
    where expense_category is not null
)

select
    cast(farm_fingerprint(
        coalesce(expense_category, '')
    ) as string) as expense_category_id,
    expense_category
from base