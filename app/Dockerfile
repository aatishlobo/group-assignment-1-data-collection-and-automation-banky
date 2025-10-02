FROM continuumio/miniconda3

WORKDIR /streamlit

# Copy everything
COPY * .

RUN conda env create -f environment.yml

# expose port 8501
EXPOSE 8501

CMD ["conda", "run", "--no-capture-output", "-n", "banky-app", "streamlit", "run", "main.py", "--server.address", "0.0.0.0"]