{{ config(
    materialized='incremental',
    partition_by={"field": "collected_at_date", "data_type": "date"},
    cluster_by=["symbol"],
) }}

-- Normaliza RAW: tipagem, remoção de duplicatas, base currency coerente
with src as (
  select
    symbol,
    source,
    cast(value as numeric) as value,
    currency,
    timestamp(collected_at) as collected_at,
    row_hash
  from `{{ var('project_id', 'sandbox-personal-projects') }}.{{ var('raw_dataset', 'fx_raw') }}.{{ var('raw_table', 'prices_raw') }}`
),

-- Dedup por row_hash (último ingestion)
dedup as (
  select as value * except(rn)
  from (
    select s.*, row_number() over(partition by row_hash order by ingestion_ts desc) rn
    from src s
  ) where rn = 1
)

select
  symbol,
  source,
  value,
  currency,
  collected_at,
  date(collected_at) as collected_at_date,
  row_hash
from dedup

{% if is_incremental() %}
  where collected_at >= timestamp_sub(current_timestamp(), interval 7 day)
{% endif %}