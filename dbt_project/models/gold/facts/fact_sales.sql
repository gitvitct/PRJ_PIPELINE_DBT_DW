{{
config(
    materialized='incremental',
    unique_key='sale_id',
    incremental_strategy='merge'
)
}}

select

    s.sale_id,
    dc.customer_sk,
    dd.date_sk,
    s.amount,
    s.sale_date,
    s.updated_at

from {{ ref('stg_sales') }} s

inner join {{ ref('dim_customer') }} dc
    on s.customer_id = dc.customer_id
   and s.sale_date >= dc.effective_date
   and s.sale_date < dc.end_date

inner join {{ ref('dim_date') }} dd
    on cast(s.sale_date as date) = dd.full_date

{% if is_incremental() %}

where s.updated_at >
(
    select coalesce(
        max(updated_at),
        cast('1900-01-01' as timestamp)
    )
    from {{ this }}
)

{% endif %}