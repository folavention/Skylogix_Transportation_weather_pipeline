# Postgres schema
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
POSTGRES_URI = os.getenv("POSTGRES_URI")


create_table = """
CREATE TABLE IF NOT EXISTS weather_readings (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(100),
    country VARCHAR(10),
    lat NUMERIC,
    lon NUMERIC,
    temp_c NUMERIC,
    feels_like_c NUMERIC,
    pressure_hpa INTEGER,
    humidity_pct INTEGER,
    wind_speed_ms NUMERIC,
    wind_deg INTEGER,
    cloud_pct INTEGER,
    visibility_m INTEGER,
    rain_1h_mm NUMERIC,
    snow_1h_mm NUMERIC,
    condition_main VARCHAR(50),
    condition_description VARCHAR(255)
);
"""
# Adding column

""" 
COMMENT ON COLUMN weather_analytics.id IS 'Surrogate key';
COMMENT ON COLUMN weather_analytics.location_name IS 'City Name';
COMMENT ON COLUMN weather_analytics.country IS 'Country Code';
COMMENT ON COLUMN weather_analytics.observed_at IS 'Time of weather observation';
COMMENT ON COLUMN weather_analytics.lat IS 'Latitude';
COMMENT ON COLUMN weather_analytics.lon IS 'Longitude';
COMMENT ON COLUMN weather_analytics.temp_c IS 'Temperature (°C)';
COMMENT ON COLUMN weather_analytics.feels_like_c IS 'Feels Like Temperature (°C)';
COMMENT ON COLUMN weather_analytics.pressure_hpa IS 'Atmospheric Pressure (hPa)';
COMMENT ON COLUMN weather_analytics.humidity_pct IS 'Humidity (%)';
COMMENT ON COLUMN weather_analytics.wind_speed_ms IS 'Wind Speed (m/s)';
COMMENT ON COLUMN weather_analytics.wind_deg IS 'Wind Direction (degrees)';
COMMENT ON COLUMN weather_analytics.cloud_pct IS 'Cloud cover (%)';
COMMENT ON COLUMN weather_analytics.visibility_m IS 'Visibility (meters)';
COMMENT ON COLUMN weather_analytics.rain_1h_mm IS 'Rain volume for the last hour (mm)';
COMMENT ON COLUMN weather_analytics.snow_1h_mm IS 'Snow volume for the last hour (mm)';
COMMENT ON COLUMN weather_analytics.condition_main IS 'Main weather condition(e.g., Rain, Clear)';
COMMENT ON COLUMN weather_analytics.condition_description IS 'Detailed weather description';
COMMENT ON COLUMN weather_analytics.ingested_at IS 'Time the record was loaded into PostgresSQL';

CREATE INDEX idx_weather_city_time ON weather_analytics (city, observed_at);
"""



conn = psycopg2.connect(POSTGRES_URI)
cur = conn.cursor()
cur.execute(create_table)
conn.commit()
cur.close()
conn.close()
print("Table created successfully")