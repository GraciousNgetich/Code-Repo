
from airflow_dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime


def print_world():
    print("world")


default_args = {
    'owner': 'Gracious',
    'start_date': datetime(2023, 7, 21),
    'retries': 1,
    'retry_delay': datetime(minute=5),
}

with DAG(dag_id='airflow_dag',
         default_args=default_args,
         ) as dag:

    hello = BashOperator(task_id='hello',
                         bash_command='echo "hello"')

    sleep = BashOperator(task_id='sleep',
                         bash_command='sleep 5')

    print_world = PythonOperator(task_id='print_world',
                                 python_callable=print_world)

    hello >> sleep >> print_world
