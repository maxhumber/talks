### Airflow Instructions

Install Airflow

```sh
pip install apache-airflow
```

Export Home:

```sh
export AIRFLOW_HOME=`pwd`
```

Create a dag file:

```sh
cat dags/01-airflow_me.py
```

Initialize the database:

```sh
airflow initdb
```

Run the schedule:

```sh
airflow scheduler
```
