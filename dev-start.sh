#!/bin/bash

# Local Development Start Script
# ===============================
# Start backend and frontend locally without Docker

set -e

echo "🚀 Starting Learn App (Local Development Mode)..."
echo ""

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "⚠️  PostgreSQL is not running on port 5432"
    echo "   Starting PostgreSQL..."
    brew services start postgresql@14 2>/dev/null || brew services start postgresql 2>/dev/null || {
        echo "❌ Could not start PostgreSQL. Please start it manually."
        exit 1
    }
    sleep 3
fi

echo "✅ PostgreSQL is running"
echo ""

# Create logs directory
mkdir -p logs

# Start Backend
echo "🐍 Starting Backend (FastAPI)..."
cd backend

if [ ! -d "venv" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

if [ ! -f "venv/bin/uvicorn" ]; then
    echo "   Installing dependencies..."
    pip install -r requirements.txt > /dev/null
fi

echo "   Running database migrations..."
alembic upgrade head 2>/dev/null || echo "   Migrations already applied"

echo "   Starting uvicorn server on port 8000..."
python -m uvicorn app.main:app --reload --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

cd ..

# Start Frontend
echo ""
echo "⚛️  Starting Frontend (Next.js)..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "   Installing dependencies..."
    npm install > /dev/null
fi

echo "   Starting Next.js dev server on port 3000..."
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

cd ..

# Create logs directory if it doesn't exist
mkdir -p logs

# Save PIDs for stop script
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

echo ""
echo "✅ All services started!"
echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📊 View logs:"
echo "   Backend: tail -f logs/backend.log"
echo "   Frontend: tail -f logs/frontend.log"
echo ""
echo "🛑 Stop services: ./dev-stop.sh"
echo ""
