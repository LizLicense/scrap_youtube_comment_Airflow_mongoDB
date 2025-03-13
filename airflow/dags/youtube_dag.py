from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


# Import task functions
from fetch_youtube_data import fetch_and_save_youtube_data
from load_data_to_mongo import load_data_to_mongodb

# Define default arguments
default_args = {
    'owner': 'Liz',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'is459_assignment_youtube',
    default_args=default_args,
    description='YouTube data ETL pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Add start task
start = EmptyOperator(
    task_id='start',
    dag=dag,
)

# Task 1: Fetch YouTube data
fetch_data_task = PythonOperator(
    task_id='fetch_youtube_data',
    python_callable=fetch_and_save_youtube_data,
    dag=dag,
)

# Task 2: Load data to MongoDB
load_data_task = PythonOperator(
    task_id='load_data_to_mongodb',
    python_callable=load_data_to_mongodb,
    dag=dag,
)

end = EmptyOperator(
    task_id='end',
    dag=dag,
)

# Set task dependencies
start >> fetch_data_task >> load_data_task >> end
