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
    dag_id=f'etl_2{today_date}',
    default_args=default_args,
    description='ETL pipeline for data processing',
    schedule_interval="@daily",
    start_date=datetime.strptime("2024-05-07", '%Y-%m-%d'),
    catchup=True
) as dag:

    t1 = BashOperator(
        task_id='fetch_the_api',
        bash_command="python3 /opt/airflow/data/config.py"
    )
    
    t2 = BashOperator(
        task_id='validate_the_api',
        bash_command="python3 /opt/airflow/data/api_utils.py"
    )
    
    t3 = BashOperator(
        task_id='log_the_data',
        bash_command="python3 /opt/airflow/data/logging_config.py"
    )
    
    t4 = BashOperator(
        task_id='decrypt_the_data',
        bash_command="python3 /opt/airflow/data/decryption_utils.py"
    )
    
    t5 = BashOperator(
        task_id='validate_the_data',
        bash_command="python3 /opt/airflow/data/validation_utils.py"
    )
    
    t6 = BashOperator(
    task_id='final_etl_processing',
    bash_command="python3 /opt/airflow/data/etl_m12.py --connection {{ var.value.data_dev_connection }} --csv '{{ task_instance.xcom_pull(task_ids='fetch_the_api') }}'"
    )

    t1 >> t2 >> t3 >> t4 >> t5 >> t6
