{{ config(materialized="table") }}

with
    base as (
        select distinct payee_name, emerging_business, woman_owned_business
        from {{ ref("stg_spending") }}
        where payee_name is not null
    )

select
    cast(farm_fingerprint(coalesce(payee_name, '')) as string) as vendor_id,
    payee_name,
    emerging_business,
    woman_owned_business
from base
