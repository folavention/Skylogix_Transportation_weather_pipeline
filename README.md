📌 Skylogix Weather ETL Pipeline

This project builds an end-to-end data engineering pipeline that ingests live weather data from OpenWeather API, stores raw data in MongoDB, orchestrates ETL using Apache Airflow, transforms the data, and loads curated analytics-ready data into PostgreSQL for insights that support logistics decision making.

🏗️ Architecture Overview
OpenWeather API
        ↓ (Extract)
Python Ingestion Script
        ↓
MongoDB (Raw Staging)
        ↓
Apache Airflow (ETL Orchestration)
        ↓ (Transform & Clean)
PostgreSQL (Analytics Warehouse)
        ↓
SQL Analytics / Dashboards

✨ Features

Live weather ingestion (multiple cities; Lagos NG, Nairaobi KE, johnannesburg ZA, Accra GH)

MongoDB raw data lake

Airflow-scheduled ETL pipeline

Data transformation & standardization

Analytics ready PostgreSQL tables

Supports logistics use cases such as:

route risk awareness

delay prediction

operational weather visibility

🧰 Tech Stack

Python

Docker + Docker Compose(windows)

Apache Airflow

MongoDB

PostgreSQL

Requests / PyMongo / Psycopg2

⚙️ Prerequisites

Ensure you have installed:

Docker Desktop

Docker Compose

Python 3.10+

Git

🔐 Environment Variables

Create a .env file in project root:

OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxx
MONGO_URI=mongodb://mongodb:27017
POSTGRES_URI=postgresql://postgres:YOUR_PASSWORD@postgres:5432/weather_db


Make sure there are no quotes in env values.

🚀 How to Run
1️⃣ Build & Start Airflow + Services

Run:

docker compose up --build


This will start:

Airflow Webserver

Airflow Scheduler

Redis

MongoDB

PostgreSQL

2️⃣ Access Airflow UI

Open:

http://localhost:8080


Credentials:

username: airflow
password: airflow

3️⃣ Enable & Trigger Pipeline

1️⃣ Enable DAG: fetch_and_upsert_weather
2️⃣ Trigger manually or wait for scheduled run

📊 Analytics
Weather Trends per City

Example Query: Check(Sample_queries.sql)

🔗 Logistics Integration Concept

This weather data can be joined to logistics records using:

city

timestamp/day

geo-coordinates proximity


Uses:

Predict route delays

Weather-aware routing

Risk management for fleet ops

🩺 Troubleshooting
❌ DAG Not Showing?

Ensure your DAG file is inside:

dags/

❌ Module Not Found (pymongo, psycopg2)?

Ensure requirements.txt exists beside docker-compose.yml
and Airflow image installs it automatically.

❌ Mongo or Postgres Connection Error?

Confirm .env values are correct.

Restart stack:

docker compose down
docker compose up --build

📁 Project Structure
dags/
  src/
   ├─ ingestion.py
   ├─ mongo_staging.py
   ├─ transform.py
   ├─ postgres_load.py
  etl.py
requirements.txt
docker-compose.yml
dockerfile
sample_queries.sql
.env
README.md

🐳 Custom Airflow Docker Image (Handling Dependencies)

During development, some Airflow tasks failed because certain Python dependencies (like pymongo) were not available inside the default Airflow container.
To fix this, I created a custom Dockerfile to extend the official Airflow image and install the required packages.


👩‍💻 Author

Skylogix Transportation – Weather Intelligence ETL
Built by Folakemi Juliet ❤️
