FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from backend folder into /app
COPY backend/ .

# Hugging Face uses port 7860
EXPOSE 7860

# Shell form allows the $PORT variable to be read
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}