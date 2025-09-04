FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

# Vars esperadas: BQ_PROJECT_ID, BQ_DATASET_RAW, BQ_TABLE_RAW, BQ_LOCATION, BASE_CURRENCY
CMD ["python", "app.py"]