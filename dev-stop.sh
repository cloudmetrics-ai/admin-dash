#!/bin/bash

# Local Development Stop Script
# ==============================
# Stop backend and frontend local services

set -e

echo "🛑 Stopping Learn App (Local Development Mode)..."
echo ""

# Stop Backend
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "🐍 Stopping Backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID 2>/dev/null || true
        rm logs/backend.pid
    else
        echo "⚠️  Backend process not found"
        rm logs/backend.pid 2>/dev/null || true
    fi
else
    echo "⚠️  No backend PID file found, trying pkill..."
    pkill -f "uvicorn app.main:app" 2>/dev/null || true
fi

# Stop Frontend
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "⚛️  Stopping Frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID 2>/dev/null || true
        rm logs/frontend.pid
    else
        echo "⚠️  Frontend process not found"
        rm logs/frontend.pid 2>/dev/null || true
    fi
else
    echo "⚠️  No frontend PID file found, trying pkill..."
    pkill -f "npm run dev" 2>/dev/null || pkill -f "next dev" 2>/dev/null || true
fi

echo ""
echo "✅ Services stopped!"
echo ""
echo "🚀 Start services again: ./dev-start.sh"
echo ""
