#!/bin/bash
set -e

echo "🚀 Bootstrapping Uploader Stack..."

# Base folders
BASE_DIR="./uploader"
SERVICES=(contentgen seo utm indexing backlinking analytics upload website)

mkdir -p $BASE_DIR/services
cd $BASE_DIR

# Create requirements.txt
cat > requirements.txt <<EOL
fastapi==0.111.1
uvicorn==0.37.0
python-multipart>=0.0.7
pydantic==2.7.0
httpx==0.28.1
jinja2==3.1.6
EOL

# Create Dockerfiles and main.py for Python services
for SERVICE in "${SERVICES[@]}"; do
  mkdir -p services/$SERVICE

  if [ "$SERVICE" != "website" ]; then
    cat > services/$SERVICE/Dockerfile <<EOL
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \\
    apt-get install -y --no-install-recommends build-essential libpq-dev && \\
    rm -rf /var/lib/apt/lists/*

COPY ../../requirements.txt .

RUN pip install --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOL

    cat > services/$SERVICE/main.py <<EOL
from fastapi import FastAPI

app = FastAPI(title="$SERVICE Service")

@app.get("/")
def read_root():
    return {"status": "ok", "service": "$SERVICE"}
EOL

  else
    # Website service
    cat > services/$SERVICE/Dockerfile <<EOL
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOL

    cat > services/$SERVICE/index.html <<EOL
<!DOCTYPE html>
<html>
<head>
    <title>Uploader Website</title>
</head>
<body>
    <h1>Welcome to Uploader Stack</h1>
    <p>All services running!</p>
</body>
</html>
EOL
  fi
done

# Create docker-compose.yml
cat > docker-compose.yml <<EOL
version: '3.9'

services:
  contentgen:
    build: ./services/contentgen
    container_name: contentgen
    networks:
      - blognet

  seo:
    build: ./services/seo
    container_name: seo
    depends_on:
      - contentgen
    networks:
      - blognet

  utm:
    build: ./services/utm
    container_name: utm
    depends_on:
      - seo
    networks:
      - blognet

  indexing:
    build: ./services/indexing
    container_name: indexing
    depends_on:
      - utm
    networks:
      - blognet

  backlinking:
    build: ./services/backlinking
    container_name: backlinking
    depends_on:
      - indexing
    networks:
      - blognet

  analytics:
    build: ./services/analytics
    container_name: analytics
    depends_on:
      - backlinking
    networks:
      - blognet

  upload:
    build: ./services/upload
    container_name: upload
    depends_on:
      - analytics
    networks:
      - blognet
    ports:
      - "8001:8000"

  website:
    build: ./services/website
    container_name: website
    depends_on:
      - upload
    ports:
      - "8080:80"
    networks:
      - blognet

networks:
  blognet:
    driver: bridge
EOL

echo "✅ Bootstrap complete! To launch all services:"
echo "cd $BASE_DIR && sudo docker-compose up --build -d"
