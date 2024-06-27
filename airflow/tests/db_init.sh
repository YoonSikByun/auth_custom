# export AIRFLOW_HOME=~/airflow
airflow db init
airflow users create  --username admin  --firstname Peter  --lastname Parker  --role Admin  --email spiderman@superhero.org