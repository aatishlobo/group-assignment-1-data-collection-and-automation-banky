import datetime
import json
import requests
import sys
import os
from dotenv import load_dotenv

# Add the datasources directory to Python path BEFORE importing
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'datasources'))
from user_definition import *

load_dotenv(dotenv_path=".env")

search_data = {
    "url": google_api_url,
    "search_engine_id": search_engine_id,
    "api_key": api_key,
    "no_days": no_days_to_search,
    "topic_name": topic_name,
    "source_dictionary": source_dictionary
}

search_response = requests.post(f"{fastapi_url}/search/articles", json=search_data, timeout=30)
print(f"search_response status: {search_response.status_code}")

# Check if the response is successful and contains JSON
if search_response.status_code == 200:
    try:
        results = search_response.json()
        print("Success! Search completed and data uploaded to GCS.")
        print(f"Topic: {results.get('topic', 'N/A')}")
        print(f"Articles scraped: {results.get('scraped_count', 'N/A')}")
        print(f"GCS file: {results.get('bucket_file', 'N/A')}")
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not valid JSON")
        print(f"Response text: {search_response.text}")
        exit(1)
else:
    print(f"Error: API request failed with status {search_response.status_code}")
    print(f"Response text: {search_response.text}")
    exit(1)
