# use the user's cloud credentials (in .env file) to authenticate to GCP and push data to the user's cloud account

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# TODO : Make sure to you have .env with the provided env names
load_dotenv(dotenv_path='.env')

project_id = os.getenv('PROJECT_ID')
bucket_name = os.getenv('GCP_BUCKET_NAME')
service_account_file_path = os.getenv('GCP_SERVICE_ACCOUNT_KEY')

fastapi_url = os.getenv('FASTAPI_URL')

# for google search:
api_key = os.getenv('API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

google_api_url = 'https://www.googleapis.com/customsearch/v1'

#for medium:
file_name_prefix = 'medium_ai'
no_days_to_search = 30
topic_name = "Artificial Intelligence"
source_dictionary = {
    "Medium_AI": "medium.com"
}