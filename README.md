# currency-tracker

**Stack**: dbt + BigQuery | Python (pandas) | (Airflow/Dagster)  
**Objetivo**: acompanhar flutuação do câmbio para moedas selecionadas, em relação ao Real.  
**Dado**: Moedas são buscadas em Frankfurter ECD e Criptomoedas são buscadas em CoinGecko    

## Arquitetura
- **Bronze**: ingestão RAW
- **Silver**: limpeza/conformidade
- **Gold**: métricas/marts para BI

## Como rodar
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
Além disso, é necessário configurar a autenticação no GCP (`GOOGLE_APLICATION_CREDENTIALS` ou `gcloud auth`).

### With Docker and Docker Compose
- You need to install Docker and Docker Compose
- [Start with Docker](https://www.docker.com/get-started)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

### Steps to Docker and Airflow configuration
1. Initialize **Docker Compose**

&ensp; Run the command below on git bash in the folder, in order to upload the services:
&ensp; ```bash
docker-compose up
```

2. Connect to **Airflow** via the URL: [http://localhost:8080](http://localhost:8080).

&ensp; The username is `airflow`, the same as the password.

3. At the end of the operation, stop **Docker Compose**

&ensp; Stop the started server with
&ensp; ```bash
docker-compose down
```