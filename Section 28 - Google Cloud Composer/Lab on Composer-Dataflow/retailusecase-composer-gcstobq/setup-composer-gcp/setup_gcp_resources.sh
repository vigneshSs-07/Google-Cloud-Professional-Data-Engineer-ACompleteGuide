#!/bin/bash

# This script automates the setup of GCP resources for the retail data pipeline.
# It enables necessary APIs, creates a GCS bucket, and a BigQuery dataset.

# --- Configuration ---
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
BUCKET_NAME="${PROJECT_ID}-data-bucket" #poised-team-467209-a1-data-bucket
BQ_DATASET_ID="retail_dataset"
SA_NAME="composer-dataflow-sa"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- GCP Resource Setup ---"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Bucket: $BUCKET_NAME"
echo "BigQuery Dataset: $BQ_DATASET_ID"
echo "Service Account: $SA_EMAIL"
echo "--------------------------"

# --- Set GCP Project ---
echo "1. Setting GCP project to '$PROJECT_ID'..."
gcloud config set project "$PROJECT_ID"
echo "✅ Project set successfully."
echo

# --- Enable APIs ---
echo "2. Enabling required GCP APIs..."
gcloud services enable \
    composer.googleapis.com \
    dataflow.googleapis.com \
    storage-component.googleapis.com \
    logging.googleapis.com \
    bigquery.googleapis.com
echo "✅ APIs enabled successfully."
echo

# --- Create GCS Bucket ---
echo "3. Checking for GCS bucket 'gs://$BUCKET_NAME'..."
# Check if the bucket already exists. The command will have a non-zero exit code if it doesn't.
if gcloud storage buckets describe "gs://$BUCKET_NAME" &>/dev/null; then
    echo "✅ Bucket 'gs://$BUCKET_NAME' already exists. Skipping creation."
else
    echo "   Bucket not found. Creating 'gs://$BUCKET_NAME' in '$REGION'..."
    gcloud storage buckets create "gs://$BUCKET_NAME" --location="$REGION"
    echo "✅ Bucket created successfully."
fi
echo

echo "5. Checking for Service Account '$SA_NAME'..."
# Check if the service account already exists
if gcloud iam service-accounts describe "$SA_EMAIL" &>/dev/null; then
    echo "✅ Service Account '$SA_EMAIL' already exists. Skipping creation."
else
    echo "   Service Account not found. Creating..."
    gcloud iam service-accounts create "$SA_NAME" \
        --display-name="Service Account for Composer and Dataflow"
    echo "✅ Service Account created successfully."
fi
echo

echo "6. Granting IAM roles to the Service Account..."

# Grant roles required for Composer, Dataflow, GCS, and BigQuery
echo "   - Granting roles/composer.worker..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/composer.worker" --condition=None >/dev/null

echo "   - Granting roles/dataflow.admin..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/dataflow.admin" --condition=None >/dev/null

echo "   - Granting roles/dataflow.worker..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/dataflow.worker" --condition=None >/dev/null

echo "   - Granting roles/storage.objectAdmin..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/storage.objectAdmin" --condition=None >/dev/null

echo "   - Granting roles/bigquery.dataEditor and roles/bigquery.jobUser..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/bigquery.dataEditor" --condition=None >/dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/bigquery.jobUser" --condition=None >/dev/null

echo "✅ IAM roles granted successfully."
echo


# Get your project ID and the service account email
USER_EMAIL="azurelearndemo@gmail.com" 
echo " 6 - Granting Individual user roles to the Service Account..."
# Grant your user account the ability to "act as" the service account
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
    --member="user:$USER_EMAIL" \
    --role="roles/iam.serviceAccountUser"

echo "Granted user '$USER_EMAIL' the Service Account User role on '$SA_EMAIL'."
echo

echo "  7 - Granting Service Account the ability to act as itself..."
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/iam.serviceAccountUser"
echo "Granted user '$SA_EMAIL' the Service Account User role on '$SA_EMAIL'."
echo "✅ Granted Service Account User role to itself."
echo

# echo "7. Calling script to create the Composer environment..."
# ./gcloud_composer_create.sh
# echo "✅ Composer env created successfully."
# echo

echo "--- ✨ Full environment setup is complete! ✨ ---"
