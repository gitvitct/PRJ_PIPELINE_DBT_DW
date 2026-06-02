{{ config(
    materialized='incremental',
    unique_key='customer_sk'
) }}

with source_data as (

    select
        customer_id,
        customer_name,
        city,
        updated_at
    from {{ ref('stg_customers') }}

)

select

    md5(
        concat(
            coalesce(customer_id::text, ''),
            coalesce(updated_at::text, '')
        )
    ) as customer_sk,

    customer_id,
    customer_name,
    city,

    updated_at as valid_from,

    null::timestamp as valid_to,

    true as current_flag

from source_data