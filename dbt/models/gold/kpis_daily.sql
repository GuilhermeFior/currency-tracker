{{ config(
    materialized='incremental',
    partition_by={"field": "collected_date", "data_type": "collected_date"},
    cluster_by=["symbol"],
) }}

with h as (
  select * from {{ ref('prices_hourly') }}
),

agg as (
  select
    symbol,
    collected_date,
    any_value(currency) as currency,
    -- close diário = último close por hora do dia
    approx_top_sum(close_value, 1)[OFFSET(0)] as close_value,
    max(high) as high,
    min(low) as low
  from h
  group by 1,2
),

kpis as (
  select
    symbol,
    collected_date,
    currency,
    close_value,
    high,
    low,
    lag(close_value) over(partition by symbol order by collected_date) as prev_close,
    safe_divide(close_value - lag(close_value) over(partition by symbol order by collected_date), lag(close_value) over(partition by symbol order by collected_date)) as daily_return,
    avg(close_value) over(partition by symbol order by collected_date rows between 6 preceding and current row) as ma7,
    avg(close_value) over(partition by symbol order by collected_date rows between 29 preceding and current row) as ma30
  from agg
)
select * from kpis

{% if is_incremental() %}
  where collected_date >= date_sub(current_date(), interval 90 day)
{% endif %}