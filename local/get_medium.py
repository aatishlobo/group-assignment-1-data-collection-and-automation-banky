# checkpoint 30/09/2025

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import datetime
from google.oauth2 import service_account
from google.cloud import storage
import json
import os
import sys
from bs4 import BeautifulSoup

# Add current directory to path to import user_definition
sys.path.append(os.path.dirname(__file__))
from user_definition import *

app = FastAPI()


class ArticleSearch(BaseModel):
    url: str
    search_engine_id: str
    api_key: str
    no_days: int
    topic_name: str
    source_dictionary: dict


def scrape_article(url: str) -> dict:
    """Scrape an article page and return its text content."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("title").get_text() if soup.find("title") else "No Title"

        paragraphs = [p.get_text() for p in soup.find_all("p")]
        content = "\n".join(paragraphs)

        return {
            "url": url,
            "title": title,
            "content": content
        }
    except requests.exceptions.RequestException as e:
        return {"url": url, "error": f"Request error: {str(e)}"}
    except Exception as e:
        return {"url": url, "error": f"Unexpected error: {str(e)}"}


@app.post("/search/articles")
def call_google_search(search_param: ArticleSearch):
    """
    Google search → scrape each article → save results to GCS.
    """
    results = []
    
    if not service_account_file_path or not project_id:
        return {"error": "Missing required environment variables: GCP_SERVICE_ACCOUNT_KEY or PROJECT_ID"}
    
    try:
        credentials = service_account.Credentials.from_service_account_file(service_account_file_path)
        client = storage.Client(project=project_id, credentials=credentials)
    except Exception as e:
        return {"error": f"Failed to authenticate with GCP: {str(e)}"}
    
    for start in range(1, 11, 10):
        params = {
            "key": search_param.api_key,
            "cx": search_param.search_engine_id,
            "q": f"{search_param.topic_name}",  
            "dateRestrict": f"d{search_param.no_days}",
            "start": start
        }

        try:
            response = requests.get(search_param.url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Debug: Log the search response
            print(f"Google Search API response status: {response.status_code}")
            print(f"Search query: {params['q']}")
            print(f"Total results found: {data.get('searchInformation', {}).get('totalResults', 'Unknown')}")
            print(f"Items returned: {len(data.get('items', []))}")

            for item in data.get("items", []):
                link = item["link"]
                print(f"Scraping article: {link}")
                article_data = scrape_article(link)
                results.append(article_data)

        except Exception as e:
            error_msg = f"Search API error: {str(e)}"
            print(error_msg)
            results.append({"error": error_msg})

    try:
        bucket = client.bucket(bucket_name)

        file_name = f"medium_ai/medium_ai_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(results, indent=2), content_type="application/json")

        return {
            "topic": search_param.topic_name,
            "scraped_count": len(results),
            "bucket_file": file_name
        }
    except Exception as e:
        return {"message": f"GCS upload failed: {e}"}

