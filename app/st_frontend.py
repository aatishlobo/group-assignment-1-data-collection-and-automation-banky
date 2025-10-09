# streamlit frontend
import re
from io import StringIO
import textwrap
import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from google.oauth2 import service_account
from google.cloud import storage
from user_definition import *
from gcs_utils import *
from gemini_summary import *


def retrieve_data_from_gcs(folder_prefix):
    credentials = service_account.Credentials.from_service_account_file(service_account_file_path)
    client = storage.Client(project=project_id, credentials=credentials)
    print("client built")
    bucket = client.bucket(bucket_name)
    print("bucket found")

    blobs = bucket.list_blobs(prefix=folder_prefix)
    print("buckets listed")

    if folder_prefix == "arxiv_papers":
        section_output = {}
    else:
        section_output = []

    for blob in blobs:
        print(blob.name)
        if blob.name.endswith('/'):
            continue

        if folder_prefix != "anthropic-ei":
            try:
                file_contents = blob.download_as_text()
                if not file_contents.strip():
                    print(f"Skipping empty file: {blob.name}")
                    continue
                data = json.loads(file_contents)
            except Exception as e:
                print(f"Skipping invalid or unreadable file {blob.name}: {e}")
                continue

        if folder_prefix == "arxiv_papers":
            if isinstance(data, dict):
                section_output = section_output | data
            else:
                print(f"Unexpected data type in {blob.name}: {type(data)}")
        elif folder_prefix == "medium_ai":
            filename = blob.name.split("/")[-1]
            if isinstance(data, dict):
                if "articles" in data:
                    batch = {**data, "bucket_file": filename}
                    section_output.append(batch)
                else:
                    print(f"Skipping blob {blob.name}: dict without 'articles'")
            elif isinstance(data, list):
                section_output.append({"bucket_file": filename, "articles": data})
            else:
                print(f"Skipping blob {blob.name}: unrecognized data type {type(data)}")
        elif folder_prefix == "anthropic-ei":
            print(blob.name)
            file_name = "/aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv"

            # /aei_raw_claude_ai_2025-08-04_to_2025-08-11.csv
            if blob.name == folder_prefix + file_name:
                csv_data = blob.download_as_text()
                df = pd.read_csv(StringIO(csv_data))

                # raw = blob.download_as_bytes()
                # df = pd.read_csv(io.BytesIO(raw))

                values_to_drop = ['none', 'not_classified']
                df = df.dropna(subset=['cluster_name'])
                df = df[~df['cluster_name'].isin(values_to_drop)]
                
                return df

    return section_output


def filter_medium_articles(data):
    datasets = data if isinstance(data, list) else [data]
    out = []
    for d in datasets:
        articles = d.get("articles", [])
        filtered = [a for a in articles if "medium.com" in a.get("url", "")]
        if filtered:
            base = {k: v for k, v in d.items() if k != "articles"}
            out.append({**base, "articles": filtered})
    return out


def _extract_date_from_bucket_file(bucket_file):
    digits = "".join(ch for ch in (bucket_file or "") if ch.isdigit())
    if len(digits) >= 8:
        d = digits[:8]
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}"
    return None


def flatten_medium_articles(data):
    datasets = data if isinstance(data, list) else [data]
    rows = []
    for d in datasets:
        published = _extract_date_from_bucket_file(d.get("bucket_file", ""))
        for a in d.get("articles", []):
            rows.append({
                "Title": a.get("title"),
                "Published": published,
                "Summary": a.get("content"),
                "Link": a.get("url"),
            })
    df = pd.DataFrame(rows, columns=["Title", "Published", "Summary", "Link"])
    df = df.drop_duplicates(subset="Title", keep="first").reset_index(drop=True)
    return df


if __name__ == '__main__':
    st.title("Scraped Data")

    arxiv_dict = retrieve_data_from_gcs("arxiv_papers")
    arxiv_titles = arxiv_dict.keys()
    df_arxiv = pd.DataFrame(arxiv_dict).T
    df_arxiv["Title"] = arxiv_titles
    df_arxiv = df_arxiv[["Title", "Published", "Summary", "Link"]]
    df_arxiv["Source"] = "Arxiv"

    batches = retrieve_data_from_gcs("medium_ai")
    filtered = filter_medium_articles(batches)
    df_medium = flatten_medium_articles(filtered)
    df_medium["Source"] = "Medium"

    df_anthropic = retrieve_data_from_gcs("anthropic-ei")
    df_anthropic = pd.DataFrame(df_anthropic)

    st.sidebar.header("Select Data Sources")
    show_arxiv = st.sidebar.checkbox("Arxiv Papers", value=True)
    show_medium = st.sidebar.checkbox("Medium Articles", value=True)
    show_ant = st.sidebar.checkbox("Anthropic Articles", value=True)

    combined_df = pd.DataFrame(columns=["Title", "Published", "Summary", "Link", "Source"])
    if show_arxiv:
        combined_df = pd.concat([combined_df, df_arxiv], ignore_index=True)
    if show_medium:
        combined_df = pd.concat([combined_df, df_medium], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset="Title", keep="first").reset_index(drop=True)

    if combined_df.empty:
        st.warning("No data selected.")
    else:
        st.dataframe(
            combined_df,
            hide_index=True,
            column_config={"Link": st.column_config.LinkColumn()},
            width='stretch'
        )

        combined_df["Published"] = pd.to_datetime(combined_df["Published"], errors="coerce")
        counts = combined_df.groupby(["Published", "Source"]).size().unstack(fill_value=0)
        counts = counts.sort_index()

        fig, ax = plt.subplots(figsize=(8, 4))
        counts.plot(ax=ax, marker="o")
        ax.set_title("Articles per Date by Source")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Articles")
        ax.grid(True, linestyle="--", alpha=0.6)
        plt.xticks(rotation=45)
        st.pyplot(fig)

if show_ant:
    cluster_counts = df_anthropic['cluster_name'].value_counts()
    cluster_counts = cluster_counts[cluster_counts.index.str.len() < 30]
    top_clusters = cluster_counts.head(20)
    # wrap labels to 15 characters per line
    wrapped_labels = [textwrap.fill(label, 15) for label in top_clusters.index]

    fig1, ax1 = plt.subplots(figsize=(8,8))
    top_clusters.plot(kind='barh', ax=ax1)
    ax1.set_yticklabels(wrapped_labels, fontsize=8)
    ax1.set_title("Anthropic Articles Topic Frequency")
    ax1.set_ylabel("Topic")
    ax1.set_xlabel("Number of Articles")
    
    
    # fig1, ax1 = plt.subplots()
    

    st.pyplot(fig1)
