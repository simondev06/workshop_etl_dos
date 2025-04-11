from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import glob

default_args = {
    "owner": "simon",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

def clean_outputs():
    print("🧹 Limpiando archivos de salidas anteriores...")

    paths = [
        "/opt/airflow/data/processed/*.parquet",
        "/opt/airflow/data/output/*.csv",
        "/opt/airflow/data/output/*.db"
    ]

    for pattern in paths:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"🗑️ Borrado: {file}")
            except Exception as e:
                print(f"  No se pudo borrar {file}: {e}")

with DAG(
    dag_id="etl_pipeline_sws",
    default_args=default_args,
    description="ETL completo con cantidad de registros configurable",
    schedule=None,
    catchup=False,
) as dag:

    clean_task = PythonOperator(
        task_id="clean_outputs",
        python_callable=clean_outputs
    )

    num_registros = 1210  # puedes ajustar el tamaño de prueba

    extract_grammy = BashOperator(
        task_id="extract_grammy",
        bash_command=f"python3 /opt/airflow/scripts/extract_grammy.py {num_registros}"
    )

    transform_grammy = BashOperator(
        task_id="transform_grammy",
        bash_command="python3 /opt/airflow/scripts/transform_grammy.py"
    )

    extract_spotify = BashOperator(
        task_id="extract_spotify",
        bash_command=f"python3 /opt/airflow/scripts/extract_spotify.py {num_registros}"
    )

    transform_spotify = BashOperator(
        task_id="transform_spotify",
        bash_command="python3 /opt/airflow/scripts/transform_spotify.py"
    )

    extract_lastfm = BashOperator(
        task_id="extract_lastfm",
        bash_command=f"python3 /opt/airflow/scripts/extract_lastfm.py {num_registros}"
    )

    transform_lastfm = BashOperator(
        task_id="transform_lastfm",
        bash_command="python3 /opt/airflow/scripts/transform_lastfm.py"
    )

    merge = BashOperator(
        task_id="merge_datasets",
        bash_command="python3 /opt/airflow/scripts/merge_datasets.py"
    )

    load_db = BashOperator(
        task_id="load_to_sqlite",
        bash_command="python3 /opt/airflow/scripts/load_to_sqlite.py"
    )

    export_csv = BashOperator(
        task_id="export_to_csv",
        bash_command="python3 /opt/airflow/scripts/export_to_csv.py"
    )

    # Flujo corregido
    clean_task >> extract_spotify >> transform_spotify
    clean_task >> extract_grammy >> transform_grammy
    clean_task >> extract_lastfm >> transform_lastfm

    [transform_spotify, transform_grammy, transform_lastfm] >> merge >> load_db >> export_csv

