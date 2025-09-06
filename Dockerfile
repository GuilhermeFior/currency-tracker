# currency-tracker/docker/airflow/Dockerfile
FROM apache/airflow:2.9.3-python3.10

USER root
RUN apt-get update && apt-get install -y gosu
USER airflow

# Instale libs Python usadas pelas suas tasks/dbt
COPY requirements.txt .
RUN pip install -r requirements.txt