#!/bin/bash

# Learn App - Start Script
# =========================
# Start all Docker services

set -e

echo "🚀 Starting Learn App services..."
docker-compose up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop services: ./stop.sh"
echo ""
