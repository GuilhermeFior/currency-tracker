import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {
    "owner": "GuilhermeFior",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="fx_pipeline",
    description="Scrape FX & Crypto → RAW → dbt staging/silver/gold",
    start_date=datetime(2025, 1, 1),
    schedule_interval='0 7 * * *',
    catchup=False,
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    tags=["fx", "dbt", "bigquery"],
) as dag:

    extract_to_raw = BashOperator(
        task_id="extract_to_raw",
        bash_command="python /project/services/scraper/app.py"
    )

    # Running dbt via Bash
    dbt_deps = BashOperator(
        task_id="dbt_deps",
        bash_command=(
            "cd /project/dags/../dbt && dbt deps --profiles-dir ~/.dbt"
        )
    )

    dbt_staging = BashOperator(
        task_id="dbt_staging",
        bash_command=(
            "cd /project/dags/../dbt && dbt run --select staging --profiles-dir ~/.dbt"
        ),
    )

    dbt_tests = BashOperator(
        task_id="dbt_tests",
        bash_command=(
            "cd /project/dags/../dbt && dbt test --select staging+ --profiles-dir ~/.dbt"
        ),
    )

    dbt_silver = BashOperator(
        task_id="dbt_silver",
        bash_command=(
            "cd /project/dags/../dbt && dbt run --select silver --profiles-dir ~/.dbt"
        ),
    )

    dbt_gold = BashOperator(
        task_id="dbt_gold",
        bash_command=(
            "cd /project/dags/../dbt && dbt run --select gold --profiles-dir ~/.dbt"
        ),
    )

    extract_to_raw >> dbt_deps >> dbt_staging >> dbt_tests >> dbt_silver >> dbt_gold