from os import environ as env
import smtplib
from airflow import DAG

from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


from airflow.models import Variable

from datetime import datetime, timedelta



defaul_args = {
    "owner": "Lautaro Poletto",
    "start_date": datetime(2025, 9, 23),
    "retries": 1,
    "retry_delay": timedelta(seconds=5),
}

with DAG(
    dag_id="spark_etl",
    default_args=defaul_args,
    description="ETL de ejemplo con Spark",
    schedule_interval="@daily",
    catchup=False,
) as dag:
    
    # Tareas
    spark_etl = SparkSubmitOperator(
        task_id="spark_etl",
        application=f'{Variable.get("spark_scripts_dir")}/spark_etl.py',
        conn_id="spark_default",
        dag=dag,
        driver_class_path=Variable.get("driver_mysql_path"),
    )


    spark_etl