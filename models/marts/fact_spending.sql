{{ config(materialized="table") }}

with
    base as (select * from {{ ref("stg_spending") }}),

    joined as (
        select
            -- surrogate key for the fact row
            cast(
                farm_fingerprint(
                    concat(
                        coalesce(agency, ''),
                        '|',
                        coalesce(payee_name, ''),
                        '|',
                        coalesce(cast(issue_date as string), ''),
                        '|',
                        coalesce(document_id, ''),
                        '|',
                        coalesce(cast(check_amount as string), '')
                    )
                ) as string
            ) as fact_spending_id,

            -- foreign keys to dimensions
            da.agency_id,
            dv.vendor_id,
            de.expense_category_id,
            ds.spending_category_id,
            dm.mwbe_category_id,
            dd.date_id,

            -- degenerate fields
            b.document_id,
            b.contract_id,
            b.fiscal_year,

            -- measures
            b.check_amount
        from base b

        left join
            {{ ref("dim_agency") }} da
            on da.agency = b.agency
            and da.department = b.department
            and da.industry = b.industry
            and da.budget_code = b.budget_code

        left join {{ ref("dim_vendor") }} dv on dv.payee_name = b.payee_name

        left join
            {{ ref("dim_expense_category") }} de
            on de.expense_category = b.expense_category

        left join
            {{ ref("dim_spending_category") }} ds
            on ds.spending_category = b.spending_category

        left join
            {{ ref("dim_mwbe_category") }} dm on dm.mwbe_category = b.mwbe_category

        left join {{ ref("dim_date") }} dd on dd.full_date = cast(b.issue_date as date)
    )

select *
from joined
