#!/bin/bash
# Start Philosopher AI Backend Server

echo "🧠 Starting Philosopher AI Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv_philosopher" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv_philosopher
fi

# Activate virtual environment
source venv_philosopher/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r philosopher_ai_requirements.txt

# Load environment variables
if [ -f ".env.philosopher" ]; then
    export $(cat .env.philosopher | xargs)
fi

echo ""
echo "✅ Backend ready!"
echo ""
echo "🚀 Starting server on http://localhost:5000"
echo ""

# Start server
python3 PHILOSOPHER_AI_BACKEND.py
