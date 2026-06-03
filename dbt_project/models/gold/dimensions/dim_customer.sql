{{ config(materialized='table') }}

select

    md5(cast(dbt_scd_id as text)) as customer_sk,

    customer_id,
    customer_name,
    city,

    dbt_valid_from as effective_date,

    coalesce(
        dbt_valid_to,
        cast('9999-12-31' as timestamp)
    ) as end_date,

    case
        when dbt_valid_to is null then true
        else false
    end as current_flag

from {{ ref('customer_snapshot') }}