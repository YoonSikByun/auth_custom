export AIRFLOW_HOME=/opt/mlstudio/source/github/auth_custom/auth_custom/airflow/tests/airflow
airflow db init
# airflow users create  --username admin  --firstname Peter  --lastname Parker  --role Admin  --email spiderman@superhero.org
airflow users create -r Admin -u admin -e admin@example.com -f admin -l user -p admin