from ingestion import ingest_weather
from mongo_staging import upsert_weather_data

def run_pipeline():
    records = ingest_weather()
    upsert_weather_data(records)