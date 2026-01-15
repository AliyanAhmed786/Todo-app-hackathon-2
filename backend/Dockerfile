FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

# Add this line to run from the app directory with proper path
CMD ["python", "-c", "import sys; sys.path.insert(0, '/app'); import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=7860)"]