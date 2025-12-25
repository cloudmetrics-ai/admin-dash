#!/bin/bash

# Local Development Setup Script
# ===============================
# One-time setup for local development without Docker

set -e

echo "🚀 Setting up Learn App for Local Development..."
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js $(node --version)"

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL is not installed. Please install PostgreSQL 14+"
    exit 1
fi
echo "✅ PostgreSQL installed"

echo ""

# Setup Backend
echo "🐍 Setting up Backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
echo "   Installing Python dependencies..."
pip install -q -r requirements.txt

# Setup database
echo "   Setting up database..."
if psql -h localhost -U postgres -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw admin_dashboard; then
    echo "   ✅ Database 'admin_dashboard' already exists"
else
    echo "   Creating database..."
    if createdb -h localhost -U postgres admin_dashboard 2>/dev/null; then
        echo "   ✅ Database created successfully"
    else
        echo "   ⚠️  Could not create database. It may already exist."
        echo "      If needed, create manually: createdb -h localhost -U postgres admin_dashboard"
    fi
fi

# Return to project root for migrations
cd ..

# Run migrations
echo "   Running database migrations..."
if [ -f "alembic.ini" ]; then
    if alembic upgrade head 2>/dev/null; then
        echo "   ✅ Migrations applied successfully"
    else
        echo "   ⚠️  Migrations skipped (run manually if needed: alembic upgrade head)"
    fi
else
    echo "   ⚠️  No alembic.ini found - database should already be set up"
fi

# Setup Frontend
echo ""
echo "⚛️  Setting up Frontend..."
cd frontend

# Install dependencies
echo "   Installing Node dependencies..."
npm install

cd ..

# Create logs directory
mkdir -p logs

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "   1. Start services: ./dev-start.sh"
echo "   2. Access frontend: http://localhost:3000"
echo "   3. Access backend: http://localhost:8000/docs"
echo ""
echo "🛠️  Useful commands:"
echo "   ./dev-start.sh  - Start all services"
echo "   ./dev-stop.sh   - Stop all services"
echo ""
