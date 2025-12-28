from pymongo import MongoClient
import psycopg2
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
POSTGRES_URI = os.getenv("POSTGRES_URI")

def transform_weather_data(raw):
    weather = (raw.get("weather") or [{}])[0]

    return {
        "location_name": raw.get("name"),
        "country": raw.get("sys", {}).get("country"),
        "lat": raw.get("coord", {}).get("lat"),
        "lon": raw.get("coord", {}).get("lon"),

        "provider": raw.get("provider_name", "openweathermap"),
        "observed_at": raw.get("dt"),

        "temperature": raw.get("main", {}).get("temp"),
        "humidity": raw.get("main", {}).get("humidity"),
        "pressure_hpa": raw.get("main", {}).get("pressure"),
        "visibility": raw.get("visibility"),

        "wind_speed": raw.get("wind", {}).get("speed"),
        "wind_deg": raw.get("wind", {}).get("deg"),

        "cloudiness": raw.get("clouds", {}).get("all"),

        "rainfall": raw.get("rain", {}).get("1h", 0.0),
        "snowfall": raw.get("snow", {}).get("1h", 0.0),

        "weather_condition": weather.get("main"),
        "weather_description": weather.get("description"),
        "icon": weather.get("icon"),

        "ingested_at": datetime.now(timezone.utc)
    }

def load_weather_data(transformed_records: list[dict]):
    
    if not transformed_records:
        print("No transformed records to load.")
        return
    pg_conn = psycopg2.connect(POSTGRES_URI)
    pg_cursor = pg_conn.cursor()


    
    for record in transformed_records:
        pg_cursor.execute(
            """
            INSERT INTO weather_analytics (
                location_name, lat, lon, observed_at,
                temperature, humidity, weather_condition,
                wind_speed, rainfall, ingested_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                record["location_name"],
                record["lat"],
                record["lon"],
                record["observed_at"],
                record["temperature"],
                record["humidity"],
                record["weather_condition"],
                record["wind_speed"],
                record["rainfall"],
                record["ingested_at"],
            )
        )

    pg_conn.commit()
    pg_cursor.close()
    pg_conn.close()
    print(f"{len(transformed_records)} records loaded into Postgres.")
