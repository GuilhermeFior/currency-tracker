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