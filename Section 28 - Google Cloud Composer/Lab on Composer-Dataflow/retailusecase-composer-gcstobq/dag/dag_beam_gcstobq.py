from __future__ import annotations

import datetime
import logging
import re

import yaml
from google.cloud import storage

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# --- CONFIGURATION LOADING ---
GCS_CONFIG_FILE_PATH = "gs://us-central1-demo-composer3--0736c962-bucket/dags/retail_config.yaml"

def get_config_from_gcs(gcs_path: str) -> dict:
    """Downloads and parses a YAML configuration file from GCS."""
    match = re.match(r"gs://([^/]+)/(.+)", gcs_path)
    if not match:
        raise ValueError(f"Invalid GCS path provided: {gcs_path}")

    bucket_name, blob_name = match.groups()
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    config_string = blob.download_as_text()
    return yaml.safe_load(config_string)

try:
    config = get_config_from_gcs(GCS_CONFIG_FILE_PATH)
except Exception as e:
    logging.error(f"Failed to load configuration from {GCS_CONFIG_FILE_PATH}: {e}")
    raise

GCP_PROJECT_ID = config["gcp_project_id"]
GCP_REGION = config["gcp_region"]
GCS_STAGING_BUCKET = config["gcs_staging_bucket"]
GCS_BEAM_SCRIPT_PATH = config["gcs_beam_script_path"]
DATAFLOW_SA_EMAIL = f"composer-dataflow-sa@{GCP_PROJECT_ID}.iam.gserviceaccount.com"

# Default arguments for the DAG
default_args = {
    "owner": "Cloud & AI Analytics",
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "dataflow_default_options": {
        "project": GCP_PROJECT_ID,
        "region": GCP_REGION,
        "staging_location": GCS_STAGING_BUCKET + "staging",
        "temp_location": GCS_STAGING_BUCKET + "temp",
        "service_account_email": DATAFLOW_SA_EMAIL,
    },
}

with DAG(
    dag_id="retail_sales_gcs_to_bq",
    default_args=default_args,
    # Cron expression for 00:00 on July 17th every year.
    schedule="0 0 17 7 *",
    catchup=False,
    tags=["Cloud & AI Analytics", "beam", "dataflow"],
    doc_md="""
    ### Cloud & AI Analytics Beam Dataflow Pipeline

    This DAG runs a simple Apache Beam script on Google Cloud Dataflow, reading data from GCS bucket, implementing business logic via dataflow Python Beam SDK and writing the transaformed data to BigQuery.
    """,
) as dag:
    start_pipeline = EmptyOperator(
        task_id="start_pipeline",
    )

    # Note: For this BashOperator to work, the Beam script must be available
    # on the Airflow worker's local filesystem. A common practice is to place it
    # in the 'data' folder of your Composer bucket, which is mounted at
    # /home/airflow/gcs/data/.
    run_beam_job_via_bash = BashOperator(
        task_id="run_beam_job_via_bash",
        bash_command=(
            # Assuming the script is in the 'data' folder of the Composer bucket
            f"python {GCS_BEAM_SCRIPT_PATH} "
            f"--runner=DataflowRunner "
            f"--project={GCP_PROJECT_ID} "
            f"--region={GCP_REGION} "
            f"--staging_location={GCS_STAGING_BUCKET}staging "
            f"--temp_location={GCS_STAGING_BUCKET}temp "
            f"--job_name=retail-gcs-to-bq-bash-{'{{ ds_nodash }}'} "
            f"--service_account_email={DATAFLOW_SA_EMAIL} "
            f"--config_file={GCS_CONFIG_FILE_PATH}"
        )
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline",
    )

    start_pipeline >> run_beam_job_via_bash >> end_pipeline
