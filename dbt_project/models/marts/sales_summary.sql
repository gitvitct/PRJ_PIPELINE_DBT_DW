{{ config(materialized='table') }}

select

    customer_sk,

    count(*) total_orders,

    sum(amount) total_sales,

    avg(amount) avg_ticket

from {{ ref('fact_sales') }}

group by customer_sk