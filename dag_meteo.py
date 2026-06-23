
import datetime
import json
import os
import requests

from dotenv import load_dotenv

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

from meteo_fun import connessione_estrazione, trasformazione, carica_dati


with DAG(
    dag_id="pipeline_meteo",
    description="prima_pipeline_autonoma",
    start_date=datetime.datetime(2026, 5, 27),
    schedule=datetime.timedelta(minutes=10),
    default_args={
        "owner": "mav",
        "retries": 5,
        "retry_delay": datetime.timedelta(minutes=1)
    }
) as dag:
    
    task_connessione_estrazione = PythonOperator(
        task_id="connessione_estrazione",
        python_callable=connessione_estrazione
    )

    task_transformazione = PythonOperator(
        task_id="trasformazione",
        python_callable=trasformazione
    )

    task_carica_dati = PythonOperator(
        task_id="carica_dati",
        python_callable=carica_dati
    )

    task_connessione_estrazione >> task_transformazione >> task_carica_dati















