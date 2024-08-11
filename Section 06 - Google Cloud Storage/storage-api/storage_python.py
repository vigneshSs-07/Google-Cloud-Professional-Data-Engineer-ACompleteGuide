from google.cloud import storage
from google.oauth2 import service_account
import sys

key_path= "/home/cloudaianalytics/zinc-forge-380121-84014d2f4a21.json"
project_id="zinc-forge-380121"


def create_bucket(storage_client,bucket_name):
    """Creates a new bucket."""
    # bucket_name = "your-new-bucket-name"

    # storage_client = storage.Client()

    bucket = storage_client.create_bucket(bucket_name)

    print(f"Bucket {bucket.name} created")


def get_bucket_metadata(storage_client ,bucket_name):
    bucket = client.get_bucket(bucket_name)

    print("Bucket name: {}".format(bucket.name))
    print("Bucket location: {}".format(bucket.location))
    print("Bucket storage class: {}".format(bucket.storage_class))


def list_buckets(storage_client ,bucket_name):
    """Lists all buckets."""

    # storage_client = storage_client.create_bucket(bucket_name)
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print("The buckets present are {} ", bucket.name)


def create_bucket_dual_region(bucket_name, location, region_1, region_2):
    """Creates a Dual-Region Bucket with provided location and regions.."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The bucket's pair of regions. Case-insensitive.
    # See this documentation for other valid locations:
    # https://cloud.google.com/storage/docs/locations
    # region_1 = "US-EAST1"
    # region_2 = "US-WEST1"
    # location = "US"

    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name, location=location, data_locations=[region_1, region_2])

    print(f"Created bucket {bucket_name}")
    print(f" - location: {bucket.location}")
    print(f" - location_type: {bucket.location_type}")
    print(f" - customPlacementConfig data_locations: {bucket.data_locations}")


def create_bucket_class_location(bucket_name):
    """
    Create a new bucket in the US region with the coldline storage
    class
    """
    # bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket


def upload_blob(client,bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    # storage_client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the file should be downloaded
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )

def delete_bucket(storage_client ,bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    # storage_client = storage_client.create_bucket(bucket_name)

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print(f"Bucket {bucket.name} deleted")


def delete_blob(bucket_name, blob_name, credentials,project_id ):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client(credentials=credentials, project=project_id)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to delete is aborted if the object's
    # generation number does not match your precondition.
    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation

    blob.delete(if_generation_match=generation_match_precondition)

    print(f"Blob {blob_name} deleted.")


def enable_versioning(bucket_name):
    """Enable versioning for this bucket."""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.versioning_enabled = True
    bucket.patch()

    print(f"Versioning was enabled for bucket {bucket.name}")
    return 

def enable_uniform_bucket_level_access(bucket_name):
    """Enable uniform bucket-level access for a bucket"""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    bucket.iam_configuration.uniform_bucket_level_access_enabled = True
    bucket.patch()

    print(
        f"Uniform bucket-level access was enabled for {bucket.name}."
    )

def disable_versioning(bucket_name):
    """Disable versioning for this bucket."""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.versioning_enabled = False
    bucket.patch()

    print(f"Versioning was disabled for bucket {bucket}")
    return bucket 


if __name__ == "__main__":
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
    bucket_name = "demo-kf-pde-001"
    client = storage.Client(credentials=credentials, project=project_id)
    # create_bucket(client,bucket_name)
    # source_file_name = "/home/cloudaianalytics/wordcount.py" 
    # destination_blob_name = "wordcount_file"
    # upload_blob(client,bucket_name, source_file_name, destination_blob_name)
    # list_buckets(client ,bucket_name)
    blob_name="wordcount_file"
    project=project_id
    # delete_blob(bucket_name, blob_name, credentials,project_id )
    delete_bucket(client,bucket_name)
    