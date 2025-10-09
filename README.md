# State of AI/ML Industry – Data Pipeline Project

## Project Overview

This project explores the state of the AI/ML industry by collecting, analyzing, and integrating data from multiple sources. The goal is to build a fully automated, containerized pipeline that continuously scrapes and processes data, stores it in Google Cloud Platform (GCP), and makes it available for downstream analysis.

By leveraging sources like arXiv (academic research papers) and web/Reddit articles, we aim to capture both the research trends (cutting-edge ML categories, volume of publications, author activity) and community discussions (relative popularity of topics over time). Together, these data streams provide a more complete view of the current AI/ML landscape.

This project is a work in progress, developed by team members Aatish Lobo, Borna Karimi, Jade Tseng, Kayvan Zahiri, and Niki Naderzad.

## Goals

* Gain hands-on experience in data collection, integration, automation, and cloud deployment.
* Build a unified ETL pipeline combining multiple sources.
* Automate collection with cron jobs.
* Deploy pipeline using Docker and host processed data on GCP.

## Data Sources

### 1. arXiv (Research Papers)

* Uses the [arXiv API](https://arxiv.org/help/api) to fetch metadata about the most recent AI/ML papers.
* Extracted fields include: Title, Authors, Publication date, Abstract summary, Link to full paper.
* Example analyses: how many papers are published over time, category-level distribution (e.g., NLP, agents, evaluation, computer vision), author trends.

### 2. Medium + Web Articles

* Scrapes articles from Medium.com and related sources using Google Custom Search API.
* Cleans raw text using BeautifulSoup.
* Stored in GCS as JSON files with metadata.
* Example analyses: popularity of AI-related articles over time, distribution of sources and topics.

### 3. Reddit (planned)

* r/MachineLearning subreddit (and possibly related communities).
* Track: number of posts per week, categories/topics of discussion, topic popularity shifts over time.

## Technical Implementation

### Code Structure

* `user_define_project.py` – Stores environment variables and constants (API keys, GCP paths, etc.).
* `extract_save_data_project.py` – FastAPI app handling scraping, API calls, and saving data to GCS.
* `call_fast_apiproject.py` – Calls the FastAPI endpoints to trigger scraping and uploading.
* `arxiv_scraper.py` – Fetches ML-related research papers from arXiv and uploads structured data to GCS.

### Tools & Libraries

* Python (requests, BeautifulSoup, arxiv, FastAPI, dotenv)
* Google Cloud Platform (GCS) for storage
* Crontab for automation
* Docker for containerization

## Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Environment Variables

Create `.env.project` with the following:

```env
PROJECT_ID=your-gcp-project
GCP_BUCKET_NAME=your-bucket-name
GCP_SERVICE_ACCOUNT_KEY=/path/to/service_account.json
API_KEY=your-google-api-key
SEARCH_ENGINE_ID=your-search-engine-id
API_SERVICE_URL=http://localhost:8000
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

Start the FastAPI server:

```bash
uvicorn extract_save_data_project:app --reload
```

Trigger scraping:

```bash
python call_fast_apiproject.py
```

Run arXiv scraper:

```bash
python arxiv_scraper.py
```

### 5. Automate with Cron

Example cron job to run every day at midnight:

```bash
0 0 * * * /usr/bin/python3 /path/to/call_fast_apiproject.py >> /var/log/cron_ai_pipeline.log 2>&1
```

### 6. Containerization with Docker

Build and run container:

```bash
docker build -t ai-ml-pipeline .
docker run -p 8000:8000 ai-ml-pipeline
```

## Deliverables

* `.py` scripts for each data source
* Unified ETL pipeline script
* Cron job configuration
* `Dockerfile`
* Documentation (README)
* Demo video showing automation and updates

## Status

* Article scraping pipeline (Google Custom Search + Medium)
* arXiv data collection
* Reddit integration (work in progress)
* Unified ETL pipeline (work in progress)
* Dockerization and automation (work in progress)

## Team

* Aatish Lobo
* Borna Karimi
* Kayvan Zaheri
* Niki Naderzad
* Yu (Jade) Tseng
