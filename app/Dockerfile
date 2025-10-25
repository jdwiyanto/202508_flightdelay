# app/Dockerfile

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . . 

RUN pip3 install -r requirements.txt

EXPOSE $PORT

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
