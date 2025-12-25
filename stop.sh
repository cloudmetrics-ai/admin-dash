#!/bin/bash

# Learn App - Stop Script
# ========================
# Stop all Docker services

set -e

echo "🛑 Stopping Learn App services..."
docker-compose down

echo ""
echo "✅ Services stopped successfully!"
echo ""
echo "🚀 Start services again: ./start.sh"
echo "🗑️  Remove all data: docker-compose down -v"
echo ""
