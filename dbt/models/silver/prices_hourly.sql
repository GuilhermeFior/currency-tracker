{{ config(
    materialized='incremental',
    partition_by={"field": "collected_date", "data_type": "date"},
    cluster_by=["symbol"],
) }}

with base as (
  select * from `sandbox-personal-projects.fx_dev.stg_prices`
),
-- Padroniza para granularidade horária (floor para hora)
hourly as (
  select
    symbol,
    source,
    currency,
    date(collected_at) as collected_date,
    min(value) over (
      partition by symbol, source, currency, date(collected_at)
    ) AS low,
    max(value) over (
      partition by symbol, source, currency, date(collected_at)
    ) AS high,
    last_value(value) over (
      partition by symbol, source, currency, date(collected_at)
      order by timestamp_trunc(collected_at, hour) desc
      rows between unbounded preceding and unbounded following
    ) as last_value
  from base
)

select
  symbol,
  currency,
  collected_date,
  low,
  high,
  last_value
from hourly

{% if is_incremental() %}
  where collected_date >= date_sub(current_date(), interval 30 day)
{% endif %}