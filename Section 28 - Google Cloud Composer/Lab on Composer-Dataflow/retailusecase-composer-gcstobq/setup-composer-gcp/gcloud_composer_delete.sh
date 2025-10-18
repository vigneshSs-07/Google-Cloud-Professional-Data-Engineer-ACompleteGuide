# --- Configuration ---
ENVIRONMENT_NAME="demo-composer3-env"
PROJECT_ID=$(gcloud config get-value project)

gcloud composer environments delete "$ENVIRONMENT_NAME" \
  --location=us-central1 --quiet
