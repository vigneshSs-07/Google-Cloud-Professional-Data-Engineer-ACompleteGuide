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
GCS_CONFIG_FILE_PATH = "gs://us-central1-gcstobq-df-pipe-d9fbe1b3-bucket/dags/retail_config.yaml"
GCS_BEAM_SCRIPT_PATH = "gs://us-central1-gcstobq-df-pipe-d9fbe1b3-bucket/scripts/gcs_to_bq_beam.py"

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

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "dataflow_default_options": {
        "project": GCP_PROJECT_ID,
        "region": GCP_REGION,
        "staging_location": GCS_STAGING_BUCKET + "staging",
        "temp_location": GCS_STAGING_BUCKET + "temp",
    },
}

with DAG(
    dag_id="retail_sales_gcs_to_bq",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["retail", "beam", "dataflow"],
    doc_md="""
    ### Retail Beam Dataflow Pipeline

    This DAG runs a simple Apache Beam script on Google Cloud Dataflow.
    """,
) as dag:
    start_pipeline = EmptyOperator(
        task_id="start_pipeline",
    )

    # Note: For this BashOperator to work, the Beam script must be available
    # on the Airflow worker's local filesystem. A common practice is to place it
    # in the 'data' folder of your Composer bucket, which is mounted at
    # /home/airflow/gcs/data/.
    # The DataFlowPythonOperator is generally preferred as it can directly use
    # a script from a GCS path.
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
            f"--config_file={GCS_CONFIG_FILE_PATH}"
        )
    )

    end_pipeline = EmptyOperator(
        task_id="end_pipeline",
    )


    start_pipeline >> run_beam_job_via_bash >> end_pipeline
