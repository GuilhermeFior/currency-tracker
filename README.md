# currency-tracker

This project aims to store daily quotations of USD, EUR, BTC and ETH compared to BRL, so we can track events as such as when they reached the lowest value.

![Pipeline diagram](/excalidraw_diagram.png)

**Data source**:
- USD and EUR are retrieved from Frankfurter ECD
- BTC and ETH from CoinGecko

**Stack**: dbt + BigQuery | Airflow | Docker

- BigQuery is for data storage and analytics
- dbt is used for data transformation (*bronze* → *silver* → *gold*), as well as for enforcing data quality
- Airflow handles orchestration (DAGs)
- Docker provides containerization for reproducibility

## Data Architecture
This project follows the **Medallion Architecture**:

| Layer | Purpose |
|-------|---------|
| **Raw** | Data ingestion (initial landing zone) |
| **Bronze** | Raw data mirrored for audition |
| **Silver** | Cleaned and transformed data |
| **Gold** | Final metrics analytics-ready datasets |

---

## How to run

### 1. Configure Google Cloud Service Account

This project uses **Google BigQuery** to store currency and crypto exchange rate data.
To run it locally or in Docker, you need to set up a **Google Cloud Service Account** with the correct permissions and provide its credentials to the project.

Follow the steps bellow carefully:

1. **Create a Google Cloud Service Account**

- Go to [IAM & Admin → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
- Click **"+ Create Service Account"**
   - Under **"Grant this service account access to the project"**, add the roles:
     - `BigQuery Data Editor`
     - `BigQuery User`

2. **Generate and download a key file**

- Choose **JSON** format and click **Create**
- A `.json` file will automatically download - this is your **private key**.

3. **Save the key file locally**

Move the downloaded file to a safe folder on your computer, for example:
- Windows: `C:\Users\<your_user>\keys\<key.json>`
- macOS/Linux: `~/keys/<key.json>`

4. **Update your project's `.env` file**

- Inside your project's root folder, create a `.env` (from `.env.example` in this repo) and update:

```bash
HOST_KEYS_DIR=/ABSOLUTE/PATH/TO/your/local/keys
HOST_DBT_DIR=/ABSOLUTE/PATH/TO/your/local/.dbt
BQ_PROJECT_ID=YOUR_PROJECT_ID
BQ_DATASET_RAW=YOUR_DATASET_RAW
BQ_TABLE_RAW=YOUR_TABLE_RAW
BQ_LOCATION=YOUR_BQ_LOCATION
GCP_KEY_FILENAME=KEY_FILE_NAME.json
```

### 2. Configure `profiles.yml` for dbt

dbt requires a configuration file named `profiles.yml` that stores connection details to BigQuery. This file should not be inside your project folder, but rather in your user's home directory, inside a `.dbt` folder.

```perl
C:/Users/<your_user>/
└── .dbt/
    └── profiles.yml
```

Inside Docker (mapped automatically by `docker-compose.yml`):
```swift
/home/airflow/.dbt/profiles.yml
```

I left `profiles.example.yml` as an example on how it should be configured. This version dinamically reads the environment variables provided by Docker on your terminal (`.env` file), so you never hard-code credentials or paths.

### 3. Run the Scraper locally (optional) 

You can test the Scraper outside of Docker:

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

> [!WARNING]
> You must have Google authentication configured either via `GOOGLE_APLICATION_CREDENTIALS` or `gcloud auth application-default login`.

### 4. Run with Docker and Docker Compose

- [Start with Docker](https://www.docker.com/get-started)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

**1. Initialize Docker Compose**

Run the command below on git bash in the folder, in order to start the services:

```bash
docker-compose up
```

**2. Connect to Airflow via the URL: [http://localhost:8080](http://localhost:8080).**

The username and password are `airflow`.

**3. At the end of the operation, stop Docker Compose**

```bash
docker-compose down
```

---

## Next steps

Here are some ideas and improvements planned for the next iterations of the project:

- Connect the gold layer to a BI tool for monitoring currency trends
- Deploy the pipeline on GCP using Cloud Composer

---

Enjoy exploring your currency-tracker pipeline, and feel free to make suggestions or ask any questions!