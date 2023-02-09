from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

default_args = {
   'owner': 'Ibisen Brito Goncalves',
   'depends_on_past': False,
   'start_date': days_ago(2),
   'retries': 1,
   }

with DAG(
   'DAG-indicium',
   schedule_interval=timedelta(days=1),
   default_args=default_args
   ) as dag:

   tsk1 = BashOperator(
   task_id='task1',
   bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 task1.py {{ execution_date }}
   """)
   
   tsk2 = BashOperator(
   task_id='task2',
   bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 task2.py {{ execution_date }}
   """)

   tsk3 = BashOperator(
   task_id='task3',
   bash_command="""
   cd $AIRFLOW_HOME/dags/tasks/
   python3 task3.py {{ execution_date }}
   """)

[tsk1,tsk2] >> tsk3