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

# Search Medium articles
print("=== Searching Medium Articles ===")
medium_response = requests.post(f"{fastapi_url}/search/medium", json=search_data, timeout=30)
print(f"Medium search response status: {medium_response.status_code}")

if medium_response.status_code == 200:
    try:
        results = medium_response.json()
        print("Success! Medium search completed and data uploaded to GCS.")
        print(f"Source: {results.get('source', 'N/A')}")
        print(f"Topic: {results.get('topic', 'N/A')}")
        print(f"Results count: {results.get('results_count', 'N/A')}")
        print(f"GCS file: {results.get('gcs_file', 'N/A')}")
    except requests.exceptions.JSONDecodeError:
        print("Error: Medium response is not valid JSON")
        print(f"Response text: {medium_response.text}")
else:
    print(f"Error: Medium API request failed with status {medium_response.status_code}")
    print(f"Response text: {medium_response.text}")

print("\n=== Searching arXiv Papers ===")
# Search arXiv papers
arxiv_data = {
    "topic": topic_name,
    "limit": 10
}

arxiv_response = requests.post(f"{fastapi_url}/search/arxiv", json=arxiv_data, timeout=30)
print(f"arXiv search response status: {arxiv_response.status_code}")

if arxiv_response.status_code == 200:
    try:
        results = arxiv_response.json()
        print("Success! arXiv search completed and data uploaded to GCS.")
        print(f"Source: {results.get('source', 'N/A')}")
        print(f"Topic: {results.get('topic', 'N/A')}")
        print(f"Results count: {results.get('results_count', 'N/A')}")
        print(f"GCS file: {results.get('gcs_file', 'N/A')}")
    except requests.exceptions.JSONDecodeError:
        print("Error: arXiv response is not valid JSON")
        print(f"Response text: {arxiv_response.text}")
else:
    print(f"Error: arXiv API request failed with status {arxiv_response.status_code}")
    print(f"Response text: {arxiv_response.text}")
