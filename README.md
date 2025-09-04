# currency-tracker

**Stack**: dbt + BigQuery | Python (pandas) | (Airflow/Dagster)  
**Objetivo**: acompanhar flutuação do câmbio para moedas selecionadas, em relação ao Real.
**Dado**: <fonte, granularidade, período>  *TBD*

## Arquitetura
- **Bronze**: ingestão RAW
- **Silver**: limpeza/conformidade
- **Gold**: métricas/marts para BI

## Como rodar
```bash
python -m venv .venv && . .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
pre-commit install
dbt deps && dbt debug && dbt compile

## Sugestão Chat

Scraping (Python + pandas) de EUR, USD, BTC, ETH pela manhã.
- Faça o scraper idempotente (mesmo input → mesmo output) e com retry + backoff.
- Adicione hash da linha e timestamp de coleta para deduplicação.

Ingestão → RAW (BigQuery)
- Tabela particionada por ingestion_ts (DATE/TIMESTAMP) e clusterizada por symbol (e.g., EUR, USD, BTC, ETH).

Transformações
- Em vez de “procedures”, recomendo dbt (ou Dataform no BigQuery) para staging → silver → gold. Fica versionado, testável e documentado.
- Alerta por e-mail quando meta for batida (defina regras por ativo, p.ex. “variação diária > X%”).
- Airflow para orquestrar tudo. Se quiser GCP-native, use Cloud Composer (Airflow gerenciado).