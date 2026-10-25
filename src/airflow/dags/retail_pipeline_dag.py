
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="retail_intelligence_pipeline",
    description="Orchestrate the retail data engineering pipeline",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="30 6 * * *",
    catchup=False,
    tags=["retail", "azure", "databricks"],
) as dag:

    validate_environment = BashOperator(
        task_id="validate_environment",
        bash_command="python --version",
    )

    run_databricks_pipeline = BashOperator(
        task_id="run_databricks_pipeline",
        bash_command=(
            "echo 'Replace this command with the authenticated "
            "Databricks Jobs API invocation.'"
        ),
    )

    validate_environment >> run_databricks_pipeline
