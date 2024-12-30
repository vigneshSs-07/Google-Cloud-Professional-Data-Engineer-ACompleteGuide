

export GOOGLE_CLOUD_PROJECT=lucky-leaf-396003
export REGION=us-east4
export ZONE=us-east4-a
export BUCKET=demodataset-biglake
export CLUSTERNAME=demo-dataproc-cluster-pyspark

#create bucket at run-time
gsutil mb -l ${REGION} gs://${BUCKET}

echo "Creating Dataproc cluster in '$REGION' region"
#gcloud command to create dataproc cluster
gcloud dataproc clusters create ${CLUSTERNAME} \
                --enable-component-gateway \
                --bucket ${BUCKET} \
                --region ${REGION} \
                --zone ${ZONE} \
                --project ${GOOGLE_CLOUD_PROJECT} \
                --single-node \
                --image-version 2.0-debian10 \
                --labels env=dev \
                --initialization-actions=gs://goog-dataproc-initialization-actions-${REGION}/connectors/connectors.sh \
                --metadata bigquery-connector-version=1.2.0 \
                --metadata spark-bigquery-connector-version=0.21.0 \
                --metadata GCS_CONNECTOR_VERSION=2.2.2 
