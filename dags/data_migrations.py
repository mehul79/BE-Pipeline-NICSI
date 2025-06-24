from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.exceptions import AirflowException
import requests


# Get today's date in the desired format
today_date = datetime.now().strftime("%Y-%m-%d")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id=f'data_migrations{today_date}',
    default_args=default_args,
    description='ETL pipeline for data processing',
    schedule_interval="@daily",
    start_date=datetime.strptime("2024-05-07", '%Y-%m-%d'),
    catchup=True
) as dag:

    t1 = BashOperator(
        task_id='table_created',
        bash_command="python3 /opt/airflow/data/database.py"
    )

    t2 = BashOperator(
        task_id='fetch_the_api',
        bash_command="python3 /opt/airflow/data/etl_m12_local_db.py"
    )

    t1 >> t2
    # t2