# https://medium.com/google-cloud/apache-spark-and-jupyter-notebooks-made-easy-with-dataproc-component-gateway-fa91d48d6a5a

current_date=$(date '+%Y-%m-%d %H:%M:%S')
echo "ok, Starting now...!, '$current_date'"
echo "required services api's are getting enabled"

#enable apis
gcloud services enable dataproc.googleapis.com \
  compute.googleapis.com \
  storage-component.googleapis.com \
  bigquery.googleapis.com \
  bigquerystorage.googleapis.com  

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
                --master-machine-type n1-standard-4 \
                --master-boot-disk-size 500 \
                --image-version 2.0-debian10 \
                --optional-components JUPYTER \
                --labels env=dev \
                --initialization-actions=gs://goog-dataproc-initialization-actions-${REGION}/connectors/connectors.sh \
                --metadata 'PIP_PACKAGES=mysql-connector-python' \
                --metadata bigquery-connector-version=1.2.0 \
                --metadata spark-bigquery-connector-version=0.21.0 \
                --metadata GCS_CONNECTOR_VERSION=2.2.2  

#Check status 
if [ $? -eq 0 ] 
then
  echo "###########################SUCCESS - Cluster creation is Successful###########################"
else
  echo "***************************FAILURE - Cluster creation is a Failure****************************"
  exit 1
fi 

#Submit PySpark Job
echo "Submitting PySpark Job"

##gcloud command to submit pyspark job in Dataproc cluster
gcloud dataproc jobs submit pyspark gs://demodataset_biglake_dataproc/citibike.py \
                --cluster=${CLUSTERNAME} \
                --region=${REGION} \
                --labels env=dev \
                --jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
                --driver-log-levels root=FATAL \  #List of key value pairs to configure driver logging, where key is a package and value is the log4j log level. For example: root=FATAL,com.example=INFO
                -- ${BUCKET}  #passing argument to pyspark script file  

#Check status 
if [ $? -eq 0 ]
then
  echo "###########################SUCCESS - PySpark Job ran Successfully###########################"
else
  echo "***************************FAILURE - PySpark Job is a Failure*******************************"
  exit 1
fi 

#Submit PySpark Job
echo "Deleting Dataproc Cluster"
#gcloud command to delete dataproc cluster
gcloud dataproc clusters delete ${CLUSTERNAME} \
                --region=${REGION} \
                --quiet

#Check status 
if [ $? -eq 0 ]
then
  echo "###########################SUCCESS - Dataproc cluster deleted Successfully###########################"
else
  echo "***************************FAILURE - Dataproc cluster deletion is a Failure**************************"
  exit 1
fi 
