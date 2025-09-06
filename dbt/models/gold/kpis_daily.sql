{{ config(
    materialized='incremental',
    partition_by={"field": "collected_date", "data_type": "date"},
    cluster_by=["symbol"],
) }}

with h as (
  select * from `sandbox-personal-projects.fx_dev.prices_hourly`
),

kpis as (
  select
    symbol,
    collected_date,
    currency,
    last_value,
    high,
    low,
    lag(last_value) over(partition by symbol order by collected_date) as prev_close,
    safe_divide(last_value - lag(last_value) over(partition by symbol order by collected_date), lag(last_value) over(partition by symbol order by collected_date)) as daily_return,
    max(high) over(partition by symbol order by collected_date rows between 6 preceding and current row) as ma7,
    max(high) over(partition by symbol order by collected_date rows between 29 preceding and current row) as ma30
  from h
)
select * from kpis

{% if is_incremental() %}
  where collected_date >= date_sub(current_date(), interval 90 day)
{% endif %}