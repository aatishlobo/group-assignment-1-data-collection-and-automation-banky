FROM continuumio/miniconda3

WORKDIR /app

# Copy environment file from parent directory
COPY environment.yml .

# Create conda environment
RUN conda env create -f environment.yml

# Copy all Python files and dependencies
COPY *.py .
COPY .env .

# Create directory for mounted service account key
RUN mkdir -p /app

# Expose port
EXPOSE 8000

# Run FastAPI using the correct environment name from environment.yml
CMD ["conda", "run", "--no-capture-output", "-n", "banky-data-collection", "fastapi", "run", "fastapi.py", "--host", "0.0.0.0", "--port", "8000"]