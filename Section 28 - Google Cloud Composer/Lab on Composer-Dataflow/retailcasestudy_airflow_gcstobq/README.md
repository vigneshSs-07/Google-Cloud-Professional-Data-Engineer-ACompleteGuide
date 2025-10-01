# Retail Sales Data Pipeline (GCS to BigQuery via Dataflow)

This project demonstrates a simple, scalable ETL (Extract, Transform, Load) pipeline built on Google Cloud Platform. It processes retail sales data from a tab-separated values (TSV) file stored in Google Cloud Storage (GCS), performs transformations using an Apache Beam pipeline running on Cloud Dataflow, and loads the processed data into a BigQuery table. The entire workflow is orchestrated by an Airflow DAG running in a Cloud Composer environment.

## Project Overview

The pipeline performs the following steps:
1.  **Extract**: Reads raw sales data from a TSV file in a GCS bucket.
2.  **Transform**:
    *   Parses each tab-separated row.
    *   Validates the data and separates malformed records into a dead-letter queue (another GCS location).
    *   For valid records, it calculates the `total_amount` for each sale (`quantity * price`).
    *   Categorizes each sale as `HIGH`, `MEDIUM`, or `LOW` based on the `total_amount`.
3.  **Load**:
    *   Writes the transformed, enriched data to a specified BigQuery table.
    *   Writes any parsing errors to a text file in GCS for later analysis.

The entire process is triggered and managed by an Airflow DAG.

## Components

### 1. Apache Beam Pipeline (`gcs_to_bq_beam.py`)

This is the core data processing script. It's written in Python using the Apache Beam SDK.

-   **Dynamic Configuration**: The pipeline doesn't use hardcoded paths. Instead, it accepts a GCS path to a YAML configuration file (`--config_file`) as a command-line argument. This makes the pipeline flexible and reusable.
-   **Error Handling**: Implements a dead-letter pattern using `with_outputs`. Good records are sent to the main processing branch, while bad records (e.g., incorrect number of columns, type conversion errors) are routed to a separate branch that writes them to GCS.
-   **Transformations**: Includes functions to calculate new fields (`total_amount`, `sales_category`).
-   **Pre-flight Checks**: Before running the main pipeline, the script connects to BigQuery to check if the target dataset exists. If not, it creates it automatically, making the pipeline more robust and self-sufficient.
-   **Sink**: Writes the final `PCollection` of records to BigQuery using `WriteToBigQuery`.

### 2. Airflow DAG (`dag_beam_gcstobq.py`)

This Python script defines the orchestration logic using Apache Airflow.

-   **Orchestration**: Defines a DAG named `retail_sales_gcs_to_bq`.
-   **Configuration Loading**: The DAG itself reads the same central `retail_config.yaml` from GCS to get parameters like project ID, region, and GCS paths. This ensures consistency between the orchestration layer and the execution layer.
-   **Job Invocation**: Uses the `BashOperator` to launch the Beam script as a Dataflow job. The Beam script must be present on the local filesystem of the Airflow worker. The recommended practice, followed here, is to place the script in the Composer bucket's `data` folder, which is automatically mounted on the workers.
-   **Templating**: The Dataflow job name is templated with the execution date (`{{ ds_nodash }}`) to ensure uniqueness.

### 3. Configuration File (`retail_config.yaml`)

A single source of truth for all pipeline settings. This externalizes configuration from the code, which is a best practice.

-   **GCP Settings**: `gcp_project_id`, `gcp_region`.
-   **GCS Paths**: Locations for the input data, error logs, and Dataflow staging/temp files.
-   **BigQuery Details**: The target dataset, table name, and the complete table schema.

## Prerequisites

-   A Google Cloud Project.
-   Enabled APIs: Cloud Composer, Dataflow, BigQuery, Cloud Storage.
-   A Cloud Composer environment.
-   A GCS bucket for storing data, scripts, and temporary files.
-   `gcloud` CLI and permissions to manage the services above.

## How to Run

### Step 1: Configure `retail_config.yaml`

Modify `retail_config.yaml` with your specific GCP project details and GCS bucket name.

```yaml
gcp_project_id: "your-gcp-project-id"
gcp_region: "us-central1"

gcs_staging_bucket: "gs://your-gcs-bucket/"
# ... and other paths
```

### Step 2: Upload Artifacts to GCS

1.  **Upload the configuration file**:
    ```sh
    gsutil cp retail_config.yaml gs://your-gcs-bucket/config/retail_config.yaml
    ```
    *(Note: The DAG `dag_beam_gcstobq.py` is hardcoded to look for the config at `gs://us-central1-gcstobq-df-pipe-d9fbe1b3-bucket/dags/retail_config.yaml`. You must update the `GCS_CONFIG_FILE_PATH` variable in the DAG if you use a different location.)*

2.  **Upload the Beam script**:
    ```sh
    gsutil cp gcs_to_bq_beam.py gs://your-composer-bucket/data/gcs_to_bq_beam.py
    ```
    *(Note: The script **must** be placed in the `data` folder of your Composer environment's bucket. This folder is mounted at `/home/airflow/gcs/data/` on the Airflow workers, which is the path the `BashOperator` uses to execute the script.)*

3.  **Upload sample input data**: Create a `sales_data.csv` file and upload it to the location specified by `gcs_input_file` in your config.
    *(Note: The file is named `.csv` but its content must be tab-separated).*
    ```tsv
    product_name	category	quantity	price	customer_id	store_id
    Laptop	Electronics	1	1200.50	CUST001	STORE01
    Coffee Mug	Kitchenware	2	15.00	CUST002	STORE02
    T-Shirt	Apparel	3	25.75	CUST001	STORE03
    Invalid,Record # This line has too few fields and will be sent to the error log.
    ```
    ```sh
    gsutil cp sales_data.csv gs://your-gcs-bucket/sales_data.csv
    ```

### Step 3: Deploy and Trigger the DAG

1.  **Upload the DAG file** to your Cloud Composer environment's `dags` folder.
    ```sh
    gcloud composer environments storage dags import \
        --environment your-composer-environment-name \
        --location your-composer-region \
        --source dag_beam_gcstobq.py
    ```

2.  **Trigger the DAG** from the Airflow UI. Once the DAG run completes, you can verify:
    -   The processed data in your BigQuery table (`retail_dataset.sales_summary_data`).
    -   The error file (`bad_records-xxxxx-of-xxxxx`) in the GCS error prefix location, containing the "Invalid,Record" line.