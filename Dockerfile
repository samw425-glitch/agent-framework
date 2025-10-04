# Use official Python slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files

# copy python dependencies


# copy app files
COPY main.py .
COPY routes.py .
COPY generate_html.py .
COPY tracker.py .
COPY uploader.py .

# copy directories
COPY services/ ./services/
COPY static/ ./static/
COPY config/ ./config/



# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
