# currency-tracker

This project aims to store daily quotations of USD, EUR, BTC and ETH, as compared to BRL, so that we can track when they reached the lowest, for example.

**Data source**: USD and EUR are retrieved from Frankfurter ECD e BTC and ETH from CoinGecko  
**Stack**: dbt + BigQuery | Airflow | Docker

- BigQuery is for data storage and analytics
- dbt will be used for data transformation (*bronze* -> *silver* -> *gold*). It also acts on data quality.
- Airflow is for the orchestration (DAGs)
- Docker is being used for containerization

## Data Architecture
For this project I used the Medallion Architecture.
- **Raw**: bucketing/data ingestion
- **Bronze**: raw data mirroring
- **Silver**: treated data
- **Gold**: metrics for BI and analytics

## How to run

### GCP Service Account
This project uses Google BigQuery to store currency and crypto exchange rate data.
To run it locally or in Docker, you need to set up a Google Cloud service account with the correct permissions and provide its credentials to the project.

Follow the steps bellow carefully:
1. Create a Google Cloud Service Account

Under "Grant this service account acess to the project", add the following roles:
- `Bigquery Data Editor`
- `BigQuery User`

2. Generate and download a key file (choose JSON format)

A `.json` file will automatically download - this is your private key.

3. Save the key file locally

Move the downloaded file to a safe folder on your computer, for example:
- Windows: `C:\Users\<your_user>\keys\<key.json>`
- macOS/Linux: `~/keys/<key.json>`

4. Inside your project's `.env` file (which you create from `.env.example`), update:

```bash
HOST_KEYS_DIR=C:/Users/<your_user>/keys
GCP_KEY_FILENAME=<key.json>
```

### Run locally
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
