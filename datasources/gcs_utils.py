import json
import datetime
from google.oauth2 import service_account
from google.cloud import storage
import os
import sys

# Add current directory to path to import user_definition
sys.path.append(os.path.dirname(__file__))
from user_definition import *


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
        if not service_account_file_path or not project_id or not bucket_name:
            return {"error": "Missing required environment variables: GCP_SERVICE_ACCOUNT_KEY, PROJECT_ID, or GCP_BUCKET_NAME"}
        
        # Authenticate with GCP
        credentials = service_account.Credentials.from_service_account_file(service_account_file_path)
        client = storage.Client(project=project_id, credentials=credentials)
        
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
