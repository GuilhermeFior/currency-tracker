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