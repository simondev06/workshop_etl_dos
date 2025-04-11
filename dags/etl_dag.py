from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'simon',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='etl_pipeline_dag',
    default_args=default_args,
    schedule=None,
    catchup=False,
    description="DAG alternativo para ejecutar el ETL completo",
) as dag:

    extract_spotify = BashOperator(
        task_id='extract_spotify',
        bash_command='python3 /opt/airflow/scripts/extract_spotify.py 1210'
    )

    transform_spotify = BashOperator(
        task_id='transform_spotify',
        bash_command='python3 /opt/airflow/scripts/transform_spotify.py'
    )

    extract_grammy = BashOperator(
        task_id='extract_grammy',
        bash_command='python3 /opt/airflow/scripts/extract_grammy.py 1210'
    )

    transform_grammy = BashOperator(
        task_id='transform_grammy',
        bash_command='python3 /opt/airflow/scripts/transform_grammy.py'
    )

    extract_lastfm = BashOperator(
        task_id='extract_lastfm',
        bash_command='python3 /opt/airflow/scripts/extract_lastfm.py 1210'
    )

    transform_lastfm = BashOperator(
        task_id='transform_lastfm',
        bash_command='python3 /opt/airflow/scripts/transform_lastfm.py'
    )

    merge = BashOperator(
        task_id='merge_datasets',
        bash_command='python3 /opt/airflow/scripts/merge_datasets.py'
    )

    load = BashOperator(
        task_id='load_to_sqlite',
        bash_command='python3 /opt/airflow/scripts/load_to_sqlite.py'
    )

    export_csv = BashOperator(
        task_id='export_to_csv',
        bash_command='python3 /opt/airflow/scripts/export_to_csv.py'
    )

    # Flujo corregido
    extract_spotify >> transform_spotify
    extract_grammy >> transform_grammy
    extract_lastfm >> transform_lastfm

    [transform_spotify, transform_grammy, transform_lastfm] >> merge >> load >> export_csv

