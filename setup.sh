#!/bin/bash

# Parlant Lifestyle Agent - Quick Start Script

set -e

echo "🚀 Parlant Lifestyle Agent - Setup"
echo "=================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check if service-account.json exists
if [ ! -f "service-account.json" ]; then
    echo "❌ Error: service-account.json not found!"
    echo "   Please add your Google Cloud service account JSON file to the project root."
    exit 1
fi
echo "✓ Service account found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi
echo "✓ Virtual environment ready"

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo "✓ Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "   Please edit .env file with your configuration!"
fi
echo "✓ Environment configured"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Edit .env file with your settings"
echo "  2. Run: python -m app.main"
echo ""
echo "Or use Docker:"
echo "  docker-compose up -d"
echo ""
echo "Access points:"
echo "  - Web UI: http://localhost:8000"
echo "  - Parlant Playground: http://localhost:8800"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
