# integrate our data sources and send it to GCS
from google.cloud import storage
import os
from dotenv import load_dotenv
from user_definition import *

load_dotenv(dotenv_path='.env')

# 1 authenticate to GCS
# Init client
client = storage.Client.from_service_account_json(service_account_file_path, project=project_id)

# Fetch bucket and list blobs
bucket = client.get_bucket(bucket_name)
for blob in bucket.list_blobs():
    print(blob.name)

# Download a file example
blob = bucket.blob("anthropic-ei/aei_raw_1p_api_2025-08-04_to_2025-08-11.csv")
blob.download_to_filename("local_file.txt")
