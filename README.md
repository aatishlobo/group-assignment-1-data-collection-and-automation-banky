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
fastapi dev extract_save_data_project:app --reload
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

### 6. Containerization and Deployment

This project includes three containerized components:

1. **Cron container** – runs automated scraping tasks (located in `crontab/`)
2. **Streamlit frontend** – dashboard visualization interface (located in `app/`)
3. **FastAPI backend** – handles data extraction and upload to GCS (located in `datasources/`)

Each container can be built, tested locally, and pushed to Docker Hub for deployment.

---

#### 6.1 Authenticate with Docker Hub

Before building images, log in to Docker Hub:

```bash
docker login

```
Enter your Docker Hub username and personal access token (or password).

#### 6.2 Build Images Locally

From the project root directory, run the following commands to build all three images.
Each is explicitly set to build for the linux/amd64 platform (required for Google Cloud Run

# Cron container (located in crontab/)
```
docker build --platform linux/amd64 -t username/banky-cron:latest -f crontab/Dockerfile .
```
# Streamlit frontend (located in app/)
```
docker build --no-cache --platform linux/amd64 -t username/banky-streamlit:latest -f app/Dockerfile .
```
# FastAPI backend (located in datasources/)
```
docker build --platform linux/amd64 -t username/banky-fastapi:latest -f datasources/Dockerfile .
```
These commands create three reproducible Docker images on your local system.

#### 6.3 Test Containers Locally (Optional)

You can test each container before pushing:

# Streamlit frontend
```
docker run -p 8501:8501 bornakarimi/banky-streamlit:latest
```
# FastAPI backend
```
docker run -p 8000:8000 bornakarimi/banky-fastapi:latest
```
# Cron container (manual execution)
```
docker run bornakarimi/banky-cron:latest
```
Access the local URLs:

Streamlit: http://localhost:8501

FastAPI: http://localhost:8000/docs

#### 6.4 Push Images to Docker Hub

Once verified, push each image to your Docker Hub repository:
```
docker push username/banky-cron:latest

docker push username/banky-streamlit:latest

docker push username/banky-fastapi:latest
```
After pushing, all three containers will appear on your Docker Hub account under the corresponding tags.

#### 6.5 Notes on Reproducibility

Every image build includes the --platform linux/amd64 flag to ensure compatibility with Google Cloud Run.

Dependencies for each image are defined by their respective Dockerfile and environment.yml (if applicable).

Rebuilding and pushing these images from any system reproduces identical containers.

To update a container, rebuild it with a new tag (e.g., :v2) and push again.

#### 6.6 Next Steps: Deploy to Google Cloud Run

Instructions for guiding reproducibility of this were not expected in the deliverables of this project, but this was part of our project.

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
* Unified ETL pipeline
* Dockerization and automation
* Google Cloud Run Publish

## Team

* Aatish Lobo
* Borna Karimi
* Kayvan Zaheri
* Niki Naderzad
* Yu (Jade) Tseng
