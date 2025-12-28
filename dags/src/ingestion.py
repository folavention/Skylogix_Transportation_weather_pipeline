import os
import requests 
from datetime import datetime, timezone 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

locations = [
    {"name": "Lagos_NG", "lat" : "6.5244", "lon": "3.3792"},
    {"name": "Nairobi_KE", "lat" : "-1.2921", "lon": "36.8219"},
    {"name": "Johannesburg_ZA", "lat" : "-26.2041", "lon": "28.0473"},
    {"name": "Accra_GH", "lat" : "5.6037", "lon": "-0.1870"}
]
weather_url = "https://api.openweathermap.org/data/2.5/weather"

def get_weather_data(lat, lon):
    
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(weather_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching weather data:", response.status_code)
    return None


def ingest_weather():
    Ingested_data = []

    for location in locations:
        weather_data = get_weather_data(location["lat"], location["lon"])
        if weather_data:
            record = {
                "location": location["name"],
                "lat": location["lat"],
                "lon": location["lon"],
                "Updated_at": datetime.now(timezone.utc).timestamp(),
                "raw": weather_data,
                "observed_at": datetime.fromtimestamp(weather_data["dt"], tz=timezone.utc).isoformat()
            }

            Ingested_data.append(record)

    return Ingested_data


if __name__ == "__main__":
    data = ingest_weather()
    print(f"Ingested {len(data)} weather records.")