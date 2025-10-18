# Base image: official Apache Airflow image, version 2.9.3
# This already comes with Airflow installed and ready to run on Python 3.10
# It also brings Airflow's CLI, webserver, scheduler and core dependencies
FROM apache/airflow:2.9.3-python3.10
# Changing to root to install system-level packages
USER root
# Install system dependencies inside the container
RUN apt-get update && apt-get install -y gosu
# Going back to non-root airflow user
USER airflow
# Install Python libs use by tasks/dbt
COPY requirements.txt .
RUN pip install -r requirements.txt