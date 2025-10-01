"""
Simple Apache Beam pipeline for retail sales data.
Reads CSV from GCS, applies 2 basic transformations, writes to BigQuery.
"""

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition
from apache_beam.options.pipeline_options import GoogleCloudOptions, PipelineOptions
import logging
import re
import yaml
from google.cloud import bigquery, storage
from google.cloud.exceptions import NotFound


class ConfigOptions(PipelineOptions):
    """Custom options to accept the config file path."""
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--config_file',
            required=True,
            help='GCS path for the YAML configuration file.')


def get_config_from_gcs(gcs_path: str) -> dict:
    """Downloads and parses a YAML configuration file from GCS."""
    logging.info(f"Reading configuration from {gcs_path}")
    match = re.match(r"gs://([^/]+)/(.+)", gcs_path)
    if not match:
        raise ValueError(f"Invalid GCS path provided: {gcs_path}")

    bucket_name, blob_name = match.groups()
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    config_string = blob.download_as_text()
    return yaml.safe_load(config_string)


def parse_tsv(line: str) -> tuple[dict | None, str | None]:
    """Parse a tab-separated line into a dictionary. Returns a tuple of (data, error_message)."""
    try:
        fields = line.split('\t')
        if len(fields) >= 6:
            record = {
                'product_name': fields[0].strip(),
                'category': fields[1].strip(),
                'quantity': int(fields[2]),
                'price': float(fields[3]),
                'customer_id': fields[4].strip(),
                'store_id': fields[5].strip()
            }
            return record, None  # Good record, no error
        return None, f"Invalid number of fields ({len(fields)}) in line: {line}"
    except (ValueError, IndexError) as e:
        return None, f"Error parsing line '{line}': {e}"


def add_total_and_category(record):
    """Apply 2 basic transformations:
    1. Calculate total_amount = quantity * price
    2. Categorize sales as HIGH/MEDIUM/LOW based on total amount
    """
    if record:
        # Transformation 1: Calculate total amount
        total_amount = record['quantity'] * record['price']
        record['total_amount'] = round(total_amount, 2)
        
        # Transformation 2: Categorize sales volume
        if total_amount > 100:
            record['sales_category'] = 'HIGH'
        elif total_amount > 50:
            record['sales_category'] = 'MEDIUM'
        else:
            record['sales_category'] = 'LOW'
    
    return record


def run(argv=None):
    # Parse the config file path argument
    pipeline_options = PipelineOptions(argv)
    config_options = pipeline_options.view_as(ConfigOptions)
    
    # Load configuration from the YAML file in GCS
    config = get_config_from_gcs(config_options.config_file)
    
    # Get project ID from pipeline options for better decoupling.
    # This is passed by the Airflow operator's `dataflow_default_options`.
    gcp_project_id = pipeline_options.view_as(GoogleCloudOptions).project
    if not gcp_project_id:
        raise ValueError("GCP project ID must be specified in pipeline options (e.g., --project).")

    # --- Pre-flight check: Ensure BigQuery dataset exists ---
    dataset_id = config['bq_output_table_dataset']
    try:
        bq_client = bigquery.Client(project=gcp_project_id)
        bq_client.get_dataset(dataset_id)  # API request to check existence
        logging.info(f"Dataset '{dataset_id}' already exists in project '{gcp_project_id}'.")
    except NotFound:
        logging.info(f"Dataset '{dataset_id}' not found in project '{gcp_project_id}'. Creating it...")
        dataset_ref = bigquery.Dataset(f"{gcp_project_id}.{dataset_id}")
        # Set the location for the new dataset.
        # Using the region from config is a good practice.
        dataset_ref.location = config['gcp_region']
        bq_client.create_dataset(dataset_ref, timeout=30)
        logging.info(f"Successfully created dataset '{dataset_id}'.")
    # --- End pre-flight check ---

    # Construct full BQ table spec and other paths from config
    bq_output_table = f"{gcp_project_id}:{config['bq_output_table_dataset']}.{config['bq_output_table_name']}"
    gcs_input_file = config["gcs_input_file"]
    gcs_error_output_prefix = config["gcs_error_output_prefix"]
    table_schema = config["bq_table_schema"]

    with beam.Pipeline(options=pipeline_options) as p:
        # Step 1: Read CSV from GCS
        lines = p | 'Read from GCS' >> ReadFromText(
            gcs_input_file, skip_header_lines=1
        )

        # Step 2: Parse TSV lines and separate good/bad records
        parsed_results = lines | 'Parse TSV' >> beam.Map(parse_tsv).with_outputs(
            'bad_records', main='good_records'
        )

        good_records = parsed_results.good_records
        bad_records = parsed_results.bad_records

        # Step 3: Process good records
        (good_records
         | 'Extract Good Records' >> beam.Map(lambda x: x[0])
         | 'Filter None Records' >> beam.Filter(lambda record: record is not None)
         | 'Add Total and Category' >> beam.Map(add_total_and_category)
         | 'Write to BigQuery' >> WriteToBigQuery(
             table=bq_output_table,
             schema=table_schema,
             create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
             write_disposition=BigQueryDisposition.WRITE_APPEND
         ))

        # Step 4: Process bad records (dead-letter queue)
        (bad_records
         | 'Extract Error Messages' >> beam.Map(lambda x: x[1])
         | 'Write Errors to GCS' >> beam.io.WriteToText(gcs_error_output_prefix))


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
