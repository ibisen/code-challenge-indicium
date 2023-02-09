# Indicium code-challenge Solution by Ibisen de Brito Gonçalves

Create an ETL process that extracts data every day from two different sources and writes the data first to a local disk, and after to a database. 

![Nortwind Database Schema](https://user-images.githubusercontent.com/49417424/105997621-9666b980-608a-11eb-86fd-db6b44ece02a.png)

More info about this test can be found at: https://github.com/techindicium/code-challenge

## Solution

To complete this test I prefer to work with Python and Airflow. 
Python due to its gorgeous libraries for data, and great community support.
Airflow because it is open source, and this tool can describe, execute, and monitor workloads.

### Tasks
This challenge asks us to solve three main tasks:
1. To extract data from the Postgres database and write to the local disk;
2. To extract data from CSV file and write to local disk;
3. To extract data from the local filesystem, to transform and load for a final database.

I used Python to code:

**Task1:** connects to the Postgres Database to retrieve the names of all tables and then writes the data into a local file, which includes the path for each source, table, and the day of execution. 
```python
#importing libraries to work with Postgres, CSV and file system
import  psycopg2
import  pandas  as  pd
import  os
import  sys

date = sys.argv[1][:10]

#PostgreSQL Connection
host = "postgres-container-indicium"
database = "northwind"
user = "northwind_user"
password = "thewindisblowing"
  
db_conn = psycopg2.connect(host=host,database = database, user = user, password = password)
db_cursor = db_conn.cursor()

...
``` 

**Task 2:** Duplicate the CSV file and save it to the local file system, specifying a path for each source, table, and execution day. 
```python
#importing libraries
import  shutil
import  os
import  sys

date = sys.argv[1][:10]

...
```
**Task 3:** Extracting local data, aggregating tables, and storing the result as a JSON file in a Mongo. 

Thinking about current technologies, with mobile and web first, I decided to use JSON due to its extremely lightweight to send back and forth in HTTP requests and responses due to the small file size, which makes JSON one of the best options for web development and mobile apps.
```python
#importing libraries to work with Pandas and MongoDB and others
import  collections
from  numpy  import  product
import  pandas  as  pd
from  pymongo  import  MongoClient
import  sys

...

# Load the data to a MongoDB Database
client = MongoClient('mongo-container', 27017, username='mongo', password = 'mongo1234')
db = client['orders']
collection = db['details']
collection.insert_many(details)

### DAG
For Task 3 to be successful, it is necessary that Tasks 1 and 2 have been executed without issue. To ensure this, Airflow requires a DAG to be created. This DAG is set to run daily and its last line enforces the necessary dependencies between the tasks.

DAG File

```python
from  airflow  import  DAG
from  datetime  import  datetime, timedelta
from  airflow.operators.bash_operator  import  BashOperator
from  airflow.utils.dates  import  days_ago

default_args = {
'owner': 'Ibisen de Brito Goncalves',
'depends_on_past': False,
'start_date': days_ago(2),
'retries': 1,
}

with  DAG(
'DAG',
schedule_interval=timedelta(days=1),
default_args=default_args
) as  dag:

	tsk1 = BashOperator(
	task_id='task1',
	bash_command="""
	cd $AIRFLOW_HOME/dags/tasks/
	python3 task1.py {{ execution_date }}
	""")
	...
```
## Setup of the Solution

I used Docker to containerize the solution, due to Docker is an effective way to containerize a solution, allowing for easy setup and installation. With Docker Compose, you can easily set up the source code for your project. To get started, simply follow the instructions at the appropriate website. This will ensure that your project runs smoothly and is properly integrated with the necessary resources. Official Docker and Docker Composer documentation: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)
With docker compose installed simply run:

```
docker-compose up -d
```
## Testing the Pipeline

After configuring the code, testing each task or the entire pipeline can be carried out retrospectively.
Access the Airflow container:
```
docker exec -it airflow-container bash
```
Testing some tassk:

```
airflow test DAG-indicium task1 2023-02-02
```
Tasks available in DAG-indicium: task1, task2, task3. 

To run the pipeline in past days:
```
airflow backfill DAG-indicium -s 2023-02-03 -e 2023-02-04
```
The output files will be load at `/data` folder.

## MongoDB Database

Accessing the MongoDB (and see the outputs), in a terminal execute:
```
mongo -u mongo -p mongo1234 --authenticationDatabase "admin"
```
At mongo terminal:
```
> use orders
> db.details.find().pretty()
```
