{{ config(
    materialized='incremental',
    partition_by={"field": "collected_date", "data_type": "collected_date"},
    cluster_by=["symbol"],
) }}

with base as (
  select * from {{ ref('stg_prices') }}
),
-- Padroniza para granularidade horária (floor para hora)
hourly as (
  select
    symbol,
    source,
    currency,
    timestamp_trunc(collected_at, hour) as collected_hour,
    date(collected_at) as collected_date,
    -- preço de fechamento da hora
    any_value(value) ignore nulls as any_value_value,
    -- usa last_value por hora (ordenado por collected_at)
    approx_top_sum(value, 1)[OFFSET(0)] as close_guess, -- alternativa barata
    max(value) as high,
    min(value) as low
  from base
  group by 1,2,3,4,5
)
select
  symbol,
  currency,
  collected_hour,
  collected_date,
  close_guess as close_value,
  high,
  low
from hourly

{% if is_incremental() %}
  where collected_date >= date_sub(current_date(), interval 30 day)
{% endif %}