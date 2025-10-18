# currency-tracker

I started this project to study the integration of dbt and BigQuery (GCP) as well as data orchestration with Apache Airflow.

It aims to load on BigQuery the daily quotations of USD, EUR, BTC and ETH, as compared to BRL, so that we can track when they reached the lowest, for example.

**Stack**: dbt + BigQuery | Python (pandas) | (Airflow/Dagster)  
**Data source**: USD and EUR are retrieved from Frankfurter ECD e BTC and ETH from CoinGecko    

## Data Architecture
For this project I used the Medallion Architecture.
- **Raw**: bucketing/data ingestion
- **Bronze**: raw data mirroring
- **Silver**: treated data
- **Gold**: metrics for BI and analytics

## How to run
```bash
cd services/scraper
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
export BQ_PROJECT_ID=YOUR_GCP_PROJECT
export BQ_DATASET_RAW=YOUR_GCP_DATASET
export BQ_TABLE_RAW=YOUR_GCP_TABLE
export BQ_LOCATION=US
python app.py
``` 
It is also necessary to have Google auth configured (`GOOGLE_APLICATION_CREDENTIALS` or `gcloud auth`).

### With Docker and Docker Compose
- You need to install Docker and Docker Compose
- [Start with Docker](https://www.docker.com/get-started)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

### Steps to Docker and Airflow configuration
1. Initialize **Docker Compose**

&ensp; Run the command below on git bash in the folder, in order to upload the services:

```bash
docker-compose up
```

2. Connect to **Airflow** via the URL: [http://localhost:8080](http://localhost:8080).

&ensp; The username is `airflow`, the same as the password.

3. At the end of the operation, stop **Docker Compose**

&ensp; Stop the started server with

```bash
docker-compose down
```