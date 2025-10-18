import os
import hashlib
import time
from datetime import datetime, timezone
from typing import List, Dict


import pandas as pd
from google.cloud import bigquery
import requests
from decimal import Decimal, ROUND_HALF_UP

# ===== Config via env vars =====
PROJECT_ID = os.getenv("BQ_PROJECT_ID", "sandbox-personal-projects")
DATASET_RAW = os.getenv("BQ_DATASET_RAW", "fx_raw")
TABLE_RAW = os.getenv("BQ_TABLE_RAW", "prices_raw")
LOCATION = os.getenv("BQ_LOCATION", "US")
# Defines BRL as the base currency
BASE_CURRENCY = os.getenv("BASE_CURRENCY", "BRL")

# Public data sources for USD, EUR, BTC and ETH
FRANKFURTER_ECB_URL = os.getenv("FRANKFURTER_ECB_URL", "https://api.frankfurter.dev/v1/latest")
COINGECKO_SIMPLE_URL = os.getenv("COINGECKO_SIMPLE_URL", "https://api.coingecko.com/api/v3/simple/price")

SYMBOLS_FRANKFURTER = ["EUR", "USD"]
SYMBOLS_CRYPTO = ["BTC", "ETH"]

SCALE = Decimal("0.000000001")  # 9 decimal places

# ===== Functions =====
def _row_hash(*values: str) -> str:
    """Generates hash to identify each row
    """
    h = hashlib.sha256()
    for v in values:
        h.update(str(v).encode("utf-8"))
    return h.hexdigest()

def fetch_currency(base_currency: str = BASE_CURRENCY) -> List[Dict]:
    """Colects exchange rates from FRANKFURTER and returns a list of dicts.
    Uses frankfurter.dev (free).
    """
    rows = []
    collected_at = datetime.now(timezone.utc)

    for sym in SYMBOLS_FRANKFURTER:
        # Frankfurter: from = moeda de referência; to = moeda alvo
        resp = requests.get(
            FRANKFURTER_ECB_URL, 
            params={"from": sym, "to": base_currency}, 
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        value_in_base = float(data["rates"][base_currency])

        rows.append(
            {
                "symbol": sym,
                "source": "frankfurter.dev",
                "value": value_in_base,
                "currency": base_currency,
                "collected_at": collected_at,
            }
        )
    return rows

def fetch_crypto(base_currency: str = BASE_CURRENCY) -> List[Dict]:
    """Colects crypto quotations via CoinGecko (compared to BRL) and returns
    a list of dicts"""
    ids_map = {"BTC": "bitcoin", "ETH": "ethereum"}
    ids = ",".join(ids_map[s] for s in SYMBOLS_CRYPTO)
    resp = requests.get(
        COINGECKO_SIMPLE_URL,
        params={"ids": ids, "vs_currencies": base_currency.lower()},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()


    collected_at = datetime.now(timezone.utc)
    rows = []
    for sym in SYMBOLS_CRYPTO:
        coin = ids_map[sym]
        value_in_base = data.get(coin, {}).get(base_currency.lower())
        if value_in_base is None:
            continue
        rows.append(
            {
                "symbol": sym,
                "source": "coingecko",
                "value": float(value_in_base),
                "currency": base_currency,
                "collected_at": collected_at,
            }
        )
    return rows

def ensure_table(client: bigquery.Client):
    """ Defines the BigQuery table's schema and configures the
    table's storage (partitioning by collected_at and clustering by symbol)
    """
    table_id = f"{PROJECT_ID}.{DATASET_RAW}.{TABLE_RAW}"
    schema = [
        bigquery.SchemaField("symbol",          "STRING",       mode="REQUIRED"),
        bigquery.SchemaField("source",          "STRING",       mode="REQUIRED"),
        bigquery.SchemaField("value",           "NUMERIC",      mode="REQUIRED"),
        bigquery.SchemaField("currency",        "STRING",       mode="REQUIRED"),
        bigquery.SchemaField("collected_at",    "TIMESTAMP",    mode="REQUIRED"),
        bigquery.SchemaField("row_hash",        "STRING",       mode="REQUIRED"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.DAY, field="collected_at")
    table.clustering_fields = ["symbol"]
    try:
        client.get_table(table_id)
    except Exception:
        client.create_dataset(DATASET_RAW, exists_ok=True)
        client.create_table(table)

def to_decimal(x):
    """ Takes a float/str/None var and turns into a Decimal var
    with SCALE decimal places, as defined inside the program
    """
    if x is None:
        return None
    d = Decimal(str(x))
    return d.quantize(SCALE, rounding=ROUND_HALF_UP)

def write_rows(rows: List[Dict]):
    """Writes rows into the BigQuery table
    """
    if not rows:
        print("No rows to insert.")
        return

    for r in rows:
        r["row_hash"] = _row_hash(
            r["symbol"], r["source"], r["currency"], r["value"], r["collected_at"]
        )
        # >>> critical adjustment for NUMERIC:
        r["value"] = to_decimal(r["value"])

    df = pd.DataFrame(rows)

    # makes sure dtypes are friendly to Arrow
    df["symbol"] = df["symbol"].astype("string")
    df["source"] = df["source"].astype("string")
    df["currency"] = df["currency"].astype("string")
    df["row_hash"] = df["row_hash"].astype("string")
    df["collected_at"] = pd.to_datetime(df["collected_at"], utc=True)

    client = bigquery.Client(project=PROJECT_ID, location=LOCATION)
    ensure_table(client)

    table_id = f"{PROJECT_ID}.{DATASET_RAW}.{TABLE_RAW}"
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"),
    )
    job.result()
    print(f"Inserted {len(rows)} rows into {table_id}")

def main():
    start = time.time()
    rows = []
    rows += fetch_currency()
    rows += fetch_crypto()
    write_rows(rows)
    print(f"Done in {time.time()-start:.2f}s")

if __name__ == "__main__":
    main()