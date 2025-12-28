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

# Check if port 8000 is already in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "❌ ERROR: Port 8000 is already in use!"
    echo "   Process using port 8000:"
    lsof -Pi :8000 -sTCP:LISTEN | grep -v COMMAND
    echo ""
    echo "   Run './dev-stop.sh' or kill the process manually:"
    echo "   kill \$(lsof -ti:8000)"
    cd ..
    exit 1
fi

echo "   Starting uvicorn server on port 8000..."
python -m uvicorn app.main:app --reload --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait and verify backend started successfully
sleep 2
if ! ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo "❌ ERROR: Backend failed to start on port 8000"
    echo "   Check logs for details: tail -20 logs/backend.log"
    echo ""
    echo "   Last 10 lines of backend log:"
    tail -10 ../logs/backend.log
    cd ..
    exit 1
fi

# Verify backend is responding
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "⚠️  WARNING: Backend started but not responding on port 8000"
    echo "   It may still be initializing. Check logs: tail -f logs/backend.log"
fi

cd ..

# Start Frontend
echo ""
echo "⚛️  Starting Frontend (Next.js)..."
cd frontend

# Check if port 3000 is already in use
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "❌ ERROR: Port 3000 is already in use!"
    echo "   Process using port 3000:"
    lsof -Pi :3000 -sTCP:LISTEN | grep -v COMMAND
    echo ""
    echo "   Kill the backend process and the conflicting process:"
    echo "   kill $BACKEND_PID \$(lsof -ti:3000)"
    kill $BACKEND_PID 2>/dev/null
    cd ..
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "   Installing dependencies..."
    npm install > /dev/null
fi

echo "   Starting Next.js dev server on port 3000..."
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

# Wait and verify frontend started successfully
sleep 3
if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
    echo "❌ ERROR: Frontend failed to start on port 3000"
    echo "   Check logs for details: tail -20 logs/frontend.log"
    echo ""
    echo "   Last 10 lines of frontend log:"
    tail -10 ../logs/frontend.log
    echo ""
    echo "   Stopping backend..."
    kill $BACKEND_PID 2>/dev/null
    cd ..
    exit 1
fi

cd ..

# Create logs directory if it doesn't exist
mkdir -p logs

# Save PIDs for stop script
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

echo ""
echo "✅ All services started successfully!"
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
