from fastapi import FastAPI
from pydantic import BaseModel
import requests
import datetime
from user_define_project import *
from google.oauth2 import service_account
from google.cloud import storage
import json
import os
from bs4 import BeautifulSoup

app = FastAPI()


class ArticleSearch(BaseModel):
    url: str
    search_engine_id: str
    api_key: str
    no_days: int
    topic_name: str
    source_dictionary: dict


class GcsStringUpload(BaseModel):
    service_account_key: str
    project_id: str
    bucket_name: str
    file_name: str
    data: str


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
            "content": content[:2000]
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
    key_path = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
    gcp_project_id = os.getenv("PROJECT_ID")

    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = storage.Client(project=gcp_project_id, credentials=credentials)
    
    for start in range(1, 2, 10):
        params = {
            "key": search_param.api_key,
            "cx": search_param.search_engine_id,
            "q": f"{search_param.topic_name} site:medium.com",
            "dateRestrict": f"d{search_param.no_days}",
            "start": start
        }

        try:
            response = requests.get(search_param.url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                link = item["link"]
                article_data = scrape_article(link)
                results.append(article_data)

        except Exception as e:
            results.append({"error": str(e)})

    try:
        bucket = client.bucket(os.getenv("GCP_BUCKET_NAME"))

        file_name = f"medium_ai_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(results, indent=2), content_type="application/json")

        return {
            "topic": search_param.topic_name,
            "scraped_count": len(results),
            "bucket_file": file_name
        }
    except Exception as e:
        return {"message": f"GCS upload failed: {e}"}


@app.put("/save_to_gcs")
def save_to_gcs(gcs_upload_param: GcsStringUpload):
    """Save any string (HTML/text) to GCS."""
    credentials = service_account.Credentials.from_service_account_file(
        gcs_upload_param.service_account_key
    )
    client = storage.Client(
        project=gcs_upload_param.project_id, credentials=credentials
    )
    bucket = client.bucket(gcs_upload_param.bucket_name)
    file = bucket.blob(gcs_upload_param.file_name)
    file.upload_from_string(gcs_upload_param.data)
    return {"message": f"{gcs_upload_param.file_name} saved to {gcs_upload_param.bucket_name}"}
