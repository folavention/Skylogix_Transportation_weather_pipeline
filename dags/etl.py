from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.ingestion import ingest_weather
from src.mongo_staging import upsert_weather
from src.transform import transform_weather_data, load_weather_data

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}


def fetch_weather_data_task():
    weather_data = ingest_weather()
    return weather_data


def upsert_weather_task(**kwargs):
    ti = kwargs["ti"]
    weather_data = ti.xcom_pull(task_ids="fetch_weather_data_task")
    if weather_data:
        upsert_weather(weather_data)
        ti.xcom_push(key="raw_data", value=weather_data)


def transform_task(**kwargs):
    ti = kwargs["ti"]
    raw_data = ti.xcom_pull(task_ids="upsert_weather_data")  # make sure upsert pushes XCom
    if not raw_data:
        print("No raw data to transform")
        return
    transformed = transform_weather_data(raw_data)
    ti.xcom_push(key="transformed", value=transformed)


def load_task(**kwargs):
    ti = kwargs["ti"]
    transformed = ti.xcom_pull(key="transformed", task_ids="transform_weather_data")
    load_weather_data(transformed_records=transformed)


with DAG(
    dag_id="fetch_and_upsert_weather",
    default_args=default_args,
    description="Fetch weather → Staging → Transform → Load Postgres",
    schedule_interval=timedelta(minutes=15),
    start_date=datetime(2024, 12, 1),
    catchup=False,
) as dag:

    fetch_weather_data_op = PythonOperator(
        task_id="fetch_weather_data_task",
        python_callable=fetch_weather_data_task,
    )
    
    upsert_weather_op = PythonOperator(
        task_id="upsert_weather_data",
        python_callable=upsert_weather_task,
    )

    transform_task_op = PythonOperator(
        task_id="transform_weather_data",
        python_callable=transform_task,
    )

    load_task_op = PythonOperator(
        task_id="load_weather_data_to_postgres",
        python_callable=load_task,
    )

    fetch_weather_data_op >> upsert_weather_op >> transform_task_op >> load_task_op
