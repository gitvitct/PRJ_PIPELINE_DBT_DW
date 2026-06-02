{% snapshot customer_snapshot %}

{{
    config(
        target_schema='public',
        unique_key='customer_id',

        strategy='timestamp',
        updated_at='updated_at'
    )
}}

select

    customer_id,
    customer_name,
    city,
    updated_at

from {{ ref('stg_customers') }}

{% endsnapshot %}