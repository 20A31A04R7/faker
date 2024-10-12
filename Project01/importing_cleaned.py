import os

from google.cloud import storage
from google.oauth2 import service_account


def upload_csv_to_gcs(bucket_name, source_file_name, destination_blob_name):
    try:
        # Get the credentials path from the environment variable
        key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

        # Load the credentials directly from the JSON key file
        credentials = service_account.Credentials.from_service_account_file(key_path)

        # Initialize the storage client with the specified credentials
        storage_client = storage.Client(credentials=credentials)

        # Get the bucket and upload the file
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        print(f"File {source_file_name} uploaded to {bucket_name}/{destination_blob_name}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    upload_csv_to_gcs("e-commerce_02", "ECommerce_generated_data.csv", "ECommerce_generated_data.csv")
