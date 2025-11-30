{{ config(materialized='table') }}

with base as (
    select distinct
        spending_category
    from {{ ref('stg_spending') }}
    where spending_category is not null
)

select
    cast(farm_fingerprint(
        coalesce(spending_category, '')
    ) as string) as spending_category_id,
    spending_category
from base