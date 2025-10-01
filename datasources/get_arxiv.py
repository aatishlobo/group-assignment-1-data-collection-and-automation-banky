## calls arxiv API to fetch data on ML papers 
# note to team: arxiv is where the industry reads state-of-the-art ML papers. we can use this data to find different categories of AI/ML research
# (like voice, computer vision, NLP etc.) and compare this to the economic index data on what kind of tasks people use LLMs for.
import arxiv
import os
import sys

# Add current directory to path to import user_definition
sys.path.append(os.path.dirname(__file__))
from user_definition import *

def search_arxiv_papers(topic, limit=10):
    # API client
    arx_client = arxiv.Client()

    # Most recent articles matching the topic
    search = arxiv.Search(
      query = topic,
      max_results = limit,
      sort_by = arxiv.SortCriterion.SubmittedDate
    )

    results = arx_client.results(search)

    try:
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
        
    except Exception as e:
        return {"error": f"arXiv search failed: {str(e)}"}