from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "weather_db"
COLLECTION_NAME = "weather_raw"


def upsert_weather(records: list[dict]):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    if not records:
        print("No records to upsert.")
        return
    
    for record in records:
        filter_query = {
            "location": record["location"],
            "observed_at": record["observed_at"]
        }
        update_query = {"$set": record}
        
        
        collection.update_one(filter_query, update_query, upsert=True)

    