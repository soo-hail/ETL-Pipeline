import json

from airflow import DAG
# Allows you to make API calls (like GET or POST) from inside your DAG.
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.decorators import task
# PostgresHook lets to connect with a PostgreSQL Database and run SQL queries.
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Define DAG
with DAG(
    dag_id='ETL_NASA_APOD',
    start_date=days_ago(1),
    schedule='@daily',
    catchup=False
) as dag:
    
    # Create Table in PostgreSQL, if not exists.
    @task
    def create_table():
        hook = PostgresHook(postgres_conn_id='') 
        
        # SQL Queries.
        q1 = '''
            CREATE TABLE IF NOT EXISTS apod_data(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url TEXT,
                date DATE,
                media_type VARCHAR(50)
            )
        '''
        
        hook.run(q1)
        
    # Extract NASA API Data (APOD) - Call API
    extract_apod = SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',  # Defined in Airflow Connections
        endpoint='planetary/apod',  # NASA API Endpoint for APOD
        method='GET',
        params={
            'api_key': '{{ conn.nasa_api.extra_dejson.api_key }}'
        },
        response_filter=lambda response: response.json(),
        log_response=True
    )
    
    # Transform Data.
    
    
    # Load Data into PostgreSQL.
    
    # Verify Data using DBViewer.
    
    # Define Dependencies.
    