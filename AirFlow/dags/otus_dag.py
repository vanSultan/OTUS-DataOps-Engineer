from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

with DAG(
    dag_id="otus-hw-dag",
    start_date=datetime.fromisoformat("2022-07-31"),
    schedule_interval="@once",
) as dag:
    start_task = EmptyOperator(task_id="start")

    print_hello_world = BashOperator(
        task_id="print_hello_world", bash_command='echo "HelloWorld!"'
    )

    end_task = EmptyOperator(task_id="end")

start_task >> print_hello_world >> end_task
