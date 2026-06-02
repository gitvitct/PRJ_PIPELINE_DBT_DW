{{
    config(
        materialized='incremental',
        unique_key='sale_id',
        incremental_strategy='merge'
    )
}}

select

    s.sale_id,
    d.customer_sk,
    s.amount,
    s.sale_date,
    s.updated_at

from {{ ref('stg_sales') }} s

inner join {{ ref('dim_customer') }} d
    on s.customer_id = d.customer_id

where d.current_flag = true

{% if is_incremental() %}

and s.updated_at >
(
    select coalesce(max(updated_at), '1900-01-01')
    from {{ this }}
)

{% endif %}