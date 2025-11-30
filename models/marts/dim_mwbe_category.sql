{{ config(materialized="table") }}

with
    base as (
        select distinct mwbe_category
        from {{ ref("stg_spending") }}
        where mwbe_category is not null
    )

select
    cast(farm_fingerprint(coalesce(mwbe_category, '')) as string) as mwbe_category_id,
    mwbe_category
from base
