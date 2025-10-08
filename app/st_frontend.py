# streamlit frontend

import json

import pandas as pd

from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
import pandas as pd

from user_definition import *
from gcs_utils import *
from gemini_summary import *


def retrieve_data_from_gcs(
                            # service_account_key: str,
                            # project_id: str,
                            # bucket_name: str,
                            # file_name_prefix: str
                            folder_prefix
                           ):

    credentials = service_account.Credentials.from_service_account_file(service_account_file_path)
    client = storage.Client(project=project_id, credentials=credentials)
    print("client built")
    bucket = client.bucket(bucket_name)
    print("bucket found")
    # blobs = bucket.list_blobs()

    blobs = bucket.list_blobs(prefix=folder_prefix)
    print("buckets listed")

    section_output = {}

    i = 0
    for blob in blobs:
        print(blob.name)

        if blob.name.endswith('/'):
            continue

        if folder_prefix == "arxiv_papers":
            file_contents = blob.download_as_text()
            data = json.loads(file_contents)
            section_output = section_output | data
            

        i += 1
    
    # print(section_output)
    return section_output


if __name__ == '__main__':
    # formatting arxiv stuff
    arxiv_dict = retrieve_data_from_gcs("arxiv_papers")
    arxiv_titles = arxiv_dict.keys()
    df_arxiv = pd.DataFrame(arxiv_dict)
    transposed_df_arxiv = df_arxiv.T
    transposed_df_arxiv['Title'] = arxiv_titles
    arxiv_columns = ['Title', 'Published', 'Summary', 'Link']




    # print(df_arxiv.T)

    st.title(f"Scraped Data!!")

    st.dataframe(
        transposed_df_arxiv[arxiv_columns],
        hide_index=True,
        column_config={"Link": st.column_config.LinkColumn()},
        width='stretch')
    # retrieve_data_from_gcs("arxiv_papers")
    # retrieve_data_from_gcs("arxiv_papers")
