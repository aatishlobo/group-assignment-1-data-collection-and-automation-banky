## data collection requirements

Goal: Build the foundation for automated
data acquisition.
• Requirements:
o Project Description (Extension of Phase 1)
o Title & Problem Statement: Define the
central research/analysis question.
o Data Sources and Integration Goal
o Write scripts that collect and clean data
from your chosen sources.
o Handle errors and logging (e.g., retry failed
API calls, log scraper errors).
o Use crontab (or equivalent) to schedule
recurring collection.
o Store raw + processed data (e.g., in local
storage, SQLite, or cloud bucket).
o Containerize the pipeline using Docker.
• Deliverables:
o Code Repository (GitHub Classroom):
o .py scripts for each data source.
o .py showing Unified ETL pipeline
(integrating sources).
o Cron job configuration file.
o Dockerfile
o Documentation (README):
• Setup instructions (local +
containerized).
• Description of each data source and
how it’s processed.
o Demo: Record a video to show that cron job
runs and updates dataset automatically.
6
