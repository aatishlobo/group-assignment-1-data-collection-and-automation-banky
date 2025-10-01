from fastapi import FastAPI
from pydantic import BaseModel
import os
import sys

# Add current directory to path to import modules
sys.path.append(os.path.dirname(__file__))
from user_definition import *
from get_medium import search_medium_articles
from get_arxiv import search_arxiv_papers
from gcs_utils import upload_to_gcs

app = FastAPI()


class MediumSearchRequest(BaseModel):
    url: str
    search_engine_id: str
    api_key: str
    no_days: int
    topic_name: str
    source_dictionary: dict


class ArxivSearchRequest(BaseModel):
    topic: str
    limit: int = 10


@app.post("/search/medium")
def search_medium(search_param: MediumSearchRequest):
    """
    Search Medium articles using Google Custom Search API and save to GCS.
    """
    try:
        # Search for articles
        results = search_medium_articles(
            topic_name=search_param.topic_name,
            no_days=search_param.no_days,
            api_key=search_param.api_key,
            search_engine_id=search_param.search_engine_id,
            google_api_url=search_param.url
        )
        
        # Upload to GCS
        upload_result = upload_to_gcs(results, "medium_ai")
        
        if "error" in upload_result:
            return {"error": upload_result["error"]}
        
        return {
            "source": "medium",
            "topic": search_param.topic_name,
            "results_count": len(results),
            "gcs_file": upload_result["file_name"],
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"Medium search failed: {str(e)}"}


@app.post("/search/arxiv")
def search_arxiv(search_param: ArxivSearchRequest):
    """
    Search arXiv papers and save to GCS.
    """
    try:
        # Search for papers
        results = search_arxiv_papers(
            topic=search_param.topic,
            limit=search_param.limit
        )
        
        if "error" in results:
            return {"error": results["error"]}
        
        # Upload to GCS
        upload_result = upload_to_gcs(results, "arxiv_papers", search_param.topic.lower())
        
        if "error" in upload_result:
            return {"error": upload_result["error"]}
        
        return {
            "source": "arxiv",
            "topic": search_param.topic,
            "results_count": len(results),
            "gcs_file": upload_result["file_name"],
            "status": "success"
        }
        
    except Exception as e:
        return {"error": f"arXiv search failed: {str(e)}"}
