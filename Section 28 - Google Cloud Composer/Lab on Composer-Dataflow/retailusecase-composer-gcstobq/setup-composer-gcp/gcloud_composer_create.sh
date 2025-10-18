#!/bin/bash
# This script creates a Cloud Composer environment optimized for real-time data processing.

# --- Configuration ---
ENVIRONMENT_NAME="demo-composer3-env"
PROJECT_ID=$(gcloud config get-value project)
SERVICE_ACCOUNT="composer-dataflow-sa@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud composer environments create "$ENVIRONMENT_NAME" \
  --location=us-central1 \
  --image-version=composer-3-airflow-2.10.5-build.16 \
  --service-account="$SERVICE_ACCOUNT" \
  --project="$PROJECT_ID" \
  --labels=env=dev,team=cloudaianalytics \
  --enable-high-resilience \
  --environment-size=medium \
  --scheduler-count=2 \
  --scheduler-cpu=1 \
  --scheduler-memory=4GB \
  --scheduler-storage=5GB \
  --dag-processor-cpu=4 \
  --dag-processor-memory=7GB \
  --triggerer-count=2 \
  --triggerer-cpu=0.5 \
  --triggerer-memory=1GB \
  --web-server-cpu=2 \
  --web-server-memory=7GB \
  --web-server-storage=5GB \
  --min-workers=3 \
  --worker-cpu=2 \
  --worker-memory=7GB \
  --worker-storage=10GB \
  --no-enable-private-environment \
  --web-server-allow-all \
  --support-web-server-plugins \
  --disable-cloud-data-lineage-integration \
  --airflow-database-retention-days=0


