#!/bin/bash

# Learn App - Setup Script
# =========================
# This script sets up the application for first-time use

set -e

echo "🚀 Setting up Learn App..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Create environment files if they don't exist
echo "📝 Setting up environment files..."

if [ ! -f backend/.env ]; then
    if [ -f backend/.env.example ]; then
        cp backend/.env.example backend/.env
        echo "✅ Created backend/.env from .env.example"
    else
        echo "⚠️  backend/.env.example not found, skipping"
    fi
else
    echo "✅ backend/.env already exists"
fi

if [ ! -f frontend/.env.local ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
    echo "✅ Created frontend/.env.local"
else
    echo "✅ frontend/.env.local already exists"
fi

echo ""
echo "🐳 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for database to be ready..."
sleep 10

echo ""
echo "🗄️  Running database migrations..."
docker-compose exec -T backend alembic upgrade head || echo "⚠️  Migrations may have already been applied"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📚 Next steps:"
echo "   1. Visit http://localhost:3000 to access the application"
echo "   2. Register a new account"
echo "   3. Check backend logs for verification link (if SMTP not configured)"
echo ""
echo "🛠️  Useful commands:"
echo "   ./start.sh  - Start all services"
echo "   ./stop.sh   - Stop all services"
echo "   docker-compose logs -f  - View logs"
echo ""
