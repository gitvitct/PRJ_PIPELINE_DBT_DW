{{ config(materialized='view') }}

select

    sale_id,
    customer_id,
    cast(amount as numeric(12,2)) amount,
    --cast(sale_date as date) sale_date,
    sale_date            sale_date,
    cast(now()  as date)          updated_at

from {{ source('bronze', 'raw_sales') }}
where amount > 0


