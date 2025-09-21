## calls arxiv API to fetch data on ML papers 
# note to team: arxiv is where the industry reads state-of-the-art ML papers. we can use this data to find different categories of AI/ML research
# (like voice, computer vision, NLP etc.) and compare this to the economic index data on what kind of tasks people use LLMs for.
# integrate our data sources and send it to GCS
from google.cloud import storage
from dotenv import load_dotenv
from user_definition import *
import arxiv
import json

load_dotenv(dotenv_path='.env')

def arxiv_calls(topic, limit=10):
    # API client
    arx_client = arxiv.Client()

    # Most recent articles matching the topic
    search = arxiv.Search(
      query = topic,
      max_results = limit,
      sort_by = arxiv.SortCriterion.SubmittedDate
    )

    results = arx_client.results(search)

    paper_dict = {}
    for result in results:
        paper_info = {
            "Authors": [author.name for author in result.authors],
            "Published": result.published.strftime("%Y-%m-%d"),
            "Summary": result.summary[:250].strip() + "...",
            "Link": result.entry_id,
        }
        paper_dict[result.title] = paper_info

    return paper_dict

def upload_to_gcs(data):
    # Init client
    client = storage.Client.from_service_account_json(service_account_file_path, project=project_id)

    # Convert dic to JSON
    json_data = json.dumps(data)
    
    # Fetch bucket and list blobs
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('arxiv_papers')
    blob.upload_from_string(json_data)

papers_1 = arxiv_calls("NLP")
papers_2 = arxiv_calls("GenAI")
upload_to_gcs(papers_1)
upload_to_gcs(papers_2)