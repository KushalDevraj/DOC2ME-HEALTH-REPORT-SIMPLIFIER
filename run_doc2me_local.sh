#!/bin/bash

# Kill any existing processes on ports 8000 and 5001
lsof -ti :8000 | xargs kill -9 2>/dev/null
lsof -ti :5001 | xargs kill -9 2>/dev/null

echo "Starting Backend (FastAPI)..."
cd "$(dirname "$0")/backend"
# Use the local venv if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
# Run backend in background
uvicorn main:medicalsearch --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID"

echo "Starting Frontend (Flask)..."
cd "../frontend"
# Use the local venv if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
# Run frontend in background
python3 main.py > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started with PID $FRONTEND_PID"

echo "Waiting for services to warm up..."
sleep 10

echo "Checking Backend health..."
curl -s http://localhost:8000/ > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Backend is UP"
else
    echo "❌ Backend FAILED to start. Check backend.log"
fi

echo "Checking Frontend health..."
curl -s http://localhost:5001/ > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Frontend is UP"
else
    echo "❌ Frontend FAILED to start. Check frontend.log"
fi

echo "Startup process complete."
