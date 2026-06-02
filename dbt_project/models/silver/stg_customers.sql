{{ config(materialized='view') }}

select

    customer_id,
    customer_name,
    city,
    updated_at

from {{ source('bronze', 'raw_customers') }}