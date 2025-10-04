#!/bin/bash

# Navigate to project root
cd "$(dirname "$0")" || exit 1

echo "🔧 Building all Docker services..."
sudo docker-compose build

echo "🚀 Starting all containers..."
sudo docker-compose up -d

echo "📊 Streaming logs (last 50 lines)..."
sudo docker-compose logs -f --tail=50
