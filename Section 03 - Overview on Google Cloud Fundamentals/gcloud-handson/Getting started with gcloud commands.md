# 🧰 Google Cloud CLI (`gcloud`) Commands Cheat Sheet

The `gcloud` CLI is the main tool for managing Google Cloud Platform (GCP) resources from the command line.

## 📋 Project Configuration
```bash
export PROJECT_ID="soy-sound-475700-v9"
export REGION="us-east4"
export ZONE="us-east4-b"
```

---

## ⚙️ Setup & Configuration
```bash
# Initialize gcloud CLI
gcloud init

# Authenticate user
gcloud auth login

# Set default project
gcloud config set project $PROJECT_ID

# List current configuration
gcloud config list

# List all configurations
gcloud config configurations list

# Display system information
gcloud info
```

---

## 🏗️ Projects & Billing
```bash
# List all projects
gcloud projects list

# Get project details
gcloud projects describe $PROJECT_ID

# Create new project
gcloud projects create $PROJECT_ID --name="My Project"

# Link billing account to project
gcloud beta billing projects link $PROJECT_ID --billing-account=ACCOUNT_ID

# List billing accounts
gcloud beta billing accounts list
```

---

## 🌍 Region and Zone Management
```bash
# List available regions
gcloud compute regions list

# List available zones
gcloud compute zones list

# Set default region
gcloud config set compute/region $REGION

# Set default zone
gcloud config set compute/zone $ZONE

# Get current region/zone settings
gcloud config get-value compute/region
gcloud config get-value compute/zone
```

---

## ☁️ Compute Engine (VMs, Disks, Networks)
```bash
# List all instances
gcloud compute instances list

# Create VM instance
gcloud compute instances create INSTANCE_NAME \
  --zone=$ZONE \
  --machine-type=e2-medium \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --boot-disk-size=10GB \
  --boot-disk-type=pd-standard

# SSH into instance
gcloud compute ssh INSTANCE_NAME --zone=$ZONE

# Stop instance
gcloud compute instances stop INSTANCE_NAME --zone=$ZONE

# Start instance
gcloud compute instances start INSTANCE_NAME --zone=$ZONE

# Delete instance
gcloud compute instances delete INSTANCE_NAME --zone=$ZONE

# List machine types
gcloud compute machine-types list --zones=$ZONE

# List images
gcloud compute images list
```

---

## 🪣 Cloud Storage (GCS)
```bash
# List all buckets
gcloud storage buckets list

# Create bucket
gcloud storage buckets create gs://BUCKET_NAME --location=$REGION

# List bucket contents
gcloud storage ls gs://BUCKET_NAME/

# Copy file to bucket
gcloud storage cp localfile.txt gs://BUCKET_NAME/

# Copy file from bucket
gcloud storage cp gs://BUCKET_NAME/file.txt ./

# Sync directory
gcloud storage rsync ./local-dir gs://BUCKET_NAME/remote-dir

# Remove file
gcloud storage rm gs://BUCKET_NAME/file.txt

# Remove bucket (with all contents)
gcloud storage rm -r gs://BUCKET_NAME

# Make bucket public
gcloud storage buckets add-iam-policy-binding gs://BUCKET_NAME \
  --member=allUsers \
  --role=roles/storage.objectViewer
```

---

## 🧠 BigQuery
```bash
# List datasets
gcloud bigquery datasets list

# Create dataset
gcloud bigquery datasets create DATASET_ID --location=$REGION

# List tables in dataset
gcloud bigquery tables list DATASET_ID

# Run query
gcloud bigquery query --use_legacy_sql=false \
  "SELECT name, COUNT(*) FROM \`$PROJECT_ID.DATASET_ID.TABLE_ID\` GROUP BY name"

# Load data from GCS
gcloud bigquery load DATASET_ID.TABLE_ID \
  gs://BUCKET_NAME/data.csv \
  schema.json

# Export table to GCS
gcloud bigquery extract DATASET_ID.TABLE_ID gs://BUCKET_NAME/export.csv

# Delete dataset
gcloud bigquery datasets delete DATASET_ID
```

---

## 🔐 IAM (Identity & Access Management)
```bash
# List IAM roles
gcloud iam roles list

# Add IAM policy binding
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="user:example@gmail.com" \
  --role="roles/viewer"

# Remove IAM policy binding
gcloud projects remove-iam-policy-binding $PROJECT_ID \
  --member="user:example@gmail.com" \
  --role="roles/viewer"

# Get IAM policy for project
gcloud projects get-iam-policy $PROJECT_ID

# List service accounts
gcloud iam service-accounts list

# Create service account
gcloud iam service-accounts create SERVICE_ACCOUNT_NAME \
  --display-name="My Service Account"

# Generate service account key
gcloud iam service-accounts keys create key.json \
  --iam-account=SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com
```

---

## 🔄 Cloud Functions
```bash
# List functions
gcloud functions list

# Deploy function
gcloud functions deploy FUNCTION_NAME \
  --runtime=python39 \
  --trigger-http \
  --allow-unauthenticated \
  --region=$REGION

# Call function
gcloud functions call FUNCTION_NAME --region=$REGION

# Delete function
gcloud functions delete FUNCTION_NAME --region=$REGION
```

---

## 🚀 Cloud Run
```bash
# List services
gcloud run services list

# Deploy service
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/$PROJECT_ID/IMAGE_NAME \
  --region=$REGION \
  --allow-unauthenticated

# Get service URL
gcloud run services describe SERVICE_NAME --region=$REGION --format="value(status.url)"

# Delete service
gcloud run services delete SERVICE_NAME --region=$REGION
```

---

## 📊 Cloud Pub/Sub
```bash
# List topics
gcloud pubsub topics list

# Create topic
gcloud pubsub topics create TOPIC_NAME

# Publish message
gcloud pubsub topics publish TOPIC_NAME --message="Hello World"

# List subscriptions
gcloud pubsub subscriptions list

# Create subscription
gcloud pubsub subscriptions create SUBSCRIPTION_NAME --topic=TOPIC_NAME

# Pull messages
gcloud pubsub subscriptions pull SUBSCRIPTION_NAME --auto-ack
```

---

## 🧰 Services & APIs
```bash
# List available services
gcloud services list --available

# List enabled services
gcloud services list --enabled

# Enable service
gcloud services enable compute.googleapis.com

# Disable service
gcloud services disable dataflow.googleapis.com
```

---

## 🔍 Logging & Monitoring
```bash
# View logs
gcloud logging logs list

# Read logs
gcloud logging read "resource.type=gce_instance" --limit=10

# Create log-based metric
gcloud logging metrics create METRIC_NAME \
  --description="My metric" \
  --log-filter="resource.type=gce_instance"
```

---

## 🛠️ Helpful Commands
```bash
# Get help for any command
gcloud COMMAND --help

# Set verbosity level
gcloud COMMAND --verbosity=debug

# Output in different formats
gcloud COMMAND --format=json
gcloud COMMAND --format=yaml
gcloud COMMAND --format=table

# Filter output
gcloud compute instances list --filter="zone:us-central1-a"

# Sort output
gcloud compute instances list --sort-by=name

# Use configuration files
gcloud config configurations create dev-config
gcloud config configurations activate dev-config
```