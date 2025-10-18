# Starts from a minimal Python image (3.11-slim), which is lighter and
# best suited for small services, such as the scraper
FROM python:3.11-slim
# Sets /app as the working directory
WORKDIR /app
# Copies the dependencies
COPY requirements.txt ./
# Installs only what's needed for scraping
RUN pip install --no-cache-dir -r requirements.txt
# Copies the actual scraper code
COPY app.py ./
# Expected vars: BQ_PROJECT_ID, BQ_DATASET_RAW, BQ_TABLE_RAW, BQ_LOCATION, BASE_CURRENCY
# Specifies how the container should start (running python app.py)
CMD ["python", "app.py"]