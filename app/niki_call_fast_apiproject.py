import datetime
import json
import requests
from dotenv import load_dotenv
from user_define_project import *

load_dotenv(dotenv_path=".env.project")

search_data = {
    "url": google_api_url,
    "search_engine_id": search_engine_id,
    "api_key": api_key,
    "no_days": no_days_to_search,
    "topic_name": topic_name,
    "source_dictionary": source_dictionary
}

search_response = requests.post(f"{api_server_url}/search/articles", json=search_data, timeout=30)
print(f"search_response status: {search_response.status_code}")

results = search_response.json()

metadata_file = f"{file_name_prefix}/{datetime.date.today()}_metadata.json"

upload_payload = {
    "service_account_key": service_account_file_path,
    "project_id": project_id,
    "bucket_name": bucket_name,
    "file_name": metadata_file,
    "data": json.dumps(results, indent=4)
}

upload_response = requests.put(f"{api_server_url}/save_to_gcs", json=upload_payload, timeout=30)
print(f"upload_response status: {upload_response.status_code}")
