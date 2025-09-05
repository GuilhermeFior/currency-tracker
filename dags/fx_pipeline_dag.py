import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

# Se você usar Cloud Run, troque por um operador customizado/Hook.
# Aqui vamos ilustrar rodando o scraper local via Docker (ambiente do worker precisa ter Docker).

DEFAULT_ARGS = {
    "owner": "GuilhermeFior",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="fx_pipeline",
    description="Scrape FX & Crypto → RAW → dbt staging/silver/gold → KPIs",
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 8,20 * * *",  # 08:00 UTC e 20:00 UTC (~05:00 e 17:00 BRT)
    catchup=False,
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    tags=["fx", "dbt", "bigquery"],
) as dag:

    docker_scraper = BashOperator(
        task_id="extract_to_raw",
        bash_command="python /project/services/scraper/app.py",
        env={
            "BQ_PROJECT_ID": "{{ var.value.BQ_PROJECT_ID }}",
            "BQ_DATASET_RAW": os.getenv("BQ_DATASET_RAW", "fx_raw"),
            "BQ_TABLE_RAW": os.getenv("BQ_TABLE_RAW", "prices_raw"),
            "BQ_LOCATION": os.getenv("BQ_LOCATION", "US"),
            "BASE_CURRENCY": os.getenv("BASE_CURRENCY", "BRL"),
            "GOOGLE_APPLICATION_CREDENTIALS": "/keys/sandbox-personal-projects-26ad98d02f4f.json",
        },
    )

    # Rodando dbt via Bash (o ambiente do worker precisa ter dbt instalado/configurado)
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command="cd /project/dags/../dbt && dbt deps",
    )

    dbt_staging = BashOperator(
        task_id="dbt_staging",
        bash_command=(
            "cd /project/dags/../dbt && "
            "dbt run --select staging --profiles-dir ~/.dbt"
        ),
    )

    dbt_tests = BashOperator(
        task_id="dbt_tests",
        bash_command=(
            "cd /project/dags/../dbt && "
            "dbt test --select staging+ --profiles-dir ~/.dbt"
        ),
    )

    dbt_silver = BashOperator(
        task_id="dbt_silver",
        bash_command=(
            "cd /project/dags/../dbt && "
            "dbt run --select silver --profiles-dir ~/.dbt"
        ),
    )

    dbt_gold = BashOperator(
        task_id="dbt_gold",
        bash_command=(
            "cd /project/dags/../dbt && "
            "dbt run --select gold --profiles-dir ~/.dbt"
        ),
    )

    docker_scraper >> dbt_deps >> dbt_staging >> dbt_tests >> dbt_silver >> dbt_gold