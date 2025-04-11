from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "simon",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="etl_pipeline_modo_prueba",
    default_args=default_args,
    description="ETL completo en modo prueba usando Airflow + Docker",
    schedule_interval=None,  # Puedes cambiarlo a "@daily" si quieres que corra automáticamente
    catchup=False,
) as dag:

    # Extracciones
    extract_grammy = BashOperator(
        task_id="extract_grammy",
        bash_command="python3 /opt/airflow/scripts/extract_grammy.py"
    )

    extract_spotify = BashOperator(
        task_id="extract_spotify",
        bash_command="python3 /opt/airflow/scripts/extract_spotify.py"
    )

    extract_lastfm = BashOperator(
        task_id="extract_lastfm",
        bash_command="python3 /opt/airflow/scripts/extract_lastfm.py"
    )

    # Transformaciones
    transform_grammy = BashOperator(
        task_id="transform_grammy",
        bash_command="python3 /opt/airflow/scripts/transform_grammy.py"
    )

    transform_spotify = BashOperator(
        task_id="transform_spotify",
        bash_command="python3 /opt/airflow/scripts/transform_spotify.py"
    )

    transform_lastfm = BashOperator(
        task_id="transform_lastfm",
        bash_command="python3 /opt/airflow/scripts/transform_lastfm.py"
    )

    # Merge
    merge = BashOperator(
        task_id="merge_datasets",
        bash_command="python3 /opt/airflow/scripts/merge_datasets.py"
    )

    # Carga
    load_db = BashOperator(
        task_id="load_to_sqlite",
        bash_command="python3 /opt/airflow/scripts/load_to_sqlite.py"
    )

    # Exportar CSV
    export_csv = BashOperator(
        task_id="export_to_csv",
        bash_command="python3 /opt/airflow/scripts/export_to_csv.py"
    )

    # Definir dependencias (orden correcto)
    extract_spotify >> transform_spotify
    extract_grammy >> transform_grammy
    extract_lastfm >> transform_lastfm

    [transform_spotify, transform_grammy, transform_lastfm] >> merge >> load_db >> export_csv

