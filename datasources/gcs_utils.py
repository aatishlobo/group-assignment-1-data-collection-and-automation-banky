import json
import datetime
from google.oauth2 import service_account
from google.cloud import storage
import os
import sys

# Add current directory to path to import user_definition
sys.path.append(os.path.dirname(__file__))
from user_definition import *


def get_gcs_client():
    """
    Get a GCS client that works both locally and in cloud deployment.
    
    Returns:
        storage.Client: Authenticated GCS client
    """
    try:
        # Check if we have a service account file path and it exists
        if service_account_file_path and service_account_file_path.strip() and os.path.exists(service_account_file_path):
            # Local docker: use mounted service account key file
            print(f"Using service account key file: {service_account_file_path}")
            credentials = service_account.Credentials.from_service_account_file(service_account_file_path)
            return storage.Client(project=project_id, credentials=credentials)
        else:
            # Cloud deployment: use default identity (no key file needed)
            if service_account_file_path:
                print(f"Service account file path set but file not found: {service_account_file_path}")
            print("Using default cloud identity (no service account key file)")
            return storage.Client(project=project_id)
    except Exception as e:
        print(f"Error creating GCS client: {str(e)}")
        # Fallback to default identity
        print("Falling back to default cloud identity")
        return storage.Client(project=project_id)


def upload_to_gcs(data, folder_prefix, file_suffix=""):
    """
    Upload data to Google Cloud Storage.
    
    Args:
        data: The data to upload (will be converted to JSON)
        folder_prefix: Folder name in GCS (e.g., 'medium_ai', 'arxiv_papers')
        file_suffix: Optional suffix for filename (e.g., topic name)
    
    Returns:
        dict: Success/error response with file information
    """
    try:
        # Validate required environment variables
        if not bucket_name:
            return {"error": "Missing required environment variable: GCP_BUCKET_NAME"}
        
        # Get authenticated GCS client (works for both local and cloud)
        client = get_gcs_client()
        
        # Get bucket
        bucket = client.bucket(bucket_name)
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        if file_suffix:
            file_name = f"{folder_prefix}/{folder_prefix}_{file_suffix}_{timestamp}.json"
        else:
            file_name = f"{folder_prefix}/{folder_prefix}_{timestamp}.json"
        
        # Upload data
        blob = bucket.blob(file_name)
        json_data = json.dumps(data, indent=2)
        blob.upload_from_string(json_data, content_type="application/json")
        
        return {
            "success": True,
            "file_name": file_name,
            "bucket_name": bucket_name,
            "data_size": len(json_data)
        }
        
    except Exception as e:
        return {"error": f"GCS upload failed: {str(e)}"}
