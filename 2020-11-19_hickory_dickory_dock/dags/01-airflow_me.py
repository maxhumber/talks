from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def flip_coin():
    face = random.choice(["Heads", "Tails"])
    print(face)

default_args = {
    "owner": "Max",
    "start_date": datetime(2020, 11, 19),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "flip_dag",
    default_args=default_args,
    schedule_interval=timedelta(days=1)
)

task_1 = PythonOperator(task_id="flip_function", python_callable=flip_coin, dag=dag)
