{{ config(
    materialized='table'
) }}

with date_spine as (

    select

        generate_series(
            '2020-01-01'::date,
            '2035-12-31'::date,
            interval '1 day'
        )::date as date_day

)

select

    to_char(date_day, 'YYYYMMDD')::integer as date_sk,

    date_day as full_date,

    extract(year from date_day)::integer as year,

    extract(month from date_day)::integer as month,

    extract(day from date_day)::integer as day,

    extract(quarter from date_day)::integer as quarter,

    extract(week from date_day)::integer as week_of_year,

    extract(dow from date_day)::integer as day_of_week,

    trim(to_char(date_day, 'Day')) as day_name,

    trim(to_char(date_day, 'Month')) as month_name,

    case
        when extract(dow from date_day) in (0, 6)
        then true
        else false
    end as is_weekend

from date_spine