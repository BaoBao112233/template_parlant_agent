#!/bin/bash
set -e

echo "🚀 Starting Parlant Lifestyle Agent..."

# Start Parlant Server in background on port 8800
echo "📡 Starting Parlant Server on port 8800..."
parlant serve --port 8800 --host 0.0.0.0 &
PARLANT_PID=$!

# Wait a bit for Parlant Server to initialize
sleep 5

# Start FastAPI server on port 8000
echo "🌐 Starting FastAPI server on port 8000..."
python -m app.main

# If FastAPI exits, kill Parlant Server
kill $PARLANT_PID 2>/dev/null || true
