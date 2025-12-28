FROM apache/airflow:2.9.0

USER airflow

# Install Python libs here
RUN pip install --no-cache-dir \
    requests \
    pymongo \
    python-dotenv \
    psycopg2-binary

USER root
